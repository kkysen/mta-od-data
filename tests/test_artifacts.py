"""`artifacts`' keys change with what an entry is built from, and only with that,
and an entry is there only once it's fully built."""

from pathlib import Path

import pytest

from mta_od_data import artifacts
from mta_od_data.artifacts import cached, cached_value, key, modules, partial


@pytest.fixture
def package(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A fake `mta_od_data`: `a` imports `b` and the extension `_ext`, `c` is apart."""
    root = tmp_path / "src" / "mta_od_data"
    (root / "sub").mkdir(parents=True)
    (root / "__init__.py").write_text("")
    (root / "sub" / "__init__.py").write_text("import mta_od_data.c\n")
    (root / "a.py").write_text(
        "import json\nfrom mta_od_data.sub import b\nfrom mta_od_data._ext import run\n"
    )
    (root / "sub" / "b.py").write_text("from .. import __name__\n")
    (root / "c.py").write_text("")
    monkeypatch.setattr(artifacts, "PACKAGE", root)
    return root


@pytest.fixture
def extension(tmp_path: Path) -> dict[str, list[Path]]:
    crate = tmp_path / "crate.rs"
    crate.write_text("fn main() {}\n")
    return {"mta_od_data._ext": [crate]}


def test_modules_follow_imports(
    package: Path, extension: dict[str, list[Path]]
) -> None:
    assert modules("mta_od_data.a", extension) == sorted(
        [
            package / "__init__.py",
            package / "a.py",
            package / "sub" / "__init__.py",
            package / "sub" / "b.py",
            *extension["mta_od_data._ext"],
        ]
    )


def test_unknown_extension_is_an_error(package: Path) -> None:
    with pytest.raises(ValueError, match="_ext has no source"):
        modules("mta_od_data.a")


def code_key(extension: dict[str, list[Path]], data: Path, args: object) -> str:
    return key(modules("mta_od_data.a", extension), [data], args)


def test_key_changes_with_inputs(
    package: Path, extension: dict[str, list[Path]], tmp_path: Path
) -> None:
    data = tmp_path / "data.parquet"
    data.write_bytes(b"rows")
    before = code_key(extension, data, ("2025-09-17", True))
    assert code_key(extension, data, ("2025-09-17", True)) == before

    # Not by a module nothing imports, nor `sub/__init__.py`'s own imports.
    (package / "c.py").write_text("x = 1\n")
    assert code_key(extension, data, ("2025-09-17", True)) == before

    for changed in [package / "sub" / "b.py", *extension["mta_od_data._ext"]]:
        text = changed.read_text()
        changed.write_text(text + "# changed\n")
        assert code_key(extension, data, ("2025-09-17", True)) != before
        changed.write_text(text)
        assert code_key(extension, data, ("2025-09-17", True)) == before

    data.write_bytes(b"other rows")
    assert code_key(extension, data, ("2025-09-17", True)) != before


def test_key_changes_with_args(
    package: Path, extension: dict[str, list[Path]], tmp_path: Path
) -> None:
    data = tmp_path / "data.parquet"
    data.write_bytes(b"rows")
    before = code_key(extension, data, ("2025-09-17", True))
    assert code_key(extension, data, ("2025-09-17", False)) != before
    assert code_key(extension, data, ("2025-09-18", True)) != before


def test_partial_keeps_the_extension_last() -> None:
    assert partial(Path("k.osm.pbf")) == Path("k.partial.osm.pbf")
    assert partial(Path("k")) == Path("k.partial")


def test_built_once(tmp_path: Path) -> None:
    builds: list[Path] = []

    def build(tmp: Path) -> None:
        builds.append(tmp)
        tmp.mkdir()
        (tmp / "manifest.csv").write_text("date\n")

    entry = tmp_path / "routing" / "abc"
    assert cached(entry, build) == entry
    assert cached(entry, build) == entry
    assert builds == [tmp_path / "routing" / "abc.partial"]
    assert (entry / "manifest.csv").read_text() == "date\n"


def test_interrupted_build_leaves_no_entry(tmp_path: Path) -> None:
    entry = tmp_path / "abc.pickle"

    def interrupted() -> int:
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        cached_value(entry, interrupted)
    assert not entry.exists()

    def half_written(tmp: Path) -> None:
        tmp.write_text("half")
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        cached(entry, half_written)
    assert not entry.exists()

    # The next build writes over the partial one.
    assert cached_value(entry, lambda: 3) == 3
    assert cached_value(entry, lambda: 4) == 3


def test_entry_read_by_content_not_its_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An entry built again, the same, under another key, leaves keys reading it."""
    monkeypatch.setattr(artifacts, "CACHE", tmp_path)
    (tmp_path / "streets").mkdir()
    first = tmp_path / "streets" / "abc.osm.pbf"
    again = tmp_path / "streets" / "def.osm.pbf"
    first.write_bytes(b"ways")
    again.write_bytes(b"ways")
    assert key([first], [], ()) == key([again], [], ())
    again.write_bytes(b"other ways")
    assert key([first], [], ()) != key([again], [], ())
