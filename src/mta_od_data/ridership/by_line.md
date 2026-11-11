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
| Lexington Av | 951,054 | 1,270,915 | 5:00 PM | 103,055 |
| 8 Av | 838,509 | 1,126,830 | 5:00 PM | 89,832 |
| Broadway-7 Av | 814,196 | 1,100,964 | 5:00 PM | 89,084 |
| Broadway | 748,578 | 982,247 | 5:00 PM | 77,345 |
| 6 Av | 738,188 | 967,436 | 5:00 PM | 82,550 |
| Lexington Av local | 515,774 | 676,385 | 5:00 PM | 48,547 |
| Queens Blvd | 497,436 | 635,579 | 5:00 PM | 52,068 |
| Flushing | 492,034 | 565,807 | 5:00 PM | 53,777 |
| Lexington Av express | 468,738 | 631,328 | 5:00 PM | 46,184 |
| 8 Av local | 449,934 | 582,471 | 5:00 PM | 43,027 |
| Queens Blvd west | 438,919 | 565,208 | 5:00 PM | 43,058 |
| Broadway-7 Av local | 434,143 | 575,137 | 5:00 PM | 42,485 |
| Broadway local | 393,306 | 518,002 | 5:00 PM | 38,444 |
| Canarsie | 376,186 | 424,383 | 5:00 PM | 35,461 |
| 8 Av express | 365,707 | 506,753 | 5:00 PM | 37,391 |
| 6 Av local | 359,506 | 468,775 | 5:00 PM | 38,075 |
| Broadway-7 Av express | 348,257 | 483,343 | 5:00 PM | 33,866 |
| 53 St | 332,425 | 435,393 | 5:00 PM | 33,672 |
| Broadway express | 303,482 | 393,917 | 5:00 PM | 31,437 |
| Eastern Pkwy | 298,694 | 399,850 | 8:00 AM | 33,050 |
| Queens Blvd local | 285,103 | 380,482 | 8:00 AM | 23,718 |
| Manhattan Bridge | 284,041 | 362,993 | 5:00 PM | 27,951 |
| Queens Blvd express | 283,279 | 359,690 | 5:00 PM | 28,931 |
| 4 Av | 281,397 | 343,025 | 8:00 AM | 29,247 |
| Queens Blvd west express | 272,972 | 346,169 | 5:00 PM | 27,442 |
| 63 St | 267,574 | 346,740 | 5:00 PM | 25,848 |
| 6 Av express | 249,000 | 334,914 | 5:00 PM | 25,334 |
| Fulton St | 246,195 | 338,046 | 5:00 PM | 23,440 |
| Flushing local | 220,703 | 246,049 | 4:00 PM | 16,378 |
| Brighton | 220,170 | 294,982 | 8:00 AM | 22,285 |
| Queens Blvd west local | 195,731 | 259,673 | 8:00 AM | 15,719 |
| Jamaica | 188,303 | 253,448 | 8:00 AM | 18,001 |
| Queens Blvd east | 183,558 | 241,353 | 5:00 PM | 16,305 |
| White Plains Rd | 162,951 | 243,473 | 7:00 AM | 16,687 |
| Jerome Av | 160,638 | 229,167 | 3:00 PM | 13,212 |
| Culver | 157,271 | 198,073 | 8:00 AM | 15,654 |
| 4 Av express | 149,103 | 180,395 | 8:00 AM | 14,663 |
| Eastern Pkwy express | 149,021 | 199,859 | 8:00 AM | 14,297 |
| Culver local | 148,559 | 187,575 | 8:00 AM | 15,004 |
| Eastern Pkwy local | 146,233 | 195,440 | 8:00 AM | 13,198 |
| Upper Culver | 143,051 | 179,726 | 8:00 AM | 14,340 |
| Upper Culver local | 140,966 | 176,920 | 8:00 AM | 14,340 |
| SAS Phase 1 | 140,286 | 183,076 | 8:00 AM | 14,173 |
| Fulton St express | 136,496 | 194,271 | 5:00 PM | 13,609 |
| 4 Av local | 135,459 | 166,260 | 5:00 PM | 11,316 |
| Crosstown | 133,141 | 154,325 | 5:00 PM | 12,282 |
| Lenox Av | 127,907 | 188,373 | 8:00 AM | 11,092 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,427 |
| Jamaica local | 117,128 | 157,308 | 8:00 AM | 11,303 |
| Concourse | 113,426 | 179,428 | 4:00 PM | 9,964 |
| Brighton local | 109,612 | 145,304 | 8:00 AM | 9,796 |
| White Plains Rd local | 109,510 | 162,872 | 3:00 PM | 9,453 |
| Concourse local | 107,116 | 168,671 | 3:00 PM | 8,416 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,021 |
| Fulton St local | 91,801 | 122,052 | 5:00 PM | 6,912 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,743 |
| West End | 82,024 | 107,163 | 7:00 AM | 7,860 |
| Pelham local | 80,771 | 115,815 | 7:00 AM | 6,465 |
| Sea Beach | 79,259 | 87,130 | 5:00 PM | 7,306 |
| Brighton express | 66,700 | 92,567 | 8:00 AM | 7,225 |
| Nassau St | 64,439 | 89,595 | 5:00 PM | 6,193 |
| 42 St Shuttle | 63,814 | 85,619 | 5:00 PM | 7,614 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,463 |
| Hillside Av local | 55,698 | 77,411 | 5:00 PM | 4,790 |
| Myrtle Av | 49,044 | 61,612 | 8:00 AM | 4,308 |
| Lower Culver | 39,750 | 54,041 | 7:00 AM | 4,110 |
| Lower Culver local | 37,059 | 50,554 | 7:00 AM | 3,872 |
| Pelham express | 36,881 | 55,353 | 7:00 AM | 5,396 |
| Flushing express | 35,231 | 40,447 | 5:00 PM | 5,743 |
| Jamaica express | 28,379 | 38,952 | 8:00 AM | 4,336 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,580 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,766 |
| White Plains Rd express | 18,340 | 27,077 | 7:00 AM | 4,306 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,568 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,672 |
| Concourse express | 15,027 | 25,199 | 7:00 AM | 3,234 |
| Franklin Av Shuttle | 13,030 | 17,391 | 8:00 AM | 1,111 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 295 |
| Culver express | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Upper Culver express | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Hillside Av express | 2,028 | 2,924 | 7:00 AM | 847 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
