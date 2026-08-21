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
from enum import StrEnum
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
    PlatformIndex,
    Station,
    haversine_m,
)

app = Typer()

SCENARIOS_FILE = ROOT / "src" / "mta_od_data" / "analyze" / "scenarios.json5"

type Routes = frozenset[str]

# `(origin, dest, origin routes, dest routes) ->
#  (close, walk distance, station walked to, walk is at the origin)`.
# Both ends and both route sets, because the walk can be at either end;
# see `make_close_lookup`.
type CloseLookup = Callable[
    [Station, Station, Routes, Routes], tuple[bool, float, str | None, bool]
]

# Built per scenario, since which stations serve a corridor
# is exactly what a scenario changes.
type CloseLookupFactory = Callable[[Scenario], CloseLookup]


class ScenarioError(Exception):
    """Raised rather than exiting,
    so everything but `deinterlining()` itself
    stays usable as a library function."""


def table_rule(alignments: str) -> str:
    """A markdown table's header rule, `l`/`r` per column.

    Right-aligned numeric columns so a reader can compare magnitudes
    down a column at a glance.
    Alignment markers only, not padding:
    a rendered table lines up either way,
    while padding the source to the widest cell
    means one number gaining a digit repads its whole column
    and every row of a committed report shows as changed.
    """
    cells = {"l": " --- ", "r": " ---: "}
    return "|" + "|".join(cells[a] for a in alignments) + "|"


def table_row(*cells: str) -> str:
    """One markdown table row, `| |` for an empty cell.

    Not `|  |`: a cell padded on both sides of nothing
    is trailing whitespace, which markdown linters flag.
    """
    return "|" + "|".join(f" {cell} " if cell else " " for cell in cells) + "|"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "scenario"


@dataclass(slots=True, frozen=True)
class ODPair:
    origin_id: int
    # Split rather than one display string, so a scenario comparison can
    # say what changed at an end (`8 Av (N -> B)`) without taking the
    # string back apart, and so the CSV can be filtered on either.
    origin_station: str
    origin_routes: str
    dest_id: int
    dest_station: str
    dest_routes: str
    riders: float
    # Both ends served by the comparison's routes.
    # The detailed tables are scoped to these
    # (see `comparison_table_markdown`);
    # the CSV keeps every row, with this column to filter on.
    both_ends: bool
    one_seat: bool
    # Only meaningful when `one_seat` is false.
    close: bool
    # Which end the walk in `dist_m` is at.
    # Symmetric in the pair, but not a property of it:
    # which end is the shorter walk is exactly what this records.
    walk_at_origin: bool
    # 0.0 for a one-seat ride, where the ridden route stops at both ends
    # and there is no walk to model.
    dist_m: float
    near_station: str | None

    @property
    def origin_name(self) -> str:
        return f"{self.origin_station} ({self.origin_routes})"

    @property
    def dest_name(self) -> str:
        return f"{self.dest_station} ({self.dest_routes})"

    @staticmethod
    def end_label(
        station: str, routes: str, other_station: str, other_routes: str
    ) -> str:
        """One end of a pair as the baseline names it,
        carrying what a scenario does to it.

        `8 Av (N)` against `8 Av (B)` reads `8 Av (N → B)`.
        A changed-pairs row is about the change,
        and naming only today's routes
        left a reader to look up what the scenario does to that station,
        which is the one thing the row is for.

        Usually only the routes differ.
        A route move can take the narrowed platform name with it,
        though, and then there is no shared name to factor out
        and both halves are named in full.
        """
        if (station, routes) == (other_station, other_routes):
            return f"{station} ({routes})"
        if station == other_station:
            return f"{station} ({routes} → {other_routes})"
        return f"{station} ({routes}) → {other_station} ({other_routes})"


class Outcome(StrEnum):
    """What a scenario leaves a rider with.

    Three states, not two:
    losing a one-seat ride to a 200m walk
    and losing it outright
    are the same drop in the direct column
    and nothing like the same thing for a rider,
    which is why the comparison reports transitions
    and not a single signed number.
    """

    DIRECT = "direct"
    CLOSE = "close"
    FAR = "far"

    @classmethod
    def of(cls, pair: ODPair) -> Outcome:
        if pair.one_seat:
            return cls.DIRECT
        return cls.CLOSE if pair.close else cls.FAR

    @property
    def effective(self) -> bool:
        """Whether this counts towards effective one-seat."""
        return self is not Outcome.FAR


