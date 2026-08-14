"""`scenarios.schema.json` (checked in, for editor autocompletion) must
match the schema `OverrideGroup`/`ScenarioFile` -- the Pydantic models that
actually validate a scenario file at load time -- currently generate, or
it's silently documenting a shape `Scenario.load_all` no longer accepts.

Skipped when the station reference CSVs are missing: they're gitignored,
`mta-od-data prepare`-generated, and `generate_scenario_schema` reads them
to populate the schema's `line`/`stations`/`add`/`remove` enums.
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
        "found (run `mta-od-data prepare` first)"
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
