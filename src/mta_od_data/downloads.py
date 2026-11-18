"""What the reports read that's downloaded, fetched when missing into `data/`,
where it's kept rather than in the cache: a download needn't be fetched again,
and the MTA's or the Mobility Database's copy can change or go.
Geofabrik's extract and the station ridership spreadsheet are fetched beside
what reads them (`platforms.fetch_extract`, `scale_od.fetch_spreadsheet`).

The OD Parquet is here too: it's converted from a 27 GB CSV by `prepare`
or downloaded from the `od-data` release, and both give the same file.
Apart from `builds`, so that the `analyze` commands reading only it
don't import all that routing does.
"""

import subprocess
from pathlib import Path

from mta_od_data.gtfs import DEFAULT_GTFS_DIR, VERSIONS_FILE, fetch_version
from mta_od_data.gtfs import load_versions as load_version_ids
from mta_od_data.prepare import (
    COMPLEXES_URL,
    DEFAULT_COMPLEXES_CSV,
    DEFAULT_PARQUET,
    DEFAULT_STATIONS_CSV,
    DEFAULT_YEAR,
    STATIONS_URL,
    convert_od_to_parquet,
    fetch_csv,
    od_csv,
)

# The release the OD Parquet is an asset of (see `README.md`).
OD_RELEASE = "od-data"


def od_parquet(path: Path = DEFAULT_PARQUET) -> Path:
    """An OD Parquet, built from the 2025 extract's CSV if it's missing and that one,
    or else downloaded from the release, which has each year's by its name."""
    if path.exists():
        return path
    if path == DEFAULT_PARQUET and od_csv(DEFAULT_YEAR).exists():
        convert_od_to_parquet(od_csv(DEFAULT_YEAR), path, False, None)
        return path
    print(f"downloading {path.name} from the {OD_RELEASE} release")
    part = path.with_name(f"{path.name}.part")
    subprocess.run(
        [
            "gh",
            "release",
            "download",
            OD_RELEASE,
            "--pattern",
            path.name,
            "--output",
            str(part),
            "--clobber",
        ],
        check=True,
    )
    part.replace(path)
    return path


def complexes_csv() -> Path:
    """The complex reference CSV, fetched from data.ny.gov if it's missing."""
    return fetch_reference(COMPLEXES_URL, DEFAULT_COMPLEXES_CSV)


def stations_csv() -> Path:
    """The station reference CSV, fetched from data.ny.gov if it's missing."""
    return fetch_reference(STATIONS_URL, DEFAULT_STATIONS_CSV)


def fetch_reference(url: str, path: Path) -> Path:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        fetch_csv(url, path, force=False)
    return path


def gtfs_feeds(gtfs_dir: Path = DEFAULT_GTFS_DIR) -> Path:
    """`gtfs_dir`, with every feed version in `gtfs_versions.json5` fetched into it."""
    gtfs_dir.mkdir(parents=True, exist_ok=True)
    for dataset_id in load_version_ids(VERSIONS_FILE):
        if not (gtfs_dir / f"{dataset_id}.zip").exists():
            fetch_version(dataset_id, gtfs_dir, force=False)
    return gtfs_dir
