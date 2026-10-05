# Design: RAPTOR journey assignment for the OD data

Assign every OD trip in the MTA origin-destination dataset
to the concrete journeys (trains, transfers, walks) a rider could have taken,
using static GTFS timetables and RAPTOR.

This is deliberately separate from `analyze/` and deinterlining.
Deinterlining can consume its output later
(see `src/mta_od_data/analyze/deinterlining_design.md`,
"GTFS and RAPTOR sequencing"),
but nothing here depends on scenarios.

## Inputs and outputs

**Inputs:**

- Static GTFS for the subway, a feed version valid on the chosen service date.
  GTFS-RT is out of scope for now;
  the timetable layer should not assume static-only,
  so RT can replace it later.
- The OD Parquet produced by `prepare.py` (`data/mta_od.parquet`,
  currently all of 2025):
  (year, month, day of week, hour, origin complex, destination complex, ridership).
  The OD data is an average per (month, day of week, hour),
  not per calendar date.
- A curated transfer-time table (see below).

**Output:** Parquet, one row per journey leg, keyed by
(OD row, journey index), with:

- journey share of the OD row's ridership,
- leg kind (`ride`, `transfer`, `access`, `egress`),
- for rides: `trip_id`, route, board/alight stop, board/alight time,
- for transfers: from/to stop, walk time, wait time.

Plus a per-journey summary table
(arrival time, ride count, total walk, total wait, generalized cost)
so most analyses never touch legs.

## Prior art

### `nycriders` (`circularsquare/maps`, `riders/nycriders/build.py`)

The visualization at `https://anita.garden/nycriders/`.
No license on the repo, so reference only, no code reuse.
Same overall shape as this design
(GTFS weekday schedule + OD, RAPTOR per OD-hour, assign riders to trips).
Worth keeping:

- patterns keyed on (route, direction, exact stop sequence);
- midnight-wrapped copies of trips with times >= 24:00;
- max 3 rounds (2 transfers) as the practical cap;
- the author ships a patched `stop_times_fixed.txt`,
  so expect the raw feed to need cleaning
  (their README: "timetables are a bit wonky").

Problems to avoid:

- **Single backpointer map across rounds.**
  `journey[stop]` is overwritten by later rounds,
  so the extracted path can disagree with the computed arrival.
  We keep per-round labels.
- **Earliest-arrival only**, no Pareto set over transfers.
- **Same-stop transfers are free** in every direction
  (`tau_prev` boards directly at the alighting stop).
- **One sampled departure per OD row**:
  every rider in a (origin, destination, hour) row takes the same path,
  from a random departure second.
  We use rRAPTOR over the whole hour instead (see below).
- `service_id == "Weekday"` hard-coded.

### MTA's own assignment model

`https://www.mta.info/article/where-everybody-subway-going`
and the technical documentation it links
(`https://data.ny.gov/api/views/r7qk-6tcy/files/5cbd3068-979b-461b-a40d-56ad184c4823`).
The OD data we have is the *input* to this model's step 2.
Relevant points:

- Paths are chosen by **perceived time**:
  actual time plus multipliers on waiting, walking, and crowding,
  and **separate transfer multipliers** for
  cross-platform same-direction transfers,
  same-line opposite-direction transfers,
  and transfers across a complex.
- Riders are split into two classes, "speed-first" and "comfort-first",
  each with its own parameter set.
- A small **per-stop-passed penalty**
  keeps riders on the express until the last transfer point
  when total time ties.
- Crowding is handled by ~15 iterations of multi-class Frank-Wolfe
  with Dijkstra on a time-expanded network.
- It uses a **walking-time table for transfers**
  ("relatively static data on the subway system")
  that is not published.
- The parameter values themselves are not published.

We copy the cost *structure* (transfer classes, two rider classes,
the passing-stop tie-breaker) without crowding, at least initially.

## Algorithm

### Timetable

1. Pick a service date for each OD slice:
   a representative date for (year, month, day of week),
   e.g. the second such weekday of the month, avoiding holidays.
   Resolve active `service_id`s through
   `calendar.txt` + `calendar_dates.txt` for that date,
   never by matching `service_id` names.
2. Build patterns: trips grouped by (route, direction, stop sequence),
   sorted by departure; verify FIFO (no overtaking within a pattern)
   and split a pattern if it isn't.
3. Include trips from the previous service day still running after midnight
   (times >= 24:00), shifted by -24h,
   so times are signed seconds.
   The MTA files trips starting after midnight under the new day's service
   (`...-Sunday-00_000600_...`), so these don't double up;
   the timetable reports any trip with exactly another's times.
   On a feed version's first date the previous date is outside it,
   and its overnight trips are missing (reported, not an error).
   Consecutive versions abut (one ends 2025-11-01, the next starts 2025-11-02),
   so taking overnight trips from the previous version is a later fix.

