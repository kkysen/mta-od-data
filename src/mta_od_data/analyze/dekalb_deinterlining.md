# Deinterlining Scenario Comparison: B,D,N,Q,R

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), over every origin/destination pair with both ends served by B,D,N,Q,R under any scenario compared here. Pairs with only one end on those routes are reported alongside as context, but can't be a one-seat ride under any of them.

Produced by `mta-od-data analyze deinterlining --category DeKalb --markdown-out src/mta_od_data/analyze/dekalb_deinterlining.md`.

---

## Scenario Comparison

Two cuts of the same classification. Neither is the whole answer: the first says what a scenario does to the riders it can reach, the second how much of the system it reaches at all. In both, only how many riders get a one-seat ride changes between scenarios, never the total. Close one-seat counts a transfer trip whose destination is within 300m of a station on that scenario's effective origin corridor.

### Both Ends on the Comparison's Routes

The 837,408 riders whose origin *and* destination are served by B,D,N,Q,R: the trips these routes could carry end to end, including the many that keep a one-seat ride whatever the scenario. Every table below is scoped to these.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | ---: | ---: | ---: | ---: |
| Current | 837,408 | 612,795 (73.2%) | 86,527 (10.3%) | 699,321 (83.5%) |
| B/D 4 Av Express | 837,408 | 590,180 (70.5%), -22,615 (-2.7%) | 95,655 (11.4%), +9,129 (+1.1%) | 685,835 (81.9%), -13,486 (-1.6%) |
| N/Q 4 Av Express | 837,408 | 579,146 (69.2%), -33,649 (-4.0%) | 96,421 (11.5%), +9,895 (+1.2%) | 675,567 (80.7%), -23,754 (-2.8%) |

### Either End on the Comparison's Routes

The wider 2,332,194 riders with *either* end served by B,D,N,Q,R, the above among them. The difference is transfer trips with one end off these routes entirely, which no scenario here can change: they can only dilute the rate, which is why a junction's effect washes out against this total.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | ---: | ---: | ---: | ---: |
| Current | 2,332,194 | 612,795 (26.3%) | 205,453 (8.8%) | 818,248 (35.1%) |
| B/D 4 Av Express | 2,332,194 | 590,180 (25.3%), -22,615 (-1.0%) | 213,129 (9.1%), +7,676 (+0.3%) | 803,309 (34.4%), -14,938 (-0.6%) |
| N/Q 4 Av Express | 2,332,194 | 579,146 (24.8%), -33,649 (-1.4%) | 214,339 (9.2%), +8,886 (+0.4%) | 793,485 (34.0%), -24,763 (-1.1%) |

---

## Current

