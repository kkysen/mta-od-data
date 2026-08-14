"""Systemwide deinterlining scenario comparator.

See `deinterlining_design.md` (next to this file) for the design this
implements. Deliberately kept independent of `one_seat_rides.py` --
duplicates a couple of small helpers (`parse_route_set`, `write_csv`,
nearest-station search) rather than importing them, since the user doesn't
want that module touched until this one is proven out; reconcile the
duplication if/when the two get merged.

Unlike `one_seat_rides.py` (one latitude boundary, two named corridors
converging into two named trunks, origin-side reassignment only), this
classifies *every* origin/destination pair whose origin could plausibly
use one of `--routes` (today or under the scenario) -- no boundary, same
shape as `regional_flow.py`'s unfiltered OD-pairs query -- comparing
one-seat-ride share under today's real routes against a scenario's
route-override map.
"""

import csv
import json
import shlex
import sys
from dataclasses import asdict, dataclass, fields
from datetime import date
from functools import cache
from pathlib import Path
from typing import Annotated

import duckdb
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import DAY_TYPE_PRESETS, DayType, Station, haversine_m

app = Typer()


def parse_route_set(s: str) -> frozenset[str]:
    return frozenset(r.strip() for r in s.split(",") if r.strip())


@dataclass(slots=True, frozen=True)
class Scenario:
    """A deinterlining scenario: real routes overridden only for the
    specific stations it actually changes. `effective_routes` falls back
    to a station's real current routes for every complex ID absent from
    `overrides` -- see `deinterlining_design.md` for why this replaces
    `one_seat_rides.py`'s corridor-A/corridor-B machinery instead of
    extending it."""

    label: str
    overrides: dict[int, frozenset[str]]

    def effective_routes(self, station: Station) -> frozenset[str]:
        return self.overrides.get(station.complex_id, station.routes)


def load_scenario(path: Path, stations_by_id: dict[int, Station]) -> Scenario:
    data = json.loads(path.read_text())
    label = data.get("label", path.stem)
    overrides: dict[int, frozenset[str]] = {}
    for complex_id_str, routes in data["overrides"].items():
        complex_id = int(complex_id_str)
        if complex_id not in stations_by_id:
            print(
                f"error: scenario {path} overrides complex {complex_id}, not found "
                f"in the station reference data",
                file=sys.stderr,
            )
            raise SystemExit(1)
        overrides[complex_id] = frozenset(routes)
    return Scenario(label=label, overrides=overrides)


@dataclass(slots=True, frozen=True)
class ODPair:
    origin_id: int
    origin_name: str
    dest_id: int
    dest_name: str
    riders: float
    one_seat_current: bool
    one_seat_scenario: bool
    # Only meaningful when the matching `one_seat_*` is false: is a station
    # on the effective origin corridor (today's real one, or the
    # scenario's) within `close_threshold_m` of the destination anyway (a
    # short walk, not a real transfer)? Computed symmetrically for both
    # today and the scenario -- comparing "effective one-seat under the
    # scenario" against plain "one-seat today" (no close boost) would be
    # an apples-to-oranges headline number.
    close_current: bool
    dist_m_current: float
    near_station_current: str | None
    close_scenario: bool
    dist_m_scenario: float
    near_station_scenario: str | None


@dataclass(slots=True)
class DestStats:
    name: str
    total: float = 0.0
    one_seat_current: float = 0.0
    one_seat_scenario: float = 0.0
    close_current: float = 0.0
    close_scenario: float = 0.0


def write_csv(path: Path, rows: list[ODPair]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(ODPair)])
        writer.writeheader()
        writer.writerows(asdict(r) for r in rows)
    print(f"\nWrote {len(rows):,} rows to {path}")


