//! RAPTOR journey assignment for the MTA OD data; see `raptor_design.md`.

mod assign;
mod calendar;
mod gtfs;
mod od;
mod raptor;
mod timetable;

use std::path::PathBuf;

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use jiff::civil::Date;

use crate::assign::{Config, assign, write_paths};
use crate::gtfs::{Feed, Secs, parse_time};
use crate::od::{Complexes, load_slice};
use crate::raptor::{Journey, Leg, Router};
use crate::timetable::{DEFAULT_MIN_CHANGE, NEXT_DATE_HORIZON, Timetable};

#[derive(Parser)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Load a static GTFS feed zip and summarize it.
    Feed {
        /// A feed zip, e.g. from `mta-od-data fetch-gtfs`.
        #[arg(long)]
        feed: PathBuf,
    },
    /// Build one service date's timetable and report what it found.
    Timetable {
        #[arg(long)]
        feed: PathBuf,
        /// The service date, e.g. `2025-09-03`.
        #[arg(long)]
        date: Date,
    },
    /// Earliest-arrival journeys between two stops, one per number of rides.
    Route {
        #[arg(long)]
        feed: PathBuf,
        #[arg(long)]
        date: Date,
        /// Origin stop IDs (parent stations, e.g. `127`); several means any of them.
        #[arg(long, num_args = 1.., required = true)]
        from: Vec<String>,
        /// Destination stop IDs; several means any of them.
        #[arg(long, num_args = 1.., required = true)]
        to: Vec<String>,
        /// Departure time, `HH:MM:SS` from the service date's start.
        #[arg(long, value_parser = parse_secs)]
        depart: Secs,
    },
    /// Load the OD rows for a date's (year, month, day of week),
    /// and map their station complexes to the date's timetable.
    Od {
        #[arg(long)]
        feed: PathBuf,
        #[arg(long)]
        date: Date,
        /// The OD Parquet, from `mta-od-data prepare`.
        #[arg(long, default_value = "../data/mta_od.parquet")]
        od: PathBuf,
        /// The station reference CSV, from `mta-od-data prepare`.
        #[arg(long, default_value = "../data/stations.csv")]
        stations: PathBuf,
    },
    /// Split a date's OD rows across their journeys, and write the paths taken.
    Assign {
        #[arg(long)]
        feed: PathBuf,
        #[arg(long)]
        date: Date,
        #[arg(long, default_value = "../data/mta_od.parquet")]
        od: PathBuf,
        #[arg(long, default_value = "../data/stations.csv")]
        stations: PathBuf,
        /// Generalized cost weights.
        #[arg(long, default_value = "assign.json5")]
        config: PathBuf,
        /// Output Parquet (default: `../data/raptor/paths-<date>.parquet`).
        #[arg(long)]
        out: Option<PathBuf>,
    },
    /// Every Pareto-optimal journey between two stops departing in a window.
    Profile {
        #[arg(long)]
        feed: PathBuf,
        #[arg(long)]
        date: Date,
        #[arg(long, num_args = 1.., required = true)]
        from: Vec<String>,
        #[arg(long, num_args = 1.., required = true)]
        to: Vec<String>,
        /// Window start, `HH:MM:SS`, inclusive.
        #[arg(long, value_parser = parse_secs)]
        after: Secs,
        /// Window end, `HH:MM:SS`, exclusive.
        #[arg(long, value_parser = parse_secs)]
        before: Secs,
    },
}

fn parse_secs(s: &str) -> Result<Secs, String> {
    parse_time(s).ok_or_else(|| format!("expected HH:MM:SS, got {s:?}"))
}

