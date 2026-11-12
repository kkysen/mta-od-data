# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (5.7%) 230,219 |
| Rider time saved a day (h:mm) | 8,757:15 |
| By riders making a free transfer | 5,659:06 |
| By the rest, splitting differently (not attributed) | 3,098:09 |
| Time saved per rider making one | 1:28 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Hewes St (J,M) ↔ Broadway (G) | 5:54 | 6,092 | 1,272 / 4,820 | 670:33 | 6:36 |
| 2 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 7:32 | 9,885 | 4,991 / 4,894 | 500:10 | 3:02 |
| 3 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:50 | 3,144 | 1,573 / 1,571 | 453:26 | 8:39 |
| 4 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 5:07 | 6,019 | 3,934 / 2,085 | 264:54 | 2:38 |
| 5 | Whitlock Av (6) ↔ Freeman St (2,5) | 10:36 | 1,127 | 632 / 495 | 263:12 | 14:01 |
| 6 | Broadway (G) ↔ Lorimer St (J,M) | 5:59 | 3,188 | 0 / 3,188 | 259:01 | 4:52 |
| 7 | 50 St (C,E) ↔ 50 St (1) | 3:54 | 12,366 | 7,791 / 4,574 | 247:24 | 1:12 |
| 8 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 4:08 | 10,309 | 5,072 / 5,237 | 182:41 | 1:04 |
| 9 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:55 | 1,429 | 837 / 593 | 166:09 | 6:59 |
| 10 | 116 St (B,C) ↔ 116 St (2,3) | 8:32 | 1,499 | 662 / 837 | 155:05 | 6:12 |
| 11 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:55 | 5,488 | 2,742 / 2,746 | 153:23 | 1:41 |
| 12 | Rector St (1) ↔ Wall St (4,5) | 3:47 | 4,888 | 2,383 / 2,505 | 150:47 | 1:51 |
| 13 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 6:51 | 1,988 | 954 / 1,034 | 130:10 | 3:56 |
| 14 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 7:14 | 6,170 | 3,296 / 2,874 | 123:36 | 1:12 |
| 15 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 4:14 | 5,646 | 3,851 / 1,795 | 122:34 | 1:18 |
| 16 | 116 St (6) ↔ 116 St (2,3) | 11:05 | 2,459 | 909 / 1,550 | 117:10 | 2:52 |
| 17 | 145 St (A,B,C,D) ↔ 145 St (1) | 9:03 | 3,640 | 1,900 / 1,740 | 114:38 | 1:53 |
| 18 | 135 St (B,C) ↔ 135 St (2,3) | 10:31 | 1,485 | 585 / 900 | 106:25 | 4:18 |
| 19 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 6:09 | 1,159 | 477 / 681 | 102:50 | 5:20 |
| 20 | 86 St (4,5,6) ↔ 86 St (Q) | 7:40 | 1,857 | 1,393 / 463 | 100:45 | 3:15 |
| 21 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:54 | 2,243 | 1,093 / 1,150 | 98:58 | 2:39 |
| 22 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:38 | 1,181 | 465 / 716 | 98:08 | 4:59 |
| 23 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 3:12 | 6,127 | 3,148 / 2,979 | 98:03 | 0:58 |
| 24 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:28 | 2,185 | 1,338 / 847 | 94:01 | 2:35 |
| 25 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:50 | 2,077 | 1,019 / 1,058 | 92:22 | 2:40 |
| 26 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:43 | 5,974 | 2,713 / 3,261 | 91:05 | 0:55 |
| 27 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 5:35 | 4,105 | 2,312 / 1,793 | 87:54 | 1:17 |
| 28 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 4:12 | 4,200 | 2,069 / 2,131 | 83:24 | 1:11 |
| 29 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 12:08 | 1,969 | 977 / 993 | 80:38 | 2:27 |
| 30 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:27 | 5,157 | 2,914 / 2,243 | 73:58 | 0:52 |
| 31 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 6:28 | 619 | 291 / 328 | 68:40 | 6:40 |
| 32 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 9:38 | 626 | 413 / 213 | 63:13 | 6:04 |
| 33 | Rector St (R,W) ↔ Wall St (4,5) | 3:11 | 1,642 | 1,047 / 595 | 59:53 | 2:11 |
| 34 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:57 | 2,894 | 1,592 / 1,301 | 55:47 | 1:09 |
| 35 | Flushing Av (G) ↔ Flushing Av (J,M) | 12:02 | 559 | 0 / 559 | 53:19 | 5:43 |
| 36 | 49 St (N,R,W) ↔ 50 St (1) | 3:57 | 7,400 | 3,174 / 4,226 | 52:48 | 0:26 |
| 37 | 96 St (6) ↔ 96 St (Q) | 6:47 | 1,172 | 1,039 / 132 | 49:14 | 2:31 |
| 38 | 145 St (A,B,C,D) ↔ 145 St (3) | 12:40 | 448 | 299 / 148 | 47:29 | 6:22 |
| 39 | Marcy Av (J,M,Z) ↔ Broadway (G) | 10:49 | 664 | 241 / 422 | 40:42 | 3:41 |
| 40 | Flushing Av (G) ↔ Lorimer St (J,M) | 10:00 | 308 | 308 / 0 | 40:33 | 7:55 |
| 41 | WTC Cortlandt (1) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 5:35 | 2,615 | 1,203 / 1,412 | 39:05 | 0:54 |
| 42 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 9:39 | 1,099 | 527 / 571 | 38:10 | 2:05 |
| 43 | Canal St (A,C,E) ↔ Canal St (1) | 4:43 | 1,346 | 790 / 557 | 37:58 | 1:42 |
| 44 | Winthrop St (2,5) ↔ Parkside Av (Q) | 13:55 | 820 | 399 / 420 | 37:53 | 2:46 |
| 45 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:57 | 748 | 470 / 278 | 37:33 | 3:01 |
| 46 | 103 St (B,C) ↔ 103 St (1) | 10:48 | 629 | 246 / 383 | 35:22 | 3:22 |
| 47 | Dyckman St (A) ↔ Dyckman St (1) | 8:41 | 441 | 175 / 266 | 32:07 | 4:22 |
| 48 | WTC Cortlandt (1) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 4:17 | 1,225 | 753 / 472 | 32:03 | 1:34 |
| 49 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 7:54 | 4,333 | 2,556 / 1,778 | 31:29 | 0:26 |
| 50 | Avenue P (F) ↔ Bay Pkwy (N) | 13:37 | 315 | 145 / 169 | 30:48 | 5:52 |
