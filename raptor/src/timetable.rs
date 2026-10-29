//! One service date's timetable: stops, FIFO trip patterns, and transfers.
//!
//! Stops are where trains stop, a station's directions (`127N`, `127S`), not stations,
//! and `transfers.txt` is taken at its word.

use std::collections::{BTreeMap, HashMap, HashSet};

use anyhow::{Context, Result, bail};
use jiff::ToSpan;
use jiff::civil::Date;

use crate::calendar::{active_services, span};
use crate::gtfs::{DAY, Feed, Secs};
use crate::pathways::Walk;
use crate::platforms::Platforms;

/// A date's service day runs from 04:00 to 04:00 the next morning,
/// around when the subway is quietest, so a night counts with the evening before it.
/// Its OD rows are the date's hours 4 to 23 and the next date's 0 to 3, as hours 24 to 27.
pub const SERVICE_DAY_START: Secs = 4 * 60 * 60;
pub const SERVICE_DAY_END: Secs = DAY + SERVICE_DAY_START;
/// Trips starting before this are included and their departures routed,
/// for riders entering just before the service day ends.
pub const DEPARTURES_UNTIL: Secs = SERVICE_DAY_END + 3 * 60 * 60;

pub type StopIdx = u32;

/// Trips sharing one of these share a pattern, before FIFO splitting.
type PatternKey<'a> = (&'a str, Option<u8>, Vec<StopIdx>);

#[derive(Clone, Debug)]
pub struct Stop {
    pub id: String,
    /// Its parent station's ID, or its own if it has none:
    /// what outputs name it by.
    pub station: String,
    pub name: String,
    /// `(latitude, longitude)`, if `stops.txt` has them.
    pub coords: Option<(f64, f64)>,
    /// Its physical platform, once `split_platforms` knows it.
    pub platform: Option<String>,
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
    pub direction_id: Option<u8>,
    pub stops: Vec<StopIdx>,
    pub trips: Vec<TripTimes>,
}

#[derive(Debug)]
pub struct Timetable {
    pub date: Date,
    pub stops: Vec<Stop>,
    /// The stops at each station, and each stop on its own, by ID.
    pub places: HashMap<String, Vec<StopIdx>>,
    pub patterns: Vec<Pattern>,
    /// Minimum time between alighting and boarding at the same stop.
    pub min_change: Vec<Secs>,
    /// `(to, walk time)` from each stop to other stops.
    pub footpaths: Vec<Vec<(StopIdx, Secs)>>,
    /// Footpaths out of the paid area through the gates and back in,
    /// and how many times (`use_pathways`).
    pub exits: HashMap<(StopIdx, StopIdx), u8>,
    pub report: Report,
}

/// What building the timetable found, worth a look before trusting it.
#[derive(Debug, Default)]
pub struct Report {
    pub services: Vec<String>,
    /// The date's trips running in its service day.
    pub trips: usize,
    /// The previous date's trips still running at `SERVICE_DAY_START`.
    pub overnight_trips: usize,
    /// The previous date is outside the feed, so its overnight trips are missing.
    pub previous_date_missing: bool,
    /// The next date's trips starting before `DEPARTURES_UNTIL`.
    pub next_date_trips: usize,
    /// The next date is outside the feed, so its early trips are missing.
    pub next_date_missing: bool,
    /// Patterns split because a trip overtook another.
    pub fifo_splits: usize,
    /// Trips with exactly the same times as another on the same pattern.
    pub duplicate_trips: Vec<String>,
    /// The most common same-stop `min_transfer_time`,
    /// for same-stop changes `transfers.txt` gives no time for.
    pub default_change: Secs,
    /// The most common `min_transfer_time` between different stops,
    /// for footpaths `transfers.txt` gives no time for.
    pub default_footpath: Secs,
    /// Served stops with no same-stop transfer row, so on `default_change`.
    pub default_change_stops: usize,
    pub transfer_types: BTreeMap<u8, usize>,
    /// Transfer rows with no `min_transfer_time`, so on `default_change` or `default_footpath`.
    pub transfers_without_time: usize,
    /// Footpaths `a -> b` with no `b -> a`.
    pub asymmetric_footpaths: Vec<(String, String)>,
    /// `a -> c` missing although `a -> b -> c` exists:
    /// RAPTOR relaxes footpaths once a round, so assumes closure.
    pub unclosed_footpaths: Vec<(String, String, String)>,
}

