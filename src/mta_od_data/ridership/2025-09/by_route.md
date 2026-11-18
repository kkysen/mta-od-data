# Ridership by route

Average weekday riders with fare evaders, over 22 weekdays from 2025-09-16 to 2025-09-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Sep 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by route --month 2025-09 --markdown-out src/mta_od_data/ridership/2025-09/by_route.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Sep 2025 | 2019 | Route-km | Per Route-km, Sep 2025 | Trips | Train-km | Per Train-km, Sep 2025 | Per Car\*-km, Sep 2025 | Peak Hour | Riders in Peak Hour, Sep 2025 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 6 | 572,655 | 761,483 | 24.1 | 23,765 | 552 | 12,495 | 45.8 | 5.39 | 8:00 AM | 55,563 |
| 6L | 433,267 | 572,706 | 24.1 | 17,981 | 439 | 9,772 | 44.3 | 5.22 | 8:00 AM | 38,200 |
| 6X | 147,252 | 199,882 | 24.1 | 6,111 | 113 | 2,723 | 54.1 | 6.36 | 5:00 PM | 17,444 |
| F | 535,883 | 682,022 | 42.5 | 12,599 | 392 | 16,125 | 33.2 | 3.32 | 5:00 PM | 53,995 |
| FL | 528,875 | 672,930 | 42.5 | 12,434 | 388 | 15,951 | 33.2 | 3.32 | 5:00 PM | 50,764 |
| FX | 7,313 | 9,500 | 42.2 | 173 | 4 | 174 | 41.9 | 4.19 | 5:00 PM | 3,231 |
| 1 | 527,991 | 698,379 | 23.5 | 22,452 | 462 | 10,750 | 49.1 | 5.78 | 5:00 PM | 53,668 |
| 7 | 524,369 | 601,543 | 15.8 | 33,120 | 642 | 10,243 | 51.2 | 5.48 | 5:00 PM | 51,515 |
| 7L | 425,356 | 488,477 | 15.8 | 26,866 | 535 | 8,552 | 49.7 | 5.32 | 5:00 PM | 34,179 |
| 7X | 104,461 | 119,581 | 15.8 | 6,602 | 107 | 1,691 | 61.8 | 6.61 | 5:00 PM | 17,337 |
| A | 447,803 | 619,924 | 53.5 | 8,375 | 375 | 15,585 | 28.7 | 2.87 | 5:00 PM | 46,826 |
| 4 | 437,008 | 601,558 | 25.1 | 17,379 | 370 | 12,097 | 36.1 | 4.25 | 5:00 PM | 39,092 |
| E | 426,658 | 544,456 | 25.4 | 16,802 | 410 | 10,252 | 41.6 | 4.16 | 5:00 PM | 42,982 |
| L | 398,975 | 450,793 | 16.3 | 24,486 | 546 | 8,760 | 45.5 | 5.69 | 5:00 PM | 37,856 |
| R | 388,001 | 508,082 | 34.8 | 11,163 | 303 | 9,449 | 41.1 | 4.11 | 5:00 PM | 40,182 |
| Q | 381,794 | 499,158 | 27.9 | 13,691 | 315 | 8,772 | 43.5 | 4.35 | 5:00 PM | 37,213 |
| 2 | 374,878 | 525,828 | 32.1 | 11,696 | 324 | 13,264 | 28.3 | 3.33 | 5:00 PM | 35,140 |
| 5 | 316,736 | 433,790 | 38.8 | 8,170 | 329 | 10,471 | 30.2 | 3.56 | 8:00 AM | 34,035 |
| D | 314,376 | 433,058 | 40.3 | 7,806 | 296 | 12,133 | 25.9 | 2.59 | 8:00 AM | 28,402 |
| N | 303,924 | 364,196 | 34.4 | 8,847 | 285 | 9,327 | 32.6 | 3.26 | 5:00 PM | 28,290 |
| B | 263,560 | 353,976 | 37.6 | 7,002 | 220 | 7,566 | 34.8 | 3.48 | 5:00 PM | 31,053 |
| C | 261,740 | 339,722 | 29.9 | 8,751 | 222 | 6,635 | 39.5 | 3.95 | 8:00 AM | 21,863 |
| 3 | 258,093 | 356,904 | 29.2 | 8,832 | 294 | 7,776 | 33.2 | 3.90 | 8:00 AM | 27,948 |
| M | 242,460 | 322,759 | 29.0 | 8,358 | 292 | 6,952 | 34.9 | 4.36 | 8:00 AM | 24,126 |
| J | 161,898 | 219,265 | 21.4 | 7,565 | 285 | 6,025 | 26.9 | 3.36 | 4:00 PM | 12,754 |
| G | 160,456 | 187,958 | 16.4 | 9,777 | 298 | 5,037 | 31.9 | 6.37 | 5:00 PM | 14,675 |
| W | 154,961 | 199,800 | 15.6 | 9,929 | 187 | 2,996 | 51.7 | 5.17 | 5:00 PM | 15,487 |
| GS | 58,850 | 79,025 | 0.7 | 84,315 | 508 | 355 | 166.0 | 32.54 | 5:00 PM | 6,853 |
| FS | 14,882 | 19,816 | 2.2 | 6,812 | 238 | 520 | 28.6 | 11.45 | 8:00 AM | 1,304 |
| Z | 11,100 | 15,089 | 21.4 | 519 | 12 | 257 | 43.2 | 5.40 | 5:00 PM | 4,428 |
| H | 3,263 | 6,446 | 4.5 | 719 | 168 | 763 | 4.3 | 0.86 | 4:00 PM | 285 |

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
