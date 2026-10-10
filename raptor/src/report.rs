//! Human-readable reports of what a step found, for checking it by hand.

use std::collections::{BTreeSet, HashSet};
use std::fmt::Write;
use std::time::Duration;

use crate::assign::{PathRow, Unassigned};
use crate::gtfs::{Feed, Secs};
use crate::od::{ComplexId, Complexes, OdRow};
use crate::raptor::{Journey, Leg, Legs, MAX_RIDES};
use crate::timetable::{DEFAULT_MIN_CHANGE, NEXT_DATE_HORIZON, Timetable};

/// At most this many examples of each problem.
const EXAMPLES: usize = 5;

// Writing to a `String` can't fail.
macro_rules! line {
    ($out:expr, $($arg:tt)*) => {
        writeln!($out, $($arg)*).expect("writing to a String")
    };
}

pub fn hms(t: Secs) -> String {
    let sign = if t < 0 { "-" } else { "" };
    let t = t.abs();
    format!("{sign}{:02}:{:02}:{:02}", t / 3600, t / 60 % 60, t % 60)
}

pub fn feed(feed: &Feed) -> String {
    let mut out = String::new();
    line!(out, "stops: {}", feed.stops.len());
    line!(out, "trips: {}", feed.trips.len());
    line!(out, "stop_times: {}", feed.stop_times.len());
    line!(out, "calendar: {}", feed.calendar.len());
    line!(out, "calendar_dates: {}", feed.calendar_dates.len());
    line!(out, "transfers: {}", feed.transfers.len());
    out
}

pub fn timetable(tt: &Timetable) -> String {
    let mut out = String::new();
    let r = &tt.report;
    let trips: usize = tt.patterns.iter().map(|p| p.trips.len()).sum();
    line!(out, "date: {} ({:?})", tt.date, tt.date.weekday());
    line!(out, "services: {}", r.services.join(", "));
    line!(
        out,
        "trips: {} today + {} overnight from the previous date",
        r.trips,
        r.overnight_trips
    );
    line!(
        out,
        "  + {} from the next date starting before {}",
        r.next_date_trips,
        hms(NEXT_DATE_HORIZON)
    );
    if r.next_date_missing {
        line!(
            out,
            "warning: the next date is outside the feed, so its early trips are missing"
        );
    }
    if r.previous_date_missing {
        line!(
            out,
            "warning: the previous date is outside the feed, so its overnight trips are missing"
        );
    }
    let served = tt
        .patterns
        .iter()
        .flat_map(|p| &p.stops)
        .collect::<HashSet<_>>();
    line!(
        out,
        "stops: {} parents, {} served",
        tt.stops.len(),
        served.len()
    );
    line!(
        out,
        "patterns: {} ({} from FIFO splits), {trips} trips",
        tt.patterns.len(),
        r.fifo_splits
    );
    line!(
        out,
        "duplicate trips: {} {:?}",
        r.duplicate_trips.len(),
        &r.duplicate_trips[..r.duplicate_trips.len().min(EXAMPLES)]
    );
    line!(out, "transfer types: {:?}", r.transfer_types);
    line!(
        out,
        "transfers without a time: {}",
        r.transfers_without_time
    );
    line!(
        out,
        "served stops on the default {DEFAULT_MIN_CHANGE}s change: {}",
        r.default_change_stops
    );
    let zero = tt.min_change.iter().filter(|&&c| c == 0).count();
    line!(out, "stops with a 0s change: {zero}");
    let footpaths: usize = tt.footpaths.iter().map(Vec::len).sum();
    line!(out, "footpaths: {footpaths}");
    line!(
        out,
        "asymmetric footpaths: {} {:?}",
        r.asymmetric_footpaths.len(),
        &r.asymmetric_footpaths[..r.asymmetric_footpaths.len().min(EXAMPLES)]
    );
    line!(
        out,
        "unclosed footpaths: {} {:?}",
        r.unclosed_footpaths.len(),
        &r.unclosed_footpaths[..r.unclosed_footpaths.len().min(EXAMPLES)]
    );
    out
}

