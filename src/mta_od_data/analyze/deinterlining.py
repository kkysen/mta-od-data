"""Systemwide deinterlining scenario comparator.

See `deinterlining_design.md` (next to this file) for the design this
implements. Deliberately kept independent of `one_seat_rides.py` --
duplicates a couple of small helpers (the CSV/markdown rendering shape,
nearest-station search) rather than importing them, since the user
doesn't want that module touched until this one is proven out;
reconcile the duplication if/when the two get merged.

Unlike `one_seat_rides.py` (one latitude boundary, two named corridors
converging into two named trunks, origin-side reassignment only), this
classifies *every* origin/destination pair whose origin could plausibly
use one of the run's routes (under any scenario being compared) -- no
boundary, same shape as `regional_flow.py`'s unfiltered OD-pairs query
-- comparing one-seat-ride share across today's real routes and any
number of scenarios' route overrides. Those routes come from the
scenarios themselves (each declares its own, unioned across the run --
see `ScenarioRun`), not from the command line.

"Today" is not a special case: it's the `CURRENT` scenario, a `Scenario`
with no overrides, classified through the exact same code path as every
other scenario. Selecting several scenarios via `--category`
classifies all of them (plus `Current`) against the *same* fetched OD
pairs in one run, so comparing several proposals doesn't reclassify
"today" once per proposal. Selecting more than one category at once
combines them -- see `Scenario.combine`/`resolve_scenarios` -- for
comparing compound proposals across independent junctions, not just each
junction's proposals in isolation.
"""

import csv
import itertools
import json
import re
import shlex
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from datetime import date
from functools import cache
from pathlib import Path
from typing import Annotated, Any

import duckdb
import json5
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError
from typer import Option, Typer

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import DAY_TYPE_PRESETS, DayType, Station, haversine_m

app = Typer()

SCENARIOS_FILE = ROOT / "src" / "mta_od_data" / "analyze" / "scenarios.json5"

# A set of route letters (e.g. `{"A", "C"}`), not a single station's or
# pair's routes specifically -- named for what it holds, not where it's
# used, since it shows up as a station's actual routes, a scenario's
# effective routes, and a run's whole route universe alike.
type Routes = frozenset[str]


class ScenarioError(Exception):
    """Raised for a scenario/CLI-input problem that only `deinterlining()`
    (the CLI command) should turn into a printed error and `SystemExit` --
    every other method here raises this instead of exiting directly, so
    it stays usable as a library function."""


def slugify(name: str) -> str:
    """A scenario's `name` (e.g. "Columbus A/C Express") isn't safe as a
    filename suffix (spaces, `/`) -- this derives one that is, for
    `suffixed_path`."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "scenario"


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
class RouteDelta:
    """A scenario's change to one station's real routes, as an explicit
    add/remove pair rather than a full replacement list -- so a scenario
    author only has to say what actually changes (e.g. "the B stops
    running here"), not re-derive and spell out every route that's
    unaffected. `apply` applies `remove` before `add`, so listing a route
    in both is equivalent to just `add`."""

    add: Routes
    remove: Routes

    def __or__(self, other: RouteDelta) -> RouteDelta:
        """Two deltas for the same station -- from two override groups in
        one `ScenarioEntry`, or two scenarios being combined -- union
        cleanly: `add`/`remove` are each just sets, so there's no real
        conflict to detect, even when one delta's `add` is another's
        `remove` (`apply`'s remove-before-add order already means add
        wins for a single delta; unioning preserves that). `|`, not a
        named method, since it's exactly `add`/`remove` each unioned with
        `|` in turn."""
        return RouteDelta(add=self.add | other.add, remove=self.remove | other.remove)

    def apply(self, station: Station) -> Routes:
        return (station.routes - self.remove) | self.add


class OverrideGroup(BaseModel):
    """One override group in a scenario file's `overrides` array: an
    add/remove pair shared by every station in `stations` -- the usual
    case, since a deinterlining change typically affects several stations
    on one line the same way. `line` (e.g. "8th Av - Fulton St", from the
    individual-station reference data) is required on every group: it
    disambiguates a `stations` entry whose bare name is shared by more
    than one real complex elsewhere in the system (see
    `StationIndex.resolve`), and lets a reader tell which physical line a
    group's `add`/`remove` applies to without cross-referencing
    `stations_individual.csv`, even when every name here happens to
    already be unique on its own."""

    model_config = ConfigDict(extra="forbid")

    line: str = Field(min_length=1)
    add: list[str] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list)
    stations: list[str] = Field(min_length=1)


class ScenarioEntry(BaseModel):
    """One scenario in a scenario file's top-level JSON object (see
    `SCENARIO_FILE_ADAPTER`), grouped under its category's key rather than
    carrying its own `category` field. `name` is a short identifier, used
    for dedup and as this scenario's CSV-suffix/label when several are
    compared in one run; `description` defaults to `name` when omitted.

    `routes` is the route universe this scenario is about (e.g. A,B,C,D
    for a Columbus Circle swap): which routes a rider can be considered
    to have a one-seat ride on, and which stations are origins worth
    classifying at all. It lives here rather than on the command line
    because it's a property of the scenario -- a Columbus swap is about
    the same four routes no matter who runs it -- and every route the
    scenario moves must be in it (`Scenario.load`), so it can't silently
    disagree with the scenario's own `add`/`remove`. A run selecting
    several categories classifies every scenario under the union of
    theirs, so the comparison stays like-for-like; see `ScenarioRun`."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    description: str | None = None
    routes: list[str] = Field(min_length=1)
    overrides: list[OverrideGroup] = Field(default_factory=list)


