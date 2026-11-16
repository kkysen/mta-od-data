"""`compute`'s rows, cached on disk (`mta_od_data.artifacts`),
so a report whose wording or names change
is laid out again in seconds, not recomputed in half a minute.

A cache is read back only if nothing its rows could depend on has changed:
- the source of `compute.py` and every module of the package it imports,
  transitively (`modules`): not the rest of `analyze/`, say,
  nor `ridership/__init__.py`, which only names and lays out rows;
- every data file in the package (like `platforms.csv`)
  but its `.md` reports, their `.svg` charts, and `RENDER_ONLY`'s;
- `uv.lock`, for DuckDB's version and the rest, and Python's version;
- what it reads under `data/` (`DATA_INPUTS`), the argument paths,
  and every file beside the manifest (size and modification time);
- `compute`'s arguments.
So it can miss more than it has to (a change to `platform_areas.csv`, say),
but never serves rows from other inputs.
Not every file under `data/`, as that's also where commands write their outputs,
like `one-seat-rides`' `--csv-out`, and rewriting one would miss every entry.
"""

from pathlib import Path

from mta_od_data.analyze.path_riders import DEFAULT_FARE_EVASION
from mta_od_data.artifacts import CACHE, PACKAGE, cached_value, files, modules
from mta_od_data.artifacts import key as artifact_key
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.ridership.compute import By, Computed, compute

# Each report's rows, by `key`.
ROWS = CACHE / "ridership"
HERE = Path(__file__).resolve().parent
# Read only to lay out rows, by `__init__.py`.
RENDER_ONLY = frozenset({HERE / "__init__.py", HERE / "direction_labels.json5"})
# What computes the rows, and what's imported from it is followed from.
COMPUTE = "mta_od_data.ridership.compute"
# What `compute` reads under `data/` besides its argument paths:
# the GTFS feeds the manifest's dates name, and each quarter's fare evasion.
DATA_INPUTS = [DEFAULT_GTFS_DIR, DEFAULT_FARE_EVASION]


def key(args: tuple[object, ...], paths: list[Path]) -> str:
    """What `compute`'s rows for `args` could depend on, hashed."""
    code = [f for f in modules(COMPUTE) if f not in RENDER_ONLY]
    data = [
        f
        for f in files(PACKAGE, skip=[ROWS])
        if f.suffix not in {".py", ".md", ".svg", ".pyi", ".so"}
        and f not in RENDER_ONLY
    ]
    inputs = [f for d in DATA_INPUTS for f in (files(d) if d.is_dir() else [d])]
    return artifact_key([*code, *data], [*inputs, *paths], args)


def cached_compute(
    by: list[By],
    route: list[str],
    manifest: Path,
    od_factors: list[Path],
    unscaled: bool,
    fare_evasion: bool,
    lines: Path,
    top: int,
) -> Computed:
    """`compute`'s rows, from the cache if they're there for the same inputs."""
    args = (by, route, manifest, od_factors, unscaled, fare_evasion, lines, top)
    # The manifest's own directory too, for its dates' files, wherever it is.
    paths = [*files(manifest.parent, skip=[ROWS]), manifest, *od_factors, lines]
    return cached_value(ROWS / f"{key(args, paths)}.pickle", lambda: compute(*args))
