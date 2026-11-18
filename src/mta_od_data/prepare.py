from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve

import duckdb
from typer import Option, Typer

from mta_od_data import DATA

app = Typer()


# The data.ny.gov dataset holding each year's OD extract.
# 2026's is the one "Beginning 2026", which later years are appended to.
OD_DATASETS = {
    2021: "rapa-97zv",
    2022: "nqnz-e9z9",
    2023: "uhf3-t34z",
    2024: "jsu2-fbtj",
    2025: "y2qv-fytt",
    2026: "28vm-gjqr",
}
DEFAULT_YEAR = 2025


def od_csv(year: int) -> Path:
    return DATA / f"mta_od_{year}.csv"


def od_parquet(year: int) -> Path:
    return DATA / f"mta_od_{year}.parquet"


DEFAULT_PARQUET = od_parquet(DEFAULT_YEAR)
DEFAULT_COMPLEXES_CSV = DATA / "complexes.csv"
DEFAULT_STATIONS_CSV = DATA / "stations.csv"
COMPLEXES_URL = "https://data.ny.gov/resource/5f5g-n3cz.csv?$limit=1000"
# Per-station coordinates; see `Station.load_individual`.
STATIONS_URL = "https://data.ny.gov/resource/39hk-dx4f.csv?$limit=1000"

# Every one of these is functionally determined by the complex ID next to it
# (verified over all 121M rows: one distinct value per ID), so they're the
# station reference CSVs repeated once per row: half the file, and `analyze`
# reads none of them, joining the station data by complex ID instead.
DERIVED_COLUMNS = """
    "Origin Station Complex Name", "Origin Latitude",
    "Origin Longitude", "Origin Point",
    "Destination Station Complex Name", "Destination Latitude",
    "Destination Longitude", "Destination Point",
    -- One distinct value per (Year, Month, Day of Week, Hour of Day): the
    -- extract has no real dates, just a label per averaged group, which is
    -- what `DayCoverage` reconstructs from those four columns instead.
    "Timestamp"
"""

# Every ridership value is an exact multiple of 1e-4, so this is lossless,
# and it packs as an integer rather than a `DOUBLE` that never compresses.
RIDERSHIP_DECIMAL = "DECIMAL(9, 4)"


def fetch_csv(url: str, out: Path, *, force: bool) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force-stations to refetch)")
        return
    print(f"fetching {url}")
    urlretrieve(url, out)
    n = sum(1 for _ in out.open()) - 1
    print(f"wrote {out} ({n} rows)")


def fetch_od_csv(year: int) -> Path:
    """The year's OD extract, downloaded to `od_csv(year)` when missing."""
    out = od_csv(year)
    if out.exists():
        return out
    dataset = OD_DATASETS[year]
    url = f"https://data.ny.gov/api/views/{dataset}/rows.csv?accessType=DOWNLOAD"
    print(f"fetching {url} (large: up to ~16GB)")
    # Written beside `out` and renamed, so an interrupted download is never
    # mistaken for the finished file.
    partial = out.with_suffix(".csv.part")
    urlretrieve(url, partial)
    partial.rename(out)
    return out


def convert_od_to_parquet(
    csv: Path,
    out: Path,
    force: bool,
    ridership_decimals: int | None,
) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force to reconvert)")
        return
    print(f"converting {csv} -> {out}")
    # Two constant `SELECT`s chosen by a branch, with the precision bound as a
    # parameter: nothing the caller controls is ever interpolated into the SQL.
    if ridership_decimals is None:
        select = (
            f"* EXCLUDE ({DERIVED_COLUMNS}) "
            f'REPLACE ("Estimated Average Ridership"::{RIDERSHIP_DECIMAL} '
            'AS "Estimated Average Ridership")'
        )
    else:
        if ridership_decimals < 0:
            raise ValueError(
                f"--ridership-decimals must be >= 0, got {ridership_decimals}"
            )
        select = (
            f"* EXCLUDE ({DERIVED_COLUMNS}) "
            'REPLACE (round("Estimated Average Ridership", $decimals)'
            f'::{RIDERSHIP_DECIMAL} AS "Estimated Average Ridership")'
        )
        print(f"rounding ridership to {ridership_decimals} decimals")
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
            SELECT {select}
            FROM read_csv($csv, union_by_name=true, thousands=',')
            -- Sorted so `analyze`'s row-group statistics can skip data
            -- rather than scan the whole file: every analysis so far
            -- scopes to some set of origins, and filters by day of week.
            -- Clustering the OD pair also runs the ID columns into long
            -- constant stretches and puts similar ridership values next to
            -- each other, which is worth ~190M on the 2025 extract.
            ORDER BY "Origin Station Complex ID", "Destination Station Complex ID",
                     "Day of Week", "Hour of Day"
        -- v2 pages, for the delta encoding the ridership column packs into.
        ) TO $out (
            FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL 3,
            PARQUET_VERSION v2
        )
        """,
        {"csv": str(csv), "out": str(out)}
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
    year: Annotated[
        int,
        Option(
            min=min(OD_DATASETS),
            max=max(OD_DATASETS),
            help=(
                "Which year's OD extract to convert, downloaded from data.ny.gov "
                "to `data/mta_od_<year>.csv` when missing"
            ),
        ),
    ] = DEFAULT_YEAR,
    out: Annotated[
        Path | None,
        Option(help="Output Parquet path (default: `data/mta_od_<year>.parquet`)"),
    ] = None,
    force: Annotated[
        bool, Option(help="Reconvert even if --out already exists")
    ] = False,
    complexes_out: Annotated[
        Path,
        Option("--complexes-out", help="Output path for the complex reference CSV"),
    ] = DEFAULT_COMPLEXES_CSV,
    stations_out: Annotated[
        Path,
        Option(
            "--stations-out",
            help="Output path for the per-station (a line's stop) reference CSV",
        ),
    ] = DEFAULT_STATIONS_CSV,
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
    """Fetch station reference data and convert a year's MTA OD CSV to Parquet.

    Downloads the year's extract from data.ny.gov when `data/` lacks it.
    To pick up months released since, delete `data/mta_od_<year>.csv`
    and run again with --force.

    \b
    Examples:
        mta-od-data prepare
        mta-od-data prepare --year 2024
        mta-od-data prepare --force-stations
        mta-od-data prepare --stations-only
        mta-od-data prepare --ridership-decimals 2
    """
    DATA.mkdir(exist_ok=True)
    force_stations = force_stations or stations_only
    fetch_csv(COMPLEXES_URL, complexes_out, force=force_stations)
    fetch_csv(STATIONS_URL, stations_out, force=force_stations)
    if stations_only:
        return
    convert_od_to_parquet(
        fetch_od_csv(year), out or od_parquet(year), force, ridership_decimals
    )
