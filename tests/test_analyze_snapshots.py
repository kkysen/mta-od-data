"""Each `analyze` subcommand's committed `.md` report
must match a fresh run of the same command.

Runs each command through the CLI's own `app`, in this process,
with the argv handed in rather than taken from `sys.argv`:
`InvocationGroup` records what it was given either way, so the
`Produced by` line comes out as it would from a shell, and a run
costs one parse rather than one interpreter.

Skipped when `data/mta_od.parquet` is missing:
it's gitignored, so this can't run in CI.
"""

import shlex
from dataclasses import dataclass
from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.cli import app

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
    Snapshot(
        name="deinterlining-nostrand",
        cmd=["mta-od-data", "analyze", "deinterlining", "--category", "Nostrand"],
        path=ANALYZE_DIR / "nostrand_deinterlining.md",
    ),
    Snapshot(
        name="deinterlining-fm-swap",
        cmd=["mta-od-data", "analyze", "deinterlining", "--category", "F/M Swap"],
        path=ANALYZE_DIR / "fm_swap_deinterlining.md",
    ),
]


@pytest.mark.skipif(
    not PARQUET.exists(),
    reason=(
        f"{PARQUET.relative_to(ROOT)} not found "
        "(run `uv run mta-od-data prepare` first)"
    ),
)
@pytest.mark.parametrize("snapshot", SNAPSHOTS, ids=lambda s: s.name)
def test_snapshot_matches_fresh_run(
    snapshot: Snapshot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tmp_out = tmp_path / snapshot.path.name
    prog, *args = snapshot.cmd
    # `cmd` names its paths relative to the repo root, and the committed
    # `Produced by` line quotes them exactly as written, so they have to
    # be resolved from there rather than from wherever pytest was run.
    monkeypatch.chdir(ROOT)
    # `app(args=...)`, so the `prog_name` and the arguments are this
    # list and not pytest's own argv, and `standalone_mode` left on, so
    # a command that fails exits the way it would in a shell.
    with pytest.raises(SystemExit) as exit:
        app(args=[*args, "--markdown-out", str(tmp_out)], prog_name=prog)
    # `None` is `sys.exit()` with nothing to say, which is a success.
    assert exit.value.code in (0, None), (
        f"{shlex.join(snapshot.cmd)} exited {exit.value.code}; "
        f"its own output is captured above"
    )

    # The snapshot embeds its own producing argv,
    # so undo the substitution of the real path for this scratch one,
    # which would otherwise be a spurious diff on that line alone.
    rel_path = snapshot.path.relative_to(ROOT)
    fresh = tmp_out.read_text().replace(str(tmp_out), str(rel_path))
    # A missing snapshot is just the empty case of an out-of-date one:
    # read it as such so it gets the same "regenerate it with" message
    # instead of an opaque `FileNotFoundError`.
    committed = snapshot.path.read_text() if snapshot.path.exists() else None
    # `shlex.join`, so the line can be pasted into a shell as-is:
    # a category like `F/M Swap` is one argument only once quoted,
    # which is also how the report's own `Produced by` line writes it.
    rerun = shlex.join(["uv", "run", *snapshot.cmd, "--markdown-out", str(rel_path)])
    assert fresh == committed, (
        f"{rel_path} is {'out of date' if committed is not None else 'missing'}. "
        "Regenerate it with:\n"
        f"  {rerun}\n"
        "and commit the result."
    )
