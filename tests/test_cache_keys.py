"""`uv` rebuilds the `raptor` extension only when a file in `pyproject.toml`'s
`tool.uv.cache-keys` changes, so every file compiled into it must be one:
each crate's sources and build script, and what they embed with `include_str!`
or `include_bytes!`, which a stale build otherwise keeps the old copy of.
"""

import re
import tomllib
from glob import glob
from pathlib import Path

from mta_od_data import ROOT

CRATES = ["raptor", "streets"]
EMBED = re.compile(r"include_(?:str|bytes)!\(\s*\"([^\"]+)\"\s*\)")


def cache_keys() -> set[Path]:
    keys = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["uv"]
    return {
        Path(f).resolve()
        for k in keys["cache-keys"]
        for f in glob(str(ROOT / k["file"]), recursive=True)
    }


def compiled() -> set[Path]:
    """Every file the crates build from: their sources, build scripts,
    and what the sources embed, relative to the file naming them."""
    found: set[Path] = set()
    for crate in CRATES:
        sources = [*(ROOT / crate / "src").rglob("*.rs"), ROOT / crate / "build.rs"]
        for rs in sources:
            if not rs.exists():
                continue
            found.add(rs.resolve())
            for embedded in EMBED.findall(rs.read_text()):
                found.add((rs.parent / embedded).resolve())
        found.add((ROOT / crate / "Cargo.toml").resolve())
    return found


def test_every_compiled_file_is_a_cache_key() -> None:
    missing = sorted(
        str(p.relative_to(ROOT.resolve())) for p in compiled() - cache_keys()
    )
    assert not missing, (
        "the extension builds from these, but `uv` wouldn't rebuild it "
        f"when they change; add them to `tool.uv.cache-keys`: {missing}"
    )
