from pathlib import Path
from typing import Any

import pytest

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import AveragePaths
from mta_od_data.ridership import (
    LINES,
    Column,
    base_route,
    build_events,
    built,
    line_rows,
    load_legs,
    place_rows,
    ride_routes,
    route_groups,
    route_groups_table,
    route_rows,
)


def test_route_groups_split_variants_only_beside_them() -> None:
    routes = ["6", "6X", "5", "1"]
    assert route_groups("6", routes) == ["6", "6L"]
    assert route_groups("6X", routes) == ["6", "6X"]
    # No 5X ran, so no 5L either.
    assert route_groups("5", routes) == ["5"]
    assert route_groups("SI", routes) == []
    assert [base_route(g) for g in ["6L", "6X", "6", "L"]] == ["6", "6", "6", "L"]


@pytest.fixture
def paths(tmp_path: Path) -> list[str]:
    """Paths' average riders, and their legs, as `ridership` reads them."""
    file = tmp_path / "average.parquet"
    rows = [
        # A change between two routes at the same stop.
        ("N R01>R11 | R R11>R13", 1.0),
        # A walk between two stations of a complex.
        ("1 120>127 | walk 127>R16 | W R16>R15", 2.0),
        # Express variant, over a stretch of the line.
        ("6X 621>631", 4.0),
        ("Q Q05>Q04>Q03>B08>R14>R16", 8.0),
    ]
    values = ", ".join(f"('{p}', {r})" for p, r in rows)
    connection().execute(
        f"COPY (SELECT * FROM (VALUES {values}) t(path, riders)) "
        f"TO '{file}' (FORMAT parquet)"
    )
    built.clear()
    names = load_legs([Column("test", AveragePaths(file=file, days=1))])
    connection().execute(
        "CREATE OR REPLACE TEMP TABLE directions AS "
        "SELECT * FROM (VALUES ('N', 'R01', 'R11', 'S', 'S'), "
        "('R', 'R11', 'R13', 'S', 'S')) t(route, a, b, da, db)"
    )
    built["directions"] = "test"
    return names


def by_stop(rows: list[tuple[Any, ...]]) -> dict[tuple[Any, ...], tuple[Any, ...]]:
    return {tuple(r[:-5]): tuple(r[-5:]) for r in rows}


def test_place_counts_boardings_alightings_and_transfers(paths: list[str]) -> None:
    kept, groups = ride_routes([])
    route_groups_table(groups)
    build_events(kept, paths, merge=False)
    got = by_stop(place_rows(False, paths))
    # (riders on + off, on, off, transfers on + off, staying on)
    assert got[("R11", "S")] == (2.0, 1.0, 1.0, 2.0, 0.0)
    assert got[("R01", "S")] == (1.0, 1.0, 0.0, 0.0, 0.0)
    # No direction known for the walk's stations.
    assert got[("127", "")] == (2.0, 0.0, 2.0, 2.0, 0.0)
    assert got[("R16", "")] == (10.0, 2.0, 8.0, 2.0, 0.0)
    # The Q stays on past 72 St and the rest, and only stops there.
    assert got[("Q03", "")] == (0.0, 0.0, 0.0, 0.0, 8.0)


def test_route_filter_merges_same_stop_changes(paths: list[str]) -> None:
    kept, groups = ride_routes(["N", "R", "W"])
    route_groups_table(groups)
    build_events(kept, paths, merge=True)
    got = by_stop(place_rows(False, paths))
    # The N to R change at R11 is one ride: neither off nor on there, but staying on.
    assert got[("R11", "S")] == (0.0, 0.0, 0.0, 0.0, 1.0)
    assert got[("R01", "S")] == (1.0, 1.0, 0.0, 0.0, 0.0)
    # The W after a walk is still a transfer on.
    assert got[("R16", "")] == (2.0, 2.0, 0.0, 2.0, 0.0)


def test_routes_count_each_journey_once_per_row(paths: list[str]) -> None:
    kept, groups = ride_routes([])
    route_groups_table(groups)
    got = dict(route_rows(paths, with_line=False))
    assert got["6"] == 4.0
    assert got["6X"] == 4.0
    assert got["N"] == 1.0
    assert got["W"] == 2.0


def test_lines_count_rides_between_consecutive_stops_on_them(
    paths: list[str],
) -> None:
    kept, groups = ride_routes([])
    route_groups_table(groups)
    LINES.clear()
    LINES["SAS Phase 1"] = ["R14", "B08", "Q03", "Q04", "Q05"]
    assert dict(line_rows(paths)) == {"SAS Phase 1": 8.0}