impl Timetable {
    /// Whether routing on `self` and `other` finds the same journeys:
    /// the same stops, patterns, trip times, and transfers,
    /// whatever their dates, trip IDs, or which date each trip is filed under.
    pub fn routes_like(&self, other: &Self) -> bool {
        let same_pattern = |a: &Pattern, b: &Pattern| {
            (&a.route_id, a.direction_id, &a.stops) == (&b.route_id, b.direction_id, &b.stops)
                && a.trips
                    .iter()
                    .map(|t| &t.times)
                    .eq(b.trips.iter().map(|t| &t.times))
        };
        self.stops
            .iter()
            .map(|s| &s.id)
            .eq(other.stops.iter().map(|s| &s.id))
            && self.min_change == other.min_change
            && self.footpaths == other.footpaths
            && self.exits == other.exits
            && self.patterns.len() == other.patterns.len()
            && self
                .patterns
                .iter()
                .zip(&other.patterns)
                .all(|(a, b)| same_pattern(a, b))
    }

    pub fn stop(&self, id: &str) -> Option<StopIdx> {
        self.stops
            .iter()
            .position(|s| s.id == id)
            .map(|i| i as StopIdx)
    }

    /// The stops at the station `id`, or the stop `id` alone.
    pub fn stops_at(&self, id: &str) -> &[StopIdx] {
        self.places.get(id).map_or(&[], Vec::as_slice)
    }

    /// Whether `a` and `b` are at one station.
    pub fn same_station(&self, a: StopIdx, b: StopIdx) -> bool {
        self.stops[a as usize].station == self.stops[b as usize].station
    }

