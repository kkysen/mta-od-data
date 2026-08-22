# Deinterlining Scenario Comparison: 2,3,4,5

Average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12), over every origin/destination pair with both ends served by 2,3,4,5 under any scenario compared here. Pairs with only one end on those routes are reported alongside as context, but can't be a one-seat ride under any of them.

Produced by `mta-od-data analyze deinterlining --category Nostrand --markdown-out src/mta_od_data/analyze/nostrand_deinterlining.md`.

---

## Scenario Comparison

Two cuts of the same classification. Neither is the whole answer: the first says what a scenario does to the riders it can reach, the second how much of the system it reaches at all. In both, only how many riders get a one-seat ride changes between scenarios, never the total. Each `Δ` is against Current. Close one-seat counts a transfer trip whose destination is within 300m of a station on that scenario's effective origin corridor.

### Both Ends on the Comparison's Routes

The 503,188 riders whose origin *and* destination are served by 2,3,4,5: the trips these routes could carry end to end, including the many that keep a one-seat ride whatever the scenario. Every table below is scoped to these.

| Scenario | Total Riders | Direct 1-Seat | Δ | Close 1-Seat | Δ | Effective 1-Seat | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current | 503,188 | 420,896 (83.6%) | | 4,236 (0.8%) | | 425,131 (84.5%) | |
| 2/3 Nostrand | 503,188 | 404,300 (80.3%) | -16,596 (-3.3%) | 6,165 (1.2%) | +1,929 (+0.4%) | 410,464 (81.6%) | -14,667 (-2.9%) |
| 4/5 Nostrand | 503,188 | 401,727 (79.8%) | -19,169 (-3.8%) | 5,984 (1.2%) | +1,748 (+0.3%) | 407,710 (81.0%) | -17,421 (-3.5%) |

### Either End on the Comparison's Routes

The wider 1,765,300 riders with *either* end served by 2,3,4,5, the above among them. The difference is transfer trips with one end off these routes entirely, which no scenario here can change: they can only dilute the rate, which is why a junction's effect washes out against this total.

| Scenario | Total Riders | Direct 1-Seat | Δ | Close 1-Seat | Δ | Effective 1-Seat | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current | 1,765,300 | 420,896 (23.8%) | | 89,865 (5.1%) | | 510,761 (28.9%) | |
| 2/3 Nostrand | 1,765,300 | 404,300 (22.9%) | -16,596 (-0.9%) | 89,623 (5.1%) | -242 (-0.0%) | 493,923 (28.0%) | -16,838 (-1.0%) |
| 4/5 Nostrand | 1,765,300 | 401,727 (22.8%) | -19,169 (-1.1%) | 89,478 (5.1%) | -387 (-0.0%) | 491,205 (27.8%) | -19,556 (-1.1%) |

---

## Current

### Top 25 Origin/Destination Pairs

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 12,244 | 2.43% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Fulton St (2,3,4,5) |
| 2 | 8,657 | 1.72% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | Times Sq-42 St (2,3) ↔ Grand Central-42 St (4,5) |
| 3 | 8,056 | 1.60% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 14 St-Union Sq (4,5) |
| 4 | 5,828 | 1.16% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Park Pl (2,3) |
| 5 | 5,566 | 1.11% | 1-seat | | | | 86 St (4,5) ↔ Grand Central-42 St (4,5) |
| 6 | 5,414 | 1.08% | xfer | far | 932m | dest: 14 St (2,3) | Times Sq-42 St (2,3) ↔ 14 St-Union Sq (4,5) |
| 7 | 5,329 | 1.06% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Fulton St (2,3,4,5) |
| 8 | 5,082 | 1.01% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Brooklyn Bridge-City Hall (4,5) |
| 9 | 5,067 | 1.01% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | 34 St-Penn Station (2,3) ↔ Grand Central-42 St (4,5) |
| 10 | 4,228 | 0.84% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Wall St (2,3) |
| 11 | 3,855 | 0.77% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 72 St (2,3) |
| 12 | 3,852 | 0.77% | 1-seat | | | | Bowling Green (4,5) ↔ Grand Central-42 St (4,5) |
| 13 | 3,836 | 0.76% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 72 St (2,3) |
| 14 | 3,721 | 0.74% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 59 St (4,5) |
| 15 | 3,612 | 0.72% | 1-seat | | | | Wall St (4,5) ↔ Grand Central-42 St (4,5) |
| 16 | 3,477 | 0.69% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 96 St (2,3) |
| 17 | 3,304 | 0.66% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 96 St (2,3) |
| 18 | 3,272 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Chambers St (2,3) |
| 19 | 3,255 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Fulton St (2,3,4,5) |
| 20 | 2,978 | 0.59% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Times Sq-42 St (2,3) |
| 21 | 2,800 | 0.56% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 14 St-Union Sq (4,5) |
| 22 | 2,755 | 0.55% | xfer | far | 978m | origin: Grand Central-42 St (4,5) | Times Sq-42 St (2,3) ↔ 59 St (4,5) |
| 23 | 2,716 | 0.54% | 1-seat | | | | Wall St (2,3) ↔ Times Sq-42 St (2,3) |
| 24 | 2,423 | 0.48% | 1-seat | | | | Borough Hall (2,3,4,5) ↔ Grand Central-42 St (4,5) |
| 25 | 2,412 | 0.48% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 86 St (4,5) |

