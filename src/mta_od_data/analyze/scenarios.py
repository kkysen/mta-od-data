"""What a deinterlining scenario is, and how one is read off a file.

Route overrides and the station data they resolve against, no ridership:
what a scenario does to a rider is `deinterlining.py`'s half,
which imports this one and not the other way round.
See `deinterlining_design.md` for why per-station overrides
replace `one_seat_rides.py`'s corridor-A/corridor-B machinery.
"""

import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import json5
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from mta_od_data import ROOT
from mta_od_data.analyze.common import PlatformIndex, Station

SCENARIOS_FILE = ROOT / "src" / "mta_od_data" / "analyze" / "scenarios.json5"


type Routes = frozenset[str]


class ScenarioError(Exception):
    """Raised rather than exiting,
    so everything but `deinterlining()` itself
    stays usable as a library function."""


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "scenario"


@dataclass(slots=True, frozen=True)
class RouteDelta:
    add: Routes
    remove: Routes

    def __or__(self, other: RouteDelta) -> RouteDelta:
        return RouteDelta(add=self.add | other.add, remove=self.remove | other.remove)

    @property
    def conflict(self) -> Routes:
        """Routes this delta both adds and removes.

        `apply` removes before it adds, so a route in both survives,
        and the delta silently means "add" whatever the author intended.
        Two deltas that disagree about a route
        have no defensible merge, so callers raise instead:
        this is the whole of `#5`, a plan combining two junctions
        where both move the same route at the same platform.
        """
        return self.add & self.remove

    def apply(self, station: Station) -> Routes:
        return (station.routes - self.remove) | self.add


# A complex and the line an override named,
# which is what a delta is keyed by; see `Scenario.overrides` for why both.
type OverrideKey = tuple[Station, str]
type Overrides = dict[OverrideKey, RouteDelta]


def merge_override(overrides: Overrides, key: OverrideKey, delta: RouteDelta) -> Routes:
    """Merge `delta` into whatever `key` already holds.

    Returns the routes the two disagree about, empty when they agree.
    A disagreement leaves `overrides` untouched
    and is the caller's to report,
    since who is disagreeing is all that separates the two ways
    to arrive here: two override groups in one scenario,
    and two scenarios being combined.
    """
    existing = overrides.get(key)
    merged = delta if existing is None else existing | delta
    if not merged.conflict:
        overrides[key] = merged
    return merged.conflict


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


