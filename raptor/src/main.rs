//! RAPTOR journey assignment for the MTA OD data; see `raptor_design.md`.

use std::path::PathBuf;

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use jiff::civil::{Date, Weekday};

use raptor::assign_date;
use raptor::batch::{Version, load_versions, pick_dates};
use raptor::gtfs::{Feed, Secs, parse_time};
use raptor::od::{self, Complexes, load_slice};
use raptor::raptor::Router;
use raptor::report;
use raptor::timetable::Timetable;

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
    /// `assign` each (month, weekday) in a date range on a representative date,
    /// with the latest feed version covering it,
    /// and write a manifest of the dates run and how many days each stands for.
    AssignRange {
        /// Feed version zips, from `mta-od-data fetch-gtfs`.
        #[arg(long, default_value = "../data/gtfs")]
        gtfs_dir: PathBuf,
        /// First date, inclusive.
        #[arg(long)]
        from: Date,
        /// Last date, inclusive.
        #[arg(long)]
        to: Date,
        #[arg(long, default_value = "../data/mta_od.parquet")]
        od: PathBuf,
        #[arg(long, default_value = "../data/stations.csv")]
        stations: PathBuf,
        #[arg(long, default_value = "assign.json5")]
        config: PathBuf,
        /// Where the path Parquets and `manifest.csv` go.
        #[arg(long, default_value = "../data/raptor")]
        out_dir: PathBuf,
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

fn default_paths_out(date: Date) -> PathBuf {
    format!("../data/raptor/paths-{date}.parquet").into()
}

fn parse_secs(s: &str) -> Result<Secs, String> {
    parse_time(s).ok_or_else(|| format!("expected HH:MM:SS, got {s:?}"))
}

fn stops(tt: &Timetable, ids: &[String]) -> Result<Vec<u32>> {
    ids.iter()
        .map(|id| tt.stop(id).with_context(|| format!("no stop {id}")))
        .collect()
}

fn main() -> Result<()> {
    match Cli::parse().command {
        Command::Feed { feed } => print!("{}", report::feed(&Feed::open(&feed)?)),
        Command::Timetable { feed, date } => {
            let tt = Timetable::build(&Feed::open(&feed)?, date)?;
            print!("{}", report::timetable(&tt));
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
            let journeys = router.query(&from, depart).journeys(&to);
            print!("{}", report::journeys(&tt, &journeys));
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
            print!("{}", report::od(&complexes, &rows));
        }
        Command::Assign {
            feed,
            date,
            od,
            stations,
            config,
            out,
        } => {
            let out = out.unwrap_or_else(|| default_paths_out(date));
            let s = assign_date(&Version::open(&feed)?, date, &od, &stations, &config, &out)?;
            print!("{}", s.report);
            println!("wrote {}", out.display());
        }
        Command::AssignRange {
            gtfs_dir,
            from,
            to,
            od,
            stations,
            config,
            out_dir,
        } => {
            let versions = load_versions(&gtfs_dir)?;
            let refs: Vec<&Version> = versions.iter().collect();
            let weekdays = [
                Weekday::Monday,
                Weekday::Tuesday,
                Weekday::Wednesday,
                Weekday::Thursday,
                Weekday::Friday,
            ];
            let picks = pick_dates(&refs, from, to, &weekdays)?;
            std::fs::create_dir_all(&out_dir)?;
            let mut manifest = csv::Writer::from_path(out_dir.join("manifest.csv"))?;
            manifest.write_record([
                "date",
                "year",
                "month",
                "day_of_week",
                "days",
                "feed",
                "paths",
                "riders_in",
                "riders_assigned",
                "unassigned_no_stops",
                "unassigned_unreachable",
                "unassigned_no_departure",
            ])?;
            for pick in &picks {
                let version = refs[pick.version];
                let out = out_dir.join(format!("paths-{}.parquet", pick.date));
                println!("== {} ({:?})", pick.date, pick.date.weekday());
                let s = assign_date(version, pick.date, &od, &stations, &config, &out)?;
                print!("{}", s.report);
                manifest.write_record([
                    pick.date.to_string(),
                    pick.date.year().to_string(),
                    pick.date.month().to_string(),
                    od::day_of_week(pick.date).to_string(),
                    pick.days.to_string(),
                    version.path.display().to_string(),
                    out.display().to_string(),
                    s.riders_in.to_string(),
                    s.riders_assigned.to_string(),
                    s.unassigned_no_stops.to_string(),
                    s.unassigned_unreachable.to_string(),
                    s.unassigned_no_departure.to_string(),
                ])?;
                manifest.flush()?;
            }
            println!("wrote {}", out_dir.join("manifest.csv").display());
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
            print!("{}", report::journeys(&tt, &journeys[0]));
        }
    }
    Ok(())
}
