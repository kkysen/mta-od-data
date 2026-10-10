//! Splits each OD row's riders across its Pareto-optimal journeys.
//!
//! Phase 6 of `raptor_design.md`.
//! Riders enter uniformly over their row's hour.
//! A rider entering at `t` chooses among the Pareto set over (arrival, rides)
//! of journeys departing at or after `t`, by logit over generalized cost.
//! That set only changes at a departure,
//! and every journey's cost depends on `t` the same way (waiting longer at the origin),
//! so the shares are constant between consecutive departures.

use std::collections::BTreeMap;
use std::ops::Index;
use std::path::Path;

use anyhow::{Context, Result};
use parquet::file::properties::DEFAULT_MAX_ROW_GROUP_ROW_COUNT;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use rustc_hash::FxHashMap;
use serde::Deserialize;

use crate::gtfs::{DAY, Secs};
use crate::od::{ComplexId, Complexes, OdRow, Riders};
use crate::raptor::{Journey, Leg, MAX_RIDES, Router};
use crate::timetable::{NEXT_DATE_HORIZON, StopIdx, Timetable};

const HOUR: Secs = 60 * 60;

#[derive(Clone, Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Config {
    pub wait_weight: f64,
    pub walk_weight: f64,
    pub transfer_penalty_min: f64,
    pub logit_scale_per_min: f64,
    #[serde(default)]
    pub transfers: Transfers,
}

/// Where transfer times come from.
#[derive(Clone, Copy, Debug, Default, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum Transfers {
    /// `transfers.txt` at its word (`Timetable::build`).
    #[default]
    Gtfs,
    /// `nycriders`' rules (`Timetable::use_walk_distance_transfers`).
    WalkDistance,
}

impl Config {
    pub fn load(path: &Path) -> Result<(Self, String)> {
        let text =
            std::fs::read_to_string(path).with_context(|| format!("reading {}", path.display()))?;
        let config =
            json5::from_str(&text).with_context(|| format!("parsing {}", path.display()))?;
        Ok((config, text))
    }
}

/// One path an OD row's riders take, over every departure in the hour.
#[derive(Clone, Debug, PartialEq)]
pub struct PathRow {
    pub hour: u8,
    pub origin: ComplexId,
    pub destination: ComplexId,
    /// Rides as `<route> <board stop>><each stop passed>><alight stop>`
    /// and walks as `walk <from>><to>`,
    /// joined by ` | `, with GTFS stop IDs.
    /// Every stop a ride passes is there,
    /// so riders on a stretch of track can be found
    /// whatever their origin and destination.
    /// Its text is in the assignment's `PathTexts`.
    pub path: PathId,
    pub rides: u8,
    /// Rounded as the path Parquet stores it.
    pub riders: Riders,
    /// Averages over the row's riders on this path, in whole seconds,
    /// as the path Parquet stores them.
    pub wait: u32,
    pub in_vehicle: u32,
    pub walk: u32,
}

impl PathRow {
    /// Seconds from entering the origin to leaving the train at the destination.
    pub fn total(&self) -> u32 {
        self.wait + self.in_vehicle + self.walk
    }
}

/// Riders not assigned, by why.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Unassigned {
    /// The origin or destination complex has no served stop.
    pub no_stops: f64,
    /// No journey within `MAX_RIDES` rides departs that day.
    pub unreachable: f64,
    /// Entering after the day's last journey departs.
    pub no_departure: f64,
}

impl Unassigned {
    fn add(&mut self, other: &Self) {
        self.no_stops += other.no_stops;
        self.unreachable += other.unreachable;
        self.no_departure += other.no_departure;
    }

    pub fn total(&self) -> f64 {
        self.no_stops + self.unreachable + self.no_departure
    }
}