GTFS times count from "noon minus 12h", not wall-clock midnight,
so on daylight-saving change dates (2025-11-02, 2026-03-08)
they're an hour off the OD data's wall-clock hours.
The representative-date rule must skip those.

Feed version selection is explicit (`--feed`) for now.
Some versions cover the same dates,
so automatic selection will mean
the latest-fetched version whose calendar covers the date.

On the 2025-10-18 version, a Wednesday is 8474 trips
plus 262 overnight from Tuesday (matching a DuckDB count),
in 211 patterns, none needing a FIFO split.

Stops are the directional platform stops (`101N`, `101S`),
not parent stations:
transfer cost depends on direction (see below),
and parents would hide that.
OD complexes map to their set of directional stops
via the station reference CSV's `gtfs_stop_id`.

### Transfers

**Phase 2 takes `transfers.txt` at its word**,
keyed on parent stops as the feed does:

- a same-stop row (`127,127,2,0`) is the minimum time
  between alighting and boarding at that stop,
  kept separate from footpaths so RAPTOR charges it
  (`nycriders` makes every same-stop change free);
- a stop with no same-stop row gets `DEFAULT_MIN_CHANGE`, 180s,
  what the feed gives almost every stop it lists
  (33 served stops on the 2025-10-18 version, single-line stops);
- other rows are footpaths;
- `transfer_type` 3 (not possible) rows are dropped.

The timetable reports asymmetric footpaths
and footpaths not transitively closed,
since RAPTOR relaxes footpaths once a round and assumes closure.
Every version so far has none of either.

Everything below is the plan for making it accurate later.

GTFS `transfers.txt` is not good enough on its own.
Current feed (2026-08 version):
613 rows, 504 of them a flat 180s,
463 are same-parent-stop rows (`101,101,2,180`),
no `pathways.txt`.

The 59 rows with `min_transfer_time = 0`
are exactly the express/local cross-platform stations
(`123` 72 St, `127` Times Sq, `132` 14 St, `227` Chambers, ...).
But they are keyed on the *parent* stop,
so taken literally they also make
a downtown 1 to uptown 2 at 72 St free.

Rules:

- **Same-direction at a `0` parent stop** (`123S` -> `123S`): 0s walk.
- **Opposite direction at the same parent**: real walk time
  (stairs/mezzanine), default from GTFS's 180s until curated.
- **Between parents in a complex**: GTFS value, else
  base + distance / walk speed (as `nycriders` does),
  until curated.
- **Curated overrides**: `raptor/data/transfer_times.csv`,
  keyed on directional stop IDs,
  with a `source` column (GTFS, measured, OSM-derived, estimate)
  so we know which numbers are real.

No public dataset of platform-to-platform walk times turned up.
Candidates to seed the curated table:
OSM platform/stair geometry,
Wikipedia station layout diagrams (for which platforms are shared),
and measured walks.

