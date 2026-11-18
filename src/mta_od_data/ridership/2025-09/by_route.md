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
| 6 | 572,162 | 760,880 | 24.1 | 23,745 | 552 | 12,495 | 45.8 | 5.39 | 8:00 AM | 55,481 |
| 6L | 432,859 | 572,210 | 24.1 | 17,964 | 439 | 9,772 | 44.3 | 5.21 | 8:00 AM | 38,108 |
| 6X | 147,158 | 199,762 | 24.1 | 6,107 | 113 | 2,723 | 54.0 | 6.36 | 5:00 PM | 17,432 |
| F | 535,424 | 681,405 | 42.5 | 12,588 | 392 | 16,125 | 33.2 | 3.32 | 5:00 PM | 53,895 |
| FL | 528,453 | 672,363 | 42.5 | 12,424 | 388 | 15,951 | 33.1 | 3.31 | 5:00 PM | 50,694 |
| FX | 7,276 | 9,449 | 42.2 | 173 | 4 | 174 | 41.7 | 4.17 | 5:00 PM | 3,201 |
| 1 | 527,874 | 698,232 | 23.5 | 22,447 | 462 | 10,750 | 49.1 | 5.78 | 5:00 PM | 53,654 |
| 7 | 524,175 | 601,290 | 15.8 | 33,108 | 642 | 10,243 | 51.2 | 5.47 | 5:00 PM | 51,485 |
| 7L | 425,187 | 488,256 | 15.8 | 26,856 | 535 | 8,552 | 49.7 | 5.32 | 5:00 PM | 34,151 |
| 7X | 104,438 | 119,552 | 15.8 | 6,601 | 107 | 1,691 | 61.8 | 6.61 | 5:00 PM | 17,334 |
| A | 447,935 | 620,122 | 53.5 | 8,377 | 375 | 15,585 | 28.7 | 2.87 | 5:00 PM | 47,017 |
| 4 | 438,464 | 603,414 | 25.1 | 17,437 | 370 | 12,097 | 36.2 | 4.26 | 5:00 PM | 39,492 |
| E | 426,466 | 544,192 | 25.4 | 16,794 | 410 | 10,252 | 41.6 | 4.16 | 5:00 PM | 42,969 |
| L | 399,125 | 451,005 | 16.3 | 24,495 | 546 | 8,760 | 45.6 | 5.70 | 5:00 PM | 37,816 |
| R | 386,793 | 506,557 | 34.8 | 11,128 | 303 | 9,449 | 40.9 | 4.09 | 5:00 PM | 40,002 |
| Q | 382,098 | 499,503 | 27.9 | 13,702 | 315 | 8,772 | 43.6 | 4.36 | 5:00 PM | 37,167 |
| 2 | 374,699 | 525,684 | 32.1 | 11,691 | 324 | 13,264 | 28.3 | 3.32 | 5:00 PM | 35,308 |
| 5 | 317,091 | 434,267 | 38.8 | 8,179 | 329 | 10,471 | 30.3 | 3.56 | 8:00 AM | 34,061 |
| D | 315,222 | 434,144 | 40.3 | 7,827 | 296 | 12,133 | 26.0 | 2.60 | 8:00 AM | 28,511 |
| N | 304,376 | 364,838 | 34.4 | 8,860 | 285 | 9,327 | 32.6 | 3.26 | 5:00 PM | 28,311 |
| B | 263,744 | 354,124 | 37.6 | 7,007 | 220 | 7,566 | 34.9 | 3.49 | 5:00 PM | 31,071 |
| C | 261,636 | 339,623 | 29.9 | 8,747 | 222 | 6,635 | 39.4 | 3.94 | 8:00 AM | 21,871 |
| 3 | 258,543 | 357,512 | 29.2 | 8,847 | 294 | 7,776 | 33.2 | 3.91 | 8:00 AM | 27,864 |
| M | 242,397 | 322,685 | 29.0 | 8,356 | 292 | 6,952 | 34.9 | 4.36 | 8:00 AM | 24,137 |
| J | 161,885 | 219,217 | 21.4 | 7,564 | 285 | 6,025 | 26.9 | 3.36 | 4:00 PM | 12,734 |
| G | 160,465 | 187,983 | 16.4 | 9,777 | 298 | 5,037 | 31.9 | 6.37 | 5:00 PM | 14,699 |
| W | 154,892 | 199,693 | 15.6 | 9,925 | 187 | 2,996 | 51.7 | 5.17 | 5:00 PM | 15,480 |
| GS | 58,713 | 78,840 | 0.7 | 84,119 | 508 | 355 | 165.6 | 32.47 | 5:00 PM | 6,827 |
| FS | 14,667 | 19,538 | 2.2 | 6,714 | 238 | 520 | 28.2 | 11.28 | 8:00 AM | 1,281 |
| Z | 11,161 | 15,170 | 21.4 | 521 | 12 | 257 | 43.5 | 5.43 | 5:00 PM | 4,417 |
| H | 3,264 | 6,448 | 4.5 | 719 | 168 | 763 | 4.3 | 0.86 | 4:00 PM | 285 |

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