fn main() -> Result<()> {
    match Cli::parse().command {
        Command::Feed { feed } => {
            let feed = Feed::open(&feed)?;
            println!("stops: {}", feed.stops.len());
            println!("trips: {}", feed.trips.len());
            println!("stop_times: {}", feed.stop_times.len());
            println!("calendar: {}", feed.calendar.len());
            println!("calendar_dates: {}", feed.calendar_dates.len());
            println!("transfers: {}", feed.transfers.len());
        }
        Command::Timetable { feed, date } => {
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            print_report(&tt);
        }
        Command::Route {
            feed,
            date,
            from,
            to,
            depart,
        } => {
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            let (from, to) = (stops(&tt, &from)?, stops(&tt, &to)?);
            let router = Router::new(&tt);
            print_journeys(&tt, &router.query(&from, depart).journeys(&to));
        }
        Command::Od {
            feed,
            date,
            od,
            stations,
        } => {
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            let complexes = Complexes::load(&stations, &tt)?;
            let rows = load_slice(&od, date)?;
            print_od(&complexes, &rows);
        }
        Command::Assign {
            feed,
            date,
            od,
            stations,
            config,
            out,
        } => {
            let start = std::time::Instant::now();
            let (config_values, config_text) = Config::load(&config)?;
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            let complexes = Complexes::load(&stations, &tt)?;
            let rows = load_slice(&od, date)?;
            println!("loaded in {:.1?}", start.elapsed());
            let (paths, unassigned) = assign(&tt, &complexes, &rows, &config_values);
            println!("assigned in {:.1?}", start.elapsed());
            let out = out.unwrap_or_else(|| format!("../data/raptor/paths-{date}.parquet").into());
            let metadata = vec![
                ("feed".to_string(), feed.display().to_string()),
                ("date".to_string(), date.to_string()),
                ("config".to_string(), config_text),
            ];
            write_paths(&out, &paths, date, metadata)?;
            println!("wrote {} paths to {}", paths.len(), out.display());
            print_assignment(&rows, &paths, &unassigned);
        }
        Command::Profile {
            feed,
            date,
            from,
            to,
            after,
            before,
        } => {
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            let (from, to) = (stops(&tt, &from)?, stops(&tt, &to)?);
            let router = Router::new(&tt);
            let mut journeys = router.profile(&from, after, before, &[&to]);
            journeys[0].sort_by_key(|j| (j.depart, j.rides()));
            print_journeys(&tt, &journeys[0]);
        }
    }
    Ok(())
}

/// At most this many examples of each problem.
const EXAMPLES: usize = 5;

fn print_report(tt: &Timetable) {
    let r = &tt.report;
    let trips: usize = tt.patterns.iter().map(|p| p.trips.len()).sum();
    println!("date: {} ({:?})", tt.date, tt.date.weekday());
    println!("services: {}", r.services.join(", "));
    println!(
        "trips: {} today + {} overnight from the previous date",
        r.trips, r.overnight_trips
    );
    println!(
        "  + {} from the next date starting before {}",
        r.next_date_trips,
        hms(NEXT_DATE_HORIZON)
    );
    if r.next_date_missing {
        println!("warning: the next date is outside the feed, so its early trips are missing");
    }
    if r.previous_date_missing {
        println!(
            "warning: the previous date is outside the feed, so its overnight trips are missing"
        );
    }
    let served = tt
        .patterns
        .iter()
        .flat_map(|p| &p.stops)
        .collect::<std::collections::HashSet<_>>();
    println!("stops: {} parents, {} served", tt.stops.len(), served.len());
    println!(
        "patterns: {} ({} from FIFO splits), {trips} trips",
        tt.patterns.len(),
        r.fifo_splits
    );
    println!(
        "duplicate trips: {} {:?}",
        r.duplicate_trips.len(),
        &r.duplicate_trips[..r.duplicate_trips.len().min(EXAMPLES)]
    );
    println!("transfer types: {:?}", r.transfer_types);
    println!("transfers without a time: {}", r.transfers_without_time);
    println!(
        "served stops on the default {DEFAULT_MIN_CHANGE}s change: {}",
        r.default_change_stops
    );
    let zero = tt.min_change.iter().filter(|&&c| c == 0).count();
    println!("stops with a 0s change: {zero}");
    let footpaths: usize = tt.footpaths.iter().map(Vec::len).sum();
    println!("footpaths: {footpaths}");
    println!(
        "asymmetric footpaths: {} {:?}",
        r.asymmetric_footpaths.len(),
        &r.asymmetric_footpaths[..r.asymmetric_footpaths.len().min(EXAMPLES)]
    );
    println!(
        "unclosed footpaths: {} {:?}",
        r.unclosed_footpaths.len(),
        &r.unclosed_footpaths[..r.unclosed_footpaths.len().min(EXAMPLES)]
    );
}

fn stops(tt: &Timetable, ids: &[String]) -> Result<Vec<u32>> {
    ids.iter()
        .map(|id| tt.stop(id).with_context(|| format!("no stop {id}")))
        .collect()
}

