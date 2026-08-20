# Deinterlining scenario comparison: B,D,N,Q,R

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), over every origin/destination pair with both ends served by B,D,N,Q,R under any scenario compared here. Pairs with only one end on those routes are reported alongside as context, but can't be a one-seat ride under any of them.

Produced by `mta-od-data analyze deinterlining --category DeKalb --markdown-out src/mta_od_data/analyze/dekalb_deinterlining.md`.

---

## Scenario comparison

Two cuts of the same classification. Neither is the whole answer: the first says what a scenario does to the riders it can reach, the second how much of the system it reaches at all. In both, only how many riders get a one-seat ride changes between scenarios, never the total. Close one-seat counts a transfer trip whose destination is within 300m of a station on that scenario's effective origin corridor.

### Both ends on the comparison's routes

The 837,408 riders whose origin *and* destination are served by B,D,N,Q,R: the trips these routes could carry end to end, including the many that keep a one-seat ride whatever the scenario. Every table below is scoped to these.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 837,408 | 612,795 (73.2%) | 86,527 (10.3%) | 699,321 (83.5%) |
| B/D 4 Av Express | 837,408 | 593,038 (70.8%, -19,757) | 93,517 (11.2%, +6,991) | 686,555 (82.0%, -12,766) |

### Either end on the comparison's routes

The wider 2,332,194 riders with *either* end served by B,D,N,Q,R, the above among them. The difference is transfer trips with one end off these routes entirely, which no scenario here can change: they can only dilute the rate, which is why a junction's effect washes out against this total.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 2,332,194 | 612,795 (26.3%) | 229,764 (9.9%) | 842,558 (36.1%) |
| B/D 4 Av Express | 2,332,194 | 593,038 (25.4%, -19,757) | 235,698 (10.1%, +5,935) | 828,736 (35.5%, -13,822) |

---

## Current

