# MTA OD data: subway deinterlining analysis

MTA has floated "deinterlining" several subway junctions:
no longer letting two route pairs cross between trunks,
in exchange for more reliable service.
This analyzes MTA's public subway origin-destination ridership data
to quantify, for a given junction and route set:

1. What share are one-seat rides (no transfer needed)?
2. Of those riders who'd lose a one-seat ride under a given deinterlining
   scenario, what share would still be a short walk from the *other* trunk,
   i.e. riders who wouldn't really be stranded by it?

Two junctions are currently tracked as committed snapshots:

- **DeKalb Av**: no longer letting B/D (6 Av express trunk)
  and N/Q (Broadway express trunk) trains cross between trunks in Manhattan,
  for weekday trips on B/D/N/Q/R
  originating south of Atlantic Av-Barclays Ctr in Brooklyn.
  See [`src/mta_od_data/analyze/dekalb_one_seat_rides.md`](src/mta_od_data/analyze/dekalb_one_seat_rides.md).
- **Nostrand/Rogers Junction**: MTA's planned reroute of 2,3 to the Nostrand
  Av Line and 4,5 to Eastern Pkwy/New Lots
  (today's actual routing interlines 2,5/3,4),
  for weekday trips on 2,3,4,5 originating south of Franklin Av.
  See [`src/mta_od_data/analyze/nostrand_one_seat_rides.md`](src/mta_od_data/analyze/nostrand_one_seat_rides.md).

Both are generated, not hand-written:
see each file's own `Produced by` line for its exact invocation,
and [Development](#development) for the hook that keeps them from drifting.

## Data

- **OD ridership**: MTA's "Subway Origin-Destination Ridership Estimate"
  extract (not committed here, see [`.gitignore`](.gitignore)--it's a 27GB
  CSV).
  Each row is an (origin station complex, destination station complex, date,
  hour) with an estimated rider count.
  Get it from
  [data.ny.gov](https://data.ny.gov/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/jsu2-fbtj)
  (2025 vintage used here; there's a separate dataset per year)
  and drop the CSV (or its `.xz`) in `data/`.
- **Station reference data**: fetched automatically from `data.ny.gov`.
  The "Subway Stations and Complexes" dataset
  (resource `5f5g-n3cz`, one row per station complex:
  borough, routes served, lat/long),
  plus the per-physical-station dataset (resource `39hk-dx4f`),
  which is needed because a complex can merge multiple physical stations
  (e.g. Times Sq-42 St/Port Authority Bus Terminal)
  whose combined centroid can sit well away from any actual platform.

## The `mta-od-data` CLI

[`src/mta_od_data/`](src/mta_od_data/) is an installable package
(`duckdb`/`typer` as its only runtime dependencies);
`uv sync` installs it and its `mta-od-data` entry point
into the project's `.venv`.

### `mta-od-data prepare`

Fetches the station reference CSVs
and converts the OD CSV(s) into Parquet (`data/mta_od.parquet`)
for fast repeated querying.
Re-runnable as new OD extracts are released:
point `--csv` at the new file(s) (globs work) and/or `--out` at a new
Parquet path.
Run `--help` for all options.

```sh
uv run mta-od-data prepare
```

The Parquet comes out considerably smaller than the extract it's built from
(1.5GB to 358MB for 2025), losslessly:

- The origin/destination name, latitude, longitude, and point columns are dropped:
  each is functionally determined by the complex ID beside it,
  so they are the station reference CSVs repeated once per row,
  and `analyze` joins them by complex ID instead.
- `Timestamp` is dropped too:
  it holds one synthesized label per (year, month, day of week, hour) group,
  which `DayCoverage` reconstructs from those columns.
- Ridership is stored as `DECIMAL(9, 4)`,
  exact for every value in the extract,
  and packed as an integer rather than as a `DOUBLE` that never compresses.
- Rows are sorted by origin/destination pair,
  which runs the ID columns into long constant stretches: ~190MB by itself.

### Publishing the Parquet as a release asset

`data/mta_od.parquet` is too big to commit (358MB for the 2025 extract),
but small enough to download in seconds, so it lives as an asset on the `od-data` release.
CI fetches it before `pytest`, which is what lets
the `analyze` tests run there instead of skipping.

Publish (or replace) it from a machine that has run `prepare`:

```sh
# first time only
gh release create od-data --title 'OD dataset' \
    --notes 'Parquet built by `mta-od-data prepare` from the 2025 extract.'

gh release upload od-data data/mta_od.parquet --clobber
```

Anyone (including a fresh clone) can then get it without rebuilding from the 27GB CSV:

```sh
gh release download od-data --pattern mta_od.parquet --dir data
```

### `mta-od-data analyze one-seat-rides`

Does the actual classification:
resolves the origin station set,
queries the Parquet file for average-weekday ridership by (origin,
destination) pair,
classifies each pair as one-seat or transfer,
and for one-seat trips whether the destination is close to the trunk not
used to reach it.
Prints a summary plus per-origin and per-destination breakdowns,
can dump full row-level detail with `--csv-out`,
and can write a markdown report with `--markdown-out`.

```sh
uv run mta-od-data analyze one-seat-rides --routes B,D,N,Q,R \
    --primary-routes B,D,N,Q --trunk-b N,Q,R \
    --csv-out data/dekalb_weekday_pairs.csv \
    --markdown-out src/mta_od_data/analyze/dekalb_one_seat_rides.md
```

Everything is parameterized via CLI flags,
so the same command covers other day types, other station criteria,
other data extracts,
and other deinterlining scenarios entirely
(different junction, different trunk pairs).
Run `--help` for the full list, or see the module docstring for worked
examples.

### `mta-od-data analyze deinterlining`

The systemwide successor to `one-seat-rides`,
for junctions its shape can't express:
a scenario overrides which routes serve individual stations,
so it covers express/local swaps at a single trunk (Columbus Circle)
as well as corridor swaps.
Scenarios live in
[`scenarios.json5`](src/mta_od_data/analyze/scenarios.json5),
grouped into categories that `--category` selects by,
each declaring the routes it covers.
Today's real routing is always compared against,
and selecting two categories runs every combination of them.
See [`deinterlining_design.md`](src/mta_od_data/analyze/deinterlining_design.md).

```sh
uv run mta-od-data analyze deinterlining --category Columbus
```

### `mta-od-data analyze regional-flow`

A more general question than `one-seat-rides`:
for any region, what share of riders enter it from outside,
leave it for outside, stay entirely within it, or never touch it at all?
Unlike `one-seat-rides` this is system-wide
(every origin/destination pair, no route filter or side-of-junction split),
and classifies each pair
by whether its origin/destination fall inside the region,
using `--region`/`--region-borough`/`--region-bbox`
(see [How regions are defined](#how-regions-are-defined) below).

```sh
uv run mta-od-data analyze regional-flow --region cbd
```

Defaults to `cbd`.
Same `--csv-out`/`--markdown-out` options as `one-seat-rides`;
see [`src/mta_od_data/analyze/regional_flow.md`](src/mta_od_data/analyze/regional_flow.md)
for example output.

## How the classification works

- **Origin set**: stations served by at least one route in `--routes`,
  on the `--origin-side` (default south) of `--boundary-complex-id`'s
  latitude (default Atlantic Av-Barclays Ctr).
  This is a latitude-based proxy, not real route topology,
  but it cleanly separates the Brooklyn B/D/N/Q/R branches from everything
  else without needing a GTFS feed.
- **Destination scope**: destinations on `--dest-side` (default north)
  of the same boundary latitude,
  i.e. trips that actually cross the junction;
  intra-Brooklyn trips that never reach it are excluded.
  The boundary complex itself counts as a valid destination by default.
- **One-seat ride**: true if some route in `--routes`
  serves both origin and destination.
  `--primary-routes` (a subset of `--routes`)
  marks which routes actually cross the boundary junction.
  A route in `--routes` but not `--primary-routes`
  (e.g. R, which reaches Manhattan via the Montague St Tunnel
  and never goes near DeKalb/Atlantic)
  only makes a trip one-seat
  if the destination isn't served by any primary route either;
  otherwise a real transfer at the junction is assumed,
  matching actual rider behavior
  even though the OD data has no transfer field.
- **Close to the other trunk**: for one-seat trips,
  `--trunk-a`/`--trunk-b` (default B,D / N,Q)
  define the two trunks being compared.
  A trip whose one-seat connection doesn't use any primary route at all
  is trivially close
  (deinterlining can't affect a trip that never crosses the junction).
  Otherwise, a destination already served by both trunks
  (e.g. Herald Sq, Atlantic Av-Barclays Ctr) is trivially close (0m);
  a single-trunk destination is compared by haversine distance,
  using per-physical-station coordinates,
  against every station on the other trunk system-wide,
  and flagged close within `--close-threshold-m`
  (default 300m, roughly one long Manhattan avenue block).

## How regions are defined

`regional-flow`'s `Region` abstraction
([`src/mta_od_data/analyze/regions.py`](src/mta_od_data/analyze/regions.py))
is just a name plus a predicate over a station,
so its containment test can be backed
by whatever's available for a given region. Currently:

- **`--region cbd`** (the default): the source station data's own curated
  `cbd` flag, i.e. Manhattan's real Congestion Relief Zone boundary,
  not a latitude cut.
  Manhattan's grid is rotated relative to true north,
  so no single latitude cleanly separates "below 60th St,"
  and a latitude cut would also wrongly include Roosevelt Island
  (south of 60th St by latitude, but not part of the zone),
  which `cbd` correctly excludes.
- **`--region manhattan`/`brooklyn`/`queens`/`bronx`/`staten-island`**:
  the station data's `borough` column.
- **`--region-borough M,Bk`**: a custom combination of boroughs
  (overrides `--region`), for regions like "Manhattan + Brooklyn."
- **`--region-bbox MIN_LAT,MIN_LON,MAX_LAT,MAX_LON`**: a lat/lon bounding
  box (overrides `--region`),
  for an ad hoc region like a rough Midtown Manhattan.

Neighborhood-level regions (Midtown, Downtown Brooklyn, etc.)
aren't built in yet:
there's no authoritative boundary data for them bundled here,
only the crude `--region-bbox` approximation above.
A geojson-polygon backend
(point-in-polygon against a real neighborhood boundary dataset,
e.g. NYC's Neighborhood Tabulation Areas)
would slot into the same `Region` abstraction without changing the CLI
shape, once there's a real geojson file to build and test it against.

## Development

```sh
uv run pre-commit install
```

installs the `git` hooks in
[`.pre-commit-config.yaml`](.pre-commit-config.yaml):
`ruff`, `ty`, `pyrefly`, and `pytest`.

[`tests/test_analyze_snapshots.py`](tests/test_analyze_snapshots.py)
reruns each `analyze` subcommand
and diffs it against its committed `.md` snapshot.
Check-only, like every other hook here:
it fails with a diff and the regen command
rather than rewriting the snapshot itself.
Skipped, not failed, without `data/mta_od.parquet`,
which is gitignored, so a fresh clone that hasn't downloaded the release asset
still gets a passing suite.
