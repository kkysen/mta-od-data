"""Snapshot tests: each `analyze` subcommand's committed `.md` report, kept
alongside its module under `src/mta_od_data/analyze/`, must match a fresh
run of the same command.

Runs the real installed CLI as a subprocess (not an in-process call) so the
`Produced by` line it embeds reflects the actual invocation, the same way a
human regenerating the file by hand would see it.

Skipped when `data/mta_od.parquet` is missing: it's gitignored (1.1GB, not
committed) and only exists locally after `mta-od-data prepare`, so this
can't run in CI.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT

PARQUET = DATA / "mta_od.parquet"
ANALYZE_DIR = ROOT / "src" / "mta_od_data" / "analyze"


@dataclass(frozen=True, slots=True)
class Snapshot:
    # Also the pytest ID for this case (see `ids=` below).
    name: str
    # Canonical invocation, keep in sync with the snapshot file's own
    # "Produced by" line.
    cmd: list[str]
    path: Path


SNAPSHOTS = [
    Snapshot(
        name="one-seat-rides",
        cmd=[
            "mta-od-data",
            "analyze",
            "one-seat-rides",
            "--routes",
            "B,D,N,Q,R",
            "--primary-routes",
            "B,D,N,Q",
            "--trunk-b",
            "N,Q,R",
            "--all-corridor-scenarios",
            "--csv-out",
            "data/dekalb_weekday_pairs.csv",
        ],
        path=ANALYZE_DIR / "one_seat_rides.md",
    ),
    Snapshot(
        name="regional-flow",
        cmd=["mta-od-data", "analyze", "regional-flow"],
        path=ANALYZE_DIR / "regional_flow.md",
    ),
]


@pytest.mark.skipif(
    not PARQUET.exists(),
    reason=(f"{PARQUET.relative_to(ROOT)} not found (run `mta-od-data prepare` first)"),
)
@pytest.mark.parametrize("snapshot", SNAPSHOTS, ids=lambda s: s.name)
def test_snapshot_matches_fresh_run(snapshot: Snapshot, tmp_path: Path) -> None:
    tmp_out = tmp_path / snapshot.path.name
    result = subprocess.run(
        [*snapshot.cmd, "--markdown-out", str(tmp_out)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    # The snapshot embeds its own producing argv, so undo the substitution of
    # the real path for this scratch one -- otherwise this always reports a
    # spurious diff on that line alone.
    rel_path = snapshot.path.relative_to(ROOT)
    fresh = tmp_out.read_text().replace(str(tmp_out), str(rel_path))
    committed = snapshot.path.read_text()
    assert fresh == committed, (
        f"{rel_path} is out of date. Regenerate it with:\n"
        f"  {' '.join(snapshot.cmd)} --markdown-out {rel_path}\n"
        "and commit the result."
    )
