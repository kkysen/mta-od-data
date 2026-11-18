# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Route | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| 4 Av | R | 144,001 | 178,006 | 8:00 AM | 14,532 |
| 4 Av | N | 93,120 | 106,213 | 8:00 AM | 7,650 |
| 4 Av | D | 76,478 | 98,659 | 5:00 PM | 6,710 |
| 4 Av | W | 1,527 | 1,830 | 7:00 AM | 715 |
| 4 Av express | N | 82,493 | 94,093 | 8:00 AM | 7,650 |
| 4 Av express | D | 65,241 | 84,411 | 5:00 PM | 6,710 |
| 4 Av local | R | 111,593 | 137,661 | 5:00 PM | 11,167 |
| 4 Av local | N | 12,205 | 13,868 | 5:00 AM | 1,989 |
| 4 Av local | D | 9,525 | 12,067 | 5:00 AM | 1,832 |
| 4 Av local | W | 1,109 | 1,305 | 7:00 AM | 447 |
| 42 St Shuttle | GS | 58,777 | 78,965 | 5:00 PM | 6,699 |
| 53 St | E | 258,052 | 335,592 | 5:00 PM | 26,773 |
| 53 St | M | 47,030 | 63,723 | 8:00 AM | 4,483 |
| 53 St | F | 39,208 | 51,206 | 5:00 PM | 4,146 |
| 53 St | FL | 38,923 | 50,829 | 5:00 PM | 4,067 |
| 53 St | FX | 285 | 376 | 8:00 AM | 108 |
| 6 Av | F | 353,685 | 450,575 | 5:00 PM | 36,318 |
| 6 Av | FL | 348,926 | 444,393 | 5:00 PM | 33,908 |
| 6 Av | D | 192,837 | 262,862 | 5:00 PM | 18,311 |
| 6 Av | B | 158,929 | 208,174 | 5:00 PM | 18,330 |
| 6 Av | M | 125,753 | 169,635 | 5:00 PM | 12,820 |
| 6 Av | FX | 4,758 | 6,182 | 5:00 PM | 2,410 |
| 6 Av express | D | 142,957 | 195,213 | 5:00 PM | 13,824 |
| 6 Av express | B | 118,611 | 156,722 | 5:00 PM | 13,920 |
| 6 Av local | F | 243,705 | 314,076 | 5:00 PM | 25,216 |
| 6 Av local | FL | 240,594 | 309,974 | 5:00 PM | 23,366 |
| 6 Av local | M | 97,885 | 132,826 | 5:00 PM | 10,451 |
| 6 Av local | FX | 3,111 | 4,102 | 5:00 PM | 1,851 |
| 63 St | F | 157,203 | 201,254 | 5:00 PM | 14,582 |
| 63 St | FL | 156,233 | 199,991 | 5:00 PM | 14,222 |
| 63 St | Q | 103,937 | 136,125 | 8:00 AM | 10,280 |
| 63 St | M | 18,099 | 23,451 | 5:00 PM | 1,695 |
| 63 St | N | 4,117 | 5,382 | 4:00 PM | 1,420 |
| 63 St | FX | 989 | 1,290 | 8:00 AM | 381 |
| 63 St | R | 460 | 600 | 7:00 AM | 460 |
| 8 Av | A | 349,935 | 481,921 | 5:00 PM | 36,720 |
| 8 Av | C | 188,510 | 243,724 | 6:00 PM | 15,298 |
| 8 Av | E | 186,286 | 243,842 | 5:00 PM | 19,711 |
| 8 Av | D | 87,003 | 130,105 | 4:00 PM | 6,534 |
| 8 Av | B | 75,191 | 97,221 | 5:00 PM | 9,059 |
| 8 Av express | A | 274,776 | 374,386 | 5:00 PM | 29,365 |
| 8 Av express | D | 87,003 | 130,105 | 4:00 PM | 6,534 |
| 8 Av local | E | 185,388 | 242,426 | 5:00 PM | 19,603 |
| 8 Av local | C | 157,000 | 200,814 | 6:00 PM | 13,115 |
| 8 Av local | B | 75,191 | 97,221 | 5:00 PM | 9,059 |
| 8 Av local | A | 22,052 | 29,061 | 11:00 PM | 9,991 |
| Astoria | N | 54,475 | 63,402 | 5:00 PM | 5,597 |
| Astoria | W | 46,548 | 54,820 | 8:00 AM | 5,402 |
| Brighton | Q | 151,886 | 200,218 | 8:00 AM | 13,370 |
| Brighton | B | 86,519 | 118,157 | 8:00 AM | 9,180 |
| Brighton express | B | 66,575 | 92,483 | 8:00 AM | 7,145 |
| Brighton local | Q | 108,332 | 143,543 | 8:00 AM | 9,743 |
| Broadway | R | 231,286 | 312,701 | 5:00 PM | 24,376 |
| Broadway | Q | 226,255 | 298,844 | 5:00 PM | 22,651 |
| Broadway | N | 205,749 | 255,451 | 5:00 PM | 19,616 |
| Broadway | W | 141,681 | 185,471 | 5:00 PM | 14,423 |
| Broadway express | Q | 220,477 | 291,264 | 5:00 PM | 22,651 |
| Broadway express | N | 111,413 | 137,155 | 4:00 PM | 12,854 |
| Broadway local | R | 152,358 | 208,159 | 5:00 PM | 16,010 |
| Broadway local | N | 121,860 | 150,268 | 5:00 PM | 10,915 |
| Broadway local | W | 117,490 | 155,980 | 5:00 PM | 11,764 |
| Broadway local | Q | 11,547 | 14,931 | 12:00 AM | 4,114 |
| Broadway-7 Av | 1 | 518,495 | 687,307 | 5:00 PM | 52,184 |
| Broadway-7 Av | 2 | 237,511 | 328,098 | 5:00 PM | 22,798 |
| Broadway-7 Av | 3 | 183,406 | 252,913 | 5:00 PM | 19,642 |
| Broadway-7 Av express | 2 | 210,333 | 290,740 | 5:00 PM | 20,435 |
| Broadway-7 Av express | 3 | 162,779 | 223,983 | 5:00 PM | 17,240 |
| Broadway-7 Av local | 1 | 389,234 | 515,764 | 5:00 PM | 38,185 |
| Broadway-7 Av local | 2 | 6,780 | 9,343 | 1:00 AM | 2,051 |
| Canarsie | L | 381,164 | 431,011 | 5:00 PM | 35,951 |
| Concourse | D | 79,656 | 127,722 | 3:00 PM | 6,167 |
| Concourse | B | 34,387 | 52,779 | 5:00 PM | 4,984 |
| Concourse express | D | 14,816 | 24,866 | 7:00 AM | 3,217 |
| Concourse express | B | 46 | 85 | 9:00 AM | 46 |
| Concourse local | D | 72,329 | 115,341 | 3:00 PM | 6,150 |
| Concourse local | B | 34,385 | 52,776 | 5:00 PM | 4,984 |
| Crosstown | G | 132,782 | 154,161 | 5:00 PM | 12,296 |
| Culver | F | 114,124 | 147,243 | 8:00 AM | 11,571 |
| Culver | FL | 111,732 | 144,038 | 8:00 AM | 11,571 |
| Culver | G | 47,176 | 55,926 | 5:00 PM | 4,178 |
| Culver | FX | 2,614 | 3,499 | 7:00 AM | 1,583 |
| Culver express | F | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Culver express | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Culver local | F | 110,336 | 142,333 | 8:00 AM | 11,315 |
| Culver local | FL | 108,815 | 140,269 | 8:00 AM | 11,315 |
| Culver local | G | 38,256 | 45,538 | 8:00 AM | 3,512 |
| Culver local | FX | 1,539 | 2,087 | 7:00 AM | 965 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,769 |
| Eastern Pkwy | 3 | 95,277 | 131,075 | 8:00 AM | 9,605 |
| Eastern Pkwy | 2 | 87,545 | 114,292 | 8:00 AM | 8,711 |
| Eastern Pkwy | 4 | 79,812 | 108,834 | 7:00 AM | 6,873 |
| Eastern Pkwy | 5 | 74,173 | 98,077 | 8:00 AM | 7,839 |
| Eastern Pkwy express | 4 | 76,383 | 104,176 | 7:00 AM | 6,854 |
| Eastern Pkwy express | 5 | 69,377 | 91,814 | 8:00 AM | 7,703 |
| Eastern Pkwy local | 3 | 70,590 | 96,557 | 8:00 AM | 6,641 |
| Eastern Pkwy local | 2 | 66,086 | 85,626 | 8:00 AM | 5,983 |
| Eastern Pkwy local | 4 | 8,011 | 11,006 | 5:00 AM | 1,899 |
| Eastern Pkwy local | 5 | 183 | 259 | 5:00 AM | 167 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Flushing | 7 | 488,486 | 561,645 | 5:00 PM | 54,244 |
| Flushing | 7L | 399,501 | 459,441 | 5:00 PM | 36,182 |
| Flushing | 7X | 92,615 | 106,391 | 5:00 PM | 18,062 |
| Flushing express | 7 | 35,638 | 40,881 | 5:00 PM | 6,084 |
| Flushing express | 7X | 35,638 | 40,881 | 5:00 PM | 6,084 |
| Flushing local | 7 | 220,813 | 246,214 | 4:00 PM | 16,263 |
| Flushing local | 7L | 220,813 | 246,214 | 4:00 PM | 16,263 |
| Franklin Av Shuttle | FS | 13,770 | 18,363 | 8:00 AM | 1,218 |
| Fulton St | A | 174,305 | 244,753 | 5:00 PM | 16,276 |
| Fulton St | C | 89,783 | 117,431 | 5:00 PM | 8,146 |
| Fulton St express | A | 137,224 | 195,105 | 5:00 PM | 13,732 |
| Fulton St local | C | 77,697 | 102,454 | 5:00 PM | 6,998 |
| Fulton St local | A | 14,260 | 19,749 | 11:00 PM | 3,823 |
| Hillside Av | F | 55,520 | 77,159 | 5:00 PM | 4,803 |
| Hillside Av | FL | 55,149 | 76,658 | 5:00 PM | 4,734 |
| Hillside Av | E | 2,323 | 3,334 | 7:00 AM | 910 |
| Hillside Av | FX | 371 | 500 | 8:00 AM | 158 |
| Hillside Av express | E | 2,169 | 3,118 | 7:00 AM | 910 |
| Hillside Av local | F | 55,520 | 77,159 | 5:00 PM | 4,803 |
| Hillside Av local | FL | 55,149 | 76,658 | 5:00 PM | 4,734 |
| Hillside Av local | FX | 371 | 500 | 8:00 AM | 158 |
| Hillside Av local | E | 155 | 216 | 8:00 PM | 155 |
| Jamaica | J | 131,066 | 177,458 | 4:00 PM | 10,476 |
| Jamaica | M | 56,554 | 75,633 | 8:00 AM | 5,683 |
| Jamaica | Z | 9,005 | 12,203 | 5:00 PM | 3,407 |
| Jamaica express | J | 22,953 | 31,459 | 9:00 AM | 3,035 |
| Jamaica express | Z | 4,054 | 5,552 | 8:00 AM | 1,848 |
| Jamaica local | J | 66,804 | 90,563 | 4:00 PM | 5,153 |
| Jamaica local | M | 49,350 | 65,480 | 8:00 AM | 4,984 |
| Jamaica local | Z | 4,316 | 5,926 | 8:00 AM | 1,549 |
| Jerome Av | 4 | 155,604 | 221,480 | 4:00 PM | 12,744 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Lenox Av | 2 | 96,733 | 142,364 | 8:00 AM | 8,368 |
| Lenox Av | 3 | 32,776 | 48,268 | 8:00 AM | 2,990 |
| Lexington Av | 6 | 484,423 | 633,502 | 5:00 PM | 46,290 |
| Lexington Av | 6L | 365,553 | 475,851 | 5:00 PM | 31,835 |
| Lexington Av | 4 | 333,254 | 454,888 | 5:00 PM | 30,697 |
| Lexington Av | 5 | 244,083 | 333,601 | 8:00 AM | 26,053 |
| Lexington Av | 6X | 119,714 | 158,733 | 5:00 PM | 14,455 |
| Lexington Av express | 4 | 276,317 | 371,993 | 5:00 PM | 25,377 |
| Lexington Av express | 5 | 209,958 | 283,339 | 5:00 PM | 22,490 |
| Lexington Av local | 6 | 484,423 | 633,502 | 5:00 PM | 46,290 |
| Lexington Av local | 6L | 365,553 | 475,851 | 5:00 PM | 31,835 |
| Lexington Av local | 6X | 119,714 | 158,733 | 5:00 PM | 14,455 |
| Lexington Av local | 4 | 7,042 | 9,412 | 5:00 AM | 1,502 |
| Lower Culver | F | 39,757 | 54,072 | 7:00 AM | 4,124 |
| Lower Culver | FL | 38,175 | 51,929 | 8:00 AM | 3,954 |
| Lower Culver | FX | 1,581 | 2,143 | 7:00 AM | 991 |
| Lower Culver local | F | 36,797 | 50,247 | 7:00 AM | 3,864 |
| Lower Culver local | FL | 35,258 | 48,159 | 8:00 AM | 3,698 |
| Lower Culver local | FX | 1,539 | 2,087 | 7:00 AM | 965 |
| Manhattan Bridge | Q | 102,954 | 134,749 | 8:00 AM | 10,487 |
| Manhattan Bridge | N | 70,733 | 83,475 | 5:00 PM | 7,172 |
| Manhattan Bridge | D | 60,660 | 77,726 | 5:00 PM | 5,374 |
| Manhattan Bridge | B | 57,032 | 75,800 | 5:00 PM | 6,292 |
| Myrtle Av | M | 48,030 | 60,453 | 8:00 AM | 4,220 |
| Nassau St | J | 59,189 | 82,231 | 4:00 PM | 4,520 |
| Nassau St | Z | 4,564 | 6,437 | 8:00 AM | 2,425 |
| Nostrand Av | 5 | 43,348 | 55,985 | 7:00 AM | 4,787 |
| Nostrand Av | 2 | 40,268 | 51,842 | 8:00 AM | 3,474 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,446 |
| Pelham | 6L | 90,193 | 129,145 | 7:00 AM | 7,384 |
| Pelham | 6X | 41,121 | 61,649 | 7:00 AM | 6,062 |
| Pelham express | 6 | 36,609 | 54,969 | 7:00 AM | 5,356 |
| Pelham express | 6X | 36,563 | 54,895 | 7:00 AM | 5,356 |
| Pelham express | 6L | 46 | 75 | 9:00 PM | 35 |
| Pelham local | 6 | 80,726 | 115,745 | 7:00 AM | 6,541 |
| Pelham local | 6L | 80,726 | 115,745 | 7:00 AM | 6,541 |
| Queens Blvd | E | 228,671 | 283,678 | 5:00 PM | 20,868 |
| Queens Blvd | F | 190,384 | 245,738 | 5:00 PM | 17,349 |
| Queens Blvd | FL | 189,337 | 244,391 | 5:00 PM | 17,087 |
| Queens Blvd | M | 84,470 | 113,008 | 8:00 AM | 8,198 |
| Queens Blvd | R | 82,523 | 110,425 | 5:00 PM | 8,588 |
| Queens Blvd | FX | 1,047 | 1,347 | 8:00 AM | 446 |
| Queens Blvd east | E | 105,431 | 133,416 | 7:00 AM | 9,259 |
| Queens Blvd east | F | 82,194 | 113,487 | 8:00 AM | 7,564 |
| Queens Blvd east | FL | 81,624 | 112,719 | 8:00 AM | 7,316 |
| Queens Blvd east | FX | 571 | 768 | 8:00 AM | 249 |
| Queens Blvd express | E | 202,216 | 250,291 | 5:00 PM | 20,215 |
| Queens Blvd express | F | 98,270 | 130,961 | 5:00 PM | 9,562 |
| Queens Blvd express | FL | 97,639 | 130,140 | 5:00 PM | 9,374 |
| Queens Blvd express | FX | 632 | 821 | 8:00 AM | 271 |
| Queens Blvd local | F | 94,697 | 129,451 | 8:00 AM | 7,789 |
| Queens Blvd local | FL | 94,105 | 128,654 | 8:00 AM | 7,528 |
| Queens Blvd local | M | 83,991 | 112,292 | 8:00 AM | 8,134 |
| Queens Blvd local | R | 82,523 | 110,425 | 5:00 PM | 8,588 |
| Queens Blvd local | E | 32,875 | 41,001 | 10:00 PM | 4,802 |
| Queens Blvd local | FX | 592 | 797 | 8:00 AM | 261 |
| Queens Blvd west | E | 207,826 | 256,539 | 5:00 PM | 19,196 |
| Queens Blvd west | F | 113,091 | 150,091 | 5:00 PM | 9,562 |
| Queens Blvd west | FL | 112,460 | 149,270 | 5:00 PM | 9,374 |
| Queens Blvd west | M | 83,991 | 112,292 | 8:00 AM | 8,134 |
| Queens Blvd west | R | 82,523 | 110,425 | 5:00 PM | 8,588 |
| Queens Blvd west | FX | 632 | 821 | 8:00 AM | 271 |
| Queens Blvd west express | E | 192,847 | 237,960 | 5:00 PM | 19,196 |
| Queens Blvd west express | F | 98,270 | 130,961 | 5:00 PM | 9,562 |
| Queens Blvd west express | FL | 97,639 | 130,140 | 5:00 PM | 9,374 |
| Queens Blvd west express | FX | 632 | 821 | 8:00 AM | 271 |
| Queens Blvd west local | M | 83,991 | 112,292 | 8:00 AM | 8,134 |
| Queens Blvd west local | R | 82,523 | 110,425 | 5:00 PM | 8,588 |
| Queens Blvd west local | E | 15,093 | 18,736 | 10:00 PM | 3,846 |
| Queens Blvd west local | F | 14,850 | 19,169 | 10:00 PM | 4,482 |
| Queens Blvd west local | FL | 14,850 | 19,169 | 10:00 PM | 4,482 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,435 |
| Rockaway | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | A | 425 | 836 | 7:00 AM | 150 |
| SAS Phase 1 | Q | 141,510 | 184,028 | 8:00 AM | 14,169 |
| SAS Phase 1 | N | 5,519 | 7,184 | 4:00 PM | 2,639 |
| SAS Phase 1 | R | 788 | 1,011 | 7:00 AM | 788 |
| Sea Beach | N | 78,680 | 86,472 | 5:00 PM | 7,347 |
| Sea Beach | W | 504 | 543 | 7:00 AM | 286 |
| Upper Culver | F | 103,518 | 132,882 | 8:00 AM | 10,640 |
| Upper Culver | FL | 101,358 | 129,982 | 8:00 AM | 10,640 |
| Upper Culver | G | 38,256 | 45,538 | 8:00 AM | 3,512 |
| Upper Culver | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | F | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver local | F | 101,358 | 129,982 | 8:00 AM | 10,640 |
| Upper Culver local | FL | 101,358 | 129,982 | 8:00 AM | 10,640 |
| Upper Culver local | G | 38,256 | 45,538 | 8:00 AM | 3,512 |
| West End | D | 81,798 | 106,885 | 7:00 AM | 7,875 |
| West End | W | 69 | 89 | 10:00 AM | 44 |
| West End | R | 38 | 48 | 9:00 AM | 38 |
| White Plains Rd | 2 | 99,148 | 151,627 | 7:00 AM | 8,821 |
| White Plains Rd | 5 | 77,855 | 113,219 | 7:00 AM | 8,999 |
| White Plains Rd express | 5 | 20,693 | 30,757 | 7:00 AM | 4,619 |
| White Plains Rd local | 2 | 74,703 | 112,979 | 7:00 AM | 6,386 |
| White Plains Rd local | 5 | 33,011 | 47,132 | 3:00 PM | 4,519 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
