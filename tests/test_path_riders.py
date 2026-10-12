from datetime import date
from pathlib import Path

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import (
    DatePaths,
    load_factors,
    paths_params,
    paths_query,
)


def write_od(path: Path, rows: list[tuple[int, str, int, int, float]]) -> None:
    values = ", ".join(f"({m}, '{dow}', {h}, {o}, {r})" for m, dow, h, o, r in rows)
    connection().execute(
        f"""
        COPY (
            SELECT
                2025 AS "Year", m AS "Month", dow AS "Day of Week", h AS "Hour of Day",
                o AS "Origin Station Complex ID", 9 AS "Destination Station Complex ID",
                r::DECIMAL(9, 4) AS "Estimated Average Ridership"
            FROM (VALUES {values}) t(m, dow, h, o, r)
        ) TO '{path}' (FORMAT parquet)
        """
    )


def test_scaled_riders_from_each_rows_od_slice(tmp_path: Path) -> None:
    # Tuesday, 2025-09-30: its hours 24 to 27 are Wednesday, October 1's 0 to 3.
    routed = tmp_path / "routed.parquet"
    scaled = tmp_path / "scaled.parquet"
    write_od(
        routed,
        [
            (9, "Tuesday", 8, 1, 10.0),
            (10, "Wednesday", 1, 1, 4.0),
            # Another month's Tuesday, the same hour and pair: not this date's.
            (10, "Tuesday", 8, 1, 10.0),
            (9, "Tuesday", 8, 2, 0.0),
        ],
    )
    write_od(
        scaled,
        [
            (9, "Tuesday", 8, 1, 15.0),
            (10, "Wednesday", 1, 1, 2.0),
            (10, "Tuesday", 8, 1, 100.0),
            (9, "Tuesday", 8, 2, 0.0),
        ],
    )
    paths = tmp_path / "paths.parquet"
    connection().execute(
        f"""
        COPY (
            SELECT path_id, h AS hour, o AS origin, 9 AS destination,
                r::DECIMAL(9, 4) AS riders
            FROM (
                VALUES (0, 8, 1, 6.0), (1, 8, 1, 4.0), (2, 25, 1, 4.0), (3, 8, 2, 0.0)
            ) t(path_id, h, o, r)
        ) TO '{paths}' (FORMAT parquet)
        """
    )
    d = DatePaths(date(2025, 9, 30), paths, tmp_path / "texts.parquet")
    scale = load_factors(routed, scaled, [d.day])
    rows = (
        connection()
        .execute(
            f"SELECT path_id, riders FROM ({paths_query(scale)}) ORDER BY path_id",
            paths_params(d, scale),
        )
        .fetchall()
    )
    # x1.5 on September Tuesday's 8:00, x0.5 on October Wednesday's 1:00,
    # and none on a row with no riders to scale.
    assert [(i, float(r)) for i, r in rows] == [(0, 9.0), (1, 6.0), (2, 2.0), (3, 0.0)]
