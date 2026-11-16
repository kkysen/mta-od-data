"""What the reports read, built when they need it, through the cache (`artifacts`),
so no command has to be run first, and none reads a stale earlier one's output.

- Downloads, and the OD Parquet, are fetched or built when missing, and kept in `data/`:
  the GTFS feed versions (`fetch-gtfs`), Geofabrik's extract,
  the station ridership spreadsheet, and the OD Parquet (`prepare`).
  The OD Parquet is built from the extract's CSV if it's in `data/`,
  or else downloaded from the `od-data` release.
- What's derived from them is keyed on everything it's built from:
  the streets cut for walking (`streets`), `scale-od`'s factors (`od_factors`),
  and a routing run (`routed`).

A routing run is keyed on its code and everything it reads:
`routing.py` and the package modules it imports,
all of the `raptor` crate and the crates it depends on by path
but their tests, docs, and builds (`crate_sources`),
`pyproject.toml`, for how `maturin` builds it,
the stations, the platform CSVs, the GTFS feed versions,
and with `street_walks`, the streets and each entrance's time, all by content,
the OD Parquet by size and modification time, too big to hash on each run,
and its dates and flags.
"""

import subprocess
import tomllib
from datetime import date
from pathlib import Path

from mta_od_data.access import TABLE as DEFAULT_ACCESS
from mta_od_data.artifacts import CACHE, REPO, cached, files, key, modules
from mta_od_data.gtfs import DEFAULT_GTFS_DIR, VERSIONS_FILE, fetch_version
from mta_od_data.gtfs import load_versions as load_version_ids
from mta_od_data.platforms import DEFAULT_EXTRACT
from mta_od_data.platforms import DEFAULT_OUT as DEFAULT_PLATFORMS
from mta_od_data.prepare import DEFAULT_CSV_GLOB, DEFAULT_PARQUET, convert_od_to_parquet
from mta_od_data.raptor import DEFAULT_CONFIG, DEFAULT_STATIONS, ZSTD_LEVELS
from mta_od_data.routing import route_range
from mta_od_data.scale_od import MAPPING, fetch_spreadsheet, fit_factors
from mta_od_data.street_walks import fetch_extract, filter_streets, station_bounds

# The dates the reports route, as `assign-range` picks a weekday of each month in them.
REPORT_FROM = date(2025, 8, 11)
REPORT_TO = date(2025, 12, 31)
# The release the OD Parquet is an asset of (see `README.md`).
OD_RELEASE = "od-data"
EXTENSION = "mta_od_data._raptor"


def od_parquet(path: Path = DEFAULT_PARQUET) -> Path:
    """The OD Parquet, built from the extract's CSV if missing,
    or downloaded if the CSV isn't here either."""
    if path.exists():
        return path
    if any(REPO.glob(DEFAULT_CSV_GLOB)):
        convert_od_to_parquet([DEFAULT_CSV_GLOB], path, False, None)
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


def gtfs_feeds(gtfs_dir: Path = DEFAULT_GTFS_DIR) -> Path:
    """`gtfs_dir`, with every feed version in `gtfs_versions.json5` fetched into it."""
    gtfs_dir.mkdir(parents=True, exist_ok=True)
    for dataset_id in load_version_ids(VERSIONS_FILE):
        if not (gtfs_dir / f"{dataset_id}.zip").exists():
            fetch_version(dataset_id, gtfs_dir, force=False)
    return gtfs_dir


def streets(stations: Path = DEFAULT_STATIONS, extract: Path = DEFAULT_EXTRACT) -> Path:
    """The streets near `stations`, cut from Geofabrik's extract."""
    extract = fetch_extract(extract)
    # The extract by its size and time, as it's 500 MB.
    entry = key(
        [*modules("mta_od_data.street_walks"), stations.resolve()],
        [extract.resolve()],
        (),
    )

    def build(tmp: Path) -> None:
        kept = filter_streets(extract, tmp, station_bounds(stations))
        print(f"cut {kept} ways from {extract}")

    return cached(CACHE / "streets" / f"{entry}.osm.pbf", build)


def od_factors(
    year: int, to_counts: bool, od_year: int = 2025, od: Path | None = None
) -> Path:
    """`scale-od --year year`'s factors, with `--to-counts` if `to_counts`."""
    od = (od or od_parquet()).resolve()
    spreadsheet = fetch_spreadsheet().resolve()
    entry = key(
        [*modules("mta_od_data.scale_od"), MAPPING.resolve(), spreadsheet],
        [od],
        (year, od_year, to_counts),
    )
    return cached(
        CACHE / "od-factors" / f"{entry}.parquet",
        lambda tmp: fit_factors(year, tmp, od, od_year, spreadsheet, to_counts),
    )


def crate_sources(crate: Path = REPO / "raptor") -> list[Path]:
    """What `crate` is built from: its files but its tests, docs, and builds,
    and the same of every crate it depends on by path, with the workspace's."""
    skip = [crate / d for d in ("target", "tests", "examples", "benches")]
    found = [f for f in files(crate, skip) if f.suffix != ".md"]
    manifest = tomllib.loads((crate / "Cargo.toml").read_text())
    for dep in manifest.get("dependencies", {}).values():
        if isinstance(dep, dict) and "path" in dep:
            found += crate_sources((crate / dep["path"]).resolve())
    if crate == REPO / "raptor":
        found += [REPO / "Cargo.toml", REPO / "Cargo.lock", REPO / "pyproject.toml"]
        found += files(REPO / ".cargo")
    return sorted(set(found))


def routed(
    street_walks: bool = False,
    start: date = REPORT_FROM,
    end: date = REPORT_TO,
    zstd_level: str = "fast",
) -> Path:
    """`raptor assign-range --from start --to end`'s manifest,
    with `--street-walks` if `street_walks`,
    routed first if it hasn't been on these inputs."""
    gtfs_dir = gtfs_feeds().resolve()
    od = od_parquet().resolve()
    stations = DEFAULT_STATIONS.resolve()
    platforms = DEFAULT_PLATFORMS.resolve()
    config = DEFAULT_CONFIG.resolve()
    access = DEFAULT_ACCESS.resolve()
    walks = (streets(stations).resolve(), access) if street_walks else None
    contents = [
        *modules("mta_od_data.routing", {EXTENSION: crate_sources()}),
        stations,
        # And the platforms `raptor` reads beside it.
        *sorted(platforms.parent.glob("*.csv")),
        config,
        *files(gtfs_dir),
        *(walks or ()),
    ]
    level = ZSTD_LEVELS[zstd_level]
    entry = key(
        contents, [od], (start.isoformat(), end.isoformat(), street_walks, level)
    )
    run = CACHE / "routing" / entry

    def build(tmp: Path) -> None:
        print(f"routing {start} to {end} into {run}")
        route_range(
            start,
            end,
            gtfs_dir,
            od,
            stations,
            platforms,
            config,
            level,
            walks,
            tmp,
            run,
        )

    return cached(run, build) / "manifest.csv"
