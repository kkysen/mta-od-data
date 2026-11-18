# Ridership by line

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --markdown-out src/mta_od_data/ridership/by_line.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 937,455 | 1,252,886 | 5:00 PM | 102,593 |
| 8 Av | 831,329 | 1,120,060 | 5:00 PM | 87,221 |
| Broadway-7 Av | 817,594 | 1,105,211 | 5:00 PM | 94,677 |
| Broadway | 781,409 | 1,021,562 | 5:00 PM | 80,956 |
| 6 Av | 769,937 | 1,010,619 | 5:00 PM | 85,691 |
| Queens Blvd | 504,139 | 643,506 | 5:00 PM | 54,018 |
| Lexington Av local | 490,672 | 641,869 | 5:00 PM | 46,242 |
| Flushing | 488,275 | 561,370 | 5:00 PM | 54,222 |
| Lexington Av express | 486,978 | 656,300 | 5:00 PM | 47,972 |
| Queens Blvd west | 444,641 | 572,007 | 5:00 PM | 44,509 |
| 8 Av local | 436,084 | 564,882 | 5:00 PM | 41,540 |
| Broadway local | 400,356 | 525,538 | 5:00 PM | 38,663 |
| Broadway-7 Av local | 395,820 | 524,848 | 5:00 PM | 38,175 |
| Canarsie | 381,323 | 431,239 | 5:00 PM | 35,926 |
| Broadway-7 Av express | 372,563 | 513,964 | 5:00 PM | 37,628 |
| 8 Av express | 357,059 | 497,282 | 5:00 PM | 35,667 |
| 53 St | 343,537 | 449,484 | 5:00 PM | 34,905 |
| 6 Av local | 341,295 | 446,508 | 5:00 PM | 35,652 |
| Broadway express | 332,110 | 428,840 | 5:00 PM | 35,032 |
| Queens Blvd express | 298,502 | 378,563 | 5:00 PM | 29,772 |
| Eastern Pkwy | 297,104 | 397,769 | 8:00 AM | 32,929 |
| Manhattan Bridge | 291,280 | 371,731 | 5:00 PM | 28,712 |
| Queens Blvd west express | 289,148 | 366,256 | 5:00 PM | 28,753 |
| Queens Blvd local | 283,963 | 378,930 | 8:00 AM | 23,522 |
| 4 Av | 280,336 | 341,570 | 8:00 AM | 28,974 |
| 63 St | 273,313 | 353,863 | 5:00 PM | 27,565 |
| 6 Av express | 261,374 | 351,649 | 5:00 PM | 27,743 |
| Fulton St | 252,140 | 345,173 | 5:00 PM | 24,457 |
| Brighton | 226,913 | 303,348 | 8:00 AM | 22,449 |
| Flushing local | 220,808 | 246,208 | 4:00 PM | 16,264 |
| Queens Blvd west local | 196,158 | 260,230 | 5:00 PM | 15,756 |
| Jamaica | 189,376 | 255,167 | 8:00 AM | 17,916 |
| Queens Blvd east | 184,491 | 242,646 | 5:00 PM | 16,310 |
| White Plains Rd | 164,231 | 245,304 | 7:00 AM | 17,820 |
| Culver | 155,950 | 196,767 | 8:00 AM | 15,652 |
| Jerome Av | 155,623 | 221,500 | 4:00 PM | 12,745 |
| SAS Phase 1 | 147,781 | 192,169 | 5:00 PM | 15,082 |
| Eastern Pkwy express | 147,231 | 197,726 | 8:00 AM | 14,470 |
| 4 Av express | 147,016 | 177,764 | 8:00 AM | 14,247 |
| Culver local | 146,704 | 185,609 | 8:00 AM | 14,833 |
| Eastern Pkwy local | 144,243 | 192,592 | 8:00 AM | 12,687 |
| Upper Culver | 141,092 | 177,624 | 8:00 AM | 14,162 |
| Upper Culver local | 139,035 | 174,855 | 8:00 AM | 14,162 |
| Fulton St express | 137,155 | 195,009 | 5:00 PM | 13,784 |
| 4 Av local | 133,935 | 164,391 | 5:00 PM | 11,220 |
| Crosstown | 132,699 | 154,068 | 5:00 PM | 12,288 |
| Lenox Av | 128,684 | 189,335 | 8:00 AM | 11,354 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,444 |
| Jamaica local | 113,691 | 152,611 | 8:00 AM | 11,000 |
| Concourse | 112,843 | 178,552 | 4:00 PM | 9,845 |
| Brighton local | 108,233 | 143,418 | 8:00 AM | 9,748 |
| White Plains Rd local | 107,429 | 159,621 | 3:00 PM | 9,475 |
| Concourse local | 106,510 | 167,754 | 3:00 PM | 8,318 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,008 |
| Fulton St local | 91,772 | 121,962 | 5:00 PM | 6,969 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,865 |
| West End | 81,881 | 106,993 | 7:00 AM | 7,878 |
| Pelham local | 80,730 | 115,750 | 7:00 AM | 6,539 |
| Sea Beach | 78,967 | 86,729 | 5:00 PM | 7,326 |
| Brighton express | 66,719 | 92,665 | 8:00 AM | 7,156 |
| Nassau St | 63,445 | 88,233 | 5:00 PM | 6,004 |
| 42 St Shuttle | 58,624 | 78,757 | 5:00 PM | 6,679 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,523 |
| Hillside Av local | 55,675 | 77,374 | 5:00 PM | 4,802 |
| Myrtle Av | 47,944 | 60,350 | 8:00 AM | 4,214 |
| Lower Culver | 39,712 | 54,014 | 7:00 AM | 4,121 |
| Lower Culver local | 36,759 | 50,197 | 7:00 AM | 3,862 |
| Pelham express | 36,606 | 54,964 | 7:00 AM | 5,357 |
| Flushing express | 35,641 | 40,885 | 5:00 PM | 6,084 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,587 |
| Jamaica express | 26,968 | 36,952 | 8:00 AM | 4,077 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,769 |
| White Plains Rd express | 20,698 | 30,764 | 7:00 AM | 4,622 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Concourse express | 14,863 | 24,954 | 7:00 AM | 3,218 |
| Franklin Av Shuttle | 13,566 | 18,097 | 8:00 AM | 1,197 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 300 |
| Culver express | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Upper Culver express | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Hillside Av express | 2,169 | 3,118 | 7:00 AM | 910 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
