"""Each path's riders in one date of `mta-od-data raptor assign-range`'s paths,
as routed, as if the OD data had been scaled, or with fare evaders.

Riders choose among journeys by the timetable and cost weights alone,
not by how many others ride (there's no crowding),
so routing scaled OD data would split each OD row's riders the same way.
Each path's riders are then its OD row's scaled riders over the routed ones
times its routed riders, and a scaled run needn't be routed at all.
Likewise fare evaders, missing from the OD data (counted from swipes and taps):
each path's riders over 1 less the evasion rate counts them too.
"""

from collections.abc import Iterable
from csv import DictReader
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated

from typer import Option

from mta_od_data import DATA
from mta_od_data.analyze.common import connection
from mta_od_data.prepare import fetch_csv


@dataclass(frozen=True, slots=True)
class DatePaths:
    """One manifest row's date and the files of its paths."""

    day: date
    paths: Path
    texts: Path


def date_paths(manifest: Path, row: dict[str, str]) -> DatePaths:
    """A manifest row's date and files,
    found beside the manifest, wherever it was written from
    (older manifests' paths are relative to `raptor/`)."""
    return DatePaths(
        day=date.fromisoformat(row["date"]),
        paths=manifest.parent / Path(row["paths"]).name,
        texts=manifest.parent / Path(row["path_texts"]).name,
    )


type Slice = tuple[int, int, str]
"""An OD slice: (year, month, day of week)."""


def slice_of(d: date) -> Slice:
    return (d.year, d.month, f"{d:%A}")


@dataclass(frozen=True, slots=True)
class OdScale:
    """Scaling from the OD data the paths were routed with
    to OD data from `mta-od-data scale-od`, row for row,
    as `load_factors` loaded it: each slice's id in its table."""

    slices: dict[Slice, int]


ScaledOd = Annotated[
    Path | None,
    Option(
        help=(
            "Count riders as if routed with this OD data, "
            "from `mta-od-data scale-od`, e.g. data/mta_od_scaled_to_2019.parquet"
        )
    ),
]
RoutedOd = Annotated[
    Path, Option(help="The OD data the paths were routed with, for --scaled-od")
]


FareEvasionOption = Annotated[
    bool,
    Option(
        "--fare-evasion",
        help=(
            "Count fare evaders too: riders over 1 less the evasion rate "
            "in each date's quarter, from data.ny.gov"
        ),
    ),
]
EvasionYear = Annotated[
    int | None,
    Option(
        help=(
            "With --fare-evasion, the same quarter's rate in this year, "
            "for OD data scaled to it, e.g. 2019"
        )
    ),
]

# "MTA NYCT Subway Fare Evasion: Beginning 2018": quarterly subway evasion rates,
# estimated from traffic checkers' surveys, as on https://metrics.mta.info.
FARE_EVASION_URL = (
    "https://data.ny.gov/api/views/6kj3-ijvb/rows.csv?accessType=DOWNLOAD"
)
DEFAULT_FARE_EVASION = DATA / "fare_evasion.csv"


