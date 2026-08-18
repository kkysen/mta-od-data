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

The cost is a denominator far wider than any one junction can move.
`B/D 4 Av Express` takes 19,757 riders off a direct one-seat ride,
and the systemwide effective share still reads 31.0% either way:
the close-one-seat column absorbs almost exactly what the direct column loses,
and what's left is a rounding error against 2.3M riders.
So the subset with *both* ends on the routes is reported alongside it,
837,408 riders, where the same swap reads 73.2% to 70.8% direct.
Neither number is the real one:
the wide scope says how much of the system a plan touches at all,
the narrow one says what it does to the riders it touches.

That subset is a reporting split, not a second pass:
one query, one classification,
with each pair's contribution added to both sets of totals
(`RiderStats`, shared so the two tables can't drift apart).
Direct one-seat riders are necessarily identical in both,
since sharing a route puts both ends in scope by construction;
the wider scope only ever adds transfer trips.

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
  `min_dist_to_corridor` already returns `None` rather than crashing.
