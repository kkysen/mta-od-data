# Regional flow: Lower Manhattan (below 60th St / Congestion Relief Zone)

Scenario: average weekday ridership (60 distinct days in the data, 2025-01-06 to 2025-12-12), every origin/destination pair classified by whether each end falls inside Lower Manhattan (below 60th St / Congestion Relief Zone).

Produced by `mta-od-data analyze regional-flow --markdown-out src/mta_od_data/analyze/regional_flow.md`.

---

## Headline numbers

Total: 3,962,101 riders/weekday

| Flow | Riders | % Total |
| --- | --- | --- |
| Outside -> Inside | 947,666 | 23.9% |
| Inside -> Outside | 904,092 | 22.8% |
| Inside -> Inside | 733,579 | 18.5% |
| Outside -> Outside | 1,376,766 | 34.7% |
| **Inter** | 1,851,757 | 46.7% |
| **Intra** | 2,110,344 | 53.3% |

## Top 25 origin/destination pairs

| # | Riders | % Total | Flow | Origin -> Destination |
| --- | --- | --- | --- | --- |
| 1 | 6,160 | 0.16% | in→in | Grand Central-42 St → Fulton St |
| 2 | 6,084 | 0.15% | in→in | Fulton St → Grand Central-42 St |
| 3 | 4,381 | 0.11% | in→in | Times Sq-42 St/PABT → Grand Central-42 St |
| 4 | 4,284 | 0.11% | in→in | Grand Central-42 St → 14 St-Union Sq |
| 5 | 4,276 | 0.11% | in→in | Grand Central-42 St → Times Sq-42 St/PABT |
| 6 | 3,771 | 0.10% | in→in | 14 St-Union Sq → Grand Central-42 St |
| 7 | 2,981 | 0.08% | in→in | Times Sq-42 St/PABT → Chambers St/WTC/Park Pl/Cortlandt St |
| 8 | 2,847 | 0.07% | in→in | Chambers St/WTC/Park Pl/Cortlandt St → Times Sq-42 St/PABT |
| 9 | 2,839 | 0.07% | out→in | 86 St → Grand Central-42 St |
| 10 | 2,831 | 0.07% | in→in | Times Sq-42 St/PABT → 14 St-Union Sq |
| 11 | 2,829 | 0.07% | in→in | Times Sq-42 St/PABT → Fulton St |
| 12 | 2,738 | 0.07% | in→in | Times Sq-42 St/PABT → 59 St-Columbus Circle |
| 13 | 2,728 | 0.07% | in→out | Grand Central-42 St → 86 St |
| 14 | 2,646 | 0.07% | in→in | 34 St-Herald Sq → 47-50 Sts-Rockefeller Ctr |
| 15 | 2,622 | 0.07% | in→in | Grand Central-42 St → 34 St-Hudson Yards |
| 16 | 2,592 | 0.07% | in→in | 59 St-Columbus Circle → Times Sq-42 St/PABT |
| 17 | 2,589 | 0.07% | in→in | 34 St-Hudson Yards → Grand Central-42 St |
| 18 | 2,584 | 0.07% | in→in | 14 St-Union Sq → Times Sq-42 St/PABT |
| 19 | 2,571 | 0.06% | in→in | 34 St-Penn Station → Grand Central-42 St |
| 20 | 2,541 | 0.06% | in→in | Grand Central-42 St → Brooklyn Bridge-City Hall/Chambers St |
| 21 | 2,541 | 0.06% | in→in | Brooklyn Bridge-City Hall/Chambers St → Grand Central-42 St |
| 22 | 2,512 | 0.06% | in→in | 34 St-Penn Station → 59 St-Columbus Circle |
| 23 | 2,500 | 0.06% | in→in | Fulton St → Times Sq-42 St/PABT |
| 24 | 2,496 | 0.06% | in→in | Grand Central-42 St → 34 St-Penn Station |
| 25 | 2,464 | 0.06% | in→in | Times Sq-42 St/PABT → Lexington Av/51-53 Sts |
