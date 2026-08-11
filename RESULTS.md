# 6 Ave express/Broadway express deinterlining: one-seat-ride results at Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R)

Scenario: average weekday ridership (35 distinct days in the data) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R), with destinations north of Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) (i.e. trips that cross the junction).

Produced by `scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --csv-out data/dekalb_weekday_pairs.csv --markdown-out RESULTS.md`.

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
|---|---|---|---|---|---|
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
- Full row-level detail (every origin/destination pair, not just the top 25) is in the `--csv-out` file (`data/dekalb_weekday_pairs.csv`), if one was written.
