//! One service date's timetable: stops, FIFO trip patterns, and transfers.
//!
//! Phase 2 of `raptor_design.md`: stops are parent stations,
//! and `transfers.txt` is taken at its word.

use std::collections::{BTreeMap, HashMap, HashSet};

use anyhow::{Context, Result, bail};
use jiff::ToSpan;
use jiff::civil::Date;

use crate::calendar::{active_services, span};
use crate::gtfs::{DAY, Feed, Secs};

/// Minimum time to change trains at a stop `transfers.txt` gives no same-stop row for.
/// 180s is what the feed gives almost every stop it does list.
pub const DEFAULT_MIN_CHANGE: Secs = 180;

/// The next date's trips starting before this are included, shifted forward a day,
/// for journeys late in the date: the MTA files a trip starting after midnight
/// under the next date's service, so the date's own trips stop at midnight.
pub const NEXT_DATE_HORIZON: Secs = 3 * 60 * 60;

pub type StopIdx = u32;

/// Trips sharing one of these share a pattern, before FIFO splitting.
type PatternKey<'a> = (&'a str, Option<u8>, Vec<StopIdx>);

#[derive(Debug)]
pub struct Stop {
    pub id: String,
    pub name: String,
}

#[derive(Debug, PartialEq)]
pub struct TripTimes {
    pub trip_id: String,
    /// The service date the trip runs on, relative to the timetable's:
    /// -1 or 1 for the previous or next date's, shifted by a day.
    pub day: i8,
    /// `(arrival, departure)` at each of the pattern's stops.
    pub times: Vec<(Secs, Secs)>,
}

/// Trips of one route and direction over the same stops,
/// none overtaking another, sorted by departure.
#[derive(Debug)]
pub struct Pattern {
    pub route_id: String,
    #[expect(dead_code, reason = "for journey output, phase 5")]
    pub direction_id: Option<u8>,
    pub stops: Vec<StopIdx>,
    pub trips: Vec<TripTimes>,
}

#[derive(Debug)]
pub struct Timetable {
    pub date: Date,
    pub stops: Vec<Stop>,
    pub patterns: Vec<Pattern>,
    /// Minimum time between alighting and boarding at the same stop.
    pub min_change: Vec<Secs>,
    /// `(to, walk time)` from each stop to other stops.
    pub footpaths: Vec<Vec<(StopIdx, Secs)>>,
    pub report: Report,
}

/// What building the timetable found, worth a look before trusting it.
#[derive(Debug, Default)]
pub struct Report {
    pub services: Vec<String>,
    pub trips: usize,
    pub overnight_trips: usize,
    /// The previous date is outside the feed, so its overnight trips are missing.
    pub previous_date_missing: bool,
    /// The next date's trips starting before `NEXT_DATE_HORIZON`.
    pub next_date_trips: usize,
    /// The next date is outside the feed, so its early trips are missing.
    pub next_date_missing: bool,
    /// Patterns split because a trip overtook another.
    pub fifo_splits: usize,
    /// Trips with exactly the same times as another on the same pattern.
    pub duplicate_trips: Vec<String>,
    /// Served stops with no same-stop transfer row, so on `DEFAULT_MIN_CHANGE`.
    pub default_change_stops: usize,
    pub transfer_types: BTreeMap<u8, usize>,
    /// Transfer rows with no `min_transfer_time`, so on `DEFAULT_MIN_CHANGE`.
    pub transfers_without_time: usize,
    /// Footpaths `a -> b` with no `b -> a`.
    pub asymmetric_footpaths: Vec<(String, String)>,
    /// `a -> c` missing although `a -> b -> c` exists:
    /// RAPTOR relaxes footpaths once a round, so assumes closure.
    pub unclosed_footpaths: Vec<(String, String, String)>,
}

