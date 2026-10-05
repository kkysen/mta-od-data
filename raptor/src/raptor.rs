//! Round-based earliest-arrival RAPTOR (Delling, Pajor, Werneck 2012).
//!
//! Phase 3 of `raptor_design.md`.
//! Round `k` finds journeys of exactly `k` rides,
//! kept only if they arrive earlier than any journey with fewer,
//! so the rounds that reach a stop give its Pareto set over (arrival, rides).
//! Every label has its own backpointer per round,
//! so a journey is always extracted from the round that computed it.

use crate::gtfs::Secs;
use crate::timetable::{StopIdx, Timetable};

/// Most rides in a journey. 3 is `nycriders`' cap, unexamined; raising it is a todo.
pub const MAX_RIDES: usize = 3;

const NEVER: Secs = Secs::MAX;

/// How a stop came to be ready to board from.
#[derive(Clone, Copy, Debug, PartialEq)]
enum Ready {
    Origin,
    /// Alighted here in the same round, then waited out the stop's change time.
    Change,
    /// Walked here from another stop, after alighting there (or from an origin in round 0).
    Walk {
        from: StopIdx,
    },
}

/// How a stop was reached by train.
#[derive(Clone, Copy, Debug, PartialEq)]
struct Ride {
    pattern: u32,
    trip: u32,
    board_pos: u32,
    alight_pos: u32,
}

#[derive(Clone, Debug, PartialEq)]
pub enum Leg {
    Ride {
        pattern: u32,
        trip: u32,
        /// Positions in the pattern's stops, for the stops passed between.
        board_pos: u32,
        alight_pos: u32,
        board_stop: StopIdx,
        alight_stop: StopIdx,
        depart: Secs,
        arrive: Secs,
    },
    Walk {
        from: StopIdx,
        to: StopIdx,
        duration: Secs,
    },
}

#[derive(Clone, Debug, PartialEq)]
pub struct Journey {
    pub depart: Secs,
    pub arrive: Secs,
    pub legs: Vec<Leg>,
}

impl Journey {
    pub fn rides(&self) -> usize {
        self.legs
            .iter()
            .filter(|l| matches!(l, Leg::Ride { .. }))
            .count()
    }
}

/// Per-timetable indices, built once and shared by every query.
pub struct Router<'a> {
    tt: &'a Timetable,
    /// `(pattern, position)` of each stop's every appearance in a pattern.
    stop_patterns: Vec<Vec<(u32, u32)>>,
}

/// Labels per round, kept across runs of one range query.
///
/// A label is only lowered, never reset,
/// so after runs at departures `d1 > d2 > ...`,
/// a label lowered in the run at `d` is a journey leaving at `d`
/// that beats every journey leaving later with no more rides.
pub struct Labels<'a> {
    router: &'a Router<'a>,
    /// The latest run's departure.
    depart: Secs,
    /// `ride_arrival[k][s]`: arriving at `s` on the `k`th ride.
    ride_arrival: Vec<Vec<Secs>>,
    ride_from: Vec<Vec<Option<Ride>>>,
    /// `ready[k][s]`: able to board at `s` after `k` rides.
    ready: Vec<Vec<Secs>>,
    ready_from: Vec<Vec<Option<Ready>>>,
}

impl<'a> Router<'a> {
    pub fn new(tt: &'a Timetable) -> Self {
        let mut stop_patterns = vec![Vec::new(); tt.stops.len()];
        for (p, pattern) in tt.patterns.iter().enumerate() {
            for (pos, &s) in pattern.stops.iter().enumerate() {
                stop_patterns[s as usize].push((p as u32, pos as u32));
            }
        }
        Self { tt, stop_patterns }
    }

