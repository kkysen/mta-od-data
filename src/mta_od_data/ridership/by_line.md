# Ridership by line

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --markdown-out src/mta_od_data/ridership/by_line.md`.

| Line | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 952,577 | 1,272,974 | 5:00 PM | 103,041 |
| 8 Av | 842,925 | 1,132,724 | 5:00 PM | 90,180 |
| Broadway-7 Av | 815,734 | 1,102,764 | 5:00 PM | 89,169 |
| Broadway | 752,380 | 987,275 | 5:00 PM | 77,580 |
| 6 Av | 731,117 | 957,840 | 5:00 PM | 82,310 |
| Lexington Av local | 515,507 | 676,250 | 5:00 PM | 48,514 |
| Flushing | 500,053 | 576,654 | 5:00 PM | 54,801 |
| Queens Blvd | 496,608 | 634,621 | 5:00 PM | 52,043 |
| Lexington Av express | 470,464 | 633,571 | 5:00 PM | 46,233 |
| 8 Av local | 452,244 | 585,921 | 5:00 PM | 42,979 |
| Queens Blvd west | 438,643 | 564,910 | 5:00 PM | 42,983 |
| Broadway-7 Av local | 436,143 | 577,878 | 5:00 PM | 42,609 |
| Broadway local | 394,137 | 519,126 | 5:00 PM | 38,431 |
| Canarsie | 376,101 | 424,267 | 5:00 PM | 35,446 |
| 8 Av express | 368,496 | 510,187 | 5:00 PM | 37,769 |
| 6 Av local | 354,073 | 461,312 | 5:00 PM | 37,790 |
| Broadway-7 Av express | 348,471 | 483,385 | 5:00 PM | 33,862 |
| 53 St | 332,524 | 435,833 | 5:00 PM | 33,649 |
| Broadway express | 306,301 | 397,650 | 5:00 PM | 31,693 |
| Eastern Pkwy | 299,195 | 400,542 | 8:00 AM | 33,071 |
| Queens Blvd local | 284,886 | 380,183 | 8:00 AM | 23,693 |
| Manhattan Bridge | 283,829 | 362,696 | 5:00 PM | 27,946 |
| Queens Blvd express | 283,136 | 359,556 | 5:00 PM | 28,873 |
| 4 Av | 281,435 | 343,069 | 8:00 AM | 29,199 |
| Queens Blvd west express | 272,835 | 346,047 | 5:00 PM | 27,375 |
| 63 St | 266,217 | 345,028 | 5:00 PM | 25,886 |
| 6 Av express | 246,953 | 332,032 | 5:00 PM | 25,163 |
| Fulton St | 246,192 | 338,057 | 5:00 PM | 23,437 |
| Flushing local | 220,818 | 246,171 | 4:00 PM | 16,394 |
| Brighton | 220,096 | 294,891 | 8:00 AM | 22,253 |
| Queens Blvd west local | 195,744 | 259,701 | 8:00 AM | 15,719 |
| Jamaica | 188,244 | 253,355 | 8:00 AM | 17,983 |
| Queens Blvd east | 183,575 | 241,366 | 5:00 PM | 16,315 |
| White Plains Rd | 163,009 | 243,559 | 7:00 AM | 16,690 |
| Jerome Av | 160,095 | 228,370 | 3:00 PM | 13,160 |
| Culver | 157,320 | 198,128 | 8:00 AM | 15,661 |
| 4 Av express | 149,153 | 180,453 | 8:00 AM | 14,653 |
| Eastern Pkwy express | 149,053 | 199,937 | 8:00 AM | 14,283 |
| Culver local | 148,595 | 187,613 | 8:00 AM | 15,011 |
| Eastern Pkwy local | 146,802 | 196,216 | 8:00 AM | 13,259 |
| Upper Culver | 143,085 | 179,763 | 8:00 AM | 14,348 |
| SAS Phase 1 | 141,144 | 184,197 | 8:00 AM | 14,196 |
| Upper Culver local | 140,999 | 176,955 | 8:00 AM | 14,348 |
| Fulton St express | 136,847 | 194,726 | 5:00 PM | 13,635 |
| 4 Av local | 135,512 | 166,330 | 5:00 PM | 11,326 |
| Crosstown | 132,849 | 153,941 | 5:00 PM | 12,254 |
| Lenox Av | 128,176 | 188,771 | 8:00 AM | 11,126 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,413 |
| Jamaica local | 117,208 | 157,412 | 8:00 AM | 11,301 |
| Concourse | 112,638 | 178,276 | 4:00 PM | 9,888 |
| Brighton local | 109,659 | 145,364 | 8:00 AM | 9,790 |
| White Plains Rd local | 109,510 | 162,871 | 3:00 PM | 9,449 |
| Concourse local | 106,333 | 167,528 | 3:00 PM | 8,343 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,021 |
| Fulton St local | 91,237 | 121,319 | 5:00 PM | 6,873 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,741 |
| West End | 82,041 | 107,184 | 7:00 AM | 7,860 |
| Pelham local | 80,784 | 115,836 | 4:00 PM | 6,466 |
| Sea Beach | 79,252 | 87,116 | 5:00 PM | 7,307 |
| Brighton express | 66,569 | 92,414 | 8:00 AM | 7,213 |
| Nassau St | 64,644 | 89,861 | 5:00 PM | 6,220 |
| 42 St Shuttle | 63,151 | 84,848 | 5:00 PM | 7,500 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,465 |
| Hillside Av local | 55,669 | 77,369 | 5:00 PM | 4,784 |
| Myrtle Av | 48,984 | 61,545 | 8:00 AM | 4,305 |
| Lower Culver | 39,795 | 54,095 | 7:00 AM | 4,111 |
| Lower Culver local | 37,107 | 50,612 | 7:00 AM | 3,873 |
| Pelham express | 36,803 | 55,247 | 7:00 AM | 5,390 |
| Flushing express | 35,176 | 40,390 | 5:00 PM | 5,743 |
| Jamaica express | 28,431 | 39,024 | 8:00 AM | 4,336 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,580 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,766 |
| White Plains Rd express | 18,341 | 27,079 | 7:00 AM | 4,307 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,568 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,672 |
| Concourse express | 15,013 | 25,176 | 7:00 AM | 3,231 |
| Franklin Av Shuttle | 12,854 | 17,160 | 8:00 AM | 1,099 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 295 |
| Culver express | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Upper Culver express | 2,423 | 3,247 | 7:00 AM | 1,385 |
| Hillside Av express | 2,060 | 2,970 | 7:00 AM | 857 |

![Riders by line](by_line-riders.svg)
