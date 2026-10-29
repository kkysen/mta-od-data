//! Raw static GTFS records, read by header name from a feed zip.

use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::Read;
use std::path::Path;

use anyhow::{Context, Result, bail};
use jiff::civil::Date;
use serde::Deserialize;
use serde::de::DeserializeOwned;
use zip::ZipArchive;

/// Seconds since the service day's "noon minus 12h".
/// Signed, since a previous day's trips are shifted back a day.
pub type Secs = i32;

pub const DAY: Secs = 24 * 60 * 60;

/// Where a feed's `.txt` files come from.
pub trait Source {
    /// The named file's contents, or `None` if the feed doesn't have it.
    fn read(&mut self, name: &str) -> Result<Option<String>>;
}

pub struct ZipSource(ZipArchive<File>);

impl ZipSource {
    pub fn open(path: &Path) -> Result<Self> {
        let file = File::open(path).with_context(|| format!("opening {}", path.display()))?;
        Ok(Self(ZipArchive::new(file)?))
    }
}

impl Source for ZipSource {
    fn read(&mut self, name: &str) -> Result<Option<String>> {
        // By exact name, never by iterating entries:
        // some versions also hold `__MACOSX/._<name>` AppleDouble junk.
        let mut entry = match self.0.by_name(name) {
            Ok(entry) => entry,
            Err(zip::result::ZipError::FileNotFound) => return Ok(None),
            Err(e) => return Err(e.into()),
        };
        let mut text = String::new();
        entry.read_to_string(&mut text)?;
        Ok(Some(text))
    }
}

/// In-memory files, for tests.
impl Source for HashMap<&str, &str> {
    fn read(&mut self, name: &str) -> Result<Option<String>> {
        Ok(self.get(name).map(|s| s.to_string()))
    }
}

#[derive(Debug, Deserialize)]
pub struct Stop {
    pub stop_id: String,
    pub stop_name: String,
    #[serde(default)]
    pub stop_lat: Option<f64>,
    #[serde(default)]
    pub stop_lon: Option<f64>,
    #[serde(default)]
    pub parent_station: Option<String>,
    /// 0 or missing for a stop or platform, 1 a station, 2 an entrance,
    /// 3 a pathway node, 4 a boarding area.
    #[serde(default)]
    pub location_type: Option<u8>,
}

#[derive(Clone, Debug, Deserialize)]
pub struct Trip {
    pub route_id: String,
    pub trip_id: String,
    pub service_id: String,
    #[serde(default)]
    pub direction_id: Option<u8>,
}

#[derive(Clone, Debug, Deserialize)]
pub struct StopTime {
    pub trip_id: String,
    pub stop_id: String,
    #[serde(deserialize_with = "de_time")]
    pub arrival_time: Secs,
    #[serde(deserialize_with = "de_time")]
    pub departure_time: Secs,
    pub stop_sequence: u32,
}

#[derive(Debug, Deserialize)]
pub struct Calendar {
    pub service_id: String,
    pub monday: u8,
    pub tuesday: u8,
    pub wednesday: u8,
    pub thursday: u8,
    pub friday: u8,
    pub saturday: u8,
    pub sunday: u8,
    #[serde(deserialize_with = "de_date")]
    pub start_date: Date,
    #[serde(deserialize_with = "de_date")]
    pub end_date: Date,
}

#[derive(Debug, Deserialize)]
pub struct CalendarDate {
    pub service_id: String,
    #[serde(deserialize_with = "de_date")]
    pub date: Date,
    pub exception_type: u8,
}

#[derive(Debug, Deserialize)]
pub struct Transfer {
    pub from_stop_id: String,
    pub to_stop_id: String,
    pub transfer_type: u8,
    #[serde(default)]
    pub min_transfer_time: Option<Secs>,
}

/// A step of walking within a station, between two of its locations.
#[derive(Debug, Deserialize)]
pub struct Pathway {
    pub from_stop_id: String,
    pub to_stop_id: String,
    /// 1 walkway, 2 stairs, 3 moving walkway, 4 escalator, 5 elevator,
    /// 6 fare gate into the paid area, 7 exit gate out of it.
    pub pathway_mode: u8,
    /// 1 if it goes from `to_stop_id` to `from_stop_id` too.
    pub is_bidirectional: u8,
    /// Meters.
    #[serde(default)]
    pub length: Option<f64>,
    #[serde(default)]
    pub traversal_time: Option<Secs>,
    /// Steps up from `from_stop_id` to `to_stop_id`, negative for down.
    #[serde(default)]
    pub stair_count: Option<i32>,
}

