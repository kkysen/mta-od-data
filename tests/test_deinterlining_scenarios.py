"""The checked-in `scenarios.json5` must still load:
it's hand-edited, so a typo'd station name, line, or route
only surfaces when `mta-od-data analyze deinterlining` actually resolves it.

Skipped without the station reference CSVs,
which resolving a scenario's overrides needs.
"""

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.deinterlining import (
    SCENARIOS_FILE,
    ScenarioFile,
    Station,
    StationIndex,
    resolve_scenarios,
)

STATIONS = DATA / "stations_complexes.csv"
STATIONS_INDIVIDUAL = DATA / "stations_individual.csv"

pytestmark = pytest.mark.skipif(
    not (STATIONS.exists() and STATIONS_INDIVIDUAL.exists()),
    reason=(
        f"{STATIONS.relative_to(ROOT)}/{STATIONS_INDIVIDUAL.relative_to(ROOT)} not "
        "found (run `mta-od-data prepare` first)"
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
