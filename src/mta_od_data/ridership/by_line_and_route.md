# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Route | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| 4 Av | R | 145,567 | 180,413 | 8:00 AM | 14,584 |
| 4 Av | N | 94,532 | 108,001 | 8:00 AM | 7,986 |
| 4 Av | D | 78,380 | 100,977 | 5:00 PM | 6,848 |
| 4 Av | W | 1,530 | 1,847 | 7:00 AM | 691 |
| 4 Av express | N | 83,846 | 95,798 | 8:00 AM | 7,986 |
| 4 Av express | D | 66,669 | 86,166 | 5:00 PM | 6,848 |
| 4 Av local | R | 112,700 | 139,118 | 5:00 PM | 11,293 |
| 4 Av local | N | 12,477 | 14,196 | 5:00 AM | 2,034 |
| 4 Av local | D | 9,884 | 12,476 | 5:00 AM | 1,855 |
| 4 Av local | W | 1,094 | 1,291 | 7:00 AM | 442 |
| 42 St Shuttle | GS | 63,814 | 85,619 | 5:00 PM | 7,614 |
| 53 St | E | 241,580 | 314,394 | 5:00 PM | 24,971 |
| 53 St | M | 52,926 | 71,540 | 6:00 PM | 4,891 |
| 53 St | F | 38,379 | 50,070 | 5:00 PM | 3,964 |
| 53 St | FL | 38,097 | 49,698 | 5:00 PM | 3,872 |
| 53 St | FX | 282 | 372 | 8:00 AM | 105 |
| 6 Av | F | 359,007 | 456,618 | 5:00 PM | 37,499 |
| 6 Av | FL | 354,234 | 450,434 | 5:00 PM | 35,121 |
| 6 Av | D | 176,302 | 239,792 | 5:00 PM | 16,556 |
| 6 Av | B | 143,244 | 188,165 | 5:00 PM | 15,925 |
| 6 Av | M | 125,679 | 169,025 | 6:00 PM | 12,596 |
| 6 Av | FX | 4,773 | 6,184 | 5:00 PM | 2,378 |
| 6 Av express | D | 137,334 | 187,309 | 5:00 PM | 12,832 |
| 6 Av express | B | 111,677 | 147,621 | 5:00 PM | 12,502 |
| 6 Av local | F | 258,043 | 331,577 | 5:00 PM | 27,315 |
| 6 Av local | FL | 254,753 | 327,265 | 5:00 PM | 25,306 |
| 6 Av local | M | 103,294 | 139,611 | 5:00 PM | 10,760 |
| 6 Av local | FX | 3,289 | 4,312 | 5:00 PM | 2,009 |
| 63 St | F | 150,625 | 192,802 | 5:00 PM | 13,803 |
| 63 St | FL | 149,848 | 191,794 | 5:00 PM | 13,529 |
| 63 St | Q | 97,138 | 128,044 | 8:00 AM | 9,486 |
| 63 St | M | 18,111 | 23,483 | 5:00 PM | 1,712 |
| 63 St | N | 3,963 | 5,201 | 4:00 PM | 1,433 |
| 63 St | FX | 797 | 1,037 | 8:00 AM | 290 |
| 63 St | R | 490 | 637 | 7:00 AM | 490 |
| 8 Av | A | 358,684 | 491,837 | 5:00 PM | 38,017 |
| 8 Av | E | 202,140 | 264,298 | 5:00 PM | 21,822 |
| 8 Av | C | 184,765 | 238,130 | 6:00 PM | 14,939 |
| 8 Av | D | 86,218 | 129,288 | 5:00 PM | 6,405 |
| 8 Av | B | 74,607 | 97,011 | 5:00 PM | 9,057 |
| 8 Av express | A | 286,093 | 387,682 | 5:00 PM | 30,986 |
| 8 Av express | D | 86,218 | 129,288 | 5:00 PM | 6,405 |
| 8 Av local | E | 201,158 | 262,750 | 5:00 PM | 21,700 |
| 8 Av local | C | 155,914 | 198,691 | 6:00 PM | 12,933 |
| 8 Av local | B | 74,607 | 97,011 | 5:00 PM | 9,057 |
| 8 Av local | A | 22,104 | 29,016 | 11:00 PM | 10,430 |
| Astoria | N | 54,519 | 63,430 | 5:00 PM | 5,601 |
| Astoria | W | 46,504 | 54,792 | 8:00 AM | 5,402 |
| Brighton | Q | 149,446 | 197,206 | 8:00 AM | 13,070 |
| Brighton | B | 85,619 | 116,940 | 8:00 AM | 9,216 |
| Brighton express | B | 66,700 | 92,567 | 8:00 AM | 7,225 |
| Brighton local | Q | 109,612 | 145,304 | 8:00 AM | 9,796 |
| Broadway | R | 230,406 | 312,379 | 5:00 PM | 24,408 |
| Broadway | Q | 205,264 | 272,857 | 5:00 PM | 19,557 |
| Broadway | N | 197,252 | 245,169 | 5:00 PM | 19,249 |
| Broadway | W | 139,039 | 182,407 | 5:00 PM | 14,131 |
| Broadway express | Q | 200,319 | 266,303 | 5:00 PM | 19,557 |
| Broadway express | N | 104,199 | 128,808 | 4:00 PM | 12,151 |
| Broadway local | R | 152,946 | 209,729 | 5:00 PM | 16,119 |
| Broadway local | N | 118,534 | 146,140 | 5:00 PM | 11,081 |
| Broadway local | W | 113,500 | 151,320 | 5:00 PM | 11,244 |
| Broadway local | Q | 10,805 | 14,075 | 12:00 AM | 3,927 |
| Broadway-7 Av | 1 | 511,652 | 678,410 | 5:00 PM | 50,348 |
| Broadway-7 Av | 2 | 230,327 | 319,746 | 5:00 PM | 21,871 |
| Broadway-7 Av | 3 | 165,839 | 230,271 | 8:00 AM | 17,055 |
| Broadway-7 Av express | 2 | 202,590 | 281,505 | 5:00 PM | 19,352 |
| Broadway-7 Av express | 3 | 145,689 | 201,870 | 8:00 AM | 15,123 |
| Broadway-7 Av local | 1 | 427,356 | 565,795 | 5:00 PM | 42,485 |
| Broadway-7 Av local | 2 | 6,931 | 9,543 | 1:00 AM | 2,077 |
| Canarsie | L | 376,186 | 424,383 | 5:00 PM | 35,461 |
| Concourse | D | 79,997 | 128,229 | 3:00 PM | 6,234 |
| Concourse | B | 34,658 | 53,205 | 5:00 PM | 4,928 |
| Concourse express | D | 14,984 | 25,119 | 7:00 AM | 3,234 |
| Concourse express | B | 43 | 80 | 9:00 AM | 43 |
| Concourse local | D | 72,637 | 115,798 | 3:00 PM | 6,217 |
| Concourse local | B | 34,656 | 53,202 | 5:00 PM | 4,928 |
| Crosstown | G | 133,141 | 154,325 | 5:00 PM | 12,282 |
| Culver | F | 115,225 | 148,627 | 8:00 AM | 11,663 |
| Culver | FL | 112,776 | 145,348 | 8:00 AM | 11,663 |
| Culver | G | 47,319 | 55,715 | 5:00 PM | 4,130 |
| Culver | FX | 2,686 | 3,592 | 7:00 AM | 1,578 |
| Culver express | F | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Culver express | FX | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Culver local | F | 111,684 | 144,027 | 8:00 AM | 11,411 |
| Culver local | FL | 110,137 | 141,928 | 8:00 AM | 11,411 |
| Culver local | G | 39,659 | 46,876 | 8:00 AM | 3,593 |
| Culver local | FX | 1,561 | 2,117 | 7:00 AM | 965 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,766 |
| Eastern Pkwy | 3 | 95,842 | 131,856 | 8:00 AM | 9,390 |
| Eastern Pkwy | 2 | 88,552 | 115,808 | 8:00 AM | 9,073 |
| Eastern Pkwy | 4 | 81,525 | 110,898 | 7:00 AM | 6,926 |
| Eastern Pkwy | 5 | 75,936 | 100,188 | 8:00 AM | 7,999 |
| Eastern Pkwy express | 4 | 78,073 | 106,206 | 7:00 AM | 6,904 |
| Eastern Pkwy express | 5 | 71,026 | 93,767 | 8:00 AM | 7,709 |
| Eastern Pkwy local | 3 | 71,946 | 98,443 | 8:00 AM | 6,905 |
| Eastern Pkwy local | 2 | 67,130 | 87,252 | 8:00 AM | 6,294 |
| Eastern Pkwy local | 4 | 8,103 | 11,127 | 5:00 AM | 1,924 |
| Eastern Pkwy local | 5 | 161 | 227 | 5:00 AM | 147 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,568 |
| Flushing | 7 | 492,034 | 565,807 | 5:00 PM | 53,777 |
| Flushing | 7L | 401,266 | 461,716 | 5:00 PM | 36,495 |
| Flushing | 7X | 93,004 | 106,666 | 5:00 PM | 17,282 |
| Flushing express | 7 | 35,231 | 40,447 | 5:00 PM | 5,743 |
| Flushing express | 7X | 35,231 | 40,447 | 5:00 PM | 5,743 |
| Flushing local | 7 | 220,703 | 246,049 | 4:00 PM | 16,378 |
| Flushing local | 7L | 220,703 | 246,049 | 4:00 PM | 16,378 |
| Franklin Av Shuttle | FS | 13,030 | 17,391 | 8:00 AM | 1,111 |
| Fulton St | A | 171,539 | 241,526 | 5:00 PM | 15,989 |
| Fulton St | C | 85,413 | 112,009 | 5:00 PM | 7,452 |
| Fulton St express | A | 136,496 | 194,271 | 5:00 PM | 13,609 |
| Fulton St local | C | 77,507 | 102,241 | 5:00 PM | 6,912 |
| Fulton St local | A | 14,295 | 19,812 | 11:00 PM | 3,862 |
| Hillside Av | F | 55,565 | 77,226 | 5:00 PM | 4,790 |
| Hillside Av | FL | 55,202 | 76,739 | 5:00 PM | 4,720 |
| Hillside Av | E | 2,161 | 3,109 | 7:00 AM | 847 |
| Hillside Av | FX | 363 | 487 | 8:00 AM | 151 |
| Hillside Av express | E | 2,028 | 2,924 | 7:00 AM | 847 |
| Hillside Av local | F | 55,565 | 77,226 | 5:00 PM | 4,790 |
| Hillside Av local | FL | 55,202 | 76,739 | 5:00 PM | 4,720 |
| Hillside Av local | FX | 363 | 487 | 8:00 AM | 151 |
| Hillside Av local | E | 133 | 185 | 8:00 PM | 133 |
| Jamaica | J | 129,659 | 175,399 | 4:00 PM | 10,607 |
| Jamaica | M | 57,806 | 77,296 | 8:00 AM | 5,829 |
| Jamaica | Z | 9,004 | 12,187 | 5:00 PM | 3,526 |
| Jamaica express | J | 24,219 | 33,264 | 9:00 AM | 3,151 |
| Jamaica express | Z | 4,160 | 5,688 | 8:00 AM | 1,944 |
| Jamaica local | J | 68,626 | 93,150 | 4:00 PM | 5,365 |
| Jamaica local | M | 50,321 | 66,744 | 8:00 AM | 5,111 |
| Jamaica local | Z | 4,418 | 6,052 | 8:00 AM | 1,616 |
| Jerome Av | 4 | 160,638 | 229,167 | 3:00 PM | 13,212 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,672 |
| Lenox Av | 2 | 95,859 | 141,249 | 8:00 AM | 8,214 |
| Lenox Av | 3 | 32,693 | 48,154 | 5:00 PM | 2,930 |
| Lexington Av | 6 | 508,923 | 667,267 | 5:00 PM | 48,547 |
| Lexington Av | 6L | 383,138 | 499,734 | 5:00 PM | 33,104 |
| Lexington Av | 4 | 327,507 | 447,971 | 5:00 PM | 29,893 |
| Lexington Av | 5 | 231,990 | 316,116 | 8:00 AM | 25,180 |
| Lexington Av | 6X | 125,990 | 167,795 | 5:00 PM | 15,442 |
| Lexington Av express | 4 | 269,207 | 362,902 | 5:00 PM | 24,492 |
| Lexington Av express | 5 | 199,721 | 268,676 | 8:00 AM | 21,693 |
| Lexington Av local | 6 | 508,923 | 667,267 | 5:00 PM | 48,547 |
| Lexington Av local | 6L | 383,138 | 499,734 | 5:00 PM | 33,104 |
| Lexington Av local | 6X | 125,990 | 167,795 | 5:00 PM | 15,442 |
| Lexington Av local | 4 | 7,057 | 9,425 | 5:00 AM | 1,535 |
| Lower Culver | F | 39,750 | 54,041 | 7:00 AM | 4,110 |
| Lower Culver | FL | 38,136 | 51,857 | 8:00 AM | 3,949 |
| Lower Culver | FX | 1,614 | 2,184 | 7:00 AM | 995 |
| Lower Culver local | F | 37,059 | 50,554 | 7:00 AM | 3,872 |
| Lower Culver local | FL | 35,497 | 48,437 | 8:00 AM | 3,698 |
| Lower Culver local | FX | 1,561 | 2,117 | 7:00 AM | 965 |
| Manhattan Bridge | Q | 92,553 | 121,823 | 8:00 AM | 8,711 |
| Manhattan Bridge | N | 71,458 | 84,524 | 5:00 PM | 7,663 |
| Manhattan Bridge | D | 64,189 | 82,165 | 5:00 PM | 5,819 |
| Manhattan Bridge | B | 55,842 | 74,482 | 5:00 PM | 6,251 |
| Myrtle Av | M | 49,044 | 61,612 | 8:00 AM | 4,308 |
| Nassau St | J | 59,755 | 83,000 | 4:00 PM | 4,633 |
| Nassau St | Z | 4,684 | 6,594 | 8:00 AM | 2,515 |
| Nostrand Av | 5 | 43,084 | 55,556 | 7:00 AM | 4,618 |
| Nostrand Av | 2 | 39,036 | 50,253 | 8:00 AM | 3,347 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,427 |
| Pelham | 6L | 90,200 | 129,163 | 7:00 AM | 7,309 |
| Pelham | 6X | 41,430 | 62,084 | 7:00 AM | 6,117 |
| Pelham express | 6 | 36,881 | 55,353 | 7:00 AM | 5,396 |
| Pelham express | 6X | 36,837 | 55,282 | 7:00 AM | 5,396 |
| Pelham express | 6L | 44 | 71 | 9:00 PM | 30 |
| Pelham local | 6 | 80,771 | 115,815 | 7:00 AM | 6,465 |
| Pelham local | 6L | 80,771 | 115,815 | 7:00 AM | 6,465 |
| Queens Blvd | E | 214,249 | 265,708 | 5:00 PM | 19,966 |
| Queens Blvd | F | 183,748 | 237,356 | 5:00 PM | 16,444 |
| Queens Blvd | FL | 182,768 | 236,096 | 5:00 PM | 16,192 |
| Queens Blvd | R | 84,700 | 113,056 | 5:00 PM | 8,486 |
| Queens Blvd | M | 82,151 | 110,080 | 8:00 AM | 8,383 |
| Queens Blvd | FX | 980 | 1,260 | 8:00 AM | 407 |
| Queens Blvd east | E | 103,610 | 131,001 | 7:00 AM | 9,022 |
| Queens Blvd east | F | 83,971 | 115,874 | 8:00 AM | 7,795 |
| Queens Blvd east | FL | 83,404 | 115,112 | 8:00 AM | 7,558 |
| Queens Blvd east | FX | 568 | 762 | 8:00 AM | 238 |
| Queens Blvd express | E | 186,235 | 230,251 | 5:00 PM | 19,214 |
| Queens Blvd express | F | 99,125 | 132,136 | 5:00 PM | 9,716 |
| Queens Blvd express | FL | 98,521 | 131,354 | 5:00 PM | 9,528 |
| Queens Blvd express | FX | 605 | 782 | 8:00 AM | 259 |
| Queens Blvd local | F | 95,722 | 130,865 | 8:00 AM | 8,000 |
| Queens Blvd local | FL | 95,133 | 130,075 | 8:00 AM | 7,749 |
| Queens Blvd local | R | 84,700 | 113,056 | 5:00 PM | 8,486 |
| Queens Blvd local | M | 81,694 | 109,384 | 8:00 AM | 8,323 |
| Queens Blvd local | E | 32,999 | 41,259 | 10:00 PM | 4,813 |
| Queens Blvd local | FX | 589 | 791 | 8:00 AM | 250 |
| Queens Blvd west | E | 189,310 | 233,356 | 5:00 PM | 17,726 |
| Queens Blvd west | F | 113,405 | 150,577 | 5:00 PM | 9,716 |
| Queens Blvd west | FL | 112,801 | 149,795 | 5:00 PM | 9,528 |
| Queens Blvd west | R | 84,700 | 113,056 | 5:00 PM | 8,486 |
| Queens Blvd west | M | 81,694 | 109,384 | 8:00 AM | 8,323 |
| Queens Blvd west | FX | 605 | 782 | 8:00 AM | 259 |
| Queens Blvd west express | E | 174,205 | 214,514 | 5:00 PM | 17,726 |
| Queens Blvd west express | F | 99,125 | 132,136 | 5:00 PM | 9,716 |
| Queens Blvd west express | FL | 98,521 | 131,354 | 5:00 PM | 9,528 |
| Queens Blvd west express | FX | 605 | 782 | 8:00 AM | 259 |
| Queens Blvd west local | R | 84,700 | 113,056 | 5:00 PM | 8,486 |
| Queens Blvd west local | M | 81,694 | 109,384 | 8:00 AM | 8,323 |
| Queens Blvd west local | E | 15,208 | 18,987 | 10:00 PM | 3,797 |
| Queens Blvd west local | F | 14,321 | 18,498 | 10:00 PM | 4,393 |
| Queens Blvd west local | FL | 14,321 | 18,498 | 10:00 PM | 4,393 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,435 |
| Rockaway | H | 2,771 | 5,419 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,771 | 5,419 | 4:00 PM | 242 |
| Rockaway Park branch | A | 431 | 847 | 7:00 AM | 149 |
| SAS Phase 1 | Q | 134,288 | 175,274 | 8:00 AM | 13,234 |
| SAS Phase 1 | N | 5,231 | 6,828 | 4:00 PM | 2,495 |
| SAS Phase 1 | R | 796 | 1,018 | 7:00 AM | 796 |
| Sea Beach | N | 78,741 | 86,571 | 5:00 PM | 7,306 |
| Sea Beach | W | 519 | 560 | 7:00 AM | 293 |
| Upper Culver | F | 104,940 | 134,694 | 8:00 AM | 10,748 |
| Upper Culver | FL | 102,752 | 131,756 | 8:00 AM | 10,748 |
| Upper Culver | G | 39,659 | 46,876 | 8:00 AM | 3,593 |
| Upper Culver | FX | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Upper Culver express | F | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Upper Culver express | FX | 2,423 | 3,249 | 7:00 AM | 1,386 |
| Upper Culver local | F | 102,752 | 131,756 | 8:00 AM | 10,748 |
| Upper Culver local | FL | 102,752 | 131,756 | 8:00 AM | 10,748 |
| Upper Culver local | G | 39,659 | 46,876 | 8:00 AM | 3,593 |
| West End | D | 81,950 | 107,068 | 7:00 AM | 7,860 |
| West End | W | 57 | 73 | 10:00 AM | 35 |
| West End | R | 30 | 37 | 9:00 AM | 30 |
| White Plains Rd | 2 | 97,838 | 149,611 | 8:00 AM | 8,386 |
| White Plains Rd | 5 | 70,785 | 102,466 | 7:00 AM | 8,304 |
| White Plains Rd express | 5 | 18,340 | 27,077 | 7:00 AM | 4,306 |
| White Plains Rd local | 2 | 77,239 | 117,012 | 7:00 AM | 6,684 |
| White Plains Rd local | 5 | 32,471 | 46,205 | 3:00 PM | 4,431 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