A zero walk time is not a zero-cost transfer:
the journey still uses another round,
and the cost model still charges a transfer penalty
(smaller for cross-platform, per the MTA's transfer classes).

### rRAPTOR

Range RAPTOR per (origin complex, hour):
run RAPTOR for every departure in the hour, latest first,
reusing labels across departures (standard rRAPTOR),
from all directional stops of the origin complex.
Labels are per round `k` (at most 3 rides),
with a backpointer per (round, stop),
so every Pareto-optimal (arrival, rides) journey per departure
is extractable without ambiguity.

Each journey is dominated by another departing no earlier
and arriving no later, with no more rides, and dropped.
What's left per (OD, hour) is the set of
non-dominated journeys over the hour.

Departure times within the hour are uniform for now
(`nycriders` skews toward the busier neighboring hour;
cheap to add later, as a weight per departure second).

### Splitting ridership across the trade-off set

The Pareto set alone gives no shares.
Each candidate journey `j` gets a generalized cost

    C_j = in_vehicle + w_wait * wait + w_walk * walk
          + sum over transfers of penalty(transfer class)
          + p_stop * stops_passed

and the OD row's ridership is split by multinomial logit,
`share_j ∝ exp(-theta * C_j)`,
over the candidates usable from each departure,
integrated uniformly across departures in the hour.
Run once per rider class (speed-first, comfort-first)
with that class's weights, then mixed by class fraction.

All weights live in one config file,
so tuning is a config change, not a code change.
Initial values are guesses; calibrating them
(e.g. against the MTA's published journey-metrics datasets)
is a later step.

Note the criteria RAPTOR itself optimizes are only (arrival, rides).
Transfer *quality* enters through walk time in the timetable
and the penalty in `C_j`,
so a journey with a bad transfer can be Pareto-optimal
yet get a small share.
If that turns out to drop good journeys
(e.g. one with an extra cross-platform transfer and the same arrival),
switch to McRAPTOR with generalized cost as a third criterion.

## Phases

Each phase is its own commit(s), verified before the next.
Complexity is added only once the simple version works end to end.

1. **GTFS fetch**: `mta-od-data fetch-gtfs` downloads every
   Mobility Database version listed in
   `src/mta_od_data/gtfs_versions.json5` into `data/gtfs/`.
   A hand-kept manifest for now; the Mobility Database API
   (free account, token) can replace it later.
2. **Timetable**: load one feed, resolve services for one date,
   build FIFO patterns. Stops at the parent level;
   transfers straight from `transfers.txt`.
   `raptor timetable --feed <zip> --date <date>` prints what it found.
3. **RAPTOR**: plain round-based earliest arrival, per-round labels,
   max 3 rides, unit-tested on tiny hand-built feeds.
   Round `k` keeps a label only if it beats every round before it,
   so the rounds reaching a target are its Pareto set over (arrival, rides).
   Each round has two labels per stop:
   arriving by train, and ready to board,
   which is arrival plus the stop's change time, or a footpath's walk time
   (not both: `transfers.txt` times between stops are the whole transfer).
   `raptor route --feed <zip> --date <date> --from <stops> --to <stops> --depart <time>`
   prints a query's journeys.
4. **rRAPTOR**: all departures in an hour, Pareto (arrival, rides) set.
5. **Assignment**: OD Parquet in, leg + journey Parquet out,
   ridership split by logit over generalized cost
   with a single flat transfer penalty.
6. **Later, in any order**:
   directional stops and the transfer rules above;
   curated `transfer_times.csv`;
   per-class transfer penalties and the two rider classes;
   passing-stop tie-breaker;
   supplemented-feed planned work;
   departure-time skew within the hour;
   McRAPTOR if needed; crowding.

## Implementation

Rust, for the core:
`nycriders` needs 8 worker processes for pure Python,
and we want full-year, all-hours runs.
Parallelize across origin complexes with `rayon`.
Read/write Parquet with `arrow`/`parquet` crates
(or `polars` if it saves enough code).

A standalone binary, not a Python extension:
it reads OD Parquet and writes leg/journey Parquet,
so the Python side only needs a subprocess call,
and the `hatchling` build stays as is
(PyO3 would mean switching to `maturin`).
Parquet is the whole interface,
so moving to PyO3 later stays possible if a tight loop needs it.

Layout: a Cargo crate at `raptor/`,
with GTFS loading, timetable building, transfers, rRAPTOR,
and assignment as separate modules,
each unit-tested on tiny hand-built feeds
(two lines, one cross-platform transfer, one opposite-direction transfer).

## GTFS archive

The OD data is 2025.

- **Mobility Database** `mdb-516` (regular feed): **used for now.**
  Public zip URLs, no key:
  `https://files.mobilitydatabase.org/mdb-516/<dataset id>/<dataset id>.zip`.
  Listing versions needs the API (token),
  so they're kept by hand in `src/mta_od_data/gtfs_versions.json5`.
  History starts with the 2025-10-18 snapshot,
  whose service starts 2025-08-11,
  so only the August (partial) through December 2025 OD months
  are routable until older feeds are found.
  Older versions also lack `feed_info.txt`,
  so service ranges come from `calendar.txt`.
- **Transitland** `f-dr5r-nyctsubway` (regular feed):
  77 versions back to 2016, covering all of 2025,
  via the REST API (`/api/v2/rest/feed_versions/<sha1>/download`)
  with a free API key. Next to try, for January through early August 2025.
- **Mobility Database** `mdb-511` (supplemented):
  daily snapshots, but only the most recent ones are visible.

**Regular vs supplemented.**
The supplemented feed is not a delta to combine with the regular one:
it *is* the regular feed with planned work for roughly the next week
merged in, superseding the affected trips.
So for a given date, the right feed is
the supplemented snapshot fetched shortly before that date,
which needs daily snapshots we mostly don't have for 2025.

It also matters less than it seems:
the OD data averages over every (say) Wednesday in a month,
so per-date planned work would have to be averaged too,
meaning RAPTOR per actual date, weighted together.
That's a reasonable later phase.
Phase 1 uses the regular feed and one representative date per
(month, day of week).

## Open questions

- **Transitland API key**: needed for January through early August 2025.
- **Representative date** rule per (month, day of week).
- **Initial cost weights** and the logit `theta`.
- **Crowding**: out of scope initially; revisit if assignments
  load trains far past capacity.
