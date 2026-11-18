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
| 6 | 551,449 | 733,761 | 24.1 | 22,885 | 552 | 12,495 | 44.1 | 5.19 | 5:00 PM | 52,670 |
| 6L | 418,226 | 553,179 | 24.1 | 17,356 | 439 | 9,772 | 42.8 | 5.04 | 5:00 PM | 35,888 |
| 6X | 141,394 | 192,105 | 24.1 | 5,868 | 113 | 2,723 | 51.9 | 6.11 | 5:00 PM | 16,782 |
| F | 519,345 | 664,211 | 44.8 | 11,582 | 392 | 16,278 | 31.9 | 3.19 | 5:00 PM | 51,750 |
| FL | 512,900 | 655,795 | 44.8 | 11,438 | 388 | 16,104 | 31.8 | 3.18 | 5:00 PM | 48,858 |
| FX | 6,686 | 8,737 | 42.4 | 158 | 4 | 174 | 38.4 | 3.84 | 5:00 PM | 2,892 |
| 1 | 518,591 | 687,464 | 23.5 | 22,052 | 462 | 10,750 | 48.2 | 5.68 | 5:00 PM | 52,207 |
| 7 | 497,180 | 572,106 | 16.0 | 31,090 | 642 | 10,307 | 48.2 | 5.16 | 5:00 PM | 48,913 |
| 7L | 405,081 | 466,678 | 16.0 | 25,331 | 535 | 8,598 | 47.1 | 5.04 | 5:00 PM | 33,050 |
| 7X | 97,129 | 111,437 | 16.0 | 6,077 | 107 | 1,709 | 56.8 | 6.08 | 5:00 PM | 15,863 |
| A | 434,386 | 601,292 | 53.5 | 8,124 | 377 | 15,662 | 27.7 | 2.77 | 5:00 PM | 44,322 |
| 4 | 413,980 | 570,591 | 25.1 | 16,463 | 370 | 12,098 | 34.2 | 4.03 | 5:00 PM | 36,891 |
| E | 407,464 | 521,501 | 25.4 | 16,046 | 410 | 10,252 | 39.7 | 3.97 | 5:00 PM | 40,882 |
| R | 382,400 | 501,474 | 34.8 | 11,001 | 303 | 9,453 | 40.5 | 4.05 | 5:00 PM | 39,935 |
| L | 381,254 | 431,152 | 16.3 | 23,398 | 549 | 8,809 | 43.3 | 5.41 | 5:00 PM | 35,918 |
| Q | 367,888 | 482,022 | 28.1 | 13,097 | 315 | 8,839 | 41.6 | 4.16 | 5:00 PM | 35,708 |
| 2 | 359,807 | 505,247 | 32.1 | 11,226 | 324 | 13,264 | 27.1 | 3.19 | 5:00 PM | 33,716 |
| D | 309,005 | 426,174 | 40.5 | 7,626 | 296 | 12,154 | 25.4 | 2.54 | 5:00 PM | 26,456 |
| 5 | 300,703 | 412,136 | 38.8 | 7,756 | 329 | 10,481 | 28.7 | 3.38 | 5:00 PM | 31,181 |
| N | 297,679 | 357,839 | 34.4 | 8,665 | 285 | 9,328 | 31.9 | 3.19 | 5:00 PM | 27,670 |
| B | 254,361 | 341,704 | 37.9 | 6,706 | 220 | 7,628 | 33.3 | 3.33 | 5:00 PM | 29,234 |
| 3 | 249,667 | 345,545 | 29.2 | 8,544 | 294 | 7,782 | 32.1 | 3.77 | 8:00 AM | 25,650 |
| M | 244,450 | 323,715 | 29.1 | 8,390 | 293 | 7,017 | 34.8 | 4.35 | 5:00 PM | 23,126 |
| C | 238,786 | 310,078 | 29.9 | 7,983 | 222 | 6,636 | 36.0 | 3.60 | 5:00 PM | 19,885 |
| J | 155,274 | 210,622 | 21.4 | 7,255 | 285 | 6,025 | 25.8 | 3.22 | 4:00 PM | 12,459 |
| W | 154,295 | 199,436 | 15.6 | 9,887 | 187 | 2,997 | 51.5 | 5.15 | 5:00 PM | 15,334 |
| G | 151,458 | 177,653 | 16.5 | 9,167 | 298 | 5,037 | 30.1 | 6.01 | 5:00 PM | 13,947 |
| GS | 58,625 | 78,759 | 0.7 | 83,993 | 508 | 355 | 165.3 | 32.42 | 5:00 PM | 6,679 |
| FS | 13,566 | 18,097 | 2.2 | 6,210 | 238 | 520 | 26.1 | 10.44 | 8:00 AM | 1,197 |
| Z | 10,495 | 14,287 | 21.4 | 490 | 12 | 257 | 40.9 | 5.11 | 5:00 PM | 4,205 |
| H | 2,777 | 5,430 | 4.5 | 612 | 168 | 763 | 3.6 | 0.73 | 4:00 PM | 242 |

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
