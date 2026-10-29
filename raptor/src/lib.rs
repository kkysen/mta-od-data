//! RAPTOR journey assignment for the MTA OD data; see `raptor_design.md`.
//! Python drives it through the `mta_od_data._raptor` module.

pub mod assign;
pub mod batch;
pub mod calendar;
pub mod gtfs;
pub mod od;
pub mod pathways;
pub mod platforms;
pub mod raptor;
pub mod report;
pub mod timetable;

use std::collections::VecDeque;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::time::Instant;

use anyhow::{Context, Result};
use jiff::civil::{Date, Weekday};
use pyo3::types::{PyModule, PyModuleMethods};
use pyo3::{Bound, PyResult, Python, pyclass, pyfunction, pymethods, pymodule, wrap_pyfunction};
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};

use crate::assign::{
    Config, DEFAULT_FARE_GATE_PENALTY_MIN, Transfers, TripLoads, Unassigned, route, split,
    write_path_texts, write_paths, write_platform_waits, write_trips,
};
use crate::batch::{Version, load_versions, pick_dates};
use crate::gtfs::{Feed, Secs, parse_time};
use crate::od::{Complexes, load_service_day, load_service_days};
use crate::platforms::Platforms;
use crate::raptor::Router;
use crate::report::Timings;
use crate::timetable::Timetable;

/// Assigning a date allocates path text, journeys, and intervals on every core:
/// glibc's `malloc` and `free` took ~26% of a date's samples.
#[cfg(not(feature = "dhat-heap"))]
#[global_allocator]
static ALLOCATOR: mimalloc::MiMalloc = mimalloc::MiMalloc;

#[cfg(feature = "dhat-heap")]
#[global_allocator]
static ALLOCATOR: dhat::Alloc = dhat::Alloc;

/// What `assign_date` did.
#[pyclass(frozen, get_all, module = "mta_od_data._raptor")]
pub struct AssignSummary {
    pub riders_in: f64,
    pub riders_assigned: f64,
    pub unassigned_no_stops: f64,
    pub unassigned_unreachable: f64,
    pub unassigned_no_departure: f64,
    /// How many path rows were written.
    pub paths: usize,
    /// The Parquet of the paths' texts, by `path_id`,
    /// shared with the other dates routed alike.
    pub path_texts: PathBuf,
    /// `report::assignment`'s summary, for printing.
    pub report: String,
}

/// One date to assign, on its feed version, writing its paths to `out`.
/// Their texts go beside the first `out` of the dates routed alike.
pub struct Job<'a> {
    pub version: &'a Version,
    pub date: Date,
    pub out: PathBuf,
}

/// Assigns `date`'s OD rows on `version`'s timetable for it,
/// with the config at `config`, and writes the paths to `out`, zstd at `zstd_level`.
#[allow(clippy::too_many_arguments)]
pub fn assign_date(
    version: &Version,
    date: Date,
    od: &Path,
    stations: &Path,
    platforms: &Path,
    config: &Path,
    out: &Path,
    zstd_level: i32,
) -> Result<AssignSummary> {
    let job = Job {
        version,
        date,
        out: out.to_owned(),
    };
    let mut summaries = assign_dates(&[job], od, stations, platforms, config, zstd_level)?;
    Ok(summaries.pop().expect("one summary per job"))
}

/// Dates whose timetables route alike, sharing one routing.
struct Group {
    tt: Timetable,
    complexes: Complexes,
    /// Indices into the jobs.
    jobs: Vec<usize>,
}

/// Each pattern's trips' IDs: a date's own, which a group's timetable,
/// its first date's, doesn't have for the rest (`routes_like` ignores them).
fn trip_ids(tt: &Timetable) -> Vec<Vec<String>> {
    tt.patterns
        .iter()
        .map(|p| p.trips.iter().map(|t| t.trip_id.clone()).collect())
        .collect()
}

