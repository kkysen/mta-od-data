"""The checked-in `scenarios.schema.json` must match what the models
that actually validate a scenario file generate, or it's silently
documenting a shape `ScenarioFile.load` no longer accepts.
"""

from mta_od_data.analyze.scenario_schema import (
    SCENARIOS_SCHEMA_FILE,
    generate_scenario_schema,
)


def test_scenarios_schema_matches_models() -> None:
    fresh = generate_scenario_schema()
    committed = SCENARIOS_SCHEMA_FILE.read_text()
    assert fresh == committed, (
        f"{SCENARIOS_SCHEMA_FILE} is out of date. Regenerate it with:\n"
        '  uv run python -c "from mta_od_data.analyze.scenario_schema import '
        "SCENARIOS_SCHEMA_FILE, generate_scenario_schema; "
        'SCENARIOS_SCHEMA_FILE.write_text(generate_scenario_schema())"\n'
        "and commit the result."
    )
