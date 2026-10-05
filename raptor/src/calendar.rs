//! Which `service_id`s run on a date, from `calendar.txt` + `calendar_dates.txt`.

use std::collections::BTreeSet;

use anyhow::{Result, bail};
use jiff::civil::{Date, Weekday};

use crate::gtfs::Feed;

/// The first and last dates any `calendar.txt` period covers, inclusive.
pub fn span(feed: &Feed) -> Option<(Date, Date)> {
    let start = feed.calendar.iter().map(|c| c.start_date).min()?;
    let end = feed.calendar.iter().map(|c| c.end_date).max()?;
    Some((start, end))
}

/// The services running on `date`.
///
/// An error, never an empty set, for a date outside the feed's span
/// or one nothing runs on: either means the wrong feed was picked.
pub fn active_services(feed: &Feed, date: Date) -> Result<BTreeSet<&str>> {
    match span(feed) {
        Some((start, end)) if (start..=end).contains(&date) => {}
        Some((start, end)) => bail!("{date} is outside the feed's service span {start} to {end}"),
        None => bail!("feed has no calendar.txt periods"),
    }
    let mut services: BTreeSet<&str> = feed
        .calendar
        .iter()
        .filter(|c| (c.start_date..=c.end_date).contains(&date))
        .filter(|c| {
            let day = match date.weekday() {
                Weekday::Monday => c.monday,
                Weekday::Tuesday => c.tuesday,
                Weekday::Wednesday => c.wednesday,
                Weekday::Thursday => c.thursday,
                Weekday::Friday => c.friday,
                Weekday::Saturday => c.saturday,
                Weekday::Sunday => c.sunday,
            };
            day == 1
        })
        .map(|c| c.service_id.as_str())
        .collect();
    for exception in feed.calendar_dates.iter().filter(|d| d.date == date) {
        match exception.exception_type {
            1 => services.insert(&exception.service_id),
            2 => services.remove(exception.service_id.as_str()),
            other => bail!(
                "calendar_dates.txt: bad exception_type {other} for {} on {date}",
                exception.service_id
            ),
        };
    }
    if services.is_empty() {
        bail!("no service runs on {date}");
    }
    Ok(services)
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;

    fn feed() -> Feed {
        let files = HashMap::from([
            ("stops.txt", "stop_id,stop_name\n"),
            ("trips.txt", "route_id,trip_id,service_id\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n",
            ),
            (
                "calendar.txt",
                "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n\
                 Weekday,1,1,1,1,1,0,0,20250811,20251101\n\
                 Saturday,0,0,0,0,0,1,0,20250811,20251101\n\
                 Sunday,0,0,0,0,0,0,1,20250811,20251101\n",
            ),
            // Labor Day 2025 runs a Sunday schedule, as the real feed says.
            (
                "calendar_dates.txt",
                "service_id,date,exception_type\nWeekday,20250901,2\nSunday,20250901,1\n",
            ),
        ]);
        Feed::load(&mut { files }).unwrap()
    }

    fn date(y: i16, m: i8, d: i8) -> Date {
        Date::new(y, m, d).unwrap()
    }

    #[test]
    fn weekdays() {
        let feed = feed();
        let services = |d| {
            active_services(&feed, d)
                .unwrap()
                .into_iter()
                .collect::<Vec<_>>()
        };
        assert_eq!(services(date(2025, 9, 3)), ["Weekday"]);
        assert_eq!(services(date(2025, 9, 6)), ["Saturday"]);
        assert_eq!(services(date(2025, 9, 7)), ["Sunday"]);
    }

    #[test]
    fn labor_day_exception() {
        let feed = feed();
        let services: Vec<_> = active_services(&feed, date(2025, 9, 1))
            .unwrap()
            .into_iter()
            .collect();
        assert_eq!(services, ["Sunday"]);
    }

    #[test]
    fn outside_span() {
        let feed = feed();
        assert!(active_services(&feed, date(2025, 8, 10)).is_err());
        assert!(active_services(&feed, date(2025, 11, 2)).is_err());
    }
}
