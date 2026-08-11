# Scenario comparison

Average weekday ridership is the same 152,882/weekday across every scenario below -- only how many of those riders get a one-seat ride changes.

| Scenario | Direct one-seat % | Effective one-seat % (direct + close) |
| --- | --- | --- |
| today's actual routing | 40.8% | -- |
| B,D on 4 Ave express, N,Q,R on Brighton | 37.5% | 54.8% |
| N,Q,R on 4 Ave express, B,D on Brighton | 35.4% | 52.3% |

`--` marks today's actual routing: it has no "effective one-seat" figure because that metric only applies under a corridor scenario (crediting riders who lose their direct one-seat ride but stay close to an alternative). Today's actual routing answers a different question instead -- of *today's* one-seat riders, how many would stay close to the other trunk if deinterlined generically -- see its own section below for that number.

---

# 6 Ave express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: today's actual routing**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Produced by `scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

## Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 40.8%** (62,425/weekday)
- **Close to the other trunk if deinterlined: 64.1%** of one-seat riders (39,995 of 62,425) -- i.e. wouldn't need a materially longer walk/transfer even if 6 Ave express and Broadway express stopped interlining at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R).

## Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % of total | % of one-seat | Type | Close? | Dist | Origin → Destination |
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
| 21 | 310 | 0.20% | -- | xfer | -- | -- | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.49% | 1-seat | True | 0m | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | 0.49% | 1-seat | True | 191m | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.49% | 1-seat | True | 0m | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | 0.49% | 1-seat | False | 867m | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

## Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 62,425/weekday one-seat total).

| Riders | One-seat % | % of all one-seat | Close? | Dist | Destination |
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

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the trunk *not* used to reach it one-seat (6 Ave express vs Broadway express), thresholded at 300m. In the per-pair table this is a single trip's classification; `True`/`0m` covers destinations already served by both trunks, and one-seat connections that never actually cross the junction (via a route in the universe but not in `--primary-routes`) -- those can't be affected by deinterlining either way.
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified one-seat pairs.
- `xfer` rows have no close/dist value since the classification only applies to one-seat trips.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_actual.csv`), if one was written.

---

# 6 Ave express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: B,D on 4 Ave express, N,Q,R on Brighton**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Deinterlining scenario: 4 Ave express served by B,D; Brighton served by N,Q,R (each origin's one-seat eligibility uses these assigned routes instead of its real current routes; a station touching both corridors keeps access to both).

Produced by `scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

## Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 37.5%** (57,398/weekday)
- **Close one-seat rides: 27.6%** of the riders without a direct one-seat ride under this scenario (26,361 of 95,483) are within 300m of a station on their own corridor's assigned trunk -- i.e. no train change, just a short walk at the end to reach their actual destination.
- **Effective one-seat rides (direct + close): 54.8%** (83,760/weekday) -- direct one-seat riders plus the close one-seat riders above, i.e. riders who wouldn't feel a materially worse trip under this scenario.

## Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % of total | % of one-seat | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.26% | 1-seat | -- | -- | Kings Hwy (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 2 | 548 | 0.36% | 0.95% | 1-seat | -- | -- | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 3 | 530 | 0.35% | 0.92% | 1-seat | -- | -- | 7 Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 4 | 471 | 0.31% | 0.82% | 1-seat | -- | -- | Church Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 5 | 444 | 0.29% | 0.77% | 1-seat | -- | -- | Church Av (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6 | 439 | 0.29% | 0.76% | 1-seat | -- | -- | Kings Hwy (B,Q) → DeKalb Av (B,Q,R) |
| 7 | 429 | 0.28% | -- | xfer | False | 518m | 8 Av (N) → Canal St (6,J,Z,N,Q,R,W) |
| 8 | 409 | 0.27% | 0.71% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 9 | 400 | 0.26% | 0.70% | 1-seat | -- | -- | 59 St (N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 10 | 392 | 0.26% | -- | xfer | True | 274m | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 11 | 390 | 0.26% | 0.68% | 1-seat | -- | -- | Church Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 12 | 382 | 0.25% | 0.67% | 1-seat | -- | -- | Church Av (B,Q) → DeKalb Av (B,Q,R) |
| 13 | 347 | 0.23% | -- | xfer | True | 191m | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 14 | 332 | 0.22% | 0.58% | 1-seat | -- | -- | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 15 | 330 | 0.22% | 0.58% | 1-seat | -- | -- | 79 St (D) → Grand St (B,D) |
| 16 | 328 | 0.21% | 0.57% | 1-seat | -- | -- | Church Av (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 17 | 325 | 0.21% | 0.57% | 1-seat | -- | -- | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 18 | 320 | 0.21% | 0.56% | 1-seat | -- | -- | 7 Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 19 | 317 | 0.21% | 0.55% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → DeKalb Av (B,Q,R) |
| 20 | 310 | 0.20% | 0.54% | 1-seat | -- | -- | Bay Pkwy (D) → Grand St (B,D) |
| 21 | 310 | 0.20% | -- | xfer | True | 0m | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.53% | 1-seat | -- | -- | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | 0.53% | 1-seat | -- | -- | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.53% | 1-seat | -- | -- | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | 0.53% | 1-seat | -- | -- | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

## Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 57,398/weekday one-seat total).

| Riders | One-seat % | % of all one-seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 13.65% | 100% | 0m | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 8,565 | 78.5% | 11.72% | 100% | 0m | Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 5,513 | 77.2% | 7.41% | 100% | 0m | DeKalb Av (B,Q,R) |
| 5,521 | 62.6% | 6.02% | 0% | 602m | Grand St (B,D) |
| 6,250 | 52.1% | 5.67% | 42% | 500m | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 6,000 | 48.3% | 5.05% | 100% | 116m | Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 3,612 | 69.0% | 4.34% | 0% | 1333m | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) |
| 5,768 | 37.9% | 3.81% | 25% | 388m | Canal St (6,J,Z,N,Q,R,W) |
| 3,283 | 64.9% | 3.71% | 0% | 387m | Jay St-MetroTech (A,C,F,R) |
| 2,542 | 70.0% | 3.10% | 0% | 729m | Borough Hall/Court St (2,3,4,5,R) |
| 4,179 | 34.1% | 2.48% | 100% | 259m | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 1,988 | 71.4% | 2.47% | 0% | 2341m | Whitehall St-South Ferry (1,R,W) |
| 3,476 | 38.7% | 2.35% | 100% | 178m | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 2,191 | 61.2% | 2.34% | 0% | 1441m | 72 St (Q) |
| 2,167 | 59.9% | 2.26% | 100% | 131m | 57 St-7 Av (N,Q,R,W) |
| 2,444 | 36.5% | 1.56% | 8% | 641m | W 4 St-Wash Sq (A,C,E,B,D,F,M) |
| 2,413 | 34.8% | 1.46% | 100% | 153m | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 2,210 | 36.9% | 1.42% | 0% | 413m | 59 St-Columbus Circle (1,A,C,B,D) |
| 1,110 | 70.9% | 1.37% | 0% | 945m | 23 St (R,W) |
| 982 | 73.7% | 1.26% | 39% | 904m | Lexington Av/63 St (M,Q) |
| 1,126 | 57.7% | 1.13% | 0% | 1851m | 86 St (Q) |
| 957 | 67.5% | 1.13% | 0% | 1245m | City Hall (R,W) |
| 1,002 | 63.5% | 1.11% | 0% | 2165m | 96 St (Q) |
| 885 | 67.3% | 1.04% | 0% | 7689m | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 720 | 73.1% | 0.92% | 0% | 635m | 8 St-NYU (R,W) |

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the trunk the origin's *own* corridor got assigned in this scenario, thresholded at 300m. They only apply to `xfer` rows -- riders without a direct one-seat ride under this scenario -- since a `1-seat` row already has a direct train and needs no walk. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination.
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified indirect (non-direct-one-seat) pairs.
- `1-seat` rows have no close/dist value since the classification only applies to trips without a direct one-seat ride under this scenario.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_a.csv`), if one was written.

---

# 6 Ave express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

**Scenario: N,Q,R on 4 Ave express, B,D on Brighton**

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Deinterlining scenario: 4 Ave express served by N,Q,R; Brighton served by B,D (each origin's one-seat eligibility uses these assigned routes instead of its real current routes; a station touching both corridors keeps access to both).

Produced by `scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

## Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 35.4%** (54,186/weekday)
- **Close one-seat rides: 26.1%** of the riders without a direct one-seat ride under this scenario (25,752 of 98,695) are within 300m of a station on their own corridor's assigned trunk -- i.e. no train change, just a short walk at the end to reach their actual destination.
- **Effective one-seat rides (direct + close): 52.3%** (79,938/weekday) -- direct one-seat riders plus the close one-seat riders above, i.e. riders who wouldn't feel a materially worse trip under this scenario.

## Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % of total | % of one-seat | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.33% | 1-seat | -- | -- | Kings Hwy (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 2 | 548 | 0.36% | 1.01% | 1-seat | -- | -- | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 3 | 530 | 0.35% | -- | xfer | False | 867m | 7 Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 4 | 471 | 0.31% | 0.87% | 1-seat | -- | -- | Church Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 5 | 444 | 0.29% | 0.82% | 1-seat | -- | -- | Church Av (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 6 | 439 | 0.29% | 0.81% | 1-seat | -- | -- | Kings Hwy (B,Q) → DeKalb Av (B,Q,R) |
| 7 | 429 | 0.28% | 0.79% | 1-seat | -- | -- | 8 Av (N) → Canal St (6,J,Z,N,Q,R,W) |
| 8 | 409 | 0.27% | 0.75% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 9 | 400 | 0.26% | 0.74% | 1-seat | -- | -- | 59 St (N,R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 10 | 392 | 0.26% | 0.72% | 1-seat | -- | -- | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 11 | 390 | 0.26% | -- | xfer | False | 867m | Church Av (B,Q) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 12 | 382 | 0.25% | 0.71% | 1-seat | -- | -- | Church Av (B,Q) → DeKalb Av (B,Q,R) |
| 13 | 347 | 0.23% | 0.64% | 1-seat | -- | -- | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 14 | 332 | 0.22% | 0.61% | 1-seat | -- | -- | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 15 | 330 | 0.22% | -- | xfer | False | 565m | 79 St (D) → Grand St (B,D) |
| 16 | 328 | 0.21% | -- | xfer | True | 191m | Church Av (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 17 | 325 | 0.21% | 0.60% | 1-seat | -- | -- | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 18 | 320 | 0.21% | 0.59% | 1-seat | -- | -- | 7 Av (B,Q) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 19 | 317 | 0.21% | 0.59% | 1-seat | -- | -- | Sheepshead Bay (B,Q) → DeKalb Av (B,Q,R) |
| 20 | 310 | 0.20% | -- | xfer | False | 565m | Bay Pkwy (D) → Grand St (B,D) |
| 21 | 310 | 0.20% | -- | xfer | True | 0m | 86 St (R) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 22 | 306 | 0.20% | 0.57% | 1-seat | -- | -- | 8 Av (N) → Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 23 | 306 | 0.20% | -- | xfer | True | 191m | Kings Hwy (B,Q) → Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 24 | 304 | 0.20% | 0.56% | 1-seat | -- | -- | 36 St (D,N,R) → 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 25 | 304 | 0.20% | -- | xfer | False | 867m | Prospect Park (B,Q,S) → 14 St-Union Sq (4,5,6,L,N,Q,R,W) |

## Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the 54,186/weekday one-seat total).

| Riders | One-seat % | % of all one-seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 14.46% | 100% | 0m | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 8,565 | 78.5% | 12.41% | 100% | 0m | Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) |
| 5,513 | 77.2% | 7.85% | 100% | 0m | DeKalb Av (B,Q,R) |
| 5,768 | 48.4% | 5.15% | 30% | 362m | Canal St (6,J,Z,N,Q,R,W) |
| 3,283 | 79.5% | 4.82% | 0% | 387m | Jay St-MetroTech (A,C,F,R) |
| 3,612 | 70.0% | 4.67% | 0% | 1333m | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) |
| 4,179 | 50.4% | 3.89% | 100% | 254m | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 6,000 | 34.7% | 3.85% | 100% | 131m | Times Sq-42 St/Port Authority Bus Terminal (1,2,3,7,A,C,E,N,Q,R,W,S) |
| 6,250 | 29.7% | 3.43% | 29% | 617m | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 2,542 | 65.6% | 3.08% | 0% | 729m | Borough Hall/Court St (2,3,4,5,R) |
| 3,476 | 46.1% | 2.96% | 100% | 176m | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 5,521 | 27.0% | 2.75% | 0% | 584m | Grand St (B,D) |
| 1,988 | 70.7% | 2.59% | 0% | 2341m | Whitehall St-South Ferry (1,R,W) |
| 2,413 | 48.3% | 2.15% | 100% | 150m | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 2,444 | 42.8% | 1.93% | 9% | 634m | W 4 St-Wash Sq (A,C,E,B,D,F,M) |
| 2,210 | 46.3% | 1.89% | 0% | 413m | 59 St-Columbus Circle (1,A,C,B,D) |
| 1,110 | 66.8% | 1.37% | 0% | 945m | 23 St (R,W) |
| 957 | 77.5% | 1.37% | 0% | 1245m | City Hall (R,W) |
| 1,447 | 46.1% | 1.23% | 47% | 614m | Lexington Av/59 St (4,5,6,N,R,W) |
| 1,351 | 43.7% | 1.09% | 100% | 137m | 49 St (N,R,W) |
| 2,191 | 26.4% | 1.07% | 0% | 1560m | 72 St (Q) |
| 2,167 | 26.1% | 1.04% | 100% | 170m | 57 St-7 Av (N,Q,R,W) |
| 885 | 61.7% | 1.01% | 0% | 7689m | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 736 | 73.2% | 0.99% | 0% | 2058m | Rector St (R,W) |
| 720 | 72.5% | 0.96% | 0% | 635m | 8 St-NYU (R,W) |

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the trunk the origin's *own* corridor got assigned in this scenario, thresholded at 300m. They only apply to `xfer` rows -- riders without a direct one-seat ride under this scenario -- since a `1-seat` row already has a direct train and needs no walk. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination.
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified indirect (non-direct-one-seat) pairs.
- `1-seat` rows have no close/dist value since the classification only applies to trips without a direct one-seat ride under this scenario.
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs_b.csv`), if one was written.
