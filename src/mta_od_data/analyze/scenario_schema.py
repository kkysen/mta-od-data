"""The JSON Schema an editor validates a scenario file against.

Editor-time only: nothing here runs during an analysis,
and `ScenarioFile.load` re-checks every value itself
against whichever station data was actually passed.
"""

import json
from pathlib import Path
from typing import Any

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import Station
from mta_od_data.analyze.deinterlining import SCENARIO_FILE_ADAPTER

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

        uv run python -c "from mta_od_data.analyze.scenario_schema import \\
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
