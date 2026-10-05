"""Scale the OD data's weekdays to another year's station entries.

The OD data starts in 2023, but the MTA's annual station ridership spreadsheet
has each station complex's average weekday entries back to 2019,
from the turnstile counts.
Scaling an OD slice by iterative proportional fitting (Fratar)
so each complex's trips from and to it match that year's entries
keeps the slice's pattern of who goes where,
while restoring each station's volume.
A station's daily exits are taken to equal its entries,
the turnstile exit counts being incomplete (exits through emergency gates).
"""

import csv
from collections import defaultdict
from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve

from openpyxl import load_workbook
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import connection
from mta_od_data.prepare import DEFAULT_PARQUET, RIDERSHIP_DECIMAL

app = Typer()

# "2024 Subway ridership data", from
# https://www.mta.info/agency/new-york-city-transit/subway-bus-ridership-2024:
# average weekday, weekend, and annual entries per station complex, 2019 to 2024.
SPREADSHEET_URL = "https://www.mta.info/document/175471"
DEFAULT_SPREADSHEET = DATA / "mta_subway_ridership_2019_2024.xlsx"
# The spreadsheet's station names, matched to complex IDs by hand.
# The spreadsheet's Times Sq row also counts 42 St-Bryant Pk/5 Av,
# a separate complex here, so that row maps to both.
MAPPING = Path(__file__).parent / "station_ridership_complexes.csv"
# Iterating until every complex's trips from and to it are within this of its target,
# or for at most so many iterations, when a slice can't fit exactly.
TOLERANCE = 1e-6
MAX_ITERATIONS = 30


def average_weekday_entries(spreadsheet: Path, year: int) -> dict[str, float]:
    """Each station row's average weekday entries in `year`, by its name."""
    workbook = load_workbook(spreadsheet, read_only=True)
    rows = list(workbook["Avg Weekday"].iter_rows(values_only=True))
    header = rows[1]
    column = header.index(year)
    entries: dict[str, float] = {}
    for row in rows[2:]:
        name, borough, value = row[0], row[2], row[column]
        # Borough subtotals and the systemwide total have no borough.
        if isinstance(name, str) and borough and isinstance(value, int | float):
            entries[name] = float(value)
    return entries


def complex_targets(
    entries: dict[str, float], complex_weights: dict[int, float]
) -> dict[int, float]:
    """Each complex's entries: a station row's, split across its complexes by weight."""
    complexes_of: dict[str, list[int]] = defaultdict(list)
    with MAPPING.open() as f:
        for row in csv.DictReader(f):
            complexes_of[row["station"]].append(int(row["complex_id"]))
    if missing := sorted(set(entries) - set(complexes_of)):
        raise ValueError(f"{MAPPING}: no complex for {missing}")
    targets: dict[int, float] = {}
    for station, value in entries.items():
        complexes = complexes_of[station]
        weight = sum(complex_weights.get(c, 0.0) for c in complexes)
        for c in complexes:
            share = (
                complex_weights.get(c, 0.0) / weight if weight else 1 / len(complexes)
            )
            targets[c] = value * share
    return targets


