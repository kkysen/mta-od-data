# `mta-od-data analyze`: OD analyses

These read only the OD Parquet from `mta-od-data prepare` (`data/mta_od_2025.parquet`),
so they run without any routing.
Each takes `--csv-out` for row-level detail and `--markdown-out` for a report,
and every committed report here has its own `Produced by` line with its exact invocation.
Run any subcommand's `--help` for every option.

MTA has floated "deinterlining" several subway junctions:
no longer letting two route pairs cross between trunks,
in exchange for more reliable service.
`one-seat-rides` and `deinterlining` quantify what that means for riders.
Two junctions are tracked by both:

- **DeKalb Av**: no longer letting B/D (6 Av express trunk)
  and N/Q (Broadway express trunk) trains cross between trunks in Manhattan,
  for weekday trips on B/D/N/Q/R
  originating south of Atlantic Av-Barclays Ctr in Brooklyn.
- **Nostrand/Rogers Junction**: MTA's planned reroute of 2,3 to the Nostrand Av Line
  and 4,5 to Eastern Pkwy/New Lots
  (today's actual routing interlines 2,5/3,4),
  for weekday trips on 2,3,4,5 originating south of Franklin Av.

## `one-seat-rides`

For weekday trips crossing one junction,
what share are one-seat rides,
and of riders who'd lose one under a deinterlining scenario,
what share end a short walk from the *other* trunk anyway?

```sh
uv run mta-od-data analyze one-seat-rides --routes B,D,N,Q,R \
    --primary-routes B,D,N,Q --trunk-b N,Q,R \
    --csv-out data/dekalb_weekday_pairs.csv \
    --markdown-out src/mta_od_data/analyze/dekalb_one_seat_rides.md
```

It resolves the origin station set,
queries the Parquet for average-weekday ridership by (origin, destination) pair,
and prints a summary plus per-origin and per-destination breakdowns.
Everything is parameterized via CLI flags,
so the same command covers other day types, other station criteria, other data extracts,
and other deinterlining scenarios entirely (different junction, different trunk pairs).
See the module docstring for worked examples.

Reports:
[`dekalb_one_seat_rides.md`](dekalb_one_seat_rides.md),
[`nostrand_one_seat_rides.md`](nostrand_one_seat_rides.md).

How it classifies:

- **Origin set**: stations served by at least one route in `--routes`,
  on the `--origin-side` (default south) of `--boundary-complex-id`'s latitude
  (default Atlantic Av-Barclays Ctr).
  This is a latitude-based proxy, not real route topology,
  but it cleanly separates the Brooklyn B/D/N/Q/R branches from everything else
  without needing a GTFS feed.
- **Destination scope**: destinations on `--dest-side` (default north) of the same latitude,
  i.e. trips that actually cross the junction;
  intra-Brooklyn trips that never reach it are excluded.
  The boundary complex itself counts as a valid destination by default.
- **One-seat ride**: true if some route in `--routes` serves both origin and destination.
  `--primary-routes` (a subset of `--routes`) marks which routes actually cross the junction.
  A route in `--routes` but not `--primary-routes`
  (e.g. R, which reaches Manhattan via the Montague St Tunnel)
  only makes a trip one-seat if no primary route serves the destination either;
  otherwise a real transfer at the junction is assumed,
  matching actual rider behavior even though the OD data has no transfer field.
- **Close to the other trunk**: for one-seat trips,
  `--trunk-a`/`--trunk-b` (default B,D / N,Q) define the two trunks.
  A trip whose one-seat connection doesn't use any primary route at all is trivially close
  (deinterlining can't affect a trip that never crosses the junction).
  Otherwise, a destination already served by both trunks
  (e.g. Herald Sq, Atlantic Av-Barclays Ctr) is trivially close (0m).
  A single-trunk destination is compared by haversine distance,
  using per-physical-station coordinates,
  against every station on the other trunk systemwide,
  and flagged close within `--close-threshold-m`
  (default 300m, roughly one long Manhattan avenue block).

## `regional-flow`

For any region, systemwide (every OD pair, no route filter):
what share of riders enter it from outside, leave it for outside,
stay entirely within it, or never touch it at all?

```sh
uv run mta-od-data analyze regional-flow --region cbd
```

Report: [`regional_flow.md`](regional_flow.md).

A `Region` ([`regions.py`](regions.py)) is a name plus a predicate over a station,
so its containment test can be backed by whatever's available. Currently:

- **`--region cbd`** (the default): the station data's own curated `cbd` flag,
  i.e. Manhattan's real Congestion Relief Zone boundary, not a latitude cut.
  Manhattan's grid is rotated relative to true north,
  so no single latitude cleanly separates "below 60th St,"
  and a latitude cut would also wrongly include Roosevelt Island
  (south of 60th St by latitude, but not part of the zone),
  which `cbd` correctly excludes.
- **`--region manhattan`/`brooklyn`/`queens`/`bronx`/`staten-island`**:
  the station data's `borough` column.
- **`--region-borough M,Bk`**: a custom combination of boroughs (overrides `--region`).
- **`--region-bbox MIN_LAT,MIN_LON,MAX_LAT,MAX_LON`**: a lat/lon bounding box
  (overrides `--region`), for an ad hoc region like a rough Midtown.

Neighborhood-level regions aren't built in yet:
there's no authoritative boundary data bundled here.
A geojson-polygon backend
(e.g. NYC's Neighborhood Tabulation Areas)
would slot into the same `Region` abstraction without changing the CLI.

## `deinterlining`

Classifies every OD pair with either end on the selected scenarios' routes
as one-seat or transfer,
under today's routing and any number of route-override scenarios,
in one pass over the same OD pairs,
for junctions `one-seat-rides`' single-boundary shape can't express.
A scenario overrides which routes serve individual stations,
so it covers express/local swaps at a single trunk (Columbus Circle)
as well as corridor swaps.
Scenarios live in [`scenarios.json5`](scenarios.json5),
grouped into categories that `--category` selects by,
each declaring the routes it covers.
Today's real routing is always compared against,
and selecting two categories runs every combination of them.

```sh
uv run mta-od-data analyze deinterlining --category Nostrand
```

Design: [`deinterlining_design.md`](deinterlining_design.md).
Reports:
[`dekalb_deinterlining.md`](dekalb_deinterlining.md),
[`nostrand_deinterlining.md`](nostrand_deinterlining.md),
[`fm_swap_deinterlining.md`](fm_swap_deinterlining.md).
