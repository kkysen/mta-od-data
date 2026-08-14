"""Systemwide deinterlining scenario comparator.

See `deinterlining_design.md` (next to this file) for the design this
implements. Deliberately kept independent of `one_seat_rides.py` --
duplicates a couple of small helpers (`parse_route_set`, the CSV/markdown
rendering shape, nearest-station search) rather than importing them, since
the user doesn't want that module touched until this one is proven out;
reconcile the duplication if/when the two get merged.

Unlike `one_seat_rides.py` (one latitude boundary, two named corridors
converging into two named trunks, origin-side reassignment only), this
classifies *every* origin/destination pair whose origin could plausibly
use one of `--routes` (under any scenario being compared) -- no boundary,
same shape as `regional_flow.py`'s unfiltered OD-pairs query -- comparing
one-seat-ride share across today's real routes and any number of
scenarios' route overrides.

"Today" is not a special case: it's `CURRENT_SCENARIO`, a `Scenario` with
no overrides, classified through the exact same code path as every other
scenario. Passing multiple `--scenario-file`s classifies all of them (plus
`CURRENT_SCENARIO`) against the *same* fetched OD pairs in one run, so
comparing several proposals doesn't reclassify "today" once per proposal.
"""

import csv
import shlex
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from datetime import date
from functools import cache
from pathlib import Path
from typing import Annotated

import duckdb
import json5
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import DAY_TYPE_PRESETS, DayType, Station, haversine_m

app = Typer()


class ScenarioError(Exception):
    """Raised for a scenario/CLI-input problem that only `deinterlining()`
    (the CLI command) should turn into a printed error and `SystemExit` --
    every other method here raises this instead of exiting directly, so
    it stays usable as a library function."""


def parse_route_set(s: str) -> frozenset[str]:
    return frozenset(r.strip() for r in s.split(",") if r.strip())


@dataclass(slots=True, frozen=True)
class ODPair:
    origin_id: int
    origin_name: str
    dest_id: int
    dest_name: str
    riders: float
    one_seat: bool
    # Only meaningful when `one_seat` is false: is a station on the
    # scenario-effective origin corridor within `close_threshold_m` of the
    # destination anyway (a short walk, not a real transfer)?
    close: bool
    dist_m: float
    near_station: str | None


@dataclass(slots=True)
class DestStats:
    name: str
    total: float = 0.0
    one_seat: float = 0.0
    close: float = 0.0


