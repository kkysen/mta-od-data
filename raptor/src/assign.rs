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
use std::sync::atomic::{AtomicI64, AtomicU64, Ordering};

use anyhow::{Context, Result};
use parquet::basic::{Compression, Encoding, ZstdLevel};
use parquet::file::properties::{DEFAULT_MAX_ROW_GROUP_ROW_COUNT, WriterPropertiesBuilder};
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use rustc_hash::FxHashMap;
use serde::Deserialize;

use crate::gtfs::Secs;
use crate::od::{ComplexId, Complexes, OdRow, Riders};
use crate::raptor::{DEFAULT_MAX_RIDES, Journey, Leg, Legs, Router};
use crate::timetable::{DEPARTURES_UNTIL, Pattern, SERVICE_DAY_START, StopIdx, Timetable};

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
    /// Most rides in a journey.
    #[serde(default = "default_max_rides")]
    pub max_rides: usize,
}

fn default_max_rides() -> usize {
    DEFAULT_MAX_RIDES
}

/// Where transfer times come from.
#[derive(Clone, Copy, Debug, Default, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum Transfers {
    /// `transfers.txt` at its word (`Timetable::build`).
    #[default]
    Gtfs,
    /// Anita's rules (`Timetable::use_walk_distance_transfers`).
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
    /// Its text is in the routing's `PathTexts`,
    /// shared by every date routed with it.
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
    /// No journey within `Config::max_rides` rides departs that day.
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

/// Routes `rows`' OD pairs on `tt` and splits their riders: `route`, then `split`.
pub fn assign(
    tt: &Timetable,
    complexes: &Complexes,
    rows: &[OdRow],
    config: &Config,
) -> (Vec<PathRow>, PathTexts, Unassigned) {
    let routes = route(tt, complexes, config.max_rides);
    let (paths, unassigned) = split(&routes, complexes, rows, config, &TripLoads::new(tt));
    let texts = PathTexts(routes.texts().map(Box::from).collect());
    (paths, texts, unassigned)
}

/// Every origin's choice intervals to each of its destinations on one timetable.
/// They depend only on the timetable, not the config,
/// whose weights `split` applies, so any config splits over the same routes,
/// and dates whose timetables route alike share them.
pub struct Routes(BTreeMap<ComplexId, OriginRoutes>);

impl Routes {
    /// Every routed path's text, by `PathId`:
    /// each origin's after those of the origins before it.
    pub fn texts(&self) -> impl Iterator<Item = &str> {
        self.0.values().flat_map(|o| o.texts.0.iter().map(|t| &**t))
    }
}

pub struct OriginRoutes {
    intervals: FxHashMap<ComplexId, Intervals>,
    /// Indexed by this origin's own ids, which `offset` turns into `Routes`'.
    texts: PathTexts,
    /// Each choice's legs, by its `LegsId`, and the path they read as:
    /// two patterns over the same stops are one path but different legs,
    /// and a ride's train is a trip of its legs' pattern.
    legs: AllLegs,
    offset: u32,
}

/// An origin's choices' legs, each with its path, all in one `Vec`:
/// a `Box` each was ~7M allocations a timetable.
#[derive(Default)]
struct AllLegs {
    /// Each `LegsId`'s path, and where its legs end in `legs`.
    ends: Vec<(PathId, u32)>,
    legs: Vec<LegKey>,
}

impl AllLegs {
    fn push(&mut self, path: PathId, legs: &[LegKey]) -> LegsId {
        let id = LegsId(u32::try_from(self.ends.len()).expect("under 2^32 legs"));
        self.legs.extend_from_slice(legs);
        let end = u32::try_from(self.legs.len()).expect("under 2^32 legs");
        self.ends.push((path, end));
        id
    }

    fn path(&self, id: LegsId) -> PathId {
        self.ends[id.0 as usize].0
    }

    /// `id`'s legs, in order.
    fn legs(&self, id: LegsId) -> &[LegKey] {
        let i = id.0 as usize;
        let start = i.checked_sub(1).map_or(0, |i| self.ends[i].1) as usize;
        &self.legs[start..self.ends[i].1 as usize]
    }

    /// `id`'s rides' patterns and board and alight positions, in order.
    fn rides(&self, id: LegsId) -> impl Iterator<Item = (u32, u16, u16)> {
        self.legs(id).iter().filter_map(|leg| match *leg {
            LegKey::Ride {
                pattern,
                board_pos,
                alight_pos,
            } => Some((pattern, board_pos, alight_pos)),
            LegKey::Walk { .. } => None,
        })
    }
}

/// Riders boarding and alighting each train at each of its stops, over a date's rows,
/// and waiting on each platform each minute, in billionths of a rider.
/// Integers, added atomically from every origin's thread at once:
/// integer sums are the same in any order, as floating-point ones aren't.
pub struct TripLoads<'a> {
    tt: &'a Timetable,
    /// Each pattern's first slot and stop count: a trip's stops are consecutive slots.
    patterns: Vec<(usize, usize)>,
    on: Vec<AtomicU64>,
    off: Vec<AtomicU64>,
    /// Each pattern's stops' boardings' slots in `waits`:
    /// patterns boarding on the same route, way, and stop, to the same next stop, share one,
    /// since a platform is told by a route's trains between two stops.
    board_slots: Vec<Vec<u32>>,
    /// Each slot's first pattern and stop position boarding there.
    boardings: Vec<(u32, u16)>,
    waits: Waits,
}

