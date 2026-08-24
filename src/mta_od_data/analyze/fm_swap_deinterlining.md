# Deinterlining Scenario Comparison: F/M Swap

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), over every origin/destination pair with both ends served by E,F,M,R under any scenario compared here. Pairs with only one end on those routes are reported alongside as context, but can't be a one-seat ride under any of them.

Produced by `mta-od-data analyze deinterlining --category 'F/M Swap' --markdown-out src/mta_od_data/analyze/fm_swap_deinterlining.md`.

---

## Scenario Comparison

Two cuts of the same classification. Neither is the whole answer: the first says what a scenario does to the riders it can reach, the second how much of the system it reaches at all. In both, only how many riders get a one-seat ride changes between scenarios, never the total. Each `Δ` is against Current. Close one-seat counts a transfer trip whose destination is within 300m of a station on that scenario's effective origin corridor.

### Both Ends on the Comparison's Routes

The 872,173 riders whose origin *and* destination are served by E,F,M,R: the trips these routes could carry end to end, including the many that keep a one-seat ride whatever the scenario. Every table below is scoped to these.

| Scenario | Total Riders | Direct 1-Seat | Δ | Close 1-Seat | Δ | Effective 1-Seat | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current | 872,173 | 636,938 (73.0%) | | 58,282 (6.7%) | | 695,220 (79.7%) | |
| F 63 St | 872,173 | 647,889 (74.3%) | +10,951 (+1.3%) | 61,698 (7.1%) | +3,416 (+0.4%) | 709,587 (81.4%) | +14,367 (+1.6%) |

### Either End on the Comparison's Routes

The wider 2,487,892 riders with *either* end served by E,F,M,R, the above among them. The difference is transfer trips with one end off these routes entirely, which no scenario here can change: they can only dilute the rate, which is why a junction's effect washes out against this total.

| Scenario | Total Riders | Direct 1-Seat | Δ | Close 1-Seat | Δ | Effective 1-Seat | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current | 2,487,892 | 636,938 (25.6%) | | 185,886 (7.5%) | | 822,824 (33.1%) | |
| F 63 St | 2,487,892 | 647,889 (26.0%) | +10,951 (+0.4%) | 189,658 (7.6%) | +3,772 (+0.2%) | 837,547 (33.7%) | +14,723 (+0.6%) |

---

## Current

### Top 25 Origin/Destination Pairs

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 5,828 | 0.67% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 2 | 5,414 | 0.62% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 14 St-Union Sq (R) |
| 3 | 5,074 | 0.58% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ 47-50 Sts-Rockefeller Ctr (F,M) |
| 4 | 4,761 | 0.55% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 14 St (E) |
| 5 | 4,715 | 0.54% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Lexington Av/53 St (E,F) |
| 6 | 4,337 | 0.50% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ 14 St-Union Sq (R) |
| 7 | 3,990 | 0.46% | 1-seat | | | | 34 St-Penn Station (E) ↔ Times Sq-42 St/PABT (E,R) |
| 8 | 3,907 | 0.45% | 1-seat | | | | 34 St-Penn Station (E) ↔ Lexington Av/53 St (E,F) |
| 9 | 3,745 | 0.43% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 5 Av/53 St (E,F) |
| 10 | 3,739 | 0.43% | 1-seat | | | | 34 St-Penn Station (E) ↔ 14 St (E) |
| 11 | 3,658 | 0.42% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ W 4 St-Wash Sq (E,F,M) |
| 12 | 3,293 | 0.38% | 1-seat | | | | Jackson Hts-Roosevelt Av (E,F,M,R) ↔ Times Sq-42 St/PABT (E,R) |
| 13 | 3,242 | 0.37% | 1-seat | | | | 34 St-Penn Station (E) ↔ Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 14 | 3,166 | 0.36% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Whitehall St-South Ferry (R) |
| 15 | 3,144 | 0.36% | 1-seat | | | | 34 St-Penn Station (E) ↔ 5 Av/53 St (E,F) |
| 16 | 2,846 | 0.33% | 1-seat | | | | 34 St-Penn Station (E) ↔ W 4 St-Wash Sq (E,F,M) |
| 17 | 2,822 | 0.32% | 1-seat | | | | Canal St (R) ↔ Times Sq-42 St/PABT (E,R) |
| 18 | 2,779 | 0.32% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 34 St-Herald Sq (F,M,R) |
| 19 | 2,755 | 0.32% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Lexington Av/59 St (R) |
| 20 | 2,679 | 0.31% | 1-seat | | | | 34 St-Penn Station (E) ↔ 50 St (E) |
| 21 | 2,397 | 0.27% | 1-seat | | | | 23 St (F,M) ↔ 47-50 Sts-Rockefeller Ctr (F,M) |
| 22 | 2,378 | 0.27% | 1-seat | | | | 23 St (R) ↔ Times Sq-42 St/PABT (E,R) |
| 23 | 2,365 | 0.27% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ Canal St (R) |
| 24 | 2,322 | 0.27% | 1-seat | | | | 23 St (E) ↔ Times Sq-42 St/PABT (E,R) |
| 25 | 2,294 | 0.26% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Canal St (E) |

