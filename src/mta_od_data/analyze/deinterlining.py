"""Systemwide deinterlining scenario comparator.

See `deinterlining_design.md` (next to this file) for the design this
implements,
and `ScenarioComparison` for what a single one covers.

Unlike `one_seat_rides.py`
(one latitude boundary, two named corridors converging into two named
trunks, origin-side reassignment only),
this classifies *every* origin/destination pair
with either end on one of the comparison's routes,
symmetrically: a swap changes a trip the same way whichever way it runs.
The subset with *both* ends on them is reported alongside,
since a junction's effect washes out in a systemwide total.
Kept independent of it,
duplicating a couple of small helpers rather than importing them;
reconcile if the two ever merge.
"""

import csv
import itertools
import json
import re
import shlex
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from functools import cache
from pathlib import Path
from typing import Annotated, Any

import duckdb
import json5
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError
from typer import Option, Typer

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import (
    DAY_TYPE_PRESETS,
    DayCoverage,
    DayType,
    Station,
    haversine_m,
)

app = Typer()

SCENARIOS_FILE = ROOT / "src" / "mta_od_data" / "analyze" / "scenarios.json5"

type Routes = frozenset[str]


class ScenarioError(Exception):
    """Raised rather than exiting,
    so everything but `deinterlining()` itself
    stays usable as a library function."""


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "scenario"


@dataclass(slots=True, frozen=True)
class ODPair:
    origin_id: int
    origin_name: str
    dest_id: int
    dest_name: str
    riders: float
    # Both ends served by the comparison's routes.
    # The detailed tables are scoped to these
    # (see `comparison_table_markdown`);
    # the CSV keeps every row, with this column to filter on.
    both_ends: bool
    one_seat: bool
    # Only meaningful when `one_seat` is false.
    close: bool
    # `None` when there is no corridor to measure against at all,
    # i.e. the origin has no route in the comparison's universe,
    # which is distinct from a measured distance of 0m
    # (the destination is itself on the corridor).
    dist_m: float | None
    near_station: str | None


@dataclass(slots=True)
class DestStats:
    name: str
    total: float = 0.0
    one_seat: float = 0.0
    close: float = 0.0


@dataclass(slots=True, frozen=True)
class RouteDelta:
    add: Routes
    remove: Routes

    def __or__(self, other: RouteDelta) -> RouteDelta:
        return RouteDelta(add=self.add | other.add, remove=self.remove | other.remove)

    def apply(self, station: Station) -> Routes:
        return (station.routes - self.remove) | self.add


class OverrideGroup(BaseModel):
    """`line` (e.g. "8th Av - Fulton St") is required
    even where a station name is already unique:
    names are shared by several complexes ("72 St" is three),
    and it says which physical line a group is about
    without cross-referencing `stations_individual.csv`."""

    model_config = ConfigDict(extra="forbid")

    line: str = Field(min_length=1)
    add: list[str] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list)
    stations: list[str] = Field(min_length=1)


