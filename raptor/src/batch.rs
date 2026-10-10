//! Assigning every (month, weekday) of a date range,
//! each on one representative date and feed version.

use std::path::{Path, PathBuf};

use anyhow::{Context, Result, bail};
use jiff::ToSpan;
use jiff::civil::{Date, Time, Weekday};
use jiff::tz::TimeZone;

use pyo3::pyclass;

use crate::calendar::span;
use crate::gtfs::Feed;
use crate::timetable::SERVICE_DAY_START;

/// A feed version on disk, with its `calendar.txt` span.
#[pyclass(frozen, module = "mta_od_data._raptor")]
pub struct Version {
    pub path: PathBuf,
    pub feed: Feed,
    pub start: Date,
    pub end: Date,
}

/// Every `*.zip` in `dir`, oldest first by name:
/// Mobility Database dataset IDs end in their fetch time.
pub fn load_versions(dir: &Path) -> Result<Vec<Version>> {
    let mut paths: Vec<PathBuf> = std::fs::read_dir(dir)
        .with_context(|| format!("reading {}", dir.display()))?
        .map(|e| e.map(|e| e.path()))
        .collect::<Result<_, _>>()?;
    paths.retain(|p| p.extension().is_some_and(|e| e == "zip"));
    paths.sort();
    paths.into_iter().map(|path| Version::open(&path)).collect()
}

impl Version {
    pub fn open(path: &Path) -> Result<Self> {
        let feed = Feed::open(path)?;
        let (start, end) =
            span(&feed).with_context(|| format!("{} has no calendar", path.display()))?;
        Ok(Self {
            path: path.to_owned(),
            feed,
            start,
            end,
        })
    }
}

/// The latest-fetched version covering `date` and both its neighbors,
/// so its overnight trips from the previous date and early ones from the next are there.
pub fn version_for(versions: &[&Version], date: Date) -> Option<usize> {
    let (before, after) = (
        date.checked_sub(1.day()).ok()?,
        date.checked_add(1.day()).ok()?,
    );
    versions
        .iter()
        .rposition(|v| v.start <= before && after <= v.end)
}

/// Whether `date`'s service day (see `SERVICE_DAY_START`)
/// has a daylight-saving change in New York,
/// when GTFS times are an hour off wall-clock time.
fn dst_change(date: Date) -> Result<bool> {
    let tz = TimeZone::get("America/New_York")?;
    let start_of = |date: Date| -> Result<_> {
        let start = date.to_datetime(Time::midnight()) + SERVICE_DAY_START.seconds();
        Ok(start.to_zoned(tz.clone())?.offset())
    };
    Ok(start_of(date)? != start_of(date.checked_add(1.day())?)?)
}

/// One (month, weekday)'s representative date.
pub struct Pick {
    pub date: Date,
    /// Its feed version, as an index into the versions picked from.
    pub version: usize,
    /// How many of the month's dates in the range fall on this weekday:
    /// its weight in an average over the range.
    pub days: usize,
}

/// For each (month, weekday) in `[from, to]` with `weekdays`,
/// the middle date usable for routing:
/// covered with its neighbors by a feed version,
/// no `calendar_dates.txt` exception in that version on it or the next date,
/// and no daylight-saving change in its service day.
/// Middle, to stay clear of a version's edges.
pub fn pick_dates(
    versions: &[&Version],
    from: Date,
    to: Date,
    weekdays: &[Weekday],
) -> Result<Vec<Pick>> {
    let mut picks = Vec::new();
    let mut month = from.first_of_month();
    while month <= to {
        for &weekday in weekdays {
            let in_range: Vec<Date> = month
                .series(1.day())
                .take_while(|d| d.month() == month.month())
                .filter(|d| d.weekday() == weekday && (from..=to).contains(d))
                .collect();
            let mut usable = Vec::new();
            for &d in &in_range {
                let Some(v) = version_for(versions, d) else {
                    continue;
                };
                // The service day runs into the next date, on its early trips.
                let next = d.checked_add(1.day())?;
                let exception = versions[v]
                    .feed
                    .calendar_dates
                    .iter()
                    .any(|c| c.date == d || c.date == next);
                if exception || dst_change(d)? {
                    continue;
                }
                usable.push((d, v));
            }
            if in_range.is_empty() {
                continue;
            }
            let Some(&(date, version)) = usable.get(usable.len() / 2) else {
                bail!(
                    "no usable {weekday:?} in {} {}",
                    month.year(),
                    month.month()
                );
            };
            picks.push(Pick {
                date,
                version,
                days: in_range.len(),
            });
        }
        month = month.checked_add(1.month())?;
    }
    Ok(picks)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn version(name: &str, calendar_end: &str, calendar_dates: &str) -> Version {
        let calendar = format!(
            "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
             W,1,1,1,1,1,1,1,20250811,{calendar_end}\n"
        );
        let files = std::collections::HashMap::from([
            ("stops.txt", "stop_id,stop_name\n"),
            ("trips.txt", "route_id,trip_id,service_id\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n",
            ),
            ("calendar.txt", calendar.as_str()),
            ("calendar_dates.txt", calendar_dates),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        let (start, end) = span(&feed).unwrap();
        Version {
            path: name.into(),
            feed,
            start,
            end,
        }
    }

    #[test]
    fn picks_the_middle_usable_date() {
        // Labor Day, Monday 2025-09-01, has an exception;
        // `newer` covers through September 30, `older` all of it.
        let header = "service_id,date,exception_type\n";
        let versions = [
            version("older", "20251231", &format!("{header}W,20250901,2\n")),
            version("newer", "20250930", &format!("{header}W,20250901,2\n")),
        ];
        let date = |m, d| Date::new(2025, m, d).unwrap();
        let refs: Vec<_> = versions.iter().collect();
        let picks = pick_dates(&refs, date(8, 11), date(10, 31), &[Weekday::Monday]).unwrap();
        let got: Vec<_> = picks
            .iter()
            .map(|p| (p.date, versions[p.version].path.to_str().unwrap(), p.days))
            .collect();
        assert_eq!(
            got,
            [
                // 08-11 is the feed's first date, so lacks the day before:
                // usable are 08-18 and 08-25, of the 3 Mondays in range.
                (date(8, 25), "newer", 3),
                // 09-01 is a holiday: 09-08, 09-15, 09-22, 09-29.
                (date(9, 22), "newer", 5),
                // `newer` ends 09-30, so October is `older`'s:
                // 10-06, 10-13, 10-20, 10-27.
                (date(10, 20), "older", 4),
            ]
        );
    }

    #[test]
    fn dst_dates() {
        // The changes are at 02:00 on Sundays, in Saturday's service day.
        assert!(dst_change(Date::new(2025, 11, 1).unwrap()).unwrap());
        assert!(dst_change(Date::new(2025, 3, 8).unwrap()).unwrap());
        assert!(!dst_change(Date::new(2025, 11, 2).unwrap()).unwrap());
        assert!(!dst_change(Date::new(2025, 3, 9).unwrap()).unwrap());
    }
}
