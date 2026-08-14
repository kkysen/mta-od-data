# One Seat Ride Analysis for Deinterlining 6 Av express/Broadway express at Atlantic Av (B,D,N,Q,R)

Scenario: average weekday ridership (60 distinct days in the data, 2025-01-06 to 2025-12-12) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av (B,D,N,Q,R), with destinations north of it (i.e. trips that cross the junction).

Produced by `mta-od-data analyze one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out src/mta_od_data/analyze/one_seat_rides.md`.

---

## Scenario comparison

Average weekday ridership is the same 163,203/weekday across every scenario below -- only how many of those riders get a one-seat ride changes.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| D,N on 4 Av express, B,Q on Brighton | 163,203 | 65,384 (40.1%) | 18,468 (18.9%) | 83,852 (51.4%) |
| B,D on 4 Av express, N,Q on Brighton | 163,203 | 55,794 (34.2%) | 24,215 (22.5%) | 80,009 (49.0%) |
| N,Q on 4 Av express, B,D on Brighton | 163,203 | 51,623 (31.6%) | 23,794 (21.3%) | 75,417 (46.2%) |

---

## D,N on 4 Av express, B,Q on Brighton

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 727 | 0.45% | 1.11% | 1-seat | close | 0m | Kings Hwy (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 2 | 621 | 0.38% | 0.95% | 1-seat | close | 0m | 36 St (D,N) → Atlantic Av (D,N) |  |
| 3 | 583 | 0.36% | 0.89% | 1-seat | close | 0m | 7 Av (Q) → 14 St-Union Sq (Q) |  |
| 4 | 471 | 0.29% | 0.72% | 1-seat | close | 0m | Kings Hwy (B,Q) → DeKalb Av (B,Q) |  |
| 5 | 455 | 0.28% | 0.70% | 1-seat | close | 0m | 8 Av (N) → Canal St (N) |  |
| 6 | 449 | 0.28% | 0.69% | 1-seat | close | 0m | 59 St (N) → Atlantic Av (N) |  |
| 7 | 416 | 0.25% | 0.64% | 1-seat | close | 0m | Church Av (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 8 | 403 | 0.25% | 0.62% | 1-seat | close | 0m | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 9 | 396 | 0.24% | 0.61% | 1-seat | close | 0m | Church Av (B,Q) → Atlantic Av (B,Q) |  |
| 10 | 396 | 0.24% | 0.61% | 1-seat | close | 0m | Kings Hwy (B) → 47-50 Sts-Rockefeller Ctr (B) |  |
| 11 | 363 | 0.22% | 0.55% | 1-seat | close | 0m | Kings Hwy (B,Q) → Atlantic Av (B,Q) |  |
| 12 | 356 | 0.22% | 0.54% | 1-seat | close | 0m | Church Av (Q) → 14 St-Union Sq (Q) |  |
| 13 | 346 | 0.21% | 0.53% | 1-seat | close | 0m | 36 St (D,N) → 34 St-Herald Sq (D,N) |  |
| 14 | 343 | 0.21% | 0.52% | 1-seat | close | 0m | 59 St (N) → 34 St-Herald Sq (N) |  |
| 15 | 338 | 0.21% | 0.52% | 1-seat | close | 0m | Kings Hwy (Q) → Times Sq-42 St/PABT (Q) |  |
| 16 | 338 | 0.21% | 0.52% | 1-seat | close | 0m | Prospect Park (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 17 | 334 | 0.20% | 0.51% | 1-seat | close | 0m | Prospect Park (Q) → 14 St-Union Sq (Q) |  |
| 18 | 330 | 0.20% | 0.51% | 1-seat | close | 0m | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 19 | 329 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 20 | 328 | 0.20% | 0.50% | 1-seat | close | 0m | 8 Av (N) → Atlantic Av (N) |  |
| 21 | 325 | 0.20% | 0.50% | 1-seat | close | 0m | Church Av (B,Q) → DeKalb Av (B,Q) |  |
| 22 | 321 | 0.20% | 0.49% | 1-seat | close | 0m | Kings Hwy (B) → 42 St-Bryant Pk/5 Av (B) |  |
| 23 | 321 | 0.20% | 0.49% | 1-seat | close | 0m | 7 Av (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 24 | 320 | 0.20% | 0.49% | 1-seat | close | 0m | Parkside Av (Q) → 14 St-Union Sq (Q) |  |
| 25 | 309 | 0.19% | 0.47% | 1-seat | close | 0m | Sheepshead Bay (B,Q) → DeKalb Av (B,Q) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 65,384/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,882 | 83.0% | 12.54% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 9,334 | 78.3% | 11.18% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 6,795 | 73.2% | 7.60% | 76% | 211m | 14 St-Union Sq (N,Q) |
| 6,365 | 72.2% | 7.03% | 100% | 51m | Times Sq-42 St/PABT (N,Q) |
| 5,982 | 75.8% | 6.94% | 67% | 170m | Canal St (N,Q) |
| 5,402 | 62.4% | 5.16% | 0% | 609m | Grand St (B,D) |
| 5,881 | 54.5% | 4.90% | 65% | 282m | DeKalb Av (B,Q) |
| 4,413 | 64.0% | 4.32% | 68% | 391m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 3,583 | 66.8% | 3.66% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 2,340 | 81.2% | 2.91% | 100% | 34m | 57 St-7 Av (N,Q) |
| 3,941 | 45.5% | 2.74% | 0% | 943m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2,636 | 64.0% | 2.58% | 57% | 457m | Broadway-Lafayette St/Bleecker St (B,D) |
| 3,441 | 48.4% | 2.55% | 0% | 764m | Jay St-MetroTech (R) |
| 2,685 | 57.6% | 2.36% | 0% | 782m | W 4 St-Wash Sq (B,D) |
| 2,268 | 62.1% | 2.15% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 2,271 | 60.9% | 2.12% | 0% | 1236m | 72 St (Q) |
| 2,603 | 41.0% | 1.63% | 0% | 982m | Borough Hall/Court St (R) |
| 2,032 | 46.6% | 1.45% | 0% | 2065m | Whitehall St-South Ferry (R) |
| 1,069 | 70.6% | 1.15% | 66% | 607m | Lexington Av/63 St (Q) |
| 1,235 | 56.7% | 1.07% | 0% | 2270m | 86 St (Q) |
| 1,107 | 62.3% | 1.05% | 0% | 2943m | 96 St (Q) |
| 927 | 71.6% | 1.02% | 100% | 217m | 7 Av (B,D) |
| 1,576 | 39.5% | 0.95% | 81% | 211m | 49 St (N) |
| 1,201 | 43.3% | 0.80% | 0% | 663m | 23 St (R) |
| 1,509 | 34.1% | 0.79% | 83% | 301m | Lexington Av/59 St (N) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_actual.csv`._

---

## B,D on 4 Av express, N,Q on Brighton

Deinterlining scenario: 4 Av express served by B,D; Brighton served by N,Q (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 727 | 0.45% | 1.30% | 1-seat | close | 0m | Kings Hwy (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 2 | 621 | 0.38% | 1.11% | 1-seat | close | 0m | 36 St (B,D) → Atlantic Av (B,D) |  |
| 3 | 583 | 0.36% | 1.05% | 1-seat | close | 0m | 7 Av (N,Q) → 14 St-Union Sq (N,Q) |  |
| 4 | 471 | 0.29% | 0.84% | 1-seat | close | 0m | Kings Hwy (Q) → DeKalb Av (Q) |  |
| 5 | 455 | 0.28% |  | xfer | far | 518m | 8 Av (B,D) → Canal St (N,Q) | Grand St (B,D) |
| 6 | 449 | 0.28% | 0.80% | 1-seat | close | 0m | 59 St (B,D) → Atlantic Av (B,D) |  |
| 7 | 416 | 0.25% | 0.75% | 1-seat | close | 0m | Church Av (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 8 | 403 | 0.25% | 0.72% | 1-seat | close | 0m | Sheepshead Bay (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 9 | 396 | 0.24% | 0.71% | 1-seat | close | 0m | Church Av (N,Q) → Atlantic Av (N,Q) |  |
| 10 | 396 | 0.24% |  | xfer | close | 274m | Kings Hwy (N,Q) → 47-50 Sts-Rockefeller Ctr (B,D) | 49 St (N,R) |
| 11 | 363 | 0.22% | 0.65% | 1-seat | close | 0m | Kings Hwy (N,Q) → Atlantic Av (N,Q) |  |
| 12 | 356 | 0.22% | 0.64% | 1-seat | close | 0m | Church Av (N,Q) → 14 St-Union Sq (N,Q) |  |
| 13 | 346 | 0.21% | 0.62% | 1-seat | close | 0m | 36 St (B,D) → 34 St-Herald Sq (B,D) |  |
| 14 | 343 | 0.21% | 0.61% | 1-seat | close | 0m | 59 St (B,D) → 34 St-Herald Sq (B,D) |  |
| 15 | 338 | 0.21% | 0.61% | 1-seat | close | 0m | Kings Hwy (N,Q) → Times Sq-42 St/PABT (N,Q) |  |
| 16 | 338 | 0.21% | 0.61% | 1-seat | close | 0m | Prospect Park (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 17 | 334 | 0.20% | 0.60% | 1-seat | close | 0m | Prospect Park (N,Q) → 14 St-Union Sq (N,Q) |  |
| 18 | 330 | 0.20% | 0.59% | 1-seat | close | 0m | Newkirk Plaza (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 19 | 329 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 20 | 328 | 0.20% | 0.59% | 1-seat | close | 0m | 8 Av (B,D) → Atlantic Av (B,D) |  |
| 21 | 325 | 0.20% | 0.58% | 1-seat | close | 0m | Church Av (Q) → DeKalb Av (Q) |  |
| 22 | 321 | 0.20% |  | xfer | close | 191m | Kings Hwy (N,Q) → 42 St-Bryant Pk/5 Av (B,D) | Times Sq-42 St (N,Q,R) |
| 23 | 321 | 0.20% | 0.58% | 1-seat | close | 0m | 7 Av (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 24 | 320 | 0.20% | 0.57% | 1-seat | close | 0m | Parkside Av (N,Q) → 14 St-Union Sq (N,Q) |  |
| 25 | 309 | 0.19% | 0.55% | 1-seat | close | 0m | Sheepshead Bay (Q) → DeKalb Av (Q) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 55,794/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,882 | 83.0% | 14.70% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 9,334 | 78.3% | 13.10% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 5,881 | 76.6% | 8.07% | 100% | 0m | DeKalb Av (B,Q) |
| 6,795 | 52.1% | 6.35% | 60% | 349m | 14 St-Union Sq (N,Q) |
| 5,402 | 62.2% | 6.03% | 0% | 608m | Grand St (B,D) |
| 6,365 | 48.3% | 5.50% | 100% | 83m | Times Sq-42 St/PABT (N,Q) |
| 5,982 | 38.8% | 4.16% | 38% | 322m | Canal St (N,Q) |
| 3,941 | 45.5% | 3.22% | 0% | 1044m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 3,441 | 48.4% | 2.99% | 0% | 387m | Jay St-MetroTech (R) |
| 4,413 | 34.4% | 2.72% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 3,583 | 39.8% | 2.55% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 2,340 | 60.9% | 2.55% | 100% | 94m | 57 St-7 Av (N,Q) |
| 2,271 | 60.9% | 2.48% | 0% | 1353m | 72 St (Q) |
| 2,603 | 41.0% | 1.91% | 0% | 729m | Borough Hall/Court St (R) |
| 2,685 | 37.3% | 1.80% | 0% | 837m | W 4 St-Wash Sq (B,D) |
| 2,636 | 36.1% | 1.71% | 29% | 653m | Broadway-Lafayette St/Bleecker St (B,D) |
| 2,032 | 46.6% | 1.70% | 0% | 2140m | Whitehall St-South Ferry (R) |
| 2,268 | 37.6% | 1.53% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 1,069 | 70.6% | 1.35% | 47% | 814m | Lexington Av/63 St (Q) |
| 1,235 | 56.7% | 1.26% | 0% | 1854m | 86 St (Q) |
| 1,107 | 62.3% | 1.24% | 0% | 2156m | 96 St (Q) |
| 1,201 | 43.3% | 0.93% | 0% | 744m | 23 St (R) |
| 949 | 52.2% | 0.89% | 0% | 1012m | City Hall (R) |
| 1,576 | 30.5% | 0.86% | 100% | 120m | 49 St (N) |
| 1,509 | 30.9% | 0.84% | 51% | 559m | Lexington Av/59 St (N) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_a.csv`._

---

## N,Q on 4 Av express, B,D on Brighton

Deinterlining scenario: 4 Av express served by N,Q; Brighton served by B,D (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 727 | 0.45% | 1.41% | 1-seat | close | 0m | Kings Hwy (B,D) → 34 St-Herald Sq (B,D) |  |
| 2 | 621 | 0.38% | 1.20% | 1-seat | close | 0m | 36 St (N,Q) → Atlantic Av (N,Q) |  |
| 3 | 583 | 0.36% |  | xfer | far | 867m | 7 Av (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 4 | 471 | 0.29% | 0.91% | 1-seat | close | 0m | Kings Hwy (B) → DeKalb Av (B) |  |
| 5 | 455 | 0.28% | 0.88% | 1-seat | close | 0m | 8 Av (N,Q) → Canal St (N,Q) |  |
| 6 | 449 | 0.28% | 0.87% | 1-seat | close | 0m | 59 St (N,Q) → Atlantic Av (N,Q) |  |
| 7 | 416 | 0.25% | 0.81% | 1-seat | close | 0m | Church Av (B,D) → 34 St-Herald Sq (B,D) |  |
| 8 | 403 | 0.25% | 0.78% | 1-seat | close | 0m | Sheepshead Bay (B,D) → 34 St-Herald Sq (B,D) |  |
| 9 | 396 | 0.24% | 0.77% | 1-seat | close | 0m | Church Av (B,D) → Atlantic Av (B,D) |  |
| 10 | 396 | 0.24% | 0.77% | 1-seat | close | 0m | Kings Hwy (B,D) → 47-50 Sts-Rockefeller Ctr (B,D) |  |
| 11 | 363 | 0.22% | 0.70% | 1-seat | close | 0m | Kings Hwy (B,D) → Atlantic Av (B,D) |  |
| 12 | 356 | 0.22% |  | xfer | far | 867m | Church Av (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 13 | 346 | 0.21% | 0.67% | 1-seat | close | 0m | 36 St (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 14 | 343 | 0.21% | 0.66% | 1-seat | close | 0m | 59 St (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 15 | 338 | 0.21% |  | xfer | close | 191m | Kings Hwy (B,D) → Times Sq-42 St/PABT (N,Q) | 42 St-Bryant Pk (B,D) |
| 16 | 338 | 0.21% | 0.65% | 1-seat | close | 0m | Prospect Park (B,D) → 34 St-Herald Sq (B,D) |  |
| 17 | 334 | 0.20% |  | xfer | far | 867m | Prospect Park (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 18 | 330 | 0.20% | 0.64% | 1-seat | close | 0m | Newkirk Plaza (B,D) → 34 St-Herald Sq (B,D) |  |
| 19 | 329 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 20 | 328 | 0.20% | 0.64% | 1-seat | close | 0m | 8 Av (N,Q) → Atlantic Av (N,Q) |  |
| 21 | 325 | 0.20% | 0.63% | 1-seat | close | 0m | Church Av (B) → DeKalb Av (B) |  |
| 22 | 321 | 0.20% | 0.62% | 1-seat | close | 0m | Kings Hwy (B,D) → 42 St-Bryant Pk/5 Av (B,D) |  |
| 23 | 321 | 0.20% | 0.62% | 1-seat | close | 0m | 7 Av (B,D) → 34 St-Herald Sq (B,D) |  |
| 24 | 320 | 0.20% |  | xfer | far | 867m | Parkside Av (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 25 | 309 | 0.19% | 0.60% | 1-seat | close | 0m | Sheepshead Bay (B) → DeKalb Av (B) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 51,623/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,882 | 83.0% | 15.89% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 9,334 | 78.3% | 14.15% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 5,881 | 76.6% | 8.72% | 100% | 0m | DeKalb Av (B,Q) |
| 5,982 | 46.9% | 5.43% | 31% | 359m | Canal St (N,Q) |
| 4,413 | 49.9% | 4.26% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 6,365 | 34.5% | 4.26% | 100% | 131m | Times Sq-42 St/PABT (N,Q) |
| 6,795 | 29.5% | 3.89% | 29% | 617m | 14 St-Union Sq (N,Q) |
| 3,941 | 45.5% | 3.48% | 0% | 1103m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 3,441 | 48.4% | 3.23% | 0% | 387m | Jay St-MetroTech (R) |
| 3,583 | 44.0% | 3.05% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 5,402 | 26.6% | 2.79% | 0% | 588m | Grand St (B,D) |
| 2,636 | 47.3% | 2.42% | 49% | 511m | Broadway-Lafayette St/Bleecker St (B,D) |
| 2,685 | 41.2% | 2.15% | 0% | 800m | W 4 St-Wash Sq (B,D) |
| 2,603 | 41.0% | 2.07% | 0% | 729m | Borough Hall/Court St (R) |
| 2,268 | 45.3% | 1.99% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 2,032 | 46.6% | 1.84% | 0% | 2188m | Whitehall St-South Ferry (R) |
| 1,576 | 44.7% | 1.37% | 100% | 137m | 49 St (N) |
| 1,509 | 45.5% | 1.33% | 48% | 594m | Lexington Av/59 St (N) |
| 2,271 | 26.4% | 1.16% | 0% | 1555m | 72 St (Q) |
| 2,340 | 25.3% | 1.15% | 100% | 171m | 57 St-7 Av (N,Q) |
| 1,201 | 43.3% | 1.01% | 0% | 819m | 23 St (R) |
| 949 | 52.2% | 0.96% | 0% | 1009m | City Hall (R) |
| 927 | 46.8% | 0.84% | 100% | 217m | 7 Av (B,D) |
| 821 | 52.4% | 0.83% | 0% | 631m | 8 St-NYU (R) |
| 1,235 | 30.0% | 0.72% | 0% | 1793m | 86 St (Q) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_b.csv`._

---

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the origin's own effective corridor (real routes in baseline, the scenario's assigned routes otherwise), thresholded at 300m, for `xfer` rows -- riders without a direct one-seat ride. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination. `1-seat` rows are always `close`/`0m`: the destination is a Complex ID in the source data, not a specific platform, so there's no way to tell which platform a rider actually used -- the effective route already stops somewhere in that same complex, the rider's real historical destination either way.
- In the per-pair table (and CSV), "1-Seat Destination" names the specific station `dist_m` was measured to for a `xfer` row: the nearest station on the origin's own effective corridor -- i.e. what the destination would have had to be for this row to be a `1-seat` ride instead. Empty for `1-seat` rows (already true of the actual destination) and omitted from the per-destination table (an average across many pairs, not a single station).
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified `xfer` pairs.