# The root of a scenario file: a JSON object mapping a category name to
# the `ScenarioEntry`s in it (e.g. `"Columbus"` to that junction's swap
# directions) -- `--category` selects by this key directly. A
# category's list can't be empty (`min_length=1`): `resolve_scenarios`'s
# cartesian product over selected categories would otherwise silently
# produce zero combined scenarios for an empty one, with no error at all.
# Also what `scenarios.schema.json` is generated from -- see
# `tests/test_scenarios_schema.py`.
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
    """The JSON Schema for a scenario file, generated from
    `SCENARIO_FILE_ADAPTER` (i.e. from `OverrideGroup`/`ScenarioEntry`
    directly) plus the top-level metadata a standalone schema file needs
    (`$schema`, `title`), plus real `line`/`stations`/`add`/`remove`
    values from the station reference data as JSON Schema `enum`s -- an
    editor can then autocomplete (and flag a typo in) an actual line,
    station name, or route directly while editing a scenario file,
    without cross-referencing the CSVs by hand. These `enum`s are an
    editor-time snapshot only: `OverrideGroup`/`ScenarioEntry` themselves
    stay plain `str`, so a real load still goes through
    `StationIndex.resolve`/`check_routes`'s own runtime checks (against
    whichever `--stations`/`--stations-individual` was actually passed,
    not necessarily these defaults) rather than trusting this baked-in
    list -- the two can disagree (e.g. a rider count run against an older
    station extract) without either one being wrong for its own purpose.

    `stations_path`/`individual_stations_path` aren't committed
    (gitignored, `mta-od-data prepare`-generated) -- see the
    `pytest.mark.skipif` in `tests/test_scenarios_schema.py`, which skips
    rather than fails when they're missing. What `scenarios.schema.json`
    must always equal when they *are* present -- regenerate it with:

        uv run python -c "from mta_od_data.analyze.deinterlining import \\
            SCENARIOS_SCHEMA_FILE, generate_scenario_schema; \\
            SCENARIOS_SCHEMA_FILE.write_text(generate_scenario_schema())"
    """
    stations_by_id = Station.load_complexes(stations_path)
    individual_stations = Station.load_individuals(individual_stations_path)
    known_lines = sorted({s.line for s in individual_stations if s.line})
    # A `stations` entry always resolves against an individual platform's
    # own name plus `line` (`StationIndex.by_name_line`), never a
    # complex's own name -- `line` is required on every `OverrideGroup`,
    # so the complex-level name (e.g. "62 St/New Utrecht Av", merging
    # "62 St" and "New Utrecht Av") is never what's actually checked.
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
    """Resolves a scenario override's (station name, line) to a `Station`,
    and checks an override's `add`/`remove` routes against the real route
    universe. Keyed by (individual platform name, line) rather than a
    complex's own name -- `line` is required on every `OverrideGroup` (see
    its docstring), so a bare-name lookup with no line is never actually
    needed: station names alone aren't unique (e.g. "72 St" is three
    different real complexes: CPW, Broadway-7 Av, and 2 Av), and `line`
    (e.g. "8th Av - Fulton St", from the individual-station reference
    data) always resolves which one is meant instead. Built once per
    invocation from the same station reference data used everywhere else,
    not a separate lookup source."""

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
        """Only a scenario's own `routes` needs checking against the real
        route universe: `Scenario.load` requires every `add`/`remove`
        route to be in it, so an unknown route anywhere in a scenario
        surfaces here rather than needing its own near-identical check."""
        unknown = sorted(routes - self.known_routes)
        if unknown:
            raise ScenarioError(
                f'scenario {path}: scenario "{name}" lists unknown route(s) '
                f'{unknown} in "routes" (not in the station reference data)'
            )


