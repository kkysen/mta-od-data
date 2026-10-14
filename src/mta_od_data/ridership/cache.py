"""`compute`'s rows, cached on disk, so a report whose wording or names change
is laid out again in seconds, not recomputed in half a minute.

A cache is read back only if nothing its rows could depend on has changed,
which is kept broad rather than listed, since a missed input is a stale report
the snapshot tests would pass:
- every file in the package (its code and data files, like `platforms.csv`)
  but its `.md` reports and `RENDER_ONLY`'s, which only name and lay out rows,
  and `uv.lock`, for DuckDB's version and the rest, and Python's version;
- every file under `data/`, the argument paths, and every file beside the manifest
  (size and modification time);
- `compute`'s arguments.
So it misses more than it has to (a change to an `analyze` report's code, say),
but never serves rows from other inputs.
"""

import os
import pickle
import sys
from hashlib import sha256
from pathlib import Path

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import SCRATCH
from mta_od_data.ridership.compute import By, Computed, compute

CACHE = SCRATCH / "ridership"
PACKAGE = Path(__file__).parent.parent
HERE = Path(__file__).parent
# Read only to lay out rows, by `__init__.py`.
RENDER_ONLY = frozenset({HERE / "__init__.py", HERE / "direction_labels.json5"})


def files(root: Path) -> list[Path]:
    """Every file under `root`, in a set order, but the cache's own."""
    found: list[Path] = []
    for parent, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        found += (Path(parent) / n for n in sorted(names))
    return [f for f in found if CACHE not in f.parents]


def stat(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path), st.st_size, st.st_mtime_ns)


def key(args: tuple[object, ...], paths: list[Path]) -> str:
    """What `compute`'s rows for `args` could depend on, hashed."""
    h = sha256()
    h.update(sys.version.encode())
    h.update((ROOT / "uv.lock").read_bytes())
    for f in files(PACKAGE):
        if f in RENDER_ONLY or f.suffix == ".md":
            continue
        h.update(str(f.relative_to(PACKAGE)).encode())
        h.update(f.read_bytes())
    for f in [*files(DATA), *paths]:
        h.update(repr(stat(f)).encode())
    h.update(repr(args).encode())
    return h.hexdigest()


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
    paths = [*files(manifest.parent), manifest, *od_factors, lines]
    file = CACHE / f"{key(args, paths)}.pickle"
    if file.exists():
        with file.open("rb") as f:
            return pickle.load(f)
    rows = compute(*args)
    CACHE.mkdir(parents=True, exist_ok=True)
    # To a temporary name, then renamed: an interrupted write leaves no cache behind.
    tmp = file.with_suffix(f".{os.getpid()}.tmp")
    with tmp.open("wb") as f:
        pickle.dump(rows, f)
    tmp.replace(file)
    return rows
