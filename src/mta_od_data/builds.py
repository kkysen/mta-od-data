"""What the reports read, built when they need it, through the cache (`artifacts`),
so no command has to be run first, and none reads a stale earlier one's output.

- Downloads, and the OD Parquet, are fetched or built when missing, and kept in `data/`
  (`downloads`, `platforms.fetch_extract`, `scale_od.fetch_spreadsheet`).
- What's derived from them is keyed on everything it's built from:
  the streets cut for walking (`streets`), `scale-od`'s factors (`od_factors`),
  and a routing run (`routed`).

A routing run is keyed on its code and everything it reads:
`routing.py` and the package modules it imports,
all of the `raptor` crate and the crates it depends on by path
but their tests, docs, and builds (`crate_sources`),
`pyproject.toml`, for how `maturin` builds it,
and the built extension itself (`extension_file`),
as a stale build, or one built differently, routes differently from the same sources,
the stations, the platform CSVs, the GTFS feed versions,
and with `street_walks`, the streets and each entrance's time, all by content,
the OD Parquet by size and modification time, too big to hash on each run,
and its dates and flags.
"""

import tomllib
from datetime import date
from importlib.util import find_spec
from pathlib import Path

from typer import BadParameter

from mta_od_data.access import EDGES
from mta_od_data.access import TABLE as DEFAULT_ACCESS
from mta_od_data.artifacts import CACHE, REPO, cached, files, key, modules
from mta_od_data.downloads import gtfs_feeds, od_parquet
from mta_od_data.platforms import DEFAULT_EXTRACT, fetch_extract
from mta_od_data.platforms import DEFAULT_OUT as DEFAULT_PLATFORMS
from mta_od_data.raptor import DEFAULT_CONFIG, DEFAULT_STATIONS, ZSTD_LEVELS
from mta_od_data.routing import route_range
from mta_od_data.scale_od import MAPPING, fetch_spreadsheet, fit_factors
from mta_od_data.street_walks import filter_streets, station_bounds

# The dates the reports route, as `assign-range` picks a weekday of each month in them.
REPORT_FROM = date(2025, 8, 11)
REPORT_TO = date(2025, 12, 31)
EXTENSION = "mta_od_data._raptor"


def report_dates(month: str | None) -> tuple[date, date]:
    """The dates a report routes: `month`'s (`YYYY-MM`), or else all the reports',
    for the snapshot tests to check one month on each commit, a fifth of the routing."""
    if month is None:
        return REPORT_FROM, REPORT_TO
    try:
        first = date.fromisoformat(f"{month}-01")
    except ValueError:
        raise BadParameter(
            f"{month!r} isn't a YYYY-MM month", param_hint="--month"
        ) from None
    after = date(first.year + first.month // 12, first.month % 12 + 1, 1)
    return first, date.fromordinal(after.toordinal() - 1)


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


def extension_file() -> Path:
    """The `raptor` extension this process loads, built from `crate_sources`."""
    spec = find_spec(EXTENSION)
    assert spec is not None and spec.origin is not None, f"{EXTENSION} isn't built"
    return Path(spec.origin)


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
        extension_file(),
        stations,
        # And the platforms `raptor` reads beside it.
        *sorted(platforms.parent.glob("*.csv")),
        config,
        *files(gtfs_dir),
        *(walks or ()),
        # And the stops' platform edges `raptor` reads beside the entrances.
        *([access.with_name(EDGES.name)] if walks else []),
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
