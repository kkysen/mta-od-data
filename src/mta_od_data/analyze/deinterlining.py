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
import shlex
import sys
from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, fields, is_dataclass
from enum import StrEnum
from functools import cache
from operator import attrgetter, itemgetter
from pathlib import Path
from typing import Annotated, Any

import duckdb
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import (
    DAY_TYPE_PRESETS,
    Coord,
    DayCoverage,
    DayFilterError,
    DayType,
    PlatformIndex,
    Station,
    haversine,
)
from mta_od_data.analyze.markdown import table_row, table_rule
from mta_od_data.analyze.scenarios import (
    CURRENT,
    SCENARIOS_FILE,
    Routes,
    Scenario,
    ScenarioError,
    ScenarioFile,
    StationIndex,
)

app = Typer()


def suffixed_path(path: Path, suffix: str) -> Path:
    return path.with_name(f"{path.stem}_{suffix}{path.suffix}")


@dataclass(slots=True, frozen=True)
class Walk:
    """The shorter of the two walks that would turn a transfer trip into
    a one-seat ride; see `ScenarioWalks.shortest_walk`, which measures it."""

    # Within the comparison's `--close-threshold-m`.
    # Only meaningful against a pair that isn't already a one-seat ride.
    close: bool
    dist_m: float
    # The station the walk reaches, named under the scenario.
    station: str | None
    # Which end the walk is at.
    # Symmetric in the pair, but not a property of it:
    # which end is the shorter walk is exactly what this records.
    at_origin: bool


# A one-seat ride, where the ridden route stops at both ends
# and there is no walk to model.
NO_WALK = Walk(close=False, dist_m=0.0, station=None, at_origin=False)


@dataclass(slots=True, frozen=True)
class TripEnd:
    """One end of an `ODPair`--its origin or its destination--as one
    scenario names it."""

    id: int
    # Split rather than one display string, so a scenario comparison can
    # say what changed at an end (`8 Av (N -> B)`) without taking the
    # string back apart, and so the CSV can be filtered on either.
    station: str
    routes: str

    @property
    def name(self) -> str:
        return f"{self.station} ({self.routes})"

    def label(self, other: TripEnd) -> str:
        """This end as the baseline names it,
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
        if (self.station, self.routes) == (other.station, other.routes):
            return self.name
        if self.station == other.station:
            return f"{self.station} ({self.routes} → {other.routes})"
        return f"{self.name} → {other.name}"


@dataclass(slots=True, frozen=True)
class ODPair:
    origin: TripEnd
    destination: TripEnd
    riders: float
    # Both ends served by the comparison's routes.
    # The detailed tables are scoped to these
    # (see `comparison_table_markdown`);
    # the CSV keeps every row, with this column to filter on.
    both_ends: bool
    one_seat: bool
    # `NO_WALK` when `one_seat`, there being no walk to model then.
    walk: Walk

    @property
    def ends(self) -> tuple[TripEnd, TripEnd]:
        return self.origin, self.destination

    @property
    def outcome(self) -> Outcome:
        """What this scenario leaves the pair's riders with."""
        if self.one_seat:
            return Outcome.DIRECT
        return Outcome.CLOSE if self.walk.close else Outcome.FAR

    @classmethod
    def csv_fields(cls) -> list[str]:
        """The columns `csv_row` produces, in its order."""
        return [
            name
            for fld in fields(cls)
            for name in (
                [f"{fld.name}_{nested.name}" for nested in fields(fld.type)]
                if is_dataclass(fld.type)
                else [fld.name]
            )
        ]

    @property
    def csv_row(self) -> dict[str, Any]:
        """One flat row: a CSV column can't hold a nested `TripEnd` or
        `Walk`, so each one's fields are inlined under the field's own
        name as a prefix (`origin_id`, `walk_dist_m`).

        The prefix rather than their bare names,
        which is what a nested field loses by being flattened:
        `at_origin` says nothing beside an `origin_id` column,
        and a lone `station` doesn't say which end's.
        """
        row: dict[str, Any] = {}
        for name, value in asdict(self).items():
            if isinstance(value, dict):
                row |= {f"{name}_{nested}": v for nested, v in value.items()}
            else:
                row[name] = value
        return row


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

    @property
    def effective(self) -> bool:
        """Whether this counts towards effective one-seat."""
        return self is not Outcome.FAR