@dataclass(slots=True, frozen=True)
class Scenario:
    """A deinterlining scenario: real routes overridden only for the
    specific stations it actually changes -- see `deinterlining_design.md`
    for why this replaces `one_seat_rides.py`'s corridor-A/corridor-B
    machinery instead of extending it.

    `name` is a short identifier (e.g. "A/C CPW Express"); `description`
    is the longer explanatory text. `category` is the scenario file key
    this scenario was loaded from (e.g. "Columbus" for every Columbus
    Circle swap direction) -- `--category` selects by it, the only way to
    select a scenario besides always-included `Current`."""

    name: str
    description: str
    category: str
    # The route universe this scenario classifies under -- everything
    # here is already narrowed to it, so nothing downstream intersects
    # again. On a scenario as loaded from a file, it's that entry's own
    # `routes`; on a combined one (`combine`, what a run actually
    # classifies with) it's the whole run's universe, so every row of a
    # comparison covers the same routes. Empty only on `CURRENT`, which
    # is unrestricted until it's combined into a run.
    routes: Routes
    # Keyed by `Station` itself, not `complex_id` -- `Station` is frozen
    # (so hashable), letting every consumer here look a station up
    # directly instead of needing an indirection through its id.
    overrides: dict[Station, RouteDelta]
    # A station absent from `overrides` (the overwhelming majority of
    # them) has no entry here either -- `routes_of` falls back to the
    # station's own real routes, rather than this dict carrying a
    # redundant real-routes entry for every unaffected station. Computed
    # once in `load`/`combine`, from `overrides` alone -- no station
    # population (e.g. `stations_by_id`) needed -- and already narrowed
    # to `routes`, so `routes_of` is the only place that narrowing lives.
    effective_routes: dict[Station, Routes]

    def slug(self) -> str:
        """Names this scenario's own suffixed CSV file when several are
        compared in one run (see `suffixed_path`). Derived from `name`
        every time it's asked for, rather than stored alongside it, so
        there's nothing that can fall out of sync with it."""
        return slugify(self.name)

    def routes_of(self, station: Station) -> Routes:
        """This scenario's routes for `station`, within its universe: its
        override if it has one, otherwise the station's real routes. The
        `& self.routes` on the fallback is what `effective_routes`
        already baked into every override, so both sides come out
        narrowed the same way."""
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
            # A scenario that moves a route its own universe leaves out
            # would be classified as if that move never happened -- the
            # narrowing to `routes` drops it right back out again -- so
            # it's a scenario-file mistake, not a subtlety to document.
            outside = sorted((add | remove) - routes)
            if outside:
                raise ScenarioError(
                    f'scenario {path}: scenario "{entry.name}" adds/removes '
                    f"route(s) {outside} outside its own routes "
                    f"{sorted(routes)} -- a scenario's routes must cover "
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
        """Merges several scenarios -- one per category in a
        `resolve_scenarios` cartesian-product combination -- into one:
        `overrides` is their union (two scenarios touching the same
        station combine via `RouteDelta.__or__`, same as two override
        groups within one `ScenarioEntry`), `name`/`description`/
        `category` are each `" + "`-joined.

        `routes` is the whole run's universe, not the union of these
        scenarios' own: every combination in a run has to classify under
        the same routes for their totals to be comparable. That's also
        why a single-element `scenarios` isn't returned as-is -- its
        `effective_routes` is still narrowed to its own declared routes,
        which the run's universe may be wider than."""
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
        close_lookup: Callable[[Station, Routes], tuple[bool, float, str | None]],
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

            effective_origin_routes = self.routes_of(origin)
            effective_dest_routes = self.routes_of(dest)
            origin_name = origin.display(effective_origin_routes)
            dest_name = dest.display(effective_dest_routes)
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
                    origin_name=origin_name,
                    dest_id=dest_id,
                    dest_name=dest_name,
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

        if not total_riders:
            raise ScenarioError(
                f"scenario {self.name!r}: no ridership among the fetched "
                f"origin/destination pairs -- nothing to classify (check "
                f"the selected scenarios' routes and the day filter)"
            )

        return ScenarioResult(
            scenario=self,
            total_riders=total_riders,
            one_seat_riders=one_seat_riders,
            close_riders=close_riders,
            rows=rows,
            dest_stats=dest_stats,
        )


# Today's real routing: the one scenario that isn't authored in a
# scenario file at all. It's a scenario with no overrides -- there's
# nothing for an author to write, and requiring an empty entry in every
# ad-hoc `--scenario-file` was pure ceremony -- but it's still classified
# through the exact same code path as every other scenario, never as a
# special case.
#
# It's also the one scenario with no route universe of its own: today's
# routing isn't about any particular set of routes, so it adopts
# whichever ones the run it's compared in is about (see `ScenarioRun`),
# rather than declaring a superset by hand.
#
# A constant rather than a factory: nothing ever mutates a `Scenario`'s
# `overrides`/`effective_routes` (`load`/`combine` each build their own),
# so one shared instance is as good as a fresh one per run.
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
    """Every scenario loaded under one category key in a scenario file's
    top-level JSON object (e.g. "DeKalb", grouping its swap-direction
    scenarios) -- one element of `ScenarioFile.categories`. Selecting more
    than one category at once takes the cartesian product of their
    `scenarios` (one scenario per selected category per combination,
    "unchanged" -- the `CURRENT` scenario -- being one of the options for
    every category), each combination merged into a single scenario
    by `Scenario.combine` -- see `ScenarioFile.combine_scenarios`."""

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
    """Every category in one scenario file (`path`, e.g. `scenarios.json5`
    or an ad-hoc `--scenario-file`) -- what `load` parses the whole file
    into. `filter` narrows to the named categories (raising
    `ScenarioError` for any that don't exist), preserving `categories`'
    own order rather than the order they were requested in.
    `combine_scenarios` takes the cartesian product of `categories`'
    `scenarios` (plus the baseline it's passed, as an option for every
    category) and merges each combination via `Scenario.combine`.
    `resolve_scenarios` composes these: `filter` to the `--category`
    selection, then combine it against the `CURRENT` scenario as the
    baseline."""

    path: Path
    categories: list[ScenarioCategory]

    @classmethod
    def load(cls, path: Path, station_index: StationIndex) -> ScenarioFile:
        """A scenario file holds a JSON object of category name to the
        `ScenarioEntry`s in it, not just one -- `--scenario-file` (the
        catalog) defines several related scenarios, across several
        categories, together."""
        # JSON5 (a strict superset of JSON): tolerates a trailing comma
        # before a closing `}`/`]`, an easy slip when hand-editing scenario
        # files -- plain `json.loads` would reject it outright.
        try:
            data = json5.loads(path.read_text())
        except ValueError as e:
            raise ScenarioError(f"scenario file {path} isn't valid JSON: {e}") from e
        # `ScenarioEntry`/`OverrideGroup` (both `pydantic.BaseModel`s) own
        # the shape validation here -- a required field missing, an unknown
        # field (`extra="forbid"`), or a wrong type all become one
        # `ValidationError`, so there's no manual field-by-field checking
        # to keep in sync with the schema (`scenarios.schema.json`, itself
        # generated from these same models).
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
        """Every route any scenario in this file's categories is about --
        the run's universe once `filter`ed down to the selected
        categories. See `ScenarioRun` for why one universe covers the
        whole run rather than each scenario keeping its own."""
        return frozenset(
            route
            for category in self.categories
            for scenario in category.scenarios
            for route in scenario.routes
        )

    def combine_scenarios(self, baseline: list[Scenario]) -> list[Scenario]:
        """`baseline` (the `CURRENT` scenario) joins *every*
        category's own options, rather than standing alone as one more
        combination: leaving a category unchanged is itself one of the
        choices for it, so selecting two categories with two scenarios
        each yields nine combinations (three options per category), not
        four -- each category's scenarios on their own (the other left at
        today's routing) included, not just every proposal paired with
        another proposal.

        Every combination is built against this file's `routes` -- one
        universe for the whole run, `baseline` (which has none of its
        own) included."""
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
        # `total_riders` is never 0 here: `Scenario.classify` raises
        # `ScenarioError` before constructing a `ScenarioResult` with one,
        # rather than let every caller of `pct()` guard against it.
        return 100 * riders / self.total_riders

    def write_csv(self, path: Path) -> None:
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(ODPair)])
            writer.writeheader()
            writer.writerows(asdict(r) for r in self.rows)
        print(f"\nWrote {len(self.rows):,} rows to {path}")

    def print_headline(self, *, close_threshold_m: float) -> None:
        print(f"\n=== Scenario: {self.scenario.name} ===")
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
        lines: list[str] = [f"## {self.scenario.name}", ""] if show_label else []

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
            f"  {r.scenario.name:<55} total={r.total_riders:>9,.0f}  "
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
            f"| {r.scenario.name} | {r.total_riders:,.0f} | "
            f"{r.one_seat_riders:,.0f} ({r.pct(r.one_seat_riders):.1f}%) | "
            f"{r.close_riders:,.0f} ({r.pct(r.close_riders):.1f}%) | "
            f"{r.effective_riders:,.0f} ({r.pct(r.effective_riders):.1f}%) |"
        )
    lines.append("")
    return "\n".join(lines)


