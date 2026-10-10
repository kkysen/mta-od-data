//! The OD data's rows for one (year, month, day of week),
//! and each station complex's stops in a timetable.

use std::collections::{BTreeMap, HashSet};
use std::fs::File;
use std::ops::Range;
use std::path::Path;

use anyhow::{Context, Result, bail};
use arrow_array::cast::AsArray;
use arrow_array::types::{Decimal128Type, Int64Type};
use arrow_array::{Array, RecordBatch};
use arrow_schema::DataType;
use jiff::ToSpan;
use jiff::civil::{Date, Weekday};
use parquet::arrow::ProjectionMask;
use parquet::arrow::arrow_reader::ParquetRecordBatchReaderBuilder;
use serde::Deserialize;

use crate::timetable::{SERVICE_DAY_START, StopIdx, Timetable};

/// Station complex IDs run to ~640.
pub type ComplexId = u16;

/// Riders in ten-thousandths: the OD Parquet's `DECIMAL(9,4)`, exactly,
/// in half an `f64`'s space (an `f32` can't hold 4 decimal places past 1,024).
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, PartialOrd, Ord)]
pub struct Riders(pub u32);

impl Riders {
    /// Decimal places.
    pub const SCALE: i8 = 4;
    const UNIT: f64 = 1e4;

    /// Rounded to the nearest ten-thousandth.
    pub fn from_f64(riders: f64) -> Self {
        Self((riders * Self::UNIT).round() as u32)
    }

    pub fn to_f64(self) -> f64 {
        f64::from(self.0) / Self::UNIT
    }
}

/// One OD row: average riders on a (month, day of week) from one complex to another,
/// entering in one hour.
#[derive(Clone, Debug, PartialEq)]
pub struct OdRow {
    pub hour: u8,
    pub origin: ComplexId,
    pub destination: ComplexId,
    pub riders: Riders,
}

const YEAR: &str = "Year";
const MONTH: &str = "Month";
const DAY_OF_WEEK: &str = "Day of Week";
const HOUR: &str = "Hour of Day";
const ORIGIN: &str = "Origin Station Complex ID";
const DESTINATION: &str = "Destination Station Complex ID";
const RIDERSHIP: &str = "Estimated Average Ridership";

/// The OD data's name for `date`'s day of week.
pub fn day_of_week(date: Date) -> &'static str {
    match date.weekday() {
        Weekday::Monday => "Monday",
        Weekday::Tuesday => "Tuesday",
        Weekday::Wednesday => "Wednesday",
        Weekday::Thursday => "Thursday",
        Weekday::Friday => "Friday",
        Weekday::Saturday => "Saturday",
        Weekday::Sunday => "Sunday",
    }
}

/// Rows of the OD Parquet (`mta-od-data prepare`'s output)
/// for `date`'s service day (see `SERVICE_DAY_START`):
/// its (year, month, day of week)'s hours from the start,
/// and the next date's before it, as hours from 24.
pub fn load_service_day(path: &Path, date: Date) -> Result<Vec<OdRow>> {
    let mut days = load_service_days(path, &[date])?;
    Ok(days.pop().unwrap_or_default())
}

/// `load_service_day` for each of `dates`, in one read of the file.
pub fn load_service_days(path: &Path, dates: &[Date]) -> Result<Vec<Vec<OdRow>>> {
    let file = File::open(path).with_context(|| format!("opening {}", path.display()))?;
    let builder = ParquetRecordBatchReaderBuilder::try_new(file)?;
    let schema = builder.parquet_schema();
    let columns = [
        YEAR,
        MONTH,
        DAY_OF_WEEK,
        HOUR,
        ORIGIN,
        DESTINATION,
        RIDERSHIP,
    ];
    let indices = columns
        .iter()
        .map(|&name| {
            schema
                .columns()
                .iter()
                .position(|c| c.name() == name)
                .with_context(|| format!("{} has no column {name:?}", path.display()))
        })
        .collect::<Result<Vec<_>>>()?;
    let mask = ProjectionMask::leaves(schema, indices);
    let reader = builder.with_projection(mask).build()?;

    let start = i64::from(SERVICE_DAY_START / (60 * 60));
    let mut slices = Vec::new();
    for (k, &date) in dates.iter().enumerate() {
        slices.push(Slice::new(date, start..24, 0, k));
        slices.push(Slice::new(date.checked_add(1.day())?, 0..start, 24, k));
    }
    let mut rows = vec![Vec::new(); dates.len()];
    for batch in reader {
        read_batch(&batch?, &slices, &mut rows)?;
    }
    Ok(rows)
}

