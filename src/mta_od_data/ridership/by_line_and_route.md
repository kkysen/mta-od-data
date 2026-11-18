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
| 4 Av | R | 145,122 | 179,640 | 8:00 AM | 14,744 |
| 4 Av | N | 93,015 | 106,049 | 8:00 AM | 7,654 |
| 4 Av | D | 77,171 | 99,558 | 5:00 PM | 6,798 |
| 4 Av | W | 1,602 | 1,935 | 7:00 AM | 793 |
| 4 Av express | N | 82,344 | 93,873 | 8:00 AM | 7,654 |
| 4 Av express | D | 65,808 | 85,143 | 5:00 PM | 6,798 |
| 4 Av local | R | 111,858 | 138,043 | 5:00 PM | 11,200 |
| 4 Av local | N | 12,195 | 13,855 | 5:00 AM | 1,973 |
| 4 Av local | D | 9,532 | 12,075 | 5:00 AM | 1,841 |
| 4 Av local | W | 1,124 | 1,325 | 7:00 AM | 466 |
| 42 St Shuttle | GS | 58,625 | 78,759 | 5:00 PM | 6,679 |
| 53 St | E | 257,886 | 335,370 | 5:00 PM | 26,760 |
| 53 St | M | 47,018 | 63,702 | 8:00 AM | 4,482 |
| 53 St | F | 39,192 | 51,182 | 5:00 PM | 4,146 |
| 53 St | FL | 38,907 | 50,806 | 5:00 PM | 4,067 |
| 53 St | FX | 285 | 376 | 8:00 AM | 108 |
| 6 Av | F | 353,195 | 449,917 | 5:00 PM | 36,248 |
| 6 Av | FL | 348,458 | 443,762 | 5:00 PM | 33,854 |
| 6 Av | D | 192,840 | 262,889 | 5:00 PM | 18,382 |
| 6 Av | B | 158,466 | 207,506 | 5:00 PM | 18,239 |
| 6 Av | M | 125,723 | 169,591 | 5:00 PM | 12,816 |
| 6 Av | FX | 4,737 | 6,154 | 5:00 PM | 2,393 |
| 6 Av express | D | 143,113 | 195,441 | 5:00 PM | 13,890 |
| 6 Av express | B | 118,252 | 156,197 | 5:00 PM | 13,852 |
| 6 Av local | F | 243,510 | 313,817 | 5:00 PM | 25,197 |
| 6 Av local | FL | 240,407 | 309,725 | 5:00 PM | 23,350 |
| 6 Av local | M | 97,885 | 132,826 | 5:00 PM | 10,449 |
| 6 Av local | FX | 3,103 | 4,092 | 5:00 PM | 1,846 |
| 63 St | F | 157,099 | 201,110 | 5:00 PM | 14,566 |
| 63 St | FL | 156,134 | 199,854 | 5:00 PM | 14,211 |
| 63 St | Q | 103,979 | 136,183 | 8:00 AM | 10,281 |
| 63 St | M | 18,076 | 23,421 | 5:00 PM | 1,691 |
| 63 St | N | 4,121 | 5,387 | 4:00 PM | 1,422 |
| 63 St | FX | 984 | 1,283 | 8:00 AM | 381 |
| 63 St | R | 460 | 600 | 7:00 AM | 460 |
| 8 Av | A | 350,237 | 482,372 | 5:00 PM | 36,823 |
| 8 Av | C | 188,501 | 243,741 | 5:00 PM | 15,276 |
| 8 Av | E | 186,161 | 243,666 | 5:00 PM | 19,704 |
| 8 Av | D | 87,058 | 130,188 | 4:00 PM | 6,540 |
| 8 Av | B | 75,198 | 97,227 | 5:00 PM | 9,059 |
| 8 Av express | A | 274,518 | 374,041 | 5:00 PM | 29,321 |
| 8 Av express | D | 87,058 | 130,188 | 4:00 PM | 6,540 |
| 8 Av local | E | 185,265 | 242,253 | 5:00 PM | 19,596 |
| 8 Av local | C | 156,914 | 200,710 | 6:00 PM | 13,110 |
| 8 Av local | B | 75,198 | 97,227 | 5:00 PM | 9,059 |
| 8 Av local | A | 22,038 | 29,043 | 11:00 PM | 9,979 |
| Astoria | N | 54,470 | 63,397 | 5:00 PM | 5,597 |
| Astoria | W | 46,553 | 54,825 | 8:00 AM | 5,401 |
| Brighton | Q | 153,902 | 202,687 | 8:00 AM | 13,306 |
| Brighton | B | 86,828 | 118,407 | 8:00 AM | 9,143 |
| Brighton express | B | 66,723 | 92,670 | 8:00 AM | 7,156 |
| Brighton local | Q | 108,230 | 143,414 | 8:00 AM | 9,748 |
| Broadway | R | 230,845 | 312,032 | 5:00 PM | 24,334 |
| Broadway | Q | 226,358 | 298,958 | 5:00 PM | 22,601 |
| Broadway | N | 205,634 | 255,458 | 5:00 PM | 19,672 |
| Broadway | W | 141,570 | 185,304 | 5:00 PM | 14,408 |
| Broadway express | Q | 220,581 | 291,380 | 5:00 PM | 22,601 |
| Broadway express | N | 111,461 | 137,375 | 4:00 PM | 12,812 |
| Broadway local | R | 152,055 | 207,711 | 5:00 PM | 15,984 |
| Broadway local | N | 121,916 | 150,364 | 5:00 PM | 10,943 |
| Broadway local | W | 117,336 | 155,758 | 5:00 PM | 11,744 |
| Broadway local | Q | 11,545 | 14,926 | 12:00 AM | 4,120 |
| Broadway-7 Av | 1 | 518,591 | 687,464 | 5:00 PM | 52,207 |
| Broadway-7 Av | 2 | 237,271 | 327,827 | 5:00 PM | 22,879 |
| Broadway-7 Av | 3 | 183,112 | 252,559 | 5:00 PM | 19,567 |
| Broadway-7 Av express | 2 | 210,055 | 290,354 | 5:00 PM | 20,409 |
| Broadway-7 Av express | 3 | 162,480 | 223,581 | 5:00 PM | 17,217 |
| Broadway-7 Av local | 1 | 389,122 | 515,636 | 5:00 PM | 38,183 |
| Broadway-7 Av local | 2 | 6,773 | 9,334 | 1:00 AM | 2,051 |
| Canarsie | L | 381,254 | 431,152 | 5:00 PM | 35,918 |
| Concourse | D | 79,641 | 127,706 | 3:00 PM | 6,167 |
| Concourse | B | 34,367 | 52,751 | 5:00 PM | 4,979 |
| Concourse express | D | 14,817 | 24,868 | 7:00 AM | 3,218 |
| Concourse express | B | 46 | 85 | 9:00 AM | 46 |
| Concourse local | D | 72,313 | 115,323 | 3:00 PM | 6,150 |
| Concourse local | B | 34,365 | 52,747 | 5:00 PM | 4,979 |
| Crosstown | G | 132,699 | 154,068 | 5:00 PM | 12,288 |
| Culver | F | 113,985 | 147,064 | 8:00 AM | 11,555 |
| Culver | FL | 111,599 | 143,866 | 8:00 AM | 11,555 |
| Culver | G | 47,338 | 56,126 | 5:00 PM | 4,204 |
| Culver | FX | 2,608 | 3,491 | 7:00 AM | 1,580 |
| Culver express | F | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Culver express | FX | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Culver local | F | 110,205 | 142,164 | 8:00 AM | 11,299 |
| Culver local | FL | 108,688 | 140,105 | 8:00 AM | 11,299 |
| Culver local | G | 38,437 | 45,761 | 8:00 AM | 3,532 |
| Culver local | FX | 1,535 | 2,082 | 7:00 AM | 963 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,769 |
| Eastern Pkwy | 3 | 95,735 | 131,689 | 8:00 AM | 9,593 |
| Eastern Pkwy | 2 | 87,321 | 114,086 | 8:00 AM | 8,707 |
| Eastern Pkwy | 4 | 80,936 | 110,193 | 7:00 AM | 6,962 |
| Eastern Pkwy | 5 | 74,664 | 98,660 | 8:00 AM | 7,932 |
| Eastern Pkwy express | 4 | 77,402 | 105,397 | 7:00 AM | 6,943 |
| Eastern Pkwy express | 5 | 69,927 | 92,470 | 8:00 AM | 7,815 |
| Eastern Pkwy local | 3 | 71,124 | 97,285 | 8:00 AM | 6,647 |
| Eastern Pkwy local | 2 | 65,861 | 85,433 | 8:00 AM | 6,010 |
| Eastern Pkwy local | 4 | 8,034 | 11,032 | 5:00 AM | 1,896 |
| Eastern Pkwy local | 5 | 177 | 253 | 5:00 AM | 162 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Flushing | 7 | 488,276 | 561,370 | 5:00 PM | 54,222 |
| Flushing | 7L | 399,318 | 459,200 | 5:00 PM | 36,165 |
| Flushing | 7X | 92,590 | 106,359 | 5:00 PM | 18,057 |
| Flushing express | 7 | 35,641 | 40,885 | 5:00 PM | 6,084 |
| Flushing express | 7X | 35,641 | 40,885 | 5:00 PM | 6,084 |
| Flushing local | 7 | 220,808 | 246,208 | 4:00 PM | 16,264 |
| Flushing local | 7L | 220,808 | 246,208 | 4:00 PM | 16,264 |
| Franklin Av Shuttle | FS | 13,566 | 18,097 | 8:00 AM | 1,197 |
| Fulton St | A | 174,226 | 244,640 | 5:00 PM | 16,345 |
| Fulton St | C | 89,601 | 117,201 | 5:00 PM | 8,113 |
| Fulton St express | A | 137,157 | 195,011 | 5:00 PM | 13,785 |
| Fulton St local | C | 77,549 | 102,265 | 5:00 PM | 6,968 |
| Fulton St local | A | 14,225 | 19,699 | 11:00 PM | 3,821 |
| Hillside Av | F | 55,520 | 77,159 | 5:00 PM | 4,802 |
| Hillside Av | FL | 55,149 | 76,658 | 5:00 PM | 4,734 |
| Hillside Av | E | 2,324 | 3,334 | 7:00 AM | 910 |
| Hillside Av | FX | 371 | 500 | 8:00 AM | 157 |
| Hillside Av express | E | 2,169 | 3,118 | 7:00 AM | 910 |
| Hillside Av local | F | 55,520 | 77,159 | 5:00 PM | 4,802 |
| Hillside Av local | FL | 55,149 | 76,658 | 5:00 PM | 4,734 |
| Hillside Av local | FX | 371 | 500 | 8:00 AM | 157 |
| Hillside Av local | E | 155 | 216 | 8:00 PM | 155 |
| Jamaica | J | 131,242 | 177,673 | 4:00 PM | 10,487 |
| Jamaica | M | 56,448 | 75,492 | 8:00 AM | 5,674 |
| Jamaica | Z | 9,043 | 12,255 | 5:00 PM | 3,410 |
| Jamaica express | J | 22,922 | 31,408 | 9:00 AM | 3,025 |
| Jamaica express | Z | 4,046 | 5,544 | 8:00 AM | 1,836 |
| Jamaica local | J | 66,718 | 90,413 | 4:00 PM | 5,148 |
| Jamaica local | M | 49,243 | 65,338 | 8:00 AM | 4,974 |
| Jamaica local | Z | 4,318 | 5,932 | 8:00 AM | 1,538 |
| Jerome Av | 4 | 155,622 | 221,499 | 4:00 PM | 12,745 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Lenox Av | 2 | 96,690 | 142,297 | 8:00 AM | 8,365 |
| Lenox Av | 3 | 32,770 | 48,260 | 8:00 AM | 2,989 |
| Lexington Av | 6 | 483,878 | 632,827 | 5:00 PM | 46,242 |
| Lexington Av | 6L | 365,096 | 475,291 | 5:00 PM | 31,798 |
| Lexington Av | 4 | 334,154 | 456,055 | 5:00 PM | 30,915 |
| Lexington Av | 5 | 243,739 | 333,202 | 8:00 AM | 25,923 |
| Lexington Av | 6X | 119,625 | 158,617 | 5:00 PM | 14,444 |
| Lexington Av express | 4 | 277,233 | 373,185 | 5:00 PM | 25,582 |
| Lexington Av express | 5 | 209,762 | 283,134 | 5:00 PM | 22,389 |
| Lexington Av local | 6 | 483,878 | 632,827 | 5:00 PM | 46,242 |
| Lexington Av local | 6L | 365,096 | 475,291 | 5:00 PM | 31,798 |
| Lexington Av local | 6X | 119,625 | 158,617 | 5:00 PM | 14,444 |
| Lexington Av local | 4 | 7,036 | 9,403 | 5:00 AM | 1,497 |
| Lower Culver | F | 39,712 | 54,014 | 7:00 AM | 4,121 |
| Lower Culver | FL | 38,134 | 51,877 | 8:00 AM | 3,949 |
| Lower Culver | FX | 1,577 | 2,137 | 7:00 AM | 989 |
| Lower Culver local | F | 36,758 | 50,197 | 7:00 AM | 3,862 |
| Lower Culver local | FL | 35,223 | 48,115 | 8:00 AM | 3,693 |
| Lower Culver local | FX | 1,535 | 2,082 | 7:00 AM | 963 |
| Manhattan Bridge | Q | 103,423 | 135,290 | 8:00 AM | 10,314 |
| Manhattan Bridge | N | 70,504 | 83,380 | 5:00 PM | 7,264 |
| Manhattan Bridge | D | 60,624 | 77,776 | 5:00 PM | 5,475 |
| Manhattan Bridge | B | 56,668 | 75,208 | 5:00 PM | 6,190 |
| Myrtle Av | M | 47,944 | 60,350 | 8:00 AM | 4,214 |
| Nassau St | J | 58,876 | 81,792 | 4:00 PM | 4,482 |
| Nassau St | Z | 4,541 | 6,408 | 8:00 AM | 2,406 |
| Nostrand Av | 5 | 43,598 | 56,292 | 7:00 AM | 4,812 |
| Nostrand Av | 2 | 40,014 | 51,530 | 8:00 AM | 3,406 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,444 |
| Pelham | 6L | 90,198 | 129,152 | 7:00 AM | 7,382 |
| Pelham | 6X | 41,117 | 61,643 | 7:00 AM | 6,062 |
| Pelham express | 6 | 36,606 | 54,964 | 7:00 AM | 5,357 |
| Pelham express | 6X | 36,560 | 54,890 | 7:00 AM | 5,357 |
| Pelham express | 6L | 46 | 74 | 9:00 PM | 35 |
| Pelham local | 6 | 80,730 | 115,750 | 7:00 AM | 6,539 |
| Pelham local | 6L | 80,730 | 115,750 | 7:00 AM | 6,539 |
| Queens Blvd | E | 228,582 | 283,565 | 5:00 PM | 20,866 |
| Queens Blvd | F | 190,366 | 245,713 | 5:00 PM | 17,349 |
| Queens Blvd | FL | 189,320 | 244,366 | 5:00 PM | 17,087 |
| Queens Blvd | M | 84,472 | 113,011 | 8:00 AM | 8,198 |
| Queens Blvd | R | 82,517 | 110,416 | 5:00 PM | 8,588 |
| Queens Blvd | FX | 1,046 | 1,347 | 8:00 AM | 446 |
| Queens Blvd east | E | 105,346 | 133,311 | 7:00 AM | 9,255 |
| Queens Blvd east | F | 82,185 | 113,473 | 8:00 AM | 7,564 |
| Queens Blvd east | FL | 81,614 | 112,705 | 8:00 AM | 7,315 |
| Queens Blvd east | FX | 570 | 768 | 8:00 AM | 248 |
| Queens Blvd express | E | 202,134 | 250,188 | 5:00 PM | 20,210 |
| Queens Blvd express | F | 98,257 | 130,941 | 5:00 PM | 9,562 |
| Queens Blvd express | FL | 97,625 | 130,121 | 5:00 PM | 9,374 |
| Queens Blvd express | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd local | F | 94,687 | 129,437 | 8:00 AM | 7,788 |
| Queens Blvd local | FL | 94,096 | 128,641 | 8:00 AM | 7,528 |
| Queens Blvd local | M | 83,994 | 112,295 | 8:00 AM | 8,134 |
| Queens Blvd local | R | 82,517 | 110,416 | 5:00 PM | 8,588 |
| Queens Blvd local | E | 32,843 | 40,962 | 10:00 PM | 4,801 |
| Queens Blvd local | FX | 592 | 797 | 8:00 AM | 261 |
| Queens Blvd west | E | 207,725 | 256,412 | 5:00 PM | 19,191 |
| Queens Blvd west | F | 113,074 | 150,068 | 5:00 PM | 9,562 |
| Queens Blvd west | FL | 112,443 | 149,247 | 5:00 PM | 9,374 |
| Queens Blvd west | M | 83,994 | 112,295 | 8:00 AM | 8,134 |
| Queens Blvd west | R | 82,517 | 110,416 | 5:00 PM | 8,588 |
| Queens Blvd west | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd west express | E | 192,757 | 237,846 | 5:00 PM | 19,191 |
| Queens Blvd west express | F | 98,257 | 130,941 | 5:00 PM | 9,562 |
| Queens Blvd west express | FL | 97,625 | 130,121 | 5:00 PM | 9,374 |
| Queens Blvd west express | FX | 631 | 821 | 8:00 AM | 271 |
| Queens Blvd west local | M | 83,994 | 112,295 | 8:00 AM | 8,134 |
| Queens Blvd west local | R | 82,517 | 110,416 | 5:00 PM | 8,588 |
| Queens Blvd west local | E | 15,081 | 18,723 | 10:00 PM | 3,846 |
| Queens Blvd west local | F | 14,847 | 19,165 | 10:00 PM | 4,481 |
| Queens Blvd west local | FL | 14,847 | 19,165 | 10:00 PM | 4,481 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,437 |
| Rockaway | H | 2,777 | 5,430 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,777 | 5,430 | 4:00 PM | 242 |
| Rockaway Park branch | A | 425 | 836 | 7:00 AM | 150 |
| SAS Phase 1 | Q | 141,520 | 184,042 | 8:00 AM | 14,169 |
| SAS Phase 1 | N | 5,522 | 7,187 | 4:00 PM | 2,643 |
| SAS Phase 1 | R | 788 | 1,011 | 7:00 AM | 788 |
| Sea Beach | N | 78,473 | 86,197 | 5:00 PM | 7,326 |
| Sea Beach | W | 496 | 534 | 7:00 AM | 279 |
| Upper Culver | F | 103,423 | 132,763 | 8:00 AM | 10,629 |
| Upper Culver | FL | 101,267 | 129,869 | 8:00 AM | 10,629 |
| Upper Culver | G | 38,437 | 45,761 | 8:00 AM | 3,532 |
| Upper Culver | FX | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Upper Culver express | F | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Upper Culver express | FX | 2,376 | 3,185 | 7:00 AM | 1,406 |
| Upper Culver local | F | 101,267 | 129,869 | 8:00 AM | 10,629 |
| Upper Culver local | FL | 101,267 | 129,869 | 8:00 AM | 10,629 |
| Upper Culver local | G | 38,437 | 45,761 | 8:00 AM | 3,532 |
| West End | D | 81,809 | 106,901 | 7:00 AM | 7,878 |
| West End | W | 71 | 90 | 10:00 AM | 45 |
| West End | R | 38 | 48 | 9:00 AM | 38 |
| White Plains Rd | 2 | 99,126 | 151,594 | 7:00 AM | 8,819 |
| White Plains Rd | 5 | 77,882 | 113,260 | 7:00 AM | 9,000 |
| White Plains Rd express | 5 | 20,698 | 30,764 | 7:00 AM | 4,622 |
| White Plains Rd local | 2 | 74,682 | 112,947 | 7:00 AM | 6,384 |
| White Plains Rd local | 5 | 33,027 | 47,157 | 3:00 PM | 4,522 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