fn print_journeys(tt: &Timetable, journeys: &[Journey]) {
    if journeys.is_empty() {
        println!("no journey");
    }
    for journey in journeys {
        print_journey(tt, journey);
    }
}

pub fn hms(t: Secs) -> String {
    let sign = if t < 0 { "-" } else { "" };
    let t = t.abs();
    format!("{sign}{:02}:{:02}:{:02}", t / 3600, t / 60 % 60, t % 60)
}

fn print_journey(tt: &Timetable, j: &Journey) {
    let name = |s: u32| {
        let stop = &tt.stops[s as usize];
        format!("{} ({})", stop.name, stop.id)
    };
    println!(
        "depart {}, {} rides, arrive {} ({} min)",
        hms(j.depart),
        j.rides(),
        hms(j.arrive),
        (j.arrive - j.depart) / 60
    );
    for leg in &j.legs {
        match *leg {
            Leg::Ride {
                pattern,
                board_stop,
                alight_stop,
                depart,
                arrive,
                ..
            } => println!(
                "  {} {} {} -> {} {}",
                tt.patterns[pattern as usize].route_id,
                hms(depart),
                name(board_stop),
                hms(arrive),
                name(alight_stop),
            ),
            Leg::Walk { from, to, duration } => {
                println!("  walk {}s {} -> {}", duration, name(from), name(to))
            }
        }
    }
}

fn print_od(complexes: &Complexes, rows: &[od::OdRow]) {
    use std::collections::BTreeSet;
    let total = riders(rows.iter());
    let origins: BTreeSet<_> = rows.iter().map(|r| r.origin).collect();
    let destinations: BTreeSet<_> = rows.iter().map(|r| r.destination).collect();
    let hours: BTreeSet<_> = rows.iter().map(|r| r.hour).collect();
    println!("rows: {}", rows.len());
    println!("riders: {total:.4}");
    println!(
        "origins: {}, destinations: {}, hours: {hours:?}",
        origins.len(),
        destinations.len()
    );
    println!("stops not in the timetable: {:?}", complexes.unknown_stops);
    println!(
        "stops not served on the date: {:?}",
        complexes.unserved_stops
    );
    let stopless = |c: &od::ComplexId| complexes.stops.get(c).is_none_or(Vec::is_empty);
    let unmapped: BTreeSet<_> = origins
        .iter()
        .chain(&destinations)
        .filter(|c| stopless(c))
        .collect();
    let unmapped_riders = riders(
        rows.iter()
            .filter(|r| stopless(&r.origin) || stopless(&r.destination)),
    );
    println!("complexes with no served stop: {unmapped:?} ({unmapped_riders:.4} riders)");
    let same = riders(rows.iter().filter(|r| r.origin == r.destination));
    println!("riders with the same origin and destination: {same:.4}");
}

/// Not `Sum`, which gives -0.0 for nothing.
fn riders<'a>(rows: impl Iterator<Item = &'a od::OdRow>) -> f64 {
    rows.fold(0.0, |sum, r| sum + r.riders)
}

fn print_assignment(
    rows: &[od::OdRow],
    paths: &[assign::PathRow],
    unassigned: &assign::Unassigned,
) {
    let input = riders(rows.iter());
    let assigned = paths.iter().fold(0.0, |sum, p| sum + p.riders);
    println!(
        "riders: {input:.4} in, {assigned:.4} assigned, {:.4} unassigned",
        unassigned.total()
    );
    println!(
        "  unassigned: {:.4} no served stop, {:.4} unreachable in {} rides, {:.4} after the last departure",
        unassigned.no_stops,
        unassigned.unreachable,
        raptor::MAX_RIDES,
        unassigned.no_departure
    );
    println!(
        "  conservation error: {:.6}",
        input - assigned - unassigned.total()
    );
    let mut by_rides = [0.0; raptor::MAX_RIDES + 1];
    let mut minutes = 0.0;
    for p in paths {
        by_rides[p.rides as usize] += p.riders;
        minutes += p.riders * p.total / 60.0;
    }
    for (k, r) in by_rides.iter().enumerate().skip(1) {
        println!("  {k} rides: {:.1}%", 100.0 * r / assigned);
    }
    println!("  mean journey: {:.1} min", minutes / assigned);
}
