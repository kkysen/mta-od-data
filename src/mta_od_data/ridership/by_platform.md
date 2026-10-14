# Ridership by platform

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.

Produced by `mta-od-data ridership --by platform --markdown-out src/mta_od_data/ridership/by_platform.md`.

| Platform | Name | On + Off, Aug-Dec 2025 | On + Off, 2019 | On, Aug-Dec 2025 | Off, Aug-Dec 2025 | Transfers On + Off, Aug-Dec 2025 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 631N | Grand Central-42 St (4,5,6), Uptown | 178,315 | 235,680 | 81,187 | 97,129 | 96,310 |
| 631S | Grand Central-42 St (4,5,6), Downtown | 169,860 | 224,037 | 90,634 | 79,226 | 86,915 |
| 127N | Times Sq-42 St (1,2,3), Uptown | 158,225 | 210,961 | 86,368 | 71,858 | 113,103 |
| 127S | Times Sq-42 St (1,2,3), Downtown | 155,389 | 208,181 | 71,163 | 84,227 | 114,585 |
| 635N | 14 St-Union Sq (4,5,6), Uptown | 133,965 | 174,311 | 83,762 | 50,203 | 95,374 |
| 635S | 14 St-Union Sq (4,5,6), Downtown | 125,990 | 164,350 | 40,367 | 85,623 | 87,687 |
| G14S | Jackson Hts-Roosevelt Av (E,F,M,R), Manhattan | 119,427 | 142,197 | 81,328 | 38,100 | 77,517 |
| R16S | Times Sq-42 St (N,Q,R,W), Downtown | 116,454 | 151,931 | 64,134 | 52,321 | 71,414 |
| A27S | 42 St-PABT (A,C,E), Downtown | 113,976 | 150,830 | 49,412 | 64,564 | 65,249 |
| G14N | Jackson Hts-Roosevelt Av (E,F,M,R), Outbound | 111,049 | 132,819 | 38,386 | 72,664 | 72,007 |
| R16N | Times Sq-42 St (N,Q,R,W), Uptown | 101,187 | 131,690 | 44,590 | 56,597 | 59,790 |
| A27N | 42 St-PABT (A,C,E), Uptown | 99,495 | 130,774 | 58,834 | 40,660 | 52,700 |
| R20S | 14 St-Union Sq (N,Q,R,W), Downtown | 93,588 | 121,446 | 42,651 | 50,937 | 60,043 |
| D16S | 42 St-Bryant Pk (B,D,F,M), Downtown | 91,321 | 119,305 | 46,858 | 44,463 | 55,848 |
| A24N | 59 St-Columbus Circle (A,B,C,D), Uptown | 90,550 | 122,009 | 37,866 | 52,684 | 50,927 |
| A24S | 59 St-Columbus Circle (A,B,C,D), Downtown | 89,295 | 118,142 | 53,271 | 36,023 | 49,371 |
| D21N | Broadway-Lafayette St (B,D,F,M), Uptown | 87,958 | 111,560 | 35,582 | 52,376 | 63,848 |
| R20N | 14 St-Union Sq (N,Q,R,W), Uptown | 86,809 | 112,700 | 49,360 | 37,449 | 55,845 |
| D17N | 34 St-Herald Sq (B,D,F,M), Uptown | 86,274 | 123,251 | 47,656 | 38,618 | 37,749 |
| 629S | 59 St (4,5,6), Downtown | 85,178 | 112,672 | 41,032 | 44,146 | 57,980 |
| 629N | 59 St (4,5,6), Uptown | 81,307 | 107,585 | 37,229 | 44,078 | 50,764 |
| L03S | 14 St-Union Sq (L), Brooklyn | 77,785 | 90,061 | 61,231 | 16,554 | 61,579 |
| 132N | 14 St (1,2,3), Uptown | 77,704 | 101,298 | 45,698 | 32,006 | 60,312 |
| L03N | 14 St-Union Sq (L), West Side | 76,732 | 89,493 | 17,050 | 59,682 | 60,140 |
| A41N | Jay St-MetroTech (A,C,F), Manhattan | 75,212 | 100,931 | 38,500 | 36,712 | 48,536 |
| D20S | W 4 St-Wash Sq (B,D,F,M), Downtown | 74,642 | 94,306 | 36,458 | 38,184 | 49,299 |
| 123S | 72 St (1,2,3), Downtown | 72,950 | 95,739 | 45,022 | 27,928 | 39,561 |
| 123N | 72 St (1,2,3), Uptown | 72,462 | 94,585 | 27,032 | 45,430 | 38,959 |
| D17S | 34 St-Herald Sq (B,D,F,M), Downtown | 72,070 | 104,139 | 29,255 | 42,815 | 25,817 |
| R31N | Atlantic Av (D,N,R), Manhattan | 71,648 | 89,320 | 25,629 | 46,019 | 57,533 |
| R17N | 34 St-Herald Sq (N,Q,R,W), Uptown | 71,073 | 100,553 | 34,166 | 36,907 | 29,269 |
| R17S | 34 St-Herald Sq (N,Q,R,W), Downtown | 70,656 | 100,901 | 38,069 | 32,587 | 24,053 |
| R31S | Atlantic Av (D,N,R), Southbound | 70,618 | 87,621 | 42,633 | 27,986 | 55,138 |
| 621S | 125 St (4,5,6), Downtown | 70,001 | 101,475 | 31,227 | 38,774 | 49,888 |
| A28N | 34 St-Penn Station (A,C,E), Uptown | 69,700 | 89,084 | 40,816 | 28,884 | 17 |
| A28S | 34 St-Penn Station (A,C,E), Downtown | 69,121 | 88,167 | 30,412 | 38,708 | 17 |
| 132S | 14 St (1,2,3), Downtown | 67,382 | 87,746 | 28,002 | 39,380 | 49,762 |
| 725N | Times Sq-42 St (7), Queens | 66,269 | 79,580 | 55,827 | 10,442 | 49,998 |
| A41S | Jay St-MetroTech (A,C,F), Outbound | 65,263 | 88,049 | 31,802 | 33,461 | 39,817 |
| 725S | Times Sq-42 St (7), Hudson Yards | 61,966 | 73,821 | 10,608 | 51,358 | 46,904 |
| B08S | Lexington Av/63 St (M,Q), Downtown | 61,373 | 80,021 | 19,174 | 42,199 | 46,408 |
| D16N | 42 St-Bryant Pk (B,D,F,M), Uptown | 61,163 | 80,032 | 28,518 | 32,644 | 26,780 |
| 128S | 34 St-Penn Station (1,2,3), Downtown | 61,040 | 90,241 | 24,763 | 36,276 | 1 |
| 723N | Grand Central-42 St (7), Queens | 60,913 | 74,066 | 32,099 | 28,813 | 29,712 |
| 128N | 34 St-Penn Station (1,2,3), Uptown | 60,854 | 89,449 | 37,429 | 23,425 | 108 |
| B08N | Lexington Av/63 St (M,Q), Uptown & Queens | 60,364 | 79,788 | 43,353 | 17,011 | 42,301 |
| 630S | 51 St (6), Downtown | 59,682 | 80,239 | 36,356 | 23,326 | 32,940 |
| F11S | Lexington Av/53 St (E,F), Downtown | 59,362 | 78,953 | 19,590 | 39,772 | 34,750 |
| 235N | Atlantic Av (2,3,4,5), Manhattan | 58,237 | 76,066 | 32,792 | 25,445 | 43,380 |
| 630N | 51 St (6), Uptown | 57,770 | 77,641 | 25,416 | 32,355 | 31,821 |
| R11S | Lexington Av/59 St (N,R,W), Downtown | 57,212 | 73,326 | 19,227 | 37,985 | 41,069 |
| 710S | 74 St-Broadway (7), Manhattan | 56,490 | 64,800 | 11,454 | 45,036 | 47,953 |
| 723S | Grand Central-42 St (7), Hudson Yards | 56,265 | 68,217 | 27,414 | 28,851 | 26,455 |
| 418N | Fulton St (4,5), Uptown | 54,754 | 76,386 | 44,502 | 10,252 | 21,492 |
| D15S | 47-50 Sts-Rockefeller Ctr (B,D,F,M), Downtown | 54,526 | 74,586 | 30,991 | 23,535 | 1,179 |
| D20N | W 4 St-Wash Sq (B,D,F,M), Uptown | 54,465 | 69,003 | 30,413 | 24,052 | 30,438 |
| F11N | Lexington Av/53 St (E,F), Queens | 54,352 | 72,801 | 33,520 | 20,832 | 29,940 |
| 710N | 74 St-Broadway (7), Outbound | 54,312 | 62,753 | 40,421 | 13,891 | 45,073 |
| 418S | Fulton St (4,5), Downtown | 54,285 | 75,979 | 9,878 | 44,407 | 21,956 |
| 621N | 125 St (4,5,6), The Bronx | 54,241 | 78,442 | 31,399 | 22,842 | 35,004 |
| G08N | Forest Hills-71 Av (E,F,M,R), Outbound | 53,349 | 71,035 | 13,517 | 39,832 | 30,560 |
| 626S | 86 St (4,5,6), Downtown | 52,952 | 65,287 | 35,342 | 17,610 | 14,514 |
| D15N | 47-50 Sts-Rockefeller Ctr (B,D,F,M), Uptown | 52,468 | 71,953 | 21,561 | 30,907 | 24 |
| A31S | 14 St (A,C,E), Downtown | 52,389 | 62,723 | 15,189 | 37,200 | 24,193 |
| D21S | Broadway-Lafayette St (B,D,F,M), Downtown | 51,914 | 63,948 | 32,828 | 19,086 | 27,342 |
| 718S | Queensboro Plaza (7), Manhattan | 51,743 | 60,983 | 17,976 | 33,766 | 45,061 |
| 701S | Flushing-Main St (7), Manhattan | 50,494 | 59,545 | 50,494 | 0 | 0 |
| 120S | 96 St (1,2,3), Downtown | 50,265 | 67,247 | 29,389 | 20,876 | 20,585 |
| R11N | Lexington Av/59 St (N,R,W), Queens | 50,100 | 63,595 | 36,135 | 13,965 | 35,335 |
| G08S | Forest Hills-71 Av (E,F,M,R), Manhattan | 50,055 | 66,877 | 38,266 | 11,788 | 26,863 |
| A31N | 14 St (A,C,E), Uptown | 48,627 | 57,996 | 35,515 | 13,112 | 21,152 |
| A38N | Fulton St (A,C), Uptown | 48,405 | 67,892 | 17,506 | 30,899 | 26,962 |
| 626N | 86 St (4,5,6), Uptown | 48,061 | 58,398 | 14,612 | 33,449 | 8,597 |
| 701N | Flushing-Main St (7), Last Stop | 47,978 | 56,607 | 0 | 47,978 | 0 |
| 235S | Atlantic Av (2,3,4,5), Outbound | 47,091 | 61,830 | 25,490 | 21,602 | 33,318 |
| A32N | W 4 St-Wash Sq (A,C,E), Uptown | 46,753 | 60,666 | 23,611 | 23,142 | 30,341 |
| A32S | W 4 St-Wash Sq (A,C,E), Downtown | 45,758 | 58,084 | 19,181 | 26,577 | 29,019 |
| A38S | Fulton St (A,C), Brooklyn | 43,681 | 61,436 | 27,712 | 15,969 | 21,430 |
| L02N | 6 Av (L), West Side | 43,607 | 51,464 | 6,111 | 37,495 | 33,796 |
| 125N | 59 St-Columbus Circle (1), Uptown | 43,130 | 57,284 | 21,119 | 22,011 | 18,624 |
| 125S | 59 St-Columbus Circle (1), Downtown | 42,783 | 56,985 | 19,219 | 23,564 | 22,987 |
| A15S | 125 St (A,B,C,D), Downtown | 42,721 | 60,625 | 26,258 | 16,463 | 21,788 |
| R36N | 36 St (D,N,R), Manhattan | 42,273 | 49,765 | 24,870 | 17,403 | 28,658 |
| L02S | 6 Av (L), Brooklyn | 40,752 | 47,800 | 36,069 | 4,684 | 30,633 |
| A15N | 125 St (A,B,C,D), Uptown | 40,745 | 57,139 | 15,513 | 25,233 | 19,252 |
| D19N | 14 St (F,M), Uptown | 40,526 | 50,603 | 21,320 | 19,205 | 28,039 |
| D14N | 7 Av (B,D,E), Outbound | 40,476 | 51,913 | 28,382 | 12,094 | 23,431 |
| D14S | 7 Av (B,D,E), Downtown | 40,298 | 51,521 | 11,807 | 28,491 | 24,419 |
| 239N | Franklin Av-Medgar Evers College (2,3,4,5), Manhattan | 39,852 | 53,576 | 21,149 | 18,703 | 27,819 |
| A42S | Hoyt-Schermerhorn Sts (A,C,G), Queens | 38,469 | 47,911 | 14,253 | 24,215 | 27,307 |
| R09S | Queensboro Plaza (N,W), Manhattan | 37,423 | 44,478 | 25,703 | 11,720 | 32,296 |
| D19S | 14 St (F,M), Downtown | 37,300 | 46,495 | 15,292 | 22,008 | 24,268 |
| 718N | Queensboro Plaza (7), Outbound | 36,907 | 43,680 | 24,858 | 12,049 | 29,206 |
| 120N | 96 St (1,2,3), Uptown | 36,664 | 48,553 | 13,932 | 22,733 | 7,206 |
| 640N | Brooklyn Bridge-City Hall (4,5,6), Uptown | 36,218 | 51,016 | 27,002 | 9,216 | 14,819 |
| L01N | 8 Av (L), Last Stop | 36,100 | 41,468 | 0 | 36,100 | 21,605 |
| A42N | Hoyt-Schermerhorn Sts (A,C,G), Westbound | 35,462 | 44,144 | 22,575 | 12,887 | 25,187 |
| 724S | 5 Av (7), Hudson Yards | 35,336 | 44,501 | 10,970 | 24,366 | 19,919 |
| 637N | Bleecker St (6), Uptown | 35,135 | 44,056 | 29,297 | 5,838 | 21,730 |
| R09N | Queensboro Plaza (N,W), Astoria | 34,916 | 41,325 | 11,652 | 23,264 | 29,965 |
| 901N | Grand Central-42 St (S), Times Square | 34,400 | 46,262 | 34,400 | 0 | 14,434 |
| 902N | Times Sq-42 St (S), Last Stop | 34,400 | 46,262 | 0 | 34,400 | 22,995 |
| 724N | 5 Av (7), Queens | 34,259 | 42,984 | 23,676 | 10,583 | 18,681 |
| 637S | Bleecker St (6), Downtown | 34,234 | 42,455 | 5,554 | 28,680 | 21,049 |
| F06S | Kew Gardens-Union Tpke (E,F), Manhattan | 34,050 | 46,850 | 23,715 | 10,335 | 14,781 |
| R14N | 57 St-7 Av (N,Q,R,W), Uptown | 33,936 | 43,805 | 15,768 | 18,167 | 2,136 |
| G06S | Sutphin Blvd-Archer Av-JFK Airport (E,J,Z), Manhattan | 33,845 | 36,424 | 33,762 | 83 | 7,517 |
| R30S | DeKalb Av (B,Q,R), Southbound | 33,612 | 42,826 | 15,168 | 18,445 | 13,665 |
| L01S | 8 Av (L), Brooklyn | 33,401 | 38,196 | 33,401 | 0 | 20,341 |
| R14S | 57 St-7 Av (N,Q,R,W), Downtown | 33,383 | 42,918 | 16,825 | 16,558 | 4,037 |
| 239S | Franklin Av-Medgar Evers College (2,3,4,5), Outbound | 33,241 | 44,832 | 15,196 | 18,046 | 21,407 |
| 137N | Chambers St (1,2,3), Uptown | 32,791 | 43,865 | 17,814 | 14,978 | 16,418 |
| R36S | 36 St (D,N,R), Southbound | 31,706 | 36,865 | 12,016 | 19,690 | 18,166 |
| L08N | Bedford Av (L), Manhattan | 31,303 | 28,259 | 23,441 | 7,862 | 0 |
| Q01N | Canal St (N,Q), Uptown | 31,170 | 40,392 | 17,966 | 13,203 | 10,216 |
| A51N | Broadway Junction (A,C), Manhattan | 30,708 | 42,330 | 20,983 | 9,726 | 27,075 |
| L08S | Bedford Av (L), Outbound | 30,547 | 27,701 | 6,706 | 23,841 | 0 |
| G22S | Court Sq (G), Brooklyn | 30,296 | 34,957 | 30,296 | 0 | 27,118 |
| A51S | Broadway Junction (A,C), Outbound | 30,159 | 41,255 | 8,849 | 21,311 | 26,576 |
| Q01S | Canal St (N,Q), Downtown | 30,152 | 39,316 | 11,216 | 18,936 | 9,053 |
| R30N | DeKalb Av (B,Q,R), Manhattan | 29,989 | 37,920 | 16,504 | 13,484 | 10,472 |
| 640S | Brooklyn Bridge-City Hall (4,5,6), Downtown | 29,919 | 42,397 | 6,473 | 23,446 | 10,297 |
| D24N | Atlantic Av (B,Q), Manhattan | 29,844 | 39,704 | 10,711 | 19,133 | 22,602 |
| R41N | 59 St (N,R), Manhattan | 29,804 | 34,756 | 17,142 | 12,662 | 18,486 |
| G05S | Jamaica Center-Parsons/Archer (E,J,Z), Manhattan | 29,367 | 41,831 | 29,367 | 0 | 4,497 |
| G22N | Court Sq (G), Last Stop | 29,272 | 33,796 | 0 | 29,272 | 25,872 |
| L10N | Lorimer St (L), Manhattan | 29,208 | 32,003 | 18,763 | 10,444 | 18,991 |
| G06N | Sutphin Blvd-Archer Av-JFK Airport (E,J,Z), Jamaica | 29,127 | 32,189 | 720 | 28,406 | 8,778 |
| 250N | Crown Hts-Utica Av (3,4), Manhattan | 29,078 | 40,864 | 22,764 | 6,314 | 10,088 |
| L10S | Lorimer St (L), Outbound | 28,934 | 31,725 | 10,773 | 18,161 | 18,140 |
| F09S | Court Sq-23 St (E,F), Manhattan | 28,905 | 34,785 | 16,596 | 12,309 | 16,626 |
| 901S | Grand Central-42 St (S), Last Stop | 28,751 | 38,586 | 0 | 28,751 | 13,558 |
| 902S | Times Sq-42 St (S), Grand Central | 28,751 | 38,586 | 28,751 | 0 | 17,203 |
| F09N | Court Sq-23 St (E,F), Outbound | 28,733 | 34,820 | 10,431 | 18,302 | 16,444 |
| R29N | Jay St-MetroTech (R), Manhattan | 27,553 | 35,998 | 7,583 | 19,970 | 20,843 |
| D24S | Atlantic Av (B,Q), Southbound | 27,380 | 36,064 | 14,873 | 12,507 | 17,703 |
| G05N | Jamaica Center-Parsons/Archer (E,J,Z), Last Stop | 27,129 | 38,608 | 0 | 27,129 | 4,497 |
| Q03S | 72 St (Q), Downtown | 27,035 | 33,590 | 26,166 | 869 | 189 |
| Q03N | 72 St (Q), Uptown | 27,008 | 33,566 | 753 | 26,255 | 189 |
| 222N | 149 St-Hostos (2,5), Northbound | 26,948 | 40,279 | 15,166 | 11,783 | 22,471 |
| A09S | 168 St (A,C), Downtown | 26,554 | 33,659 | 22,987 | 3,566 | 13,329 |
| 137S | Chambers St (1,2,3), Downtown | 26,393 | 35,746 | 11,232 | 15,162 | 9,974 |
| 707S | Junction Blvd (7), Manhattan | 25,547 | 26,065 | 21,297 | 4,250 | 3,213 |
| R15S | 49 St (N,R,W), Downtown | 25,530 | 27,495 | 17,262 | 8,268 | 0 |
| 726S | 34 St-Hudson Yards (7), Queens | 25,502 | 21,612 | 0 | 25,502 | 0 |
| R15N | 49 St (N,R,W), Uptown | 25,085 | 27,001 | 7,836 | 17,249 | 0 |
| R29S | Jay St-MetroTech (R), Southbound | 25,026 | 32,822 | 17,939 | 7,087 | 18,850 |
| 726N | 34 St-Hudson Yards (7), Last Stop | 25,021 | 21,194 | 25,021 | 0 | 0 |
| 229N | Fulton St (2,3), Uptown | 25,015 | 35,371 | 16,340 | 8,675 | 10,834 |
| D18N | 23 St (F,M), Uptown | 24,904 | 33,239 | 14,190 | 10,714 | 0 |
| L06S | 1 Av (L), Brooklyn | 24,901 | 20,858 | 8,437 | 16,464 | 0 |
| 414N | 161 St-Yankee Stadium (4), Northbound | 24,847 | 35,493 | 7,018 | 17,829 | 13,586 |
| L17N | Myrtle-Wyckoff Avs (L), Manhattan | 24,429 | 26,980 | 19,801 | 4,628 | 8,282 |
| 707N | Junction Blvd (7), Outbound | 24,238 | 24,360 | 3,856 | 20,383 | 2,053 |
| 627S | 77 St (6), Downtown | 24,191 | 28,256 | 19,522 | 4,669 | 16 |
| A09N | 168 St (A,C), Uptown | 24,176 | 30,515 | 3,524 | 20,652 | 10,886 |
| 719N | Court Sq (7), Outbound | 24,147 | 27,305 | 15,655 | 8,492 | 16,392 |
| L17S | Myrtle-Wyckoff Avs (L), Outbound | 23,896 | 26,494 | 4,848 | 19,048 | 8,451 |
| 634N | 23 St-Baruch College (6), Uptown | 23,848 | 34,012 | 13,180 | 10,667 | 0 |
| 627N | 77 St (6), Uptown | 23,743 | 27,701 | 4,320 | 19,423 | 16 |
| D35N | Kings Hwy (B,Q), Manhattan | 23,683 | 30,796 | 16,683 | 7,001 | 7,342 |
| A36S | Chambers St (A,C), Brooklyn | 23,662 | 35,288 | 10,646 | 13,016 | 5,533 |
| 234S | Nevins St (2,3,4,5), Outbound | 23,489 | 31,607 | 10,658 | 12,832 | 15,687 |
| D18S | 23 St (F,M), Downtown | 23,439 | 31,142 | 9,727 | 13,712 | 0 |
| 222S | 149 St-Hostos (2,5), Manhattan | 23,429 | 35,058 | 9,529 | 13,900 | 18,928 |
| 126N | 50 St (1), Uptown | 23,381 | 30,904 | 9,900 | 13,482 | 0 |
| 632S | 33 St (6), Downtown | 23,258 | 32,644 | 9,386 | 13,872 | 1 |
| G29S | Metropolitan Av (G), Southbound | 23,186 | 25,673 | 11,263 | 11,923 | 18,636 |
| 719S | Court Sq (7), Manhattan | 23,105 | 25,919 | 8,689 | 14,416 | 15,529 |
| G29N | Metropolitan Av (G), Queens | 23,038 | 25,501 | 11,069 | 11,970 | 18,496 |
| M18S | Delancey St-Essex St (J,M,Z), Inbound | 22,959 | 27,858 | 10,417 | 12,541 | 8,973 |
| 634S | 23 St-Baruch College (6), Downtown | 22,907 | 32,703 | 9,947 | 12,960 | 0 |
| L22N | Broadway Junction (L), Manhattan | 22,869 | 30,121 | 13,799 | 9,070 | 20,882 |
| 632N | 33 St (6), Uptown | 22,863 | 32,146 | 13,731 | 9,132 | 1 |
| A25N | 50 St (C,E), Uptown | 22,832 | 26,916 | 10,855 | 11,976 | 2,445 |
| 228S | Park Pl (2,3), Brooklyn | 22,794 | 33,337 | 5,989 | 16,805 | 6,788 |
| L06N | 1 Av (L), West Side | 22,781 | 19,153 | 15,067 | 7,714 | 0 |
| 229S | Fulton St (2,3), Brooklyn | 22,759 | 32,701 | 8,064 | 14,694 | 7,289 |
| F15S | Delancey St-Essex St (F), Brooklyn | 22,499 | 26,841 | 7,200 | 15,299 | 8,564 |
| A25S | 50 St (C,E), Downtown | 22,399 | 26,445 | 11,664 | 10,735 | 2,814 |
| 628S | 68 St-Hunter College (6), Downtown | 22,363 | 27,336 | 16,633 | 5,730 | 84 |
| J27S | Broadway Junction (J,Z), Manhattan | 22,247 | 30,198 | 7,308 | 14,939 | 21,055 |
| G21S | Queens Plaza (E,F,R), Manhattan | 22,212 | 24,972 | 13,793 | 8,419 | 7,051 |
| 414S | 161 St-Yankee Stadium (4), Manhattan | 22,140 | 31,367 | 15,341 | 6,798 | 11,562 |
| 250S | Crown Hts-Utica Av (3,4), Outbound | 22,108 | 30,990 | 3,586 | 18,522 | 5,029 |
| A36N | Chambers St (A,C), Uptown | 22,036 | 33,074 | 11,392 | 10,644 | 2,966 |
| M18N | Delancey St-Essex St (J,M,Z), Brooklyn | 22,020 | 27,452 | 13,435 | 8,584 | 11,017 |
| 628N | 68 St-Hunter College (6), Uptown | 21,878 | 26,676 | 4,937 | 16,941 | 84 |
| M11N | Myrtle Av (J,M,Z), Outbound | 21,852 | 28,823 | 12,321 | 9,531 | 11,512 |
| 415S | 149 St-Hostos (4), Manhattan | 21,749 | 32,379 | 10,877 | 10,872 | 16,816 |
| Q04S | 86 St (Q), Downtown | 21,535 | 28,184 | 21,535 | 0 | 52 |
| D22S | Grand St (B,D), Brooklyn | 21,387 | 28,030 | 7,414 | 13,974 | 0 |
| M11S | Myrtle Av (J,M,Z), Manhattan | 21,336 | 28,170 | 9,460 | 11,876 | 11,803 |
| A34N | Canal St (A,C,E), Uptown | 21,254 | 31,111 | 13,307 | 7,947 | 5,791 |
| 126S | 50 St (1), Downtown | 21,162 | 28,209 | 12,197 | 8,966 | 0 |
| D11N | 161 St-Yankee Stadium (B,D), Northbound | 21,148 | 31,003 | 7,947 | 13,201 | 13,427 |
| F15N | Delancey St-Essex St (F), Uptown | 21,137 | 24,799 | 12,580 | 8,558 | 7,108 |
| Q04N | 86 St (Q), Uptown | 21,095 | 27,619 | 0 | 21,095 | 52 |
| F06N | Kew Gardens-Union Tpke (E,F), Jamaica | 21,065 | 29,941 | 3,878 | 17,188 | 2,600 |
| L22S | Broadway Junction (L), Outbound | 21,028 | 27,750 | 8,684 | 12,344 | 19,071 |
| D35S | Kings Hwy (B,Q), Southbound | 20,827 | 26,975 | 5,736 | 15,091 | 4,759 |
| D13S | 145 St (B,D), Downtown | 20,791 | 30,278 | 9,835 | 10,956 | 12,073 |
| 415N | 149 St-Hostos (4), Northbound | 20,752 | 30,984 | 10,908 | 9,844 | 16,012 |
| D22N | Grand St (B,D), Uptown | 20,654 | 27,077 | 13,061 | 7,593 | 200 |
| A12S | 145 St (A,C), Downtown | 20,378 | 28,614 | 12,476 | 7,901 | 10,413 |
| J27N | Broadway Junction (J,Z), Outbound | 20,336 | 27,764 | 14,075 | 6,261 | 19,251 |
| D11S | 161 St-Yankee Stadium (B,D), Manhattan | 20,240 | 29,259 | 14,014 | 6,226 | 11,720 |
| R41S | 59 St (N,R), Southbound | 20,235 | 22,737 | 8,103 | 12,132 | 9,308 |
| 228N | Park Pl (2,3), Uptown | 19,798 | 29,171 | 14,877 | 4,921 | 4,028 |
| G21N | Queens Plaza (E,F,R), Outbound | 19,732 | 21,832 | 7,087 | 12,645 | 4,517 |
| 420N | Bowling Green (4,5), Uptown | 19,579 | 30,726 | 14,741 | 4,839 | 51 |
| D43N | Coney Island-Stillwell Av (D,F,N,Q), Manhattan | 19,577 | 23,510 | 19,577 | 0 | 8,149 |
| 420S | Bowling Green (4,5), Downtown | 19,191 | 30,146 | 4,542 | 14,649 | 0 |
| 234N | Nevins St (2,3,4,5), Manhattan | 19,041 | 25,520 | 10,549 | 8,491 | 10,905 |
| F12N | 5 Av/53 St (E,F), Queens | 18,611 | 33,308 | 6,544 | 12,067 | 1,517 |
| D43S | Coney Island-Stillwell Av (D,F,N,Q), Last Stop | 18,554 | 22,345 | 0 | 18,554 | 8,149 |
| R33N | 4 Av-9 St (R), Manhattan | 18,519 | 22,448 | 8,938 | 9,581 | 13,126 |
| A30N | 23 St (C,E), Uptown | 18,503 | 26,094 | 10,403 | 8,100 | 0 |
| 124S | 66 St-Lincoln Center (1), Downtown | 18,456 | 26,170 | 12,438 | 6,018 | 0 |
| 221S | 3 Av-149 St (2,5), Manhattan | 18,343 | 27,424 | 13,907 | 4,436 | 2,924 |
| 639N | Canal St (6), Uptown | 18,295 | 24,411 | 15,339 | 2,955 | 8,155 |
| R19N | 23 St (R,W), Uptown | 18,254 | 28,037 | 10,301 | 7,953 | 0 |
| A30S | 23 St (C,E), Downtown | 18,045 | 25,439 | 7,643 | 10,403 | 0 |
| A34S | Canal St (A,C,E), Downtown | 17,976 | 26,574 | 5,817 | 12,158 | 2,123 |
| F23N | 4 Av-9 St (F,G), Northbound | 17,962 | 21,594 | 12,634 | 5,328 | 12,522 |
| 706S | 103 St-Corona Plaza (7), Manhattan | 17,955 | 19,768 | 16,368 | 1,587 | 0 |
| 124N | 66 St-Lincoln Center (1), Uptown | 17,848 | 25,355 | 5,414 | 12,433 | 0 |
| 712S | 61 St-Woodside (7), Manhattan | 17,280 | 21,714 | 11,751 | 5,529 | 2,358 |
| 712N | 61 St-Woodside (7), Outbound | 17,201 | 21,590 | 5,644 | 11,557 | 2,358 |
| F12S | 5 Av/53 St (E,F), Downtown | 17,201 | 31,436 | 10,945 | 6,255 | 58 |
| A48N | Utica Av (A,C), Manhattan | 17,010 | 23,666 | 12,802 | 4,209 | 4,756 |
| 633N | 28 St (6), Uptown | 16,971 | 20,979 | 10,001 | 6,969 | 2 |
| 633S | 28 St (6), Downtown | 16,800 | 20,754 | 6,915 | 9,885 | 2 |
| 112S | 168 St-Washington Hts (1), Downtown | 16,793 | 22,117 | 7,187 | 9,605 | 11,108 |
| 708S | 90 St-Elmhurst Av (7), Manhattan | 16,704 | 18,030 | 13,106 | 3,597 | 0 |
| G11S | Woodhaven Blvd (M,R), Manhattan | 16,462 | 22,769 | 12,897 | 3,565 | 0 |
| 230S | Wall St (2,3), Brooklyn | 16,346 | 26,843 | 3,300 | 13,046 | 0 |
| R19S | 23 St (R,W), Downtown | 16,317 | 25,014 | 6,526 | 9,791 | 0 |
| 221N | 3 Av-149 St (2,5), Northbound | 16,116 | 24,371 | 3,718 | 12,398 | 802 |
| A48S | Utica Av (A,C), Outbound | 15,961 | 22,289 | 3,898 | 12,063 | 4,121 |
| G12S | Grand Av-Newtown (M,R), Manhattan | 15,917 | 19,574 | 13,700 | 2,218 | 0 |
| 230N | Wall St (2,3), Uptown | 15,915 | 26,094 | 12,467 | 3,448 | 0 |
| 706N | 103 St-Corona Plaza (7), Outbound | 15,910 | 17,585 | 1,170 | 14,739 | 0 |
| 721S | Vernon Blvd-Jackson Av (7), Manhattan | 15,830 | 17,020 | 11,730 | 4,100 | 0 |
| G12N | Grand Av-Newtown (M,R), Outbound | 15,819 | 19,462 | 2,168 | 13,651 | 0 |
| 423N | Borough Hall (4,5), Manhattan | 15,815 | 23,946 | 8,639 | 7,175 | 1,596 |
| F14S | 2 Av (F), Downtown | 15,747 | 20,000 | 3,998 | 11,748 | 0 |
| F23S | 4 Av-9 St (F,G), Southbound | 15,698 | 18,909 | 4,722 | 10,976 | 9,911 |
| 138N | WTC Cortlandt (1), Uptown | 15,551 | 15,617 | 14,659 | 892 | 0 |
| A46S | Nostrand Av (A,C), Outbound | 15,551 | 19,847 | 3,522 | 12,029 | 986 |
| R21S | 8 St-NYU (R,W), Downtown | 15,545 | 19,943 | 3,108 | 12,437 | 0 |
| Q05S | 96 St (Q), Downtown | 15,503 | 20,963 | 15,503 | 0 | 0 |
| G11N | Woodhaven Blvd (M,R), Outbound | 15,439 | 21,327 | 2,983 | 12,456 | 0 |
| 138S | WTC Cortlandt (1), Downtown | 15,419 | 15,538 | 1,069 | 14,350 | 0 |
| 112N | 168 St-Washington Hts (1), Uptown | 15,267 | 19,918 | 7,391 | 7,876 | 9,632 |
| 721N | Vernon Blvd-Jackson Av (7), Outbound | 15,178 | 16,350 | 3,686 | 11,492 | 0 |
| 247N | Flatbush Av-Brooklyn College (2,5), Manhattan | 15,125 | 20,950 | 15,125 | 0 | 0 |
| F14N | 2 Av (F), Uptown | 15,116 | 19,227 | 10,978 | 4,137 | 0 |
| 625N | 96 St (6), The Bronx | 15,058 | 18,743 | 3,053 | 12,005 | 9 |
| A46N | Nostrand Av (A,C), Manhattan | 15,027 | 19,031 | 11,917 | 3,110 | 478 |
| D28S | Church Av (B,Q), Southbound | 15,014 | 23,776 | 3,348 | 11,666 | 3,471 |
| 121S | 86 St (1), Downtown | 14,969 | 19,654 | 11,190 | 3,778 | 23 |
| Q05N | 96 St (Q), Last Stop | 14,969 | 20,249 | 0 | 14,969 | 0 |
| 121N | 86 St (1), Uptown | 14,950 | 19,579 | 3,685 | 11,265 | 23 |
| A12N | 145 St (A,C), Uptown | 14,942 | 20,619 | 5,817 | 9,125 | 5,185 |
| 708N | 90 St-Elmhurst Av (7), Outbound | 14,904 | 16,062 | 2,671 | 12,234 | 0 |
| 625S | 96 St (6), Downtown | 14,883 | 18,511 | 11,900 | 2,983 | 9 |
| R21N | 8 St-NYU (R,W), Uptown | 14,849 | 19,116 | 11,701 | 3,148 | 0 |
| M20S | Canal St (J,Z), Downtown | 14,844 | 20,028 | 3,467 | 11,376 | 9,691 |
| F01S | Jamaica-179 St (F), Manhattan | 14,819 | 22,258 | 14,819 | 0 | 0 |
| D39N | Sheepshead Bay (B,Q), Manhattan | 14,702 | 20,010 | 11,137 | 3,566 | 4,412 |
| A33S | Spring St (C,E), Downtown | 14,620 | 17,338 | 3,901 | 10,719 | 0 |
| R13S | 5 Av/59 St (N,R,W), Downtown | 14,569 | 19,213 | 7,236 | 7,333 | 131 |
| R33S | 4 Av-9 St (R), Southbound | 14,349 | 17,384 | 6,815 | 7,534 | 9,162 |
| 247S | Flatbush Av-Brooklyn College (2,5), Last Stop | 14,342 | 19,876 | 0 | 14,342 | 0 |
| 419N | Wall St (4,5), Uptown | 14,341 | 21,727 | 12,283 | 2,058 | 0 |
| A33N | Spring St (C,E), Uptown | 14,219 | 16,861 | 10,039 | 4,180 | 0 |
| 423S | Borough Hall (4,5), Outbound | 14,214 | 21,467 | 6,104 | 8,110 | 1,839 |
| 636N | Astor Pl (6), Uptown | 14,109 | 19,204 | 10,679 | 3,430 | 0 |
| 419S | Wall St (4,5), Downtown | 14,030 | 21,270 | 1,778 | 12,252 | 0 |
| F01N | Jamaica-179 St (F), Last Stop | 13,956 | 20,973 | 0 | 13,956 | 0 |
| B10N | 57 St (M), Uptown | 13,915 | 16,775 | 4,976 | 8,939 | 170 |
| D26S | Prospect Park (B,Q,S), Southbound | 13,780 | 18,595 | 3,408 | 10,373 | 5,295 |
| 639S | Canal St (6), Downtown | 13,758 | 18,400 | 2,150 | 11,608 | 4,833 |
| B10S | 57 St (M), Downtown | 13,606 | 16,372 | 8,357 | 5,249 | 170 |
| R27N | Whitehall St-South Ferry (R,W), Uptown | 13,490 | 20,668 | 7,862 | 5,629 | 0 |
| R27S | Whitehall St-South Ferry (R,W), Downtown | 13,427 | 20,488 | 5,680 | 7,747 | 51 |
| 636S | Astor Pl (6), Downtown | 13,415 | 18,174 | 2,817 | 10,599 | 0 |
| R13N | 5 Av/59 St (N,R,W), Queens | 13,392 | 17,672 | 6,380 | 7,012 | 131 |
| F18N | York St (F), Manhattan | 13,382 | 14,802 | 9,455 | 3,927 | 0 |
| 709N | 82 St-Jackson Hts (7), Outbound | 13,366 | 17,156 | 3,469 | 9,897 | 50 |
| 117S | 116 St-Columbia University (1), Downtown | 13,344 | 17,034 | 11,037 | 2,307 | 0 |
| F20S | Bergen St (F,G), Southbound | 13,292 | 15,752 | 2,596 | 10,696 | 2,908 |
| 714S | 46 St-Bliss St (7), Manhattan | 13,232 | 15,103 | 9,077 | 4,155 | 486 |
| D26N | Prospect Park (B,Q,S), Northbound | 13,219 | 17,727 | 9,937 | 3,282 | 5,033 |
| D13N | 145 St (B,D), Uptown | 13,174 | 18,616 | 6,582 | 6,592 | 4,692 |
| 714N | 46 St-Bliss St (7), Outbound | 13,153 | 15,008 | 4,084 | 9,069 | 486 |
| 134N | Houston St (1), Uptown | 13,149 | 16,985 | 11,129 | 2,020 | 0 |
| F16S | East Broadway (F), Brooklyn | 13,135 | 15,634 | 3,944 | 9,192 | 0 |
| 117N | 116 St-Columbia University (1), Uptown | 13,072 | 16,680 | 2,117 | 10,954 | 0 |
| 134S | Houston St (1), Downtown | 13,059 | 16,950 | 1,600 | 11,458 | 0 |
| 213S | E 180 St (2,5), Manhattan | 13,054 | 17,821 | 8,613 | 4,441 | 6,640 |
| R25N | Cortlandt St (R,W), Uptown | 12,966 | 19,498 | 6,958 | 6,008 | 2,729 |
| D28N | Church Av (B,Q), Manhattan | 12,940 | 21,100 | 10,884 | 2,056 | 1,191 |
| 122S | 79 St (1), Downtown | 12,792 | 16,195 | 10,023 | 2,770 | 0 |
| 122N | 79 St (1), Uptown | 12,786 | 16,179 | 2,740 | 10,047 | 0 |
| M16N | Marcy Av (J,M,Z), Outbound | 12,730 | 18,221 | 6,327 | 6,403 | 1,997 |
| 705S | 111 St (7), Manhattan | 12,700 | 13,072 | 10,531 | 2,169 | 0 |
| F16N | East Broadway (F), Uptown | 12,676 | 15,068 | 8,719 | 3,957 | 0 |
| M20N | Canal St (J,Z), Brooklyn | 12,674 | 17,204 | 10,482 | 2,191 | 8,064 |
| 709S | 82 St-Jackson Hts (7), Manhattan | 12,668 | 16,330 | 9,529 | 3,139 | 50 |
| R01S | Astoria-Ditmars Blvd (N,W), Manhattan | 12,572 | 19,206 | 12,572 | 0 | 0 |
| R25S | Cortlandt St (R,W), Downtown | 12,537 | 18,746 | 6,017 | 6,520 | 2,670 |
| 705N | 111 St (7), Outbound | 12,495 | 12,843 | 2,171 | 10,324 | 0 |
| F18S | York St (F), Southbound | 12,419 | 13,668 | 3,231 | 9,188 | 0 |
| 608S | Parkchester (6), Manhattan | 12,397 | 19,884 | 11,281 | 1,116 | 1,830 |
| R01N | Astoria-Ditmars Blvd (N,W), Last Stop | 12,349 | 18,875 | 0 | 12,349 | 0 |
| M16S | Marcy Av (J,M,Z), Manhattan | 12,292 | 17,592 | 6,242 | 6,050 | 1,793 |
| R22N | Prince St (R,W), Uptown | 12,271 | 15,964 | 8,264 | 4,007 | 17 |
| 608N | Parkchester (6), Northbound | 12,186 | 19,517 | 1,104 | 11,082 | 1,935 |
| F20N | Bergen St (F,G), Northbound | 12,181 | 14,387 | 10,187 | 1,995 | 1,875 |
| D31S | Newkirk Plaza (B,Q), Southbound | 12,157 | 16,311 | 3,139 | 9,018 | 4,195 |
| G10S | 63 Dr-Rego Park (M,R), Manhattan | 11,914 | 17,089 | 7,392 | 4,522 | 0 |
| 225N | 125 St (2,3), Uptown | 11,862 | 16,442 | 3,943 | 7,918 | 125 |
| 613N | Hunts Point Av (6), Northbound | 11,825 | 16,734 | 3,853 | 7,972 | 4,066 |
| F24S | 7 Av (F,G), Southbound | 11,759 | 14,452 | 1,704 | 10,055 | 1,337 |
| 129S | 28 St (1), Downtown | 11,738 | 16,819 | 3,486 | 8,252 | 0 |
| L29N | Canarsie-Rockaway Pkwy (L), Manhattan | 11,697 | 16,741 | 11,697 | 0 | 4 |
| R04S | 30 Av (N,W), Manhattan | 11,652 | 18,943 | 11,249 | 404 | 0 |
| R18S | 28 St (R,W), Downtown | 11,619 | 15,335 | 3,953 | 7,666 | 0 |
| 225S | 125 St (2,3), Downtown | 11,608 | 16,064 | 7,760 | 3,848 | 125 |
| F21N | Carroll St (F,G), Northbound | 11,608 | 13,651 | 9,909 | 1,699 | 770 |
| D31N | Newkirk Plaza (B,Q), Manhattan | 11,592 | 15,700 | 8,934 | 2,658 | 3,297 |
| R22S | Prince St (R,W), Downtown | 11,578 | 14,976 | 3,206 | 8,372 | 17 |
| R23N | Canal St (R,W), Uptown | 11,554 | 16,282 | 5,250 | 6,304 | 6,089 |
| A21S | 81 St-Museum of Natural History (B,C), Downtown | 11,538 | 14,464 | 9,875 | 1,663 | 0 |
| A21N | 81 St-Museum of Natural History (B,C), Uptown | 11,537 | 14,429 | 1,601 | 9,936 | 0 |
| 129N | 28 St (1), Uptown | 11,497 | 16,380 | 7,926 | 3,571 | 0 |
| 130N | 23 St (1), Uptown | 11,461 | 16,295 | 7,428 | 4,033 | 0 |
| M08N | Myrtle-Wyckoff Avs (M), Inbound | 11,398 | 13,489 | 5,619 | 5,778 | 8,881 |
| R04N | 30 Av (N,W), Astoria | 11,391 | 18,525 | 437 | 10,954 | 0 |
| F21S | Carroll St (F,G), Southbound | 11,342 | 13,333 | 1,664 | 9,679 | 770 |
| G13S | Elmhurst Av (M,R), Manhattan | 11,240 | 12,987 | 9,506 | 1,734 | 0 |
| 638N | Spring St (6), Uptown | 11,236 | 13,216 | 9,175 | 2,061 | 0 |
| G13N | Elmhurst Av (M,R), Outbound | 11,213 | 12,965 | 1,794 | 9,419 | 0 |
| E01N | World Trade Center (E), Uptown | 11,144 | 16,341 | 11,144 | 0 | 2,743 |
| L16N | DeKalb Av (L), Manhattan | 11,119 | 12,103 | 8,985 | 2,133 | 0 |
| R18N | 28 St (R,W), Uptown | 11,090 | 14,657 | 7,073 | 4,017 | 0 |
| 130S | 23 St (1), Downtown | 11,087 | 15,885 | 3,579 | 7,508 | 0 |
| G10N | 63 Dr-Rego Park (M,R), Outbound | 10,994 | 15,762 | 4,150 | 6,845 | 0 |
| 622S | 116 St (6), Downtown | 10,929 | 15,151 | 7,267 | 3,662 | 63 |
| D39S | Sheepshead Bay (B,Q), Southbound | 10,853 | 15,247 | 1,872 | 8,982 | 955 |
| 638S | Spring St (6), Downtown | 10,796 | 12,635 | 1,510 | 9,286 | 0 |
| 624S | 103 St (6), Downtown | 10,735 | 14,329 | 7,337 | 3,398 | 39 |
| M22S | Fulton St (J,Z), Downtown | 10,734 | 14,988 | 1,126 | 9,608 | 5,290 |
| 133S | Christopher St-Stonewall (1), Downtown | 10,663 | 11,549 | 1,236 | 9,428 | 0 |
| F24N | 7 Av (F,G), Northbound | 10,642 | 13,070 | 9,372 | 1,270 | 246 |
| 613S | Hunts Point Av (6), Manhattan | 10,615 | 14,851 | 7,624 | 2,991 | 2,872 |
| 142N | South Ferry (1), Uptown | 10,614 | 16,042 | 10,614 | 0 | 0 |
| 622N | 116 St (6), The Bronx | 10,605 | 14,724 | 3,682 | 6,923 | 63 |
| G19N | Steinway St (M,R), Outbound | 10,525 | 16,152 | 3,496 | 7,029 | 37 |
| L29S | Canarsie-Rockaway Pkwy (L), Last Stop | 10,515 | 15,056 | 0 | 10,515 | 4 |
| M08S | Myrtle-Wyckoff Avs (M), Middle Village | 10,509 | 12,260 | 5,053 | 5,456 | 7,853 |
| L16S | DeKalb Av (L), Outbound | 10,483 | 11,428 | 1,853 | 8,629 | 0 |
| 133N | Christopher St-Stonewall (1), Uptown | 10,467 | 11,301 | 9,072 | 1,395 | 0 |
| R05S | Broadway (N,W), Manhattan | 10,366 | 10,907 | 9,878 | 488 | 0 |
| R05N | Broadway (N,W), Astoria | 10,338 | 10,896 | 515 | 9,822 | 0 |
| B04S | 21 St-Queensbridge (M), Manhattan | 10,327 | 12,701 | 7,107 | 3,220 | 27 |
| 118S | Cathedral Pkwy (110 St) (1), Downtown | 10,314 | 12,547 | 8,533 | 1,781 | 0 |
| 118N | Cathedral Pkwy (110 St) (1), Uptown | 10,285 | 12,514 | 1,825 | 8,460 | 0 |
| 624N | 103 St (6), The Bronx | 10,249 | 13,678 | 3,303 | 6,946 | 39 |
| F27N | Church Av (F,G), Northbound | 10,229 | 13,194 | 8,102 | 2,126 | 2,641 |
| R44N | 86 St (R), Manhattan | 10,151 | 12,356 | 10,146 | 4 | 0 |
| 142S | South Ferry (1), Last Stop | 10,146 | 15,371 | 0 | 10,146 | 0 |
| 119S | 103 St (1), Downtown | 10,080 | 12,742 | 8,450 | 1,630 | 0 |
| 119N | 103 St (1), Uptown | 10,015 | 12,650 | 1,643 | 8,372 | 0 |
| B04N | 21 St-Queensbridge (M), Outbound | 10,010 | 12,391 | 3,139 | 6,871 | 27 |
| G19S | Steinway St (M,R), Manhattan | 9,984 | 15,326 | 6,691 | 3,293 | 37 |
| A55N | Euclid Av (A,C), Manhattan | 9,959 | 14,261 | 8,708 | 1,251 | 2,294 |
| A40N | High St (A,C), Manhattan | 9,925 | 12,665 | 7,211 | 2,714 | 0 |
| A20N | 86 St (B,C), Uptown | 9,911 | 11,618 | 2,116 | 7,795 | 0 |
| 213N | E 180 St (2,5), Northbound | 9,826 | 12,728 | 2,926 | 6,900 | 3,503 |
| 115N | 137 St-City College (1), Uptown | 9,794 | 13,607 | 1,912 | 7,882 | 0 |
| 115S | 137 St-City College (1), Downtown | 9,793 | 13,611 | 7,900 | 1,893 | 0 |
| N02N | 8 Av (N), Manhattan | 9,765 | 12,090 | 6,598 | 3,167 | 0 |
| 224S | 135 St (2,3), Downtown | 9,669 | 15,235 | 6,831 | 2,838 | 519 |
| A20S | 86 St (B,C), Downtown | 9,655 | 11,342 | 7,668 | 1,987 | 0 |
| E01S | World Trade Center (E), Last Stop | 9,644 | 14,052 | 0 | 9,644 | 2,252 |
| N02S | 8 Av (N), Coney Island | 9,632 | 11,984 | 3,228 | 6,404 | 0 |
| G26S | Greenpoint Av (G), Southbound | 9,622 | 10,778 | 4,714 | 4,907 | 0 |
| A40S | High St (A,C), Outbound | 9,541 | 12,230 | 2,386 | 7,155 | 0 |
| R44S | 86 St (R), Bay Ridge | 9,531 | 11,608 | 4 | 9,527 | 0 |
| G26N | Greenpoint Av (G), Queens | 9,530 | 10,631 | 4,808 | 4,722 | 0 |
| 224N | 135 St (2,3), Uptown | 9,438 | 14,884 | 2,727 | 6,711 | 308 |
| M22N | Fulton St (J,Z), Brooklyn | 9,369 | 13,038 | 8,409 | 960 | 4,535 |
| 715S | 40 St-Lowery St (7), Manhattan | 9,294 | 11,410 | 6,125 | 3,169 | 340 |
| D40N | Brighton Beach (B,Q), Manhattan | 9,281 | 12,940 | 7,838 | 1,443 | 190 |
| A55S | Euclid Av (A,C), Queens | 9,277 | 13,325 | 1,085 | 8,192 | 2,001 |
| A22N | 72 St (B,C), Uptown | 9,267 | 9,656 | 1,240 | 8,027 | 0 |
| 715N | 40 St-Lowery St (7), Outbound | 9,259 | 11,373 | 3,110 | 6,150 | 340 |
| 702N | Mets-Willets Point (7), Outbound | 9,131 | 7,025 | 689 | 8,442 | 89 |
| A22S | 72 St (B,C), Downtown | 9,117 | 9,521 | 7,884 | 1,233 | 0 |
| R03S | Astoria Blvd (N,W), Manhattan | 8,989 | 2,546 | 8,836 | 152 | 0 |
| 716S | 33 St-Rawson St (7), Manhattan | 8,920 | 11,442 | 4,198 | 4,722 | 3 |
| 716N | 33 St-Rawson St (7), Outbound | 8,911 | 11,441 | 4,511 | 4,400 | 3 |
| G28N | Nassau Av (G), Queens | 8,867 | 10,558 | 4,185 | 4,682 | 0 |
| G28S | Nassau Av (G), Southbound | 8,861 | 10,634 | 4,580 | 4,281 | 0 |
| D40S | Brighton Beach (B,Q), Southbound | 8,766 | 12,259 | 1,397 | 7,369 | 0 |
| R03N | Astoria Blvd (N,W), Astoria | 8,758 | 2,483 | 162 | 8,596 | 0 |
| A07S | 175 St (A), Downtown | 8,655 | 14,428 | 8,281 | 374 | 0 |
| 232S | Borough Hall (2,3), Outbound | 8,639 | 12,930 | 3,464 | 5,174 | 1,698 |
| A19N | 96 St (B,C), Uptown | 8,583 | 11,087 | 2,276 | 6,306 | 0 |
| 623S | 110 St (6), Downtown | 8,534 | 11,083 | 6,398 | 2,136 | 42 |
| L11S | Graham Av (L), Outbound | 8,443 | 10,085 | 1,225 | 7,218 | 0 |
| R40N | 53 St (R), Manhattan | 8,428 | 10,397 | 6,325 | 2,104 | 104 |
| D25S | 7 Av (B,Q), Southbound | 8,414 | 11,206 | 1,802 | 6,612 | 0 |
| R23S | Canal St (R,W), Downtown | 8,377 | 11,561 | 3,718 | 4,659 | 3,150 |
| L11N | Graham Av (L), Manhattan | 8,351 | 9,974 | 7,181 | 1,170 | 0 |
| 702S | Mets-Willets Point (7), Manhattan | 8,268 | 6,347 | 7,434 | 835 | 62 |
| L15S | Jefferson St (L), Outbound | 8,263 | 7,815 | 1,509 | 6,754 | 0 |
| A19S | 96 St (B,C), Downtown | 8,239 | 10,656 | 6,110 | 2,128 | 0 |
| L15N | Jefferson St (L), Manhattan | 8,204 | 7,738 | 6,586 | 1,617 | 0 |
| D25N | 7 Av (B,Q), Manhattan | 8,176 | 10,873 | 6,452 | 1,724 | 0 |
| A07N | 175 St (A), Uptown | 8,119 | 13,524 | 334 | 7,785 | 0 |
| 113S | 157 St (1), Downtown | 8,108 | 12,717 | 5,863 | 2,245 | 0 |
| 113N | 157 St (1), Uptown | 8,097 | 12,693 | 2,275 | 5,822 | 0 |
| 623N | 110 St (6), The Bronx | 8,063 | 10,470 | 2,040 | 6,023 | 42 |
| A06S | 181 St (A), Downtown | 8,050 | 11,461 | 7,682 | 369 | 0 |
| 111N | 181 St (1), The Bronx | 8,018 | 11,527 | 1,847 | 6,170 | 0 |
| 111S | 181 St (1), Downtown | 7,996 | 11,467 | 6,401 | 1,595 | 0 |
| B06S | Roosevelt Island (M), Downtown | 7,953 | 8,597 | 6,848 | 1,105 | 237 |
| B06N | Roosevelt Island (M), Queens | 7,841 | 8,504 | 1,049 | 6,792 | 237 |
| 232N | Borough Hall (2,3), Manhattan | 7,820 | 11,752 | 5,083 | 2,736 | 1,252 |
| A06N | 181 St (A), Uptown | 7,791 | 11,082 | 319 | 7,473 | 0 |
| 226S | 116 St (2,3), Downtown | 7,718 | 11,342 | 5,739 | 1,978 | 0 |
| 226N | 116 St (2,3), Uptown | 7,672 | 11,300 | 1,999 | 5,673 | 0 |
| 244N | Church Av (2,5), Manhattan | 7,644 | 10,084 | 7,273 | 370 | 0 |
| 116S | 125 St (1), Downtown | 7,618 | 8,452 | 6,069 | 1,549 | 0 |
| 116N | 125 St (1), Uptown | 7,591 | 8,409 | 1,501 | 6,090 | 0 |
| R28N | Court St (R), Manhattan | 7,455 | 10,816 | 2,204 | 5,252 | 2,996 |
| G33N | Bedford-Nostrand Avs (G), Queens | 7,451 | 9,443 | 4,427 | 3,024 | 0 |
| F27S | Church Av (F,G), Southbound | 7,448 | 9,816 | 780 | 6,669 | 77 |
| M12N | Flushing Av (J,M), Outbound | 7,440 | 9,482 | 3,938 | 3,502 | 87 |
| 407S | Fordham Rd (4), Manhattan | 7,405 | 10,572 | 6,915 | 490 | 0 |
| R28S | Court St (R), Southbound | 7,343 | 10,701 | 4,702 | 2,641 | 3,244 |
| R39N | 45 St (R), Manhattan | 7,321 | 8,788 | 6,179 | 1,142 | 7 |
| M12S | Flushing Av (J,M), Manhattan | 7,317 | 9,315 | 3,540 | 3,776 | 97 |
| 244S | Church Av (2,5), Flatbush | 7,282 | 9,611 | 405 | 6,877 | 0 |
| L19N | Halsey St (L), Manhattan | 7,262 | 7,916 | 5,781 | 1,481 | 0 |
| D07S | Tremont Av (B,D), Manhattan | 7,245 | 11,781 | 6,596 | 648 | 1,057 |
| R32N | Union St (R), Manhattan | 7,199 | 8,237 | 5,634 | 1,565 | 0 |
| D05S | Fordham Rd (B,D), Manhattan | 7,165 | 13,113 | 6,993 | 172 | 352 |
| 114N | 145 St (1), Uptown | 7,137 | 9,762 | 1,653 | 5,484 | 0 |
| 407N | Fordham Rd (4), Northbound | 7,134 | 10,210 | 563 | 6,571 | 0 |
| 104S | 231 St (1), Manhattan | 7,089 | 10,333 | 6,969 | 119 | 0 |
| M21S | Chambers St (J,Z), Downtown | 7,073 | 9,960 | 1,289 | 5,784 | 4,048 |
| L26S | Livonia Av (L), Canarsie | 7,052 | 9,372 | 1,409 | 5,643 | 4,854 |
| 114S | 145 St (1), Downtown | 7,043 | 9,649 | 5,440 | 1,603 | 0 |
| 104N | 231 St (1), Van Cortlandt | 7,009 | 10,221 | 116 | 6,893 | 0 |
| R40S | 53 St (R), Southbound | 7,003 | 8,625 | 1,546 | 5,456 | 104 |
| 409S | Burnside Av (4), Manhattan | 7,002 | 10,596 | 6,247 | 755 | 45 |
| 413S | 167 St (4), Manhattan | 6,985 | 9,115 | 5,988 | 997 | 0 |
| D05N | Fordham Rd (B,D), Northbound | 6,966 | 12,765 | 192 | 6,774 | 361 |
| A45N | Franklin Av (C), Manhattan | 6,960 | 9,670 | 3,501 | 3,460 | 3,469 |
| 409N | Burnside Av (4), Northbound | 6,959 | 10,504 | 1,033 | 5,925 | 547 |
| L19S | Halsey St (L), Outbound | 6,957 | 7,582 | 1,411 | 5,546 | 0 |
| R32S | Union St (R), Southbound | 6,953 | 7,970 | 1,477 | 5,476 | 0 |
| G33S | Bedford-Nostrand Avs (G), Southbound | 6,927 | 8,815 | 2,894 | 4,033 | 0 |
| A02S | Inwood-207 St (A), Downtown | 6,926 | 10,213 | 6,926 | 0 | 0 |
| L05S | 3 Av (L), Brooklyn | 6,918 | 7,214 | 3,507 | 3,411 | 0 |
| G18S | 46 St (M,R), Manhattan | 6,903 | 9,483 | 5,250 | 1,653 | 5 |
| 406S | Kingsbridge Rd (4), Manhattan | 6,884 | 9,583 | 6,484 | 400 | 0 |
| L14N | Morgan Av (L), Manhattan | 6,871 | 7,642 | 5,723 | 1,147 | 0 |
| G18N | 46 St (M,R), Outbound | 6,867 | 9,445 | 1,627 | 5,240 | 5 |
| L14S | Morgan Av (L), Outbound | 6,864 | 7,643 | 1,012 | 5,852 | 0 |
| D07N | Tremont Av (B,D), Northbound | 6,861 | 11,255 | 644 | 6,217 | 1,043 |
| G09S | 67 Av (M,R), Manhattan | 6,805 | 9,600 | 3,326 | 3,479 | 0 |
| A44N | Clinton-Washington Avs (C), Manhattan | 6,743 | 7,908 | 5,375 | 1,368 | 0 |
| 619S | 3 Av-138 St (6), Manhattan | 6,733 | 9,125 | 5,343 | 1,390 | 239 |
| 131N | 18 St (1), Uptown | 6,728 | 9,931 | 4,119 | 2,609 | 0 |
| G36N | Fulton St (G), Queens | 6,709 | 7,003 | 3,423 | 3,286 | 0 |
| 413N | 167 St (4), Northbound | 6,684 | 8,735 | 1,024 | 5,660 | 0 |
| R39S | 45 St (R), Southbound | 6,629 | 7,965 | 997 | 5,631 | 7 |
| A17S | Cathedral Pkwy (110 St) (B,C), Downtown | 6,623 | 8,136 | 4,829 | 1,794 | 1 |
| A45S | Franklin Av (C), Outbound | 6,612 | 9,160 | 3,183 | 3,430 | 3,343 |
| R42N | Bay Ridge Av (R), Manhattan | 6,608 | 8,243 | 6,138 | 470 | 0 |
| A02N | Inwood-207 St (A), Last Stop | 6,574 | 9,699 | 0 | 6,574 | 0 |
| 131S | 18 St (1), Downtown | 6,563 | 9,786 | 2,355 | 4,208 | 0 |
| G09N | 67 Av (M,R), Outbound | 6,549 | 9,245 | 3,500 | 3,049 | 0 |
| 243N | Winthrop St (2,5), Manhattan | 6,526 | 6,947 | 6,220 | 306 | 0 |
| F05S | Briarwood (E,F), Manhattan | 6,515 | 8,261 | 5,060 | 1,455 | 2,220 |
| 406N | Kingsbridge Rd (4), Northbound | 6,502 | 9,065 | 425 | 6,078 | 0 |
| 233S | Hoyt St (2,3), Outbound | 6,467 | 8,345 | 3,602 | 2,865 | 0 |
| L26N | Livonia Av (L), Manhattan | 6,418 | 8,542 | 5,077 | 1,340 | 3,700 |
| A44S | Clinton-Washington Avs (C), Outbound | 6,412 | 7,520 | 1,253 | 5,160 | 0 |
| 110S | 191 St (1), Downtown | 6,396 | 8,532 | 5,157 | 1,239 | 0 |
| 243S | Winthrop St (2,5), Flatbush | 6,389 | 6,804 | 329 | 6,060 | 0 |
| 619N | 3 Av-138 St (6), Northbound | 6,372 | 8,641 | 1,355 | 5,017 | 95 |
| 139N | Rector St (1), Uptown | 6,344 | 9,235 | 6,294 | 50 | 0 |
| 139S | Rector St (1), Downtown | 6,328 | 9,221 | 61 | 6,267 | 0 |
| R42S | Bay Ridge Av (R), Bay Ridge | 6,303 | 7,867 | 448 | 5,854 | 0 |
| F02S | 169 St (F), Manhattan | 6,292 | 8,390 | 6,203 | 89 | 0 |
| 254N | Junius St (3), Manhattan | 6,213 | 8,055 | 4,619 | 1,594 | 4,093 |
| D10S | 167 St (B,D), Manhattan | 6,194 | 9,474 | 5,480 | 714 | 0 |
| 227S | 110 St-Malcolm X Plaza (2,3), Downtown | 6,128 | 9,430 | 4,579 | 1,549 | 122 |
| 254S | Junius St (3), New Lots | 6,118 | 8,041 | 1,731 | 4,387 | 4,461 |
| A17N | Cathedral Pkwy (110 St) (B,C), Uptown | 6,109 | 7,501 | 1,605 | 4,504 | 1 |
| B21N | Bay Pkwy (D), Manhattan | 6,030 | 8,291 | 5,358 | 672 | 4 |
| 237S | Grand Army Plaza (2,3), Outbound | 6,024 | 7,897 | 1,313 | 4,711 | 3 |
| A47N | Kingston-Throop Avs (C), Manhattan | 6,016 | 7,627 | 4,526 | 1,490 | 0 |
| F02N | 169 St (F), Jamaica | 5,990 | 7,992 | 90 | 5,900 | 0 |
| L13N | Montrose Av (L), Manhattan | 5,953 | 7,056 | 4,872 | 1,081 | 0 |
| L13S | Montrose Av (L), Outbound | 5,941 | 7,029 | 992 | 4,949 | 0 |
| 227N | 110 St-Malcolm X Plaza (2,3), Uptown | 5,940 | 9,137 | 1,384 | 4,555 | 88 |
| D10N | 167 St (B,D), Northbound | 5,927 | 9,075 | 630 | 5,297 | 0 |
| A61N | Rockaway Blvd (A), Manhattan | 5,923 | 8,154 | 5,167 | 756 | 293 |
| J30S | Gates Av (J,Z), Manhattan | 5,908 | 7,860 | 4,358 | 1,550 | 0 |
| M21N | Chambers St (J,Z), Brooklyn | 5,889 | 8,318 | 4,328 | 1,561 | 3,236 |
| 237N | Grand Army Plaza (2,3), Manhattan | 5,880 | 7,725 | 4,570 | 1,309 | 3 |
| B21S | Bay Pkwy (D), Southbound | 5,880 | 8,085 | 649 | 5,231 | 20 |
| 246N | Newkirk Av-Little Haiti (2,5), Manhattan | 5,875 | 7,698 | 5,685 | 190 | 0 |
| L12S | Grand St (L), Outbound | 5,824 | 6,908 | 1,091 | 4,734 | 0 |
| 217N | Simpson St (2,5), Northbound | 5,801 | 8,333 | 1,282 | 4,519 | 0 |
| A61S | Rockaway Blvd (A), Outbound | 5,799 | 8,003 | 665 | 5,134 | 74 |
| F03S | Parsons Blvd (F), Manhattan | 5,777 | 7,111 | 5,474 | 303 | 91 |
| R06S | 36 Av (N,W), Manhattan | 5,763 | 7,220 | 5,216 | 547 | 0 |
| 412S | 170 St (4), Manhattan | 5,754 | 8,430 | 4,780 | 973 | 0 |
| G16S | Northern Blvd (M,R), Manhattan | 5,749 | 7,048 | 3,889 | 1,860 | 8 |
| 217S | Simpson St (2,5), Manhattan | 5,745 | 8,226 | 4,585 | 1,160 | 0 |
| 233N | Hoyt St (2,3), Manhattan | 5,733 | 7,441 | 2,368 | 3,365 | 0 |
| N07N | Bay Pkwy (N), Manhattan | 5,722 | 7,025 | 5,007 | 716 | 0 |
| R06N | 36 Av (N,W), Astoria | 5,695 | 7,171 | 485 | 5,211 | 0 |
| 713N | 52 St (7), Outbound | 5,689 | 8,331 | 2,892 | 2,797 | 0 |
| 110N | 191 St (1), The Bronx | 5,676 | 7,611 | 988 | 4,688 | 0 |
| D37N | Avenue U (Q), Manhattan | 5,652 | 7,689 | 4,673 | 979 | 0 |
| L05N | 3 Av (L), West Side | 5,623 | 5,822 | 2,480 | 3,143 | 0 |
| 402N | Mosholu Pkwy (4), Woodlawn | 5,612 | 8,959 | 59 | 5,553 | 0 |
| J29S | Halsey St (J), Manhattan | 5,609 | 7,642 | 3,781 | 1,828 | 0 |
| 109S | Dyckman St (1), Downtown | 5,607 | 7,013 | 4,870 | 737 | 0 |
| 402S | Mosholu Pkwy (4), Manhattan | 5,607 | 8,947 | 5,546 | 61 | 0 |
| L12N | Grand St (L), Manhattan | 5,605 | 6,655 | 4,519 | 1,086 | 0 |
| 412N | 170 St (4), Northbound | 5,576 | 8,176 | 965 | 4,611 | 0 |
| N07S | Bay Pkwy (N), Coney Island | 5,564 | 6,834 | 676 | 4,888 | 0 |
| J30N | Gates Av (J,Z), Outbound | 5,544 | 7,408 | 1,514 | 4,030 | 0 |
| 136N | Franklin St (1), Uptown | 5,525 | 6,015 | 4,409 | 1,116 | 2 |
| G16N | Northern Blvd (M,R), Outbound | 5,523 | 6,787 | 1,755 | 3,768 | 8 |
| M23S | Broad St (J,Z), Last Stop | 5,522 | 8,810 | 0 | 5,522 | 0 |
| N03N | Fort Hamilton Pkwy (N), Manhattan | 5,520 | 4,639 | 4,379 | 1,140 | 0 |
| 231S | Clark St (2,3), Outbound | 5,495 | 6,006 | 1,638 | 3,857 | 0 |
| F03N | Parsons Blvd (F), Jamaica | 5,451 | 6,718 | 320 | 5,130 | 63 |
| 136S | Franklin St (1), Downtown | 5,421 | 5,970 | 939 | 4,482 | 2 |
| 246S | Newkirk Av-Little Haiti (2,5), Flatbush | 5,409 | 7,089 | 161 | 5,248 | 0 |
| N03S | Fort Hamilton Pkwy (N), Coney Island | 5,361 | 4,514 | 1,155 | 4,206 | 0 |
| 211N | Pelham Pkwy (2,5), Northbound | 5,355 | 8,711 | 1,034 | 4,321 | 0 |
| D37S | Avenue U (Q), Southbound | 5,327 | 7,259 | 903 | 4,424 | 0 |
| A16S | 116 St (B,C), Downtown | 5,312 | 7,668 | 3,181 | 2,131 | 0 |
| B18N | 79 St (D), Manhattan | 5,302 | 6,667 | 4,621 | 681 | 0 |
| A03S | Dyckman St (A), Downtown | 5,283 | 7,417 | 5,282 | 2 | 4 |
| G35N | Clinton-Washington Avs (G), Queens | 5,258 | 5,842 | 2,603 | 2,655 | 0 |
| R34N | Prospect Av (R), Manhattan | 5,257 | 6,557 | 4,168 | 1,089 | 12 |
| 211S | Pelham Pkwy (2,5), Manhattan | 5,249 | 8,483 | 4,324 | 925 | 0 |
| 231N | Clark St (2,3), Manhattan | 5,232 | 5,719 | 3,616 | 1,617 | 0 |
| A16N | 116 St (B,C), Uptown | 5,213 | 7,515 | 2,165 | 3,048 | 0 |
| N04N | New Utrecht Av (N), Manhattan | 5,199 | 6,169 | 3,648 | 1,550 | 2,882 |
| 611S | Elder Av (6), Manhattan | 5,198 | 7,206 | 4,630 | 568 | 0 |
| 610S | Morrison Av-Soundview (6), Manhattan | 5,196 | 7,398 | 4,431 | 766 | 0 |
| 401S | Woodlawn (4), Manhattan | 5,184 | 7,249 | 5,184 | 0 | 0 |
| A47S | Kingston-Throop Avs (C), Outbound | 5,183 | 6,585 | 1,175 | 4,009 | 0 |
| M23N | Broad St (J,Z), Brooklyn | 5,174 | 8,251 | 5,174 | 0 | 0 |
| 109N | Dyckman St (1), The Bronx | 5,166 | 6,483 | 754 | 4,413 | 0 |
| A65N | Ozone Park-Lefferts Blvd (A), Manhattan | 5,155 | 7,919 | 5,155 | 0 | 0 |
| D30N | Cortelyou Rd (Q), Manhattan | 5,145 | 6,694 | 4,140 | 1,005 | 0 |
| B18S | 79 St (D), Southbound | 5,133 | 6,457 | 669 | 4,464 | 0 |
| A03N | Dyckman St (A), Uptown | 5,089 | 7,149 | 13 | 5,076 | 0 |
| M04N | Fresh Pond Rd (M), Inbound | 5,080 | 6,389 | 4,889 | 191 | 0 |
| F25N | 15 St-Prospect Park (F,G), Northbound | 5,060 | 6,781 | 4,620 | 440 | 2 |
| F25S | 15 St-Prospect Park (F,G), Southbound | 5,038 | 6,744 | 400 | 4,638 | 2 |
| D03S | Bedford Park Blvd (B,D), Manhattan | 5,030 | 7,790 | 4,792 | 238 | 366 |
| 251N | Sutter Av-Rutland Rd (3), Manhattan | 5,022 | 7,093 | 4,336 | 685 | 25 |
| G35S | Clinton-Washington Avs (G), Southbound | 5,017 | 5,609 | 2,524 | 2,494 | 0 |
| J31S | Kosciuszko St (J), Manhattan | 5,010 | 6,100 | 3,911 | 1,099 | 0 |
| B19N | 18 Av (D), Manhattan | 4,990 | 6,590 | 4,515 | 475 | 0 |
| 401N | Woodlawn (4), Last Stop | 4,984 | 6,972 | 0 | 4,984 | 0 |
| 711N | 69 St (7), Outbound | 4,980 | 6,490 | 2,511 | 2,469 | 0 |
| R34S | Prospect Av (R), Southbound | 4,973 | 6,182 | 987 | 3,986 | 12 |
| B12N | 9 Av (D), Manhattan | 4,963 | 5,919 | 4,251 | 712 | 0 |
| 108N | 207 St (1), The Bronx | 4,957 | 6,662 | 638 | 4,319 | 0 |
| F26N | Fort Hamilton Pkwy (F,G), Northbound | 4,932 | 6,253 | 4,659 | 273 | 0 |
| 219S | Prospect Av (2,5), Manhattan | 4,901 | 7,375 | 4,098 | 803 | 0 |
| 611N | Elder Av (6), Northbound | 4,900 | 6,783 | 488 | 4,412 | 0 |
| A65S | Ozone Park-Lefferts Blvd (A), Last Stop | 4,885 | 7,507 | 0 | 4,885 | 0 |
| 215S | 174 St (2,5), Manhattan | 4,883 | 7,043 | 3,984 | 900 | 4 |
| 135S | Canal St (1), Downtown | 4,880 | 7,941 | 933 | 3,947 | 30 |
| M04S | Fresh Pond Rd (M), Middle Village | 4,849 | 6,103 | 172 | 4,677 | 0 |
| B12S | 9 Av (D), Southbound | 4,846 | 5,783 | 689 | 4,157 | 0 |
| D01S | Norwood-205 St (D), Manhattan | 4,840 | 8,926 | 4,840 | 0 | 0 |
| F26S | Fort Hamilton Pkwy (F,G), Southbound | 4,839 | 6,129 | 222 | 4,617 | 0 |
| D01N | Norwood-205 St (D), Last Stop | 4,831 | 8,913 | 0 | 4,831 | 0 |
| D27N | Parkside Av (Q), Manhattan | 4,831 | 5,543 | 4,129 | 702 | 0 |
| D04S | Kingsbridge Rd (B,D), Manhattan | 4,821 | 8,509 | 4,718 | 103 | 6 |
| N08N | Kings Hwy (N), Manhattan | 4,817 | 4,622 | 4,318 | 499 | 0 |
| B19S | 18 Av (D), Southbound | 4,813 | 6,357 | 429 | 4,384 | 0 |
| A43S | Lafayette Av (C), Outbound | 4,811 | 5,607 | 1,805 | 3,006 | 0 |
| N04S | New Utrecht Av (N), Coney Island | 4,803 | 5,652 | 1,311 | 3,492 | 2,394 |
| 135N | Canal St (1), Uptown | 4,797 | 7,722 | 3,758 | 1,039 | 30 |
| D34N | Avenue M (Q), Manhattan | 4,796 | 5,912 | 3,381 | 1,415 | 0 |
| D30S | Cortelyou Rd (Q), Southbound | 4,789 | 6,232 | 938 | 3,851 | 0 |
| G36S | Fulton St (G), Southbound | 4,785 | 5,039 | 2,122 | 2,663 | 0 |
| J29N | Halsey St (J), Outbound | 4,772 | 6,533 | 1,555 | 3,217 | 0 |
| G34N | Classon Av (G), Queens | 4,769 | 5,947 | 2,592 | 2,177 | 0 |
| J31N | Kosciuszko St (J), Outbound | 4,768 | 5,829 | 1,089 | 3,679 | 0 |
| R24N | City Hall (R,W), Uptown | 4,758 | 6,964 | 3,088 | 1,671 | 0 |
| B16N | 62 St (D), Manhattan | 4,752 | 5,725 | 2,127 | 2,626 | 2,967 |
| D34S | Avenue M (Q), Southbound | 4,744 | 5,852 | 1,442 | 3,301 | 0 |
| 219N | Prospect Av (2,5), Northbound | 4,740 | 7,159 | 873 | 3,867 | 0 |
| A14S | 135 St (B,C), Downtown | 4,728 | 6,319 | 3,538 | 1,190 | 57 |
| 108S | 207 St (1), Downtown | 4,717 | 6,306 | 4,228 | 490 | 0 |
| 607S | Castle Hill Av (6), Manhattan | 4,710 | 6,888 | 4,368 | 342 | 0 |
| R43N | 77 St (R), Manhattan | 4,707 | 6,101 | 4,654 | 53 | 0 |
| A14N | 135 St (B,C), Uptown | 4,693 | 6,277 | 1,271 | 3,423 | 56 |
| 215N | 174 St (2,5), Northbound | 4,690 | 6,784 | 944 | 3,746 | 4 |
| D27S | Parkside Av (Q), Southbound | 4,689 | 5,384 | 712 | 3,978 | 0 |
| D04N | Kingsbridge Rd (B,D), Northbound | 4,683 | 8,274 | 112 | 4,571 | 6 |
| 101S | Van Cortlandt Park-242 St (1), Manhattan | 4,663 | 7,423 | 4,663 | 0 | 0 |
| 601S | Pelham Bay Park (6), Manhattan | 4,656 | 7,499 | 4,656 | 0 | 0 |
| D03N | Bedford Park Blvd (B,D), Northbound | 4,656 | 7,125 | 106 | 4,550 | 94 |
| 610N | Morrison Av-Soundview (6), Northbound | 4,607 | 6,571 | 559 | 4,047 | 0 |
| N08S | Kings Hwy (N), Coney Island | 4,607 | 4,412 | 462 | 4,145 | 0 |
| 242N | Sterling St (2,5), Manhattan | 4,602 | 5,835 | 4,249 | 353 | 0 |
| 214S | West Farms Sq-E Tremont Av (2,5), Manhattan | 4,583 | 7,450 | 3,668 | 915 | 118 |
| A49N | Ralph Av (C), Manhattan | 4,582 | 6,587 | 3,671 | 911 | 0 |
| R26N | Rector St (R,W), Uptown | 4,572 | 7,521 | 3,166 | 1,406 | 0 |
| S01S | Franklin Av (S), Prospect Park | 4,555 | 6,196 | 4,555 | 0 | 3,409 |
| R45N | Bay Ridge-95 St (R), Manhattan | 4,546 | 6,216 | 4,546 | 0 | 0 |
| 251S | Sutter Av-Rutland Rd (3), New Lots | 4,540 | 6,437 | 654 | 3,885 | 25 |
| A50N | Rockaway Av (C), Manhattan | 4,508 | 6,184 | 3,246 | 1,262 | 0 |
| D09S | 170 St (B,D), Manhattan | 4,448 | 7,650 | 3,814 | 634 | 0 |
| R43S | 77 St (R), Bay Ridge | 4,443 | 5,762 | 53 | 4,390 | 0 |
| 101N | Van Cortlandt Park-242 St (1), Last Stop | 4,436 | 7,065 | 0 | 4,436 | 0 |
| 607N | Castle Hill Av (6), Pelham Bay | 4,430 | 6,475 | 345 | 4,085 | 0 |
| D33S | Avenue J (Q), Southbound | 4,430 | 6,014 | 1,348 | 3,082 | 0 |
| G34S | Classon Av (G), Southbound | 4,411 | 5,521 | 2,111 | 2,300 | 0 |
| R26S | Rector St (R,W), Downtown | 4,411 | 7,246 | 1,402 | 3,010 | 0 |
| 410S | 176 St (4), Manhattan | 4,404 | 5,971 | 3,832 | 572 | 0 |
| D33N | Avenue J (Q), Manhattan | 4,401 | 5,974 | 3,139 | 1,262 | 0 |
| 242S | Sterling St (2,5), Flatbush | 4,382 | 5,558 | 339 | 4,043 | 0 |
| 208S | Gun Hill Rd (2,5), Manhattan | 4,374 | 7,166 | 3,949 | 425 | 0 |
| 214N | West Farms Sq-E Tremont Av (2,5), Northbound | 4,356 | 7,107 | 939 | 3,417 | 118 |
| G20N | 36 St (M,R), Outbound | 4,344 | 6,600 | 1,510 | 2,833 | 881 |
| A43N | Lafayette Av (C), Manhattan | 4,296 | 5,016 | 2,672 | 1,623 | 0 |
| R24S | City Hall (R,W), Downtown | 4,286 | 6,293 | 1,406 | 2,880 | 0 |
| 257N | New Lots Av (3), Manhattan | 4,275 | 5,847 | 4,275 | 0 | 112 |
| N05N | 18 Av (N), Manhattan | 4,275 | 3,927 | 3,643 | 631 | 0 |
| S01N | Franklin Av (S), Last Stop | 4,275 | 5,735 | 0 | 4,275 | 3,403 |
| G32S | Myrtle-Willoughby Avs (G), Southbound | 4,259 | 6,070 | 1,727 | 2,532 | 0 |
| R45S | Bay Ridge-95 St (R), Last Stop | 4,258 | 5,825 | 0 | 4,258 | 0 |
| 601N | Pelham Bay Park (6), Last Stop | 4,250 | 6,848 | 0 | 4,250 | 0 |
| G30S | Broadway (G), Southbound | 4,230 | 5,151 | 1,402 | 2,828 | 0 |
| N05S | 18 Av (N), Coney Island | 4,221 | 3,891 | 615 | 3,606 | 0 |
| F05N | Briarwood (E,F), Jamaica | 4,201 | 5,324 | 371 | 3,830 | 98 |
| 405S | Bedford Park Blvd-Lehman College (4), Manhattan | 4,194 | 5,551 | 4,100 | 94 | 0 |
| G07S | Jamaica-Van Wyck (E), Manhattan | 4,194 | 5,015 | 3,441 | 753 | 0 |
| G32N | Myrtle-Willoughby Avs (G), Queens | 4,193 | 5,959 | 2,609 | 1,583 | 0 |
| 220S | Jackson Av (2,5), Manhattan | 4,182 | 5,580 | 3,490 | 692 | 1 |
| 252N | Saratoga Av (3), Manhattan | 4,175 | 5,761 | 3,469 | 706 | 200 |
| A57N | Grant Av (A), Manhattan | 4,169 | 6,107 | 3,842 | 327 | 11 |
| 408S | 183 St (4), Manhattan | 4,168 | 6,071 | 3,812 | 357 | 0 |
| J15S | Woodhaven Blvd (J,Z), Manhattan | 4,134 | 4,913 | 2,355 | 1,780 | 41 |
| H11N | Far Rockaway-Mott Av (A), Manhattan | 4,123 | 7,127 | 4,123 | 0 | 0 |
| 720S | Hunters Point Av (7), Manhattan | 4,122 | 7,301 | 2,957 | 1,164 | 5 |
| 208N | Gun Hill Rd (2,5), Northbound | 4,121 | 6,777 | 487 | 3,634 | 0 |
| 220N | Jackson Av (2,5), Northbound | 4,109 | 5,499 | 754 | 3,354 | 1 |
| B20N | 20 Av (D), Manhattan | 4,092 | 5,312 | 3,693 | 399 | 0 |
| 405N | Bedford Park Blvd-Lehman College (4), Northbound | 4,073 | 5,395 | 92 | 3,982 | 0 |
| B17N | 71 St (D), Manhattan | 4,062 | 5,927 | 3,461 | 601 | 0 |
| A49S | Ralph Av (C), Outbound | 4,060 | 5,841 | 788 | 3,272 | 0 |
| B17S | 71 St (D), Southbound | 4,033 | 5,885 | 623 | 3,410 | 0 |
| 618S | Brook Av (6), Manhattan | 4,021 | 6,295 | 3,382 | 639 | 0 |
| D09N | 170 St (B,D), Northbound | 4,010 | 6,925 | 525 | 3,486 | 0 |
| 410N | 176 St (4), Northbound | 4,001 | 5,430 | 545 | 3,456 | 0 |
| L20N | Wilson Av (L), Manhattan | 3,989 | 4,722 | 2,936 | 1,053 | 0 |
| B20S | 20 Av (D), Southbound | 3,982 | 5,171 | 374 | 3,608 | 0 |
| F22N | Smith-9 Sts (F,G), Northbound | 3,972 | 5,179 | 3,092 | 880 | 73 |
| F22S | Smith-9 Sts (F,G), Southbound | 3,953 | 5,158 | 868 | 3,085 | 73 |
| 408N | 183 St (4), Northbound | 3,942 | 5,747 | 351 | 3,591 | 0 |
| A57S | Grant Av (A), Queens | 3,938 | 5,781 | 311 | 3,627 | 11 |
| H03N | Howard Beach-JFK Airport (A), Manhattan | 3,917 | 3,595 | 3,602 | 315 | 321 |
| B16S | 62 St (D), Southbound | 3,916 | 4,693 | 2,255 | 1,661 | 2,309 |
| 257S | New Lots Av (3), Last Stop | 3,913 | 5,353 | 0 | 3,913 | 112 |
| J15N | Woodhaven Blvd (J,Z), Jamaica | 3,911 | 4,664 | 1,728 | 2,183 | 11 |
| M05N | Forest Av (M), Inbound | 3,911 | 4,611 | 3,802 | 109 | 0 |
| 238N | Eastern Pkwy-Brooklyn Museum (2,3), Manhattan | 3,904 | 4,427 | 3,111 | 793 | 68 |
| A18S | 103 St (B,C), Downtown | 3,895 | 5,115 | 3,036 | 859 | 0 |
| M13N | Lorimer St (J,M), Outbound | 3,884 | 5,973 | 2,191 | 1,693 | 21 |
| 253N | Rockaway Av (3), Manhattan | 3,882 | 5,365 | 3,045 | 837 | 210 |
| 252S | Saratoga Av (3), New Lots | 3,864 | 5,349 | 649 | 3,215 | 200 |
| G07N | Jamaica-Van Wyck (E), Jamaica | 3,863 | 4,634 | 628 | 3,236 | 0 |
| 106S | Marble Hill-225 St (1), Downtown | 3,859 | 5,480 | 3,707 | 152 | 0 |
| 106N | Marble Hill-225 St (1), The Bronx | 3,830 | 5,438 | 139 | 3,690 | 0 |
| 720N | Hunters Point Av (7), Outbound | 3,824 | 6,789 | 1,001 | 2,823 | 5 |
| M09N | Knickerbocker Av (M), Inbound | 3,809 | 5,050 | 2,646 | 1,162 | 0 |
| A50S | Rockaway Av (C), Outbound | 3,803 | 5,244 | 987 | 2,815 | 0 |
| 618N | Brook Av (6), Northbound | 3,792 | 5,934 | 646 | 3,146 | 0 |
| 245N | Beverly Rd (2,5), Manhattan | 3,779 | 4,549 | 3,620 | 158 | 0 |
| L20S | Wilson Av (L), Outbound | 3,757 | 4,431 | 914 | 2,843 | 0 |
| D38N | Neck Rd (Q), Manhattan | 3,756 | 4,713 | 3,114 | 642 | 0 |
| 103S | 238 St (1), Manhattan | 3,752 | 4,424 | 3,745 | 6 | 0 |
| 103N | 238 St (1), Van Cortlandt | 3,748 | 4,422 | 8 | 3,740 | 0 |
| A18N | 103 St (B,C), Uptown | 3,748 | 4,915 | 808 | 2,940 | 0 |
| S04S | Botanic Garden (S), Prospect Park | 3,724 | 4,969 | 1,142 | 2,582 | 2,672 |
| 238S | Eastern Pkwy-Brooklyn Museum (2,3), Outbound | 3,709 | 4,206 | 637 | 3,072 | 68 |
| G30N | Broadway (G), Queens | 3,702 | 4,451 | 2,600 | 1,102 | 0 |
| 604S | Westchester Sq-E Tremont Av (6), Manhattan | 3,698 | 6,544 | 3,487 | 211 | 0 |
| M05S | Forest Av (M), Middle Village | 3,693 | 4,356 | 98 | 3,595 | 0 |
| N06N | 20 Av (N), Manhattan | 3,691 | 3,871 | 3,273 | 418 | 0 |
| M13S | Lorimer St (J,M), Manhattan | 3,682 | 5,663 | 1,556 | 2,126 | 0 |
| 416S | 138 St-Grand Concourse (4,5), Manhattan | 3,672 | 4,012 | 2,316 | 1,356 | 373 |
| B13N | Fort Hamilton Pkwy (D), Manhattan | 3,654 | 4,249 | 2,704 | 950 | 0 |
| M19S | Bowery (J,Z), Downtown | 3,626 | 4,702 | 1,503 | 2,123 | 0 |
| B13S | Fort Hamilton Pkwy (D), Southbound | 3,605 | 4,192 | 948 | 2,657 | 0 |
| R08N | 39 Av-Dutch Kills (N,W), Astoria | 3,602 | 2,904 | 398 | 3,205 | 0 |
| 411S | Mt Eden Av (4), Manhattan | 3,593 | 5,290 | 3,082 | 511 | 0 |
| 416N | 138 St-Grand Concourse (4,5), Northbound | 3,592 | 3,916 | 1,362 | 2,231 | 275 |
| 236S | Bergen St (2,3), Outbound | 3,568 | 3,883 | 699 | 2,870 | 5 |
| 249N | Kingston Av (3), Manhattan | 3,549 | 4,961 | 3,034 | 515 | 0 |
| 615S | E 149 St (6), Manhattan | 3,546 | 4,904 | 2,988 | 557 | 0 |
| 236N | Bergen St (2,3), Manhattan | 3,540 | 3,867 | 2,893 | 647 | 5 |
| 245S | Beverly Rd (2,5), Flatbush | 3,539 | 4,263 | 161 | 3,378 | 0 |
| 604N | Westchester Sq-E Tremont Av (6), Pelham Bay | 3,517 | 6,221 | 202 | 3,315 | 0 |
| H11S | Far Rockaway-Mott Av (A), Last Stop | 3,509 | 6,069 | 0 | 3,509 | 0 |
| J20S | Crescent St (J,Z), Manhattan | 3,508 | 4,872 | 2,622 | 887 | 25 |
| F04S | Sutphin Blvd (F), Manhattan | 3,507 | 4,525 | 3,210 | 296 | 0 |
| N06S | 20 Av (N), Coney Island | 3,506 | 3,682 | 406 | 3,100 | 0 |
| A10S | 163 St-Amsterdam Av (C), Downtown | 3,484 | 4,943 | 2,788 | 696 | 0 |
| J20N | Crescent St (J,Z), Outbound | 3,484 | 4,846 | 877 | 2,607 | 12 |
| A05S | 190 St (A), Downtown | 3,473 | 5,158 | 3,302 | 171 | 0 |
| D08S | 174-175 Sts (B,D), Manhattan | 3,472 | 5,401 | 2,929 | 543 | 0 |
| R08S | 39 Av-Dutch Kills (N,W), Manhattan | 3,468 | 2,796 | 3,136 | 332 | 0 |
| A59N | 80 St (A), Manhattan | 3,463 | 4,732 | 3,090 | 373 | 59 |
| G20S | 36 St (M,R), Manhattan | 3,455 | 5,397 | 2,339 | 1,116 | 134 |
| D06S | 182-183 Sts (B,D), Manhattan | 3,453 | 5,162 | 3,077 | 376 | 0 |
| R35N | 25 St (R), Manhattan | 3,449 | 4,325 | 2,503 | 946 | 25 |
| D38S | Neck Rd (Q), Southbound | 3,446 | 4,327 | 596 | 2,850 | 0 |
| 216S | Freeman St (2,5), Manhattan | 3,437 | 4,719 | 2,891 | 546 | 121 |
| 615N | E 149 St (6), Northbound | 3,437 | 4,768 | 606 | 2,830 | 0 |
| D42N | W 8 St-NY Aquarium (F,Q), Manhattan | 3,425 | 4,312 | 3,286 | 139 | 1,326 |
| M10N | Central Av (M), Inbound | 3,416 | 4,855 | 2,640 | 776 | 0 |
| A05N | 190 St (A), Uptown | 3,406 | 5,051 | 136 | 3,270 | 0 |
| D42S | W 8 St-NY Aquarium (F,Q), Coney Island | 3,404 | 4,290 | 124 | 3,280 | 1,326 |
| M19N | Bowery (J,Z), Brooklyn | 3,389 | 4,394 | 1,837 | 1,552 | 0 |
| 609S | St Lawrence Av (6), Manhattan | 3,388 | 4,484 | 2,862 | 526 | 0 |
| A59S | 80 St (A), Outbound | 3,373 | 4,613 | 327 | 3,047 | 55 |
| M01N | Middle Village-Metropolitan Av (M), Inbound | 3,372 | 3,926 | 3,372 | 0 | 0 |
| B22N | 25 Av (D), Manhattan | 3,357 | 5,198 | 3,021 | 336 | 0 |
| F04N | Sutphin Blvd (F), Jamaica | 3,353 | 4,335 | 316 | 3,036 | 0 |
| S04N | Botanic Garden (S), Franklin Av | 3,347 | 4,416 | 2,397 | 950 | 2,352 |
| 411N | Mt Eden Av (4), Northbound | 3,328 | 4,908 | 514 | 2,814 | 0 |
| G15S | 65 St (M,R), Manhattan | 3,309 | 4,102 | 2,117 | 1,192 | 1 |
| N09N | Avenue U (N), Manhattan | 3,305 | 3,469 | 3,017 | 288 | 0 |
| 216N | Freeman St (2,5), Northbound | 3,260 | 4,454 | 505 | 2,756 | 0 |
| 501S | Eastchester-Dyre Av (5), Manhattan | 3,254 | 5,203 | 3,254 | 0 | 0 |
| M09S | Knickerbocker Av (M), Middle Village | 3,254 | 4,346 | 1,063 | 2,191 | 0 |
| 253S | Rockaway Av (3), New Lots | 3,241 | 4,474 | 699 | 2,542 | 210 |
| B22S | 25 Av (D), Coney Island | 3,217 | 4,981 | 306 | 2,911 | 0 |
| N09S | Avenue U (N), Coney Island | 3,174 | 3,328 | 231 | 2,942 | 0 |
| 503N | Gun Hill Rd (5), Eastchester | 3,167 | 4,500 | 60 | 3,108 | 0 |
| 503S | Gun Hill Rd (5), Manhattan | 3,167 | 4,498 | 3,107 | 60 | 0 |
| M01S | Middle Village-Metropolitan Av (M), Last Stop | 3,153 | 3,673 | 0 | 3,153 | 0 |
| F29N | Ditmas Av (F), Manhattan | 3,148 | 4,211 | 2,523 | 625 | 0 |
| 201S | Wakefield-241 St (2), Manhattan | 3,146 | 4,673 | 3,146 | 0 | 0 |
| 255N | Pennsylvania Av (3), Manhattan | 3,145 | 5,004 | 3,099 | 46 | 246 |
| 249S | Kingston Av (3), Outbound | 3,125 | 4,387 | 460 | 2,665 | 0 |
| 210S | Allerton Av (2,5), Manhattan | 3,116 | 5,435 | 2,842 | 274 | 0 |
| A10N | 163 St-Amsterdam Av (C), Uptown | 3,089 | 4,383 | 505 | 2,584 | 0 |
| D06N | 182-183 Sts (B,D), Northbound | 3,083 | 4,623 | 302 | 2,781 | 0 |
| D29N | Beverley Rd (Q), Manhattan | 3,079 | 3,276 | 2,631 | 448 | 0 |
| 255S | Pennsylvania Av (3), New Lots | 3,069 | 4,881 | 47 | 3,021 | 246 |
| 501N | Eastchester-Dyre Av (5), Last Stop | 3,050 | 4,878 | 0 | 3,050 | 0 |
| 609N | St Lawrence Av (6), Northbound | 3,045 | 4,033 | 438 | 2,607 | 0 |
| M10S | Central Av (M), Middle Village | 3,029 | 4,327 | 716 | 2,313 | 0 |
| 210N | Allerton Av (2,5), Northbound | 3,024 | 5,277 | 265 | 2,759 | 0 |
| D08N | 174-175 Sts (B,D), Northbound | 3,024 | 4,719 | 433 | 2,591 | 0 |
| R35S | 25 St (R), Southbound | 3,017 | 3,773 | 737 | 2,280 | 25 |
| H04N | Broad Channel (A,S), Inbound | 2,991 | 5,826 | 1,476 | 1,516 | 2,764 |
| L27N | New Lots Av (L), Manhattan | 2,990 | 4,637 | 2,809 | 182 | 245 |
| D29S | Beverley Rd (Q), Southbound | 2,973 | 3,166 | 456 | 2,517 | 0 |
| G15N | 65 St (M,R), Outbound | 2,959 | 3,686 | 1,051 | 1,908 | 1 |
| 241N | President St-Medgar Evers College (2,5), Manhattan | 2,955 | 3,859 | 2,521 | 433 | 0 |
| F29S | Ditmas Av (F), Southbound | 2,931 | 3,915 | 599 | 2,333 | 0 |
| 241S | President St-Medgar Evers College (2,5), Flatbush | 2,921 | 3,814 | 449 | 2,473 | 0 |
| J17S | 75 St-Elderts Ln (J,Z), Manhattan | 2,892 | 3,417 | 1,910 | 982 | 0 |
| 602S | Buhre Av (6), Manhattan | 2,883 | 4,101 | 2,807 | 76 | 0 |
| J16S | 85 St-Forest Pkwy (J), Manhattan | 2,882 | 5,335 | 1,731 | 1,151 | 0 |
| L27S | New Lots Av (L), Canarsie | 2,878 | 4,468 | 187 | 2,691 | 245 |
| H04S | Broad Channel (A,S), Rockaways | 2,863 | 5,653 | 1,453 | 1,411 | 2,641 |
| 201N | Wakefield-241 St (2), Last Stop | 2,862 | 4,253 | 0 | 2,862 | 0 |
| F30N | 18 Av (F), Manhattan | 2,862 | 3,926 | 2,225 | 637 | 0 |
| B14N | 50 St (D), Manhattan | 2,816 | 3,411 | 1,792 | 1,024 | 0 |
| J17N | 75 St-Elderts Ln (J,Z), Jamaica | 2,794 | 3,313 | 949 | 1,845 | 0 |
| F07S | 75 Av (E,F), Manhattan | 2,759 | 3,837 | 2,359 | 401 | 4 |
| A60N | 88 St (A), Manhattan | 2,755 | 3,869 | 2,356 | 399 | 446 |
| 205S | 233 St (2,5), Manhattan | 2,748 | 4,909 | 2,696 | 52 | 0 |
| G31S | Flushing Av (G), Southbound | 2,734 | 2,613 | 1,141 | 1,592 | 0 |
| F30S | 18 Av (F), Southbound | 2,732 | 3,745 | 594 | 2,138 | 0 |
| B14S | 50 St (D), Southbound | 2,724 | 3,305 | 1,019 | 1,705 | 0 |
| J28S | Chauncey St (J,Z), Manhattan | 2,719 | 3,926 | 1,550 | 1,169 | 0 |
| D32N | Avenue H (Q), Manhattan | 2,717 | 3,545 | 2,043 | 674 | 0 |
| 248S | Nostrand Av (3), Outbound | 2,711 | 4,316 | 741 | 1,970 | 0 |
| 602N | Buhre Av (6), Pelham Bay | 2,710 | 3,851 | 60 | 2,650 | 0 |
| J16N | 85 St-Forest Pkwy (J), Jamaica | 2,709 | 5,031 | 1,089 | 1,620 | 0 |
| F07N | 75 Av (E,F), Jamaica | 2,696 | 3,760 | 354 | 2,341 | 4 |
| D32S | Avenue H (Q), Southbound | 2,684 | 3,504 | 687 | 1,996 | 0 |
| H03S | Howard Beach-JFK Airport (A), Rockaways | 2,654 | 2,720 | 327 | 2,327 | 320 |
| 248N | Nostrand Av (3), Manhattan | 2,646 | 4,195 | 2,002 | 644 | 0 |
| 205N | 233 St (2,5), Northbound | 2,645 | 4,728 | 47 | 2,598 | 0 |
| G31N | Flushing Av (G), Queens | 2,603 | 2,477 | 1,557 | 1,046 | 0 |
| 218S | Intervale Av (2,5), Manhattan | 2,549 | 3,423 | 2,095 | 453 | 0 |
| A53N | Van Siclen Av (C), Manhattan | 2,530 | 3,290 | 2,242 | 288 | 1 |
| J23S | Van Siclen Av (J,Z), Manhattan | 2,525 | 2,879 | 2,016 | 510 | 0 |
| M06N | Seneca Av (M), Inbound | 2,515 | 3,488 | 2,405 | 110 | 0 |
| L25N | Sutter Av (L), Manhattan | 2,431 | 3,804 | 1,901 | 530 | 260 |
| 504S | Pelham Pkwy (5), Manhattan | 2,429 | 3,459 | 2,276 | 152 | 0 |
| 218N | Intervale Av (2,5), Northbound | 2,428 | 3,274 | 482 | 1,947 | 31 |
| J23N | Van Siclen Av (J,Z), Outbound | 2,424 | 2,765 | 555 | 1,869 | 0 |
| 302S | 145 St (3), Downtown | 2,421 | 3,409 | 2,421 | 0 | 0 |
| 614S | Longwood Av (6), Manhattan | 2,416 | 3,319 | 1,840 | 575 | 0 |
| D41N | Ocean Pkwy (Q), Manhattan | 2,381 | 3,322 | 1,995 | 386 | 0 |
| A60S | 88 St (A), Outbound | 2,373 | 3,299 | 225 | 2,148 | 131 |
| B23N | Bay 50 St (D), Manhattan | 2,372 | 2,880 | 1,955 | 417 | 0 |
| M06S | Seneca Av (M), Middle Village | 2,354 | 3,260 | 128 | 2,226 | 0 |
| 301S | Harlem-148 St (3), Downtown | 2,349 | 3,808 | 2,349 | 0 | 0 |
| 504N | Pelham Pkwy (5), Eastchester | 2,345 | 3,361 | 194 | 2,152 | 0 |
| D41S | Ocean Pkwy (Q), Coney Island | 2,345 | 3,267 | 403 | 1,941 | 0 |
| M14N | Hewes St (J,M), Outbound | 2,337 | 3,659 | 1,459 | 878 | 0 |
| 204S | Nereid Av (2,5), Manhattan | 2,333 | 3,932 | 2,210 | 123 | 247 |
| J14S | 104 St (J,Z), Manhattan | 2,313 | 2,952 | 1,109 | 1,204 | 0 |
| 617S | Cypress Av (6), Manhattan | 2,303 | 3,715 | 1,947 | 356 | 0 |
| F35N | Kings Hwy (F), Manhattan | 2,301 | 3,587 | 1,888 | 412 | 0 |
| L28N | East 105 St (L), Manhattan | 2,297 | 3,741 | 2,231 | 66 | 33 |
| B23S | Bay 50 St (D), Coney Island | 2,294 | 2,788 | 401 | 1,892 | 0 |
| 302N | 145 St (3), Harlem | 2,278 | 3,209 | 0 | 2,278 | 0 |
| A53S | Van Siclen Av (C), Outbound | 2,276 | 2,963 | 233 | 2,043 | 1 |
| L25S | Sutter Av (L), Canarsie | 2,270 | 3,550 | 479 | 1,791 | 260 |
| 614N | Longwood Av (6), Northbound | 2,254 | 3,115 | 515 | 1,739 | 0 |
| J28N | Chauncey St (J,Z), Outbound | 2,218 | 3,219 | 956 | 1,262 | 0 |
| J21S | Norwood Av (J,Z), Manhattan | 2,214 | 3,584 | 1,753 | 461 | 0 |
| F33N | Avenue N (F), Manhattan | 2,205 | 3,216 | 1,885 | 320 | 0 |
| J21N | Norwood Av (J,Z), Outbound | 2,203 | 3,580 | 452 | 1,751 | 0 |
| J14N | 104 St (J,Z), Jamaica | 2,197 | 2,815 | 1,179 | 1,018 | 0 |
| A54N | Shepherd Av (C), Manhattan | 2,196 | 3,566 | 1,746 | 450 | 4 |
| 206S | 225 St (2,5), Manhattan | 2,174 | 3,977 | 2,098 | 76 | 0 |
| 505S | Morris Park (5), Manhattan | 2,170 | 2,723 | 2,097 | 73 | 0 |
| 301N | Harlem-148 St (3), Last Stop | 2,159 | 3,501 | 0 | 2,159 | 0 |
| L28S | East 105 St (L), Canarsie | 2,151 | 3,499 | 53 | 2,098 | 33 |
| F34N | Avenue P (F), Manhattan | 2,149 | 2,779 | 1,818 | 332 | 0 |
| L24N | Atlantic Av (L), Manhattan | 2,149 | 1,741 | 1,646 | 503 | 127 |
| F35S | Kings Hwy (F), Southbound | 2,141 | 3,346 | 357 | 1,784 | 0 |
| D12S | 155 St (B,D), Downtown | 2,139 | 3,786 | 1,470 | 669 | 0 |
| L21N | Bushwick Av-Aberdeen St (L), Manhattan | 2,132 | 2,290 | 1,601 | 532 | 0 |
| 617N | Cypress Av (6), Northbound | 2,129 | 3,433 | 329 | 1,799 | 0 |
| F38N | Avenue X (F), Manhattan | 2,121 | 2,775 | 1,768 | 353 | 0 |
| 502S | Baychester Av (5), Manhattan | 2,117 | 4,054 | 2,099 | 18 | 0 |
| L24S | Atlantic Av (L), Canarsie | 2,093 | 1,713 | 580 | 1,512 | 127 |
| A11S | 155 St (C), Downtown | 2,078 | 3,044 | 1,797 | 280 | 0 |
| A52N | Liberty Av (C), Manhattan | 2,077 | 3,078 | 1,904 | 173 | 0 |
| M14S | Hewes St (J,M), Manhattan | 2,071 | 3,231 | 761 | 1,310 | 0 |
| J13S | 111 St (J), Manhattan | 2,060 | 1,290 | 1,018 | 1,042 | 3 |
| D12N | 155 St (B,D), The Bronx | 2,058 | 3,659 | 679 | 1,380 | 0 |
| 207S | 219 St (2,5), Manhattan | 2,054 | 3,541 | 1,960 | 95 | 0 |
| F33S | Avenue N (F), Southbound | 2,052 | 2,999 | 288 | 1,765 | 0 |
| G24S | 21 St (G), Brooklyn | 2,051 | 2,233 | 1,444 | 607 | 0 |
| 502N | Baychester Av (5), Eastchester | 2,036 | 3,900 | 18 | 2,018 | 0 |
| 204N | Nereid Av (2,5), Northbound | 2,035 | 3,468 | 46 | 1,989 | 92 |
| 206N | 225 St (2,5), Northbound | 2,034 | 3,721 | 69 | 1,965 | 0 |
| F34S | Avenue P (F), Southbound | 2,029 | 2,629 | 308 | 1,721 | 0 |
| N10N | 86 St (N), Manhattan | 2,016 | 2,387 | 1,786 | 230 | 2 |
| 505N | Morris Park (5), Eastchester | 2,012 | 2,527 | 73 | 1,940 | 0 |
| J12S | 121 St (J,Z), Manhattan | 2,012 | 2,536 | 1,099 | 913 | 0 |
| A52S | Liberty Av (C), Outbound | 1,993 | 2,957 | 168 | 1,825 | 0 |
| 107N | 215 St (1), The Bronx | 1,968 | 1,930 | 205 | 1,762 | 0 |
| 256N | Van Siclen Av (3), Manhattan | 1,968 | 3,145 | 1,968 | 0 | 143 |
| 209S | Burke Av (2,5), Manhattan | 1,958 | 3,513 | 1,830 | 128 | 0 |
| J22S | Cleveland St (J), Manhattan | 1,947 | 3,340 | 1,470 | 478 | 2 |
| F38S | Avenue X (F), Coney Island | 1,946 | 2,555 | 289 | 1,657 | 0 |
| J13N | 111 St (J), Jamaica | 1,930 | 1,211 | 996 | 934 | 3 |
| J22N | Cleveland St (J), Outbound | 1,922 | 3,307 | 481 | 1,441 | 2 |
| N10S | 86 St (N), Coney Island | 1,893 | 2,238 | 198 | 1,695 | 9 |
| A11N | 155 St (C), Uptown | 1,880 | 2,757 | 210 | 1,670 | 0 |
| A54S | Shepherd Av (C), Outbound | 1,880 | 3,053 | 310 | 1,570 | 4 |
| 256S | Van Siclen Av (3), New Lots | 1,870 | 2,987 | 0 | 1,870 | 143 |
| 107S | 215 St (1), Downtown | 1,856 | 1,816 | 1,689 | 167 | 0 |
| J12N | 121 St (J,Z), Jamaica | 1,855 | 2,332 | 852 | 1,003 | 0 |
| 207N | 219 St (2,5), Northbound | 1,850 | 3,189 | 90 | 1,761 | 0 |
| 606S | Zerega Av (6), Manhattan | 1,834 | 2,784 | 1,719 | 115 | 0 |
| 212S | Bronx Park East (2,5), Manhattan | 1,831 | 2,734 | 1,586 | 246 | 0 |
| J24N | Alabama Av (J,Z), Outbound | 1,800 | 2,431 | 956 | 844 | 1 |
| 209N | Burke Av (2,5), Northbound | 1,780 | 3,176 | 85 | 1,695 | 0 |
| L21S | Bushwick Av-Aberdeen St (L), Outbound | 1,777 | 1,900 | 344 | 1,433 | 0 |
| 212N | Bronx Park East (2,5), Northbound | 1,746 | 2,604 | 234 | 1,512 | 0 |
| 606N | Zerega Av (6), Pelham Bay | 1,705 | 2,583 | 103 | 1,603 | 0 |
| A64N | 111 St (A), Manhattan | 1,688 | 2,737 | 1,688 | 0 | 0 |
| F36N | Avenue U (F), Manhattan | 1,679 | 2,091 | 1,376 | 303 | 0 |
| H06N | Beach 67 St (A), Manhattan | 1,640 | 3,479 | 1,463 | 178 | 0 |
| A64S | 111 St (A), Ozone Park | 1,633 | 2,648 | 0 | 1,633 | 0 |
| J24S | Alabama Av (J,Z), Manhattan | 1,626 | 2,193 | 792 | 834 | 35 |
| 616S | E 143 St-St Mary's St (6), Manhattan | 1,624 | 1,210 | 1,332 | 292 | 0 |
| 603S | Middletown Rd (6), Manhattan | 1,613 | 2,194 | 1,546 | 68 | 0 |
| H06S | Beach 67 St (A), Far Rockaway | 1,562 | 3,295 | 152 | 1,410 | 0 |
| 616N | E 143 St-St Mary's St (6), Northbound | 1,561 | 1,163 | 271 | 1,290 | 0 |
| B15N | 55 St (D), Manhattan | 1,547 | 2,234 | 1,071 | 476 | 0 |
| F36S | Avenue U (F), Coney Island | 1,536 | 1,924 | 243 | 1,293 | 0 |
| S03S | Park Pl (S), Prospect Park | 1,514 | 1,854 | 1,044 | 470 | 0 |
| 603N | Middletown Rd (6), Pelham Bay | 1,487 | 2,018 | 56 | 1,431 | 0 |
| B15S | 55 St (D), Southbound | 1,480 | 2,145 | 461 | 1,019 | 0 |
| A63N | 104 St (A), Manhattan | 1,426 | 1,925 | 1,396 | 29 | 0 |
| A63S | 104 St (A), Ozone Park | 1,360 | 1,837 | 29 | 1,331 | 0 |
| F39N | Neptune Av (F), Manhattan | 1,349 | 1,686 | 995 | 353 | 0 |
| 612S | Whitlock Av (6), Manhattan | 1,335 | 1,973 | 1,153 | 182 | 0 |
| 612N | Whitlock Av (6), Northbound | 1,327 | 1,972 | 208 | 1,119 | 0 |
| G24N | 21 St (G), Court Square | 1,303 | 1,409 | 191 | 1,112 | 0 |
| S03N | Park Pl (S), Franklin Av | 1,281 | 1,572 | 393 | 888 | 0 |
| H07N | Beach 60 St (A), Manhattan | 1,259 | 3,312 | 1,100 | 159 | 0 |
| F31S | Avenue I (F), Southbound | 1,231 | 2,064 | 338 | 894 | 0 |
| F31N | Avenue I (F), Manhattan | 1,222 | 2,050 | 900 | 322 | 0 |
| H07S | Beach 60 St (A), Far Rockaway | 1,154 | 3,020 | 134 | 1,020 | 0 |
| F39S | Neptune Av (F), Coney Island | 1,130 | 1,412 | 240 | 891 | 0 |
| H10N | Beach 25 St (A), Manhattan | 1,110 | 2,878 | 1,032 | 78 | 0 |
| H01N | Aqueduct Racetrack (A), Manhattan | 1,050 | 3,402 | 501 | 550 | 0 |
| H10S | Beach 25 St (A), Far Rockaway | 1,018 | 2,634 | 67 | 950 | 0 |
| J19S | Cypress Hills (J), Manhattan | 940 | 2,329 | 606 | 334 | 4 |
| J19N | Cypress Hills (J), Queens | 939 | 2,327 | 353 | 586 | 4 |
| H02N | Aqueduct-N Conduit Av (A), Manhattan | 915 | 1,669 | 837 | 78 | 208 |
| F32N | Bay Pkwy (F), Manhattan | 914 | 1,333 | 741 | 173 | 0 |
| H02S | Aqueduct-N Conduit Av (A), Rockaways | 890 | 1,637 | 76 | 814 | 208 |
| F32S | Bay Pkwy (F), Southbound | 861 | 1,259 | 151 | 709 | 0 |
| H15N | Rockaway Park-Beach 116 St (A,S), Inbound | 616 | 1,003 | 616 | 0 | 0 |
| H09N | Beach 36 St (A), Manhattan | 579 | 1,619 | 536 | 44 | 0 |
| H12N | Beach 90 St (A,S), Inbound | 560 | 1,341 | 537 | 23 | 0 |
| H12S | Beach 90 St (A,S), Rockaway Park | 560 | 1,336 | 17 | 543 | 0 |
| H08N | Beach 44 St (A), Manhattan | 542 | 1,165 | 475 | 66 | 0 |
| H09S | Beach 36 St (A), Far Rockaway | 516 | 1,413 | 28 | 488 | 0 |
| H15S | Rockaway Park-Beach 116 St (A,S), Last Stop | 491 | 799 | 0 | 491 | 0 |
| H08S | Beach 44 St (A), Far Rockaway | 482 | 1,033 | 54 | 427 | 0 |
| H13N | Beach 98 St (A,S), Inbound | 321 | 682 | 308 | 13 | 0 |
| H13S | Beach 98 St (A,S), Rockaway Park | 298 | 632 | 9 | 289 | 0 |
| H14N | Beach 105 St (A,S), Inbound | 216 | 330 | 212 | 4 | 0 |
| H14S | Beach 105 St (A,S), Rockaway Park | 204 | 310 | 0 | 204 | 0 |
