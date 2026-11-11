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
| 6 | 554,737 | 738,242 | 24.1 | 23,022 | 552 | 12,495 | 44.4 | 5.22 | 5:00 PM | 53,008 |
| 6L | 420,131 | 555,731 | 24.1 | 17,435 | 439 | 9,772 | 43.0 | 5.06 | 5:00 PM | 36,106 |
| 6X | 142,267 | 193,337 | 24.1 | 5,904 | 113 | 2,723 | 52.2 | 6.15 | 5:00 PM | 16,901 |
| F | 522,858 | 668,713 | 44.8 | 11,660 | 392 | 16,278 | 32.1 | 3.21 | 5:00 PM | 52,200 |
| FL | 516,430 | 660,330 | 44.8 | 11,517 | 388 | 16,104 | 32.1 | 3.21 | 5:00 PM | 49,274 |
| FX | 6,666 | 8,703 | 42.4 | 157 | 4 | 174 | 38.3 | 3.83 | 5:00 PM | 2,927 |
| 1 | 514,785 | 682,754 | 23.5 | 21,890 | 462 | 10,750 | 47.9 | 5.63 | 5:00 PM | 51,321 |
| 7 | 495,958 | 570,334 | 16.0 | 31,014 | 642 | 10,307 | 48.1 | 5.15 | 5:00 PM | 47,681 |
| 7L | 403,808 | 465,154 | 16.0 | 25,251 | 535 | 8,598 | 47.0 | 5.02 | 5:00 PM | 32,750 |
| 7X | 95,962 | 109,876 | 16.0 | 6,004 | 107 | 1,709 | 56.2 | 6.01 | 5:00 PM | 14,930 |
| A | 442,621 | 610,822 | 53.5 | 8,278 | 377 | 15,662 | 28.3 | 2.83 | 5:00 PM | 45,520 |
| E | 418,711 | 535,988 | 25.4 | 16,489 | 410 | 10,252 | 40.8 | 4.08 | 5:00 PM | 42,158 |
| 4 | 411,064 | 567,251 | 25.1 | 16,347 | 370 | 12,098 | 34.0 | 4.00 | 5:00 PM | 36,181 |
| R | 382,628 | 502,030 | 34.8 | 11,008 | 303 | 9,453 | 40.5 | 4.05 | 5:00 PM | 39,994 |
| L | 370,379 | 417,108 | 16.3 | 22,731 | 549 | 8,809 | 42.0 | 5.26 | 5:00 PM | 34,864 |
| 2 | 357,694 | 502,367 | 32.1 | 11,160 | 324 | 13,264 | 27.0 | 3.17 | 5:00 PM | 33,763 |
| Q | 352,492 | 462,753 | 28.1 | 12,549 | 315 | 8,839 | 39.9 | 3.99 | 5:00 PM | 33,841 |
| D | 305,189 | 421,342 | 40.5 | 7,532 | 296 | 12,154 | 25.1 | 2.51 | 5:00 PM | 25,931 |
| 5 | 301,367 | 412,709 | 38.8 | 7,774 | 329 | 10,481 | 28.8 | 3.38 | 5:00 PM | 31,388 |
| N | 283,774 | 340,599 | 34.4 | 8,261 | 285 | 9,328 | 30.4 | 3.04 | 5:00 PM | 26,356 |
| B | 250,673 | 337,362 | 37.9 | 6,609 | 220 | 7,628 | 32.9 | 3.29 | 5:00 PM | 28,574 |
| 3 | 244,204 | 338,194 | 29.2 | 8,357 | 294 | 7,782 | 31.4 | 3.69 | 8:00 AM | 24,871 |
| M | 244,072 | 322,615 | 29.1 | 8,377 | 293 | 7,017 | 34.8 | 4.35 | 5:00 PM | 23,134 |
| C | 239,544 | 310,483 | 29.9 | 8,008 | 222 | 6,636 | 36.1 | 3.61 | 5:00 PM | 19,762 |
| J | 154,146 | 209,060 | 21.4 | 7,202 | 285 | 6,025 | 25.6 | 3.20 | 4:00 PM | 12,434 |
| W | 150,862 | 195,157 | 15.6 | 9,667 | 187 | 2,997 | 50.3 | 5.03 | 5:00 PM | 14,965 |
| G | 150,213 | 175,730 | 16.5 | 9,092 | 298 | 5,037 | 29.8 | 5.96 | 5:00 PM | 13,783 |
| GS | 62,778 | 84,192 | 0.7 | 89,943 | 508 | 355 | 177.1 | 34.72 | 5:00 PM | 7,501 |
| FS | 13,901 | 18,531 | 2.2 | 6,363 | 238 | 520 | 26.7 | 10.69 | 8:00 AM | 1,245 |
| Z | 10,279 | 13,986 | 21.4 | 480 | 12 | 257 | 40.0 | 5.00 | 5:00 PM | 4,102 |
| H | 2,776 | 5,429 | 4.5 | 611 | 168 | 763 | 3.6 | 0.73 | 4:00 PM | 242 |

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
