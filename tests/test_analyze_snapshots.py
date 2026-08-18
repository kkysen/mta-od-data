"""Each `analyze` subcommand's committed `.md` report
must match a fresh run of the same command.

Runs the real installed CLI as a subprocess, not an in-process call,
so the `Produced by` line it embeds reflects the actual invocation,
the same way a human regenerating the file by hand would see it.

Skipped when `data/mta_od.parquet` is missing:
it's gitignored, so this can't run in CI.
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
    # Keep in sync with the snapshot file's own "Produced by" line.
    cmd: list[str]
    path: Path


SNAPSHOTS = [
    Snapshot(
        name="one-seat-rides-dekalb",
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
        path=ANALYZE_DIR / "dekalb_one_seat_rides.md",
    ),
    Snapshot(
        name="one-seat-rides-nostrand",
        cmd=[
            "mta-od-data",
            "analyze",
            "one-seat-rides",
            "--boundary-complex-id",
            "626",
            "--origin-side",
            "south",
            "--dest-side",
            "north",
            "--routes",
            "2,3,4,5",
            "--primary-routes",
            "2,3,4,5",
            "--trunk-a",
            "2,3",
            "--trunk-a-label",
            "7 Av/West Side",
            "--trunk-b",
            "4,5",
            "--trunk-b-label",
            "Lexington Av/East Side",
            "--origin-corridor-a-routes",
            "2,5",
            "--origin-corridor-a-label",
            "Nostrand Av Line",
            "--origin-corridor-b-routes",
            "3,4",
            "--origin-corridor-b-label",
            "Eastern Pkwy/New Lots Line",
            "--all-corridor-scenarios",
            "--csv-out",
            "data/nostrand_weekday_pairs.csv",
        ],
        path=ANALYZE_DIR / "nostrand_one_seat_rides.md",
    ),
    Snapshot(
        name="regional-flow",
        cmd=["mta-od-data", "analyze", "regional-flow"],
        path=ANALYZE_DIR / "regional_flow.md",
    ),
    Snapshot(
        name="deinterlining-dekalb",
        cmd=["mta-od-data", "analyze", "deinterlining", "--category", "DeKalb"],
        path=ANALYZE_DIR / "dekalb_deinterlining.md",
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

    # The snapshot embeds its own producing argv,
    # so undo the substitution of the real path for this scratch one,
    # which would otherwise be a spurious diff on that line alone.
    rel_path = snapshot.path.relative_to(ROOT)
    fresh = tmp_out.read_text().replace(str(tmp_out), str(rel_path))
    committed = snapshot.path.read_text()
    assert fresh == committed, (
        f"{rel_path} is out of date. Regenerate it with:\n"
        f"  {' '.join(snapshot.cmd)} --markdown-out {rel_path}\n"
        "and commit the result."
    )
