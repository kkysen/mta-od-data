# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (22 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --month 2025-09 --markdown-out src/mta_od_data/analyze/2025-09/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,181,290 |
| Riders making a free transfer out of the system | (6.3%) 264,664 |
| Rider time saved a day (h:mm) | 10,845:51 |
| By riders making a free transfer | 7,325:59 |
| By the rest, splitting differently (not attributed) | 3,519:52 |
| Time saved per rider making one | 1:40 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 5:58 | 12,774 | 5,747 / 7,027 | 783:05 | 3:41 |
| 2 | Broadway (G) ↔ Lorimer St (J,M) | 4:38 | 6,740 | 3,163 / 3,577 | 648:52 | 5:47 |
| 3 | Hewes St (J,M) ↔ Broadway (G) | 4:36 | 5,152 | 1,362 / 3,790 | 574:44 | 6:42 |
| 4 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:01 | 3,101 | 1,416 / 1,685 | 424:00 | 8:12 |
| 5 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 3:55 | 8,107 | 4,780 / 3,327 | 385:11 | 2:51 |
| 6 | Whitlock Av (6) ↔ Freeman St (2,5) | 9:32 | 1,537 | 857 / 680 | 353:11 | 13:47 |
| 7 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 5:50 | 11,083 | 5,544 / 5,538 | 298:17 | 1:37 |
| 8 | 50 St (C,E) ↔ 50 St (1) | 3:12 | 11,725 | 7,272 / 4,454 | 227:52 | 1:10 |
| 9 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 2:11 | 9,562 | 4,332 / 5,230 | 217:48 | 1:22 |
| 10 | 116 St (B,C) ↔ 116 St (2,3) | 7:46 | 2,052 | 906 / 1,147 | 203:03 | 5:56 |
| 11 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 3:34 | 9,936 | 5,336 / 4,600 | 201:18 | 1:13 |
| 12 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:16 | 6,912 | 4,980 / 1,932 | 191:44 | 1:40 |
| 13 | 145 St (A,B,C,D) ↔ 145 St (1) | 8:09 | 4,415 | 2,368 / 2,047 | 175:37 | 2:23 |
| 14 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 5:35 | 2,269 | 1,059 / 1,210 | 174:07 | 4:36 |
| 15 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:02 | 5,533 | 2,709 / 2,824 | 170:54 | 1:51 |
| 16 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 4:54 | 5,846 | 3,366 / 2,479 | 152:24 | 1:34 |
| 17 | 135 St (B,C) ↔ 135 St (2,3) | 9:43 | 1,887 | 808 / 1,079 | 137:43 | 4:23 |
| 18 | 116 St (6) ↔ 116 St (2,3) | 10:56 | 2,520 | 951 / 1,568 | 136:31 | 3:15 |
| 19 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:40 | 1,058 | 590 / 468 | 123:56 | 7:02 |
| 20 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 5:02 | 1,391 | 547 / 845 | 121:31 | 5:14 |
| 21 | Rector St (1) ↔ Wall St (4,5) | 3:13 | 4,114 | 2,027 / 2,087 | 119:03 | 1:44 |
| 22 | 86 St (4,5,6) ↔ 86 St (Q) | 7:23 | 2,132 | 1,583 / 550 | 116:10 | 3:16 |
| 23 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 3:18 | 4,682 | 2,430 / 2,252 | 97:25 | 1:15 |
| 24 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:12 | 1,140 | 462 / 678 | 94:31 | 4:59 |
| 25 | Flushing Av (G) ↔ Lorimer St (J,M) | 8:49 | 822 | 75 / 747 | 87:31 | 6:23 |
| 26 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 11:57 | 1,840 | 867 / 973 | 87:02 | 2:50 |
| 27 | Fulton St (G) ↔ Nevins St (2,3,4,5) | 6:57 | 1,265 | 863 / 403 | 83:11 | 3:57 |
| 28 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 5:23 | 797 | 304 / 493 | 81:47 | 6:09 |
| 29 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:23 | 1,873 | 1,195 / 678 | 78:56 | 2:32 |
| 30 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 6:30 | 6,007 | 3,597 / 2,410 | 78:33 | 0:47 |
| 31 | Canal St (A,C,E) ↔ Canal St (1) | 3:21 | 2,444 | 1,533 / 911 | 75:47 | 1:52 |
| 32 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 8:48 | 728 | 494 / 234 | 73:46 | 6:05 |
| 33 | Hunts Point Av (6) ↔ Intervale Av (2,5) | 9:50 | 308 | 218 / 90 | 65:57 | 12:50 |
| 34 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:34 | 4,289 | 1,994 / 2,295 | 65:34 | 0:55 |
| 35 | Hewes St (J,M) ↔ Metropolitan Av/Lorimer St (G,L) | 10:26 | 1,131 | 461 / 670 | 63:17 | 3:21 |
| 36 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:38 | 1,503 | 674 / 829 | 61:16 | 2:27 |
| 37 | Rector St (R,W) ↔ Wall St (4,5) | 2:29 | 1,619 | 862 / 757 | 54:52 | 2:02 |
| 38 | 145 St (A,B,C,D) ↔ 145 St (3) | 11:33 | 483 | 311 / 172 | 53:13 | 6:36 |
| 39 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:15 | 1,293 | 539 / 755 | 50:31 | 2:21 |
| 40 | 49 St (N,R,W) ↔ 50 St (1) | 2:44 | 6,684 | 2,996 / 3,687 | 49:47 | 0:27 |
| 41 | Dyckman St (A) ↔ Dyckman St (1) | 7:47 | 610 | 262 / 348 | 49:05 | 4:50 |
| 42 | 96 St (6) ↔ 96 St (Q) | 6:39 | 1,101 | 993 / 108 | 49:03 | 2:40 |
| 43 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:25 | 4,162 | 2,053 / 2,109 | 48:28 | 0:42 |
| 44 | Parsons Blvd (F) ↔ Jamaica Center-Parsons/Archer (E,J,Z) | 9:43 | 752 | 402 / 349 | 46:05 | 3:41 |
| 45 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:05 | 817 | 517 / 300 | 44:07 | 3:14 |
| 46 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:11 | 2,283 | 1,459 / 825 | 43:44 | 1:09 |
| 47 | 57 St (M) ↔ 59 St-Columbus Circle (1,A,B,C,D) | 8:49 | 2,720 | 1,781 / 939 | 40:50 | 0:54 |
| 48 | Nostrand Av (A,C) ↔ Franklin Av (C,S) | 6:54 | 1,102 | 428 / 674 | 39:59 | 2:11 |
| 49 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 8:34 | 1,177 | 584 / 593 | 38:09 | 1:57 |
| 50 | 103 St (B,C) ↔ 103 St (1) | 10:23 | 649 | 258 / 390 | 37:48 | 3:30 |
