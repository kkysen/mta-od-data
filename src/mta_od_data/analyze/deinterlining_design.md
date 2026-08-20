# Design: a systemwide, scenario-based deinterlining comparator

Why `deinterlining.py` (next to this file) exists alongside
`one_seat_rides.py`, and why it's shaped the way it is.

## Context

`one-seat-rides` was built for one junction: DeKalb Av.
Adding a second (Nostrand) and attempting a third (Columbus Circle)
showed its shape--one latitude boundary,
two named corridors converging into two named trunks,
origin-side route reassignment only--doesn't generalize:

- **DeKalb / Nostrand fit**: both are two physically distinct origin
  corridors converging at one junction into two destination trunks.
  Nostrand was added with flag changes only, no code changes.
- **Columbus Circle doesn't fit**: its deinterlining is an express/local
  swap on *one* shared trunk
  (which two of A/B/C/D stop between 59 St and 145 St),
  not a corridor swap.
  There's no origin-side split to key off,
  every real CPW-local station having the same route set today,
  and `--corridor-a-assigned`/`--corridor-b-assigned`
  only ever reassign *origin*-side routes,
  never which routes serve a *destination*.
- **149 St-Grand Concourse** is bigger still:
  two physically separate changes
  (a Manhattan shuttle conversion at 135 St,
  a Bronx route redistribution at 149 St),
  involving three routes
  and possibly a synthetic "shuttle" route absent from the source station
  data.

## Why systemwide, not another boundary+corridor variant

`regional_flow.py` is already built the right way for this:
its OD-pairs query has no origin/destination filter at all,
classifying every pair
through a pluggable `Region.contains(station) -> bool` (`regions.py`).
Stretching a boundary+corridor shape
to cover topologies with no natural geographic boundary
is the wrong direction;
swapping `Region.contains` for a scenario's effective-routes lookup
is the right one.

## Which pairs are in scope

Systemwide doesn't mean every pair in the extract:
a pair is in scope if *either* end is served by one of the comparison's routes
under any scenario in it.

Either end, not the origin,
because a swap changes a trip the same way whichever direction it runs,
so scoping by the origin counted the outbound half of a commute
and dropped the inbound half of the same journey.
For the DeKalb category that's 1,576,111 riders/weekday against 2,332,194.

## Which pairs are reported

Fetching by either end is not the same question as reporting by it,
and the two came apart in practice.

A pair with only *one* end on the comparison's routes
can never be a one-seat ride under any scenario:
that needs the two ends to share a route,
which puts both of them in scope by construction.
Such a pair therefore sits in the denominator, never the numerator,
and its classification is identical in every scenario.
For the DeKalb category that's 1,494,786 of the 2,332,194 riders,
which is why the effective share reads 31.0% under every scenario
while the same swap moves 73.2% to 70.8% among both-ends riders.
It also put
`Times Sq-42 St/PABT (N,Q,R) -> Grand Central-42 St ()`
at the top of every detailed table,
a trip no scenario here can move.

So both-ends leads:
it is the headline comparison table,
and the per-scenario pair and destination tables are scoped to it.
Either-end is kept below as context,
saying how much of the system a plan touches at all.

Both-ends is not the narrow cut its name suggests.
It keeps every trip these routes could carry end to end,
including the large majority that keep their one-seat ride
whatever the scenario:
59 St-Columbus Circle to 86 St stays one-seat under every CPW swap,
and belongs in the denominator precisely because it does.
Restricting instead to pairs with an end at an *overridden* station
would be exactly complete for what changes
and wrong as a denominator,
dropping every such related-but-unchanged trip.