pub fn assign(
    tt: &Timetable,
    complexes: &Complexes,
    rows: &[OdRow],
    config: &Config,
) -> (Vec<PathRow>, PathTexts, Unassigned) {
    let router = Router::new(tt);
    let mut by_origin: BTreeMap<ComplexId, Vec<&OdRow>> = BTreeMap::new();
    for row in rows {
        by_origin.entry(row.origin).or_default().push(row);
    }
    let results: Vec<_> = by_origin
        .par_iter()
        .map(|(&origin, rows)| assign_origin(tt, &router, complexes, origin, rows, config))
        .collect();

    let mut paths = Vec::new();
    let mut texts = PathTexts::default();
    let mut unassigned = Unassigned::default();
    for (p, t, u) in results {
        // Each origin's ids index its own texts, so they move up past those before them.
        // No two origins share a path: each starts at its own origin's stops.
        let offset = u32::try_from(texts.0.len()).expect("under 2^32 paths");
        paths.extend(p.into_iter().map(|row| PathRow {
            path: PathId(row.path.0 + offset),
            ..row
        }));
        texts.0.extend(t.0);
        unassigned.add(&u);
    }
    // `rayon` doesn't fix the order.
    paths.sort_by(|a, b| {
        (a.origin, a.destination, a.hour, &texts[a.path]).cmp(&(
            b.origin,
            b.destination,
            b.hour,
            &texts[b.path],
        ))
    });
    (paths, texts, unassigned)
}

/// A path's index in its assignment's `PathTexts`:
/// a date has ~1.5M distinct paths, so `u32`, not `u16`.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct PathId(u32);

/// Each path's text, by `PathId`.
#[derive(Debug, Default)]
pub struct PathTexts(Vec<Box<str>>);

impl Index<PathId> for PathTexts {
    type Output = str;

    fn index(&self, id: PathId) -> &str {
        &self.0[id.0 as usize]
    }
}

fn stops_of(complexes: &Complexes, c: ComplexId) -> &[u32] {
    complexes.stops.get(&c).map_or(&[], Vec::as_slice)
}

fn assign_origin(
    tt: &Timetable,
    router: &Router,
    complexes: &Complexes,
    origin: ComplexId,
    rows: &[&OdRow],
    config: &Config,
) -> (Vec<PathRow>, PathTexts, Unassigned) {
    let mut unassigned = Unassigned::default();
    let origin_stops = stops_of(complexes, origin);
    let mut destinations: Vec<ComplexId> = rows.iter().map(|r| r.destination).collect();
    destinations.sort_unstable();
    destinations.dedup();
    let targets: Vec<&[u32]> = destinations
        .iter()
        .map(|&d| stops_of(complexes, d))
        .collect();
    let profiles = if origin_stops.is_empty() {
        vec![Vec::new(); targets.len()]
    } else {
        // Through the next date's early trips, for riders entering late.
        router.profile(origin_stops, 0, DAY + NEXT_DATE_HORIZON, &targets)
    };
    // An origin's journeys mostly repeat a few paths, departure after departure.
    let mut paths = Paths::default();
    // Each destination's journeys are dropped once its intervals are built.
    let intervals: FxHashMap<ComplexId, Vec<Interval>> = destinations
        .iter()
        .zip(profiles)
        .map(|(&d, journeys)| (d, intervals(tt, &mut paths, &journeys, config)))
        .collect();
    // Drops the interner's maps now, not at the end of the function.
    let Paths { texts, .. } = paths;

    let mut paths = Vec::new();
    for row in rows {
        if origin_stops.is_empty() || stops_of(complexes, row.destination).is_empty() {
            unassigned.no_stops += row.riders.to_f64();
            continue;
        }
        let intervals = &intervals[&row.destination];
        if intervals.is_empty() {
            unassigned.unreachable += row.riders.to_f64();
            continue;
        }
        let (row_paths, assigned) = assign_row(row, intervals);
        unassigned.no_departure += row.riders.to_f64() * (1.0 - assigned);
        paths.extend(row_paths);
    }
    (paths, texts, unassigned)
}

/// Riders entering in `(after, until]` choose among the same journeys.
struct Interval {
    after: Secs,
    until: Secs,
    choices: Vec<Choice>,
}

