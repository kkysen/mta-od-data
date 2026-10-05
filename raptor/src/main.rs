//! RAPTOR journey assignment for the MTA OD data; see `raptor_design.md`.

mod calendar;
mod gtfs;
mod raptor;
mod timetable;

use std::path::PathBuf;

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use jiff::civil::Date;

use crate::gtfs::{Feed, Secs, parse_time};
use crate::raptor::{Journey, Leg, Router};
use crate::timetable::{DEFAULT_MIN_CHANGE, Timetable};

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
            let stops = |ids: &[String]| {
                ids.iter()
                    .map(|id| tt.stop(id).with_context(|| format!("no stop {id}")))
                    .collect::<Result<Vec<_>>>()
            };
            let (from, to) = (stops(&from)?, stops(&to)?);
            let router = Router::new(&tt);
            let journeys = router.query(&from, depart).journeys(&to);
            if journeys.is_empty() {
                println!("no journey");
            }
            for journey in &journeys {
                print_journey(&tt, journey);
            }
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

fn hms(t: Secs) -> String {
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
        "{} rides, arrive {} ({} min)",
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