@dataclass(slots=True, frozen=True)
class Scenario:
    """A deinterlining scenario: real routes overridden only for the
    specific stations it actually changes. `effective_routes` falls back
    to a station's real current routes for every complex ID absent from
    `overrides` -- see `deinterlining_design.md` for why this replaces
    `one_seat_rides.py`'s corridor-A/corridor-B machinery instead of
    extending it. `slug` names this scenario's own suffixed CSV file when
    multiple scenarios are compared in one run (see `suffixed_path`)."""

    label: str
    slug: str
    overrides: dict[int, frozenset[str]]

    @classmethod
    def load(cls, path: Path, stations_by_id: dict[int, Station]) -> Scenario:
        # JSON5 (a strict superset of JSON): tolerates a trailing comma
        # before a closing `}`/`]`, an easy slip when hand-editing scenario
        # files -- plain `json.loads` would reject it outright.
        try:
            data = json5.loads(path.read_text())
        except ValueError as e:
            raise ScenarioError(f"scenario {path} isn't valid JSON: {e}") from e
        label = data.get("label", path.stem)
        overrides: dict[int, frozenset[str]] = {}
        for complex_id_str, routes in data["overrides"].items():
            complex_id = int(complex_id_str)
            if complex_id not in stations_by_id:
                raise ScenarioError(
                    f"scenario {path} overrides complex {complex_id}, not found "
                    f"in the station reference data"
                )
            overrides[complex_id] = frozenset(routes)
        return cls(label=label, slug=path.stem, overrides=overrides)

    def effective_routes(self, station: Station) -> frozenset[str]:
        return self.overrides.get(station.complex_id, station.routes)

    def classify(
        self,
        *,
        pairs: list[tuple[int, int, float]],
        stations_by_id: dict[int, Station],
        stations_path: Path,
        routes_set: frozenset[str],
        close_lookup: Callable[
            [Station, frozenset[str]], tuple[bool, float, str | None]
        ],
    ) -> ScenarioResult:
        rows: list[ODPair] = []
        total_riders = 0.0
        one_seat_riders = 0.0
        close_riders = 0.0
        dest_stats: dict[int, DestStats] = {}
        for origin_id, dest_id, riders in pairs:
            origin = stations_by_id.get(origin_id)
            dest = stations_by_id.get(dest_id)
            if origin is None or dest is None:
                missing_id = origin_id if origin is None else dest_id
                raise ScenarioError(
                    f"station complex {missing_id} not found in {stations_path} -- "
                    "refetch station reference data with "
                    "`mta-od-data prepare --force-stations`"
                )

            effective_origin_routes = self.effective_routes(origin) & routes_set
            effective_dest_routes = self.effective_routes(dest) & routes_set
            one_seat = bool(effective_origin_routes & effective_dest_routes)

            total_riders += riders
            # A `False`/`0.0`/`None` no-op result when the pair is already
            # one-seat (no walk to evaluate) matches `one_seat_rides.py`'s
            # `close, dist_m = True, 0.0` convention for that case, just
            # inverted here since `close` at 1-seat distance 0 isn't a
            # meaningful "close transfer".
            if one_seat:
                one_seat_riders += riders
                close, dist_m, near_station_name = False, 0.0, None
            else:
                close, dist_m, near_station_name = close_lookup(
                    dest, effective_origin_routes
                )
                if close:
                    close_riders += riders

            rows.append(
                ODPair(
                    origin_id=origin_id,
                    origin_name=origin.display(effective_origin_routes),
                    dest_id=dest_id,
                    dest_name=dest.display(effective_dest_routes),
                    riders=riders,
                    one_seat=one_seat,
                    close=close,
                    dist_m=dist_m,
                    near_station=near_station_name,
                )
            )

            d = dest_stats.setdefault(
                dest_id, DestStats(name=dest.display(dest.routes))
            )
            d.total += riders
            if one_seat:
                d.one_seat += riders
            elif close:
                d.close += riders

        return ScenarioResult(
            scenario=self,
            total_riders=total_riders,
            one_seat_riders=one_seat_riders,
            close_riders=close_riders,
            rows=rows,
            dest_stats=dest_stats,
        )


# Today's real routing, expressed the same way any other scenario is: no
# overrides, so `effective_routes` always falls through to a station's own
# real `Station.routes`. Classified through the same `Scenario.classify`
# as every loaded scenario -- there's no separate "current" code path to
# keep in sync with the general one.
CURRENT_SCENARIO = Scenario(
    label="Current (today's real routing)", slug="current", overrides={}
)


def suffixed_path(path: Path, suffix: str) -> Path:
    return path.with_name(f"{path.stem}_{suffix}{path.suffix}")


