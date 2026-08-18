"""The checked-in `scenarios.schema.json` must match what the models
that actually validate a scenario file generate, or it's silently
documenting a shape `ScenarioFile.load` no longer accepts.

Skipped without the station reference CSVs, which
`generate_scenario_schema` reads for its enums.
"""

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.deinterlining import (
    SCENARIOS_SCHEMA_FILE,
    generate_scenario_schema,
)

STATIONS = DATA / "stations_complexes.csv"
STATIONS_INDIVIDUAL = DATA / "stations_individual.csv"


@pytest.mark.skipif(
    not (STATIONS.exists() and STATIONS_INDIVIDUAL.exists()),
    reason=(
        f"{STATIONS.relative_to(ROOT)}/{STATIONS_INDIVIDUAL.relative_to(ROOT)} not "
        "found (run `uv run mta-od-data prepare` first)"
    ),
)
def test_scenarios_schema_matches_models() -> None:
    fresh = generate_scenario_schema()
    committed = SCENARIOS_SCHEMA_FILE.read_text()
    assert fresh == committed, (
        f"{SCENARIOS_SCHEMA_FILE} is out of date. Regenerate it with:\n"
        '  uv run python -c "from mta_od_data.analyze.deinterlining import '
        "SCENARIOS_SCHEMA_FILE, generate_scenario_schema; "
        'SCENARIOS_SCHEMA_FILE.write_text(generate_scenario_schema())"\n'
        "and commit the result."
    )
