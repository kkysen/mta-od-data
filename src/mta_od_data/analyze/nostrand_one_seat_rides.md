# One Seat Ride Analysis for Deinterlining 7 Av/West Side/Lexington Av/East Side at Franklin Av-Medgar Evers College/Botanic Garden (2,3,4,5)

Scenario: average weekday ridership (60 distinct days in the data, 2025-01 to 2025-12) on trains originating at stations served by 2,3,4,5, south of Franklin Av-Medgar Evers College/Botanic Garden (2,3,4,5), with destinations north of it (i.e. trips that cross the junction).

Produced by `mta-od-data analyze one-seat-rides --boundary-complex-id 626 --origin-side south --dest-side north --routes 2,3,4,5 --primary-routes 2,3,4,5 --trunk-a 2,3 --trunk-a-label '7 Av/West Side' --trunk-b 4,5 --trunk-b-label 'Lexington Av/East Side' --origin-corridor-a-routes 2,5 --origin-corridor-a-label 'Nostrand Av Line' --origin-corridor-b-routes 3,4 --origin-corridor-b-label 'Eastern Pkwy/New Lots Line' --all-corridor-scenarios --csv-out data/nostrand_weekday_pairs.csv --markdown-out src/mta_od_data/analyze/nostrand_one_seat_rides.md`.

---

## Scenario comparison

Average weekday ridership is the same 66,992/weekday across every scenario below; only how many of those riders get a one-seat ride changes.

| Scenario | Total Riders | Direct 1-Seat | Close 1-Seat | Effective 1-Seat |
| --- | --- | --- | --- | --- |
| 2,5 on Nostrand Av Line, 3,4 on Eastern Pkwy/New Lots Line | 66,992 | 36,532 (54.5%) | 4,023 (13.2%) | 40,555 (60.5%) |
| 2,3 on Nostrand Av Line, 4,5 on Eastern Pkwy/New Lots Line | 66,992 | 28,332 (42.3%) | 3,648 (9.4%) | 31,980 (47.7%) |
| 4,5 on Nostrand Av Line, 2,3 on Eastern Pkwy/New Lots Line | 66,992 | 27,108 (40.5%) | 3,718 (9.3%) | 30,826 (46.0%) |

---

