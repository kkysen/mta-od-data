"""Each `analyze` subcommand's committed `.md` report
must match a fresh run of the same command.

Runs each command through the CLI's own `app`, in this process,
with the argv handed in rather than taken from `sys.argv`:
`InvocationGroup` records what it was given either way, so the
`Produced by` line comes out as it would from a shell, and a run
costs one parse rather than one interpreter.

Each command builds what it reads when it's missing or out of date:
the OD Parquet (`downloads.od_parquet`), and for `free-transfers` and `ridership`,
the routing and OD factors, through the cache (`builds.routed`, `builds.od_factors`).
So a commit changing what routes reruns the routing here.

The reports that route are checked on every commit for one month, `MONTH`,
from a copy of each report for it in a folder named for it beside the full one,
as a fifth of the routing, so a commit still shows how it moves their numbers.
Their full reports, over all of `builds.report_dates`, are marked `full`,
and checked by the `pytest-full` hook before each push instead.
"""

import shlex
from dataclasses import dataclass
from pathlib import Path

import pytest

from mta_od_data import ROOT
from mta_od_data.cli import app

# Every case reruns a report through the CLI, which can route on a cache miss:
# minutes to hours, so commits on agent worktrees skip them (`SKIP=pytest-e2e`).
pytestmark = pytest.mark.e2e

# The one month the reports that route are checked for on each commit.
MONTH = "2025-09"
ANALYZE_DIR = ROOT / "src" / "mta_od_data" / "analyze"
RIDERSHIP_DIR = ROOT / "src" / "mta_od_data" / "ridership"


@dataclass(frozen=True, slots=True)
class Snapshot:
    # Also the pytest ID for this case (see `ids=` below).
    name: str
    # Keep in sync with the snapshot file's own "Produced by" line.
    cmd: list[str]
    path: Path
    # Checked before each push rather than on each commit (see the docstring).
    full: bool = False


def routed_snapshots(name: str, cmd: list[str], path: Path) -> list[Snapshot]:
    """A report that routes: in full, and for `MONTH` alone, in its own folder."""
    return [
        Snapshot(name, cmd, path, full=True),
        Snapshot(
            f"{name}-{MONTH}",
            [*cmd, "--month", MONTH],
            path.parent / MONTH / path.name,
        ),
    ]


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
    *routed_snapshots(
        "free-transfers",
        ["mta-od-data", "analyze", "free-transfers"],
        ANALYZE_DIR / "free_transfers.md",
    ),
    *(
        snapshot
        for by in [
            ["complex"],
            ["station"],
            ["station-direction"],
            ["platform"],
            ["route"],
            ["line"],
            ["line", "route"],
            ["trip"],
        ]
        for snapshot in routed_snapshots(
            f"ridership-by-{'-and-'.join(by)}",
            ["mta-od-data", "ridership", *(a for b in by for a in ("--by", b))],
            RIDERSHIP_DIR / f"by_{'_and_'.join(by).replace('-', '_')}.md",
        )
    ),
]


@pytest.mark.parametrize(
    "snapshot",
    [pytest.param(s, marks=[pytest.mark.full] if s.full else []) for s in SNAPSHOTS],
    ids=lambda s: s.name,
)
def test_snapshot_matches_fresh_run(
    snapshot: Snapshot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tmp_out = tmp_path / snapshot.path.name
    prog, *args = snapshot.cmd
    # `--csv-out` to the scratch directory too, not into `data/`:
    # rewriting files there would change `ridership`'s cache key,
    # which stats every file under `data/`, so every run missed it.
    csv_dir: Path | None = None
    for i, arg in enumerate(args[:-1]):
        if arg == "--csv-out":
            csv_out = Path(args[i + 1])
            csv_dir = csv_out.parent
            args[i + 1] = str(tmp_path / csv_out.name)
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
    if csv_dir is not None:
        fresh = fresh.replace(f"{tmp_path}/", f"{csv_dir}/")
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

    # And its charts, `<its name>-<chart>.svg` beside it, the same way.
    charts = f"{snapshot.path.stem}-*.svg"
    fresh_charts = {p.name: p.read_text() for p in tmp_path.glob(charts)}
    committed_charts = {
        p.name: p.read_text() for p in snapshot.path.parent.glob(charts)
    }
    assert fresh_charts == committed_charts, (
        f"{rel_path}'s charts are out of date. Regenerate them with:\n"
        f"  {rerun}\n"
        "and commit the result."
    )
