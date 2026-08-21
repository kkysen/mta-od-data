"""The checked-in `scenarios.json5` must still load:
it's hand-edited, so a typo'd station name, line, or route
only surfaces when `mta-od-data analyze deinterlining` actually resolves it.

Skipped without the station reference CSVs,
which resolving a scenario's overrides needs.
"""

import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import Station
from mta_od_data.analyze.deinterlining import NO_WALK, Outcome, Walks, resolve_scenarios
from mta_od_data.analyze.scenarios import (
    SCENARIOS_FILE,
    ScenarioError,
    ScenarioFile,
    StationIndex,
)

STATIONS = DATA / "stations_complexes.csv"
STATIONS_INDIVIDUAL = DATA / "stations_individual.csv"

pytestmark = pytest.mark.skipif(
    not (STATIONS.exists() and STATIONS_INDIVIDUAL.exists()),
    reason=(
        f"{STATIONS.relative_to(ROOT)}/{STATIONS_INDIVIDUAL.relative_to(ROOT)} not "
        "found (run `uv run mta-od-data prepare` first)"
    ),
)


@pytest.fixture(scope="module")
def stations_by_id() -> dict[int, Station]:
    return Station.load_complexes(STATIONS)


@pytest.fixture(scope="module")
def individual_stations() -> list[Station]:
    return Station.load_individuals(STATIONS_INDIVIDUAL)


@pytest.fixture(scope="module")
def station_index(
    stations_by_id: dict[int, Station], individual_stations: list[Station]
) -> StationIndex:
    return StationIndex.build(stations_by_id, individual_stations)


@pytest.fixture(scope="module")
def scenario_file(station_index: StationIndex) -> ScenarioFile:
    return ScenarioFile.load(SCENARIOS_FILE, station_index)


def test_scenarios_file_loads(scenario_file: ScenarioFile) -> None:
    assert scenario_file.categories, f"{SCENARIOS_FILE} has no categories"
    for category in scenario_file.categories:
        assert category.scenarios, f'category "{category.name}" has no scenarios'


def test_every_category_resolves(
    scenario_file: ScenarioFile, station_index: StationIndex
) -> None:
    """Each category on its own is what `--category` selects,
    and it has to yield both a route universe and something to compare."""
    for category in scenario_file.categories:
        comparison = resolve_scenarios(
            categories=[category.name],
            scenario_file=SCENARIOS_FILE,
            station_index=station_index,
        )
        assert comparison.routes, f'category "{category.name}" resolves to no routes'
        assert len(comparison.scenarios) > 1, (
            f'category "{category.name}" has nothing to compare against CURRENT'
        )


CONFLICT_ROUTES = ["B", "D", "N", "Q", "R"]
# A real complex on a real line, so the failure under test is the
# conflict and not a name that doesn't resolve.
CONFLICT_STATION = {"line": "Broadway - Brighton", "stations": ["Kings Hwy"]}


def write_scenarios(tmp_path: Path, categories: Mapping[str, object]) -> Path:
    path = tmp_path / "scenarios.json5"
    path.write_text(json.dumps(categories))
    return path


def test_a_group_cannot_add_and_remove_the_same_route(
    tmp_path: Path, station_index: StationIndex
) -> None:
    path = write_scenarios(
        tmp_path,
        {
            "X": [
                {
                    "name": "Self-contradicting",
                    "routes": CONFLICT_ROUTES,
                    "overrides": [{"add": ["B"], "remove": ["B"], **CONFLICT_STATION}],
                }
            ]
        },
    )
    with pytest.raises(ScenarioError, match="both adds and removes"):
        ScenarioFile.load(path, station_index)


def test_two_categories_cannot_disagree_about_a_route(
    tmp_path: Path, station_index: StationIndex
) -> None:
    """`RouteDelta.apply` removes before it adds, so a route one category
    adds and another removes would silently survive.
    Combining them raises instead."""
    path = write_scenarios(
        tmp_path,
        {
            "Adds": [
                {
                    "name": "Adds B",
                    "routes": CONFLICT_ROUTES,
                    "overrides": [{"add": ["B"], "remove": [], **CONFLICT_STATION}],
                }
            ],
            "Removes": [
                {
                    "name": "Removes B",
                    "routes": CONFLICT_ROUTES,
                    "overrides": [{"add": [], "remove": ["B"], **CONFLICT_STATION}],
                }
            ],
        },
    )
    # Either alone is fine; only the combination is ambiguous.
    for category in ("Adds", "Removes"):
        resolve_scenarios(
            categories=[category], scenario_file=path, station_index=station_index
        )
    with pytest.raises(ScenarioError, match="disagree about route"):
        resolve_scenarios(
            categories=["Adds", "Removes"],
            scenario_file=path,
            station_index=station_index,
        )


# Every route Kings Hwy has on the Brighton line, so the scenario leaves
# it with nothing: a station losing its service is a thing a plan can
# legitimately propose, and the comparison has to classify trips to it
# rather than fall over.
STRANDING_SCENARIOS = {
    "Strip": [
        {
            "name": "No B/Q at Kings Hwy",
            "routes": ["B", "Q"],
            "overrides": [
                {
                    "line": "Broadway - Brighton",
                    "remove": ["B", "Q"],
                    "stations": ["Kings Hwy"],
                },
            ],
        },
    ],
}


def test_a_stranded_pair_is_far_not_a_crash(
    tmp_path: Path,
    station_index: StationIndex,
    stations_by_id: dict[int, Station],
    individual_stations: list[Station],
) -> None:
    """A trip between two stations the scenario leaves with no route in
    the comparison's universe: no walk at either end turns it into a
    one-seat ride, which is what `far` means."""
    path = write_scenarios(tmp_path, STRANDING_SCENARIOS)
    comparison = resolve_scenarios(
        categories=["Strip"], scenario_file=path, station_index=station_index
    )
    # Stranded under the scenario, and off B/Q entirely to begin with:
    # the origin is in scope only because today's routing puts it there.
    origin = station_index.resolve("Kings Hwy", "Broadway - Brighton", path=path)
    dest = station_index.resolve("Astoria-Ditmars Blvd", "Astoria", path=path)
    # As `deinterlining()` scopes a run: every complex some scenario
    # gives one of the comparison's routes.
    scope_ids = frozenset(
        station.complex_id
        for station in stations_by_id.values()
        if any(s.routes_of(station) for s in comparison.scenarios)
    )
    assert origin.complex_id in scope_ids, "the origin should be in scope today"

    result = comparison.classify(
        pairs=[(origin.complex_id, dest.complex_id, 100.0)],
        stations_path=STATIONS,
        scope_ids=scope_ids,
        walks=Walks(
            stations_by_id=stations_by_id,
            individual_stations=individual_stations,
            platforms=station_index.platforms,
            close_threshold_m=300.0,
        ),
    )
    stranded = result.results[-1].rows[0]
    assert stranded.outcome is Outcome.FAR
    assert stranded.walk == NO_WALK