</details>

### Top 25 Origin Stations, Summed across All Destinations

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 44,713 | 70.4% | 71.6% | Grand Central-42 St (4,5) |
| 37,629 | 65.2% | 66.1% | Times Sq-42 St (2,3) |
| 27,189 | 81.1% | 82.3% | 34 St-Penn Station (2,3) |
| 25,334 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 22,248 | 72.2% | 73.4% | 14 St-Union Sq (4,5) |
| 15,323 | 86.6% | 87.1% | 86 St (4,5) |
| 14,083 | 78.5% | 79.3% | 59 St (4,5) |
| 12,679 | 82.4% | 82.7% | 72 St (2,3) |
| 12,205 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,176 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,289 | 83.7% | 83.9% | 96 St (2,3) |
| 10,239 | 92.8% | 93.2% | Crown Hts-Utica Av (3,4) |
| 10,228 | 80.0% | 81.0% | 14 St (2,3) |
| 9,794 | 80.4% | 81.0% | Park Pl (2,3) |
| 9,295 | 84.7% | 85.5% | Bowling Green (4,5) |
| 8,867 | 84.9% | 85.5% | Brooklyn Bridge-City Hall (4,5) |
| 8,824 | 90.0% | 90.1% | 3 Av-149 St (2,5) |
| 8,468 | 88.4% | 88.7% | 125 St (4,5) |
| 8,127 | 92.5% | 92.9% | Flatbush Av-Brooklyn College (2,5) |
| 7,880 | 93.0% | 100.0% | Wall St (2,3) |
| 7,324 | 69.5% | 69.9% | 161 St-Yankee Stadium (4) |
| 6,720 | 85.6% | 86.2% | Chambers St (2,3) |
| 6,420 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,290 | 88.2% | 88.4% | 125 St (2,3) |
| 6,155 | 87.6% | 100.0% | Wall St (4,5) |

</details>

### Top 25 Destination Stations, Summed across All Origins

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 44,614 | 71.9% | 72.6% | Grand Central-42 St (4,5) |
| 35,813 | 66.8% | 67.4% | Times Sq-42 St (2,3) |
| 26,747 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 24,864 | 81.0% | 81.6% | 34 St-Penn Station (2,3) |
| 24,106 | 73.8% | 74.4% | 14 St-Union Sq (4,5) |
| 15,640 | 87.4% | 87.7% | 86 St (4,5) |
| 14,252 | 80.4% | 80.8% | 59 St (4,5) |
| 13,366 | 84.9% | 85.0% | 72 St (2,3) |
| 12,442 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,264 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,515 | 85.5% | 85.6% | 96 St (2,3) |
| 11,267 | 76.9% | 77.3% | Park Pl (2,3) |
| 10,981 | 79.8% | 80.4% | 14 St (2,3) |
| 9,680 | 92.7% | 92.9% | Crown Hts-Utica Av (3,4) |
| 9,646 | 81.0% | 81.5% | Bowling Green (4,5) |
| 9,447 | 81.9% | 82.5% | Brooklyn Bridge-City Hall (4,5) |
| 8,617 | 88.0% | 100.0% | Wall St (2,3) |
| 8,578 | 88.6% | 88.6% | 3 Av-149 St (2,5) |
| 8,098 | 84.4% | 84.7% | 125 St (4,5) |
| 7,786 | 92.2% | 92.4% | Flatbush Av-Brooklyn College (2,5) |
| 7,634 | 73.3% | 73.4% | 161 St-Yankee Stadium (4) |
| 7,274 | 85.1% | 85.3% | Chambers St (2,3) |
| 6,807 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,404 | 80.6% | 100.0% | Wall St (4,5) |
| 6,281 | 86.4% | 86.5% | 125 St (2,3) |

</details>

---

## 2/3 Nostrand

### What Changed, against Current

Every both-ends rider, and their share of the 503,188 of them: **was** is what Current gives them, **now** what 2/3 Nostrand would. Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| Riders | now direct | now close | now far |
| --- | ---: | ---: | ---: |
| **was direct** | 398,449 (79.2%) | 2,587 (0.5%) | 19,859 (3.9%) |
| **was close** | 658 (0.1%) | 3,577 (0.7%) | 0 (0.0%) |
| **was far** | 5,193 (1.0%) | 0 (0.0%) | 72,864 (14.5%) |

- Gained: 5,193 (1.0%)
- Lost: 19,859 (3.9%)
- Net: -14,667 (-2.9%)

### Biggest Changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. An end reads `today→2/3 Nostrand` where its routes change, and today's alone where they don't; `Dist` and `Walk` are the walk under 2/3 Nostrand, as in the pairs table below.

