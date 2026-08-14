# Design: a systemwide, scenario-based deinterlining comparator

Status: **draft, awaiting review** -- see `deinterlining.py` (next to this
file) for the CLI-shape scaffold this describes. No real classification
logic has been written yet; `deinterlining.py` raises `NotImplementedError`
after loading stations, deliberately.

## Context

This repo's existing `one-seat-rides` command (`one_seat_rides.py`) was
built for one junction: DeKalb Av. Over the course of adding a second
junction (Nostrand) and attempting a third (Columbus Circle), it became
clear the command's shape -- one latitude boundary, two named corridors
converging into two named trunks, origin-side route reassignment only --
doesn't generalize to every deinterlining topology:

- **DeKalb / Nostrand fit**: both are two physically distinct origin
  corridors converging at one junction into two destination trunks.
  Nostrand was added with flag changes only, no code changes.
- **Columbus Circle doesn't fit**: its deinterlining is an express/local
  swap on *one* shared trunk (which two of A/B/C/D stop at the local
  stations between 59 St and 145 St), not a corridor swap. There's no
  origin-side split to key off -- every real CPW-local station already has
  the same route set today. `one_seat_rides.py`'s `--corridor-a-assigned`/
  `--corridor-b-assigned` only ever reassigns *origin*-side effective
  routes; there's no mechanism to reassign which routes serve a
  *destination* station at all.
- **149 St-Grand Concourse** is bigger still: two physically separate
  changes (a Manhattan shuttle conversion at 135 St, and a Bronx
  route-redistribution at 149 St itself), involving three routes and
  possibly a synthetic "shuttle" route that doesn't exist in the source
  station data.