@app.command()
def deinterlining(
    # Required (no default): Typer's `...`-as-default convention for
    # required Options isn't a real `str`/`Path`, which `ty`/`pyrefly` both
    # (correctly) reject -- a plain absent default is the type-correct way
    # to make a Typer parameter required, so these two come first.
    routes: Annotated[
        str,
        Option(
            help=(
                "Route universe: which routes this scenario's classification "
                "covers (e.g. A,B,C,D for a Columbus Circle scenario)"
            )
        ),
    ],
    scenario_file: Annotated[
        Path,
        Option(
            help=(
                "JSON file: {'label': str, 'overrides': {complex_id: "
                "[route, ...]}}. Only the listed complex IDs' routes change; "
                "every other station keeps its real current routes."
            )
        ),
    ],
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
    """Systemwide deinterlining scenario comparator: classify every
    origin/destination pair whose origin could plausibly use one of
    `--routes` (today or under the scenario) as one-seat or transfer,
    under both today's real routes and a scenario's route overrides.

    Unlike `one-seat-rides`, there's no latitude boundary and no
    origin-side-only corridor restriction -- a scenario can reassign which
    routes serve a *destination* station too, so this can express
    deinterlining shapes `one-seat-rides` can't (e.g. Columbus Circle's
    destination-stopping-pattern swap). Also unlike `one-seat-rides`,
    there's no primary/non-primary route distinction: any route a rider
    actually shares with their destination counts as one-seat, even a
    "slower" one -- see `deinterlining_design.md` for why.

    \b
    Examples:
        # Columbus Circle: what if A,C ran express and B,D local on CPW?
        mta-od-data analyze deinterlining --routes A,B,C,D \\
            --scenario-file \\
            src/mta_od_data/analyze/scenarios/columbus_circle_ac_express.json \\
            --markdown-out src/mta_od_data/analyze/deinterlining_columbus_circle.md
    """
    days_list = (
        [d.strip() for d in days.split(",")] if days else DAY_TYPE_PRESETS[day_type]
    )
    day_type_label = (
        "/".join(d.strip() for d in days.split(",")) if days else str(day_type)
    )
    routes_set = parse_route_set(routes)

    stations_by_id = Station.load_complexes(stations)
    scenario = load_scenario(scenario_file, stations_by_id)
    print(f"Scenario: {scenario.label} ({len(scenario.overrides)} stations overridden)")
    print(f"Route universe: {sorted(routes_set)}")
    print(f"Day filter: {days_list if days_list else 'all days'} ({day_type_label})")

    # Systemwide, but not literally every station: an origin only matters
    # if it could plausibly use one of `--routes`, today or under the
    # scenario -- otherwise its trips have nothing to do with the junction
    # being analyzed (unlike `regional_flow.py`, whose question -- does a
    # trip touch this region -- has no such natural restriction).
    origin_ids = [
        s.complex_id
        for s in stations_by_id.values()
        if (s.routes | scenario.effective_routes(s)) & routes_set
    ]
    print(f"Origin stations in scope: {len(origin_ids):,} of {len(stations_by_id):,}")

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

    individual_stations = Station.load_individuals(stations_individual)
    platforms_by_complex: dict[int, list[Station]] = {}
    for s in individual_stations:
        platforms_by_complex.setdefault(s.complex_id, []).append(s)

    # Same caching structure as `one_seat_rides.py`'s `assigned_points`/
    # `min_dist_to_corridor` -- local rather than cached at their own
    # definition since both close over `individual_stations`/
    # `platforms_by_complex`, loaded fresh per invocation.
    @cache
    def assigned_points(assigned_routes: frozenset[str]) -> list[Station]:
        return [s for s in individual_stations if s.routes & assigned_routes]

    @cache
    def min_dist_to_corridor(
        dest: Station, assigned_routes: frozenset[str]
    ) -> tuple[float, Station] | None:
        candidates = assigned_points(assigned_routes)
        if not candidates:
            # Unlike `one_seat_rides.py`, this can legitimately happen here:
            # systemwide, a scenario-effective route set might have no
            # individual-station match at all for some origin (e.g. a
            # synthetic route with no real platform data -- not used by any
            # scenario yet, but the classifier shouldn't crash if one ever
            # is).
            return None
        points = [s.loc for s in platforms_by_complex.get(dest.complex_id, [dest])]
        best: tuple[float, Station] | None = None
        for p in points:
            for c in candidates:
                dist_m = haversine_m(p, c.loc)
                if best is None or dist_m < best[0]:
                    best = (dist_m, c)
        return best

    def close_lookup(
        dest: Station, effective_origin_routes: frozenset[str]
    ) -> tuple[bool, float, str | None]:
        best = min_dist_to_corridor(dest, effective_origin_routes)
        if best is None:
            return False, 0.0, None
        dist_m, near_station = best
        close = dist_m <= close_threshold_m
        near_station_name = near_station.display(near_station.routes & routes_set)
        return close, dist_m, near_station_name

    rows: list[ODPair] = []
    total_riders = 0.0
    one_seat_current_riders = 0.0
    one_seat_scenario_riders = 0.0
    close_current_riders = 0.0
    close_scenario_riders = 0.0
    dest_stats: dict[int, DestStats] = {}
    for origin_id, dest_id, riders in pairs:
        origin = stations_by_id.get(origin_id)
        dest = stations_by_id.get(dest_id)
        if origin is None or dest is None:
            missing_id = origin_id if origin is None else dest_id
            print(
                f"error: station complex {missing_id} not found in "
                f"{stations} -- refetch station reference data with "
                "`mta-od-data prepare --force-stations`",
                file=sys.stderr,
            )
            raise SystemExit(1)

        current_origin_routes = origin.routes & routes_set
        one_seat_current = bool(current_origin_routes & dest.routes & routes_set)
        effective_origin_routes = scenario.effective_routes(origin) & routes_set
        effective_dest_routes = scenario.effective_routes(dest) & routes_set
        one_seat_scenario = bool(effective_origin_routes & effective_dest_routes)

        total_riders += riders

        # Computed symmetrically for both today and the scenario -- see
        # `ODPair.close_current`'s docstring comment for why. A `False`/
        # `0.0`/`None` no-op result when the pair is already one-seat (no
        # walk to evaluate) matches `one_seat_rides.py`'s `close, dist_m =
        # True, 0.0` convention for that case, just inverted here since
        # `close` at 1-seat distance 0 isn't a meaningful "close transfer".
        if one_seat_current:
            one_seat_current_riders += riders
            close_current, dist_m_current, near_station_current_name = (
                False,
                0.0,
                None,
            )
        else:
            close_current, dist_m_current, near_station_current_name = close_lookup(
                dest, current_origin_routes
            )
            if close_current:
                close_current_riders += riders

        if one_seat_scenario:
            one_seat_scenario_riders += riders
            close_scenario, dist_m_scenario, near_station_scenario_name = (
                False,
                0.0,
                None,
            )
        else:
            close_scenario, dist_m_scenario, near_station_scenario_name = close_lookup(
                dest, effective_origin_routes
            )
            if close_scenario:
                close_scenario_riders += riders

        rows.append(
            ODPair(
                origin_id=origin_id,
                origin_name=origin.display(origin.routes & routes_set),
                dest_id=dest_id,
                dest_name=dest.display(dest.routes & routes_set),
                riders=riders,
                one_seat_current=one_seat_current,
                one_seat_scenario=one_seat_scenario,
                close_current=close_current,
                dist_m_current=dist_m_current,
                near_station_current=near_station_current_name,
                close_scenario=close_scenario,
                dist_m_scenario=dist_m_scenario,
                near_station_scenario=near_station_scenario_name,
            )
        )

        d = dest_stats.setdefault(dest_id, DestStats(name=dest.display(dest.routes)))
        d.total += riders
        if one_seat_current:
            d.one_seat_current += riders
        elif close_current:
            d.close_current += riders
        if one_seat_scenario:
            d.one_seat_scenario += riders
        elif close_scenario:
            d.close_scenario += riders

    effective_current_riders = one_seat_current_riders + close_current_riders
    effective_scenario_riders = one_seat_scenario_riders + close_scenario_riders

    def pct(riders: float) -> float:
        return 100 * riders / total_riders if total_riders else float("nan")

    print(f"\n=== Scenario: {scenario.label} ===")
    print(f"Average {day_type_label} ridership: {total_riders:,.0f}")
    print(
        f"One-seat today:                    {one_seat_current_riders:>12,.0f} "
        f"({pct(one_seat_current_riders):5.1f}%)"
    )
    print(
        f"Close one-seat today:               {close_current_riders:>12,.0f} "
        f"({pct(close_current_riders):5.1f}%)"
    )
    print(
        f"Effective one-seat today:          {effective_current_riders:>12,.0f} "
        f"({pct(effective_current_riders):5.1f}%)"
    )
    print(
        f"One-seat under scenario:           {one_seat_scenario_riders:>12,.0f} "
        f"({pct(one_seat_scenario_riders):5.1f}%)"
    )
    print(
        f"Close one-seat under scenario:      {close_scenario_riders:>12,.0f} "
        f"({pct(close_scenario_riders):5.1f}%)"
    )
    print(
        f"Effective one-seat under scenario: {effective_scenario_riders:>12,.0f} "
        f"({pct(effective_scenario_riders):5.1f}%)"
    )

    if csv_out:
        write_csv(csv_out, rows)

    if markdown_out:
        produced_by = shlex.join([Path(sys.argv[0]).name, *sys.argv[1:]])
        lines: list[str] = [
            f"# Deinterlining scenario: {scenario.label}",
            "",
            f"Scenario: average {day_type_label} ridership ({n_distinct_days} "
            f"distinct days in the data, {min_date} to {max_date}), every "
            f"origin/destination pair whose origin could plausibly use "
            f"{','.join(sorted(routes_set))}.",
            "",
            f"Produced by `{produced_by}`.",
            "",
            "## Headline numbers",
            "",
            f"- **Total: {total_riders:,.0f} riders/{day_type_label}**",
            f"- **One-seat today: {pct(one_seat_current_riders):.1f}%** "
            f"({one_seat_current_riders:,.0f}/{day_type_label})",
            f"- **Effective one-seat today: "
            f"{pct(effective_current_riders):.1f}%** "
            f"({effective_current_riders:,.0f}/{day_type_label}) -- direct "
            f"one-seat plus riders within {close_threshold_m:.0f}m of a "
            f"station on their own real corridor",
            f"- **One-seat under scenario: {pct(one_seat_scenario_riders):.1f}%** "
            f"({one_seat_scenario_riders:,.0f}/{day_type_label})",
            f"- **Effective one-seat under scenario: "
            f"{pct(effective_scenario_riders):.1f}%** "
            f"({effective_scenario_riders:,.0f}/{day_type_label}) -- direct "
            f"one-seat plus riders within {close_threshold_m:.0f}m of a "
            f"station on the scenario-effective origin corridor",
            "",
            f"## Top {top_n} origin/destination pairs",
            "",
            "| # | Riders | % Total | Today | Today Close? | Today Dist | "
            "Scenario | Scenario Close? | Scenario Dist | Origin → Destination |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]

        def pair_riders(r: ODPair) -> float:
            return r.riders

        for i, r in enumerate(sorted(rows, key=pair_riders, reverse=True)[:top_n], 1):
            today_str = "1-seat" if r.one_seat_current else "xfer"
            today_close_str = (
                "" if r.one_seat_current else ("close" if r.close_current else "far")
            )
            today_dist_str = "" if r.one_seat_current else f"{r.dist_m_current:.0f}m"
            scenario_str = "1-seat" if r.one_seat_scenario else "xfer"
            scenario_close_str = (
                "" if r.one_seat_scenario else ("close" if r.close_scenario else "far")
            )
            scenario_dist_str = (
                "" if r.one_seat_scenario else f"{r.dist_m_scenario:.0f}m"
            )
            lines.append(
                f"| {i} | {r.riders:,.0f} | {pct(r.riders):.2f}% | {today_str} | "
                f"{today_close_str} | {today_dist_str} | {scenario_str} | "
                f"{scenario_close_str} | {scenario_dist_str} | "
                f"{r.origin_name} → {r.dest_name} |"
            )
        lines.append("")

        lines.append(f"## Top {top_n} destination stations, summed across all origins")
        lines.append("")
        lines.append(
            "| Riders | 1-Seat % Today | Effective % Today | 1-Seat % Scenario | "
            "Effective % Scenario | Destination |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- |")

        def dest_total(d: DestStats) -> float:
            return d.total

        for d in sorted(dest_stats.values(), key=dest_total, reverse=True)[:top_n]:
            current_pct = (
                100 * d.one_seat_current / d.total if d.total else float("nan")
            )
            current_effective_pct = (
                100 * (d.one_seat_current + d.close_current) / d.total
                if d.total
                else float("nan")
            )
            scenario_pct = (
                100 * d.one_seat_scenario / d.total if d.total else float("nan")
            )
            scenario_effective_pct = (
                100 * (d.one_seat_scenario + d.close_scenario) / d.total
                if d.total
                else float("nan")
            )
            lines.append(
                f"| {d.total:,.0f} | {current_pct:.1f}% | "
                f"{current_effective_pct:.1f}% | {scenario_pct:.1f}% | "
                f"{scenario_effective_pct:.1f}% | {d.name} |"
            )
        lines.append("")

        if csv_out:
            lines.append(
                f"_Full row-level detail (every origin/destination pair, not "
                f"just the top {top_n}): `{csv_out}`._"
            )
            lines.append("")

        markdown_out.write_text("\n".join(lines))
        print(f"\nWrote markdown report to {markdown_out}")