/// Riders waiting to board each slot's trains at the start of each minute,
/// as differences, so a rider's whole wait is a few additions:
/// `steps` adds to the count from its minute on,
/// and `slopes` to how much it rises each minute from its minute on.
struct Waits {
    steps: Vec<AtomicI64>,
    slopes: Vec<AtomicI64>,
}

/// The minutes a platform's waits are counted over: the service day's clock,
/// through the last departure a journey can take.
pub const WAIT_MINUTES: usize = (DEPARTURES_UNTIL / 60) as usize + 4 * 60;

fn minute(t: Secs) -> usize {
    usize::try_from(t.div_euclid(60))
        .unwrap_or(0)
        .min(WAIT_MINUTES - 1)
}

impl Waits {
    fn new(slots: usize) -> Self {
        let zeros = || {
            (0..slots * WAIT_MINUTES)
                .map(|_| AtomicI64::new(0))
                .collect()
        };
        Self {
            steps: zeros(),
            slopes: zeros(),
        }
    }

    fn slot(platform: usize, t: Secs) -> usize {
        platform * WAIT_MINUTES + minute(t)
    }

    /// `nano` riders on `platform` from `from` until `until`.
    fn wait(&self, platform: usize, from: Secs, until: Secs, nano: i64) {
        if from >= until {
            return;
        }
        self.steps[Self::slot(platform, from)].fetch_add(nano, Ordering::Relaxed);
        self.steps[Self::slot(platform, until)].fetch_sub(nano, Ordering::Relaxed);
    }

    /// `nano` riders reaching `platform` evenly from `from` to `to`,
    /// and all waiting until `until`.
    fn ramp(&self, platform: usize, from: Secs, to: Secs, until: Secs, nano: i64) {
        let to = to.min(until);
        let (a, b) = (minute(from), minute(to));
        if a >= b {
            return self.wait(platform, to, until, nano);
        }
        let minutes = (b - a) as i64;
        let slope = nano / minutes;
        let first = platform * WAIT_MINUTES;
        self.slopes[first + a].fetch_add(slope, Ordering::Relaxed);
        self.slopes[first + b].fetch_sub(slope, Ordering::Relaxed);
        // What the slope's rounding left, so they're all there from `to`.
        self.steps[first + b].fetch_add(nano - slope * minutes, Ordering::Relaxed);
        self.steps[Self::slot(platform, until)].fetch_sub(nano, Ordering::Relaxed);
    }

    /// Each minute's riders waiting on `platform`, in billionths.
    fn at(&self, platform: usize) -> impl Iterator<Item = i64> + '_ {
        let first = platform * WAIT_MINUTES;
        let (mut count, mut rise, mut ramped) = (0i64, 0i64, 0i64);
        (0..WAIT_MINUTES).map(move |m| {
            ramped += rise;
            rise += self.slopes[first + m].load(Ordering::Relaxed);
            count += self.steps[first + m].load(Ordering::Relaxed);
            count + ramped
        })
    }
}

/// Billionths of a rider: an OD row's share on a choice is often well under 1e-4,
/// the riders' precision elsewhere, and rounding each to that would lose them.
pub const NANO: f64 = 1e9;

impl<'a> TripLoads<'a> {
    pub fn new(tt: &'a Timetable) -> Self {
        let mut patterns = Vec::with_capacity(tt.patterns.len());
        let mut slots = 0;
        for p in &tt.patterns {
            patterns.push((slots, p.stops.len()));
            slots += p.trips.len() * p.stops.len();
        }
        let zeros = || (0..slots).map(|_| AtomicU64::new(0)).collect();
        let mut by_key = FxHashMap::default();
        let mut boardings = Vec::new();
        let board_slots = tt
            .patterns
            .iter()
            .enumerate()
            .map(|(i, p)| {
                (0..p.stops.len().saturating_sub(1))
                    .map(|k| {
                        let key = (&p.route_id, p.direction_id, p.stops[k], p.stops[k + 1]);
                        *by_key.entry(key).or_insert_with(|| {
                            boardings.push((i as u32, k as u16));
                            (boardings.len() - 1) as u32
                        })
                    })
                    .collect()
            })
            .collect();
        Self {
            tt,
            patterns,
            on: zeros(),
            off: zeros(),
            waits: Waits::new(boardings.len()),
            board_slots,
            boardings,
        }
    }

    /// Where `pattern`'s riders board at `pos`.
    fn platform(&self, pattern: u32, pos: u16) -> usize {
        self.board_slots[pattern as usize][usize::from(pos)] as usize
    }