@dataclass(frozen=True, slots=True)
class FareEvasion:
    """Each (year, quarter)'s evasion rate, and the year to take them from,
    if not each date's own."""

    rates: dict[tuple[int, int], float]
    year: int | None

    def rate(self, d: date) -> float:
        key = (self.year or d.year, (d.month - 1) // 3 + 1)
        if key not in self.rates:
            raise ValueError(f"no fare evasion rate for {key[0]} Q{key[1]}")
        return self.rates[key]


def load_fare_evasion(
    year: int | None, path: Path = DEFAULT_FARE_EVASION
) -> FareEvasion:
    fetch_csv(FARE_EVASION_URL, path, force=False)
    rates: dict[tuple[int, int], float] = {}
    with path.open() as f:
        for row in DictReader(f):
            # "2025-Q3"; a quarter not surveyed (2020-Q2) has no rate.
            y, q = row["Time Period"].split("-Q")
            if row["Fare Evasion"]:
                rates[int(y), int(q)] = float(row["Fare Evasion"])
    return FareEvasion(rates=rates, year=year)


@dataclass(frozen=True, slots=True)
class Counting:
    """How paths' riders are counted: OD data scaled or not, evaders or not."""

    scale: OdScale | None = None
    evasion: FareEvasion | None = None


AS_ROUTED = Counting()


def counting(
    rows: Iterable[dict[str, str]],
    scaled_od: Path | None,
    routed_od: Path,
    fare_evasion: bool,
    evasion_year: int | None,
) -> Counting:
    """The commands' options' `Counting`, for the manifest `rows`' dates."""
    days = [date.fromisoformat(r["date"]) for r in rows]
    return Counting(
        scale=None if scaled_od is None else load_factors(routed_od, scaled_od, days),
        evasion=load_fare_evasion(evasion_year) if fare_evasion else None,
    )


def read_manifest(manifest: Path) -> list[dict[str, str]]:
    with manifest.open() as f:
        return list(DictReader(f))


# Each OD row's scaled riders over its routed ones, in the slices of `$slices`,
# by slice id `s`: each OD file is read once for every date, not once a date.
_FACTORS = """
    CREATE OR REPLACE TEMP TABLE od_factors_unsorted AS
    WITH slices AS (
        SELECT s.y, s.m, s.dow, s.s FROM (SELECT unnest($slices) AS s)
    ),
    routed AS ({routed}),
    scaled AS ({scaled})
    SELECT s, h, origin, destination,
        coalesce(scaled.riders / nullif(routed.riders, 0), 0)::FLOAT AS f
    FROM routed LEFT JOIN scaled USING (s, h, origin, destination)
"""

# An OD file's riders in `slices`, keyed as path rows are.
_OD_SLICE = """
    SELECT
        s, "Hour of Day"::UTINYINT AS h,
        "Origin Station Complex ID"::USMALLINT AS origin,
        "Destination Station Complex ID"::USMALLINT AS destination,
        sum("Estimated Average Ridership") AS riders
    FROM read_parquet({od}) JOIN slices
        ON "Year" = y AND "Month" = m AND "Day of Week" = dow
    GROUP BY ALL
"""

# A service day's hours 24 to 27 are the next date's 0 to 3, from its own OD slice,
# and with its own fare evasion.
_SCALED = """
    SELECT p.path_id, p.riders * coalesce(f.f, 0) AS riders
    FROM (
        SELECT
            path_id, origin, destination,
            riders * if(hour < 24, $evasion, $next_evasion) AS riders,
            if(hour < 24, $slice, $next_slice) AS s,
            hour % 24 AS h
        FROM read_parquet($paths)
    ) p
    LEFT JOIN (
        SELECT * FROM od_factors WHERE s = $slice OR s = $next_slice
    ) f USING (s, h, origin, destination)
"""


def load_factors(routed: Path, scaled: Path, days: Iterable[date]) -> OdScale:
    """Load the factors scaling `routed` to `scaled`, for the service days `days`."""
    slices = {slice_of(d) for day in days for d in (day, day + timedelta(days=1))}
    ids = {sl: i for i, sl in enumerate(sorted(slices))}
    db = connection()
    db.execute(
        _FACTORS.format(
            routed=_OD_SLICE.format(od="$routed"), scaled=_OD_SLICE.format(od="$scaled")
        ),
        {
            "routed": str(routed),
            "scaled": str(scaled),
            "slices": [
                {"y": y, "m": m, "dow": dow, "s": i} for (y, m, dow), i in ids.items()
            ],
        },
    )
    # Slice by slice, so each date reads its two slices' row groups, not all of them:
    # sorting it all at once ran out of memory.
    db.execute(
        "CREATE OR REPLACE TEMP TABLE od_factors AS FROM od_factors_unsorted LIMIT 0"
    )
    for i in ids.values():
        db.execute(
            "INSERT INTO od_factors FROM od_factors_unsorted WHERE s = $s", {"s": i}
        )
    db.execute("DROP TABLE od_factors_unsorted")
    return OdScale(slices=ids)


_UNSCALED = """
    SELECT path_id, riders * if(hour < 24, $evasion, $next_evasion) AS riders
    FROM read_parquet($paths)
"""


def paths_query(c: Counting) -> str:
    """A query of `path_id` and `riders`, with `paths_params`' parameters."""
    return _UNSCALED if c.scale is None else _SCALED


def paths_params(d: DatePaths, c: Counting) -> dict[str, object]:
    next_day = d.day + timedelta(days=1)

    # Riders and evaders, over the paid riders that are 1 less the evasion rate.
    def evasion(day: date) -> float:
        return 1.0 if c.evasion is None else 1 / (1 - c.evasion.rate(day))

    params: dict[str, object] = {
        "paths": str(d.paths),
        "evasion": evasion(d.day),
        "next_evasion": evasion(next_day),
    }
    if (scale := c.scale) is not None:
        params |= {
            "slice": scale.slices[slice_of(d.day)],
            "next_slice": scale.slices[slice_of(next_day)],
        }
    return params