</details>

### Top 25 Origin Stations, Summed across All Destinations

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 53,938 | 82.7% | 100.0% | Times Sq-42 St/PABT (E,R) |
| 39,449 | 94.5% | 95.6% | 34 St-Herald Sq (F,M,R) |
| 31,546 | 62.9% | 64.3% | 34 St-Penn Station (E) |
| 27,183 | 100.0% | 100.0% | Jackson Hts-Roosevelt Av (E,F,M,R) |
| 26,617 | 83.8% | 89.0% | Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 25,347 | 64.0% | 71.5% | 14 St-Union Sq (R) |
| 23,989 | 75.3% | 93.2% | 47-50 Sts-Rockefeller Ctr (F,M) |
| 21,066 | 72.6% | 74.1% | Lexington Av/53 St (E,F) |
| 20,467 | 75.5% | 92.7% | 42 St-Bryant Pk (F,M) |
| 18,411 | 85.2% | 88.6% | W 4 St-Wash Sq (E,F,M) |
| 16,501 | 54.8% | 56.0% | 14 St (E) |
| 15,359 | 64.6% | 72.3% | Canal St (R) |
| 14,624 | 62.5% | 90.1% | Broadway-Lafayette St (F,M) |
| 14,553 | 80.8% | 81.9% | Jay St-MetroTech (F,R) |
| 13,965 | 100.0% | 100.0% | Forest Hills-71 Av (E,F,M,R) |
| 13,652 | 83.4% | 89.4% | 23 St (F,M) |
| 12,363 | 63.8% | 75.3% | 14 St (F,M) |
| 12,223 | 69.2% | 78.3% | Atlantic Av (R) |
| 12,014 | 71.0% | 77.8% | Delancey St-Essex St (F,M) |
| 11,931 | 54.5% | 55.5% | Sutphin Blvd-Archer Av-JFK Airport (E) |
| 11,925 | 68.7% | 83.4% | Lexington Av/59 St (R) |
| 11,214 | 72.0% | 72.7% | Kew Gardens-Union Tpke (E,F) |
| 11,029 | 56.2% | 56.6% | Jamaica Center-Parsons/Archer (E) |
| 10,826 | 79.1% | 95.3% | 49 St (R) |
| 10,714 | 70.4% | 76.8% | Whitehall St-South Ferry (R) |

</details>

