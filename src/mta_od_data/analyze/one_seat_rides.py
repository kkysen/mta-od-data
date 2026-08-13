import csv
import shlex
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from datetime import date
from functools import cache
from pathlib import Path
from typing import Annotated, Literal

import duckdb
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import (
    DAY_TYPE_PRESETS,
    DayType,
    Station,
    haversine_m,
)

app = Typer()


def prefer_primary(
    routes: frozenset[str], primary_routes: frozenset[str]
) -> frozenset[str]:
    """A primary/express route beats a non-primary/local one (e.g. R)
    when both are available: a rider with the choice just takes the express,
    so a merely-present local isn't worth listing alongside it.
    Falls back to the full set when there's no primary route in it at all."""
    return (routes & primary_routes) or routes


@dataclass(slots=True, frozen=True)
class PairRow:
    origin_id: int
    origin_name: str
    origin_routes: str
    dest_id: int
    dest_name: str
    dest_routes: str
    riders: float
    one_seat: bool
    close: bool
    dist_m: float
    # The specific station `dist_m` was measured to (on the origin's own
    # effective corridor) -- None for `1-seat` rows: there's no walk to
    # name, since the classification already proves `dist_m` is 0.
    near_station: str | None


@dataclass(slots=True)
class DestStats:
    name: str
    total: float = 0.0
    one_seat: float = 0.0
    # `1-seat` rows are always close/0m by construction (see `run_scenario`),
    # so only `xfer` rows carry any real close/dist signal worth tracking.
    many_seat_classified: float = 0.0
    many_seat_close: float = 0.0
    many_seat_dist_weighted: float = 0.0

    @property
    def one_seat_pct(self) -> float:
        return 100 * self.one_seat / self.total

    @property
    def many_seat_close_pct(self) -> float | None:
        return (
            100 * self.many_seat_close / self.many_seat_classified
            if self.many_seat_classified
            else None
        )

    @property
    def many_seat_avg_dist_m(self) -> float | None:
        return (
            self.many_seat_dist_weighted / self.many_seat_classified
            if self.many_seat_classified
            else None
        )


