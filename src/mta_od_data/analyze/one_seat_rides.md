# 6 Av express/Broadway express deinterlining: one-seat-ride results at Atlantic Av (B,D,N,Q,R)

Scenario: average weekday ridership (35 distinct days in the data, 2024-01-08 to 2024-07-12) on trains originating at stations served by B,D,N,Q,R, south of Atlantic Av (B,D,N,Q,R), with destinations north of it (i.e. trips that cross the junction).

Produced by `mta-od-data analyze one-seat-rides --routes B,D,N,Q,R --primary-routes B,D,N,Q --trunk-b N,Q,R --all-corridor-scenarios --csv-out data/dekalb_weekday_pairs.csv --markdown-out src/mta_od_data/analyze/one_seat_rides.md`.

---

## Scenario comparison

Average weekday ridership is the same 152,882/weekday across every scenario below -- only how many of those riders get a one-seat ride changes.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| D,N on 4 Av express, B,Q on Brighton | 152,882 | 62,425 (40.8%) | 16,805 (18.6%) | 79,230 (51.8%) |
| B,D on 4 Av express, N,Q on Brighton | 152,882 | 52,723 (34.5%) | 22,410 (22.4%) | 75,132 (49.1%) |
| N,Q on 4 Av express, B,D on Brighton | 152,882 | 49,180 (32.2%) | 21,813 (21.0%) | 70,993 (46.4%) |

---