    pub fn labels(&self) -> Labels<'_> {
        let n = self.tt.stops.len();
        let rounds = MAX_RIDES + 1;
        Labels {
            router: self,
            depart: NEVER,
            ride_arrival: vec![vec![NEVER; n]; rounds],
            ride_from: vec![vec![None; n]; rounds],
            ready: vec![vec![NEVER; n]; rounds],
            ready_from: vec![vec![None; n]; rounds],
        }
    }

    /// Every stop's earliest arrivals from `origins`, leaving at `depart`.
    pub fn query(&self, origins: &[StopIdx], depart: Secs) -> Labels<'_> {
        let mut labels = self.labels();
        labels.run(origins, depart);
        labels
    }

    /// Every time in `[from, until)` a journey from `origins` can start
    /// by boarding a train, at an origin or after a footpath from one,
    /// latest first, as range RAPTOR runs them.
    pub fn departures(&self, origins: &[StopIdx], from: Secs, until: Secs) -> Vec<Secs> {
        let mut starts: Vec<(StopIdx, Secs)> = origins.iter().map(|&o| (o, 0)).collect();
        for &o in origins {
            // Not to another origin, already a start without the walk:
            // its departures less the walk would be runs finding nothing new.
            starts.extend(
                self.tt.footpaths[o as usize]
                    .iter()
                    .filter(|(s, _)| !origins.contains(s)),
            );
        }
        let mut times = Vec::new();
        for (s, walk) in starts {
            for &(p, pos) in &self.stop_patterns[s as usize] {
                let trips = &self.tt.patterns[p as usize].trips;
                times.extend(
                    trips
                        .iter()
                        .map(|t| t.times[pos as usize].1 - walk)
                        .filter(|t| (from..until).contains(t)),
                );
            }
        }
        times.sort_unstable_by(|a, b| b.cmp(a));
        times.dedup();
        times
    }

    /// The Pareto set over (departure, arrival, rides)
    /// of journeys from `origins` departing in `[from, until)`,
    /// to each set of stops in `targets`, latest departure first.
    pub fn profile(
        &self,
        origins: &[StopIdx],
        from: Secs,
        until: Secs,
        targets: &[&[StopIdx]],
    ) -> Vec<Vec<Journey>> {
        let mut labels = self.labels();
        let mut journeys = vec![Vec::new(); targets.len()];
        // Each target set's earliest arrival per round, over the runs so far.
        let mut best = vec![[NEVER; MAX_RIDES + 1]; targets.len()];
        for depart in self.departures(origins, from, until) {
            labels.run(origins, depart);
            for ((target, best), journeys) in targets.iter().zip(&mut best).zip(&mut journeys) {
                let mut fewer = NEVER;
                for (k, best) in best.iter_mut().enumerate().skip(1) {
                    let (arrive, stop) = labels.earliest(k, target);
                    // Lowered this run, so it leaves now,
                    // and beats every journey with fewer rides leaving now or later.
                    if arrive < *best && arrive < fewer {
                        journeys.push(labels.extract(k, stop));
                    }
                    *best = arrive;
                    fewer = fewer.min(arrive);
                }
            }
        }
        journeys
    }
}