/// A trip running every `headway_secs` from `start_time` until before `end_time`,
/// its `stop_times.txt` times giving only the times between stops.
#[derive(Debug, Deserialize)]
pub struct Frequency {
    pub trip_id: String,
    #[serde(deserialize_with = "de_time")]
    pub start_time: Secs,
    #[serde(deserialize_with = "de_time")]
    pub end_time: Secs,
    pub headway_secs: Secs,
    /// 1 for trips leaving exactly on the headway; 0 or missing for headways only,
    /// which are taken as exact from `start_time` too.
    #[serde(default)]
    pub exact_times: Option<u8>,
}

/// `trips` and `stop_times` have each frequency-based trip expanded
/// into one trip per departure, as if the feed had listed them,
/// with IDs `<trip_id>@<HH:MM:SS>` of their first departure.
pub struct Feed {
    pub stops: Vec<Stop>,
    pub trips: Vec<Trip>,
    pub stop_times: Vec<StopTime>,
    pub calendar: Vec<Calendar>,
    pub calendar_dates: Vec<CalendarDate>,
    pub transfers: Vec<Transfer>,
    pub frequencies: Vec<Frequency>,
    pub pathways: Vec<Pathway>,
}

impl Feed {
    pub fn load(source: &mut impl Source) -> Result<Self> {
        let mut feed = Self {
            stops: required(source, "stops.txt")?,
            trips: required(source, "trips.txt")?,
            stop_times: required(source, "stop_times.txt")?,
            calendar: optional(source, "calendar.txt")?,
            calendar_dates: optional(source, "calendar_dates.txt")?,
            transfers: optional(source, "transfers.txt")?,
            frequencies: optional(source, "frequencies.txt")?,
            pathways: optional(source, "pathways.txt")?,
        };
        feed.expand_frequencies()?;
        Ok(feed)
    }

    /// Replaces each trip in `frequencies` with one trip per departure.
    fn expand_frequencies(&mut self) -> Result<()> {
        if self.frequencies.is_empty() {
            return Ok(());
        }
        let templates: HashSet<&str> = self
            .frequencies
            .iter()
            .map(|f| f.trip_id.as_str())
            .collect();
        let mut stop_times: HashMap<&str, Vec<&StopTime>> = HashMap::new();
        for st in &self.stop_times {
            if templates.contains(st.trip_id.as_str()) {
                stop_times.entry(st.trip_id.as_str()).or_default().push(st);
            }
        }
        let trips: HashMap<&str, &Trip> =
            self.trips.iter().map(|t| (t.trip_id.as_str(), t)).collect();

        let (mut new_trips, mut new_stop_times) = (Vec::new(), Vec::new());
        for f in &self.frequencies {
            let trip = trips
                .get(f.trip_id.as_str())
                .with_context(|| format!("frequencies.txt trip {} not in trips.txt", f.trip_id))?;
            let sts = stop_times
                .get(f.trip_id.as_str())
                .map_or(&[][..], Vec::as_slice);
            let Some(first) = sts.iter().min_by_key(|st| st.stop_sequence) else {
                bail!("frequencies.txt trip {} has no stop times", f.trip_id);
            };
            if f.headway_secs <= 0 {
                bail!(
                    "frequencies.txt trip {} has headway {}",
                    f.trip_id,
                    f.headway_secs
                );
            }
            let mut start = f.start_time;
            while start < f.end_time {
                let trip_id = format!(
                    "{}@{:02}:{:02}:{:02}",
                    f.trip_id,
                    start / 3600,
                    start / 60 % 60,
                    start % 60
                );
                let shift = start - first.departure_time;
                new_stop_times.extend(sts.iter().map(|&st| StopTime {
                    trip_id: trip_id.clone(),
                    arrival_time: st.arrival_time + shift,
                    departure_time: st.departure_time + shift,
                    ..st.clone()
                }));
                new_trips.push(Trip {
                    trip_id,
                    ..(*trip).clone()
                });
                start += f.headway_secs;
            }
        }
        self.trips
            .retain(|t| !templates.contains(t.trip_id.as_str()));
        self.stop_times
            .retain(|st| !templates.contains(st.trip_id.as_str()));
        self.trips.extend(new_trips);
        self.stop_times.extend(new_stop_times);
        Ok(())
    }

    pub fn open(path: &Path) -> Result<Self> {
        Self::load(&mut ZipSource::open(path)?)
            .with_context(|| format!("loading {}", path.display()))
    }
}

fn parse<T: DeserializeOwned>(name: &str, text: &str) -> Result<Vec<T>> {
    // `csv` strips a leading UTF-8 BOM, so headers match either way.
    csv::Reader::from_reader(text.as_bytes())
        .deserialize()
        .enumerate()
        .map(|(i, row)| row.with_context(|| format!("{name} record {}", i + 1)))
        .collect()
}

