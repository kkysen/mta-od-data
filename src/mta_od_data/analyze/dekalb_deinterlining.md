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
| Current | 837,408 | 612,795 (73.2%) | 49,159 (5.9%) | 661,953 (79.0%) |
| B/D 4 Av Express | 837,408 | 593,038 (70.8%) | 68,679 (8.2%) | 661,717 (79.0%) |

### Either end on the comparison's routes

The wider 2,332,194 riders with *either* end served by B,D,N,Q,R, the above among them. The difference is transfer trips with one end off these routes entirely, which no scenario here can change: they can only dilute the rate, which is why a junction's effect washes out against this total.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 2,332,194 | 612,795 (26.3%) | 111,095 (4.8%) | 723,890 (31.0%) |
| B/D 4 Av Express | 2,332,194 | 593,038 (25.4%) | 130,686 (5.6%) | 723,724 (31.0%) |

---

## Current

### Top 25 origin/destination pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. One-seat is symmetric, but close one-seat measures the destination against the origin's corridor, so it is given per direction.

| # | Riders | % Total | Type | → Close? | → Dist | ← Close? | ← Dist | Origin ↔ Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | far | 413m | close | 191m | Times Sq-42 St/PABT (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat |  |  |  |  | 72 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | far | 699m | close | 191m | Times Sq-42 St/PABT (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat |  |  |  |  | 86 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat |  |  |  |  | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat |  |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat |  |  |  |  | Canal St (N,Q,R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat |  |  |  |  | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat |  |  |  |  | 23 St (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat |  |  |  |  | 96 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat |  |  |  |  | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat |  |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat |  |  |  |  | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat |  |  |  |  | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 origin stations, summed across all destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| --- | --- | --- | --- |
| 54,350 | 71.7% | 76.7% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 29,069 | 84.4% | 89.6% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 22,108 | 56.1% | 60.2% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 22,015 | 67.1% | 74.2% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,234 | 61.8% | 77.3% | 59 St-Columbus Circle (1,A,B,C,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 18,101 | 87.3% | 92.5% | Canal St (6,J,N,Q,R,W,Z) |
| 17,855 | 55.5% | 60.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 16,103 | 94.2% | 96.4% | 57 St-7 Av (N,Q,R,W) |
| 15,212 | 50.3% | 65.1% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 78.4% | 83.8% | Lexington Av/59 St (4,5,6,N,R,W) |
| 13,206 | 84.4% | 87.5% | 49 St (N,R,W) |
| 13,162 | 91.9% | 91.9% | DeKalb Av (B,Q,R) |
| 12,565 | 54.9% | 64.5% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
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
| 31,416 | 86.4% | 86.4% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 55.9% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 21,158 | 57.6% | 57.6% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 67.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 87.1% | 87.1% | Canal St (6,J,N,Q,R,W,Z) |
| 18,786 | 53.9% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 61.0% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 89.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,995 | 50.6% | 50.6% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,601 | 80.5% | 87.3% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 66.2% | 72 St (Q) |
| 14,100 | 54.1% | 92.9% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,855 | 79.7% | 92.0% | 49 St (N,R,W) |
| 12,413 | 63.6% | 63.6% | Grand St (B,D) |
| 12,331 | 91.4% | 91.4% | DeKalb Av (B,Q,R) |
| 11,243 | 64.9% | 64.9% | 86 St (Q) |
| 11,048 | 85.1% | 85.1% | Kings Hwy (B,Q) |
| 10,457 | 59.5% | 59.5% | Jay St-MetroTech (A,C,F,R) |
| 9,785 | 73.8% | 73.8% | Whitehall St-South Ferry (1,R,W) |
| 9,281 | 68.7% | 68.7% | 23 St (R,W) |
| 9,136 | 60.2% | 60.2% | Forest Hills-71 Av (E,F,M,R) |
| 9,112 | 71.8% | 71.8% | 125 St (A,B,C,D) |

---

## B/D 4 Av Express

### Top 25 origin/destination pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. One-seat is symmetric, but close one-seat measures the destination against the origin's corridor, so it is given per direction.

| # | Riders | % Total | Type | → Close? | → Dist | ← Close? | ← Dist | Origin ↔ Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | far | 413m | close | 191m | Times Sq-42 St/PABT (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat |  |  |  |  | 72 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | far | 699m | close | 191m | Times Sq-42 St/PABT (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat |  |  |  |  | 86 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat |  |  |  |  | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat |  |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat |  |  |  |  | Canal St (N,Q,R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat |  |  |  |  | Times Sq-42 St/PABT (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat |  |  |  |  | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat |  |  |  |  | 23 St (R) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat |  |  |  |  | 96 St (Q) ↔ Times Sq-42 St/PABT (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat |  |  |  |  | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat |  |  |  |  | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat |  |  |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat |  |  |  |  | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat |  |  |  |  | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 origin stations, summed across all destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| --- | --- | --- | --- |
| 54,350 | 69.9% | 76.7% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 29,069 | 81.6% | 89.6% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 22,108 | 50.8% | 61.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 22,015 | 67.1% | 74.2% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,234 | 59.3% | 78.1% | 59 St-Columbus Circle (1,A,B,C,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 18,101 | 77.6% | 92.5% | Canal St (6,J,N,Q,R,W,Z) |
| 17,855 | 50.6% | 61.1% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 16,103 | 92.3% | 96.4% | 57 St-7 Av (N,Q,R,W) |
| 15,212 | 47.0% | 66.7% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 77.9% | 85.4% | Lexington Av/59 St (4,5,6,N,R,W) |
| 13,206 | 83.1% | 89.2% | 49 St (N,R,W) |
| 13,162 | 95.3% | 95.3% | DeKalb Av (B,Q,R) |
| 12,565 | 49.7% | 66.1% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,290 | 64.7% | 68.1% | 86 St (Q) |
| 11,900 | 64.7% | 79.3% | Grand St (B,D) |
| 10,959 | 69.8% | 79.3% | Kings Hwy (B,Q) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (1,R,W) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (A,C,F,R) |
| 9,284 | 69.8% | 83.6% | 125 St (A,B,C,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R,W) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (E,F,M,R) |

### Top 25 destination stations, summed across all origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 54,675 | 69.8% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 31,416 | 83.6% | 83.6% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 50.3% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 21,158 | 55.0% | 55.0% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 67.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 77.7% | 77.7% | Canal St (6,J,N,Q,R,W,Z) |
| 18,786 | 48.8% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 61.0% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 87.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 15,995 | 47.2% | 47.2% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 14,601 | 80.1% | 85.0% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 66.2% | 72 St (Q) |
| 14,100 | 48.9% | 87.2% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 12,855 | 78.6% | 92.0% | 49 St (N,R,W) |
| 12,413 | 63.6% | 63.6% | Grand St (B,D) |
| 12,331 | 95.0% | 95.0% | DeKalb Av (B,Q,R) |
| 11,243 | 64.9% | 64.9% | 86 St (Q) |
| 11,048 | 70.2% | 89.2% | Kings Hwy (B,Q) |
| 10,457 | 59.5% | 59.5% | Jay St-MetroTech (A,C,F,R) |
| 9,785 | 73.8% | 73.8% | Whitehall St-South Ferry (1,R,W) |
| 9,281 | 68.7% | 68.7% | 23 St (R,W) |
| 9,136 | 60.2% | 60.2% | Forest Hills-71 Av (E,F,M,R) |
| 9,112 | 70.9% | 70.9% | 125 St (A,B,C,D) |