/// Assigns each job's date as `assign_date` does,
/// but routes each distinct timetable once, for every date with it:
/// a feed version's Mondays to Thursdays mostly share one.
/// Summaries are in `jobs`' order.
pub fn assign_dates(
    jobs: &[Job],
    od: &Path,
    stations: &Path,
    platforms: &Path,
    config: &Path,
    zstd_level: i32,
) -> Result<Vec<AssignSummary>> {
    // Writes `dhat-heap.json` to the working directory when dropped.
    #[cfg(feature = "dhat-heap")]
    let _profiler = dhat::Profiler::new_heap();
    let (config, config_text) = Config::load(config)?;

    let platforms = match config.transfers {
        Transfers::Osm => Some(Platforms::load(platforms)?),
        Transfers::Gtfs => None,
    };

    let start = Instant::now();
    let timetables: Vec<(Timetable, Complexes)> = jobs
        .par_iter()
        .map(|job| -> Result<_> {
            let mut tt = Timetable::build(&job.version.feed, job.date)?;
            if let Some(platforms) = &platforms {
                tt.split_platforms(platforms);
            }
            let complexes = Complexes::load(stations, &tt)?;
            match config.transfers {
                Transfers::Gtfs => {}
                Transfers::Osm => tt.use_osm_transfers(
                    complexes.stops.values().map(Vec::as_slice),
                    platforms.as_ref().expect("loaded for osm"),
                    config.up_and_over_secs,
                    config.stacked_secs_per_level,
                ),
            }
            // Pathways, where a feed has them, over either.
            if !job.version.feed.pathways.is_empty() {
                let gate_penalty = (config.fare_gate_penalty_min * 60.0).round() as Secs;
                let (walks, report) =
                    pathways::walks(&job.version.feed, &tt, gate_penalty, pathways::MAX_WALK);
                tt.use_pathways(&walks, &report.covered);
            }
            Ok((tt, complexes))
        })
        .collect::<Result<_>>()?;
    let mut groups: Vec<Group> = Vec::new();
    let mut job_trip_ids = Vec::with_capacity(jobs.len());
    for (i, (tt, complexes)) in timetables.into_iter().enumerate() {
        job_trip_ids.push(trip_ids(&tt));
        match groups.iter_mut().find(|g| g.tt.routes_like(&tt)) {
            Some(group) => group.jobs.push(i),
            None => groups.push(Group {
                tt,
                complexes,
                jobs: vec![i],
            }),
        }
    }
    eprintln!(
        "built {} timetables, {} distinct, in {:.1?}",
        jobs.len(),
        groups.len(),
        start.elapsed()
    );

    let mut summaries: Vec<Option<AssignSummary>> = jobs.iter().map(|_| None).collect();
    let dates = |group: &Group| -> Vec<Date> { group.jobs.iter().map(|&i| jobs[i].date).collect() };
    // Loading and writing each take one core, routing and splitting every core:
    // a timetable's dates load while it routes, which doesn't need them,
    // and the next's while its dates split and write,
    // and up to `WRITERS` dates write while the next split.
    std::thread::scope(|scope| -> Result<()> {
        let load = |group: &Group| {
            let dates = dates(group);
            scope.spawn(move || -> Result<_> {
                let start = Instant::now();
                let slices = load_service_days(od, &dates)?;
                Ok((slices, start.elapsed()))
            })
        };
        let mut loading = groups.first().map(load);
        let mut writing = VecDeque::new();
        for (g, group) in groups.iter().enumerate() {
            let start = Instant::now();
            let routes = route(&group.tt, &group.complexes, config.max_rides);
            let routed = start.elapsed();
            let (slices, loaded) = join(loading.take().expect("loading this group"))?;
            loading = groups.get(g + 1).map(load);
            let dates = dates(group);
            eprintln!(
                "routed timetable {} of {} in {routed:.1?}, for {}",
                g + 1,
                groups.len(),
                dates
                    .iter()
                    .map(Date::to_string)
                    .collect::<Vec<_>>()
                    .join(", ")
            );
            let first = &jobs[group.jobs[0]];
            let path_texts = path_texts_out(&first.out, first.date);
            // Written with the dates' paths, as they split.
            let routes = Arc::new(routes);
            while writing.len() >= WRITERS {
                join(writing.pop_front().expect("WRITERS > 0"))?;
            }
            writing.push_back({
                let routes = Arc::clone(&routes);
                let path_texts = path_texts.clone();
                let metadata = vec![
                    ("feed".to_string(), first.version.path.display().to_string()),
                    (
                        "dates".to_string(),
                        dates
                            .iter()
                            .map(Date::to_string)
                            .collect::<Vec<_>>()
                            .join(","),
                    ),
                    ("config".to_string(), config_text.clone()),
                ];
                scope.spawn(move || -> Result<()> {
                    let start = Instant::now();
                    write_path_texts(&path_texts, &routes, metadata, zstd_level)?;
                    eprintln!("wrote {} in {:.1?}", path_texts.display(), start.elapsed());
                    Ok(())
                })
            });
            for (&i, rows) in group.jobs.iter().zip(&slices) {
                let job = &jobs[i];
                let start = Instant::now();
                let loads = TripLoads::new(&group.tt);
                let (paths, unassigned) = split(&routes, &group.complexes, rows, &config, &loads);
                let timings = Timings {
                    loaded,
                    routed,
                    dates: dates.len(),
                    split: start.elapsed(),
                };
                let metadata = vec![
                    ("feed".to_string(), job.version.path.display().to_string()),
                    ("date".to_string(), job.date.to_string()),
                    ("config".to_string(), config_text.clone()),
                    ("path_texts".to_string(), file_name(&path_texts)),
                ];
                let Unassigned {
                    no_stops,
                    unreachable,
                    no_departure,
                } = unassigned;
                summaries[i] = Some(AssignSummary {
                    riders_in: report::riders(rows.iter()),
                    riders_assigned: report::assigned(&paths),
                    unassigned_no_stops: no_stops,
                    unassigned_unreachable: unreachable,
                    unassigned_no_departure: no_departure,
                    paths: paths.len(),
                    path_texts: path_texts.clone(),
                    report: report::assignment(
                        rows,
                        &paths,
                        &unassigned,
                        config.max_rides,
                        &timings,
                    ),
                });
                while writing.len() >= WRITERS {
                    join(writing.pop_front().expect("WRITERS > 0"))?;
                }
                let tt = &group.tt;
                let ids = &job_trip_ids[i];
                let trips = trips_out(&job.out, job.date);
                let trips_metadata = metadata.clone();
                let waits = waits_out(&job.out, job.date);
                let waits_metadata = metadata.clone();
                writing.push_back(scope.spawn(move || -> Result<()> {
                    let start = Instant::now();
                    write_paths(&job.out, &paths, job.date, metadata, zstd_level)?;
                    eprintln!("wrote {} in {:.1?}", job.out.display(), start.elapsed());
                    let start = Instant::now();
                    write_trips(&trips, tt, ids, &loads, trips_metadata, zstd_level)?;
                    eprintln!("wrote {} in {:.1?}", trips.display(), start.elapsed());
                    let start = Instant::now();
                    write_platform_waits(&waits, tt, &loads, waits_metadata, zstd_level)?;
                    eprintln!("wrote {} in {:.1?}", waits.display(), start.elapsed());
                    Ok(())
                }));
            }
        }
        for handle in writing {
            join(handle)?;
        }
        Ok(())
    })?;
    Ok(summaries
        .into_iter()
        .map(|s| s.expect("every job is in a group"))
        .collect())
}