@dataclass(slots=True, frozen=True)
class StationIndex:
    # The complexes a (station name, line) names, which is all of them
    # rather than the last one seen: a name shared by two complexes on
    # one line has no right answer, and `resolve` says so instead of
    # picking whichever the CSV happened to end with.
    by_name_line: dict[tuple[str, str], frozenset[Station]]
    known_routes: frozenset[str]
    # A scenario's overrides are declared per line and resolved to a
    # complex, so applying them needs the complex's platforms.
    platforms: PlatformIndex

    @classmethod
    def build(
        cls,
        stations_by_id: dict[int, Station],
        individual_stations: list[Station],
    ) -> StationIndex:
        by_name_line: defaultdict[tuple[str, str], set[Station]] = defaultdict(set)
        for platform in individual_stations:
            # By complex, so a complex's several platforms of one name
            # on one line (which is routine) count once.
            by_name_line[platform.name, platform.line].add(
                stations_by_id[platform.complex_id]
            )
        return cls(
            by_name_line={key: frozenset(v) for key, v in by_name_line.items()},
            known_routes=frozenset(
                r for s in stations_by_id.values() for r in s.routes
            ),
            platforms=PlatformIndex.build(individual_stations),
        )

    def resolve(self, name: str, line: str, *, path: Path) -> Station:
        stations = self.by_name_line.get((name, line), frozenset())
        if not stations:
            raise ScenarioError(
                f'scenario {path}: no station named "{name}" on line "{line}"'
            )
        if len(stations) > 1:
            ids = sorted(s.complex_id for s in stations)
            raise ScenarioError(
                f'scenario {path}: "{name}" on line "{line}" names '
                f"{len(stations)} station complexes ({ids}), so there is no "
                f"one station to override. Split the group so each names a "
                f"line only one of them is on"
            )
        return next(iter(stations))

    def routes_on_line(self, station: Station, line: str) -> Routes:
        """What the complex's platforms *on this line* serve.

        Not the complex's own routes, which are every line's together:
        a delta names a line and applies to that line's platforms alone.
        """
        return frozenset(
            route
            for platform in self.platforms.by_complex.get(station.complex_id, ())
            if platform.line == line
            for route in platform.routes
        )

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
    # Keyed by the complex *and the line the override named*, because a
    # complex can span lines: 62 St/New Utrecht Av is one complex whose
    # West End and Sea Beach platforms a scenario moves separately, and
    # a delta keyed by the complex alone would apply to both.
    overrides: Overrides
    # A complex's routes are the union of its platforms', which the
    # station data holds to exactly, so these stay derived rather than
    # tracked.
    effective_routes: dict[Station, Routes]
    platform_routes: dict[Station, Routes]

    def slug(self) -> str:
        return slugify(self.name)

    def routes_of(self, station: Station) -> Routes:
        """A complex's routes under this scenario."""
        return self.effective_routes.get(station, station.routes & self.routes)

    def routes_at(self, platform: Station) -> Routes:
        """One platform's routes under this scenario.

        What decides whether a rider can board a corridor *here*, as
        opposed to somewhere else in the same complex: `corridor_platforms`
        measures a walk to a platform's own coordinates, and a complex can
        span 200m.
        """
        return self.platform_routes.get(platform, platform.routes & self.routes)

    @staticmethod
    def resolve_routes(
        overrides: Overrides,
        platforms: PlatformIndex,
        routes: Routes,
    ) -> tuple[dict[Station, Routes], dict[Station, Routes]]:
        """`(complex -> routes, platform -> routes)` for the overridden
        complexes; everything else falls back to its real routes."""
        effective: dict[Station, Routes] = {}
        platform_routes: dict[Station, Routes] = {}
        for complex_station in {c for c, _line in overrides}:
            union: Routes = frozenset()
            for platform in platforms.by_complex.get(complex_station.complex_id, ()):
                delta = overrides.get((complex_station, platform.line))
                at = (delta.apply(platform) if delta else platform.routes) & routes
                platform_routes[platform] = at
                union |= at
            effective[complex_station] = union
        return effective, platform_routes

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
        overrides: Overrides = {}
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
            if delta.conflict:
                raise ScenarioError(
                    f'scenario {path}: scenario "{entry.name}" both adds '
                    f"and removes route(s) {sorted(delta.conflict)} on line "
                    f'"{group.line}"'
                )
            for station_name in group.stations:
                station = station_index.resolve(station_name, group.line, path=path)
                # Removing a route a station doesn't serve is a no-op,
                # so it can't be caught by reading the numbers,
                # but it is never what an author meant:
                # either the station doesn't belong in the group,
                # or the route named is the wrong one.
                # The one that prompted this check was the first kind,
                # and it silently invented service:
                # `59 St (N,R)` listed under a `remove D` group
                # also had `add Q`, giving 959 riders a day
                # a one-seat Q that doesn't stop there.
                # Per line, not per complex: a complex can span lines
                # (62 St/New Utrecht Av is West End and Sea Beach both),
                # and a route the complex has elsewhere is still absent
                # from the platforms this group names.
                on_line = station_index.routes_on_line(station, group.line)
                absent = sorted(remove - on_line)
                if absent:
                    raise ScenarioError(
                        f'scenario {path}: scenario "{entry.name}" removes '
                        f"route(s) {absent} from "
                        f'"{station_name}" on line "{group.line}", which '
                        f"only serves {sorted(on_line)}. Either the "
                        f"station doesn't belong in this group, or the "
                        f"wrong route is named"
                    )
                conflict = merge_override(overrides, (station, group.line), delta)
                if conflict:
                    raise ScenarioError(
                        f'scenario {path}: scenario "{entry.name}" has two '
                        f'override groups for "{station_name}" on line '
                        f'"{group.line}" that disagree about route(s) '
                        f"{sorted(conflict)}"
                    )
        effective_routes, platform_routes = cls.resolve_routes(
            overrides, station_index.platforms, routes
        )
        return cls(
            name=entry.name,
            description=entry.description or entry.name,
            category=category,
            routes=routes,
            overrides=overrides,
            effective_routes=effective_routes,
            platform_routes=platform_routes,
        )

    @classmethod
    def combine(
        cls, scenarios: list[Scenario], routes: Routes, platforms: PlatformIndex
    ) -> Scenario:
        """`routes` is the whole comparison's universe
        (`ScenarioComparison`),
        not these scenarios' own,
        which is also why a single-element `scenarios` isn't returned
        as-is, its `effective_routes` being narrowed to just its own."""
        overrides: Overrides = {}
        # Which scenario last touched a key, to name both sides of a
        # disagreement rather than just the second one.
        source: dict[OverrideKey, str] = {}
        for scenario in scenarios:
            for key, delta in scenario.overrides.items():
                conflict = merge_override(overrides, key, delta)
                if conflict:
                    station, line = key
                    raise ScenarioError(
                        f'scenarios "{source[key]}" and "{scenario.name}" '
                        f"can't be combined: they disagree about route(s) "
                        f"{sorted(conflict)} at "
                        f'"{station.name}" on line "{line}". One adds what '
                        f"the other takes away, and `RouteDelta.apply` "
                        f"removes before it adds, so combining them would "
                        f"silently keep the route"
                    )
                source[key] = scenario.name
        effective_routes, platform_routes = cls.resolve_routes(
            overrides, platforms, routes
        )
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
            effective_routes=effective_routes,
            platform_routes=platform_routes,
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
    platform_routes={},
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
    station_index: StationIndex

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
            station_index=station_index,
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
            station_index=self.station_index,
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
            Scenario.combine(list(combo), routes, self.station_index.platforms)
            for combo in itertools.product(
                *([*baseline, *c.scenarios] for c in self.categories)
            )
        ]