# An index into `WalkPoints.locations`, naming one platform -- or the
# centroid of a complex with no platform rows of its own, which is the
# only other thing a walk is ever measured from.
# An `int` rather than a type of its own: it is used as a dict key
# hundreds of thousands of times a run, which is the whole point of it,
# and anything wrapping it hashes an order of magnitude slower.
type PlatformId = int


# Not `slots=True`, alone among this module's dataclasses: `distance`
# below is a method each instance replaces with a cached one of its own,
# and a slot of that name would collide with the method -- silently, the
# slot winning and the method disappearing.
@dataclass(frozen=True, eq=False)
class WalkPoints:
    """Every location a walk can be measured between, by `PlatformId`.

    Walks run platform to platform: a rider leaves from whichever of
    their complex's platforms is nearest what they are walking to, so a
    complex enters as all of its platforms at once, which is what
    `by_complex` holds.

    `eq=False` because a table of coordinates has no meaningful equality
    and no cheap hash: two of them holding the same numbers still aren't
    interchangeable, and a frozen dataclass's generated hash would raise
    on the `list` anyway. `distance`'s cache doesn't key on it -- it
    wraps a bound method, so the table is the closure, not the key.
    """

    locations: list[Coord]
    by_complex: dict[int, tuple[PlatformId, ...]]
    # Ids below this are platforms, in `individual_stations` order;
    # ids at or above it are the centroids standing in for complexes
    # with no platform rows of their own.
    n_platforms: int

    def __post_init__(self) -> None:
        # Each table remembers its own distances, shadowing the method
        # below with a cached one. `@cache` on the method itself would
        # be a store on the *function*, keyed by `self` and kept for the
        # life of the process, however briefly the table was wanted.
        # `object.__setattr__` because the dataclass is frozen: normal
        # assignment raises, and this is how a frozen one fills in what
        # it derives from its fields.
        object.__setattr__(self, "distance", cache(self.distance))

    def distance(self, point: PlatformId, other: PlatformId) -> float:
        """Metres between two of these, remembered per table.

        Ids rather than the `Coord`s themselves, which are dataclasses:
        a dataclass recomputes its hash on every lookup, where an int is
        its own.
        """
        here, there = self.locations[point], self.locations[other]
        return haversine(here.lat, here.lon, there.lat, there.lon)

    def platform(self, point: PlatformId) -> PlatformId | None:
        """`point` if it is a platform, `None` if it is a centroid."""
        return point if point < self.n_platforms else None

    @classmethod
    def build(
        cls, individual_stations: list[Station], stations_by_id: dict[int, Station]
    ) -> WalkPoints:
        locations = [platform.loc for platform in individual_stations]
        by_complex: defaultdict[int, list[PlatformId]] = defaultdict(list)
        for platform_id, platform in enumerate(individual_stations):
            by_complex[platform.complex_id].append(platform_id)
        for complex_id, station in stations_by_id.items():
            if complex_id not in by_complex:
                # No platform rows of its own, so its centroid stands in,
                # and takes an id past the last platform's.
                by_complex[complex_id] = [len(locations)]
                locations.append(station.loc)
        return cls(
            locations=locations,
            by_complex={cid: tuple(ids) for cid, ids in by_complex.items()},
            n_platforms=len(individual_stations),
        )


@dataclass(slots=True, frozen=True, eq=False)
class Walks:
    """One run's station data, everything measuring a walk needs
    that a scenario doesn't supply.

    Nothing here answers on its own: `for_scenario` binds it to the
    scenario that says which stations serve what, which is the other
    half of every question below.

    `eq=False` so both these classes hash by identity, which their
    `@cache`d methods need: the fields are dicts and lists, and a
    field-by-field hash of a station table would be neither cheap nor
    possible.
    """

    stations_by_id: dict[int, Station]
    individual_stations: list[Station]
    platforms: PlatformIndex
    close_threshold_m: float

    def for_scenario(self, scenario: Scenario) -> ScenarioWalks:
        return ScenarioWalks(walks=self, scenario=scenario)

    # One per run, so every scenario shares its distances: where a
    # platform is doesn't depend on which routes stop there.
    @cache  # noqa: B019  (see `ScenarioWalks.corridor_platforms`)
    def points(self) -> WalkPoints:
        return WalkPoints.build(self.individual_stations, self.stations_by_id)


