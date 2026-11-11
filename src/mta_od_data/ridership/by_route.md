# Ridership by route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by route --markdown-out src/mta_od_data/ridership/by_route.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Aug-Dec 2025 | 2019 | Route-km | Per Route-km, Aug-Dec 2025 | Trips | Train-km | Per Train-km, Aug-Dec 2025 | Per Car\*-km, Aug-Dec 2025 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 6 | 560,614 | 745,868 | 24.1 | 23,266 | 552 | 12,495 | 44.9 | 5.28 | 5:00 PM | 53,514 |
| 6L | 424,953 | 562,006 | 24.1 | 17,636 | 439 | 9,772 | 43.5 | 5.12 | 5:00 PM | 36,476 |
| 6X | 141,782 | 192,500 | 24.1 | 5,884 | 113 | 2,723 | 52.1 | 6.13 | 5:00 PM | 17,037 |
| F | 512,692 | 655,612 | 44.8 | 11,434 | 392 | 16,278 | 31.5 | 3.15 | 5:00 PM | 51,392 |
| FL | 506,431 | 647,439 | 44.8 | 11,294 | 388 | 16,104 | 31.4 | 3.14 | 5:00 PM | 48,508 |
| FX | 6,518 | 8,516 | 42.4 | 154 | 4 | 174 | 37.4 | 3.74 | 5:00 PM | 2,883 |
| 1 | 511,652 | 678,410 | 23.5 | 21,757 | 462 | 10,750 | 47.6 | 5.60 | 5:00 PM | 50,348 |
| 7 | 500,585 | 576,118 | 16.0 | 31,303 | 642 | 10,307 | 48.6 | 5.19 | 5:00 PM | 48,096 |
| 7L | 406,867 | 468,977 | 16.0 | 25,443 | 535 | 8,598 | 47.3 | 5.06 | 5:00 PM | 32,978 |
| 7X | 97,562 | 111,773 | 16.0 | 6,104 | 107 | 1,709 | 57.1 | 6.11 | 5:00 PM | 15,117 |
| A | 438,394 | 605,158 | 53.5 | 8,199 | 377 | 15,662 | 28.0 | 2.80 | 5:00 PM | 45,210 |
| 4 | 407,137 | 562,311 | 25.1 | 16,191 | 370 | 12,098 | 33.7 | 3.96 | 5:00 PM | 35,743 |
| E | 384,454 | 491,670 | 25.4 | 15,140 | 410 | 10,252 | 37.5 | 3.75 | 5:00 PM | 39,084 |
| L | 376,186 | 424,383 | 16.3 | 23,087 | 549 | 8,809 | 42.7 | 5.34 | 5:00 PM | 35,461 |
| R | 372,007 | 488,425 | 34.8 | 10,702 | 303 | 9,453 | 39.4 | 3.94 | 5:00 PM | 38,681 |
| 2 | 344,533 | 485,342 | 32.1 | 10,749 | 324 | 13,264 | 26.0 | 3.06 | 8:00 AM | 31,509 |
| Q | 337,522 | 444,405 | 28.1 | 12,016 | 315 | 8,839 | 38.2 | 3.82 | 5:00 PM | 31,952 |
| D | 294,659 | 406,805 | 40.5 | 7,272 | 296 | 12,154 | 24.2 | 2.42 | 5:00 PM | 24,816 |
| N | 290,021 | 348,396 | 34.4 | 8,442 | 285 | 9,328 | 31.1 | 3.11 | 5:00 PM | 27,320 |
| 5 | 286,603 | 391,691 | 38.8 | 7,393 | 329 | 10,481 | 27.3 | 3.22 | 5:00 PM | 30,047 |
| B | 237,837 | 320,672 | 37.9 | 6,271 | 220 | 7,628 | 31.2 | 3.12 | 5:00 PM | 26,947 |
| M | 236,819 | 313,177 | 29.1 | 8,128 | 293 | 7,017 | 33.7 | 4.22 | 8:00 AM | 22,954 |
| C | 231,891 | 300,555 | 29.9 | 7,752 | 222 | 6,636 | 34.9 | 3.49 | 5:00 PM | 18,745 |
| 3 | 230,561 | 320,720 | 29.2 | 7,890 | 294 | 7,782 | 29.6 | 3.49 | 8:00 AM | 23,453 |
| J | 152,057 | 205,950 | 21.4 | 7,105 | 285 | 6,025 | 25.2 | 3.15 | 4:00 PM | 12,400 |
| W | 152,023 | 196,802 | 15.6 | 9,741 | 187 | 2,997 | 50.7 | 5.07 | 5:00 PM | 15,150 |
| G | 149,674 | 175,069 | 16.5 | 9,059 | 298 | 5,037 | 29.7 | 5.94 | 5:00 PM | 13,639 |
| GS | 63,814 | 85,619 | 0.7 | 91,427 | 508 | 355 | 180.0 | 35.29 | 5:00 PM | 7,614 |
| FS | 13,030 | 17,391 | 2.2 | 5,965 | 238 | 520 | 25.1 | 10.02 | 8:00 AM | 1,111 |
| Z | 10,123 | 13,731 | 21.4 | 473 | 12 | 257 | 39.4 | 4.93 | 5:00 PM | 3,965 |
| H | 2,771 | 5,419 | 4.5 | 610 | 168 | 763 | 3.6 | 0.73 | 4:00 PM | 242 |

\* A car is 60 ft of train, about one B Division car's length, so routes with different train lengths compare (`train_lengths.json5`).

</details>

## Charts

### Riders by route

<details>
<summary>The chart</summary>

![Riders by route](by_route-riders.svg)

</details>

### Riders per route-km

<details>
<summary>The chart</summary>

![Riders per route-km](by_route-per-route-km.svg)

</details>

### Riders per train-km

<details>
<summary>The chart</summary>

![Riders per train-km](by_route-per-train-km.svg)

</details>

### Riders per car\*-km

<details>
<summary>The chart</summary>

![Riders per car\*-km](by_route-per-car-km.svg)

</details>