@dataclass(slots=True, frozen=True)
class ScenarioResult:
    scenario: Scenario
    total_riders: float
    one_seat_riders: float
    close_riders: float
    rows: list[ODPair]
    dest_stats: dict[int, DestStats]

    @property
    def effective_riders(self) -> float:
        return self.one_seat_riders + self.close_riders

    def pct(self, riders: float) -> float:
        return 100 * riders / self.total_riders if self.total_riders else float("nan")

    def write_csv(self, path: Path) -> None:
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(ODPair)])
            writer.writeheader()
            writer.writerows(asdict(r) for r in self.rows)
        print(f"\nWrote {len(self.rows):,} rows to {path}")

    def print_headline(self, *, close_threshold_m: float) -> None:
        print(f"\n=== Scenario: {self.scenario.label} ===")
        print(f"Total riders: {self.total_riders:,.0f}")
        print(
            f"One-seat:              {self.one_seat_riders:>12,.0f} "
            f"({self.pct(self.one_seat_riders):5.1f}%)"
        )
        print(
            f"Close one-seat (within {close_threshold_m:.0f}m): "
            f"{self.close_riders:>12,.0f} ({self.pct(self.close_riders):5.1f}%)"
        )
        print(
            f"Effective one-seat:    {self.effective_riders:>12,.0f} "
            f"({self.pct(self.effective_riders):5.1f}%)"
        )

    def render_markdown(
        self,
        *,
        show_label: bool,
        close_threshold_m: float,
        top_n: int,
        csv_out: Path | None,
    ) -> str:
        h2 = "###" if show_label else "##"
        lines: list[str] = [f"## {self.scenario.label}", ""] if show_label else []

        lines += [
            f"{h2} Headline numbers",
            "",
            f"- **Total: {self.total_riders:,.0f} riders**",
            f"- **One-seat: {self.pct(self.one_seat_riders):.1f}%** "
            f"({self.one_seat_riders:,.0f})",
            f"- **Close one-seat: {self.pct(self.close_riders):.1f}%** "
            f"({self.close_riders:,.0f}) -- within {close_threshold_m:.0f}m of a "
            f"station on the scenario-effective origin corridor",
            f"- **Effective one-seat: {self.pct(self.effective_riders):.1f}%** "
            f"({self.effective_riders:,.0f})",
            "",
            f"{h2} Top {top_n} origin/destination pairs",
            "",
            "| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]

        def pair_riders(pair: ODPair) -> float:
            return pair.riders

        top_pairs = sorted(self.rows, key=pair_riders, reverse=True)[:top_n]
        for i, pr in enumerate(top_pairs, 1):
            type_str = "1-seat" if pr.one_seat else "xfer"
            close_str = "" if pr.one_seat else ("close" if pr.close else "far")
            dist_str = "" if pr.one_seat else f"{pr.dist_m:.0f}m"
            lines.append(
                f"| {i} | {pr.riders:,.0f} | {self.pct(pr.riders):.2f}% | "
                f"{type_str} | {close_str} | {dist_str} | "
                f"{pr.origin_name} → {pr.dest_name} |"
            )
        lines.append("")

        lines.append(
            f"{h2} Top {top_n} destination stations, summed across all origins"
        )
        lines.append("")
        lines.append("| Riders | 1-Seat % | Effective % | Destination |")
        lines.append("| --- | --- | --- | --- |")

        def dest_total(d: DestStats) -> float:
            return d.total

        for d in sorted(self.dest_stats.values(), key=dest_total, reverse=True)[:top_n]:
            one_seat_pct = 100 * d.one_seat / d.total if d.total else float("nan")
            effective_pct = (
                100 * (d.one_seat + d.close) / d.total if d.total else float("nan")
            )
            lines.append(
                f"| {d.total:,.0f} | {one_seat_pct:.1f}% | {effective_pct:.1f}% | "
                f"{d.name} |"
            )
        lines.append("")

        if csv_out:
            lines.append(
                f"_Full row-level detail (every origin/destination pair, not "
                f"just the top {top_n}): `{csv_out}`._"
            )
            lines.append("")
        return "\n".join(lines)


def print_comparison(results: list[ScenarioResult]) -> None:
    print("\n=== Scenario comparison ===")
    for r in results:
        print(
            f"  {r.scenario.label:<55} total={r.total_riders:>9,.0f}  "
            f"direct={r.one_seat_riders:>8,.0f} ({r.pct(r.one_seat_riders):5.1f}%)  "
            f"close={r.close_riders:>7,.0f}  "
            f"effective={r.effective_riders:>8,.0f} ({r.pct(r.effective_riders):5.1f}%)"
        )


def render_comparison_markdown(results: list[ScenarioResult]) -> str:
    lines = [
        "## Scenario comparison",
        "",
        f"Total riders is the same {results[0].total_riders:,.0f} across every "
        f"scenario below -- only how many of those riders get a one-seat ride "
        f"changes.",
        "",
        "| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in results:
        lines.append(
            f"| {r.scenario.label} | {r.total_riders:,.0f} | "
            f"{r.one_seat_riders:,.0f} ({r.pct(r.one_seat_riders):.1f}%) | "
            f"{r.close_riders:,.0f} ({r.pct(r.close_riders):.1f}%) | "
            f"{r.effective_riders:,.0f} ({r.pct(r.effective_riders):.1f}%) |"
        )
    lines.append("")
    return "\n".join(lines)


@app.command()
def deinterlining(
    # Required (no default): only `routes` has no sensible default, so it
    # comes first -- every other parameter (including `scenario_files`,
    # which defaults to comparing `CURRENT_SCENARIO` alone) has one.
    routes: Annotated[
        str,
        Option(
            help=(
                "Route universe: which routes this comparison covers (e.g. "
                "A,B,C,D for a Columbus Circle scenario)"
            )
        ),
    ],
    scenario_files: Annotated[
        list[Path],
        Option(
            "--scenario-file",
            help=(
                "JSON file: {'label': str, 'overrides': {complex_id: "
                "[route, ...]}}. Repeatable -- classifies every scenario "
                "given (plus today's real routing) against the same fetched "
                "OD pairs in one run. Only the listed complex IDs' routes "
                "change; every other station keeps its real current routes. "
                "Trailing commas are tolerated."
            ),
        ),
    ] = [],  # noqa: B006 -- never mutated; Typer replaces this with parsed CLI values
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
        Option(
            help=(
                "Optional: dump classified per-OD-pair rows here. Suffixed per "
                "scenario (e.g. `_current`, `_<scenario-file-stem>`) when "
                "comparing more than one."
            )
        ),
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
    `--routes` as one-seat or transfer, under today's real routing and any
    number of `--scenario-file` route-override scenarios -- all classified
    in one pass over the same fetched OD pairs, so comparing several
    proposals doesn't reclassify "today" once per proposal.

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
        # Columbus Circle: both proposed swap directions vs. today, in one run
        mta-od-data analyze deinterlining --routes A,B,C,D \\
            --scenario-file \\
            src/mta_od_data/analyze/scenarios/columbus_circle_ac_express.json \\
            --scenario-file \\
            src/mta_od_data/analyze/scenarios/columbus_circle_bd_express.json \\
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
    try:
        scenarios = [
            CURRENT_SCENARIO,
            *(Scenario.load(f, stations_by_id) for f in scenario_files),
        ]
    except ScenarioError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    show_label = len(scenarios) > 1
    for s in scenarios:
        print(f"Scenario: {s.label} ({len(s.overrides)} stations overridden)")
    print(f"Route universe: {sorted(routes_set)}")
    print(f"Day filter: {days_list if days_list else 'all days'} ({day_type_label})")

    # Systemwide, but not literally every station: an origin only matters
    # if it could plausibly use one of `--routes` under *any* scenario
    # being compared (today's real routing included) -- otherwise its
    # trips have nothing to do with the junction(s) being analyzed (unlike
    # `regional_flow.py`, whose question -- does a trip touch this region
    # -- has no such natural restriction).
    origin_ids = [
        s.complex_id
        for s in stations_by_id.values()
        if any(sc.effective_routes(s) & routes_set for sc in scenarios)
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
    # `platforms_by_complex`, loaded fresh per invocation. Shared across
    # every scenario's `Scenario.classify` call (including
    # `CURRENT_SCENARIO`'s), since cache keys are (dest, effective routes)
    # pairs, not scenario-specific.
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

    try:
        results = [
            s.classify(
                pairs=pairs,
                stations_by_id=stations_by_id,
                stations_path=stations,
                routes_set=routes_set,
                close_lookup=close_lookup,
            )
            for s in scenarios
        ]
    except ScenarioError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    for result in results:
        result.print_headline(close_threshold_m=close_threshold_m)
    if show_label:
        print_comparison(results)

    csv_paths: list[Path | None] = [
        None
        if csv_out is None
        else (csv_out if not show_label else suffixed_path(csv_out, s.slug))
        for s in scenarios
    ]
    if csv_out:
        for path, result in zip(csv_paths, results, strict=True):
            assert path is not None
            result.write_csv(path)

    if markdown_out:
        produced_by = shlex.join([Path(sys.argv[0]).name, *sys.argv[1:]])
        preamble_lines = [
            f"# Deinterlining scenario comparison: {','.join(sorted(routes_set))}",
            "",
            f"Average {day_type_label} ridership ({n_distinct_days} distinct "
            f"days in the data, {min_date} to {max_date}), every "
            f"origin/destination pair whose origin could plausibly use "
            f"{','.join(sorted(routes_set))} under any scenario compared here.",
            "",
            f"Produced by `{produced_by}`.",
            "",
        ]
        sections = [
            "\n".join(preamble_lines),
            *([render_comparison_markdown(results)] if show_label else []),
            *(
                result.render_markdown(
                    show_label=show_label,
                    close_threshold_m=close_threshold_m,
                    top_n=top_n,
                    csv_out=path,
                )
                for result, path in zip(results, csv_paths, strict=True)
            ),
        ]
        markdown_out.write_text("\n---\n\n".join(sections))
        print(f"\nWrote markdown report to {markdown_out}")
