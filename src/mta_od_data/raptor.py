"""RAPTOR journey assignment of the OD data (see `raptor/raptor_design.md`).

The routing is the `raptor` crate's, through `mta_od_data._raptor`;
this drives it and writes the manifest of dates run.
"""

from csv import DictWriter
from datetime import date
from pathlib import Path
from typing import Annotated

from typer import Option, Typer

from mta_od_data import DATA, ROOT
from mta_od_data._raptor import (
    Version,
    assign_date,
    assign_dates,
    feed_report,
    load_versions,
    od_report,
    pick_weekdays,
    profile_report,
    route_report,
    timetable_report,
)
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.prepare import DEFAULT_PARQUET

app = Typer()

DEFAULT_STATIONS = DATA / "stations.csv"
DEFAULT_CONFIG = ROOT / "raptor" / "assign.json5"
DEFAULT_OUT_DIR = DATA / "raptor"
MANIFEST_FIELDS = [
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
]

Feed = Annotated[Path, Option(help="A feed zip, from `mta-od-data fetch-gtfs`")]
Day = Annotated[
    date, Option(parser=date.fromisoformat, help="The service date, e.g. 2025-09-17")
]
Stops = Annotated[
    list[str],
    Option(help="Parent stop ID, e.g. 127 (repeatable; several means any of them)"),
]
Od = Annotated[Path, Option(help="The OD Parquet, from `mta-od-data prepare`")]
Stations = Annotated[Path, Option(help="The station reference CSV")]
Config = Annotated[Path, Option(help="Generalized cost weights")]


@app.command()
def feed(feed: Feed) -> None:
    """Load a static GTFS feed zip and summarize it."""
    print(feed_report(feed), end="")


@app.command()
def timetable(feed: Feed, date: Day) -> None:
    """Build one service date's timetable and report what it found."""
    print(timetable_report(feed, date), end="")


@app.command()
def route(
    feed: Feed,
    date: Day,
    origin: Stops,
    destination: Stops,
    depart: Annotated[
        str, Option(help="Departure time, HH:MM:SS from the service date's start")
    ],
) -> None:
    """Earliest-arrival journeys between two stops, one per number of rides."""
    print(route_report(feed, date, origin, destination, depart), end="")


@app.command()
def profile(
    feed: Feed,
    date: Day,
    origin: Stops,
    destination: Stops,
    after: Annotated[str, Option(help="Window start, HH:MM:SS, inclusive")],
    before: Annotated[str, Option(help="Window end, HH:MM:SS, exclusive")],
) -> None:
    """Every Pareto-optimal journey between two stops departing in a window."""
    print(profile_report(feed, date, origin, destination, after, before), end="")


@app.command()
def od(
    feed: Feed,
    date: Day,
    od: Od = DEFAULT_PARQUET,
    stations: Stations = DEFAULT_STATIONS,
) -> None:
    """Load the OD rows for a date's service day, 04:00 to 04:00:
    its (year, month, day of week)'s hours 4 to 23 and the next date's 0 to 3,
    and map their station complexes to the date's timetable."""
    print(od_report(feed, date, od, stations), end="")


@app.command()
def assign(
    feed: Feed,
    date: Day,
    od: Od = DEFAULT_PARQUET,
    stations: Stations = DEFAULT_STATIONS,
    config: Config = DEFAULT_CONFIG,
    out: Annotated[
        Path | None,
        Option(help="Output Parquet (default: data/raptor/paths-<date>.parquet)"),
    ] = None,
) -> None:
    """Split a date's OD rows across their journeys, and write the paths taken."""
    out = out or DEFAULT_OUT_DIR / f"paths-{date}.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    summary = assign_date(Version.open(feed), date, od, stations, config, out)
    print(summary.report, end="")
    print(f"wrote {out}")


@app.command()
def assign_range(
    start: Annotated[
        date, Option("--from", parser=date.fromisoformat, help="First date, inclusive")
    ],
    end: Annotated[
        date, Option("--to", parser=date.fromisoformat, help="Last date, inclusive")
    ],
    gtfs_dir: Annotated[
        Path, Option(help="Feed version zips, from `mta-od-data fetch-gtfs`")
    ] = DEFAULT_GTFS_DIR,
    od: Od = DEFAULT_PARQUET,
    stations: Stations = DEFAULT_STATIONS,
    config: Config = DEFAULT_CONFIG,
    out_dir: Annotated[
        Path, Option(help="Where the path Parquets and manifest.csv go")
    ] = DEFAULT_OUT_DIR,
) -> None:
    """`assign` each (month, weekday) in a date range on a representative date,
    with the latest feed version covering it,
    and write a manifest of the dates run and how many days each stands for.
    Dates whose timetables route alike share one routing.

    \b
    Examples:
        mta-od-data raptor assign-range --from 2025-08-11 --to 2025-12-31
    """
    picks = pick_weekdays(load_versions(gtfs_dir), start, end)
    out_dir.mkdir(parents=True, exist_ok=True)
    outs = [out_dir / f"paths-{day}.parquet" for day, _, _ in picks]
    summaries = assign_dates(
        [
            (version, day, out)
            for (day, version, _), out in zip(picks, outs, strict=True)
        ],
        od,
        stations,
        config,
    )
    manifest_path = out_dir / "manifest.csv"
    with manifest_path.open("w", newline="") as f:
        manifest = DictWriter(f, MANIFEST_FIELDS)
        manifest.writeheader()
        for (day, version, days), out, s in zip(picks, outs, summaries, strict=True):
            print(f"== {day} ({day:%A})")
            print(s.report, end="")
            manifest.writerow(
                {
                    "date": day,
                    "year": day.year,
                    "month": day.month,
                    "day_of_week": f"{day:%A}",
                    "days": days,
                    "feed": version.path,
                    "paths": out,
                    "riders_in": s.riders_in,
                    "riders_assigned": s.riders_assigned,
                    "unassigned_no_stops": s.unassigned_no_stops,
                    "unassigned_unreachable": s.unassigned_unreachable,
                    "unassigned_no_departure": s.unassigned_no_departure,
                }
            )
    print(f"wrote {manifest_path}")
