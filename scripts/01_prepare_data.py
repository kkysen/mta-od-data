#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = ["duckdb"]
# ///
"""Fetch station reference data and convert MTA OD CSV extract(s) to Parquet.

Re-runnable as new monthly/yearly OD extracts are released: point --csv at
the new file(s) (globs are fine) and/or --out at a new Parquet path.

Examples:
    uv run scripts/01_prepare_data.py
    uv run scripts/01_prepare_data.py \
        --csv 'MTA_Subway_Origin-Destination_Ridership_Estimate__2025_*.csv' \
        --out data/mta_od_2025.parquet
    uv run scripts/01_prepare_data.py --force-stations
"""

import argparse
import urllib.request
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

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
    result = con.execute(
        f"""
        SELECT count(*), min(Year * 100 + Month), max(Year * 100 + Month)
        FROM '{out}'
        """
    ).fetchone()
    assert result is not None, "aggregate query always returns exactly one row"
    row_count, min_ym, max_ym = result
    print(f"wrote {out}: {row_count:,} rows, year*100+month range {min_ym}-{max_ym}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--csv",
        nargs="+",
        default=[DEFAULT_CSV_GLOB],
        help=(
            "Source OD CSV path(s)/glob(s), relative to the project root "
            "(default: %(default)s)"
        ),
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_PARQUET, help="Output Parquet path"
    )
    parser.add_argument(
        "--force", action="store_true", help="Reconvert even if --out already exists"
    )
    parser.add_argument(
        "--stations-out",
        type=Path,
        default=DEFAULT_STATIONS_CSV,
        help="Output path for complex-level station reference CSV",
    )
    parser.add_argument(
        "--stations-individual-out",
        type=Path,
        default=DEFAULT_STATIONS_INDIVIDUAL_CSV,
        help="Output path for individual (per-physical-station) reference CSV",
    )
    parser.add_argument(
        "--force-stations",
        action="store_true",
        help="Refetch station reference data even if it exists",
    )
    args = parser.parse_args()

    DATA.mkdir(exist_ok=True)
    fetch_csv(STATIONS_URL, args.stations_out, args.force_stations)
    fetch_csv(
        STATIONS_INDIVIDUAL_URL, args.stations_individual_out, args.force_stations
    )
    convert_od_to_parquet(args.csv, args.out, args.force)


if __name__ == "__main__":
    main()
