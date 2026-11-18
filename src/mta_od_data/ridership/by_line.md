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
| Lexington Av | 937,659 | 1,253,109 | 5:00 PM | 102,538 |
| 8 Av | 830,917 | 1,119,447 | 5:00 PM | 87,102 |
| Broadway-7 Av | 817,680 | 1,105,268 | 5:00 PM | 94,624 |
| Broadway | 782,591 | 1,023,067 | 5:00 PM | 81,066 |
| 6 Av | 770,772 | 1,011,761 | 5:00 PM | 85,778 |
| Queens Blvd | 504,237 | 643,632 | 5:00 PM | 54,020 |
| Lexington Av local | 491,225 | 642,556 | 5:00 PM | 46,290 |
| Flushing | 488,486 | 561,645 | 5:00 PM | 54,244 |
| Lexington Av express | 486,255 | 655,307 | 5:00 PM | 47,867 |
| Queens Blvd west | 444,755 | 572,152 | 5:00 PM | 44,515 |
| 8 Av local | 436,295 | 565,164 | 5:00 PM | 41,557 |
| Broadway local | 400,817 | 526,187 | 5:00 PM | 38,689 |
| Broadway-7 Av local | 395,898 | 524,945 | 5:00 PM | 38,185 |
| Canarsie | 381,164 | 431,011 | 5:00 PM | 35,951 |
| Broadway-7 Av express | 373,090 | 514,690 | 5:00 PM | 37,675 |
| 8 Av express | 357,253 | 497,531 | 5:00 PM | 35,705 |
| 53 St | 343,730 | 449,750 | 5:00 PM | 34,921 |
| 6 Av local | 341,439 | 446,702 | 5:00 PM | 35,667 |
| Broadway express | 331,890 | 428,419 | 5:00 PM | 35,004 |
| Queens Blvd express | 298,596 | 378,685 | 5:00 PM | 29,777 |
| Eastern Pkwy | 294,602 | 394,541 | 8:00 AM | 32,574 |
| Manhattan Bridge | 291,378 | 371,749 | 5:00 PM | 28,691 |
| Queens Blvd west express | 289,250 | 366,388 | 5:00 PM | 28,759 |
| Queens Blvd local | 284,009 | 378,988 | 8:00 AM | 23,523 |
| 4 Av | 277,876 | 338,292 | 8:00 AM | 28,711 |
| 63 St | 273,397 | 353,979 | 5:00 PM | 27,578 |
| 6 Av express | 261,568 | 351,934 | 5:00 PM | 27,744 |
| Fulton St | 252,456 | 345,591 | 5:00 PM | 24,422 |
| Brighton | 224,579 | 300,615 | 8:00 AM | 22,550 |
| Flushing local | 220,813 | 246,214 | 4:00 PM | 16,263 |
| Queens Blvd west local | 196,177 | 260,252 | 5:00 PM | 15,756 |
| Jamaica | 189,209 | 254,956 | 8:00 AM | 17,913 |
| Queens Blvd east | 184,583 | 242,763 | 5:00 PM | 16,315 |
| White Plains Rd | 164,234 | 245,308 | 7:00 AM | 17,820 |
| Culver | 155,896 | 196,709 | 8:00 AM | 15,648 |
| Jerome Av | 155,604 | 221,480 | 4:00 PM | 12,744 |
| SAS Phase 1 | 147,769 | 192,152 | 5:00 PM | 15,086 |
| Culver local | 146,642 | 185,541 | 8:00 AM | 14,827 |
| 4 Av express | 146,504 | 177,143 | 5:00 PM | 14,197 |
| Eastern Pkwy express | 145,680 | 195,871 | 8:00 AM | 14,122 |
| Eastern Pkwy local | 143,632 | 191,679 | 8:00 AM | 12,624 |
| Upper Culver | 140,997 | 177,508 | 8:00 AM | 14,152 |
| Upper Culver local | 138,935 | 174,733 | 8:00 AM | 14,152 |
| Fulton St express | 137,224 | 195,105 | 5:00 PM | 13,732 |
| 4 Av local | 133,710 | 164,058 | 5:00 PM | 11,189 |
| Crosstown | 132,782 | 154,161 | 5:00 PM | 12,296 |
| Lenox Av | 128,735 | 189,411 | 8:00 AM | 11,358 |
| Pelham | 126,272 | 183,651 | 7:00 AM | 13,446 |
| Jamaica local | 113,822 | 152,811 | 8:00 AM | 11,032 |
| Concourse | 112,877 | 178,598 | 4:00 PM | 9,848 |
| Brighton local | 108,332 | 143,543 | 8:00 AM | 9,743 |
| White Plains Rd local | 107,434 | 159,628 | 3:00 PM | 9,475 |
| Concourse local | 106,545 | 167,800 | 3:00 PM | 8,319 |
| Astoria | 101,023 | 118,222 | 8:00 AM | 10,008 |
| Fulton St local | 91,956 | 122,202 | 5:00 PM | 6,998 |
| Nostrand Av | 82,120 | 105,809 | 8:00 AM | 7,855 |
| West End | 81,869 | 106,977 | 7:00 AM | 7,875 |
| Pelham local | 80,726 | 115,745 | 7:00 AM | 6,541 |
| Sea Beach | 79,183 | 87,014 | 5:00 PM | 7,347 |
| Brighton express | 66,575 | 92,483 | 8:00 AM | 7,145 |
| Nassau St | 63,752 | 88,668 | 5:00 PM | 6,035 |
| 42 St Shuttle | 58,777 | 78,965 | 5:00 PM | 6,699 |
| Hillside Av | 57,653 | 80,236 | 7:00 AM | 5,523 |
| Hillside Av local | 55,675 | 77,374 | 5:00 PM | 4,803 |
| Myrtle Av | 48,030 | 60,453 | 8:00 AM | 4,220 |
| Lower Culver | 39,757 | 54,072 | 7:00 AM | 4,124 |
| Lower Culver local | 36,797 | 50,247 | 7:00 AM | 3,864 |
| Pelham express | 36,609 | 54,969 | 7:00 AM | 5,356 |
| Flushing express | 35,638 | 40,881 | 5:00 PM | 6,084 |
| Rockaway | 27,467 | 49,200 | 7:00 AM | 2,586 |
| Jamaica express | 27,007 | 37,011 | 8:00 AM | 4,109 |
| Dyre Av | 25,099 | 37,996 | 7:00 AM | 2,769 |
| White Plains Rd express | 20,693 | 30,757 | 7:00 AM | 4,619 |
| Far Rockaway branch | 16,535 | 34,093 | 7:00 AM | 1,572 |
| Lefferts branch | 16,087 | 24,484 | 7:00 AM | 1,668 |
| Concourse express | 14,862 | 24,952 | 7:00 AM | 3,217 |
| Franklin Av Shuttle | 13,770 | 18,363 | 8:00 AM | 1,218 |
| Rockaway Park branch | 3,201 | 6,265 | 7:00 AM | 300 |
| Culver express | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Upper Culver express | 2,381 | 3,192 | 7:00 AM | 1,409 |
| Hillside Av express | 2,169 | 3,118 | 7:00 AM | 910 |

</details>

## Charts

### Riders by line

<details>
<summary>The chart</summary>

![Riders by line](by_line-riders.svg)

</details>
