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
| 4 Av | R | 148,655 | 183,940 | 8:00 AM | 15,604 |
| 4 Av | N | 96,993 | 110,519 | 7:00 AM | 8,399 |
| 4 Av | D | 78,848 | 101,717 | 8:00 AM | 6,906 |
| 4 Av | W | 1,870 | 2,275 | 7:00 AM | 1,031 |
| 4 Av express | N | 86,144 | 98,165 | 7:00 AM | 8,343 |
| 4 Av express | D | 66,467 | 86,035 | 8:00 AM | 6,906 |
| 4 Av local | R | 113,683 | 140,192 | 8:00 AM | 11,708 |
| 4 Av local | N | 12,415 | 14,074 | 5:00 AM | 2,030 |
| 4 Av local | D | 10,616 | 13,422 | 5:00 AM | 1,904 |
| 4 Av local | W | 1,222 | 1,440 | 7:00 AM | 560 |
| 42 St Shuttle | GS | 58,713 | 78,840 | 5:00 PM | 6,827 |
| 53 St | E | 274,844 | 356,144 | 5:00 PM | 28,987 |
| 53 St | M | 61,957 | 83,760 | 8:00 AM | 6,117 |
| 6 Av | F | 357,548 | 453,086 | 5:00 PM | 36,995 |
| 6 Av | FL | 352,394 | 446,444 | 5:00 PM | 34,314 |
| 6 Av | D | 191,707 | 260,879 | 5:00 PM | 18,551 |
| 6 Av | B | 162,245 | 212,240 | 5:00 PM | 19,055 |
| 6 Av | M | 124,446 | 168,943 | 6:00 PM | 12,875 |
| 6 Av | FX | 5,154 | 6,642 | 5:00 PM | 2,681 |
| 6 Av express | D | 142,326 | 194,093 | 8:00 AM | 14,107 |
| 6 Av express | B | 120,888 | 159,485 | 5:00 PM | 14,736 |
| 6 Av local | F | 245,822 | 314,537 | 5:00 PM | 25,771 |
| 6 Av local | FL | 242,537 | 310,256 | 5:00 PM | 23,711 |
| 6 Av local | M | 97,534 | 133,293 | 5:00 PM | 10,630 |
| 6 Av local | FX | 3,285 | 4,282 | 5:00 PM | 2,060 |
| 63 St | F | 203,245 | 259,784 | 5:00 PM | 19,426 |
| 63 St | FL | 201,945 | 258,095 | 5:00 PM | 18,954 |
| 63 St | Q | 108,366 | 141,675 | 8:00 AM | 11,255 |
| 63 St | N | 4,275 | 5,579 | 4:00 PM | 1,470 |
| 63 St | FX | 1,325 | 1,727 | 8:00 AM | 523 |
| 63 St | R | 480 | 625 | 7:00 AM | 480 |
| 8 Av | A | 359,063 | 494,391 | 5:00 PM | 39,493 |
| 8 Av | C | 208,188 | 269,205 | 6:00 PM | 17,305 |
| 8 Av | E | 188,077 | 245,819 | 5:00 PM | 20,033 |
| 8 Av | D | 90,163 | 134,153 | 8:00 AM | 7,408 |
| 8 Av | B | 79,295 | 102,900 | 5:00 PM | 10,042 |
| 8 Av express | A | 279,682 | 380,876 | 5:00 PM | 31,669 |
| 8 Av express | D | 90,163 | 134,153 | 8:00 AM | 7,408 |
| 8 Av local | E | 187,197 | 244,433 | 5:00 PM | 19,921 |
| 8 Av local | C | 174,665 | 223,604 | 6:00 PM | 15,185 |
| 8 Av local | B | 79,295 | 102,900 | 5:00 PM | 10,042 |
| 8 Av local | A | 23,795 | 31,333 | 11:00 PM | 10,905 |
| Astoria | N | 56,433 | 65,623 | 5:00 PM | 5,817 |
| Astoria | W | 48,467 | 57,036 | 8:00 AM | 5,827 |
| Brighton | Q | 162,849 | 213,920 | 8:00 AM | 14,347 |
| Brighton | B | 91,546 | 124,681 | 8:00 AM | 9,770 |
| Brighton express | B | 70,951 | 98,341 | 8:00 AM | 7,714 |
| Brighton local | Q | 115,737 | 152,859 | 8:00 AM | 10,516 |
| Broadway | Q | 232,462 | 306,362 | 5:00 PM | 23,472 |
| Broadway | R | 232,425 | 313,980 | 5:00 PM | 24,422 |
| Broadway | N | 207,862 | 257,661 | 5:00 PM | 20,044 |
| Broadway | W | 141,377 | 184,743 | 5:00 PM | 14,513 |
| Broadway express | Q | 226,717 | 298,844 | 5:00 PM | 23,472 |
| Broadway express | N | 113,572 | 139,574 | 4:00 PM | 12,627 |
| Broadway local | R | 150,690 | 205,801 | 5:00 PM | 15,796 |
| Broadway local | N | 121,335 | 149,410 | 5:00 PM | 10,974 |
| Broadway local | W | 115,645 | 153,352 | 5:00 PM | 11,683 |
| Broadway local | Q | 11,523 | 14,857 | 12:00 AM | 4,048 |
| Broadway-7 Av | 1 | 527,874 | 698,232 | 5:00 PM | 53,654 |
| Broadway-7 Av | 2 | 245,476 | 338,767 | 5:00 PM | 23,968 |
| Broadway-7 Av | 3 | 189,558 | 261,228 | 8:00 AM | 20,876 |
| Broadway-7 Av express | 2 | 216,596 | 299,066 | 5:00 PM | 21,309 |
| Broadway-7 Av express | 3 | 167,488 | 230,295 | 8:00 AM | 18,582 |
| Broadway-7 Av local | 1 | 392,697 | 519,309 | 5:00 PM | 38,965 |
| Broadway-7 Av local | 2 | 6,994 | 9,601 | 1:00 AM | 2,090 |
| Canarsie | L | 399,125 | 451,005 | 5:00 PM | 37,816 |
| Concourse | D | 83,414 | 133,020 | 3:00 PM | 6,728 |
| Concourse | B | 37,758 | 57,557 | 7:00 AM | 5,738 |
| Concourse express | D | 15,523 | 26,037 | 8:00 AM | 3,358 |
| Concourse express | B | 32 | 60 | 9:00 AM | 32 |
| Concourse local | D | 75,908 | 120,327 | 3:00 PM | 6,710 |
| Concourse local | B | 37,756 | 57,555 | 7:00 AM | 5,738 |
| Crosstown | G | 140,802 | 163,253 | 5:00 PM | 12,938 |
| Culver | F | 120,205 | 154,911 | 8:00 AM | 12,604 |
| Culver | FL | 117,566 | 151,378 | 8:00 AM | 12,604 |
| Culver | G | 49,581 | 58,758 | 5:00 PM | 4,459 |
| Culver | FX | 2,918 | 3,902 | 7:00 AM | 1,775 |
| Culver express | F | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Culver express | FX | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Culver local | F | 116,104 | 149,603 | 8:00 AM | 12,336 |
| Culver local | FL | 114,443 | 147,347 | 8:00 AM | 12,336 |
| Culver local | G | 40,281 | 47,933 | 8:00 AM | 3,715 |
| Culver local | FX | 1,681 | 2,281 | 7:00 AM | 1,051 |
| Dyre Av | 5 | 26,911 | 40,735 | 7:00 AM | 3,101 |
| Eastern Pkwy | 3 | 100,062 | 137,440 | 8:00 AM | 10,316 |
| Eastern Pkwy | 2 | 92,342 | 120,592 | 8:00 AM | 9,521 |
| Eastern Pkwy | 4 | 83,720 | 113,750 | 7:00 AM | 7,579 |
| Eastern Pkwy | 5 | 78,846 | 104,056 | 8:00 AM | 8,555 |
| Eastern Pkwy express | 4 | 80,576 | 109,513 | 7:00 AM | 7,559 |
| Eastern Pkwy express | 5 | 73,649 | 97,269 | 8:00 AM | 8,433 |
| Eastern Pkwy local | 3 | 74,224 | 101,324 | 8:00 AM | 7,145 |
| Eastern Pkwy local | 2 | 69,471 | 90,042 | 8:00 AM | 6,590 |
| Eastern Pkwy local | 4 | 7,479 | 10,186 | 5:00 AM | 2,011 |
| Eastern Pkwy local | 5 | 192 | 274 | 5:00 AM | 174 |
| Far Rockaway branch | A | 17,237 | 35,445 | 7:00 AM | 1,692 |
| Flushing | 7 | 514,888 | 590,090 | 5:00 PM | 57,255 |
| Flushing | 7L | 419,110 | 480,362 | 5:00 PM | 37,341 |
| Flushing | 7X | 99,694 | 114,243 | 5:00 PM | 19,913 |
| Flushing express | 7 | 39,908 | 45,329 | 5:00 PM | 6,923 |
| Flushing express | 7X | 39,908 | 45,329 | 5:00 PM | 6,923 |
| Flushing local | 7 | 237,008 | 262,683 | 7:00 AM | 17,320 |
| Flushing local | 7L | 237,008 | 262,683 | 7:00 AM | 17,320 |
| Franklin Av Shuttle | FS | 14,667 | 19,538 | 8:00 AM | 1,281 |
| Fulton St | A | 181,556 | 254,971 | 5:00 PM | 16,714 |
| Fulton St | C | 97,647 | 127,489 | 5:00 PM | 9,043 |
| Fulton St express | A | 143,453 | 203,899 | 5:00 PM | 14,465 |
| Fulton St local | C | 83,556 | 110,025 | 5:00 PM | 7,563 |
| Fulton St local | A | 15,027 | 20,742 | 11:00 PM | 3,876 |
| Hillside Av | F | 58,173 | 80,763 | 5:00 PM | 5,030 |
| Hillside Av | FL | 57,794 | 80,254 | 7:00 AM | 4,994 |
| Hillside Av | E | 2,485 | 3,569 | 7:00 AM | 976 |
| Hillside Av | FX | 379 | 509 | 8:00 AM | 161 |
| Hillside Av express | E | 2,316 | 3,333 | 7:00 AM | 976 |
| Hillside Av local | F | 58,173 | 80,763 | 5:00 PM | 5,030 |
| Hillside Av local | FL | 57,794 | 80,254 | 7:00 AM | 4,994 |
| Hillside Av local | FX | 379 | 509 | 8:00 AM | 161 |
| Hillside Av local | E | 169 | 235 | 8:00 PM | 169 |
| Jamaica | J | 137,084 | 185,203 | 4:00 PM | 10,752 |
| Jamaica | M | 58,768 | 78,541 | 8:00 AM | 6,117 |
| Jamaica | Z | 9,624 | 13,020 | 5:00 PM | 3,562 |
| Jamaica express | J | 24,310 | 33,280 | 9:00 AM | 3,211 |
| Jamaica express | Z | 4,364 | 5,970 | 8:00 AM | 1,996 |
| Jamaica local | J | 69,577 | 94,197 | 4:00 PM | 5,316 |
| Jamaica local | M | 51,513 | 68,331 | 8:00 AM | 5,317 |
| Jamaica local | Z | 4,632 | 6,354 | 8:00 AM | 1,642 |
| Jerome Av | 4 | 167,827 | 237,917 | 7:00 AM | 13,809 |
| Lefferts branch | A | 17,210 | 26,170 | 7:00 AM | 1,832 |
| Lenox Av | 2 | 99,867 | 146,812 | 8:00 AM | 8,763 |
| Lenox Av | 3 | 33,544 | 49,385 | 8:00 AM | 3,210 |
| Lexington Av | 6 | 500,932 | 654,575 | 8:00 AM | 48,771 |
| Lexington Av | 6L | 377,466 | 491,031 | 8:00 AM | 33,693 |
| Lexington Av | 4 | 354,168 | 482,672 | 5:00 PM | 33,245 |
| Lexington Av | 5 | 256,155 | 349,858 | 8:00 AM | 28,566 |
| Lexington Av | 6X | 124,400 | 164,739 | 8:00 AM | 15,078 |
| Lexington Av express | 4 | 294,752 | 396,190 | 5:00 PM | 27,479 |
| Lexington Av express | 5 | 220,293 | 296,979 | 8:00 AM | 24,500 |
| Lexington Av local | 6 | 500,932 | 654,575 | 8:00 AM | 48,771 |
| Lexington Av local | 6L | 377,466 | 491,031 | 8:00 AM | 33,693 |
| Lexington Av local | 6X | 124,400 | 164,739 | 8:00 AM | 15,078 |
| Lexington Av local | 4 | 7,091 | 9,453 | 5:00 AM | 1,494 |
| Lower Culver | F | 42,303 | 57,428 | 7:00 AM | 4,511 |
| Lower Culver | FL | 40,577 | 55,088 | 8:00 AM | 4,195 |
| Lower Culver | FX | 1,727 | 2,340 | 7:00 AM | 1,081 |
| Lower Culver local | F | 39,135 | 53,337 | 7:00 AM | 4,219 |
| Lower Culver local | FL | 37,454 | 51,057 | 8:00 AM | 3,927 |
| Lower Culver local | FX | 1,681 | 2,281 | 7:00 AM | 1,051 |
| Manhattan Bridge | Q | 108,815 | 142,085 | 8:00 AM | 11,302 |
| Manhattan Bridge | N | 72,446 | 85,536 | 5:00 PM | 7,427 |
| Manhattan Bridge | D | 61,419 | 78,707 | 5:00 PM | 5,576 |
| Manhattan Bridge | B | 58,884 | 78,047 | 5:00 PM | 6,441 |
| Myrtle Av | M | 50,098 | 62,986 | 8:00 AM | 4,526 |
| Nassau St | J | 61,333 | 85,186 | 6:00 PM | 4,582 |
| Nassau St | Z | 4,833 | 6,822 | 8:00 AM | 2,590 |
| Nostrand Av | 5 | 46,249 | 59,665 | 7:00 AM | 5,303 |
| Nostrand Av | 2 | 42,103 | 54,162 | 8:00 AM | 3,635 |
| Pelham | 6 | 132,255 | 192,126 | 7:00 AM | 14,577 |
| Pelham | 6L | 94,346 | 134,925 | 7:00 AM | 8,252 |
| Pelham | 6X | 42,233 | 63,358 | 7:00 AM | 6,325 |
| Pelham express | 6 | 37,170 | 55,884 | 7:00 AM | 5,579 |
| Pelham express | 6X | 37,170 | 55,884 | 7:00 AM | 5,579 |
| Pelham local | 6 | 84,134 | 120,492 | 7:00 AM | 7,300 |
| Pelham local | 6L | 84,134 | 120,492 | 7:00 AM | 7,300 |
| Queens Blvd | E | 246,110 | 304,644 | 5:00 PM | 22,510 |
| Queens Blvd | F | 197,738 | 254,483 | 5:00 PM | 18,324 |
| Queens Blvd | FL | 196,682 | 253,127 | 5:00 PM | 18,054 |
| Queens Blvd | R | 85,668 | 114,440 | 5:00 PM | 8,809 |
| Queens Blvd | M | 83,478 | 112,161 | 8:00 AM | 8,369 |
| Queens Blvd | FX | 1,056 | 1,357 | 8:00 AM | 468 |
| Queens Blvd east | E | 110,880 | 140,268 | 7:00 AM | 9,903 |
| Queens Blvd east | F | 85,764 | 118,223 | 8:00 AM | 8,027 |
| Queens Blvd east | FL | 85,175 | 117,431 | 8:00 AM | 7,769 |
| Queens Blvd east | FX | 589 | 791 | 8:00 AM | 258 |
| Queens Blvd express | E | 218,973 | 270,528 | 5:00 PM | 21,818 |
| Queens Blvd express | F | 84,374 | 114,380 | 5:00 PM | 8,313 |
| Queens Blvd express | FL | 83,826 | 113,661 | 5:00 PM | 8,139 |
| Queens Blvd express | FX | 548 | 719 | 8:00 AM | 256 |
| Queens Blvd local | F | 98,781 | 134,774 | 8:00 AM | 8,253 |
| Queens Blvd local | FL | 98,171 | 133,954 | 8:00 AM | 7,983 |
| Queens Blvd local | R | 85,668 | 114,440 | 5:00 PM | 8,809 |
| Queens Blvd local | M | 83,478 | 112,161 | 8:00 AM | 8,369 |
| Queens Blvd local | E | 33,981 | 42,248 | 10:00 PM | 4,914 |
| Queens Blvd local | FX | 610 | 820 | 8:00 AM | 270 |
| Queens Blvd west | E | 224,490 | 276,517 | 5:00 PM | 20,793 |
| Queens Blvd west | F | 99,652 | 133,989 | 5:00 PM | 8,313 |
| Queens Blvd west | FL | 99,104 | 133,270 | 5:00 PM | 8,139 |
| Queens Blvd west | R | 85,668 | 114,440 | 5:00 PM | 8,809 |
| Queens Blvd west | M | 83,478 | 112,161 | 8:00 AM | 8,369 |
| Queens Blvd west | FX | 548 | 719 | 8:00 AM | 256 |
| Queens Blvd west express | E | 209,408 | 257,933 | 5:00 PM | 20,793 |
| Queens Blvd west express | F | 84,374 | 114,380 | 5:00 PM | 8,313 |
| Queens Blvd west express | FL | 83,826 | 113,661 | 5:00 PM | 8,139 |
| Queens Blvd west express | FX | 548 | 719 | 8:00 AM | 256 |
| Queens Blvd west local | R | 85,668 | 114,440 | 5:00 PM | 8,809 |
| Queens Blvd west local | M | 83,478 | 112,161 | 8:00 AM | 8,369 |
| Queens Blvd west local | F | 15,308 | 19,650 | 10:00 PM | 4,676 |
| Queens Blvd west local | FL | 15,308 | 19,650 | 10:00 PM | 4,676 |
| Queens Blvd west local | E | 15,208 | 18,756 | 10:00 PM | 3,917 |
| Rockaway | A | 29,252 | 52,113 | 7:00 AM | 2,615 |
| Rockaway | H | 3,264 | 6,448 | 4:00 PM | 285 |
| Rockaway Park branch | H | 3,264 | 6,448 | 4:00 PM | 285 |
| Rockaway Park branch | A | 448 | 888 | 7:00 AM | 154 |
| SAS Phase 1 | Q | 148,158 | 192,290 | 8:00 AM | 15,451 |
| SAS Phase 1 | N | 5,749 | 7,476 | 4:00 PM | 2,729 |
| SAS Phase 1 | R | 828 | 1,062 | 7:00 AM | 828 |
| Sea Beach | N | 81,951 | 89,913 | 7:00 AM | 7,591 |
| Sea Beach | W | 531 | 572 | 7:00 AM | 292 |
| Upper Culver | F | 108,965 | 139,719 | 8:00 AM | 11,650 |
| Upper Culver | FL | 106,566 | 136,501 | 8:00 AM | 11,650 |
| Upper Culver | G | 40,281 | 47,933 | 8:00 AM | 3,715 |
| Upper Culver | FX | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Upper Culver express | F | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Upper Culver express | FX | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Upper Culver local | F | 106,566 | 136,501 | 8:00 AM | 11,650 |
| Upper Culver local | FL | 106,566 | 136,501 | 8:00 AM | 11,650 |
| Upper Culver local | G | 40,281 | 47,933 | 8:00 AM | 3,715 |
| West End | D | 85,259 | 111,308 | 7:00 AM | 8,646 |
| West End | W | 75 | 96 | 10:00 AM | 52 |
| West End | R | 36 | 46 | 9:00 AM | 36 |
| White Plains Rd | 2 | 103,985 | 158,862 | 7:00 AM | 9,831 |
| White Plains Rd | 5 | 82,742 | 120,269 | 7:00 AM | 9,946 |
| White Plains Rd express | 5 | 22,344 | 33,224 | 7:00 AM | 5,090 |
| White Plains Rd local | 2 | 78,462 | 118,526 | 7:00 AM | 7,138 |
| White Plains Rd local | 5 | 34,951 | 49,851 | 3:00 PM | 4,893 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
