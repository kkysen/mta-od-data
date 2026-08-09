# MTA OD data: DeKalb Ave deinterlining analysis

MTA has floated "deinterlining" DeKalb Ave, i.e. no longer letting B/D
(6 Ave express trunk) and N/Q (Broadway express trunk) trains cross between
trunks in Manhattan. This analyzes MTA's public subway origin-destination
ridership data to quantify, for weekday trips on B/D/N/Q/R originating south
of Atlantic Av-Barclays Ctr in Brooklyn:

1. What share are one-seat rides (no transfer needed)?
2. Of those one-seat rides, what share would still be a short walk from the
   *other* trunk even if deinterlining happened, i.e. riders who wouldn't
   really be stranded by losing the DeKalb interline?

See `RESULTS.md` for the current output (headline numbers plus the top 25
origin/destination pairs and top 25 destination stations).

## Data

- **OD ridership**: MTA's "Subway Origin-Destination Ridership Estimate"
  extract (not committed here, see `.gitignore` — it's a 13GB CSV). Each row
  is an (origin station complex, destination station complex, date, hour)
  with an estimated rider count. Get it from
  [data.ny.gov](https://data.ny.gov/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/jsu2-fbtj)
  (2024 vintage used here; there's a separate dataset per year) and drop the
  CSV (or its `.xz`) in the project root.
- **Station reference data**: fetched automatically from `data.ny.gov` —
  the "Subway Stations and Complexes" dataset (resource `5f5g-n3cz`, one row
  per station complex: borough, routes served, lat/long) and the
  per-physical-station dataset (resource `39hk-dx4f`), used because a
  complex can merge multiple physical stations (e.g. Times Sq-42
  St/Port Authority Bus Terminal) whose combined centroid can sit well away
  from any actual platform — the per-station points give accurate
  nearest-station distances instead.

## Scripts

All Python runs through `uv` (PEP 723 inline script metadata, `duckdb` as
the only dependency — no venv or requirements file needed).

### `scripts/01_prepare_data.py`

Fetches the station reference CSVs and converts the OD CSV(s) into Parquet
(`data/mta_od.parquet`) for fast repeated querying. Re-runnable as new OD
extracts are released — point `--csv` at the new file(s) (globs work) and/or
`--out` at a new Parquet path. Run `--help` for all options.

```
uv run scripts/01_prepare_data.py
```

### `scripts/02_analyze.py`

Does the actual classification: resolves the origin station set, queries the
Parquet file for average-weekday ridership by (origin, destination) pair,
classifies each pair as one-seat or transfer, and for one-seat trips whether
the destination is close to the trunk not used to reach it. Prints a summary
plus per-origin and per-destination breakdowns, and can dump full row-level
detail with `--csv-out`.

```
uv run scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q \
    --trunk-b N,Q,R --csv-out data/dekalb_weekday_pairs.csv
```

Everything is parameterized via CLI flags so the same script covers other
day types, other station criteria, other data extracts, and other
deinterlining scenarios entirely (different junction, different trunk
pairs) — run `--help` for the full list, or see the module docstring for
worked examples.

## How the classification works

- **Origin set**: stations in `--origin-borough` (default Brooklyn) served
  by at least one route in `--routes`, on the `--origin-side` (default
  south) of `--boundary-complex-id`'s latitude (default Atlantic
  Av-Barclays Ctr). This is a latitude-based proxy, not real route topology,
  but it cleanly separates the Brooklyn B/D/N/Q/R branches from everything
  else without needing a GTFS feed.
- **Destination scope**: destinations on `--dest-side` (default north) of
  the same boundary latitude, i.e. trips that actually cross the junction —
  intra-Brooklyn trips that never reach it are excluded. The boundary
  complex itself counts as a valid destination by default.
- **One-seat ride**: true if some route in `--routes` serves both origin and
  destination. `--primary-routes` (a subset of `--routes`) marks which
  routes actually cross the boundary junction — a route in `--routes` but
  not `--primary-routes` (e.g. R, which reaches Manhattan via the Montague
  St Tunnel and never goes near DeKalb/Atlantic) only makes a trip one-seat
  if the destination isn't served by any primary route either; otherwise a
  real transfer at the junction is assumed, matching actual rider behavior
  even though the OD data has no transfer field.
- **Close to the other trunk**: for one-seat trips, `--trunk-a`/`--trunk-b`
  (default B,D / N,Q) define the two trunks being compared. A trip whose
  one-seat connection doesn't use any primary route at all is trivially
  close (deinterlining can't affect a trip that never crosses the junction).
  Otherwise, a destination already served by both trunks (e.g. Herald Sq,
  Atlantic Av-Barclays Ctr) is trivially close (0m); a single-trunk
  destination is compared by haversine distance, using per-physical-station
  coordinates, against every station on the other trunk system-wide, and
  flagged close within `--close-threshold-m` (default 300m, roughly one
  long Manhattan avenue block).