## 2,5 on Nostrand Av Line, 3,4 on Eastern Pkwy/New Lots Line

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 896 | 1.34% | 2.45% | 1-seat | close | 0m | Crown Hts-Utica Av (3,4) → Atlantic Av (3,4) |  |
| 2 | 753 | 1.12% | 2.06% | 1-seat | close | 0m | Crown Hts-Utica Av (3,4) → Borough Hall/Court St (3,4) |  |
| 3 | 680 | 1.02% | 1.86% | 1-seat | close | 0m | Crown Hts-Utica Av (4) → Grand Central-42 St (4) |  |
| 4 | 655 | 0.98% | 1.79% | 1-seat | close | 0m | Crown Hts-Utica Av (3,4) → Fulton St (3,4) |  |
| 5 | 595 | 0.89% | 1.63% | 1-seat | close | 0m | Crown Hts-Utica Av (4) → 14 St-Union Sq (4) |  |
| 6 | 562 | 0.84% | 1.54% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,5) → Borough Hall/Court St (2,5) |  |
| 7 | 546 | 0.81% | 1.49% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,5) → Atlantic Av (2,5) |  |
| 8 | 531 | 0.79% | 1.45% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,5) → Fulton St (2,5) |  |
| 9 | 479 | 0.72% | 1.31% | 1-seat | close | 0m | Crown Hts-Utica Av (3,4) → Franklin Av-Medgar Evers College/Botanic Garden (3,4) |  |
| 10 | 454 | 0.68% | 1.24% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (5) → Grand Central-42 St (5) |  |
| 11 | 448 | 0.67% | 1.23% | 1-seat | close | 0m | Crown Hts-Utica Av (3,4) → Nevins St (3,4) |  |
| 12 | 436 | 0.65% | 1.19% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2) → Times Sq-42 St/PABT (2) |  |
| 13 | 406 | 0.61% | 1.11% | 1-seat | close | 0m | Crown Hts-Utica Av (3) → Times Sq-42 St/PABT (3) |  |
| 14 | 387 | 0.58% | 1.06% | 1-seat | close | 0m | Crown Hts-Utica Av (4) → Bowling Green (4) |  |
| 15 | 364 | 0.54% | 1.00% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2) → 34 St-Penn Station (2) |  |
| 16 | 317 | 0.47% | 0.87% | 1-seat | close | 0m | Church Av (2,5) → Atlantic Av (2,5) |  |
| 17 | 313 | 0.47% | 0.86% | 1-seat | close | 0m | Crown Hts-Utica Av (3) → 34 St-Penn Station (3) |  |
| 18 | 308 | 0.46% | 0.84% | 1-seat | close | 0m | Winthrop St (2,5) → Atlantic Av (2,5) |  |
| 19 | 290 | 0.43% | 0.79% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (5) → 14 St-Union Sq (5) |  |
| 20 | 283 | 0.42% | 0.77% | 1-seat | close | 0m | Crown Hts-Utica Av (4) → Lexington Av/59 St (4) |  |
| 21 | 276 | 0.41% | 0.75% | 1-seat | close | 0m | Church Av (2,5) → Borough Hall/Court St (2,5) |  |
| 22 | 267 | 0.40% | 0.73% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (5) → Bowling Green (5) |  |
| 23 | 266 | 0.40% | 0.73% | 1-seat | close | 0m | Crown Hts-Utica Av (4) → 86 St (4) |  |
| 24 | 251 | 0.38% | 0.69% | 1-seat | close | 0m | Winthrop St (2,5) → Fulton St (2,5) |  |
| 25 | 250 | 0.37% | 0.69% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,5) → Franklin Av-Medgar Evers College/Botanic Garden (2,5) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 36,532/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 3,928 | 100.0% | 10.75% |  |  | Atlantic Av (2,3,4,5) |
| 3,319 | 100.0% | 9.09% |  |  | Borough Hall/Court St (2,3,4,5) |
| 2,926 | 100.0% | 8.01% |  |  | Fulton St (2,3,4,5) |
| 2,527 | 100.0% | 6.92% |  |  | Times Sq-42 St/PABT (2,3) |
| 2,096 | 100.0% | 5.74% |  |  | 34 St-Penn Station (2,3) |
| 2,655 | 77.2% | 5.61% | 0% | 754m | Grand Central-42 St (4,5) |
| 1,817 | 100.0% | 4.97% |  |  | Franklin Av-Medgar Evers College/Botanic Garden (2,3,4,5) |
| 1,800 | 100.0% | 4.93% |  |  | Nevins St (2,3,4,5) |
| 2,120 | 79.2% | 4.59% | 0% | 844m | 14 St-Union Sq (4,5) |
| 1,579 | 100.0% | 4.32% |  |  | Hoyt St (2,3) |
| 1,491 | 74.9% | 3.05% | 0% | 474m | Bowling Green (4,5) |
| 969 | 100.0% | 2.65% |  |  | Grand Army Plaza (2,3) |
| 822 | 100.0% | 2.25% |  |  | 14 St/6 Av (2,3) |
| 1,011 | 76.7% | 2.12% | 0% | 1831m | Lexington Av/59 St (4,5) |
| 769 | 100.0% | 2.11% |  |  | Chambers St/WTC/Park Pl/Cortlandt St (2,3) |
| 909 | 76.1% | 1.89% | 0% | 394m | Brooklyn Bridge-City Hall/Chambers St (4,5) |
| 669 | 100.0% | 1.83% |  |  | 72 St (2,3) |
| 877 | 74.9% | 1.80% | 0% | 2135m | 86 St (4,5) |
| 643 | 100.0% | 1.76% |  |  | Chambers St (2,3) |
| 598 | 100.0% | 1.64% |  |  | Wall St (2,3) |
| 635 | 80.5% | 1.40% | 100% | 247m | Wall St (4,5) |
| 495 | 100.0% | 1.36% |  |  | 96 St (2,3) |
| 480 | 100.0% | 1.31% |  |  | Bergen St (2,3) |
| 449 | 100.0% | 1.23% |  |  | Eastern Pkwy-Brooklyn Museum (2,3) |
| 523 | 72.4% | 1.04% | 0% | 777m | 125 St (4,5) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/nostrand_weekday_pairs_actual.csv`._

---

## 2,3 on Nostrand Av Line, 4,5 on Eastern Pkwy/New Lots Line

Deinterlining scenario: Nostrand Av Line served by 2,3; Eastern Pkwy/New Lots Line served by 4,5 (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 896 | 1.34% | 3.16% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Atlantic Av (4,5) |  |
| 2 | 753 | 1.12% | 2.66% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Borough Hall/Court St (4,5) |  |
| 3 | 680 | 1.02% | 2.40% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Grand Central-42 St (4,5) |  |
| 4 | 655 | 0.98% | 2.31% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Fulton St (4,5) |  |
| 5 | 595 | 0.89% | 2.10% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → 14 St-Union Sq (4,5) |  |
| 6 | 562 | 0.84% | 1.98% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → Borough Hall/Court St (2,3) |  |
| 7 | 546 | 0.81% | 1.93% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → Atlantic Av (2,3) |  |
| 8 | 531 | 0.79% | 1.87% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → Fulton St (2,3) |  |
| 9 | 479 | 0.72% | 1.69% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Franklin Av-Medgar Evers College/Botanic Garden (4,5) |  |
| 10 | 454 | 0.68% |  | xfer | far | 754m | Flatbush Av-Brooklyn College (2,3) → Grand Central-42 St (4,5) | Times Sq-42 St (2,3) |
| 11 | 448 | 0.67% | 1.58% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Nevins St (4,5) |  |
| 12 | 436 | 0.65% | 1.54% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → Times Sq-42 St/PABT (2,3) |  |
| 13 | 406 | 0.61% |  | xfer | far | 894m | Crown Hts-Utica Av (4,5) → Times Sq-42 St/PABT (2,3) | Grand Central-42 St (4,5) |
| 14 | 387 | 0.58% | 1.37% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Bowling Green (4,5) |  |
| 15 | 364 | 0.54% | 1.28% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → 34 St-Penn Station (2,3) |  |
| 16 | 317 | 0.47% | 1.12% | 1-seat | close | 0m | Church Av (2,3) → Atlantic Av (2,3) |  |
| 17 | 313 | 0.47% |  | xfer | far | 1207m | Crown Hts-Utica Av (4,5) → 34 St-Penn Station (2,3) | Grand Central-42 St (4,5) |
| 18 | 308 | 0.46% | 1.09% | 1-seat | close | 0m | Winthrop St (2,3) → Atlantic Av (2,3) |  |
| 19 | 290 | 0.43% |  | xfer | far | 844m | Flatbush Av-Brooklyn College (2,3) → 14 St-Union Sq (4,5) | 14 St (2,3) |
| 20 | 283 | 0.42% | 1.00% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → Lexington Av/59 St (4,5) |  |
| 21 | 276 | 0.41% | 0.97% | 1-seat | close | 0m | Church Av (2,3) → Borough Hall/Court St (2,3) |  |
| 22 | 267 | 0.40% |  | xfer | far | 474m | Flatbush Av-Brooklyn College (2,3) → Bowling Green (4,5) | Wall St (2,3) |
| 23 | 266 | 0.40% | 0.94% | 1-seat | close | 0m | Crown Hts-Utica Av (4,5) → 86 St (4,5) |  |
| 24 | 251 | 0.38% | 0.89% | 1-seat | close | 0m | Winthrop St (2,3) → Fulton St (2,3) |  |
| 25 | 250 | 0.37% | 0.88% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (2,3) → Franklin Av-Medgar Evers College/Botanic Garden (2,3) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 28,332/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 3,928 | 100.0% | 13.87% |  |  | Atlantic Av (2,3,4,5) |
| 3,319 | 100.0% | 11.72% |  |  | Borough Hall/Court St (2,3,4,5) |
| 2,926 | 100.0% | 10.33% |  |  | Fulton St (2,3,4,5) |
| 1,817 | 100.0% | 6.41% |  |  | Franklin Av-Medgar Evers College/Botanic Garden (2,3,4,5) |
| 1,800 | 100.0% | 6.35% |  |  | Nevins St (2,3,4,5) |
| 2,527 | 54.3% | 4.85% | 0% | 894m | Times Sq-42 St/PABT (2,3) |
| 2,655 | 48.4% | 4.54% | 0% | 754m | Grand Central-42 St (4,5) |
| 2,096 | 56.6% | 4.19% | 0% | 1207m | 34 St-Penn Station (2,3) |
| 2,120 | 48.9% | 3.66% | 0% | 844m | 14 St-Union Sq (4,5) |
| 1,579 | 49.4% | 2.75% | 0% | 463m | Hoyt St (2,3) |
| 1,491 | 51.1% | 2.69% | 0% | 474m | Bowling Green (4,5) |
| 1,011 | 51.3% | 1.83% | 0% | 1831m | Lexington Av/59 St (4,5) |
| 822 | 60.5% | 1.75% | 0% | 648m | 14 St/6 Av (2,3) |
| 877 | 55.4% | 1.72% | 0% | 2135m | 86 St (4,5) |
| 909 | 49.1% | 1.58% | 0% | 394m | Brooklyn Bridge-City Hall/Chambers St (4,5) |
| 969 | 45.2% | 1.55% | 0% | 1158m | Grand Army Plaza (2,3) |
| 769 | 56.2% | 1.53% | 100% | 132m | Chambers St/WTC/Park Pl/Cortlandt St (2,3) |
| 643 | 57.9% | 1.31% | 0% | 509m | Chambers St (2,3) |
| 669 | 52.1% | 1.23% | 0% | 2128m | 72 St (2,3) |
| 598 | 57.6% | 1.22% | 100% | 247m | Wall St (2,3) |
| 523 | 55.5% | 1.03% | 0% | 777m | 125 St (4,5) |
| 635 | 43.6% | 0.98% | 100% | 247m | Wall St (4,5) |
| 265 | 100.0% | 0.93% |  |  | 3 Av-149 St (2,5) |
| 495 | 51.4% | 0.90% | 0% | 2135m | 96 St (2,3) |
| 480 | 50.3% | 0.85% | 0% | 448m | Bergen St (2,3) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/nostrand_weekday_pairs_a.csv`._