class ScenarioEntry(BaseModel):
    """`routes` is the universe this scenario is about
    (e.g. A,B,C,D for a Columbus Circle swap):
    which routes count towards a one-seat ride,
    and which origins are worth classifying at all.
    A comparison uses the union of the selected scenarios';
    see `ScenarioComparison`."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    description: str | None = None
    routes: list[str] = Field(min_length=1)
    overrides: list[OverrideGroup] = Field(default_factory=list)


# An empty category (`min_length=1`) would silently contribute zero
# combinations to `combine_scenarios`'s cartesian product.
# Also what `scenarios.schema.json` is generated from,
# see `tests/test_scenarios_schema.py`.
SCENARIO_FILE_ADAPTER = TypeAdapter(
    dict[str, Annotated[list[ScenarioEntry], Field(min_length=1)]]
)

SCENARIOS_SCHEMA_FILE = (
    ROOT / "src" / "mta_od_data" / "analyze" / "scenarios.schema.json"
)


def generate_scenario_schema(
    *,
    stations_path: Path = DATA / "stations_complexes.csv",
    individual_stations_path: Path = DATA / "stations_individual.csv",
) -> str:
    """The JSON Schema for a scenario file,
    with real line, station, and route values baked in as `enum`s
    so an editor can autocomplete them and flag a typo.

    Those `enum`s are an editor-time snapshot only:
    a real load re-checks
    against whichever `--stations`/`--stations-individual` was actually
    passed, which can legitimately differ from these defaults.

    The reference CSVs aren't committed
    (gitignored, `mta-od-data prepare`-generated);
    `tests/test_scenarios_schema.py` skips rather than fails without them.
    Regenerate `scenarios.schema.json` with:

        uv run python -c "from mta_od_data.analyze.deinterlining import \\
            SCENARIOS_SCHEMA_FILE, generate_scenario_schema; \\
            SCENARIOS_SCHEMA_FILE.write_text(generate_scenario_schema())"
    """
    stations_by_id = Station.load_complexes(stations_path)
    individual_stations = Station.load_individuals(individual_stations_path)
    known_lines = sorted({s.line for s in individual_stations if s.line})
    # Platform names, not a complex's merged name (e.g. "62 St/New
    # Utrecht Av"): that's what a `stations` entry resolves against.
    known_stations = sorted({s.name for s in individual_stations})
    known_routes = sorted({r for s in stations_by_id.values() for r in s.routes})

    schema: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Deinterlining scenario file",
        "description": (
            "A JSON object mapping category name to the deinterlining "
            "scenarios in it, for `mta-od-data analyze deinterlining` "
            "(--scenario-file, scenarios.json5 by default). See "
            "OverrideGroup/ScenarioEntry in deinterlining.py for the models "
            "this is generated from."
        ),
        **SCENARIO_FILE_ADAPTER.json_schema(),
    }
    override_group = schema["$defs"]["OverrideGroup"]
    override_group["properties"]["line"]["enum"] = known_lines
    override_group["properties"]["stations"]["items"]["enum"] = known_stations
    override_group["properties"]["add"]["items"]["enum"] = known_routes
    override_group["properties"]["remove"]["items"]["enum"] = known_routes
    scenario_entry = schema["$defs"]["ScenarioEntry"]
    scenario_entry["properties"]["routes"]["items"]["enum"] = known_routes
    return json.dumps(schema, indent=2) + "\n"


@dataclass(slots=True, frozen=True)
class StationIndex:
    by_name_line: dict[tuple[str, str], Station]
    known_routes: frozenset[str]

    @classmethod
    def build(
        cls,
        stations_by_id: dict[int, Station],
        individual_stations: list[Station],
    ) -> StationIndex:
        by_name_line = {
            (s.name, s.line): stations_by_id[s.complex_id] for s in individual_stations
        }
        return cls(
            by_name_line=by_name_line,
            known_routes=frozenset(
                r for s in stations_by_id.values() for r in s.routes
            ),
        )

    def resolve(self, name: str, line: str, *, path: Path) -> Station:
        key = (name, line)
        if key not in self.by_name_line:
            raise ScenarioError(
                f'scenario {path}: no station named "{name}" on line "{line}"'
            )
        return self.by_name_line[key]

    def check_routes(self, routes: Routes, *, name: str, path: Path) -> None:
        unknown = sorted(routes - self.known_routes)
        if unknown:
            raise ScenarioError(
                f'scenario {path}: scenario "{name}" lists unknown route(s) '
                f'{unknown} in "routes" (not in the station reference data)'
            )


@dataclass(slots=True, frozen=True)
class Scenario:
    """See `deinterlining_design.md` for why per-station overrides
    replace `one_seat_rides.py`'s corridor-A/corridor-B machinery
    instead of extending it."""

    name: str
    description: str
    category: str
    # What everything below is already narrowed to:
    # the entry's own `routes` as loaded,
    # the whole comparison's once combined.
    # Empty on `CURRENT` until then.
    routes: Routes
    overrides: dict[Station, RouteDelta]
    effective_routes: dict[Station, Routes]

    def slug(self) -> str:
        return slugify(self.name)

    def routes_of(self, station: Station) -> Routes:
        return self.effective_routes.get(station, station.routes & self.routes)

    @classmethod
    def load(
        cls,
        entry: ScenarioEntry,
        category: str,
        path: Path,
        station_index: StationIndex,
    ) -> Scenario:
        routes = frozenset(entry.routes)
        station_index.check_routes(routes, name=entry.name, path=path)
        overrides: dict[Station, RouteDelta] = {}
        for group in entry.overrides:
            add = frozenset(group.add)
            remove = frozenset(group.remove)
            outside = sorted((add | remove) - routes)
            if outside:
                raise ScenarioError(
                    f'scenario {path}: scenario "{entry.name}" adds/removes '
                    f"route(s) {outside} outside its own routes "
                    f"{sorted(routes)}: a scenario's routes must cover "
                    f"every route it moves"
                )
            delta = RouteDelta(add=add, remove=remove)
            for station_name in group.stations:
                station = station_index.resolve(station_name, group.line, path=path)
                existing = overrides.get(station)
                overrides[station] = delta if existing is None else existing | delta
        return cls(
            name=entry.name,
            description=entry.description or entry.name,
            category=category,
            routes=routes,
            overrides=overrides,
            effective_routes={
                station: delta.apply(station) & routes
                for station, delta in overrides.items()
            },
        )

    @classmethod
    def combine(cls, scenarios: list[Scenario], routes: Routes) -> Scenario:
        """`routes` is the whole comparison's universe
        (`ScenarioComparison`),
        not these scenarios' own,
        which is also why a single-element `scenarios` isn't returned
        as-is, its `effective_routes` being narrowed to just its own."""
        overrides: dict[Station, RouteDelta] = {}
        for scenario in scenarios:
            for station, delta in scenario.overrides.items():
                existing = overrides.get(station)
                overrides[station] = delta if existing is None else existing | delta
        name = " + ".join(s.name for s in scenarios)
        return cls(
            name=name,
            description=" + ".join(s.description for s in scenarios),
            category=" + ".join(s.category for s in scenarios),
            routes=routes,
            overrides=overrides,
            effective_routes={
                station: delta.apply(station) & routes
                for station, delta in overrides.items()
            },
        )

    def classify(
        self,
        *,
        pairs: list[tuple[int, int, float]],
        stations_by_id: dict[int, Station],
        stations_path: Path,
        scope_ids: frozenset[int],
        close_lookup: Callable[
            [Station, Routes], tuple[bool, float | None, str | None]
        ],
    ) -> ScenarioResult:
        rows: list[ODPair] = []
        total_riders = 0.0
        one_seat_riders = 0.0
        close_riders = 0.0
        both_total = 0.0
        both_one_seat = 0.0
        both_close = 0.0
        dest_stats: dict[int, DestStats] = {}
        for origin_id, dest_id, riders in pairs:
            origin = stations_by_id.get(origin_id)
            dest = stations_by_id.get(dest_id)
            if origin is None or dest is None:
                missing_id = origin_id if origin is None else dest_id
                raise ScenarioError(
                    f"station complex {missing_id} not found in "
                    f"{stations_path}; refetch station reference data with "
                    "`mta-od-data prepare --force-stations`"
                )

            effective_origin_routes = self.routes_of(origin)
            effective_dest_routes = self.routes_of(dest)
            origin_name = origin.display(effective_origin_routes)
            dest_name = dest.display(effective_dest_routes)
            one_seat = bool(effective_origin_routes & effective_dest_routes)

            both_ends = origin_id in scope_ids and dest_id in scope_ids
            total_riders += riders
            if both_ends:
                both_total += riders
            if one_seat:
                one_seat_riders += riders
                if both_ends:
                    both_one_seat += riders
                close, dist_m, near_station_name = False, None, None
            else:
                close, dist_m, near_station_name = close_lookup(
                    dest, effective_origin_routes
                )
                if close:
                    close_riders += riders
                    if both_ends:
                        both_close += riders

            rows.append(
                ODPair(
                    origin_id=origin_id,
                    origin_name=origin_name,
                    dest_id=dest_id,
                    dest_name=dest_name,
                    riders=riders,
                    both_ends=both_ends,
                    one_seat=one_seat,
                    close=close,
                    dist_m=dist_m,
                    near_station=near_station_name,
                )
            )

            # Both-ends only, to match the tables it feeds:
            # a destination off the comparison's routes has no one-seat
            # ridership from anywhere, so it would only ever add rows
            # reading 0.0%.
            if both_ends:
                d = dest_stats.setdefault(
                    dest_id, DestStats(name=dest.display(dest.routes))
                )
                d.total += riders
                if one_seat:
                    d.one_seat += riders
                elif close:
                    d.close += riders

        if not total_riders:
            raise ScenarioError(
                f"scenario {self.name!r}: no ridership among the fetched "
                f"origin/destination pairs, nothing to classify (check "
                f"the selected scenarios' routes and the day filter)"
            )

        return ScenarioResult(
            scenario=self,
            overall=RiderStats(
                total=total_riders,
                one_seat=one_seat_riders,
                close=close_riders,
            ),
            both_ends=RiderStats(
                total=both_total,
                one_seat=both_one_seat,
                close=both_close,
            ),
            rows=rows,
            dest_stats=dest_stats,
        )


# Today's real routing, which no scenario file has to declare.
# Its empty `routes` is what makes it adopt the comparison's universe
# (see `ScenarioComparison`).
CURRENT = Scenario(
    name="Current",
    description="Current routes today",
    category="Current",
    routes=frozenset(),
    overrides={},
    effective_routes={},
)


@dataclass(slots=True, frozen=True)
class ScenarioCategory:
    name: str
    scenarios: list[Scenario]

    @classmethod
    def load(
        cls,
        name: str,
        entries: list[ScenarioEntry],
        path: Path,
        station_index: StationIndex,
    ) -> ScenarioCategory:
        return cls(
            name=name,
            scenarios=[
                Scenario.load(entry, name, path, station_index) for entry in entries
            ],
        )


@dataclass(slots=True, frozen=True)
class ScenarioFile:
    path: Path
    categories: list[ScenarioCategory]

    @classmethod
    def load(cls, path: Path, station_index: StationIndex) -> ScenarioFile:
        # JSON5, not JSON:
        # tolerates the trailing comma before a closing `}`/`]`
        # that's easy to leave when hand-editing.
        try:
            data = json5.loads(path.read_text())
        except ValueError as e:
            raise ScenarioError(f"scenario file {path} isn't valid JSON: {e}") from e
        try:
            by_category = SCENARIO_FILE_ADAPTER.validate_python(data)
        except ValidationError as e:
            raise ScenarioError(
                f"scenario file {path} doesn't match the expected shape:\n{e}"
            ) from e
        return cls(
            path=path,
            categories=[
                ScenarioCategory.load(category, entries, path, station_index)
                for category, entries in by_category.items()
            ],
        )

    def filter(self, categories: frozenset[str]) -> ScenarioFile:
        by_name = {c.name: c for c in self.categories}
        missing = categories - by_name.keys()
        if missing:
            available = ", ".join(sorted(by_name)) or "none"
            raise ScenarioError(
                f"unknown categories {sorted(missing)!r} in {self.path} "
                f"(available: {available})"
            )
        return ScenarioFile(
            path=self.path,
            categories=[c for c in self.categories if c.name in categories],
        )

    @property
    def routes(self) -> Routes:
        return frozenset(
            route
            for category in self.categories
            for scenario in category.scenarios
            for route in scenario.routes
        )

    def combine_scenarios(self, baseline: list[Scenario]) -> list[Scenario]:
        """`baseline` is an option for *every* category
        rather than one extra combination alongside them:
        leaving a category unchanged is itself one of its choices.
        So two categories with two scenarios each
        give nine combinations, not four."""
        if not self.categories:
            return []
        routes = self.routes
        return [
            Scenario.combine(list(combo), routes)
            for combo in itertools.product(
                *([*baseline, *c.scenarios] for c in self.categories)
            )
        ]


def suffixed_path(path: Path, suffix: str) -> Path:
    return path.with_name(f"{path.stem}_{suffix}{path.suffix}")


@dataclass(slots=True, frozen=True)
class RiderStats:
    """One-seat split over some set of pairs,
    so the same arithmetic serves the whole comparison
    and the both-ends subset of it."""

    total: float
    one_seat: float
    close: float

    @property
    def effective(self) -> float:
        return self.one_seat + self.close

    def pct(self, riders: float) -> float:
        # `Scenario.classify` raises before building a `ScenarioResult`
        # with no riders at all, but the both-ends subset of a category
        # whose routes share no station can legitimately be empty.
        if not self.total:
            return 0.0
        return 100 * riders / self.total

    def markdown_row(self, label: str) -> str:
        return (
            f"| {label} | {self.total:,.0f} "
            f"| {self.one_seat:,.0f} ({self.pct(self.one_seat):.1f}%) "
            f"| {self.close:,.0f} ({self.pct(self.close):.1f}%) "
            f"| {self.effective:,.0f} "
            f"({self.pct(self.effective):.1f}%) |"
        )

    def summary_line(self, label: str) -> str:
        return (
            f"  {label:<55} total={self.total:>9,.0f}  "
            f"direct={self.one_seat:>8,.0f} ({self.pct(self.one_seat):5.1f}%)  "
            f"close={self.close:>7,.0f}  "
            f"effective={self.effective:>8,.0f} ({self.pct(self.effective):5.1f}%)"
        )

    def print_lines(self, *, close_threshold_m: float) -> None:
        print(f"Total riders: {self.total:,.0f}")
        print(
            f"One-seat:              {self.one_seat:>12,.0f} "
            f"({self.pct(self.one_seat):5.1f}%)"
        )
        print(
            f"Close one-seat (within {close_threshold_m:.0f}m): "
            f"{self.close:>12,.0f} ({self.pct(self.close):5.1f}%)"
        )
        print(
            f"Effective one-seat:    {self.effective:>12,.0f} "
            f"({self.pct(self.effective):5.1f}%)"
        )


@dataclass(slots=True, frozen=True)
class ScenarioResult:
    scenario: Scenario
    overall: RiderStats
    # Pairs with both ends on the comparison's routes, a subset of `overall`:
    # the trips the routes could plausibly carry end to end,
    # where a swap shows up undiluted by trips only half in scope.
    both_ends: RiderStats
    rows: list[ODPair]
    dest_stats: dict[int, DestStats]

    def write_csv(self, path: Path) -> None:
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(ODPair)])
            writer.writeheader()
            writer.writerows(asdict(r) for r in self.rows)
        print(f"\nWrote {len(self.rows):,} rows to {path}")

    def print_headline(self, *, close_threshold_m: float) -> None:
        print(f"\n=== Scenario: {self.scenario.name} ===")
        print("Both ends on the comparison's routes:")
        self.both_ends.print_lines(close_threshold_m=close_threshold_m)
        print("Either end on the comparison's routes:")
        self.overall.print_lines(close_threshold_m=close_threshold_m)

    def render_markdown(
        self,
        *,
        show_label: bool,
        close_threshold_m: float,
        top_n: int,
        csv_out: Path | None,
    ) -> str:
        h2 = "###" if show_label else "##"
        t = self.both_ends
        lines: list[str] = [f"## {self.scenario.name}", ""] if show_label else []

        # Only without a comparison table above, which says all of this
        # for every scenario at once.
        if not show_label:
            lines += [
                f"{h2} Headline numbers",
                "",
                f"- **Total: {t.total:,.0f} riders**",
                f"- **One-seat: {t.pct(t.one_seat):.1f}%** ({t.one_seat:,.0f})",
                f"- **Close one-seat: {t.pct(t.close):.1f}%** "
                f"({t.close:,.0f}), within {close_threshold_m:.0f}m of a "
                f"station on the scenario-effective origin corridor",
                f"- **Effective one-seat: {t.pct(t.effective):.1f}%** "
                f"({t.effective:,.0f})",
                f"- **Either end on the routes: {self.overall.total:,.0f} "
                f"riders**, {self.overall.pct(self.overall.effective):.1f}% "
                f"effective one-seat",
                "",
            ]

        lines += [
            f"{h2} Top {top_n} origin/destination pairs",
            "",
            "Both ends on the comparison's routes, as in the comparison table above.",
            "",
            "| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]

        def pair_riders(pair: ODPair) -> float:
            return pair.riders

        both_ends_rows = [r for r in self.rows if r.both_ends]
        top_pairs = sorted(both_ends_rows, key=pair_riders, reverse=True)[:top_n]
        for i, pr in enumerate(top_pairs, 1):
            type_str = "1-seat" if pr.one_seat else "xfer"
            close_str = "" if pr.one_seat else ("close" if pr.close else "far")
            dist_str = "" if pr.dist_m is None else f"{pr.dist_m:.0f}m"
            lines.append(
                f"| {i} | {pr.riders:,.0f} | {self.both_ends.pct(pr.riders):.2f}% | "
                f"{type_str} | {close_str} | {dist_str} | "
                f"{pr.origin_name} → {pr.dest_name} |"
            )
        lines.append("")

        lines.append(
            f"{h2} Top {top_n} destination stations, summed across all origins"
        )
        lines.append("")
        lines.append(
            "Both ends on the comparison's routes, as in the comparison table above."
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
                f"_Full row-level detail (every origin/destination pair, "
                f"either end on the routes, not just the top {top_n} with "
                f"both: `{csv_out}`, whose `both_ends` column is what the "
                f"tables above filter on)._"
            )
            lines.append("")
        return "\n".join(lines)


@dataclass(slots=True, frozen=True)
class ScenarioComparison:
    """The `routes` universe is the union of the selected scenarios' own,
    applied to all of them alike.
    Scenarios classified under different universes aren't comparable:
    origins in scope are the union either way,
    so the narrower one carries the other's riders in its total
    while never giving them a one-seat ride."""

    routes: Routes
    scenarios: list[Scenario]

    def classify(
        self,
        *,
        pairs: list[tuple[int, int, float]],
        stations_by_id: dict[int, Station],
        stations_path: Path,
        scope_ids: frozenset[int],
        close_lookup: Callable[
            [Station, Routes], tuple[bool, float | None, str | None]
        ],
    ) -> ScenarioComparisonResult:
        return ScenarioComparisonResult(
            comparison=self,
            results=[
                scenario.classify(
                    pairs=pairs,
                    stations_by_id=stations_by_id,
                    stations_path=stations_path,
                    scope_ids=scope_ids,
                    close_lookup=close_lookup,
                )
                for scenario in self.scenarios
            ],
        )


@dataclass(slots=True, frozen=True)
class ScenarioComparisonResult:
    """Every scenario in a `ScenarioComparison`,
    classified over the same OD pairs."""

    comparison: ScenarioComparison
    results: list[ScenarioResult]

    @property
    def labelled(self) -> bool:
        """Whether output has to name which scenario it's describing.
        With one there's nothing to tell apart,
        and no comparison table to write either."""
        return len(self.results) > 1

    def csv_paths(self, csv_out: Path | None) -> list[Path | None]:
        """One path per scenario, suffixed to keep them apart,
        except for a lone scenario, which keeps `csv_out` itself."""
        if csv_out is None:
            return [None] * len(self.results)
        if not self.labelled:
            return [csv_out]
        return [suffixed_path(csv_out, r.scenario.slug()) for r in self.results]

    def print_summary(self, *, close_threshold_m: float) -> None:
        if not self.labelled:
            for result in self.results:
                result.print_headline(close_threshold_m=close_threshold_m)
            return
        print(
            f"\n=== Scenario comparison, both ends on the comparison's "
            f"routes (close one-seat: within {close_threshold_m:.0f}m) ==="
        )
        for r in self.results:
            print(r.both_ends.summary_line(r.scenario.name))
        print("\n=== Either end on the comparison's routes ===")
        for r in self.results:
            print(r.overall.summary_line(r.scenario.name))

    def write_csvs(self, csv_out: Path) -> None:
        for path, result in zip(self.csv_paths(csv_out), self.results, strict=True):
            assert path is not None
            result.write_csv(path)

    def comparison_table_markdown(self, *, close_threshold_m: float) -> str:
        routes = ",".join(sorted(self.comparison.routes))
        header = (
            "| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | "
            "Effective 1-Seat |\n| --- | --- | --- | --- | --- |"
        )

        # Both ends first, and every detailed table below scoped to it:
        # it's the denominator a reader needs, the trips these routes could
        # carry end to end. Trips with only one end on them can never be a
        # one-seat ride under any scenario (that needs a shared route, which
        # puts both ends in scope), so they only ever dilute the rate.
        lines = [
            "## Scenario comparison",
            "",
            f"Every origin/destination pair with *both* ends served by "
            f"{routes}: the trips these routes could carry end to end, "
            f"including the many that keep a one-seat ride whatever the "
            f"scenario. Total riders is the same "
            f"{self.results[0].both_ends.total:,.0f} across every scenario "
            f"below; only how many of those riders get a one-seat ride "
            f"changes. Close one-seat counts a transfer trip whose "
            f"destination is within {close_threshold_m:.0f}m of a station on "
            f"that scenario's effective origin corridor.",
            "",
            header,
        ]
        for r in self.results:
            lines.append(r.both_ends.markdown_row(r.scenario.name))

        # Kept as context, not as the headline: it says how much of the
        # system a plan touches at all, but a single junction's effect
        # washes out against a systemwide total.
        lines += [
            "",
            "### Either end on the comparison's routes",
            "",
            f"The wider {self.results[0].overall.total:,.0f} riders with "
            f"*either* end served by {routes}, the above among them. This "
            f"says how much of the system a plan touches at all; the "
            f"difference is transfer trips with one end off these routes "
            f"entirely, which no scenario here can change.",
            "",
            header,
        ]
        for r in self.results:
            lines.append(r.overall.markdown_row(r.scenario.name))
        lines.append("")
        return "\n".join(lines)

    def render_markdown(
        self,
        *,
        preamble: str,
        close_threshold_m: float,
        top_n: int,
        csv_out: Path | None,
    ) -> str:
        sections = [
            preamble,
            *(
                [self.comparison_table_markdown(close_threshold_m=close_threshold_m)]
                if self.labelled
                else []
            ),
            *(
                result.render_markdown(
                    show_label=self.labelled,
                    close_threshold_m=close_threshold_m,
                    top_n=top_n,
                    csv_out=path,
                )
                for result, path in zip(
                    self.results, self.csv_paths(csv_out), strict=True
                )
            ),
        ]
        return "\n---\n\n".join(sections)


def resolve_scenarios(
    *,
    categories: list[str],
    scenario_file: Path,
    station_index: StationIndex,
) -> ScenarioComparison:
    """The comparison for a `--category` selection,
    `CURRENT` among every category's options
    (see `ScenarioFile.combine_scenarios`)."""
    try:
        file = ScenarioFile.load(scenario_file, station_index)
    except FileNotFoundError as e:
        raise ScenarioError(f"missing required scenario file {scenario_file}") from e

    if not categories:
        available = ", ".join(sorted(c.name for c in file.categories)) or "none"
        raise ScenarioError(
            f"no --category selected: the scenarios to compare, and the "
            f"routes to compare them over, both come from one (available "
            f"in {scenario_file}: {available})"
        )
    selected = file.filter(frozenset(categories))
    return ScenarioComparison(
        routes=selected.routes,
        scenarios=selected.combine_scenarios([CURRENT]),
    )


@app.command()
def deinterlining(
    categories: Annotated[
        list[str] | None,
        Option(
            "--category",
            help=(
                "Select a category in --scenario-file (e.g. a junction's "
                "proposed swap directions). Required: both the scenarios "
                "to compare and the routes to compare them over come from "
                "it, with today's routing always included. Repeatable: "
                "with two or more, every scenario in each selected "
                "category runs combined with one from every other, and "
                "leaving a category unchanged is one of its options, so "
                "two categories with two scenarios each run nine "
                "combinations."
            ),
        ),
    ] = None,
    scenario_file: Annotated[
        Path,
        Option(
            help=(
                "JSON file, a JSON object of {category: [{'name': str, "
                "'description': str, 'routes': [route, ...], 'overrides': "
                "[{'line': str, 'add': [route, ...], 'remove': [route, "
                "...], 'stations': [station_name, ...]}, ...]}, ...]}. "
                "Each override group applies the same add/remove to every "
                "station listed; 'routes' must cover every route the "
                "scenario moves. 'line' (e.g. '8th Av - Fulton St') is "
                "required on every group: it disambiguates station names "
                "shared by several complexes, and states which physical "
                "line the group applies to. --category selects by the "
                'top-level key; "Current" (today\'s real routing) is built '
                "in rather than defined here. Trailing commas are "
                "tolerated."
            ),
        ),
    ] = SCENARIOS_FILE,
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
    """Systemwide deinterlining scenario comparator:
    classify every origin/destination pair
    with either end on one of the selected scenarios' routes
    as one-seat or transfer,
    under today's routing and any number of route-override scenarios,
    all in one pass over the same fetched OD pairs.

    Unlike `one-seat-rides`,
    there's no latitude boundary and no origin-side-only corridor
    restriction--a scenario can reassign which routes serve a
    *destination* station too, e.g. Columbus Circle's stopping-pattern
    swap--and no primary/non-primary route distinction:
    any route a rider shares with their destination counts,
    even a "slower" one.
    See `deinterlining_design.md` for why.

    \b
    Examples:
        # Columbus Circle: both proposed swap directions vs. today,
        # in one run (every scenario in the "Columbus" category)
        mta-od-data analyze deinterlining --category "Columbus" \\
            --markdown-out src/mta_od_data/analyze/deinterlining_columbus_circle.md

    \b
        # DeKalb and Columbus together, over both categories' routes:
        # every pairing of one swap direction from each,
        # plus each junction's own swaps with the other left as it is today
        mta-od-data analyze deinterlining --category "DeKalb" --category "Columbus"

    \b
        # A draft catalog not yet merged into scenarios.json5
        # (--scenario-file replaces the catalog rather than adding to it)
        mta-od-data analyze deinterlining \\
            --scenario-file scratch_scenarios.json5 --category "My Category"
    """
    categories = categories or []

    days_list = (
        [d.strip() for d in days.split(",")] if days else DAY_TYPE_PRESETS[day_type]
    )
    day_type_label = (
        "/".join(d.strip() for d in days.split(",")) if days else str(day_type)
    )
    stations_by_id = Station.load_complexes(stations)
    individual_stations = Station.load_individuals(stations_individual)
    station_index = StationIndex.build(stations_by_id, individual_stations)
    try:
        comparison = resolve_scenarios(
            categories=categories,
            scenario_file=scenario_file,
            station_index=station_index,
        )
    except ScenarioError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    scenarios = comparison.scenarios
    routes_set = comparison.routes
    for s in scenarios:
        print(f"Scenario: {s.name} ({len(s.overrides)} stations overridden)")
    print(f"Route universe: {sorted(routes_set)}")
    print(f"Day filter: {days_list if days_list else 'all days'} ({day_type_label})")

    # Systemwide, but not literally every station:
    # a station only matters
    # if some scenario gives it one of the comparison's routes.
    # Either end putting a pair in scope, since a swap changes a trip
    # the same way whichever direction it runs.
    scope_ids = frozenset(
        s.complex_id
        for s in stations_by_id.values()
        if any(sc.routes_of(s) for sc in scenarios)
    )
    print(f"Stations in scope: {len(scope_ids):,} of {len(stations_by_id):,}")

    con = duckdb.connect()
    day_params: list[str] = list(days_list) if days_list else []
    day_filter_sql = (
        "TRUE"
        if not days_list
        else '"Day of Week" IN (' + ", ".join("?" for _ in days_list) + ")"
    )
    scope_id_list = ", ".join(str(i) for i in sorted(scope_ids))
    scope_filter_sql = (
        f'("Origin Station Complex ID" IN ({scope_id_list})'
        f' OR "Destination Station Complex ID" IN ({scope_id_list}))'
    )

    coverage = DayCoverage.query(con, parquet, day_filter_sql, day_params)
    n_distinct_days = coverage.n_days

    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM read_parquet(?)
        WHERE {day_filter_sql} AND {scope_filter_sql}
        GROUP BY 1, 2
    """
    pairs: list[tuple[int, int, float]] = con.execute(
        pairs_query, [str(parquet), *day_params]
    ).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter "
        f"({coverage.first_month} to {coverage.last_month})"
    )

    platforms_by_complex: dict[int, list[Station]] = {}
    for s in individual_stations:
        platforms_by_complex.setdefault(s.complex_id, []).append(s)

    # Local, since both close over per-invocation station data.
    # The cache is still shared across scenarios:
    # its keys are (dest, effective routes), nothing scenario-specific.
    @cache
    def assigned_points(assigned_routes: Routes) -> list[Station]:
        return [s for s in individual_stations if s.routes & assigned_routes]

    @cache
    def min_dist_to_corridor(
        dest: Station, assigned_routes: Routes
    ) -> tuple[float, Station] | None:
        candidates = assigned_points(assigned_routes)
        if not candidates:
            # A route with no individual-station data at all,
            # e.g. a synthetic one no scenario uses yet.
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
        dest: Station, effective_origin_routes: Routes
    ) -> tuple[bool, float | None, str | None]:
        best = min_dist_to_corridor(dest, effective_origin_routes)
        if best is None:
            return False, None, None
        dist_m, near_station = best
        close = dist_m <= close_threshold_m
        near_station_name = near_station.display(near_station.routes & routes_set)
        return close, dist_m, near_station_name

    try:
        result = comparison.classify(
            pairs=pairs,
            stations_by_id=stations_by_id,
            stations_path=stations,
            scope_ids=scope_ids,
            close_lookup=close_lookup,
        )
    except ScenarioError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    result.print_summary(close_threshold_m=close_threshold_m)
    if csv_out:
        result.write_csvs(csv_out)

    if markdown_out:
        produced_by = shlex.join([Path(sys.argv[0]).name, *sys.argv[1:]])
        preamble = "\n".join(
            [
                f"# Deinterlining scenario comparison: {','.join(sorted(routes_set))}",
                "",
                f"Average {day_type_label} ridership ({n_distinct_days} distinct "
                f"days in the data, {coverage.first_month} to "
                f"{coverage.last_month}), over every origin/destination pair "
                f"with both ends served by {','.join(sorted(routes_set))} "
                f"under any scenario compared here. Pairs with only one end "
                f"on those routes are reported alongside as context, but "
                f"can't be a one-seat ride under any of them.",
                "",
                f"Produced by `{produced_by}`.",
                "",
            ]
        )
        markdown_out.write_text(
            result.render_markdown(
                preamble=preamble,
                close_threshold_m=close_threshold_m,
                top_n=top_n,
                csv_out=csv_out,
            )
        )
        print(f"\nWrote markdown report to {markdown_out}")
