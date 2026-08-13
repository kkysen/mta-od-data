# Regional flow: Lower Manhattan (below 60th St / Congestion Relief Zone)

Scenario: average weekday ridership (35 distinct days in the data, 2024-01-08 to 2024-07-12), every origin/destination pair classified by whether each end falls inside Lower Manhattan (below 60th St / Congestion Relief Zone).

Produced by `mta-od-data analyze regional-flow --markdown-out src/mta_od_data/analyze/regional_flow.md`.

---

## Headline numbers

Total: 3,622,680 riders/weekday

| Flow | Riders | % Total |
| --- | --- | --- |
| Outside -> Inside | 873,734 | 24.1% |
| Inside -> Outside | 830,377 | 22.9% |
| Inside -> Inside | 673,037 | 18.6% |
| Outside -> Outside | 1,245,532 | 34.4% |
| **Inter** | 1,704,111 | 47.0% |
| **Intra** | 1,918,569 | 53.0% |

## Top 25 origin/destination pairs

| # | Riders | % Total | Flow | Origin -> Destination |
| --- | --- | --- | --- | --- |
| 1 | 5,538 | 0.15% | in→in | Grand Central-42 St → Fulton St |
| 2 | 5,448 | 0.15% | in→in | Fulton St → Grand Central-42 St |
| 3 | 4,148 | 0.11% | in→in | Times Sq-42 St/PABT → Grand Central-42 St |
| 4 | 4,020 | 0.11% | in→in | Grand Central-42 St → Times Sq-42 St/PABT |
| 5 | 3,859 | 0.11% | in→in | Grand Central-42 St → 14 St-Union Sq |
| 6 | 3,407 | 0.09% | in→in | 14 St-Union Sq → Grand Central-42 St |
| 7 | 2,737 | 0.08% | in→in | Times Sq-42 St/PABT → Chambers St/WTC/Park Pl/Cortlandt St |
| 8 | 2,713 | 0.07% | out→in | 86 St → Grand Central-42 St |
| 9 | 2,625 | 0.07% | in→in | Chambers St/WTC/Park Pl/Cortlandt St → Times Sq-42 St/PABT |
| 10 | 2,615 | 0.07% | in→in | Times Sq-42 St/PABT → 59 St-Columbus Circle |
| 11 | 2,600 | 0.07% | in→out | Grand Central-42 St → 86 St |
| 12 | 2,577 | 0.07% | in→in | Times Sq-42 St/PABT → 14 St-Union Sq |
| 13 | 2,533 | 0.07% | in→in | Times Sq-42 St/PABT → Fulton St |
| 14 | 2,486 | 0.07% | in→in | 34 St-Herald Sq → 47-50 Sts-Rockefeller Ctr |
| 15 | 2,479 | 0.07% | in→in | 59 St-Columbus Circle → Times Sq-42 St/PABT |
| 16 | 2,423 | 0.07% | out→out | Junction Blvd → Flushing-Main St |
| 17 | 2,364 | 0.07% | in→in | Times Sq-42 St/PABT → 14 St/8 Av |
| 18 | 2,361 | 0.07% | in→in | 34 St-Penn Station → 59 St-Columbus Circle |
| 19 | 2,357 | 0.07% | in→in | 14 St-Union Sq → Times Sq-42 St/PABT |
| 20 | 2,349 | 0.06% | in→in | Grand Central-42 St → Brooklyn Bridge-City Hall/Chambers St |
| 21 | 2,335 | 0.06% | out→out | Flushing-Main St → 103 St-Corona Plaza |
| 22 | 2,323 | 0.06% | in→in | Brooklyn Bridge-City Hall/Chambers St → Grand Central-42 St |
| 23 | 2,320 | 0.06% | out→out | Flushing-Main St → Junction Blvd |
| 24 | 2,319 | 0.06% | out→out | 103 St-Corona Plaza → Flushing-Main St |
| 25 | 2,300 | 0.06% | in→in | 34 St-Penn Station → Grand Central-42 St |