impl Labels<'_> {
    /// Lowers labels with journeys from `origins` leaving at `depart`.
    /// Runs of a range query must go latest first.
    pub fn run(&mut self, origins: &[StopIdx], depart: Secs) {
        debug_assert!(depart <= self.depart, "runs must go latest first");
        self.depart = depart;
        let tt = self.router.tt;

        let mut marked = Vec::new();
        for &o in origins {
            if self.lower_ready(0, o, depart, Ready::Origin) {
                marked.push(o);
            }
        }
        for &o in origins {
            for &(to, walk) in &tt.footpaths[o as usize] {
                if self.lower_ready(0, to, depart + walk, Ready::Walk { from: o }) {
                    marked.push(to);
                }
            }
        }

        for k in 1..self.ride_arrival.len() {
            if marked.is_empty() {
                break;
            }
            // Each pattern serving a marked stop, from its earliest marked position.
            let mut scan: Vec<(u32, u32)> = Vec::new();
            for &s in &marked {
                for &(p, pos) in &self.router.stop_patterns[s as usize] {
                    match scan.iter_mut().find(|(q, _)| *q == p) {
                        Some((_, from)) => *from = (*from).min(pos),
                        None => scan.push((p, pos)),
                    }
                }
            }
            scan.sort_unstable();

            let mut improved = Vec::new();
            for (p, from) in scan {
                let pattern = &tt.patterns[p as usize];
                // The trip being ridden, and where it was boarded.
                let mut riding: Option<(usize, u32)> = None;
                for pos in from as usize..pattern.stops.len() {
                    let s = pattern.stops[pos];
                    if let Some((trip, board_pos)) = riding {
                        let arrive = pattern.trips[trip].times[pos].0;
                        let ride = Ride {
                            pattern: p,
                            trip: trip as u32,
                            board_pos,
                            alight_pos: pos as u32,
                        };
                        if self.lower_ride(k, s, arrive, ride) {
                            improved.push(s);
                        }
                    }
                    // Catch an earlier trip here, if the previous round makes one reachable.
                    let ready = self.ready[k - 1][s as usize];
                    if ready == NEVER {
                        continue;
                    }
                    if riding.is_none_or(|(trip, _)| ready < pattern.trips[trip].times[pos].1) {
                        // FIFO patterns are sorted by departure at every stop.
                        let trip = pattern.trips.partition_point(|t| t.times[pos].1 < ready);
                        if trip < pattern.trips.len() && riding.is_none_or(|(r, _)| trip < r) {
                            riding = Some((trip, pos as u32));
                        }
                    }
                }
            }

            marked.clear();
            improved.sort_unstable();
            improved.dedup();
            for &s in &improved {
                let arrive = self.ride_arrival[k][s as usize];
                if self.lower_ready(k, s, arrive + tt.min_change[s as usize], Ready::Change) {
                    marked.push(s);
                }
            }
            for &s in &improved {
                let arrive = self.ride_arrival[k][s as usize];
                for &(to, walk) in &tt.footpaths[s as usize] {
                    if self.lower_ready(k, to, arrive + walk, Ready::Walk { from: s }) {
                        marked.push(to);
                    }
                }
            }
            marked.sort_unstable();
            marked.dedup();
        }
    }

    /// Lowers `ride_arrival[k][s]` if `arrive` beats it
    /// and every arrival there with fewer rides.
    fn lower_ride(&mut self, k: usize, s: StopIdx, arrive: Secs, ride: Ride) -> bool {
        let s = s as usize;
        if (0..=k).any(|j| self.ride_arrival[j][s] <= arrive) {
            return false;
        }
        self.ride_arrival[k][s] = arrive;
        self.ride_from[k][s] = Some(ride);
        true
    }

    /// Lowers `ready[k][s]` if `t` beats it and every readiness there with fewer rides.
    fn lower_ready(&mut self, k: usize, s: StopIdx, t: Secs, how: Ready) -> bool {
        let s = s as usize;
        if (0..=k).any(|j| self.ready[j][s] <= t) {
            return false;
        }
        self.ready[k][s] = t;
        self.ready_from[k][s] = Some(how);
        true
    }

    /// The earliest arrival at any of `targets` on the `k`th ride, and where.
    fn earliest(&self, k: usize, targets: &[StopIdx]) -> (Secs, StopIdx) {
        targets
            .iter()
            .map(|&t| (self.ride_arrival[k][t as usize], t))
            .min()
            .unwrap_or((NEVER, 0))
    }

    /// The Pareto set of journeys to any of `targets`, fewest rides first:
    /// each arrives strictly earlier than every one with fewer rides.
    pub fn journeys(&self, targets: &[StopIdx]) -> Vec<Journey> {
        let mut journeys = Vec::new();
        let mut fewer = NEVER;
        for k in 1..self.ride_arrival.len() {
            let (arrive, stop) = self.earliest(k, targets);
            if arrive < fewer {
                journeys.push(self.extract(k, stop));
                fewer = arrive;
            }
        }
        journeys
    }

    fn extract(&self, rides: usize, target: StopIdx) -> Journey {
        let tt = self.router.tt;
        let mut legs = Vec::new();
        let mut stop = target;
        for k in (1..=rides).rev() {
            let r = self.ride_from[k][stop as usize].expect("a reached stop has a ride label");
            let pattern = &tt.patterns[r.pattern as usize];
            let times = &pattern.trips[r.trip as usize].times;
            let board_stop = pattern.stops[r.board_pos as usize];
            legs.push(Leg::Ride {
                pattern: r.pattern,
                trip: r.trip,
                board_pos: r.board_pos,
                alight_pos: r.alight_pos,
                board_stop,
                alight_stop: stop,
                depart: times[r.board_pos as usize].1,
                arrive: times[r.alight_pos as usize].0,
            });
            stop = board_stop;
            match self.ready_from[k - 1][stop as usize].expect("a boarded stop has a ready label") {
                Ready::Origin | Ready::Change => {}
                Ready::Walk { from } => {
                    let duration = tt.footpaths[from as usize]
                        .iter()
                        .find(|&&(to, _)| to == stop)
                        .expect("a walk label has its footpath")
                        .1;
                    legs.push(Leg::Walk {
                        from,
                        to: stop,
                        duration,
                    });
                    stop = from;
                }
            }
        }
        legs.reverse();
        let journey = Journey {
            depart: self.depart,
            arrive: self.ride_arrival[rides][target as usize],
            legs,
        };
        debug_assert!(journey.is_consistent(), "{journey:?}");
        journey
    }
}