@dataclass(slots=True, frozen=True)
class ScenarioRun:
    """Everything one comparison run classifies: its `scenarios` and the
    `routes` universe they all share.

    That universe is the union of every selected scenario's own `routes`,
    applied to all of them alike (`Scenario.combine`) rather than each
    scenario classifying under just its own. Two scenarios compared under
    different universes aren't comparable: the origins in scope are the
    union either way, so the one with the narrower universe would count
    the other's riders in its total while never being able to give them a
    one-seat ride, and would look worse for no reason but the
    bookkeeping. `Current` has no universe of its own at all, and only
    ever gets one from here."""

    routes: Routes
    scenarios: list[Scenario]


def resolve_scenarios(
    *,
    categories: list[str],
    scenario_file: Path,
    station_index: StationIndex,
) -> ScenarioRun:
    """One combined scenario per element of the cartesian product of every
    `--category`-selected category's scenarios *plus* the `CURRENT`
    scenario (today's real routing, i.e. the option of leaving that
    category unchanged) -- `Scenario.combine`, via
    `ScenarioFile.filter`/`combine_scenarios`. So two categories with two
    scenarios each select nine combined scenarios: every pairing, each
    category's scenarios on their own, and `Current` throughout as the
    baseline. A single selected category just yields `Current` plus its
    own scenarios, nothing to combine. Raises `ScenarioError` (not
    `SystemExit`) for a missing/malformed `--scenario-file`, an unknown
    `--category`, or no `--category` at all; only `deinterlining()` itself
    exits."""
    try:
        file = ScenarioFile.load(scenario_file, station_index)
    except FileNotFoundError as e:
        raise ScenarioError(f"missing required scenario file {scenario_file}") from e

    if not categories:
        available = ", ".join(sorted(c.name for c in file.categories)) or "none"
        # Not just "nothing to compare against today's routing": the route
        # universe comes from the selected scenarios now, so a selection
        # of none leaves nothing to classify under either.
        raise ScenarioError(
            f"no --category selected: the scenarios to compare, and the "
            f"routes to compare them over, both come from one (available "
            f"in {scenario_file}: {available})"
        )
    selected = file.filter(frozenset(categories))
    return ScenarioRun(
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
                "proposed swap directions) -- required, and the only way "
                'to select scenarios besides always-included "Current". '
                "The routes a run covers come from the scenarios it "
                "selects (each declares its own), not from the command "
                "line. Repeatable: "
                "with two or more, every scenario in each selected "
                "category is combined with one from every other (their "
                "overrides unioned), leaving a category unchanged being "
                "one of the options for it, so two categories with two "
                "scenarios each run nine combined scenarios -- every "
                "pairing, each category's two on their own, and today's "
                "routing throughout."
            ),
        ),
    ] = None,
    scenario_file: Annotated[
        Path,
        Option(
            help=(
                "JSON file, a JSON object of {category: [{'name': str, "
                "'description': str, 'overrides': [{'line': str, 'add': "
                "[route, ...], 'remove': [route, ...], 'stations': "
                "[station_name, ...]}, ...]}, ...]}. Each override group "
                "applies the same add/remove to every listed station -- "
                "the usual case, since a deinterlining change typically "
                "affects several stations on one line the same way. "
                "'line' (e.g. '8th Av - Fulton St') is required on every "
                "group: besides disambiguating a station_name shared by "
                "multiple complexes elsewhere in the system, it states "
                "which physical line a group applies to without cross-"
                "referencing station reference data. --category selects by "
                'the top-level key; "Current" (today\'s real routing) is '
                "built in rather than defined here, and always compared "
                "against. Trailing commas are tolerated."
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
    """Systemwide deinterlining scenario comparator: classify every
    origin/destination pair whose origin could plausibly use one of the
    selected scenarios' own routes as one-seat or transfer, under today's
    real routing and any
    number of route-override scenarios -- selected from `--scenario-file`
    by `--category` (every scenario in it with that category; selecting
    more than one category combines them into every pairing, see
    `Scenario.combine`) -- all classified in one pass over the same
    fetched OD pairs, so comparing several proposals doesn't reclassify
    "today" once per proposal.

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
        # (every scenario in the "Columbus" category)
        mta-od-data analyze deinterlining --category "Columbus" \\
            --markdown-out src/mta_od_data/analyze/deinterlining_columbus_circle.md

    \b
        # DeKalb and Columbus together: every combination of one DeKalb
        # swap direction and one Columbus swap direction, each a single
        # combined scenario with both changes' overrides applied at once,
        # plus each junction's own swaps with the other left as it is today
        # (classified over both categories' routes together)
        mta-od-data analyze deinterlining --category "DeKalb" --category "Columbus"

    \b
        # A draft catalog not yet merged into scenarios.json5 (--scenario-file
        # replaces the catalog rather than adding to it)
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
        run = resolve_scenarios(
            categories=categories,
            scenario_file=scenario_file,
            station_index=station_index,
        )
    except ScenarioError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    scenarios = run.scenarios
    routes_set = run.routes
    show_label = len(scenarios) > 1
    for s in scenarios:
        print(f"Scenario: {s.name} ({len(s.overrides)} stations overridden)")
    print(f"Route universe: {sorted(routes_set)}")
    print(f"Day filter: {days_list if days_list else 'all days'} ({day_type_label})")

    # Systemwide, but not literally every station: an origin only matters
    # if it could plausibly use one of the run's routes under *any* scenario
    # being compared (today's real routing included) -- otherwise its
    # trips have nothing to do with the junction(s) being analyzed (unlike
    # `regional_flow.py`, whose question -- does a trip touch this region
    # -- has no such natural restriction).
    origin_ids = [
        s.complex_id
        for s in stations_by_id.values()
        if any(sc.routes_of(s) for sc in scenarios)
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

    platforms_by_complex: dict[int, list[Station]] = {}
    for s in individual_stations:
        platforms_by_complex.setdefault(s.complex_id, []).append(s)

    # Same caching structure as `one_seat_rides.py`'s `assigned_points`/
    # `min_dist_to_corridor` -- local rather than cached at their own
    # definition since both close over `individual_stations`/
    # `platforms_by_complex`, loaded fresh per invocation. Shared across
    # every scenario's `Scenario.classify` call (including the "Current"
    # scenario's), since cache keys are (dest, effective routes) pairs,
    # not scenario-specific.
    @cache
    def assigned_points(assigned_routes: Routes) -> list[Station]:
        return [s for s in individual_stations if s.routes & assigned_routes]

    @cache
    def min_dist_to_corridor(
        dest: Station, assigned_routes: Routes
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
        dest: Station, effective_origin_routes: Routes
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
        else (csv_out if not show_label else suffixed_path(csv_out, s.slug()))
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
