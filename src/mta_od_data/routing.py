"""Routing each (month, weekday) in a range of dates, as `raptor assign-range` does,
writing the paths and a manifest of the dates run.

Apart from `raptor.py`, which is the command line around it,
so that what a cached run (`builds.routed`) is keyed on is the code that routes,
not every module the commands import for their defaults.
"""

from csv import DictWriter
from datetime import date
from pathlib import Path

from mta_od_data._raptor import assign_dates, load_versions, pick_weekdays

MANIFEST_FIELDS = [
    "date",
    "year",
    "month",
    "day_of_week",
    "days",
    "feed",
    "paths",
    "path_texts",
    "trips",
    "riders_in",
    "riders_assigned",
    "unassigned_no_stops",
    "unassigned_unreachable",
    "unassigned_no_departure",
]


def route_range(
    start: date,
    end: date,
    gtfs_dir: Path,
    od: Path,
    stations: Path,
    platforms: Path,
    config: Path,
    zstd_level: int,
    walks: tuple[Path, Path] | None,
    out_dir: Path,
    named: Path | None = None,
) -> Path:
    """Route a representative date per (month, weekday) from `start` to `end`
    into `out_dir`, with the latest feed version covering it,
    and write a manifest of the dates run and how many days each stands for,
    naming their files as in `named` if given, where `out_dir` will be moved to.
    Returns the manifest's path."""
    named = named or out_dir
    picks = pick_weekdays(load_versions(gtfs_dir), start, end)
    out_dir.mkdir(parents=True, exist_ok=True)
    outs = [out_dir / f"paths-{day}.parquet" for day, _, _ in picks]
    summaries = assign_dates(
        [
            (version, day, out)
            for (day, version, _), out in zip(picks, outs, strict=True)
        ],
        od,
        stations,
        platforms,
        config,
        zstd_level,
        walks,
    )
    manifest_path = out_dir / "manifest.csv"
    with manifest_path.open("w", newline="") as f:
        manifest = DictWriter(f, MANIFEST_FIELDS)
        manifest.writeheader()
        for (day, version, days), out, s in zip(picks, outs, summaries, strict=True):
            print(f"== {day} ({day:%A})")
            print(s.report, end="")
            paths = named / out.name
            manifest.writerow(
                {
                    "date": day,
                    "year": day.year,
                    "month": day.month,
                    "day_of_week": f"{day:%A}",
                    "days": days,
                    "feed": version.path,
                    "paths": paths,
                    "path_texts": named / s.path_texts.name,
                    # Beside its paths, as `assign_dates` writes it (`trips_out`).
                    "trips": paths.with_name(f"trips-{day}.parquet"),
                    "riders_in": s.riders_in,
                    "riders_assigned": s.riders_assigned,
                    "unassigned_no_stops": s.unassigned_no_stops,
                    "unassigned_unreachable": s.unassigned_unreachable,
                    "unassigned_no_departure": s.unassigned_no_departure,
                }
            )
    print(f"wrote {manifest_path}")
    return manifest_path
