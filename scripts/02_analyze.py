#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = ["duckdb", "typer"]
# ///
import csv
import math
import shlex
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal, Self

import duckdb
from typer import Option, Typer

app = Typer(rich_markup_mode=None)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


class DayType(StrEnum):
    WEEKDAY = "weekday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    ALL = "all"


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
DAY_TYPE_PRESETS: dict[DayType, tuple[str, ...] | None] = {
    DayType.WEEKDAY: WEEKDAYS,
    DayType.SATURDAY: ("Saturday",),
    DayType.SUNDAY: ("Sunday",),
    DayType.ALL: None,
}


@dataclass(slots=True)
class Station:
    complex_id: int
    name: str
    routes: set[str]
    lat: float
    lon: float

    @classmethod
    def load_complex(cls, row: dict[str, str]) -> Self:
        cid = int(row["complex_id"])
        return cls(
            complex_id=cid,
            name=row["display_name"],
            routes=set(row["daytime_routes"].split()),
            lat=float(row["latitude"]),
            lon=float(row["longitude"]),
        )

    @classmethod
    def load_complexes(cls, path: Path) -> dict[int, Self]:
        with path.open(newline="") as f:
            return {
                (station := cls.load_complex(row)).complex_id: station
                for row in csv.DictReader(f)
            }

    @classmethod
    def load_individual(cls, row: dict[str, str]) -> Self:
        """Per-physical-station rows (not complex centroids). A complex can merge
        several physical stations (e.g. Times Sq-42 St/Port Authority Bus
        Terminal), so its centroid can sit well away from any actual platform;
        these per-station points give accurate nearest-station distances."""
        return cls(
            complex_id=int(row["complex_id"]),
            name=row["stop_name"],
            routes=set(row["daytime_routes"].split()),
            lat=float(row["gtfs_latitude"]),
            lon=float(row["gtfs_longitude"]),
        )

    @classmethod
    def load_individuals(cls, path: Path) -> list[Self]:
        with path.open(newline="") as f:
            return [cls.load_individual(row) for row in csv.DictReader(f)]


@dataclass(slots=True)
class PairRow:
    origin_id: int
    origin_name: str
    origin_routes: str
    dest_id: int
    dest_name: str
    dest_routes: str
    riders: float
    one_seat: bool
    close: bool | None
    dist_m: float | None


@dataclass(slots=True)
class DestStats:
    name: str
    total: float = 0.0
    one_seat: float = 0.0
    classified: float = 0.0
    close: float = 0.0
    dist_weighted: float = 0.0

    @property
    def one_seat_pct(self) -> float:
        return 100 * self.one_seat / self.total if self.total else float("nan")

    @property
    def close_pct(self) -> float | None:
        return 100 * self.close / self.classified if self.classified else None

    @property
    def avg_dist_m(self) -> float | None:
        return self.dist_weighted / self.classified if self.classified else None


