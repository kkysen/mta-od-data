# Incremental routing and reports

How a commit could reroute and recount only what its change can reach,
instead of every origin on every date,
with results proven equal to a full run.

## Where the time goes now

Measured in this session (2026-11-18):

- Full routing, 25 dates, two runs (as today and with `--street-walks`): about 8:30,
  roughly 10 s a date, most of it `assign::route` over every origin.
- September alone, 5 dates, two runs: 1:17.
- A September regeneration of every report: 3:14 to 4:37,
  most of it `ridership`'s `compute` recounting its rows
  over every date's paths, not the routing.
- A commit changing nothing the reports read: about 5 s (all cached).

So a change that reaches the routing costs routing plus recounting,
and recounting is now the bigger part on a September commit.
Both stages below matter.

## How routing is split today

`assign_dates` (`raptor/src/lib.rs`) groups the dates whose timetables route alike
(`Timetable::routes_like`), routes each group once with `assign::route`,
then splits each date's OD rows over the routes and writes its files.

`assign::route` (`raptor/src/assign.rs`) runs `route_origin` for each origin complex,
independently and in parallel:
a range query (`Router::profile`) over the whole service day from that origin's stops
to every destination's,
then each destination's journeys turned into departure intervals and interned paths.
`split` then shares each OD row's riders over its origin's intervals,
again one origin at a time (`split_origin`),
and adds each ride's riders to its train's loads (`TripLoads`),
which only accumulate: no origin's split reads another's loads.

So the natural unit of incremental work is an (origin complex, timetable group):
about 430 origins a group,
and an origin's routes and split rows depend only on the timetable, the config,
and that origin's own OD rows.
Its departure times are already inside the unit, as one range query.

## Stage 1: reroute only the origins a change can affect

### What to keep from the previous run

For each timetable group, each origin's `OriginRoutes` (intervals, path texts, legs),
which the run's `paths-*.parquet` and `path-texts-*.parquet` already hold in another form,
plus, for the tests below, a small summary per (origin, stop, round):

- the fewest seconds from leaving the origin to reaching the stop on that many rides,
  over the day's departures (`t_min`);
- the most seconds any departure takes to reach it (`t_max`), waits included;
- and which stops and footpaths any of the origin's kept journeys use.

Size: about 430 origins times about 1,500 stops (after platforms are split) times 5 rounds
(`max_rides`), two 4-byte numbers each: about 30 MB a group,
small next to a run's 2.5 GB of Parquet (`~/.cache/mta-od-data/routing/<key>/`).
The stops and footpaths used per origin are a few thousand entries each, a few MB a group.

### Finding the affected origins

By the kind of change, comparing the new timetable with the previous run's:

- **A walk or transfer removed or made longer** (a footpath `(a, b, secs)`):
  only journeys using it get worse, and only destinations whose kept journeys used it
  can change, including journeys it used to beat coming back.
  Reroute the origins any of whose kept journeys walk it.
  Exact, from the used-footpaths summary.
- **A walk or transfer added or made shorter**:
  it can only help a departure that reaches `a`
  and then reaches `b` sooner through it than without it.
  For a round `k`, it can't help origin `o` if `t_min(o, a, k) + secs >= t_max(o, b, k')`
  for every round `k' >= k`; reroute every origin it might help.
  This is a bound, not exact: it never skips an origin that changes,
  but may reroute some that don't.
  How many it rules out at a walk inside one complex is the first open question.
- **A timetable change** (a trip added, removed or retimed, a new feed version):
  a removed or slower trip is like a longer walk (origins whose journeys ride it);
  an added or faster one is like a shorter walk, bounded at the stops it serves.
  A new feed version changes too much: route it in full.
- **OD rows changed** (a new OD Parquet, new factors): no rerouting at all,
  only re-splitting the origins whose rows changed; with a new extract, all of them.
- **The config** (`raptor/assign.json5`): speeds and stair times change every walk at once,
  and `max_rides` or weights change every query or every split: route in full.
  Only the split weights could be re-split without rerouting.
- **The code** (`raptor` itself, `routing.py`): always in full.

Each affected origin is rerouted with the new timetable;
every other origin's routes and split rows are copied from the previous run,
and the date's `trips` and `platform-waits` are recomputed from the loads,
as the sum of every origin's riders on each train,
or updated by the changed origins' old and new riders.

## Stage 2: recount only the changed rows

`ridership`'s `compute` and `free-transfers`' `compare` read every date's paths.
Most of what they produce are sums over (origin, destination, path, hour) rows:
riders by station, line, route, segment and hour, and time saved.
The new sums are the previous run's,
less what the changed origins' old rows contributed, plus what their new rows do.

### What to keep

The previous run's results before they're laid out,
which `cache.py` and `cached_compare` already pickle,
broken down by origin so a changed origin's share can be taken out:
about 430 times each report's rows.
Most reports have a few thousand rows, so this is tens to hundreds of MB.
The changed origins' old rows can be read from the previous run's Parquet,
which stays in the cache.

### What isn't a plain sum

- Peaks (the busiest hour, the most crowded train): kept as per-hour or per-train sums,
  which are sums, with the peak picked after.
- Ratios (time saved per rider, riders per m²): sums of numerator and denominator.
- `DISTINCT` lists (routes, legs, lines used): kept with counts, dropping a name at zero.
- Anything truly not decomposable, if one turns up: recomputed in full.

## Proving it equal to a full run

The incremental path is only an optimization,
so every result must be byte-identical to a full run's.

- `pytest-full`, before each push, reroutes and recounts in full and compares the reports,
  so an incremental result that differs fails the push.
- A test running both paths on a small fixture (a few origins, one changed walk)
  and comparing the outputs exactly, for every kind of change above.
- At first, a debug flag that runs both and diffs them on real data, per origin.

## Order to build it in

1. **Measure first (small, no new routing code).**
   From two routing runs already in the cache that differ by one change
   (`6d13139`'s walk directions, or `79544f0`'s level climbs),
   count the origins whose paths actually changed, per date.
   That's the most stage 1 can save on that change,
   and shows whether it's worth building.
2. **Stage 2 for OD-only and report-only changes first**,
   where the changed rows are easy to find,
   and for the `ridership` recount, now the larger cost on a September commit.
3. **Stage 1 for removed or longer walks**, the exact case.
4. **Stage 1 for added or shorter walks**, with the bound, measuring how many origins it keeps.
5. **Timetable changes within a feed version.**

## Open questions

- How many origins the added-walk bound rules out in practice:
  if it keeps most of them, stage 1 needs exact per-departure labels instead,
  which are far bigger (about 150 departures per (origin, stop)).
- Whether to store the per-origin summaries in the routing run's directory,
  or keyed separately so a run without them can still be reused.
- How to key an incremental run: on its inputs, like a full one,
  plus the previous run it was built from, so it's reproducible.
- The routing cache is already 48 GB (`~/.cache/mta-od-data/routing/`),
  as entries are never deleted; incremental runs that copy most of a run would add to that,
  unless unchanged origins' files are shared by hard links.