@app.command()
def scale_od(
    year: Annotated[int, Option(help="The year whose station entries to scale to")],
    out: Annotated[Path, Option(help="Output Parquet, in the OD Parquet's schema")],
    od: Annotated[Path, Option(help="The OD Parquet")] = DEFAULT_PARQUET,
    od_year: Annotated[int, Option(help="The OD data's year to scale")] = 2025,
    spreadsheet: Annotated[
        Path, Option(help="The MTA station ridership spreadsheet (fetched if missing)")
    ] = DEFAULT_SPREADSHEET,
) -> None:
    """Scale `--od-year`'s weekday OD slices to `--year`'s station entries.

    Each complex grows by its `--year` entries over its `--od-year` average,
    applied to each (month, weekday) slice's own trips from and to it,
    so an average over slices is the target year's average weekday,
    while a slice's own closures and seasonality stay.

    \b
    Examples:
        mta-od-data scale-od --year 2019 --out data/mta_od_scaled_to_2019.parquet
    """
    if not spreadsheet.exists():
        print(f"fetching {SPREADSHEET_URL}")
        urlretrieve(SPREADSHEET_URL, spreadsheet)
    con = connection()
    con.execute(
        """
        CREATE OR REPLACE TEMP TABLE daily AS
        SELECT Month AS month, "Day of Week" AS dow,
               "Origin Station Complex ID" AS o, "Destination Station Complex ID" AS d,
               sum("Estimated Average Ridership")::DOUBLE AS v
        FROM read_parquet($od)
        WHERE Year = $od_year AND "Day of Week" NOT IN ('Saturday', 'Sunday')
        GROUP BY ALL
        """,
        {"od": str(od), "od_year": od_year},
    )
    # Each complex's average entries a slice, like the targets' a day.
    weights = dict(
        con.execute(
            """
            SELECT o, sum(v) / (SELECT count(DISTINCT (month, dow)) FROM daily)
            FROM daily GROUP BY o
            """
        ).fetchall()
    )
    targets = complex_targets(average_weekday_entries(spreadsheet, year), weights)
    # The subway spreadsheet has no Staten Island Railway,
    # but the OD data has its two fare-controlled stations, St George and Tompkinsville:
    # those scale by the systemwide ratio.
    if missing := sorted(set(weights) - set(targets)):
        ratio = sum(targets[c] for c in weights if c in targets) / sum(
            w for c, w in weights.items() if c in targets
        )
        print(
            f"no {year} entries for complexes {missing}: "
            f"scaling by the systemwide {ratio:.3f}"
        )
        for c in missing:
            targets[c] = weights[c] * ratio
    # Each complex's growth: the target year's entries over the OD year's average.
    con.execute("CREATE OR REPLACE TEMP TABLE growth (c BIGINT, g DOUBLE)")
    con.executemany(
        "INSERT INTO growth VALUES (?, ?)",
        [(c, t / weights[c]) for c, t in targets.items()],
    )
    # Each slice's trips from and to a complex, grown:
    # so a complex closed or busier in one slice stays so, scaled.
    # Trips to are normalized to the same total as trips from, for a feasible fit.
    con.execute(
        """
        CREATE OR REPLACE TEMP TABLE row_target AS
        SELECT month, dow, o AS c, sum(v) * g AS t
        FROM daily JOIN growth ON growth.c = o GROUP BY month, dow, o, g;
        CREATE OR REPLACE TEMP TABLE col_target AS
        WITH raw AS (
            SELECT month, dow, d AS c, sum(v) * g AS t
            FROM daily JOIN growth ON growth.c = d GROUP BY month, dow, d, g
        )
        SELECT month, dow, c,
               t * (
                   SELECT sum(t) FROM row_target r
                   WHERE r.month = raw.month AND r.dow = raw.dow
               ) / sum(t) OVER (PARTITION BY month, dow) AS t
        FROM raw;
        """
    )

    # Row factors `a` and column factors `b` per slice, alternately fitted.
    con.execute(
        """
        CREATE OR REPLACE TEMP TABLE a AS
        SELECT DISTINCT month, dow, o, 1.0::DOUBLE AS f FROM daily;
        CREATE OR REPLACE TEMP TABLE b AS
        SELECT DISTINCT month, dow, d, 1.0::DOUBLE AS f FROM daily;
        """
    )
    # Columns fit exactly after `b`; how far rows are off, and by how many riders.
    row_errors = """
        SELECT s.month, s.dow, s.o, s.s, t.t, abs(s.s / t.t - 1) AS error
        FROM (
            SELECT month, dow, o, sum(v * a.f * b.f) AS s
            FROM daily JOIN a USING (month, dow, o) JOIN b USING (month, dow, d)
            GROUP BY ALL
        ) s JOIN row_target t ON t.month = s.month AND t.dow = s.dow AND t.c = s.o
    """
    iterations = 0
    while iterations < MAX_ITERATIONS:
        iterations += 1
        con.execute(
            """
            CREATE OR REPLACE TEMP TABLE a AS
            SELECT month, dow, o, t.t / sum(v * b.f) AS f
            FROM daily JOIN b USING (month, dow, d)
            JOIN row_target t ON t.month = daily.month AND t.dow = daily.dow AND t.c = o
            GROUP BY month, dow, o, t.t;
            CREATE OR REPLACE TEMP TABLE b AS
            SELECT month, dow, d, t.t / sum(v * a.f) AS f
            FROM daily JOIN a USING (month, dow, o)
            JOIN col_target t ON t.month = daily.month AND t.dow = daily.dow AND t.c = d
            GROUP BY month, dow, d, t.t;
            """
        )
        result: tuple[float] | None = con.execute(
            f"SELECT max(error) FROM ({row_errors})"
        ).fetchone()
        assert result is not None, "aggregate query always returns one row"
        if result[0] < TOLERANCE:
            break
    # Not always exact: a complex all but cut off in a slice
    # (e.g. by a service suspension) can't always reach its target through what's left.
    summary: tuple[float, float] | None = con.execute(
        f"SELECT sum(abs(s - t)) / sum(t), max(error) FROM ({row_errors})"
    ).fetchone()
    assert summary is not None, "aggregate query always returns one row"
    print(
        f"after {iterations} iterations: trips from complexes off target by "
        f"{summary[0]:.2e} of all trips, at most {summary[1]:.2e} of one complex's"
    )
    if summary[1] >= TOLERANCE:
        worst = con.execute(
            f"SELECT * FROM ({row_errors}) ORDER BY error DESC LIMIT 5"
        ).fetchall()
        print(f"worst (month, day, complex, trips from, target, error): {worst}")

    con.execute(
        f"""
        COPY (
            SELECT p.Year, p.Month, p."Day of Week", p."Hour of Day",
                   p."Origin Station Complex ID", p."Destination Station Complex ID",
                   (p."Estimated Average Ridership" * a.f * b.f)::{RIDERSHIP_DECIMAL}
                       AS "Estimated Average Ridership"
            FROM read_parquet($od) p
            JOIN a ON a.month = p.Month AND a.dow = p."Day of Week"
                  AND a.o = p."Origin Station Complex ID"
            JOIN b ON b.month = p.Month AND b.dow = p."Day of Week"
                  AND b.d = p."Destination Station Complex ID"
            WHERE p.Year = $od_year
            ORDER BY "Origin Station Complex ID", "Destination Station Complex ID",
                     "Day of Week", "Hour of Day"
        ) TO $out (FORMAT parquet, COMPRESSION zstd, PARQUET_VERSION v2)
        """,
        {"od": str(od), "od_year": od_year, "out": str(out)},
    )
    total: tuple[float] | None = con.execute(
        """
        SELECT avg(s) FROM (
            SELECT Month, "Day of Week", sum("Estimated Average Ridership") s
            FROM read_parquet($out) GROUP BY ALL
        )
        """,
        {"out": str(out)},
    ).fetchone()
    assert total is not None, "aggregate query always returns one row"
    print(
        f"wrote {out}: {total[0]:,.0f} riders a weekday slice "
        f"(targets sum to {sum(targets.values()):,.0f})"
    )
