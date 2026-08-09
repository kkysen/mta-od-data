# DeKalb Ave deinterlining: one-seat-ride results

Scenario: average weekday ridership (35 distinct weekdays, Jan-Jul 2024) on
trains originating at Brooklyn B/D/N/Q/R stations south of Atlantic
Av-Barclays Ctr, with destinations at or north of Atlantic Av (i.e. trips
that actually cross the DeKalb/Atlantic junction). Produced by
`scripts/02_analyze.py --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R`.
See `README.md` for what the columns mean and how the classification works.

## Headline numbers

- **Total: 152,882 riders/weekday**
- **One-seat rides (no transfer): 40.8%** (62,425/weekday)
- **Close to the other trunk if deinterlined: 64.1%** of one-seat riders
  (39,995 of 62,425) — i.e. wouldn't need a materially longer walk/transfer
  even if B/D and N/Q stopped interlining at DeKalb.

## Top 25 origin/destination pairs (avg weekday riders)

| # | Riders | % of total | % of one-seat | Type | Close? | Dist | Origin → Destination |
|---|---|---|---|---|---|---|---|
| 1 | 722 | 0.47% | 1.16% | 1-seat | True | 0m | Kings Hwy (B,Q) → 34 St-Herald Sq (Manhattan) |
| 2 | 548 | 0.36% | 0.88% | 1-seat | True | 0m | 36 St (D,N,R) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 3 | 530 | 0.35% | 0.85% | 1-seat | False | 867m | 7 Av (B,Q) → 14 St-Union Sq (Manhattan) |
| 4 | 471 | 0.31% | 0.75% | 1-seat | True | 0m | Church Av (B,Q) → 34 St-Herald Sq (Manhattan) |
| 5 | 444 | 0.29% | 0.71% | 1-seat | True | 0m | Church Av (B,Q) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 6 | 439 | 0.29% | 0.70% | 1-seat | True | 0m | Kings Hwy (B,Q) → DeKalb Av (Brooklyn) |
| 7 | 429 | 0.28% | 0.69% | 1-seat | False | 518m | 8 Av (N) → Canal St (Manhattan) |
| 8 | 409 | 0.27% | 0.65% | 1-seat | True | 0m | Sheepshead Bay (B,Q) → 34 St-Herald Sq (Manhattan) |
| 9 | 400 | 0.26% | 0.64% | 1-seat | True | 0m | 59 St (N,R) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 10 | 392 | 0.26% | 0.63% | 1-seat | True | 274m | Kings Hwy (B,Q) → 47-50 Sts-Rockefeller Ctr (Manhattan) |
| 11 | 390 | 0.26% | 0.63% | 1-seat | False | 867m | Church Av (B,Q) → 14 St-Union Sq (Manhattan) |
| 12 | 382 | 0.25% | 0.61% | 1-seat | True | 0m | Church Av (B,Q) → DeKalb Av (Brooklyn) |
| 13 | 347 | 0.23% | 0.56% | 1-seat | True | 191m | Kings Hwy (B,Q) → 42 St-Bryant Pk/5 Av (Manhattan) |
| 14 | 332 | 0.22% | 0.53% | 1-seat | True | 0m | Newkirk Plaza (B,Q) → 34 St-Herald Sq (Manhattan) |
| 15 | 330 | 0.22% | 0.53% | 1-seat | False | 565m | 79 St (D) → Grand St (Manhattan) |
| 16 | 328 | 0.21% | 0.53% | 1-seat | True | 191m | Church Av (B,Q) → Times Sq-42 St/PABT (Manhattan) |
| 17 | 325 | 0.21% | 0.52% | 1-seat | True | 0m | Kings Hwy (B,Q) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 18 | 320 | 0.21% | 0.51% | 1-seat | True | 0m | 7 Av (B,Q) → 34 St-Herald Sq (Manhattan) |
| 19 | 317 | 0.21% | 0.51% | 1-seat | True | 0m | Sheepshead Bay (B,Q) → DeKalb Av (Brooklyn) |
| 20 | 310 | 0.20% | 0.50% | 1-seat | False | 565m | Bay Pkwy (D) → Grand St (Manhattan) |
| 21 | 310 | 0.20% | — | xfer | — | — | 86 St (R) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 22 | 306 | 0.20% | 0.49% | 1-seat | True | 0m | 8 Av (N) → Atlantic Av-Barclays Ctr (Brooklyn) |
| 23 | 306 | 0.20% | 0.49% | 1-seat | True | 191m | Kings Hwy (B,Q) → Times Sq-42 St/PABT (Manhattan) |
| 24 | 304 | 0.20% | 0.49% | 1-seat | True | 0m | 36 St (D,N,R) → 34 St-Herald Sq (Manhattan) |
| 25 | 304 | 0.20% | 0.49% | 1-seat | False | 867m | Prospect Park (B,Q,S) → 14 St-Union Sq (Manhattan) |

