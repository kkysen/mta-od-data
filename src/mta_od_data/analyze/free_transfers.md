# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (6.4%) 260,584 |
| Rider time saved a day (h:mm) | 10,592:26 |
| By riders making a free transfer | 7,109:19 |
| By the rest, splitting differently (not attributed) | 3,483:08 |
| Time saved per rider making one | 1:38 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 5:58 | 12,309 | 5,600 / 6,710 | 749:41 | 3:39 |
| 2 | Broadway (G) ↔ Lorimer St (J,M) | 4:38 | 6,538 | 3,005 / 3,533 | 628:46 | 5:46 |
| 3 | Hewes St (J,M) ↔ Broadway (G) | 4:36 | 4,983 | 1,309 / 3,673 | 556:58 | 6:42 |
| 4 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:01 | 2,923 | 1,365 / 1,558 | 410:44 | 8:26 |
| 5 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 3:55 | 7,715 | 4,596 / 3,119 | 375:12 | 2:55 |
| 6 | Whitlock Av (6) ↔ Freeman St (2,5) | 9:32 | 1,459 | 810 / 648 | 326:15 | 13:25 |
| 7 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 5:50 | 10,857 | 5,448 / 5,409 | 294:26 | 1:38 |
| 8 | 50 St (C,E) ↔ 50 St (1) | 3:12 | 11,490 | 7,081 / 4,409 | 221:16 | 1:09 |
| 9 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 2:11 | 9,503 | 4,228 / 5,275 | 216:40 | 1:22 |
| 10 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 3:34 | 10,580 | 5,619 / 4,961 | 215:26 | 1:13 |
| 11 | 116 St (B,C) ↔ 116 St (2,3) | 7:46 | 1,910 | 835 / 1,075 | 194:36 | 6:07 |
| 12 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:16 | 6,753 | 4,840 / 1,913 | 184:08 | 1:38 |
| 13 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:02 | 5,295 | 2,608 / 2,687 | 174:49 | 1:59 |
| 14 | 145 St (A,B,C,D) ↔ 145 St (1) | 8:09 | 4,215 | 2,246 / 1,969 | 165:25 | 2:21 |
| 15 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 5:35 | 2,094 | 995 / 1,099 | 162:36 | 4:40 |
| 16 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 4:54 | 5,923 | 3,344 / 2,579 | 152:36 | 1:33 |
| 17 | 135 St (B,C) ↔ 135 St (2,3) | 9:43 | 1,871 | 831 / 1,040 | 137:57 | 4:25 |
| 18 | 116 St (6) ↔ 116 St (2,3) | 10:56 | 2,510 | 923 / 1,587 | 134:54 | 3:14 |
| 19 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 5:02 | 1,357 | 526 / 831 | 119:22 | 5:17 |
| 20 | Rector St (1) ↔ Wall St (4,5) | 3:13 | 4,021 | 2,038 / 1,983 | 117:01 | 1:45 |
| 21 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:40 | 1,003 | 549 / 453 | 116:21 | 6:58 |
| 22 | 86 St (4,5,6) ↔ 86 St (Q) | 7:23 | 1,999 | 1,474 / 525 | 110:50 | 3:20 |
| 23 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 3:18 | 4,602 | 2,425 / 2,177 | 99:47 | 1:18 |
| 24 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:12 | 1,133 | 500 / 633 | 93:29 | 4:57 |
| 25 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 11:57 | 1,845 | 881 / 964 | 88:13 | 2:52 |
| 26 | Flushing Av (G) ↔ Lorimer St (J,M) | 8:49 | 796 | 74 / 722 | 84:31 | 6:22 |
| 27 | Fulton St (G) ↔ Nevins St (2,3,4,5) | 6:57 | 1,213 | 829 / 385 | 80:15 | 3:58 |
| 28 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 8:48 | 741 | 492 / 249 | 78:35 | 6:22 |
| 29 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 6:30 | 5,833 | 3,571 / 2,262 | 78:19 | 0:48 |
| 30 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 5:23 | 742 | 286 / 456 | 76:12 | 6:10 |
| 31 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:23 | 1,759 | 1,131 / 628 | 75:15 | 2:34 |
| 32 | Canal St (A,C,E) ↔ Canal St (1) | 3:21 | 2,260 | 1,341 / 919 | 73:21 | 1:57 |
| 33 | Hunts Point Av (6) ↔ Intervale Av (2,5) | 9:50 | 308 | 219 / 89 | 69:33 | 13:32 |
| 34 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:34 | 4,302 | 2,021 / 2,281 | 64:31 | 0:54 |
| 35 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:38 | 1,503 | 689 / 813 | 63:26 | 2:32 |
| 36 | Hewes St (J,M) ↔ Metropolitan Av/Lorimer St (G,L) | 10:26 | 1,082 | 451 / 631 | 61:49 | 3:26 |
| 37 | Rector St (R,W) ↔ Wall St (4,5) | 2:29 | 1,617 | 894 / 723 | 55:44 | 2:04 |
| 38 | 49 St (N,R,W) ↔ 50 St (1) | 2:44 | 6,639 | 2,951 / 3,688 | 51:19 | 0:28 |
| 39 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:15 | 1,258 | 546 / 711 | 50:42 | 2:25 |
| 40 | 145 St (A,B,C,D) ↔ 145 St (3) | 11:33 | 454 | 290 / 165 | 49:59 | 6:36 |
| 41 | 96 St (6) ↔ 96 St (Q) | 6:39 | 1,073 | 962 / 111 | 47:13 | 2:38 |
| 42 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:25 | 4,058 | 2,047 / 2,011 | 46:33 | 0:41 |
| 43 | Parsons Blvd (F) ↔ Jamaica Center-Parsons/Archer (E,J,Z) | 9:43 | 726 | 384 / 342 | 44:36 | 3:41 |
| 44 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:11 | 2,288 | 1,427 / 861 | 42:02 | 1:06 |
| 45 | Nostrand Av (A,C) ↔ Franklin Av (C,S) | 6:54 | 1,044 | 441 / 604 | 41:43 | 2:24 |
| 46 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:05 | 779 | 482 / 296 | 40:53 | 3:09 |
| 47 | Dyckman St (A) ↔ Dyckman St (1) | 7:47 | 527 | 236 / 291 | 39:49 | 4:32 |
| 48 | 23 St (C,E) ↔ 23 St (1) | 4:27 | 1,692 | 733 / 959 | 38:33 | 1:22 |
| 49 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 8:34 | 1,099 | 538 / 562 | 38:31 | 2:06 |
| 50 | 103 St (B,C) ↔ 103 St (1) | 10:23 | 617 | 249 / 369 | 37:30 | 3:39 |