@dataclass(slots=True, frozen=True, eq=False)
class ScenarioWalks:
    """How far a rider without a one-seat ride would have to walk under
    one scenario, and so whether the trip is still effectively one.

    One of these per scenario rather than one shared: which stations
    serve a corridor is exactly what a scenario changes, so a lookup
    shared across scenarios would answer with today's routes under every
    one of them. The caches below are keyed per scenario for the same
    reason, `self` being part of every key.
    """

    walks: Walks
    scenario: Scenario

    @property
    def platforms(self) -> PlatformIndex:
        return self.walks.platforms

    @cache  # noqa: B019  (see `corridor_platforms`)
    def routes_by_complex(self) -> dict[int, Routes]:
        """Every complex's routes under this scenario, worked out once.

        `Scenario.routes_of` is a dict lookup and a set intersection,
        and `classify` asks it twice per OD pair, which on a
        three-scenario run over 250k pairs is 780k calls for 445
        distinct answers.
        """
        return {
            complex_id: self.scenario.routes_of(station)
            for complex_id, station in self.walks.stations_by_id.items()
        }

    @cache  # noqa: B019  (see `corridor_platforms`)
    def ends_by_complex(self) -> dict[int, TripEnd]:
        """How every complex reads under this scenario, worked out once.

        Its narrowed platform name and its route list are as fixed for
        the scenario as its routes are, and `classify` names both ends
        of every OD pair: another 780k calls for 445 answers, each one
        sorting a route set and joining it.

        A `TripEnd` rather than the two strings, since that is what a
        row wants: its `id` is the complex's, so the pair is two
        lookups.
        """
        return {
            complex_id: TripEnd(
                id=complex_id,
                station=self.platforms.name(station, routes),
                routes=",".join(sorted(routes)),
            )
            for complex_id, routes in self.routes_by_complex().items()
            if (station := self.walks.stations_by_id[complex_id]) is not None
        }

    # B019: `cache` on a method stores its entries on the *function*,
    # keyed by `self` among the arguments, so every `ScenarioWalks` ever
    # built stays alive with its measurements until the process ends.
    # That is what a command wants -- it classifies each scenario once
    # and exits -- but a long-lived caller comparing scenario after
    # scenario would grow this without bound, and wants its own cache.
    @cache  # noqa: B019
    def corridor_platforms(
        self, corridor_routes: Routes
    ) -> list[tuple[PlatformId, Station]]:
        """The platforms a rider could board this corridor at,
        under this scenario.

        Per platform, not per complex.
        The distance is measured to a platform's own coordinates, and
        a complex can span physically separate stations
        (Times Sq-42 St and 42 St-Port Authority Bus Terminal are
        200m apart), so crediting every platform of a complex with
        every route the complex has understated a walk by up to that.
        """
        return [
            (platform_id, platform)
            for platform_id, platform in enumerate(self.walks.individual_stations)
            if self.scenario.routes_at(platform) & corridor_routes
        ]

    @cache  # noqa: B019  (see `corridor_platforms`)
    def corridor_points(self, complex_id: int) -> tuple[PlatformId, ...]:
        """Where a rider of this comparison stands at this complex.

        Its platforms that serve one of the comparison's routes, not all
        of them: a rider walking to or from Times Sq for the N,Q,R is on
        its Broadway platform, and crediting them with the 7's, 386m
        away, would measure a walk they don't take. It is the same
        narrowing the row's own label makes when it reads
        `Times Sq-42 St (N,Q,R)`.

        All of them when none serves one, which is a complex the other
        end put in scope: there is no corridor platform to stand on, so
        the complex is all that is known about where they are.
        """
        points = self.walks.points()
        platforms = self.walks.individual_stations
        on_corridor = tuple(
            point
            for point in points.by_complex[complex_id]
            if (platform := points.platform(point)) is not None
            and self.scenario.routes_at(platforms[platform])
        )
        return on_corridor or points.by_complex[complex_id]

    @cache  # noqa: B019  (see `corridor_platforms`)
    def min_dist_to_route(
        self, complex_id: int, route: str
    ) -> tuple[float, Station] | None:
        """The nearest platform this route stops at, and how far.

        `None` when the route stops nowhere under this scenario, e.g. a
        synthetic one no scenario uses yet, or one every scenario in the
        comparison takes off the map.
        """
        candidates = self.corridor_platforms(frozenset({route}))
        if not candidates:
            return None

        points = self.walks.points()
        distance = points.distance
        # By distance alone: two platforms exactly as far away would
        # otherwise be compared as `Station`s, which don't order.
        return min(
            (
                (distance(point, platform_id), platform)
                for point in self.corridor_points(complex_id)
                for platform_id, platform in candidates
            ),
            key=itemgetter(0),
        )

    @cache  # noqa: B019  (see `corridor_platforms`)
    def min_dist_to_corridor(
        self, complex_id: int, corridor_routes: Routes
    ) -> tuple[float, Station] | None:
        """The nearest platform a rider could board this corridor at.

        The nearest of a set of routes is the nearest of each route's
        own nearest, so the sweep is keyed per route: one per (station,
        route), a few thousand, where keying it on the set swept once
        per distinct set, which is every combination of routes the
        scenarios put on a station.

        `None` when there is nothing to measure to: either the station
        has no route in this comparison at all, so there is no corridor
        of its own to measure against, or none of these routes stops
        anywhere. The caller decides what an unmeasurable end means.
        """
        # Sorted, so which of two equally distant platforms wins doesn't
        # depend on a `frozenset`'s iteration order.
        measured = [
            nearest
            for route in sorted(corridor_routes)
            if (nearest := self.min_dist_to_route(complex_id, route)) is not None
        ]
        return min(measured, key=itemgetter(0)) if measured else None

    def shortest_walk(
        self,
        origin: Station,
        dest: Station,
        origin_routes: Routes,
        dest_routes: Routes,
    ) -> Walk:
        """The shorter of the two walks that would turn this trip into a
        one-seat ride.

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
            (self.min_dist_to_corridor(dest.complex_id, origin_routes), False),
            (self.min_dist_to_corridor(origin.complex_id, dest_routes), True),
        ]
        measured = [
            (*best, at_origin) for best, at_origin in options if best is not None
        ]
        if not measured:
            # Neither end has a route in this comparison *under this
            # scenario*, so there is no corridor at either end to walk
            # to and no walk that would make the trip a one-seat ride:
            # `far`, which is what `NO_WALK` classifies as.
            #
            # Reachable, and not a bug in scoping: a pair is fetched if
            # either end is in `scope_ids`, which is the union across
            # scenarios, while a corridor to measure against is per
            # scenario. A scenario that takes a station's every
            # comparison route away strands it under that scenario
            # alone, and a trip from there to somewhere off the routes
            # entirely has nothing measurable at either end.
            return NO_WALK

        # Keyed on the distance alone: two equal walks would otherwise
        # be compared by the `Station` beside it, which doesn't order.
        dist_m, platform, walk_at_origin = min(measured, key=itemgetter(0))
        return Walk(
            close=dist_m <= self.walks.close_threshold_m,
            dist_m=dist_m,
            station=self.ends_by_complex()[platform.complex_id].name,
            at_origin=walk_at_origin,
        )

    def classify(
        self,
        *,
        pairs: list[tuple[int, int, float]],
        stations_path: Path,
        scope_ids: frozenset[int],
    ) -> ScenarioResult:
        rows: list[ODPair] = []
        routes_by_complex = self.routes_by_complex()
        ends_by_complex = self.ends_by_complex()
        for origin_id, dest_id, riders in pairs:
            origin = self.walks.stations_by_id.get(origin_id)
            dest = self.walks.stations_by_id.get(dest_id)
            if origin is None or dest is None:
                missing_id = origin_id if origin is None else dest_id
                raise ScenarioError(
                    f"station complex {missing_id} not found in "
                    f"{stations_path}; refetch station reference data with "
                    "`mta-od-data prepare --force-stations`"
                )

            effective_origin_routes = routes_by_complex[origin_id]
            effective_dest_routes = routes_by_complex[dest_id]
            one_seat = bool(effective_origin_routes & effective_dest_routes)

            walk = (
                NO_WALK
                if one_seat
                else self.shortest_walk(
                    origin,
                    dest,
                    effective_origin_routes,
                    effective_dest_routes,
                )
            )

            rows.append(
                ODPair(
                    origin=ends_by_complex[origin_id],
                    destination=ends_by_complex[dest_id],
                    riders=riders,
                    both_ends=origin_id in scope_ids and dest_id in scope_ids,
                    one_seat=one_seat,
                    walk=walk,
                )
            )

        result = ScenarioResult.of(self.scenario, rows)
        if not result.overall.total:
            raise ScenarioError(
                f"scenario {self.scenario.name!r}: no ridership among the fetched "
                f"origin/destination pairs, nothing to classify (check "
                f"the selected scenarios' routes and the day filter)"
            )
        return result


@dataclass(slots=True, frozen=True)
class RiderStats:
    """One-seat split over some set of pairs,
    so the same arithmetic serves the whole comparison
    and the both-ends subset of it."""

    total: float
    one_seat: float
    close: float

    @classmethod
    def of(cls, rows: Sequence[ODPair]) -> RiderStats:
        """Summed in row order,
        the order every scenario classifies the same pairs in,
        so two scenarios' totals differ only where their classifications
        do and not in how the floats were added up."""
        return cls(
            total=sum(row.riders for row in rows),
            one_seat=sum(row.riders for row in rows if row.one_seat),
            # `NO_WALK.close` is false, so a one-seat ride,
            # which has no walk to be close, never lands in both.
            close=sum(row.riders for row in rows if row.walk.close),
        )

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

    def cell(self, value: float, base: float | None) -> str:
        """One markdown cell: riders and their share of this total,
        and how both differ from `base` where there is one."""
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

    def markdown_row(self, label: str, baseline: RiderStats | None = None) -> str:
        """`baseline` adds each column's change against it,
        saving the reader the subtraction.
        `None` for the baseline's own row, which has nothing to differ
        from."""
        one_seat, close, effective = (
            (None, None, None)
            if baseline is None
            else (baseline.one_seat, baseline.close, baseline.effective)
        )
        return table_row(
            label,
            f"{self.total:,.0f}",
            self.cell(self.one_seat, one_seat),
            self.cell(self.close, close),
            self.cell(self.effective, effective),
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
class TripEndStats:
    """One end of a trip--an origin or a destination--summed over every
    trip with the other end anywhere.
    The same shape either way,
    since a pair contributes its one classification to both of its ends."""

    name: str
    stats: RiderStats

    @classmethod
    def by_station(
        cls, rows: list[ODPair], end: Callable[[ODPair], TripEnd]
    ) -> dict[int, TripEndStats]:
        """Every station `end` picks out, keyed by complex.

        Keyed by first appearance in `rows`,
        which is the order the report's ties fall out in
        (see the `ORDER BY` the pairs are fetched with).
        """
        by_station: defaultdict[int, list[ODPair]] = defaultdict(list)
        for row in rows:
            by_station[end(row).id].append(row)
        return {
            station_id: cls(
                # The pair rows' own labels, not a second naming of the
                # same stations: displaying every real route here
                # (`Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W)`) gave
                # one report two conventions, and named the station by
                # routes no row in it is about.
                name=end(station_rows[0]).name,
                stats=RiderStats.of(station_rows),
            )
            for station_id, station_rows in by_station.items()
        }


@dataclass(slots=True, frozen=True)
class SymmetricPair:
    """Both directions of one station pair, as a single row.

    A swap changes a trip the same way whichever way it runs,
    so listing A->B and B->A separately
    spent two of the top N slots on one fact,
    and buried the pair that would otherwise have been last.

    Every classification here is symmetric--`one_seat` because a shared
    route is a shared route, `close`/`dist_m` because a rider can walk
    at either end (see `ScenarioWalks`)--so the two directions differ
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
        by_ends: defaultdict[frozenset[int], list[ODPair]] = defaultdict(list)
        for row in rows:
            by_ends[frozenset(e.id for e in row.ends)].append(row)

        pairs: list[SymmetricPair] = []
        for directions in by_ends.values():
            forward, *rest = sorted(directions, key=attrgetter("riders"), reverse=True)
            pairs.append(cls(forward=forward, reverse=rest[0] if rest else None))
        return pairs


