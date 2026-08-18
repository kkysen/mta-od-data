# Deinterlining scenario comparison: B,D,N,Q,R

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), every origin/destination pair with either end served by B,D,N,Q,R under any scenario compared here.

Produced by `mta-od-data analyze deinterlining --category DeKalb --markdown-out src/mta_od_data/analyze/dekalb_deinterlining.md`.

---

## Scenario comparison

Total riders is the same 2,332,194 across every scenario below; only how many of those riders get a one-seat ride changes. Close one-seat counts a transfer trip whose destination is within 300m of a station on that scenario's effective origin corridor.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 2,332,194 | 612,795 (26.3%) | 111,095 (4.8%) | 723,890 (31.0%) |
| B/D 4 Av Express | 2,332,194 | 593,038 (25.4%) | 130,686 (5.6%) | 723,724 (31.0%) |

### Both ends on the comparison's routes

The 837,408 riders above whose origin *and* destination are served by B,D,N,Q,R, where a scenario's effect isn't diluted by trips only half in scope.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 837,408 | 612,795 (73.2%) | 49,159 (5.9%) | 661,953 (79.0%) |
| B/D 4 Av Express | 837,408 | 593,038 (70.8%) | 68,679 (8.2%) | 661,717 (79.0%) |

---

## Current

### Top 25 origin/destination pairs

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4,381 | 0.19% | xfer | far | 671m | Times Sq-42 St/PABT (N,Q,R) → Grand Central-42 St () |
| 2 | 4,284 | 0.18% | xfer | far | 0m | Grand Central-42 St () → 14 St-Union Sq (N,Q,R) |
| 3 | 4,276 | 0.18% | xfer | far | 0m | Grand Central-42 St () → Times Sq-42 St/PABT (N,Q,R) |
| 4 | 3,771 | 0.16% | xfer | far | 671m | 14 St-Union Sq (N,Q,R) → Grand Central-42 St () |
| 5 | 2,981 | 0.13% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 6 | 2,847 | 0.12% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 7 | 2,831 | 0.12% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 8 | 2,829 | 0.12% | xfer | close | 132m | Times Sq-42 St/PABT (N,Q,R) → Fulton St () |
| 9 | 2,738 | 0.12% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 10 | 2,646 | 0.11% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 11 | 2,592 | 0.11% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 12 | 2,584 | 0.11% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 13 | 2,512 | 0.11% | xfer | far | 0m | 34 St-Penn Station () → 59 St-Columbus Circle (B,D) |
| 14 | 2,500 | 0.11% | xfer | far | 0m | Fulton St () → Times Sq-42 St/PABT (N,Q,R) |
| 15 | 2,464 | 0.11% | xfer | far | 588m | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/51-53 Sts () |
| 16 | 2,445 | 0.10% | xfer | far | 1041m | Times Sq-42 St/PABT (N,Q,R) → 14 St/8 Av () |
| 17 | 2,428 | 0.10% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 18 | 2,351 | 0.10% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 19 | 2,333 | 0.10% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 20 | 2,315 | 0.10% | xfer | far | 0m | 14 St/8 Av () → Times Sq-42 St/PABT (N,Q,R) |
| 21 | 2,306 | 0.10% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 22 | 2,291 | 0.10% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 23 | 2,269 | 0.10% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 24 | 2,251 | 0.10% | xfer | far | 0m | Lexington Av/51-53 Sts () → Times Sq-42 St/PABT (N,Q,R) |
| 25 | 2,184 | 0.09% | xfer | far | 549m | 59 St-Columbus Circle (B,D) → 34 St-Penn Station () |

### Top 25 destination stations, summed across all origins

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 141,635 | 27.6% | 38.6% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 80,522 | 60.1% | 60.1% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 77,392 | 35.1% | 35.1% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 54,511 | 22.4% | 22.4% | 59 St-Columbus Circle (1,A,B,C,D) |
| 45,842 | 28.5% | 47.1% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 45,792 | 30.8% | 30.8% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 43,380 | 23.4% | 43.3% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 42,493 | 24.4% | 24.4% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 40,012 | 29.4% | 31.8% | Lexington Av/59 St (4,5,6,N,R,W) |
| 36,275 | 22.3% | 22.3% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 35,767 | 47.2% | 47.2% | Canal St (6,J,N,Q,R,W,Z) |
| 33,621 | 51.8% | 51.8% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 33,577 | 22.7% | 39.0% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 33,120 | 0.0% | 0.0% | Grand Central-42 St (4,5,6,7,S) |
| 28,431 | 21.9% | 21.9% | Jay St-MetroTech (A,C,F,R) |
| 27,538 | 54.9% | 61.1% | 57 St-7 Av (N,Q,R,W) |
| 24,115 | 39.1% | 39.1% | 72 St (Q) |
| 23,217 | 0.0% | 0.0% | 34 St-Penn Station (A,C,E) |
| 22,311 | 21.9% | 21.9% | Borough Hall/Court St (2,3,4,5,R) |
| 21,480 | 47.7% | 55.1% | 49 St (N,R,W) |
| 20,661 | 34.9% | 34.9% | Whitehall St-South Ferry (1,R,W) |
| 19,563 | 28.1% | 28.1% | Forest Hills-71 Av (E,F,M,R) |
| 18,984 | 0.0% | 64.1% | Fulton St (2,3,4,5,A,C,J,Z) |
| 18,879 | 34.7% | 34.7% | 125 St (A,B,C,D) |
| 18,605 | 42.5% | 42.5% | Grand St (B,D) |

