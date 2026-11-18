"""RAPTOR journey assignment of the OD data (see `raptor/raptor_design.md`).

The routing is the `raptor` crate's, through `mta_od_data._raptor`;
this is its command line, and `routing.py` routes a range of dates for `assign-range`.
"""

from datetime import date, timedelta
from pathlib import Path
from typing import Annotated

from typer import BadParameter, Option, Typer

from mta_od_data import DATA, ROOT
from mta_od_data._raptor import (
    DEFAULT_MAX_RIDES,
    Version,
    assign_date,
    feed_report,
    load_versions,
    od_report,
    profile_report,
    route_report,
    timetable_report,
)
from mta_od_data.access import TABLE as DEFAULT_ACCESS
from mta_od_data.downloads import gtfs_feeds, od_parquet
from mta_od_data.platforms import DEFAULT_OUT as DEFAULT_PLATFORMS
from mta_od_data.routing import route_range
from mta_od_data.street_walks import cut

app = Typer()

DEFAULT_STATIONS = DATA / "stations.csv"
DEFAULT_CONFIG = ROOT / "raptor" / "assign.json5"
DEFAULT_OUT_DIR = DATA / "raptor"

Day = Annotated[
    date, Option(parser=date.fromisoformat, help="The service date, e.g. 2025-09-17")
]
Stops = Annotated[
    list[str],
    Option(help="Parent stop ID, e.g. 127 (repeatable; several means any of them)"),
]
MaxRides = Annotated[int, Option(min=1, max=255, help="Most rides in a journey")]
Config = Annotated[Path, Option(help="Generalized cost weights")]
StreetWalks = Annotated[
    bool,
    Option(
        help="Also change trains between complexes on the streets, "
        "out of the system and back in with no fare, "
        "walked each run at `--config`'s speeds, "
        "writing the transfers added beside each date's paths"
    ),
]


def streets_to_walk(street_walks: bool) -> tuple[Path, Path] | None:
    """With `street_walks`, the streets, cut if need be, and the entrances, to walk."""
    return (cut(), DEFAULT_ACCESS) if street_walks else None


def feed_for(day: date) -> Path:
    """The latest-fetched feed version covering `day` and both its neighbors,
    so its overnight trips from the previous date and early ones from the next
    are there, with every version in `gtfs_versions.json5` fetched when missing."""
    one = timedelta(days=1)
    covering = [
        v
        for v in load_versions(gtfs_feeds())
        if v.start <= day - one and day + one <= v.end
    ]
    return covering[-1].path


ZSTD_LEVELS = {"fast": 1, "medium": 6, "slow": 9}


def parse_zstd_level(value: str) -> int:
    """A zstd level, or one of `ZSTD_LEVELS`' names for one."""
    if value in ZSTD_LEVELS:
        return ZSTD_LEVELS[value]
    try:
        return int(value)
    except ValueError:
        raise BadParameter(
            f"{value!r} is not fast, medium, slow, or a number",
            param_hint="'--zstd-level'",
        ) from None


# A name or number, parsed by the commands with `parse_zstd_level`:
# Typer has no union type for `int` with a default of "fast".
ZstdLevel = Annotated[
    str,
    Option(
        metavar="[fast|medium|slow|LEVEL]",
        help=(
            "zstd level of the path Parquets: fast (1) writes fastest; "
            "medium (6) and slow (9) make the path texts ~2/3 the size, "
            "for outputs to keep"
        ),
    ),
]


@app.command()
def feed() -> None:
    """Load the latest static GTFS feed version and summarize it."""
    print(feed_report(load_versions(gtfs_feeds())[-1].path), end="")


@app.command()
def timetable(date: Day) -> None:
    """Build one service date's timetable and report what it found."""
    print(timetable_report(feed_for(date), date), end="")


@app.command()
def route(
    date: Day,
    origin: Stops,
    destination: Stops,
    depart: Annotated[
        str, Option(help="Departure time, HH:MM:SS from the service date's start")
    ],
    max_rides: MaxRides = DEFAULT_MAX_RIDES,
) -> None:
    """Earliest-arrival journeys between two stops, one per number of rides."""
    print(
        route_report(feed_for(date), date, origin, destination, depart, max_rides),
        end="",
    )


@app.command()
def profile(
    date: Day,
    origin: Stops,
    destination: Stops,
    after: Annotated[str, Option(help="Window start, HH:MM:SS, inclusive")],
    before: Annotated[str, Option(help="Window end, HH:MM:SS, exclusive")],
    max_rides: MaxRides = DEFAULT_MAX_RIDES,
) -> None:
    """Every Pareto-optimal journey between two stops departing in a window."""
    print(
        profile_report(
            feed_for(date), date, origin, destination, after, before, max_rides
        ),
        end="",
    )


@app.command()
def od(date: Day) -> None:
    """Load the OD rows for a date's service day, 04:00 to 04:00:
    its (year, month, day of week)'s hours 4 to 23 and the next date's 0 to 3,
    and map their station complexes to the date's timetable."""
    print(
        od_report(feed_for(date), date, od_parquet(), DEFAULT_STATIONS),
        end="",
    )


@app.command()
def assign(
    date: Day,
    config: Config = DEFAULT_CONFIG,
    street_walks: StreetWalks = False,
    out: Annotated[
        Path | None,
        Option(help="Output Parquet (default: data/raptor/paths-<date>.parquet)"),
    ] = None,
    zstd_level: ZstdLevel = "fast",
) -> None:
    """Split a date's OD rows across their journeys, and write the paths taken."""
    out = out or DEFAULT_OUT_DIR / f"paths-{date}.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    summary = assign_date(
        Version.open(feed_for(date)),
        date,
        od_parquet(),
        DEFAULT_STATIONS,
        DEFAULT_PLATFORMS,
        config,
        out,
        parse_zstd_level(zstd_level),
        streets_to_walk(street_walks),
    )
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
    config: Config = DEFAULT_CONFIG,
    street_walks: StreetWalks = False,
    out_dir: Annotated[
        Path, Option(help="Where the path Parquets and manifest.csv go")
    ] = DEFAULT_OUT_DIR,
    zstd_level: ZstdLevel = "fast",
) -> None:
    """`assign` each (month, weekday) in a date range on a representative date,
    with the latest feed version covering it,
    and write a manifest of the dates run and how many days each stands for.
    Dates whose timetables route alike share one routing.

    \b
    Examples:
        mta-od-data raptor assign-range --from 2025-08-11 --to 2025-12-31
    """
    route_range(
        start,
        end,
        gtfs_feeds(),
        od_parquet(),
        DEFAULT_STATIONS,
        DEFAULT_PLATFORMS,
        config,
        parse_zstd_level(zstd_level),
        streets_to_walk(street_walks),
        out_dir,
    )
