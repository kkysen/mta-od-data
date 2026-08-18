# Deinterlining scenario comparison: B,D,N,Q,R

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), every origin/destination pair whose origin could plausibly use B,D,N,Q,R under any scenario compared here.

Produced by `mta-od-data analyze deinterlining --category DeKalb --markdown-out src/mta_od_data/analyze/dekalb_deinterlining.md`.

---

## Scenario comparison

Total riders is the same 1,576,111 across every scenario below; only how many of those riders get a one-seat ride changes.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| Current | 1,576,111 | 612,795 (38.9%) | 111,095 (7.0%) | 723,890 (45.9%) |
| B/D 4 Av Express | 1,576,111 | 593,038 (37.6%) | 130,686 (8.3%) | 723,724 (45.9%) |

---

## Current

### Headline numbers

- **Total: 1,576,111 riders**
- **One-seat: 38.9%** (612,795)
- **Close one-seat: 7.0%** (111,095), within 300m of a station on the scenario-effective origin corridor
- **Effective one-seat: 45.9%** (723,890)

### Top 25 origin/destination pairs

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4,381 | 0.28% | xfer | far | 671m | Times Sq-42 St/PABT (N,Q,R) → Grand Central-42 St () |
| 2 | 3,771 | 0.24% | xfer | far | 671m | 14 St-Union Sq (N,Q,R) → Grand Central-42 St () |
| 3 | 2,981 | 0.19% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 4 | 2,847 | 0.18% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 5 | 2,831 | 0.18% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 6 | 2,829 | 0.18% | xfer | close | 132m | Times Sq-42 St/PABT (N,Q,R) → Fulton St () |
| 7 | 2,738 | 0.17% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 8 | 2,646 | 0.17% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 9 | 2,592 | 0.16% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 10 | 2,584 | 0.16% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 11 | 2,464 | 0.16% | xfer | far | 588m | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/51-53 Sts () |
| 12 | 2,445 | 0.16% | xfer | far | 1041m | Times Sq-42 St/PABT (N,Q,R) → 14 St/8 Av () |
| 13 | 2,428 | 0.15% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 14 | 2,351 | 0.15% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 15 | 2,333 | 0.15% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 16 | 2,306 | 0.15% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 17 | 2,291 | 0.15% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 18 | 2,269 | 0.14% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 19 | 2,184 | 0.14% | xfer | far | 549m | 59 St-Columbus Circle (B,D) → 34 St-Penn Station () |
| 20 | 2,077 | 0.13% | xfer | far | 4145m | Times Sq-42 St/PABT (N,Q,R) → Flushing-Main St () |
| 21 | 2,006 | 0.13% | xfer | far | 1537m | Times Sq-42 St/PABT (N,Q,R) → 72 St () |
| 22 | 2,004 | 0.13% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → 34 St-Herald Sq (B,D,N,Q,R) |
| 23 | 1,917 | 0.12% | xfer | far | 540m | Times Sq-42 St/PABT (N,Q,R) → 5 Av/53 St () |
| 24 | 1,891 | 0.12% | xfer | far | 549m | Times Sq-42 St/PABT (N,Q,R) → 34 St-Penn Station () |
| 25 | 1,872 | 0.12% | 1-seat |  |  | 86 St (Q) → Times Sq-42 St/PABT (N,Q,R) |

### Top 25 destination stations, summed across all origins

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 54,675 | 71.6% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 33,120 | 0.0% | 0.0% | Grand Central-42 St (4,5,6,7,S) |
| 31,416 | 86.4% | 86.4% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 55.9% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 23,217 | 0.0% | 0.0% | 34 St-Penn Station (A,C,E) |
| 21,158 | 57.6% | 57.6% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 67.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 87.1% | 87.1% | Canal St (6,J,N,Q,R,W,Z) |
| 18,984 | 0.0% | 64.1% | Fulton St (2,3,4,5,A,C,J,Z) |
| 18,786 | 53.9% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 61.0% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 89.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 16,236 | 0.0% | 0.0% | Flushing-Main St (7) |
| 15,995 | 50.6% | 50.6% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 15,972 | 0.0% | 0.0% | Lexington Av/51-53 Sts (6,E,F) |
| 14,601 | 80.5% | 87.3% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 66.2% | 72 St (Q) |
| 14,100 | 54.1% | 92.9% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 14,038 | 0.0% | 0.0% | 14 St/8 Av (A,C,E,L) |
| 12,855 | 79.7% | 92.0% | 49 St (N,R,W) |
| 12,545 | 0.0% | 100.0% | 34 St-Penn Station (1,2,3) |
| 12,413 | 63.6% | 63.6% | Grand St (B,D) |
| 12,331 | 91.4% | 91.4% | DeKalb Av (B,Q,R) |

---

## B/D 4 Av Express

### Headline numbers

- **Total: 1,576,111 riders**
- **One-seat: 37.6%** (593,038)
- **Close one-seat: 8.3%** (130,686), within 300m of a station on the scenario-effective origin corridor
- **Effective one-seat: 45.9%** (723,724)

### Top 25 origin/destination pairs

