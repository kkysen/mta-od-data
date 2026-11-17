# Ridership by route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by route --markdown-out src/mta_od_data/ridership/by_route.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Aug-Dec 2025 | 2019 | Route-km | Per Route-km, Aug-Dec 2025 | Trips | Train-km | Per Train-km, Aug-Dec 2025 | Per Car\*-km, Aug-Dec 2025 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 6 | 551,202 | 733,451 | 24.1 | 22,875 | 552 | 12,495 | 44.1 | 5.19 | 5:00 PM | 52,636 |
| 6L | 418,080 | 552,988 | 24.1 | 17,350 | 439 | 9,772 | 42.8 | 5.03 | 5:00 PM | 35,875 |
| 6X | 141,300 | 191,995 | 24.1 | 5,864 | 113 | 2,723 | 51.9 | 6.11 | 5:00 PM | 16,761 |
| F | 518,923 | 663,778 | 44.8 | 11,573 | 392 | 16,278 | 31.9 | 3.19 | 5:00 PM | 51,676 |
| FL | 512,459 | 655,337 | 44.8 | 11,428 | 388 | 16,104 | 31.8 | 3.18 | 5:00 PM | 48,766 |
| FX | 6,705 | 8,763 | 42.4 | 158 | 4 | 174 | 38.5 | 3.85 | 5:00 PM | 2,910 |
| 1 | 517,384 | 686,005 | 23.5 | 22,001 | 462 | 10,750 | 48.1 | 5.66 | 5:00 PM | 52,078 |
| 7 | 500,819 | 576,837 | 16.0 | 31,318 | 642 | 10,307 | 48.6 | 5.20 | 5:00 PM | 49,196 |
| 7L | 407,929 | 470,442 | 16.0 | 25,509 | 535 | 8,598 | 47.4 | 5.07 | 5:00 PM | 33,258 |
| 7X | 97,916 | 112,399 | 16.0 | 6,126 | 107 | 1,709 | 57.3 | 6.13 | 5:00 PM | 15,938 |
| A | 437,528 | 605,034 | 53.5 | 8,182 | 377 | 15,662 | 27.9 | 2.79 | 5:00 PM | 44,618 |
| 4 | 412,097 | 568,164 | 25.1 | 16,388 | 370 | 12,098 | 34.1 | 4.01 | 5:00 PM | 36,592 |
| E | 407,603 | 521,483 | 25.4 | 16,052 | 410 | 10,252 | 39.8 | 3.98 | 5:00 PM | 41,014 |
| R | 382,928 | 502,206 | 34.8 | 11,017 | 303 | 9,453 | 40.5 | 4.05 | 5:00 PM | 39,983 |
| L | 378,402 | 427,580 | 16.3 | 23,223 | 549 | 8,809 | 43.0 | 5.37 | 5:00 PM | 35,706 |
| Q | 368,248 | 482,592 | 28.1 | 13,110 | 315 | 8,839 | 41.7 | 4.17 | 5:00 PM | 35,816 |
| 2 | 360,270 | 505,792 | 32.1 | 11,240 | 324 | 13,264 | 27.2 | 3.20 | 5:00 PM | 33,679 |
| D | 305,647 | 421,795 | 40.5 | 7,543 | 296 | 12,154 | 25.1 | 2.51 | 5:00 PM | 26,055 |
| 5 | 300,272 | 411,584 | 38.8 | 7,745 | 329 | 10,481 | 28.6 | 3.37 | 5:00 PM | 31,236 |
| N | 298,069 | 358,365 | 34.4 | 8,677 | 285 | 9,328 | 32.0 | 3.20 | 5:00 PM | 27,688 |
| B | 252,139 | 339,001 | 37.9 | 6,648 | 220 | 7,628 | 33.1 | 3.31 | 5:00 PM | 29,058 |
| 3 | 249,257 | 345,012 | 29.2 | 8,529 | 294 | 7,782 | 32.0 | 3.77 | 8:00 AM | 25,683 |
| M | 244,231 | 323,442 | 29.1 | 8,382 | 293 | 7,017 | 34.8 | 4.35 | 5:00 PM | 23,094 |
| C | 240,196 | 311,686 | 29.9 | 8,030 | 222 | 6,636 | 36.2 | 3.62 | 5:00 PM | 19,954 |
| J | 155,150 | 210,488 | 21.4 | 7,249 | 285 | 6,025 | 25.8 | 3.22 | 4:00 PM | 12,469 |
| W | 154,770 | 200,094 | 15.6 | 9,917 | 187 | 2,997 | 51.6 | 5.16 | 5:00 PM | 15,404 |
| G | 151,390 | 177,551 | 16.5 | 9,163 | 298 | 5,037 | 30.1 | 6.01 | 5:00 PM | 13,930 |
| GS | 57,285 | 77,045 | 0.7 | 82,073 | 508 | 355 | 161.6 | 31.68 | 5:00 PM | 6,576 |
| FS | 13,766 | 18,357 | 2.2 | 6,301 | 238 | 520 | 26.5 | 10.59 | 8:00 AM | 1,218 |
| Z | 10,463 | 14,243 | 21.4 | 489 | 12 | 257 | 40.7 | 5.09 | 5:00 PM | 4,201 |
| H | 2,776 | 5,429 | 4.5 | 612 | 168 | 763 | 3.6 | 0.73 | 4:00 PM | 242 |

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
