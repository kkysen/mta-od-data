# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (6.5%) 263,162 |
| Rider time saved a day (h:mm) | 10,712:08 |
| By riders making a free transfer | 7,203:31 |
| By the rest, splitting differently (not attributed) | 3,508:37 |
| Time saved per rider making one | 1:39 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 5:58 | 12,405 | 5,616 / 6,789 | 764:03 | 3:42 |
| 2 | Broadway (G) ↔ Lorimer St (J,M) | 4:38 | 6,548 | 3,005 / 3,543 | 632:36 | 5:48 |
| 3 | Hewes St (J,M) ↔ Broadway (G) | 4:36 | 4,986 | 1,310 / 3,676 | 557:37 | 6:43 |
| 4 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:01 | 2,923 | 1,365 / 1,558 | 410:43 | 8:26 |
| 5 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 3:55 | 7,770 | 4,608 / 3,162 | 382:11 | 2:57 |
| 6 | Whitlock Av (6) ↔ Freeman St (2,5) | 9:32 | 1,459 | 811 / 648 | 326:14 | 13:25 |
| 7 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 5:50 | 10,875 | 5,448 / 5,426 | 294:58 | 1:38 |
| 8 | 50 St (C,E) ↔ 50 St (1) | 3:12 | 11,494 | 7,086 / 4,409 | 221:36 | 1:09 |
| 9 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 2:11 | 9,670 | 4,284 / 5,386 | 217:21 | 1:21 |
| 10 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 3:34 | 10,600 | 5,623 / 4,977 | 216:47 | 1:14 |
| 11 | 116 St (B,C) ↔ 116 St (2,3) | 7:46 | 1,911 | 835 / 1,076 | 194:30 | 6:06 |
| 12 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:16 | 6,818 | 4,861 / 1,957 | 190:08 | 1:40 |
| 13 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:02 | 5,340 | 2,626 / 2,714 | 178:44 | 2:01 |
| 14 | 145 St (A,B,C,D) ↔ 145 St (1) | 8:09 | 4,215 | 2,246 / 1,969 | 165:24 | 2:21 |
| 15 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 5:35 | 2,094 | 995 / 1,099 | 162:36 | 4:40 |
| 16 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 4:54 | 5,926 | 3,346 / 2,580 | 152:44 | 1:33 |
| 17 | 135 St (B,C) ↔ 135 St (2,3) | 9:43 | 1,871 | 831 / 1,040 | 137:57 | 4:25 |
| 18 | 116 St (6) ↔ 116 St (2,3) | 10:56 | 2,510 | 923 / 1,587 | 134:55 | 3:14 |
| 19 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 5:02 | 1,358 | 527 / 832 | 119:23 | 5:16 |
| 20 | Rector St (1) ↔ Wall St (4,5) | 3:13 | 4,052 | 2,044 / 2,008 | 118:40 | 1:45 |
| 21 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:40 | 1,003 | 549 / 453 | 116:21 | 6:58 |
| 22 | 86 St (4,5,6) ↔ 86 St (Q) | 7:23 | 1,999 | 1,474 / 526 | 110:47 | 3:19 |
| 23 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 3:18 | 4,793 | 2,562 / 2,231 | 109:35 | 1:22 |
| 24 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:12 | 1,133 | 500 / 633 | 93:30 | 4:57 |
| 25 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 11:57 | 1,845 | 881 / 964 | 88:14 | 2:52 |
| 26 | Flushing Av (G) ↔ Lorimer St (J,M) | 8:49 | 800 | 74 / 726 | 87:19 | 6:33 |
| 27 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 6:30 | 5,942 | 3,659 / 2,283 | 81:44 | 0:50 |
| 28 | Fulton St (G) ↔ Nevins St (2,3,4,5) | 6:57 | 1,215 | 829 / 386 | 80:39 | 3:59 |
| 29 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 8:48 | 741 | 492 / 249 | 78:35 | 6:22 |
| 30 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 5:23 | 742 | 286 / 456 | 76:13 | 6:10 |
| 31 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:23 | 1,759 | 1,131 / 628 | 75:17 | 2:34 |
| 32 | Canal St (A,C,E) ↔ Canal St (1) | 3:21 | 2,277 | 1,356 / 921 | 74:30 | 1:58 |
| 33 | Hunts Point Av (6) ↔ Intervale Av (2,5) | 9:50 | 308 | 219 / 89 | 69:33 | 13:32 |
| 34 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:34 | 4,380 | 2,044 / 2,336 | 67:46 | 0:56 |
| 35 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:38 | 1,505 | 689 / 815 | 63:28 | 2:32 |
| 36 | Hewes St (J,M) ↔ Metropolitan Av/Lorimer St (G,L) | 10:26 | 1,091 | 460 / 631 | 63:13 | 3:29 |
| 37 | Rector St (R,W) ↔ Wall St (4,5) | 2:29 | 1,658 | 892 / 766 | 56:17 | 2:02 |
| 38 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:25 | 4,130 | 2,107 / 2,023 | 53:42 | 0:47 |
| 39 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:15 | 1,276 | 552 / 725 | 52:54 | 2:29 |
| 40 | 49 St (N,R,W) ↔ 50 St (1) | 2:44 | 6,643 | 2,951 / 3,692 | 50:41 | 0:27 |
| 41 | 145 St (A,B,C,D) ↔ 145 St (3) | 11:33 | 454 | 290 / 165 | 49:59 | 6:36 |
| 42 | 96 St (6) ↔ 96 St (Q) | 6:39 | 1,073 | 962 / 111 | 47:13 | 2:38 |
| 43 | Parsons Blvd (F) ↔ Jamaica Center-Parsons/Archer (E,J,Z) | 9:43 | 725 | 382 / 342 | 44:26 | 3:41 |
| 44 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:11 | 2,309 | 1,436 / 873 | 44:02 | 1:09 |
| 45 | Nostrand Av (A,C) ↔ Franklin Av (C,S) | 6:54 | 1,047 | 438 / 610 | 42:25 | 2:26 |
| 46 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:05 | 779 | 482 / 297 | 40:53 | 3:09 |
| 47 | Dyckman St (A) ↔ Dyckman St (1) | 7:47 | 527 | 236 / 291 | 39:48 | 4:32 |
| 48 | 23 St (C,E) ↔ 23 St (1) | 4:27 | 1,692 | 733 / 959 | 38:33 | 1:22 |
| 49 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 8:34 | 1,101 | 537 / 564 | 38:22 | 2:06 |
| 50 | 103 St (B,C) ↔ 103 St (1) | 10:23 | 617 | 249 / 369 | 37:30 | 3:39 |
