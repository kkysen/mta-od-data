# MTA OD data

Analyses of MTA's public subway origin-destination (OD) ridership data,
which says how many riders go from each station complex to each other,
by month, day of week, and hour,
but not which trains they take.
The `mta-od-data` CLI converts that data to Parquet,
analyzes it directly (deinterlining scenarios, flows across a region),
routes it onto the GTFS timetable's trains,
and from the routed paths counts riders by station, platform, route, line, and train.

This is an overview, one section per subcommand;
each links to the details.
Every committed `.md` report is generated, not hand-written:
each has its own `Produced by` line with its exact invocation,
and [the snapshot tests](#tests) keep them from drifting.

## Setup

```sh
mise install        # uv and pre-commit, pinned in mise.toml
uv sync             # Python, dependencies, and the Rust extension
pre-commit install  # the git hooks, see Tests below
```

[`src/mta_od_data/`](src/mta_od_data/) is a package with a `mta-od-data` entry point,
built by `maturin`, which compiles the [`raptor`](raptor/) crate as the `mta_od_data._raptor` extension,
so `uv sync` needs a Rust toolchain.
Run `uv run mta-od-data --help`, or any subcommand's `--help`, for every option.

## Getting the data

- **OD ridership**: MTA's "Subway Origin-Destination Ridership Estimate" extract
  (not committed here, see [`.gitignore`](.gitignore): it's a 27GB CSV).
  Each row is an (origin station complex, destination station complex, date, hour)
  with an estimated rider count.
  Get it from
  [data.ny.gov](https://data.ny.gov/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/jsu2-fbtj)
  (2025 vintage used here; there's a separate dataset per year)
  and drop the CSV (or its `.xz`) in `data/`,
  or skip it and download the Parquet `prepare` builds from it (below).
- **Station reference data**: fetched automatically from data.ny.gov by `prepare`.
  The "Subway Stations and Complexes" dataset
  (resource `5f5g-n3cz`, one row per station complex:
  borough, routes served, lat/long),
  plus the per-physical-station dataset (resource `39hk-dx4f`),
  which is needed because a complex can merge multiple physical stations
  (e.g. Times Sq-42 St/Port Authority Bus Terminal)
  whose combined centroid can sit well away from any actual platform.

### The prepared Parquet, as a release asset

`data/mta_od_2025.parquet` is too big to commit (358MB for the 2025 extract),
but small enough to download in seconds, so it lives as an asset on the `od-data` GitHub release.
CI fetches it before `pytest`, which is what lets
the `analyze` tests run there instead of skipping.
Anyone (including a fresh clone) can get it without rebuilding from the 27GB CSV:

```sh
gh release download od-data --pattern mta_od_2025.parquet --dir data
```

Publish (or replace) it from a machine that has run `prepare`:

```sh
# first time only
gh release create od-data --title 'OD dataset' \
    --notes 'Parquet built by `mta-od-data prepare` from the 2025 extract.'

gh release upload od-data data/mta_od_2025.parquet --clobber
```

Other years' extracts are assets beside it, each built to its own Parquet,
e.g. 2026's (January to August, 242MB, from a 16GB CSV):

```sh
uv run mta-od-data prepare \
    --csv 'data/MTA_Subway_Origin-Destination_Ridership_Estimate__2026_*.csv' \
    --out data/mta_od_2026.parquet
gh release upload od-data data/mta_od_2026.parquet --clobber

gh release download od-data --pattern mta_od_2026.parquet --dir data
```

## How the pieces fit together

```text
OD CSV ──prepare──> data/mta_od_2025.parquet ──analyze──> src/mta_od_data/analyze/*.md
                              │
GTFS (fetch-gtfs) ──raptor assign-range──> data/raptor/ (routed paths)
                                                  │
entry counts ──scale-od──> data/*.factors.parquet │
OSM (fetch-platforms) ──> platforms.csv           │
                         └──────────ridership──> src/mta_od_data/ridership/*.md
```

Inputs and outputs live in the gitignored `data/`.
Caches live on disk outside the repo:
`~/.cache/mta-od-data/` holds `analyze`'s scans of the OD data and `ridership`'s computed rows,
each keyed on what it was computed from,
and `~/.cache/mta-od-scratch/` is DuckDB's spill directory.

## `prepare`

Fetches the station reference CSVs
and converts the OD CSV(s) into Parquet (`data/mta_od_2025.parquet`)
for fast repeated querying.
Re-runnable as new OD extracts are released:
point `--csv` at the new file(s) (globs work) and/or `--out` at a new Parquet path.
To skip it, download its output instead ([above](#the-prepared-parquet-as-a-release-asset)).

```sh
uv run mta-od-data prepare
```

Details: [why the Parquet is smaller](src/mta_od_data/README.md#prepare), and `--help`.

## `fetch-gtfs`

Downloads every static GTFS feed version listed in
[`gtfs_versions.json5`](src/mta_od_data/gtfs_versions.json5) to `data/gtfs/`,
the timetables `raptor` routes on and `fetch-platforms` maps.

```sh
uv run mta-od-data fetch-gtfs
```

Details: [`raptor/README.md`](raptor/README.md#running-it).

## `fetch-platforms`

Maps each route's consecutive stops, in every feed version,
to the OpenStreetMap platforms its trains stop at
(© OpenStreetMap contributors, under the [ODbL](https://www.openstreetmap.org/copyright)),
read from [Geofabrik's New York extract](https://download.geofabrik.de/north-america/us/new-york.html)
(fetched to `data/osm/` if missing, ~500MB),
writing the checked-in [`platforms.csv`](src/mta_od_data/ridership/platforms.csv)
that `ridership --by platform` reads.

```sh
uv run mta-od-data fetch-platforms
```

Details: [`raptor/README.md`](raptor/README.md).

## `fetch-mbta`

Fetches a pinned MBTA GTFS version to `data/mbta-gtfs/` (~22MB; it has `pathways.txt`, unlike MTA's)
and cuts from it the checked-in fixture RAPTOR's pathways tests read,
four downtown Boston stations
(data provided by MassDOT, under its [Developers License Agreement](https://github.com/mbta/gtfs-documentation/blob/master/developers-license-agreement.pdf)).
With the whole version fetched, `cargo test -- --ignored` in `raptor/` checks it too.

```sh
uv run mta-od-data fetch-mbta
```

Details: [`raptor/tests/data/mbta-downtown/README.md`](raptor/tests/data/mbta-downtown/README.md).

## `scale-od`

Fits factors, per complex and (month, weekday) slice,
scaling the OD data's trips to another year's counted station entries
(from mta.info's ridership spreadsheet),
or with `--to-counts`, leveling it to its own year's counts.
`ridership --od-factors` reads them, a column per factors file.

```sh
uv run mta-od-data scale-od --year 2019 --out data/mta_od_scaled_to_2019.factors.parquet
```

Details: [`scale_od.py`](src/mta_od_data/scale_od.py) and `--help`.

## `ridership`

Average weekday riders by where they actually ride,
over `raptor assign-range`'s routed dates,
`--by` complex, station, station direction, platform, route, line, or trip,
with fare evaders added back and a column per OD scaling.

```sh
uv run mta-od-data ridership --by line
```

Details: [the reports and how to read them](raptor/README.md#the-reports-in-srcmta_od_dataridership),
e.g. [`by_line.md`](src/mta_od_data/ridership/by_line.md).

## `raptor`

Routes each OD row onto the journeys a rider could have taken
(trains, transfers, walks) on that day's GTFS timetable, using RAPTOR,
and splits its riders across them.
`assign-range` routes a representative date per (month, weekday) into `data/raptor/`;
the other subcommands inspect one step at a time.

```sh
uv run mta-od-data raptor assign-range --from 2025-08-11 --to 2025-12-31
```

Details: [`raptor/README.md`](raptor/README.md), and the design in [`raptor/raptor_design.md`](raptor/raptor_design.md).

## `analyze one-seat-rides`

For weekday trips crossing one junction,
what share are one-seat rides,
and of riders who'd lose one under a deinterlining scenario,
what share end a short walk from the other trunk anyway?

```sh
uv run mta-od-data analyze one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R
```

Details: [`analyze/README.md`](src/mta_od_data/analyze/README.md#one-seat-rides),
e.g. [`dekalb_one_seat_rides.md`](src/mta_od_data/analyze/dekalb_one_seat_rides.md).

## `analyze regional-flow`

For any region (the Congestion Relief Zone, a borough, a bounding box),
what share of riders enter it, leave it, stay within it, or never touch it?

```sh
uv run mta-od-data analyze regional-flow --region cbd
```

Details: [`analyze/README.md`](src/mta_od_data/analyze/README.md#regional-flow),
e.g. [`regional_flow.md`](src/mta_od_data/analyze/regional_flow.md).

## `analyze deinterlining`

Classifies every OD pair on the selected scenarios' routes as one-seat or transfer,
under today's routing and each route-override scenario
in [`scenarios.json5`](src/mta_od_data/analyze/scenarios.json5),
selected by `--category`.

```sh
uv run mta-od-data analyze deinterlining --category Nostrand
```

Details: [`analyze/README.md`](src/mta_od_data/analyze/README.md#deinterlining),
e.g. [`nostrand_deinterlining.md`](src/mta_od_data/analyze/nostrand_deinterlining.md).

## Tests

`pre-commit install` installs the git hooks in [`.pre-commit-config.yaml`](.pre-commit-config.yaml):
`ruff`, `ty`, `pyrefly`, and `pytest` ([`tests/`](tests/)) for Python,
and `cargo fmt`, `cargo clippy`, and `cargo test` for the Rust crates
([`raptor`](raptor/), and [`streets`](streets/), for walking OpenStreetMap's streets).
[`tests/test_analyze_snapshots.py`](tests/test_analyze_snapshots.py)
reruns every `analyze` and `ridership` report and diffs it against its committed `.md`,
Check-only, like every other hook here:
it fails with a diff and the regen command
rather than rewriting the snapshot itself.
It skips, rather than fails, a report whose gitignored inputs are missing
(e.g. `data/mta_od_2025.parquet`),
so a fresh clone that hasn't downloaded the release asset
still gets a passing suite.
