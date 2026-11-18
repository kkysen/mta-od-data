# Ridership by line

Average weekday riders with fare evaders, over 22 weekdays from 2025-09-16 to 2025-09-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Sep 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --month 2025-09 --markdown-out src/mta_od_data/ridership/2025-09/by_line.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Sep 2025 | 2019 | Peak Hour | Riders in Peak Hour, Sep 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 981,182 | 1,310,274 | 5:00 PM | 108,767 |
| 8 Av | 866,051 | 1,165,275 | 5:00 PM | 92,610 |
| Broadway-7 Av | 837,038 | 1,129,958 | 5:00 PM | 97,878 |
| Broadway | 791,881 | 1,033,531 | 5:00 PM | 82,519 |
| 6 Av | 775,188 | 1,015,136 | 5:00 PM | 87,460 |
| Queens Blvd | 528,036 | 672,467 | 5:00 PM | 56,610 |
| Lexington Av express | 515,015 | 693,132 | 5:00 PM | 51,520 |
| Flushing | 514,888 | 590,090 | 5:00 PM | 57,254 |
| Lexington Av local | 507,777 | 663,663 | 8:00 AM | 48,772 |
| 8 Av local | 461,625 | 597,908 | 5:00 PM | 43,842 |
| Queens Blvd west | 454,489 | 585,055 | 5:00 PM | 44,882 |
| Broadway-7 Av local | 399,538 | 528,711 | 5:00 PM | 38,973 |
| Canarsie | 399,052 | 450,913 | 5:00 PM | 37,807 |
| Broadway local | 396,784 | 520,306 | 5:00 PM | 38,461 |
| Broadway-7 Av express | 384,009 | 529,262 | 5:00 PM | 39,081 |
| 8 Av express | 365,260 | 507,983 | 5:00 PM | 37,958 |
| 6 Av local | 343,193 | 447,615 | 5:00 PM | 36,393 |
| Broadway express | 340,219 | 438,328 | 5:00 PM | 36,075 |
| 53 St | 336,371 | 439,300 | 5:00 PM | 34,284 |
| Eastern Pkwy | 311,193 | 416,112 | 8:00 AM | 35,498 |
| 63 St | 304,041 | 392,552 | 5:00 PM | 31,244 |
| Manhattan Bridge | 301,500 | 384,295 | 5:00 PM | 29,774 |
| Queens Blvd express | 300,848 | 381,523 | 5:00 PM | 30,130 |
| Queens Blvd local | 292,358 | 390,158 | 7:00 AM | 24,662 |
| Queens Blvd west express | 291,306 | 368,963 | 5:00 PM | 29,105 |
| 4 Av | 289,326 | 352,214 | 8:00 AM | 30,808 |
| Fulton St | 267,136 | 365,237 | 5:00 PM | 25,758 |
| 6 Av express | 263,207 | 353,569 | 5:00 PM | 28,501 |
| Brighton | 239,709 | 319,778 | 8:00 AM | 24,117 |
| Flushing local | 237,008 | 262,683 | 7:00 AM | 17,320 |
| Queens Blvd west local | 199,433 | 264,703 | 8:00 AM | 16,390 |
| Jamaica | 197,801 | 266,057 | 8:00 AM | 19,100 |
| Queens Blvd east | 193,003 | 253,535 | 7:00 AM | 17,255 |
| White Plains Rd | 172,986 | 258,111 | 7:00 AM | 19,777 |
| Jerome Av | 167,826 | 237,916 | 7:00 AM | 13,809 |
| Culver | 164,143 | 206,929 | 8:00 AM | 16,913 |
| SAS Phase 1 | 154,685 | 200,754 | 8:00 AM | 16,412 |
| Culver local | 154,313 | 195,063 | 8:00 AM | 16,049 |
| Eastern Pkwy express | 154,159 | 206,679 | 8:00 AM | 15,583 |
| 4 Av express | 151,509 | 182,977 | 8:00 AM | 15,184 |
| Eastern Pkwy local | 149,900 | 199,792 | 8:00 AM | 13,702 |
| Upper Culver | 148,407 | 186,666 | 8:00 AM | 15,363 |
| Upper Culver local | 146,116 | 183,584 | 8:00 AM | 15,363 |
| Fulton St express | 143,454 | 203,901 | 5:00 PM | 14,466 |
| Crosstown | 140,802 | 163,253 | 5:00 PM | 12,938 |
| 4 Av local | 137,286 | 168,374 | 8:00 AM | 11,717 |
| Lenox Av | 132,548 | 194,841 | 8:00 AM | 11,973 |
| Pelham | 132,255 | 192,126 | 7:00 AM | 14,577 |
| Concourse | 120,031 | 188,707 | 7:00 AM | 10,668 |
| Jamaica local | 118,863 | 159,433 | 8:00 AM | 11,727 |
| Brighton local | 115,734 | 152,855 | 8:00 AM | 10,516 |
| Concourse local | 113,485 | 177,547 | 7:00 AM | 9,029 |
| White Plains Rd local | 113,110 | 167,855 | 3:00 PM | 10,203 |
| Astoria | 104,899 | 122,659 | 8:00 AM | 10,780 |
| Fulton St local | 98,585 | 130,768 | 5:00 PM | 7,563 |
| Nostrand Av | 86,753 | 111,669 | 8:00 AM | 8,407 |
| West End | 85,329 | 111,397 | 7:00 AM | 8,646 |
| Pelham local | 84,134 | 120,492 | 7:00 AM | 7,300 |
| Sea Beach | 82,483 | 90,486 | 7:00 AM | 7,884 |
| Brighton express | 70,954 | 98,345 | 8:00 AM | 7,714 |
| Nassau St | 66,139 | 91,977 | 5:00 PM | 6,274 |
| Hillside Av | 60,434 | 84,031 | 7:00 AM | 5,969 |
| 42 St Shuttle | 58,714 | 78,842 | 5:00 PM | 6,828 |
| Hillside Av local | 58,342 | 80,998 | 5:00 PM | 5,030 |
| Myrtle Av | 50,098 | 62,986 | 8:00 AM | 4,526 |
| Lower Culver | 42,303 | 57,427 | 7:00 AM | 4,511 |
| Flushing express | 39,908 | 45,329 | 5:00 PM | 6,923 |
| Lower Culver local | 39,134 | 53,337 | 7:00 AM | 4,220 |
| Pelham express | 37,170 | 55,884 | 7:00 AM | 5,579 |
| Rockaway | 29,331 | 52,320 | 5:00 PM | 2,808 |
| Jamaica express | 28,674 | 39,250 | 8:00 AM | 4,436 |
| Dyre Av | 26,911 | 40,735 | 7:00 AM | 3,101 |
| White Plains Rd express | 22,344 | 33,224 | 7:00 AM | 5,090 |
| Far Rockaway branch | 17,237 | 35,445 | 7:00 AM | 1,692 |
| Lefferts branch | 17,210 | 26,170 | 7:00 AM | 1,832 |
| Concourse express | 15,555 | 26,097 | 8:00 AM | 3,358 |
| Franklin Av Shuttle | 14,667 | 19,538 | 8:00 AM | 1,281 |
| Rockaway Park branch | 3,712 | 7,336 | 5:00 PM | 337 |
| Culver express | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Upper Culver express | 2,676 | 3,585 | 7:00 AM | 1,591 |
| Hillside Av express | 2,316 | 3,333 | 7:00 AM | 976 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