impl Journey {
    /// Each leg starts no earlier than the one before it ends,
    /// the first no earlier than the journey's departure.
    fn is_consistent(&self) -> bool {
        let mut t = self.depart;
        for leg in &self.legs {
            match *leg {
                Leg::Ride { depart, arrive, .. } => {
                    if depart < t {
                        return false;
                    }
                    t = arrive;
                }
                Leg::Walk { duration, .. } => t += duration,
            }
        }
        t == self.arrive
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use jiff::civil::Date;

    use super::*;
    use crate::gtfs::{Feed, parse_time};

    /// ```text
    /// A --1-- B --1-- C            (route 1, slow)
    ///         B --2-- D            (route 2)
    /// A --3-- E                    (route 3), E <-> B footpath
    /// ```
    const STOPS: &str = "stop_id,stop_name\nA,A\nB,B\nC,C\nD,D\nE,E\n";
    const CALENDAR: &str = "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
        W,1,1,1,1,1,1,1,20250101,20251231\n";

    fn timetable(trips: &str, stop_times: &str, transfers: &str) -> Timetable {
        let files = HashMap::from([
            ("stops.txt", STOPS),
            ("trips.txt", trips),
            ("stop_times.txt", stop_times),
            ("calendar.txt", CALENDAR),
            ("transfers.txt", transfers),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        Timetable::build(&feed, Date::new(2025, 9, 3).unwrap()).unwrap()
    }

    fn t(s: &str) -> Secs {
        parse_time(s).unwrap()
    }

    fn stop(tt: &Timetable, id: &str) -> StopIdx {
        tt.stops.iter().position(|s| s.id == id).unwrap() as StopIdx
    }

    /// `(trip_id, board stop, alight stop)` of each ride, and walks as `walk`.
    fn summary(tt: &Timetable, j: &Journey) -> Vec<String> {
        j.legs
            .iter()
            .map(|l| match *l {
                Leg::Ride {
                    pattern,
                    trip,
                    board_stop,
                    alight_stop,
                    ..
                } => format!(
                    "{} {}-{}",
                    tt.patterns[pattern as usize].trips[trip as usize].trip_id,
                    tt.stops[board_stop as usize].id,
                    tt.stops[alight_stop as usize].id,
                ),
                Leg::Walk { from, to, .. } => {
                    format!(
                        "walk {}-{}",
                        tt.stops[from as usize].id, tt.stops[to as usize].id
                    )
                }
            })
            .collect()
    }

    const TRIPS: &str = "route_id,trip_id,service_id\n\
        1,r1a,W\n1,r1b,W\n2,r2a,W\n2,r2b,W\n";
    const STOP_TIMES: &str = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
        r1a,A,08:00:00,08:00:00,1\nr1a,B,08:10:00,08:10:00,2\nr1a,C,08:30:00,08:30:00,3\n\
        r1b,A,08:20:00,08:20:00,1\nr1b,B,08:30:00,08:30:00,2\nr1b,C,08:50:00,08:50:00,3\n\
        r2a,B,08:11:00,08:11:00,1\nr2a,D,08:20:00,08:20:00,2\n\
        r2b,B,08:15:00,08:15:00,1\nr2b,D,08:24:00,08:24:00,2\n";

    #[test]
    fn direct_ride_waits_for_the_next_trip() {
        let tt = timetable(
            TRIPS,
            STOP_TIMES,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n",
        );
        let router = Router::new(&tt);
        let js = router
            .query(&[stop(&tt, "A")], t("08:01:00"))
            .journeys(&[stop(&tt, "C")]);
        assert_eq!(js.len(), 1);
        assert_eq!(summary(&tt, &js[0]), ["r1b A-C"]);
        assert_eq!(js[0].arrive, t("08:50:00"));
    }

    #[test]
    fn change_time_decides_the_connection() {
        let a_to_d = |transfers: &str| {
            let tt = timetable(TRIPS, STOP_TIMES, transfers);
            let router = Router::new(&tt);
            let js = router
                .query(&[stop(&tt, "A")], t("08:00:00"))
                .journeys(&[stop(&tt, "D")]);
            js.iter().map(|j| summary(&tt, j)).collect::<Vec<_>>()
        };
        let header = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n";
        // Cross-platform at B: make the 08:11.
        assert_eq!(
            a_to_d(&format!("{header}B,B,2,0\n")),
            [["r1a A-B", "r2a B-D"]]
        );
        // 180s at B: miss it, take the 08:15.
        assert_eq!(
            a_to_d(&format!("{header}B,B,2,180\n")),
            [["r1a A-B", "r2b B-D"]]
        );
        // No row for B: the 180s default.
        assert_eq!(a_to_d(header), [["r1a A-B", "r2b B-D"]]);
    }

    #[test]
    fn footpath_between_stops() {
        let trips = "route_id,trip_id,service_id\n3,r3,W\n2,r2a,W\n2,r2b,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            r3,A,08:00:00,08:00:00,1\nr3,E,08:09:00,08:09:00,2\n\
            r2a,B,08:11:00,08:11:00,1\nr2a,D,08:20:00,08:20:00,2\n\
            r2b,B,08:15:00,08:15:00,1\nr2b,D,08:24:00,08:24:00,2\n";
        // E's own change time doesn't apply on top of the walk.
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
            E,B,2,120\nB,E,2,120\nE,E,2,600\n";
        let tt = timetable(trips, stop_times, transfers);
        let router = Router::new(&tt);
        let js = router
            .query(&[stop(&tt, "A")], t("08:00:00"))
            .journeys(&[stop(&tt, "D")]);
        assert_eq!(js.len(), 1);
        assert_eq!(summary(&tt, &js[0]), ["r3 A-E", "walk E-B", "r2a B-D"]);
        assert_eq!(
            js[0].legs[1],
            Leg::Walk {
                from: stop(&tt, "E"),
                to: stop(&tt, "B"),
                duration: 120
            }
        );
    }

    #[test]
    fn pareto_over_rides() {
        // One ride A-C at 08:50, or A-B on route 1 then B-C on a fast route 5 by 08:20.
        let trips = "route_id,trip_id,service_id\n1,r1a,W\n1,r1b,W\n5,r5,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            r1b,A,08:20:00,08:20:00,1\nr1b,B,08:30:00,08:30:00,2\nr1b,C,08:50:00,08:50:00,3\n\
            r1a,A,08:00:00,08:00:00,1\nr1a,B,08:10:00,08:10:00,2\nr1a,C,09:30:00,09:30:00,3\n\
            r5,B,08:15:00,08:15:00,1\nr5,C,08:20:00,08:20:00,2\n";
        // r1a and r1b overtake each other at C, so they're separate patterns.
        let tt = timetable(
            trips,
            stop_times,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,0\n",
        );
        let router = Router::new(&tt);
        let js = router
            .query(&[stop(&tt, "A")], t("08:00:00"))
            .journeys(&[stop(&tt, "C")]);
        let got: Vec<_> = js
            .iter()
            .map(|j| (j.rides(), j.arrive, summary(&tt, j)))
            .collect();
        assert_eq!(
            got,
            [
                (1, t("08:50:00"), vec!["r1b A-C".to_string()]),
                (
                    2,
                    t("08:20:00"),
                    vec!["r1a A-B".to_string(), "r5 B-C".to_string()]
                ),
            ]
        );
    }

    #[test]
    fn dominated_transfer_journey_dropped() {
        // Transferring to route 5 arrives no earlier than staying on, so only one journey.
        let trips = "route_id,trip_id,service_id\n1,r1a,W\n5,r5,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            r1a,A,08:00:00,08:00:00,1\nr1a,B,08:10:00,08:10:00,2\nr1a,C,08:30:00,08:30:00,3\n\
            r5,B,08:15:00,08:15:00,1\nr5,C,08:30:00,08:30:00,2\n";
        let tt = timetable(
            trips,
            stop_times,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,0\n",
        );
        let router = Router::new(&tt);
        let js = router
            .query(&[stop(&tt, "A")], t("08:00:00"))
            .journeys(&[stop(&tt, "C")]);
        assert_eq!(js.len(), 1);
        assert_eq!(js[0].rides(), 1);
    }

    #[test]
    fn several_origins_and_targets() {
        let tt = timetable(
            TRIPS,
            STOP_TIMES,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n",
        );
        let router = Router::new(&tt);
        // From A or B, to C or D: B-D on r2a is earliest.
        let js = router
            .query(&[stop(&tt, "A"), stop(&tt, "B")], t("08:05:00"))
            .journeys(&[stop(&tt, "C"), stop(&tt, "D")]);
        assert_eq!(js.len(), 1);
        assert_eq!(summary(&tt, &js[0]), ["r2a B-D"]);
    }

    #[test]
    fn unreachable() {
        let tt = timetable(
            TRIPS,
            STOP_TIMES,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n",
        );
        let router = Router::new(&tt);
        let js = router
            .query(&[stop(&tt, "D")], t("08:00:00"))
            .journeys(&[stop(&tt, "A")]);
        assert!(js.is_empty());
    }

    fn profile(tt: &Timetable, from: &str, to: &str, window: (&str, &str)) -> Vec<String> {
        let router = Router::new(tt);
        let (origins, targets) = ([stop(tt, from)], [stop(tt, to)]);
        let journeys = router.profile(&origins, t(window.0), t(window.1), &[&targets]);
        journeys[0]
            .iter()
            .map(|j| format!("{} {}", crate::hms(j.depart), summary(tt, j).join(", ")))
            .collect()
    }

    #[test]
    fn departures_latest_first_including_footpaths() {
        let trips = "route_id,trip_id,service_id\n3,r3,W\n2,r2a,W\n2,r2b,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            r3,E,08:00:00,08:00:00,1\nr3,A,08:09:00,08:09:00,2\n\
            r2a,B,08:11:00,08:11:00,1\nr2a,D,08:20:00,08:20:00,2\n\
            r2b,B,08:15:00,08:15:00,1\nr2b,D,08:24:00,08:24:00,2\n";
        let transfers =
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nE,B,2,120\nB,E,2,120\n";
        let tt = timetable(trips, stop_times, transfers);
        let router = Router::new(&tt);
        // From E: its own 08:00, and B's trains less the 2 min walk.
        let times = router.departures(&[stop(&tt, "E")], t("08:00:00"), t("08:13:00"));
        assert_eq!(times, [t("08:09:00"), t("08:00:00")]);
    }

    #[test]
    fn profile_keeps_each_departure_that_arrives_earlier() {
        let tt = timetable(
            TRIPS,
            STOP_TIMES,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n",
        );
        assert_eq!(
            profile(&tt, "A", "C", ("07:00:00", "09:00:00")),
            ["08:20:00 r1b A-C", "08:00:00 r1a A-C"]
        );
        // The window is half-open, and the 08:20 is outside it.
        assert_eq!(
            profile(&tt, "A", "C", ("07:00:00", "08:20:00")),
            ["08:00:00 r1a A-C"]
        );
    }

    #[test]
    fn profile_drops_earlier_departure_arriving_later() {
        // The 08:00 local arrives after the 08:10 express.
        let trips = "route_id,trip_id,service_id\n1,local,W\n1,express,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            local,A,08:00:00,08:00:00,1\nlocal,C,09:00:00,09:00:00,2\n\
            express,A,08:10:00,08:10:00,1\nexpress,C,08:40:00,08:40:00,2\n";
        let tt = timetable(
            trips,
            stop_times,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n",
        );
        assert_eq!(
            profile(&tt, "A", "C", ("08:00:00", "09:00:00")),
            ["08:10:00 express A-C"]
        );
    }

    #[test]
    fn profile_keeps_fewer_rides_leaving_earlier() {
        // 08:00 one ride arriving 08:50; 08:05 two rides arriving 08:40.
        // Neither dominates: one leaves earlier with fewer rides.
        // A label from the later, two-ride run mustn't prune the earlier one-ride journey.
        let trips = "route_id,trip_id,service_id\n1,slow,W\n2,feeder,W\n5,fast,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            slow,A,08:00:00,08:00:00,1\nslow,C,08:50:00,08:50:00,2\n\
            feeder,A,08:05:00,08:05:00,1\nfeeder,B,08:10:00,08:10:00,2\n\
            fast,B,08:10:00,08:10:00,1\nfast,C,08:40:00,08:40:00,2\n";
        let tt = timetable(
            trips,
            stop_times,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,0\n",
        );
        assert_eq!(
            profile(&tt, "A", "C", ("08:00:00", "09:00:00")),
            ["08:05:00 feeder A-B, fast B-C", "08:00:00 slow A-C"]
        );
    }

    #[test]
    fn departures_skip_footpaths_between_origins() {
        let tt = timetable(
            TRIPS,
            STOP_TIMES,
            "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nA,B,2,60\nB,A,2,60\n",
        );
        let router = Router::new(&tt);
        // From A and B: their own trains, and none of either's less the walk from the other.
        let times = router.departures(
            &[stop(&tt, "A"), stop(&tt, "B")],
            t("08:00:00"),
            t("08:12:00"),
        );
        assert_eq!(times, [t("08:11:00"), t("08:10:00"), t("08:00:00")]);
    }
}
