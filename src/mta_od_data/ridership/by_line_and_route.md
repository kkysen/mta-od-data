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
| 4 Av | R | 145,315 | 179,592 | 8:00 AM | 14,655 |
| 4 Av | N | 91,387 | 104,164 | 8:00 AM | 7,493 |
| 4 Av | D | 77,079 | 99,366 | 5:00 PM | 6,764 |
| 4 Av | W | 1,535 | 1,837 | 7:00 AM | 746 |
| 4 Av express | N | 80,763 | 92,041 | 8:00 AM | 7,493 |
| 4 Av express | D | 65,844 | 85,117 | 5:00 PM | 6,764 |
| 4 Av local | R | 112,769 | 139,105 | 8:00 AM | 11,251 |
| 4 Av local | N | 12,122 | 13,766 | 5:00 AM | 1,998 |
| 4 Av local | D | 9,483 | 12,020 | 5:00 AM | 1,807 |
| 4 Av local | W | 1,086 | 1,275 | 7:00 AM | 452 |
| 42 St Shuttle | GS | 62,778 | 84,192 | 5:00 PM | 7,501 |
| 53 St | E | 265,901 | 345,966 | 5:00 PM | 27,817 |
| 53 St | M | 45,898 | 62,153 | 8:00 AM | 4,377 |
| 53 St | F | 37,755 | 49,355 | 5:00 PM | 3,924 |
| 53 St | FL | 37,495 | 49,012 | 5:00 PM | 3,853 |
| 53 St | FX | 260 | 343 | 8:00 AM | 101 |
| 6 Av | F | 352,688 | 449,058 | 5:00 PM | 36,265 |
| 6 Av | FL | 348,033 | 443,022 | 5:00 PM | 33,873 |
| 6 Av | D | 189,129 | 257,960 | 5:00 PM | 17,951 |
| 6 Av | B | 154,745 | 202,983 | 5:00 PM | 17,497 |
| 6 Av | M | 124,250 | 167,136 | 5:00 PM | 12,839 |
| 6 Av | FX | 4,655 | 6,036 | 5:00 PM | 2,392 |
| 6 Av express | D | 137,553 | 188,187 | 5:00 PM | 13,197 |
| 6 Av express | B | 112,160 | 148,642 | 5:00 PM | 12,931 |
| 6 Av local | F | 243,159 | 313,062 | 5:00 PM | 25,274 |
| 6 Av local | FL | 240,046 | 308,971 | 5:00 PM | 23,387 |
| 6 Av local | M | 96,765 | 130,846 | 5:00 PM | 10,548 |
| 6 Av local | FX | 3,113 | 4,091 | 5:00 PM | 1,887 |
| 63 St | F | 156,718 | 200,552 | 5:00 PM | 14,517 |
| 63 St | FL | 155,788 | 199,351 | 5:00 PM | 14,162 |
| 63 St | Q | 102,755 | 134,776 | 8:00 AM | 10,074 |
| 63 St | M | 18,616 | 24,087 | 5:00 PM | 1,763 |
| 63 St | N | 4,220 | 5,501 | 4:00 PM | 1,583 |
| 63 St | FX | 956 | 1,239 | 8:00 AM | 361 |
| 63 St | R | 470 | 612 | 7:00 AM | 470 |
| 8 Av | A | 357,444 | 490,543 | 5:00 PM | 37,858 |
| 8 Av | E | 195,739 | 255,875 | 5:00 PM | 20,843 |
| 8 Av | C | 189,321 | 244,314 | 6:00 PM | 15,472 |
| 8 Av | D | 84,811 | 126,952 | 4:00 PM | 6,301 |
| 8 Av | B | 74,357 | 96,261 | 5:00 PM | 8,967 |
| 8 Av express | A | 283,961 | 385,275 | 5:00 PM | 30,722 |
| 8 Av express | D | 84,811 | 126,952 | 4:00 PM | 6,301 |
| 8 Av local | E | 194,775 | 254,356 | 5:00 PM | 20,723 |
| 8 Av local | C | 159,324 | 203,363 | 6:00 PM | 13,320 |
| 8 Av local | B | 74,357 | 96,261 | 5:00 PM | 8,967 |
| 8 Av local | A | 22,159 | 29,099 | 11:00 PM | 10,408 |
| Astoria | N | 54,399 | 63,309 | 5:00 PM | 5,570 |
| Astoria | W | 46,624 | 54,912 | 8:00 AM | 5,409 |
| Brighton | Q | 148,678 | 195,988 | 8:00 AM | 13,034 |
| Brighton | B | 86,416 | 118,134 | 8:00 AM | 9,121 |
| Brighton express | B | 66,533 | 92,532 | 8:00 AM | 7,131 |
| Brighton local | Q | 108,026 | 143,085 | 8:00 AM | 9,747 |
| Broadway | R | 231,003 | 312,652 | 5:00 PM | 24,368 |
| Broadway | Q | 208,757 | 276,931 | 5:00 PM | 20,581 |
| Broadway | N | 190,228 | 236,515 | 5:00 PM | 18,136 |
| Broadway | W | 137,839 | 180,721 | 5:00 PM | 13,988 |
| Broadway express | Q | 203,414 | 269,885 | 5:00 PM | 20,581 |
| Broadway express | N | 98,548 | 121,727 | 4:00 PM | 11,747 |
| Broadway local | R | 148,670 | 203,738 | 5:00 PM | 15,757 |
| Broadway local | N | 115,517 | 142,489 | 5:00 PM | 10,547 |
| Broadway local | W | 113,249 | 150,773 | 5:00 PM | 11,255 |
| Broadway local | Q | 11,297 | 14,651 | 12:00 AM | 4,189 |
| Broadway-7 Av | 1 | 514,785 | 682,754 | 5:00 PM | 51,321 |
| Broadway-7 Av | 2 | 235,980 | 325,882 | 5:00 PM | 23,150 |
| Broadway-7 Av | 3 | 178,916 | 246,907 | 5:00 PM | 18,946 |
| Broadway-7 Av express | 2 | 208,388 | 287,942 | 5:00 PM | 20,738 |
| Broadway-7 Av express | 3 | 158,049 | 217,589 | 5:00 PM | 16,486 |
| Broadway-7 Av local | 1 | 386,381 | 512,316 | 5:00 PM | 37,547 |
| Broadway-7 Av local | 2 | 6,822 | 9,393 | 1:00 AM | 2,044 |
| Canarsie | L | 370,379 | 417,108 | 5:00 PM | 34,864 |
| Concourse | D | 79,616 | 127,613 | 3:00 PM | 6,192 |
| Concourse | B | 34,959 | 53,627 | 5:00 PM | 5,038 |
| Concourse express | D | 14,547 | 24,448 | 7:00 AM | 3,193 |
| Concourse express | B | 46 | 86 | 9:00 AM | 46 |
| Concourse local | D | 72,341 | 115,313 | 3:00 PM | 6,175 |
| Concourse local | B | 34,957 | 53,623 | 5:00 PM | 5,038 |
| Crosstown | G | 133,593 | 154,895 | 5:00 PM | 12,356 |
| Culver | F | 115,623 | 149,242 | 8:00 AM | 11,869 |
| Culver | FL | 113,207 | 146,005 | 8:00 AM | 11,869 |
| Culver | G | 45,020 | 53,090 | 5:00 PM | 3,963 |
| Culver | FX | 2,628 | 3,518 | 7:00 AM | 1,569 |
| Culver express | F | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Culver express | FX | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Culver local | F | 111,963 | 144,493 | 8:00 AM | 11,612 |
| Culver local | FL | 110,427 | 142,410 | 8:00 AM | 11,612 |
| Culver local | G | 36,933 | 43,690 | 8:00 AM | 3,294 |
| Culver local | FX | 1,550 | 2,102 | 7:00 AM | 974 |
| Dyre Av | 5 | 25,099 | 37,996 | 7:00 AM | 2,769 |
| Eastern Pkwy | 3 | 94,643 | 130,179 | 8:00 AM | 9,214 |
| Eastern Pkwy | 2 | 85,955 | 112,177 | 8:00 AM | 8,736 |
| Eastern Pkwy | 4 | 79,981 | 108,897 | 7:00 AM | 6,869 |
| Eastern Pkwy | 5 | 75,089 | 99,106 | 8:00 AM | 7,743 |
| Eastern Pkwy express | 4 | 76,570 | 104,259 | 7:00 AM | 6,841 |
| Eastern Pkwy express | 5 | 70,271 | 92,815 | 8:00 AM | 7,528 |
| Eastern Pkwy local | 3 | 70,897 | 96,978 | 5:00 PM | 6,827 |
| Eastern Pkwy local | 2 | 64,925 | 84,174 | 8:00 AM | 5,988 |
| Eastern Pkwy local | 4 | 8,076 | 11,094 | 5:00 AM | 1,914 |
| Eastern Pkwy local | 5 | 163 | 230 | 5:00 AM | 149 |
| Far Rockaway branch | A | 16,535 | 34,093 | 7:00 AM | 1,570 |
| Flushing | 7 | 486,930 | 559,421 | 5:00 PM | 53,041 |
| Flushing | 7L | 397,985 | 457,573 | 5:00 PM | 36,048 |
| Flushing | 7X | 91,611 | 105,010 | 5:00 PM | 16,993 |
| Flushing express | 7 | 35,035 | 40,248 | 5:00 PM | 5,833 |
| Flushing express | 7X | 35,035 | 40,248 | 5:00 PM | 5,833 |
| Flushing local | 7 | 220,297 | 245,609 | 4:00 PM | 16,253 |
| Flushing local | 7L | 220,297 | 245,609 | 4:00 PM | 16,253 |
| Franklin Av Shuttle | FS | 13,901 | 18,531 | 8:00 AM | 1,245 |
| Fulton St | A | 173,180 | 243,154 | 5:00 PM | 16,119 |
| Fulton St | C | 88,970 | 116,354 | 5:00 PM | 8,088 |
| Fulton St express | A | 137,042 | 194,797 | 5:00 PM | 13,692 |
| Fulton St local | C | 77,697 | 102,458 | 5:00 PM | 7,016 |
| Fulton St local | A | 14,311 | 19,816 | 11:00 PM | 3,807 |
| Hillside Av | F | 55,484 | 77,105 | 5:00 PM | 4,806 |
| Hillside Av | FL | 55,115 | 76,609 | 5:00 PM | 4,737 |
| Hillside Av | E | 2,363 | 3,393 | 7:00 AM | 931 |
| Hillside Av | FX | 369 | 496 | 8:00 AM | 156 |
| Hillside Av express | E | 2,204 | 3,171 | 7:00 AM | 931 |
| Hillside Av local | F | 55,484 | 77,105 | 5:00 PM | 4,806 |
| Hillside Av local | FL | 55,115 | 76,609 | 5:00 PM | 4,737 |
| Hillside Av local | FX | 369 | 496 | 8:00 AM | 156 |
| Hillside Av local | E | 160 | 222 | 8:00 PM | 160 |
| Jamaica | J | 131,313 | 177,822 | 4:00 PM | 10,508 |
| Jamaica | M | 57,605 | 77,002 | 8:00 AM | 5,818 |
| Jamaica | Z | 8,860 | 12,006 | 5:00 PM | 3,340 |
| Jamaica express | J | 23,427 | 32,145 | 9:00 AM | 3,036 |
| Jamaica express | Z | 4,038 | 5,533 | 8:00 AM | 1,864 |
| Jamaica local | J | 67,330 | 91,384 | 4:00 PM | 5,193 |
| Jamaica local | M | 50,427 | 66,890 | 8:00 AM | 5,125 |
| Jamaica local | Z | 4,309 | 5,921 | 8:00 AM | 1,553 |
| Jerome Av | 4 | 156,404 | 222,698 | 4:00 PM | 12,837 |
| Lefferts branch | A | 16,087 | 24,484 | 7:00 AM | 1,670 |
| Lenox Av | 2 | 96,414 | 141,941 | 8:00 AM | 8,322 |
| Lenox Av | 3 | 32,607 | 48,036 | 8:00 AM | 2,951 |
| Lexington Av | 6 | 487,349 | 637,565 | 5:00 PM | 46,649 |
| Lexington Av | 6L | 367,276 | 478,213 | 5:00 PM | 32,060 |
| Lexington Av | 4 | 332,133 | 453,882 | 5:00 PM | 30,402 |
| Lexington Av | 5 | 244,996 | 334,522 | 8:00 AM | 26,354 |
| Lexington Av | 6X | 120,820 | 160,317 | 5:00 PM | 14,589 |
| Lexington Av express | 4 | 274,018 | 369,321 | 5:00 PM | 25,062 |
| Lexington Av express | 5 | 210,139 | 283,216 | 8:00 AM | 22,562 |
| Lexington Av local | 6 | 487,349 | 637,565 | 5:00 PM | 46,649 |
| Lexington Av local | 6L | 367,276 | 478,213 | 5:00 PM | 32,060 |
| Lexington Av local | 6X | 120,820 | 160,317 | 5:00 PM | 14,589 |
| Lexington Av local | 4 | 6,931 | 9,254 | 5:00 AM | 1,441 |
| Lower Culver | F | 39,759 | 54,063 | 7:00 AM | 4,134 |
| Lower Culver | FL | 38,163 | 51,902 | 8:00 AM | 3,952 |
| Lower Culver | FX | 1,596 | 2,161 | 7:00 AM | 1,003 |
| Lower Culver local | F | 36,934 | 50,409 | 7:00 AM | 3,873 |
| Lower Culver local | FL | 35,384 | 48,307 | 8:00 AM | 3,694 |
| Lower Culver local | FX | 1,550 | 2,102 | 7:00 AM | 974 |
| Manhattan Bridge | Q | 99,211 | 129,997 | 8:00 AM | 10,082 |
| Manhattan Bridge | N | 66,787 | 78,856 | 5:00 PM | 6,938 |
| Manhattan Bridge | D | 62,413 | 79,909 | 5:00 PM | 5,601 |
| Manhattan Bridge | B | 57,911 | 76,977 | 5:00 PM | 6,403 |
| Myrtle Av | M | 48,614 | 61,128 | 8:00 AM | 4,278 |
| Nassau St | J | 58,287 | 81,015 | 4:00 PM | 4,519 |
| Nassau St | Z | 4,542 | 6,407 | 8:00 AM | 2,453 |
| Nostrand Av | 5 | 43,622 | 56,291 | 7:00 AM | 4,717 |
| Nostrand Av | 2 | 40,018 | 51,565 | 8:00 AM | 3,467 |
| Pelham | 6 | 126,272 | 183,651 | 7:00 AM | 13,401 |
| Pelham | 6L | 90,200 | 129,156 | 7:00 AM | 7,388 |
| Pelham | 6X | 40,727 | 61,114 | 7:00 AM | 6,013 |
| Pelham express | 6 | 36,198 | 54,405 | 7:00 AM | 5,307 |
| Pelham express | 6X | 36,151 | 54,329 | 7:00 AM | 5,307 |
| Pelham express | 6L | 47 | 76 | 9:00 PM | 36 |
| Pelham local | 6 | 80,733 | 115,755 | 7:00 AM | 6,540 |
| Pelham local | 6L | 80,733 | 115,755 | 7:00 AM | 6,540 |
| Queens Blvd | E | 232,694 | 288,803 | 5:00 PM | 21,411 |
| Queens Blvd | F | 187,034 | 241,499 | 5:00 PM | 16,874 |
| Queens Blvd | FL | 186,014 | 240,190 | 5:00 PM | 16,611 |
| Queens Blvd | M | 83,916 | 112,149 | 8:00 AM | 8,016 |
| Queens Blvd | R | 83,442 | 111,756 | 5:00 PM | 8,704 |
| Queens Blvd | FX | 1,019 | 1,309 | 8:00 AM | 428 |
| Queens Blvd east | E | 106,241 | 134,591 | 7:00 AM | 9,343 |
| Queens Blvd east | F | 81,744 | 112,837 | 8:00 AM | 7,540 |
| Queens Blvd east | FL | 81,180 | 112,079 | 8:00 AM | 7,295 |
| Queens Blvd east | FX | 564 | 757 | 8:00 AM | 245 |
| Queens Blvd express | E | 206,171 | 255,263 | 5:00 PM | 20,757 |
| Queens Blvd express | F | 95,623 | 127,427 | 5:00 PM | 9,208 |
| Queens Blvd express | FL | 95,023 | 126,650 | 5:00 PM | 9,024 |
| Queens Blvd express | FX | 600 | 777 | 8:00 AM | 260 |
| Queens Blvd local | F | 94,125 | 128,640 | 8:00 AM | 7,762 |
| Queens Blvd local | FL | 93,540 | 127,854 | 8:00 AM | 7,504 |
| Queens Blvd local | M | 83,450 | 111,452 | 8:00 AM | 7,955 |
| Queens Blvd local | R | 83,442 | 111,756 | 5:00 PM | 8,704 |
| Queens Blvd local | E | 32,885 | 41,084 | 10:00 PM | 4,767 |
| Queens Blvd local | FX | 585 | 786 | 8:00 AM | 257 |
| Queens Blvd west | E | 211,597 | 261,361 | 5:00 PM | 19,724 |
| Queens Blvd west | F | 110,230 | 146,268 | 5:00 PM | 9,208 |
| Queens Blvd west | FL | 109,631 | 145,491 | 5:00 PM | 9,024 |
| Queens Blvd west | M | 83,450 | 111,452 | 8:00 AM | 7,955 |
| Queens Blvd west | R | 83,442 | 111,756 | 5:00 PM | 8,704 |
| Queens Blvd west | FX | 600 | 777 | 8:00 AM | 260 |
| Queens Blvd west express | E | 196,662 | 242,778 | 5:00 PM | 19,724 |
| Queens Blvd west express | F | 95,623 | 127,427 | 5:00 PM | 9,208 |
| Queens Blvd west express | FL | 95,023 | 126,650 | 5:00 PM | 9,024 |
| Queens Blvd west express | FX | 600 | 777 | 8:00 AM | 260 |
| Queens Blvd west local | M | 83,450 | 111,452 | 8:00 AM | 7,955 |
| Queens Blvd west local | R | 83,442 | 111,756 | 5:00 PM | 8,704 |
| Queens Blvd west local | E | 15,017 | 18,696 | 10:00 PM | 3,813 |
| Queens Blvd west local | F | 14,627 | 18,868 | 10:00 PM | 4,388 |
| Queens Blvd west local | FL | 14,627 | 18,868 | 10:00 PM | 4,388 |
| Rockaway | A | 27,390 | 48,997 | 7:00 AM | 2,434 |
| Rockaway | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | H | 2,776 | 5,429 | 4:00 PM | 242 |
| Rockaway Park branch | A | 426 | 836 | 7:00 AM | 150 |
| SAS Phase 1 | Q | 143,330 | 186,472 | 5:00 PM | 14,269 |
| SAS Phase 1 | N | 5,755 | 7,477 | 4:00 PM | 2,859 |
| SAS Phase 1 | R | 798 | 1,023 | 7:00 AM | 798 |
| Sea Beach | N | 78,562 | 86,338 | 5:00 PM | 7,330 |
| Sea Beach | W | 526 | 568 | 7:00 AM | 300 |
| Upper Culver | F | 105,175 | 135,089 | 8:00 AM | 10,945 |
| Upper Culver | FL | 103,003 | 132,172 | 8:00 AM | 10,945 |
| Upper Culver | G | 36,933 | 43,690 | 8:00 AM | 3,294 |
| Upper Culver | FX | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Upper Culver express | F | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Upper Culver express | FX | 2,382 | 3,195 | 7:00 AM | 1,383 |
| Upper Culver local | F | 103,003 | 132,172 | 8:00 AM | 10,945 |
| Upper Culver local | FL | 103,003 | 132,172 | 8:00 AM | 10,945 |
| Upper Culver local | G | 36,933 | 43,690 | 8:00 AM | 3,294 |
| West End | D | 81,889 | 106,995 | 7:00 AM | 7,858 |
| West End | W | 68 | 87 | 10:00 AM | 42 |
| West End | R | 29 | 36 | 9:00 AM | 29 |
| White Plains Rd | 2 | 99,027 | 151,514 | 7:00 AM | 8,819 |
| White Plains Rd | 5 | 77,900 | 113,227 | 7:00 AM | 8,945 |
| White Plains Rd express | 5 | 20,564 | 30,561 | 7:00 AM | 4,597 |
| White Plains Rd local | 2 | 74,666 | 112,952 | 7:00 AM | 6,414 |
| White Plains Rd local | 5 | 32,994 | 47,072 | 3:00 PM | 4,532 |

</details>

## Charts

### Riders by line and route

<details>
<summary>The chart</summary>

![Riders by line and route](by_line_and_route-riders.svg)

</details>
