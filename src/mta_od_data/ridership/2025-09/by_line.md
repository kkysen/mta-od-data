# Ridership by line

Average weekday riders with fare evaders, over 22 weekdays from 2025-09-16 to 2025-09-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Sep 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --month 2025-09 --markdown-out src/mta_od_data/ridership/2025-09/by_line.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Sep 2025 | 2019 | Peak Hour | Riders in Peak Hour, Sep 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 981,451 | 1,310,593 | 5:00 PM | 108,623 |
| 8 Av | 865,768 | 1,164,821 | 5:00 PM | 92,392 |
| Broadway-7 Av | 836,998 | 1,129,825 | 5:00 PM | 97,818 |
| Broadway | 792,461 | 1,034,286 | 5:00 PM | 82,627 |
| 6 Av | 776,150 | 1,016,447 | 5:00 PM | 87,585 |
| Queens Blvd | 528,151 | 672,614 | 5:00 PM | 56,614 |
| Flushing | 515,082 | 590,342 | 5:00 PM | 57,286 |
| Lexington Av express | 514,332 | 692,196 | 5:00 PM | 51,321 |
| Lexington Av local | 508,314 | 664,330 | 8:00 AM | 48,860 |
| 8 Av local | 461,858 | 598,213 | 5:00 PM | 43,866 |
| Queens Blvd west | 454,616 | 585,218 | 5:00 PM | 44,887 |
| Broadway-7 Av local | 399,645 | 528,834 | 5:00 PM | 38,979 |
| Canarsie | 398,975 | 450,793 | 5:00 PM | 37,856 |
| Broadway local | 397,202 | 520,906 | 5:00 PM | 38,511 |
| Broadway-7 Av express | 384,578 | 530,037 | 5:00 PM | 39,133 |
| 8 Av express | 365,451 | 508,223 | 5:00 PM | 38,030 |
| 6 Av local | 343,391 | 447,875 | 5:00 PM | 36,429 |
| Broadway express | 340,077 | 438,004 | 5:00 PM | 36,078 |
| 53 St | 336,565 | 439,565 | 5:00 PM | 34,305 |
| Eastern Pkwy | 308,934 | 413,188 | 8:00 AM | 35,192 |
| 63 St | 304,129 | 392,674 | 5:00 PM | 31,266 |
| Manhattan Bridge | 301,639 | 384,366 | 5:00 PM | 29,777 |
| Queens Blvd express | 300,953 | 381,659 | 5:00 PM | 30,135 |
| Queens Blvd local | 292,413 | 390,231 | 7:00 AM | 24,661 |
| Queens Blvd west express | 291,420 | 369,110 | 5:00 PM | 29,111 |
| 4 Av | 286,650 | 348,667 | 8:00 AM | 30,523 |
| Fulton St | 267,467 | 365,676 | 5:00 PM | 25,663 |
| 6 Av express | 263,479 | 353,959 | 5:00 PM | 28,494 |
| Brighton | 237,295 | 316,941 | 8:00 AM | 24,262 |
| Flushing local | 237,014 | 262,691 | 7:00 AM | 17,320 |
| Queens Blvd west local | 199,451 | 264,724 | 8:00 AM | 16,390 |
| Jamaica | 197,613 | 265,815 | 8:00 AM | 19,092 |
| Queens Blvd east | 193,103 | 253,663 | 7:00 AM | 17,254 |
| White Plains Rd | 172,989 | 258,115 | 7:00 AM | 19,778 |
| Jerome Av | 167,809 | 237,899 | 7:00 AM | 13,811 |
| Culver | 164,082 | 206,863 | 8:00 AM | 16,909 |
| SAS Phase 1 | 154,664 | 200,723 | 8:00 AM | 16,414 |
| Culver local | 154,245 | 194,989 | 8:00 AM | 16,041 |
| Eastern Pkwy express | 152,651 | 204,894 | 8:00 AM | 15,214 |
| 4 Av express | 151,114 | 182,504 | 8:00 AM | 15,143 |
| Eastern Pkwy local | 149,468 | 199,079 | 8:00 AM | 13,661 |
| Upper Culver | 148,302 | 186,538 | 8:00 AM | 15,351 |
| Upper Culver local | 146,005 | 183,449 | 8:00 AM | 15,351 |
| Fulton St express | 143,508 | 203,978 | 5:00 PM | 14,364 |
| Crosstown | 140,883 | 163,343 | 5:00 PM | 12,946 |
| 4 Av local | 136,937 | 167,882 | 8:00 AM | 11,657 |
| Lenox Av | 132,598 | 194,917 | 8:00 AM | 11,978 |
| Pelham | 132,255 | 192,126 | 7:00 AM | 14,577 |
| Concourse | 120,069 | 188,757 | 7:00 AM | 10,670 |
| Jamaica local | 118,971 | 159,601 | 8:00 AM | 11,754 |
| Brighton local | 115,906 | 153,083 | 8:00 AM | 10,500 |
| Concourse local | 113,524 | 177,598 | 7:00 AM | 9,032 |
| White Plains Rd local | 113,116 | 167,864 | 3:00 PM | 10,202 |
| Astoria | 104,899 | 122,659 | 8:00 AM | 10,780 |
| Fulton St local | 98,789 | 131,032 | 5:00 PM | 7,597 |
| Nostrand Av | 86,753 | 111,669 | 8:00 AM | 8,398 |
| West End | 85,320 | 111,384 | 7:00 AM | 8,642 |
| Pelham local | 84,128 | 120,483 | 7:00 AM | 7,303 |
| Sea Beach | 82,740 | 90,828 | 7:00 AM | 7,894 |
| Brighton express | 70,718 | 98,036 | 8:00 AM | 7,711 |
| Nassau St | 66,468 | 92,434 | 5:00 PM | 6,322 |
| Hillside Av | 60,434 | 84,031 | 7:00 AM | 5,969 |
| 42 St Shuttle | 58,850 | 79,025 | 5:00 PM | 6,853 |
| Hillside Av local | 58,342 | 80,998 | 5:00 PM | 5,030 |
| Myrtle Av | 50,185 | 63,090 | 8:00 AM | 4,531 |
| Lower Culver | 42,354 | 57,493 | 7:00 AM | 4,511 |
| Flushing express | 39,903 | 45,323 | 5:00 PM | 6,923 |
| Lower Culver local | 39,180 | 53,395 | 7:00 AM | 4,220 |
| Pelham express | 37,172 | 55,888 | 7:00 AM | 5,577 |
| Rockaway | 29,331 | 52,320 | 5:00 PM | 2,801 |
| Jamaica express | 28,666 | 39,243 | 8:00 AM | 4,460 |
| Dyre Av | 26,911 | 40,735 | 7:00 AM | 3,101 |
| White Plains Rd express | 22,339 | 33,215 | 7:00 AM | 5,088 |
| Far Rockaway branch | 17,237 | 35,445 | 7:00 AM | 1,692 |
| Lefferts branch | 17,210 | 26,170 | 7:00 AM | 1,832 |
| Concourse express | 15,553 | 26,094 | 8:00 AM | 3,357 |
| Franklin Av Shuttle | 14,882 | 19,816 | 8:00 AM | 1,304 |
| Rockaway Park branch | 3,712 | 7,336 | 5:00 PM | 337 |
| Culver express | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Upper Culver express | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Hillside Av express | 2,316 | 3,333 | 7:00 AM | 975 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