### Top 25 Origin/Destination Pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat | | | | 72 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat | | | | 86 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat | | | | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ Times Sq-42 St (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat | | | | Canal St (N,Q,R) ↔ Times Sq-42 St (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat | | | | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat | | | | 23 St (R) ↔ Times Sq-42 St (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat | | | | 96 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat | | | | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat | | | | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat | | | | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 Origin Stations, Summed across All Destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 54,350 | 71.7% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 29,069 | 84.4% | 89.6% | 14 St-Union Sq (N,Q,R) |
| 22,108 | 56.1% | 93.2% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 22,015 | 67.1% | 74.2% | Cortlandt St (R) |
| 19,234 | 61.8% | 77.3% | 59 St-Columbus Circle (B,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av (R) |
| 18,101 | 87.3% | 92.5% | Canal St (N,Q,R) |
| 17,855 | 55.5% | 100.0% | 42 St-Bryant Pk (B,D) |
| 16,103 | 94.2% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,212 | 50.3% | 65.1% | W 4 St-Wash Sq (B,D) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 78.4% | 89.8% | Lexington Av/59 St (N,R) |
| 13,206 | 84.4% | 93.6% | 49 St (N,R) |
| 13,162 | 91.9% | 91.9% | DeKalb Av (B,Q,R) |
| 12,565 | 54.9% | 92.0% | Broadway-Lafayette St (B,D) |
| 12,290 | 64.7% | 68.1% | 86 St (Q) |
| 11,900 | 64.4% | 71.4% | Grand St (B,D) |
| 10,959 | 85.1% | 86.1% | Kings Hwy (B,Q) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (R) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (R) |
| 9,284 | 70.7% | 82.9% | 125 St (B,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (R) |

### Top 25 Destination Stations, Summed across All Origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 54,675 | 71.6% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 31,416 | 86.4% | 90.8% | 14 St-Union Sq (N,Q,R) |
| 23,378 | 55.9% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 21,158 | 57.6% | 72.0% | 59 St-Columbus Circle (B,D) |
| 20,826 | 67.7% | 72.7% | Cortlandt St (R) |
| 19,376 | 87.1% | 91.8% | Canal St (N,Q,R) |
| 18,786 | 53.9% | 100.0% | 42 St-Bryant Pk (B,D) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 16,993 | 61.0% | 78.2% | Jackson Hts-Roosevelt Av (R) |
| 16,838 | 89.8% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,995 | 50.6% | 64.2% | W 4 St-Wash Sq (B,D) |
| 14,601 | 80.5% | 92.0% | Lexington Av/59 St (N,R) |
| 14,250 | 66.2% | 67.8% | 72 St (Q) |
| 14,100 | 54.1% | 92.9% | Broadway-Lafayette St (B,D) |
| 12,855 | 79.7% | 92.6% | 49 St (N,R) |
| 12,413 | 63.6% | 69.2% | Grand St (B,D) |
| 12,331 | 91.4% | 91.4% | DeKalb Av (B,Q,R) |
| 11,243 | 64.9% | 67.8% | 86 St (Q) |
| 11,048 | 85.1% | 85.9% | Kings Hwy (B,Q) |
| 10,457 | 59.5% | 67.6% | Jay St-MetroTech (R) |
| 9,785 | 73.8% | 76.5% | Whitehall St-South Ferry (R) |
| 9,281 | 68.7% | 73.3% | 23 St (R) |
| 9,136 | 60.2% | 81.8% | Forest Hills-71 Av (R) |
| 9,112 | 71.8% | 83.6% | 125 St (B,D) |

---

## B/D 4 Av Express

### What Changed, against Current

Every both-ends rider, and their share of the 837,408 of them: **was** is what Current gives them, **now** what B/D 4 Av Express would. Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| Riders | now direct | now close | now far |
| --- | ---: | ---: | ---: |
| **was direct** | 582,843 (69.6%) | 11,390 (1.4%) | 18,562 (2.2%) |
| **was close** | 2,130 (0.3%) | 84,124 (10.0%) | 272 (0.0%) |
| **was far** | 5,207 (0.6%) | 142 (0.0%) | 132,738 (15.9%) |

- **Gained an effective one-seat ride: 5,349 (0.6%)**
- **Lost one: 18,835 (2.2%)**
- **Net: -13,486 (-1.6%)**

### Biggest Changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. An end reads `today → B/D 4 Av Express` where its routes change, and today's alone where they don't; `Dist` is the walk under B/D 4 Av Express.

| # | Riders | Was | Now | Dist | Origin ↔ Destination |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 919 | direct | far | 565m | Canal St (N,Q,R) ↔ 8 Av (N → B) |
| 2 | 774 | direct | close | 274m | Kings Hwy (B,Q → N,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 3 | 707 | direct | close | 274m | DeKalb Av (B,Q,R → N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 4 | 633 | direct | close | 191m | Kings Hwy (B,Q → N,Q) ↔ 42 St-Bryant Pk (B,D) |
| 5 | 599 | direct | far | 565m | DeKalb Av (B,Q,R → N,Q,R) ↔ Grand St (B,D) |
| 6 | 584 | far | direct | | 8 Av (N → B) ↔ Grand St (B,D) |
| 7 | 582 | direct | close | 191m | DeKalb Av (B,Q,R → N,Q,R) ↔ 42 St-Bryant Pk (B,D) |
| 8 | 575 | direct | close | 274m | Sheepshead Bay (B,Q → N,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 9 | 557 | direct | far | 565m | Kings Hwy (B,Q → N,Q) ↔ Grand St (B,D) |
| 10 | 534 | direct | close | 166m | DeKalb Av (B,Q,R → N,Q,R) ↔ Broadway-Lafayette St (B,D) |
| 11 | 534 | direct | far | 565m | Fort Hamilton Pkwy (N → B) ↔ Canal St (N,Q,R) |
| 12 | 509 | direct | far | 565m | Bay Pkwy (N → B) ↔ Canal St (N,Q,R) |
| 13 | 505 | direct | close | 274m | 7 Av (B,Q → N,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 14 | 436 | direct | close | 191m | Times Sq-42 St (N,Q,R) ↔ 8 Av (N → B) |
| 15 | 435 | direct | close | 191m | Sheepshead Bay (B,Q → N,Q) ↔ 42 St-Bryant Pk (B,D) |
| 16 | 423 | direct | far | 565m | Sheepshead Bay (B,Q → N,Q) ↔ Grand St (B,D) |
| 17 | 408 | direct | far | 848m | 7 Av (B,Q → N,Q) ↔ Broadway-Lafayette St (B,D) |
| 18 | 393 | direct | far | 565m | Kings Hwy (N → B) ↔ Canal St (N,Q,R) |
| 19 | 381 | direct | far | 699m | W 4 St-Wash Sq (B,D) ↔ DeKalb Av (B,Q,R → N,Q,R) |
| 20 | 349 | direct | far | 565m | 20 Av (N → B) ↔ Canal St (N,Q,R) |
| 21 | 340 | direct | far | 414m | Kings Hwy (B,Q → N,Q) ↔ 59 St-Columbus Circle (B,D) |
| 22 | 332 | direct | close | 191m | 7 Av (B,Q → N,Q) ↔ 42 St-Bryant Pk (B,D) |
| 23 | 318 | direct | close | 274m | Newkirk Plaza (B,Q → N,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 24 | 314 | direct | far | 872m | 8 Av (N → B) ↔ 14 St-Union Sq (N,Q,R) |
| 25 | 312 | direct | close | 274m | Church Av (B,Q → N,Q) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |

### Top 25 Origin/Destination Pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat | | | | 72 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat | | | | 86 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat | | | | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ Times Sq-42 St (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat | | | | Canal St (N,Q,R) ↔ Times Sq-42 St (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat | | | | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat | | | | 23 St (R) ↔ Times Sq-42 St (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat | | | | 96 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat | | | | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat | | | | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat | | | | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 Origin Stations, Summed across All Destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 54,350 | 69.9% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 29,069 | 81.6% | 86.7% | 14 St-Union Sq (N,Q,R) |
| 22,108 | 49.3% | 93.2% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 22,015 | 67.1% | 74.2% | Cortlandt St (R) |
| 19,234 | 58.6% | 74.1% | 59 St-Columbus Circle (B,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av (R) |
| 18,101 | 77.6% | 82.9% | Canal St (N,Q,R) |
| 17,855 | 49.1% | 100.0% | 42 St-Bryant Pk (B,D) |
| 16,103 | 92.3% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,212 | 45.7% | 60.5% | W 4 St-Wash Sq (B,D) |
| 14,511 | 64.0% | 66.7% | 72 St (Q) |
| 14,205 | 77.7% | 87.6% | Lexington Av/59 St (N,R) |
| 13,206 | 82.6% | 93.6% | 49 St (N,R) |
| 13,162 | 77.8% | 85.9% | DeKalb Av (N,Q,R) |
| 12,565 | 47.7% | 86.4% | Broadway-Lafayette St (B,D) |
| 12,290 | 64.7% | 68.1% | 86 St (Q) |
| 11,900 | 62.3% | 69.3% | Grand St (B,D) |
| 10,959 | 69.8% | 77.2% | Kings Hwy (N,Q) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (R) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (R) |
| 9,284 | 69.5% | 81.7% | 125 St (B,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (R) |

### Top 25 Destination Stations, Summed across All Origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 54,675 | 69.8% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 31,416 | 83.6% | 88.1% | 14 St-Union Sq (N,Q,R) |
| 23,378 | 48.6% | 92.4% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 21,158 | 54.3% | 68.7% | 59 St-Columbus Circle (B,D) |
| 20,826 | 67.7% | 72.7% | Cortlandt St (R) |
| 19,376 | 77.7% | 82.5% | Canal St (N,Q,R) |
| 18,786 | 47.1% | 100.0% | 42 St-Bryant Pk (B,D) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 16,993 | 61.0% | 78.2% | Jackson Hts-Roosevelt Av (R) |
| 16,838 | 87.8% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,995 | 46.1% | 59.7% | W 4 St-Wash Sq (B,D) |
| 14,601 | 79.8% | 89.8% | Lexington Av/59 St (N,R) |
| 14,250 | 66.2% | 67.8% | 72 St (Q) |
| 14,100 | 46.9% | 87.2% | Broadway-Lafayette St (B,D) |
| 12,855 | 78.2% | 92.6% | 49 St (N,R) |
| 12,413 | 61.0% | 66.6% | Grand St (B,D) |
| 12,331 | 77.8% | 85.0% | DeKalb Av (N,Q,R) |
| 11,243 | 64.9% | 67.8% | 86 St (Q) |
| 11,048 | 70.2% | 77.2% | Kings Hwy (N,Q) |
| 10,457 | 59.5% | 67.6% | Jay St-MetroTech (R) |
| 9,785 | 73.8% | 76.5% | Whitehall St-South Ferry (R) |
| 9,281 | 68.7% | 73.3% | 23 St (R) |
| 9,136 | 60.2% | 81.8% | Forest Hills-71 Av (R) |
| 9,112 | 70.6% | 82.4% | 125 St (B,D) |

---

## N/Q 4 Av Express

### What Changed, against Current

Every both-ends rider, and their share of the 837,408 of them: **was** is what Current gives them, **now** what N/Q 4 Av Express would. Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| Riders | now direct | now close | now far |
| --- | ---: | ---: | ---: |
| **was direct** | 570,266 (68.1%) | 11,968 (1.4%) | 30,561 (3.6%) |
| **was close** | 1,848 (0.2%) | 83,675 (10.0%) | 1,004 (0.1%) |
| **was far** | 7,032 (0.8%) | 778 (0.1%) | 130,277 (15.6%) |

- **Gained an effective one-seat ride: 7,810 (0.9%)**
- **Lost one: 31,564 (3.8%)**
- **Net: -23,754 (-2.8%)**

### Biggest Changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. An end reads `today → N/Q 4 Av Express` where its routes change, and today's alone where they don't; `Dist` is the walk under N/Q 4 Av Express.

| # | Riders | Was | Now | Dist | Origin ↔ Destination |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 1,058 | direct | far | 906m | 7 Av (B,Q → B,D) ↔ 14 St-Union Sq (N,Q,R) |
| 2 | 715 | direct | far | 918m | 14 St-Union Sq (N,Q,R) ↔ Church Av (B,Q → B,D) |
| 3 | 682 | direct | far | 918m | 14 St-Union Sq (N,Q,R) ↔ Prospect Park (B,Q → B,D) |
| 4 | 668 | direct | close | 191m | Kings Hwy (B,Q → B,D) ↔ Times Sq-42 St (N,Q,R) |
| 5 | 628 | direct | far | 918m | Parkside Av (Q → D) ↔ 14 St-Union Sq (N,Q,R) |
| 6 | 600 | direct | far | 565m | 79 St (D → Q) ↔ Grand St (B,D) |
| 7 | 595 | direct | far | 565m | Bay Pkwy (D → Q) ↔ Grand St (B,D) |
| 8 | 590 | direct | far | 918m | Kings Hwy (B,Q → B,D) ↔ 14 St-Union Sq (N,Q,R) |
| 9 | 579 | direct | close | 191m | Church Av (B,Q → B,D) ↔ Times Sq-42 St (N,Q,R) |
| 10 | 560 | direct | far | 565m | 18 Av (D → Q) ↔ Grand St (B,D) |
| 11 | 488 | direct | far | 918m | Newkirk Plaza (B,Q → B,D) ↔ 14 St-Union Sq (N,Q,R) |
| 12 | 485 | direct | far | 803m | DeKalb Av (B,Q,R → B,D,R) ↔ 72 St (Q) |
| 13 | 485 | direct | far | 565m | Kings Hwy (B,Q → B,D) ↔ Canal St (N,Q,R) |
| 14 | 476 | direct | close | 191m | Prospect Park (B,Q → B,D) ↔ Times Sq-42 St (N,Q,R) |
| 15 | 467 | direct | close | 191m | 7 Av (B,Q → B,D) ↔ Times Sq-42 St (N,Q,R) |
| 16 | 461 | direct | far | 565m | 71 St (D → Q) ↔ Grand St (B,D) |
| 17 | 460 | direct | far | 565m | 9 Av (D → Q) ↔ Grand St (B,D) |
| 18 | 459 | direct | far | 565m | Avenue U (Q → D) ↔ Canal St (N,Q,R) |
| 19 | 450 | direct | close | 191m | Parkside Av (Q → D) ↔ Times Sq-42 St (N,Q,R) |
| 20 | 437 | direct | far | 565m | 25 Av (D → Q) ↔ Grand St (B,D) |
| 21 | 422 | direct | far | 565m | Grand St (B,D) ↔ 36 St (D,N,R → N,Q,R) |
| 22 | 418 | direct | far | 565m | 7 Av (B,Q → B,D) ↔ Canal St (N,Q,R) |
| 23 | 418 | direct | far | 918m | Cortelyou Rd (Q → D) ↔ 14 St-Union Sq (N,Q,R) |
| 24 | 391 | direct | close | 191m | Newkirk Plaza (B,Q → B,D) ↔ Times Sq-42 St (N,Q,R) |
| 25 | 389 | direct | far | 565m | Grand St (B,D) ↔ 20 Av (D → Q) |

### Top 25 Origin/Destination Pairs

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 5,828 | 0.70% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Cortlandt St (R) |
| 2 | 5,414 | 0.65% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 3 | 5,330 | 0.64% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 4 | 5,074 | 0.61% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 47-50 Sts-Rockefeller Ctr (B,D) |
| 5 | 4,620 | 0.55% | 1-seat | | | | 72 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 6 | 4,597 | 0.55% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 72 St (Q) |
| 7 | 4,337 | 0.52% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |
| 8 | 3,658 | 0.44% | xfer | close | 191m | origin: 42 St-Bryant Pk (B,D) | Times Sq-42 St (N,Q,R) ↔ W 4 St-Wash Sq (B,D) |
| 9 | 3,522 | 0.42% | 1-seat | | | | 86 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 10 | 3,356 | 0.40% | 1-seat | | | | 86 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 11 | 3,293 | 0.39% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ Times Sq-42 St (N,Q,R) |
| 12 | 3,166 | 0.38% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Whitehall St-South Ferry (R) |
| 13 | 2,822 | 0.34% | 1-seat | | | | Canal St (N,Q,R) ↔ Times Sq-42 St (N,Q,R) |
| 14 | 2,779 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 15 | 2,755 | 0.33% | 1-seat | | | | Times Sq-42 St (N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 16 | 2,622 | 0.31% | 1-seat | | | | 86 St (Q) ↔ 57 St-7 Av (N,Q,R) |
| 17 | 2,378 | 0.28% | 1-seat | | | | 23 St (R) ↔ Times Sq-42 St (N,Q,R) |
| 18 | 2,365 | 0.28% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Canal St (N,Q,R) |
| 19 | 2,362 | 0.28% | 1-seat | | | | 96 St (Q) ↔ Times Sq-42 St (N,Q,R) |
| 20 | 2,273 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ 59 St-Columbus Circle (B,D) |
| 21 | 2,257 | 0.27% | 1-seat | | | | 96 St (Q) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 22 | 2,251 | 0.27% | 1-seat | | | | 34 St-Herald Sq (B,D,N,Q,R) ↔ Lexington Av/59 St (N,R) |
| 23 | 2,189 | 0.26% | 1-seat | | | | Jackson Hts-Roosevelt Av (R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 24 | 2,128 | 0.25% | 1-seat | | | | 49 St (N,R) ↔ 34 St-Herald Sq (B,D,N,Q,R) |
| 25 | 2,072 | 0.25% | 1-seat | | | | 57 St-7 Av (N,Q,R) ↔ 14 St-Union Sq (N,Q,R) |

### Top 25 Origin Stations, Summed across All Destinations

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 54,350 | 67.4% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,290 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 29,069 | 74.8% | 79.9% | 14 St-Union Sq (N,Q,R) |
| 22,108 | 53.4% | 91.3% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 22,015 | 67.1% | 74.2% | Cortlandt St (R) |
| 19,234 | 59.8% | 75.3% | 59 St-Columbus Circle (B,D) |
| 18,461 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 18,143 | 61.2% | 78.1% | Jackson Hts-Roosevelt Av (R) |
| 18,101 | 78.1% | 83.4% | Canal St (N,Q,R) |
| 17,855 | 50.9% | 100.0% | 42 St-Bryant Pk (B,D) |
| 16,103 | 86.7% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,212 | 47.6% | 62.4% | W 4 St-Wash Sq (B,D) |
| 14,511 | 55.8% | 58.5% | 72 St (Q) |
| 14,205 | 78.4% | 88.4% | Lexington Av/59 St (N,R) |
| 13,206 | 84.4% | 94.3% | 49 St (N,R) |
| 13,162 | 87.1% | 87.8% | DeKalb Av (B,D,R) |
| 12,565 | 51.5% | 89.8% | Broadway-Lafayette St (B,D) |
| 12,290 | 59.4% | 62.7% | 86 St (Q) |
| 11,900 | 48.2% | 55.2% | Grand St (B,D) |
| 10,959 | 71.9% | 76.7% | Kings Hwy (B,D) |
| 10,676 | 70.7% | 76.5% | Whitehall St-South Ferry (R) |
| 10,159 | 59.7% | 68.5% | Jay St-MetroTech (R) |
| 9,284 | 69.6% | 81.8% | 125 St (B,D) |
| 9,225 | 67.9% | 73.7% | 23 St (R) |
| 9,209 | 59.5% | 81.1% | Forest Hills-71 Av (R) |

### Top 25 Destination Stations, Summed across All Origins

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 54,675 | 67.2% | 100.0% | Times Sq-42 St (N,Q,R) |
| 48,360 | 100.0% | 100.0% | 34 St-Herald Sq (B,D,N,Q,R) |
| 31,416 | 76.9% | 81.4% | 14 St-Union Sq (N,Q,R) |
| 23,378 | 53.2% | 90.5% | 47-50 Sts-Rockefeller Ctr (B,D) |
| 21,158 | 55.8% | 70.2% | 59 St-Columbus Circle (B,D) |
| 20,826 | 67.7% | 72.7% | Cortlandt St (R) |
| 19,376 | 78.1% | 82.8% | Canal St (N,Q,R) |
| 18,786 | 49.6% | 100.0% | 42 St-Bryant Pk (B,D) |
| 17,432 | 100.0% | 100.0% | Atlantic Av (B,D,N,Q,R) |
| 16,993 | 61.0% | 78.2% | Jackson Hts-Roosevelt Av (R) |
| 16,838 | 82.0% | 100.0% | 57 St-7 Av (N,Q,R) |
| 15,995 | 47.9% | 61.5% | W 4 St-Wash Sq (B,D) |
| 14,601 | 80.5% | 90.3% | Lexington Av/59 St (N,R) |
| 14,250 | 56.9% | 58.5% | 72 St (Q) |
| 14,100 | 51.0% | 90.8% | Broadway-Lafayette St (B,D) |
| 12,855 | 79.7% | 93.3% | 49 St (N,R) |
| 12,413 | 48.1% | 53.6% | Grand St (B,D) |
| 12,331 | 86.6% | 87.2% | DeKalb Av (B,D,R) |
| 11,243 | 59.1% | 62.0% | 86 St (Q) |
| 11,048 | 72.2% | 76.7% | Kings Hwy (B,D) |
| 10,457 | 59.5% | 67.6% | Jay St-MetroTech (R) |
| 9,785 | 73.8% | 76.5% | Whitehall St-South Ferry (R) |
| 9,281 | 68.7% | 73.3% | 23 St (R) |
| 9,136 | 60.2% | 81.8% | Forest Hills-71 Av (R) |
| 9,112 | 70.7% | 82.5% | 125 St (B,D) |
