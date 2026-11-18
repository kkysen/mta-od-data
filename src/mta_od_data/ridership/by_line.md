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
| Lexington Av | 937,453 | 1,252,882 | 5:00 PM | 102,592 |
| 8 Av | 831,171 | 1,119,864 | 5:00 PM | 87,208 |
| Broadway-7 Av | 817,634 | 1,105,274 | 5:00 PM | 94,653 |
| Broadway | 782,048 | 1,022,370 | 5:00 PM | 81,015 |
| 6 Av | 769,894 | 1,010,562 | 5:00 PM | 85,685 |
| Queens Blvd | 504,137 | 643,505 | 5:00 PM | 54,018 |
| Lexington Av local | 490,674 | 641,872 | 5:00 PM | 46,242 |
| Flushing | 488,276 | 561,370 | 5:00 PM | 54,222 |
| Lexington Av express | 486,975 | 656,295 | 5:00 PM | 47,972 |
| Queens Blvd west | 444,639 | 572,005 | 5:00 PM | 44,509 |
| 8 Av local | 436,079 | 564,875 | 5:00 PM | 41,539 |
| Broadway local | 400,407 | 525,600 | 5:00 PM | 38,671 |
| Broadway-7 Av local | 395,780 | 524,809 | 5:00 PM | 38,183 |
| Canarsie | 381,254 | 431,152 | 5:00 PM | 35,918 |
| Broadway-7 Av express | 372,514 | 513,902 | 5:00 PM | 37,626 |
| 8 Av express | 357,050 | 497,269 | 5:00 PM | 35,666 |
| 53 St | 343,536 | 449,483 | 5:00 PM | 34,905 |
| 6 Av local | 341,243 | 446,442 | 5:00 PM | 35,645 |
| Broadway express | 332,042 | 428,754 | 5:00 PM | 35,025 |
| Queens Blvd express | 298,500 | 378,562 | 5:00 PM | 29,772 |
| Eastern Pkwy | 296,790 | 397,362 | 8:00 AM | 32,888 |
| Manhattan Bridge | 291,219 | 371,654 | 5:00 PM | 28,705 |
| Queens Blvd west express | 289,147 | 366,255 | 5:00 PM | 28,753 |
| Queens Blvd local | 283,963 | 378,929 | 8:00 AM | 23,522 |
| 4 Av | 280,406 | 341,655 | 8:00 AM | 28,985 |
| 63 St | 273,313 | 353,864 | 5:00 PM | 27,565 |
| 6 Av express | 261,365 | 351,638 | 5:00 PM | 27,743 |
| Fulton St | 252,138 | 345,171 | 5:00 PM | 24,458 |
| Brighton | 226,910 | 303,344 | 8:00 AM | 22,449 |
| Flushing local | 220,808 | 246,208 | 4:00 PM | 16,264 |
| Queens Blvd west local | 196,158 | 260,229 | 5:00 PM | 15,756 |
| Jamaica | 189,377 | 255,168 | 8:00 AM | 17,916 |
| Queens Blvd east | 184,490 | 242,645 | 5:00 PM | 16,310 |
| White Plains Rd | 164,231 | 245,304 | 7:00 AM | 17,820 |
| Culver | 155,940 | 196,754 | 8:00 AM | 15,651 |
| Jerome Av | 155,622 | 221,499 | 4:00 PM | 12,745 |
| SAS Phase 1 | 147,781 | 192,170 | 5:00 PM | 15,082 |
| Eastern Pkwy express | 147,248 | 197,747 | 8:00 AM | 14,471 |
| 4 Av express | 146,964 | 177,701 | 8:00 AM | 14,241 |
| Culver local | 146,694 | 185,597 | 8:00 AM | 14,832 |
| Eastern Pkwy local | 143,966 | 192,244 | 8:00 AM | 12,657 |
| Upper Culver | 141,083 | 177,612 | 8:00 AM | 14,161 |
| Upper Culver local | 139,025 | 174,842 | 8:00 AM | 14,161 |
| Fulton St express | 137,157 | 195,011 | 5:00 PM | 13,785 |
| 4 Av local | 133,994 | 164,463 | 5:00 PM | 11,223 |
| Crosstown | 132,699 | 154,068 | 5:00 PM | 12,288 |
| Lenox Av | 128,685 | 189,336 | 8:00 AM | 11,354 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,444 |
| Jamaica local | 113,691 | 152,611 | 8:00 AM | 11,000 |
| Concourse | 112,843 | 178,552 | 4:00 PM | 9,845 |
| Brighton local | 108,230 | 143,414 | 8:00 AM | 9,748 |
| White Plains Rd local | 107,429 | 159,621 | 3:00 PM | 9,475 |
| Concourse local | 106,510 | 167,754 | 3:00 PM | 8,318 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,008 |
| Fulton St local | 91,773 | 121,964 | 5:00 PM | 6,968 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,865 |
| West End | 81,881 | 106,993 | 7:00 AM | 7,878 |
| Pelham local | 80,730 | 115,750 | 7:00 AM | 6,539 |
| Sea Beach | 78,968 | 86,730 | 5:00 PM | 7,326 |
| Brighton express | 66,723 | 92,670 | 8:00 AM | 7,156 |
| Nassau St | 63,417 | 88,201 | 5:00 PM | 5,998 |
| 42 St Shuttle | 58,625 | 78,759 | 5:00 PM | 6,679 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,523 |
| Hillside Av local | 55,675 | 77,374 | 5:00 PM | 4,802 |
| Myrtle Av | 47,944 | 60,350 | 8:00 AM | 4,214 |
| Lower Culver | 39,712 | 54,014 | 7:00 AM | 4,121 |
| Lower Culver local | 36,758 | 50,197 | 7:00 AM | 3,862 |
| Pelham express | 36,606 | 54,964 | 7:00 AM | 5,357 |
| Flushing express | 35,641 | 40,885 | 5:00 PM | 6,084 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,587 |
| Jamaica express | 26,967 | 36,951 | 8:00 AM | 4,077 |
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
