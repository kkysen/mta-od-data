# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (5.8%) 235,052 |
| Rider time saved a day (h:mm) | 8,948:55 |
| By riders making a free transfer | 5,771:54 |
| By the rest, splitting differently (not attributed) | 3,177:01 |
| Time saved per rider making one | 1:28 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Hewes St (J,M) ↔ Broadway (G) | 5:54 | 4,826 | 1,202 / 3,624 | 545:34 | 6:47 |
| 2 | Fulton St (G) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 7:32 | 9,516 | 4,754 / 4,762 | 488:48 | 3:05 |
| 3 | Broadway (G) ↔ Lorimer St (J,M) | 5:59 | 5,030 | 2,064 / 2,966 | 461:29 | 5:30 |
| 4 | Hunts Point Av (6) ↔ Simpson St (2,5) | 8:50 | 2,926 | 1,363 / 1,563 | 408:52 | 8:23 |
| 5 | 50 St (C,E) ↔ 50 St (1) | 3:54 | 12,309 | 7,735 / 4,574 | 247:59 | 1:13 |
| 6 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 5:07 | 5,603 | 3,601 / 2,002 | 245:17 | 2:38 |
| 7 | Whitlock Av (6) ↔ Freeman St (2,5) | 10:36 | 1,003 | 531 / 473 | 233:26 | 13:58 |
| 8 | 7 Av (B,D,E) ↔ 57 St-7 Av (N,Q,R,W) | 4:08 | 10,211 | 4,985 / 5,225 | 182:28 | 1:04 |
| 9 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:55 | 1,384 | 800 / 585 | 159:13 | 6:54 |
| 10 | Lafayette Av (C) ↔ Atlantic Av (2,3,4,5,B,D,N,Q,R) | 6:55 | 5,398 | 2,667 / 2,731 | 153:39 | 1:42 |
| 11 | 116 St (B,C) ↔ 116 St (2,3) | 8:32 | 1,486 | 649 / 836 | 153:22 | 6:12 |
| 12 | Rector St (1) ↔ Wall St (4,5) | 3:47 | 4,759 | 2,353 / 2,406 | 149:45 | 1:53 |
| 13 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 6:51 | 1,975 | 943 / 1,032 | 130:06 | 3:57 |
| 14 | 59 St-Columbus Circle (1,A,B,C,D) ↔ 57 St-7 Av (N,Q,R,W) | 7:14 | 6,111 | 3,293 / 2,818 | 123:37 | 1:13 |
| 15 | 116 St (6) ↔ 116 St (2,3) | 11:05 | 2,456 | 906 / 1,550 | 117:33 | 2:52 |
| 16 | 145 St (A,B,C,D) ↔ 145 St (1) | 9:03 | 3,639 | 1,900 / 1,740 | 114:39 | 1:53 |
| 17 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 4:14 | 5,335 | 3,849 / 1,486 | 113:36 | 1:17 |
| 18 | 135 St (B,C) ↔ 135 St (2,3) | 10:31 | 1,480 | 581 / 899 | 105:41 | 4:17 |
| 19 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 6:09 | 1,147 | 466 / 680 | 101:15 | 5:18 |
| 20 | 86 St (4,5,6) ↔ 86 St (Q) | 7:40 | 1,851 | 1,388 / 463 | 100:50 | 3:16 |
| 21 | Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 3:12 | 5,969 | 3,119 / 2,850 | 100:16 | 1:00 |
| 22 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 5:38 | 1,174 | 459 / 715 | 96:38 | 4:56 |
| 23 | 125 St (A,B,C,D) ↔ 125 St (2,3) | 9:54 | 2,226 | 1,077 / 1,149 | 96:38 | 2:36 |
| 24 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:28 | 2,184 | 1,337 / 847 | 94:03 | 2:35 |
| 25 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:43 | 5,918 | 2,709 / 3,209 | 90:55 | 0:55 |
| 26 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 5:35 | 4,072 | 2,287 / 1,785 | 89:55 | 1:19 |
| 27 | Hunts Point Av (6) ↔ Intervale Av (2,5) | 10:30 | 397 | 299 / 98 | 89:05 | 13:27 |
| 28 | Borough Hall/Court St (2,3,4,5,R) ↔ Jay St-MetroTech (A,C,F,R) | 5:27 | 5,493 | 2,892 / 2,601 | 88:54 | 0:58 |
| 29 | Flushing Av (G) ↔ Lorimer St (J,M) | 10:00 | 809 | 82 / 727 | 84:03 | 6:14 |
| 30 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 12:08 | 1,967 | 975 / 992 | 80:58 | 2:28 |
| 31 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 4:12 | 4,007 | 2,050 / 1,957 | 78:03 | 1:10 |
| 32 | Fulton St (G) ↔ Nevins St (2,3,4,5) | 8:07 | 1,126 | 914 / 212 | 71:32 | 3:49 |
| 33 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 6:28 | 613 | 286 / 327 | 67:50 | 6:38 |
| 34 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 7:50 | 1,587 | 609 / 978 | 65:05 | 2:28 |
| 35 | Cathedral Pkwy (110 St) (B,C) ↔ 110 St-Malcolm X Plaza (2,3) | 9:38 | 621 | 411 / 209 | 62:42 | 6:04 |
| 36 | Rector St (R,W) ↔ Wall St (4,5) | 3:11 | 1,633 | 1,041 / 592 | 59:43 | 2:12 |
| 37 | City Hall (R,W) ↔ Chambers St/WTC/Park Pl/Cortlandt St (2,3,A,C,E,R,W) | 3:57 | 2,867 | 1,578 / 1,289 | 55:35 | 1:10 |
| 38 | 49 St (N,R,W) ↔ 50 St (1) | 3:57 | 7,369 | 3,163 / 4,206 | 51:42 | 0:25 |
| 39 | 96 St (6) ↔ 96 St (Q) | 6:47 | 1,158 | 1,026 / 132 | 49:24 | 2:34 |
| 40 | 145 St (A,B,C,D) ↔ 145 St (3) | 12:40 | 417 | 268 / 148 | 44:55 | 6:28 |
| 41 | WTC Cortlandt (1) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 5:35 | 2,506 | 1,179 / 1,327 | 41:34 | 1:00 |
| 42 | Canal St (A,C,E) ↔ Franklin St (1) | 4:43 | 1,341 | 843 / 497 | 41:03 | 1:50 |
| 43 | Marcy Av (J,M,Z) ↔ Broadway (G) | 10:49 | 624 | 207 / 417 | 41:00 | 3:56 |
| 44 | Sutphin Blvd (F) ↔ Sutphin Blvd-Archer Av-JFK Airport (E,J,Z) | 9:39 | 1,097 | 526 / 571 | 38:05 | 2:05 |
| 45 | Winthrop St (2,5) ↔ Parkside Av (Q) | 13:55 | 820 | 399 / 420 | 37:53 | 2:46 |
| 46 | Tremont Av (B,D) ↔ Burnside Av (4) | 7:57 | 738 | 461 / 277 | 37:16 | 3:02 |
| 47 | 103 St (B,C) ↔ 103 St (1) | 10:48 | 629 | 246 / 383 | 35:22 | 3:22 |
| 48 | Canal St (A,C,E) ↔ Canal St (1) | 4:43 | 1,197 | 643 / 554 | 34:34 | 1:44 |
| 49 | Dyckman St (A) ↔ Dyckman St (1) | 8:41 | 435 | 170 / 266 | 32:09 | 4:26 |
| 50 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 7:54 | 4,256 | 2,492 / 1,764 | 31:54 | 0:27 |