@dataclass(slots=True)
class ScenarioResult:
    label: str
    corridor_scenario_active: bool
    corridor_scenario_note: str | None
    total_riders: float
    one_seat_riders: float
    classified_one_seat_riders: float
    close_riders: float
    classified_indirect_riders: float
    close_one_seat_riders: float
    effective_one_seat_riders: float
    rows: list[PairRow]
    dest_stats: dict[int, DestStats]
    per_origin: dict[int, list[float]]

    @property
    def direct_one_seat_pct(self) -> float:
        return (
            100 * self.one_seat_riders / self.total_riders
            if self.total_riders
            else float("nan")
        )

    @property
    def effective_one_seat_pct(self) -> float | None:
        if not self.corridor_scenario_active or not self.total_riders:
            return None
        return 100 * self.effective_one_seat_riders / self.total_riders

    def print_headline(
        self,
        *,
        show_label: bool,
        day_type: DayType,
        dest_side: str,
        trunk_a_label: str,
        trunk_b_label: str,
        close_threshold_m: float,
    ) -> None:
        if show_label:
            print(f"\n=== Scenario: {self.label} ===")
        else:
            print(
                f"\n=== Scope: origin in {{south of boundary}}, destination "
                f"{dest_side} of boundary, day-type={day_type} ==="
            )
        print(f"Average {day_type} ridership: {self.total_riders:,.0f}")
        if self.total_riders:
            print(
                f"One-seat (no transfer): {self.one_seat_riders:,.0f} "
                f"({100 * self.one_seat_riders / self.total_riders:.1f}%)"
            )
            print(
                f"Transfer required:      "
                f"{self.total_riders - self.one_seat_riders:,.0f} "
                f"({100 * (1 - self.one_seat_riders / self.total_riders):.1f}%)"
            )

        if self.corridor_scenario_active:
            if self.classified_indirect_riders:
                pct = 100 * self.close_one_seat_riders / self.classified_indirect_riders
                print(
                    f"Close one-seat (short walk instead): "
                    f"{self.close_one_seat_riders:,.0f} of "
                    f"{self.classified_indirect_riders:,.0f} riders without a "
                    f"direct one-seat ride ({pct:.1f}%)"
                )
            if self.total_riders:
                print(
                    f"Effective one-seat (direct + close): "
                    f"{self.effective_one_seat_riders:,.0f} "
                    f"({100 * self.effective_one_seat_riders / self.total_riders:.1f}%)"
                )
        elif self.classified_one_seat_riders:
            pct = 100 * self.close_riders / self.classified_one_seat_riders
            print(
                f"Close to the other trunk if deinterlined "
                f"({trunk_a_label} vs {trunk_b_label}): "
                f"{self.close_riders:,.0f} of "
                f"{self.classified_one_seat_riders:,.0f} one-seat riders ({pct:.1f}%)"
            )

    def print_details(
        self,
        stations_by_id: dict[int, Station],
        origin_ids: list[int],
    ) -> None:
        print("\n=== Per-origin-station breakdown (avg weekday riders) ===")
        for cid in origin_ids:
            name = stations_by_id[cid].name
            total, one_seat = self.per_origin[cid]
            pct = 100 * one_seat / total if total else float("nan")
            print(f"  {name:<45} total={total:>9,.0f}  one-seat={pct:5.1f}%")

        print(
            "\n=== Per-destination-station breakdown "
            "(avg weekday riders, sorted by total) ==="
        )
        for d in sorted(self.dest_stats.values(), key=_dest_total, reverse=True):
            pct = 100 * d.one_seat / d.total if d.total else float("nan")
            print(f"  {d.name:<55} total={d.total:>9,.0f}  one-seat={pct:5.1f}%")

    def render_markdown(
        self,
        *,
        show_label: bool,
        boundary_name: str,
        day_type: DayType,
        n_distinct_days: int,
        routes_set: set[str],
        origin_side: str,
        dest_side: str,
        trunk_a_label: str,
        trunk_b_label: str,
        close_threshold_m: float,
        top_n: int,
        csv_out: Path | None,
    ) -> str:
        lines: list[str] = []
        lines.append(
            f"# {trunk_a_label}/{trunk_b_label} deinterlining: one-seat-ride results "
            f"at {boundary_name}"
        )
        lines.append("")
        if show_label:
            lines.append(f"**Scenario: {self.label}**")
            lines.append("")
        lines.append(
            f"Scenario: average {day_type} ridership ({n_distinct_days} distinct days "
            f"in the data) on trains originating at stations served by "
            f"{','.join(sorted(routes_set))}, {origin_side} of {boundary_name}, with "
            f"destinations {dest_side} of {boundary_name} (i.e. trips that cross the "
            f"junction)."
        )
        lines.append("")
        if self.corridor_scenario_note:
            lines.append(self.corridor_scenario_note)
            lines.append("")
        lines.append(f"Produced by `{shlex.join(sys.argv)}`.")
        lines.append("")

        lines.append("## Headline numbers")
        lines.append("")
        lines.append(f"- **Total: {self.total_riders:,.0f} riders/{day_type}**")
        if self.total_riders:
            one_seat_pct = 100 * self.one_seat_riders / self.total_riders
            lines.append(
                f"- **One-seat rides (no transfer): {one_seat_pct:.1f}%** "
                f"({self.one_seat_riders:,.0f}/{day_type})"
            )
        if self.corridor_scenario_active:
            if self.classified_indirect_riders:
                close_pct = (
                    100 * self.close_one_seat_riders / self.classified_indirect_riders
                )
                lines.append(
                    f"- **Close one-seat rides: {close_pct:.1f}%** of the riders "
                    f"without a direct one-seat ride under this scenario "
                    f"({self.close_one_seat_riders:,.0f} of "
                    f"{self.classified_indirect_riders:,.0f}) are within "
                    f"{close_threshold_m:.0f}m of a station on their own corridor's "
                    f"assigned trunk -- i.e. no train change, just a short walk at "
                    f"the end to reach their actual destination."
                )
            if self.total_riders:
                effective_pct = 100 * self.effective_one_seat_riders / self.total_riders
                lines.append(
                    f"- **Effective one-seat rides (direct + close): "
                    f"{effective_pct:.1f}%** ({self.effective_one_seat_riders:,.0f}/"
                    f"{day_type}) -- direct one-seat riders plus the close one-seat "
                    f"riders above, i.e. riders who wouldn't feel a materially worse "
                    f"trip under this scenario."
                )
        elif self.classified_one_seat_riders:
            close_pct = 100 * self.close_riders / self.classified_one_seat_riders
            lines.append(
                f"- **Close to the other trunk if deinterlined: {close_pct:.1f}%** of "
                f"one-seat riders ({self.close_riders:,.0f} of "
                f"{self.classified_one_seat_riders:,.0f}) -- i.e. wouldn't need a "
                f"materially longer walk/transfer even if {trunk_a_label} and "
                f"{trunk_b_label} stopped interlining at {boundary_name}."
            )
        lines.append("")

        lines.append(f"## Top {top_n} origin/destination pairs (avg {day_type} riders)")
        lines.append("")
        lines.append(
            "| # | Riders | % of total | % of one-seat | Type | Close? | Dist "
            "| Origin → Destination |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        top_pairs = sorted(self.rows, key=_pair_riders, reverse=True)[:top_n]
        for i, r in enumerate(top_pairs, start=1):
            pct_total = (
                100 * r.riders / self.total_riders
                if self.total_riders
                else float("nan")
            )
            pct_one_seat_str = "--"
            if r.one_seat and self.one_seat_riders:
                pct_one_seat_str = f"{100 * r.riders / self.one_seat_riders:.2f}%"
            type_str = "1-seat" if r.one_seat else "xfer"
            close_str = "--" if r.close is None else str(r.close)
            dist_str = "--" if r.dist_m is None else f"{r.dist_m:.0f}m"
            lines.append(
                f"| {i} | {r.riders:,.0f} | {pct_total:.2f}% | {pct_one_seat_str} | "
                f"{type_str} | {close_str} | {dist_str} | "
                f"{r.origin_name} → {r.dest_name} |"
            )
        lines.append("")

        lines.append(
            f"## Top {top_n} destination stations, summed across all origins "
            f"(avg {day_type} riders)"
        )
        lines.append("")
        lines.append(
            "Sorted by each destination's one-seat ridership (i.e. its share of the "
            f"{self.one_seat_riders:,.0f}/{day_type} one-seat total)."
        )
        lines.append("")
        lines.append(
            "| Riders | One-seat % | % of all one-seat | Close? | Dist | Destination |"
        )
        lines.append("|---|---|---|---|---|---|")
        top_dests = sorted(self.dest_stats.values(), key=_dest_one_seat, reverse=True)[
            :top_n
        ]
        for d in top_dests:
            pct_all_one_seat = (
                100 * d.one_seat / self.one_seat_riders
                if self.one_seat_riders
                else float("nan")
            )
            close_pct = d.close_pct
            close_str = "--" if close_pct is None else f"{close_pct:.0f}%"
            avg_dist = d.avg_dist_m
            dist_str = "--" if avg_dist is None else f"{avg_dist:.0f}m"
            lines.append(
                f"| {d.total:,.0f} | {d.one_seat_pct:.1f}% | {pct_all_one_seat:.2f}% | "
                f"{close_str} | {dist_str} | {d.name} |"
            )
        lines.append("")

        lines.append("## Notes on reading these tables")
        lines.append("")
        if self.corridor_scenario_active:
            lines.append(
                f'- "Close?"/"Dist" describe distance from the destination to the '
                f"nearest station on the trunk the origin's *own* corridor got "
                f"assigned in this scenario, thresholded at {close_threshold_m:.0f}m. "
                f"They only apply to `xfer` rows -- riders without a direct "
                f"one-seat ride under this scenario -- since a `1-seat` row "
                f"already has a direct train and needs no walk. A close `xfer` "
                f"row is a *close one-seat ride*: no train change, just a short "
                f"walk to the actual destination."
            )
            lines.append(
                '- In the per-destination table, "Close?"/"Dist" are '
                "ridership-weighted across that destination's classified "
                "indirect (non-direct-one-seat) pairs."
            )
            lines.append(
                "- `1-seat` rows have no close/dist value since the classification "
                "only applies to trips without a direct one-seat ride under this "
                "scenario."
            )
        else:
            lines.append(
                f'- "Close?"/"Dist" describe distance from the destination to the '
                f"nearest station on the trunk *not* used to reach it one-seat "
                f"({trunk_a_label} vs {trunk_b_label}), thresholded at "
                f"{close_threshold_m:.0f}m. In the per-pair table this is a single "
                f"trip's classification; `True`/`0m` covers destinations already "
                f"served by both trunks, and one-seat connections that never "
                f"actually cross the junction (via a route in the universe but not "
                f"in `--primary-routes`) -- those can't be affected by deinterlining "
                f"either way."
            )
            lines.append(
                '- In the per-destination table, "Close?"/"Dist" are '
                "ridership-weighted across that destination's classified "
                "one-seat pairs."
            )
            lines.append(
                "- `xfer` rows have no close/dist value since the classification only "
                "applies to one-seat trips."
            )
        csv_note = f" (`{csv_out}`)" if csv_out else ""
        lines.append(
            f"- Full row-level detail (every origin/destination pair, not just the top "
            f"{top_n}) is in the `--csv-out` file{csv_note}, if one was written."
        )
        lines.append("")
        return "\n".join(lines)


@dataclass(slots=True)
class ScenarioDef:
    label: str
    corridor_a_assigned_set: set[str]
    corridor_b_assigned_set: set[str]
    active: bool
    # Filename suffix for per-scenario CSV output; None means "write to the
    # given path unchanged" (only used when there's exactly one scenario, so
    # single-scenario invocations keep their exact historical filenames).
    suffix: str | None


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def parse_route_set(s: str) -> set[str]:
    return {r.strip() for r in s.split(",") if r.strip()}


def classify_one_seat(
    origin_routes: set[str],
    dest_routes: set[str],
    routes: set[str],
    primary_routes: set[str],
) -> tuple[bool, set[str]]:
    """A trip is one-seat if some shared route actually crosses the boundary
    junction (a primary route), or if the destination isn't served by any
    primary route anyway (so the non-primary connection, e.g. R, isn't
    standing in for a junction crossing that never really happens)."""
    shared = origin_routes & dest_routes & routes
    is_one_seat = bool(shared) and (
        bool(shared & primary_routes) or not (dest_routes & primary_routes)
    )
    return is_one_seat, shared


def corridor_swap_label(
    corridor_a_routes: set[str],
    corridor_b_routes: set[str],
    origin_corridor_a_label: str,
    origin_corridor_b_label: str,
) -> str:
    return (
        f"{','.join(sorted(corridor_a_routes))} on {origin_corridor_a_label}, "
        f"{','.join(sorted(corridor_b_routes))} on {origin_corridor_b_label}"
    )


def suffixed_path(path: Path, suffix: str) -> Path:
    return path.with_name(f"{path.stem}_{suffix}{path.suffix}")


def write_csv(path: Path, rows: list[PairRow]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(PairRow)])
        writer.writeheader()
        writer.writerows(asdict(r) for r in rows)
    print(f"\nWrote {len(rows):,} rows to {path}")