## D,N on 4 Av express, B,Q on Brighton

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.16% | 1-seat | close | 0m | Kings Hwy (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 2 | 548 | 0.36% | 0.88% | 1-seat | close | 0m | 36 St (D,N) → Atlantic Av (D,N) |  |
| 3 | 530 | 0.35% | 0.85% | 1-seat | close | 0m | 7 Av (Q) → 14 St-Union Sq (Q) |  |
| 4 | 471 | 0.31% | 0.75% | 1-seat | close | 0m | Church Av (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 5 | 444 | 0.29% | 0.71% | 1-seat | close | 0m | Church Av (B,Q) → Atlantic Av (B,Q) |  |
| 6 | 439 | 0.29% | 0.70% | 1-seat | close | 0m | Kings Hwy (B,Q) → DeKalb Av (B,Q) |  |
| 7 | 429 | 0.28% | 0.69% | 1-seat | close | 0m | 8 Av (N) → Canal St (N) |  |
| 8 | 409 | 0.27% | 0.65% | 1-seat | close | 0m | Sheepshead Bay (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 9 | 400 | 0.26% | 0.64% | 1-seat | close | 0m | 59 St (N) → Atlantic Av (N) |  |
| 10 | 392 | 0.26% | 0.63% | 1-seat | close | 0m | Kings Hwy (B) → 47-50 Sts-Rockefeller Ctr (B) |  |
| 11 | 390 | 0.26% | 0.63% | 1-seat | close | 0m | Church Av (Q) → 14 St-Union Sq (Q) |  |
| 12 | 382 | 0.25% | 0.61% | 1-seat | close | 0m | Church Av (B,Q) → DeKalb Av (B,Q) |  |
| 13 | 347 | 0.23% | 0.56% | 1-seat | close | 0m | Kings Hwy (B) → 42 St-Bryant Pk/5 Av (B) |  |
| 14 | 332 | 0.22% | 0.53% | 1-seat | close | 0m | Newkirk Plaza (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 15 | 330 | 0.22% | 0.53% | 1-seat | close | 0m | 79 St (D) → Grand St (D) |  |
| 16 | 328 | 0.21% | 0.53% | 1-seat | close | 0m | Church Av (Q) → Times Sq-42 St/PABT (Q) |  |
| 17 | 325 | 0.21% | 0.52% | 1-seat | close | 0m | Kings Hwy (B,Q) → Atlantic Av (B,Q) |  |
| 18 | 320 | 0.21% | 0.51% | 1-seat | close | 0m | 7 Av (B,Q) → 34 St-Herald Sq (B,Q) |  |
| 19 | 317 | 0.21% | 0.51% | 1-seat | close | 0m | Sheepshead Bay (B,Q) → DeKalb Av (B,Q) |  |
| 20 | 310 | 0.20% | 0.50% | 1-seat | close | 0m | Bay Pkwy (D) → Grand St (D) |  |
| 21 | 310 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 22 | 306 | 0.20% | 0.49% | 1-seat | close | 0m | 8 Av (N) → Atlantic Av (N) |  |
| 23 | 306 | 0.20% | 0.49% | 1-seat | close | 0m | Kings Hwy (Q) → Times Sq-42 St/PABT (Q) |  |
| 24 | 304 | 0.20% | 0.49% | 1-seat | close | 0m | 36 St (D,N) → 34 St-Herald Sq (D,N) |  |
| 25 | 304 | 0.20% | 0.49% | 1-seat | close | 0m | Prospect Park (Q) → 14 St-Union Sq (Q) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 62,425/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 12.55% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 8,565 | 78.5% | 10.77% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 6,250 | 73.0% | 7.30% | 75% | 217m | 14 St-Union Sq (N,Q) |
| 5,768 | 76.1% | 7.03% | 65% | 180m | Canal St (N,Q) |
| 6,000 | 71.9% | 6.91% | 100% | 53m | Times Sq-42 St/PABT (N,Q) |
| 5,521 | 64.3% | 5.69% | 0% | 608m | Grand St (B,D) |
| 5,513 | 55.2% | 4.87% | 64% | 291m | DeKalb Av (B,Q) |
| 4,179 | 65.7% | 4.40% | 69% | 386m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 3,476 | 69.4% | 3.86% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 2,167 | 81.3% | 2.82% | 100% | 32m | 57 St-7 Av (N,Q) |
| 3,612 | 44.6% | 2.58% | 0% | 942m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2,413 | 65.9% | 2.55% | 61% | 431m | Broadway-Lafayette St/Bleecker St (B,D) |
| 3,283 | 48.3% | 2.54% | 0% | 763m | Jay St-MetroTech (R) |
| 2,444 | 60.5% | 2.37% | 0% | 778m | W 4 St-Wash Sq (B,D) |
| 2,210 | 63.8% | 2.26% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 2,191 | 61.2% | 2.15% | 0% | 1246m | 72 St (Q) |
| 2,542 | 40.6% | 1.65% | 0% | 975m | Borough Hall/Court St (R) |
| 1,988 | 46.0% | 1.46% | 0% | 2068m | Whitehall St-South Ferry (R) |
| 982 | 73.7% | 1.16% | 69% | 570m | Lexington Av/63 St (Q) |
| 898 | 73.3% | 1.05% | 100% | 217m | 7 Av (B,D) |
| 1,126 | 57.7% | 1.04% | 0% | 2272m | 86 St (Q) |
| 1,002 | 63.5% | 1.02% | 0% | 2943m | 96 St (Q) |
| 1,351 | 39.5% | 0.85% | 81% | 208m | 49 St (N) |
| 1,447 | 34.7% | 0.80% | 83% | 307m | Lexington Av/59 St (N) |
| 957 | 51.6% | 0.79% | 0% | 899m | City Hall (R) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_actual.csv`._

---

## B,D on 4 Av express, N,Q on Brighton

Deinterlining scenario: 4 Av express served by B,D; Brighton served by N,Q (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.37% | 1-seat | close | 0m | Kings Hwy (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 2 | 548 | 0.36% | 1.04% | 1-seat | close | 0m | 36 St (B,D) → Atlantic Av (B,D) |  |
| 3 | 530 | 0.35% | 1.01% | 1-seat | close | 0m | 7 Av (N,Q) → 14 St-Union Sq (N,Q) |  |
| 4 | 471 | 0.31% | 0.89% | 1-seat | close | 0m | Church Av (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 5 | 444 | 0.29% | 0.84% | 1-seat | close | 0m | Church Av (N,Q) → Atlantic Av (N,Q) |  |
| 6 | 439 | 0.29% | 0.83% | 1-seat | close | 0m | Kings Hwy (Q) → DeKalb Av (Q) |  |
| 7 | 429 | 0.28% |  | xfer | far | 518m | 8 Av (B,D) → Canal St (N,Q) | Grand St (B,D) |
| 8 | 409 | 0.27% | 0.77% | 1-seat | close | 0m | Sheepshead Bay (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 9 | 400 | 0.26% | 0.76% | 1-seat | close | 0m | 59 St (B,D) → Atlantic Av (B,D) |  |
| 10 | 392 | 0.26% |  | xfer | close | 274m | Kings Hwy (N,Q) → 47-50 Sts-Rockefeller Ctr (B,D) | 49 St (N,R) |
| 11 | 390 | 0.26% | 0.74% | 1-seat | close | 0m | Church Av (N,Q) → 14 St-Union Sq (N,Q) |  |
| 12 | 382 | 0.25% | 0.73% | 1-seat | close | 0m | Church Av (Q) → DeKalb Av (Q) |  |
| 13 | 347 | 0.23% |  | xfer | close | 191m | Kings Hwy (N,Q) → 42 St-Bryant Pk/5 Av (B,D) | Times Sq-42 St (N,Q,R) |
| 14 | 332 | 0.22% | 0.63% | 1-seat | close | 0m | Newkirk Plaza (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 15 | 330 | 0.22% | 0.63% | 1-seat | close | 0m | 79 St (B,D) → Grand St (B,D) |  |
| 16 | 328 | 0.21% | 0.62% | 1-seat | close | 0m | Church Av (N,Q) → Times Sq-42 St/PABT (N,Q) |  |
| 17 | 325 | 0.21% | 0.62% | 1-seat | close | 0m | Kings Hwy (N,Q) → Atlantic Av (N,Q) |  |
| 18 | 320 | 0.21% | 0.61% | 1-seat | close | 0m | 7 Av (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 19 | 317 | 0.21% | 0.60% | 1-seat | close | 0m | Sheepshead Bay (Q) → DeKalb Av (Q) |  |
| 20 | 310 | 0.20% | 0.59% | 1-seat | close | 0m | Bay Pkwy (B,D) → Grand St (B,D) |  |
| 21 | 310 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 22 | 306 | 0.20% | 0.58% | 1-seat | close | 0m | 8 Av (B,D) → Atlantic Av (B,D) |  |
| 23 | 306 | 0.20% | 0.58% | 1-seat | close | 0m | Kings Hwy (N,Q) → Times Sq-42 St/PABT (N,Q) |  |
| 24 | 304 | 0.20% | 0.58% | 1-seat | close | 0m | 36 St (B,D) → 34 St-Herald Sq (B,D) |  |
| 25 | 304 | 0.20% | 0.58% | 1-seat | close | 0m | Prospect Park (N,Q) → 14 St-Union Sq (N,Q) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 52,723/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 14.86% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 8,565 | 78.5% | 12.76% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 5,513 | 77.2% | 8.07% | 100% | 0m | DeKalb Av (B,Q) |
| 5,521 | 62.6% | 6.56% | 0% | 606m | Grand St (B,D) |
| 6,250 | 52.1% | 6.17% | 58% | 361m | 14 St-Union Sq (N,Q) |
| 6,000 | 48.3% | 5.50% | 100% | 86m | Times Sq-42 St/PABT (N,Q) |
| 5,768 | 37.9% | 4.15% | 36% | 333m | Canal St (N,Q) |
| 3,612 | 44.6% | 3.06% | 0% | 1044m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 3,283 | 48.3% | 3.01% | 0% | 387m | Jay St-MetroTech (R) |
| 4,179 | 34.1% | 2.70% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 3,476 | 38.7% | 2.55% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 2,191 | 61.2% | 2.54% | 0% | 1365m | 72 St (Q) |
| 2,167 | 59.9% | 2.46% | 100% | 97m | 57 St-7 Av (N,Q) |
| 2,542 | 40.6% | 1.96% | 0% | 729m | Borough Hall/Court St (R) |
| 1,988 | 46.0% | 1.73% | 0% | 2141m | Whitehall St-South Ferry (R) |
| 2,444 | 36.5% | 1.69% | 0% | 841m | W 4 St-Wash Sq (B,D) |
| 2,413 | 34.8% | 1.59% | 29% | 653m | Broadway-Lafayette St/Bleecker St (B,D) |
| 2,210 | 36.9% | 1.55% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 982 | 73.7% | 1.37% | 49% | 796m | Lexington Av/63 St (Q) |
| 1,126 | 57.7% | 1.23% | 0% | 1851m | 86 St (Q) |
| 1,002 | 63.5% | 1.21% | 0% | 2165m | 96 St (Q) |
| 957 | 51.6% | 0.94% | 0% | 1018m | City Hall (R) |
| 1,110 | 44.3% | 0.93% | 0% | 744m | 23 St (R) |
| 1,447 | 31.5% | 0.86% | 51% | 565m | Lexington Av/59 St (N) |
| 1,351 | 31.1% | 0.80% | 100% | 117m | 49 St (N) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_a.csv`._

---

## N,Q on 4 Av express, B,D on Brighton

Deinterlining scenario: 4 Av express served by N,Q; Brighton served by B,D (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 722 | 0.47% | 1.47% | 1-seat | close | 0m | Kings Hwy (B,D) → 34 St-Herald Sq (B,D) |  |
| 2 | 548 | 0.36% | 1.11% | 1-seat | close | 0m | 36 St (N,Q) → Atlantic Av (N,Q) |  |
| 3 | 530 | 0.35% |  | xfer | far | 867m | 7 Av (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 4 | 471 | 0.31% | 0.96% | 1-seat | close | 0m | Church Av (B,D) → 34 St-Herald Sq (B,D) |  |
| 5 | 444 | 0.29% | 0.90% | 1-seat | close | 0m | Church Av (B,D) → Atlantic Av (B,D) |  |
| 6 | 439 | 0.29% | 0.89% | 1-seat | close | 0m | Kings Hwy (B) → DeKalb Av (B) |  |
| 7 | 429 | 0.28% | 0.87% | 1-seat | close | 0m | 8 Av (N,Q) → Canal St (N,Q) |  |
| 8 | 409 | 0.27% | 0.83% | 1-seat | close | 0m | Sheepshead Bay (B,D) → 34 St-Herald Sq (B,D) |  |
| 9 | 400 | 0.26% | 0.81% | 1-seat | close | 0m | 59 St (N,Q) → Atlantic Av (N,Q) |  |
| 10 | 392 | 0.26% | 0.80% | 1-seat | close | 0m | Kings Hwy (B,D) → 47-50 Sts-Rockefeller Ctr (B,D) |  |
| 11 | 390 | 0.26% |  | xfer | far | 867m | Church Av (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |
| 12 | 382 | 0.25% | 0.78% | 1-seat | close | 0m | Church Av (B) → DeKalb Av (B) |  |
| 13 | 347 | 0.23% | 0.71% | 1-seat | close | 0m | Kings Hwy (B,D) → 42 St-Bryant Pk/5 Av (B,D) |  |
| 14 | 332 | 0.22% | 0.67% | 1-seat | close | 0m | Newkirk Plaza (B,D) → 34 St-Herald Sq (B,D) |  |
| 15 | 330 | 0.22% |  | xfer | far | 565m | 79 St (N,Q) → Grand St (B,D) | Canal St (N,Q) |
| 16 | 328 | 0.21% |  | xfer | close | 191m | Church Av (B,D) → Times Sq-42 St/PABT (N,Q) | 42 St-Bryant Pk (B,D) |
| 17 | 325 | 0.21% | 0.66% | 1-seat | close | 0m | Kings Hwy (B,D) → Atlantic Av (B,D) |  |
| 18 | 320 | 0.21% | 0.65% | 1-seat | close | 0m | 7 Av (B,D) → 34 St-Herald Sq (B,D) |  |
| 19 | 317 | 0.21% | 0.64% | 1-seat | close | 0m | Sheepshead Bay (B) → DeKalb Av (B) |  |
| 20 | 310 | 0.20% |  | xfer | far | 565m | Bay Pkwy (N,Q) → Grand St (B,D) | Canal St (N,Q) |
| 21 | 310 | 0.20% |  | xfer | close | 0m | 86 St (R) → Atlantic Av (D,N) | Atlantic Av (D,N,R) |
| 22 | 306 | 0.20% | 0.62% | 1-seat | close | 0m | 8 Av (N,Q) → Atlantic Av (N,Q) |  |
| 23 | 306 | 0.20% |  | xfer | close | 191m | Kings Hwy (B,D) → Times Sq-42 St/PABT (N,Q) | 42 St-Bryant Pk (B,D) |
| 24 | 304 | 0.20% | 0.62% | 1-seat | close | 0m | 36 St (N,Q) → 34 St-Herald Sq (N,Q) |  |
| 25 | 304 | 0.20% |  | xfer | far | 867m | Prospect Park (B,D) → 14 St-Union Sq (N,Q) | W 4 St-Wash Sq (B,D) |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 49,180/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 9,376 | 83.5% | 15.93% | 100% | 0m | 34 St-Herald Sq (B,D,N,Q) |
| 8,565 | 78.5% | 13.68% | 100% | 0m | Atlantic Av (B,D,N,Q) |
| 5,513 | 77.2% | 8.65% | 100% | 0m | DeKalb Av (B,Q) |
| 5,768 | 48.4% | 5.67% | 30% | 362m | Canal St (N,Q) |
| 4,179 | 50.4% | 4.29% | 100% | 274m | 47-50 Sts-Rockefeller Ctr (B,D) |
| 6,000 | 34.7% | 4.24% | 100% | 131m | Times Sq-42 St/PABT (N,Q) |
| 6,250 | 29.7% | 3.78% | 29% | 617m | 14 St-Union Sq (N,Q) |
| 3,612 | 44.6% | 3.28% | 0% | 1104m | Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 3,476 | 46.1% | 3.26% | 100% | 191m | 42 St-Bryant Pk/5 Av (B,D) |
| 3,283 | 48.3% | 3.22% | 0% | 387m | Jay St-MetroTech (R) |
| 5,521 | 27.0% | 3.03% | 0% | 586m | Grand St (B,D) |
| 2,413 | 48.3% | 2.37% | 50% | 507m | Broadway-Lafayette St/Bleecker St (B,D) |
| 2,444 | 42.8% | 2.13% | 0% | 800m | W 4 St-Wash Sq (B,D) |
| 2,542 | 40.6% | 2.10% | 0% | 729m | Borough Hall/Court St (R) |
| 2,210 | 46.3% | 2.08% | 0% | 413m | 59 St-Columbus Circle (B,D) |
| 1,988 | 46.0% | 1.86% | 0% | 2186m | Whitehall St-South Ferry (R) |
| 1,447 | 46.1% | 1.36% | 47% | 614m | Lexington Av/59 St (N) |
| 1,351 | 43.7% | 1.20% | 100% | 137m | 49 St (N) |
| 2,191 | 26.4% | 1.18% | 0% | 1560m | 72 St (Q) |
| 2,167 | 26.1% | 1.15% | 100% | 170m | 57 St-7 Av (N,Q) |
| 957 | 51.6% | 1.00% | 0% | 1001m | City Hall (R) |
| 1,110 | 44.3% | 1.00% | 0% | 816m | 23 St (R) |
| 898 | 50.4% | 0.92% | 100% | 217m | 7 Av (B,D) |
| 720 | 52.7% | 0.77% | 0% | 631m | 8 St-NYU (R) |
| 810 | 44.7% | 0.74% | 45% | 399m | 5 Av/59 St (N) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/dekalb_weekday_pairs_b.csv`._

---

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the origin's own effective corridor (real routes in baseline, the scenario's assigned routes otherwise), thresholded at 300m, for `xfer` rows -- riders without a direct one-seat ride. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination. `1-seat` rows are always `close`/`0m`: the destination is a Complex ID in the source data, not a specific platform, so there's no way to tell which platform a rider actually used -- the effective route already stops somewhere in that same complex, the rider's real historical destination either way.
- In the per-pair table (and CSV), "1-Seat Destination" names the specific station `dist_m` was measured to for a `xfer` row: the nearest station on the origin's own effective corridor -- i.e. what the destination would have had to be for this row to be a `1-seat` ride instead. Empty for `1-seat` rows (already true of the actual destination) and omitted from the per-destination table (an average across many pairs, not a single station).
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified `xfer` pairs.
