"""Derived files, built once and kept on disk under `CACHE`,
each named by a hash of everything it could depend on (its key),
so a command builds what it needs itself, and builds it again only when that changes.

A key hashes what it's built from, found rather than listed where it can be,
since a missed input is a silently stale result, and an extra one only a rebuild:
- Python's version and `uv.lock`, for every package's version;
- code and checked-in data, by content: the source of the module building it
  and of every module of the package it imports, transitively (`modules`),
  and any other files the caller names;
- big files that aren't checked in, like downloads and other builds' outputs,
  by their size and modification time (`stat`), as reading them all would take long;
- its arguments.
Content rather than modification time for whatever git tracks,
since a checkout or a rebase rewrites the time of every file it touches.

An entry is built under a temporary name beside it and renamed into place,
so an interrupted build leaves no entry behind, only its partial build,
which the next build of the same key writes over.
Entries are never deleted: one whose inputs changed is just never read again.
"""

import ast
import os
import pickle
import sys
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from fcntl import LOCK_EX, flock
from hashlib import sha256
from pathlib import Path

# The package's source, and the repository it's in.
PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent.parent
# Every entry, by what builds it, then its key.
CACHE = Path.home() / ".cache" / "mta-od-data"


def files(root: Path, skip: Collection[Path] = ()) -> list[Path]:
    """Every file under `root`, in a set order,
    but those under `skip` and Python's `__pycache__`."""
    found: list[Path] = []
    for parent, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        found += (Path(parent) / n for n in sorted(names))
    return [f for f in found if not any(s in f.parents for s in skip)]


def module_file(name: str) -> Path | None:
    """A module of the package's source, or `None` if it's not one."""
    if name.split(".")[0] != PACKAGE.name:
        return None
    path = PACKAGE.parent.joinpath(*name.split("."))
    for file in (path.with_suffix(".py"), path / "__init__.py"):
        if file.exists():
            return file
    return None


def modules(
    root: str, extensions: Mapping[str, Sequence[Path]] | None = None
) -> list[Path]:
    """The source of `root` and of every module of the package it imports,
    transitively, with their packages' `__init__.py`s,
    whose own imports aren't followed: they're for the CLI, not what's imported.
    An extension module is the source it's built from, in `extensions`;
    an import of one with no source to hash is an error rather than left out."""
    extensions = extensions or {}
    found: dict[str, Path] = {}
    built: set[Path] = set()
    todo = [root]
    while todo:
        name = todo.pop()
        if name in found or name.split(".")[0] != PACKAGE.name:
            continue
        if name in extensions:
            built.update(extensions[name])
            continue
        file = module_file(name)
        if file is None:
            raise ValueError(f"{name} has no source to key a cache on")
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
                    or f"{base}.{a.name}" in extensions
                )
    return sorted({*found.values(), *built})


def stat(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path), st.st_size, st.st_mtime_ns)


def label(path: Path) -> str:
    """A file's name in a key: relative to the package, or else the repository,
    so the key is the same wherever the repository is."""
    for base in (PACKAGE, REPO):
        if path.is_relative_to(base):
            return str(path.relative_to(base))
    return str(path)


def key(contents: Iterable[Path], stats: Iterable[Path], args: object) -> str:
    """What an entry could depend on, hashed:
    `contents` by their names and bytes, `stats` by `stat`, and `args` by `repr`."""
    h = sha256()
    h.update(sys.version.encode())
    h.update((REPO / "uv.lock").read_bytes())
    for f in contents:
        h.update(label(f).encode())
        h.update(f.read_bytes())
    for f in stats:
        h.update(repr(stat(f)).encode())
    h.update(repr(args).encode())
    return h.hexdigest()


def partial(entry: Path) -> Path:
    """Where `entry` is built before it's renamed into place:
    `<key>.partial.osm.pbf` for `<key>.osm.pbf`,
    the extension last, as some writers tell the format by it."""
    head, dot, rest = entry.name.partition(".")
    return entry.with_name(f"{head}.partial{dot}{rest}")


def cached(entry: Path, build: Callable[[Path], None]) -> Path:
    """`entry`, a file or a directory, built first if it isn't there yet:
    `build` writes it to the path it's handed, `partial(entry)`,
    which is then renamed to `entry`.
    One process builds an entry at a time; another waits, then finds it built."""
    if entry.exists():
        return entry
    entry.parent.mkdir(parents=True, exist_ok=True)
    with entry.with_name(f"{entry.name}.lock").open("w") as lock:
        flock(lock, LOCK_EX)
        if not entry.exists():
            tmp = partial(entry)
            build(tmp)
            tmp.rename(entry)
    return entry


def cached_value[T](entry: Path, compute: Callable[[], T]) -> T:
    """`compute()`, pickled to `entry` the first time, read back after."""

    def build(tmp: Path) -> None:
        with tmp.open("wb") as f:
            pickle.dump(compute(), f)

    with cached(entry, build).open("rb") as f:
        return pickle.load(f)