---

## 4,5 on Nostrand Av Line, 2,3 on Eastern Pkwy/New Lots Line

Deinterlining scenario: Nostrand Av Line served by 4,5; Eastern Pkwy/New Lots Line served by 2,3 (each origin's one-seat eligibility swaps in these assigned primary routes in place of its real current primary routes; any non-primary route it already has (e.g. R, which never crosses the junction) is unaffected, and a station touching both corridors keeps access to both).

### Top 25 origin/destination pairs

| # | Riders | % Total | % 1-Seat | Type | Close? | Dist | Origin → Destination | 1-Seat Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 896 | 1.34% | 3.30% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Atlantic Av (2,3) |  |
| 2 | 753 | 1.12% | 2.78% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Borough Hall/Court St (2,3) |  |
| 3 | 680 | 1.02% |  | xfer | far | 754m | Crown Hts-Utica Av (2,3) → Grand Central-42 St (4,5) | Times Sq-42 St (2,3) |
| 4 | 655 | 0.98% | 2.42% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Fulton St (2,3) |  |
| 5 | 595 | 0.89% |  | xfer | far | 844m | Crown Hts-Utica Av (2,3) → 14 St-Union Sq (4,5) | 14 St (2,3) |
| 6 | 562 | 0.84% | 2.07% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Borough Hall/Court St (4,5) |  |
| 7 | 546 | 0.81% | 2.01% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Atlantic Av (4,5) |  |
| 8 | 531 | 0.79% | 1.96% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Fulton St (4,5) |  |
| 9 | 479 | 0.72% | 1.77% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Franklin Av-Medgar Evers College/Botanic Garden (2,3) |  |
| 10 | 454 | 0.68% | 1.67% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Grand Central-42 St (4,5) |  |
| 11 | 448 | 0.67% | 1.65% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Nevins St (2,3) |  |
| 12 | 436 | 0.65% |  | xfer | far | 894m | Flatbush Av-Brooklyn College (4,5) → Times Sq-42 St/PABT (2,3) | Grand Central-42 St (4,5) |
| 13 | 406 | 0.61% | 1.50% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → Times Sq-42 St/PABT (2,3) |  |
| 14 | 387 | 0.58% |  | xfer | far | 474m | Crown Hts-Utica Av (2,3) → Bowling Green (4,5) | Wall St (2,3) |
| 15 | 364 | 0.54% |  | xfer | far | 1207m | Flatbush Av-Brooklyn College (4,5) → 34 St-Penn Station (2,3) | Grand Central-42 St (4,5) |
| 16 | 317 | 0.47% | 1.17% | 1-seat | close | 0m | Church Av (4,5) → Atlantic Av (4,5) |  |
| 17 | 313 | 0.47% | 1.16% | 1-seat | close | 0m | Crown Hts-Utica Av (2,3) → 34 St-Penn Station (2,3) |  |
| 18 | 308 | 0.46% | 1.14% | 1-seat | close | 0m | Winthrop St (4,5) → Atlantic Av (4,5) |  |
| 19 | 290 | 0.43% | 1.07% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → 14 St-Union Sq (4,5) |  |
| 20 | 283 | 0.42% |  | xfer | far | 1831m | Crown Hts-Utica Av (2,3) → Lexington Av/59 St (4,5) | Times Sq-42 St (2,3) |
| 21 | 276 | 0.41% | 1.02% | 1-seat | close | 0m | Church Av (4,5) → Borough Hall/Court St (4,5) |  |
| 22 | 267 | 0.40% | 0.98% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Bowling Green (4,5) |  |
| 23 | 266 | 0.40% |  | xfer | far | 2135m | Crown Hts-Utica Av (2,3) → 86 St (4,5) | 96 St (2,3) |
| 24 | 251 | 0.38% | 0.93% | 1-seat | close | 0m | Winthrop St (4,5) → Fulton St (4,5) |  |
| 25 | 250 | 0.37% | 0.92% | 1-seat | close | 0m | Flatbush Av-Brooklyn College (4,5) → Franklin Av-Medgar Evers College/Botanic Garden (4,5) |  |

### Top 25 destination stations, summed across all origins

Sorted by each destination's one-seat ridership (i.e. its share of the 27,108/weekday one-seat total).

| Riders | 1-Seat % | % All 1-Seat | Close? | Dist | Destination |
| --- | --- | --- | --- | --- | --- |
| 3,928 | 100.0% | 14.49% |  |  | Atlantic Av (2,3,4,5) |
| 3,319 | 100.0% | 12.24% |  |  | Borough Hall/Court St (2,3,4,5) |
| 2,926 | 100.0% | 10.79% |  |  | Fulton St (2,3,4,5) |
| 1,817 | 100.0% | 6.70% |  |  | Franklin Av-Medgar Evers College/Botanic Garden (2,3,4,5) |
| 1,800 | 100.0% | 6.64% |  |  | Nevins St (2,3,4,5) |
| 2,655 | 51.6% | 5.05% | 0% | 754m | Grand Central-42 St (4,5) |
| 2,527 | 45.7% | 4.26% | 0% | 894m | Times Sq-42 St/PABT (2,3) |
| 2,120 | 51.1% | 4.00% | 0% | 844m | 14 St-Union Sq (4,5) |
| 2,096 | 43.4% | 3.35% | 0% | 1207m | 34 St-Penn Station (2,3) |
| 1,579 | 50.6% | 2.95% | 0% | 463m | Hoyt St (2,3) |
| 1,491 | 48.9% | 2.69% | 0% | 474m | Bowling Green (4,5) |
| 969 | 54.8% | 1.96% | 0% | 1158m | Grand Army Plaza (2,3) |
| 1,011 | 48.7% | 1.82% | 0% | 1831m | Lexington Av/59 St (4,5) |
| 909 | 50.9% | 1.71% | 0% | 394m | Brooklyn Bridge-City Hall/Chambers St (4,5) |
| 877 | 44.6% | 1.44% | 0% | 2135m | 86 St (4,5) |
| 635 | 56.4% | 1.32% | 100% | 247m | Wall St (4,5) |
| 769 | 43.8% | 1.24% | 100% | 132m | Chambers St/WTC/Park Pl/Cortlandt St (2,3) |
| 822 | 39.5% | 1.20% | 0% | 648m | 14 St/6 Av (2,3) |
| 669 | 47.9% | 1.18% | 0% | 2128m | 72 St (2,3) |
| 643 | 42.1% | 1.00% | 0% | 509m | Chambers St (2,3) |
| 265 | 100.0% | 0.98% |  |  | 3 Av-149 St (2,5) |
| 598 | 42.4% | 0.94% | 100% | 247m | Wall St (2,3) |
| 449 | 55.6% | 0.92% | 0% | 546m | Eastern Pkwy-Brooklyn Museum (2,3) |
| 495 | 48.6% | 0.89% | 0% | 2135m | 96 St (2,3) |
| 480 | 49.7% | 0.88% | 0% | 448m | Bergen St (2,3) |

_Full row-level detail (every origin/destination pair, not just the top 25): `data/nostrand_weekday_pairs_b.csv`._

---

## Notes on reading these tables

- "Close?"/"Dist" describe distance from the destination to the nearest station on the origin's own effective corridor (real routes in baseline, the scenario's assigned routes otherwise), thresholded at 300m, for `xfer` rows, i.e. riders without a direct one-seat ride. A close `xfer` row is a *close one-seat ride*: no train change, just a short walk to the actual destination. `1-seat` rows are always `close`/`0m`: the destination is a Complex ID in the source data, not a specific platform, so there's no way to tell which platform a rider actually used; the effective route already stops somewhere in that same complex, the rider's real historical destination either way.
- In the per-pair table (and CSV), "1-Seat Destination" names the specific station `dist_m` was measured to for a `xfer` row: the nearest station on the origin's own effective corridor, i.e. what the destination would have had to be for this row to be a `1-seat` ride instead. Empty for `1-seat` rows (already true of the actual destination) and omitted from the per-destination table (an average across many pairs, not a single station).
- In the per-destination table, "Close?"/"Dist" are ridership-weighted across that destination's classified `xfer` pairs.
