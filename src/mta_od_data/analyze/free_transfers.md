# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (6.4%) 257,929 |
| Rider time saved a day (h:mm) | 10,524:12 |
| By riders making a free transfer | 7,088:23 |
| By the rest, splitting differently (not attributed) | 3,435:49 |
| Time saved per rider making one | 1:39 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 5:58 | 12,402 | 5,615 / 6,787 | 763:59 | 3:42 |
| 2 | Broadway (G) ↔ Lorimer St (J,M) | 4:38 | 6,546 | 3,004 / 3,542 | 632:33 | 5:48 |
| 3 | Hewes St (J,M) ↔ Broadway (G) | 4:36 | 4,983 | 1,310 / 3,673 | 557:23 | 6:43 |
| 4 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:01 | 2,923 | 1,365 / 1,558 | 410:42 | 8:26 |
| 5 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 3:55 | 7,770 | 4,607 / 3,163 | 382:04 | 2:57 |
| 6 | Whitlock Av (6) ↔ Freeman St (2,5) | 9:32 | 1,459 | 811 / 648 | 326:15 | 13:25 |
| 7 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 5:50 | 9,925 | 5,129 / 4,796 | 261:37 | 1:35 |
| 8 | 50 St (C,E) ↔ 50 St (1) | 3:12 | 11,207 | 6,957 / 4,250 | 221:42 | 1:11 |
| 9 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 2:11 | 9,607 | 4,254 / 5,353 | 218:53 | 1:22 |
| 10 | 116 St (B,C) ↔ 116 St (2,3) | 7:46 | 1,907 | 837 / 1,070 | 194:20 | 6:07 |
| 11 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:16 | 6,866 | 4,909 / 1,957 | 190:21 | 1:40 |
| 12 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:02 | 5,326 | 2,621 / 2,705 | 178:58 | 2:01 |
| 13 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 3:34 | 9,529 | 4,917 / 4,612 | 165:41 | 1:03 |
| 14 | 145 St (A,B,C,D) ↔ 145 St (1) | 8:09 | 4,214 | 2,245 / 1,970 | 165:26 | 2:21 |
| 15 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 5:35 | 2,093 | 995 / 1,098 | 162:33 | 4:40 |
| 16 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 4:54 | 5,771 | 3,298 / 2,473 | 149:33 | 1:33 |
| 17 | 135 St (B,C) ↔ 135 St (2,3) | 9:43 | 1,871 | 831 / 1,040 | 138:01 | 4:26 |
| 18 | 116 St (6) ↔ 116 St (2,3) | 10:56 | 2,509 | 923 / 1,586 | 134:53 | 3:14 |
| 19 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 5:02 | 1,358 | 527 / 832 | 119:25 | 5:17 |
| 20 | Rector St (1) ↔ Wall St (4,5) | 3:13 | 4,051 | 2,042 / 2,008 | 118:38 | 1:45 |
| 21 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:40 | 1,003 | 549 / 453 | 116:21 | 6:58 |
| 22 | 86 St (4,5,6) ↔ 86 St (Q) | 7:23 | 1,999 | 1,474 / 526 | 110:46 | 3:19 |
| 23 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 3:18 | 4,803 | 2,560 / 2,243 | 109:07 | 1:22 |
| 24 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:12 | 1,133 | 500 / 633 | 93:31 | 4:57 |
| 25 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 11:57 | 1,849 | 885 / 964 | 87:59 | 2:51 |
| 26 | Flushing Av (G) ↔ Lorimer St (J,M) | 8:49 | 800 | 74 / 726 | 87:19 | 6:33 |
| 27 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 6:30 | 5,856 | 3,648 / 2,208 | 81:23 | 0:50 |
| 28 | Fulton St (G) ↔ Nevins St (2,3,4,5) | 6:57 | 1,215 | 829 / 386 | 80:38 | 3:59 |
| 29 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 8:48 | 741 | 494 / 248 | 78:41 | 6:22 |
| 30 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 5:23 | 742 | 286 / 457 | 76:12 | 6:10 |
| 31 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:23 | 1,759 | 1,131 / 628 | 75:16 | 2:34 |
| 32 | Canal St (A,C,E) ↔ Canal St (1) | 3:21 | 2,291 | 1,359 / 931 | 74:21 | 1:57 |
| 33 | Hunts Point Av (6) ↔ Intervale Av (2,5) | 9:50 | 308 | 219 / 89 | 69:33 | 13:32 |
| 34 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:34 | 4,334 | 2,023 / 2,311 | 66:14 | 0:55 |
| 35 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:38 | 1,517 | 690 / 827 | 63:34 | 2:31 |
| 36 | Hewes St (J,M) ↔ Metropolitan Av/Lorimer St (G,L) | 10:26 | 1,091 | 460 / 631 | 63:13 | 3:29 |
| 37 | Rector St (R,W) ↔ Wall St (4,5) | 2:29 | 1,652 | 887 / 765 | 55:59 | 2:02 |
| 38 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:25 | 4,129 | 2,106 / 2,023 | 53:40 | 0:47 |
| 39 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:15 | 1,276 | 552 / 724 | 52:53 | 2:29 |
| 40 | 145 St (A,B,C,D) ↔ 145 St (3) | 11:33 | 454 | 288 / 165 | 49:55 | 6:36 |
| 41 | 49 St (N,R,W) ↔ 50 St (1) | 2:44 | 6,599 | 2,946 / 3,653 | 49:32 | 0:27 |
| 42 | 96 St (6) ↔ 96 St (Q) | 6:39 | 1,074 | 963 / 111 | 47:12 | 2:38 |
| 43 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:11 | 2,225 | 1,395 / 830 | 45:24 | 1:13 |
| 44 | Parsons Blvd (F) ↔ Jamaica Center-Parsons/Archer (E,J,Z) | 9:43 | 724 | 381 / 342 | 44:30 | 3:41 |
| 45 | Nostrand Av (A,C) ↔ Franklin Av (C,S) | 6:54 | 1,047 | 438 / 609 | 42:25 | 2:26 |
| 46 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:05 | 778 | 481 / 297 | 40:46 | 3:09 |
| 47 | Dyckman St (A) ↔ Dyckman St (1) | 7:47 | 527 | 236 / 291 | 39:47 | 4:32 |
| 48 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 8:34 | 1,098 | 534 / 564 | 38:31 | 2:06 |
| 49 | 23 St (C,E) ↔ 23 St (1) | 4:27 | 1,730 | 740 / 989 | 37:50 | 1:19 |
| 50 | 103 St (B,C) ↔ 103 St (1) | 10:23 | 617 | 249 / 368 | 37:30 | 3:39 |
