from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve

import duckdb
from typer import Option, Typer

from mta_od_data import DATA, ROOT

app = Typer()

DEFAULT_CSV_GLOB = "data/MTA_Subway_Origin-Destination_Ridership_Estimate__2025_*.csv"
DEFAULT_PARQUET = DATA / "mta_od.parquet"
DEFAULT_STATIONS_CSV = DATA / "stations_complexes.csv"
DEFAULT_STATIONS_INDIVIDUAL_CSV = DATA / "stations_individual.csv"
STATIONS_URL = "https://data.ny.gov/resource/5f5g-n3cz.csv?$limit=1000"
# Per-platform coordinates; see `Station.load_individual`.
STATIONS_INDIVIDUAL_URL = "https://data.ny.gov/resource/39hk-dx4f.csv?$limit=1000"

# Every one of these is functionally determined by the complex ID next to it
# (verified over all 121M rows: one distinct value per ID), so they're the
# station reference CSVs repeated once per row: half the file, and `analyze`
# reads none of them, joining the station data by complex ID instead.
DERIVED_COLUMNS = """
    "Origin Station Complex Name", "Origin Latitude",
    "Origin Longitude", "Origin Point",
    "Destination Station Complex Name", "Destination Latitude",
    "Destination Longitude", "Destination Point"
"""


def fetch_csv(url: str, out: Path, *, force: bool) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force-stations to refetch)")
        return
    print(f"fetching {url}")
    urlretrieve(url, out)
    n = sum(1 for _ in out.open()) - 1
    print(f"wrote {out} ({n} rows)")


def convert_od_to_parquet(
    csv_patterns: list[str],
    out: Path,
    force: bool,
    ridership_decimals: int | None,
) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force to reconvert)")
        return
    resolved = [str(ROOT / p) if not Path(p).is_absolute() else p for p in csv_patterns]
    print(f"converting {resolved} -> {out}")
    # Two constant `SELECT`s chosen by a branch, with the precision bound as a
    # parameter: nothing the caller controls is ever interpolated into the SQL.
    if ridership_decimals is None:
        select = f"* EXCLUDE ({DERIVED_COLUMNS})"
    else:
        if ridership_decimals < 0:
            raise ValueError(
                f"--ridership-decimals must be >= 0, got {ridership_decimals}"
            )
        select = (
            f"* EXCLUDE ({DERIVED_COLUMNS}) "
            'REPLACE (round("Estimated Average Ridership", $decimals) '
            'AS "Estimated Average Ridership")'
        )
        print(f"rounding ridership to {ridership_decimals} decimals")
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
            SELECT {select}
            FROM read_csv($csv_patterns, union_by_name=true, thousands=',')
            -- Sorted so `analyze`'s row-group statistics can skip data
            -- rather than scan the whole file: every analysis so far
            -- filters by day of week, and scopes to some set of origins.
            -- Never worse than the original date/hour order even for a
            -- query filtering by neither, and it compresses better.
            ORDER BY "Day of Week", "Origin Station Complex ID"
        ) TO $out (FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL 3)
        """,
        {"csv_patterns": resolved, "out": str(out)}
        | ({} if ridership_decimals is None else {"decimals": ridership_decimals}),
    )
    result: tuple[int, int, int] | None = con.execute(
        """
        SELECT count(*), min(Year * 100 + Month), max(Year * 100 + Month)
        FROM read_parquet($out)
        """,
        {"out": str(out)},
    ).fetchone()
    assert result is not None, "aggregate query always returns exactly one row"
    row_count, min_ym, max_ym = result
    print(f"wrote {out}: {row_count:,} rows, year*100+month range {min_ym}-{max_ym}")


@app.command()
def prepare(
    csv: Annotated[
        list[str] | None,
        Option(
            help=(
                "Source OD CSV path(s)/glob(s), relative to the project root "
                f"(repeatable; default: {DEFAULT_CSV_GLOB})"
            ),
        ),
    ] = None,
    out: Annotated[Path, Option(help="Output Parquet path")] = DEFAULT_PARQUET,
    force: Annotated[
        bool, Option(help="Reconvert even if --out already exists")
    ] = False,
    stations_out: Annotated[
        Path,
        Option(help="Output path for complex-level station reference CSV"),
    ] = DEFAULT_STATIONS_CSV,
    stations_individual_out: Annotated[
        Path,
        Option(help="Output path for individual (per-physical-station) reference CSV"),
    ] = DEFAULT_STATIONS_INDIVIDUAL_CSV,
    force_stations: Annotated[
        bool, Option(help="Refetch station reference data even if it exists")
    ] = False,
    ridership_decimals: Annotated[
        int | None,
        Option(
            help=(
                "Round `Estimated Average Ridership` to this many decimals "
                "(default: keep every digit the extract has). The ridership "
                "column is most of the Parquet; 2 decimals is ~35% smaller"
            )
        ),
    ] = None,
    stations_only: Annotated[
        bool,
        Option(
            help=(
                "Refetch only the station reference data, skipping the OD "
                "Parquet conversion (implies --force-stations)"
            )
        ),
    ] = False,
) -> None:
    """Fetch station reference data and convert MTA OD CSV extract(s) to Parquet.

    Re-runnable as new monthly/yearly OD extracts are released: point --csv at
    the new file(s) (globs are fine) and/or --out at a new Parquet path.

    \b
    Examples:
        mta-od-data prepare
        mta-od-data prepare \\
            --csv 'data/MTA_Subway_Origin-Destination_Ridership_Estimate__2024_*.csv' \\
            --out data/mta_od_2024.parquet
        mta-od-data prepare --force-stations
        mta-od-data prepare --stations-only
        mta-od-data prepare --ridership-decimals 2
    """
    DATA.mkdir(exist_ok=True)
    force_stations = force_stations or stations_only
    fetch_csv(STATIONS_URL, stations_out, force=force_stations)
    fetch_csv(STATIONS_INDIVIDUAL_URL, stations_individual_out, force=force_stations)
    if stations_only:
        return
    convert_od_to_parquet(
        csv if csv else [DEFAULT_CSV_GLOB], out, force, ridership_decimals
    )
