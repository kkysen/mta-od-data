# Ridership by line

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (as `raptor assign-range` routes them).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The peak hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --markdown-out src/mta_od_data/ridership/by_line.md`.

## Table

<details open>
<summary>The table</summary>

| Line | Aug-Dec 2025 | 2019 | Peak Hour | Riders in Peak Hour, Aug-Dec 2025 |
| --- | ---: | ---: | --- | ---: |
| Lexington Av | 936,555 | 1,251,750 | 5:00 PM | 102,400 |
| 8 Av | 835,305 | 1,124,448 | 5:00 PM | 87,639 |
| Broadway-7 Av | 816,325 | 1,103,691 | 5:00 PM | 94,528 |
| Broadway | 785,051 | 1,026,485 | 5:00 PM | 81,263 |
| 6 Av | 765,288 | 1,004,797 | 5:00 PM | 85,112 |
| Queens Blvd | 503,533 | 642,801 | 5:00 PM | 53,990 |
| Flushing | 491,982 | 566,189 | 5:00 PM | 54,522 |
| Lexington Av local | 490,418 | 641,553 | 5:00 PM | 46,200 |
| Lexington Av express | 485,907 | 654,886 | 5:00 PM | 47,823 |
| Queens Blvd west | 444,083 | 571,351 | 5:00 PM | 44,528 |
| 8 Av local | 438,219 | 567,197 | 5:00 PM | 41,811 |
| Broadway local | 402,693 | 528,753 | 5:00 PM | 38,803 |
| Broadway-7 Av local | 394,811 | 523,661 | 5:00 PM | 38,077 |
| Canarsie | 378,402 | 427,580 | 5:00 PM | 35,706 |
| Broadway-7 Av express | 372,707 | 514,250 | 5:00 PM | 37,675 |
| 8 Av express | 359,847 | 500,561 | 5:00 PM | 36,006 |
| 53 St | 341,619 | 446,936 | 5:00 PM | 34,814 |
| 6 Av local | 340,598 | 445,721 | 5:00 PM | 35,513 |
| Broadway express | 333,112 | 430,107 | 5:00 PM | 35,141 |
| Queens Blvd express | 298,208 | 378,176 | 5:00 PM | 29,793 |
| Eastern Pkwy | 294,593 | 394,530 | 8:00 AM | 32,574 |
| Manhattan Bridge | 291,510 | 371,900 | 5:00 PM | 28,703 |
| Queens Blvd west express | 288,863 | 365,879 | 5:00 PM | 28,774 |
| Queens Blvd local | 283,749 | 378,709 | 8:00 AM | 23,524 |
| 4 Av | 277,846 | 338,254 | 8:00 AM | 28,703 |
| 63 St | 273,202 | 353,784 | 5:00 PM | 27,508 |
| 6 Av express | 257,413 | 346,591 | 5:00 PM | 27,325 |
| Fulton St | 252,473 | 345,605 | 5:00 PM | 24,423 |
| Brighton | 224,624 | 300,670 | 8:00 AM | 22,545 |
| Flushing local | 220,671 | 246,058 | 4:00 PM | 16,249 |
| Queens Blvd west local | 195,929 | 259,981 | 5:00 PM | 15,754 |
| Jamaica | 189,202 | 254,946 | 8:00 AM | 17,913 |
| Queens Blvd east | 184,592 | 242,772 | 5:00 PM | 16,317 |
| White Plains Rd | 164,234 | 245,309 | 7:00 AM | 17,820 |
| Culver | 155,879 | 196,689 | 8:00 AM | 15,647 |
| Jerome Av | 155,539 | 221,393 | 4:00 PM | 12,739 |
| SAS Phase 1 | 147,888 | 192,323 | 5:00 PM | 15,089 |
| Culver local | 146,624 | 185,520 | 8:00 AM | 14,826 |
| 4 Av express | 146,548 | 177,194 | 5:00 PM | 14,199 |
| Eastern Pkwy express | 145,679 | 195,869 | 8:00 AM | 14,121 |
| Eastern Pkwy local | 143,621 | 191,666 | 8:00 AM | 12,625 |
| Upper Culver | 140,980 | 177,488 | 8:00 AM | 14,151 |
| Upper Culver local | 138,918 | 174,713 | 8:00 AM | 14,151 |
| Fulton St express | 137,252 | 195,137 | 5:00 PM | 13,733 |
| 4 Av local | 133,662 | 164,004 | 5:00 PM | 11,186 |
| Crosstown | 132,697 | 154,054 | 5:00 PM | 12,291 |
| Lenox Av | 128,719 | 189,389 | 8:00 AM | 11,359 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,446 |
| Jamaica local | 113,811 | 152,796 | 8:00 AM | 11,031 |
| Concourse | 112,816 | 178,511 | 4:00 PM | 9,841 |
| Brighton local | 108,387 | 143,620 | 8:00 AM | 9,746 |
| White Plains Rd local | 107,434 | 159,628 | 3:00 PM | 9,475 |
| Concourse local | 106,484 | 167,714 | 3:00 PM | 8,315 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,008 |
| Fulton St local | 91,947 | 122,191 | 5:00 PM | 6,998 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,855 |
| West End | 81,855 | 106,960 | 7:00 AM | 7,874 |
| Pelham local | 80,726 | 115,744 | 7:00 AM | 6,540 |
| Sea Beach | 79,197 | 87,031 | 5:00 PM | 7,347 |
| Brighton express | 66,470 | 92,341 | 8:00 AM | 7,137 |
| Nassau St | 63,610 | 88,484 | 5:00 PM | 6,021 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,523 |
| 42 St Shuttle | 57,285 | 77,045 | 5:00 PM | 6,576 |
| Hillside Av local | 55,669 | 77,367 | 5:00 PM | 4,801 |
| Myrtle Av | 48,030 | 60,453 | 8:00 AM | 4,220 |
| Lower Culver | 39,746 | 54,059 | 7:00 AM | 4,123 |
| Lower Culver local | 36,786 | 50,234 | 7:00 AM | 3,863 |
| Pelham express | 36,612 | 54,973 | 7:00 AM | 5,357 |
| Flushing express | 35,705 | 40,958 | 5:00 PM | 6,085 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,586 |
| Jamaica express | 26,999 | 37,002 | 8:00 AM | 4,109 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,769 |
| White Plains Rd express | 20,693 | 30,757 | 7:00 AM | 4,620 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Concourse express | 14,856 | 24,944 | 7:00 AM | 3,216 |
| Franklin Av Shuttle | 13,766 | 18,357 | 8:00 AM | 1,218 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 300 |
| Culver express | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Hillside Av express | 2,175 | 3,126 | 7:00 AM | 912 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