pub fn journeys(tt: &Timetable, legs: &Legs, journeys: &[Journey]) -> String {
    let mut out = String::new();
    if journeys.is_empty() {
        line!(out, "no journey");
    }
    let name = |s: u32| {
        let stop = &tt.stops[s as usize];
        format!("{} ({})", stop.name, stop.id)
    };
    for j in journeys {
        line!(
            out,
            "depart {}, {} rides, arrive {} ({} min)",
            hms(j.depart),
            j.rides(),
            hms(j.arrive),
            (j.arrive - j.depart) / 60
        );
        for leg in legs.of(j) {
            match *leg {
                Leg::Ride(r) => line!(
                    out,
                    "  {} {} {} -> {} {}",
                    tt.patterns[r.pattern as usize].route_id,
                    hms(r.depart(tt)),
                    name(r.board_stop(tt)),
                    hms(r.arrive(tt)),
                    name(r.alight_stop(tt)),
                ),
                Leg::Walk { from, to, duration } => {
                    line!(out, "  walk {}s {} -> {}", duration, name(from), name(to))
                }
            }
        }
    }
    out
}

pub fn od(complexes: &Complexes, rows: &[OdRow]) -> String {
    let mut out = String::new();
    let total = riders(rows.iter());
    let origins: BTreeSet<_> = rows.iter().map(|r| r.origin).collect();
    let destinations: BTreeSet<_> = rows.iter().map(|r| r.destination).collect();
    let hours: BTreeSet<_> = rows.iter().map(|r| r.hour).collect();
    line!(out, "rows: {}", rows.len());
    line!(out, "riders: {total:.4}");
    line!(
        out,
        "origins: {}, destinations: {}, hours: {hours:?}",
        origins.len(),
        destinations.len()
    );
    line!(
        out,
        "stops not in the timetable: {:?}",
        complexes.unknown_stops
    );
    line!(
        out,
        "stops not served on the date: {:?}",
        complexes.unserved_stops
    );
    let stopless = |c: &ComplexId| complexes.stops.get(c).is_none_or(Vec::is_empty);
    let unmapped: BTreeSet<_> = origins
        .iter()
        .chain(&destinations)
        .filter(|c| stopless(c))
        .collect();
    let unmapped_riders = riders(
        rows.iter()
            .filter(|r| stopless(&r.origin) || stopless(&r.destination)),
    );
    line!(
        out,
        "complexes with no served stop: {unmapped:?} ({unmapped_riders:.4} riders)"
    );
    let same = riders(rows.iter().filter(|r| r.origin == r.destination));
    line!(
        out,
        "riders with the same origin and destination: {same:.4}"
    );
    out
}

/// Not `Sum`, which gives -0.0 for nothing.
pub fn riders<'a>(rows: impl Iterator<Item = &'a OdRow>) -> f64 {
    rows.fold(0.0, |sum, r| sum + r.riders.to_f64())
}

pub fn assigned(paths: &[PathRow]) -> f64 {
    paths.iter().fold(0.0, |sum, p| sum + p.riders.to_f64())
}

/// How long each stage took.
/// Loading and routing may be shared with other dates on a timetable routing alike.
pub struct Timings {
    pub loaded: Duration,
    pub routed: Duration,
    /// How many dates shared the routing.
    pub dates: usize,
    pub split: Duration,
}

pub fn assignment(
    rows: &[OdRow],
    paths: &[PathRow],
    unassigned: &Unassigned,
    timings: &Timings,
) -> String {
    let mut out = String::new();
    line!(out, "loaded in {:.1?}", timings.loaded);
    line!(
        out,
        "routed in {:.1?}, for {} date(s)",
        timings.routed,
        timings.dates
    );
    line!(out, "split in {:.1?}", timings.split);
    line!(out, "{} paths", paths.len());
    let input = riders(rows.iter());
    let assigned = assigned(paths);
    line!(
        out,
        "riders: {input:.4} in, {assigned:.4} assigned, {:.4} unassigned",
        unassigned.total()
    );
    line!(
        out,
        "  unassigned: {:.4} no served stop, {:.4} unreachable in {} rides, {:.4} after the last departure",
        unassigned.no_stops,
        unassigned.unreachable,
        MAX_RIDES,
        unassigned.no_departure
    );
    // Not exactly 0: each path's riders are rounded to a ten-thousandth, as written,
    // and the many paths with only a sliver of a row's riders round down,
    // ~2 riders a date.
    line!(
        out,
        "  conservation error: {:.6} (paths' riders rounded to 0.0001)",
        input - assigned - unassigned.total()
    );
    let mut by_rides = [0.0; MAX_RIDES + 1];
    let mut minutes = 0.0;
    for p in paths {
        by_rides[p.rides as usize] += p.riders.to_f64();
        minutes += p.riders.to_f64() * f64::from(p.total()) / 60.0;
    }
    for (k, r) in by_rides.iter().enumerate().skip(1) {
        line!(out, "  {k} rides: {:.1}%", 100.0 * r / assigned);
    }
    line!(out, "  mean journey: {:.1} min", minutes / assigned);
    out
}
