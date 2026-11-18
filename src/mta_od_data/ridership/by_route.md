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
| 6 | 551,950 | 734,374 | 24.1 | 22,906 | 552 | 12,495 | 44.2 | 5.20 | 5:00 PM | 52,719 |
| 6L | 418,651 | 553,695 | 24.1 | 17,374 | 439 | 9,772 | 42.8 | 5.04 | 5:00 PM | 35,926 |
| 6X | 141,480 | 192,214 | 24.1 | 5,871 | 113 | 2,723 | 52.0 | 6.11 | 5:00 PM | 16,794 |
| F | 519,754 | 664,762 | 44.8 | 11,591 | 392 | 16,278 | 31.9 | 3.19 | 5:00 PM | 51,815 |
| FL | 513,282 | 656,310 | 44.8 | 11,447 | 388 | 16,104 | 31.9 | 3.19 | 5:00 PM | 48,904 |
| FX | 6,712 | 8,773 | 42.4 | 158 | 4 | 174 | 38.6 | 3.86 | 5:00 PM | 2,912 |
| 1 | 518,495 | 687,307 | 23.5 | 22,048 | 462 | 10,750 | 48.2 | 5.67 | 5:00 PM | 52,184 |
| 7 | 497,389 | 572,380 | 16.0 | 31,103 | 642 | 10,307 | 48.3 | 5.16 | 5:00 PM | 48,934 |
| 7L | 405,265 | 466,920 | 16.0 | 25,342 | 535 | 8,598 | 47.1 | 5.04 | 5:00 PM | 33,067 |
| 7X | 97,153 | 111,467 | 16.0 | 6,078 | 107 | 1,709 | 56.9 | 6.08 | 5:00 PM | 15,867 |
| A | 434,293 | 601,138 | 53.5 | 8,122 | 377 | 15,662 | 27.7 | 2.77 | 5:00 PM | 44,262 |
| 4 | 412,378 | 568,513 | 25.1 | 16,399 | 370 | 12,098 | 34.1 | 4.01 | 5:00 PM | 36,618 |
| E | 407,659 | 521,770 | 25.4 | 16,054 | 410 | 10,252 | 39.8 | 3.98 | 5:00 PM | 40,891 |
| R | 382,868 | 502,050 | 34.8 | 11,015 | 303 | 9,453 | 40.5 | 4.05 | 5:00 PM | 40,012 |
| L | 381,164 | 431,011 | 16.3 | 23,393 | 549 | 8,809 | 43.3 | 5.41 | 5:00 PM | 35,951 |
| Q | 367,515 | 481,571 | 28.1 | 13,084 | 315 | 8,839 | 41.6 | 4.16 | 5:00 PM | 35,728 |
| 2 | 360,347 | 505,863 | 32.1 | 11,243 | 324 | 13,264 | 27.2 | 3.20 | 5:00 PM | 33,647 |
| D | 308,141 | 425,046 | 40.5 | 7,605 | 296 | 12,154 | 25.4 | 2.54 | 5:00 PM | 26,303 |
| 5 | 300,396 | 411,733 | 38.8 | 7,748 | 329 | 10,481 | 28.7 | 3.37 | 5:00 PM | 31,262 |
| N | 297,249 | 357,226 | 34.4 | 8,653 | 285 | 9,328 | 31.9 | 3.19 | 5:00 PM | 27,642 |
| B | 254,296 | 341,737 | 37.9 | 6,705 | 220 | 7,628 | 33.3 | 3.33 | 5:00 PM | 29,289 |
| 3 | 249,524 | 345,326 | 29.2 | 8,539 | 294 | 7,782 | 32.1 | 3.77 | 8:00 AM | 25,699 |
| M | 244,574 | 323,869 | 29.1 | 8,394 | 293 | 7,017 | 34.9 | 4.36 | 5:00 PM | 23,141 |
| C | 238,898 | 310,191 | 29.9 | 7,986 | 222 | 6,636 | 36.0 | 3.60 | 5:00 PM | 19,883 |
| J | 155,286 | 210,666 | 21.4 | 7,256 | 285 | 6,025 | 25.8 | 3.22 | 4:00 PM | 12,482 |
| W | 154,391 | 199,579 | 15.6 | 9,893 | 187 | 2,997 | 51.5 | 5.15 | 5:00 PM | 15,349 |
| G | 151,471 | 177,656 | 16.5 | 9,168 | 298 | 5,037 | 30.1 | 6.01 | 5:00 PM | 13,936 |
| GS | 58,777 | 78,965 | 0.7 | 84,210 | 508 | 355 | 165.8 | 32.50 | 5:00 PM | 6,699 |
| FS | 13,770 | 18,363 | 2.2 | 6,303 | 238 | 520 | 26.5 | 10.59 | 8:00 AM | 1,218 |
| Z | 10,467 | 14,249 | 21.4 | 489 | 12 | 257 | 40.8 | 5.09 | 5:00 PM | 4,206 |
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