@dataclass(slots=True, frozen=True)
class Change:
    """One station pair whose outcome a scenario moved."""

    before: Outcome
    after: Outcome
    # Classified under the scenario, so its distance is the walk a rider
    # would face *after* the change.
    pair: SymmetricPair
    # `origin ↔ destination` as the baseline names them.
    label: str


@dataclass(slots=True, frozen=True)
class Transitions:
    """Where one scenario's riders end up relative to another's.

    Both scenarios classify the same `pairs` list in the same order,
    so the two `rows` lists are positionally aligned
    and a transition is a zip, not a join.
    """

    baseline_name: str
    scenario_name: str
    riders: dict[tuple[Outcome, Outcome], float]
    # Every both-ends rider, what each cell is a share of.
    total: float
    # The pairs that moved, most riders first.
    changed: list[Change]

    @classmethod
    def between(cls, baseline: ScenarioResult, result: ScenarioResult) -> Transitions:
        riders: dict[tuple[Outcome, Outcome], float] = {}
        changed_rows: list[tuple[Outcome, Outcome, ODPair]] = []
        baseline_labels: dict[tuple[int, int], str] = {}
        for before_pair, after_pair in zip(baseline.rows, result.rows, strict=True):
            assert (before_pair.origin_id, before_pair.dest_id) == (
                after_pair.origin_id,
                after_pair.dest_id,
            ), "scenario rows are not aligned"
            if not before_pair.both_ends:
                continue
            before = Outcome.of(before_pair)
            after = Outcome.of(after_pair)
            riders[before, after] = riders.get((before, after), 0.0) + after_pair.riders
            if before is not after:
                changed_rows.append((before, after, after_pair))
                baseline_labels[after_pair.origin_id, after_pair.dest_id] = f"{
                    ODPair.end_label(
                        before_pair.origin_station,
                        before_pair.origin_routes,
                        after_pair.origin_station,
                        after_pair.origin_routes,
                    )
                } ↔ {
                    ODPair.end_label(
                        before_pair.dest_station,
                        before_pair.dest_routes,
                        after_pair.dest_station,
                        after_pair.dest_routes,
                    )
                }"

        # Grouped the same way the pair tables are, so a reader comparing
        # the two isn't matching one row against two.
        by_transition: dict[tuple[Outcome, Outcome], list[ODPair]] = {}
        for before, after, pair in changed_rows:
            by_transition.setdefault((before, after), []).append(pair)
        changed = [
            Change(
                before=before,
                after=after,
                pair=symmetric,
                # Named from the baseline, since a reader knows the pair
                # by what serves it today, and a `Was direct` row
                # labelled with the scenario's routes would assert a
                # one-seat ride between route sets sharing none. Each end
                # carries what the scenario does to it (`8 Av (N -> B)`).
                label=baseline_labels[
                    symmetric.forward.origin_id, symmetric.forward.dest_id
                ],
            )
            for (before, after), pairs in by_transition.items()
            for symmetric in SymmetricPair.group(pairs)
        ]

        def changed_riders(change: Change) -> float:
            return change.pair.riders

        changed.sort(key=changed_riders, reverse=True)
        return cls(
            baseline_name=baseline.scenario.name,
            scenario_name=result.scenario.name,
            riders=riders,
            total=sum(riders.values()),
            changed=changed,
        )

    def cell(self, before: Outcome, after: Outcome) -> float:
        return self.riders.get((before, after), 0.0)

    def pct(self, riders: float) -> str:
        """Shares of the same both-ends total the comparison table uses,
        so a matrix cell and a table column are read against the same
        denominator."""
        if not self.total:
            return "0.0%"
        return f"{100 * riders / self.total:.1f}%"

    @property
    def gained(self) -> float:
        return sum(
            v
            for (before, after), v in self.riders.items()
            if not before.effective and after.effective
        )

    @property
    def lost(self) -> float:
        return sum(
            v
            for (before, after), v in self.riders.items()
            if before.effective and not after.effective
        )

    @property
    def net(self) -> float:
        return self.gained - self.lost

    def markdown(self, *, h2: str, top_n: int, close_threshold_m: float) -> str:
        order = list(Outcome)
        lines = [
            f"{h2} What Changed, against {self.baseline_name}",
            "",
            f"Every both-ends rider, and their share of the "
            f"{self.total:,.0f} of them: **was** is what "
            f"{self.baseline_name} gives them, **now** what "
            f"{self.scenario_name} would. Off-diagonal cells are the whole "
            f"effect of the swap; the diagonal is everyone it leaves alone. "
            f"`direct` is a one-seat ride, `close` a one-seat ride after a "
            f"walk of {close_threshold_m:.0f}m or less, `far` neither.",
            "",
            # Each label carries its own axis, rather than a corner cell
            # naming both and leaving the reader to apply it.
            # `was`/`now` are the words the changed-pairs table below
            # already uses for the same two states.
            "| Riders | " + " | ".join(f"now {o}" for o in order) + " |",
            table_rule("l" + "r" * len(order)),
        ]
        for before in order:
            lines.append(
                table_row(
                    f"**was {before}**",
                    *(
                        f"{self.cell(before, after):,.0f} "
                        f"({self.pct(self.cell(before, after))})"
                        for after in order
                    ),
                )
            )
        lines += [
            "",
            f"- **Gained an effective one-seat ride: {self.gained:,.0f} "
            f"({self.pct(self.gained)})**",
            f"- **Lost one: {self.lost:,.0f} ({self.pct(self.lost)})**",
            f"- **Net: {self.net:+,.0f} ({self.pct(self.net)})**",
            "",
        ]

        if self.changed:
            lines += [
                f"{h2} Biggest Changes, against {self.baseline_name}",
                "",
                f"The top {top_n} station pairs by riders whose outcome "
                f"moved, both directions combined as above. An end reads "
                f"`today → {self.scenario_name}` where its routes change, "
                f"and today's alone where they don't; `Dist` is the walk "
                f"under {self.scenario_name}.",
                "",
                "| # | Riders | Was | Now | Dist | Origin ↔ Destination |",
                table_rule("rrllrl"),
            ]
            for i, change in enumerate(self.changed[:top_n], 1):
                fwd = change.pair.forward
                dist = "" if fwd.one_seat else f"{fwd.dist_m:.0f}m"
                lines.append(
                    table_row(
                        str(i),
                        f"{change.pair.riders:,.0f}",
                        str(change.before),
                        str(change.after),
                        dist,
                        change.label,
                    )
                )
            lines.append("")
        return "\n".join(lines)


