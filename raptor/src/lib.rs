//! RAPTOR journey assignment for the MTA OD data; see `raptor_design.md`.
//! Python drives it through the `mta_od_data._raptor` module.

pub mod assign;
pub mod batch;
pub mod calendar;
pub mod gtfs;
pub mod od;
pub mod raptor;
pub mod report;
pub mod timetable;

use std::path::{Path, PathBuf};
use std::time::Instant;

use anyhow::{Context, Result};
use jiff::civil::{Date, Weekday};
use pyo3::types::{PyModule, PyModuleMethods};
use pyo3::{Bound, PyResult, Python, pyclass, pyfunction, pymethods, pymodule, wrap_pyfunction};

use crate::assign::{Config, Transfers, Unassigned, assign, write_paths};
use crate::batch::{Version, load_versions, pick_dates};
use crate::gtfs::{Feed, Secs, parse_time};
use crate::od::{Complexes, load_slice};
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
    /// `report::assignment`'s summary, for printing.
    pub report: String,
}

/// Assigns `date`'s OD rows on `version`'s timetable for it,
/// with the config at `config`, and writes the paths to `out`.
pub fn assign_date(
    version: &Version,
    date: Date,
    od: &Path,
    stations: &Path,
    config: &Path,
    out: &Path,
) -> Result<AssignSummary> {
    // Writes `dhat-heap.json` to the working directory when dropped.
    #[cfg(feature = "dhat-heap")]
    let _profiler = dhat::Profiler::new_heap();
    let start = Instant::now();
    let (config, config_text) = Config::load(config)?;
    let mut tt = Timetable::build(&version.feed, date)?;
    let complexes = Complexes::load(stations, &tt)?;
    if config.transfers == Transfers::WalkDistance {
        tt.use_walk_distance_transfers(complexes.stops.values().map(Vec::as_slice));
    }
    let rows = load_slice(od, date)?;
    let loaded = start.elapsed();
    let (paths, texts, unassigned) = assign(&tt, &complexes, &rows, &config);
    let timings = Timings {
        loaded,
        assigned: start.elapsed(),
    };
    let metadata = vec![
        ("feed".to_string(), version.path.display().to_string()),
        ("date".to_string(), date.to_string()),
        ("config".to_string(), config_text),
    ];
    write_paths(out, &paths, &texts, date, metadata)?;
    let Unassigned {
        no_stops,
        unreachable,
        no_departure,
    } = unassigned;
    Ok(AssignSummary {
        riders_in: report::riders(rows.iter()),
        riders_assigned: report::assigned(&paths),
        unassigned_no_stops: no_stops,
        unassigned_unreachable: unreachable,
        unassigned_no_departure: no_departure,
        paths: paths.len(),
        report: report::assignment(&rows, &paths, &unassigned, &timings),
    })
}

fn stops(tt: &Timetable, ids: &[String]) -> Result<Vec<u32>> {
    ids.iter()
        .map(|id| tt.stop(id).with_context(|| format!("no stop {id}")))
        .collect()
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
fn py_assign_date(
    py: Python<'_>,
    version: &Bound<'_, Version>,
    date: Date,
    od: PathBuf,
    stations: PathBuf,
    config: PathBuf,
    out: PathBuf,
) -> Result<AssignSummary> {
    let version = version.get();
    py.detach(|| assign_date(version, date, &od, &stations, &config, &out))
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
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        Ok(report::timetable(&tt))
    })
}

/// Earliest-arrival journeys between two sets of stops, one per number of rides.
#[pyfunction]
fn route_report(
    py: Python<'_>,
    feed: PathBuf,
    date: Date,
    origins: Vec<String>,
    destinations: Vec<String>,
    depart: &str,
) -> Result<String> {
    let depart = secs(depart)?;
    py.detach(|| {
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        let (from, to) = (stops(&tt, &origins)?, stops(&tt, &destinations)?);
        let router = Router::new(&tt);
        Ok(report::journeys(
            &tt,
            &router.query(&from, depart).journeys(&to),
        ))
    })
}

/// Every Pareto-optimal journey between two sets of stops departing in `[after, before)`.
#[pyfunction]
fn profile_report(
    py: Python<'_>,
    feed: PathBuf,
    date: Date,
    origins: Vec<String>,
    destinations: Vec<String>,
    after: &str,
    before: &str,
) -> Result<String> {
    let (after, before) = (secs(after)?, secs(before)?);
    py.detach(|| {
        let tt = Timetable::build(&Feed::open(&feed)?, date)?;
        let (from, to) = (stops(&tt, &origins)?, stops(&tt, &destinations)?);
        let router = Router::new(&tt);
        let mut journeys = router.profile(&from, after, before, &[&to]);
        journeys[0].sort_by_key(|j| (j.depart, j.rides()));
        Ok(report::journeys(&tt, &journeys[0]))
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
        let rows = load_slice(&od, date)?;
        Ok(report::od(&complexes, &rows))
    })
}

#[pymodule]
#[pyo3(name = "_raptor")]
fn raptor_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Version>()?;
    m.add_class::<AssignSummary>()?;
    m.add("MAX_RIDES", raptor::MAX_RIDES)?;
    m.add_function(wrap_pyfunction!(py_load_versions, m)?)?;
    m.add_function(wrap_pyfunction!(py_pick_weekdays, m)?)?;
    m.add_function(wrap_pyfunction!(py_assign_date, m)?)?;
    m.add_function(wrap_pyfunction!(feed_report, m)?)?;
    m.add_function(wrap_pyfunction!(timetable_report, m)?)?;
    m.add_function(wrap_pyfunction!(route_report, m)?)?;
    m.add_function(wrap_pyfunction!(profile_report, m)?)?;
    m.add_function(wrap_pyfunction!(od_report, m)?)?;
    Ok(())
}