## Top 25 destination stations, summed across all origins (avg weekday riders)

Sorted by each destination's one-seat ridership (i.e. its share of the
62,425/weekday one-seat total).

| Riders | One-seat % | % of all one-seat | Close? | Dist | Destination |
|---|---|---|---|---|---|
| 9,376 | 83.5% | 12.55% | 100% | 0m | 34 St-Herald Sq (Manhattan) |
| 8,565 | 78.5% | 10.77% | 100% | 0m | Atlantic Av-Barclays Ctr (Brooklyn) |
| 6,250 | 73.0% | 7.30% | 0% | 867m | 14 St-Union Sq (Manhattan) |
| 5,768 | 76.1% | 7.03% | 0% | 518m | Canal St (Manhattan) |
| 6,000 | 71.9% | 6.91% | 100% | 191m | Times Sq-42 St/Port Authority Bus Terminal (Manhattan) |
| 5,521 | 64.3% | 5.69% | 0% | 565m | Grand St (Manhattan) |
| 5,513 | 55.2% | 4.87% | 100% | 0m | DeKalb Av (Brooklyn) |
| 4,179 | 65.7% | 4.40% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (Manhattan) |
| 3,476 | 69.4% | 3.86% | 100% | 191m | 42 St-Bryant Pk/5 Av (Manhattan) |
| 2,167 | 81.3% | 2.82% | 100% | 217m | 57 St-7 Av (Manhattan) |
| 3,612 | 44.6% | 2.58% | 100% | 0m | Chambers St/WTC/Park Place/Cortlandt St (Manhattan) |
| 2,413 | 65.9% | 2.55% | 100% | 166m | Broadway-Lafayette St/Bleecker St (Manhattan) |
| 3,283 | 48.3% | 2.54% | 100% | 0m | Jay St-MetroTech (Brooklyn) |
| 2,444 | 60.5% | 2.37% | 0% | 699m | W 4 St-Wash Sq (Manhattan) |
| 2,210 | 63.8% | 2.26% | 0% | 413m | 59 St-Columbus Circle (Manhattan) |
| 2,191 | 61.2% | 2.15% | 0% | 1693m | 72 St (Manhattan) |
| 2,542 | 40.6% | 1.65% | 100% | 0m | Borough Hall/Court St (Brooklyn) |
| 1,988 | 46.0% | 1.46% | 100% | 0m | Whitehall St-South Ferry (Manhattan) |
| 982 | 73.7% | 1.16% | 0% | 1322m | Lexington Av/63 St (Manhattan) |
| 898 | 73.3% | 1.05% | 100% | 217m | 7 Av (Manhattan) |
| 1,126 | 57.7% | 1.04% | 0% | 1693m | 86 St (Manhattan) |
| 1,002 | 63.5% | 1.02% | 0% | 1687m | 96 St (Manhattan) |
| 1,351 | 39.5% | 0.85% | 100% | 274m | 49 St (Manhattan) |
| 1,447 | 34.7% | 0.80% | 0% | 1152m | Lexington Av/59 St (Manhattan) |
| 957 | 51.6% | 0.79% | 100% | 0m | City Hall (Manhattan) |

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest
  station on the trunk *not* used to reach it one-seat (6 Ave express vs
  Broadway express), thresholded at 300m. `100%`/`0m` covers two cases:
  destinations that already have routes from both trunks (e.g. Herald Sq,
  Atlantic Av-Barclays Ctr, DeKalb Av), and one-seat connections that never
  actually cross the DeKalb/Atlantic junction at all (purely via R, e.g. Jay
  St-MetroTech, Chambers St/WTC, Borough Hall/Court St, Whitehall St) — those
  can't be affected by deinterlining either way.
- `xfer` rows have no close/dist value since the classification only applies
  to one-seat trips.
- Full row-level detail (every origin/destination pair, not just the top 25)
  is in `data/dekalb_weekday_pairs.csv`, regenerated by `scripts/02_analyze.py`.
