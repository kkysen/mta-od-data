"""`compute`'s rows, cached on disk, so a report whose wording or names change
is laid out again in seconds, not recomputed in half a minute.

A cache is read back only if nothing its rows could depend on has changed,
which is found rather than listed, since a missed input is a stale report
the snapshot tests would pass:
- the source of `compute.py` and every module of the package it imports,
  transitively (`modules`): not the rest of `analyze/`, say,
  nor `ridership/__init__.py`, which only names and lays out rows;
- every data file in the package (like `platforms.csv`)
  but its `.md` reports and `RENDER_ONLY`'s;
- `uv.lock`, for DuckDB's version and the rest, and Python's version;
- every file under `data/`, the argument paths, and every file beside the manifest
  (size and modification time);
- `compute`'s arguments.
So it can miss more than it has to (a change to `platform_areas.csv`, say),
but never serves rows from other inputs.
"""

import ast
import os
import pickle
import sys
from hashlib import sha256
from pathlib import Path

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import CACHE
from mta_od_data.ridership.compute import By, Computed, compute

# Each report's rows, by `key`.
ROWS = CACHE / "ridership"
PACKAGE = Path(__file__).parent.parent
HERE = Path(__file__).parent
# Read only to lay out rows, by `__init__.py`.
RENDER_ONLY = frozenset({HERE / "__init__.py", HERE / "direction_labels.json5"})
# What computes the rows, and what's imported from it is followed from.
COMPUTE = "mta_od_data.ridership.compute"


def files(root: Path) -> list[Path]:
    """Every file under `root`, in a set order, but the cache's own."""
    found: list[Path] = []
    for parent, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        found += (Path(parent) / n for n in sorted(names))
    return [f for f in found if ROWS not in f.parents]


def module_file(name: str) -> Path | None:
    """A module of the package's source, or `None` if it's not one."""
    if name.split(".")[0] != PACKAGE.name:
        return None
    path = PACKAGE.parent.joinpath(*name.split("."))
    for file in (path.with_suffix(".py"), path / "__init__.py"):
        if file.exists():
            return file
    return None


def modules(root: str) -> list[Path]:
    """The source of `root` and of every module of the package it imports,
    transitively, with their packages' `__init__.py`s,
    whose own imports aren't followed: they're for the CLI, not what's imported.
    An import of a module with no source to hash, like the Rust extension's,
    is an error rather than left out."""
    found: dict[str, Path] = {}
    todo = [root]
    while todo:
        name = todo.pop()
        if name in found or name.split(".")[0] != PACKAGE.name:
            continue
        file = module_file(name)
        if file is None:
            raise ValueError(f"{name} has no source to key `ridership`'s cache on")
        found[name] = file
        parts = name.split(".")
        for i in range(1, len(parts)):
            parent = ".".join(parts[:i])
            found.setdefault(parent, PACKAGE.parent.joinpath(*parts[:i], "__init__.py"))
        package = name if file.name == "__init__.py" else name.rpartition(".")[0]
        for node in ast.walk(ast.parse(file.read_text(), str(file))):
            if isinstance(node, ast.Import):
                todo += (a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    up = package.rsplit(".", node.level - 1)[0]
                    base = f"{up}.{base}" if base else up
                todo.append(base)
                # `from package import module`, not just a name in it.
                todo += (
                    f"{base}.{a.name}"
                    for a in node.names
                    if module_file(f"{base}.{a.name}") is not None
                )
    return sorted(found.values())


def stat(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path), st.st_size, st.st_mtime_ns)


def key(args: tuple[object, ...], paths: list[Path]) -> str:
    """What `compute`'s rows for `args` could depend on, hashed."""
    h = sha256()
    h.update(sys.version.encode())
    h.update((ROOT / "uv.lock").read_bytes())
    code = [f for f in modules(COMPUTE) if f not in RENDER_ONLY]
    data = [
        f
        for f in files(PACKAGE)
        if f.suffix not in {".py", ".md", ".pyi", ".so"} and f not in RENDER_ONLY
    ]
    for f in [*code, *data]:
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
    file = ROWS / f"{key(args, paths)}.pickle"
    if file.exists():
        with file.open("rb") as f:
            return pickle.load(f)
    rows = compute(*args)
    ROWS.mkdir(parents=True, exist_ok=True)
    # To a temporary name, then renamed: an interrupted write leaves no cache behind.
    tmp = file.with_suffix(f".{os.getpid()}.tmp")
    with tmp.open("wb") as f:
        pickle.dump(rows, f)
    tmp.replace(file)
    return rows
