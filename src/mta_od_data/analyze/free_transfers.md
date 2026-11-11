# Free transfers out of the system

Which transfers out of the system would save riders the most time if they were free, on an average weekday (103 weekdays, as `assign-range` routes them): routed as today, where the only free ones are Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, and with every walk between complexes on the streets free, out one entrance and in another, all at once.

A path's time saved is its OD row's mean journey as today less its own, from entering to leaving the train, split evenly between the transfers out of the system it makes. Two transfers serving the same riders split them, so either alone would save more than its share here. Changes between a complex's stations take `transfers.txt`'s flat times, mostly 180s, until the MTA publishes pathways. See `free_transfers.py` for the rest.

Produced by `mta-od-data analyze free-transfers --markdown-out src/mta_od_data/analyze/free_transfers.md`.

## Summary

| Measure | Value |
| --- | ---: |
| Riders on an average weekday | 4,054,989 |
| Riders making a free transfer out of the system | (9.7%) 392,277 |
| Rider time saved a day (h:mm) | 15,822:37 |
| By riders making a free transfer | 11,971:34 |
| By the rest, splitting differently (not attributed) | 3,851:03 |
| Time saved per rider making one | 1:50 |

## The 50 transfers saving the most

Each way's riders are in the order the transfer names its complexes.

| # | Transfer | Walk | Riders a day | Each way | Rider time saved a day (h:mm) | Time saved per rider |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Fulton St (G) ↔ Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) | 5:02 | 17,146 | 7,793 / 9,353 | 1,208:01 | 4:14 |
| 2 | Broadway (G) ↔ Lorimer St (M,J) | 3:55 | 11,535 | 6,691 / 4,844 | 1,114:08 | 5:48 |
| 3 | 59 St-Columbus Circle (1,A,C,B,D) ↔ 57 St-7 Av (N,Q,R,W) | 4:16 | 26,537 | 15,078 / 11,460 | 966:49 | 2:11 |
| 4 | Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 1:06 | 18,682 | 8,960 / 9,721 | 607:18 | 1:57 |
| 5 | Hunts Point Av (6) ↔ Simpson St (2,5) | 7:24 | 3,767 | 1,727 / 2,040 | 523:38 | 8:20 |
| 6 | 50 St (C,E) ↔ 50 St (1) | 2:46 | 15,340 | 9,601 / 5,739 | 505:23 | 1:59 |
| 7 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Hoyt St (2,3) | 3:33 | 7,688 | 5,035 / 2,653 | 436:14 | 3:24 |
| 8 | Chambers St (1,2,3) ↔ Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) | 2:56 | 9,735 | 5,366 / 4,369 | 362:55 | 2:14 |
| 9 | Whitlock Av (6) ↔ Freeman St (2,5) | 9:05 | 1,662 | 1,002 / 660 | 358:32 | 12:57 |
| 10 | 49 St (N,R,W) ↔ 50 St (1) | 2:17 | 11,771 | 5,044 / 6,727 | 266:31 | 1:22 |
| 11 | Lafayette Av (C) ↔ Atlantic Av-Barclays Ctr (2,3,4,5,B,D,N,Q,R) | 5:34 | 6,020 | 3,091 / 2,929 | 251:57 | 2:31 |
| 12 | Hoyt St (2,3) ↔ Jay St-MetroTech (A,C,F,R) | 2:53 | 7,642 | 3,577 / 4,066 | 238:08 | 1:52 |
| 13 | 7 Av (E,B,D) ↔ 57 St-7 Av (N,Q,R,W) | 3:11 | 10,378 | 4,507 / 5,872 | 227:11 | 1:19 |
| 14 | 116 St (C,B) ↔ 116 St (2,3) | 7:22 | 2,024 | 886 / 1,138 | 208:48 | 6:11 |
| 15 | 145 St (A,C,B,D) ↔ 145 St (1) | 7:48 | 4,894 | 2,578 / 2,316 | 207:08 | 2:32 |
| 16 | 36 St (M,R) ↔ 39 Av-Dutch Kills (N,W) | 4:40 | 2,592 | 1,161 / 1,430 | 206:54 | 4:47 |
| 17 | Rector St (1) ↔ Wall St (4,5) | 2:53 | 4,578 | 2,329 / 2,248 | 186:30 | 2:27 |
| 18 | Hoyt-Schermerhorn Sts (A,C,G) ↔ DeKalb Av (B,Q,R) | 6:00 | 7,974 | 4,675 / 3,299 | 178:41 | 1:21 |
| 19 | 135 St (C,B) ↔ 135 St (2,3) | 9:10 | 2,073 | 942 / 1,131 | 160:22 | 4:38 |
| 20 | Hewes St (M,J) ↔ Metropolitan Av/Lorimer St (G,L) | 9:43 | 1,389 | 205 / 1,185 | 158:20 | 6:50 |
| 21 | Hewes St (M,J) ↔ Broadway (G) | 4:04 | 1,454 | 1,454 / 0 | 136:53 | 5:39 |
| 22 | 116 St (6) ↔ 116 St (2,3) | 10:36 | 2,122 | 828 / 1,293 | 134:20 | 3:48 |
| 23 | Prince St (R,W) ↔ Broadway-Lafayette St/Bleecker St (6,B,D,F,M) | 3:11 | 7,215 | 3,147 / 4,067 | 134:08 | 1:07 |
| 24 | 47-50 Sts-Rockefeller Ctr (B,D,F,M) ↔ 50 St (1) | 4:51 | 6,768 | 3,754 / 3,014 | 128:35 | 1:08 |
| 25 | Nostrand Av (A,C) ↔ Franklin Av (C,S) | 4:18 | 1,992 | 1,030 / 962 | 128:25 | 3:52 |
| 26 | Bedford Park Blvd (B,D) ↔ Bedford Park Blvd-Lehman College (4) | 4:32 | 1,444 | 564 / 879 | 125:36 | 5:13 |
| 27 | 110 St (6) ↔ 110 St-Malcolm X Plaza (2,3) | 11:29 | 2,259 | 1,051 / 1,207 | 124:13 | 3:18 |
| 28 | Longwood Av (6) ↔ Prospect Av (2,5) | 8:19 | 1,108 | 565 / 543 | 121:57 | 6:36 |
| 29 | 3 Av (L) ↔ 14 St-Union Sq (4,5,6,L,N,Q,R,W) | 4:00 | 14,793 | 10,708 / 4,085 | 120:31 | 0:29 |
| 30 | 14 St/6 Av (1,2,3,L,F,M) ↔ 14 St/8 Av (A,C,E,L) | 4:19 | 6,350 | 4,062 / 2,289 | 116:48 | 1:06 |
| 31 | Queens Plaza (E,F,R) ↔ Queensboro Plaza (7,N,W) | 4:29 | 5,863 | 4,098 / 1,765 | 115:37 | 1:11 |
| 32 | Canal St (A,C,E) ↔ Canal St (1) | 2:39 | 2,843 | 1,804 / 1,038 | 113:38 | 2:24 |
| 33 | Fordham Rd (B,D) ↔ Fordham Rd (4) | 4:50 | 1,397 | 616 / 781 | 112:11 | 4:49 |
| 34 | 86 St (4,5,6) ↔ 86 St (Q) | 7:01 | 2,009 | 1,448 / 561 | 111:40 | 3:20 |
| 35 | Kingsbridge Rd (B,D) ↔ Kingsbridge Rd (4) | 4:54 | 835 | 371 / 465 | 84:21 | 6:03 |
| 36 | Cathedral Pkwy (110 St) (C,B) ↔ 110 St-Malcolm X Plaza (2,3) | 8:11 | 763 | 499 / 264 | 84:11 | 6:37 |
| 37 | 125 St (A,C,B,D) ↔ 125 St (2,3) | 9:16 | 1,808 | 822 / 986 | 83:15 | 2:46 |
| 38 | W 4 St-Wash Sq (A,C,E,B,D,F,M) ↔ Christopher St-Stonewall (1) | 4:33 | 6,465 | 3,251 / 3,214 | 82:12 | 0:46 |
| 39 | 125 St (4,5,6) ↔ 125 St (2,3) | 11:02 | 1,729 | 1,127 / 602 | 82:01 | 2:51 |
| 40 | 34 St-Penn Station (1,2,3) ↔ 34 St-Herald Sq (B,D,F,M,N,Q,R,W) | 4:59 | 11,951 | 4,543 / 7,408 | 81:03 | 0:24 |
| 41 | Rector St (R,W) ↔ Wall St (4,5) | 2:09 | 1,804 | 1,066 / 739 | 72:16 | 2:24 |
| 42 | 23 St (F,M) ↔ 23 St (1) | 3:43 | 3,948 | 2,347 / 1,601 | 70:37 | 1:04 |
| 43 | DeKalb Av (B,Q,R) ↔ Nevins St (2,3,4,5) | 3:45 | 7,789 | 5,203 / 2,585 | 69:26 | 0:32 |
| 44 | Flushing Av (G) ↔ Flushing Av (M,J) | 10:09 | 648 | 0 / 648 | 67:55 | 6:17 |
| 45 | City Hall (R,W) ↔ Chambers St/WTC/Park Place/Cortlandt St (2,3,A,C,E,R,W) | 2:39 | 2,659 | 1,641 / 1,018 | 66:27 | 1:30 |
| 46 | 145 St (A,C,B,D) ↔ 145 St (3) | 11:16 | 535 | 362 / 173 | 64:31 | 7:14 |
| 47 | Queens Plaza (E,F,R) ↔ 39 Av-Dutch Kills (N,W) | 6:35 | 1,412 | 0 / 1,412 | 63:34 | 2:42 |
| 48 | Hoyt-Schermerhorn Sts (A,C,G) ↔ Nevins St (2,3,4,5) | 6:55 | 1,403 | 908 / 496 | 62:02 | 2:39 |
| 49 | Parsons Blvd (F) ↔ Jamaica Center-Parsons/Archer (E,J,Z) | 9:06 | 831 | 433 / 398 | 60:23 | 4:22 |
| 50 | WTC Cortlandt (1) ↔ Fulton St (2,3,4,5,A,C,J,Z) | 4:38 | 2,226 | 1,053 / 1,172 | 59:06 | 1:36 |