### Top 25 Destination Stations, Summed across All Origins

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 53,466 | 82.5% | 100.0% | Times Sq-42 St/PABT (E,R) |
| 39,257 | 93.6% | 94.7% | 34 St-Herald Sq (F,M,R) |
| 29,014 | 62.7% | 63.4% | 34 St-Penn Station (E) |
| 27,805 | 66.1% | 72.5% | 14 St-Union Sq (R) |
| 25,851 | 100.0% | 100.0% | Jackson Hts-Roosevelt Av (E,F,M,R) |
| 24,901 | 75.3% | 92.9% | 47-50 Sts-Rockefeller Ctr (F,M) |
| 24,863 | 84.8% | 88.3% | Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 21,689 | 74.7% | 75.7% | Lexington Av/53 St (E,F) |
| 20,654 | 74.0% | 93.1% | 42 St-Bryant Pk (F,M) |
| 19,269 | 86.8% | 89.3% | W 4 St-Wash Sq (E,F,M) |
| 16,959 | 59.3% | 59.9% | 14 St (E) |
| 16,555 | 64.7% | 71.4% | Canal St (R) |
| 16,476 | 60.9% | 89.6% | Broadway-Lafayette St (F,M) |
| 14,228 | 81.1% | 82.2% | Jay St-MetroTech (F,R) |
| 14,124 | 100.0% | 100.0% | Forest Hills-71 Av (E,F,M,R) |
| 13,791 | 63.9% | 80.4% | Lexington Av/59 St (R) |
| 13,353 | 74.7% | 80.5% | Delancey St-Essex St (F,M) |
| 13,237 | 80.2% | 86.7% | 23 St (F,M) |
| 13,139 | 62.3% | 74.6% | 14 St (F,M) |
| 12,257 | 67.0% | 76.0% | Atlantic Av (R) |
| 11,378 | 73.3% | 73.8% | Kew Gardens-Union Tpke (E,F) |
| 11,237 | 71.4% | 96.6% | 57 St-7 Av (R) |
| 10,909 | 84.7% | 85.2% | 5 Av/53 St (E,F) |
| 10,817 | 80.3% | 81.9% | Court Sq-23 St (E,F) |
| 10,633 | 73.2% | 91.0% | 49 St (R) |

</details>

---

## F 63 St

### What Changed, against Current

Every both-ends rider, and their share of the 872,173 of them: **was** is what Current gives them, **now** what F 63 St would. Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| Riders | now direct | now close | now far |
| --- | ---: | ---: | ---: |
| **was direct** | 627,081 (71.9%) | 2,446 (0.3%) | 7,411 (0.8%) |
| **was close** | 402 (0.0%) | 56,772 (6.5%) | 1,108 (0.1%) |
| **was far** | 20,406 (2.3%) | 2,480 (0.3%) | 154,067 (17.7%) |

- Gained: 22,886 (2.6%)
- Lost: 8,519 (1.0%)
- Net: +14,367 (1.6%)

### Biggest Changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. An end reads `today→F 63 St` where its routes change, and today's alone where they don't; `Dist` and `Walk` are the walk under F 63 St, as in the pairs table below.