    pub fn build(feed: &Feed, date: Date) -> Result<Self> {
        let mut report = Report::default();

        // Every stop, platform, or station no other stop is in,
        // under its own ID and its station's;
        // not entrances, pathway nodes, or boarding areas (2 to 4).
        let parents: HashSet<&str> = feed.stops.iter().filter_map(parent_of).collect();
        let mut stops = Vec::new();
        let mut places: HashMap<String, Vec<StopIdx>> = HashMap::new();
        for stop in &feed.stops {
            if stop.location_type.unwrap_or(0) > 1 || parents.contains(stop.stop_id.as_str()) {
                continue;
            }
            let i = stops.len() as StopIdx;
            let station = parent_of(stop).unwrap_or(&stop.stop_id);
            places.entry(stop.stop_id.clone()).or_default().push(i);
            if station != stop.stop_id {
                places.entry(station.to_string()).or_default().push(i);
            }
            stops.push(Stop {
                id: stop.stop_id.clone(),
                station: station.to_string(),
                name: stop.stop_name.clone(),
                coords: stop.stop_lat.zip(stop.stop_lon),
                platform: None,
            });
        }
        let stop_idx = |id: &str| match places.get(id).map(Vec::as_slice) {
            Some(&[i]) if stops[i as usize].id == id => Ok(i),
            Some(_) => bail!("trips stop at station {id}, not one of its stops"),
            None => bail!("unknown stop {id}"),
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
            // A trip filed under the previous date, the date, or the next,
            // shifted onto the date's clock, if it runs in the service day:
            // the MTA files a trip starting after midnight under the next date's service,
            // and one running past midnight as `24:xx` under its own.
            for (day, runs, count) in [
                (-1, runs_yesterday, &mut report.overnight_trips),
                (0, runs_today, &mut report.trips),
                (1, runs_tomorrow, &mut report.next_date_trips),
            ] {
                let shift = Secs::from(day) * DAY;
                let (first, last) = (times[0].1 + shift, times[times.len() - 1].0 + shift);
                if !runs || last < SERVICE_DAY_START || first >= DEPARTURES_UNTIL {
                    continue;
                }
                *count += 1;
                groups.entry(key.clone()).or_default().push(TripTimes {
                    trip_id: trip.trip_id.clone(),
                    day,
                    times: times.iter().map(|&(a, d)| (a + shift, d + shift)).collect(),
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

        // 3: transfers between these stops aren't possible.
        // A row is between stations or stops, or within a station when from and to are one.
        let place = |id: &str| {
            places
                .get(id)
                .map(Vec::as_slice)
                .with_context(|| format!("unknown stop {id}"))
        };
        let mut transfers = Vec::new();
        for t in &feed.transfers {
            *report.transfer_types.entry(t.transfer_type).or_default() += 1;
            if t.transfer_type != 3 {
                let (from, to) = (place(&t.from_stop_id)?, place(&t.to_stop_id)?);
                transfers.push((
                    from,
                    to,
                    t.from_stop_id == t.to_stop_id,
                    t.min_transfer_time,
                ));
            }
        }
        let time_mode = |same_stop: bool| {
            mode(
                transfers
                    .iter()
                    .filter(|&&(_, _, same, _)| same == same_stop)
                    .filter_map(|&(_, _, _, time)| time),
            )
        };
        report.default_change = time_mode(true);
        report.default_footpath = time_mode(false);

        let mut min_change: Vec<Option<Secs>> = vec![None; stops.len()];
        let mut footpaths: Vec<Vec<(StopIdx, Secs)>> = vec![Vec::new(); stops.len()];
        for (from, to, same, time) in transfers {
            let time = time.unwrap_or_else(|| {
                report.transfers_without_time += 1;
                if same {
                    report.default_change
                } else {
                    report.default_footpath
                }
            });
            if same {
                for &s in from {
                    let change = &mut min_change[s as usize];
                    *change = Some(change.map_or(time, |c| c.max(time)));
                }
                continue;
            }
            for &a in from {
                for &b in to.iter().filter(|&&b| b != a) {
                    add_footpath(&mut footpaths[a as usize], b, time);
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
        let min_change: Vec<Secs> = min_change
            .into_iter()
            .map(|c| c.unwrap_or(report.default_change))
            .collect();

        // Changing to another of a station's stops takes as long as changing at one,
        // as when the station was one stop.
        for i in 0..stops.len() {
            for &b in &places[&stops[i].station] {
                if b as usize != i {
                    add_footpath(&mut footpaths[i], b, min_change[i]);
                }
            }
        }

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
            places,
            patterns,
            min_change,
            footpaths,
            exits: HashMap::new(),
            report,
        })
    }
}

/// Fixed time to walk between a complex's stops, on top of the distance:
/// stairs, doors, overhead (Anita's `BASE_TRANSFER_TIME`).
pub const BASE_WALK: Secs = 60;
/// Walking speed in a station, in meters a second (Anita's `WALK_SPEED`).
pub const WALK_SPEED: f64 = 1.2;

impl Timetable {
    /// Splits each stop whose trains stop at more than one of `platforms`
    /// into a stop for each, as Penn's uptown 1 and 2 at night, and 2 and 3 by day,
    /// and gives each stop its platform.
    /// A copy has its stop's ID, station, footpaths, and same-stop time,
    /// and walking between them takes that same-stop time, as within a station.
    /// A train whose platform there is unknown stays at the stop.
    pub fn split_platforms(&mut self, platforms: &Platforms) {
        let station = |stops: &[Stop], s: StopIdx| stops[s as usize].station.clone();
        let mut copies: HashMap<(StopIdx, String), StopIdx> = HashMap::new();
        // Each copy's original.
        let mut originals: Vec<(StopIdx, StopIdx)> = Vec::new();
        for p in &mut self.patterns {
            let n = p.stops.len();
            for k in 0..n {
                let s = p.stops[k];
                let prev = if k > 0 {
                    station(&self.stops, p.stops[k - 1])
                } else {
                    String::new()
                };
                let next = if k + 1 < n {
                    station(&self.stops, p.stops[k + 1])
                } else {
                    String::new()
                };
                let here = station(&self.stops, s);
                let Some(platform) = platforms.get(&p.route_id, &prev, &here, &next) else {
                    continue;
                };
                let stop = &mut self.stops[s as usize];
                match &stop.platform {
                    None => stop.platform = Some(platform.to_string()),
                    Some(q) if q == platform => {}
                    Some(_) => {
                        p.stops[k] =
                            *copies.entry((s, platform.to_string())).or_insert_with(|| {
                                let c = self.stops.len() as StopIdx;
                                let mut copy = self.stops[s as usize].clone();
                                copy.platform = Some(platform.to_string());
                                self.places.entry(copy.id.clone()).or_default().push(c);
                                if copy.station != copy.id {
                                    self.places.entry(copy.station.clone()).or_default().push(c);
                                }
                                self.stops.push(copy);
                                self.min_change.push(self.min_change[s as usize]);
                                self.footpaths.push(self.footpaths[s as usize].clone());
                                originals.push((c, s));
                                c
                            });
                    }
                }
            }
        }
        for &(c, s) in &originals {
            for paths in &mut self.footpaths {
                if let Some(&(_, walk)) = paths.iter().find(|&&(t, _)| t == s) {
                    paths.push((c, walk));
                }
            }
        }
        // Between a stop and its copies, and its copies one another.
        for &(c, s) in &originals {
            let change = self.min_change[s as usize];
            for &(d, _) in originals.iter().filter(|&&(d, t)| t == s && d != c) {
                add_footpath(&mut self.footpaths[c as usize], d, change);
            }
            add_footpath(&mut self.footpaths[c as usize], s, change);
            add_footpath(&mut self.footpaths[s as usize], c, change);
        }
    }

    /// Anita's transfer rules instead of `transfers.txt`'s at its word:
    /// changing trains on one platform is free, at one stop or across an island,
    /// changing to another of the station's platforms takes `up_and_over`,
    /// and every pair of a complex's stops without a `transfers.txt` footpath gets one
    /// of `BASE_WALK` plus the straight-line distance at `WALK_SPEED`.
    /// A stop's platform is from `split_platforms`;
    /// two stops whose platforms aren't both known are up and over.
    pub fn use_walk_distance_transfers<'a>(
        &mut self,
        complexes: impl Iterator<Item = &'a [StopIdx]>,
        up_and_over: Secs,
    ) {
        self.min_change.fill(0);
        for (a, paths) in self.footpaths.iter_mut().enumerate() {
            let a = &self.stops[a];
            for (b, walk) in paths {
                let b = &self.stops[*b as usize];
                if a.station == b.station {
                    let same_platform = a.platform.is_some() && a.platform == b.platform;
                    *walk = if same_platform { 0 } else { up_and_over };
                }
            }
        }
        for stops in complexes {
            for &a in stops {
                for &b in stops {
                    let has_path = self.footpaths[a as usize].iter().any(|&(s, _)| s == b);
                    if a == b || has_path {
                        continue;
                    }
                    let (Some(from), Some(to)) =
                        (self.stops[a as usize].coords, self.stops[b as usize].coords)
                    else {
                        continue;
                    };
                    let walk = BASE_WALK + (distance_m(from, to) / WALK_SPEED) as Secs;
                    self.footpaths[a as usize].push((b, walk));
                }
            }
        }
    }
}

impl Timetable {
    /// `pathways.txt`'s walks instead of `transfers.txt`'s times between the stops they join,
    /// and changing trains at a stop a pathway reaches is free, on one platform.
    /// Two of a station's `covered` stops with no walk between them have no footpath,
    /// not the station's same-stop time: pathways say there's no way, or none short enough.
    /// Stops pathways don't reach keep `transfers.txt`'s.
    pub fn use_pathways(&mut self, walks: &[Walk], covered: &[StopIdx]) {
        let is_covered = |s: StopIdx| covered.binary_search(&s).is_ok();
        for &a in covered {
            let station = &self.stops[a as usize].station;
            let stops = &self.stops;
            self.footpaths[a as usize]
                .retain(|&(b, _)| !(is_covered(b) && stops[b as usize].station == *station));
        }
        for w in walks {
            self.min_change[w.from as usize] = 0;
            let paths = &mut self.footpaths[w.from as usize];
            match paths.iter_mut().find(|(s, _)| *s == w.to) {
                Some((_, t)) => *t = w.secs,
                None => paths.push((w.to, w.secs)),
            }
            if w.exits > 0 {
                self.exits.insert((w.from, w.to), w.exits);
            }
        }
    }
}

/// A footpath to `to` taking `time`, or the longer of it and the one there is.
fn add_footpath(paths: &mut Vec<(StopIdx, Secs)>, to: StopIdx, time: Secs) {
    match paths.iter_mut().find(|(s, _)| *s == to) {
        Some((_, t)) => *t = (*t).max(time),
        None => paths.push((to, time)),
    }
}

/// The most common time, the shortest of any tied, or 0 if there are none.
fn mode(times: impl Iterator<Item = Secs>) -> Secs {
    let mut counts: BTreeMap<Secs, usize> = BTreeMap::new();
    for time in times {
        *counts.entry(time).or_default() += 1;
    }
    counts
        .into_iter()
        .rev()
        .max_by_key(|&(_, n)| n)
        .map_or(0, |(time, _)| time)
}

/// Approximate meters between two nearby `(latitude, longitude)` points.
fn distance_m((lat1, lon1): (f64, f64), (lat2, lon2): (f64, f64)) -> f64 {
    let dy = (lat2 - lat1) * 111_320.0;
    let dx = (lon2 - lon1) * 111_320.0 * ((lat1 + lat2) / 2.0).to_radians().cos();
    dx.hypot(dy)
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
    fn stops_are_directions() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        let ids: Vec<_> = tt.stops.iter().map(|s| s.id.as_str()).collect();
        assert_eq!(ids, ["AN", "AS", "BN", "BS", "C"]);
        let stations: Vec<_> = tt.stops.iter().map(|s| s.station.as_str()).collect();
        assert_eq!(stations, ["A", "A", "B", "B", "C"]);
        assert_eq!(tt.stops_at("A"), [0, 1]);
        assert_eq!(tt.stops_at("AS"), [1]);
        assert_eq!(tt.stops_at("C"), [4]);
        assert_eq!(tt.patterns[0].stops, [0, 2]);
    }

    #[test]
    fn changing_within_a_station() {
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
            A,A,2,90\nA,B,2,120\nB,A,2,120\n";
        let mut tt = build(TRIPS, STOP_TIMES, transfers, wednesday());
        // A station's same-stop time is each of its stops',
        // and the walk between them, as when it was one stop.
        assert_eq!(tt.min_change[..2], [90, 90]);
        assert_eq!(tt.footpaths[0], [(2, 120), (3, 120), (1, 90)]);
        assert_eq!(tt.footpaths[2], [(0, 120), (1, 120), (3, 90)]);
        assert!(tt.report.unclosed_footpaths.is_empty());
        // Anita's rules make changing at one stop free,
        // and to the other direction's, on a platform not known to be the same, up and over.
        tt.use_walk_distance_transfers(std::iter::empty(), 90);
        assert_eq!(tt.footpaths[0], [(2, 120), (3, 120), (1, 90)]);
    }

    #[test]
    fn platforms_split_stops_and_islands_join_them() {
        // At Beta, uptown 1s stop at the local platform, uptown 2s at the island,
        // and downtown 1s at the island's other side.
        let trips = "route_id,trip_id,service_id,direction_id\n\
            1,up1,Weekday,0\n2,up2,Weekday,0\n1,down1,Weekday,1\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            up1,AN,08:00:00,08:00:00,1\nup1,BN,08:10:00,08:10:00,2\n\
            up2,AN,08:01:00,08:01:00,1\nup2,BN,08:09:00,08:09:00,2\n\
            down1,BS,08:00:00,08:00:00,1\ndown1,AS,08:10:00,08:10:00,2\n";
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
            B,B,2,180\n";
        let mut tt = build(trips, stop_times, transfers, wednesday());
        let key = |route: &str, prev: &str, next: &str| {
            (route.into(), prev.into(), "B".into(), next.into())
        };
        let platforms: Platforms = [
            (key("1", "A", ""), "local".to_string()),
            (key("2", "A", ""), "island".to_string()),
            (key("1", "", "A"), "island".to_string()),
        ]
        .into_iter()
        .collect();
        tt.split_platforms(&platforms);

        // The uptown 2s' stop is a copy of Beta's uptown stop,
        // reached from it as from another of the station's stops.
        assert_eq!(tt.stops.len(), 6);
        assert_eq!(tt.stops[5].id, "BN");
        assert_eq!(tt.stops_at("BN"), [2, 5]);
        assert_eq!(tt.stops_at("B"), [2, 3, 5]);
        let up2 = tt.patterns.iter().find(|p| p.route_id == "2").unwrap();
        assert_eq!(up2.stops, [0, 5]);
        let walk = |tt: &Timetable, a: usize, b: StopIdx| {
            tt.footpaths[a].iter().find(|p| p.0 == b).unwrap().1
        };
        assert_eq!(
            (walk(&tt, 2, 5), walk(&tt, 5, 2), walk(&tt, 5, 3)),
            (180, 180, 180)
        );

        tt.use_walk_distance_transfers(std::iter::empty(), 90);
        // Across the island is free, whichever direction; up and over isn't.
        assert_eq!((walk(&tt, 5, 3), walk(&tt, 3, 5)), (0, 0));
        assert_eq!((walk(&tt, 2, 5), walk(&tt, 2, 3)), (90, 90));
        assert_eq!(tt.min_change[2], 0);
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
        assert_eq!(trip_ids, [vec!["early", "late", "owl"], vec!["overtaker"]]);
        // `late`'s rows were out of order in the file.
        let late = &tt.patterns[0].trips[1];
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
        let trips = "route_id,trip_id,service_id,direction_id\n\
            1,owl,Weekday,0\n1,dawn,Weekday,0\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            owl,AN,24:30:00,24:30:00,1\nowl,BN,24:40:00,24:40:00,2\n\
            dawn,AN,27:50:00,27:50:00,1\ndawn,BN,28:10:00,28:10:00,2\n";
        let tt = build(trips, stop_times, TRANSFERS, wednesday());
        // Tuesday's `owl` ends before Wednesday's service day starts at 04:00,
        // but its `dawn` runs into it, shifted back a day;
        // Wednesday's own run past midnight.
        let got: Vec<_> = tt.patterns[0]
            .trips
            .iter()
            .map(|t| (t.trip_id.as_str(), t.day, t.times[0].0))
            .collect();
        assert_eq!(
            got,
            [
                ("dawn", -1, 3 * 3600 + 50 * 60),
                ("owl", 0, DAY + 30 * 60),
                ("dawn", 0, DAY + 3 * 3600 + 50 * 60),
            ]
        );
        assert_eq!(tt.report.trips, 2);
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
        // Wednesday's `dawn` is in Tuesday's service day;
        // Thursday's runs late in Wednesday's, shifted forward a day,
        // but Thursday's `early` starts after `DEPARTURES_UNTIL`.
        let got: Vec<_> = tt.patterns[0]
            .trips
            .iter()
            .map(|t| (t.trip_id.as_str(), t.day, t.times[0].0))
            .collect();
        assert_eq!(got, [("early", 0, 8 * 3600), ("dawn", 1, DAY + 10 * 60)]);
        assert_eq!(tt.report.trips, 1);
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
    fn walk_distance_transfers() {
        // A and B 120m apart, C 240m north of A; one complex of all three.
        let stops = "stop_id,stop_name,stop_lat,stop_lon\n\
            A,A,40.0,-74.0\nB,B,40.0,-73.99859\nC,C,40.002156,-74.0\n";
        let files = HashMap::from([
            ("stops.txt", stops),
            ("trips.txt", "route_id,trip_id,service_id\n1,t,Weekday\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
                 t,A,08:00:00,08:00:00,1\nt,B,08:10:00,08:10:00,2\n",
            ),
            ("calendar.txt", CALENDAR),
            (
                "transfers.txt",
                "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
                 A,A,2,180\nA,B,2,300\n",
            ),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        let mut tt = Timetable::build(&feed, wednesday()).unwrap();
        tt.use_walk_distance_transfers([[0, 1, 2].as_slice()].into_iter(), 90);

        assert_eq!(tt.min_change, [0, 0, 0]);
        let walk = |a: usize, b: StopIdx| tt.footpaths[a].iter().find(|p| p.0 == b).unwrap().1;
        // `transfers.txt`'s stays; the rest are 60s plus the distance at 1.2 m/s.
        assert_eq!(walk(0, 1), 300);
        assert_eq!(walk(1, 0), 60 + 100);
        assert_eq!(walk(0, 2), 60 + 200);
        assert_eq!(walk(2, 1), 60 + 223);
    }

    #[test]
    fn missing_times_get_the_mode() {
        // Same-stop times 60, 180, 180, 300; footpath times 120, 240, 240.
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n\
            A,A,2,180\nC,C,2,180\nD,D,2,60\nE,E,2,300\nB,B,2,\n\
            A,C,2,240\nC,A,2,240\nD,E,2,120\nA,B,2,\n";
        let stops = "stop_id,stop_name,stop_lat,stop_lon\n\
            A,A,40,-74\nB,B,40,-74\nC,C,40,-74\nD,D,40,-74\nE,E,40,-74\nF,F,40,-74\n";
        let files = HashMap::from([
            ("stops.txt", stops),
            ("trips.txt", "route_id,trip_id,service_id\n1,t,Weekday\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
                 t,A,08:00:00,08:00:00,1\nt,B,08:10:00,08:10:00,2\n",
            ),
            ("calendar.txt", CALENDAR),
            ("transfers.txt", transfers),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        let tt = Timetable::build(&feed, wednesday()).unwrap();
        assert_eq!(
            (tt.report.default_change, tt.report.default_footpath),
            (180, 240)
        );
        assert_eq!(tt.report.transfers_without_time, 2);
        // `B`'s row has no time, and `F` has no row.
        assert_eq!(tt.min_change, [180, 180, 180, 60, 300, 180]);
        assert_eq!(tt.footpaths[0], [(2, 240), (1, 240)]);
    }

    #[test]
    fn mode_ties_go_to_the_shortest() {
        assert_eq!(mode([300, 60, 300, 60].into_iter()), 60);
        assert_eq!(mode(std::iter::empty()), 0);
    }

    #[test]
    fn transfers_at_their_word() {
        let tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        // `B` and `C` have no same-stop row, so get `A`'s, the only one.
        assert_eq!(tt.min_change, [0; 5]);
        // `BN` is served and has no same-stop row.
        assert_eq!(tt.report.default_change_stops, 1);
        assert_eq!(tt.footpaths[0], [(2, 120), (3, 120), (1, 0)]);
        // `A` to `B` has no way back, from either of `A`'s stops to either of `B`'s.
        assert_eq!(tt.report.asymmetric_footpaths.len(), 4);
        assert_eq!(
            tt.report.asymmetric_footpaths[0],
            ("AN".into(), "BN".into())
        );
        assert_eq!(tt.report.unclosed_footpaths.len(), 4);
        assert_eq!(
            tt.report.unclosed_footpaths[0],
            ("AN".into(), "BN".into(), "C".into())
        );
    }

    #[test]
    fn cross_platform_free_under_both_rules() {
        // `A`'s same-stop row is 0 in `transfers.txt`: a cross-platform change.
        let mut tt = build(TRIPS, STOP_TIMES, TRANSFERS, wednesday());
        assert_eq!(tt.min_change[0], 0);
        tt.use_walk_distance_transfers(std::iter::empty(), 90);
        assert_eq!(tt.min_change[0], 0);
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