def run_scenario(
    *,
    label: str,
    scoped: list[tuple[int, int, float]],
    total_riders: float,
    stations_by_id: dict[int, Station],
    origin_ids: list[int],
    routes_set: set[str],
    primary_routes_set: set[str],
    trunk_a_set: set[str],
    trunk_b_set: set[str],
    trunk_a_points: list[tuple[float, float]],
    trunk_b_points: list[tuple[float, float]],
    assigned_points: Callable[[set[str]], list[tuple[float, float]]],
    dest_points: Callable[[Station], list[tuple[float, float]]],
    min_dist_to_points: Callable[
        [list[tuple[float, float]], list[tuple[float, float]]], float | None
    ],
    close_threshold_m: float,
    origin_corridor_a_routes_set: set[str],
    origin_corridor_b_routes_set: set[str],
    origin_corridor_a_label: str,
    origin_corridor_b_label: str,
    corridor_a_assigned_set: set[str],
    corridor_b_assigned_set: set[str],
    corridor_scenario_active: bool,
    verbose: bool,
) -> ScenarioResult:
    # Effective routes used for one-seat classification at each origin. Under
    # a corridor scenario, this replaces an origin's real current routes with
    # whichever routes the scenario assigns to its physical corridor -- a
    # station that touches both corridors (e.g. a shared terminal) keeps
    # access to both assigned route sets, since no DeKalb-only deinterlining
    # scenario changes what serves it.
    effective_origin_routes: dict[int, set[str]] = {}
    if verbose:
        print(f"\nCorridor assignment (scenario active: {corridor_scenario_active}):")
    for cid in origin_ids:
        s = stations_by_id[cid]
        in_a = bool(s.routes & origin_corridor_a_routes_set)
        in_b = bool(s.routes & origin_corridor_b_routes_set)
        corridor_tag = "a+b" if in_a and in_b else "a" if in_a else "b" if in_b else "?"
        if not corridor_scenario_active:
            effective_origin_routes[cid] = s.routes
        elif in_a and in_b:
            effective_origin_routes[cid] = (
                corridor_a_assigned_set | corridor_b_assigned_set
            )
        elif in_a:
            effective_origin_routes[cid] = corridor_a_assigned_set
        elif in_b:
            effective_origin_routes[cid] = corridor_b_assigned_set
        else:
            effective_origin_routes[cid] = s.routes
            if corridor_scenario_active:
                print(
                    f"  warning: {s.name} (routes={sorted(s.routes)}) matches "
                    f"neither --origin-corridor-a-routes nor "
                    f"--origin-corridor-b-routes; leaving its real routes unscoped"
                )
        if verbose:
            print(
                f"  {cid:>4}  {s.name:<40}  corridor={corridor_tag:<3}  "
                f"effective_routes={sorted(effective_origin_routes[cid])}"
            )

    one_seat_riders = 0.0
    classified_one_seat_riders = 0.0
    close_riders = 0.0
    classified_indirect_riders = 0.0
    close_one_seat_riders = 0.0

    rows: list[PairRow] = []
    for origin_id, dest_id, riders in scoped:
        origin = stations_by_id[origin_id]
        dest = stations_by_id.get(dest_id)
        dest_routes = dest.routes if dest else set()
        is_one_seat, shared = classify_one_seat(
            effective_origin_routes[origin_id],
            dest_routes,
            routes_set,
            primary_routes_set,
        )
        if is_one_seat:
            one_seat_riders += riders

        close = None
        dist_m = None
        if corridor_scenario_active:
            # is_one_seat already reflects this scenario's deinterlined
            # routing, so a one-seat rider here already has a direct train --
            # no walk to evaluate. The riders worth asking about are the ones
            # who DON'T connect one-seat: how far would they need to walk to
            # reach a station on the trunk their own corridor actually got
            # assigned? If it's close, that's a "close one-seat ride" (get
            # off/board a short walk away, no train change), not a transfer.
            if not is_one_seat and dest:
                dist_m = min_dist_to_points(
                    dest_points(dest),
                    assigned_points(effective_origin_routes[origin_id]),
                )
                close = None if dist_m is None else dist_m <= close_threshold_m
                if close is not None:
                    classified_indirect_riders += riders
                    if close:
                        close_one_seat_riders += riders
        elif is_one_seat and dest:
            if not (shared & primary_routes_set):
                # This one-seat connection doesn't use any route that
                # actually crosses the boundary junction (e.g. it's via R,
                # which reaches Manhattan through the Montague St Tunnel and
                # never goes near DeKalb/Atlantic). Deinterlining the
                # junction can't affect a trip that never uses it, so this
                # rider needs no extra walk/transfer either way -- trivially
                # close.
                close, dist_m = True, 0.0
            else:
                # Trunk membership is a property of the destination complex
                # itself (what it's near/at), not of which specific shared
                # route made this particular pair one-seat.
                home_a = bool(dest_routes & trunk_a_set)
                home_b = bool(dest_routes & trunk_b_set)
                if home_a and home_b:
                    # The destination already has routes from both groups
                    # (e.g. a junction complex like Atlantic Av-Barclays Ctr
                    # or DeKalb Av) -- trivially "at" the other trunk.
                    close, dist_m = True, 0.0
                elif home_a:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_b_points)
                    close = None if dist_m is None else dist_m <= close_threshold_m
                elif home_b:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_a_points)
                    close = None if dist_m is None else dist_m <= close_threshold_m
                # close/dist_m stay None only if the destination has neither
                # trunk's routes at all -- no "other trunk" to speak of.

            if close is not None:
                classified_one_seat_riders += riders
                if close:
                    close_riders += riders

        rows.append(
            PairRow(
                origin_id=origin_id,
                origin_name=origin.name,
                origin_routes=",".join(sorted(effective_origin_routes[origin_id])),
                dest_id=dest_id,
                dest_name=dest.name if dest else f"complex {dest_id}",
                dest_routes=",".join(sorted(dest_routes)),
                riders=riders,
                one_seat=is_one_seat,
                close=close,
                dist_m=dist_m,
            )
        )

    # Riders with either a direct one-seat ride, or a close one-seat ride
    # instead (short walk, no train change). Only meaningful under a
    # corridor scenario -- close_one_seat_riders is always 0 otherwise, so
    # this trivially equals one_seat_riders in baseline mode.
    effective_one_seat_riders = one_seat_riders + close_one_seat_riders

    per_origin: dict[int, list[float]] = {cid: [0.0, 0.0] for cid in origin_ids}
    dest_stats: dict[int, DestStats] = {}
    for r in rows:
        per_origin[r.origin_id][0] += r.riders
        if r.one_seat:
            per_origin[r.origin_id][1] += r.riders
        d = dest_stats.setdefault(r.dest_id, DestStats(name=r.dest_name))
        d.total += r.riders
        if r.one_seat:
            d.one_seat += r.riders
        if r.close is not None:
            assert r.dist_m is not None
            d.classified += r.riders
            d.dist_weighted += r.riders * r.dist_m
            if r.close:
                d.close += r.riders

    corridor_scenario_note = None
    if corridor_scenario_active:
        corridor_scenario_note = (
            f"Deinterlining scenario: {origin_corridor_a_label} served by "
            f"{','.join(sorted(corridor_a_assigned_set))}; {origin_corridor_b_label} "
            f"served by {','.join(sorted(corridor_b_assigned_set))} (each origin's "
            f"one-seat eligibility uses these assigned routes instead of its real "
            f"current routes; a station touching both corridors keeps access to "
            f"both)."
        )

    return ScenarioResult(
        label=label,
        corridor_scenario_active=corridor_scenario_active,
        corridor_scenario_note=corridor_scenario_note,
        total_riders=total_riders,
        one_seat_riders=one_seat_riders,
        classified_one_seat_riders=classified_one_seat_riders,
        close_riders=close_riders,
        classified_indirect_riders=classified_indirect_riders,
        close_one_seat_riders=close_one_seat_riders,
        effective_one_seat_riders=effective_one_seat_riders,
        rows=rows,
        dest_stats=dest_stats,
        per_origin=per_origin,
    )