@dataclass(slots=True, frozen=True, eq=False)
class ScenarioResult:
    scenario: Scenario
    overall: RiderStats
    # Pairs with both ends on the comparison's routes, a subset of `overall`:
    # the trips the routes could plausibly carry end to end,
    # where a swap shows up undiluted by trips only half in scope.
    both_ends: RiderStats
    rows: list[ODPair]
    origin_stats: dict[int, TripEndStats]
    destination_stats: dict[int, TripEndStats]

    @classmethod
    def of(cls, scenario: Scenario, rows: list[ODPair]) -> ScenarioResult:
        """Every number in a result is a cut of its rows,
        so `classify` classifies and this counts,
        rather than one pass keeping six running totals in step."""
        # Both-ends only, to match the tables these feed:
        # a station off the comparison's routes has no one-seat
        # ridership to or from anywhere, so it would only ever add
        # rows reading 0.0%.
        both_ends = [row for row in rows if row.both_ends]
        return cls(
            scenario=scenario,
            overall=RiderStats.of(rows),
            both_ends=RiderStats.of(both_ends),
            rows=rows,
            origin_stats=TripEndStats.by_station(both_ends, lambda row: row.origin),
            destination_stats=TripEndStats.by_station(
                both_ends, lambda row: row.destination
            ),
        )

    def write_csv(self, path: Path) -> None:
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=ODPair.csv_fields())
            writer.writeheader()
            writer.writerows(r.csv_row for r in self.rows)
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

        both_ends_rows = [r for r in self.rows if r.both_ends]
        top_pairs = sorted(
            SymmetricPair.group(both_ends_rows), key=attrgetter("riders"), reverse=True
        )[:top_n]
        for i, pr in enumerate(top_pairs, 1):
            fwd = pr.forward
            if fwd.one_seat:
                type_str, close_str, dist_str, walk_str = "1-seat", "", "", ""
            else:
                type_str = "xfer"
                close_str = "close" if fwd.walk.close else "far"
                dist_str = f"{fwd.walk.dist_m:.0f}m"
                # The station walked *to*, which is the actionable half,
                # tagged with the end it's at rather than an arrow, so it
                # reads the same whichever way the row is oriented.
                end = "origin" if fwd.walk.at_origin else "dest"
                walk_str = f"{end}: {fwd.walk.station}"
            lines.append(
                table_row(
                    str(i),
                    f"{pr.riders:,.0f}",
                    f"{self.both_ends.pct(pr.riders):.2f}%",
                    type_str,
                    close_str,
                    dist_str,
                    walk_str,
                    f"{fwd.origin.name} ↔ {fwd.destination.name}",
                )
            )
        lines.append("")

        # Origins and destinations both, and not one table standing in for
        # the other: a station's one-seat share is not symmetric, since
        # "close one-seat" measures the *destination* against the origin's
        # corridor. A terminal that reads well as an origin can read badly
        # as a destination.
        for label, end, stats in (
            ("origin", "destinations", self.origin_stats),
            ("destination", "origins", self.destination_stats),
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
            top = sorted(stats.values(), key=attrgetter("stats.total"), reverse=True)
            for e in top[:top_n]:
                lines.append(
                    table_row(
                        f"{e.stats.total:,.0f}",
                        f"{e.stats.pct(e.stats.one_seat):.1f}%",
                        f"{e.stats.pct(e.stats.effective):.1f}%",
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
        riders: defaultdict[tuple[Outcome, Outcome], float] = defaultdict(float)
        changed_rows: list[tuple[Outcome, Outcome, ODPair]] = []
        baseline_labels: dict[tuple[int, int], str] = {}
        for before_pair, after_pair in zip(baseline.rows, result.rows, strict=True):
            assert [e.id for e in before_pair.ends] == [
                e.id for e in after_pair.ends
            ], "scenario rows are not aligned"
            if not before_pair.both_ends:
                continue
            before = before_pair.outcome
            after = after_pair.outcome
            riders[before, after] += after_pair.riders
            if before is not after:
                changed_rows.append((before, after, after_pair))
                baseline_labels[after_pair.origin.id, after_pair.destination.id] = (
                    " ↔ ".join(
                        before_end.label(after_end)
                        for before_end, after_end in zip(
                            before_pair.ends, after_pair.ends, strict=True
                        )
                    )
                )

        # Grouped the same way the pair tables are, so a reader comparing
        # the two isn't matching one row against two.
        by_transition: defaultdict[tuple[Outcome, Outcome], list[ODPair]] = defaultdict(
            list
        )
        for before, after, pair in changed_rows:
            by_transition[before, after].append(pair)
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
                    symmetric.forward.origin.id,
                    symmetric.forward.destination.id,
                ],
            )
            for (before, after), pairs in by_transition.items()
            for symmetric in SymmetricPair.group(pairs)
        ]

        changed.sort(key=attrgetter("pair.riders"), reverse=True)
        return cls(
            baseline_name=baseline.scenario.name,
            scenario_name=result.scenario.name,
            # Plain, so that a cell never asked for stays absent
            # instead of being created by the asking.
            riders=dict(riders),
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
                dist = "" if fwd.one_seat else f"{fwd.walk.dist_m:.0f}m"
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
        stations_path: Path,
        scope_ids: frozenset[int],
        walks: Walks,
    ) -> ScenarioComparisonResult:
        return ScenarioComparisonResult(
            comparison=self,
            results=[
                walks.for_scenario(scenario).classify(
                    pairs=pairs,
                    stations_path=stations_path,
                    scope_ids=scope_ids,
                )
                for scenario in self.scenarios
            ],
        )