/// Where a date's trips go: beside its paths, `out`.
pub fn trips_out(out: &Path, date: Date) -> PathBuf {
    out.with_file_name(format!("trips-{date}.parquet"))
}

/// Where a date's platform waits go: beside its paths, `out`.
pub fn waits_out(out: &Path, date: Date) -> PathBuf {
    out.with_file_name(format!("platform-waits-{date}.parquet"))
}

/// Where a group's path texts go: beside its first date's paths, `out`.
fn path_texts_out(out: &Path, date: Date) -> PathBuf {
    out.with_file_name(format!("path-texts-{date}.parquet"))
}

fn file_name(path: &Path) -> String {
    path.file_name()
        .map_or_else(String::new, |n| n.to_string_lossy().into_owned())
}

/// Files written at once: each date holds its paths, ~150 MB, until written,
/// and each group's texts its routes.
const WRITERS: usize = 4;

/// Joins a thread, passing on its panic.
fn join<T>(handle: std::thread::ScopedJoinHandle<'_, T>) -> T {
    handle
        .join()
        .unwrap_or_else(|panic| std::panic::resume_unwind(panic))
}

/// The stops at each station or stop of `ids`.
fn stops(tt: &Timetable, ids: &[String]) -> Result<Vec<u32>> {
    let mut stops = Vec::new();
    for id in ids {
        let at = tt.stops_at(id);
        anyhow::ensure!(!at.is_empty(), "no stop {id}");
        stops.extend(at);
    }
    Ok(stops)
}

