"""Riders on a stretch of track, from `mta-od-data raptor assign-range`'s path Parquets.

A path counts if any of its rides passes between two consecutive stops
both on the stretch, whatever its origin and destination:
`raptor` paths list every stop a ride passes (`raptor/raptor_design.md`).
Each path is counted once, however many of the stretch's segments it rides.
"""

from pathlib import Path
from typing import Annotated

from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import (
    DatePaths,
    OdScale,
    RoutedOd,
    ScaledOd,
    date_paths,
    od_scale,
    paths_params,
    paths_query,
    read_manifest,
)
from mta_od_data.prepare import DEFAULT_PARQUET

app = Typer()

DEFAULT_MANIFEST = DATA / "raptor" / "manifest.csv"

# Riders on paths with a ride between consecutive stops both in `$stops`.
# A ride is `<route> <stop>><stop>>...`; walks (`walk <from>><to>`) don't count.
# Whether a path rides the stretch depends only on the path,
# so it's decided once per distinct path.
# `{paths}` is `paths_query`'s, each path's riders, perhaps scaled.
RIDERS_QUERY = """
    WITH paths AS ({paths}),
    rides AS (
        SELECT path_id, string_split(split_part(leg, ' ', 2), '>') AS stops
        FROM (
            SELECT path_id, unnest(string_split(path, ' | ')) AS leg
            FROM read_parquet($texts)
            WHERE path_id IN (SELECT path_id FROM read_parquet($paths))
        )
        WHERE NOT starts_with(leg, 'walk ')
    ),
    on_stretch AS (
        SELECT DISTINCT path_id
        FROM rides
        WHERE len(list_filter(
            range(1, len(stops)),
            i -> list_contains($stops, stops[i]) AND list_contains($stops, stops[i + 1])
        )) > 0
    )
    SELECT coalesce(sum(riders), 0)
    FROM paths
    WHERE path_id IN (SELECT path_id FROM on_stretch)
"""


def riders_on_stretch(
    d: DatePaths, stops: list[str], scale: OdScale | None = None
) -> float:
    """Riders on one date's paths with a ride between consecutive `stops`."""
    params = paths_params(d, scale) | {"texts": str(d.texts), "stops": stops}
    result: tuple[float] | None = (
        connection()
        .execute(RIDERS_QUERY.format(paths=paths_query(scale)), params)
        .fetchone()
    )
    assert result is not None, "aggregate query always returns one row"
    return float(result[0])


@app.command()
def track_ridership(
    stop: Annotated[
        list[str],
        Option(
            help=(
                "GTFS parent stop ID on the stretch (repeatable), e.g. "
                "--stop R14 --stop B08 --stop Q03 --stop Q04 --stop Q05 "
                "for Second Av Subway Phase 1"
            )
        ),
    ],
    manifest: Annotated[
        Path, Option(help="`mta-od-data raptor assign-range`'s manifest")
    ] = DEFAULT_MANIFEST,
    scaled_od: ScaledOd = None,
    routed_od: RoutedOd = DEFAULT_PARQUET,
) -> None:
    """Average weekday riders on a stretch of track,
    over `mta-od-data raptor assign-range`'s dates.

    Each date stands for its `days` (the month's dates in the range on its weekday),
    so the average weights it by them.
    """
    rows = read_manifest(manifest)
    scale = od_scale(scaled_od, routed_od, rows)
    total_riders = 0.0
    total_days = 0
    by_month: dict[str, tuple[float, int]] = {}
    print("| date | weekday | days | riders on the stretch |")
    print("| --- | --- | ---: | ---: |")
    for row in rows:
        riders = riders_on_stretch(date_paths(manifest, row), stop, scale)
        days = int(row["days"])
        print(f"| {row['date']} | {row['day_of_week']} | {days} | {riders:,.0f} |")
        total_riders += riders * days
        total_days += days
        month = f"{row['year']}-{int(row['month']):02}"
        month_riders, month_days = by_month.get(month, (0.0, 0))
        by_month[month] = (month_riders + riders * days, month_days + days)
    print()
    print("| month | weekdays | average weekday riders |")
    print("| --- | ---: | ---: |")
    for month, (riders, days) in by_month.items():
        print(f"| {month} | {days} | {riders / days:,.0f} |")
    print()
    print(
        f"average weekday riders over {total_days} weekdays: "
        f"{total_riders / total_days:,.0f}"
    )
