# Ridership by line and route

Average weekday riders with fare evaders, over 22 weekdays from 2025-09-16 to 2025-09-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Sep 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --by route --month 2025-09 --markdown-out src/mta_od_data/ridership/2025-09/by_line_and_route.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Route | Sep 2025 | 2019 | Peak Hour | Riders in Peak Hour, Sep 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| 4 Av | R | 147,697 | 182,513 | 8:00 AM | 15,381 |
| 4 Av | N | 97,170 | 110,780 | 7:00 AM | 8,323 |
| 4 Av | D | 78,058 | 100,695 | 8:00 AM | 6,860 |
| 4 Av | W | 1,768 | 2,128 | 7:00 AM | 929 |
| 4 Av express | N | 86,379 | 98,500 | 8:00 AM | 8,283 |
| 4 Av express | D | 65,822 | 85,206 | 8:00 AM | 6,860 |
| 4 Av local | R | 113,430 | 139,820 | 8:00 AM | 11,657 |
| 4 Av local | N | 12,415 | 14,074 | 5:00 AM | 2,034 |
| 4 Av local | D | 10,593 | 13,395 | 5:00 AM | 1,888 |
| 4 Av local | W | 1,217 | 1,430 | 7:00 AM | 556 |
| 42 St Shuttle | GS | 58,850 | 79,025 | 5:00 PM | 6,853 |
| 53 St | E | 275,025 | 356,387 | 5:00 PM | 29,004 |
| 53 St | M | 61,968 | 83,781 | 8:00 AM | 6,117 |
| 6 Av | F | 358,116 | 453,848 | 5:00 PM | 37,110 |
| 6 Av | FL | 352,931 | 447,165 | 5:00 PM | 34,402 |
| 6 Av | D | 191,727 | 260,895 | 5:00 PM | 18,488 |
| 6 Av | B | 162,710 | 212,899 | 5:00 PM | 19,121 |
| 6 Av | M | 124,417 | 168,907 | 5:00 PM | 12,866 |
| 6 Av | FX | 5,185 | 6,683 | 5:00 PM | 2,708 |
| 6 Av express | D | 142,240 | 193,964 | 8:00 AM | 14,010 |
| 6 Av express | B | 121,239 | 159,995 | 5:00 PM | 14,786 |
| 6 Av local | F | 246,006 | 314,784 | 5:00 PM | 25,797 |
| 6 Av local | FL | 242,713 | 310,492 | 5:00 PM | 23,732 |
| 6 Av local | M | 97,492 | 133,235 | 5:00 PM | 10,632 |
| 6 Av local | FX | 3,293 | 4,292 | 5:00 PM | 2,066 |
| 63 St | F | 203,391 | 259,986 | 5:00 PM | 19,452 |
| 63 St | FL | 202,084 | 258,286 | 5:00 PM | 18,973 |
| 63 St | Q | 108,311 | 141,600 | 8:00 AM | 11,255 |
| 63 St | N | 4,269 | 5,572 | 4:00 PM | 1,467 |
| 63 St | FX | 1,333 | 1,738 | 8:00 AM | 523 |
| 63 St | R | 480 | 625 | 7:00 AM | 480 |
| 8 Av | A | 358,657 | 493,814 | 5:00 PM | 39,232 |
| 8 Av | C | 208,125 | 269,097 | 6:00 PM | 17,322 |
| 8 Av | E | 188,189 | 245,977 | 5:00 PM | 20,043 |
| 8 Av | D | 90,106 | 134,067 | 8:00 AM | 7,399 |
| 8 Av | B | 79,285 | 102,890 | 5:00 PM | 10,042 |
| 8 Av express | A | 279,919 | 381,187 | 5:00 PM | 31,747 |
| 8 Av express | D | 90,106 | 134,067 | 8:00 AM | 7,399 |
| 8 Av local | E | 187,308 | 244,588 | 5:00 PM | 19,930 |
| 8 Av local | C | 174,784 | 223,748 | 6:00 PM | 15,188 |
| 8 Av local | B | 79,285 | 102,890 | 5:00 PM | 10,042 |
| 8 Av local | A | 23,802 | 31,341 | 11:00 PM | 10,914 |
| Astoria | N | 56,438 | 65,629 | 5:00 PM | 5,816 |
| Astoria | W | 48,461 | 57,030 | 8:00 AM | 5,827 |
| Brighton | Q | 160,854 | 211,506 | 8:00 AM | 14,414 |
| Brighton | B | 91,120 | 124,254 | 8:00 AM | 9,848 |
| Brighton express | B | 70,718 | 98,036 | 8:00 AM | 7,711 |
| Brighton local | Q | 115,906 | 153,083 | 8:00 AM | 10,500 |
| Broadway | R | 233,698 | 315,717 | 5:00 PM | 24,575 |
| Broadway | Q | 232,350 | 306,238 | 5:00 PM | 23,523 |
| Broadway | N | 207,925 | 257,582 | 5:00 PM | 20,008 |
| Broadway | W | 141,454 | 184,865 | 5:00 PM | 14,521 |
| Broadway express | Q | 226,605 | 298,718 | 5:00 PM | 23,523 |
| Broadway express | N | 113,473 | 139,286 | 4:00 PM | 12,657 |
| Broadway local | R | 151,125 | 206,419 | 5:00 PM | 15,870 |
| Broadway local | N | 121,238 | 149,263 | 5:00 PM | 10,952 |
| Broadway local | W | 115,767 | 153,531 | 5:00 PM | 11,690 |
| Broadway local | Q | 11,524 | 14,862 | 12:00 AM | 4,041 |
| Broadway-7 Av | 1 | 527,991 | 698,379 | 5:00 PM | 53,668 |
| Broadway-7 Av | 2 | 245,312 | 338,513 | 5:00 PM | 23,819 |
| Broadway-7 Av | 3 | 189,566 | 261,219 | 8:00 AM | 20,920 |
| Broadway-7 Av express | 2 | 216,847 | 299,420 | 5:00 PM | 21,330 |
| Broadway-7 Av express | 3 | 167,752 | 230,650 | 8:00 AM | 18,610 |
| Broadway-7 Av local | 1 | 392,754 | 519,379 | 5:00 PM | 38,979 |
| Broadway-7 Av local | 2 | 7,000 | 9,608 | 1:00 AM | 2,090 |
| Canarsie | L | 398,975 | 450,793 | 5:00 PM | 37,856 |
| Concourse | D | 83,432 | 133,041 | 3:00 PM | 6,727 |
| Concourse | B | 37,777 | 57,585 | 7:00 AM | 5,742 |
| Concourse express | D | 15,521 | 26,034 | 8:00 AM | 3,357 |
| Concourse express | B | 32 | 60 | 9:00 AM | 32 |
| Concourse local | D | 75,928 | 120,351 | 3:00 PM | 6,709 |
| Concourse local | B | 37,776 | 57,583 | 7:00 AM | 5,742 |
| Crosstown | G | 140,883 | 163,343 | 5:00 PM | 12,946 |
| Culver | F | 120,354 | 155,103 | 8:00 AM | 12,620 |
| Culver | FL | 117,708 | 151,561 | 8:00 AM | 12,620 |
| Culver | G | 49,381 | 58,511 | 5:00 PM | 4,420 |
| Culver | FX | 2,925 | 3,912 | 7:00 AM | 1,779 |
| Culver express | F | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Culver express | FX | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Culver local | F | 116,245 | 149,783 | 8:00 AM | 12,351 |
| Culver local | FL | 114,579 | 147,521 | 8:00 AM | 12,351 |
| Culver local | G | 40,063 | 47,666 | 8:00 AM | 3,690 |
| Culver local | FX | 1,686 | 2,287 | 7:00 AM | 1,053 |
| Dyre Av | 5 | 26,911 | 40,735 | 7:00 AM | 3,101 |
| Eastern Pkwy | 3 | 99,406 | 136,572 | 8:00 AM | 10,378 |
| Eastern Pkwy | 2 | 92,321 | 120,462 | 8:00 AM | 9,458 |
| Eastern Pkwy | 4 | 82,705 | 112,550 | 7:00 AM | 7,491 |
| Eastern Pkwy | 5 | 78,341 | 103,450 | 8:00 AM | 8,493 |
| Eastern Pkwy express | 4 | 79,658 | 108,440 | 7:00 AM | 7,471 |
| Eastern Pkwy express | 5 | 73,078 | 96,581 | 8:00 AM | 8,351 |
| Eastern Pkwy local | 3 | 73,486 | 100,337 | 8:00 AM | 7,169 |
| Eastern Pkwy local | 2 | 69,493 | 89,961 | 8:00 AM | 6,492 |
| Eastern Pkwy local | 4 | 7,457 | 10,162 | 5:00 AM | 2,015 |
| Eastern Pkwy local | 5 | 195 | 276 | 5:00 AM | 177 |
| Far Rockaway branch | A | 17,237 | 35,445 | 7:00 AM | 1,692 |
| Flushing | 7 | 515,082 | 590,342 | 5:00 PM | 57,286 |
| Flushing | 7L | 419,278 | 480,581 | 5:00 PM | 37,369 |
| Flushing | 7X | 99,719 | 114,274 | 5:00 PM | 19,917 |
| Flushing express | 7 | 39,903 | 45,323 | 5:00 PM | 6,923 |
| Flushing express | 7X | 39,903 | 45,323 | 5:00 PM | 6,923 |
| Flushing local | 7 | 237,014 | 262,691 | 7:00 AM | 17,320 |
| Flushing local | 7L | 237,014 | 262,691 | 7:00 AM | 17,320 |
| Franklin Av Shuttle | FS | 14,882 | 19,816 | 8:00 AM | 1,304 |
| Fulton St | A | 181,615 | 255,061 | 5:00 PM | 16,579 |
| Fulton St | C | 97,852 | 127,745 | 5:00 PM | 9,083 |
| Fulton St express | A | 143,508 | 203,978 | 5:00 PM | 14,364 |
| Fulton St local | C | 83,723 | 110,236 | 5:00 PM | 7,597 |
| Fulton St local | A | 15,067 | 20,797 | 11:00 PM | 3,878 |
| Hillside Av | F | 58,173 | 80,763 | 5:00 PM | 5,030 |
| Hillside Av | FL | 57,794 | 80,254 | 7:00 AM | 4,994 |
| Hillside Av | E | 2,485 | 3,568 | 7:00 AM | 975 |
| Hillside Av | FX | 379 | 509 | 8:00 AM | 161 |
| Hillside Av express | E | 2,316 | 3,333 | 7:00 AM | 975 |
| Hillside Av local | F | 58,173 | 80,763 | 5:00 PM | 5,030 |
| Hillside Av local | FL | 57,794 | 80,254 | 7:00 AM | 4,994 |
| Hillside Av local | FX | 379 | 509 | 8:00 AM | 161 |
| Hillside Av local | E | 169 | 235 | 8:00 PM | 169 |
| Jamaica | J | 136,918 | 185,000 | 4:00 PM | 10,743 |
| Jamaica | M | 58,868 | 78,676 | 8:00 AM | 6,123 |
| Jamaica | Z | 9,553 | 12,923 | 5:00 PM | 3,571 |
| Jamaica express | J | 24,314 | 33,294 | 9:00 AM | 3,219 |
| Jamaica express | Z | 4,352 | 5,949 | 8:00 AM | 1,996 |
| Jamaica local | J | 69,669 | 94,356 | 4:00 PM | 5,316 |
| Jamaica local | M | 51,615 | 68,467 | 8:00 AM | 5,324 |
| Jamaica local | Z | 4,598 | 6,301 | 8:00 AM | 1,640 |
| Jerome Av | 4 | 167,809 | 237,899 | 7:00 AM | 13,811 |
| Lefferts branch | A | 17,210 | 26,170 | 7:00 AM | 1,832 |
| Lenox Av | 2 | 99,911 | 146,880 | 8:00 AM | 8,769 |
| Lenox Av | 3 | 33,551 | 49,394 | 8:00 AM | 3,209 |
| Lexington Av | 6 | 501,470 | 655,243 | 8:00 AM | 48,860 |
| Lexington Av | 6L | 377,904 | 491,570 | 8:00 AM | 33,782 |
| Lexington Av | 4 | 353,340 | 481,618 | 5:00 PM | 32,930 |
| Lexington Av | 5 | 256,518 | 350,273 | 8:00 AM | 28,784 |
| Lexington Av | 6X | 124,501 | 164,869 | 8:00 AM | 15,078 |
| Lexington Av express | 4 | 293,840 | 395,016 | 5:00 PM | 27,193 |
| Lexington Av express | 5 | 220,518 | 297,212 | 8:00 AM | 24,630 |
| Lexington Av local | 6 | 501,470 | 655,243 | 8:00 AM | 48,860 |
| Lexington Av local | 6L | 377,904 | 491,570 | 8:00 AM | 33,782 |
| Lexington Av local | 6X | 124,501 | 164,869 | 8:00 AM | 15,078 |
| Lexington Av local | 4 | 7,093 | 9,456 | 5:00 AM | 1,495 |
| Lower Culver | F | 42,354 | 57,493 | 7:00 AM | 4,511 |
| Lower Culver | FL | 40,623 | 55,147 | 8:00 AM | 4,203 |
| Lower Culver | FX | 1,731 | 2,346 | 7:00 AM | 1,083 |
| Lower Culver local | F | 39,180 | 53,395 | 7:00 AM | 4,220 |
| Lower Culver local | FL | 37,494 | 51,107 | 8:00 AM | 3,934 |
| Lower Culver local | FX | 1,686 | 2,287 | 7:00 AM | 1,053 |
| Manhattan Bridge | Q | 108,317 | 141,514 | 8:00 AM | 11,548 |
| Manhattan Bridge | N | 72,637 | 85,580 | 5:00 PM | 7,323 |
| Manhattan Bridge | D | 61,414 | 78,618 | 5:00 PM | 5,509 |
| Manhattan Bridge | B | 59,271 | 78,656 | 5:00 PM | 6,511 |
| Myrtle Av | M | 50,185 | 63,090 | 8:00 AM | 4,531 |
| Nassau St | J | 61,626 | 85,603 | 4:00 PM | 4,601 |
| Nassau St | Z | 4,842 | 6,830 | 8:00 AM | 2,597 |
| Nostrand Av | 5 | 45,986 | 59,342 | 7:00 AM | 5,270 |
| Nostrand Av | 2 | 42,367 | 54,487 | 8:00 AM | 3,710 |
| Pelham | 6 | 132,255 | 192,126 | 7:00 AM | 14,577 |
| Pelham | 6L | 94,339 | 134,913 | 7:00 AM | 8,254 |
| Pelham | 6X | 42,237 | 63,363 | 7:00 AM | 6,323 |
| Pelham express | 6 | 37,172 | 55,888 | 7:00 AM | 5,577 |
| Pelham express | 6X | 37,172 | 55,888 | 7:00 AM | 5,577 |
| Pelham local | 6 | 84,128 | 120,483 | 7:00 AM | 7,303 |
| Pelham local | 6L | 84,128 | 120,483 | 7:00 AM | 7,303 |
| Queens Blvd | E | 246,208 | 304,768 | 5:00 PM | 22,513 |
| Queens Blvd | F | 197,765 | 254,521 | 5:00 PM | 18,325 |
| Queens Blvd | FL | 196,709 | 253,164 | 5:00 PM | 18,055 |
| Queens Blvd | R | 85,676 | 114,450 | 5:00 PM | 8,809 |
| Queens Blvd | M | 83,473 | 112,156 | 8:00 AM | 8,367 |
| Queens Blvd | FX | 1,056 | 1,357 | 8:00 AM | 468 |
| Queens Blvd east | E | 110,966 | 140,377 | 7:00 AM | 9,902 |
| Queens Blvd east | F | 85,777 | 118,242 | 8:00 AM | 8,028 |
| Queens Blvd east | FL | 85,188 | 117,450 | 8:00 AM | 7,770 |
| Queens Blvd east | FX | 589 | 792 | 8:00 AM | 258 |
| Queens Blvd express | E | 219,062 | 270,640 | 5:00 PM | 21,822 |
| Queens Blvd express | F | 84,390 | 114,403 | 5:00 PM | 8,313 |
| Queens Blvd express | FL | 83,841 | 113,683 | 5:00 PM | 8,140 |
| Queens Blvd express | FX | 548 | 720 | 8:00 AM | 256 |
| Queens Blvd local | F | 98,794 | 134,793 | 8:00 AM | 8,254 |
| Queens Blvd local | FL | 98,184 | 133,973 | 8:00 AM | 7,983 |
| Queens Blvd local | R | 85,676 | 114,450 | 5:00 PM | 8,809 |
| Queens Blvd local | M | 83,473 | 112,156 | 8:00 AM | 8,367 |
| Queens Blvd local | E | 34,018 | 42,295 | 10:00 PM | 4,915 |
| Queens Blvd local | FX | 610 | 820 | 8:00 AM | 271 |
| Queens Blvd west | E | 224,599 | 276,653 | 5:00 PM | 20,797 |
| Queens Blvd west | F | 99,671 | 134,015 | 5:00 PM | 8,313 |
| Queens Blvd west | FL | 99,122 | 133,296 | 5:00 PM | 8,140 |
| Queens Blvd west | R | 85,676 | 114,450 | 5:00 PM | 8,809 |
| Queens Blvd west | M | 83,473 | 112,156 | 8:00 AM | 8,367 |
| Queens Blvd west | FX | 548 | 720 | 8:00 AM | 256 |
| Queens Blvd west express | E | 209,505 | 258,056 | 5:00 PM | 20,797 |
| Queens Blvd west express | F | 84,390 | 114,403 | 5:00 PM | 8,313 |
| Queens Blvd west express | FL | 83,841 | 113,683 | 5:00 PM | 8,140 |
| Queens Blvd west express | FX | 548 | 720 | 8:00 AM | 256 |
| Queens Blvd west local | R | 85,676 | 114,450 | 5:00 PM | 8,809 |
| Queens Blvd west local | M | 83,473 | 112,156 | 8:00 AM | 8,367 |
| Queens Blvd west local | F | 15,311 | 19,654 | 10:00 PM | 4,677 |
| Queens Blvd west local | FL | 15,311 | 19,654 | 10:00 PM | 4,677 |
| Queens Blvd west local | E | 15,219 | 18,769 | 10:00 PM | 3,918 |
| Rockaway | A | 29,252 | 52,113 | 7:00 AM | 2,612 |
| Rockaway | H | 3,263 | 6,446 | 4:00 PM | 285 |
| Rockaway Park branch | H | 3,263 | 6,446 | 4:00 PM | 285 |
| Rockaway Park branch | A | 449 | 889 | 7:00 AM | 154 |
| SAS Phase 1 | Q | 148,142 | 192,267 | 8:00 AM | 15,453 |
| SAS Phase 1 | N | 5,744 | 7,469 | 4:00 PM | 2,723 |
| SAS Phase 1 | R | 828 | 1,062 | 7:00 AM | 828 |
| Sea Beach | N | 82,196 | 90,241 | 7:00 AM | 7,589 |
| Sea Beach | W | 545 | 588 | 7:00 AM | 305 |
| Upper Culver | F | 109,065 | 139,843 | 8:00 AM | 11,661 |
| Upper Culver | FL | 106,661 | 136,617 | 8:00 AM | 11,661 |
| Upper Culver | G | 40,063 | 47,666 | 8:00 AM | 3,690 |
| Upper Culver | FX | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Upper Culver express | F | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Upper Culver express | FX | 2,682 | 3,593 | 7:00 AM | 1,594 |
| Upper Culver local | F | 106,661 | 136,617 | 8:00 AM | 11,661 |
| Upper Culver local | FL | 106,661 | 136,617 | 8:00 AM | 11,661 |
| Upper Culver local | G | 40,063 | 47,666 | 8:00 AM | 3,690 |
| West End | D | 85,251 | 111,295 | 7:00 AM | 8,642 |
| West End | W | 74 | 94 | 10:00 AM | 51 |
| West End | R | 36 | 46 | 9:00 AM | 36 |
| White Plains Rd | 2 | 104,012 | 158,901 | 7:00 AM | 9,832 |
| White Plains Rd | 5 | 82,709 | 120,220 | 7:00 AM | 9,946 |
| White Plains Rd express | 5 | 22,339 | 33,215 | 7:00 AM | 5,088 |
| White Plains Rd local | 2 | 78,485 | 118,561 | 7:00 AM | 7,140 |
| White Plains Rd local | 5 | 34,933 | 49,824 | 3:00 PM | 4,889 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