struct Choice {
    path: PathId,
    rides: u8,
    share: f64,
    arrive: Secs,
    in_vehicle: Secs,
    walk: Secs,
}

/// The choice intervals of one OD pair's profile (latest departure first),
/// earliest first.
fn intervals(
    tt: &Timetable,
    paths: &mut Paths,
    journeys: &[Journey],
    config: &Config,
) -> Vec<Interval> {
    let mut intervals = Vec::new();
    // The latest journey seen per ride count:
    // the earliest arriving of those departing at or after the current departure,
    // since the profile dropped any arriving no earlier than a later one.
    let mut latest: [Option<&Journey>; MAX_RIDES + 1] = [None; MAX_RIDES + 1];
    let mut i = 0;
    while i < journeys.len() {
        let depart = journeys[i].depart;
        while i < journeys.len() && journeys[i].depart == depart {
            latest[journeys[i].rides()] = Some(&journeys[i]);
            i += 1;
        }
        let after = journeys.get(i).map_or(Secs::MIN, |j| j.depart);
        // Pareto over (arrival, rides): each arriving before every one with fewer rides.
        let mut candidates = Vec::new();
        let mut fewer = Secs::MAX;
        for j in latest.iter().flatten() {
            if j.arrive < fewer {
                fewer = j.arrive;
                candidates.push(*j);
            }
        }
        intervals.push(Interval {
            after,
            until: depart,
            choices: choices(tt, paths, &candidates, depart, config),
        });
    }
    intervals.reverse();
    intervals
}

/// Each candidate's share, by logit over generalized cost for a rider entering at `t`.
fn choices(
    tt: &Timetable,
    paths: &mut Paths,
    candidates: &[&Journey],
    t: Secs,
    config: &Config,
) -> Vec<Choice> {
    let mut choices: Vec<Choice> = candidates
        .iter()
        .map(|j| {
            let (in_vehicle, walk) = in_vehicle_and_walk(tt, j);
            Choice {
                path: paths.get(tt, j),
                rides: j.rides() as u8,
                share: 0.0,
                arrive: j.arrive,
                in_vehicle,
                walk,
            }
        })
        .collect();
    let cost = |o: &Choice| {
        let wait = (o.arrive - t - o.in_vehicle - o.walk) as f64;
        (o.in_vehicle as f64 + config.wait_weight * wait + config.walk_weight * o.walk as f64)
            / 60.0
            + config.transfer_penalty_min * f64::from(o.rides - 1)
    };
    let costs: Vec<f64> = choices.iter().map(cost).collect();
    let min = costs.iter().copied().fold(f64::INFINITY, f64::min);
    let weights: Vec<f64> = costs
        .iter()
        .map(|c| (-config.logit_scale_per_min * (c - min)).exp())
        .collect();
    let sum: f64 = weights.iter().sum();
    for (c, w) in choices.iter_mut().zip(weights) {
        c.share = w / sum;
    }
    choices
}

/// Time on trains, and walking: footpaths,
/// plus each same-stop change's minimum change time.
fn in_vehicle_and_walk(tt: &Timetable, j: &Journey) -> (Secs, Secs) {
    let (mut in_vehicle, mut walk) = (0, 0);
    let mut alighted_at = None;
    for leg in &j.legs {
        match *leg {
            Leg::Ride(r) => {
                let board_stop = r.board_stop(tt);
                if alighted_at == Some(board_stop) {
                    walk += tt.min_change[board_stop as usize];
                }
                in_vehicle += r.arrive(tt) - r.depart(tt);
                alighted_at = Some(r.alight_stop(tt));
            }
            Leg::Walk { duration, .. } => {
                walk += duration;
                alighted_at = None;
            }
        }
    }
    (in_vehicle, walk)
}

/// A leg, as far as its path's text goes.
#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum LegKey {
    Ride {
        pattern: u32,
        board_pos: u16,
        alight_pos: u16,
    },
    Walk {
        from: StopIdx,
        to: StopIdx,
    },
}

