# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

| Line | Route | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| 4 Av | R | 145,403 | 180,198 | 8:00 AM | 14,546 |
| 4 Av | N | 94,517 | 107,962 | 8:00 AM | 7,962 |
| 4 Av | D | 78,470 | 101,110 | 5:00 PM | 6,852 |
| 4 Av | W | 1,508 | 1,818 | 7:00 AM | 677 |
| 4 Av express | N | 83,794 | 95,713 | 8:00 AM | 7,962 |
| 4 Av express | D | 66,762 | 86,301 | 5:00 PM | 6,852 |
| 4 Av local | R | 112,711 | 139,136 | 5:00 PM | 11,302 |
| 4 Av local | N | 12,519 | 14,247 | 5:00 AM | 2,034 |
| 4 Av local | D | 9,879 | 12,473 | 5:00 AM | 1,856 |
| 4 Av local | W | 1,094 | 1,291 | 7:00 AM | 443 |
| 42 St Shuttle | GS | 63,151 | 84,848 | 5:00 PM | 7,500 |
| 53 St | E | 244,148 | 318,143 | 5:00 PM | 25,072 |
| 53 St | M | 51,438 | 69,512 | 6:00 PM | 4,735 |
| 53 St | F | 37,507 | 48,944 | 5:00 PM | 3,918 |
| 53 St | FL | 37,237 | 48,589 | 5:00 PM | 3,826 |
| 53 St | FX | 269 | 355 | 8:00 AM | 95 |
| 6 Av | F | 355,937 | 452,579 | 5:00 PM | 37,396 |
| 6 Av | FL | 351,217 | 446,469 | 5:00 PM | 35,027 |
| 6 Av | D | 175,643 | 238,776 | 5:00 PM | 16,583 |
| 6 Av | B | 143,469 | 188,599 | 5:00 PM | 15,924 |
| 6 Av | M | 123,399 | 165,719 | 5:00 PM | 12,406 |
| 6 Av | FX | 4,720 | 6,110 | 5:00 PM | 2,369 |
| 6 Av express | D | 135,832 | 185,083 | 5:00 PM | 12,745 |
| 6 Av express | B | 111,132 | 146,966 | 5:00 PM | 12,419 |
| 6 Av local | F | 254,926 | 327,469 | 5:00 PM | 27,201 |
| 6 Av local | FL | 251,690 | 323,232 | 5:00 PM | 25,205 |
| 6 Av local | M | 100,984 | 136,263 | 5:00 PM | 10,589 |
| 6 Av local | FX | 3,236 | 4,237 | 5:00 PM | 1,996 |
| 63 St | F | 149,272 | 191,086 | 5:00 PM | 13,791 |
| 63 St | FL | 148,508 | 190,096 | 5:00 PM | 13,521 |
| 63 St | Q | 98,008 | 129,178 | 8:00 AM | 9,541 |
| 63 St | M | 17,912 | 23,210 | 5:00 PM | 1,698 |
| 63 St | N | 3,992 | 5,239 | 4:00 PM | 1,448 |
| 63 St | FX | 783 | 1,019 | 8:00 AM | 280 |
| 63 St | R | 494 | 643 | 7:00 AM | 494 |
| 8 Av | A | 362,280 | 496,514 | 5:00 PM | 38,418 |
| 8 Av | E | 204,313 | 267,486 | 5:00 PM | 21,825 |
| 8 Av | C | 184,931 | 238,391 | 6:00 PM | 14,973 |
| 8 Av | D | 86,046 | 129,028 | 5:00 PM | 6,401 |
| 8 Av | B | 74,403 | 96,767 | 5:00 PM | 9,033 |
| 8 Av express | A | 289,462 | 392,027 | 5:00 PM | 31,368 |
| 8 Av express | D | 86,046 | 129,028 | 5:00 PM | 6,401 |
| 8 Av local | E | 203,350 | 265,965 | 5:00 PM | 21,706 |
| 8 Av local | C | 156,099 | 198,969 | 6:00 PM | 12,969 |
| 8 Av local | B | 74,403 | 96,767 | 5:00 PM | 9,033 |
| 8 Av local | A | 22,237 | 29,211 | 11:00 PM | 10,506 |
| Astoria | N | 54,543 | 63,458 | 5:00 PM | 5,608 |
| Astoria | W | 46,481 | 54,763 | 8:00 AM | 5,398 |
| Brighton | Q | 149,432 | 197,183 | 8:00 AM | 13,057 |
| Brighton | B | 85,518 | 116,829 | 8:00 AM | 9,197 |
| Brighton express | B | 66,569 | 92,414 | 8:00 AM | 7,213 |
| Brighton local | Q | 109,659 | 145,364 | 8:00 AM | 9,790 |
| Broadway | R | 231,076 | 313,302 | 5:00 PM | 24,412 |
| Broadway | Q | 207,940 | 276,376 | 5:00 PM | 19,799 |
| Broadway | N | 198,119 | 246,295 | 5:00 PM | 19,309 |
| Broadway | W | 138,592 | 181,830 | 5:00 PM | 14,061 |
| Broadway express | Q | 202,994 | 269,817 | 5:00 PM | 19,799 |
| Broadway express | N | 104,341 | 129,024 | 4:00 PM | 12,137 |
| Broadway local | R | 153,742 | 210,790 | 5:00 PM | 16,140 |
| Broadway local | N | 119,042 | 146,814 | 5:00 PM | 11,107 |
| Broadway local | W | 113,046 | 150,736 | 5:00 PM | 11,183 |
| Broadway local | Q | 10,799 | 14,066 | 12:00 AM | 3,918 |
| Broadway-7 Av | 1 | 513,210 | 680,527 | 5:00 PM | 50,439 |
| Broadway-7 Av | 2 | 230,583 | 319,966 | 5:00 PM | 21,854 |
| Broadway-7 Av | 3 | 165,919 | 230,277 | 8:00 AM | 17,131 |
| Broadway-7 Av express | 2 | 202,719 | 281,539 | 5:00 PM | 19,335 |
| Broadway-7 Av express | 3 | 145,776 | 201,882 | 8:00 AM | 15,185 |
| Broadway-7 Av local | 1 | 429,340 | 568,514 | 5:00 PM | 42,609 |
| Broadway-7 Av local | 2 | 6,949 | 9,567 | 1:00 AM | 2,078 |
| Canarsie | L | 376,101 | 424,267 | 5:00 PM | 35,446 |
| Concourse | D | 79,459 | 127,434 | 3:00 PM | 6,161 |
| Concourse | B | 34,407 | 52,848 | 7:00 AM | 4,878 |
| Concourse express | D | 14,970 | 25,096 | 7:00 AM | 3,231 |
| Concourse express | B | 43 | 80 | 9:00 AM | 43 |
| Concourse local | D | 72,106 | 115,017 | 3:00 PM | 6,144 |
| Concourse local | B | 34,405 | 52,844 | 7:00 AM | 4,878 |
| Crosstown | G | 132,849 | 153,941 | 5:00 PM | 12,254 |
| Culver | F | 115,134 | 148,509 | 8:00 AM | 11,659 |
| Culver | FL | 112,686 | 145,231 | 8:00 AM | 11,659 |
| Culver | G | 47,414 | 55,831 | 5:00 PM | 4,141 |
| Culver | FX | 2,684 | 3,589 | 7:00 AM | 1,576 |
| Culver express | F | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Culver express | FX | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Culver local | F | 102,667 | 131,645 | 8:00 AM | 10,745 |
| Culver local | FL | 102,667 | 131,645 | 8:00 AM | 10,745 |
| Culver local | G | 39,778 | 47,023 | 8:00 AM | 3,603 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,766 |
| Eastern Pkwy | 3 | 95,927 | 131,962 | 8:00 AM | 9,392 |
| Eastern Pkwy | 2 | 88,842 | 116,214 | 8:00 AM | 9,104 |
| Eastern Pkwy | 4 | 81,449 | 110,820 | 7:00 AM | 6,908 |
| Eastern Pkwy | 5 | 76,009 | 100,294 | 8:00 AM | 7,997 |
| Eastern Pkwy express | 4 | 78,002 | 106,137 | 7:00 AM | 6,885 |
| Eastern Pkwy express | 5 | 71,129 | 93,915 | 8:00 AM | 7,705 |
| Eastern Pkwy local | 3 | 72,161 | 98,728 | 8:00 AM | 6,922 |
| Eastern Pkwy local | 2 | 67,478 | 87,732 | 8:00 AM | 6,337 |
| Eastern Pkwy local | 4 | 8,109 | 11,136 | 5:00 AM | 1,925 |
| Eastern Pkwy local | 5 | 162 | 228 | 5:00 AM | 147 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,568 |
| Flushing | 7 | 500,053 | 576,654 | 5:00 PM | 54,801 |
| Flushing | 7L | 408,252 | 471,188 | 5:00 PM | 37,349 |
| Flushing | 7X | 94,012 | 108,009 | 5:00 PM | 17,452 |
| Flushing express | 7 | 35,176 | 40,390 | 5:00 PM | 5,743 |
| Flushing express | 7X | 35,176 | 40,390 | 5:00 PM | 5,743 |
| Flushing local | 7 | 220,818 | 246,171 | 4:00 PM | 16,394 |
| Flushing local | 7L | 220,818 | 246,171 | 4:00 PM | 16,394 |
| Franklin Av Shuttle | FS | 12,854 | 17,160 | 8:00 AM | 1,099 |
| Fulton St | A | 171,999 | 242,116 | 5:00 PM | 16,019 |
| Fulton St | C | 84,837 | 111,266 | 5:00 PM | 7,418 |
| Fulton St express | A | 136,847 | 194,726 | 5:00 PM | 13,635 |
| Fulton St local | C | 76,945 | 101,511 | 5:00 PM | 6,873 |
| Fulton St local | A | 14,293 | 19,809 | 11:00 PM | 3,862 |
| Hillside Av | F | 55,526 | 77,171 | 5:00 PM | 4,784 |
| Hillside Av | FL | 55,165 | 76,686 | 5:00 PM | 4,714 |
| Hillside Av | E | 2,203 | 3,169 | 7:00 AM | 857 |
| Hillside Av | FX | 361 | 484 | 8:00 AM | 149 |
| Jamaica | J | 129,591 | 175,299 | 4:00 PM | 10,617 |
| Jamaica | M | 57,794 | 77,270 | 8:00 AM | 5,820 |
| Jamaica | Z | 8,994 | 12,171 | 5:00 PM | 3,529 |
| Jamaica express | J | 24,259 | 33,322 | 9:00 AM | 3,155 |
| Jamaica express | Z | 4,171 | 5,703 | 8:00 AM | 1,950 |
| Jamaica local | J | 68,668 | 93,211 | 4:00 PM | 5,373 |
| Jamaica local | M | 50,343 | 66,766 | 8:00 AM | 5,106 |
| Jamaica local | Z | 4,415 | 6,046 | 8:00 AM | 1,614 |
| Jerome Av | 4 | 160,095 | 228,370 | 3:00 PM | 13,160 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,672 |
| Lenox Av | 2 | 96,166 | 141,703 | 8:00 AM | 8,247 |
| Lenox Av | 3 | 32,653 | 48,096 | 5:00 PM | 2,931 |
| Lexington Av | 6 | 508,660 | 667,137 | 5:00 PM | 48,514 |
| Lexington Av | 6L | 383,383 | 500,250 | 5:00 PM | 33,146 |
| Lexington Av | 4 | 327,939 | 448,470 | 5:00 PM | 29,876 |
| Lexington Av | 5 | 232,684 | 317,007 | 8:00 AM | 25,240 |
| Lexington Av | 6X | 125,471 | 167,136 | 5:00 PM | 15,367 |
| Lexington Av express | 4 | 270,219 | 364,216 | 5:00 PM | 24,505 |
| Lexington Av express | 5 | 200,483 | 269,662 | 8:00 AM | 21,775 |
| Lexington Av local | 6 | 508,660 | 667,137 | 5:00 PM | 48,514 |
| Lexington Av local | 6L | 383,383 | 500,250 | 5:00 PM | 33,146 |
| Lexington Av local | 6X | 125,471 | 167,136 | 5:00 PM | 15,367 |
| Lexington Av local | 4 | 7,051 | 9,418 | 5:00 AM | 1,536 |
| Lower Culver | F | 39,795 | 54,095 | 7:00 AM | 4,111 |
| Lower Culver | FL | 38,180 | 51,910 | 8:00 AM | 3,952 |
| Lower Culver | FX | 1,615 | 2,185 | 7:00 AM | 995 |
| Manhattan Bridge | Q | 92,786 | 122,126 | 8:00 AM | 8,728 |
| Manhattan Bridge | N | 71,629 | 84,732 | 5:00 PM | 7,682 |
| Manhattan Bridge | D | 63,827 | 81,707 | 5:00 PM | 5,788 |
| Manhattan Bridge | B | 55,587 | 74,132 | 5:00 PM | 6,225 |
| Myrtle Av | M | 48,984 | 61,545 | 8:00 AM | 4,305 |
| Nassau St | J | 59,940 | 83,242 | 4:00 PM | 4,649 |
| Nassau St | Z | 4,704 | 6,620 | 8:00 AM | 2,522 |
| Nostrand Av | 5 | 43,136 | 55,619 | 7:00 AM | 4,617 |
| Nostrand Av | 2 | 38,984 | 50,190 | 8:00 AM | 3,341 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,413 |
| Pelham | 6L | 90,212 | 129,181 | 7:00 AM | 7,305 |
| Pelham | 6X | 41,346 | 61,967 | 7:00 AM | 6,108 |
| Pelham express | 6 | 36,803 | 55,247 | 7:00 AM | 5,390 |
| Pelham express | 6X | 36,759 | 55,176 | 7:00 AM | 5,390 |
| Pelham express | 6L | 44 | 71 | 9:00 PM | 30 |
| Pelham local | 6 | 80,784 | 115,836 | 4:00 PM | 6,466 |
| Pelham local | 6L | 80,784 | 115,836 | 4:00 PM | 6,466 |
| Queens Blvd | E | 215,485 | 267,378 | 5:00 PM | 19,969 |
| Queens Blvd | F | 182,072 | 235,256 | 5:00 PM | 16,424 |
| Queens Blvd | FL | 181,102 | 234,009 | 5:00 PM | 16,174 |
| Queens Blvd | R | 85,561 | 114,226 | 5:00 PM | 8,538 |
| Queens Blvd | M | 81,327 | 108,957 | 8:00 AM | 8,324 |
| Queens Blvd | FX | 970 | 1,247 | 8:00 AM | 400 |
| Queens Blvd east | E | 104,050 | 131,597 | 7:00 AM | 9,055 |
| Queens Blvd east | F | 83,596 | 115,348 | 8:00 AM | 7,769 |
| Queens Blvd east | FL | 83,032 | 114,591 | 8:00 AM | 7,534 |
| Queens Blvd east | FX | 564 | 757 | 8:00 AM | 235 |
| Queens Blvd express | E | 187,388 | 231,809 | 5:00 PM | 19,222 |
| Queens Blvd express | F | 97,917 | 130,563 | 5:00 PM | 9,651 |
| Queens Blvd express | FL | 97,320 | 129,791 | 5:00 PM | 9,463 |
| Queens Blvd express | FX | 597 | 772 | 8:00 AM | 253 |
| Queens Blvd local | F | 95,205 | 130,161 | 8:00 AM | 7,973 |
| Queens Blvd local | FL | 94,620 | 129,376 | 8:00 AM | 7,726 |
| Queens Blvd local | R | 85,561 | 114,226 | 5:00 PM | 8,538 |
| Queens Blvd local | M | 80,881 | 108,277 | 8:00 AM | 8,265 |
| Queens Blvd local | E | 33,266 | 41,618 | 10:00 PM | 4,918 |
| Queens Blvd local | FX | 586 | 786 | 8:00 AM | 248 |
| Queens Blvd west | E | 190,614 | 235,124 | 5:00 PM | 17,725 |
| Queens Blvd west | F | 112,005 | 148,757 | 5:00 PM | 9,651 |
| Queens Blvd west | FL | 111,408 | 147,986 | 5:00 PM | 9,463 |
| Queens Blvd west | R | 85,561 | 114,226 | 5:00 PM | 8,538 |
| Queens Blvd west | M | 80,881 | 108,277 | 8:00 AM | 8,265 |
| Queens Blvd west | FX | 597 | 772 | 8:00 AM | 253 |
| Queens Blvd west express | E | 175,330 | 216,039 | 5:00 PM | 17,725 |
| Queens Blvd west express | F | 97,917 | 130,563 | 5:00 PM | 9,651 |
| Queens Blvd west express | FL | 97,320 | 129,791 | 5:00 PM | 9,463 |
| Queens Blvd west express | FX | 597 | 772 | 8:00 AM | 253 |
| Queens Blvd west local | R | 85,561 | 114,226 | 5:00 PM | 8,538 |
| Queens Blvd west local | M | 80,881 | 108,277 | 8:00 AM | 8,265 |
| Queens Blvd west local | E | 15,387 | 19,229 | 10:00 PM | 3,900 |
| Queens Blvd west local | F | 14,129 | 18,252 | 10:00 PM | 4,271 |
| Queens Blvd west local | FL | 14,129 | 18,252 | 10:00 PM | 4,271 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,435 |
| Rockaway | H | 2,769 | 5,415 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,769 | 5,415 | 4:00 PM | 242 |
| Rockaway Park branch | A | 433 | 850 | 7:00 AM | 150 |
| SAS Phase 1 | Q | 135,111 | 176,349 | 8:00 AM | 13,264 |
| SAS Phase 1 | N | 5,259 | 6,863 | 4:00 PM | 2,513 |
| SAS Phase 1 | R | 800 | 1,024 | 7:00 AM | 800 |
| Sea Beach | N | 78,733 | 86,557 | 5:00 PM | 7,307 |
| Sea Beach | W | 520 | 560 | 7:00 AM | 293 |
| Upper Culver | F | 104,856 | 134,584 | 8:00 AM | 10,745 |
| Upper Culver | FL | 102,667 | 131,645 | 8:00 AM | 10,745 |
| Upper Culver | G | 39,778 | 47,023 | 8:00 AM | 3,603 |
| Upper Culver | FX | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Upper Culver express | F | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Upper Culver express | FX | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Upper Culver local | F | 102,667 | 131,645 | 8:00 AM | 10,745 |
| Upper Culver local | FL | 102,667 | 131,645 | 8:00 AM | 10,745 |
| Upper Culver local | G | 39,778 | 47,023 | 8:00 AM | 3,603 |
| West End | D | 81,966 | 107,088 | 7:00 AM | 7,860 |
| West End | W | 56 | 72 | 10:00 AM | 34 |
| West End | R | 30 | 38 | 9:00 AM | 30 |
| White Plains Rd | 2 | 97,908 | 149,718 | 8:00 AM | 8,400 |
| White Plains Rd | 5 | 70,789 | 102,473 | 7:00 AM | 8,300 |
| White Plains Rd express | 5 | 18,341 | 27,079 | 7:00 AM | 4,307 |
| White Plains Rd local | 2 | 77,295 | 117,097 | 7:00 AM | 6,688 |
| White Plains Rd local | 5 | 32,415 | 46,120 | 3:00 PM | 4,423 |