@dataclass(slots=True, frozen=True, eq=False)
class ScenarioComparisonResult:
    """Every scenario in a `ScenarioComparison`,
    classified over the same OD pairs.

    `eq=False` so this and its `ScenarioResult`s hash by identity,
    which `transitions`' cache keys on."""

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

    # Every `Transitions` walks both scenarios' rows and regroups the
    # pairs that moved, and both the printed summary and the markdown
    # want the same one. Cached, rather than passed from one to the
    # other, since neither reads the other's output.
    @cache  # noqa: B019  (see `ScenarioWalks.corridor_platforms`)
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

    try:
        coverage = DayCoverage.query(con, parquet, day_filter_sql, day_params)
    except DayFilterError as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    n_distinct_days = coverage.n_days

    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM read_parquet(?)
        WHERE {day_filter_sql} AND {scope_filter_sql}
        GROUP BY 1, 2
        -- Not decorative: a bare GROUP BY returns a different row order
        -- from one run to the next, and that order is load-bearing.
        -- Every top-N sort is stable, so ties fall out in whatever order
        -- rows arrived, and `SymmetricPair` picks its forward direction
        -- by rider count, which two equal directions leave to the same
        -- coin flip. Reports are committed and diffed against a fresh
        -- run, so any tie reaching a visible row would flake the
        -- snapshot tests rather than fail them honestly.
        ORDER BY 1, 2
    """
    pairs: list[tuple[int, int, float]] = con.execute(
        pairs_query, [str(parquet), *day_params]
    ).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter "
        f"({coverage.first_month} to {coverage.last_month})"
    )

    walks = Walks(
        stations_by_id=stations_by_id,
        individual_stations=individual_stations,
        platforms=station_index.platforms,
        close_threshold_m=close_threshold_m,
    )

    try:
        result = comparison.classify(
            pairs=pairs,
            stations_path=stations,
            scope_ids=scope_ids,
            walks=walks,
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
