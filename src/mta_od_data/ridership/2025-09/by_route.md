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
| 6 | 572,164 | 760,883 | 24.1 | 23,745 | 552 | 12,495 | 45.8 | 5.39 | 8:00 AM | 55,482 |
| 6L | 432,859 | 572,211 | 24.1 | 17,964 | 439 | 9,772 | 44.3 | 5.21 | 8:00 AM | 38,108 |
| 6X | 147,160 | 199,765 | 24.1 | 6,107 | 113 | 2,723 | 54.0 | 6.36 | 5:00 PM | 17,433 |
| F | 535,394 | 681,363 | 42.5 | 12,588 | 392 | 16,125 | 33.2 | 3.32 | 5:00 PM | 53,889 |
| FL | 528,423 | 672,322 | 42.5 | 12,424 | 388 | 15,951 | 33.1 | 3.31 | 5:00 PM | 50,689 |
| FX | 7,275 | 9,448 | 42.2 | 173 | 4 | 174 | 41.7 | 4.17 | 5:00 PM | 3,200 |
| 1 | 528,107 | 698,561 | 23.5 | 22,457 | 462 | 10,750 | 49.1 | 5.78 | 5:00 PM | 53,692 |
| 7 | 524,175 | 601,291 | 15.8 | 33,108 | 642 | 10,243 | 51.2 | 5.47 | 5:00 PM | 51,485 |
| 7L | 425,188 | 488,257 | 15.8 | 26,856 | 535 | 8,552 | 49.7 | 5.32 | 5:00 PM | 34,151 |
| 7X | 104,438 | 119,552 | 15.8 | 6,601 | 107 | 1,691 | 61.8 | 6.61 | 5:00 PM | 17,334 |
| A | 447,886 | 620,058 | 53.5 | 8,376 | 375 | 15,585 | 28.7 | 2.87 | 5:00 PM | 47,016 |
| 4 | 438,465 | 603,414 | 25.1 | 17,437 | 370 | 12,097 | 36.2 | 4.26 | 5:00 PM | 39,490 |
| E | 426,464 | 544,190 | 25.4 | 16,794 | 410 | 10,252 | 41.6 | 4.16 | 5:00 PM | 42,969 |
| L | 399,052 | 450,913 | 16.3 | 24,491 | 546 | 8,760 | 45.6 | 5.69 | 5:00 PM | 37,807 |
| R | 387,484 | 507,434 | 34.8 | 11,148 | 303 | 9,449 | 41.0 | 4.10 | 5:00 PM | 40,079 |
| Q | 382,055 | 499,448 | 27.9 | 13,701 | 315 | 8,772 | 43.6 | 4.36 | 5:00 PM | 37,164 |
| 2 | 374,362 | 525,259 | 32.1 | 11,680 | 324 | 13,264 | 28.2 | 3.32 | 5:00 PM | 35,283 |
| 5 | 317,097 | 434,274 | 38.8 | 8,179 | 329 | 10,471 | 30.3 | 3.56 | 8:00 AM | 34,061 |
| D | 315,207 | 434,127 | 40.3 | 7,827 | 296 | 12,133 | 26.0 | 2.60 | 8:00 AM | 28,508 |
| N | 304,335 | 364,788 | 34.4 | 8,859 | 285 | 9,327 | 32.6 | 3.26 | 5:00 PM | 28,309 |
| B | 263,746 | 354,127 | 37.6 | 7,007 | 220 | 7,566 | 34.9 | 3.49 | 5:00 PM | 31,070 |
| C | 261,604 | 339,579 | 29.9 | 8,746 | 222 | 6,635 | 39.4 | 3.94 | 8:00 AM | 21,869 |
| 3 | 258,248 | 357,139 | 29.2 | 8,837 | 294 | 7,776 | 33.2 | 3.91 | 8:00 AM | 27,839 |
| M | 242,390 | 322,677 | 29.0 | 8,356 | 292 | 6,952 | 34.9 | 4.36 | 8:00 AM | 24,136 |
| J | 161,861 | 219,189 | 21.4 | 7,563 | 285 | 6,025 | 26.9 | 3.36 | 4:00 PM | 12,732 |
| G | 160,462 | 187,981 | 16.4 | 9,777 | 298 | 5,037 | 31.9 | 6.37 | 5:00 PM | 14,698 |
| W | 154,838 | 199,621 | 15.6 | 9,921 | 187 | 2,996 | 51.7 | 5.17 | 5:00 PM | 15,463 |
| GS | 58,714 | 78,842 | 0.7 | 84,121 | 508 | 355 | 165.6 | 32.47 | 5:00 PM | 6,828 |
| FS | 14,667 | 19,538 | 2.2 | 6,714 | 238 | 520 | 28.2 | 11.28 | 8:00 AM | 1,281 |
| Z | 11,159 | 15,169 | 21.4 | 521 | 12 | 257 | 43.5 | 5.43 | 5:00 PM | 4,416 |
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
