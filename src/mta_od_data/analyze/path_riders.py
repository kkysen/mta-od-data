"""Each path's riders in one date of `mta-od-data raptor assign-range`'s paths,
as routed, as if the OD data had been scaled, or with fare evaders.

Riders choose among journeys by the timetable and cost weights alone,
not by how many others ride (there's no crowding),
so routing scaled OD data would split each OD row's riders the same way.
`mta-od-data scale-od` scales each OD row by its origin's and destination's factors
in its (month, weekday) slice, so each path's riders scale by them too,
and a scaled run needn't be routed at all.
Likewise fare evaders, missing from the OD data (counted from swipes and taps):
each path's riders over 1 less the evasion rate counts them too.
"""

from csv import DictReader
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Annotated

from typer import Option

from mta_od_data import DATA
from mta_od_data.analyze.common import SCRATCH, connection
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


type Slice = tuple[int, str]
"""An OD slice: (month, day of week)."""


def slice_of(d: date) -> Slice:
    return (d.month, f"{d:%A}")


@dataclass(frozen=True, slots=True)
class OdScale:
    """`mta-od-data scale-od`'s factors, as `load_factors` loaded them:
    their file, the year scaled to, and the slices scaled (weekdays only)."""

    path: Path
    year: int
    slices: frozenset[Slice]


OdFactors = Annotated[
    Path | None,
    Option(
        help=(
            "Count riders as if routed with OD data scaled by these factors, "
            "from `mta-od-data scale-od`, "
            "e.g. data/mta_od_scaled_to_2019.factors.parquet"
        )
    ),
]


