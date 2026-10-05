"""Riders on a stretch of track, from `raptor assign-range`'s path Parquets.

A path counts if any of its rides passes between two consecutive stops
both on the stretch, whatever its origin and destination:
`raptor` paths list every stop a ride passes (`raptor/raptor_design.md`).
Each path is counted once, however many of the stretch's segments it rides.
"""

from csv import DictReader
from pathlib import Path
from typing import Annotated

from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import connection

app = Typer()

DEFAULT_MANIFEST = DATA / "raptor" / "manifest.csv"

# Riders on paths with a ride between consecutive stops both in `$stops`.
# A ride is `<route> <stop>><stop>>...`; walks (`walk <from>><to>`) don't count.
# Whether a path rides the stretch depends only on the path,
# so it's decided once per distinct path.
RIDERS_QUERY = """
    WITH rides AS (
        SELECT path, string_split(split_part(leg, ' ', 2), '>') AS stops
        FROM (
            SELECT path, unnest(string_split(path, ' | ')) AS leg
            FROM (SELECT DISTINCT path FROM read_parquet($paths))
        )
        WHERE NOT starts_with(leg, 'walk ')
    ),
    on_stretch AS (
        SELECT DISTINCT path
        FROM rides
        WHERE len(list_filter(
            range(1, len(stops)),
            i -> list_contains($stops, stops[i]) AND list_contains($stops, stops[i + 1])
        )) > 0
    )
    SELECT coalesce(sum(riders), 0)
    FROM read_parquet($paths)
    WHERE path IN (SELECT path FROM on_stretch)
"""


def riders_on_stretch(paths: Path, stops: list[str]) -> float:
    """Riders in one path Parquet with a ride between consecutive `stops`."""
    result: tuple[float] | None = (
        connection()
        .execute(RIDERS_QUERY, {"paths": str(paths), "stops": stops})
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
        Path, Option(help="`raptor assign-range`'s manifest")
    ] = DEFAULT_MANIFEST,
) -> None:
    """Average weekday riders on a stretch of track, over `raptor assign-range`'s dates.

    Each date stands for its `days` (the month's dates in the range on its weekday),
    so the average weights it by them.
    """
    total_riders = 0.0
    total_days = 0
    by_month: dict[str, tuple[float, int]] = {}
    print("| date | weekday | days | riders on the stretch |")
    print("| --- | --- | ---: | ---: |")
    with manifest.open() as f:
        for row in DictReader(f):
            # Written relative to `raptor/`, so found beside the manifest instead.
            paths = manifest.parent / Path(row["paths"]).name
            riders = riders_on_stretch(paths, stop)
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
