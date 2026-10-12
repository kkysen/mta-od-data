"""Each path's riders in one date of `mta-od-data raptor assign-range`'s paths,
as routed or as if the OD data had been scaled.

Riders choose among journeys by the timetable and cost weights alone,
not by how many others ride (there's no crowding),
so routing scaled OD data would split each OD row's riders the same way.
Each path's riders are then its OD row's scaled riders over the routed ones
times its routed riders, and a scaled run needn't be routed at all.
"""

from collections.abc import Iterable
from csv import DictReader
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated

from typer import Option

from mta_od_data.analyze.common import connection


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


def read_manifest(manifest: Path) -> list[dict[str, str]]:
    with manifest.open() as f:
        return list(DictReader(f))


def od_scale(
    scaled: Path | None, routed: Path, rows: Iterable[dict[str, str]]
) -> OdScale | None:
    """The scale from `routed` to `scaled`, if any,
    for the manifest `rows`' dates."""
    if scaled is None:
        return None
    return load_factors(routed, scaled, (date.fromisoformat(r["date"]) for r in rows))


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

# A service day's hours 24 to 27 are the next date's 0 to 3, from its own OD slice.
_SCALED = """
    SELECT p.path_id, p.riders * coalesce(f.f, 0) AS riders
    FROM (
        SELECT
            path_id, riders, origin, destination,
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


def paths_query(scale: OdScale | None) -> str:
    """A query of `path_id` and `riders`, with `paths_params`' parameters."""
    if scale is None:
        return "SELECT path_id, riders FROM read_parquet($paths)"
    return _SCALED


def paths_params(d: DatePaths, scale: OdScale | None) -> dict[str, object]:
    params: dict[str, object] = {"paths": str(d.paths)}
    if scale is not None:
        params |= {
            "slice": scale.slices[slice_of(d.day)],
            "next_slice": scale.slices[slice_of(d.day + timedelta(days=1))],
        }
    return params