def print_scenario_comparison(results: list[ScenarioResult], day_type: DayType) -> None:
    print(f"\n=== Scenario comparison (avg {day_type} riders) ===")
    for r in results:
        effective_pct = r.effective_one_seat_pct
        effective_str = "n/a" if effective_pct is None else f"{effective_pct:.1f}%"
        print(
            f"  {r.label:<55} direct={r.direct_one_seat_pct:5.1f}%  "
            f"effective={effective_str}"
        )


def render_scenario_comparison(results: list[ScenarioResult], day_type: DayType) -> str:
    lines: list[str] = []
    lines.append("# Scenario comparison")
    lines.append("")
    lines.append(
        f"Average {day_type} ridership is the same {results[0].total_riders:,.0f}/"
        f"{day_type} across every scenario below -- only how many of those "
        f"riders get a one-seat ride changes."
    )
    lines.append("")
    lines.append(
        "| Scenario | Direct one-seat % | Effective one-seat % (direct + close) |"
    )
    lines.append("| --- | --- | --- |")
    for r in results:
        effective_pct = r.effective_one_seat_pct
        effective_str = "--" if effective_pct is None else f"{effective_pct:.1f}%"
        lines.append(f"| {r.label} | {r.direct_one_seat_pct:.1f}% | {effective_str} |")
    lines.append("")
    lines.append(
        '`--` marks today\'s actual routing: it has no "effective one-seat" '
        "figure because that metric only applies under a corridor scenario "
        "(crediting riders who lose their direct one-seat ride but stay close "
        "to an alternative). Today's actual routing answers a different "
        "question instead -- of *today's* one-seat riders, how many would "
        "stay close to the other trunk if deinterlined generically -- see its "
        "own section below for that number."
    )
    lines.append("")
    return "\n".join(lines)