/// An origin's paths, interned:
/// each journey's text built once, and each text given one `PathId`.
#[derive(Default)]
struct Paths {
    by_legs: FxHashMap<Box<[LegKey]>, PathId>,
    /// The journey being looked up's key, reused:
    /// most lookups find their path, so they allocate nothing.
    key: Vec<LegKey>,
    // Different legs can read the same, e.g. two patterns of a route over the same stops.
    by_text: FxHashMap<Box<str>, PathId>,
    texts: PathTexts,
}

impl Paths {
    fn get(&mut self, tt: &Timetable, j: &Journey) -> PathId {
        let Self {
            by_legs,
            key,
            by_text,
            texts,
        } = self;
        key.clear();
        key.extend(j.legs.iter().map(|leg| match *leg {
            Leg::Ride(r) => LegKey::Ride {
                pattern: r.pattern,
                board_pos: r.board_pos,
                alight_pos: r.alight_pos,
            },
            Leg::Walk { from, to, .. } => LegKey::Walk { from, to },
        }));
        if let Some(&id) = by_legs.get(key.as_slice()) {
            return id;
        }
        let text: Box<str> = path(tt, j).into();
        let id = *by_text.entry(text.clone()).or_insert_with(|| {
            let id = PathId(u32::try_from(texts.0.len()).expect("under 2^32 paths"));
            texts.0.push(text);
            id
        });
        by_legs.insert(key.as_slice().into(), id);
        id
    }
}

fn path(tt: &Timetable, j: &Journey) -> String {
    let id = |s: u32| tt.stops[s as usize].id.as_str();
    j.legs
        .iter()
        .map(|leg| match *leg {
            Leg::Ride(r) => {
                let pattern = &tt.patterns[r.pattern as usize];
                let stops = pattern.stops[usize::from(r.board_pos)..=usize::from(r.alight_pos)]
                    .iter()
                    .map(|&s| id(s))
                    .collect::<Vec<_>>()
                    .join(">");
                format!("{} {stops}", pattern.route_id)
            }
            Leg::Walk { from, to, .. } => format!("walk {}>{}", id(from), id(to)),
        })
        .collect::<Vec<_>>()
        .join(" | ")
}

/// One row's paths, and the share of its riders assigned:
/// short of 1 by those entering after the last departure.
fn assign_row(row: &OdRow, intervals: &[Interval]) -> (Vec<PathRow>, f64) {
    let (start, end) = (Secs::from(row.hour) * HOUR, Secs::from(row.hour + 1) * HOUR);
    #[derive(Default)]
    struct Acc {
        rides: u8,
        share: f64,
        wait: f64,
        in_vehicle: f64,
        walk: f64,
    }
    let mut accs: BTreeMap<PathId, Acc> = BTreeMap::new();
    let mut assigned = 0.0;
    for interval in intervals {
        let (lo, hi) = (interval.after.max(start), interval.until.min(end));
        if lo >= hi {
            continue;
        }
        let weight = f64::from(hi - lo) / f64::from(HOUR);
        let mid = f64::from(lo + hi) / 2.0;
        assigned += weight;
        for o in &interval.choices {
            let share = weight * o.share;
            let acc = accs.entry(o.path).or_default();
            acc.rides = o.rides;
            acc.share += share;
            acc.wait += share * (f64::from(o.arrive) - mid - f64::from(o.in_vehicle + o.walk));
            acc.in_vehicle += share * f64::from(o.in_vehicle);
            acc.walk += share * f64::from(o.walk);
        }
    }
    let paths = accs
        .into_iter()
        .map(|(path, a)| PathRow {
            hour: row.hour,
            origin: row.origin,
            destination: row.destination,
            path,
            rides: a.rides,
            riders: Riders::from_f64(a.share * row.riders.to_f64()),
            wait: (a.wait / a.share).round() as u32,
            in_vehicle: (a.in_vehicle / a.share).round() as u32,
            walk: (a.walk / a.share).round() as u32,
        })
        .collect();
    (paths, assigned)
}

