from datetime import date
from pathlib import Path

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import (
    Counting,
    DatePaths,
    FareEvasion,
    load_factors,
    paths_params,
    paths_query,
)


def test_scaled_riders_by_each_rows_slice_factors(tmp_path: Path) -> None:
    # (month, day, complex, origin factor, destination factor)
    rows = [
        (9, "Tuesday", 1, 1.5, None),
        (9, "Tuesday", 9, None, 2.0),
        (10, "Wednesday", 1, 0.25, None),
        (10, "Wednesday", 9, None, 2.0),
        # Another month's Tuesday: not this date's.
        (10, "Tuesday", 1, 100.0, None),
        (10, "Tuesday", 9, None, 100.0),
    ]
    values = ", ".join(
        f"({m}, '{dow}', {c}, {o or 'NULL'}, {d or 'NULL'})" for m, dow, c, o, d in rows
    )
    factors = tmp_path / "factors.parquet"
    connection().execute(
        f"""
        COPY (
            SELECT 2019 AS "Scaled To Year", m AS "Month", dow AS "Day of Week",
                c AS "Station Complex ID",
                o::DOUBLE AS "Origin Factor", d::DOUBLE AS "Destination Factor"
            FROM (VALUES {values}) t(m, dow, c, o, d)
        ) TO '{factors}' (FORMAT parquet)
        """
    )
    paths = tmp_path / "paths.parquet"
    connection().execute(
        f"""
        COPY (
            SELECT path_id, h AS hour, o AS origin, 9 AS destination,
                r::DECIMAL(9, 4) AS riders
            FROM (
                VALUES (0, 8, 1, 6.0), (1, 8, 1, 4.0), (2, 25, 1, 4.0), (3, 8, 2, 4.0)
            ) t(path_id, h, o, r)
        ) TO '{paths}' (FORMAT parquet)
        """
    )
    # Tuesday, 2025-09-30: its hours 24 to 27 are Wednesday, October 1's 0 to 3.
    d = DatePaths(date(2025, 9, 30), paths, tmp_path / "texts.parquet")
    c = Counting(scale=load_factors(factors))
    assert c.scale is not None and c.scale.year == 2019
    result = (
        connection()
        .execute(
            f"SELECT path_id, riders FROM ({paths_query(c)}) ORDER BY path_id",
            paths_params(d, c),
        )
        .fetchall()
    )
    # x3 on September Tuesday's, x0.5 on October Wednesday's,
    # and none from a complex with no trips in the slice.
    assert [(i, float(r)) for i, r in result] == [
        (0, 18.0),
        (1, 12.0),
        (2, 2.0),
        (3, 0.0),
    ]


def test_fare_evaders_by_each_hours_quarter(tmp_path: Path) -> None:
    paths = tmp_path / "paths.parquet"
    connection().execute(
        f"""
        COPY (
            SELECT path_id, h AS hour, riders::DECIMAL(9, 4) AS riders
            FROM (VALUES (0, 8, 9.0), (1, 25, 8.0)) t(path_id, h, riders)
        ) TO '{paths}' (FORMAT parquet)
        """
    )
    # Tuesday, 2025-09-30, in Q3; its hours 24 to 27 are October 1's, in Q4.
    d = DatePaths(date(2025, 9, 30), paths, tmp_path / "texts.parquet")
    rates = {(2025, 3): 0.1, (2025, 4): 0.2, (2019, 3): 0.25, (2019, 4): 0.5}
    for year, expected in [(None, [10.0, 10.0]), (2019, [12.0, 16.0])]:
        c = Counting(evasion=FareEvasion(rates=rates, year=year))
        rows = (
            connection()
            .execute(
                f"SELECT riders FROM ({paths_query(c)}) ORDER BY path_id",
                paths_params(d, c),
            )
            .fetchall()
        )
        assert [round(float(r), 9) for (r,) in rows] == expected