    /// `nano` riders entering evenly from `from` to `to` waiting for the trains of `legs`,
    /// on `trains`, and each transfer's riders waiting from reaching its platform.
    fn add_waits(&self, legs: &[LegKey], trains: &[Train], from: Secs, to: Secs, nano: u64) {
        let nano = i64::try_from(nano).expect("under 2^63 billionths");
        let mut trains = trains.iter();
        // Walked so far before the first ride, or when the last ride's riders are ready.
        let (mut walked, mut ready) = (0, None);
        for leg in legs {
            match *leg {
                LegKey::Ride {
                    pattern,
                    board_pos,
                    alight_pos,
                } => {
                    let train = *trains.next().expect("a train per ride");
                    let p = &self.tt.patterns[pattern as usize];
                    let times = &p.trips[usize::from(train)].times;
                    let depart = times[usize::from(board_pos)].1;
                    let platform = self.platform(pattern, board_pos);
                    match ready {
                        None => self
                            .waits
                            .ramp(platform, from + walked, to + walked, depart, nano),
                        Some(t) => self.waits.wait(platform, t, depart, nano),
                    }
                    ready = Some(times[usize::from(alight_pos)].0);
                }
                // Changing within a station isn't waiting time, as when it was one stop.
                LegKey::Walk { from, to } if self.tt.same_station(from, to) => {}
                LegKey::Walk { from, to } => {
                    let duration = self.tt.footpaths[from as usize]
                        .iter()
                        .find(|&&(s, _)| s == to)
                        .map_or(0, |&(_, d)| d);
                    match &mut ready {
                        None => walked += duration,
                        Some(t) => *t += duration,
                    }
                }
            }
        }
    }

    /// Riders waiting to board each minute, by where they board:
    /// `(pattern, its stop position, minute, billionths)`, only minutes with any.
    pub fn waits(&self) -> impl Iterator<Item = (&Pattern, usize, usize, i64)> + '_ {
        self.boardings
            .iter()
            .enumerate()
            .flat_map(move |(slot, &(pattern, pos))| {
                let p = &self.tt.patterns[pattern as usize];
                self.waits
                    .at(slot)
                    .enumerate()
                    .filter(|&(_, n)| n != 0)
                    .map(move |(m, n)| (p, usize::from(pos), m, n))
            })
    }

    fn slot(&self, pattern: usize, trip: usize, pos: usize) -> usize {
        let (first, stops) = self.patterns[pattern];
        first + trip * stops + pos
    }

    fn add(&self, (pattern, board, alight): (u32, u16, u16), train: Train, nano: u64) {
        let (pattern, train) = (pattern as usize, usize::from(train));
        let on = self.slot(pattern, train, board.into());
        let off = self.slot(pattern, train, alight.into());
        self.on[on].fetch_add(nano, Ordering::Relaxed);
        self.off[off].fetch_add(nano, Ordering::Relaxed);
    }

    /// Riders boarding and alighting `pattern`'s `trip` at `pos`, in billionths.
    pub fn at(&self, pattern: usize, trip: usize, pos: usize) -> (u64, u64) {
        let slot = self.slot(pattern, trip, pos);
        (
            self.on[slot].load(Ordering::Relaxed),
            self.off[slot].load(Ordering::Relaxed),
        )
    }
}

/// An origin's choice's legs, in its `OriginRoutes::legs`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct LegsId(u32);

/// Routes every pair of `complexes` on `tt`,
/// so any OD data on its dates splits over the same routes.
/// That's barely more than the OD data's own pairs, ~98% of them.
pub fn route(tt: &Timetable, complexes: &Complexes, max_rides: usize) -> Routes {
    let router = Router::with_max_rides(tt, max_rides);
    let ids: Vec<ComplexId> = complexes.stops.keys().copied().collect();
    let mut routes: BTreeMap<_, _> = ids
        .par_iter()
        .map(|&origin| {
            let routes = route_origin(tt, &router, complexes, origin, &ids);
            (origin, routes)
        })
        .collect();
    // No two origins share a path: each starts at its own origin's stops.
    let mut offset = 0u32;
    for o in routes.values_mut() {
        o.offset = offset;
        offset = offset
            .checked_add(u32::try_from(o.texts.0.len()).expect("under 2^32 paths"))
            .expect("under 2^32 paths");
    }
    Routes(routes)
}

/// Splits `rows`' riders over their journeys in `routes`,
/// by `config`'s weights.
/// Paths are `routes`' ids, so their texts are `Routes::texts`.
/// Each ride's riders are added to its train's boardings and alightings in `loads`.
pub fn split(
    routes: &Routes,
    complexes: &Complexes,
    rows: &[OdRow],
    config: &Config,
    loads: &TripLoads,
) -> (Vec<PathRow>, Unassigned) {
    let mut by_origin: BTreeMap<ComplexId, Vec<&OdRow>> = BTreeMap::new();
    for row in rows {
        by_origin.entry(row.origin).or_default().push(row);
    }
    let results: Vec<_> = by_origin
        .par_iter()
        .map(|(&origin, rows)| match routes.0.get(&origin) {
            Some(r) => split_origin(r, complexes, origin, rows, config, loads),
            // Not a complex in the station data, so it has no stops.
            None => (
                Vec::new(),
                Unassigned {
                    no_stops: rows.iter().map(|r| r.riders.to_f64()).sum(),
                    ..Unassigned::default()
                },
            ),
        })
        .collect();

    // `collect` keeps `by_origin`'s order, and each origin's rows come sorted,
    // so the rows are in (origin, destination, hour, path) order as they're appended.
    let mut paths = Vec::with_capacity(results.iter().map(|(p, _)| p.len()).sum());
    let mut unassigned = Unassigned::default();
    for (p, u) in results {
        paths.extend(p);
        unassigned.add(&u);
    }
    (paths, unassigned)
}

/// A path's index in its routing's `PathTexts`:
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

