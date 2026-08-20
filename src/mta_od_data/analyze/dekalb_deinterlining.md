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

Both ends on the comparison's routes, per that section of the comparison above.

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,981 | 0.36% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 2,847 | 0.34% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 3 | 2,831 | 0.34% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 4 | 2,738 | 0.33% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 5 | 2,646 | 0.32% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 6 | 2,592 | 0.31% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 7 | 2,584 | 0.31% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 8 | 2,428 | 0.29% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 9 | 2,351 | 0.28% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 10 | 2,333 | 0.28% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 11 | 2,306 | 0.28% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 12 | 2,291 | 0.27% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 13 | 2,269 | 0.27% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 14 | 2,004 | 0.24% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 1,872 | 0.22% | 1-seat |  |  | 86 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 16 | 1,864 | 0.22% | xfer | far | 699m | Times Sq-42 St/PABT (N,Q,R) → W 4 St-Wash Sq (B,D) |
| 17 | 1,794 | 0.21% | xfer | close | 191m | W 4 St-Wash Sq (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 18 | 1,768 | 0.21% | 1-seat |  |  | 86 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 19 | 1,700 | 0.20% | 1-seat |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) → Times Sq-42 St/PABT (N,Q,R) |
| 20 | 1,650 | 0.20% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 86 St (Q) |
| 21 | 1,638 | 0.20% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Whitehall St-South Ferry (R) |
| 22 | 1,592 | 0.19% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Jackson Hts-Roosevelt Av/74 St-Broadway (R) |
| 23 | 1,588 | 0.19% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 86 St (Q) |
| 24 | 1,528 | 0.18% | 1-seat |  |  | Whitehall St-South Ferry (R) → Times Sq-42 St/PABT (N,Q,R) |
| 25 | 1,438 | 0.17% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/59 St (N,R) |

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

Both ends on the comparison's routes, per that section of the comparison above.

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,981 | 0.36% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 2 | 2,847 | 0.34% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 3 | 2,831 | 0.34% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 4 | 2,738 | 0.33% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 5 | 2,646 | 0.32% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 6 | 2,592 | 0.31% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 7 | 2,584 | 0.31% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 8 | 2,428 | 0.29% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 9 | 2,351 | 0.28% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 10 | 2,333 | 0.28% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 11 | 2,306 | 0.28% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 12 | 2,291 | 0.27% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 13 | 2,269 | 0.27% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 14 | 2,004 | 0.24% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 1,872 | 0.22% | 1-seat |  |  | 86 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 16 | 1,864 | 0.22% | xfer | far | 699m | Times Sq-42 St/PABT (N,Q,R) → W 4 St-Wash Sq (B,D) |
| 17 | 1,794 | 0.21% | xfer | close | 191m | W 4 St-Wash Sq (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 18 | 1,768 | 0.21% | 1-seat |  |  | 86 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 19 | 1,700 | 0.20% | 1-seat |  |  | Jackson Hts-Roosevelt Av/74 St-Broadway (R) → Times Sq-42 St/PABT (N,Q,R) |
| 20 | 1,650 | 0.20% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 86 St (Q) |
| 21 | 1,638 | 0.20% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Whitehall St-South Ferry (R) |
| 22 | 1,592 | 0.19% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Jackson Hts-Roosevelt Av/74 St-Broadway (R) |
| 23 | 1,588 | 0.19% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 86 St (Q) |
| 24 | 1,528 | 0.18% | 1-seat |  |  | Whitehall St-South Ferry (R) → Times Sq-42 St/PABT (N,Q,R) |
| 25 | 1,438 | 0.17% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/59 St (N,R) |

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