FareEvasionOption = Annotated[
    bool,
    Option(
        "--fare-evasion",
        help=(
            "Count fare evaders too: riders over 1 less the evasion rate "
            "in each date's quarter, from data.ny.gov, "
            "or with --od-factors, the same quarter's in the year scaled to"
        ),
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


def counting(od_factors: Path | None, fare_evasion: bool) -> Counting:
    """The commands' options' `Counting`."""
    scale = None if od_factors is None else load_factors(od_factors)
    return Counting(
        scale=scale,
        evasion=(
            load_fare_evasion(None if scale is None else scale.year)
            if fare_evasion
            else None
        ),
    )


def read_manifest(manifest: Path) -> list[dict[str, str]]:
    with manifest.open() as f:
        return list(DictReader(f))


# A service day's hours 24 to 27 are the next date's 0 to 3, in its own OD slice,
# and with its own fare evasion.
# A complex with no factor in a slice had no trips from or to it there.
_SCALED = """
    SELECT path_id, riders * coalesce(o.f, 0) * coalesce(d.f, 0) AS riders
    FROM (
        SELECT
            path_id, origin, destination,
            riders * if(hour < 24, $evasion, $next_evasion) AS riders,
            if(hour < 24, $month, $next_month) AS month,
            if(hour < 24, $dow, $next_dow) AS dow
        FROM read_parquet($paths)
    ) p
    LEFT JOIN od_origin_factors o
        ON o.month = p.month AND o.dow = p.dow AND o.c = p.origin
    LEFT JOIN od_destination_factors d
        ON d.month = p.month AND d.dow = p.dow AND d.c = p.destination
"""


def load_factors(path: Path) -> OdScale:
    """Load `mta-od-data scale-od`'s factors, for `_SCALED`."""
    db = connection()
    for side in ["Origin", "Destination"]:
        db.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE od_{side.lower()}_factors AS
            SELECT "Month" AS month, "Day of Week" AS dow,
                "Station Complex ID" AS c, "{side} Factor" AS f
            FROM read_parquet($path) WHERE "{side} Factor" IS NOT NULL
            """,
            {"path": str(path)},
        )
    rows = db.execute(
        """
        SELECT DISTINCT "Scaled To Year", "Month", "Day of Week"
        FROM read_parquet($path)
        """,
        {"path": str(path)},
    ).fetchall()
    years = {y for y, _, _ in rows}
    if len(years) != 1:
        raise ValueError(f"{path}: not scaled to one year: {sorted(years)}")
    return OdScale(
        path=path,
        year=years.pop(),
        slices=frozenset((m, dow) for _, m, dow in rows),
    )


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
        here = slice_of(d.day)
        if here not in scale.slices:
            raise ValueError(f"{d.day}: no OD factors for {here}")
        # Scaling is weekdays only, so a Friday's late night,
        # Saturday's early hours, scales as Friday does.
        after = slice_of(next_day)
        after = after if after in scale.slices else here
        params |= {
            "month": here[0],
            "dow": here[1],
            "next_month": after[0],
            "next_dow": after[1],
        }
    return params


# Bumped by hand whenever `average_path_riders`' output changes for the same inputs,
# so caches written before don't pass for it.
AVERAGE_VERSION = 2


def _stat(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path), st.st_size, st.st_mtime_ns)


def _average_key(manifest: Path, rows: list[DatePaths], c: Counting) -> str:
    """What `average_path_riders`' output depends on, hashed:
    a cache is only ever read back for the same inputs."""
    parts: list[object] = [AVERAGE_VERSION, manifest.read_text()]
    parts += [(_stat(d.paths), _stat(d.texts)) for d in rows]
    if c.scale is not None:
        parts.append(_stat(c.scale.path))
    if c.evasion is not None:
        parts += [sorted(c.evasion.rates.items()), c.evasion.year]
    return sha256(repr(parts).encode()).hexdigest()[:16]


# Riders summed exactly, not as `DOUBLE`s: DuckDB sums in parallel, in no set order,
# so floating-point sums differ in their last bits run to run,
# reordering tied rows of a report and, rarely, rounding a total differently.
# Each term is first rounded to 1e-10 of a rider, far below any reported digit.
EXACT = "DECIMAL(38, 10)"


@dataclass(frozen=True, slots=True)
class AveragePaths:
    """Each path's riders, averaged over a manifest's dates:
    a Parquet of `path` (its text) and `riders` (`EXACT`), and the days it averages."""

    file: Path
    days: int


def average_path_riders(manifest: Path, c: Counting = AS_ROUTED) -> AveragePaths:
    """Each path's average riders over `manifest`'s dates, each weighted by its `days`.

    Every ridership measure is a sum of paths' riders,
    so averaging per path first gives each measure's average,
    with one read of the dates' paths for any number of measures.
    Paths are by text, not id: ids are per routing, and texts say what a path is.

    Cached under `SCRATCH`, keyed by everything it depends on:
    the dates' files are ~25 s to read, and the reports, snapshot tests included,
    read the same average over and over.
    """
    manifest_rows = read_manifest(manifest)
    dates = [date_paths(manifest, row) for row in manifest_rows]
    days = sum(int(row["days"]) for row in manifest_rows)
    out = SCRATCH / f"path-riders-{_average_key(manifest, dates, c)}.parquet"
    if out.exists():
        return AveragePaths(file=out, days=days)

    db = connection()
    db.execute(f"CREATE TYPE IF NOT EXISTS EXACT AS {EXACT}")
    # By id first, per routing's texts: summing a few million integers per date
    # is far cheaper than grouping by text, which then happens once per routing.
    db.execute(
        """
        CREATE OR REPLACE TEMP TABLE by_id
            (texts VARCHAR, path_id UINTEGER, riders EXACT)
        """
    )
    for row, d in zip(manifest_rows, dates, strict=True):
        db.execute(
            f"""
            INSERT INTO by_id
            SELECT $texts, path_id, sum(riders::EXACT) * $days
            FROM ({paths_query(c)})
            GROUP BY path_id
            """,
            paths_params(d, c) | {"texts": str(d.texts), "days": int(row["days"])},
        )
    db.execute("CREATE OR REPLACE TEMP TABLE by_text (path VARCHAR, riders EXACT)")
    for texts in sorted({str(d.texts) for d in dates}):
        db.execute(
            """
            INSERT INTO by_text
            SELECT t.path, sum(b.riders)
            FROM by_id b JOIN read_parquet($texts) t USING (path_id)
            WHERE b.texts = $texts
            GROUP BY t.path
            """,
            {"texts": texts},
        )
    # To a temporary name, then renamed: an interrupted write leaves no cache behind.
    partial = out.with_suffix(".partial")
    db.execute(
        f"""
        COPY (
            SELECT path, (sum(riders) / {days})::EXACT AS riders
            FROM by_text GROUP BY path ORDER BY path
        ) TO '{partial}' (FORMAT parquet, COMPRESSION zstd)
        """
    )
    db.execute("DROP TABLE by_id; DROP TABLE by_text")
    partial.rename(out)
    return AveragePaths(file=out, days=days)