| # | Riders | Was | Now | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 864 | direct | far | 978m | dest: Times Sq-42 St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ Grand Central-42 St (4,5) |
| 2 | 809 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Crown Hts-Utica Av (3→4,5) ↔ Times Sq-42 St (2,3) |
| 3 | 628 | direct | far | 1207m | origin: Grand Central-42 St (4,5) | 34 St-Penn Station (2,3) ↔ Crown Hts-Utica Av (3→4,5) |
| 4 | 574 | direct | far | 932m | dest: 14 St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ 14 St-Union Sq (4,5) |
| 5 | 520 | direct | far | 474m | dest: Wall St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ Bowling Green (4,5) |
| 6 | 415 | direct | far | 978m | dest: Times Sq-42 St (2,3) | Church Av (5→2,3) ↔ Grand Central-42 St (4,5) |
| 7 | 406 | direct | far | 463m | origin: Nevins St (2,3,4,5) | Hoyt St (2,3) ↔ Crown Hts-Utica Av (3→4,5) |
| 8 | 389 | direct | far | 932m | dest: 14 St (2,3) | Church Av (5→2,3) ↔ 14 St-Union Sq (4,5) |
| 9 | 357 | direct | far | 978m | dest: Times Sq-42 St (2,3) | Winthrop St (5→2,3) ↔ Grand Central-42 St (4,5) |
| 10 | 349 | direct | far | 394m | dest: Park Pl (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ Brooklyn Bridge-City Hall (4,5) |
| 11 | 345 | direct | far | 1158m | dest: Atlantic Av (2,3,4,5) | Crown Hts-Utica Av (3→4,5) ↔ Grand Army Plaza (2,3) |
| 12 | 340 | direct | far | 978m | dest: Times Sq-42 St (2,3) | Newkirk Av-Little Haiti (5→2,3) ↔ Grand Central-42 St (4,5) |
| 13 | 307 | direct | far | 932m | origin: 14 St (2,3) | 14 St-Union Sq (4,5) ↔ Winthrop St (5→2,3) |
| 14 | 291 | direct | far | 1831m | dest: Times Sq-42 St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ 59 St (4,5) |
| 15 | 260 | direct | far | 791m | origin: Nostrand Av (5) | Sterling St (5→2,3) ↔ 14 St-Union Sq (4,5) |
| 16 | 256 | direct | far | 932m | dest: 14 St (2,3) | Newkirk Av-Little Haiti (5→2,3) ↔ 14 St-Union Sq (4,5) |
| 17 | 253 | direct | far | 738m | origin: President St-Medgar Evers College (2,3) | Kingston Av (3→5) ↔ Times Sq-42 St (2,3) |
| 18 | 250 | direct | far | 791m | origin: Nostrand Av (5) | Sterling St (5→2,3) ↔ Grand Central-42 St (4,5) |
| 19 | 249 | direct | far | 1501m | origin: President St-Medgar Evers College (2,3) | Crown Hts-Utica Av (3→4,5) ↔ 72 St (2,3) |
| 20 | 247 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Sutter Av-Rutland Rd (3→5) ↔ Times Sq-42 St (2,3) |
| 21 | 231 | direct | far | 463m | origin: Nevins St (2,3,4,5) | Hoyt St (2,3) ↔ Sutter Av-Rutland Rd (3→5) |
| 22 | 229 | direct | far | 2135m | dest: 96 St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ 86 St (4,5) |
| 23 | 229 | direct | close | 247m | dest: Wall St (2,3) | Flatbush Av-Brooklyn College (5→2,3) ↔ Wall St (4,5) |
| 24 | 228 | direct | far | 474m | dest: Wall St (2,3) | Church Av (5→2,3) ↔ Bowling Green (4,5) |
| 25 | 219 | direct | far | 932m | dest: 14 St-Union Sq (4,5) | Crown Hts-Utica Av (3→4,5) ↔ 14 St (2,3) |

### Biggest Changes by Station, against Current

The same changed pairs as above, added up at the stations they run between: the top 25 by `Net`, which is riders gaining an effective one-seat ride here less those losing one, taken either way round. A station whose riders only move between `direct` and `close` keeps them all effective and nets nothing, however many moved. A pair is a change at both of its ends and counts at each, so `Riders` runs to twice what the matrix counts.

| # | Riders | Net | direct→close | direct→far | close→direct | close→far | far→direct | far→close | Station |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 4,449 | -3,496 | 108 | 3,918 | | | 422 | | Crown Hts-Utica Av (3→4,5) |
| 2 | 3,427 | -3,148 | 229 | 3,173 | | | 25 | | Flatbush Av-Brooklyn College (5→2,3) |
| 3 | 2,271 | -2,124 | 147 | 2,124 | | | | | Times Sq-42 St (2,3) |
| 4 | 1,807 | -1,671 | 136 | 1,671 | | | | | 34 St-Penn Station (2,3) |
| 5 | 1,700 | -1,581 | 91 | 1,595 | | | 14 | | Church Av (5→2,3) |
| 6 | 1,667 | -1,561 | 106 | 1,561 | | | | | Hoyt St (2,3) |
| 7 | 3,751 | -1,367 | 177 | 2,420 | 101 | | 1,053 | | Grand Central-42 St (4,5) |
| 8 | 1,357 | -1,237 | 99 | 1,247 | | | 10 | | Winthrop St (5→2,3) |
| 9 | 1,313 | -1,215 | 74 | 1,227 | | | 12 | | Newkirk Av-Little Haiti (5→2,3) |
| 10 | 3,024 | -1,206 | 165 | 1,976 | 114 | | 770 | | 14 St-Union Sq (4,5) |
| 11 | 1,003 | -926 | 77 | 926 | | | | | Grand Army Plaza (2,3) |
| 12 | 1,002 | -911 | 81 | 916 | | | 5 | | Sterling St (5→2,3) |
| 13 | 810 | -750 | 44 | 758 | | | 8 | | Beverly Rd (5→2,3) |
| 14 | 2,121 | -672 | 82 | 1,329 | 53 | | 657 | | Bowling Green (4,5) |
| 15 | 604 | -568 | 35 | 568 | | | | | 72 St (2,3) |
| 16 | 1,898 | -558 | 75 | 1,172 | 37 | | 614 | | Kingston Av (3→5) |
| 17 | 622 | -556 | 66 | 556 | | | | | 14 St (2,3) |
| 18 | 595 | -549 | 46 | 549 | | | | | Park Pl (2,3) |
| 19 | 1,390 | -477 | 64 | 879 | 45 | | 402 | | 59 St (4,5) |
| 20 | 500 | -465 | 35 | 465 | | | | | Chambers St (2,3) |
| 21 | 1,256 | -435 | 50 | 807 | 28 | | 371 | | Brooklyn Bridge-City Hall (4,5) |
| 22 | 455 | -432 | 23 | 432 | | | | | 96 St (2,3) |
| 23 | 2,368 | -427 | 44 | 1,354 | 43 | | 927 | | Sutter Av-Rutland Rd (3→5) |
| 24 | 468 | -419 | 48 | 419 | | | | | Bergen St (2,3) |
| 25 | 441 | -413 | 28 | 413 | | | | | Eastern Pkwy-Brooklyn Museum (2,3) |

### Top 25 Origin/Destination Pairs

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 12,244 | 2.43% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Fulton St (2,3,4,5) |
| 2 | 8,657 | 1.72% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | Times Sq-42 St (2,3) ↔ Grand Central-42 St (4,5) |
| 3 | 8,056 | 1.60% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 14 St-Union Sq (4,5) |
| 4 | 5,828 | 1.16% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Park Pl (2,3) |
| 5 | 5,566 | 1.11% | 1-seat | | | | 86 St (4,5) ↔ Grand Central-42 St (4,5) |
| 6 | 5,414 | 1.08% | xfer | far | 932m | dest: 14 St (2,3) | Times Sq-42 St (2,3) ↔ 14 St-Union Sq (4,5) |
| 7 | 5,329 | 1.06% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Fulton St (2,3,4,5) |
| 8 | 5,082 | 1.01% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Brooklyn Bridge-City Hall (4,5) |
| 9 | 5,067 | 1.01% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | 34 St-Penn Station (2,3) ↔ Grand Central-42 St (4,5) |
| 10 | 4,228 | 0.84% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Wall St (2,3) |
| 11 | 3,855 | 0.77% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 72 St (2,3) |
| 12 | 3,852 | 0.77% | 1-seat | | | | Bowling Green (4,5) ↔ Grand Central-42 St (4,5) |
| 13 | 3,836 | 0.76% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 72 St (2,3) |
| 14 | 3,721 | 0.74% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 59 St (4,5) |
| 15 | 3,612 | 0.72% | 1-seat | | | | Wall St (4,5) ↔ Grand Central-42 St (4,5) |
| 16 | 3,477 | 0.69% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 96 St (2,3) |
| 17 | 3,304 | 0.66% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 96 St (2,3) |
| 18 | 3,272 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Chambers St (2,3) |
| 19 | 3,255 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Fulton St (2,3,4,5) |
| 20 | 2,978 | 0.59% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Times Sq-42 St (2,3) |
| 21 | 2,800 | 0.56% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 14 St-Union Sq (4,5) |
| 22 | 2,755 | 0.55% | xfer | far | 978m | origin: Grand Central-42 St (4,5) | Times Sq-42 St (2,3) ↔ 59 St (4,5) |
| 23 | 2,716 | 0.54% | 1-seat | | | | Wall St (2,3) ↔ Times Sq-42 St (2,3) |
| 24 | 2,423 | 0.48% | 1-seat | | | | Borough Hall (2,3,4,5) ↔ Grand Central-42 St (4,5) |
| 25 | 2,412 | 0.48% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 86 St (4,5) |

</details>

### Top 25 Origin Stations, Summed across All Destinations

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 44,713 | 68.9% | 70.1% | Grand Central-42 St (4,5) |
| 37,629 | 62.3% | 63.4% | Times Sq-42 St (2,3) |
| 27,189 | 77.8% | 79.3% | 34 St-Penn Station (2,3) |
| 25,334 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 22,248 | 69.5% | 70.7% | 14 St-Union Sq (4,5) |
| 15,323 | 85.6% | 86.2% | 86 St (4,5) |
| 14,083 | 76.8% | 77.7% | 59 St (4,5) |
| 12,679 | 80.1% | 80.6% | 72 St (2,3) |
| 12,205 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,176 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,289 | 81.8% | 82.1% | 96 St (2,3) |
| 10,239 | 74.6% | 75.6% | Crown Hts-Utica Av (4,5) |
| 10,228 | 77.1% | 78.4% | 14 St (2,3) |
| 9,794 | 77.8% | 78.5% | Park Pl (2,3) |
| 9,295 | 81.0% | 81.9% | Bowling Green (4,5) |
| 8,867 | 82.5% | 83.3% | Brooklyn Bridge-City Hall (4,5) |
| 8,824 | 91.2% | 91.2% | 3 Av-149 St (2,5) |
| 8,468 | 87.3% | 87.7% | 125 St (4,5) |
| 8,127 | 71.0% | 72.8% | Flatbush Av-Brooklyn College (2,3) |
| 7,880 | 90.2% | 100.0% | Wall St (2,3) |
| 7,324 | 69.5% | 69.9% | 161 St-Yankee Stadium (4) |
| 6,720 | 82.2% | 83.0% | Chambers St (2,3) |
| 6,420 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,290 | 85.8% | 86.1% | 125 St (2,3) |
| 6,155 | 84.3% | 100.0% | Wall St (4,5) |

</details>

### Top 25 Destination Stations, Summed across All Origins

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 44,614 | 70.2% | 71.0% | Grand Central-42 St (4,5) |
| 35,813 | 63.6% | 64.4% | Times Sq-42 St (2,3) |
| 26,747 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 24,864 | 77.3% | 78.2% | 34 St-Penn Station (2,3) |
| 24,106 | 71.2% | 71.9% | 14 St-Union Sq (4,5) |
| 15,640 | 86.3% | 86.7% | 86 St (4,5) |
| 14,252 | 78.6% | 79.0% | 59 St (4,5) |
| 13,366 | 82.5% | 82.7% | 72 St (2,3) |
| 12,442 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,264 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,515 | 83.4% | 83.6% | 96 St (2,3) |
| 11,267 | 73.9% | 74.5% | Park Pl (2,3) |
| 10,981 | 76.8% | 77.7% | 14 St (2,3) |
| 9,680 | 74.7% | 75.4% | Crown Hts-Utica Av (4,5) |
| 9,646 | 77.3% | 78.0% | Bowling Green (4,5) |
| 9,447 | 79.4% | 80.0% | Brooklyn Bridge-City Hall (4,5) |
| 8,617 | 85.1% | 100.0% | Wall St (2,3) |
| 8,578 | 90.0% | 90.0% | 3 Av-149 St (2,5) |
| 8,098 | 83.3% | 83.6% | 125 St (4,5) |
| 7,786 | 71.4% | 72.9% | Flatbush Av-Brooklyn College (2,3) |
| 7,634 | 73.3% | 73.4% | 161 St-Yankee Stadium (4) |
| 7,274 | 81.4% | 81.8% | Chambers St (2,3) |
| 6,807 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,404 | 76.9% | 100.0% | Wall St (4,5) |
| 6,281 | 83.7% | 84.0% | 125 St (2,3) |

</details>

---

## 4/5 Nostrand

### What Changed, against Current

Every both-ends rider, and their share of the 503,188 of them: **was** is what Current gives them, **now** what 4/5 Nostrand would. Off-diagonal cells are the whole effect of the swap; the diagonal is everyone it leaves alone. `direct` is a one-seat ride, `close` a one-seat ride after a walk of 300m or less, `far` neither.

| Riders | now direct | now close | now far |
| --- | ---: | ---: | ---: |
| **was direct** | 400,585 (79.6%) | 1,710 (0.3%) | 18,601 (3.7%) |
| **was close** | 0 (0.0%) | 4,235 (0.8%) | 1 (0.0%) |
| **was far** | 1,142 (0.2%) | 39 (0.0%) | 76,876 (15.3%) |

- Gained: 1,181 (0.2%)
- Lost: 18,602 (3.7%)
- Net: -17,421 (-3.5%)

### Biggest Changes, against Current

The top 25 station pairs by riders whose outcome moved, both directions combined as above. An end reads `today→4/5 Nostrand` where its routes change, and today's alone where they don't; `Dist` and `Walk` are the walk under 4/5 Nostrand, as in the pairs table below.

| # | Riders | Was | Now | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 1,273 | direct | far | 978m | dest: Times Sq-42 St (2,3) | Crown Hts-Utica Av (4→2,3) ↔ Grand Central-42 St (4,5) |
| 2 | 1,131 | direct | far | 932m | dest: 14 St (2,3) | Crown Hts-Utica Av (4→2,3) ↔ 14 St-Union Sq (4,5) |
| 3 | 855 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Flatbush Av-Brooklyn College (2→4,5) ↔ Times Sq-42 St (2,3) |
| 4 | 732 | direct | far | 474m | dest: Wall St (2,3) | Crown Hts-Utica Av (4→2,3) ↔ Bowling Green (4,5) |
| 5 | 726 | direct | far | 1207m | dest: Grand Central-42 St (4,5) | Flatbush Av-Brooklyn College (2→4,5) ↔ 34 St-Penn Station (2,3) |
| 6 | 527 | direct | far | 1501m | origin: President St-Medgar Evers College (4,5) | Crown Hts-Utica Av (4→2,3) ↔ 59 St (4,5) |
| 7 | 501 | direct | far | 1501m | origin: President St-Medgar Evers College (4,5) | Crown Hts-Utica Av (4→2,3) ↔ 86 St (4,5) |
| 8 | 461 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Church Av (2→4,5) ↔ Times Sq-42 St (2,3) |
| 9 | 434 | direct | far | 1207m | origin: Grand Central-42 St (4,5) | 34 St-Penn Station (2,3) ↔ Church Av (2→4,5) |
| 10 | 423 | direct | far | 394m | dest: Park Pl (2,3) | Crown Hts-Utica Av (4→2,3) ↔ Brooklyn Bridge-City Hall (4,5) |
| 11 | 418 | direct | far | 463m | origin: Nevins St (2,3,4,5) | Hoyt St (2,3) ↔ Flatbush Av-Brooklyn College (2→4,5) |
| 12 | 381 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Newkirk Av-Little Haiti (2→4,5) ↔ Times Sq-42 St (2,3) |
| 13 | 372 | direct | far | 978m | origin: Grand Central-42 St (4,5) | Times Sq-42 St (2,3) ↔ Winthrop St (2→4,5) |
| 14 | 326 | direct | far | 1207m | origin: Grand Central-42 St (4,5) | 34 St-Penn Station (2,3) ↔ Winthrop St (2→4,5) |
| 15 | 317 | direct | far | 1207m | dest: Grand Central-42 St (4,5) | Newkirk Av-Little Haiti (2→4,5) ↔ 34 St-Penn Station (2,3) |
| 16 | 306 | direct | far | 463m | origin: Nevins St (2,3,4,5) | Hoyt St (2,3) ↔ Church Av (2→4,5) |
| 17 | 293 | direct | far | 777m | origin: 125 St (2,3) | 125 St (4,5) ↔ Crown Hts-Utica Av (4→2,3) |
| 18 | 288 | direct | close | 247m | dest: Wall St (2,3) | Crown Hts-Utica Av (4→2,3) ↔ Wall St (4,5) |
| 19 | 269 | direct | far | 304m | dest: Fulton St (2,3,4,5) | Flatbush Av-Brooklyn College (2→4,5) ↔ Park Pl (2,3) |
| 20 | 264 | direct | far | 791m | origin: Nostrand Av (3) | Sterling St (2→4,5) ↔ Times Sq-42 St (2,3) |
| 21 | 259 | direct | far | 791m | dest: Nostrand Av (3) | 34 St-Penn Station (2,3) ↔ Sterling St (2→4,5) |
| 22 | 255 | direct | far | 932m | dest: 14 St-Union Sq (4,5) | Flatbush Av-Brooklyn College (2→4,5) ↔ 14 St (2,3) |
| 23 | 254 | direct | far | 463m | origin: Nevins St (2,3,4,5) | Hoyt St (2,3) ↔ Winthrop St (2→4,5) |
| 24 | 244 | direct | far | 509m | dest: Brooklyn Bridge-City Hall (4,5) | Flatbush Av-Brooklyn College (2→4,5) ↔ Chambers St (2,3) |
| 25 | 244 | direct | far | 978m | dest: Grand Central-42 St (4,5) | Beverly Rd (2→4,5) ↔ Times Sq-42 St (2,3) |

### Biggest Changes by Station, against Current

The same changed pairs as above, added up at the stations they run between: the top 25 by `Net`, which is riders gaining an effective one-seat ride here less those losing one, taken either way round. A station whose riders only move between `direct` and `close` keeps them all effective and nets nothing, however many moved. A pair is a change at both of its ends and counts at each, so `Riders` runs to twice what the matrix counts.

| # | Riders | Net | direct→close | direct→far | close→direct | close→far | far→direct | far→close | Station |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 6,359 | -5,320 | 288 | 5,696 | | | 376 | | Crown Hts-Utica Av (4→2,3) |
| 2 | 4,791 | -4,016 | 217 | 4,295 | | | 279 | | Flatbush Av-Brooklyn College (2→4,5) |
| 3 | 2,721 | -2,576 | 146 | 2,576 | | | | | Times Sq-42 St (2,3) |
| 4 | 2,400 | -2,268 | 132 | 2,268 | | | | | 34 St-Penn Station (2,3) |
| 5 | 2,590 | -2,241 | 98 | 2,367 | | | 125 | | Church Av (2→4,5) |
| 6 | 2,240 | -1,883 | 111 | 2,006 | | | 123 | | Winthrop St (2→4,5) |
| 7 | 1,825 | -1,609 | 61 | 1,687 | | | 78 | | Newkirk Av-Little Haiti (2→4,5) |
| 8 | 1,683 | -1,567 | 116 | 1,567 | | | | | Hoyt St (2,3) |
| 9 | 1,569 | -1,369 | 72 | 1,433 | | | 64 | | Sterling St (2→4,5) |
| 10 | 1,273 | -1,273 | | 1,273 | | | | | Grand Central-42 St (4,5) |
| 11 | 1,131 | -1,131 | | 1,131 | | | | | 14 St-Union Sq (4,5) |
| 12 | 1,227 | -1,051 | 46 | 1,116 | | | 65 | | Beverly Rd (2→4,5) |
| 13 | 966 | -904 | 62 | 904 | | | | | 14 St (2,3) |
| 14 | 892 | -823 | 69 | 823 | | | | | Grand Army Plaza (2,3) |
| 15 | 732 | -732 | | 732 | | | | | Bowling Green (4,5) |
| 16 | 754 | -719 | 35 | 719 | | | | | Park Pl (2,3) |
| 17 | 695 | -653 | 42 | 653 | | | | | Chambers St (2,3) |
| 18 | 673 | -639 | 34 | 639 | | | | | 72 St (2,3) |
| 19 | 527 | -527 | | 527 | | | | | 59 St (4,5) |
| 20 | 501 | -501 | | 501 | | | | | 86 St (4,5) |
| 21 | 511 | -470 | 40 | 470 | | | | | Bergen St (2,3) |
| 22 | 493 | -469 | 24 | 469 | | | | | 96 St (2,3) |
| 23 | 423 | -423 | | 423 | | | | | Brooklyn Bridge-City Hall (4,5) |
| 24 | 428 | -403 | 25 | 403 | | | | | Clark St (2,3) |
| 25 | 387 | -365 | 22 | 365 | | | | | Eastern Pkwy-Brooklyn Museum (2,3) |

### Top 25 Origin/Destination Pairs

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above. Each row is both directions of one station pair, their riders summed, oriented so the arrow points the way more of them travel. Every column but the riders is symmetric, so one value covers both directions; `Walk` names the station the shorter walk reaches, and the end it is at.

| # | Riders | % Total | Type | Close? | Dist | Walk | Origin ↔ Destination |
| ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 12,244 | 2.43% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Fulton St (2,3,4,5) |
| 2 | 8,657 | 1.72% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | Times Sq-42 St (2,3) ↔ Grand Central-42 St (4,5) |
| 3 | 8,056 | 1.60% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 14 St-Union Sq (4,5) |
| 4 | 5,828 | 1.16% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Park Pl (2,3) |
| 5 | 5,566 | 1.11% | 1-seat | | | | 86 St (4,5) ↔ Grand Central-42 St (4,5) |
| 6 | 5,414 | 1.08% | xfer | far | 932m | dest: 14 St (2,3) | Times Sq-42 St (2,3) ↔ 14 St-Union Sq (4,5) |
| 7 | 5,329 | 1.06% | 1-seat | | | | Times Sq-42 St (2,3) ↔ Fulton St (2,3,4,5) |
| 8 | 5,082 | 1.01% | 1-seat | | | | Grand Central-42 St (4,5) ↔ Brooklyn Bridge-City Hall (4,5) |
| 9 | 5,067 | 1.01% | xfer | far | 978m | dest: Times Sq-42 St (2,3) | 34 St-Penn Station (2,3) ↔ Grand Central-42 St (4,5) |
| 10 | 4,228 | 0.84% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Wall St (2,3) |
| 11 | 3,855 | 0.77% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 72 St (2,3) |
| 12 | 3,852 | 0.77% | 1-seat | | | | Bowling Green (4,5) ↔ Grand Central-42 St (4,5) |
| 13 | 3,836 | 0.76% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 72 St (2,3) |
| 14 | 3,721 | 0.74% | 1-seat | | | | Grand Central-42 St (4,5) ↔ 59 St (4,5) |
| 15 | 3,612 | 0.72% | 1-seat | | | | Wall St (4,5) ↔ Grand Central-42 St (4,5) |
| 16 | 3,477 | 0.69% | 1-seat | | | | Times Sq-42 St (2,3) ↔ 96 St (2,3) |
| 17 | 3,304 | 0.66% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ 96 St (2,3) |
| 18 | 3,272 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Chambers St (2,3) |
| 19 | 3,255 | 0.65% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Fulton St (2,3,4,5) |
| 20 | 2,978 | 0.59% | 1-seat | | | | 34 St-Penn Station (2,3) ↔ Times Sq-42 St (2,3) |
| 21 | 2,800 | 0.56% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 14 St-Union Sq (4,5) |
| 22 | 2,755 | 0.55% | xfer | far | 978m | origin: Grand Central-42 St (4,5) | Times Sq-42 St (2,3) ↔ 59 St (4,5) |
| 23 | 2,716 | 0.54% | 1-seat | | | | Wall St (2,3) ↔ Times Sq-42 St (2,3) |
| 24 | 2,423 | 0.48% | 1-seat | | | | Borough Hall (2,3,4,5) ↔ Grand Central-42 St (4,5) |
| 25 | 2,412 | 0.48% | 1-seat | | | | Fulton St (2,3,4,5) ↔ 86 St (4,5) |

</details>

### Top 25 Origin Stations, Summed across All Destinations

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Origin |
| ---: | ---: | ---: | --- |
| 44,713 | 69.1% | 70.3% | Grand Central-42 St (4,5) |
| 37,629 | 61.7% | 62.8% | Times Sq-42 St (2,3) |
| 27,189 | 76.7% | 78.1% | 34 St-Penn Station (2,3) |
| 25,334 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 22,248 | 69.8% | 71.0% | 14 St-Union Sq (4,5) |
| 15,323 | 85.0% | 85.6% | 86 St (4,5) |
| 14,083 | 76.7% | 77.6% | 59 St (4,5) |
| 12,679 | 79.8% | 80.3% | 72 St (2,3) |
| 12,205 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,176 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,289 | 81.6% | 81.9% | 96 St (2,3) |
| 10,239 | 63.9% | 65.8% | Crown Hts-Utica Av (2,3) |
| 10,228 | 75.4% | 76.7% | 14 St (2,3) |
| 9,794 | 77.1% | 77.8% | Park Pl (2,3) |
| 9,295 | 81.0% | 81.8% | Bowling Green (4,5) |
| 8,867 | 82.7% | 83.4% | Brooklyn Bridge-City Hall (4,5) |
| 8,824 | 90.5% | 90.5% | 3 Av-149 St (2,5) |
| 8,468 | 86.6% | 87.0% | 125 St (4,5) |
| 8,127 | 65.9% | 67.7% | Flatbush Av-Brooklyn College (4,5) |
| 7,880 | 89.2% | 100.0% | Wall St (2,3) |
| 7,324 | 69.6% | 70.1% | 161 St-Yankee Stadium (4) |
| 6,720 | 80.8% | 81.7% | Chambers St (2,3) |
| 6,420 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,290 | 85.8% | 86.1% | 125 St (2,3) |
| 6,155 | 85.5% | 100.0% | Wall St (4,5) |

</details>

### Top 25 Destination Stations, Summed across All Origins

<details>
<summary>Show 25 rows</summary>

Both ends on the comparison's routes, per that section of the comparison above.

| Riders | 1-Seat % | Effective % | Destination |
| ---: | ---: | ---: | --- |
| 44,614 | 70.3% | 71.1% | Grand Central-42 St (4,5) |
| 35,813 | 63.0% | 63.8% | Times Sq-42 St (2,3) |
| 26,747 | 100.0% | 100.0% | Fulton St (2,3,4,5) |
| 24,864 | 76.2% | 77.1% | 34 St-Penn Station (2,3) |
| 24,106 | 71.3% | 71.9% | 14 St-Union Sq (4,5) |
| 15,640 | 85.7% | 86.0% | 86 St (4,5) |
| 14,252 | 78.4% | 78.8% | 59 St (4,5) |
| 13,366 | 82.2% | 82.5% | 72 St (2,3) |
| 12,442 | 100.0% | 100.0% | Borough Hall (2,3,4,5) |
| 12,264 | 100.0% | 100.0% | Atlantic Av (2,3,4,5) |
| 11,515 | 83.3% | 83.5% | 96 St (2,3) |
| 11,267 | 73.0% | 73.6% | Park Pl (2,3) |
| 10,981 | 75.3% | 76.1% | 14 St (2,3) |
| 9,680 | 65.3% | 66.9% | Crown Hts-Utica Av (2,3) |
| 9,646 | 76.9% | 77.5% | Bowling Green (4,5) |
| 9,447 | 79.5% | 80.0% | Brooklyn Bridge-City Hall (4,5) |
| 8,617 | 84.0% | 100.0% | Wall St (2,3) |
| 8,578 | 89.1% | 89.2% | 3 Av-149 St (2,5) |
| 8,098 | 82.6% | 82.9% | 125 St (4,5) |
| 7,786 | 65.7% | 67.2% | Flatbush Av-Brooklyn College (4,5) |
| 7,634 | 73.4% | 73.6% | 161 St-Yankee Stadium (4) |
| 7,274 | 80.0% | 80.5% | Chambers St (2,3) |
| 6,807 | 100.0% | 100.0% | Franklin Av-Medgar Evers College (2,3,4,5) |
| 6,404 | 78.2% | 100.0% | Wall St (4,5) |
| 6,281 | 83.9% | 84.2% | 125 St (2,3) |

</details>