impl Timetable {
    pub fn stop(&self, id: &str) -> Option<StopIdx> {
        self.stops
            .iter()
            .position(|s| s.id == id)
            .map(|i| i as StopIdx)
    }

    pub fn build(feed: &Feed, date: Date) -> Result<Self> {
        let mut report = Report::default();

        // Parent stations, and every other stop mapped to its parent.
        let mut stops = Vec::new();
        let mut index: HashMap<&str, StopIdx> = HashMap::new();
        for stop in feed.stops.iter().filter(|s| parent_of(s).is_none()) {
            index.insert(&stop.stop_id, stops.len() as StopIdx);
            stops.push(Stop {
                id: stop.stop_id.clone(),
                name: stop.stop_name.clone(),
            });
        }
        for stop in &feed.stops {
            if let Some(parent) = parent_of(stop) {
                let &i = index.get(parent).with_context(|| {
                    format!("stop {} has unknown parent {parent}", stop.stop_id)
                })?;
                index.insert(&stop.stop_id, i);
            }
        }
        let stop_idx = |id: &str| {
            index
                .get(id)
                .copied()
                .with_context(|| format!("unknown stop {id}"))
        };

        let today = active_services(feed, date)?;
        report.services = today.iter().map(|s| s.to_string()).collect();
        let previous = date.checked_sub(1.day())?;
        let yesterday = match span(feed) {
            Some((start, _)) if previous >= start => active_services(feed, previous)?,
            _ => {
                report.previous_date_missing = true;
                Default::default()
            }
        };
        let next = date.checked_add(1.day())?;
        let tomorrow = match span(feed) {
            Some((_, end)) if next <= end => active_services(feed, next)?,
            _ => {
                report.next_date_missing = true;
                Default::default()
            }
        };

        let mut stop_times: HashMap<&str, Vec<_>> = HashMap::new();
        for st in &feed.stop_times {
            stop_times.entry(st.trip_id.as_str()).or_default().push(st);
        }

        let mut groups: HashMap<PatternKey, Vec<TripTimes>> = HashMap::new();
        for trip in &feed.trips {
            let runs_today = today.contains(trip.service_id.as_str());
            let runs_yesterday = yesterday.contains(trip.service_id.as_str());
            let runs_tomorrow = tomorrow.contains(trip.service_id.as_str());
            if !runs_today && !runs_yesterday && !runs_tomorrow {
                continue;
            }
            let mut sts = stop_times.remove(trip.trip_id.as_str()).unwrap_or_default();
            if sts.len() < 2 {
                bail!("trip {} has {} stop times", trip.trip_id, sts.len());
            }
            sts.sort_by_key(|st| st.stop_sequence);
            let pattern_stops = sts
                .iter()
                .map(|st| stop_idx(&st.stop_id))
                .collect::<Result<Vec<_>>>()?;
            let times: Vec<_> = sts
                .iter()
                .map(|st| (st.arrival_time, st.departure_time))
                .collect();
            check_times(&trip.trip_id, &times)?;

            let key = (trip.route_id.as_str(), trip.direction_id, pattern_stops);
            if runs_today {
                report.trips += 1;
                groups.entry(key.clone()).or_default().push(TripTimes {
                    trip_id: trip.trip_id.clone(),
                    day: 0,
                    times: times.clone(),
                });
            }
            if runs_yesterday && times.last().is_some_and(|&(arr, _)| arr >= DAY) {
                report.overnight_trips += 1;
                groups.entry(key.clone()).or_default().push(TripTimes {
                    trip_id: trip.trip_id.clone(),
                    day: -1,
                    times: times.iter().map(|&(a, d)| (a - DAY, d - DAY)).collect(),
                });
            }
            if runs_tomorrow && times[0].1 < NEXT_DATE_HORIZON {
                report.next_date_trips += 1;
                groups.entry(key).or_default().push(TripTimes {
                    trip_id: trip.trip_id.clone(),
                    day: 1,
                    times: times.iter().map(|&(a, d)| (a + DAY, d + DAY)).collect(),
                });
            }
        }

        // Sorted by key so pattern indices don't depend on hash order.
        let mut groups: Vec<_> = groups.into_iter().collect();
        groups.sort_by(|a, b| a.0.cmp(&b.0));
        let mut patterns = Vec::new();
        for ((route_id, direction_id, pattern_stops), mut trips) in groups {
            trips.sort_by(|a, b| a.times.cmp(&b.times));
            let split = split_fifo(trips, &mut report.duplicate_trips);
            report.fifo_splits += split.len() - 1;
            for trips in split {
                patterns.push(Pattern {
                    route_id: route_id.to_string(),
                    direction_id,
                    stops: pattern_stops.clone(),
                    trips,
                });
            }
        }

        let mut min_change: Vec<Option<Secs>> = vec![None; stops.len()];
        let mut footpaths: Vec<Vec<(StopIdx, Secs)>> = vec![Vec::new(); stops.len()];
        for t in &feed.transfers {
            *report.transfer_types.entry(t.transfer_type).or_default() += 1;
            // 3: transfers between these stops aren't possible.
            if t.transfer_type == 3 {
                continue;
            }
            let time = t.min_transfer_time.unwrap_or_else(|| {
                report.transfers_without_time += 1;
                DEFAULT_MIN_CHANGE
            });
            let (from, to) = (stop_idx(&t.from_stop_id)?, stop_idx(&t.to_stop_id)?);
            if from == to {
                let change = &mut min_change[from as usize];
                *change = Some(change.map_or(time, |c| c.max(time)));
            } else {
                let paths = &mut footpaths[from as usize];
                match paths.iter_mut().find(|(s, _)| *s == to) {
                    Some((_, t)) => *t = (*t).max(time),
                    None => paths.push((to, time)),
                }
            }
        }
        let served: HashSet<StopIdx> = patterns
            .iter()
            .flat_map(|p| p.stops.iter().copied())
            .collect();
        report.default_change_stops = served
            .iter()
            .filter(|&&s| min_change[s as usize].is_none())
            .count();
        let min_change = min_change
            .into_iter()
            .map(|c| c.unwrap_or(DEFAULT_MIN_CHANGE))
            .collect();

        let name = |s: StopIdx| stops[s as usize].id.clone();
        let has_path = |a: StopIdx, b: StopIdx| footpaths[a as usize].iter().any(|&(s, _)| s == b);
        for (a, paths) in footpaths.iter().enumerate() {
            let a = a as StopIdx;
            for &(b, _) in paths {
                if !has_path(b, a) {
                    report.asymmetric_footpaths.push((name(a), name(b)));
                }
                for &(c, _) in &footpaths[b as usize] {
                    if c != a && !has_path(a, c) {
                        report.unclosed_footpaths.push((name(a), name(b), name(c)));
                    }
                }
            }
        }

        Ok(Self {
            date,
            stops,
            patterns,
            min_change,
            footpaths,
            report,
        })
    }
}

