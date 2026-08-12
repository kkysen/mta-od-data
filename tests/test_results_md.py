"""Snapshot test: RESULTS.md must match a fresh `mta-od-data` run.

Runs the real installed CLI as a subprocess (not an in-process call) so the
`Produced by` line it embeds reflects the actual invocation, the same way a
human regenerating RESULTS.md by hand would see it.

Skipped when `data/mta_od.parquet` is missing: it's gitignored (1.1GB, not
committed) and only exists locally after `mta-od-data prepare`, so this
can't run in CI.
"""

import subprocess
from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT

RESULTS_MD = ROOT / "RESULTS.md"
PARQUET = DATA / "mta_od.parquet"

# Canonical invocation. Keep in sync with RESULTS.md's own "Produced by" line.
ANALYZE_CMD = [
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
]


@pytest.mark.skipif(
    not PARQUET.exists(),
    reason=(f"{PARQUET.relative_to(ROOT)} not found (run `mta-od-data prepare` first)"),
)
def test_results_md_matches_fresh_run(tmp_path: Path) -> None:
    tmp_out = tmp_path / "RESULTS.md"
    result = subprocess.run(
        [*ANALYZE_CMD, "--markdown-out", str(tmp_out)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    # RESULTS.md embeds its own producing argv, so undo the substitution of
    # the real path for this scratch one -- otherwise this always reports a
    # spurious diff on that line alone.
    fresh = tmp_out.read_text().replace(str(tmp_out), "RESULTS.md")
    committed = RESULTS_MD.read_text()
    assert fresh == committed, (
        "RESULTS.md is out of date. Regenerate it with:\n"
        f"  {' '.join(ANALYZE_CMD)} --markdown-out RESULTS.md\n"
        "and commit the result."
    )
