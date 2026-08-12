import urllib.request
from pathlib import Path
from typing import Annotated

import duckdb
from typer import Option, Typer

from mta_od_data import DATA, ROOT

app = Typer()

DEFAULT_CSV_GLOB = "MTA_Subway_Origin-Destination_Ridership_Estimate_*.csv"
DEFAULT_PARQUET = DATA / "mta_od.parquet"
DEFAULT_STATIONS_CSV = DATA / "stations_complexes.csv"
DEFAULT_STATIONS_INDIVIDUAL_CSV = DATA / "stations_individual.csv"
STATIONS_URL = "https://data.ny.gov/resource/5f5g-n3cz.csv?$limit=1000"
# Per-physical-station (not complex-centroid) coordinates; complexes can merge
# multiple physical stations (e.g. Times Sq-42 St/Port Authority Bus Terminal),
# so complex centroids can sit well away from any actual platform. This gives
# the true per-station points for accurate nearest-station distance checks.
STATIONS_INDIVIDUAL_URL = "https://data.ny.gov/resource/39hk-dx4f.csv?$limit=1000"


def fetch_csv(url: str, out: Path, force: bool) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force-stations to refetch)")
        return
    print(f"fetching {url}")
    urllib.request.urlretrieve(url, out)
    n = sum(1 for _ in out.open()) - 1
    print(f"wrote {out} ({n} rows)")


def convert_od_to_parquet(csv_patterns: list[str], out: Path, force: bool) -> None:
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force to reconvert)")
        return
    resolved = [str(ROOT / p) if not Path(p).is_absolute() else p for p in csv_patterns]
    print(f"converting {resolved} -> {out}")
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (SELECT * FROM read_csv_auto({resolved}, union_by_name=true))
        TO '{out}' (FORMAT parquet)
        """
    )
    result: tuple[int, int, int] | None = con.execute(
        f"""
        SELECT count(*), min(Year * 100 + Month), max(Year * 100 + Month)
        FROM '{out}'
        """
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
) -> None:
    """Fetch station reference data and convert MTA OD CSV extract(s) to Parquet.

    Re-runnable as new monthly/yearly OD extracts are released: point --csv at
    the new file(s) (globs are fine) and/or --out at a new Parquet path.

    \b
    Examples:
        mta-od-data prepare
        mta-od-data prepare \\
            --csv 'MTA_Subway_Origin-Destination_Ridership_Estimate__2025_*.csv' \\
            --out data/mta_od_2025.parquet
        mta-od-data prepare --force-stations
    """
    DATA.mkdir(exist_ok=True)
    fetch_csv(STATIONS_URL, stations_out, force_stations)
    fetch_csv(STATIONS_INDIVIDUAL_URL, stations_individual_out, force_stations)
    convert_od_to_parquet(csv if csv else [DEFAULT_CSV_GLOB], out, force)