fn secs(s: &str) -> Result<Secs> {
    parse_time(s).with_context(|| format!("expected HH:MM:SS, got {s:?}"))
}

#[pymethods]
impl Version {
    /// Loads the feed zip at `path`.
    #[staticmethod]
    #[pyo3(name = "open")]
    fn py_open(py: Python<'_>, path: PathBuf) -> Result<Self> {
        py.detach(|| Self::open(&path))
    }

    #[getter]
    fn path(&self) -> &Path {
        &self.path
    }

    /// The first date of its `calendar.txt`.
    #[getter]
    fn start(&self) -> Date {
        self.start
    }

    /// The last date of its `calendar.txt`.
    #[getter]
    fn end(&self) -> Date {
        self.end
    }
}

/// Every feed version zip in `dir`, oldest first.
#[pyfunction(name = "load_versions")]
fn py_load_versions(py: Python<'_>, dir: PathBuf) -> Result<Vec<Version>> {
    py.detach(|| load_versions(&dir))
}

/// For each (month, weekday Monday to Friday) in `[start, end]`,
/// its representative date, the version to route it on,
/// and how many of the month's dates in the range fall on that weekday.
#[pyfunction(name = "pick_weekdays")]
fn py_pick_weekdays<'py>(
    versions: Vec<Bound<'py, Version>>,
    start: Date,
    end: Date,
) -> Result<Vec<(Date, Bound<'py, Version>, usize)>> {
    let weekdays = [
        Weekday::Monday,
        Weekday::Tuesday,
        Weekday::Wednesday,
        Weekday::Thursday,
        Weekday::Friday,
    ];
    let refs: Vec<&Version> = versions.iter().map(Bound::get).collect();
    let picks = pick_dates(&refs, start, end, &weekdays)?;
    Ok(picks
        .into_iter()
        .map(|p| (p.date, versions[p.version].clone(), p.days))
        .collect())
}

/// `assign_date`, without holding the GIL.
#[pyfunction(name = "assign_date")]
#[allow(clippy::too_many_arguments)]
fn py_assign_date(
    py: Python<'_>,
    version: &Bound<'_, Version>,
    date: Date,
    od: PathBuf,
    stations: PathBuf,
    platforms: PathBuf,
    config: PathBuf,
    out: PathBuf,
    zstd_level: i32,
) -> Result<AssignSummary> {
    let version = version.get();
    py.detach(|| {
        assign_date(
            version, date, &od, &stations, &platforms, &config, &out, zstd_level,
        )
    })
}

