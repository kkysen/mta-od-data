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
| Lexington Av | 981,184 | 1,310,277 | 5:00 PM | 108,767 |
| 8 Av | 866,223 | 1,165,489 | 5:00 PM | 92,625 |
| Broadway-7 Av | 836,997 | 1,129,896 | 5:00 PM | 97,903 |
| Broadway | 791,191 | 1,032,658 | 5:00 PM | 82,450 |
| 6 Av | 775,232 | 1,015,196 | 5:00 PM | 87,468 |
| Queens Blvd | 528,038 | 672,468 | 5:00 PM | 56,611 |
| Lexington Av express | 515,019 | 693,137 | 5:00 PM | 51,520 |
| Flushing | 514,888 | 590,090 | 5:00 PM | 57,255 |
| Lexington Av local | 507,775 | 663,660 | 8:00 AM | 48,771 |
| 8 Av local | 461,631 | 597,916 | 5:00 PM | 43,842 |
| Queens Blvd west | 454,491 | 585,057 | 5:00 PM | 44,882 |
| Broadway-7 Av local | 399,582 | 528,757 | 5:00 PM | 38,965 |
| Canarsie | 399,125 | 451,005 | 5:00 PM | 37,816 |
| Broadway local | 396,736 | 520,246 | 5:00 PM | 38,452 |
| Broadway-7 Av express | 384,062 | 529,328 | 5:00 PM | 39,083 |
| 8 Av express | 365,270 | 507,996 | 5:00 PM | 37,959 |
| 6 Av local | 343,249 | 447,686 | 5:00 PM | 36,401 |
| Broadway express | 340,289 | 438,417 | 5:00 PM | 36,082 |
| 53 St | 336,372 | 439,301 | 5:00 PM | 34,284 |
| Eastern Pkwy | 311,536 | 416,555 | 8:00 AM | 35,541 |
| 63 St | 304,041 | 392,552 | 5:00 PM | 31,244 |
| Manhattan Bridge | 301,563 | 384,374 | 5:00 PM | 29,781 |
| Queens Blvd express | 300,849 | 381,524 | 5:00 PM | 30,131 |
| Queens Blvd local | 292,359 | 390,159 | 7:00 AM | 24,662 |
| Queens Blvd west express | 291,307 | 368,964 | 5:00 PM | 29,105 |
| 4 Av | 289,248 | 352,118 | 8:00 AM | 30,795 |
| Fulton St | 267,137 | 365,238 | 5:00 PM | 25,757 |
| 6 Av express | 263,214 | 353,579 | 5:00 PM | 28,501 |
| Brighton | 239,712 | 319,782 | 8:00 AM | 24,117 |
| Flushing local | 237,008 | 262,683 | 7:00 AM | 17,320 |
| Queens Blvd west local | 199,433 | 264,704 | 8:00 AM | 16,390 |
| Jamaica | 197,800 | 266,056 | 8:00 AM | 19,100 |
| Queens Blvd east | 193,005 | 253,536 | 7:00 AM | 17,256 |
| White Plains Rd | 172,986 | 258,111 | 7:00 AM | 19,777 |
| Jerome Av | 167,827 | 237,917 | 7:00 AM | 13,809 |
| Culver | 164,155 | 206,943 | 8:00 AM | 16,915 |
| SAS Phase 1 | 154,685 | 200,753 | 8:00 AM | 16,412 |
| Culver local | 154,324 | 195,077 | 8:00 AM | 16,050 |
| Eastern Pkwy express | 154,140 | 206,656 | 8:00 AM | 15,582 |
| 4 Av express | 151,558 | 183,036 | 8:00 AM | 15,191 |
| Eastern Pkwy local | 150,207 | 200,176 | 8:00 AM | 13,734 |
| Upper Culver | 148,418 | 186,679 | 8:00 AM | 15,365 |
| Upper Culver local | 146,127 | 183,598 | 8:00 AM | 15,365 |
| Fulton St express | 143,453 | 203,899 | 5:00 PM | 14,465 |
| Crosstown | 140,802 | 163,253 | 5:00 PM | 12,938 |
| 4 Av local | 137,226 | 168,301 | 8:00 AM | 11,708 |
| Lenox Av | 132,547 | 194,840 | 8:00 AM | 11,973 |
| Pelham | 132,255 | 192,126 | 7:00 AM | 14,577 |
| Concourse | 120,031 | 188,706 | 7:00 AM | 10,668 |
| Jamaica local | 118,863 | 159,433 | 8:00 AM | 11,727 |
| Brighton local | 115,737 | 152,859 | 8:00 AM | 10,516 |
| Concourse local | 113,485 | 177,547 | 7:00 AM | 9,029 |
| White Plains Rd local | 113,110 | 167,855 | 3:00 PM | 10,203 |
| Astoria | 104,899 | 122,659 | 8:00 AM | 10,780 |
| Fulton St local | 98,582 | 130,766 | 5:00 PM | 7,563 |
| Nostrand Av | 86,753 | 111,669 | 8:00 AM | 8,407 |
| West End | 85,329 | 111,397 | 7:00 AM | 8,646 |
| Pelham local | 84,134 | 120,492 | 7:00 AM | 7,300 |
| Sea Beach | 82,481 | 90,484 | 7:00 AM | 7,884 |
| Brighton express | 70,951 | 98,341 | 8:00 AM | 7,714 |
| Nassau St | 66,166 | 92,008 | 5:00 PM | 6,280 |
| Hillside Av | 60,434 | 84,031 | 7:00 AM | 5,969 |
| 42 St Shuttle | 58,713 | 78,840 | 5:00 PM | 6,827 |
| Hillside Av local | 58,342 | 80,998 | 5:00 PM | 5,030 |
| Myrtle Av | 50,098 | 62,986 | 8:00 AM | 4,526 |
| Lower Culver | 42,303 | 57,428 | 7:00 AM | 4,511 |
| Flushing express | 39,908 | 45,329 | 5:00 PM | 6,923 |
| Lower Culver local | 39,135 | 53,337 | 7:00 AM | 4,219 |
| Pelham express | 37,170 | 55,884 | 7:00 AM | 5,579 |
| Rockaway | 29,331 | 52,320 | 5:00 PM | 2,808 |
| Jamaica express | 28,675 | 39,251 | 8:00 AM | 4,436 |
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
