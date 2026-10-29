//! Walks between a feed's platforms through its `pathways.txt`:
//! the quickest from each served stop to every other it reaches,
//! by Dijkstra over every station's pathways at once,
//! so a walk can run from one station to another, as through a shared concourse.

use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap, HashMap};

use crate::gtfs::{Feed, Pathway, Secs};
use crate::timetable::{StopIdx, Timetable, WALK_SPEED};

/// Walking on the level, in meters a second: 3 mph.
/// Slower than `WALK_SPEED`, which allows for stairs on the way.
pub const LEVEL_WALK_SPEED: f64 = 1.34112;
/// Seconds a step, up or down: a guess, as no source gives one.
pub const STEP_SECS: f64 = 0.6;
/// An elevator without a `traversal_time`: waiting for it, and riding.
pub const ELEVATOR_SECS: Secs = 60;
/// A fare or exit gate without one.
pub const GATE_SECS: Secs = 5;
/// A pathway with neither a time nor anything to estimate one from.
pub const UNKNOWN_SECS: Secs = 30;
/// No walk is longer than this on foot, fare gate penalty aside:
/// a transfer that long is no transfer.
pub const MAX_WALK: Secs = 20 * 60;

/// The quickest walk from one served stop to another,
/// counting a fare gate's penalty in choosing it, not in `secs`.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Walk {
    pub from: StopIdx,
    pub to: StopIdx,
    /// Its time on foot: 0 for a walk over walkways alone within a station,
    /// across one platform, as an island's two sides.
    pub secs: Secs,
    /// Times out of the paid area through the gates and back in.
    pub exits: u8,
}

/// What reading `pathways.txt` found.
#[derive(Debug, Default)]
pub struct Report {
    pub pathways: usize,
    /// Boarding areas (`location_type` 4), each taken as its platform.
    pub boarding_areas: usize,
    /// Pathways with no `traversal_time`, so estimated, by mode.
    pub estimated: BTreeMap<u8, usize>,
    /// Of those, ones with nothing to estimate from, so `UNKNOWN_SECS`.
    pub unknown: usize,
    /// Served stops a pathway starts or ends at.
    pub stops: usize,
    /// Those stops, which `Timetable::use_pathways` takes pathways' word on.
    pub covered: Vec<StopIdx>,
    /// Pairs of one station's covered stops with no walk between them
    /// within `max_walk`, so no footpath.
    pub unreached: usize,
    pub walks: usize,
    /// Walks over walkways alone within a station, so free.
    pub level_walks: usize,
    /// Walks out through the fare gates and back in.
    pub exit_walks: usize,
}

/// A pathway's time, and whether it's estimated, and whether from nothing.
fn traversal(p: &Pathway) -> (Secs, bool, bool) {
    if let Some(t) = p.traversal_time {
        return (t, false, false);
    }
    let at = |speed: f64| p.length.map(|m| (m / speed).round() as Secs);
    let by_length = at(LEVEL_WALK_SPEED);
    let estimate = match p.pathway_mode {
        // Stairs with no count, by their length at the pace allowing for stairs.
        2 => p
            .stair_count
            .map(|n| (f64::from(n.unsigned_abs()) * STEP_SECS).round() as Secs)
            .or(at(WALK_SPEED)),
        5 => Some(ELEVATOR_SECS),
        6 | 7 => Some(GATE_SECS),
        _ => by_length,
    };
    match estimate {
        Some(t) => (t, true, false),
        None => (UNKNOWN_SECS, true, true),
    }
}

/// Walkways and moving walkways: on one level.
/// Two of a station's platforms on one level are one platform,
/// since getting from one to another not of it means crossing tracks.
fn is_level(mode: u8) -> bool {
    matches!(mode, 1 | 3)
}

/// A fare gate into the paid area, and an exit gate out of it.
const FARE_GATE: u8 = 6;
const EXIT_GATE: u8 = 7;