/// `assign_dates` on `(version, date, out)` jobs, without holding the GIL.
#[pyfunction(name = "assign_dates")]
fn py_assign_dates(
    py: Python<'_>,
    jobs: Vec<(Bound<'_, Version>, Date, PathBuf)>,
    od: PathBuf,
    stations: PathBuf,
    platforms: PathBuf,
    config: PathBuf,
    zstd_level: i32,
) -> Result<Vec<AssignSummary>> {
    let jobs: Vec<Job> = jobs
        .iter()
        .map(|(version, date, out)| Job {
            version: version.get(),
            date: *date,
            out: out.clone(),
        })
        .collect();
    py.detach(|| assign_dates(&jobs, &od, &stations, &platforms, &config, zstd_level))
}

/// A summary of the feed zip at `feed`.
#[pyfunction]
fn feed_report(py: Python<'_>, feed: PathBuf) -> Result<String> {
    py.detach(|| Ok(report::feed(&Feed::open(&feed)?)))
}

/// What building `date`'s timetable from `feed` found.
#[pyfunction]
fn timetable_report(py: Python<'_>, feed: PathBuf, date: Date) -> Result<String> {
    py.detach(|| {
        let feed = Feed::open(&feed)?;
        let tt = Timetable::build(&feed, date)?;
        let mut out = report::timetable(&tt);
        if !feed.pathways.is_empty() {
            let gate_penalty = (DEFAULT_FARE_GATE_PENALTY_MIN * 60.0) as Secs;
            let walks = pathways::walks(&feed, &tt, gate_penalty, pathways::MAX_WALK);
            out += &report::pathways(&walks.1);
        }
        Ok(out)
    })
}

/// Earliest-arrival journeys between two sets of stops, one per number of rides.
#[pyfunction]
#[pyo3(signature = (feed, date, origins, destinations, depart, max_rides = raptor::DEFAULT_MAX_RIDES))]
fn route_report(
    py: Python<'_>,
    feed: PathBuf,
    date: Date,
    origins: Vec<String>,
    destinations: Vec<String>,
    depart: &str,
    max_rides: usize,
) -> Result<String> {
    let depart = secs(depart)?;
    py.detach(|| {
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        let (from, to) = (stops(&tt, &origins)?, stops(&tt, &destinations)?);
        let router = Router::with_max_rides(&tt, max_rides);
        let (legs, journeys) = router.query(&from, depart).journeys(&to);
        Ok(report::journeys(&tt, &legs, &journeys))
    })
}

/// Every Pareto-optimal journey between two sets of stops departing in `[after, before)`.
#[pyfunction]
#[pyo3(signature = (feed, date, origins, destinations, after, before, max_rides = raptor::DEFAULT_MAX_RIDES))]
#[allow(clippy::too_many_arguments)]
fn profile_report(
    py: Python<'_>,
    feed: PathBuf,
    date: Date,
    origins: Vec<String>,
    destinations: Vec<String>,
    after: &str,
    before: &str,
    max_rides: usize,
) -> Result<String> {
    let (after, before) = (secs(after)?, secs(before)?);
    py.detach(|| {
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        let (from, to) = (stops(&tt, &origins)?, stops(&tt, &destinations)?);
        let router = Router::with_max_rides(&tt, max_rides);
        let (legs, mut journeys) = router.profile(&from, after, before, &[&to]);
        journeys[0].sort_by_key(|j| (j.depart, j.rides()));
        Ok(report::journeys(&tt, &legs, &journeys[0]))
    })
}

/// The OD rows for `date`'s (year, month, day of week),
/// and how their station complexes map to `date`'s timetable.
#[pyfunction]
fn od_report(
    py: Python<'_>,
    feed: PathBuf,
    date: Date,
    od: PathBuf,
    stations: PathBuf,
) -> Result<String> {
    py.detach(|| {
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        let complexes = Complexes::load(&stations, &tt)?;
        let rows = load_service_day(&od, date)?;
        Ok(report::od(&complexes, &rows))
    })
}

#[pymodule]
#[pyo3(name = "_raptor")]
fn raptor_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Version>()?;
    m.add_class::<AssignSummary>()?;
    m.add("DEFAULT_MAX_RIDES", raptor::DEFAULT_MAX_RIDES)?;
    m.add_function(wrap_pyfunction!(py_load_versions, m)?)?;
    m.add_function(wrap_pyfunction!(py_pick_weekdays, m)?)?;
    m.add_function(wrap_pyfunction!(py_assign_date, m)?)?;
    m.add_function(wrap_pyfunction!(py_assign_dates, m)?)?;
    m.add_function(wrap_pyfunction!(feed_report, m)?)?;
    m.add_function(wrap_pyfunction!(timetable_report, m)?)?;
    m.add_function(wrap_pyfunction!(route_report, m)?)?;
    m.add_function(wrap_pyfunction!(profile_report, m)?)?;
    m.add_function(wrap_pyfunction!(od_report, m)?)?;
    Ok(())
}