@dataclass(slots=True, frozen=True)
class SymmetricPair:
    """Both directions of one station pair, as a single row.

    A swap changes a trip the same way whichever way it runs,
    so listing A->B and B->A separately
    spent two of the top N slots on one fact,
    and buried the pair that would otherwise have been last.

    Every classification here is symmetric--`one_seat` because a shared
    route is a shared route, `close`/`dist_m` because a rider can walk
    at either end (see `close_lookup`)--so the two directions differ
    only in their rider counts, and `forward`'s classification stands
    for the pair.

    `forward` is the busier direction, so the arrow points the way most
    riders travel; `reverse` is `None` for a pair the data only has one
    way round, and for a trip that starts and ends at one complex.
    """

    forward: ODPair
    reverse: ODPair | None

    @property
    def riders(self) -> float:
        return self.forward.riders + (
            self.reverse.riders if self.reverse is not None else 0.0
        )

    @classmethod
    def group(cls, rows: list[ODPair]) -> list[SymmetricPair]:
        by_ends: dict[frozenset[int], list[ODPair]] = {}
        for row in rows:
            by_ends.setdefault(frozenset((row.origin_id, row.dest_id)), []).append(row)

        def row_riders(row: ODPair) -> float:
            return row.riders

        pairs: list[SymmetricPair] = []
        for directions in by_ends.values():
            forward, *rest = sorted(directions, key=row_riders, reverse=True)
            pairs.append(cls(forward=forward, reverse=rest[0] if rest else None))
        return pairs