Separately: a weekend run of the existing command surfaced that
`daytime_routes` -- the only route field either station reference CSV has
-- is officially documented (per its `data.ny.gov` metadata) as "the
subway routes that serve the station **during weekdays**." Every scenario
run today, regardless of `--day-type`/`--days`, silently uses weekday
route membership. That's a separate, later piece of work (see
[GTFS and RAPTOR](#gtfs-and-raptor-sequencing) below); noted here because
it's a real accuracy gap in the same subsystem this design touches.

The user wants: a way to compare current vs. proposed routing, systemwide,
for any deinterlining scenario -- not just ones shaped like DeKalb.

## Why systemwide, not another boundary+corridor variant

`regional_flow.py` (this repo's other `analyze` command) is already built
the right way for this: its OD-pairs query has **no origin/destination
filter at all** -- it pulls every pair in the dataset and classifies each
one through a pluggable `Region.contains(station) -> bool` predicate
(`regions.py`). Stretching `one_seat_rides.py`'s boundary+corridor shape to
cover topologies that don't have a natural geographic boundary (Columbus
Circle, 149 St) is the wrong direction. Building a systemwide classifier on
`regional_flow.py`'s pattern -- swap `Region.contains` for a scenario's
effective-routes function -- is the right one.

## Core abstraction: a scenario is a route-override map

```python
Scenario = dict[int, frozenset[str]]  # complex_id -> effective routes
```

A scenario overrides real routes only for the stations a deinterlining
plan actually changes; every station absent from the map keeps its real
current routes automatically (looked up from `Station.routes`). This is
strictly more general than `one_seat_rides.py`'s corridor machinery, and
it happens to cover every topology found so far:

- **DeKalb/Nostrand-shaped** (two corridors swap which trunk they connect
  to): today's corridor-swap CLI flags already produce this kind of map --
  keep that as one *constructor* for this scenario shape, not the only way
  to build one.
- **Columbus Circle-shaped** (which routes stop at specific stations
  changes): a plain per-station override list, e.g. `{72 St: {A,C}, 81 St:
  {A,C}, ...}` for one swap direction. No corridor concept needed -- this
  was never expressible before and falls out for free from the more
  general map.
- **149 St-shaped** (multi-route redistribution, possibly a synthetic
  shuttle route): the same override map, plus explicit support for an
  invented route label with no real geo/platform data. The "close
  one-seat" distance search needs to skip or gracefully degrade for a
  synthetic route (no `stations_individual.csv` row to search against).

**Classification, once effective routes are computed for both ends of a
pair:** per the user, drop `classify_one_seat`'s primary/non-primary
fallback entirely. The new rule is just

```python
is_one_seat = bool(effective_origin_routes & effective_dest_routes & routes_universe)
```

A real one-seat ride a rider actually has today -- even on a "slower"
route like the R -- counts as one-seat. There's no assumption they would
or should have taken a faster alternative instead. This isn't only a
simplification: both real classification bugs fixed this session
(`86 St (R) -> DeKalb Av` wrongly requiring a transfer;
`4 Av-9 St` picking up a spurious `B` as an assumed express partner)
were rooted entirely in that fallback (`origin_express_partners`,
"assume they took the faster express instead").
Dropping it removes `origin_express_partners`, `prefer_primary`'s express-preference role,
and `xfer_applicable_routes` -- and the bug surface with them.
The "close one-seat" concept for a *genuine* transfer
(origin and destination share no route at all)
is unaffected and stays exactly as valuable as before.

## Relationship to `one-seat-rides`

Kept as a **separate command while under development** -- the user doesn't
want `one_seat_rides.py` touched until this one is proven out, consistent
with not deleting/replacing anything until a replacement is shown strictly
better. That's a development-time choice, not necessarily the end state:
since the systemwide comparator (without RAPTOR) asks the *same* question
`one-seat-rides` does -- is this trip one-seat? -- just scoped
systemwide instead of to one boundary+corridor, ending up with two
commands both answering "is this one-seat" would be redundant. Once this
command is proven out, revisit whether it replaces `one-seat-rides`,
whether `one-seat-rides` becomes a thin wrapper around it for the
boundary-scoped/detailed-report use case, or whether they stay separate
for a real reason found along the way.

A **new, separate command name is warranted later, specifically when
RAPTOR lands** (see below) -- at that point the tool answers a
qualitatively different question (trip time, transfer quality), which is
when a new name earns its keep. Suggestion for that future command:
`analyze deinterlining` reused as-is if this command has by then merged
into a trip-time-aware tool, or `analyze trip-times` /
`analyze journey-planner` if `deinterlining` continues to mean the
lighter one-seat-only comparator specifically.

## GTFS and RAPTOR sequencing

**RAPTOR: later, not now.** It isn't needed for one-seat classification at
all (a set-intersection question) -- only for transfer-count/
transfer-quality/trip-time questions (e.g. Herald Sq being a shorter
transfer than Atlantic Av; a 4 Av-to-Brighton rider making two easy
cross-platform transfers via the R at Atlantic Av and DeKalb, not one bad
one). Building it now would solve a problem this request doesn't have yet.

**Deferring RAPTOR isn't wasted effort**, for two reasons:

1. Static GTFS ingestion -- which RAPTOR would need as its core input
   (`stop_times.txt`) regardless -- is valuable on its own *right now*,
   independent of RAPTOR: it would fix the weekday/weekend accuracy gap
   above (`calendar.txt`/`trips.txt` give real service-day-aware route
   membership; `daytime_routes` doesn't). That's shared prerequisite work,
   not throwaway work.
2. The one-seat classification logic RAPTOR would eventually make obsolete
   (`classify_one_seat`, now just a set intersection under the
   simplification above) is small enough that replacing it later costs
   little.

**Static GTFS: worth pulling in**, as a bounded, mostly independent step --
a `prepare` addition to fetch+parse MTA's GTFS static feed, building a
per-station route-by-service-day mapping to replace/supplement
`daytime_routes`. Real prerequisite for RAPTOR later either way. GTFS-RT is
a different, harder problem (real-time, not a static reference table) --
no reason to touch it now.

**Sequencing** (per the user): the core classification refactor described
above comes first; GTFS-based service-day accuracy is a follow-up once the
core shape is settled.

## Open questions still to settle before real implementation

- **Scenario-definition CLI input.** `deinterlining.py`'s scaffold leaves
  this as a `TODO` -- candidates are a repeatable `--override
  COMPLEX_ID=ROUTE,ROUTE` flag, a small JSON/TOML scenario file, or reusing
  `one_seat_rides.py`'s corridor-swap flags as one constructor among
  several. Needs a decision before the real body is written.
- **Synthetic routes** (149 St's shuttle): how a scenario declares a route
  with no real geo/platform data, and how the "close one-seat" distance
  search degrades gracefully when it can't look one up.
- **Report shape**: reuse `one_seat_rides.py`'s top-N-pairs/
  top-N-destinations markdown tables as-is, or does systemwide scope (far
  more distinct pairs/destinations than one junction) call for something
  different?

## Rough effort shape (relative, not a schedule)

1. **Core refactor** (route-override scenario map, simplified
   `classify_one_seat`, systemwide classifier on the `regional_flow.py`
   pattern): moderate -- comparable in size to the classification fixes
   already done on `one_seat_rides.py` this session.
2. **Scenario constructors** per topology shape: corridor-swap reuses
   existing logic; express/local and multi-route-redistribution are new
   but each is just building an override dict -- mostly data entry per
   scenario, not new mechanism, once the core exists.
3. **Static GTFS ingestion**: moderate, mostly independent of (1)/(2).
4. **RAPTOR**: large, deferred, not blocking anything above.
