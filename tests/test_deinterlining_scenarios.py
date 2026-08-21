"""The checked-in `scenarios.json5` must still load:
it's hand-edited, so a typo'd station name, line, or route
only surfaces when `mta-od-data analyze deinterlining` actually resolves it.

Skipped without the station reference CSVs,
which resolving a scenario's overrides needs.
"""

import json
from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import Station
from mta_od_data.analyze.deinterlining import resolve_scenarios
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
def station_index() -> StationIndex:
    return StationIndex.build(
        Station.load_complexes(STATIONS),
        Station.load_individuals(STATIONS_INDIVIDUAL),
    )


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


def write_scenarios(tmp_path: Path, categories: dict[str, object]) -> Path:
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