| # | Riders | Was | Now | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 962 | far | direct | | | Lexington Av/63 St (M→F) ↔ Jamaica-179 St (F) |
| 2 | 810 | far | direct | | | Lexington Av/63 St (M→F) ↔ Kew Gardens-Union Tpke (E,F) |
| 3 | 684 | far | direct | | | Jamaica-179 St (F) ↔ 57 St (M→F) |
| 4 | 642 | far | direct | | | Grand Av-Newtown (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 5 | 568 | far | direct | | | Woodhaven Blvd (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 6 | 541 | far | direct | | | 63 Dr-Rego Park (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 7 | 495 | direct | far | 825m | dest: Lexington Av/63 St (F) | Jamaica-179 St (F) ↔ Lexington Av/53 St (F→E,M) |
| 8 | 476 | far | direct | | | Kew Gardens-Union Tpke (E,F) ↔ 57 St (M→F) |
| 9 | 453 | far | direct | | | Jamaica-179 St (F) ↔ 21 St-Queensbridge (M→F) |
| 10 | 402 | far | direct | | | 57 St (M→F) ↔ 2 Av (F) |
| 11 | 401 | far | direct | | | Steinway St (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 12 | 392 | far | direct | | | 21 St-Queensbridge (M→F) ↔ Kew Gardens-Union Tpke (E,F) |
| 13 | 389 | far | direct | | | Elmhurst Av (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 14 | 330 | far | direct | | | Lexington Av/63 St (M→F) ↔ Parsons Blvd (F) |
| 15 | 324 | direct | close | 239m | dest: Lexington Av/59 St (R) | Grand Av-Newtown (M,R) ↔ Lexington Av/63 St (M→F) |
| 16 | 316 | far | direct | | | 67 Av (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 17 | 313 | direct | far | 748m | dest: 21 St-Queensbridge (F) | Jamaica-179 St (F) ↔ Queens Plaza (F→E,M,R) |
| 18 | 307 | direct | close | 239m | origin: Lexington Av/59 St (R) | Lexington Av/63 St (M→F) ↔ Woodhaven Blvd (M,R) |
| 19 | 301 | far | direct | | | Lexington Av/63 St (M→F) ↔ 169 St (F) |
| 20 | 300 | far | direct | | | Parsons Blvd (F) ↔ 21 St-Queensbridge (M→F) |
| 21 | 292 | far | close | 239m | dest: Lexington Av/63 St (F) | Kew Gardens-Union Tpke (E,F) ↔ Lexington Av/59 St (R) |
| 22 | 289 | far | close | 239m | dest: Lexington Av/63 St (F) | Jamaica-179 St (F) ↔ Lexington Av/59 St (R) |
| 23 | 286 | far | direct | | | 46 St (M,R) ↔ Lexington Av/53 St (F→E,M) |
| 24 | 274 | far | direct | | | Myrtle-Wyckoff Avs (M) ↔ Lexington Av/53 St (F→E,M) |
| 25 | 272 | close | far | 588m | dest: Lexington Av/53 St (E,M) | Myrtle-Wyckoff Avs (M) ↔ Lexington Av/59 St (R) |

### Biggest Changes by Station, against Current

The same changed pairs as above, added up at the stations they run between: the top 25 by `Net`, which is riders gaining an effective one-seat ride here less those losing one, taken either way round. A station whose riders only move between `direct` and `close` keeps them all effective and nets nothing, however many moved. A pair is a change at both of its ends and counts at each, so `Riders` runs to twice what the matrix counts.

| # | Riders | Net | direct→close | direct→far | close→direct | close→far | far→direct | far→close | Station |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 6,066 | +4,010 | 1,339 | 281 | 156 | | 4,291 | | Lexington Av/63 St (M→F) |
| 2 | 5,682 | +3,537 | 1,108 | 396 | 246 | | 3,933 | | 57 St (M→F) |
| 3 | 7,220 | +2,222 | | 2,499 | | | 4,721 | | Lexington Av/53 St (F→E,M) |
| 4 | 2,060 | +2,060 | | | | | 1,768 | 292 | Kew Gardens-Union Tpke (E,F) |
| 5 | 3,241 | +1,476 | | 883 | | | 2,359 | | 21 St-Queensbridge (M→F) |
| 6 | 2,841 | +1,450 | | 696 | | | 2,146 | | 5 Av/53 St (F→E,M) |
| 7 | 3,708 | +1,361 | | 1,174 | | | 2,179 | 356 | Jamaica-179 St (F) |
| 8 | 2,396 | +1,161 | | | | 618 | | 1,779 | Lexington Av/59 St (R) |
| 9 | 1,966 | +924 | 582 | 230 | | | 1,154 | | Grand Av-Newtown (M,R) |
| 10 | 917 | +795 | 78 | 22 | | | 817 | | Steinway St (M,R) |
| 11 | 1,479 | +761 | 379 | 170 | | | 931 | | 63 Dr-Rego Park (M,R) |
| 12 | 1,925 | +743 | 537 | 323 | | | 1,066 | | Woodhaven Blvd (M,R) |
| 13 | 959 | -681 | | 820 | | | 139 | | Queens Plaza (F→E,M,R) |
| 14 | 1,338 | +681 | | 328 | | | 877 | 132 | Parsons Blvd (F) |
| 15 | 3,557 | +678 | | 1,440 | | | 2,117 | | Court Sq-23 St (F→E,M) |
| 16 | 715 | +573 | 74 | 34 | | | 607 | | 46 St (M,R) |
| 17 | 1,299 | +571 | | 364 | | | 706 | 230 | 2 Av (F) |
| 18 | 1,286 | +549 | 364 | 186 | | | 735 | | Elmhurst Av (M,R) |
| 19 | 540 | +540 | | | | | 468 | 72 | Briarwood (E,F) |
| 20 | 890 | +519 | 253 | 59 | | | 578 | | 67 Av (M,R) |
| 21 | 1,223 | +484 | | 369 | | | 712 | 142 | 169 St (F) |
| 22 | 579 | +434 | 96 | 25 | | | 459 | | Northern Blvd (M,R) |
| 23 | 394 | +394 | | | | | 345 | 49 | 75 Av (E,F) |
| 24 | 757 | +377 | | 190 | | | 500 | 67 | Sutphin Blvd (F) |
| 25 | 1,099 | +365 | | 367 | | | 522 | 210 | York St (F) |

### Top 25 Origin/Destination Pairs

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 5,828 | 0.67% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 2 | 5,414 | 0.62% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 14 St-Union Sq (R) |
| 3 | 5,074 | 0.58% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ 47-50 Sts-Rockefeller Ctr (F,M) |
| 4 | 4,761 | 0.55% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 14 St (E) |
| 5 | 4,715 | 0.54% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Lexington Av/53 St (E,M) |
| 6 | 4,337 | 0.50% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ 14 St-Union Sq (R) |
| 7 | 3,990 | 0.46% | 1-seat | | | | 34 St-Penn Station (E) ↔ Times Sq-42 St/PABT (E,R) |
| 8 | 3,907 | 0.45% | 1-seat | | | | 34 St-Penn Station (E) ↔ Lexington Av/53 St (E,M) |
| 9 | 3,745 | 0.43% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 5 Av/53 St (E,M) |
| 10 | 3,739 | 0.43% | 1-seat | | | | 34 St-Penn Station (E) ↔ 14 St (E) |
| 11 | 3,658 | 0.42% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ W 4 St-Wash Sq (E,F,M) |
| 12 | 3,293 | 0.38% | 1-seat | | | | Jackson Hts-Roosevelt Av (E,F,M,R) ↔ Times Sq-42 St/PABT (E,R) |
| 13 | 3,242 | 0.37% | 1-seat | | | | 34 St-Penn Station (E) ↔ Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 14 | 3,166 | 0.36% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Whitehall St-South Ferry (R) |
| 15 | 3,144 | 0.36% | 1-seat | | | | 34 St-Penn Station (E) ↔ 5 Av/53 St (E,M) |
| 16 | 2,846 | 0.33% | 1-seat | | | | 34 St-Penn Station (E) ↔ W 4 St-Wash Sq (E,F,M) |
| 17 | 2,822 | 0.32% | 1-seat | | | | Canal St (R) ↔ Times Sq-42 St/PABT (E,R) |
| 18 | 2,779 | 0.32% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ 34 St-Herald Sq (F,M,R) |
| 19 | 2,755 | 0.32% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Lexington Av/59 St (R) |
| 20 | 2,679 | 0.31% | 1-seat | | | | 34 St-Penn Station (E) ↔ 50 St (E) |
| 21 | 2,397 | 0.27% | 1-seat | | | | 23 St (F,M) ↔ 47-50 Sts-Rockefeller Ctr (F,M) |
| 22 | 2,378 | 0.27% | 1-seat | | | | 23 St (R) ↔ Times Sq-42 St/PABT (E,R) |
| 23 | 2,365 | 0.27% | 1-seat | | | | 34 St-Herald Sq (F,M,R) ↔ Canal St (R) |
| 24 | 2,322 | 0.27% | 1-seat | | | | 23 St (E) ↔ Times Sq-42 St/PABT (E,R) |
| 25 | 2,294 | 0.26% | 1-seat | | | | Times Sq-42 St/PABT (E,R) ↔ Canal St (E) |

</details>

### Top 25 Origin Stations, Summed across All Destinations

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 53,938 | 82.7% | 100.0% | Times Sq-42 St/PABT (E,R) |
| 39,449 | 94.5% | 95.6% | 34 St-Herald Sq (F,M,R) |
| 31,546 | 62.9% | 64.3% | 34 St-Penn Station (E) |
| 27,183 | 100.0% | 100.0% | Jackson Hts-Roosevelt Av (E,F,M,R) |
| 26,617 | 83.8% | 89.0% | Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 25,347 | 64.0% | 71.5% | 14 St-Union Sq (R) |
| 23,989 | 75.3% | 93.2% | 47-50 Sts-Rockefeller Ctr (F,M) |
| 21,066 | 77.7% | 79.2% | Lexington Av/53 St (E,M) |
| 20,467 | 75.5% | 92.7% | 42 St-Bryant Pk (F,M) |
| 18,411 | 85.2% | 88.6% | W 4 St-Wash Sq (E,F,M) |
| 16,501 | 54.8% | 56.0% | 14 St (E) |
| 15,359 | 64.6% | 72.3% | Canal St (R) |
| 14,624 | 62.5% | 90.1% | Broadway-Lafayette St (F,M) |
| 14,553 | 81.4% | 81.6% | Jay St-MetroTech (F,R) |
| 13,965 | 100.0% | 100.0% | Forest Hills-71 Av (E,F,M,R) |
| 13,652 | 83.4% | 89.4% | 23 St (F,M) |
| 12,363 | 63.8% | 75.3% | 14 St (F,M) |
| 12,223 | 69.2% | 78.3% | Atlantic Av (R) |
| 12,014 | 71.0% | 77.8% | Delancey St-Essex St (F,M) |
| 11,931 | 54.5% | 55.5% | Sutphin Blvd-Archer Av-JFK Airport (E) |
| 11,925 | 68.7% | 86.1% | Lexington Av/59 St (R) |
| 11,214 | 79.8% | 82.2% | Kew Gardens-Union Tpke (E,F) |
| 11,029 | 56.2% | 56.6% | Jamaica Center-Parsons/Archer (E) |
| 10,826 | 79.1% | 95.3% | 49 St (R) |
| 10,714 | 70.4% | 76.8% | Whitehall St-South Ferry (R) |

</details>

### Top 25 Destination Stations, Summed across All Origins

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 53,466 | 82.5% | 100.0% | Times Sq-42 St/PABT (E,R) |
| 39,257 | 93.6% | 94.7% | 34 St-Herald Sq (F,M,R) |
| 29,014 | 62.7% | 63.4% | 34 St-Penn Station (E) |
| 27,805 | 66.1% | 72.5% | 14 St-Union Sq (R) |
| 25,851 | 100.0% | 100.0% | Jackson Hts-Roosevelt Av (E,F,M,R) |
| 24,901 | 75.3% | 92.9% | 47-50 Sts-Rockefeller Ctr (F,M) |
| 24,863 | 84.8% | 88.3% | Chambers St/WTC/Park Pl/Cortlandt St (E,R) |
| 21,689 | 80.0% | 81.0% | Lexington Av/53 St (E,M) |
| 20,654 | 74.0% | 93.1% | 42 St-Bryant Pk (F,M) |
| 19,269 | 86.8% | 89.3% | W 4 St-Wash Sq (E,F,M) |
| 16,959 | 59.3% | 59.9% | 14 St (E) |
| 16,555 | 64.7% | 71.4% | Canal St (R) |
| 16,476 | 60.9% | 89.6% | Broadway-Lafayette St (F,M) |
| 14,228 | 81.7% | 81.9% | Jay St-MetroTech (F,R) |
| 14,124 | 100.0% | 100.0% | Forest Hills-71 Av (E,F,M,R) |
| 13,791 | 63.9% | 86.5% | Lexington Av/59 St (R) |
| 13,353 | 74.7% | 80.5% | Delancey St-Essex St (F,M) |
| 13,237 | 80.2% | 86.7% | 23 St (F,M) |
| 13,139 | 62.3% | 74.6% | 14 St (F,M) |
| 12,257 | 67.0% | 76.0% | Atlantic Av (R) |
| 11,378 | 81.2% | 82.6% | Kew Gardens-Union Tpke (E,F) |
| 11,237 | 71.4% | 97.7% | 57 St-7 Av (R) |
| 10,909 | 91.3% | 91.8% | 5 Av/53 St (E,M) |
| 10,817 | 82.8% | 84.3% | Court Sq-23 St (E,M) |
| 10,633 | 73.2% | 91.0% | 49 St (R) |

</details>