/// Some hours of one (year, month, day of week) of the OD data,
/// and the service day they go to.
struct Slice {
    year: i64,
    month: i64,
    day: &'static str,
    hours: Range<i64>,
    /// Added to their hours, onto the service day's clock.
    shift: u8,
    /// Which service day.
    to: usize,
}

impl Slice {
    fn new(date: Date, hours: Range<i64>, shift: u8, to: usize) -> Self {
        Self {
            year: i64::from(date.year()),
            month: i64::from(date.month()),
            day: day_of_week(date),
            hours,
            shift,
            to,
        }
    }
}

/// Appends `batch`'s rows in each of `slices` to its service day's `rows`.
fn read_batch(batch: &RecordBatch, slices: &[Slice], rows: &mut [Vec<OdRow>]) -> Result<()> {
    let column = |name: &str| {
        batch
            .column_by_name(name)
            .with_context(|| format!("no column {name:?}"))
    };
    let int = |name: &str| -> Result<_> {
        column(name)?
            .as_primitive_opt::<Int64Type>()
            .with_context(|| format!("{name:?} isn't INT64"))
    };
    let (years, months, hours) = (int(YEAR)?, int(MONTH)?, int(HOUR)?);
    let (origins, destinations) = (int(ORIGIN)?, int(DESTINATION)?);
    let days = column(DAY_OF_WEEK)?;
    let days = days
        .as_string_opt::<i32>()
        .with_context(|| format!("{DAY_OF_WEEK:?} isn't a string"))?;
    let ridership = column(RIDERSHIP)?;
    let DataType::Decimal128(_, scale) = *ridership.data_type() else {
        bail!("{RIDERSHIP:?} is {}, not a decimal", ridership.data_type());
    };
    if scale != Riders::SCALE {
        bail!("{RIDERSHIP:?} has scale {scale}, not {}", Riders::SCALE);
    }
    let ridership = ridership.as_primitive::<Decimal128Type>();

    for i in 0..batch.num_rows() {
        let (year, month, hour) = (years.value(i), months.value(i), hours.value(i));
        // Two service days may share a (year, month, day of week): both get its rows.
        let mut matching = slices
            .iter()
            .filter(|s| {
                s.year == year
                    && s.month == month
                    && s.hours.contains(&hour)
                    && s.day == days.value(i)
            })
            .peekable();
        if matching.peek().is_none() {
            continue;
        }
        if [
            years.is_null(i),
            hours.is_null(i),
            origins.is_null(i),
            destinations.is_null(i),
            ridership.is_null(i),
        ]
        .contains(&true)
        {
            bail!("OD row with a null");
        }
        let row = OdRow {
            hour: u8::try_from(hour)?,
            origin: ComplexId::try_from(origins.value(i))?,
            destination: ComplexId::try_from(destinations.value(i))?,
            riders: Riders(u32::try_from(ridership.value(i))?),
        };
        for s in matching {
            rows[s.to].push(OdRow {
                hour: row.hour + s.shift,
                ..row.clone()
            });
        }
    }
    Ok(())
}

#[derive(Deserialize)]
struct StationRow {
    gtfs_stop_id: String,
    complex_id: ComplexId,
}