def _dest_total(d: DestStats) -> float:
    return d.total


def _dest_one_seat(d: DestStats) -> float:
    return d.one_seat


def _pair_riders(r: PairRow) -> float:
    return r.riders


@app.command()
def main(
    parquet: Annotated[Path, Option()] = DATA / "mta_od.parquet",
    stations: Annotated[Path, Option()] = DATA / "stations_complexes.csv",
    stations_individual: Annotated[
        Path,
        Option(
            help=(
                "Per-physical-station reference CSV, used for accurate "
                "nearest-other-trunk distances"
            ),
        ),
    ] = DATA / "stations_individual.csv",
    day_type: Annotated[DayType, Option()] = DayType.WEEKDAY,
    days: Annotated[
        str | None,
        Option(help="Comma-separated exact 'Day of Week' values, overrides --day-type"),
    ] = None,
    boundary_complex_id: Annotated[
        int, Option(help="Junction station (default: Atlantic Av-Barclays Ctr)")
    ] = 617,
    origin_side: Annotated[
        Literal["south", "north"],
        Option(help="Origin relative to boundary latitude"),
    ] = "south",
    dest_side: Annotated[
        Literal["south", "north", "either"],
        Option(
            help=(
                "Destination relative to boundary latitude "
                "(scopes to trips that actually cross the junction)"
            )
        ),
    ] = "north",
    exclude_boundary_dest: Annotated[
        bool,
        Option(
            help=(
                "Exclude the boundary complex itself from valid destinations "
                "(default: included, since ending at the junction still means "
                "the trip crossed it)"
            )
        ),
    ] = False,
    routes: Annotated[
        str, Option(help="Route universe: origin filter + one-seat eligibility")
    ] = "B,D,N,Q",
    primary_routes: Annotated[
        str | None,
        Option(
            help=(
                "Routes that actually cross the boundary junction (default: same as "
                "--routes). A route in --routes but not here (e.g. R, which reaches "
                "Manhattan via the Montague St Tunnel and never passes "
                "DeKalb/Atlantic) "
                "only counts a trip as one-seat if the shared route is a primary one, "
                "or if the destination isn't served by any primary route either -- "
                "otherwise it's treated as requiring a transfer at the junction, "
                "matching real rider behavior even though the OD data itself has no "
                "transfer field."
            ),
        ),
    ] = None,
    trunk_a: Annotated[str, Option(help="Routes on trunk A")] = "B,D",
    trunk_a_label: Annotated[str, Option()] = "6 Ave express",
    trunk_b: Annotated[str, Option(help="Routes on trunk B")] = "N,Q",
    trunk_b_label: Annotated[str, Option()] = "Broadway express",
    origin_corridor_a_routes: Annotated[
        str,
        Option(
            help=(
                "Real-world routes that put an origin station on physical corridor "
                "A (used only to sort origins into a corridor, independent of any "
                "--corridor-a-assigned override below)"
            )
        ),
    ] = "D,N",
    origin_corridor_a_label: Annotated[str, Option()] = "4 Ave express",
    origin_corridor_b_routes: Annotated[
        str, Option(help="Real-world routes that put an origin station on corridor B")
    ] = "B,Q",
    origin_corridor_b_label: Annotated[str, Option()] = "Brighton",
    corridor_a_assigned: Annotated[
        str | None,
        Option(
            help=(
                "Deinterlining scenario override: routes that would actually serve "
                "corridor A stations (e.g. N,Q), replacing each such origin's real "
                "current routes for one-seat classification. Must be given together "
                "with --corridor-b-assigned; omit both to use each origin's real "
                "current routes (today's actual service, the default). Can't be "
                "combined with --all-corridor-scenarios."
            )
        ),
    ] = None,
    corridor_b_assigned: Annotated[
        str | None,
        Option(
            help=(
                "Deinterlining scenario override for corridor B. See "
                "--corridor-a-assigned."
            )
        ),
    ] = None,
    all_corridor_scenarios: Annotated[
        bool,
        Option(
            help=(
                "Run today's actual routing plus both full corridor-swap "
                "scenarios in one invocation: --trunk-a assigned to corridor A "
                "and --trunk-b to corridor B, then vice versa. Can't be combined "
                "with --corridor-a-assigned/--corridor-b-assigned. With "
                "--markdown-out, all three reports are written to one file; "
                "with --csv-out, each scenario gets its own suffixed file."
            )
        ),
    ] = False,
    close_threshold_m: Annotated[float, Option()] = 300.0,
    csv_out: Annotated[
        Path | None,
        Option(help="Optional: dump classified per-OD-pair rows here"),
    ] = None,
    markdown_out: Annotated[
        Path | None,
        Option(help="Optional: write a RESULTS.md-style markdown report here"),
    ] = None,
    top_n: Annotated[
        int, Option(help="Row count for the markdown top-pairs/top-destinations tables")
    ] = 25,
) -> None:
    """Analyze one-seat-ride / deinterlining share for trips crossing a subway junction.

    Generalized so the same script can be re-run for other day types, other
    station criteria, other data extracts, and other deinterlining scenarios
    (different junction, different trunk-line pairs) just by passing flags.

    Default scenario (the one this was built for): weekday trips on B/D/N/Q
    originating south of Atlantic Av-Barclays Ctr in Brooklyn, heading toward
    Manhattan through the DeKalb Ave interlining junction.

    \b
    Examples:
        # Default DeKalb scenario
        uv run scripts/02_analyze.py

    \b
        # Same scenario, Saturdays instead of weekdays
        uv run scripts/02_analyze.py --day-type saturday

    \b
        # Same scenario, against a newer data extract
        uv run scripts/02_analyze.py --parquet data/mta_od_2025.parquet

    \b
        # Write RESULTS.md automatically instead of transcribing output by hand
        uv run scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q \\
            --trunk-b N,Q,R --csv-out data/dekalb_weekday_pairs.csv \\
            --markdown-out RESULTS.md

    \b
        # A different junction/trunk pair, e.g. hypothetically Rogers Jct area
        uv run scripts/02_analyze.py --boundary-complex-id <id> --routes 2,3,4,5 \\
            --trunk-a 4,5 --trunk-a-label "Lexington Av express" \\
            --trunk-b 2,3 --trunk-b-label "7 Av express"

    \b
        # Full DeKalb deinterlining: N,Q run the 4 Ave express corridor,
        # B,D run Brighton (origin one-seat eligibility uses these assigned
        # routes instead of each station's real current routes)
        uv run scripts/02_analyze.py --corridor-a-assigned N,Q --corridor-b-assigned B,D

    \b
        # Today's actual routing plus both full B,D/N,Q corridor swaps, in
        # one invocation
        uv run scripts/02_analyze.py --all-corridor-scenarios --markdown-out RESULTS.md
    """
    days_list = (
        [d.strip() for d in days.split(",")] if days else DAY_TYPE_PRESETS[day_type]
    )
    routes_set = parse_route_set(routes)
    primary_routes_set = (
        parse_route_set(primary_routes) if primary_routes else routes_set
    )
    trunk_a_set = parse_route_set(trunk_a)
    trunk_b_set = parse_route_set(trunk_b)
    origin_corridor_a_routes_set = parse_route_set(origin_corridor_a_routes)
    origin_corridor_b_routes_set = parse_route_set(origin_corridor_b_routes)
    if (corridor_a_assigned is None) != (corridor_b_assigned is None):
        print(
            "error: --corridor-a-assigned and --corridor-b-assigned must be given "
            "together (or both omitted)",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if all_corridor_scenarios and (
        corridor_a_assigned is not None or corridor_b_assigned is not None
    ):
        print(
            "error: --all-corridor-scenarios can't be combined with "
            "--corridor-a-assigned/--corridor-b-assigned",
            file=sys.stderr,
        )
        raise SystemExit(1)
    corridor_scenario_active = corridor_a_assigned is not None
    corridor_a_assigned_set = (
        parse_route_set(corridor_a_assigned) if corridor_a_assigned else set()
    )
    corridor_b_assigned_set = (
        parse_route_set(corridor_b_assigned) if corridor_b_assigned else set()
    )

    if all_corridor_scenarios:
        scenario_defs = [
            ScenarioDef("today's actual routing", set(), set(), False, "actual"),
            ScenarioDef(
                corridor_swap_label(
                    trunk_a_set,
                    trunk_b_set,
                    origin_corridor_a_label,
                    origin_corridor_b_label,
                ),
                trunk_a_set,
                trunk_b_set,
                True,
                "a",
            ),
            ScenarioDef(
                corridor_swap_label(
                    trunk_b_set,
                    trunk_a_set,
                    origin_corridor_a_label,
                    origin_corridor_b_label,
                ),
                trunk_b_set,
                trunk_a_set,
                True,
                "b",
            ),
        ]
    else:
        label = (
            corridor_swap_label(
                corridor_a_assigned_set,
                corridor_b_assigned_set,
                origin_corridor_a_label,
                origin_corridor_b_label,
            )
            if corridor_scenario_active
            else "today's actual routing"
        )
        scenario_defs = [
            ScenarioDef(
                label,
                corridor_a_assigned_set,
                corridor_b_assigned_set,
                corridor_scenario_active,
                None,
            )
        ]
    show_label = len(scenario_defs) > 1

    stations_by_id = Station.load_complexes(stations)
    boundary_lat = stations_by_id[boundary_complex_id].lat
    boundary_name = stations_by_id[boundary_complex_id].name
    print(
        f"Boundary: {boundary_name} (id {boundary_complex_id}), lat {boundary_lat:.6f}"
    )
    print(f"Day filter: {days_list if days_list else 'all days'}")
    print(f"Route universe: {sorted(routes_set)}")

    def side_ok(lat: float, side: str) -> bool:
        if side == "either":
            return True
        return lat < boundary_lat if side == "south" else lat > boundary_lat

    origin_ids = [
        s.complex_id
        for s in stations_by_id.values()
        if (s.routes & routes_set) and side_ok(s.lat, origin_side)
    ]
    origin_ids.sort()
    print(f"\nOrigin stations ({len(origin_ids)}):")
    for cid in origin_ids:
        s = stations_by_id[cid]
        print(f"  {cid:>4}  {s.name}  routes={sorted(s.routes)}")

    con = duckdb.connect()
    day_filter_sql = (
        "TRUE"
        if not days_list
        else '"Day of Week" IN (' + ", ".join(f"'{d}'" for d in days_list) + ")"
    )
    origin_filter_sql = (
        '"Origin Station Complex ID" IN (' + ", ".join(str(i) for i in origin_ids) + ")"
    )

    n_days_query = f"""
        SELECT COUNT(DISTINCT CAST(Timestamp AS DATE))
        FROM '{parquet}'
        WHERE {day_filter_sql}
    """
    n_days_result: tuple[int] | None = con.execute(n_days_query).fetchone()
    assert n_days_result is not None, "aggregate query always returns exactly one row"
    (n_distinct_days,) = n_days_result

    # "riders" throughout is average weekday (or whichever day-type) ridership,
    # i.e. the sum over all matching days divided by the number of distinct
    # matching days -- not a multi-day total.
    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM '{parquet}'
        WHERE {day_filter_sql} AND {origin_filter_sql}
        GROUP BY 1, 2
    """
    pairs: list[tuple[int, int, float]] = con.execute(pairs_query).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter"
    )

    # Scope to trips that actually cross the boundary (dest on the far side,
    # or at the boundary complex itself unless excluded). Scenario-independent
    # (real geography only), so computed once and reused across scenarios.
    scoped = []
    for origin_id, dest_id, riders in pairs:
        dest = stations_by_id.get(dest_id)
        if dest is None:
            continue
        at_boundary = dest_id == boundary_complex_id and not exclude_boundary_dest
        if not at_boundary and not side_ok(dest.lat, dest_side):
            continue
        scoped.append((origin_id, dest_id, riders))

    total_riders = sum(r for _, _, r in scoped)

    individual_stations = Station.load_individuals(stations_individual)
    points_by_complex: dict[int, list[tuple[float, float]]] = {}
    for s in individual_stations:
        points_by_complex.setdefault(s.complex_id, []).append((s.lat, s.lon))

    def dest_points(dest: Station) -> list[tuple[float, float]]:
        return points_by_complex.get(dest.complex_id, [(dest.lat, dest.lon)])

    # Candidate points for the nearest-other-trunk search, system-wide (not
    # restricted to any borough): straight-line distance is already the
    # approximation this whole script uses for "close" everywhere else, so
    # there's no reason to special-case borough boundaries here too.
    trunk_a_points = [
        (s.lat, s.lon) for s in individual_stations if s.routes & trunk_a_set
    ]
    trunk_b_points = [
        (s.lat, s.lon) for s in individual_stations if s.routes & trunk_b_set
    ]

    # Under a corridor scenario, "close" is about walking to whichever trunk
    # an origin's own corridor got assigned -- not to trunk_a/trunk_b as a
    # fixed pair -- so cache point sets per distinct assigned-route-set
    # instead of hardcoding just two. Shared across scenarios: route sets
    # repeat (e.g. corridor A's assignment in one scenario is corridor B's in
    # the other), so the cache pays off across scenario runs too.
    assigned_points_cache: dict[frozenset[str], list[tuple[float, float]]] = {}

    def assigned_points(assigned_routes: set[str]) -> list[tuple[float, float]]:
        key = frozenset(assigned_routes)
        if key not in assigned_points_cache:
            assigned_points_cache[key] = [
                (s.lat, s.lon)
                for s in individual_stations
                if s.routes & assigned_routes
            ]
        return assigned_points_cache[key]

    def min_dist_to_points(
        points: list[tuple[float, float]], candidates: list[tuple[float, float]]
    ) -> float | None:
        if not candidates:
            return None
        return min(
            haversine_m(lat, lon, clat, clon)
            for lat, lon in points
            for clat, clon in candidates
        )

    results: list[ScenarioResult] = []
    for sdef in scenario_defs:
        result = run_scenario(
            label=sdef.label,
            scoped=scoped,
            total_riders=total_riders,
            stations_by_id=stations_by_id,
            origin_ids=origin_ids,
            routes_set=routes_set,
            primary_routes_set=primary_routes_set,
            trunk_a_set=trunk_a_set,
            trunk_b_set=trunk_b_set,
            trunk_a_points=trunk_a_points,
            trunk_b_points=trunk_b_points,
            assigned_points=assigned_points,
            dest_points=dest_points,
            min_dist_to_points=min_dist_to_points,
            close_threshold_m=close_threshold_m,
            origin_corridor_a_routes_set=origin_corridor_a_routes_set,
            origin_corridor_b_routes_set=origin_corridor_b_routes_set,
            origin_corridor_a_label=origin_corridor_a_label,
            origin_corridor_b_label=origin_corridor_b_label,
            corridor_a_assigned_set=sdef.corridor_a_assigned_set,
            corridor_b_assigned_set=sdef.corridor_b_assigned_set,
            corridor_scenario_active=sdef.active,
            verbose=not show_label,
        )
        result.print_headline(
            show_label=show_label,
            day_type=day_type,
            dest_side=dest_side,
            trunk_a_label=trunk_a_label,
            trunk_b_label=trunk_b_label,
            close_threshold_m=close_threshold_m,
        )
        if not show_label:
            result.print_details(stations_by_id, origin_ids)
        results.append(result)

    if show_label:
        print_scenario_comparison(results, day_type)

    csv_paths: list[Path | None] = [
        None
        if csv_out is None
        else (csv_out if sdef.suffix is None else suffixed_path(csv_out, sdef.suffix))
        for sdef in scenario_defs
    ]

    if csv_out:
        for path, result in zip(csv_paths, results, strict=True):
            assert path is not None
            write_csv(path, result.rows)

    if markdown_out:
        sections = [
            result.render_markdown(
                show_label=show_label,
                boundary_name=boundary_name,
                day_type=day_type,
                n_distinct_days=n_distinct_days,
                routes_set=routes_set,
                origin_side=origin_side,
                dest_side=dest_side,
                trunk_a_label=trunk_a_label,
                trunk_b_label=trunk_b_label,
                close_threshold_m=close_threshold_m,
                top_n=top_n,
                csv_out=path,
            )
            for result, path in zip(results, csv_paths, strict=True)
        ]
        if show_label:
            sections = [render_scenario_comparison(results, day_type), *sections]
        markdown_out.write_text("\n---\n\n".join(sections))
        print(f"\nWrote markdown report to {markdown_out}")


if __name__ == "__main__":
    app()