| # | Riders | % Total | Type | Close? | Dist | Origin → Destination |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4,381 | 0.28% | xfer | far | 671m | Times Sq-42 St/PABT (N,Q,R) → Grand Central-42 St () |
| 2 | 3,771 | 0.24% | xfer | far | 671m | 14 St-Union Sq (N,Q,R) → Grand Central-42 St () |
| 3 | 2,981 | 0.19% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → Chambers St/WTC/Park Pl/Cortlandt St (R) |
| 4 | 2,847 | 0.18% | 1-seat |  |  | Chambers St/WTC/Park Pl/Cortlandt St (R) → Times Sq-42 St/PABT (N,Q,R) |
| 5 | 2,831 | 0.18% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 6 | 2,829 | 0.18% | xfer | close | 132m | Times Sq-42 St/PABT (N,Q,R) → Fulton St () |
| 7 | 2,738 | 0.17% | xfer | far | 413m | Times Sq-42 St/PABT (N,Q,R) → 59 St-Columbus Circle (B,D) |
| 8 | 2,646 | 0.17% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 47-50 Sts-Rockefeller Ctr (B,D) |
| 9 | 2,592 | 0.16% | xfer | close | 191m | 59 St-Columbus Circle (B,D) → Times Sq-42 St/PABT (N,Q,R) |
| 10 | 2,584 | 0.16% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → Times Sq-42 St/PABT (N,Q,R) |
| 11 | 2,464 | 0.16% | xfer | far | 588m | Times Sq-42 St/PABT (N,Q,R) → Lexington Av/51-53 Sts () |
| 12 | 2,445 | 0.16% | xfer | far | 1041m | Times Sq-42 St/PABT (N,Q,R) → 14 St/8 Av () |
| 13 | 2,428 | 0.15% | 1-seat |  |  | 47-50 Sts-Rockefeller Ctr (B,D) → 34 St-Herald Sq (B,D,N,Q,R) |
| 14 | 2,351 | 0.15% | 1-seat |  |  | 72 St (Q) → Times Sq-42 St/PABT (N,Q,R) |
| 15 | 2,333 | 0.15% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 14 St-Union Sq (N,Q,R) |
| 16 | 2,306 | 0.15% | 1-seat |  |  | 34 St-Herald Sq (B,D,N,Q,R) → 72 St (Q) |
| 17 | 2,291 | 0.15% | 1-seat |  |  | 72 St (Q) → 34 St-Herald Sq (B,D,N,Q,R) |
| 18 | 2,269 | 0.14% | 1-seat |  |  | Times Sq-42 St/PABT (N,Q,R) → 72 St (Q) |
| 19 | 2,184 | 0.14% | xfer | far | 549m | 59 St-Columbus Circle (B,D) → 34 St-Penn Station () |
| 20 | 2,077 | 0.13% | xfer | far | 4145m | Times Sq-42 St/PABT (N,Q,R) → Flushing-Main St () |
| 21 | 2,006 | 0.13% | xfer | far | 1537m | Times Sq-42 St/PABT (N,Q,R) → 72 St () |
| 22 | 2,004 | 0.13% | 1-seat |  |  | 14 St-Union Sq (N,Q,R) → 34 St-Herald Sq (B,D,N,Q,R) |
| 23 | 1,917 | 0.12% | xfer | far | 540m | Times Sq-42 St/PABT (N,Q,R) → 5 Av/53 St () |
| 24 | 1,891 | 0.12% | xfer | far | 549m | Times Sq-42 St/PABT (N,Q,R) → 34 St-Penn Station () |
| 25 | 1,872 | 0.12% | 1-seat |  |  | 86 St (Q) → Times Sq-42 St/PABT (N,Q,R) |

### Top 25 destination stations, summed across all origins

| Riders | 1-Seat % | Effective % | Destination |
| --- | --- | --- | --- |
| 54,675 | 69.8% | 100.0% | Times Sq-42 St/PABT (1,2,3,7,A,C,E,N,Q,R,S,W) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,F,M,N,Q,R,W) |
| 33,120 | 0.0% | 0.0% | Grand Central-42 St (4,5,6,7,S) |
| 31,416 | 83.6% | 83.6% | 14 St-Union Sq (4,5,6,L,N,Q,R,W) |
| 23,378 | 50.3% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D,F,M) |
| 23,217 | 0.0% | 0.0% | 34 St-Penn Station (A,C,E) |
| 21,158 | 55.0% | 55.0% | 59 St-Columbus Circle (1,A,B,C,D) |
| 20,826 | 67.7% | 67.7% | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) |
| 19,376 | 77.7% | 77.7% | Canal St (6,J,N,Q,R,W,Z) |
| 18,984 | 0.0% | 64.1% | Fulton St (2,3,4,5,A,C,J,Z) |
| 18,786 | 48.8% | 100.0% | 42 St-Bryant Pk/5 Av (7,B,D,F,M) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (2,3,4,5,B,D,N,Q,R) |
| 16,993 | 61.0% | 61.0% | Jackson Hts-Roosevelt Av/74 St-Broadway (7,E,F,M,R) |
| 16,838 | 87.8% | 100.0% | 57 St-7 Av (N,Q,R,W) |
| 16,236 | 0.0% | 0.0% | Flushing-Main St (7) |
| 15,995 | 47.2% | 47.2% | W 4 St-Wash Sq (A,B,C,D,E,F,M) |
| 15,972 | 0.0% | 0.0% | Lexington Av/51-53 Sts (6,E,F) |
| 14,601 | 80.1% | 85.0% | Lexington Av/59 St (4,5,6,N,R,W) |
| 14,250 | 66.2% | 66.2% | 72 St (Q) |
| 14,100 | 48.9% | 87.2% | Broadway-Lafayette St/Bleecker St (6,B,D,F,M) |
| 14,038 | 0.0% | 0.0% | 14 St/8 Av (A,C,E,L) |
| 12,855 | 78.6% | 92.0% | 49 St (N,R,W) |
| 12,545 | 0.0% | 100.0% | 34 St-Penn Station (1,2,3) |
| 12,413 | 63.6% | 63.6% | Grand St (B,D) |
| 12,331 | 95.0% | 95.0% | DeKalb Av (B,Q,R) |