/// Each complex's stops in a timetable,
/// from the station reference CSV (`data/stations.csv`).
pub struct Complexes {
    pub stops: BTreeMap<ComplexId, Vec<StopIdx>>,
    /// `gtfs_stop_id`s the timetable doesn't have.
    pub unknown_stops: Vec<String>,
    /// Stops the timetable has but no trip serves on its date.
    pub unserved_stops: Vec<String>,
}

impl Complexes {
    pub fn load(stations_csv: &Path, tt: &Timetable) -> Result<Self> {
        let served: HashSet<StopIdx> = tt
            .patterns
            .iter()
            .flat_map(|p| p.stops.iter().copied())
            .collect();
        let mut complexes = Self {
            stops: BTreeMap::new(),
            unknown_stops: Vec::new(),
            unserved_stops: Vec::new(),
        };
        let mut reader = csv::Reader::from_path(stations_csv)
            .with_context(|| format!("opening {}", stations_csv.display()))?;
        for row in reader.deserialize() {
            let row: StationRow = row?;
            let stops = complexes.stops.entry(row.complex_id).or_default();
            match tt.stop(&row.gtfs_stop_id) {
                None => complexes.unknown_stops.push(row.gtfs_stop_id),
                Some(s) if !served.contains(&s) => complexes.unserved_stops.push(row.gtfs_stop_id),
                Some(s) => stops.push(s),
            }
        }
        Ok(complexes)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    use std::sync::Arc;

    use arrow_array::{Decimal128Array, Int64Array, StringArray};
    use parquet::arrow::ArrowWriter;

    #[test]
    fn service_day_of_parquet() {
        let ints = |v: &[i64]| Arc::new(Int64Array::from(v.to_vec())) as Arc<dyn Array>;
        let batch = RecordBatch::try_from_iter([
            (YEAR, ints(&[2025, 2025, 2025, 2024, 2025, 2025, 2025])),
            (MONTH, ints(&[9, 9, 10, 9, 9, 9, 9])),
            (
                DAY_OF_WEEK,
                Arc::new(StringArray::from(vec![
                    "Wednesday",
                    "Tuesday",
                    "Wednesday",
                    "Wednesday",
                    "Wednesday",
                    "Thursday",
                    "Thursday",
                ])) as _,
            ),
            (HOUR, ints(&[8, 8, 8, 8, 2, 3, 4])),
            (ORIGIN, ints(&[1, 1, 1, 1, 1, 1, 1])),
            (DESTINATION, ints(&[2, 2, 2, 2, 2, 2, 2])),
            (
                RIDERSHIP,
                Arc::new(
                    Decimal128Array::from(vec![12_345, 1, 1, 1, 1, 7, 1])
                        .with_precision_and_scale(9, 4)
                        .unwrap(),
                ) as _,
            ),
        ])
        .unwrap();
        let path =
            std::env::temp_dir().join(format!("raptor-od-test-{}.parquet", std::process::id()));
        let mut writer =
            ArrowWriter::try_new(File::create(&path).unwrap(), batch.schema(), None).unwrap();
        writer.write(&batch).unwrap();
        writer.close().unwrap();

        let rows = load_service_day(&path, Date::new(2025, 9, 3).unwrap());
        std::fs::remove_file(&path).unwrap();
        let row = |hour, riders| OdRow {
            hour,
            origin: 1,
            destination: 2,
            riders: Riders(riders),
        };
        // Wednesday's 02:00 is Tuesday's service day's, and Thursday's 03:00 Wednesday's.
        assert_eq!(rows.unwrap(), [row(8, 12_345), row(27, 7)]);
    }

    #[test]
    fn day_names() {
        assert_eq!(day_of_week(Date::new(2025, 9, 3).unwrap()), "Wednesday");
        assert_eq!(day_of_week(Date::new(2025, 9, 7).unwrap()), "Sunday");
    }
}
