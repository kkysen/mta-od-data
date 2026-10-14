# Ridership by platform

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
Each scaled column scales the OD data to a year's counted station entries.

Produced by `mta-od-data ridership --by platform --markdown-out src/mta_od_data/ridership/by_platform.md`.

| platform | name | on + off, scaled to 2025 | on + off, scaled to 2019 | on, scaled to 2025 | off, scaled to 2025 | transfers on + off, scaled to 2025 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 631N | Grand Central-42 St (4 5 6), Uptown | 180,333 | 235,680 | 82,343 | 97,990 | 97,582 |
| 631S | Grand Central-42 St (4 5 6), Downtown | 171,861 | 224,037 | 91,486 | 80,376 | 88,144 |
| 127N | Times Sq-42 St (1 2 3), Uptown | 160,482 | 210,961 | 87,645 | 72,837 | 114,694 |
| 127S | Times Sq-42 St (1 2 3), Downtown | 157,611 | 208,181 | 72,146 | 85,465 | 116,199 |
| 635N | 14 St-Union Sq (4 5 6), Uptown | 135,850 | 174,311 | 85,107 | 50,743 | 96,686 |
| 635S | 14 St-Union Sq (4 5 6), Downtown | 127,773 | 164,350 | 40,789 | 86,983 | 88,873 |
| G14S | Jackson Hts-Roosevelt Av (E F M R), Manhattan | 120,893 | 142,197 | 82,508 | 38,385 | 78,519 |
| R16S | Times Sq-42 St (N Q R W), Downtown | 118,267 | 151,931 | 65,052 | 53,215 | 72,489 |
| A27S | 42 St-Port Authority Bus Terminal (A C E), Downtown | 115,251 | 150,830 | 49,935 | 65,316 | 65,863 |
| G14N | Jackson Hts-Roosevelt Av (E F M R), Outbound | 112,239 | 132,819 | 38,645 | 73,594 | 72,775 |
| R16N | Times Sq-42 St (N Q R W), Uptown | 102,834 | 131,690 | 45,376 | 57,458 | 60,731 |
| A27N | 42 St-Port Authority Bus Terminal (A C E), Uptown | 100,659 | 130,774 | 59,573 | 41,086 | 53,223 |
| R20S | 14 St-Union Sq (N Q R W), Downtown | 95,027 | 121,446 | 43,203 | 51,824 | 60,896 |
| D16S | 42 St-Bryant Pk (B D F M), Downtown | 92,580 | 119,305 | 47,534 | 45,046 | 56,574 |
| A24N | 59 St-Columbus Circle (A C B D), Uptown | 91,525 | 122,009 | 38,279 | 53,246 | 51,560 |
| A24S | 59 St-Columbus Circle (A C B D), Downtown | 90,384 | 118,142 | 53,918 | 36,466 | 50,111 |
| D21N | Broadway-Lafayette St (B D F M), Uptown | 89,321 | 111,560 | 36,169 | 53,152 | 64,743 |
| R20N | 14 St-Union Sq (N Q R W), Uptown | 88,180 | 112,700 | 50,216 | 37,964 | 56,675 |
| D17N | 34 St-Herald Sq (B D F M), Uptown | 87,659 | 123,251 | 48,417 | 39,242 | 38,370 |
| 629S | 59 St (4 5 6), Downtown | 86,476 | 112,672 | 41,612 | 44,864 | 58,729 |
| 629N | 59 St (4 5 6), Uptown | 82,590 | 107,585 | 37,867 | 44,723 | 51,429 |
| L03S | 14 St-Union Sq (L), Brooklyn | 78,944 | 90,061 | 62,146 | 16,798 | 62,476 |
| 132N | 14 St (1 2 3), Uptown | 78,834 | 101,298 | 46,323 | 32,511 | 61,284 |
| L03N | 14 St-Union Sq (L), West Side | 77,865 | 89,493 | 17,304 | 60,562 | 61,010 |
| D20S | W 4 St-Wash Sq (B D F M), Downtown | 75,554 | 94,306 | 36,857 | 38,697 | 49,966 |
| A41N | Jay St-MetroTech (A C F), Manhattan | 75,062 | 100,931 | 38,549 | 36,513 | 48,755 |
| 123S | 72 St (1 2 3), Downtown | 74,001 | 95,739 | 45,721 | 28,281 | 40,011 |
| 123N | 72 St (1 2 3), Uptown | 73,494 | 94,585 | 27,366 | 46,128 | 39,390 |
| D17S | 34 St-Herald Sq (B D F M), Downtown | 73,246 | 104,139 | 29,752 | 43,494 | 26,256 |
| R17N | 34 St-Herald Sq (N Q R W), Uptown | 72,312 | 100,553 | 34,812 | 37,501 | 29,796 |
| R31N | Atlantic Av-Barclays Ctr (D N R), Manhattan | 72,024 | 89,320 | 25,701 | 46,323 | 58,108 |
| R17S | 34 St-Herald Sq (N Q R W), Downtown | 71,861 | 100,901 | 38,661 | 33,200 | 24,476 |
| R31S | Atlantic Av-Barclays Ctr (D N R), Southbound | 70,962 | 87,621 | 42,866 | 28,096 | 55,699 |
| 621S | 125 St (4 5 6), Downtown | 70,331 | 101,475 | 31,403 | 38,928 | 50,155 |
| A28N | 34 St-Penn Station (A C E), Uptown | 69,779 | 89,084 | 40,911 | 28,868 | 17 |
| A28S | 34 St-Penn Station (A C E), Downtown | 69,194 | 88,167 | 30,401 | 38,792 | 17 |
| 132S | 14 St (1 2 3), Downtown | 68,333 | 87,746 | 28,441 | 39,892 | 50,553 |
| 725N | Times Sq-42 St (7), Queens | 67,175 | 79,580 | 56,558 | 10,617 | 50,658 |
| A41S | Jay St-MetroTech (A C F), Outbound | 65,100 | 88,049 | 31,619 | 33,481 | 39,999 |
| 725S | Times Sq-42 St (7), Hudson Yards | 62,800 | 73,821 | 10,785 | 52,014 | 47,503 |
| B08S | Lexington Av/63 St (M Q), Downtown | 62,224 | 80,021 | 19,522 | 42,702 | 47,006 |
| D16N | 42 St-Bryant Pk (B D F M), Uptown | 62,055 | 80,032 | 28,911 | 33,144 | 27,159 |
| 723N | Grand Central-42 St (7), Queens | 61,644 | 74,066 | 32,406 | 29,239 | 30,125 |
| B08N | Lexington Av/63 St (M Q), Uptown & Queens | 61,228 | 79,788 | 43,893 | 17,335 | 42,871 |
| 128S | 34 St-Penn Station (1 2 3), Downtown | 61,012 | 90,241 | 24,718 | 36,294 | 1 |
| 128N | 34 St-Penn Station (1 2 3), Uptown | 60,841 | 89,449 | 37,459 | 23,382 | 106 |
| 630S | 51 St (6), Downtown | 60,777 | 80,239 | 36,966 | 23,811 | 33,305 |
| F11S | Lexington Av/53 St (E F), Downtown | 60,353 | 78,953 | 20,077 | 40,276 | 35,159 |
| 630N | 51 St (6), Uptown | 58,860 | 77,641 | 25,941 | 32,919 | 32,207 |
| R11S | Lexington Av/59 St (N R W), Downtown | 58,121 | 73,326 | 19,607 | 38,514 | 41,633 |
| 235N | Atlantic Av-Barclays Ctr (2 3 4 5), Manhattan | 58,120 | 76,066 | 32,739 | 25,382 | 43,601 |
| 710S | 74 St-Broadway (7), Manhattan | 57,130 | 64,800 | 11,549 | 45,581 | 48,500 |
| 723S | Grand Central-42 St (7), Hudson Yards | 56,951 | 68,217 | 27,808 | 29,144 | 26,819 |
| D15S | 47-50 Sts-Rockefeller Ctr (B D F M), Downtown | 55,765 | 74,586 | 31,730 | 24,035 | 1,193 |
| 418N | Fulton St (4 5), Uptown | 55,279 | 76,386 | 45,181 | 10,098 | 21,461 |
| F11N | Lexington Av/53 St (E F), Queens | 55,270 | 72,801 | 33,931 | 21,339 | 30,281 |
| D20N | W 4 St-Wash Sq (B D F M), Uptown | 55,106 | 69,003 | 30,817 | 24,289 | 30,848 |
| 710N | 74 St-Broadway (7), Outbound | 54,849 | 62,753 | 40,817 | 14,032 | 45,507 |
| 418S | Fulton St (4 5), Downtown | 54,803 | 75,979 | 9,712 | 45,092 | 21,924 |
| 621N | 125 St (4 5 6), The Bronx | 54,520 | 78,442 | 31,531 | 22,989 | 35,230 |
| 626S | 86 St (4 5 6), Downtown | 54,069 | 65,287 | 36,134 | 17,935 | 14,755 |
| D15N | 47-50 Sts-Rockefeller Ctr (B D F M), Uptown | 53,671 | 71,953 | 22,026 | 31,645 | 25 |
| G08N | Forest Hills-71 Av (E F M R), Outbound | 53,249 | 71,035 | 13,429 | 39,821 | 30,768 |
| A31S | 14 St (A C E), Downtown | 52,924 | 62,723 | 15,364 | 37,560 | 24,462 |
| D21S | Broadway-Lafayette St (B D F M), Downtown | 52,816 | 63,948 | 33,342 | 19,474 | 27,763 |
| 718S | Queensboro Plaza (7), Manhattan | 52,384 | 60,983 | 18,177 | 34,207 | 45,683 |
| R11N | Lexington Av/59 St (N R W), Queens | 50,882 | 63,595 | 36,615 | 14,267 | 35,796 |
| 120S | 96 St (1 2 3), Downtown | 50,810 | 67,247 | 29,766 | 21,044 | 20,740 |
| 701S | Flushing-Main St (7), Manhattan | 50,754 | 59,545 | 50,754 | 0 | 0 |
| G08S | Forest Hills-71 Av (E F M R), Manhattan | 49,968 | 66,877 | 38,262 | 11,706 | 27,089 |
| 626N | 86 St (4 5 6), Uptown | 49,119 | 58,398 | 14,899 | 34,220 | 8,762 |
| A31N | 14 St (A C E), Uptown | 49,117 | 57,996 | 35,867 | 13,250 | 21,383 |
| A38N | Fulton St (A C), Uptown | 48,731 | 67,892 | 17,680 | 31,050 | 27,010 |
| 701N | Flushing-Main St (7), Last Stop | 48,216 | 56,607 | 0 | 48,216 | 0 |
| A32N | W 4 St-Wash Sq (A C E), Uptown | 47,254 | 60,666 | 23,821 | 23,433 | 30,748 |
| 235S | Atlantic Av-Barclays Ctr (2 3 4 5), Outbound | 46,916 | 61,830 | 25,447 | 21,469 | 33,464 |
| A32S | W 4 St-Wash Sq (A C E), Downtown | 46,253 | 58,084 | 19,436 | 26,816 | 29,411 |
| L02N | 6 Av (L), West Side | 44,250 | 51,464 | 6,181 | 38,069 | 34,344 |
| A38S | Fulton St (A C), Brooklyn | 43,981 | 61,436 | 27,853 | 16,128 | 21,437 |
| 125N | 59 St-Columbus Circle (1), Uptown | 43,667 | 57,284 | 21,396 | 22,271 | 18,894 |
| 125S | 59 St-Columbus Circle (1), Downtown | 43,332 | 56,985 | 19,450 | 23,882 | 23,324 |
| A15S | 125 St (A C B D), Downtown | 42,918 | 60,625 | 26,382 | 16,536 | 22,001 |
| R36N | 36 St (D N R), Manhattan | 42,772 | 49,765 | 25,124 | 17,647 | 29,106 |
| L02S | 6 Av (L), Brooklyn | 41,358 | 47,800 | 36,623 | 4,735 | 31,142 |
| D19N | 14 St (F M), Uptown | 41,137 | 50,603 | 21,684 | 19,454 | 28,517 |
| A15N | 125 St (A C B D), Uptown | 40,954 | 57,139 | 15,593 | 25,361 | 19,478 |
| D14N | 7 Av (E B D), Outbound | 40,896 | 51,913 | 28,643 | 12,252 | 23,645 |
| D14S | 7 Av (E B D), Downtown | 40,702 | 51,521 | 11,957 | 28,746 | 24,630 |
| 239N | Franklin Av-Medgar Evers College (2 3 4 5), Manhattan | 39,695 | 53,576 | 21,131 | 18,565 | 27,668 |
| A42S | Hoyt-Schermerhorn Sts (A C G), Queens | 38,735 | 47,911 | 14,300 | 24,435 | 27,519 |
| R09S | Queensboro Plaza (N W), Manhattan | 37,897 | 44,478 | 26,067 | 11,830 | 32,741 |
| D19S | 14 St (F M), Downtown | 37,865 | 46,495 | 15,487 | 22,378 | 24,690 |
| 718N | Queensboro Plaza (7), Outbound | 37,322 | 43,680 | 25,167 | 12,155 | 29,603 |
| 120N | 96 St (1 2 3), Uptown | 37,089 | 48,553 | 14,041 | 23,049 | 7,244 |
| L01N | 8 Av (L), Last Stop | 36,516 | 41,468 | 0 | 36,516 | 21,852 |
| 640N | Brooklyn Bridge-City Hall (4 5 6), Uptown | 36,377 | 51,016 | 27,186 | 9,192 | 14,914 |
| 724S | 5 Av (7), Hudson Yards | 35,878 | 44,501 | 11,156 | 24,722 | 20,219 |
| 637N | Bleecker St (6), Uptown | 35,786 | 44,056 | 29,872 | 5,914 | 22,093 |
| A42N | Hoyt-Schermerhorn Sts (A C G), Westbound | 35,681 | 44,144 | 22,771 | 12,910 | 25,359 |
| R09N | Queensboro Plaza (N W), Astoria | 35,341 | 41,325 | 11,755 | 23,586 | 30,364 |
| 901N | Grand Central-42 St (S), Times Square | 34,902 | 46,262 | 34,902 | 0 | 14,700 |
| 902N | Times Sq-42 St (S), Last Stop | 34,902 | 46,262 | 0 | 34,902 | 23,308 |
| 637S | Bleecker St (6), Downtown | 34,890 | 42,455 | 5,640 | 29,249 | 21,410 |
| 724N | 5 Av (7), Queens | 34,790 | 42,984 | 24,023 | 10,767 | 18,970 |
| R14N | 57 St-7 Av (N Q R W), Uptown | 34,432 | 43,805 | 16,009 | 18,423 | 2,182 |
| F06S | Kew Gardens-Union Tpke (E F), Manhattan | 34,148 | 46,850 | 23,867 | 10,281 | 14,727 |
| R14S | 57 St-7 Av (N Q R W), Downtown | 33,868 | 42,918 | 17,062 | 16,806 | 4,116 |
| R30S | DeKalb Av (B Q R), Southbound | 33,843 | 42,826 | 15,257 | 18,586 | 13,771 |
| G06S | Sutphin Blvd-Archer Av-JFK Airport (E J Z), Manhattan | 33,812 | 36,424 | 33,731 | 81 | 7,564 |
| L01S | 8 Av (L), Brooklyn | 33,773 | 38,196 | 33,773 | 0 | 20,559 |
| 137N | Chambers St (1 2 3), Uptown | 33,247 | 43,865 | 18,117 | 15,130 | 16,556 |
| 239S | Franklin Av-Medgar Evers College (2 3 4 5), Outbound | 33,112 | 44,832 | 15,073 | 18,039 | 21,278 |
| R36S | 36 St (D N R), Southbound | 32,056 | 36,865 | 12,187 | 19,869 | 18,466 |
| L08N | Bedford Av (L), Manhattan | 31,800 | 28,259 | 23,838 | 7,962 | 0 |
| Q01N | Canal St (N Q), Uptown | 31,626 | 40,392 | 18,258 | 13,369 | 10,379 |
| L08S | Bedford Av (L), Outbound | 31,041 | 27,701 | 6,795 | 24,246 | 0 |
| G22S | Court Sq (G), Brooklyn | 30,654 | 34,957 | 30,654 | 0 | 27,439 |
| Q01S | Canal St (N Q), Downtown | 30,580 | 39,316 | 11,332 | 19,247 | 9,184 |
| A51N | Broadway Junction (A C), Manhattan | 30,443 | 42,330 | 20,820 | 9,622 | 27,073 |
| R30N | DeKalb Av (B Q R), Manhattan | 30,204 | 37,920 | 16,639 | 13,565 | 10,556 |
| R41N | 59 St (N R), Manhattan | 30,145 | 34,756 | 17,376 | 12,769 | 18,665 |
| 640S | Brooklyn Bridge-City Hall (4 5 6), Downtown | 30,055 | 42,397 | 6,443 | 23,612 | 10,365 |
| A51S | Broadway Junction (A C), Outbound | 29,901 | 41,255 | 8,749 | 21,153 | 26,578 |
| D24N | Atlantic Av-Barclays Ctr (B Q), Manhattan | 29,841 | 39,704 | 10,747 | 19,094 | 22,709 |
| G22N | Court Sq (G), Last Stop | 29,635 | 33,796 | 0 | 29,635 | 26,195 |
| L10N | Lorimer St (L), Manhattan | 29,512 | 32,003 | 18,988 | 10,524 | 19,231 |
| F09S | Court Sq-23 St (E F), Manhattan | 29,283 | 34,785 | 16,923 | 12,360 | 16,830 |
| L10S | Lorimer St (L), Outbound | 29,236 | 31,725 | 10,864 | 18,372 | 18,373 |
| 901S | Grand Central-42 St (S), Last Stop | 29,180 | 38,586 | 0 | 29,180 | 13,806 |
| 902S | Times Sq-42 St (S), Grand Central | 29,180 | 38,586 | 29,180 | 0 | 17,432 |
| F09N | Court Sq-23 St (E F), Outbound | 29,121 | 34,820 | 10,477 | 18,644 | 16,656 |
| G06N | Sutphin Blvd-Archer Av-JFK Airport (E J Z), Jamaica | 29,088 | 32,189 | 708 | 28,380 | 8,805 |
| G05S | Jamaica Center-Parsons/Archer (E J Z), Manhattan | 28,973 | 41,831 | 28,973 | 0 | 4,526 |
| 250N | Crown Hts-Utica Av (3 4), Manhattan | 28,761 | 40,864 | 22,516 | 6,245 | 10,016 |
| Q03S | 72 St (Q), Downtown | 27,671 | 33,590 | 26,782 | 888 | 192 |
| Q03N | 72 St (Q), Uptown | 27,639 | 33,566 | 770 | 26,870 | 192 |
| R29N | Jay St-MetroTech (R), Manhattan | 27,504 | 35,998 | 7,502 | 20,001 | 20,889 |
| D24S | Atlantic Av-Barclays Ctr (B Q), Southbound | 27,317 | 36,064 | 14,816 | 12,500 | 17,785 |
| 222N | 149 St-Hostos (2 5), Northbound | 27,102 | 40,279 | 15,251 | 11,851 | 22,618 |
| 137S | Chambers St (1 2 3), Downtown | 26,815 | 35,746 | 11,358 | 15,458 | 10,076 |
| G05N | Jamaica Center-Parsons/Archer (E J Z), Last Stop | 26,768 | 38,608 | 0 | 26,768 | 4,526 |
| A09S | 168 St (A C), Downtown | 26,748 | 33,659 | 23,171 | 3,577 | 13,425 |
| 707S | Junction Blvd (7), Manhattan | 26,144 | 26,065 | 21,839 | 4,304 | 3,248 |
| R15S | 49 St (N R W), Downtown | 26,045 | 27,495 | 17,619 | 8,426 | 0 |
| 726S | 34 St-Hudson Yards (7), Queens | 25,921 | 21,612 | 0 | 25,921 | 0 |
| D18N | 23 St (F M), Uptown | 25,601 | 33,239 | 14,602 | 10,998 | 0 |
| R15N | 49 St (N R W), Uptown | 25,591 | 27,001 | 7,988 | 17,604 | 0 |
| 726N | 34 St-Hudson Yards (7), Last Stop | 25,436 | 21,194 | 25,436 | 0 | 0 |
| L06S | 1 Av (L), Brooklyn | 25,337 | 20,858 | 8,577 | 16,760 | 0 |
| 229N | Fulton St (2 3), Uptown | 25,235 | 35,371 | 16,501 | 8,734 | 10,850 |
| 414N | 161 St-Yankee Stadium (4), Northbound | 24,957 | 35,493 | 7,072 | 17,885 | 13,680 |
| R29S | Jay St-MetroTech (R), Southbound | 24,955 | 32,822 | 17,949 | 7,006 | 18,868 |
| 627S | 77 St (6), Downtown | 24,819 | 28,256 | 20,041 | 4,778 | 16 |
| 707N | Junction Blvd (7), Outbound | 24,811 | 24,360 | 3,906 | 20,905 | 2,079 |
| L17N | Myrtle-Wyckoff Avs (L), Manhattan | 24,527 | 26,980 | 19,922 | 4,605 | 8,354 |
| 719N | Court Sq (7), Outbound | 24,426 | 27,305 | 15,815 | 8,611 | 16,568 |
| 627N | 77 St (6), Uptown | 24,358 | 27,701 | 4,422 | 19,936 | 16 |
| 634N | 23 St-Baruch College (6), Uptown | 24,349 | 34,012 | 13,479 | 10,870 | 0 |
| A09N | 168 St (A C), Uptown | 24,330 | 30,515 | 3,525 | 20,805 | 10,939 |
| D18S | 23 St (F M), Downtown | 24,096 | 31,142 | 9,987 | 14,110 | 0 |
| L17S | Myrtle-Wyckoff Avs (L), Outbound | 24,002 | 26,494 | 4,824 | 19,178 | 8,535 |
| A36S | Chambers St (A C), Brooklyn | 23,942 | 35,288 | 10,738 | 13,204 | 5,556 |
| 126N | 50 St (1), Uptown | 23,896 | 30,904 | 10,134 | 13,762 | 0 |
| D35N | Kings Hwy (B Q), Manhattan | 23,868 | 30,796 | 16,861 | 7,007 | 7,372 |
| 632S | 33 St (6), Downtown | 23,788 | 32,644 | 9,587 | 14,201 | 1 |
| 222S | 149 St-Hostos (2 5), Manhattan | 23,546 | 35,058 | 9,589 | 13,957 | 19,038 |
| 234S | Nevins St (2 3 4 5), Outbound | 23,523 | 31,607 | 10,669 | 12,855 | 15,705 |
| G29S | Metropolitan Av (G), Southbound | 23,436 | 25,673 | 11,396 | 12,040 | 18,865 |
| 634S | 23 St-Baruch College (6), Downtown | 23,389 | 32,703 | 10,137 | 13,252 | 0 |
| 632N | 33 St (6), Uptown | 23,383 | 32,146 | 14,059 | 9,324 | 1 |
| 719S | Court Sq (7), Manhattan | 23,380 | 25,919 | 8,814 | 14,566 | 15,705 |
| G29N | Metropolitan Av (G), Queens | 23,303 | 25,501 | 11,181 | 12,122 | 18,739 |
| M18S | Delancey St-Essex St (M J Z), Inbound | 23,250 | 27,858 | 10,527 | 12,723 | 9,086 |
| L06N | 1 Av (L), West Side | 23,176 | 19,153 | 15,339 | 7,837 | 0 |
| 228S | Park Place (2 3), Brooklyn | 23,115 | 33,337 | 6,044 | 17,072 | 6,833 |
| A25N | 50 St (C E), Uptown | 23,071 | 26,916 | 10,977 | 12,095 | 2,477 |
| 229S | Fulton St (2 3), Brooklyn | 22,963 | 32,701 | 8,130 | 14,833 | 7,270 |
| 628S | 68 St-Hunter College (6), Downtown | 22,895 | 27,336 | 17,033 | 5,862 | 86 |
| L22N | Broadway Junction (L), Manhattan | 22,827 | 30,121 | 13,756 | 9,072 | 20,968 |
| F15S | Delancey St-Essex St (F), Brooklyn | 22,795 | 26,841 | 7,257 | 15,537 | 8,694 |
| A25S | 50 St (C E), Downtown | 22,633 | 26,445 | 11,780 | 10,853 | 2,850 |
| 628N | 68 St-Hunter College (6), Uptown | 22,393 | 26,676 | 5,049 | 17,344 | 86 |
| A36N | Chambers St (A C), Uptown | 22,325 | 33,074 | 11,570 | 10,754 | 2,983 |
| M18N | Delancey St-Essex St (M J Z), Brooklyn | 22,319 | 27,452 | 13,645 | 8,674 | 11,177 |
| 414S | 161 St-Yankee Stadium (4), Manhattan | 22,238 | 31,367 | 15,394 | 6,844 | 11,641 |
| J27S | Broadway Junction (J Z), Manhattan | 22,204 | 30,198 | 7,340 | 14,864 | 21,094 |
| M11N | Myrtle Av (M J Z), Outbound | 22,194 | 28,823 | 12,520 | 9,674 | 11,641 |
| G21S | Queens Plaza (E F R), Manhattan | 22,126 | 24,972 | 13,766 | 8,360 | 7,087 |
| Q04S | 86 St (Q), Downtown | 21,966 | 28,184 | 21,966 | 0 | 53 |
| 415S | 149 St-Hostos (4), Manhattan | 21,873 | 32,379 | 10,935 | 10,938 | 16,924 |
| 250S | Crown Hts-Utica Av (3 4), Outbound | 21,859 | 30,990 | 3,543 | 18,317 | 4,998 |
| D22S | Grand St (B D), Brooklyn | 21,728 | 28,030 | 7,518 | 14,209 | 0 |
| M11S | Myrtle Av (M J Z), Manhattan | 21,649 | 28,170 | 9,594 | 12,055 | 11,927 |
| 126S | 50 St (1), Downtown | 21,617 | 28,209 | 12,445 | 9,172 | 0 |
| Q04N | 86 St (Q), Uptown | 21,513 | 27,619 | 0 | 21,513 | 53 |
| A34N | Canal St (A C E), Uptown | 21,480 | 31,111 | 13,464 | 8,016 | 5,852 |
| F15N | Delancey St-Essex St (F), Uptown | 21,384 | 24,799 | 12,764 | 8,620 | 7,193 |
| D11N | 161 St-Yankee Stadium (B D), Northbound | 21,258 | 31,003 | 7,984 | 13,274 | 13,525 |
| F06N | Kew Gardens-Union Tpke (E F), Jamaica | 21,186 | 29,941 | 3,837 | 17,349 | 2,569 |
| D22N | Grand St (B D), Uptown | 20,979 | 27,077 | 13,282 | 7,696 | 201 |
| L22S | Broadway Junction (L), Outbound | 20,960 | 27,750 | 8,667 | 12,293 | 19,131 |
| D35S | Kings Hwy (B Q), Southbound | 20,938 | 26,975 | 5,708 | 15,230 | 4,719 |
| D13S | 145 St (B D), Downtown | 20,890 | 30,278 | 9,892 | 10,998 | 12,170 |
| 415N | 149 St-Hostos (4), Northbound | 20,870 | 30,984 | 10,962 | 9,908 | 16,117 |
| R41S | 59 St (N R), Southbound | 20,484 | 22,737 | 8,169 | 12,315 | 9,402 |
| A12S | 145 St (A C), Downtown | 20,455 | 28,614 | 12,505 | 7,950 | 10,499 |
| D11S | 161 St-Yankee Stadium (B D), Manhattan | 20,330 | 29,259 | 14,076 | 6,254 | 11,796 |
| J27N | Broadway Junction (J Z), Outbound | 20,285 | 27,764 | 14,001 | 6,284 | 19,275 |
| 228N | Park Place (2 3), Uptown | 20,107 | 29,171 | 15,131 | 4,976 | 4,067 |
| G21N | Queens Plaza (E F R), Outbound | 19,636 | 21,832 | 7,025 | 12,611 | 4,543 |
| F12N | 5 Av/53 St (E F), Queens | 19,145 | 33,308 | 6,714 | 12,431 | 1,528 |
| 234N | Nevins St (2 3 4 5), Manhattan | 19,086 | 25,520 | 10,579 | 8,507 | 10,932 |
| D43N | Coney Island-Stillwell Av (D F N Q), Manhattan | 18,992 | 23,510 | 18,992 | 0 | 8,178 |
| A30N | 23 St (C E), Uptown | 18,849 | 26,094 | 10,605 | 8,245 | 0 |
| 124S | 66 St-Lincoln Center (1), Downtown | 18,826 | 26,170 | 12,690 | 6,136 | 0 |
| R33N | 4 Av-9 St (R), Manhattan | 18,690 | 22,448 | 8,970 | 9,721 | 13,245 |
| R19N | 23 St (R W), Uptown | 18,643 | 28,037 | 10,531 | 8,111 | 0 |
| 639N | Canal St (6), Uptown | 18,576 | 24,411 | 15,613 | 2,963 | 8,293 |
| 221S | 3 Av-149 St (2 5), Manhattan | 18,550 | 27,424 | 14,081 | 4,469 | 2,959 |
| 706S | 103 St-Corona Plaza (7), Manhattan | 18,391 | 19,768 | 16,789 | 1,602 | 0 |
| A30S | 23 St (C E), Downtown | 18,384 | 25,439 | 7,781 | 10,603 | 0 |
| 124N | 66 St-Lincoln Center (1), Uptown | 18,205 | 25,355 | 5,522 | 12,683 | 0 |
| A34S | Canal St (A C E), Downtown | 18,182 | 26,574 | 5,872 | 12,309 | 2,158 |
| F23N | 4 Av-9 St (F G), Northbound | 18,145 | 21,594 | 12,813 | 5,332 | 12,646 |
| 420N | Bowling Green (4 5), Uptown | 18,054 | 30,726 | 13,640 | 4,413 | 50 |
| D43S | Coney Island-Stillwell Av (D F N Q), Last Stop | 18,023 | 22,345 | 0 | 18,023 | 8,178 |
| F12S | 5 Av/53 St (E F), Downtown | 17,730 | 31,436 | 11,296 | 6,434 | 59 |
| 420S | Bowling Green (4 5), Downtown | 17,694 | 30,146 | 4,141 | 13,553 | 0 |
| 633N | 28 St (6), Uptown | 17,360 | 20,979 | 10,243 | 7,116 | 2 |
| 712S | 61 St-Woodside (7), Manhattan | 17,325 | 21,714 | 11,796 | 5,529 | 2,383 |
| 712N | 61 St-Woodside (7), Outbound | 17,241 | 21,590 | 5,643 | 11,598 | 2,383 |
| 633S | 28 St (6), Downtown | 17,186 | 20,754 | 7,063 | 10,123 | 2 |
| 708S | 90 St-Elmhurst Av (7), Manhattan | 16,996 | 18,030 | 13,351 | 3,645 | 0 |
| A48N | Utica Av (A C), Manhattan | 16,977 | 23,666 | 12,803 | 4,174 | 4,769 |
| 112S | 168 St-Washington Hts (1), Downtown | 16,903 | 22,117 | 7,262 | 9,641 | 11,166 |
| G11S | Woodhaven Blvd (M R), Manhattan | 16,721 | 22,769 | 13,134 | 3,587 | 0 |
| R19S | 23 St (R W), Downtown | 16,666 | 25,014 | 6,656 | 10,010 | 0 |
| 230S | Wall St (2 3), Brooklyn | 16,471 | 26,843 | 3,310 | 13,161 | 0 |
| 706N | 103 St-Corona Plaza (7), Outbound | 16,303 | 17,585 | 1,181 | 15,122 | 0 |
| 221N | 3 Av-149 St (2 5), Northbound | 16,288 | 24,371 | 3,739 | 12,549 | 809 |
| G12S | Grand Av-Newtown (M R), Manhattan | 16,196 | 19,574 | 13,966 | 2,231 | 0 |
| G12N | Grand Av-Newtown (M R), Outbound | 16,094 | 19,462 | 2,180 | 13,914 | 0 |
| 721S | Vernon Blvd-Jackson Av (7), Manhattan | 16,081 | 17,020 | 11,927 | 4,154 | 0 |
| 230N | Wall St (2 3), Uptown | 16,037 | 26,094 | 12,579 | 3,458 | 0 |
| F14S | 2 Av (F), Downtown | 15,925 | 20,000 | 4,027 | 11,898 | 0 |
| A48S | Utica Av (A C), Outbound | 15,921 | 22,289 | 3,860 | 12,061 | 4,130 |
| 138N | WTC Cortlandt (1), Uptown | 15,854 | 15,617 | 14,964 | 890 | 0 |
| F23S | 4 Av-9 St (F G), Southbound | 15,841 | 18,909 | 4,727 | 11,114 | 9,991 |
| R21S | 8 St-NYU (R W), Downtown | 15,806 | 19,943 | 3,153 | 12,653 | 0 |
| 138S | WTC Cortlandt (1), Downtown | 15,710 | 15,538 | 1,067 | 14,643 | 0 |
| G11N | Woodhaven Blvd (M R), Outbound | 15,682 | 21,327 | 2,997 | 12,684 | 0 |
| A46S | Nostrand Av (A C), Outbound | 15,664 | 19,847 | 3,512 | 12,153 | 983 |
| Q05S | 96 St (Q), Downtown | 15,577 | 20,963 | 15,577 | 0 | 0 |
| 423N | Borough Hall (4 5), Manhattan | 15,455 | 23,946 | 8,446 | 7,009 | 1,566 |
| 721N | Vernon Blvd-Jackson Av (7), Outbound | 15,415 | 16,350 | 3,734 | 11,682 | 0 |
| 112N | 168 St-Washington Hts (1), Uptown | 15,370 | 19,918 | 7,411 | 7,959 | 9,679 |
| 625N | 96 St (6), The Bronx | 15,349 | 18,743 | 3,098 | 12,250 | 10 |
| F14N | 2 Av (F), Uptown | 15,283 | 19,227 | 11,119 | 4,164 | 0 |
| 121S | 86 St (1), Downtown | 15,229 | 19,654 | 11,392 | 3,837 | 23 |
| 121N | 86 St (1), Uptown | 15,210 | 19,579 | 3,743 | 11,467 | 23 |
| D28S | Church Av (B Q), Southbound | 15,198 | 23,776 | 3,378 | 11,820 | 3,509 |
| 625S | 96 St (6), Downtown | 15,174 | 18,511 | 12,147 | 3,027 | 10 |
| 708N | 90 St-Elmhurst Av (7), Outbound | 15,156 | 16,062 | 2,699 | 12,457 | 0 |
| A46N | Nostrand Av (A C), Manhattan | 15,152 | 19,031 | 12,049 | 3,102 | 481 |
| R21N | 8 St-NYU (R W), Uptown | 15,098 | 19,116 | 11,906 | 3,192 | 0 |
| M20S | Canal St (J Z), Downtown | 15,070 | 20,028 | 3,504 | 11,565 | 9,848 |
| Q05N | 96 St (Q), Last Stop | 15,038 | 20,249 | 0 | 15,038 | 0 |
| A33S | Spring St (C E), Downtown | 14,970 | 17,338 | 3,988 | 10,981 | 0 |
| A12N | 145 St (A C), Uptown | 14,960 | 20,619 | 5,830 | 9,130 | 5,214 |
| R13S | 5 Av/59 St (N R W), Downtown | 14,862 | 19,213 | 7,392 | 7,470 | 134 |
| 247N | Flatbush Av-Brooklyn College (2 5), Manhattan | 14,675 | 20,950 | 14,675 | 0 | 0 |
| 419N | Wall St (4 5), Uptown | 14,649 | 21,727 | 12,569 | 2,080 | 0 |
| D39N | Sheepshead Bay (B Q), Manhattan | 14,648 | 20,010 | 11,158 | 3,490 | 4,272 |
| F01S | Jamaica-179 St (F), Manhattan | 14,638 | 22,258 | 14,638 | 0 | 0 |
| A33N | Spring St (C E), Uptown | 14,558 | 16,861 | 10,286 | 4,272 | 0 |
| R33S | 4 Av-9 St (R), Southbound | 14,485 | 17,384 | 6,915 | 7,570 | 9,247 |
| 636N | Astor Pl (6), Uptown | 14,378 | 19,204 | 10,892 | 3,486 | 0 |
| 419S | Wall St (4 5), Downtown | 14,332 | 21,270 | 1,795 | 12,537 | 0 |
| B10N | 57 St (M), Uptown | 14,187 | 16,775 | 5,056 | 9,131 | 173 |
| 639S | Canal St (6), Downtown | 13,966 | 18,400 | 2,155 | 11,811 | 4,908 |
| 247S | Flatbush Av-Brooklyn College (2 5), Last Stop | 13,914 | 19,876 | 0 | 13,914 | 0 |
| 423S | Borough Hall (4 5), Outbound | 13,889 | 21,467 | 5,965 | 7,924 | 1,808 |
| B10S | 57 St (M), Downtown | 13,874 | 16,372 | 8,540 | 5,334 | 173 |
| F01N | Jamaica-179 St (F), Last Stop | 13,783 | 20,973 | 0 | 13,783 | 0 |
| 636S | Astor Pl (6), Downtown | 13,675 | 18,174 | 2,864 | 10,810 | 0 |
| R13N | 5 Av/59 St (N R W), Queens | 13,663 | 17,672 | 6,499 | 7,163 | 134 |
| 117S | 116 St-Columbia University (1), Downtown | 13,633 | 17,034 | 11,286 | 2,347 | 0 |
| F18N | York St (F), Manhattan | 13,630 | 14,802 | 9,652 | 3,978 | 0 |
| D26S | Prospect Park (B Q S), Southbound | 13,586 | 18,595 | 3,373 | 10,213 | 5,283 |
| 709N | 82 St-Jackson Hts (7), Outbound | 13,567 | 17,156 | 3,519 | 10,049 | 51 |
| 134N | Houston St (1), Uptown | 13,505 | 16,985 | 11,436 | 2,068 | 0 |
| F20S | Bergen St (F G), Southbound | 13,471 | 15,752 | 2,619 | 10,851 | 2,934 |
| 714S | 46 St-Bliss St (7), Manhattan | 13,454 | 15,103 | 9,248 | 4,207 | 488 |
| 134S | Houston St (1), Downtown | 13,411 | 16,950 | 1,638 | 11,773 | 0 |
| 714N | 46 St-Bliss St (7), Outbound | 13,371 | 15,008 | 4,134 | 9,237 | 488 |
| 117N | 116 St-Columbia University (1), Uptown | 13,353 | 16,680 | 2,153 | 11,199 | 0 |
| R27N | Whitehall St-South Ferry (R W), Uptown | 13,335 | 20,668 | 7,803 | 5,532 | 0 |
| R27S | Whitehall St-South Ferry (R W), Downtown | 13,272 | 20,488 | 5,584 | 7,688 | 52 |
| F16S | East Broadway (F), Brooklyn | 13,252 | 15,634 | 3,958 | 9,294 | 0 |
| D13N | 145 St (B D), Uptown | 13,208 | 18,616 | 6,598 | 6,610 | 4,723 |
| R25N | Cortlandt St (R W), Uptown | 13,160 | 19,498 | 7,105 | 6,055 | 2,733 |
| D28N | Church Av (B Q), Manhattan | 13,107 | 21,100 | 11,034 | 2,073 | 1,206 |
| 705S | 111 St (7), Manhattan | 13,079 | 13,072 | 10,872 | 2,207 | 0 |
| D26N | Prospect Park (B Q S), Northbound | 13,048 | 17,727 | 9,793 | 3,255 | 5,035 |
| 122S | 79 St (1), Downtown | 13,002 | 16,195 | 10,189 | 2,813 | 0 |
| 122N | 79 St (1), Uptown | 12,996 | 16,179 | 2,784 | 10,211 | 0 |
| M16N | Marcy Av (M J Z), Outbound | 12,922 | 18,221 | 6,427 | 6,495 | 2,015 |
| 213S | E 180 St (2 5), Manhattan | 12,901 | 17,821 | 8,509 | 4,392 | 6,625 |
| M20N | Canal St (J Z), Brooklyn | 12,879 | 17,204 | 10,666 | 2,213 | 8,208 |
| 709S | 82 St-Jackson Hts (7), Manhattan | 12,865 | 16,330 | 9,679 | 3,186 | 51 |
| 705N | 111 St (7), Outbound | 12,863 | 12,843 | 2,208 | 10,655 | 0 |
| F16N | East Broadway (F), Uptown | 12,786 | 15,068 | 8,817 | 3,969 | 0 |
| R25S | Cortlandt St (R W), Downtown | 12,739 | 18,746 | 6,079 | 6,660 | 2,683 |
| F18S | York St (F), Southbound | 12,656 | 13,668 | 3,274 | 9,382 | 0 |
| R01S | Astoria-Ditmars Blvd (N W), Manhattan | 12,560 | 19,206 | 12,560 | 0 | 0 |
| M16S | Marcy Av (M J Z), Manhattan | 12,474 | 17,592 | 6,330 | 6,144 | 1,809 |
| R22N | Prince St (R W), Uptown | 12,470 | 15,964 | 8,408 | 4,061 | 17 |
| 608S | Parkchester (6), Manhattan | 12,395 | 19,884 | 11,295 | 1,101 | 1,847 |
| F20N | Bergen St (F G), Northbound | 12,362 | 14,387 | 10,345 | 2,017 | 1,904 |
| R01N | Astoria-Ditmars Blvd (N W), Last Stop | 12,335 | 18,875 | 0 | 12,335 | 0 |
| D31S | Newkirk Plaza (B Q), Southbound | 12,240 | 16,311 | 3,142 | 9,098 | 4,201 |
| 608N | Parkchester (6), Northbound | 12,184 | 19,517 | 1,090 | 11,094 | 1,952 |
| G10S | 63 Dr-Rego Park (M R), Manhattan | 12,063 | 17,089 | 7,507 | 4,556 | 0 |
| 129S | 28 St (1), Downtown | 12,012 | 16,819 | 3,563 | 8,450 | 0 |
| 613N | Hunts Point Av (6), Northbound | 11,960 | 16,734 | 3,885 | 8,075 | 4,112 |
| F24S | 7 Av (F G), Southbound | 11,944 | 14,452 | 1,709 | 10,234 | 1,340 |
| L29N | Canarsie-Rockaway Pkwy (L), Manhattan | 11,938 | 16,741 | 11,938 | 0 | 4 |
| 225N | 125 St (2 3), Uptown | 11,923 | 16,442 | 3,945 | 7,977 | 121 |
| F21N | Carroll St (F G), Northbound | 11,878 | 13,651 | 10,146 | 1,732 | 783 |
| A21S | 81 St-Museum of Natural History (C B), Downtown | 11,874 | 14,464 | 10,167 | 1,708 | 0 |
| A21N | 81 St-Museum of Natural History (C B), Uptown | 11,870 | 14,429 | 1,644 | 10,227 | 0 |
| R04S | 30 Av (N W), Manhattan | 11,857 | 18,943 | 11,453 | 405 | 0 |
| R18S | 28 St (R W), Downtown | 11,853 | 15,335 | 4,029 | 7,824 | 0 |
| 129N | 28 St (1), Uptown | 11,768 | 16,380 | 8,118 | 3,650 | 0 |
| R22S | Prince St (R W), Downtown | 11,766 | 14,976 | 3,249 | 8,517 | 17 |
| D31N | Newkirk Plaza (B Q), Manhattan | 11,718 | 15,700 | 9,038 | 2,680 | 3,341 |
| R23N | Canal St (R W), Uptown | 11,704 | 16,282 | 5,333 | 6,371 | 6,166 |
| 130N | 23 St (1), Uptown | 11,700 | 16,295 | 7,587 | 4,113 | 0 |
| 225S | 125 St (2 3), Downtown | 11,671 | 16,064 | 7,821 | 3,851 | 121 |
| F21S | Carroll St (F G), Southbound | 11,605 | 13,333 | 1,696 | 9,909 | 783 |
| R04N | 30 Av (N W), Astoria | 11,588 | 18,525 | 438 | 11,150 | 0 |
| M08N | Myrtle-Wyckoff Avs (M), Inbound | 11,482 | 13,489 | 5,704 | 5,778 | 8,961 |
| 638N | Spring St (6), Uptown | 11,453 | 13,216 | 9,366 | 2,087 | 0 |
| G13S | Elmhurst Av (M R), Manhattan | 11,383 | 12,987 | 9,640 | 1,744 | 0 |
| G13N | Elmhurst Av (M R), Outbound | 11,354 | 12,965 | 1,804 | 9,550 | 0 |
| 130S | 23 St (1), Downtown | 11,315 | 15,885 | 3,649 | 7,666 | 0 |
| R18N | 28 St (R W), Uptown | 11,313 | 14,657 | 7,221 | 4,092 | 0 |
| L16N | DeKalb Av (L), Manhattan | 11,300 | 12,103 | 9,149 | 2,151 | 0 |
| E01N | World Trade Center (E), Uptown | 11,287 | 16,341 | 11,287 | 0 | 2,754 |
| G10N | 63 Dr-Rego Park (M R), Outbound | 11,130 | 15,762 | 4,180 | 6,950 | 0 |
| 622S | 116 St (6), Downtown | 11,121 | 15,151 | 7,411 | 3,710 | 63 |
| 638S | Spring St (6), Downtown | 11,011 | 12,635 | 1,529 | 9,481 | 0 |
| 624S | 103 St (6), Downtown | 10,958 | 14,329 | 7,500 | 3,458 | 39 |
| D39S | Sheepshead Bay (B Q), Southbound | 10,922 | 15,247 | 1,861 | 9,061 | 942 |
| M22S | Fulton St (J Z), Downtown | 10,880 | 14,988 | 1,121 | 9,759 | 5,333 |
| 133S | Christopher St-Stonewall (1), Downtown | 10,828 | 11,549 | 1,252 | 9,576 | 0 |
| F24N | 7 Av (F G), Northbound | 10,826 | 13,070 | 9,549 | 1,276 | 250 |
| 622N | 116 St (6), The Bronx | 10,787 | 14,724 | 3,730 | 7,058 | 63 |
| 613S | Hunts Point Av (6), Manhattan | 10,752 | 14,851 | 7,732 | 3,020 | 2,917 |
| L29S | Canarsie-Rockaway Pkwy (L), Last Stop | 10,729 | 15,056 | 0 | 10,729 | 4 |
| G19N | Steinway St (M R), Outbound | 10,711 | 16,152 | 3,545 | 7,166 | 37 |
| L16S | DeKalb Av (L), Outbound | 10,654 | 11,428 | 1,868 | 8,786 | 0 |
| 133N | Christopher St-Stonewall (1), Uptown | 10,629 | 11,301 | 9,216 | 1,413 | 0 |
| M08S | Myrtle-Wyckoff Avs (M), Middle Village | 10,589 | 12,260 | 5,058 | 5,531 | 7,928 |
| R05S | Broadway (N W), Manhattan | 10,570 | 10,907 | 10,078 | 492 | 0 |
| R05N | Broadway (N W), Astoria | 10,538 | 10,896 | 519 | 10,019 | 0 |
| 142N | South Ferry (1), Uptown | 10,525 | 16,042 | 10,525 | 0 | 0 |
| 118S | Cathedral Pkwy (110 St) (1), Downtown | 10,480 | 12,547 | 8,678 | 1,802 | 0 |
| 624N | 103 St (6), The Bronx | 10,460 | 13,678 | 3,360 | 7,099 | 39 |
| 118N | Cathedral Pkwy (110 St) (1), Uptown | 10,448 | 12,514 | 1,846 | 8,602 | 0 |
| B04S | 21 St-Queensbridge (M), Manhattan | 10,446 | 12,701 | 7,211 | 3,235 | 28 |
| 119S | 103 St (1), Downtown | 10,242 | 12,742 | 8,591 | 1,651 | 0 |
| R44N | 86 St (R), Manhattan | 10,208 | 12,356 | 10,204 | 4 | 0 |
| 119N | 103 St (1), Uptown | 10,173 | 12,650 | 1,664 | 8,509 | 0 |
| G19S | Steinway St (M R), Manhattan | 10,163 | 15,326 | 6,824 | 3,339 | 37 |
| B04N | 21 St-Queensbridge (M), Outbound | 10,126 | 12,391 | 3,155 | 6,971 | 27 |
| A20N | 86 St (C B), Uptown | 10,090 | 11,618 | 2,149 | 7,941 | 0 |
| 142S | South Ferry (1), Last Stop | 10,062 | 15,371 | 0 | 10,062 | 0 |
| A40N | High St (A C), Manhattan | 10,038 | 12,665 | 7,308 | 2,730 | 0 |
| F27N | Church Av (F G), Northbound | 9,946 | 13,194 | 7,867 | 2,079 | 2,627 |
| N02N | 8 Av (N), Manhattan | 9,898 | 12,090 | 6,695 | 3,202 | 0 |
| A20S | 86 St (C B), Downtown | 9,830 | 11,342 | 7,813 | 2,017 | 0 |
| 115N | 137 St-City College (1), Uptown | 9,827 | 13,607 | 1,911 | 7,916 | 0 |
| 115S | 137 St-City College (1), Downtown | 9,827 | 13,611 | 7,936 | 1,892 | 0 |
| G26S | Greenpoint Av (G), Southbound | 9,789 | 10,778 | 4,791 | 4,999 | 0 |
| A55N | Euclid Av (A C), Manhattan | 9,784 | 14,261 | 8,561 | 1,224 | 2,270 |
| E01S | World Trade Center (E), Last Stop | 9,766 | 14,052 | 0 | 9,766 | 2,262 |
| N02S | 8 Av (N), Coney Island | 9,762 | 11,984 | 3,265 | 6,497 | 0 |
| 224S | 135 St (2 3), Downtown | 9,716 | 15,235 | 6,882 | 2,834 | 506 |
| G26N | Greenpoint Av (G), Queens | 9,701 | 10,631 | 4,901 | 4,800 | 0 |
| 213N | E 180 St (2 5), Northbound | 9,673 | 12,728 | 2,875 | 6,797 | 3,487 |
| A40S | High St (A C), Outbound | 9,649 | 12,230 | 2,399 | 7,250 | 0 |
| R44S | 86 St (R), Bay Ridge | 9,584 | 11,608 | 4 | 9,579 | 0 |
| 224N | 135 St (2 3), Uptown | 9,486 | 14,884 | 2,724 | 6,762 | 297 |
| M22N | Fulton St (J Z), Brooklyn | 9,482 | 13,038 | 8,527 | 955 | 4,560 |
| 715S | 40 St-Lowery St (7), Manhattan | 9,465 | 11,410 | 6,248 | 3,216 | 342 |
| A22N | 72 St (C B), Uptown | 9,449 | 9,656 | 1,264 | 8,185 | 0 |
| 715N | 40 St-Lowery St (7), Outbound | 9,427 | 11,373 | 3,156 | 6,272 | 342 |
| A22S | 72 St (C B), Downtown | 9,298 | 9,521 | 8,042 | 1,257 | 0 |
| D40N | Brighton Beach (B Q), Manhattan | 9,225 | 12,940 | 7,807 | 1,417 | 184 |
| 716S | 33 St-Rawson St (7), Manhattan | 9,123 | 11,442 | 4,292 | 4,831 | 3 |
| R03S | Astoria Blvd (N W), Manhattan | 9,117 | 2,546 | 8,966 | 152 | 0 |
| A55S | Euclid Av (A C), Queens | 9,113 | 13,325 | 1,060 | 8,053 | 1,979 |
| 716N | 33 St-Rawson St (7), Outbound | 9,111 | 11,441 | 4,614 | 4,496 | 3 |
| G28N | Nassau Av (G), Queens | 9,021 | 10,558 | 4,264 | 4,758 | 0 |
| G28S | Nassau Av (G), Southbound | 9,011 | 10,634 | 4,652 | 4,358 | 0 |
| R03N | Astoria Blvd (N W), Astoria | 8,882 | 2,483 | 162 | 8,720 | 0 |
| A07S | 175 St (A), Downtown | 8,793 | 14,428 | 8,423 | 370 | 0 |
| A19N | 96 St (C B), Uptown | 8,763 | 11,087 | 2,318 | 6,445 | 0 |
| D40S | Brighton Beach (B Q), Southbound | 8,717 | 12,259 | 1,375 | 7,342 | 0 |
| 623S | 110 St (6), Downtown | 8,677 | 11,083 | 6,515 | 2,162 | 42 |
| L11S | Graham Av (L), Outbound | 8,602 | 10,085 | 1,242 | 7,359 | 0 |
| R40N | 53 St (R), Manhattan | 8,597 | 10,397 | 6,454 | 2,143 | 104 |
| D25S | 7 Av (B Q), Southbound | 8,583 | 11,206 | 1,827 | 6,756 | 0 |
| 232S | Borough Hall (2 3), Outbound | 8,520 | 12,930 | 3,411 | 5,109 | 1,700 |
| L11N | Graham Av (L), Manhattan | 8,508 | 9,974 | 7,322 | 1,185 | 0 |
| R23S | Canal St (R W), Downtown | 8,484 | 11,561 | 3,751 | 4,733 | 3,185 |
| 702N | Mets-Willets Point (7), Outbound | 8,464 | 7,025 | 634 | 7,829 | 92 |
| A19S | 96 St (C B), Downtown | 8,413 | 10,656 | 6,246 | 2,167 | 0 |
| L15S | Jefferson St (L), Outbound | 8,383 | 7,815 | 1,520 | 6,863 | 0 |
| D25N | 7 Av (B Q), Manhattan | 8,346 | 10,873 | 6,596 | 1,750 | 0 |
| L15N | Jefferson St (L), Manhattan | 8,322 | 7,738 | 6,693 | 1,629 | 0 |
| A07N | 175 St (A), Uptown | 8,250 | 13,524 | 330 | 7,920 | 0 |
| 113S | 157 St (1), Downtown | 8,229 | 12,717 | 5,962 | 2,267 | 0 |
| 113N | 157 St (1), Uptown | 8,216 | 12,693 | 2,297 | 5,918 | 0 |
| 623N | 110 St (6), The Bronx | 8,197 | 10,470 | 2,065 | 6,132 | 42 |
| A06S | 181 St (A), Downtown | 8,177 | 11,461 | 7,813 | 364 | 0 |
| 111N | 181 St (1), The Bronx | 8,124 | 11,527 | 1,861 | 6,263 | 0 |
| 111S | 181 St (1), Downtown | 8,106 | 11,467 | 6,499 | 1,606 | 0 |
| B06S | Roosevelt Island (M), Downtown | 8,059 | 8,597 | 6,949 | 1,110 | 241 |
| B06N | Roosevelt Island (M), Queens | 7,945 | 8,504 | 1,054 | 6,891 | 241 |
| A06N | 181 St (A), Uptown | 7,918 | 11,082 | 315 | 7,602 | 0 |
| 226S | 116 St (2 3), Downtown | 7,765 | 11,342 | 5,783 | 1,982 | 0 |
| 226N | 116 St (2 3), Uptown | 7,717 | 11,300 | 2,003 | 5,714 | 0 |
| 232N | Borough Hall (2 3), Manhattan | 7,712 | 11,752 | 5,017 | 2,694 | 1,255 |
| 244N | Church Av (2 5), Manhattan | 7,698 | 10,084 | 7,333 | 365 | 0 |
| 116S | 125 St (1), Downtown | 7,687 | 8,452 | 6,131 | 1,557 | 0 |
| 702S | Mets-Willets Point (7), Manhattan | 7,662 | 6,347 | 6,895 | 767 | 64 |
| 116N | 125 St (1), Uptown | 7,659 | 8,409 | 1,508 | 6,151 | 0 |
| M12N | Flushing Av (M J), Outbound | 7,542 | 9,482 | 3,996 | 3,546 | 88 |
| G33N | Bedford-Nostrand Avs (G), Queens | 7,526 | 9,443 | 4,478 | 3,048 | 0 |
| 407S | Fordham Rd (4), Manhattan | 7,493 | 10,572 | 7,002 | 491 | 0 |
| R39N | 45 St (R), Manhattan | 7,457 | 8,788 | 6,295 | 1,163 | 7 |
| M12S | Flushing Av (M J), Manhattan | 7,410 | 9,315 | 3,582 | 3,828 | 97 |
| R28N | Court St (R), Manhattan | 7,351 | 10,816 | 2,172 | 5,179 | 2,971 |
| R32N | Union St (R), Manhattan | 7,346 | 8,237 | 5,747 | 1,599 | 0 |
| L19N | Halsey St (L), Manhattan | 7,343 | 7,916 | 5,857 | 1,486 | 0 |
| 244S | Church Av (2 5), Flatbush | 7,331 | 9,611 | 398 | 6,933 | 0 |
| D07S | Tremont Av (B D), Manhattan | 7,326 | 11,781 | 6,675 | 652 | 1,074 |
| R28S | Court St (R), Southbound | 7,242 | 10,701 | 4,638 | 2,604 | 3,215 |
| 114N | 145 St (1), Uptown | 7,222 | 9,762 | 1,666 | 5,557 | 0 |
| 407N | Fordham Rd (4), Northbound | 7,216 | 10,210 | 563 | 6,653 | 0 |
| D05S | Fordham Rd (B D), Manhattan | 7,211 | 13,113 | 7,041 | 170 | 358 |
| F27S | Church Av (F G), Southbound | 7,189 | 9,816 | 742 | 6,446 | 79 |
| 104S | 231 St (1), Manhattan | 7,182 | 10,333 | 7,063 | 120 | 0 |
| R40S | 53 St (R), Southbound | 7,141 | 8,625 | 1,574 | 5,567 | 104 |
| 114S | 145 St (1), Downtown | 7,129 | 9,649 | 5,513 | 1,615 | 0 |
| M21S | Chambers St (J Z), Downtown | 7,118 | 9,960 | 1,288 | 5,830 | 4,082 |
| 104N | 231 St (1), Van Cortlandt | 7,101 | 10,221 | 116 | 6,984 | 0 |
| 409S | Burnside Av (4), Manhattan | 7,099 | 10,596 | 6,337 | 762 | 46 |
| 413S | 167 St (4), Manhattan | 7,094 | 9,115 | 6,082 | 1,012 | 0 |
| R32S | Union St (R), Southbound | 7,094 | 7,970 | 1,509 | 5,585 | 0 |
| 409N | Burnside Av (4), Northbound | 7,049 | 10,504 | 1,041 | 6,008 | 551 |
| L19S | Halsey St (L), Outbound | 7,034 | 7,582 | 1,415 | 5,619 | 0 |
| G18S | 46 St (M R), Manhattan | 7,029 | 9,483 | 5,354 | 1,675 | 5 |
| L26S | Livonia Av (L), Canarsie | 7,013 | 9,372 | 1,413 | 5,600 | 4,813 |
| D05N | Fordham Rd (B D), Northbound | 7,010 | 12,765 | 190 | 6,819 | 367 |
| L05S | 3 Av (L), Brooklyn | 7,010 | 7,214 | 3,552 | 3,458 | 0 |
| 406S | Kingsbridge Rd (4), Manhattan | 6,997 | 9,583 | 6,596 | 401 | 0 |
| G33S | Bedford-Nostrand Avs (G), Southbound | 6,995 | 8,815 | 2,916 | 4,078 | 0 |
| G18N | 46 St (M R), Outbound | 6,992 | 9,445 | 1,649 | 5,342 | 5 |
| L14N | Morgan Av (L), Manhattan | 6,985 | 7,642 | 5,826 | 1,158 | 0 |
| L14S | Morgan Av (L), Outbound | 6,979 | 7,643 | 1,022 | 5,957 | 0 |
| A45N | Franklin Av (C), Manhattan | 6,936 | 9,670 | 3,509 | 3,427 | 3,447 |
| D07N | Tremont Av (B D), Northbound | 6,935 | 11,255 | 646 | 6,289 | 1,058 |
| G09S | 67 Av (M R), Manhattan | 6,927 | 9,600 | 3,393 | 3,534 | 0 |
| 131N | 18 St (1), Uptown | 6,894 | 9,931 | 4,222 | 2,672 | 0 |
| A44N | Clinton-Washington Avs (C), Manhattan | 6,861 | 7,908 | 5,481 | 1,381 | 0 |
| G36N | Fulton St (G), Queens | 6,811 | 7,003 | 3,478 | 3,333 | 0 |
| 413N | 167 St (4), Northbound | 6,786 | 8,735 | 1,039 | 5,748 | 0 |
| 619S | 3 Av-138 St (6), Manhattan | 6,763 | 9,125 | 5,374 | 1,389 | 242 |
| R39S | 45 St (R), Southbound | 6,751 | 7,965 | 1,015 | 5,736 | 7 |
| A17S | Cathedral Pkwy (110 St) (C B), Downtown | 6,735 | 8,136 | 4,916 | 1,818 | 1 |
| 131S | 18 St (1), Downtown | 6,723 | 9,786 | 2,411 | 4,312 | 0 |
| R42N | Bay Ridge Av (R), Manhattan | 6,707 | 8,243 | 6,232 | 474 | 0 |
| G09N | 67 Av (M R), Outbound | 6,666 | 9,245 | 3,556 | 3,110 | 0 |
| A02S | Inwood-207 St (A), Downtown | 6,631 | 10,213 | 6,631 | 0 | 0 |
| 243N | Winthrop St (2 5), Manhattan | 6,629 | 6,947 | 6,325 | 304 | 0 |
| 406N | Kingsbridge Rd (4), Northbound | 6,608 | 9,065 | 426 | 6,181 | 0 |
| A45S | Franklin Av (C), Outbound | 6,597 | 9,160 | 3,159 | 3,438 | 3,330 |
| A44S | Clinton-Washington Avs (C), Outbound | 6,524 | 7,520 | 1,264 | 5,260 | 0 |
| 243S | Winthrop St (2 5), Flatbush | 6,488 | 6,804 | 328 | 6,160 | 0 |
| F05S | Briarwood (E F), Manhattan | 6,488 | 8,261 | 5,043 | 1,446 | 2,214 |
| 110S | 191 St (1), Downtown | 6,484 | 8,532 | 5,238 | 1,246 | 0 |
| 233S | Hoyt St (2 3), Outbound | 6,439 | 8,345 | 3,579 | 2,860 | 0 |
| 619N | 3 Av-138 St (6), Northbound | 6,397 | 8,641 | 1,353 | 5,044 | 95 |
| R42S | Bay Ridge Av (R), Bay Ridge | 6,396 | 7,867 | 452 | 5,943 | 0 |
| L26N | Livonia Av (L), Manhattan | 6,391 | 8,542 | 5,045 | 1,346 | 3,674 |
| F02S | 169 St (F), Manhattan | 6,318 | 8,390 | 6,230 | 88 | 0 |
| 139N | Rector St (1), Uptown | 6,306 | 9,235 | 6,257 | 49 | 0 |
| A02N | Inwood-207 St (A), Last Stop | 6,293 | 9,699 | 0 | 6,293 | 0 |
| 139S | Rector St (1), Downtown | 6,288 | 9,221 | 60 | 6,229 | 0 |
| D10S | 167 St (B D), Manhattan | 6,278 | 9,474 | 5,558 | 720 | 0 |
| A17N | Cathedral Pkwy (110 St) (C B), Uptown | 6,211 | 7,501 | 1,627 | 4,584 | 1 |
| 227S | 110 St-Malcolm X Plaza (2 3), Downtown | 6,182 | 9,430 | 4,628 | 1,553 | 118 |
| 254N | Junius St (3), Manhattan | 6,168 | 8,055 | 4,604 | 1,564 | 4,053 |
| 237S | Grand Army Plaza (2 3), Outbound | 6,119 | 7,897 | 1,328 | 4,791 | 3 |
| 254S | Junius St (3), New Lots | 6,083 | 8,041 | 1,701 | 4,381 | 4,435 |
| A47N | Kingston-Throop Avs (C), Manhattan | 6,083 | 7,627 | 4,584 | 1,499 | 0 |
| B21N | Bay Pkwy (D), Manhattan | 6,083 | 8,291 | 5,420 | 663 | 4 |
| L13N | Montrose Av (L), Manhattan | 6,049 | 7,056 | 4,957 | 1,092 | 0 |
| L13S | Montrose Av (L), Outbound | 6,037 | 7,029 | 1,001 | 5,035 | 0 |
| F02N | 169 St (F), Jamaica | 6,013 | 7,992 | 88 | 5,925 | 0 |
| D10N | 167 St (B D), Northbound | 6,006 | 9,075 | 635 | 5,371 | 0 |
| J30S | Gates Av (J Z), Manhattan | 6,004 | 7,860 | 4,442 | 1,562 | 0 |
| 227N | 110 St-Malcolm X Plaza (2 3), Uptown | 5,992 | 9,137 | 1,388 | 4,604 | 84 |
| 237N | Grand Army Plaza (2 3), Manhattan | 5,970 | 7,725 | 4,648 | 1,322 | 3 |
| M21N | Chambers St (J Z), Brooklyn | 5,935 | 8,318 | 4,369 | 1,566 | 3,274 |
| B21S | Bay Pkwy (D), Southbound | 5,931 | 8,085 | 640 | 5,291 | 19 |
| A61N | Rockaway Blvd (A), Manhattan | 5,890 | 8,154 | 5,149 | 741 | 287 |
| 246N | Newkirk Av-Little Haiti (2 5), Manhattan | 5,885 | 7,698 | 5,700 | 185 | 0 |
| R06S | 36 Av (N W), Manhattan | 5,878 | 7,220 | 5,324 | 555 | 0 |
| L12S | Grand St (L), Outbound | 5,874 | 6,908 | 1,094 | 4,780 | 0 |
| 217N | Simpson St (2 5), Northbound | 5,855 | 8,333 | 1,285 | 4,570 | 0 |
| 412S | 170 St (4), Manhattan | 5,831 | 8,430 | 4,846 | 986 | 0 |
| R06N | 36 Av (N W), Astoria | 5,808 | 7,171 | 491 | 5,317 | 0 |
| 217S | Simpson St (2 5), Manhattan | 5,801 | 8,226 | 4,638 | 1,163 | 0 |
| G16S | Northern Blvd (M R), Manhattan | 5,798 | 7,048 | 3,929 | 1,870 | 8 |
| N07N | Bay Pkwy (N), Manhattan | 5,787 | 7,025 | 5,074 | 712 | 0 |
| A61S | Rockaway Blvd (A), Outbound | 5,770 | 8,003 | 653 | 5,118 | 71 |
| F03S | Parsons Blvd (F), Manhattan | 5,770 | 7,111 | 5,471 | 299 | 91 |
| 110N | 191 St (1), The Bronx | 5,752 | 7,611 | 991 | 4,761 | 0 |
| 713N | 52 St (7), Outbound | 5,738 | 8,331 | 2,918 | 2,821 | 0 |
| 233N | Hoyt St (2 3), Manhattan | 5,709 | 7,441 | 2,366 | 3,343 | 0 |
| J29S | Halsey St (J), Manhattan | 5,709 | 7,642 | 3,861 | 1,849 | 0 |
| D37N | Avenue U (Q), Manhattan | 5,708 | 7,689 | 4,730 | 978 | 0 |
| L05N | 3 Av (L), West Side | 5,695 | 5,822 | 2,514 | 3,182 | 0 |
| 109S | Dyckman St (1), Downtown | 5,677 | 7,013 | 4,936 | 741 | 0 |
| 136N | Franklin St (1), Uptown | 5,656 | 6,015 | 4,519 | 1,137 | 2 |
| L12N | Grand St (L), Manhattan | 5,653 | 6,655 | 4,564 | 1,089 | 0 |
| 402N | Mosholu Pkwy (4), Woodlawn | 5,651 | 8,959 | 58 | 5,594 | 0 |
| 412N | 170 St (4), Northbound | 5,650 | 8,176 | 977 | 4,673 | 0 |
| 402S | Mosholu Pkwy (4), Manhattan | 5,647 | 8,947 | 5,587 | 60 | 0 |
| J30N | Gates Av (J Z), Outbound | 5,634 | 7,408 | 1,525 | 4,108 | 0 |
| N07S | Bay Pkwy (N), Coney Island | 5,628 | 6,834 | 674 | 4,954 | 0 |
| 231S | Clark St (2 3), Outbound | 5,604 | 6,006 | 1,660 | 3,944 | 0 |
| N03N | Fort Hamilton Pkwy (N), Manhattan | 5,598 | 4,639 | 4,445 | 1,153 | 0 |
| G16N | Northern Blvd (M R), Outbound | 5,572 | 6,787 | 1,764 | 3,807 | 8 |
| 136S | Franklin St (1), Downtown | 5,548 | 5,970 | 955 | 4,593 | 2 |
| M23S | Broad St (J Z), Last Stop | 5,510 | 8,810 | 0 | 5,510 | 0 |
| F03N | Parsons Blvd (F), Jamaica | 5,442 | 6,718 | 315 | 5,127 | 63 |
| N03S | Fort Hamilton Pkwy (N), Coney Island | 5,437 | 4,514 | 1,168 | 4,268 | 0 |
| 246S | Newkirk Av-Little Haiti (2 5), Flatbush | 5,418 | 7,089 | 157 | 5,262 | 0 |
| B18N | 79 St (D), Manhattan | 5,411 | 6,667 | 4,724 | 687 | 0 |
| 211N | Pelham Pkwy (2 5), Northbound | 5,386 | 8,711 | 1,028 | 4,358 | 0 |
| D37S | Avenue U (Q), Southbound | 5,379 | 7,259 | 901 | 4,477 | 0 |
| A03S | Dyckman St (A), Downtown | 5,370 | 7,417 | 5,368 | 2 | 3 |
| R34N | Prospect Av (R), Manhattan | 5,369 | 6,557 | 4,254 | 1,115 | 12 |
| A16S | 116 St (C B), Downtown | 5,360 | 7,668 | 3,215 | 2,145 | 0 |
| 231N | Clark St (2 3), Manhattan | 5,340 | 5,719 | 3,700 | 1,640 | 0 |
| G35N | Clinton-Washington Avs (G), Queens | 5,336 | 5,842 | 2,645 | 2,691 | 0 |
| 611S | Elder Av (6), Manhattan | 5,291 | 7,206 | 4,721 | 570 | 0 |
| 211S | Pelham Pkwy (2 5), Manhattan | 5,281 | 8,483 | 4,362 | 919 | 0 |
| 610S | Morrison Av-Soundview (6), Manhattan | 5,281 | 7,398 | 4,509 | 771 | 0 |
| N04N | New Utrecht Av (N), Manhattan | 5,269 | 6,169 | 3,699 | 1,570 | 2,934 |
| A16N | 116 St (C B), Uptown | 5,257 | 7,515 | 2,178 | 3,079 | 0 |
| A47S | Kingston-Throop Avs (C), Outbound | 5,240 | 6,585 | 1,180 | 4,060 | 0 |
| B18S | 79 St (D), Southbound | 5,238 | 6,457 | 675 | 4,563 | 0 |
| 109N | Dyckman St (1), The Bronx | 5,231 | 6,483 | 758 | 4,473 | 0 |
| D30N | Cortelyou Rd (Q), Manhattan | 5,213 | 6,694 | 4,198 | 1,015 | 0 |
| A03N | Dyckman St (A), Uptown | 5,170 | 7,149 | 12 | 5,157 | 0 |
| M23N | Broad St (J Z), Brooklyn | 5,163 | 8,251 | 5,163 | 0 | 0 |
| F25N | 15 St-Prospect Park (F G), Northbound | 5,123 | 6,781 | 4,684 | 439 | 2 |
| 401S | Woodlawn (4), Manhattan | 5,122 | 7,249 | 5,122 | 0 | 0 |
| F25S | 15 St-Prospect Park (F G), Southbound | 5,101 | 6,744 | 399 | 4,701 | 2 |
| J31S | Kosciuszko St (J), Manhattan | 5,095 | 6,100 | 3,987 | 1,108 | 0 |
| G35S | Clinton-Washington Avs (G), Southbound | 5,092 | 5,609 | 2,558 | 2,534 | 0 |
| R34S | Prospect Av (R), Southbound | 5,077 | 6,182 | 1,010 | 4,067 | 12 |
| B19N | 18 Av (D), Manhattan | 5,075 | 6,590 | 4,600 | 475 | 0 |
| 711N | 69 St (7), Outbound | 5,043 | 6,490 | 2,543 | 2,499 | 0 |
| B12N | 9 Av (D), Manhattan | 5,043 | 5,919 | 4,321 | 722 | 0 |
| 251N | Sutter Av-Rutland Rd (3), Manhattan | 5,042 | 7,093 | 4,360 | 683 | 25 |
| M04N | Fresh Pond Rd (M), Inbound | 5,037 | 6,389 | 4,854 | 183 | 0 |
| F26N | Fort Hamilton Pkwy (F G), Northbound | 5,022 | 6,253 | 4,749 | 273 | 0 |
| A65N | Ozone Park-Lefferts Blvd (A), Manhattan | 5,019 | 7,919 | 5,019 | 0 | 0 |
| 611N | Elder Av (6), Northbound | 4,989 | 6,783 | 490 | 4,499 | 0 |
| 135S | Canal St (1), Downtown | 4,987 | 7,941 | 949 | 4,039 | 31 |
| 219S | Prospect Av (2 5), Manhattan | 4,966 | 7,375 | 4,158 | 808 | 0 |
| 215S | 174 St (2 5), Manhattan | 4,960 | 7,043 | 4,054 | 906 | 4 |
| F26S | Fort Hamilton Pkwy (F G), Southbound | 4,927 | 6,129 | 222 | 4,706 | 0 |
| B12S | 9 Av (D), Southbound | 4,924 | 5,783 | 698 | 4,226 | 0 |
| 401N | Woodlawn (4), Last Stop | 4,923 | 6,972 | 0 | 4,923 | 0 |
| 108N | 207 St (1), The Bronx | 4,913 | 6,662 | 628 | 4,285 | 0 |
| 135N | Canal St (1), Uptown | 4,905 | 7,722 | 3,847 | 1,058 | 31 |
| B19S | 18 Av (D), Southbound | 4,896 | 6,357 | 428 | 4,467 | 0 |
| D03S | Bedford Park Blvd (B D), Manhattan | 4,878 | 7,790 | 4,641 | 238 | 369 |
| D04S | Kingsbridge Rd (B D), Manhattan | 4,877 | 8,509 | 4,774 | 103 | 6 |
| D01S | Norwood-205 St (D), Manhattan | 4,873 | 8,926 | 4,873 | 0 | 0 |
| D27N | Parkside Av (Q), Manhattan | 4,869 | 5,543 | 4,165 | 703 | 0 |
| N04S | New Utrecht Av (N), Coney Island | 4,867 | 5,652 | 1,327 | 3,540 | 2,438 |
| D01N | Norwood-205 St (D), Last Stop | 4,864 | 8,913 | 0 | 4,864 | 0 |
| G36S | Fulton St (G), Southbound | 4,862 | 5,039 | 2,153 | 2,709 | 0 |
| A43S | Lafayette Av (C), Outbound | 4,861 | 5,607 | 1,814 | 3,048 | 0 |
| D34N | Avenue M (Q), Manhattan | 4,861 | 5,912 | 3,435 | 1,426 | 0 |
| J29N | Halsey St (J), Outbound | 4,857 | 6,533 | 1,571 | 3,285 | 0 |
| D30S | Cortelyou Rd (Q), Southbound | 4,852 | 6,232 | 948 | 3,905 | 0 |
| N08N | Kings Hwy (N), Manhattan | 4,850 | 4,622 | 4,357 | 492 | 0 |
| J31N | Kosciuszko St (J), Outbound | 4,848 | 5,829 | 1,097 | 3,751 | 0 |
| G34N | Classon Av (G), Queens | 4,846 | 5,947 | 2,639 | 2,208 | 0 |
| B16N | 62 St (D), Manhattan | 4,824 | 5,725 | 2,157 | 2,667 | 3,021 |
| R24N | City Hall (R W), Uptown | 4,811 | 6,964 | 3,127 | 1,684 | 0 |
| D34S | Avenue M (Q), Southbound | 4,809 | 5,852 | 1,454 | 3,354 | 0 |
| M04S | Fresh Pond Rd (M), Middle Village | 4,808 | 6,103 | 165 | 4,643 | 0 |
| 219N | Prospect Av (2 5), Northbound | 4,802 | 7,159 | 878 | 3,923 | 0 |
| A14S | 135 St (C B), Downtown | 4,791 | 6,319 | 3,588 | 1,202 | 58 |
| R43N | 77 St (R), Manhattan | 4,775 | 6,101 | 4,722 | 53 | 0 |
| 215N | 174 St (2 5), Northbound | 4,761 | 6,784 | 950 | 3,812 | 4 |
| A65S | Ozone Park-Lefferts Blvd (A), Last Stop | 4,755 | 7,507 | 0 | 4,755 | 0 |
| A14N | 135 St (C B), Uptown | 4,754 | 6,277 | 1,284 | 3,470 | 56 |
| 607S | Castle Hill Av (6), Manhattan | 4,752 | 6,888 | 4,415 | 337 | 0 |
| D04N | Kingsbridge Rd (B D), Northbound | 4,736 | 8,274 | 111 | 4,624 | 6 |
| D27S | Parkside Av (Q), Southbound | 4,725 | 5,384 | 713 | 4,012 | 0 |
| 610N | Morrison Av-Soundview (6), Northbound | 4,680 | 6,571 | 562 | 4,118 | 0 |
| 108S | 207 St (1), Downtown | 4,679 | 6,306 | 4,197 | 482 | 0 |
| R26N | Rector St (R W), Uptown | 4,659 | 7,521 | 3,234 | 1,425 | 0 |
| 242N | Sterling St (2 5), Manhattan | 4,645 | 5,835 | 4,293 | 352 | 0 |
| N08S | Kings Hwy (N), Coney Island | 4,639 | 4,412 | 456 | 4,183 | 0 |
| 101S | Van Cortlandt Park-242 St (1), Manhattan | 4,624 | 7,423 | 4,624 | 0 | 0 |
| 214S | West Farms Sq-E Tremont Av (2 5), Manhattan | 4,599 | 7,450 | 3,690 | 909 | 116 |
| A49N | Ralph Av (C), Manhattan | 4,596 | 6,587 | 3,687 | 909 | 0 |
| 251S | Sutter Av-Rutland Rd (3), New Lots | 4,558 | 6,437 | 652 | 3,906 | 25 |
| A50N | Rockaway Av (C), Manhattan | 4,529 | 6,184 | 3,264 | 1,266 | 0 |
| S01S | Franklin Av (S), Prospect Park | 4,524 | 6,196 | 4,524 | 0 | 3,388 |
| D09S | 170 St (B D), Manhattan | 4,519 | 7,650 | 3,878 | 641 | 0 |
| R45N | Bay Ridge-95 St (R), Manhattan | 4,517 | 6,216 | 4,517 | 0 | 0 |
| R43S | 77 St (R), Bay Ridge | 4,506 | 5,762 | 53 | 4,453 | 0 |
| D03N | Bedford Park Blvd (B D), Northbound | 4,505 | 7,125 | 104 | 4,400 | 94 |
| R26S | Rector St (R W), Downtown | 4,495 | 7,246 | 1,420 | 3,075 | 0 |
| G34S | Classon Av (G), Southbound | 4,480 | 5,521 | 2,140 | 2,340 | 0 |
| 410S | 176 St (4), Manhattan | 4,477 | 5,971 | 3,896 | 580 | 0 |
| 601S | Pelham Bay Park (6), Manhattan | 4,472 | 7,499 | 4,472 | 0 | 0 |
| D33S | Avenue J (Q), Southbound | 4,472 | 6,014 | 1,353 | 3,119 | 0 |
| 607N | Castle Hill Av (6), Pelham Bay | 4,469 | 6,475 | 339 | 4,129 | 0 |
| D33N | Avenue J (Q), Manhattan | 4,444 | 5,974 | 3,178 | 1,266 | 0 |
| 242S | Sterling St (2 5), Flatbush | 4,422 | 5,558 | 337 | 4,085 | 0 |
| 101N | Van Cortlandt Park-242 St (1), Last Stop | 4,399 | 7,065 | 0 | 4,399 | 0 |
| 208S | Gun Hill Rd (2 5), Manhattan | 4,391 | 7,166 | 3,977 | 414 | 0 |
| 214N | West Farms Sq-E Tremont Av (2 5), Northbound | 4,370 | 7,107 | 933 | 3,437 | 116 |
| A43N | Lafayette Av (C), Manhattan | 4,341 | 5,016 | 2,710 | 1,630 | 0 |
| R24S | City Hall (R W), Downtown | 4,333 | 6,293 | 1,417 | 2,917 | 0 |
| N05N | 18 Av (N), Manhattan | 4,325 | 3,927 | 3,694 | 632 | 0 |
| G32S | Myrtle-Willoughby Avs (G), Southbound | 4,318 | 6,070 | 1,747 | 2,571 | 0 |
| G20N | 36 St (M R), Outbound | 4,273 | 6,600 | 1,484 | 2,789 | 882 |
| N05S | 18 Av (N), Coney Island | 4,272 | 3,891 | 616 | 3,656 | 0 |
| G30S | Broadway (G), Southbound | 4,262 | 5,151 | 1,409 | 2,853 | 0 |
| G32N | Myrtle-Willoughby Avs (G), Queens | 4,254 | 5,959 | 2,651 | 1,603 | 0 |
| S01N | Franklin Av (S), Last Stop | 4,253 | 5,735 | 0 | 4,253 | 3,390 |
| G07S | Jamaica-Van Wyck (E), Manhattan | 4,252 | 5,015 | 3,497 | 755 | 0 |
| 408S | 183 St (4), Manhattan | 4,238 | 6,071 | 3,877 | 360 | 0 |
| 220S | Jackson Av (2 5), Manhattan | 4,232 | 5,580 | 3,536 | 697 | 1 |
| R45S | Bay Ridge-95 St (R), Last Stop | 4,230 | 5,825 | 0 | 4,230 | 0 |
| 405S | Bedford Park Blvd-Lehman College (4), Manhattan | 4,211 | 5,551 | 4,119 | 93 | 0 |
| 720S | Hunters Point Av (7), Manhattan | 4,184 | 7,301 | 3,003 | 1,180 | 5 |
| F05N | Briarwood (E F), Jamaica | 4,180 | 5,324 | 364 | 3,815 | 96 |
| 252N | Saratoga Av (3), Manhattan | 4,178 | 5,761 | 3,475 | 703 | 200 |
| B20N | 20 Av (D), Manhattan | 4,159 | 5,312 | 3,763 | 396 | 0 |
| 220N | Jackson Av (2 5), Northbound | 4,156 | 5,499 | 759 | 3,397 | 1 |
| J15S | Woodhaven Blvd (J Z), Manhattan | 4,154 | 4,913 | 2,373 | 1,781 | 41 |
| 208N | Gun Hill Rd (2 5), Northbound | 4,134 | 6,777 | 475 | 3,659 | 0 |
| B17N | 71 St (D), Manhattan | 4,126 | 5,927 | 3,520 | 606 | 0 |
| A57N | Grant Av (A), Manhattan | 4,117 | 6,107 | 3,799 | 318 | 10 |
| B17S | 71 St (D), Southbound | 4,097 | 5,885 | 629 | 3,468 | 0 |
| 405N | Bedford Park Blvd-Lehman College (4), Northbound | 4,089 | 5,395 | 91 | 3,999 | 0 |
| 618S | Brook Av (6), Manhattan | 4,084 | 6,295 | 3,438 | 646 | 0 |
| 601N | Pelham Bay Park (6), Last Stop | 4,082 | 6,848 | 0 | 4,082 | 0 |
| A49S | Ralph Av (C), Outbound | 4,077 | 5,841 | 788 | 3,289 | 0 |
| H11N | Far Rockaway-Mott Av (A), Manhattan | 4,074 | 7,127 | 4,074 | 0 | 0 |
| D09N | 170 St (B D), Northbound | 4,073 | 6,925 | 530 | 3,543 | 0 |
| 410N | 176 St (4), Northbound | 4,066 | 5,430 | 552 | 3,513 | 0 |
| L20N | Wilson Av (L), Manhattan | 4,054 | 4,722 | 2,990 | 1,064 | 0 |
| B20S | 20 Av (D), Southbound | 4,048 | 5,171 | 372 | 3,676 | 0 |
| F22N | Smith-9 Sts (F G), Northbound | 4,047 | 5,179 | 3,155 | 892 | 74 |
| 257N | New Lots Av (3), Manhattan | 4,046 | 5,847 | 4,046 | 0 | 112 |
| F22S | Smith-9 Sts (F G), Southbound | 4,028 | 5,158 | 881 | 3,147 | 74 |
| 408N | 183 St (4), Northbound | 4,007 | 5,747 | 355 | 3,652 | 0 |
| M05N | Forest Av (M), Inbound | 3,985 | 4,611 | 3,877 | 108 | 0 |
| 238N | Eastern Pkwy-Brooklyn Museum (2 3), Manhattan | 3,977 | 4,427 | 3,175 | 801 | 67 |
| B16S | 62 St (D), Southbound | 3,974 | 4,693 | 2,290 | 1,684 | 2,352 |
| A18S | 103 St (C B), Downtown | 3,971 | 5,115 | 3,099 | 873 | 0 |
| M13N | Lorimer St (M J), Outbound | 3,944 | 5,973 | 2,227 | 1,717 | 21 |
| J15N | Woodhaven Blvd (J Z), Jamaica | 3,928 | 4,664 | 1,729 | 2,199 | 11 |
| G07N | Jamaica-Van Wyck (E), Jamaica | 3,918 | 4,634 | 629 | 3,289 | 0 |
| M09N | Knickerbocker Av (M), Inbound | 3,904 | 5,050 | 2,715 | 1,188 | 0 |
| 253N | Rockaway Av (3), Manhattan | 3,897 | 5,365 | 3,061 | 836 | 210 |
| 106S | Marble Hill-225 St (1), Downtown | 3,896 | 5,480 | 3,744 | 152 | 0 |
| A57S | Grant Av (A), Queens | 3,889 | 5,781 | 302 | 3,587 | 10 |
| H03N | Howard Beach-JFK Airport (A), Manhattan | 3,883 | 3,595 | 3,578 | 305 | 315 |
| 720N | Hunters Point Av (7), Outbound | 3,881 | 6,789 | 1,015 | 2,866 | 5 |
| 106N | Marble Hill-225 St (1), The Bronx | 3,866 | 5,438 | 140 | 3,726 | 0 |
| 252S | Saratoga Av (3), New Lots | 3,866 | 5,349 | 646 | 3,220 | 200 |
| 618N | Brook Av (6), Northbound | 3,851 | 5,934 | 653 | 3,198 | 0 |
| A18N | 103 St (C B), Uptown | 3,821 | 4,915 | 821 | 3,000 | 0 |
| A50S | Rockaway Av (C), Outbound | 3,820 | 5,244 | 990 | 2,830 | 0 |
| L20S | Wilson Av (L), Outbound | 3,819 | 4,431 | 924 | 2,895 | 0 |
| 245N | Beverly Rd (2 5), Manhattan | 3,800 | 4,549 | 3,646 | 154 | 0 |
| 238S | Eastern Pkwy-Brooklyn Museum (2 3), Outbound | 3,779 | 4,206 | 643 | 3,136 | 67 |
| D38N | Neck Rd (Q), Manhattan | 3,778 | 4,713 | 3,138 | 640 | 0 |
| 103S | 238 St (1), Manhattan | 3,774 | 4,424 | 3,768 | 6 | 0 |
| 103N | 238 St (1), Van Cortlandt | 3,770 | 4,422 | 8 | 3,761 | 0 |
| M05S | Forest Av (M), Middle Village | 3,763 | 4,356 | 96 | 3,666 | 0 |
| N06N | 20 Av (N), Manhattan | 3,754 | 3,871 | 3,335 | 419 | 0 |
| M13S | Lorimer St (M J), Manhattan | 3,737 | 5,663 | 1,577 | 2,160 | 0 |
| G30N | Broadway (G), Queens | 3,731 | 4,451 | 2,624 | 1,107 | 0 |
| 604S | Westchester Sq-E Tremont Av (6), Manhattan | 3,726 | 6,544 | 3,521 | 205 | 0 |
| B13N | Fort Hamilton Pkwy (D), Manhattan | 3,724 | 4,249 | 2,757 | 967 | 0 |
| 416S | 138 St-Grand Concourse (4 5), Manhattan | 3,717 | 4,012 | 2,348 | 1,368 | 374 |
| 257S | New Lots Av (3), Last Stop | 3,704 | 5,353 | 0 | 3,704 | 112 |
| S04S | Botanic Garden (S), Prospect Park | 3,700 | 4,969 | 1,126 | 2,573 | 2,651 |
| B13S | Fort Hamilton Pkwy (D), Southbound | 3,674 | 4,192 | 965 | 2,709 | 0 |
| M19S | Bowery (J Z), Downtown | 3,665 | 4,702 | 1,518 | 2,148 | 0 |
| 411S | Mt Eden Av (4), Manhattan | 3,637 | 5,290 | 3,121 | 516 | 0 |
| 416N | 138 St-Grand Concourse (4 5), Northbound | 3,637 | 3,916 | 1,374 | 2,262 | 275 |
| 236S | Bergen St (2 3), Outbound | 3,607 | 3,883 | 703 | 2,903 | 5 |
| 249N | Kingston Av (3), Manhattan | 3,585 | 4,961 | 3,068 | 516 | 0 |
| 615S | E 149 St (6), Manhattan | 3,580 | 4,904 | 3,021 | 559 | 0 |
| 236N | Bergen St (2 3), Manhattan | 3,578 | 3,867 | 2,927 | 651 | 5 |
| R08N | 39 Av-Dutch Kills (N W), Astoria | 3,568 | 2,904 | 392 | 3,176 | 0 |
| N06S | 20 Av (N), Coney Island | 3,566 | 3,682 | 407 | 3,159 | 0 |
| 245S | Beverly Rd (2 5), Flatbush | 3,559 | 4,263 | 157 | 3,402 | 0 |
| 604N | Westchester Sq-E Tremont Av (6), Pelham Bay | 3,544 | 6,221 | 197 | 3,348 | 0 |
| J20S | Crescent St (J Z), Manhattan | 3,542 | 4,872 | 2,652 | 890 | 25 |
| A05S | 190 St (A), Downtown | 3,541 | 5,158 | 3,372 | 168 | 0 |
| A10S | 163 St-Amsterdam Av (C), Downtown | 3,537 | 4,943 | 2,832 | 706 | 0 |
| D08S | 174-175 Sts (B D), Manhattan | 3,522 | 5,401 | 2,973 | 548 | 0 |
| J20N | Crescent St (J Z), Outbound | 3,517 | 4,846 | 881 | 2,636 | 12 |
| R35N | 25 St (R), Manhattan | 3,506 | 4,325 | 2,542 | 964 | 25 |
| D06S | 182-183 Sts (B D), Manhattan | 3,501 | 5,162 | 3,122 | 379 | 0 |
| F04S | Sutphin Blvd (F), Manhattan | 3,500 | 4,525 | 3,209 | 292 | 0 |
| M10N | Central Av (M), Inbound | 3,494 | 4,855 | 2,703 | 791 | 0 |
| A05N | 190 St (A), Uptown | 3,476 | 5,051 | 134 | 3,341 | 0 |
| A59N | 80 St (A), Manhattan | 3,474 | 4,732 | 3,107 | 367 | 57 |
| 216S | Freeman St (2 5), Manhattan | 3,470 | 4,719 | 2,923 | 547 | 122 |
| 615N | E 149 St (6), Northbound | 3,469 | 4,768 | 609 | 2,861 | 0 |
| H11S | Far Rockaway-Mott Av (A), Last Stop | 3,468 | 6,069 | 0 | 3,468 | 0 |
| D38S | Neck Rd (Q), Southbound | 3,466 | 4,327 | 594 | 2,872 | 0 |
| 609S | St Lawrence Av (6), Manhattan | 3,440 | 4,484 | 2,910 | 530 | 0 |
| R08S | 39 Av-Dutch Kills (N W), Manhattan | 3,437 | 2,796 | 3,109 | 328 | 0 |
| M19N | Bowery (J Z), Brooklyn | 3,428 | 4,394 | 1,860 | 1,569 | 0 |
| D42N | W 8 St-NY Aquarium (F Q), Manhattan | 3,399 | 4,312 | 3,261 | 138 | 1,318 |
| G20S | 36 St (M R), Manhattan | 3,388 | 5,397 | 2,298 | 1,090 | 135 |
| A59S | 80 St (A), Outbound | 3,385 | 4,613 | 322 | 3,063 | 53 |
| D42S | W 8 St-NY Aquarium (F Q), Coney Island | 3,378 | 4,290 | 123 | 3,255 | 1,318 |
| 411N | Mt Eden Av (4), Northbound | 3,368 | 4,908 | 520 | 2,849 | 0 |
| G15S | 65 St (M R), Manhattan | 3,361 | 4,102 | 2,154 | 1,207 | 1 |
| B22N | 25 Av (D), Manhattan | 3,349 | 5,198 | 3,021 | 327 | 0 |
| F04N | Sutphin Blvd (F), Jamaica | 3,345 | 4,335 | 311 | 3,034 | 0 |
| M09S | Knickerbocker Av (M), Middle Village | 3,333 | 4,346 | 1,085 | 2,247 | 0 |
| N09N | Avenue U (N), Manhattan | 3,330 | 3,469 | 3,045 | 285 | 0 |
| S04N | Botanic Garden (S), Franklin Av | 3,328 | 4,416 | 2,391 | 938 | 2,337 |
| M01N | Middle Village-Metropolitan Av (M), Inbound | 3,308 | 3,926 | 3,308 | 0 | 0 |
| 216N | Freeman St (2 5), Northbound | 3,291 | 4,454 | 505 | 2,785 | 0 |
| 253S | Rockaway Av (3), New Lots | 3,251 | 4,474 | 696 | 2,555 | 210 |
| B22S | 25 Av (D), Coney Island | 3,208 | 4,981 | 297 | 2,911 | 0 |
| F29N | Ditmas Av (F), Manhattan | 3,205 | 4,211 | 2,577 | 628 | 0 |
| N09S | Avenue U (N), Coney Island | 3,198 | 3,328 | 228 | 2,970 | 0 |
| 503N | Gun Hill Rd (5), Eastchester | 3,186 | 4,500 | 59 | 3,127 | 0 |
| 503S | Gun Hill Rd (5), Manhattan | 3,186 | 4,498 | 3,127 | 59 | 0 |
| 210S | Allerton Av (2 5), Manhattan | 3,160 | 5,435 | 2,886 | 274 | 0 |
| 249S | Kingston Av (3), Outbound | 3,155 | 4,387 | 461 | 2,695 | 0 |
| 255N | Pennsylvania Av (3), Manhattan | 3,149 | 5,004 | 3,106 | 44 | 246 |
| A10N | 163 St-Amsterdam Av (C), Uptown | 3,136 | 4,383 | 511 | 2,625 | 0 |
| 501S | Eastchester-Dyre Av (5), Manhattan | 3,126 | 5,203 | 3,126 | 0 | 0 |
| D06N | 182-183 Sts (B D), Northbound | 3,125 | 4,623 | 304 | 2,821 | 0 |
| D29N | Beverley Rd (Q), Manhattan | 3,112 | 3,276 | 2,661 | 451 | 0 |
| M10S | Central Av (M), Middle Village | 3,095 | 4,327 | 728 | 2,367 | 0 |
| M01S | Middle Village-Metropolitan Av (M), Last Stop | 3,093 | 3,673 | 0 | 3,093 | 0 |
| 609N | St Lawrence Av (6), Northbound | 3,092 | 4,033 | 441 | 2,651 | 0 |
| 255S | Pennsylvania Av (3), New Lots | 3,072 | 4,881 | 45 | 3,027 | 246 |
| 210N | Allerton Av (2 5), Northbound | 3,066 | 5,277 | 265 | 2,802 | 0 |
| D08N | 174-175 Sts (B D), Northbound | 3,066 | 4,719 | 437 | 2,629 | 0 |
| R35S | 25 St (R), Southbound | 3,065 | 3,773 | 751 | 2,314 | 25 |
| G15N | 65 St (M R), Outbound | 3,006 | 3,686 | 1,065 | 1,941 | 1 |
| D29S | Beverley Rd (Q), Southbound | 3,004 | 3,166 | 459 | 2,546 | 0 |
| F29S | Ditmas Av (F), Southbound | 2,984 | 3,915 | 602 | 2,382 | 0 |
| L27N | New Lots Av (L), Manhattan | 2,973 | 4,637 | 2,790 | 183 | 243 |
| 241N | President St-Medgar Evers College (2 5), Manhattan | 2,972 | 3,859 | 2,540 | 432 | 0 |
| 241S | President St-Medgar Evers College (2 5), Flatbush | 2,937 | 3,814 | 447 | 2,490 | 0 |
| J17S | 75 St-Elderts Ln (J Z), Manhattan | 2,931 | 3,417 | 1,939 | 992 | 0 |
| 501N | Eastchester-Dyre Av (5), Last Stop | 2,929 | 4,878 | 0 | 2,929 | 0 |
| 602S | Buhre Av (6), Manhattan | 2,923 | 4,101 | 2,850 | 73 | 0 |
| J16S | 85 St-Forest Pkwy (J), Manhattan | 2,913 | 5,335 | 1,754 | 1,159 | 0 |
| 201S | Wakefield-241 St (2), Manhattan | 2,893 | 4,673 | 2,893 | 0 | 0 |
| F30N | 18 Av (F), Manhattan | 2,893 | 3,926 | 2,257 | 637 | 0 |
| B14N | 50 St (D), Manhattan | 2,875 | 3,411 | 1,831 | 1,044 | 0 |
| L27S | New Lots Av (L), Canarsie | 2,861 | 4,468 | 188 | 2,672 | 243 |
| J17N | 75 St-Elderts Ln (J Z), Jamaica | 2,832 | 3,313 | 958 | 1,873 | 0 |
| B14S | 50 St (D), Southbound | 2,781 | 3,305 | 1,039 | 1,742 | 0 |
| F07S | 75 Av (E F), Manhattan | 2,778 | 3,837 | 2,380 | 399 | 3 |
| 205S | 233 St (2 5), Manhattan | 2,773 | 4,909 | 2,725 | 48 | 0 |
| G31S | Flushing Av (G), Southbound | 2,767 | 2,613 | 1,151 | 1,615 | 0 |
| A60N | 88 St (A), Manhattan | 2,763 | 3,869 | 2,372 | 390 | 436 |
| F30S | 18 Av (F), Southbound | 2,761 | 3,745 | 593 | 2,169 | 0 |
| J28S | Chauncey St (J Z), Manhattan | 2,760 | 3,926 | 1,579 | 1,181 | 0 |
| 602N | Buhre Av (6), Pelham Bay | 2,749 | 3,851 | 58 | 2,691 | 0 |
| D32N | Avenue H (Q), Manhattan | 2,738 | 3,545 | 2,064 | 674 | 0 |
| J16N | 85 St-Forest Pkwy (J), Jamaica | 2,738 | 5,031 | 1,096 | 1,642 | 0 |
| H04N | Broad Channel (A S), Inbound | 2,731 | 5,826 | 1,352 | 1,379 | 2,519 |
| 248S | Nostrand Av (3), Outbound | 2,724 | 4,316 | 739 | 1,986 | 0 |
| F07N | 75 Av (E F), Jamaica | 2,714 | 3,760 | 352 | 2,362 | 3 |
| D32S | Avenue H (Q), Southbound | 2,704 | 3,504 | 688 | 2,016 | 0 |
| 205N | 233 St (2 5), Northbound | 2,670 | 4,728 | 44 | 2,627 | 0 |
| 248N | Nostrand Av (3), Manhattan | 2,660 | 4,195 | 2,019 | 641 | 0 |
| H04S | Broad Channel (A S), Rockaways | 2,639 | 5,653 | 1,334 | 1,304 | 2,431 |
| G31N | Flushing Av (G), Queens | 2,638 | 2,477 | 1,582 | 1,057 | 0 |
| 201N | Wakefield-241 St (2), Last Stop | 2,631 | 4,253 | 0 | 2,631 | 0 |
| H03S | Howard Beach-JFK Airport (A), Rockaways | 2,631 | 2,720 | 317 | 2,313 | 315 |
| 218S | Intervale Av (2 5), Manhattan | 2,588 | 3,423 | 2,131 | 457 | 0 |
| M06N | Seneca Av (M), Inbound | 2,570 | 3,488 | 2,461 | 109 | 0 |
| J23S | Van Siclen Av (J Z), Manhattan | 2,550 | 2,879 | 2,038 | 512 | 0 |
| A53N | Van Siclen Av (C), Manhattan | 2,513 | 3,290 | 2,230 | 283 | 1 |
| 218N | Intervale Av (2 5), Northbound | 2,464 | 3,274 | 486 | 1,979 | 31 |
| 504S | Pelham Pkwy (5), Manhattan | 2,456 | 3,459 | 2,305 | 151 | 0 |
| L25N | Sutter Av (L), Manhattan | 2,449 | 3,804 | 1,918 | 532 | 259 |
| J23N | Van Siclen Av (J Z), Outbound | 2,446 | 2,765 | 557 | 1,890 | 0 |
| 614S | Longwood Av (6), Manhattan | 2,434 | 3,319 | 1,857 | 577 | 0 |
| M06S | Seneca Av (M), Middle Village | 2,404 | 3,260 | 127 | 2,277 | 0 |
| D41N | Ocean Pkwy (Q), Manhattan | 2,387 | 3,322 | 2,003 | 384 | 0 |
| A60S | 88 St (A), Outbound | 2,386 | 3,299 | 220 | 2,166 | 126 |
| B23N | Bay 50 St (D), Manhattan | 2,378 | 2,880 | 1,966 | 412 | 0 |
| 504N | Pelham Pkwy (5), Eastchester | 2,369 | 3,361 | 192 | 2,178 | 0 |
| M14N | Hewes St (M J), Outbound | 2,364 | 3,659 | 1,476 | 888 | 0 |
| D41S | Ocean Pkwy (Q), Coney Island | 2,350 | 3,267 | 401 | 1,949 | 0 |
| 302S | 145 St (3), Downtown | 2,339 | 3,409 | 2,339 | 0 | 0 |
| J14S | 104 St (J Z), Manhattan | 2,336 | 2,952 | 1,123 | 1,213 | 0 |
| 204S | Nereid Av (2 5), Manhattan | 2,332 | 3,932 | 2,218 | 114 | 228 |
| 617S | Cypress Av (6), Manhattan | 2,328 | 3,715 | 1,970 | 358 | 0 |
| B23S | Bay 50 St (D), Coney Island | 2,301 | 2,788 | 397 | 1,904 | 0 |
| L28N | East 105 St (L), Manhattan | 2,299 | 3,741 | 2,232 | 67 | 32 |
| L25S | Sutter Av (L), Canarsie | 2,288 | 3,550 | 480 | 1,807 | 259 |
| 614N | Longwood Av (6), Northbound | 2,270 | 3,115 | 516 | 1,754 | 0 |
| 301S | Harlem-148 St (3), Downtown | 2,269 | 3,808 | 2,269 | 0 | 0 |
| F35N | Kings Hwy (F), Manhattan | 2,268 | 3,587 | 1,868 | 400 | 0 |
| A53S | Van Siclen Av (C), Outbound | 2,260 | 2,963 | 228 | 2,032 | 1 |
| J28N | Chauncey St (J Z), Outbound | 2,250 | 3,219 | 964 | 1,286 | 0 |
| J21S | Norwood Av (J Z), Manhattan | 2,225 | 3,584 | 1,764 | 461 | 0 |
| J14N | 104 St (J Z), Jamaica | 2,220 | 2,815 | 1,189 | 1,031 | 0 |
| J21N | Norwood Av (J Z), Outbound | 2,214 | 3,580 | 452 | 1,762 | 0 |
| 505S | Morris Park (5), Manhattan | 2,209 | 2,723 | 2,136 | 73 | 0 |
| F33N | Avenue N (F), Manhattan | 2,201 | 3,216 | 1,887 | 314 | 0 |
| 302N | 145 St (3), Harlem | 2,200 | 3,209 | 0 | 2,200 | 0 |
| A54N | Shepherd Av (C), Manhattan | 2,190 | 3,566 | 1,743 | 447 | 4 |
| 206S | 225 St (2 5), Manhattan | 2,189 | 3,977 | 2,116 | 73 | 0 |
| F34N | Avenue P (F), Manhattan | 2,160 | 2,779 | 1,832 | 328 | 0 |
| D12S | 155 St (B D), Downtown | 2,157 | 3,786 | 1,483 | 674 | 0 |
| L21N | Bushwick Av-Aberdeen St (L), Manhattan | 2,154 | 2,290 | 1,619 | 535 | 0 |
| 617N | Cypress Av (6), Northbound | 2,152 | 3,433 | 332 | 1,820 | 0 |
| L28S | East 105 St (L), Canarsie | 2,152 | 3,499 | 54 | 2,098 | 32 |
| 502S | Baychester Av (5), Manhattan | 2,134 | 4,054 | 2,117 | 17 | 0 |
| F35S | Kings Hwy (F), Southbound | 2,110 | 3,346 | 345 | 1,765 | 0 |
| A11S | 155 St (C), Downtown | 2,100 | 3,044 | 1,817 | 283 | 0 |
| A52N | Liberty Av (C), Manhattan | 2,099 | 3,078 | 1,927 | 172 | 0 |
| M14S | Hewes St (M J), Manhattan | 2,094 | 3,231 | 769 | 1,325 | 0 |
| L24N | Atlantic Av (L), Manhattan | 2,089 | 1,741 | 1,597 | 492 | 127 |
| 301N | Harlem-148 St (3), Last Stop | 2,085 | 3,501 | 0 | 2,085 | 0 |
| D12N | 155 St (B D), The Bronx | 2,076 | 3,659 | 684 | 1,392 | 0 |
| J13S | 111 St (J), Manhattan | 2,065 | 1,290 | 1,024 | 1,041 | 3 |
| 207S | 219 St (2 5), Manhattan | 2,064 | 3,541 | 1,973 | 92 | 0 |
| 502N | Baychester Av (5), Eastchester | 2,052 | 3,900 | 17 | 2,035 | 0 |
| 206N | 225 St (2 5), Northbound | 2,049 | 3,721 | 66 | 1,982 | 0 |
| F33S | Avenue N (F), Southbound | 2,049 | 2,999 | 282 | 1,767 | 0 |
| 505N | Morris Park (5), Eastchester | 2,048 | 2,527 | 73 | 1,976 | 0 |
| 204N | Nereid Av (2 5), Northbound | 2,044 | 3,468 | 42 | 2,001 | 85 |
| F34S | Avenue P (F), Southbound | 2,038 | 2,629 | 304 | 1,735 | 0 |
| G24S | 21 St (G), Brooklyn | 2,034 | 2,233 | 1,431 | 603 | 0 |
| L24S | Atlantic Av (L), Canarsie | 2,033 | 1,713 | 567 | 1,466 | 127 |
| A52S | Liberty Av (C), Outbound | 2,015 | 2,957 | 168 | 1,847 | 0 |
| N10N | 86 St (N), Manhattan | 2,012 | 2,387 | 1,787 | 225 | 2 |
| J12S | 121 St (J Z), Manhattan | 2,006 | 2,536 | 1,099 | 907 | 0 |
| F38N | Avenue X (F), Manhattan | 1,984 | 2,775 | 1,657 | 328 | 0 |
| J22S | Cleveland St (J), Manhattan | 1,974 | 3,340 | 1,492 | 482 | 2 |
| 209S | Burke Av (2 5), Manhattan | 1,973 | 3,513 | 1,846 | 128 | 0 |
| 256N | Van Siclen Av (3), Manhattan | 1,966 | 3,145 | 1,966 | 0 | 143 |
| J22N | Cleveland St (J), Outbound | 1,948 | 3,307 | 485 | 1,462 | 2 |
| J13N | 111 St (J), Jamaica | 1,935 | 1,211 | 996 | 939 | 3 |
| 107N | 215 St (1), The Bronx | 1,901 | 1,930 | 198 | 1,704 | 0 |
| A11N | 155 St (C), Uptown | 1,900 | 2,757 | 212 | 1,688 | 0 |
| N10S | 86 St (N), Coney Island | 1,890 | 2,238 | 193 | 1,697 | 8 |
| A54S | Shepherd Av (C), Outbound | 1,874 | 3,053 | 307 | 1,567 | 4 |
| 256S | Van Siclen Av (3), New Lots | 1,868 | 2,987 | 0 | 1,868 | 143 |
| 207N | 219 St (2 5), Northbound | 1,859 | 3,189 | 87 | 1,772 | 0 |
| 606S | Zerega Av (6), Manhattan | 1,859 | 2,784 | 1,747 | 112 | 0 |
| 212S | Bronx Park East (2 5), Manhattan | 1,852 | 2,734 | 1,607 | 245 | 0 |
| J12N | 121 St (J Z), Jamaica | 1,848 | 2,332 | 846 | 1,003 | 0 |
| F38S | Avenue X (F), Coney Island | 1,820 | 2,555 | 268 | 1,552 | 0 |
| L21S | Bushwick Av-Aberdeen St (L), Outbound | 1,796 | 1,900 | 347 | 1,449 | 0 |
| 107S | 215 St (1), Downtown | 1,795 | 1,816 | 1,634 | 161 | 0 |
| 209N | Burke Av (2 5), Northbound | 1,794 | 3,176 | 84 | 1,709 | 0 |
| 212N | Bronx Park East (2 5), Northbound | 1,765 | 2,604 | 233 | 1,532 | 0 |
| 606N | Zerega Av (6), Pelham Bay | 1,729 | 2,583 | 100 | 1,629 | 0 |
| J24N | Alabama Av (J Z), Outbound | 1,722 | 2,431 | 910 | 812 | 1 |
| A64N | 111 St (A), Manhattan | 1,691 | 2,737 | 1,691 | 0 | 0 |
| F36N | Avenue U (F), Manhattan | 1,690 | 2,091 | 1,388 | 302 | 0 |
| 616S | E 143 St-St Mary's St (6), Manhattan | 1,651 | 1,210 | 1,355 | 296 | 0 |
| A64S | 111 St (A), Ozone Park | 1,635 | 2,648 | 0 | 1,635 | 0 |
| H06N | Beach 67 St (A), Manhattan | 1,620 | 3,479 | 1,446 | 174 | 0 |
| 616N | E 143 St-St Mary's St (6), Northbound | 1,587 | 1,163 | 274 | 1,313 | 0 |
| B15N | 55 St (D), Manhattan | 1,573 | 2,234 | 1,090 | 483 | 0 |
| 603S | Middletown Rd (6), Manhattan | 1,569 | 2,194 | 1,506 | 63 | 0 |
| J24S | Alabama Av (J Z), Manhattan | 1,558 | 2,193 | 764 | 795 | 36 |
| F36S | Avenue U (F), Coney Island | 1,546 | 1,924 | 241 | 1,304 | 0 |
| H06S | Beach 67 St (A), Far Rockaway | 1,543 | 3,295 | 149 | 1,394 | 0 |
| S03S | Park Pl (S), Prospect Park | 1,528 | 1,854 | 1,053 | 475 | 0 |
| B15S | 55 St (D), Southbound | 1,505 | 2,145 | 468 | 1,037 | 0 |
| 603N | Middletown Rd (6), Pelham Bay | 1,446 | 2,018 | 52 | 1,394 | 0 |
| A63N | 104 St (A), Manhattan | 1,439 | 1,925 | 1,410 | 29 | 0 |
| A63S | 104 St (A), Ozone Park | 1,372 | 1,837 | 28 | 1,344 | 0 |
| F39N | Neptune Av (F), Manhattan | 1,357 | 1,686 | 1,001 | 355 | 0 |
| 612S | Whitlock Av (6), Manhattan | 1,344 | 1,973 | 1,162 | 181 | 0 |
| 612N | Whitlock Av (6), Northbound | 1,335 | 1,972 | 208 | 1,128 | 0 |
| S03N | Park Pl (S), Franklin Av | 1,292 | 1,572 | 398 | 894 | 0 |
| G24N | 21 St (G), Court Square | 1,290 | 1,409 | 189 | 1,102 | 0 |
| H07N | Beach 60 St (A), Manhattan | 1,257 | 3,312 | 1,099 | 158 | 0 |
| F31S | Avenue I (F), Southbound | 1,237 | 2,064 | 336 | 902 | 0 |
| F31N | Avenue I (F), Manhattan | 1,228 | 2,050 | 908 | 320 | 0 |
| H07S | Beach 60 St (A), Far Rockaway | 1,152 | 3,020 | 133 | 1,019 | 0 |
| F39S | Neptune Av (F), Coney Island | 1,136 | 1,412 | 241 | 895 | 0 |
| H10N | Beach 25 St (A), Manhattan | 1,116 | 2,878 | 1,038 | 78 | 0 |
| H01N | Aqueduct Racetrack (A), Manhattan | 1,032 | 3,402 | 492 | 540 | 0 |
| H10S | Beach 25 St (A), Far Rockaway | 1,023 | 2,634 | 67 | 956 | 0 |
| J19S | Cypress Hills (J), Manhattan | 941 | 2,329 | 608 | 333 | 4 |
| J19N | Cypress Hills (J), Queens | 939 | 2,327 | 351 | 588 | 4 |
| F32N | Bay Pkwy (F), Manhattan | 920 | 1,333 | 748 | 172 | 0 |
| H02N | Aqueduct-N Conduit Av (A), Manhattan | 903 | 1,669 | 827 | 75 | 204 |
| H02S | Aqueduct-N Conduit Av (A), Rockaways | 878 | 1,637 | 73 | 805 | 204 |
| F32S | Bay Pkwy (F), Southbound | 866 | 1,259 | 150 | 716 | 0 |
| H09N | Beach 36 St (A), Manhattan | 584 | 1,619 | 540 | 44 | 0 |
| H12S | Beach 90 St (A S), Rockaway Park | 549 | 1,336 | 13 | 536 | 0 |
| H12N | Beach 90 St (A S), Inbound | 547 | 1,341 | 529 | 19 | 0 |
| H08N | Beach 44 St (A), Manhattan | 524 | 1,165 | 460 | 64 | 0 |
| H09S | Beach 36 St (A), Far Rockaway | 520 | 1,413 | 28 | 492 | 0 |
| H15N | Rockaway Park-Beach 116 St (A S), Inbound | 495 | 1,003 | 495 | 0 | 0 |
| H08S | Beach 44 St (A), Far Rockaway | 466 | 1,033 | 52 | 414 | 0 |
| H15S | Rockaway Park-Beach 116 St (A S), Last Stop | 395 | 799 | 0 | 395 | 0 |
| H13N | Beach 98 St (A S), Inbound | 312 | 682 | 301 | 11 | 0 |
| H13S | Beach 98 St (A S), Rockaway Park | 291 | 632 | 7 | 284 | 0 |
| H14N | Beach 105 St (A S), Inbound | 201 | 330 | 198 | 3 | 0 |
| H14S | Beach 105 St (A S), Rockaway Park | 191 | 310 | 0 | 191 | 0 |