@dataclass(slots=True, frozen=True)
class ScenarioResult:
    label: str
    corridor_scenario_active: bool
    corridor_scenario_note: str | None
    total_riders: float
    one_seat_riders: float
    classified_many_seat_riders: float
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
    def close_one_seat_pct(self) -> float:
        """Of the riders without a direct one-seat ride, not of total
        ridership -- matches the "Close one-seat rides" headline bullet."""
        return (
            100 * self.close_one_seat_riders / self.classified_many_seat_riders
            if self.classified_many_seat_riders
            else float("nan")
        )

    @property
    def effective_one_seat_pct(self) -> float:
        return (
            100 * self.effective_one_seat_riders / self.total_riders
            if self.total_riders
            else float("nan")
        )

    def print_headline(
        self,
        *,
        show_label: bool,
        day_type: DayType,
        dest_side: str,
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

        if self.classified_many_seat_riders:
            pct = 100 * self.close_one_seat_riders / self.classified_many_seat_riders
            print(
                f"Close one-seat (within {close_threshold_m:.0f}m instead): "
                f"{self.close_one_seat_riders:,.0f} of "
                f"{self.classified_many_seat_riders:,.0f} riders without a "
                f"direct one-seat ride ({pct:.1f}%)"
            )
        if self.total_riders:
            print(
                f"Effective one-seat (direct + close): "
                f"{self.effective_one_seat_riders:,.0f} "
                f"({100 * self.effective_one_seat_riders / self.total_riders:.1f}%)"
            )

    def print_details(
        self,
        stations_by_id: dict[int, Station],
        origin_ids: list[int],
    ) -> None:
        print("\n=== Per-origin-station breakdown (avg weekday riders) ===")
        for cid in origin_ids:
            name = stations_by_id[cid].display()
            total, one_seat = self.per_origin[cid]
            pct = 100 * one_seat / total if total else float("nan")
            print(f"  {name:<45} total={total:>9,.0f}  one-seat={pct:5.1f}%")

        print(
            "\n=== Per-destination-station breakdown "
            "(avg weekday riders, sorted by total) ==="
        )

        def dest_total(d: DestStats) -> float:
            return d.total

        for d in sorted(self.dest_stats.values(), key=dest_total, reverse=True):
            pct = 100 * d.one_seat / d.total if d.total else float("nan")
            print(f"  {d.name:<55} total={d.total:>9,.0f}  one-seat={pct:5.1f}%")

    def render_markdown(
        self,
        *,
        show_label: bool,
        day_type: DayType,
        close_threshold_m: float,
        top_n: int,
        csv_out: Path | None,
    ) -> str:
        # Nested one level deeper under the document's own `#` title when
        # there's more than one scenario, to keep the document outline
        # correct instead of repeating `##` for every scenario's subsections.
        h2 = "###" if show_label else "##"
        lines: list[str] = []
        if show_label:
            lines.append(f"## {self.label}")
            lines.append("")
        if self.corridor_scenario_note:
            lines.append(self.corridor_scenario_note)
            lines.append("")

        # Total/direct/close/effective one-seat are already the comparison
        # table's own columns when there's more than one scenario --
        # restating them here would just repeat those same numbers under
        # every section, so keep them only when there's no such table to
        # refer back to.
        headline: list[str] = []
        if not show_label:
            headline.append(f"- **Total: {self.total_riders:,.0f} riders/{day_type}**")
            if self.total_riders:
                one_seat_pct = 100 * self.one_seat_riders / self.total_riders
                headline.append(
                    f"- **One-seat rides (no transfer): {one_seat_pct:.1f}%** "
                    f"({self.one_seat_riders:,.0f}/{day_type})"
                )
        if not show_label and self.classified_many_seat_riders:
            close_pct = (
                100 * self.close_one_seat_riders / self.classified_many_seat_riders
            )
            if self.corridor_scenario_active:
                scope_note = "under this scenario "
                own_routes_desc = "their own corridor's assigned trunk"
            else:
                scope_note = ""
                own_routes_desc = "one of their origin's own routes"
            headline.append(
                f"- **Close one-seat rides: {close_pct:.1f}%** of the riders "
                f"without a direct one-seat ride {scope_note}"
                f"({self.close_one_seat_riders:,.0f} of "
                f"{self.classified_many_seat_riders:,.0f}) are within "
                f"{close_threshold_m:.0f}m of a station on {own_routes_desc} -- "
                f"i.e. no train change, just a short walk at the end to reach "
                f"their actual destination."
            )
        if not show_label and self.total_riders:
            effective_pct = 100 * self.effective_one_seat_riders / self.total_riders
            scenario_note = (
                " under this scenario" if self.corridor_scenario_active else ""
            )
            headline.append(
                f"- **Effective one-seat rides (direct + close): "
                f"{effective_pct:.1f}%** ({self.effective_one_seat_riders:,.0f}/"
                f"{day_type}) -- direct one-seat riders plus the close one-seat "
                f"riders above, i.e. riders who wouldn't feel a materially worse "
                f"trip{scenario_note}."
            )
        if headline:
            lines.append(f"{h2} Headline numbers")
            lines.append("")
            lines.extend(headline)
            lines.append("")

        lines.append(f"{h2} Top {top_n} origin/destination pairs")
        lines.append("")
        lines.append(
            "| # | Riders | % Total | % 1-Seat | Type | Close? | Dist "
            "| Origin → Destination | 1-Seat Destination |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")

        def pair_riders(r: PairRow) -> float:
            return r.riders

        top_pairs = sorted(self.rows, key=pair_riders, reverse=True)[:top_n]
        for i, r in enumerate(top_pairs, start=1):
            pct_total = (
                100 * r.riders / self.total_riders
                if self.total_riders
                else float("nan")
            )
            pct_one_seat_str = ""
            if r.one_seat and self.one_seat_riders:
                pct_one_seat_str = f"{100 * r.riders / self.one_seat_riders:.2f}%"
            type_str = "1-seat" if r.one_seat else "xfer"
            close_str = "close" if r.close else "far"
            dist_str = f"{r.dist_m:.0f}m"
            near_station_str = r.near_station if r.near_station else ""
            lines.append(
                f"| {i} | {r.riders:,.0f} | {pct_total:.2f}% | {pct_one_seat_str} | "
                f"{type_str} | {close_str} | {dist_str} | "
                f"{r.origin_name} → {r.dest_name} | {near_station_str} |"
            )
        lines.append("")

        lines.append(
            f"{h2} Top {top_n} destination stations, summed across all origins"
        )
        lines.append("")
        lines.append(
            "Sorted by each destination's one-seat ridership (i.e. its share of the "
            f"{self.one_seat_riders:,.0f}/{day_type} one-seat total)."
        )
        lines.append("")
        lines.append(
            "| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- |")

        def dest_one_seat(d: DestStats) -> float:
            return d.one_seat

        top_dests = sorted(self.dest_stats.values(), key=dest_one_seat, reverse=True)[
            :top_n
        ]
        for d in top_dests:
            pct_all_one_seat = (
                100 * d.one_seat / self.one_seat_riders
                if self.one_seat_riders
                else float("nan")
            )
            # `1-seat` rows are always close/0m by construction, so this
            # table's "Close?"/"Dist" only carry a real signal from `xfer`
            # rows -- scoped to that destination's classified `xfer` pairs,
            # matching the per-pair table above.
            close_pct = d.many_seat_close_pct
            close_str = "" if close_pct is None else f"{close_pct:.0f}%"
            avg_dist = d.many_seat_avg_dist_m
            dist_str = "" if avg_dist is None else f"{avg_dist:.0f}m"
            lines.append(
                f"| {d.total:,.0f} | {d.one_seat_pct:.1f}% | {pct_all_one_seat:.2f}% | "
                f"{close_str} | {dist_str} | {d.name} |"
            )
        lines.append("")

        if csv_out:
            lines.append(
                f"_Full row-level detail (every origin/destination pair, not just "
                f"the top {top_n}): `{csv_out}`._"
            )
            lines.append("")
        return "\n".join(lines)


@dataclass(slots=True, frozen=True)
class ScenarioDef:
    label: str
    corridor_a_assigned_set: frozenset[str]
    corridor_b_assigned_set: frozenset[str]
    active: bool
    # Filename suffix for per-scenario CSV output; None means "write to the
    # given path unchanged" (only used when there's exactly one scenario, so
    # single-scenario invocations keep their exact historical filenames).
    suffix: str | None


def parse_route_set(s: str) -> frozenset[str]:
    return frozenset(r.strip() for r in s.split(",") if r.strip())


def classify_one_seat(
    origin_routes: frozenset[str],
    dest_routes: frozenset[str],
    routes: frozenset[str],
    primary_routes: frozenset[str],
) -> tuple[bool, frozenset[str]]:
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
    corridor_a_routes: frozenset[str],
    corridor_b_routes: frozenset[str],
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
    routes_set: frozenset[str],
    primary_routes_set: frozenset[str],
    min_dist_to_corridor: Callable[[Station, frozenset[str]], tuple[float, Station]],
    cached_display: Callable[[Station, frozenset[str]], str],
    origin_express_partners: dict[int, frozenset[str]],
    close_threshold_m: float,
    origin_corridor_a_routes_set: frozenset[str],
    origin_corridor_b_routes_set: frozenset[str],
    origin_corridor_a_label: str,
    origin_corridor_b_label: str,
    corridor_a_assigned_set: frozenset[str],
    corridor_b_assigned_set: frozenset[str],
    corridor_scenario_active: bool,
    verbose: bool,
) -> ScenarioResult:
    # Effective routes used for one-seat classification at each origin. Under
    # a corridor scenario, this replaces an origin's real current *primary*
    # routes (the ones that actually interline at the junction) with whichever
    # primary routes the scenario assigns to its physical corridor -- a
    # station that touches both corridors (e.g. a shared terminal) keeps
    # access to both assigned route sets, since no DeKalb-only deinterlining
    # scenario changes what serves it. Any real route the station already has
    # that *doesn't* interline (e.g. R, which never crosses DeKalb) is kept
    # as-is regardless of scenario -- deinterlining the junction can't move a
    # route that never used it.
    effective_origin_routes: dict[int, frozenset[str]] = {}
    if verbose:
        print(f"\nCorridor assignment (scenario active: {corridor_scenario_active}):")
    for cid in origin_ids:
        s = stations_by_id[cid]
        in_a = bool(s.routes & origin_corridor_a_routes_set)
        in_b = bool(s.routes & origin_corridor_b_routes_set)
        corridor_tag = "a+b" if in_a and in_b else "a" if in_a else "b" if in_b else "?"
        non_reassignable_routes = s.routes - primary_routes_set
        if not corridor_scenario_active:
            effective_origin_routes[cid] = s.routes
        elif in_a and in_b:
            effective_origin_routes[cid] = non_reassignable_routes | (
                (corridor_a_assigned_set | corridor_b_assigned_set) & primary_routes_set
            )
        elif in_a:
            effective_origin_routes[cid] = non_reassignable_routes | (
                corridor_a_assigned_set & primary_routes_set
            )
        elif in_b:
            effective_origin_routes[cid] = non_reassignable_routes | (
                corridor_b_assigned_set & primary_routes_set
            )
        else:
            effective_origin_routes[cid] = s.routes
            if corridor_scenario_active:
                print(
                    f"  warning: {s.display()} matches neither "
                    f"--origin-corridor-a-routes nor --origin-corridor-b-routes; "
                    f"leaving its real routes unscoped"
                )
        if verbose:
            print(
                f"  {cid:>4}  {s.display():<40}  corridor={corridor_tag:<3}  "
                f"effective_routes={sorted(effective_origin_routes[cid])}"
            )

    one_seat_riders = 0.0
    classified_many_seat_riders = 0.0
    close_one_seat_riders = 0.0

    rows: list[PairRow] = []
    # Which of a destination's routes were actually applicable across all
    # origins, for the aggregate per-destination table -- the same per-row
    # narrowing as `dest_name` (a `1-seat` row's `shared` route(s), or a
    # close `xfer` row's assumed express transfer), unioned. A destination
    # with no such rows at all is left out here and falls back to its full
    # route list when the table is built below.
    dest_route_union: dict[int, set[str]] = {}
    for origin_id, dest_id, riders in scoped:
        origin = stations_by_id[origin_id]
        # Guaranteed present: `scoped` only ever contains destinations that
        # resolved against `stations_by_id` (see its construction above,
        # which errors out immediately otherwise).
        dest = stations_by_id[dest_id]
        dest_routes = dest.routes
        is_one_seat, shared = classify_one_seat(
            effective_origin_routes[origin_id],
            dest_routes,
            routes_set,
            primary_routes_set,
        )
        if is_one_seat:
            one_seat_riders += riders

        near_station: Station | None = None
        xfer_applicable_routes: frozenset[str] | None = None
        if not is_one_seat:
            # is_one_seat already reflects this scenario's effective routing
            # (real current routes in baseline mode, the scenario's assigned
            # routes otherwise), so a one-seat rider here already has a
            # direct train -- no walk to evaluate. The riders worth asking
            # about are the ones who DON'T connect one-seat: how far would
            # they need to walk to reach a station on a route their own
            # corridor actually has (today's real routes, or the scenario's
            # assigned routes)? If it's close, that's a "close one-seat ride"
            # (get off/board a short walk away, no train change), not a
            # transfer.
            dist_m, near_station = min_dist_to_corridor(
                dest,
                # Scoped to --routes: effective_origin_routes can carry real
                # routes far outside this analysis (e.g. a station's F/G
                # service alongside its R), and without this filter those
                # would credit "close" via a line that has nothing to do with
                # the junction being analyzed.
                effective_origin_routes[origin_id] & routes_set,
            )
            close = dist_m <= close_threshold_m
            if dist_m == 0.0:
                # The origin's own assigned route stops right at this
                # destination (not just nearby), so there's no real transfer
                # happening -- the rider is exiting here, not changing
                # platforms, so which specific platform they land on doesn't
                # matter. What matters is that a non-primary route (e.g. R)
                # is slower than an express, so a rider with an express
                # option available on their own physical line (e.g. R's 4th
                # Av line also carries D and N) is assumed to have already
                # ridden that instead. A positive `dist_m` means an actual
                # transfer to a *different* nearby station instead -- see
                # the fallback below, which covers that case generically.
                xfer_applicable_routes = (
                    origin_express_partners.get(origin_id, frozenset()) & dest_routes
                )
            classified_many_seat_riders += riders
            if close:
                close_one_seat_riders += riders
        else:
            # The destination is a Complex ID in the source data, not a
            # specific platform -- so we have no way to tell which platform
            # of a merged complex a rider actually used. `is_one_seat` means
            # the origin's effective route (real routes in baseline, the
            # scenario's assigned routes otherwise) already stops somewhere
            # in this same complex, which is the rider's real historical
            # destination either way -- trivially close, no walk to model.
            # Same calculation in every mode: unlike the `xfer` branch above,
            # there's no candidate-point search to run, since a one-seat
            # classification already proves the distance is 0.
            close, dist_m = True, 0.0

        if is_one_seat:
            # A one-seat ride's `shared` route(s) are the one(s) actually
            # ridden, so they pin down which physical platform of a merged
            # complex the rider lands on -- show just that, not every route
            # in the complex (most of which may be on a different platform
            # the rider never sees). Applies to both ends, since it's the
            # same ride either way. An `xfer` ride's arrival route isn't in
            # the data at all, so it contributes no evidence either way (not
            # even the full list -- that would swamp the one-seat signal,
            # since almost every destination has some xfer riders).
            ridden_routes = prefer_primary(shared, primary_routes_set)
            dest_route_union.setdefault(dest_id, set()).update(ridden_routes)
            dest_name = cached_display(dest, ridden_routes)
            origin_name = cached_display(origin, ridden_routes)
        elif xfer_applicable_routes:
            dest_route_union.setdefault(dest_id, set()).update(xfer_applicable_routes)
            dest_name = cached_display(dest, xfer_applicable_routes)
            origin_name = cached_display(
                origin, effective_origin_routes[origin_id] & routes_set
            )
        else:
            # No specific same-complex route to assume (see `dist_m == 0.0`
            # above). Either way, a transfer is needed -- to whichever of
            # the destination's own routes are in scope, preferring a
            # primary/express one the same as everywhere else. (By
            # construction none of these can be routes the origin's own
            # corridor already has -- that would have made it a `1-seat`
            # row instead -- so this is exactly "the other corridor",
            # without needing to compute that separately.) Scoped to
            # --routes, since a station can carry real service (e.g. F, G)
            # with nothing to do with this analysis, and showing it here
            # would be just as much noise as the 2,3,4,5 at Atlantic Av
            # (never part of --routes, so never a route any of these trips
            # could have used).
            dest_name = cached_display(
                dest, prefer_primary(dest.routes & routes_set, primary_routes_set)
            )
            origin_name = cached_display(
                origin, effective_origin_routes[origin_id] & routes_set
            )

        near_station_name = (
            cached_display(near_station, near_station.routes & routes_set)
            if near_station
            else None
        )
        rows.append(
            PairRow(
                origin_id=origin_id,
                origin_name=origin_name,
                origin_routes=",".join(sorted(effective_origin_routes[origin_id])),
                dest_id=dest_id,
                dest_name=dest_name,
                dest_routes=",".join(sorted(dest_routes)),
                riders=riders,
                one_seat=is_one_seat,
                close=close,
                dist_m=dist_m,
                near_station=near_station_name,
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
        # Summed across all origins, so unlike a single row's `dest_name`
        # this shows every route observed as an arrival route across all of
        # them -- not just the route(s) accounting for the last row seen.
        dest_station = stations_by_id[r.dest_id]
        arrival_routes = dest_route_union.get(r.dest_id)
        dest_display_name = (
            cached_display(dest_station, frozenset(arrival_routes))
            if arrival_routes
            else r.dest_name
        )
        d = dest_stats.setdefault(r.dest_id, DestStats(name=dest_display_name))
        d.total += r.riders
        if r.one_seat:
            d.one_seat += r.riders
        else:
            d.many_seat_classified += r.riders
            d.many_seat_dist_weighted += r.riders * r.dist_m
            if r.close:
                d.many_seat_close += r.riders

    corridor_scenario_note = None
    if corridor_scenario_active:
        corridor_a_assigned_primary = corridor_a_assigned_set & primary_routes_set
        corridor_b_assigned_primary = corridor_b_assigned_set & primary_routes_set
        corridor_scenario_note = (
            f"Deinterlining scenario: {origin_corridor_a_label} served by "
            f"{','.join(sorted(corridor_a_assigned_primary))}; "
            f"{origin_corridor_b_label} served by "
            f"{','.join(sorted(corridor_b_assigned_primary))} (each origin's "
            f"one-seat eligibility swaps in these assigned primary routes in "
            f"place of its real current primary routes; any non-primary route "
            f"it already has (e.g. R, which never crosses the junction) is "
            f"unaffected, and a station touching both corridors keeps access "
            f"to both)."
        )

    return ScenarioResult(
        label=label,
        corridor_scenario_active=corridor_scenario_active,
        corridor_scenario_note=corridor_scenario_note,
        total_riders=total_riders,
        one_seat_riders=one_seat_riders,
        classified_many_seat_riders=classified_many_seat_riders,
        close_one_seat_riders=close_one_seat_riders,
        effective_one_seat_riders=effective_one_seat_riders,
        rows=rows,
        dest_stats=dest_stats,
        per_origin=per_origin,
    )


def print_scenario_comparison(results: list[ScenarioResult], day_type: DayType) -> None:
    print(f"\n=== Scenario comparison (avg {day_type} riders) ===")
    for r in results:
        print(
            f"  {r.label:<55} total={r.total_riders:>9,.0f}  "
            f"direct={r.one_seat_riders:>8,.0f} ({r.direct_one_seat_pct:5.1f}%)  "
            f"close={r.close_one_seat_riders:>7,.0f}  "
            f"effective={r.effective_one_seat_riders:>8,.0f} "
            f"({r.effective_one_seat_pct:5.1f}%)"
        )


def render_scenario_comparison(results: list[ScenarioResult], day_type: DayType) -> str:
    lines: list[str] = []
    lines.append("## Scenario comparison")
    lines.append("")
    lines.append(
        f"Average {day_type} ridership is the same {results[0].total_riders:,.0f}/"
        f"{day_type} across every scenario below -- only how many of those "
        f"riders get a one-seat ride changes."
    )
    lines.append("")
    lines.append(
        "| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |"
    )
    lines.append("| --- | --- | --- | --- | --- |")
    for r in results:
        lines.append(
            f"| {r.label} | {r.total_riders:,.0f} | "
            f"{r.one_seat_riders:,.0f} ({r.direct_one_seat_pct:.1f}%) | "
            f"{r.close_one_seat_riders:,.0f} ({r.close_one_seat_pct:.1f}%) | "
            f"{r.effective_one_seat_riders:,.0f} ({r.effective_one_seat_pct:.1f}%) |"
        )
    lines.append("")
    return "\n".join(lines)


def render_notes(*, close_threshold_m: float) -> str:
    return "\n".join(
        [
            "## Notes on reading these tables",
            "",
            '- "Close?"/"Dist" describe distance from the destination to the '
            "nearest station on the origin's own effective corridor (real "
            "routes in baseline, the scenario's assigned routes otherwise), "
            f"thresholded at {close_threshold_m:.0f}m, for `xfer` rows -- "
            "riders without a direct one-seat ride. A close `xfer` row is a "
            "*close one-seat ride*: no train change, just a short walk to "
            "the actual destination. `1-seat` rows are always `close`/`0m`: "
            "the destination is a Complex ID in the source data, not a "
            "specific platform, so there's no way to tell which platform a "
            "rider actually used -- the effective route already stops "
            "somewhere in that same complex, the rider's real historical "
            "destination either way.",
            '- In the per-pair table (and CSV), "1-Seat Destination" names '
            "the specific station `dist_m` was measured to for a `xfer` "
            "row: the nearest station on the origin's own effective "
            "corridor -- i.e. what the destination would have had to be "
            "for this row to be a `1-seat` ride instead. Empty for `1-seat` "
            "rows (already true of the actual destination) and omitted "
            "from the per-destination table (an average across many pairs, "
            "not a single station).",
            '- In the per-destination table, "Close?"/"Dist" are '
            "ridership-weighted across that destination's classified "
            "`xfer` pairs.",
            "",
        ]
    )


@app.command()
def one_seat_rides(
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
    trunk_a_label: Annotated[str, Option()] = "6 Av express",
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
    origin_corridor_a_label: Annotated[str, Option()] = "4 Av express",
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
        Option(help="Optional: write a markdown report here"),
    ] = None,
    top_n: Annotated[
        int, Option(help="Row count for the markdown top-pairs/top-destinations tables")
    ] = 25,
) -> None:
    """Analyze one-seat-ride / deinterlining share for trips crossing a subway junction.

    Generalized so the same command can be re-run for other day types, other
    station criteria, other data extracts, and other deinterlining scenarios
    (different junction, different trunk-line pairs) just by passing flags.

    Default scenario (the one this was built for): weekday trips on B/D/N/Q
    originating south of Atlantic Av-Barclays Ctr in Brooklyn, heading toward
    Manhattan through the DeKalb Av interlining junction.

    \b
    Examples:
        # Default DeKalb scenario
        mta-od-data analyze one-seat-rides

    \b
        # Same scenario, Saturdays instead of weekdays
        mta-od-data analyze one-seat-rides --day-type saturday

    \b
        # Same scenario, against a newer data extract
        mta-od-data analyze one-seat-rides --parquet data/mta_od_2025.parquet

    \b
        # Write the RESULTS.md-style snapshot report automatically instead of
        # transcribing output by hand
        mta-od-data analyze one-seat-rides --routes B,D,N,Q,R \\
            --primary-routes B,D,N,Q --trunk-b N,Q,R \\
            --csv-out data/dekalb_weekday_pairs.csv \\
            --markdown-out src/mta_od_data/analyze/one_seat_rides.md

    \b
        # A different junction/trunk pair, e.g. hypothetically Rogers Jct area
        mta-od-data analyze one-seat-rides --boundary-complex-id <id> \\
            --routes 2,3,4,5 --trunk-a 4,5 --trunk-a-label "Lexington Av express" \\
            --trunk-b 2,3 --trunk-b-label "7 Av express"

    \b
        # Full DeKalb deinterlining: N,Q run the 4 Av express corridor,
        # B,D run Brighton (origin one-seat eligibility uses these assigned
        # routes instead of each station's real current routes)
        mta-od-data analyze one-seat-rides \\
            --corridor-a-assigned N,Q --corridor-b-assigned B,D

    \b
        # Today's actual routing plus both full B,D/N,Q corridor swaps, in
        # one invocation
        mta-od-data analyze one-seat-rides \\
            --all-corridor-scenarios \\
            --markdown-out src/mta_od_data/analyze/one_seat_rides.md
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
        parse_route_set(corridor_a_assigned) if corridor_a_assigned else frozenset()
    )
    corridor_b_assigned_set = (
        parse_route_set(corridor_b_assigned) if corridor_b_assigned else frozenset()
    )

    # Today's actual routing isn't a single corridor->trunk assignment the way
    # the deinterlined scenarios are -- interlining lets each Brooklyn corridor
    # reach *both* Manhattan trunks today (e.g. 4 Av express gets both D, to 6
    # Av express, and N, to Broadway express), which is exactly why it beats
    # either pure swap on direct one-seat rides. Label it by the real routes
    # serving each corridor instead of a trunk assignment.
    actual_routing_label = corridor_swap_label(
        origin_corridor_a_routes_set,
        origin_corridor_b_routes_set,
        origin_corridor_a_label,
        origin_corridor_b_label,
    )
    if all_corridor_scenarios:
        # Only primary routes actually interline at the junction, so only
        # they're swappable between corridors -- a non-primary route given
        # on --trunk-a/--trunk-b never moves and shouldn't be named in the
        # swap label.
        trunk_a_primary_set = trunk_a_set & primary_routes_set
        trunk_b_primary_set = trunk_b_set & primary_routes_set
        scenario_defs = [
            ScenarioDef(
                actual_routing_label, frozenset(), frozenset(), False, "actual"
            ),
            ScenarioDef(
                corridor_swap_label(
                    trunk_a_primary_set,
                    trunk_b_primary_set,
                    origin_corridor_a_label,
                    origin_corridor_b_label,
                ),
                trunk_a_primary_set,
                trunk_b_primary_set,
                True,
                "a",
            ),
            ScenarioDef(
                corridor_swap_label(
                    trunk_b_primary_set,
                    trunk_a_primary_set,
                    origin_corridor_a_label,
                    origin_corridor_b_label,
                ),
                trunk_b_primary_set,
                trunk_a_primary_set,
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
            else actual_routing_label
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

    # An origin's own routes can be entirely primary (e.g. a B/D/N/Q-only
    # station), in which case its effective routing under an active scenario
    # is *only* whatever this corridor got assigned that's also primary --
    # if that's empty, there's no station anywhere to measure a walk to for
    # such an origin. Only reachable via a CLI misconfiguration (a corridor
    # assigned routes entirely outside --primary-routes/--routes), so check
    # it here, once, instead of discovering it deep in a per-row loop.
    for sdef in scenario_defs:
        if not sdef.active:
            continue
        for corridor_letter, assigned_set in (
            ("A", sdef.corridor_a_assigned_set),
            ("B", sdef.corridor_b_assigned_set),
        ):
            if assigned_set & primary_routes_set & routes_set:
                continue
            print(
                f"error: scenario {sdef.label!r} assigns corridor "
                f"{corridor_letter} {sorted(assigned_set)}, none of which is "
                f"in both --routes {sorted(routes_set)} and --primary-routes "
                f"{sorted(primary_routes_set)} -- an origin with only "
                "primary routes of its own would have no station on this "
                "corridor to measure a walk to",
                file=sys.stderr,
            )
            raise SystemExit(1)

    stations_by_id = Station.load_complexes(stations)
    boundary_lat = stations_by_id[boundary_complex_id].loc.lat
    boundary_station = stations_by_id[boundary_complex_id]
    boundary_name = boundary_station.display(boundary_station.routes & routes_set)
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
        if (s.routes & routes_set) and side_ok(s.loc.lat, origin_side)
    ]
    origin_ids.sort()
    print(f"\nOrigin stations ({len(origin_ids)}):")
    for cid in origin_ids:
        s = stations_by_id[cid]
        print(f"  {cid:>4}  {s.name}  routes={sorted(s.routes)}")

    con = duckdb.connect()
    day_params: list[str] = list(days_list) if days_list else []
    day_filter_sql = (
        "TRUE"
        if not days_list
        else '"Day of Week" IN (' + ", ".join("?" for _ in days_list) + ")"
    )
    origin_filter_sql = (
        '"Origin Station Complex ID" IN (' + ", ".join(str(i) for i in origin_ids) + ")"
    )

    n_days_query = f"""
        SELECT COUNT(DISTINCT CAST(Timestamp AS DATE)),
               MIN(CAST(Timestamp AS DATE)),
               MAX(CAST(Timestamp AS DATE))
        FROM read_parquet(?)
        WHERE {day_filter_sql}
    """
    n_days_result: tuple[int, date, date] | None = con.execute(
        n_days_query, [str(parquet), *day_params]
    ).fetchone()
    assert n_days_result is not None, "aggregate query always returns exactly one row"
    n_distinct_days, min_date, max_date = n_days_result

    # "riders" throughout is average weekday (or whichever day-type) ridership,
    # i.e. the sum over all matching days divided by the number of distinct
    # matching days -- not a multi-day total.
    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM read_parquet(?)
        WHERE {day_filter_sql} AND {origin_filter_sql}
        GROUP BY 1, 2
    """
    pairs: list[tuple[int, int, float]] = con.execute(
        pairs_query, [str(parquet), *day_params]
    ).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter "
        f"({min_date} to {max_date})"
    )

    # Scope to trips that actually cross the boundary (dest on the far side,
    # or at the boundary complex itself unless excluded). Scenario-independent
    # (real geography only), so computed once and reused across scenarios.
    scoped = []
    for origin_id, dest_id, riders in pairs:
        dest = stations_by_id.get(dest_id)
        if dest is None:
            # The OD data references a station complex the station
            # reference CSV doesn't have -- almost certainly a stale
            # --stations file against a newer OD extract, not something to
            # silently drop and undercount.
            print(
                f"error: destination complex {dest_id} not found in "
                f"{stations} -- refetch station reference data with "
                "`mta-od-data prepare --force-stations`",
                file=sys.stderr,
            )
            raise SystemExit(1)
        at_boundary = dest_id == boundary_complex_id and not exclude_boundary_dest
        if not at_boundary and not side_ok(dest.loc.lat, dest_side):
            continue
        scoped.append((origin_id, dest_id, riders))

    total_riders = sum(r for _, _, r in scoped)

    individual_stations = Station.load_individuals(stations_individual)
    platforms_by_complex: dict[int, list[Station]] = {}
    for s in individual_stations:
        platforms_by_complex.setdefault(s.complex_id, []).append(s)

    routes_by_line: dict[str, set[str]] = {}
    for s in individual_stations:
        routes_by_line.setdefault(s.line, set()).update(s.routes)

    # For an origin with no primary route of its own (e.g. an R-only
    # station), which primary routes are assumed reachable anyway: whichever
    # primary routes run on the same physical line the origin's own
    # non-primary route does (e.g. R's 4th Av line also carries D, N). A
    # rider whose real service is slower than that is assumed to have
    # already ridden the faster one instead, wherever it also reaches the
    # destination -- see its use for close `xfer` rows below.
    origin_express_partners: dict[int, frozenset[str]] = {
        cid: frozenset(
            route
            for s in platforms_by_complex.get(cid, [])
            for route in routes_by_line.get(s.line, set()) & primary_routes_set
        )
        for cid in origin_ids
    }

    # `Coord`/`Station` are both hashable now (frozen, and every field --
    # including `Station.routes`, a `frozenset[str]` -- is itself hashable),
    # so every cache below is a plain `functools.cache` keyed on the real
    # objects involved, no manual key-building required. That's not just
    # simpler: keying on the actual `Station` is also more precise than the
    # `complex_id`-based key an earlier version of this used, which caused a
    # real bug -- a merged complex and one of its own individual per-platform
    # stations can share a `complex_id` but have a different `name` (e.g.
    # "Chambers St/WTC/Park Pl/Cortlandt St" versus its own "Cortlandt St"
    # platform), and dataclass equality on the whole `Station` already tells
    # those apart correctly, with no extra field-picking to get right.
    cached_haversine = cache(haversine_m)

    # Under a corridor scenario, "close" is about walking to whichever trunk
    # an origin's own corridor got assigned -- not to trunk_a/trunk_b as a
    # fixed pair -- so cache candidate-point sets per distinct assigned-route
    # set instead of hardcoding just two. Shared across scenarios: route sets
    # repeat (e.g. corridor A's assignment in one scenario is corridor B's in
    # the other), so the cache pays off across scenario runs too.
    @cache
    def assigned_points(assigned_routes: frozenset[str]) -> list[Station]:
        return [s for s in individual_stations if s.routes & assigned_routes]

    # (destination, assigned route set) is the entire input to a distance
    # search, and it repeats constantly across rows -- many origins share the
    # same effective routes within a scenario, the same destination shows up
    # under many different origins, and scenarios often reuse each other's
    # route assignments -- so caching here skips re-running the whole points
    # x candidates sweep for a combination already seen. But two different
    # (dest, routes) combinations can still share individual point pairs
    # (e.g. their candidate stations overlap even though the route sets
    # differ), which this alone doesn't catch -- `cached_haversine` above
    # catches that layer too. Measured on the default DeKalb scenario: 2.19M
    # raw haversine calls collapse to ~240K sweep-level cache misses, which
    # collapse further to the ~39K individual point pairs actually distinct
    # -- a combined ~56x reduction in real distance computations, with
    # results unchanged since the underlying math is identical either way.
    @cache
    def min_dist_to_corridor(
        dest: Station, assigned_routes: frozenset[str]
    ) -> tuple[float, Station]:
        candidates = assigned_points(assigned_routes)
        # `candidates` empty would mean some route in the effective set has
        # no individual station anywhere -- the CLI-level checks above rule
        # out an empty *route set*, but not a gap in stations_individual.csv
        # itself, so this stays a real (if unlikely) assertion, not dead code.
        assert candidates, "no individual station serves this route set"
        points = [s.loc for s in platforms_by_complex.get(dest.complex_id, [dest])]
        best: tuple[float, Station] | None = None
        for p in points:
            for c in candidates:
                dist_m = cached_haversine(p, c.loc)
                if best is None or dist_m < best[0]:
                    best = (dist_m, c)
        assert best is not None
        return best

    # Same redundancy pattern as the distance search, worse: every row needs
    # up to three of these (origin/dest/near-station names), and the same
    # station with the same route set recurs constantly -- a handful of busy
    # destinations (Grand Central, Times Sq, ...) account for a large share
    # of all rows. Measured on the default DeKalb scenario: 138K calls
    # collapse to ~640 distinct (station, routes) combinations, a ~216x
    # reduction.
    cached_display = cache(Station.display)

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
            min_dist_to_corridor=min_dist_to_corridor,
            cached_display=cached_display,
            origin_express_partners=origin_express_partners,
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
        # argv[0] is the installed entry point's absolute path (e.g.
        # .venv/bin/mta-od-data), not stable across machines/checkouts -- use
        # just its basename so this line stays reproducible.
        produced_by = shlex.join([Path(sys.argv[0]).name, *sys.argv[1:]])
        preamble_lines = [
            f"# {trunk_a_label}/{trunk_b_label} deinterlining: one-seat-ride "
            f"results at {boundary_name}",
            "",
            f"Scenario: average {day_type} ridership ({n_distinct_days} distinct "
            f"days in the data, {min_date} to {max_date}) on trains originating "
            f"at stations served by {','.join(sorted(routes_set))}, "
            f"{origin_side} of {boundary_name}, with destinations {dest_side} "
            f"of it (i.e. trips that cross the junction).",
            "",
            f"Produced by `{produced_by}`.",
            "",
        ]
        sections = [
            "\n".join(preamble_lines),
            *([render_scenario_comparison(results, day_type)] if show_label else []),
            *(
                result.render_markdown(
                    show_label=show_label,
                    day_type=day_type,
                    close_threshold_m=close_threshold_m,
                    top_n=top_n,
                    csv_out=path,
                )
                for result, path in zip(results, csv_paths, strict=True)
            ),
            render_notes(close_threshold_m=close_threshold_m),
        ]
        markdown_out.write_text("\n---\n\n".join(sections))
        print(f"\nWrote markdown report to {markdown_out}")
