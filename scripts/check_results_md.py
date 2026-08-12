#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Pre-commit hook: check RESULTS.md matches a fresh run of scripts/02_analyze.py.

Check-only, like this repo's other pre-commit hooks (`ruff format --check`,
`ty`, `pyrefly-check`) -- never rewrites RESULTS.md itself. On mismatch,
prints a diff and the command to regenerate it.
"""

import difflib
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_MD = ROOT / "RESULTS.md"
PARQUET = ROOT / "data" / "mta_od.parquet"

# Canonical invocation. Keep in sync with RESULTS.md's own "Produced by" line
# -- that line embeds sys.argv from the run below, so it must match
# byte-for-byte or every check (and every real regen) reports a spurious diff.
ANALYZE_CMD = [
    "uv",
    "run",
    "scripts/02_analyze.py",
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


def main() -> int:
    if not PARQUET.exists():
        print(
            f"skip: {PARQUET.relative_to(ROOT)} not found "
            "(run scripts/01_prepare_data.py first)",
            file=sys.stderr,
        )
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "RESULTS.md"
        result = subprocess.run(
            [*ANALYZE_CMD, "--markdown-out", str(tmp_out)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            print(f"error: `{shlex.join(ANALYZE_CMD)}` failed", file=sys.stderr)
            return 1
        # RESULTS.md embeds its own producing argv (including --markdown-out),
        # so undo the substitution of the real path for this scratch one --
        # otherwise every run reports a spurious diff on that line alone.
        fresh = tmp_out.read_text().replace(str(tmp_out), "RESULTS.md")

    committed = RESULTS_MD.read_text() if RESULTS_MD.exists() else ""
    if fresh == committed:
        return 0

    diff = difflib.unified_diff(
        committed.splitlines(keepends=True),
        fresh.splitlines(keepends=True),
        fromfile="RESULTS.md (committed)",
        tofile="RESULTS.md (fresh)",
    )
    sys.stdout.writelines(diff)
    print(
        "\nRESULTS.md is out of date. Regenerate it with:\n"
        f"  {shlex.join(ANALYZE_CMD)} --markdown-out RESULTS.md\n"
        "and commit the result.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