/// Riders' precision in the path Parquet: the OD Parquet's `DECIMAL(9,4)`.
const RIDERS_PRECISION: u8 = 9;

/// Rows per row group of the path Parquet: the `parquet` crate's default.
const ROW_GROUP_SIZE: usize = DEFAULT_MAX_ROW_GROUP_ROW_COUNT;

/// Writes path rows as zstd Parquet, with `metadata` as its key-value metadata.
///
/// Riders as the OD Parquet's `DECIMAL(9,4)` and times as whole seconds:
/// a split rider count or an averaged time uses every bit of an `f64`,
/// which barely compresses.
/// No share or total time: riders over the OD row's, and the times' sum.
pub fn write_paths(
    out: &Path,
    paths: &[PathRow],
    texts: &PathTexts,
    date: jiff::civil::Date,
    metadata: Vec<(String, String)>,
) -> Result<()> {
    use std::sync::Arc;

    use arrow_array::{
        ArrayRef, Decimal128Array, DictionaryArray, RecordBatch, StringArray, UInt8Array,
        UInt16Array, UInt32Array, types::UInt32Type,
    };
    use parquet::arrow::ArrowWriter;
    use parquet::basic::{Compression, ZstdLevel};
    use parquet::file::metadata::KeyValue;
    use parquet::file::properties::WriterProperties;

    // Each path's text once, shared by every chunk's dictionary.
    let texts: ArrayRef = Arc::new(StringArray::from_iter_values(texts.0.iter().map(|t| &**t)));
    let batch = |paths: &[PathRow]| -> Result<RecordBatch> {
        let n = paths.len();
        let seconds = |f: fn(&PathRow) -> u32| -> ArrayRef {
            Arc::new(UInt32Array::from_iter_values(paths.iter().map(f)))
        };
        let riders =
            Decimal128Array::from_iter_values(paths.iter().map(|p| i128::from(p.riders.0)))
                .with_precision_and_scale(RIDERS_PRECISION, Riders::SCALE)?;
        Ok(RecordBatch::try_from_iter([
            (
                "year",
                Arc::new(UInt16Array::from(vec![date.year() as u16; n])) as ArrayRef,
            ),
            (
                "month",
                Arc::new(UInt8Array::from(vec![date.month() as u8; n])),
            ),
            (
                "day_of_week",
                Arc::new(StringArray::from(vec![crate::od::day_of_week(date); n])),
            ),
            (
                "hour",
                Arc::new(UInt8Array::from_iter_values(paths.iter().map(|p| p.hour))),
            ),
            (
                "origin",
                Arc::new(UInt32Array::from_iter_values(
                    paths.iter().map(|p| u32::from(p.origin)),
                )),
            ),
            (
                "destination",
                Arc::new(UInt32Array::from_iter_values(
                    paths.iter().map(|p| u32::from(p.destination)),
                )),
            ),
            (
                "path",
                Arc::new(DictionaryArray::<UInt32Type>::try_new(
                    UInt32Array::from_iter_values(paths.iter().map(|p| p.path.0)),
                    Arc::clone(&texts),
                )?),
            ),
            (
                "rides",
                Arc::new(UInt8Array::from_iter_values(paths.iter().map(|p| p.rides))),
            ),
            ("riders", Arc::new(riders)),
            ("wait_s", seconds(|p| p.wait)),
            ("in_vehicle_s", seconds(|p| p.in_vehicle)),
            ("walk_s", seconds(|p| p.walk)),
        ])?)
    };
    let props = WriterProperties::builder()
        .set_compression(Compression::ZSTD(ZstdLevel::try_new(3)?))
        .set_key_value_metadata(Some(
            metadata
                .into_iter()
                .map(|(k, v)| KeyValue::new(k, v))
                .collect(),
        ))
        .build();
    if let Some(dir) = out.parent() {
        std::fs::create_dir_all(dir)?;
    }
    let file = std::fs::File::create(out).with_context(|| format!("creating {}", out.display()))?;
    // A chunk of rows at a time, not all of a date's ~5.7M at once:
    // its arrays took ~500 MB.
    // One chunk per row group, as the writer would split them anyway.
    let mut chunks = paths.chunks(ROW_GROUP_SIZE);
    let first = batch(chunks.next().unwrap_or_default())?;
    let mut writer = ArrowWriter::try_new(file, first.schema(), Some(props))?;
    writer.write(&first)?;
    for chunk in chunks {
        writer.write(&batch(chunk)?)?;
    }
    writer.close()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use jiff::civil::Date;

    use super::*;
    use crate::gtfs::Feed;

    const STOPS: &str = "stop_id,stop_name\nA,A\nB,B\nC,C\nD,D\n";
    const CALENDAR: &str = "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
        W,1,1,1,1,1,1,1,20250101,20251231\n";
    const NEUTRAL: Config = Config {
        wait_weight: 1.0,
        walk_weight: 1.0,
        transfer_penalty_min: 0.0,
        logit_scale_per_min: 0.2,
        transfers: Transfers::Gtfs,
    };

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

    /// Complex `i` is stop `i` alone, and complex 9 has no stops.
    fn complexes(tt: &Timetable) -> Complexes {
        Complexes {
            stops: (0..tt.stops.len() as u32)
                .map(|s| (s as ComplexId, vec![s]))
                .chain([(9, vec![])])
                .collect(),
            unknown_stops: Vec::new(),
            unserved_stops: Vec::new(),
        }
    }

    fn row(origin: ComplexId, destination: ComplexId) -> OdRow {
        OdRow {
            hour: 8,
            origin,
            destination,
            riders: Riders::from_f64(60.0),
        }
    }

    const NO_TRANSFERS: &str = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\n";

    #[test]
    fn riders_spread_over_departures_in_the_hour() {
        // A to C at 08:10 and 08:40; riders entering after 08:40 have no train.
        let trips = "route_id,trip_id,service_id\n1,t1,W\n1,t2,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            t1,A,08:10:00,08:10:00,1\nt1,C,08:30:00,08:30:00,2\n\
            t2,A,08:40:00,08:40:00,1\nt2,C,09:00:00,09:00:00,2\n";
        let tt = timetable(trips, stop_times, NO_TRANSFERS);
        let (paths, texts, unassigned) = assign(&tt, &complexes(&tt), &[row(0, 2)], &NEUTRAL);

        assert_eq!(paths.len(), 1);
        let p = &paths[0];
        assert_eq!((&texts[p.path], p.rides), ("1 A>C", 1));
        assert_eq!(p.riders, Riders::from_f64(40.0));
        assert!((unassigned.no_departure - 20.0).abs() < 1e-9);
        // Waits average 5 min over the first 10 min, 15 over the next 30.
        assert_eq!(p.wait, (10 * 5 + 30 * 15) * 60 / 40);
        assert_eq!((p.in_vehicle, p.walk), (20 * 60, 0));
    }

    #[test]
    fn logit_split_across_the_pareto_set() {
        // At 08:10 from A: the 1 to C by 08:50,
        // or the 2 to B, a 60s change, and the 5 to C by 08:30.
        let trips = "route_id,trip_id,service_id\n1,slow,W\n2,feeder,W\n5,fast,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            slow,A,08:10:00,08:10:00,1\nslow,C,08:50:00,08:50:00,2\n\
            feeder,A,08:10:00,08:10:00,1\nfeeder,B,08:20:00,08:20:00,2\n\
            fast,B,08:21:00,08:21:00,1\nfast,C,08:30:00,08:30:00,2\n";
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,60\n";
        let tt = timetable(trips, stop_times, transfers);
        let (paths, texts, unassigned) = assign(&tt, &complexes(&tt), &[row(0, 2)], &NEUTRAL);

        let by_path: HashMap<_, _> = paths.iter().map(|p| (&texts[p.path], p)).collect();
        let (slow, fast) = (by_path["1 A>C"], by_path["2 A>B | 5 B>C"]);
        let (slow_riders, fast_riders) = (slow.riders.to_f64(), fast.riders.to_f64());
        // Only riders entering by 08:10 have a train: 1/6 of the hour,
        // each path's riders rounded to a ten-thousandth.
        assert!((slow_riders + fast_riders - 60.0 / 6.0).abs() <= 1e-4);
        assert!((unassigned.no_departure - 50.0).abs() < 1e-9);
        // Neutral weights: costs differ by the 20 min arrival difference.
        assert!((slow_riders / fast_riders - (-0.2f64 * 20.0).exp()).abs() < 1e-5);
        // The same-stop change is walk, not wait.
        assert_eq!(fast.walk, 60);
        assert_eq!(fast.in_vehicle, 19 * 60);
        // Entering at 08:05 on average, arriving 08:30.
        assert_eq!(fast.total(), 25 * 60);
        assert_eq!(fast.wait, 5 * 60);
    }

    #[test]
    fn transfer_penalty_shifts_riders_to_fewer_rides() {
        let trips = "route_id,trip_id,service_id\n1,slow,W\n2,feeder,W\n5,fast,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            slow,A,08:10:00,08:10:00,1\nslow,C,08:31:00,08:31:00,2\n\
            feeder,A,08:10:00,08:10:00,1\nfeeder,B,08:20:00,08:20:00,2\n\
            fast,B,08:21:00,08:21:00,1\nfast,C,08:30:00,08:30:00,2\n";
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,60\n";
        let tt = timetable(trips, stop_times, transfers);
        let riders = |config: &Config, path: &str| {
            let (paths, texts, _) = assign(&tt, &complexes(&tt), &[row(0, 2)], config);
            paths
                .iter()
                .find(|p| &texts[p.path] == path)
                .unwrap()
                .riders
        };
        // 1 min faster with a transfer: favored when transfers are free.
        assert!(riders(&NEUTRAL, "2 A>B | 5 B>C") > riders(&NEUTRAL, "1 A>C"));
        let penalized = Config {
            transfer_penalty_min: 5.0,
            ..NEUTRAL
        };
        assert!(riders(&penalized, "2 A>B | 5 B>C") < riders(&penalized, "1 A>C"));
    }

    #[test]
    fn path_lists_every_stop_passed() {
        let trips = "route_id,trip_id,service_id\n1,t1,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            t1,A,08:10:00,08:10:00,1\nt1,B,08:20:00,08:20:00,2\n\
            t1,C,08:30:00,08:30:00,3\nt1,D,08:40:00,08:40:00,4\n";
        let tt = timetable(trips, stop_times, NO_TRANSFERS);
        let (paths, texts, _) = assign(&tt, &complexes(&tt), &[row(0, 2)], &NEUTRAL);
        let paths: Vec<_> = paths.iter().map(|p| &texts[p.path]).collect();
        assert_eq!(paths, ["1 A>B>C"]);
    }

    #[test]
    fn unassigned_by_cause() {
        // A to C only: D is unreachable, and complex 9 has no stops.
        let trips = "route_id,trip_id,service_id\n1,t1,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            t1,A,08:10:00,08:10:00,1\nt1,C,08:30:00,08:30:00,2\n";
        let tt = timetable(trips, stop_times, NO_TRANSFERS);
        let rows = [row(0, 2), row(0, 3), row(0, 9), row(9, 2)];
        let (paths, _, unassigned) = assign(&tt, &complexes(&tt), &rows, &NEUTRAL);

        assert_eq!(unassigned.no_stops, 120.0);
        assert_eq!(unassigned.unreachable, 60.0);
        assert!((unassigned.no_departure - 50.0).abs() < 1e-9);
        // Every rider is assigned or counted as unassigned.
        let assigned: f64 = paths.iter().map(|p| p.riders.to_f64()).sum();
        assert!((assigned + unassigned.total() - 240.0).abs() <= 1e-4 * paths.len() as f64);
    }
}