fn route_origin(
    tt: &Timetable,
    router: &Router,
    complexes: &Complexes,
    origin: ComplexId,
    destinations: &[ComplexId],
) -> OriginRoutes {
    let origin_stops = stops_of(complexes, origin);
    let targets: Vec<&[u32]> = destinations
        .iter()
        .map(|&d| stops_of(complexes, d))
        .collect();
    let (legs, profiles) = if origin_stops.is_empty() {
        (Legs::default(), vec![Vec::new(); targets.len()])
    } else {
        // Through the next date's early trips, for riders entering late.
        router.profile(origin_stops, SERVICE_DAY_START, DEPARTURES_UNTIL, &targets)
    };
    // An origin's journeys mostly repeat a few paths, departure after departure.
    let mut paths = Paths::default();
    // Each destination's journeys are dropped once its intervals are built,
    // and the origin's legs once every destination's are.
    let intervals = destinations
        .iter()
        .zip(profiles)
        .map(|(&d, journeys)| {
            let intervals = intervals(tt, router.max_rides(), &mut paths, &legs, &journeys);
            (d, intervals)
        })
        .collect();
    drop(legs);
    // Drops the interner's maps now, not when the routes are.
    let Paths { texts, legs, .. } = paths;
    OriginRoutes {
        intervals,
        texts,
        legs,
        offset: 0,
    }
}

fn split_origin(
    routes: &OriginRoutes,
    complexes: &Complexes,
    origin: ComplexId,
    rows: &[&OdRow],
    config: &Config,
    loads: &TripLoads,
) -> (Vec<PathRow>, Unassigned) {
    let mut unassigned = Unassigned::default();
    let origin_stops = stops_of(complexes, origin);
    let mut paths = Vec::new();
    let mut shares = Vec::new();
    for row in rows {
        if origin_stops.is_empty() || stops_of(complexes, row.destination).is_empty() {
            unassigned.no_stops += row.riders.to_f64();
            continue;
        }
        let intervals = &routes.intervals[&row.destination];
        if intervals.is_empty() {
            unassigned.unreachable += row.riders.to_f64();
            continue;
        }
        let (row_paths, assigned) =
            assign_row(row, intervals, &routes.legs, config, &mut shares, loads);
        unassigned.no_departure += row.riders.to_f64() * (1.0 - assigned);
        paths.extend(row_paths);
    }
    for p in &mut paths {
        p.path = PathId(p.path.0 + routes.offset);
    }
    // On this origin's thread, so `split` needn't sort all of a date's rows on one.
    // A path's hours together, not an hour's paths:
    // its rows then repeat its id, rides, and walk, which compress to almost nothing.
    paths.sort_by_key(|p| (p.destination, p.path, p.hour));
    (paths, unassigned)
}

/// One OD pair's choice intervals, earliest first:
/// riders entering in an interval `(after, until]` choose among the same journeys,
/// and each interval starts where the one before ends.
/// An OD pair has ~175 intervals of ~1.4 choices each,
/// so in flat arrays, not a `Vec` of choices per interval.
#[derive(Default)]
struct Intervals {
    /// Each interval's `until`, and where its choices end in `choices`:
    /// they start where the one before's end.
    ends: Vec<(Secs, u32)>,
    choices: Vec<Choice>,
    /// Each choice's rides' trains, its `rides` of them in order,
    /// as indices into their patterns' trips.
    /// Where an interval's start is summed from its choices' rides as they're iterated,
    /// not stored: 4 bytes for each of ~37M intervals a timetable.
    trains: Vec<Train>,
}

/// A trip's index in its pattern's: no pattern has near 2^16 trips
/// (`choices_into` checks), so half a `u32` for each of ~70M rides.
type Train = u16;

impl Intervals {
    fn is_empty(&self) -> bool {
        self.ends.is_empty()
    }

    /// Each interval's `(after, until, choices, their trains)`, earliest first.
    fn iter(&self) -> impl Iterator<Item = (Secs, Secs, &[Choice], &[Train])> {
        let (mut after, mut start, mut trains_start) = (Secs::MIN, 0, 0);
        self.ends.iter().map(move |&(until, end)| {
            let choices = &self.choices[start as usize..end as usize];
            let trains_end = trains_start + rides(choices);
            let interval = (
                after,
                until,
                choices,
                &self.trains[trains_start..trains_end],
            );
            (after, start, trains_start) = (until, end, trains_end);
            interval
        })
    }
}

fn rides(choices: &[Choice]) -> usize {
    choices.iter().map(|c| usize::from(c.rides)).sum()
}

#[derive(Clone, Copy)]
struct Choice {
    /// Its legs, in its origin's `OriginRoutes::legs`.
    legs: LegsId,
    rides: u8,
    arrive: Secs,
    in_vehicle: Secs,
    walk: Secs,
}