---

## B/D 4 Av Express

### Top 25 origin/destination pairs

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4,381 | 0.19% | xfer | far | 671m | Times Sq-42 St/PABT (N,Q,R) → Grand Central-42 St () |
| 2 | 4,284 | 0.18% | xfer | far | 0m | Grand Central-42 St () → 14 St-Union Sq (N,Q,R) |
| 3 | 4,276 | 0.18% | xfer | far | 0m | Grand Central-42 St () → Times Sq-42 St/PABT (N,Q,R) |
| 4 | 3,771 | 0.16% | xfer | far | 671m | 14 St-Union Sq (N,Q,R) → Grand Central-42 St () |
| 5 | 2,981 | 0.13% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 6 | 2,847 | 0.12% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 7 | 2,831 | 0.12% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 8 | 2,829 | 0.12% | xfer | close | 132m | Times Sq-42 St/PABT (N,Q,R) → Fulton St () |
| 9 | 2,738 | 0.12% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 10 | 2,646 | 0.11% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 11 | 2,592 | 0.11% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 12 | 2,584 | 0.11% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 13 | 2,512 | 0.11% | xfer | far | 0m | 34 St-Penn Station () → 59 St-Columbus Circle (B,D) |
| 14 | 2,500 | 0.11% | xfer | far | 0m | Fulton St () → Times Sq-42 St/PABT (N,Q,R) |
| 15 | 2,464 | 0.11% | xfer | far | 588m | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/51-53 Sts () |
| 16 | 2,445 | 0.10% | xfer | far | 1041m | Times Sq-42 St/PABT (N,Q,R) → 14 St/8 Av () |
| 17 | 2,428 | 0.10% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 18 | 2,351 | 0.10% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 19 | 2,333 | 0.10% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 20 | 2,315 | 0.10% | xfer | far | 0m | 14 St/8 Av () → Times Sq-42 St/PABT (N,Q,R) |
| 21 | 2,306 | 0.10% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 22 | 2,291 | 0.10% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 23 | 2,269 | 0.10% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 24 | 2,251 | 0.10% | xfer | far | 0m | Lexington Av/51-53 Sts () → Times Sq-42 St/PABT (N,Q,R) |
| 25 | 2,184 | 0.09% | xfer | far | 549m | 59 St-Columbus Circle (B,D) → 34 St-Penn Station () |

### Top 25 destination stations, summed across all origins

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 141,635 | 27.0% | 38.6% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 80,522 | 60.1% | 60.1% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 77,392 | 33.9% | 33.9% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 54,511 | 21.3% | 21.3% | 59 St-Columbus Circle (1,A,B,C,D) |
| 45,842 | 25.6% | 47.1% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 45,792 | 30.8% | 30.8% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 43,380 | 21.1% | 43.3% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 42,493 | 24.4% | 24.4% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 40,012 | 29.2% | 31.0% | Lexington Av/59 St (4,5,6,N,R,W) |
| 36,275 | 20.8% | 20.8% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 35,767 | 42.1% | 42.1% | Canal St (6,J,N,Q,R,W,Z) |
| 33,621 | 51.8% | 51.8% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 33,577 | 20.5% | 36.6% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 33,120 | 0.0% | 0.0% | Grand Central-42 St (4,5,6,7,S) |
| 28,431 | 21.9% | 21.9% | Jay St-MetroTech (A,C,F,R) |
| 27,538 | 53.7% | 61.1% | 57 St-7 Av (N,Q,R,W) |
| 24,115 | 39.1% | 39.1% | 72 St (Q) |
| 23,217 | 0.0% | 0.0% | 34 St-Penn Station (A,C,E) |
| 22,311 | 21.9% | 21.9% | Borough Hall/Court St (2,3,4,5,R) |
| 21,480 | 47.0% | 55.1% | 49 St (N,R,W) |
| 20,661 | 34.9% | 34.9% | Whitehall St-South Ferry (1,R,W) |
| 19,563 | 28.1% | 28.1% | Forest Hills-71 Av (E,F,M,R) |
| 18,984 | 0.0% | 64.1% | Fulton St (2,3,4,5,A,C,J,Z) |
| 18,879 | 34.2% | 34.2% | 125 St (A,B,C,D) |
| 18,605 | 42.4% | 42.4% | Grand St (B,D) |
