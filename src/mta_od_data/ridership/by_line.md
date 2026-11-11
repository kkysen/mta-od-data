# Ridership by line

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --markdown-out src/mta_od_data/ridership/by_line.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 941,794 | 1,258,794 | 5:00 PM | 102,724 |
| 8 Av | 845,992 | 1,137,187 | 5:00 PM | 88,989 |
| Broadway-7 Av | 810,636 | 1,095,904 | 5:00 PM | 93,417 |
| 6 Av | 761,024 | 998,618 | 5:00 PM | 84,553 |
| Broadway | 744,750 | 976,429 | 5:00 PM | 77,073 |
| Queens Blvd | 505,399 | 645,081 | 5:00 PM | 54,105 |
| Lexington Av local | 494,143 | 646,617 | 5:00 PM | 46,649 |
| Flushing | 486,930 | 559,421 | 5:00 PM | 53,041 |
| Lexington Av express | 484,142 | 652,518 | 5:00 PM | 47,574 |
| 8 Av local | 447,325 | 578,815 | 5:00 PM | 42,607 |
| Queens Blvd west | 446,777 | 574,602 | 5:00 PM | 44,707 |
| Broadway-7 Av local | 393,113 | 521,582 | 5:00 PM | 37,547 |
| Broadway local | 386,223 | 508,397 | 5:00 PM | 37,559 |
| Canarsie | 370,379 | 417,108 | 5:00 PM | 34,864 |
| Broadway-7 Av express | 366,413 | 505,495 | 5:00 PM | 37,224 |
| 8 Av express | 364,329 | 505,429 | 5:00 PM | 36,814 |
| 53 St | 348,874 | 456,538 | 5:00 PM | 35,635 |
| 6 Av local | 339,764 | 443,693 | 5:00 PM | 35,822 |
| Broadway express | 301,962 | 391,613 | 5:00 PM | 31,635 |
| Queens Blvd express | 299,779 | 379,950 | 5:00 PM | 29,965 |
| Eastern Pkwy | 293,588 | 392,881 | 8:00 AM | 32,089 |
| Queens Blvd west express | 290,293 | 367,499 | 5:00 PM | 28,931 |
| Manhattan Bridge | 286,321 | 365,738 | 5:00 PM | 28,079 |
| Queens Blvd local | 283,742 | 378,632 | 8:00 AM | 23,487 |
| 4 Av | 278,279 | 338,818 | 8:00 AM | 28,771 |
| 63 St | 270,347 | 350,070 | 5:00 PM | 27,472 |
| Fulton St | 251,386 | 344,092 | 5:00 PM | 24,207 |
| 6 Av express | 249,713 | 336,829 | 5:00 PM | 26,128 |
| Brighton | 221,489 | 296,619 | 8:00 AM | 22,155 |
| Flushing local | 220,297 | 245,609 | 4:00 PM | 16,253 |
| Queens Blvd west local | 196,268 | 260,418 | 5:00 PM | 15,775 |
| Jamaica | 190,559 | 256,755 | 8:00 AM | 18,050 |
| Queens Blvd east | 184,814 | 243,096 | 5:00 PM | 16,372 |
| White Plains Rd | 164,076 | 245,075 | 7:00 AM | 17,764 |
| Jerome Av | 156,404 | 222,698 | 4:00 PM | 12,837 |
| Culver | 155,797 | 196,510 | 8:00 AM | 15,677 |
| SAS Phase 1 | 149,827 | 194,889 | 5:00 PM | 15,304 |
| Culver local | 147,030 | 185,949 | 8:00 AM | 14,905 |
| Eastern Pkwy express | 146,759 | 196,952 | 8:00 AM | 13,925 |
| 4 Av express | 145,221 | 175,620 | 5:00 PM | 14,130 |
| Eastern Pkwy local | 142,825 | 190,704 | 8:00 AM | 12,737 |
| Upper Culver | 141,454 | 178,009 | 8:00 AM | 14,239 |
| Upper Culver local | 139,365 | 175,198 | 8:00 AM | 14,239 |
| Fulton St express | 137,042 | 194,797 | 5:00 PM | 13,692 |
| 4 Av local | 134,774 | 165,365 | 5:00 PM | 11,268 |
| Crosstown | 133,593 | 154,895 | 5:00 PM | 12,356 |
| Lenox Av | 128,275 | 188,797 | 8:00 AM | 11,273 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,401 |
| Jamaica local | 115,564 | 155,225 | 8:00 AM | 11,180 |
| Concourse | 113,440 | 179,380 | 4:00 PM | 9,834 |
| Brighton local | 108,026 | 143,085 | 8:00 AM | 9,747 |
| White Plains Rd local | 107,393 | 159,566 | 3:00 PM | 9,486 |
| Concourse local | 107,132 | 168,624 | 3:00 PM | 8,364 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,008 |
| Fulton St local | 92,007 | 122,274 | 5:00 PM | 7,016 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,853 |
| West End | 81,961 | 107,087 | 7:00 AM | 7,858 |
| Pelham local | 80,733 | 115,755 | 7:00 AM | 6,540 |
| Sea Beach | 79,087 | 86,905 | 5:00 PM | 7,330 |
| Brighton express | 66,533 | 92,532 | 8:00 AM | 7,131 |
| Nassau St | 62,829 | 87,422 | 5:00 PM | 5,991 |
| 42 St Shuttle | 62,778 | 84,192 | 5:00 PM | 7,501 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,526 |
| Hillside Av local | 55,643 | 77,327 | 5:00 PM | 4,806 |
| Myrtle Av | 48,614 | 61,128 | 8:00 AM | 4,278 |
| Lower Culver | 39,759 | 54,063 | 7:00 AM | 4,134 |
| Lower Culver local | 36,934 | 50,409 | 7:00 AM | 3,873 |
| Pelham express | 36,198 | 54,405 | 7:00 AM | 5,307 |
| Flushing express | 35,035 | 40,248 | 5:00 PM | 5,833 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,582 |
| Jamaica express | 27,465 | 37,678 | 8:00 AM | 4,166 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,769 |
| White Plains Rd express | 20,564 | 30,561 | 7:00 AM | 4,597 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,570 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,670 |
| Concourse express | 14,594 | 24,534 | 7:00 AM | 3,193 |
| Franklin Av Shuttle | 13,901 | 18,531 | 8:00 AM | 1,245 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 297 |
| Culver express | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Upper Culver express | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Hillside Av express | 2,204 | 3,171 | 7:00 AM | 931 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