fn parent_of(stop: &crate::gtfs::Stop) -> Option<&str> {
    stop.parent_station.as_deref().filter(|p| !p.is_empty())
}

/// Arrival at or before departure at each stop, and no time running backwards.
fn check_times(trip_id: &str, times: &[(Secs, Secs)]) -> Result<()> {
    for (i, &(arr, dep)) in times.iter().enumerate() {
        if arr > dep {
            bail!("trip {trip_id} stop {i}: arrives {arr} after departing {dep}");
        }
        if i > 0 && times[i - 1].1 > arr {
            bail!("trip {trip_id} stop {i}: arrives {arr} before departing the previous stop");
        }
    }
    Ok(())
}

/// Splits trips sorted by time into groups in which none overtakes another,
/// on arrival or departure at any stop, as RAPTOR's trip scan needs.
/// Each trip goes into the first group whose last trip it doesn't overtake.
fn split_fifo(trips: Vec<TripTimes>, duplicates: &mut Vec<String>) -> Vec<Vec<TripTimes>> {
    let mut groups: Vec<Vec<TripTimes>> = Vec::new();
    for trip in trips {
        let fits = |group: &Vec<TripTimes>| {
            let last = group.last().expect("groups are never empty");
            last.times
                .iter()
                .zip(&trip.times)
                .all(|(l, t)| l.0 <= t.0 && l.1 <= t.1)
        };
        if let Some(last) = groups
            .iter()
            .flat_map(|g| g.last())
            .find(|l| l.times == trip.times)
        {
            duplicates.push(format!("{} = {}", trip.trip_id, last.trip_id));
        }
        match groups.iter_mut().find(|g| fits(g)) {
            Some(group) => group.push(trip),
            None => groups.push(vec![trip]),
        }
    }
    groups
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;

    /// Two parents `A` and `B` with N/S children, and `C` with none.
    const STOPS: &str = "stop_id,stop_name,location_type,parent_station\n\
        A,Alpha,1,\nAN,Alpha,,A\nAS,Alpha,,A\n\
        B,Beta,1,\nBN,Beta,,B\nBS,Beta,,B\n\
        C,Gamma,1,\n";
    const CALENDAR: &str = "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
        Weekday,1,1,1,1,1,0,0,20250811,20251101\n\
        Saturday,0,0,0,0,0,1,0,20250811,20251101\n";

    fn build(trips: &str, stop_times: &str, transfers: &str, date: Date) -> Timetable {
        let files = HashMap::from([
            ("stops.txt", STOPS),
            ("trips.txt", trips),
            ("stop_times.txt", stop_times),
            ("calendar.txt", CALENDAR),
            ("transfers.txt", transfers),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        Timetable::build(&feed, date).unwrap()
    }

    const TRIPS: &str = "route_id,trip_id,service_id,direction_id\n\
        1,early,Weekday,0\n1,late,Weekday,0\n1,overtaker,Weekday,0\n\
        1,owl,Weekday,0\n1,sat,Saturday,0\n";
    const STOP_TIMES: &str = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
        early,AN,08:00:00,08:00:00,1\nearly,BN,08:10:00,08:10:00,2\n\
        late,BN,08:20:00,08:20:00,2\nlate,AN,08:05:00,08:05:00,1\n\
        overtaker,AN,08:02:00,08:02:00,1\novertaker,BN,08:09:00,08:09:00,2\n\
        owl,AN,24:30:00,24:30:00,1\nowl,BN,24:40:00,24:40:00,2\n\
        sat,AN,09:00:00,09:00:00,1\nsat,BN,09:10:00,09:10:00,2\n";
    const TRANSFERS: &str = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
        A,A,2,0\nA,B,2,120\nB,C,2,60\nC,B,2,60\n";

    fn wednesday() -> Date {
        Date::new(2025, 9, 3).unwrap()
    }

    #[test]
    fn stops_are_parents() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        let ids: Vec<_> = tt.stops.iter().map(|s| s.id.as_str()).collect();
        assert_eq!(ids, ["A", "B", "C"]);
        let p = &tt.patterns[0];
        assert_eq!(p.stops, [0, 1]);
    }

    #[test]
    fn stop_sequence_order_and_overtaking_split() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        // `overtaker` leaves after `early` but arrives before it.
        assert_eq!(tt.report.fifo_splits, 1);
        let trip_ids: Vec<Vec<_>> = tt
            .patterns
            .iter()
            .map(|p| p.trips.iter().map(|t| t.trip_id.as_str()).collect())
            .collect();
        assert_eq!(
            trip_ids,
            [vec!["owl", "early", "late", "owl"], vec!["overtaker"]]
        );
        // `late`'s rows were out of order in the file.
        let late = &tt.patterns[0].trips[2];
        assert_eq!(
            late.times,
            [
                (8 * 3600 + 300, 8 * 3600 + 300),
                (8 * 3600 + 1200, 8 * 3600 + 1200)
            ]
        );
    }

    #[test]
    fn overnight_trips_from_previous_date() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        // Tuesday's `owl` runs early Wednesday, shifted back a day;
        // Wednesday's own `owl` stays at 24:30.
        let owls: Vec<_> = tt.patterns[0]
            .trips
            .iter()
            .filter(|t| t.trip_id == "owl")
            .map(|t| (t.day, t.times[0].0))
            .collect();
        assert_eq!(owls, [(-1, 30 * 60), (0, DAY + 30 * 60)]);
        assert_eq!(tt.report.trips, 4);
        assert_eq!(tt.report.overnight_trips, 1);
        assert!(!tt.report.previous_date_missing);
    }

    #[test]
    fn early_trips_from_next_date() {
        let trips = "route_id,trip_id,service_id,direction_id\n\
            1,dawn,Weekday,0\n1,early,Weekday,0\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            dawn,AN,00:10:00,00:10:00,1\ndawn,BN,00:20:00,00:20:00,2\n\
            early,AN,08:00:00,08:00:00,1\nearly,BN,08:10:00,08:10:00,2\n";
        let tt = build(trips, stop_times, TRANSFERS, wednesday());
        // Thursday's `dawn` runs late Wednesday, shifted forward a day;
        // Thursday's `early` starts after the horizon.
        let got: Vec<_> = tt.patterns[0]
            .trips
            .iter()
            .map(|t| (t.trip_id.as_str(), t.day, t.times[0].0))
            .collect();
        assert_eq!(
            got,
            [
                ("dawn", 0, 10 * 60),
                ("early", 0, 8 * 3600),
                ("dawn", 1, DAY + 10 * 60)
            ]
        );
        assert_eq!(tt.report.next_date_trips, 1);
        assert!(!tt.report.next_date_missing);
        assert!(tt.report.duplicate_trips.is_empty());
    }

    #[test]
    fn last_date_of_feed_misses_next() {
        let tt = build(
            TRIPS,
            STOP_TIMES,
            TRANSFERS,
            Date::new(2025, 11, 1).unwrap(),
        );
        assert!(tt.report.next_date_missing);
        assert_eq!(tt.report.next_date_trips, 0);
    }

    #[test]
    fn first_date_of_feed_misses_previous() {
        let tt = build(
            TRIPS,
            STOP_TIMES,
            TRANSFERS,
            Date::new(2025, 8, 11).unwrap(),
        );
        assert!(tt.report.previous_date_missing);
        assert_eq!(tt.report.overnight_trips, 0);
    }

    #[test]
    fn transfers_at_their_word() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        assert_eq!(tt.min_change, [0, DEFAULT_MIN_CHANGE, DEFAULT_MIN_CHANGE]);
        // `B` is served and has no same-stop row.
        assert_eq!(tt.report.default_change_stops, 1);
        assert_eq!(tt.footpaths[0], [(1, 120)]);
        assert_eq!(tt.report.asymmetric_footpaths, [("A".into(), "B".into())]);
        assert_eq!(
            tt.report.unclosed_footpaths,
            [("A".into(), "B".into(), "C".into())]
        );
    }

    #[test]
    fn duplicate_trips_reported() {
        let trips = "route_id,trip_id,service_id,direction_id\n1,x,Weekday,0\n1,y,Weekday,0\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            x,AN,08:00:00,08:00:00,1\nx,BN,08:10:00,08:10:00,2\n\
            y,AN,08:00:00,08:00:00,1\ny,BN,08:10:00,08:10:00,2\n";
        let tt = build(trips, stop_times, TRANSFERS, wednesday());
        assert_eq!(tt.report.duplicate_trips, ["y = x"]);
    }
}