### Top 25 origin/destination pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St/PABT (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat |  |  |  | 72 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St/PABT (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat |  |  |  | 86 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat |  |  |  | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat |  |  |  | Canal St (N,Q,R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat |  |  |  | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat |  |  |  | 23 St (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat |  |  |  | 96 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat |  |  |  | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat |  |  |  | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat |  |  |  | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 origin stations, summed across all destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| --- | --- | --- | --- |
| 54,350 | 71.7% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 29,069 | 84.4% | 89.6% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 22,108 | 56.1% | 93.2% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 22,015 | 67.1% | 74.2% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,234 | 61.8% | 77.3% | 59 St-Columbus Circle (1,A,B,C,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 18,101 | 87.3% | 92.5% | Canal St (6,J,N,Q,R,W,Z) |
| 17,855 | 55.5% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 16,103 | 94.2% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,212 | 50.3% | 65.1% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 78.4% | 89.8% | Lexington Av/59 St (4,5,6,N,R,W) |
| 13,206 | 84.4% | 93.6% | 49 St (N,R,W) |
| 13,162 | 91.9% | 91.9% | DeKalb Av (B,Q,R) |
| 12,565 | 54.9% | 92.0% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,290 | 64.7% | 68.1% | 86 St (Q) |
| 11,900 | 64.4% | 71.4% | Grand St (B,D) |
| 10,959 | 85.1% | 86.1% | Kings Hwy (B,Q) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (1,R,W) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (A,C,F,R) |
| 9,284 | 70.7% | 82.9% | 125 St (A,B,C,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R,W) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (E,F,M,R) |

### Top 25 destination stations, summed across all origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 54,675 | 71.6% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 31,416 | 86.4% | 90.8% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 55.9% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 21,158 | 57.6% | 72.0% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 72.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 87.1% | 91.8% | Canal St (6,J,N,Q,R,W,Z) |
| 18,786 | 53.9% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 78.2% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 89.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,995 | 50.6% | 64.2% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,601 | 80.5% | 92.0% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 67.8% | 72 St (Q) |
| 14,100 | 54.1% | 92.9% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,855 | 79.7% | 92.6% | 49 St (N,R,W) |
| 12,413 | 63.6% | 69.2% | Grand St (B,D) |
| 12,331 | 91.4% | 91.4% | DeKalb Av (B,Q,R) |
| 11,243 | 64.9% | 67.8% | 86 St (Q) |
| 11,048 | 85.1% | 85.9% | Kings Hwy (B,Q) |
| 10,457 | 59.5% | 67.6% | Jay St-MetroTech (A,C,F,R) |
| 9,785 | 73.8% | 76.5% | Whitehall St-South Ferry (1,R,W) |
| 9,281 | 68.7% | 73.3% | 23 St (R,W) |
| 9,136 | 60.2% | 81.8% | Forest Hills-71 Av (E,F,M,R) |
| 9,112 | 71.8% | 83.6% | 125 St (A,B,C,D) |

---

## B/D 4 Av Express

### What changed, against Current

Every both-ends rider by what Current gives them (rows) and what B/D 4 Av Express gives them (columns). Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| ↓ Current / B/D 4 Av Express → | direct | close | far |
| --- | --- | --- | --- |
| direct | 585,153 | 9,252 | 18,390 |
| close | 2,130 | 84,124 | 272 |
| far | 5,754 | 142 | 132,191 |

- **Gained an effective one-seat ride: 5,896**
- **Lost one: 18,662**
- **Net: -12,766**

### Biggest changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. Each pair is named by the routes serving it today; `Dist` is the walk under B/D 4 Av Express.

| # | Riders | Was | Now | Dist | Origin ↔ Destination |
| --- | --- | --- | --- | --- | --- |
| 1 | 919 | direct | far | 518m | Canal St (N,Q,R) ↔ 8 Av (N) |
| 2 | 774 | direct | close | 274m | Kings Hwy (B,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 3 | 633 | direct | close | 191m | Kings Hwy (B,Q) ↔ 42 St-Bryant Pk/5 Av (B,D) |
| 4 | 584 | far | direct |  | 8 Av (N) ↔ Grand St (B,D) |
| 5 | 575 | direct | close | 274m | Sheepshead Bay (B,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 6 | 557 | direct | far | 518m | Kings Hwy (B,Q) ↔ Grand St (B,D) |
| 7 | 534 | direct | far | 518m | Fort Hamilton Pkwy (N) ↔ Canal St (N,Q,R) |
| 8 | 509 | direct | far | 518m | Bay Pkwy (N) ↔ Canal St (N,Q,R) |
| 9 | 505 | direct | close | 274m | 7 Av (B,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 10 | 436 | direct | close | 191m | Times Sq-42 St/PABT (N,Q,R) ↔ 8 Av (N) |
| 11 | 435 | direct | close | 191m | Sheepshead Bay (B,Q) ↔ 42 St-Bryant Pk/5 Av (B,D) |
| 12 | 423 | direct | far | 518m | Sheepshead Bay (B,Q) ↔ Grand St (B,D) |
| 13 | 408 | direct | far | 795m | 7 Av (B,Q) ↔ Broadway-Lafayette St/Bleecker St (B,D) |
| 14 | 402 | direct | far | 1429m | Coney Island-Stillwell Av (D,N,Q) ↔ 8 Av (N) |
| 15 | 393 | direct | far | 518m | Kings Hwy (N) ↔ Canal St (N,Q,R) |
| 16 | 349 | direct | far | 518m | 20 Av (N) ↔ Canal St (N,Q,R) |
| 17 | 340 | direct | far | 413m | Kings Hwy (B,Q) ↔ 59 St-Columbus Circle (B,D) |
| 18 | 332 | direct | close | 191m | 7 Av (B,Q) ↔ 42 St-Bryant Pk/5 Av (B,D) |
| 19 | 318 | direct | close | 274m | Newkirk Plaza (B,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 20 | 314 | direct | far | 867m | 8 Av (N) ↔ 14 St-Union Sq (N,Q,R) |
| 21 | 312 | direct | close | 274m | Church Av (B,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 22 | 307 | direct | far | 1720m | Coney Island-Stillwell Av (D,N,Q) ↔ 59 St (N,R) |
| 23 | 306 | direct | close | 191m | Fort Hamilton Pkwy (N) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 24 | 305 | direct | far | 795m | Church Av (B,Q) ↔ Broadway-Lafayette St/Bleecker St (B,D) |
| 25 | 297 | direct | far | 518m | 18 Av (N) ↔ Canal St (N,Q,R) |

### Top 25 origin/destination pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St/PABT (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat |  |  |  | 72 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St/PABT (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat |  |  |  | 86 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat |  |  |  | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat |  |  |  | Canal St (N,Q,R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat |  |  |  | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat |  |  |  | 23 St (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat |  |  |  | 96 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat |  |  |  | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat |  |  |  | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat |  |  |  | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 origin stations, summed across all destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| --- | --- | --- | --- |
| 54,350 | 69.9% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 29,069 | 81.6% | 86.7% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 22,108 | 50.8% | 93.2% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 22,015 | 67.1% | 74.2% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,234 | 59.3% | 74.7% | 59 St-Columbus Circle (1,A,B,C,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 18,101 | 77.6% | 82.9% | Canal St (6,J,N,Q,R,W,Z) |
| 17,855 | 50.6% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 16,103 | 92.3% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,212 | 47.0% | 61.8% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 77.9% | 87.6% | Lexington Av/59 St (4,5,6,N,R,W) |
| 13,206 | 83.1% | 93.6% | 49 St (N,R,W) |
| 13,162 | 95.3% | 95.3% | DeKalb Av (B,Q,R) |
| 12,565 | 49.7% | 86.4% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,290 | 64.7% | 68.1% | 86 St (Q) |
| 11,900 | 64.7% | 71.7% | Grand St (B,D) |
| 10,959 | 69.8% | 77.2% | Kings Hwy (B,Q) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (1,R,W) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (A,C,F,R) |
| 9,284 | 69.8% | 82.0% | 125 St (A,B,C,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R,W) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (E,F,M,R) |

### Top 25 destination stations, summed across all origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 54,675 | 69.8% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 31,416 | 83.6% | 88.1% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 50.3% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 21,158 | 55.0% | 69.4% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 72.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 77.7% | 82.5% | Canal St (6,J,N,Q,R,W,Z) |
| 18,786 | 48.8% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 78.2% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 87.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,995 | 47.2% | 60.8% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,601 | 80.1% | 89.8% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 67.8% | 72 St (Q) |
| 14,100 | 48.9% | 87.2% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,855 | 78.6% | 92.6% | 49 St (N,R,W) |
| 12,413 | 63.6% | 69.1% | Grand St (B,D) |
| 12,331 | 95.0% | 95.0% | DeKalb Av (B,Q,R) |
| 11,243 | 64.9% | 67.8% | 86 St (Q) |
| 11,048 | 70.2% | 77.2% | Kings Hwy (B,Q) |
| 10,457 | 59.5% | 67.6% | Jay St-MetroTech (A,C,F,R) |
| 9,785 | 73.8% | 76.5% | Whitehall St-South Ferry (1,R,W) |
| 9,281 | 68.7% | 73.3% | 23 St (R,W) |
| 9,136 | 60.2% | 81.8% | Forest Hills-71 Av (E,F,M,R) |
| 9,112 | 70.9% | 82.6% | 125 St (A,B,C,D) |