/// The choice intervals of one OD pair's profile (latest departure first).
fn intervals(
    tt: &Timetable,
    max_rides: usize,
    paths: &mut Paths,
    legs: &Legs,
    journeys: &[Journey],
) -> Intervals {
    // Built latest first, then reversed.
    let mut latest_first = Intervals::default();
    // The latest journey seen per ride count:
    // the earliest arriving of those departing at or after the current departure,
    // since the profile dropped any arriving no earlier than a later one.
    let mut latest: Vec<Option<&Journey>> = vec![None; max_rides + 1];
    let mut candidates = Vec::with_capacity(max_rides);
    let mut i = 0;
    while i < journeys.len() {
        let depart = journeys[i].depart;
        while i < journeys.len() && journeys[i].depart == depart {
            latest[journeys[i].rides()] = Some(&journeys[i]);
            i += 1;
        }
        // Pareto over (arrival, rides): each arriving before every one with fewer rides.
        candidates.clear();
        let mut fewer = Secs::MAX;
        for j in latest.iter().flatten() {
            if j.arrive < fewer {
                fewer = j.arrive;
                candidates.push(*j);
            }
        }
        let Intervals {
            choices, trains, ..
        } = &mut latest_first;
        choices_into(tt, paths, legs, &candidates, choices, trains);
        let end = u32::try_from(choices.len()).expect("under 2^32 choices");
        latest_first.ends.push((depart, end));
    }
    let mut intervals = Intervals {
        ends: Vec::with_capacity(latest_first.ends.len()),
        choices: Vec::with_capacity(latest_first.choices.len()),
        trains: Vec::with_capacity(latest_first.trains.len()),
    };
    // Each interval's trains, latest first, so they reverse with their choices.
    let trains: Vec<&[Train]> = latest_first.iter().map(|(_, _, _, t)| t).collect();
    for (k, &(until, end)) in latest_first.ends.iter().enumerate().rev() {
        let start = k.checked_sub(1).map_or(0, |k| latest_first.ends[k].1);
        let choices = &latest_first.choices[start as usize..end as usize];
        intervals.choices.extend_from_slice(choices);
        intervals.trains.extend_from_slice(trains[k]);
        intervals.ends.push((until, intervals.choices.len() as u32));
    }
    intervals
}

/// Appends each candidate's choice to `choices`, and its rides' trains to `trains`.
fn choices_into(
    tt: &Timetable,
    paths: &mut Paths,
    legs: &Legs,
    candidates: &[&Journey],
    choices: &mut Vec<Choice>,
    trains: &mut Vec<Train>,
) {
    choices.extend(candidates.iter().map(|j| {
        let (in_vehicle, walk) = in_vehicle_and_walk(tt, legs.of(j));
        trains.extend(legs.of(j).iter().filter_map(|leg| match *leg {
            Leg::Ride(r) => Some(Train::try_from(r.trip).expect("under 2^16 trips a pattern")),
            Leg::Walk { .. } => None,
        }));
        Choice {
            legs: paths.get(tt, legs.of(j)),
            rides: j.rides() as u8,
            arrive: j.arrive,
            in_vehicle,
            walk,
        }
    }));
}

/// Sets `shares` to each of `choices`' shares,
/// by logit over generalized cost for a rider entering at `t`.
fn shares_into(choices: &[Choice], t: Secs, config: &Config, shares: &mut Vec<f64>) {
    let cost = |o: &Choice| {
        let wait = (o.arrive - t - o.in_vehicle - o.walk) as f64;
        (o.in_vehicle as f64 + config.wait_weight * wait + config.walk_weight * o.walk as f64)
            / 60.0
            + config.transfer_penalty_min * f64::from(o.rides - 1)
    };
    // Each share holds its cost, then its weight, then its share.
    shares.clear();
    shares.extend(choices.iter().map(cost));
    let min = shares.iter().copied().fold(f64::INFINITY, f64::min);
    for s in shares.iter_mut() {
        *s = (-config.logit_scale_per_min * (*s - min)).exp();
    }
    let sum: f64 = shares.iter().sum();
    for s in shares.iter_mut() {
        *s /= sum;
    }
}

