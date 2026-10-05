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

/// Most rides in a journey (2 transfers), as `nycriders` found enough.
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

/// One query's labels, per round.
pub struct Labels<'a> {
    router: &'a Router<'a>,
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

    /// Every stop's earliest arrivals from `origins`, leaving at `depart`.
    pub fn query(&'a self, origins: &[StopIdx], depart: Secs) -> Labels<'a> {
        let n = self.tt.stops.len();
        let rounds = MAX_RIDES + 1;
        let mut l = Labels {
            router: self,
            depart,
            ride_arrival: vec![vec![NEVER; n]; rounds],
            ride_from: vec![vec![None; n]; rounds],
            ready: vec![vec![NEVER; n]; rounds],
            ready_from: vec![vec![None; n]; rounds],
        };
        // The earliest over all rounds so far, for pruning:
        // a later round's label is only kept if it beats every earlier one.
        let mut best_ride = vec![NEVER; n];
        let mut best_ready = vec![NEVER; n];

        let mut marked = Vec::new();
        for &o in origins {
            l.ready[0][o as usize] = depart;
            l.ready_from[0][o as usize] = Some(Ready::Origin);
            best_ready[o as usize] = depart;
            marked.push(o);
        }
        for &o in origins {
            for &(to, walk) in &self.tt.footpaths[o as usize] {
                let t = depart + walk;
                if t < best_ready[to as usize] {
                    l.ready[0][to as usize] = t;
                    l.ready_from[0][to as usize] = Some(Ready::Walk { from: o });
                    best_ready[to as usize] = t;
                    marked.push(to);
                }
            }
        }

        for k in 1..rounds {
            // Each pattern serving a marked stop, from its earliest marked position.
            let mut scan: Vec<(u32, u32)> = Vec::new();
            for &s in &marked {
                for &(p, pos) in &self.stop_patterns[s as usize] {
                    match scan.iter_mut().find(|(q, _)| *q == p) {
                        Some((_, from)) => *from = (*from).min(pos),
                        None => scan.push((p, pos)),
                    }
                }
            }
            scan.sort_unstable();

            let mut improved = Vec::new();
            for (p, from) in scan {
                let pattern = &self.tt.patterns[p as usize];
                // The trip being ridden, and where it was boarded.
                let mut riding: Option<(usize, u32)> = None;
                for pos in from as usize..pattern.stops.len() {
                    let s = pattern.stops[pos] as usize;
                    if let Some((trip, board_pos)) = riding {
                        let arrive = pattern.trips[trip].times[pos].0;
                        if arrive < best_ride[s] {
                            l.ride_arrival[k][s] = arrive;
                            l.ride_from[k][s] = Some(Ride {
                                pattern: p,
                                trip: trip as u32,
                                board_pos,
                                alight_pos: pos as u32,
                            });
                            best_ride[s] = arrive;
                            improved.push(s as StopIdx);
                        }
                    }
                    // Catch an earlier trip here, if the previous round makes one reachable.
                    let ready = l.ready[k - 1][s];
                    if ready == NEVER {
                        continue;
                    }
                    let can_improve = match riding {
                        Some((trip, _)) => ready < pattern.trips[trip].times[pos].1,
                        None => true,
                    };
                    if can_improve {
                        // FIFO patterns are sorted by departure at every stop.
                        let trip = pattern.trips.partition_point(|t| t.times[pos].1 < ready);
                        if trip < pattern.trips.len() && riding.is_none_or(|(r, _)| trip < r) {
                            riding = Some((trip, pos as u32));
                        }
                    }
                }
            }

            marked.clear();
            for &s in &improved {
                let arrive = l.ride_arrival[k][s as usize];
                let t = arrive + self.tt.min_change[s as usize];
                if t < best_ready[s as usize] {
                    l.ready[k][s as usize] = t;
                    l.ready_from[k][s as usize] = Some(Ready::Change);
                    best_ready[s as usize] = t;
                    marked.push(s);
                }
            }
            for &s in &improved {
                let arrive = l.ride_arrival[k][s as usize];
                for &(to, walk) in &self.tt.footpaths[s as usize] {
                    let t = arrive + walk;
                    if t < best_ready[to as usize] {
                        l.ready[k][to as usize] = t;
                        l.ready_from[k][to as usize] = Some(Ready::Walk { from: s });
                        best_ready[to as usize] = t;
                        marked.push(to);
                    }
                }
            }
            marked.sort_unstable();
            marked.dedup();
            if marked.is_empty() {
                break;
            }
        }
        l
    }
}

impl Labels<'_> {
    /// The Pareto set of journeys to any of `targets`, fewest rides first:
    /// each arrives strictly earlier than every one with fewer rides.
    pub fn journeys(&self, targets: &[StopIdx]) -> Vec<Journey> {
        let mut journeys = Vec::new();
        let mut best = NEVER;
        for k in 1..self.ride_arrival.len() {
            let Some(&target) = targets
                .iter()
                .filter(|&&t| self.ride_arrival[k][t as usize] < best)
                .min_by_key(|&&t| self.ride_arrival[k][t as usize])
            else {
                continue;
            };
            let journey = self.extract(k, target);
            best = journey.arrive;
            journeys.push(journey);
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
        Journey {
            depart: self.depart,
            arrive: self.ride_arrival[rides][target as usize],
            legs,
        }
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
    /// A --4------------------ C    (route 4, one fast trip)
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
}