fn required<T: DeserializeOwned>(source: &mut impl Source, name: &str) -> Result<Vec<T>> {
    match source.read(name)? {
        Some(text) => parse(name, &text),
        None => bail!("feed has no {name}"),
    }
}

fn optional<T: DeserializeOwned>(source: &mut impl Source, name: &str) -> Result<Vec<T>> {
    source
        .read(name)?
        .map_or(Ok(Vec::new()), |text| parse(name, &text))
}

/// `H:MM:SS` or `HH:MM:SS`, where hours may be 24 or more.
pub fn parse_time(s: &str) -> Option<Secs> {
    let mut parts = s.trim().split(':').map(|p| p.parse::<Secs>().ok());
    let (h, m, sec) = (parts.next()??, parts.next()??, parts.next()??);
    if parts.next().is_some() || !(0..60).contains(&m) || !(0..60).contains(&sec) || h < 0 {
        return None;
    }
    Some(h * 3600 + m * 60 + sec)
}

/// `YYYYMMDD`.
pub fn parse_date(s: &str) -> Option<Date> {
    let s = s.trim();
    if s.len() != 8 || !s.bytes().all(|b| b.is_ascii_digit()) {
        return None;
    }
    Date::new(
        s[..4].parse().ok()?,
        s[4..6].parse().ok()?,
        s[6..].parse().ok()?,
    )
    .ok()
}

fn de_time<'de, D: serde::Deserializer<'de>>(d: D) -> Result<Secs, D::Error> {
    let s = String::deserialize(d)?;
    parse_time(&s).ok_or_else(|| serde::de::Error::custom(format!("bad GTFS time {s:?}")))
}

fn de_date<'de, D: serde::Deserializer<'de>>(d: D) -> Result<Date, D::Error> {
    let s = String::deserialize(d)?;
    parse_date(&s).ok_or_else(|| serde::de::Error::custom(format!("bad GTFS date {s:?}")))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn times() {
        assert_eq!(parse_time("00:06:00"), Some(360));
        assert_eq!(parse_time("7:05:09"), Some(7 * 3600 + 5 * 60 + 9));
        assert_eq!(parse_time("25:00:30"), Some(25 * 3600 + 30));
        assert_eq!(parse_time("12:60:00"), None);
        assert_eq!(parse_time("12:00"), None);
        assert_eq!(parse_time(""), None);
    }

    #[test]
    fn dates() {
        assert_eq!(parse_date("20250901"), Some(Date::new(2025, 9, 1).unwrap()));
        assert_eq!(parse_date("20251301"), None);
        assert_eq!(parse_date("2025091"), None);
    }

    #[test]
    fn header_bom_and_column_order() {
        // A BOM on the first header, columns in a nonstandard order, an extra column.
        let text =
            "\u{feff}to_stop_id,extra,from_stop_id,min_transfer_time,transfer_type\nB,x,A,,2\n";
        let rows: Vec<Transfer> = parse("transfers.txt", text).unwrap();
        assert_eq!(rows.len(), 1);
        assert_eq!(
            (rows[0].from_stop_id.as_str(), rows[0].to_stop_id.as_str()),
            ("A", "B")
        );
        assert_eq!(rows[0].min_transfer_time, None);
    }

    #[test]
    fn frequencies_expand_into_trips() {
        let files = HashMap::from([
            ("stops.txt", "stop_id,stop_name\nA,A\nB,B\n"),
            ("trips.txt", "route_id,trip_id,service_id\n1,f,W\n1,t,W\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
                 f,B,00:10:00,00:10:00,2\nf,A,00:00:00,00:01:00,1\n\
                 t,A,09:00:00,09:00:00,1\nt,B,09:10:00,09:10:00,2\n",
            ),
            (
                "frequencies.txt",
                "trip_id,start_time,end_time,headway_secs,exact_times\n\
                 f,08:00:00,08:20:00,600,1\nf,17:00:00,17:05:00,600,1\n",
            ),
        ]);
        let feed = Feed::load(&mut { files }).unwrap();
        let ids: Vec<_> = feed.trips.iter().map(|t| t.trip_id.as_str()).collect();
        // Up to but not including `end_time`; `t` isn't on frequencies so stays as it was.
        assert_eq!(ids, ["t", "f@08:00:00", "f@08:10:00", "f@17:00:00"]);
        let times: Vec<_> = feed
            .stop_times
            .iter()
            .filter(|st| st.trip_id == "f@08:10:00")
            .map(|st| (st.stop_id.as_str(), st.arrival_time, st.departure_time))
            .collect();
        // The first departure lands on the start; the rest keep their gaps.
        let t = |h: Secs, m: Secs| h * 3600 + m * 60;
        assert_eq!(times, [("B", t(8, 19), t(8, 19)), ("A", t(8, 9), t(8, 10))]);
    }
}