The split is a reporting one, not a second pass:
one query, one classification,
with each pair's contribution added to both sets of totals
(`RiderStats`, shared so the two tables can't drift apart),
and `ODPair.both_ends` recording which side a row falls on
so the CSV stays a superset of the tables.
Direct one-seat riders are necessarily identical in both,
per the argument above;
the wider scope only ever adds transfer trips.

### What both-ends scope leaves out

Two known residues, neither currently reported:

- Trips that cross the junction to a destination off the routes
  (Grand Central, Fulton St, 14 St/8 Av).
  `one-seat-rides` counts these, since it restricts only the origin side;
  for DeKalb they are 58,967 riders/weekday.
  They can never change under any scenario, so this costs context only.
- Trips with both ends on the routes
  that no scenario can nonetheless touch,
  e.g. 95 St to Whitehall St on an R that never crosses DeKalb.
  These are exactly the rows a per-pair delta report would show as zero.

## Why the numbers differ so much from `one-seat-rides`

The two scopes overlap far less than their shared subject suggests.
`one-seat-rides` is
origin on the routes and south of Atlantic Av, destination anywhere north:
163,203 riders/weekday.
Both-ends here is 837,408, and decomposes by side of that same boundary as:

| Bucket | Riders/weekday | Share |
| --- | --- | --- |
| north to north | 546,052 | 65.2% |
| south to north (the `one-seat-rides` direction) | 104,236 | 12.4% |
| north to south (the return direction) | 102,771 | 12.3% |
| south to south | 84,349 | 10.1% |

So they share only 104,236 riders.
Both-ends adds 733,172 that `one-seat-rides` excludes by construction,
and `one-seat-rides` adds the 58,967 noted above.

That two-thirds north-to-north bucket
is most of why the direct one-seat rate reads 73.2% here and 41.1% there:
it is short intra-trunk Manhattan trips
(Times Sq to Union Sq, Herald Sq to Rockefeller Ctr)
that are trivially one-seat,
where `one-seat-rides` is junction-crossing by construction,
i.e. the hardest trips only.
`one-seat-rides`' primary-route fallback classification
(see Classification below) also counts fewer trips as one-seat,
a secondary and unquantified factor.

## What a comparison reports

Levels first, and then the thing the tool exists to answer: what changed.

A scenario's own tables report levels,
and for a while that was all there was,
which left a reader subtracting two rows by hand
to get the only number they came for.
The subtraction also hides more than it shows.
A net of -19,757 direct one-seat riders for `B/D 4 Av Express`
says nothing about how many riders *gained* one (5,754 did),
nor whether those who lost one kept a walkable alternative.

Neither a signed delta nor a lost/gained column pair can say that,
because an outcome is not one-dimensional.
Each rider has a *before* and an *after*,
each one of three states (`Outcome`): direct, close, or far.
`direct -> close` and `direct -> far`
are the same drop in the direct column
and nothing like the same thing for a rider:
for DeKalb they are 9,252 riders and 18,390 riders,
and the second group is the one a plan has to answer for.
So the report is a 3x3 transition matrix
with gained/lost/net under it,
and a table of the pairs that moved.

Deltas do appear in the comparison tables,
but only as arithmetic on numbers already in the row.
They are a convenience, not the answer.

`Current` is the baseline every change is measured against.
It needs no declaring:
`combine_scenarios` offers `CURRENT` as an option in every category,
so the combination that leaves them all unchanged comes first.
`ScenarioComparisonResult.baseline` asserts that
by the scenario overriding nothing, not by its name,
which is only a label:
with two categories selected,
`Scenario.combine` would otherwise join it into `Current + Current`,
so it is named `Current` once however many were selected.

A changed pair is named by the routes serving it *today*.
Naming it from the scenario made rows contradict themselves,
a `Was direct` row labelled with two route sets sharing no route.
Its distance is the scenario's, being the walk a rider would then face.

## A scenario is a route-override map

A scenario overrides real routes
only for the stations a deinterlining plan actually changes;
every other station keeps its real current routes.
That's strictly more general than the corridor machinery,
and covers every topology found so far,
including Columbus Circle's,
which was never expressible before and falls out for free.

Overrides are add/remove pairs rather than replacement route lists,
so an author writes only what changes.

## Classification

No primary/non-primary fallback, unlike `classify_one_seat`:
a trip is one-seat if the two ends share any route at all,
even a "slower" one like the R.
A rider's real one-seat ride counts as one,
with no assumption they would or should have taken a faster alternative.

That isn't only a simplification.
Both real classification bugs found in `one_seat_rides.py`
(`86 St (R) -> DeKalb Av` wrongly requiring a transfer;
`4 Av-9 St` picking up a spurious `B` as an assumed express partner)
were rooted entirely in that fallback.
Dropping it removes `origin_express_partners`,
`prefer_primary`'s express-preference role,
and `xfer_applicable_routes`, and the bug surface with them.
"Close one-seat" for a genuine transfer,
where the two ends share no route at all, is unaffected.

### Close one-seat is symmetric, and measured at both ends

A rider with no one-seat ride has two ways to walk into one,
and no reason to prefer either:

- walk at the destination end:
  ride your own corridor to the station nearest the destination,
  and walk from there;
- walk at the origin end:
  walk to the nearest station served by a route reaching the destination,
  and ride that one seat the whole way.

Only the first was measured at first,
inherited from `one_seat_rides.py`,
whose origin-side scoping made it the only one expressible.
It reported
`Times Sq-42 St/PABT <-> 59 St-Columbus Circle` as far, 413m,
when a rider walks 191m to 42 St-Bryant Pk and takes a B or D.
Taking the shorter of the two raised close one-seat
from 49,159 to 86,527 riders/weekday among DeKalb's both-ends riders
under `Current`,
and stopped the two scenarios tying at 79.0% effective:
`Current` now reads 83.5% against `B/D 4 Av Express`'s 82.0%,
so the swap reads as a net loss rather than as no change at all.

Measuring the origin end is also what exposed
a scenario-blind corridor lookup that had been latent until then.
`assigned_points` chose corridor stations by their real
`daytime_routes`, never the scenario's,
so a walk could be measured to a station
the scenario had just moved that route away from.
Nothing caught it while only destinations were measured,
because for DeKalb no destination-side Manhattan station is overridden,
and real and effective routes agreed everywhere the lookup looked.
The origin end is precisely where the overridden stations are.
The corrected `B/D 4 Av Express` figure above is 82.0%;
before the fix the same run read 84.5%,
and reported that not one rider anywhere
lost a one-seat ride without a walkable substitute.
The general lesson, since it will recur:
anything that decides *which stations serve a route*
has to go through `Scenario.routes_of`,
because that is the one thing a scenario exists to change.

Measuring both ends is also what makes the metric symmetric,
which the underlying fact always was:
`A -> B` and `B -> A` offer the same two walks.
So every column of the pair table is a property of the *pair*,
which is why the two directions are reported as one row.
Only the rider counts are directional.

`dist_m` is a plain `float`, never `None`.
An end with no corridor to measure against is not a distance of zero,
and rendering it as `0m` said the opposite of what was meant
(that the station is *on* the corridor).
With both ends measured, at least one is always measurable
for any pair the scope query fetched,
so `close_lookup` asserts rather than carrying a null,
following `one_seat_rides.py`'s `assert candidates`
(commit `d3d031a`, which likewise removed an Optional
by guaranteeing the case instead of encoding it).
The 0.0 that *is* kept is a one-seat ride's,
where the ridden route stops at both ends and there is no walk:
a real measurement, as in `one_seat_rides.py`.

## Relationship to `one-seat-rides`

Separate while this one is proven out,
rather than deleting or replacing anything
before a replacement is shown strictly better.
Both commands ask the same question--is this trip one-seat--one scoped
systemwide and one to a boundary and corridors,
so that redundancy is worth revisiting:
whether this replaces `one-seat-rides`,
whether that becomes a thin wrapper for the boundary-scoped detailed
report, or whether a real reason to keep both turns up.

A genuinely new command name is warranted when RAPTOR lands,
since the tool then answers a qualitatively different question.

## Known gap: the route data is weekday-only

`daytime_routes`, the only route field either station reference CSV has,
is documented (per its `data.ny.gov` metadata)
as the subway routes serving a station **during weekdays**.
So every run silently uses weekday route membership,
whatever `--day-type` or `--days` says.
This affects every command here, not just this one, and is unfixed.

Static GTFS (`calendar.txt`/`trips.txt`)
would give real service-day-aware membership.

## GTFS and RAPTOR sequencing

**RAPTOR: later.**
One-seat classification is a set intersection;
RAPTOR is only needed
for transfer-count, transfer-quality, and trip-time questions
(Herald Sq being a shorter transfer than Atlantic Av;
a 4 Av-to-Brighton rider making two easy cross-platform transfers
rather than one bad one).

Deferring it isn't wasted effort.
Static GTFS ingestion is RAPTOR's core input anyway,
and worth having on its own for the gap above.
And the classification logic RAPTOR would eventually make obsolete
is a set intersection, cheap to replace later.

GTFS-RT is a different, harder problem, and not needed for any of this.

## Still open

- **Synthetic routes** (149 St's shuttle):
  how a scenario declares a route with no real geo/platform data,
  and how the close-one-seat distance search degrades
  when it can't look one up.
  `min_dist_to_corridor` returns `None` for an unmeasurable end
  rather than crashing,
  and `close_lookup` falls back to the other end,
  so a synthetic route costs precision rather than the whole row.
  It asserts only if *both* ends are unmeasurable.