@dataclass(slots=True)
class EndStats:
    """One end of a trip--an origin or a destination--summed over every
    trip with the other end anywhere.
    The same shape either way,
    since a pair contributes its one classification to both of its ends."""

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
        # A category left unchanged contributes nothing to the name:
        # "Current + A/C CPW Express" and "A/C CPW Express" describe the
        # same routing, and the longer one gets longer with every
        # category selected. Only when *every* category is unchanged is
        # there nothing else to say, and then it's `Current` once rather
        # than "Current + Current".
        # By identity, not by an empty `overrides`: a scenario file is
        # free to declare one that happens to change nothing, and that
        # one still has a name worth printing.
        changed = [s for s in scenarios if s is not CURRENT]
        named = changed or [CURRENT]
        return cls(
            name=" + ".join(s.name for s in named),
            description=" + ".join(s.description for s in named),
            category=" + ".join(s.category for s in named),
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
        platforms: PlatformIndex,
        close_lookup: CloseLookup,
    ) -> ScenarioResult:
        rows: list[ODPair] = []
        total_riders = 0.0
        one_seat_riders = 0.0
        close_riders = 0.0
        both_total = 0.0
        both_one_seat = 0.0
        both_close = 0.0
        origin_stats: dict[int, EndStats] = {}
        dest_stats: dict[int, EndStats] = {}
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
            origin_station = platforms.name(origin, effective_origin_routes)
            dest_station = platforms.name(dest, effective_dest_routes)
            origin_routes = ",".join(sorted(effective_origin_routes))
            dest_routes = ",".join(sorted(effective_dest_routes))
            one_seat = bool(effective_origin_routes & effective_dest_routes)

            both_ends = origin_id in scope_ids and dest_id in scope_ids
            total_riders += riders
            if both_ends:
                both_total += riders
            if one_seat:
                one_seat_riders += riders
                if both_ends:
                    both_one_seat += riders
                close, dist_m, near_station_name = False, 0.0, None
                walk_at_origin = False
            else:
                close, dist_m, near_station_name, walk_at_origin = close_lookup(
                    origin,
                    dest,
                    effective_origin_routes,
                    effective_dest_routes,
                )
                if close:
                    close_riders += riders
                    if both_ends:
                        both_close += riders

            pair = ODPair(
                origin_id=origin_id,
                origin_station=origin_station,
                origin_routes=origin_routes,
                dest_id=dest_id,
                dest_station=dest_station,
                dest_routes=dest_routes,
                riders=riders,
                both_ends=both_ends,
                one_seat=one_seat,
                close=close,
                walk_at_origin=walk_at_origin,
                dist_m=dist_m,
                near_station=near_station_name,
            )
            rows.append(pair)

            # Both-ends only, to match the tables these feed:
            # a station off the comparison's routes has no one-seat
            # ridership to or from anywhere, so it would only ever add
            # rows reading 0.0%.
            if both_ends:
                # The pair rows' own labels, not a second naming of the
                # same stations: displaying every real route here
                # (`Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W)`) gave
                # one report two conventions, and named the station by
                # routes no row in it is about.
                for stats, sid, name in (
                    (origin_stats, origin_id, pair.origin_name),
                    (dest_stats, dest_id, pair.dest_name),
                ):
                    e = stats.setdefault(sid, EndStats(name=name))
                    e.total += riders
                    if one_seat:
                        e.one_seat += riders
                    elif close:
                        e.close += riders

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
            origin_stats=origin_stats,
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

    def markdown_row(self, label: str, baseline: RiderStats | None = None) -> str:
        """`baseline` adds each column's change against it,
        saving the reader the subtraction.
        `None` for the baseline's own row, which has nothing to differ
        from."""

        def cell(value: float, base: float | None) -> str:
            level = f"{value:,.0f} ({self.pct(value):.1f}%)"
            if base is None:
                return level
            # `pct` of the change, not the change in `pct`:
            # identical either way, every scenario classifying the same
            # pairs and so sharing a total, and this one can't drift if
            # that ever stops being true without the subtraction below
            # becoming meaningless first.
            delta = value - base
            return f"{level}, {delta:+,.0f} ({self.pct(delta):+.1f}%)"

        one_seat, close, effective = (
            (None, None, None)
            if baseline is None
            else (baseline.one_seat, baseline.close, baseline.effective)
        )
        return table_row(
            label,
            f"{self.total:,.0f}",
            cell(self.one_seat, one_seat),
            cell(self.close, close),
            cell(self.effective, effective),
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
    origin_stats: dict[int, EndStats]
    dest_stats: dict[int, EndStats]

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
        transitions: Transitions | None = None,
    ) -> str:
        h2 = "###" if show_label else "##"
        t = self.both_ends
        lines: list[str] = [f"## {self.scenario.name}", ""] if show_label else []

        # Only without a comparison table above, which says all of this
        # for every scenario at once.
        if not show_label:
            lines += [
                f"{h2} Headline Numbers",
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

        if transitions is not None:
            lines.append(
                transitions.markdown(
                    h2=h2, top_n=top_n, close_threshold_m=close_threshold_m
                )
            )

        lines += [
            f"{h2} Top {top_n} Origin/Destination Pairs",
            "",
            "Both ends on the comparison's routes, per that section of the "
            "comparison above. Each row is both directions of one station "
            "pair, their riders summed, oriented so the arrow points the "
            "way more of them travel. Every column but the riders is "
            "symmetric, so one value covers both directions; `Walk` names the "
            "station the shorter walk reaches, and the end it is at.",
            "",
            "| # | Riders | % Total | Type | Close? | Dist | Walk | "
            "Origin ↔ Destination |",
            table_rule("rrrllrll"),
        ]

        def pair_riders(pair: SymmetricPair) -> float:
            return pair.riders

        both_ends_rows = [r for r in self.rows if r.both_ends]
        top_pairs = sorted(
            SymmetricPair.group(both_ends_rows), key=pair_riders, reverse=True
        )[:top_n]
        for i, pr in enumerate(top_pairs, 1):
            fwd = pr.forward
            if fwd.one_seat:
                type_str, close_str, dist_str, walk_str = "1-seat", "", "", ""
            else:
                type_str = "xfer"
                close_str = "close" if fwd.close else "far"
                dist_str = f"{fwd.dist_m:.0f}m"
                # The station walked *to*, which is the actionable half,
                # tagged with the end it's at rather than an arrow, so it
                # reads the same whichever way the row is oriented.
                end = "origin" if fwd.walk_at_origin else "dest"
                walk_str = f"{end}: {fwd.near_station}"
            lines.append(
                table_row(
                    str(i),
                    f"{pr.riders:,.0f}",
                    f"{self.both_ends.pct(pr.riders):.2f}%",
                    type_str,
                    close_str,
                    dist_str,
                    walk_str,
                    f"{fwd.origin_name} ↔ {fwd.dest_name}",
                )
            )
        lines.append("")

        def end_total(e: EndStats) -> float:
            return e.total

        # Origins and destinations both, and not one table standing in for
        # the other: a station's one-seat share is not symmetric, since
        # "close one-seat" measures the *destination* against the origin's
        # corridor. A terminal that reads well as an origin can read badly
        # as a destination.
        for label, end, stats in (
            ("origin", "destinations", self.origin_stats),
            ("destination", "origins", self.dest_stats),
        ):
            lines += [
                f"{h2} Top {top_n} {label.capitalize()} Stations, "
                f"Summed across All {end.capitalize()}",
                "",
                "Both ends on the comparison's routes, per that section of "
                "the comparison above.",
                "",
                f"| Riders | 1-Seat % | Effective % | {label.capitalize()} |",
                table_rule("rrrl"),
            ]
            for e in sorted(stats.values(), key=end_total, reverse=True)[:top_n]:
                one_seat_pct = 100 * e.one_seat / e.total if e.total else float("nan")
                effective_pct = (
                    100 * (e.one_seat + e.close) / e.total if e.total else float("nan")
                )
                lines.append(
                    table_row(
                        f"{e.total:,.0f}",
                        f"{one_seat_pct:.1f}%",
                        f"{effective_pct:.1f}%",
                        e.name,
                    )
                )
            lines.append("")

        if csv_out:
            lines.append(
                f"_Full row-level detail (one row per direction, every "
                f"origin/destination pair with either end on the routes, "
                f"not just the top {top_n}): `{csv_out}`, whose `both_ends` "
                f"column is what the tables above filter on._"
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
        platforms: PlatformIndex,
        close_lookup_factory: CloseLookupFactory,
    ) -> ScenarioComparisonResult:
        return ScenarioComparisonResult(
            comparison=self,
            results=[
                scenario.classify(
                    pairs=pairs,
                    stations_by_id=stations_by_id,
                    stations_path=stations_path,
                    scope_ids=scope_ids,
                    platforms=platforms,
                    close_lookup=close_lookup_factory(scenario),
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
    def baseline(self) -> ScenarioResult:
        """Today's routing, which every change is reported against.
        `combine_scenarios` puts `CURRENT` first in every category's
        options, so the all-unchanged combination is the first result."""
        baseline = self.results[0]
        # By its overrides, not its name: the name is a label, while
        # "overrides nothing" is what makes a scenario today's routing.
        assert not baseline.scenario.overrides, (
            f"expected an unchanged baseline first, got "
            f"{baseline.scenario.name!r} with "
            f"{len(baseline.scenario.overrides)} station(s) overridden"
        )
        return baseline

    def transitions(self, result: ScenarioResult) -> Transitions | None:
        """`None` for the baseline itself, which cannot differ from
        itself."""
        if result is self.baseline:
            return None
        return Transitions.between(self.baseline, result)

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
        print(f"\n=== Effective one-seat against {self.baseline.scenario.name} ===")
        for r in self.results:
            t = self.transitions(r)
            if t is None:
                continue
            print(
                f"  {r.scenario.name:<55} gained={t.gained:>8,.0f}  "
                f"lost={t.lost:>8,.0f}  net={t.net:>+9,.0f}"
            )

    def write_csvs(self, csv_out: Path) -> None:
        for path, result in zip(self.csv_paths(csv_out), self.results, strict=True):
            assert path is not None
            result.write_csv(path)

    def comparison_table_markdown(self, *, close_threshold_m: float) -> str:
        routes = ",".join(sorted(self.comparison.routes))
        header = (
            "| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | "
            "Effective 1-Seat |\n" + table_rule("lrrrr")
        )

        # Both ends first, and every detailed table below scoped to it:
        # it's the denominator a reader needs, the trips these routes could
        # carry end to end. Trips with only one end on them can never be a
        # one-seat ride under any scenario (that needs a shared route, which
        # puts both ends in scope), so they only ever dilute the rate.
        # Two cuts of one classification, as sibling `###` tables:
        # neither is *the* number, they answer different questions,
        # and nesting one under the other implied a precedence
        # that isn't there.
        # Both-ends comes first because it's the denominator the
        # detailed tables below are scoped to.
        lines = [
            "## Scenario Comparison",
            "",
            f"Two cuts of the same classification. Neither is the whole "
            f"answer: the first says what a scenario does to the riders it "
            f"can reach, the second how much of the system it reaches at "
            f"all. In both, only how many riders get a one-seat ride "
            f"changes between scenarios, never the total. Close one-seat "
            f"counts a transfer trip whose destination is within "
            f"{close_threshold_m:.0f}m of a station on that scenario's "
            f"effective origin corridor.",
            "",
            "### Both Ends on the Comparison's Routes",
            "",
            f"The {self.results[0].both_ends.total:,.0f} riders whose origin "
            f"*and* destination are served by {routes}: the trips these "
            f"routes could carry end to end, including the many that keep a "
            f"one-seat ride whatever the scenario. Every table below is "
            f"scoped to these.",
            "",
            header,
        ]
        for r in self.results:
            lines.append(
                r.both_ends.markdown_row(
                    r.scenario.name,
                    None if r is self.baseline else self.baseline.both_ends,
                )
            )

        lines += [
            "",
            "### Either End on the Comparison's Routes",
            "",
            f"The wider {self.results[0].overall.total:,.0f} riders with "
            f"*either* end served by {routes}, the above among them. The "
            f"difference is transfer trips with one end off these routes "
            f"entirely, which no scenario here can change: they can only "
            f"dilute the rate, which is why a junction's effect washes out "
            f"against this total.",
            "",
            header,
        ]
        for r in self.results:
            lines.append(
                r.overall.markdown_row(
                    r.scenario.name,
                    None if r is self.baseline else self.baseline.overall,
                )
            )
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
                    transitions=self.transitions(result),
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

    platform_index = PlatformIndex.build(individual_stations)
    platforms_by_complex: dict[int, list[Station]] = {}
    for s in individual_stations:
        platforms_by_complex.setdefault(s.complex_id, []).append(s)

    # Built per scenario, and local, since these close over
    # per-invocation station data.
    # Per scenario is the whole point: which stations serve a corridor
    # is exactly what a scenario changes, so a lookup shared across
    # scenarios answers with today's routes under every one of them.
    def make_close_lookup(scenario: Scenario) -> CloseLookup:
        @cache
        def corridor_platforms(corridor_routes: Routes) -> list[Station]:
            """The platforms a rider could board this corridor at,
            under this scenario.

            Membership is decided at the *complex* level, since that's
            the granularity a scenario's overrides are declared and
            resolved at, but the platforms themselves are what's
            returned: a complex can span physically separate stations
            (Times Sq-42 St/Port Authority), and its centroid can sit
            well away from any actual platform.
            """
            return [
                platform
                for platform in individual_stations
                if scenario.routes_of(stations_by_id[platform.complex_id])
                & corridor_routes
            ]

        @cache
        def min_dist_to_corridor(
            station: Station, corridor_routes: Routes
        ) -> tuple[float, Station] | None:
            candidates = corridor_platforms(corridor_routes)
            if not candidates:
                # Either the station has no route in this comparison at
                # all (so there is no corridor of its own to measure
                # against), or a route has no individual-station data,
                # e.g. a synthetic one no scenario uses yet.
                # The caller decides what an unmeasurable end means;
                # here it's just "nothing to measure to".
                return None
            points = [
                s.loc for s in platforms_by_complex.get(station.complex_id, [station])
            ]
            best: tuple[float, Station] | None = None
            for p in points:
                for c in candidates:
                    dist_m = haversine_m(p, c.loc)
                    if best is None or dist_m < best[0]:
                        best = (dist_m, c)
            return best

        def close_lookup(
            origin: Station,
            dest: Station,
            origin_routes: Routes,
            dest_routes: Routes,
        ) -> tuple[bool, float, str | None, bool]:
            """How far a rider without a one-seat ride would have to walk
            to turn the trip into one, at whichever end is the shorter walk.

            Two ways to do that, and a rider can take either:

            - walk at the destination end: ride your own corridor to the
              station nearest the destination, and walk from there;
            - walk at the origin end: walk to the nearest station served
              by a route that reaches the destination, and ride that.

            Taking the minimum makes the result symmetric,
            which the underlying fact is:
            `A -> B` and `B -> A` offer the same two walks,
            so they must classify alike.
            """
            options = [
                (min_dist_to_corridor(dest, origin_routes), False),
                (min_dist_to_corridor(origin, dest_routes), True),
            ]
            measured = [
                (best, at_origin) for best, at_origin in options if best is not None
            ]
            # Both ends unmeasurable means neither end is on the
            # comparison's routes, which `scope_ids` already excluded
            # from the query.
            # Loud rather than silently `far`, per the same argument as
            # `one_seat_rides.py`'s `assert candidates`.
            assert measured, (
                f"neither {origin.name} nor {dest.name} has a corridor to "
                f"measure a walk against, but the pair was fetched as in scope"
            )

            def walk_dist(option: tuple[tuple[float, Station], bool]) -> float:
                return option[0][0]

            (dist_m, near_station), walk_at_origin = min(measured, key=walk_dist)
            close = dist_m <= close_threshold_m
            near_complex = stations_by_id[near_station.complex_id]
            near_station_name = platform_index.display(
                near_complex, scenario.routes_of(near_complex)
            )
            return close, dist_m, near_station_name, walk_at_origin

        return close_lookup

    try:
        result = comparison.classify(
            pairs=pairs,
            stations_by_id=stations_by_id,
            stations_path=stations,
            scope_ids=scope_ids,
            platforms=platform_index,
            close_lookup_factory=make_close_lookup,
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
                f"# Deinterlining Scenario Comparison: {','.join(sorted(routes_set))}",
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
