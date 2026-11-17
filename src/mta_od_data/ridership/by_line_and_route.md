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
| 4 Av | R | 143,928 | 177,923 | 8:00 AM | 14,527 |
| 4 Av | N | 93,215 | 106,321 | 8:00 AM | 7,655 |
| 4 Av | D | 76,385 | 98,551 | 5:00 PM | 6,704 |
| 4 Av | W | 1,526 | 1,830 | 7:00 AM | 715 |
| 4 Av express | N | 82,582 | 94,196 | 8:00 AM | 7,655 |
| 4 Av express | D | 65,183 | 84,346 | 5:00 PM | 6,704 |
| 4 Av local | R | 111,545 | 137,607 | 5:00 PM | 11,163 |
| 4 Av local | N | 12,210 | 13,874 | 5:00 AM | 1,991 |
| 4 Av local | D | 9,517 | 12,058 | 5:00 AM | 1,827 |
| 4 Av local | W | 1,109 | 1,305 | 7:00 AM | 447 |
| 42 St Shuttle | GS | 57,285 | 77,045 | 5:00 PM | 6,576 |
| 53 St | E | 256,019 | 332,845 | 5:00 PM | 26,692 |
| 53 St | M | 47,008 | 63,707 | 8:00 AM | 4,482 |
| 53 St | F | 39,152 | 51,152 | 5:00 PM | 4,126 |
| 53 St | FL | 38,866 | 50,775 | 5:00 PM | 4,046 |
| 53 St | FX | 285 | 377 | 8:00 AM | 108 |
| 6 Av | F | 352,848 | 449,585 | 5:00 PM | 36,182 |
| 6 Av | FL | 348,099 | 443,415 | 5:00 PM | 33,773 |
| 6 Av | D | 190,355 | 259,629 | 5:00 PM | 18,059 |
| 6 Av | B | 156,675 | 205,312 | 5:00 PM | 18,101 |
| 6 Av | M | 125,439 | 169,248 | 5:00 PM | 12,770 |
| 6 Av | FX | 4,748 | 6,170 | 5:00 PM | 2,408 |
| 6 Av express | D | 140,775 | 192,368 | 5:00 PM | 13,595 |
| 6 Av express | B | 116,638 | 154,222 | 5:00 PM | 13,730 |
| 6 Av local | F | 243,107 | 313,390 | 5:00 PM | 25,104 |
| 6 Av local | FL | 239,997 | 309,289 | 5:00 PM | 23,254 |
| 6 Av local | M | 97,642 | 132,531 | 5:00 PM | 10,409 |
| 6 Av local | FX | 3,110 | 4,101 | 5:00 PM | 1,850 |
| 63 St | F | 156,805 | 200,785 | 5:00 PM | 14,499 |
| 63 St | FL | 155,842 | 199,532 | 5:00 PM | 14,141 |
| 63 St | Q | 104,187 | 136,460 | 8:00 AM | 10,306 |
| 63 St | M | 18,044 | 23,379 | 5:00 PM | 1,687 |
| 63 St | N | 4,154 | 5,430 | 4:00 PM | 1,438 |
| 63 St | FX | 982 | 1,281 | 8:00 AM | 377 |
| 63 St | R | 466 | 608 | 7:00 AM | 466 |
| 8 Av | A | 353,309 | 486,006 | 5:00 PM | 37,082 |
| 8 Av | C | 189,863 | 245,285 | 6:00 PM | 15,413 |
| 8 Av | E | 187,469 | 245,068 | 5:00 PM | 19,972 |
| 8 Av | D | 86,109 | 128,900 | 4:00 PM | 6,434 |
| 8 Av | B | 74,347 | 96,206 | 5:00 PM | 8,967 |
| 8 Av express | A | 278,145 | 378,438 | 5:00 PM | 29,733 |
| 8 Av express | D | 86,109 | 128,900 | 4:00 PM | 6,434 |
| 8 Av local | E | 186,573 | 243,654 | 5:00 PM | 19,866 |
| 8 Av local | C | 158,405 | 202,427 | 6:00 PM | 13,228 |
| 8 Av local | B | 74,347 | 96,206 | 5:00 PM | 8,967 |
| 8 Av local | A | 22,245 | 29,282 | 11:00 PM | 10,093 |
| Astoria | N | 54,471 | 63,398 | 5:00 PM | 5,601 |
| Astoria | W | 46,553 | 54,824 | 8:00 AM | 5,405 |
| Brighton | Q | 152,024 | 200,400 | 8:00 AM | 13,378 |
| Brighton | B | 86,356 | 117,944 | 8:00 AM | 9,168 |
| Brighton express | B | 66,470 | 92,341 | 8:00 AM | 7,137 |
| Brighton local | Q | 108,387 | 143,620 | 8:00 AM | 9,746 |
| Broadway | R | 231,341 | 312,862 | 5:00 PM | 24,349 |
| Broadway | Q | 227,296 | 300,255 | 5:00 PM | 22,778 |
| Broadway | N | 206,673 | 256,706 | 5:00 PM | 19,657 |
| Broadway | W | 142,076 | 186,004 | 5:00 PM | 14,479 |
| Broadway express | Q | 221,465 | 292,610 | 5:00 PM | 22,778 |
| Broadway express | N | 111,647 | 137,496 | 4:00 PM | 12,912 |
| Broadway local | R | 152,593 | 208,542 | 5:00 PM | 15,995 |
| Broadway local | N | 122,989 | 151,777 | 4:00 PM | 11,012 |
| Broadway local | W | 117,941 | 156,578 | 5:00 PM | 11,830 |
| Broadway local | Q | 11,628 | 15,032 | 12:00 AM | 4,128 |
| Broadway-7 Av | 1 | 517,384 | 686,005 | 5:00 PM | 52,078 |
| Broadway-7 Av | 2 | 237,433 | 328,027 | 5:00 PM | 22,832 |
| Broadway-7 Av | 3 | 183,144 | 252,608 | 5:00 PM | 19,617 |
| Broadway-7 Av express | 2 | 210,244 | 290,649 | 5:00 PM | 20,466 |
| Broadway-7 Av express | 3 | 162,485 | 223,634 | 5:00 PM | 17,209 |
| Broadway-7 Av local | 1 | 388,159 | 514,496 | 5:00 PM | 38,077 |
| Broadway-7 Av local | 2 | 6,767 | 9,327 | 1:00 AM | 2,046 |
| Canarsie | L | 378,402 | 427,580 | 5:00 PM | 35,706 |
| Concourse | D | 79,590 | 127,629 | 3:00 PM | 6,159 |
| Concourse | B | 34,387 | 52,781 | 5:00 PM | 4,978 |
| Concourse express | D | 14,810 | 24,859 | 7:00 AM | 3,216 |
| Concourse express | B | 46 | 85 | 9:00 AM | 46 |
| Concourse local | D | 72,267 | 115,253 | 3:00 PM | 6,143 |
| Concourse local | B | 34,386 | 52,777 | 5:00 PM | 4,978 |
| Crosstown | G | 132,697 | 154,054 | 5:00 PM | 12,291 |
| Culver | F | 114,105 | 147,222 | 8:00 AM | 11,569 |
| Culver | FL | 111,713 | 144,017 | 8:00 AM | 11,569 |
| Culver | G | 47,176 | 55,925 | 5:00 PM | 4,178 |
| Culver | FX | 2,614 | 3,499 | 7:00 AM | 1,583 |
| Culver express | F | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Culver express | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Culver local | F | 110,318 | 142,312 | 8:00 AM | 11,313 |
| Culver local | FL | 108,797 | 140,248 | 8:00 AM | 11,313 |
| Culver local | G | 38,257 | 45,538 | 8:00 AM | 3,513 |
| Culver local | FX | 1,539 | 2,087 | 7:00 AM | 965 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,769 |
| Eastern Pkwy | 3 | 95,275 | 131,072 | 8:00 AM | 9,606 |
| Eastern Pkwy | 2 | 87,537 | 114,281 | 8:00 AM | 8,711 |
| Eastern Pkwy | 4 | 79,813 | 108,835 | 7:00 AM | 6,873 |
| Eastern Pkwy | 5 | 74,172 | 98,076 | 8:00 AM | 7,839 |
| Eastern Pkwy express | 4 | 76,383 | 104,176 | 7:00 AM | 6,854 |
| Eastern Pkwy express | 5 | 69,376 | 91,813 | 8:00 AM | 7,703 |
| Eastern Pkwy local | 3 | 70,589 | 96,557 | 8:00 AM | 6,642 |
| Eastern Pkwy local | 2 | 66,073 | 85,610 | 8:00 AM | 5,983 |
| Eastern Pkwy local | 4 | 8,013 | 11,008 | 5:00 AM | 1,899 |
| Eastern Pkwy local | 5 | 183 | 259 | 5:00 AM | 167 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Flushing | 7 | 491,982 | 566,189 | 5:00 PM | 54,522 |
| Flushing | 7L | 402,221 | 463,035 | 5:00 PM | 36,381 |
| Flushing | 7X | 93,386 | 107,333 | 5:00 PM | 18,141 |
| Flushing express | 7 | 35,705 | 40,958 | 5:00 PM | 6,085 |
| Flushing express | 7X | 35,705 | 40,958 | 5:00 PM | 6,085 |
| Flushing local | 7 | 220,671 | 246,058 | 4:00 PM | 16,249 |
| Flushing local | 7L | 220,671 | 246,058 | 4:00 PM | 16,249 |
| Franklin Av Shuttle | FS | 13,766 | 18,357 | 8:00 AM | 1,218 |
| Fulton St | A | 174,347 | 244,797 | 5:00 PM | 16,279 |
| Fulton St | C | 89,767 | 117,413 | 5:00 PM | 8,144 |
| Fulton St express | A | 137,252 | 195,137 | 5:00 PM | 13,733 |
| Fulton St local | C | 77,688 | 102,444 | 5:00 PM | 6,998 |
| Fulton St local | A | 14,260 | 19,748 | 11:00 PM | 3,823 |
| Hillside Av | F | 55,514 | 77,151 | 5:00 PM | 4,801 |
| Hillside Av | FL | 55,142 | 76,650 | 5:00 PM | 4,733 |
| Hillside Av | E | 2,331 | 3,343 | 7:00 AM | 912 |
| Hillside Av | FX | 371 | 500 | 8:00 AM | 158 |
| Hillside Av express | E | 2,175 | 3,126 | 7:00 AM | 912 |
| Hillside Av local | F | 55,514 | 77,151 | 5:00 PM | 4,801 |
| Hillside Av local | FL | 55,142 | 76,650 | 5:00 PM | 4,733 |
| Hillside Av local | FX | 371 | 500 | 8:00 AM | 158 |
| Hillside Av local | E | 155 | 216 | 8:00 PM | 155 |
| Jamaica | J | 131,057 | 177,447 | 4:00 PM | 10,475 |
| Jamaica | M | 56,556 | 75,634 | 8:00 AM | 5,682 |
| Jamaica | Z | 9,005 | 12,203 | 5:00 PM | 3,405 |
| Jamaica express | J | 22,946 | 31,451 | 9:00 AM | 3,034 |
| Jamaica express | Z | 4,053 | 5,551 | 8:00 AM | 1,848 |
| Jamaica local | J | 66,791 | 90,547 | 4:00 PM | 5,152 |
| Jamaica local | M | 49,351 | 65,481 | 8:00 AM | 4,984 |
| Jamaica local | Z | 4,315 | 5,926 | 8:00 AM | 1,548 |
| Jerome Av | 4 | 155,539 | 221,393 | 4:00 PM | 12,739 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Lenox Av | 2 | 96,751 | 142,390 | 8:00 AM | 8,370 |
| Lenox Av | 3 | 32,742 | 48,220 | 8:00 AM | 2,989 |
| Lexington Av | 6 | 483,619 | 632,502 | 5:00 PM | 46,200 |
| Lexington Av | 6L | 364,950 | 475,102 | 5:00 PM | 31,782 |
| Lexington Av | 4 | 333,000 | 454,575 | 5:00 PM | 30,676 |
| Lexington Av | 5 | 243,959 | 333,451 | 8:00 AM | 26,042 |
| Lexington Av | 6X | 119,513 | 158,483 | 5:00 PM | 14,418 |
| Lexington Av express | 4 | 276,086 | 371,711 | 5:00 PM | 25,359 |
| Lexington Av express | 5 | 209,841 | 283,199 | 5:00 PM | 22,463 |
| Lexington Av local | 6 | 483,619 | 632,502 | 5:00 PM | 46,200 |
| Lexington Av local | 6L | 364,950 | 475,102 | 5:00 PM | 31,782 |
| Lexington Av local | 6X | 119,513 | 158,483 | 5:00 PM | 14,418 |
| Lexington Av local | 4 | 7,039 | 9,409 | 5:00 AM | 1,501 |
| Lower Culver | F | 39,746 | 54,059 | 7:00 AM | 4,123 |
| Lower Culver | FL | 38,164 | 51,916 | 8:00 AM | 3,953 |
| Lower Culver | FX | 1,581 | 2,142 | 7:00 AM | 991 |
| Lower Culver local | F | 36,786 | 50,234 | 7:00 AM | 3,863 |
| Lower Culver local | FL | 35,247 | 48,147 | 8:00 AM | 3,697 |
| Lower Culver local | FX | 1,539 | 2,087 | 7:00 AM | 965 |
| Manhattan Bridge | Q | 103,240 | 135,109 | 8:00 AM | 10,507 |
| Manhattan Bridge | N | 70,944 | 83,719 | 5:00 PM | 7,188 |
| Manhattan Bridge | D | 60,495 | 77,529 | 5:00 PM | 5,364 |
| Manhattan Bridge | B | 56,832 | 75,544 | 5:00 PM | 6,274 |
| Myrtle Av | M | 48,030 | 60,453 | 8:00 AM | 4,220 |
| Nassau St | J | 59,051 | 82,052 | 4:00 PM | 4,508 |
| Nassau St | Z | 4,559 | 6,431 | 8:00 AM | 2,424 |
| Nostrand Av | 5 | 43,347 | 55,985 | 7:00 AM | 4,788 |
| Nostrand Av | 2 | 40,270 | 51,844 | 8:00 AM | 3,474 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,446 |
| Pelham | 6L | 90,193 | 129,145 | 7:00 AM | 7,383 |
| Pelham | 6X | 41,123 | 61,652 | 7:00 AM | 6,063 |
| Pelham express | 6 | 36,612 | 54,973 | 7:00 AM | 5,357 |
| Pelham express | 6X | 36,565 | 54,898 | 7:00 AM | 5,357 |
| Pelham express | 6L | 46 | 75 | 9:00 PM | 35 |
| Pelham local | 6 | 80,726 | 115,744 | 7:00 AM | 6,540 |
| Pelham local | 6L | 80,726 | 115,744 | 7:00 AM | 6,540 |
| Queens Blvd | E | 228,153 | 283,004 | 5:00 PM | 20,914 |
| Queens Blvd | F | 190,152 | 245,509 | 5:00 PM | 17,275 |
| Queens Blvd | FL | 189,106 | 244,162 | 5:00 PM | 17,013 |
| Queens Blvd | M | 84,416 | 112,939 | 8:00 AM | 8,197 |
| Queens Blvd | R | 82,580 | 110,497 | 5:00 PM | 8,587 |
| Queens Blvd | FX | 1,046 | 1,347 | 8:00 AM | 446 |
| Queens Blvd east | E | 105,465 | 133,447 | 7:00 AM | 9,261 |
| Queens Blvd east | F | 82,167 | 113,463 | 8:00 AM | 7,565 |
| Queens Blvd east | FL | 81,597 | 112,695 | 8:00 AM | 7,316 |
| Queens Blvd east | FX | 570 | 768 | 8:00 AM | 249 |
| Queens Blvd express | E | 201,900 | 249,839 | 5:00 PM | 20,259 |
| Queens Blvd express | F | 98,198 | 130,903 | 5:00 PM | 9,533 |
| Queens Blvd express | FL | 97,567 | 130,082 | 5:00 PM | 9,345 |
| Queens Blvd express | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd local | F | 94,626 | 129,379 | 8:00 AM | 7,789 |
| Queens Blvd local | FL | 94,034 | 128,582 | 8:00 AM | 7,528 |
| Queens Blvd local | M | 83,938 | 112,224 | 8:00 AM | 8,133 |
| Queens Blvd local | R | 82,580 | 110,497 | 5:00 PM | 8,587 |
| Queens Blvd local | E | 32,677 | 40,783 | 10:00 PM | 4,725 |
| Queens Blvd local | FX | 592 | 797 | 8:00 AM | 261 |
| Queens Blvd west | E | 207,308 | 255,865 | 5:00 PM | 19,241 |
| Queens Blvd west | F | 112,972 | 149,983 | 5:00 PM | 9,533 |
| Queens Blvd west | FL | 112,341 | 149,162 | 5:00 PM | 9,345 |
| Queens Blvd west | M | 83,938 | 112,224 | 8:00 AM | 8,133 |
| Queens Blvd west | R | 82,580 | 110,497 | 5:00 PM | 8,587 |
| Queens Blvd west | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd west express | E | 192,531 | 237,508 | 5:00 PM | 19,241 |
| Queens Blvd west express | F | 98,198 | 130,903 | 5:00 PM | 9,533 |
| Queens Blvd west express | FL | 97,567 | 130,082 | 5:00 PM | 9,345 |
| Queens Blvd west express | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd west local | M | 83,938 | 112,224 | 8:00 AM | 8,133 |
| Queens Blvd west local | R | 82,580 | 110,497 | 5:00 PM | 8,587 |
| Queens Blvd west local | E | 14,888 | 18,509 | 10:00 PM | 3,771 |
| Queens Blvd west local | F | 14,803 | 19,119 | 10:00 PM | 4,466 |
| Queens Blvd west local | FL | 14,803 | 19,119 | 10:00 PM | 4,466 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,435 |
| Rockaway | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | A | 425 | 836 | 7:00 AM | 150 |
| SAS Phase 1 | Q | 141,596 | 184,155 | 8:00 AM | 14,176 |
| SAS Phase 1 | N | 5,550 | 7,224 | 4:00 PM | 2,655 |
| SAS Phase 1 | R | 791 | 1,015 | 7:00 AM | 791 |
| Sea Beach | N | 78,694 | 86,489 | 5:00 PM | 7,347 |
| Sea Beach | W | 504 | 543 | 7:00 AM | 286 |
| Upper Culver | F | 103,500 | 132,861 | 8:00 AM | 10,638 |
| Upper Culver | FL | 101,339 | 129,961 | 8:00 AM | 10,638 |
| Upper Culver | G | 38,257 | 45,538 | 8:00 AM | 3,513 |
| Upper Culver | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | F | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | FX | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver local | F | 101,339 | 129,961 | 8:00 AM | 10,638 |
| Upper Culver local | FL | 101,339 | 129,961 | 8:00 AM | 10,638 |
| Upper Culver local | G | 38,257 | 45,538 | 8:00 AM | 3,513 |
| West End | D | 81,783 | 106,867 | 7:00 AM | 7,874 |
| West End | W | 69 | 89 | 10:00 AM | 44 |
| West End | R | 38 | 48 | 9:00 AM | 38 |
| White Plains Rd | 2 | 99,140 | 151,616 | 7:00 AM | 8,818 |
| White Plains Rd | 5 | 77,863 | 113,230 | 7:00 AM | 9,002 |
| White Plains Rd express | 5 | 20,693 | 30,757 | 7:00 AM | 4,620 |
| White Plains Rd local | 2 | 74,697 | 112,971 | 7:00 AM | 6,385 |
| White Plains Rd local | 5 | 33,016 | 47,140 | 3:00 PM | 4,520 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
