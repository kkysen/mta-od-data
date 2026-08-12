# Scenario comparison

Average weekday ridership is the same 152,882/weekday across every scenario below -- only how many of those riders get a one-seat ride changes.

| Scenario | Total Riders | Direct 1-Seat | Direct 1-Seat % | Close 1-Seat | Effective 1-Seat | Effective 1-Seat % |
| --- | --- | --- | --- | --- | --- | --- |
| D,N on 4 Av express, B,Q on Brighton | 152,882 | 62,425 | 40.8% | 16,805 | 79,230 | 51.8% |
| B,D on 4 Av express, N,Q on Brighton | 152,882 | 52,723 | 34.5% | 22,410 | 75,132 | 49.1% |
| N,Q on 4 Av express, B,D on Brighton | 152,882 | 49,180 | 32.2% | 21,813 | 70,993 | 46.4% |

"Close one-seat" is the many-seat riders (see "Notes on reading these tables" below) close enough to an alternative not to need a materially worse trip; "Effective one-seat" is direct + close.

---

## 6 Av express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: D,N on 4 Av express, B,Q on Brighton**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Produced by `analyze-mta-od-data one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

### Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 40.8%** (62,425/weekday)
- **Close one-seat rides: 18.6%** of the riders without a direct one-seat ride (16,805 of 90,457) are within 300m of a station on one of their origin's own routes -- i.e. no train change, just a short walk at the end to reach their actual destination.
- **Effective one-seat rides (direct + close): 51.8%** (79,230/weekday) -- direct one-seat riders plus the close one-seat riders above, i.e. riders who wouldn't feel a materially worse trip.
- **Close to the other trunk if deinterlined: 64.1%** of one-seat riders (39,995 of 62,425) -- i.e. wouldn't need a materially longer walk/transfer even if 6 Av express and Broadway express stopped interlining at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R).

### Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.16% | 1-seat | True | 0m | Kings Hwy (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 2 | 548 | 0.36% | 0.88% | 1-seat | True | 0m | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 3 | 530 | 0.35% | 0.85% | 1-seat | False | 867m | 7 Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 4 | 471 | 0.31% | 0.75% | 1-seat | True | 0m | Church Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 5 | 444 | 0.29% | 0.71% | 1-seat | True | 0m | Church Av (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6 | 439 | 0.29% | 0.70% | 1-seat | True | 0m | Kings Hwy (B,Q) → DeKalb Av (B,Q,R) |
| 7 | 429 | 0.28% | 0.69% | 1-seat | False | 518m | 8 Av (N) → Canal St (6,J,Z,N,Q,R,W) |
| 8 | 409 | 0.27% | 0.65% | 1-seat | True | 0m | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 9 | 400 | 0.26% | 0.64% | 1-seat | True | 0m | 59 St (N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 10 | 392 | 0.26% | 0.63% | 1-seat | True | 274m | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 11 | 390 | 0.26% | 0.63% | 1-seat | False | 867m | Church Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 12 | 382 | 0.25% | 0.61% | 1-seat | True | 0m | Church Av (B,Q) → DeKalb Av (B,Q,R) |
| 13 | 347 | 0.23% | 0.56% | 1-seat | True | 191m | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 14 | 332 | 0.22% | 0.53% | 1-seat | True | 0m | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 15 | 330 | 0.22% | 0.53% | 1-seat | False | 565m | 79 St (D) → Grand St (B,D) |
| 16 | 328 | 0.21% | 0.53% | 1-seat | True | 191m | Church Av (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 17 | 325 | 0.21% | 0.52% | 1-seat | True | 0m | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 18 | 320 | 0.21% | 0.51% | 1-seat | True | 0m | 7 Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 19 | 317 | 0.21% | 0.51% | 1-seat | True | 0m | Sheepshead Bay (B,Q) → DeKalb Av (B,Q,R) |
| 20 | 310 | 0.20% | 0.50% | 1-seat | False | 565m | Bay Pkwy (D) → Grand St (B,D) |
| 21 | 310 | 0.20% | -- | xfer | True | 0m | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.49% | 1-seat | True | 0m | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | 0.49% | 1-seat | True | 191m | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.49% | 1-seat | True | 0m | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | 0.49% | 1-seat | False | 867m | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

### Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 62,425/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 12.55% | 100% | 0m | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 8,565 | 78.5% | 10.77% | 100% | 0m | Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6,250 | 73.0% | 7.30% | 0% | 867m | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 5,768 | 76.1% | 7.03% | 0% | 518m | Canal St (6,J,Z,N,Q,R,W) |
| 6,000 | 71.9% | 6.91% | 100% | 191m | Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 5,521 | 64.3% | 5.69% | 0% | 565m | Grand St (B,D) |
| 5,513 | 55.2% | 4.87% | 100% | 0m | DeKalb Av (B,Q,R) |
| 4,179 | 65.7% | 4.40% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 3,476 | 69.4% | 3.86% | 100% | 191m | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 2,167 | 81.3% | 2.82% | 100% | 217m | 57 St-7 Av (N,Q,R,W) |
| 3,612 | 44.6% | 2.58% | 100% | 0m | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) |
| 2,413 | 65.9% | 2.55% | 100% | 166m | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 3,283 | 48.3% | 2.54% | 100% | 0m | Jay St-MetroTech (A,C,F,R) |
| 2,444 | 60.5% | 2.37% | 0% | 699m | W 4 St-Wash Sq (A,C,E,B,D,F,M) |
| 2,210 | 63.8% | 2.26% | 0% | 413m | 59 St-Columbus Circle (1,A,C,B,D) |
| 2,191 | 61.2% | 2.15% | 0% | 1693m | 72 St (Q) |
| 2,542 | 40.6% | 1.65% | 100% | 0m | Borough Hall/Court St (2,3,4,5,R) |
| 1,988 | 46.0% | 1.46% | 100% | 0m | Whitehall St-South Ferry (1,R,W) |
| 982 | 73.7% | 1.16% | 0% | 1322m | Lexington Av/63 St (M,Q) |
| 898 | 73.3% | 1.05% | 100% | 217m | 7 Av (E,B,D) |
| 1,126 | 57.7% | 1.04% | 0% | 1693m | 86 St (Q) |
| 1,002 | 63.5% | 1.02% | 0% | 1687m | 96 St (Q) |
| 1,351 | 39.5% | 0.85% | 100% | 274m | 49 St (N,R,W) |
| 1,447 | 34.7% | 0.80% | 0% | 1152m | Lexington Av/59 St (4,5,6,N,R,W) |
| 957 | 51.6% | 0.79% | 100% | 0m | City Hall (R,W) |

### Notes on reading these tables

- "Close?"/"Dist" mean different things depending on `Type`. For `1-seat` rows: distance from the destination to the nearest station on the trunk *not* used to reach it one-seat (6 Av express vs Broadway express) -- i.e. how exposed that one-seat ride is to a generic future deinterlining; `True`/`0m` covers destinations already served by both trunks, and one-seat connections that never actually cross the junction (via a route in the universe but not in `--primary-routes`) -- those can't be affected by deinterlining either way. For `xfer` rows (riders without a direct one-seat ride): distance to the nearest station on one of the origin's own routes -- a close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination. Both thresholded at 300m.
- In the per-destination table, "Close?"/"Dist" cover only that destination's classified *one-seat* pairs (ridership-weighted), matching the table's one-seat focus -- see the CSV or the per-pair table above for the `xfer` close/dist data.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_actual.csv`), if one was written.

---

## 6 Av express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: B,D on 4 Av express, N,Q on Brighton**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Deinterlining scenario: 4 Av express served by B,D; Brighton served by N,Q (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

Produced by `analyze-mta-od-data one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

### Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 34.5%** (52,723/weekday)
- **Close one-seat rides: 22.4%** of the riders without a direct one-seat ride under this scenario (22,410 of 100,159) are within 300m of a station on their own corridor's assigned trunk -- i.e. no train change, just a short walk at the end to reach their actual destination.
- **Effective one-seat rides (direct + close): 49.1%** (75,132/weekday) -- direct one-seat riders plus the close one-seat riders above, i.e. riders who wouldn't feel a materially worse trip under this scenario.

### Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.37% | 1-seat | -- | -- | Kings Hwy (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 2 | 548 | 0.36% | 1.04% | 1-seat | -- | -- | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 3 | 530 | 0.35% | 1.01% | 1-seat | -- | -- | 7 Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 4 | 471 | 0.31% | 0.89% | 1-seat | -- | -- | Church Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 5 | 444 | 0.29% | 0.84% | 1-seat | -- | -- | Church Av (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6 | 439 | 0.29% | 0.83% | 1-seat | -- | -- | Kings Hwy (B,Q) → DeKalb Av (B,Q,R) |
| 7 | 429 | 0.28% | -- | xfer | False | 518m | 8 Av (N) → Canal St (6,J,Z,N,Q,R,W) |
| 8 | 409 | 0.27% | 0.77% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 9 | 400 | 0.26% | 0.76% | 1-seat | -- | -- | 59 St (N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 10 | 392 | 0.26% | -- | xfer | True | 274m | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 11 | 390 | 0.26% | 0.74% | 1-seat | -- | -- | Church Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 12 | 382 | 0.25% | 0.73% | 1-seat | -- | -- | Church Av (B,Q) → DeKalb Av (B,Q,R) |
| 13 | 347 | 0.23% | -- | xfer | True | 191m | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 14 | 332 | 0.22% | 0.63% | 1-seat | -- | -- | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 15 | 330 | 0.22% | 0.63% | 1-seat | -- | -- | 79 St (D) → Grand St (B,D) |
| 16 | 328 | 0.21% | 0.62% | 1-seat | -- | -- | Church Av (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 17 | 325 | 0.21% | 0.62% | 1-seat | -- | -- | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 18 | 320 | 0.21% | 0.61% | 1-seat | -- | -- | 7 Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 19 | 317 | 0.21% | 0.60% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → DeKalb Av (B,Q,R) |
| 20 | 310 | 0.20% | 0.59% | 1-seat | -- | -- | Bay Pkwy (D) → Grand St (B,D) |
| 21 | 310 | 0.20% | -- | xfer | True | 0m | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.58% | 1-seat | -- | -- | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | 0.58% | 1-seat | -- | -- | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.58% | 1-seat | -- | -- | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | 0.58% | 1-seat | -- | -- | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

### Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 52,723/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 14.86% | 100% | 0m | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 8,565 | 78.5% | 12.76% | 100% | 0m | Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 5,513 | 77.2% | 8.07% | 100% | 0m | DeKalb Av (B,Q,R) |
| 5,521 | 62.6% | 6.56% | 0% | 606m | Grand St (B,D) |
| 6,250 | 52.1% | 6.17% | 58% | 361m | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 6,000 | 48.3% | 5.50% | 100% | 86m | Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 5,768 | 37.9% | 4.15% | 36% | 333m | Canal St (6,J,Z,N,Q,R,W) |
| 3,612 | 44.6% | 3.06% | 0% | 1044m | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) |
| 3,283 | 48.3% | 3.01% | 0% | 387m | Jay St-MetroTech (A,C,F,R) |
| 4,179 | 34.1% | 2.70% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 3,476 | 38.7% | 2.55% | 100% | 191m | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 2,191 | 61.2% | 2.54% | 0% | 1365m | 72 St (Q) |
| 2,167 | 59.9% | 2.46% | 100% | 97m | 57 St-7 Av (N,Q,R,W) |
| 2,542 | 40.6% | 1.96% | 0% | 729m | Borough Hall/Court St (2,3,4,5,R) |
| 1,988 | 46.0% | 1.73% | 0% | 2141m | Whitehall St-South Ferry (1,R,W) |
| 2,444 | 36.5% | 1.69% | 0% | 841m | W 4 St-Wash Sq (A,C,E,B,D,F,M) |
| 2,413 | 34.8% | 1.59% | 29% | 653m | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 2,210 | 36.9% | 1.55% | 0% | 413m | 59 St-Columbus Circle (1,A,C,B,D) |
| 982 | 73.7% | 1.37% | 49% | 796m | Lexington Av/63 St (M,Q) |
| 1,126 | 57.7% | 1.23% | 0% | 1851m | 86 St (Q) |
| 1,002 | 63.5% | 1.21% | 0% | 2165m | 96 St (Q) |
| 957 | 51.6% | 0.94% | 0% | 1018m | City Hall (R,W) |
| 1,110 | 44.3% | 0.93% | 0% | 744m | 23 St (R,W) |
| 1,447 | 31.5% | 0.86% | 51% | 565m | Lexington Av/59 St (4,5,6,N,R,W) |
| 1,351 | 31.1% | 0.80% | 100% | 117m | 49 St (N,R,W) |

### Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the trunk the origin's *own* corridor got assigned in this scenario, thresholded at 300m. They only apply to `xfer` rows -- riders without a direct one-seat ride under this scenario -- since a `1-seat` row already has a direct train and needs no walk. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination.
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified many-seat pairs.
- `1-seat` rows have no close/dist value since the classification only applies to trips without a direct one-seat ride under this scenario.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_a.csv`), if one was written.

---

## 6 Av express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: N,Q on 4 Av express, B,D on Brighton**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Deinterlining scenario: 4 Av express served by N,Q; Brighton served by B,D (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

Produced by `analyze-mta-od-data one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

### Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 32.2%** (49,180/weekday)
- **Close one-seat rides: 21.0%** of the riders without a direct one-seat ride under this scenario (21,813 of 103,702) are within 300m of a station on their own corridor's assigned trunk -- i.e. no train change, just a short walk at the end to reach their actual destination.
- **Effective one-seat rides (direct + close): 46.4%** (70,993/weekday) -- direct one-seat riders plus the close one-seat riders above, i.e. riders who wouldn't feel a materially worse trip under this scenario.

### Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.47% | 1-seat | -- | -- | Kings Hwy (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 2 | 548 | 0.36% | 1.11% | 1-seat | -- | -- | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 3 | 530 | 0.35% | -- | xfer | False | 867m | 7 Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 4 | 471 | 0.31% | 0.96% | 1-seat | -- | -- | Church Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 5 | 444 | 0.29% | 0.90% | 1-seat | -- | -- | Church Av (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6 | 439 | 0.29% | 0.89% | 1-seat | -- | -- | Kings Hwy (B,Q) → DeKalb Av (B,Q,R) |
| 7 | 429 | 0.28% | 0.87% | 1-seat | -- | -- | 8 Av (N) → Canal St (6,J,Z,N,Q,R,W) |
| 8 | 409 | 0.27% | 0.83% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 9 | 400 | 0.26% | 0.81% | 1-seat | -- | -- | 59 St (N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 10 | 392 | 0.26% | 0.80% | 1-seat | -- | -- | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 11 | 390 | 0.26% | -- | xfer | False | 867m | Church Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 12 | 382 | 0.25% | 0.78% | 1-seat | -- | -- | Church Av (B,Q) → DeKalb Av (B,Q,R) |
| 13 | 347 | 0.23% | 0.71% | 1-seat | -- | -- | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 14 | 332 | 0.22% | 0.67% | 1-seat | -- | -- | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 15 | 330 | 0.22% | -- | xfer | False | 565m | 79 St (D) → Grand St (B,D) |
| 16 | 328 | 0.21% | -- | xfer | True | 191m | Church Av (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 17 | 325 | 0.21% | 0.66% | 1-seat | -- | -- | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 18 | 320 | 0.21% | 0.65% | 1-seat | -- | -- | 7 Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 19 | 317 | 0.21% | 0.64% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → DeKalb Av (B,Q,R) |
| 20 | 310 | 0.20% | -- | xfer | False | 565m | Bay Pkwy (D) → Grand St (B,D) |
| 21 | 310 | 0.20% | -- | xfer | True | 0m | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.62% | 1-seat | -- | -- | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | -- | xfer | True | 191m | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.62% | 1-seat | -- | -- | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | -- | xfer | False | 867m | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

### Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 49,180/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 15.93% | 100% | 0m | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 8,565 | 78.5% | 13.68% | 100% | 0m | Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 5,513 | 77.2% | 8.65% | 100% | 0m | DeKalb Av (B,Q,R) |
| 5,768 | 48.4% | 5.67% | 30% | 362m | Canal St (6,J,Z,N,Q,R,W) |
| 4,179 | 50.4% | 4.29% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 6,000 | 34.7% | 4.24% | 100% | 131m | Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 6,250 | 29.7% | 3.78% | 29% | 617m | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 3,612 | 44.6% | 3.28% | 0% | 1104m | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) |
| 3,476 | 46.1% | 3.26% | 100% | 191m | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 3,283 | 48.3% | 3.22% | 0% | 387m | Jay St-MetroTech (A,C,F,R) |
| 5,521 | 27.0% | 3.03% | 0% | 586m | Grand St (B,D) |
| 2,413 | 48.3% | 2.37% | 50% | 507m | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 2,444 | 42.8% | 2.13% | 0% | 800m | W 4 St-Wash Sq (A,C,E,B,D,F,M) |
| 2,542 | 40.6% | 2.10% | 0% | 729m | Borough Hall/Court St (2,3,4,5,R) |
| 2,210 | 46.3% | 2.08% | 0% | 413m | 59 St-Columbus Circle (1,A,C,B,D) |
| 1,988 | 46.0% | 1.86% | 0% | 2186m | Whitehall St-South Ferry (1,R,W) |
| 1,447 | 46.1% | 1.36% | 47% | 614m | Lexington Av/59 St (4,5,6,N,R,W) |
| 1,351 | 43.7% | 1.20% | 100% | 137m | 49 St (N,R,W) |
| 2,191 | 26.4% | 1.18% | 0% | 1560m | 72 St (Q) |
| 2,167 | 26.1% | 1.15% | 100% | 170m | 57 St-7 Av (N,Q,R,W) |
| 957 | 51.6% | 1.00% | 0% | 1001m | City Hall (R,W) |
| 1,110 | 44.3% | 1.00% | 0% | 816m | 23 St (R,W) |
| 898 | 50.4% | 0.92% | 100% | 217m | 7 Av (E,B,D) |
| 720 | 52.7% | 0.77% | 0% | 631m | 8 St-NYU (R,W) |
| 810 | 44.7% | 0.74% | 45% | 399m | 5 Av/59 St (N,R,W) |

### Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the trunk the origin's *own* corridor got assigned in this scenario, thresholded at 300m. They only apply to `xfer` rows -- riders without a direct one-seat ride under this scenario -- since a `1-seat` row already has a direct train and needs no walk. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination.
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified many-seat pairs.
- `1-seat` rows have no close/dist value since the classification only applies to trips without a direct one-seat ride under this scenario.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_b.csv`), if one was written.