/// Time on trains, and walking: footpaths,
/// plus each same-stop change's minimum change time.
fn in_vehicle_and_walk(tt: &Timetable, legs: &[Leg]) -> (Secs, Secs) {
    let (mut in_vehicle, mut walk) = (0, 0);
    let mut alighted_at = None;
    for leg in legs {
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
    by_legs: FxHashMap<Box<[LegKey]>, LegsId>,
    legs: AllLegs,
    /// The journey being looked up's key, reused:
    /// most lookups find their path, so they allocate nothing.
    key: Vec<LegKey>,
    // Different legs can read the same, e.g. two patterns of a route over the same stops.
    by_text: FxHashMap<Box<str>, PathId>,
    texts: PathTexts,
}

impl Paths {
    fn get(&mut self, tt: &Timetable, legs: &[Leg]) -> LegsId {
        let Self {
            by_legs,
            legs: legs_of,
            key,
            by_text,
            texts,
        } = self;
        key.clear();
        key.extend(legs.iter().map(|leg| match *leg {
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
        let text: Box<str> = path(tt, legs).into();
        let id = *by_text.entry(text.clone()).or_insert_with(|| {
            let id = PathId(u32::try_from(texts.0.len()).expect("under 2^32 paths"));
            texts.0.push(text);
            id
        });
        let legs_id = legs_of.push(id, key);
        by_legs.insert(key.as_slice().into(), legs_id);
        legs_id
    }
}

/// A path's text, by station: a change within one is no leg, as when it was one stop.
fn path(tt: &Timetable, legs: &[Leg]) -> String {
    let id = |s: u32| tt.stops[s as usize].station.as_str();
    legs.iter()
        .filter(|leg| !matches!(**leg, Leg::Walk { from, to, .. } if tt.same_station(from, to)))
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
fn assign_row(
    row: &OdRow,
    intervals: &Intervals,
    legs: &AllLegs,
    config: &Config,
    shares: &mut Vec<f64>,
    loads: &TripLoads,
) -> (Vec<PathRow>, f64) {
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
    for (after, until, choices, trains) in intervals.iter() {
        let (lo, hi) = (after.max(start), until.min(end));
        if lo >= hi {
            continue;
        }
        let weight = f64::from(hi - lo) / f64::from(HOUR);
        let mid = f64::from(lo + hi) / 2.0;
        assigned += weight;
        // A rider entering in `(after, until]` chooses as one entering at `until`,
        // the departure that ends the interval.
        shares_into(choices, until, config, shares);
        let mut trains = trains;
        for (o, &s) in choices.iter().zip(shares.iter()) {
            let share = weight * s;
            let nano = (share * row.riders.to_f64() * NANO).round() as u64;
            let (these, rest) = trains.split_at(o.rides.into());
            trains = rest;
            if nano > 0 {
                for (ride, &train) in legs.rides(o.legs).zip(these) {
                    loads.add(ride, train, nano);
                }
                loads.add_waits(legs.legs(o.legs), these, lo, hi, nano);
            }
            let acc = accs.entry(legs.path(o.legs)).or_default();
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
/// Paths as their `path_id`s, whose texts `write_path_texts` writes
/// once for every date routed alike.
pub fn write_paths(
    out: &Path,
    paths: &[PathRow],
    date: jiff::civil::Date,
    metadata: Vec<(String, String)>,
    zstd_level: i32,
) -> Result<()> {
    use std::sync::Arc;

    use arrow_array::{
        ArrayRef, Decimal128Array, RecordBatch, StringArray, UInt8Array, UInt16Array, UInt32Array,
    };
    use parquet::arrow::ArrowWriter;

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
                "path_id",
                Arc::new(UInt32Array::from_iter_values(
                    paths.iter().map(|p| p.path.0),
                )),
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
    let file = create(out)?;
    // A chunk of rows at a time, not all of a date's ~5.7M at once:
    // its arrays took ~500 MB.
    // One chunk per row group, as the writer would split them anyway.
    let mut chunks = paths.chunks(ROW_GROUP_SIZE);
    let first = batch(chunks.next().unwrap_or_default())?;
    // Delta where consecutive rows' values are close, as sorted by `split`:
    // in-vehicle times included, but not waits or walks, which delta made bigger.
    // Riders too, ~7% smaller than plain
    // (byte stream split was smaller still, but DuckDB reads it only for floats).
    let mut props = properties(metadata, zstd_level)?;
    for column in [
        "hour",
        "destination",
        "path_id",
        "rides",
        "riders",
        "in_vehicle_s",
    ] {
        props = props.set_column_encoding(column.into(), Encoding::DELTA_BINARY_PACKED);
    }
    let props = props.build();
    let mut writer = ArrowWriter::try_new(file, first.schema(), Some(props))?;
    writer.write(&first)?;
    for chunk in chunks {
        writer.write(&batch(chunk)?)?;
    }
    writer.close()?;
    Ok(())
}

/// Writes every path `routes` routed, as `path_id` and `path` text,
/// for the path Parquets of each date split on them.
pub fn write_path_texts(
    out: &Path,
    routes: &Routes,
    metadata: Vec<(String, String)>,
    zstd_level: i32,
) -> Result<()> {
    use std::sync::Arc;

    use arrow_array::builder::StringBuilder;
    use arrow_array::{ArrayRef, RecordBatch, UInt32Array};
    use arrow_schema::{DataType, Field, Schema};
    use parquet::arrow::ArrowWriter;

    let schema = Arc::new(Schema::new(vec![
        Field::new("path_id", DataType::UInt32, false),
        Field::new("path", DataType::Utf8, false),
    ]));
    let props = properties(metadata, zstd_level)?
        // Ids count up by 1, so their deltas pack to nothing.
        .set_column_encoding("path_id".into(), Encoding::DELTA_BINARY_PACKED)
        .build();
    let mut writer = ArrowWriter::try_new(create(out)?, Arc::clone(&schema), Some(props))?;
    let mut id = 0u32;
    let texts: Vec<&str> = routes.texts().collect();
    for chunk in texts.chunks(ROW_GROUP_SIZE) {
        // Sized up front, not grown (and copied) as it goes.
        let bytes = chunk.iter().map(|t| t.len()).sum();
        let mut builder = StringBuilder::with_capacity(chunk.len(), bytes);
        for text in chunk {
            builder.append_value(text);
        }
        let n = chunk.len() as u32;
        let batch = RecordBatch::try_new(
            Arc::clone(&schema),
            vec![
                Arc::new(UInt32Array::from_iter_values(id..id + n)) as ArrayRef,
                Arc::new(builder.finish()),
            ],
        )?;
        id += n;
        writer.write(&batch)?;
    }
    writer.close()?;
    Ok(())
}

/// Writes each train's riders at each of its stops as zstd Parquet:
/// its trip (`trip_ids`, by pattern, the date's own),
/// route, direction, the service date it runs on relative to the timetable's,
/// each stop's position and GTFS parent stop ID (`127`: `direction_id` says which way),
/// scheduled arrival and departure (seconds from the timetable's date's noon less 12h),
/// riders boarding and alighting there, and riders on board as it leaves.
/// Riders are in billionths summed exactly, so each trip's load ends at exactly 0,
/// which this checks.
pub fn write_trips(
    out: &Path,
    tt: &Timetable,
    trip_ids: &[Vec<String>],
    loads: &TripLoads,
    metadata: Vec<(String, String)>,
    zstd_level: i32,
) -> Result<()> {
    use std::sync::Arc;

    use arrow_array::builder::{
        Float64Builder, Int8Builder, Int32Builder, StringBuilder, UInt8Builder, UInt16Builder,
    };
    use arrow_array::{ArrayRef, RecordBatch};
    use arrow_schema::{DataType, Field, Schema};
    use parquet::arrow::ArrowWriter;

    let schema = Arc::new(Schema::new(vec![
        Field::new("trip_id", DataType::Utf8, false),
        Field::new("route_id", DataType::Utf8, false),
        Field::new("direction_id", DataType::UInt8, true),
        Field::new("day", DataType::Int8, false),
        Field::new("stop_sequence", DataType::UInt16, false),
        Field::new("stop_id", DataType::Utf8, false),
        Field::new("arrival", DataType::Int32, false),
        Field::new("departure", DataType::Int32, false),
        Field::new("boardings", DataType::Float64, false),
        Field::new("alightings", DataType::Float64, false),
        Field::new("load", DataType::Float64, false),
    ]));
    let (mut trip, mut route, mut direction, mut day) = (
        StringBuilder::new(),
        StringBuilder::new(),
        UInt8Builder::new(),
        Int8Builder::new(),
    );
    let (mut seq, mut stop, mut arrival, mut departure) = (
        UInt16Builder::new(),
        StringBuilder::new(),
        Int32Builder::new(),
        Int32Builder::new(),
    );
    let (mut on, mut off, mut load) = (
        Float64Builder::new(),
        Float64Builder::new(),
        Float64Builder::new(),
    );
    for (p, (pattern, ids)) in tt.patterns.iter().zip(trip_ids).enumerate() {
        anyhow::ensure!(ids.len() == pattern.trips.len(), "a trip ID per trip");
        for (t, (times, id)) in pattern.trips.iter().zip(ids).enumerate() {
            let mut aboard: i128 = 0;
            for (k, (&s, &(arrive, depart))) in pattern.stops.iter().zip(&times.times).enumerate() {
                let (boarded, alighted) = loads.at(p, t, k);
                aboard += i128::from(boarded) - i128::from(alighted);
                anyhow::ensure!(aboard >= 0, "{id}: fewer riders than alight at {k}");
                trip.append_value(id);
                route.append_value(&pattern.route_id);
                direction.append_option(pattern.direction_id);
                day.append_value(times.day);
                seq.append_value(u16::try_from(k)?);
                stop.append_value(&tt.stops[s as usize].station);
                arrival.append_value(arrive);
                departure.append_value(depart);
                on.append_value(boarded as f64 / NANO);
                off.append_value(alighted as f64 / NANO);
                load.append_value(aboard as f64 / NANO);
            }
            anyhow::ensure!(
                aboard == 0,
                "{id}: {aboard} billionths still aboard at its end"
            );
        }
    }
    let batch = RecordBatch::try_new(
        Arc::clone(&schema),
        vec![
            Arc::new(trip.finish()) as ArrayRef,
            Arc::new(route.finish()),
            Arc::new(direction.finish()),
            Arc::new(day.finish()),
            Arc::new(seq.finish()),
            Arc::new(stop.finish()),
            Arc::new(arrival.finish()),
            Arc::new(departure.finish()),
            Arc::new(on.finish()),
            Arc::new(off.finish()),
            Arc::new(load.finish()),
        ],
    )?;
    let props = properties(metadata, zstd_level)?.build();
    let mut writer = ArrowWriter::try_new(create(out)?, schema, Some(props))?;
    writer.write(&batch)?;
    writer.close()?;
    Ok(())
}

/// Writes riders waiting to board at the start of each minute to `out`,
/// by where they board: the route, `direction_id`, GTFS parent stop ID,
/// and next stop's, which tell the platform;
/// the minute on the service day's clock (240 is 4 AM), and the riders waiting.
/// Riders entering wait from when they enter, evenly over their hour,
/// and transfers from when their last train reaches the stop, or they walk to it.
pub fn write_platform_waits(
    out: &Path,
    tt: &Timetable,
    loads: &TripLoads,
    metadata: Vec<(String, String)>,
    zstd_level: i32,
) -> Result<()> {
    use std::sync::Arc;

    use arrow_array::builder::{Float64Builder, StringBuilder, UInt8Builder, UInt16Builder};
    use arrow_array::{ArrayRef, RecordBatch};
    use arrow_schema::{DataType, Field, Schema};
    use parquet::arrow::ArrowWriter;

    let schema = Arc::new(Schema::new(vec![
        Field::new("route_id", DataType::Utf8, false),
        Field::new("direction_id", DataType::UInt8, true),
        Field::new("stop_id", DataType::Utf8, false),
        Field::new("next_stop", DataType::Utf8, false),
        Field::new("minute", DataType::UInt16, false),
        Field::new("riders", DataType::Float64, false),
    ]));
    let (mut route, mut direction, mut stop, mut next) = (
        StringBuilder::new(),
        UInt8Builder::new(),
        StringBuilder::new(),
        StringBuilder::new(),
    );
    let (mut minute, mut riders) = (UInt16Builder::new(), Float64Builder::new());
    for (p, k, m, nano) in loads.waits() {
        let id = |k: usize| &tt.stops[p.stops[k] as usize].station;
        anyhow::ensure!(nano > 0, "{nano} billionths waiting at {}", id(k));
        route.append_value(&p.route_id);
        direction.append_option(p.direction_id);
        stop.append_value(id(k));
        next.append_value(id(k + 1));
        minute.append_value(u16::try_from(m)?);
        riders.append_value(nano as f64 / NANO);
    }
    let batch = RecordBatch::try_new(
        Arc::clone(&schema),
        vec![
            Arc::new(route.finish()) as ArrayRef,
            Arc::new(direction.finish()),
            Arc::new(stop.finish()),
            Arc::new(next.finish()),
            Arc::new(minute.finish()),
            Arc::new(riders.finish()),
        ],
    )?;
    let props = properties(metadata, zstd_level)?.build();
    let mut writer = ArrowWriter::try_new(create(out)?, schema, Some(props))?;
    writer.write(&batch)?;
    writer.close()?;
    Ok(())
}

/// Creates `out` and its directory.
fn create(out: &Path) -> Result<std::fs::File> {
    if let Some(dir) = out.parent() {
        std::fs::create_dir_all(dir)?;
    }
    std::fs::File::create(out).with_context(|| format!("creating {}", out.display()))
}

/// The path Parquets' writer properties, with `metadata` as key-value metadata.
///
/// zstd at `zstd_level`: 1, the fastest, unless the files are to be kept.
/// Level 1 was a third faster to write than 3, for ~1% more.
/// The path texts barely shrink until level 5:
/// September's are 21 MB at 1 to 4, 14.5 MB at 6 (5 times as long to write),
/// and 13 MB at 9 (10 times as long).
fn properties(metadata: Vec<(String, String)>, zstd_level: i32) -> Result<WriterPropertiesBuilder> {
    use parquet::file::metadata::KeyValue;
    use parquet::file::properties::{EnabledStatistics, WriterProperties};

    Ok(WriterProperties::builder()
        .set_compression(Compression::ZSTD(ZstdLevel::try_new(zstd_level)?))
        // Dictionary encoding hashed every value of every column,
        // ~40% of writing, for ~3% smaller files than zstd alone.
        .set_dictionary_enabled(false)
        // Min and max path text are of no use, and comparing every path's took time.
        .set_column_statistics_enabled("path".into(), EnabledStatistics::None)
        .set_key_value_metadata(Some(
            metadata
                .into_iter()
                .map(|(k, v)| KeyValue::new(k, v))
                .collect(),
        )))
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
        max_rides: DEFAULT_MAX_RIDES,
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

    /// Riders waiting at `stop` each minute, by `TripLoads::waits`.
    fn waits_at(tt: &Timetable, rows: &[OdRow], stop: &str) -> BTreeMap<usize, f64> {
        let loads = TripLoads::new(tt);
        split(
            &route(tt, &complexes(tt), DEFAULT_MAX_RIDES),
            &complexes(tt),
            rows,
            &NEUTRAL,
            &loads,
        );
        loads
            .waits()
            .filter(|&(p, k, ..)| tt.stops[p.stops[k] as usize].station == stop)
            .map(|(_, _, m, n)| (m, n as f64 / NANO))
            .collect()
    }

    #[test]
    fn riders_wait_from_entering_until_their_train() {
        // A to C at 08:10 and 08:40, a rider entering each minute from 08:00.
        let trips = "route_id,trip_id,service_id\n1,t1,W\n1,t2,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            t1,A,08:10:00,08:10:00,1\nt1,C,08:30:00,08:30:00,2\n\
            t2,A,08:40:00,08:40:00,1\nt2,C,09:00:00,09:00:00,2\n";
        let tt = timetable(trips, stop_times, NO_TRANSFERS);
        let waits = waits_at(&tt, &[row(0, 2)], "A");
        let at = |h: usize, m: usize| waits.get(&(h * 60 + m)).copied().unwrap_or(0.0);
        assert!((at(8, 5) - 5.0).abs() < 1e-6);
        assert_eq!(at(8, 10), 0.0);
        assert!((at(8, 25) - 15.0).abs() < 1e-6);
        assert!((at(8, 39) - 29.0).abs() < 1e-6);
        assert_eq!(at(8, 40), 0.0);
        assert!(waits_at(&tt, &[row(0, 2)], "C").is_empty());
    }

    #[test]
    fn transfers_wait_from_their_last_train_until_their_next() {
        // The 2 reaches B at 08:20, and the 5 leaves it at 08:22.
        let trips = "route_id,trip_id,service_id\n2,feeder,W\n5,fast,W\n";
        let stop_times = "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
            feeder,A,08:10:00,08:10:00,1\nfeeder,B,08:20:00,08:20:00,2\n\
            fast,B,08:22:00,08:22:00,1\nfast,C,08:30:00,08:30:00,2\n";
        let transfers = "from_stop_id,to_stop_id,transfer_type,min_transfer_time\nB,B,2,60\n";
        let tt = timetable(trips, stop_times, transfers);
        let waits = waits_at(&tt, &[row(0, 2)], "B");
        // The 10 riders entering by 08:10.
        let ten = |m: usize| (waits[&(8 * 60 + m)] - 10.0).abs() < 1e-6;
        assert!(ten(20) && ten(21));
        assert_eq!(waits.keys().copied().collect::<Vec<_>>(), [500, 501]);
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
