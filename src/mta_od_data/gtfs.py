"""Fetch static GTFS feed versions for RAPTOR (see `raptor/raptor_design.md`)."""

from csv import DictReader
from io import TextIOWrapper
from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve
from zipfile import ZipFile

import json5
from typer import Option, Typer

from mta_od_data import DATA, ROOT

app = Typer()

VERSIONS_FILE = ROOT / "src" / "mta_od_data" / "gtfs_versions.json5"
DEFAULT_GTFS_DIR = DATA / "gtfs"
MOBILITY_DATABASE_FILES = "https://files.mobilitydatabase.org"


def load_versions(path: Path) -> list[str]:
    versions = json5.loads(path.read_text(), allow_duplicate_keys=False)
    if not (isinstance(versions, list) and all(isinstance(v, str) for v in versions)):
        raise ValueError(f"{path}: expected a list of dataset ID strings")
    return versions


def dataset_url(dataset_id: str) -> str:
    # `mdb-516-202510180014` lives under `mdb-516/`.
    feed_id = dataset_id.rsplit("-", 1)[0]
    return f"{MOBILITY_DATABASE_FILES}/{feed_id}/{dataset_id}/{dataset_id}.zip"


def service_range(zip_path: Path) -> tuple[str, str]:
    """The span of `calendar.txt`'s service periods, as `YYYYMMDD`.

    Not `feed_info.txt`, which older versions don't have.
    """
    with ZipFile(zip_path) as z, z.open("calendar.txt") as f:
        rows = list(DictReader(TextIOWrapper(f, encoding="utf-8-sig")))
    return min(r["start_date"] for r in rows), max(r["end_date"] for r in rows)


def fetch_version(dataset_id: str, out_dir: Path, *, force: bool) -> None:
    out = out_dir / f"{dataset_id}.zip"
    if out.exists() and not force:
        print(f"skip: {out} already exists (use --force to refetch)")
    else:
        url = dataset_url(dataset_id)
        print(f"fetching {url}")
        # Downloaded beside `out` and renamed into place,
        # so an interrupted fetch never leaves a truncated zip that looks done.
        part = out.with_suffix(".zip.part")
        urlretrieve(url, part)
        part.replace(out)
    start, end = service_range(out)
    print(f"{out}: service {start} to {end}")


@app.command()
def fetch_gtfs(
    out_dir: Annotated[
        Path, Option(help="Directory to download feed zips into")
    ] = DEFAULT_GTFS_DIR,
    versions_file: Annotated[
        Path, Option(help="JSON5 list of Mobility Database dataset IDs")
    ] = VERSIONS_FILE,
    force: Annotated[bool, Option(help="Refetch zips that already exist")] = False,
) -> None:
    """Download every static GTFS feed version in the versions file.

    \b
    Examples:
        mta-od-data fetch-gtfs
        mta-od-data fetch-gtfs --force
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    for dataset_id in load_versions(versions_file):
        fetch_version(dataset_id, out_dir, force=force)