/// The quickest walks between `tt`'s served stops through `feed`'s pathways,
/// each chosen by its time plus `gate_penalty` for going out and back in,
/// none over `max_walk` on foot (`MAX_WALK`).
/// The cheapest way to a node over `max_walk` hides a dearer one under it,
/// which only matters for walks near it.
pub fn walks(
    feed: &Feed,
    tt: &Timetable,
    gate_penalty: Secs,
    max_walk: Secs,
) -> (Vec<Walk>, Report) {
    let mut report = Report {
        pathways: feed.pathways.len(),
        ..Report::default()
    };
    let boarding_areas: HashMap<&str, &str> = feed
        .stops
        .iter()
        .filter(|s| s.location_type == Some(4))
        .filter_map(|s| Some((s.stop_id.as_str(), s.parent_station.as_deref()?)))
        .collect();
    report.boarding_areas = boarding_areas.len();

    let mut nodes: HashMap<&str, usize> = HashMap::new();
    let mut ends = Vec::with_capacity(feed.pathways.len());
    for p in &feed.pathways {
        let [from, to] = [&p.from_stop_id, &p.to_stop_id].map(|id| {
            let id = boarding_areas.get(id.as_str()).copied().unwrap_or(id);
            let len = nodes.len();
            *nodes.entry(id).or_insert(len)
        });
        ends.push((from, to));
    }
    let mut edges: Vec<Vec<(usize, Secs, u8)>> = vec![Vec::new(); nodes.len()];
    for (p, &(from, to)) in feed.pathways.iter().zip(&ends) {
        let (secs, estimated, unknown) = traversal(p);
        if estimated {
            *report.estimated.entry(p.pathway_mode).or_default() += 1;
        }
        report.unknown += usize::from(unknown);
        edges[from].push((to, secs, p.pathway_mode));
        if p.is_bidirectional == 1 {
            // Back through a fare gate is out through it, no penalty.
            let mode = if p.pathway_mode == FARE_GATE {
                EXIT_GATE
            } else {
                p.pathway_mode
            };
            edges[to].push((from, secs, mode));
        }
    }

    let served: std::collections::HashSet<StopIdx> = tt
        .patterns
        .iter()
        .flat_map(|p| p.stops.iter().copied())
        .collect();
    // Each node's served stops: one, unless a stop was split by platform.
    let mut stops_of: Vec<Vec<StopIdx>> = vec![Vec::new(); edges.len()];
    for (i, stop) in tt.stops.iter().enumerate() {
        let i = i as StopIdx;
        if let Some(&n) = nodes.get(stop.id.as_str())
            && served.contains(&i)
        {
            stops_of[n].push(i);
        }
    }
    report.covered = stops_of.iter().flatten().copied().collect();
    report.covered.sort_unstable();
    report.stops = report.covered.len();

    // Each state's `(cost, secs, exits, level)`, for the current source only,
    // a state being a node, and whether the walk is out of the paid area there,
    // through an exit gate, so a fare gate after is back in (`node * 2 + out`):
    // walking in from a bus stop outside it is no going out and back in.
    // `seen` lists the states set, to reset.
    let mut best: Vec<Option<(Secs, Secs, u8, bool)>> = vec![None; edges.len() * 2];
    let mut seen = Vec::new();
    let mut reached = Vec::new();
    let mut heap = BinaryHeap::new();
    let mut walks = Vec::new();
    for source in 0..edges.len() {
        if stops_of[source].is_empty() {
            continue;
        }
        for state in seen.drain(..) {
            best[state] = None;
        }
        best[source * 2] = Some((0, 0, 0, true));
        seen.push(source * 2);
        heap.push(Reverse((0, source * 2)));
        while let Some(Reverse((cost, state))) = heap.pop() {
            let (at, secs, exits, level) = best[state].expect("set before pushed");
            if cost > at {
                continue;
            }
            let (n, out) = (state / 2, state % 2 == 1);
            for &(to, t, mode) in &edges[n] {
                let back_in = out && mode == FARE_GATE;
                let next_out = match mode {
                    EXIT_GATE => true,
                    FARE_GATE => false,
                    _ => out,
                };
                let next = to * 2 + usize::from(next_out);
                let next_cost = cost + t + if back_in { gate_penalty } else { 0 };
                if secs + t > max_walk || best[next].is_some_and(|(c, ..)| c <= next_cost) {
                    continue;
                }
                if best[next].is_none() {
                    seen.push(next);
                }
                best[next] = Some((
                    next_cost,
                    secs + t,
                    exits + u8::from(back_in),
                    level && is_level(mode),
                ));
                heap.push(Reverse((next_cost, next)));
            }
        }
        // Each node once, its cheapest state.
        reached.clear();
        reached.extend(seen.iter().map(|state| state / 2));
        reached.sort_unstable();
        reached.dedup();
        for &n in &reached {
            let (_, secs, exits, level) = [best[n * 2], best[n * 2 + 1]]
                .into_iter()
                .flatten()
                .min_by_key(|&(cost, ..)| cost)
                .expect("seen");
            for &from in &stops_of[source] {
                // Not between one GTFS stop's copies split by platform:
                // pathways can't tell them apart.
                for &to in stops_of[n].iter().filter(|&&to| !tt.same_stop(from, to)) {
                    let across = level && tt.same_station(from, to);
                    walks.push(Walk {
                        from,
                        to,
                        secs: if across { 0 } else { secs },
                        exits,
                    });
                }
            }
        }
    }
    walks.sort_by_key(|w| (w.from, w.to));
    let walked: std::collections::HashSet<(StopIdx, StopIdx)> =
        walks.iter().map(|w| (w.from, w.to)).collect();
    for &a in &report.covered {
        for &b in &report.covered {
            if !tt.same_stop(a, b) && tt.same_station(a, b) && !walked.contains(&(a, b)) {
                report.unreached += 1;
            }
        }
    }
    report.walks = walks.len();
    report.level_walks = walks.iter().filter(|w| w.secs == 0).count();
    report.exit_walks = walks.iter().filter(|w| w.exits > 0).count();
    (walks, report)
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use jiff::civil::Date;

    use super::*;

    // Alpha: an island, North and South, up the stairs from Upper;
    // Beta, a block away: the street from Alpha's exit, or a long passage.
    const STOPS: &str = "stop_id,stop_name,location_type,parent_station\n\
        A,Alpha,1,\nAN,Alpha North,0,A\nAS,Alpha South,0,A\nAU,Alpha Upper,0,A\n\
        landing,Alpha landing,3,A\nstair,Alpha stair top,3,A\n\
        paid,Alpha paid side,3,A\nstreet,Alpha street,2,A\nAB,Alpha busway,0,A\n\
        B,Beta,1,\nBP,Beta platform,0,B\nbpaid,Beta paid side,3,B\nbstreet,Beta street,2,B\n";
    const CALENDAR: &str = "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
        W,1,1,1,1,1,1,1,20250101,20251231\n";

    fn feed(pathways: &str) -> Feed {
        let files = HashMap::from([
            ("stops.txt", STOPS),
            (
                "trips.txt",
                "route_id,trip_id,service_id\n1,n,W\n1,s,W\n2,u,W\nbus,b,W\n",
            ),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
                 n,AN,08:00:00,08:00:00,1\nn,BP,08:05:00,08:05:00,2\n\
                 s,BP,08:00:00,08:00:00,1\ns,AS,08:05:00,08:05:00,2\n\
                 u,AU,08:00:00,08:00:00,1\nu,BP,08:07:00,08:07:00,2\n\
                 b,AB,08:00:00,08:00:00,1\nb,BP,08:10:00,08:10:00,2\n",
            ),
            ("calendar.txt", CALENDAR),
            ("pathways.txt", pathways),
        ]);
        Feed::load(&mut { files }).unwrap()
    }

    const HEADER: &str = "pathway_id,from_stop_id,to_stop_id,pathway_mode,is_bidirectional,length,traversal_time,stair_count\n";

    fn walks_of(pathways: &str, gate_penalty: Secs) -> (Timetable, Vec<Walk>, Report) {
        let feed = feed(&format!("{HEADER}{pathways}"));
        let tt = Timetable::build(&feed, Date::new(2025, 9, 3).unwrap()).unwrap();
        let (walks, report) = walks(&feed, &tt, gate_penalty, MAX_WALK);
        (tt, walks, report)
    }

    fn walk(tt: &Timetable, walks: &[Walk], from: &str, to: &str) -> Option<(Secs, u8)> {
        let (from, to) = (tt.stop(from).unwrap(), tt.stop(to).unwrap());
        walks
            .iter()
            .find(|w| (w.from, w.to) == (from, to))
            .map(|w| (w.secs, w.exits))
    }

    const ALPHA: &str = "\
        n,AN,landing,1,1,12,,\ns,AS,landing,1,1,12,,\n\
        up,landing,stair,2,1,,,20\nupper,stair,AU,1,1,24,,\n";

    #[test]
    fn across_an_island_is_free_and_stairs_are_estimated() {
        let (tt, walks, report) = walks_of(ALPHA, 600);
        assert_eq!(walk(&tt, &walks, "AN", "AS"), Some((0, 0)));
        // 12 m and 24 m at 3 mph, and 20 steps at 0.6s.
        assert_eq!(walk(&tt, &walks, "AN", "AU"), Some((9 + 12 + 18, 0)));
        assert_eq!(walk(&tt, &walks, "AU", "AS"), Some((18 + 12 + 9, 0)));
        assert_eq!(report.estimated, BTreeMap::from([(1, 3), (2, 1)]));
        assert_eq!((report.stops, report.walks, report.level_walks), (3, 6, 2));
    }

    #[test]
    fn one_way_unless_bidirectional() {
        let (tt, walks, _) = walks_of("n,AN,landing,1,0,12,,\ns,landing,AS,1,0,12,,\n", 600);
        assert_eq!(walk(&tt, &walks, "AN", "AS"), Some((0, 0)));
        assert_eq!(walk(&tt, &walks, "AS", "AN"), None);
    }

    // Out of Alpha's gates, along the street, and in at Beta's: 4 minutes,
    // or along the passage, 6 minutes.
    const TO_BETA: &str = "\
        paid,AU,paid,1,1,,0,\nexit,paid,street,7,0,,5,\n\
        road,street,bstreet,1,1,,215,\nenter,bstreet,bpaid,6,0,,5,\n\
        bplat,bpaid,BP,1,1,,15,\n";
    const PASSAGE: &str = "passage,paid,bpaid,1,1,,345,\n";

    #[test]
    fn out_and_back_in_only_when_worth_the_penalty() {
        let (tt, walks, report) = walks_of(&format!("{ALPHA}{TO_BETA}"), 600);
        // The only way: out and back in, its time on foot alone.
        assert_eq!(walk(&tt, &walks, "AU", "BP"), Some((240, 1)));
        assert_eq!(report.exit_walks, 3);
        // Beta's way back is in: its fare gate only goes in.
        assert_eq!(walk(&tt, &walks, "BP", "AU"), None);

        let (tt, walks, _) = walks_of(&format!("{ALPHA}{TO_BETA}{PASSAGE}"), 600);
        assert_eq!(walk(&tt, &walks, "AU", "BP"), Some((360, 0)));
        // Unless the penalty is under the 2 minutes it saves.
        let (tt, walks, _) = walks_of(&format!("{ALPHA}{TO_BETA}{PASSAGE}"), 60);
        assert_eq!(walk(&tt, &walks, "AU", "BP"), Some((240, 1)));
    }

    #[test]
    fn in_from_outside_is_no_going_out() {
        let bus = "busway,AB,street,1,1,,30,\nfare,street,paid,6,0,,5,\n";
        let (tt, walks, report) = walks_of(&format!("{ALPHA}{TO_BETA}{bus}"), 600);
        assert_eq!(walk(&tt, &walks, "AB", "AU"), Some((35, 0)));
        // Out to the busway is no going back in either.
        assert_eq!(walk(&tt, &walks, "AU", "AB"), Some((35, 0)));
        // But out of Alpha and in at Beta is, from either.
        assert_eq!(walk(&tt, &walks, "AU", "BP"), Some((240, 1)));
        assert_eq!(walk(&tt, &walks, "AB", "BP"), Some((265, 0)));
        assert_eq!(report.exit_walks, 3);
    }

    #[test]
    fn a_penalty_over_the_longest_walk_still_finds_the_way_out_and_in() {
        // Alpha's Upper and its island, both on pathways: walked, no fallback.
        let (mut tt, walks, report) = walks_of(&format!("{ALPHA}{TO_BETA}"), 1200);
        tt.use_pathways(&walks, &report.covered);
        let (au, bp) = (tt.stop("AU").unwrap(), tt.stop("BP").unwrap());
        let path = |a: StopIdx, b: StopIdx| {
            tt.footpaths[a as usize]
                .iter()
                .find(|p| p.0 == b)
                .map(|p| p.1)
        };
        assert_eq!(path(au, bp), Some(240));
        assert_eq!(tt.exits.get(&(au, bp)), Some(&1));
        assert_eq!(report.unreached, 0);
    }

    #[test]
    fn one_station_without_a_way_between_has_no_footpath() {
        // North and South, with no pathway from South: not the station's same-stop time.
        let (mut tt, walks, report) =
            walks_of("n,AN,landing,1,0,12,,\ns,landing,AS,1,0,12,,\n", 600);
        let (an, as_) = (tt.stop("AN").unwrap(), tt.stop("AS").unwrap());
        assert!(tt.footpaths[as_ as usize].iter().any(|p| p.0 == an));
        assert_eq!(report.unreached, 1);
        tt.use_pathways(&walks, &report.covered);
        assert!(!tt.footpaths[as_ as usize].iter().any(|p| p.0 == an));
        assert!(tt.footpaths[an as usize].contains(&(as_, 0)));
    }

    #[test]
    fn pathways_replace_transfers_where_they_reach() {
        let (mut tt, walks, report) = walks_of(&format!("{ALPHA}{TO_BETA}"), 600);
        let (au, bp, an) = (
            tt.stop("AU").unwrap(),
            tt.stop("BP").unwrap(),
            tt.stop("AN").unwrap(),
        );
        assert_eq!(tt.min_change[au as usize], tt.report.default_change);
        tt.use_pathways(&walks, &report.covered);
        assert_eq!(tt.min_change[au as usize], 0);
        let path = |a: StopIdx, b: StopIdx| {
            tt.footpaths[a as usize]
                .iter()
                .find(|p| p.0 == b)
                .map(|p| p.1)
        };
        assert_eq!(path(au, bp), Some(240));
        assert_eq!(path(au, an), Some(39));
        assert_eq!(tt.exits.get(&(au, bp)), Some(&1));
        assert!(!tt.exits.contains_key(&(au, an)));
    }

    /// Floyd–Warshall over every `(node, out)` state:
    /// each pair of served stops' cheapest cost, fare gate penalty included.
    fn reference(feed: &Feed, tt: &Timetable, penalty: Secs) -> HashMap<(StopIdx, StopIdx), Secs> {
        let mut ids: Vec<&str> = feed
            .pathways
            .iter()
            .flat_map(|p| [p.from_stop_id.as_str(), p.to_stop_id.as_str()])
            .collect();
        ids.sort_unstable();
        ids.dedup();
        let n = ids.len() * 2;
        let at = |id: &str| ids.binary_search(&id).unwrap();
        let mut d = vec![vec![Secs::MAX / 4; n]; n];
        for (i, row) in d.iter_mut().enumerate() {
            row[i] = 0;
        }
        for p in &feed.pathways {
            let (t, ..) = traversal(p);
            let mut edges = vec![(at(&p.from_stop_id), at(&p.to_stop_id), p.pathway_mode)];
            if p.is_bidirectional == 1 {
                let back = if p.pathway_mode == FARE_GATE {
                    EXIT_GATE
                } else {
                    p.pathway_mode
                };
                edges.push((at(&p.to_stop_id), at(&p.from_stop_id), back));
            }
            for (a, b, mode) in edges {
                for out in [0, 1] {
                    let next_out = match mode {
                        EXIT_GATE => 1,
                        FARE_GATE => 0,
                        _ => out,
                    };
                    let cost = t + if out == 1 && mode == FARE_GATE {
                        penalty
                    } else {
                        0
                    };
                    let (x, y) = (a * 2 + out, b * 2 + next_out);
                    d[x][y] = d[x][y].min(cost);
                }
            }
        }
        for k in 0..n {
            for i in 0..n {
                for j in 0..n {
                    d[i][j] = d[i][j].min(d[i][k] + d[k][j]);
                }
            }
        }
        let mut costs = HashMap::new();
        for a in 0..tt.stops.len() as StopIdx {
            for b in 0..tt.stops.len() as StopIdx {
                let (Ok(x), Ok(y)) = (
                    ids.binary_search(&tt.stops[a as usize].id.as_str()),
                    ids.binary_search(&tt.stops[b as usize].id.as_str()),
                ) else {
                    continue;
                };
                let cost = d[x * 2][y * 2].min(d[x * 2][y * 2 + 1]);
                if a != b && cost < Secs::MAX / 4 {
                    costs.insert((a, b), cost);
                }
            }
        }
        costs
    }

    #[test]
    fn quickest_walks_match_floyd_warshall() {
        // Random pathways between Alpha's and Beta's platforms and some nodes,
        // from a fixed seed, so a failure reproduces.
        let mut seed: u64 = 0x5eed;
        let mut next = |n: u64| {
            seed = seed
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            (seed >> 33) % n
        };
        let places = [
            "AN", "AS", "AU", "AB", "BP", "landing", "stair", "paid", "street", "bpaid", "bstreet",
        ];
        for _ in 0..200 {
            let mut pathways = String::new();
            for i in 0..12 {
                let from = places[next(places.len() as u64) as usize];
                let to = places[next(places.len() as u64) as usize];
                let mode = [1, 1, 2, 4, 5, 6, 7][next(7) as usize];
                let bidirectional = next(2);
                let time = 1 + next(300);
                pathways += &format!("p{i},{from},{to},{mode},{bidirectional},,{time},\n");
            }
            let penalty = [0, 60, 600][next(3) as usize] as Secs;
            let feed = feed(&format!("{HEADER}{pathways}"));
            let tt = Timetable::build(&feed, Date::new(2025, 9, 3).unwrap()).unwrap();
            let (walks, _) = walks(&feed, &tt, penalty, Secs::MAX / 4);
            let want = reference(&feed, &tt, penalty);
            let got: HashMap<(StopIdx, StopIdx), &Walk> =
                walks.iter().map(|w| ((w.from, w.to), w)).collect();
            assert_eq!(
                got.keys().collect::<std::collections::BTreeSet<_>>(),
                want.keys().collect::<std::collections::BTreeSet<_>>(),
                "{pathways}"
            );
            for (pair, w) in got {
                // A walk across one platform is free, whatever its cost.
                if w.secs != 0 {
                    let cost = w.secs + penalty * Secs::from(w.exits);
                    assert_eq!(cost, want[&pair], "{pair:?} {pathways}");
                }
            }
        }
    }
}
