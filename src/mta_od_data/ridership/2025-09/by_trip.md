# Ridership by trip

Average weekday riders with fare evaders, over 22 weekdays from 2025-09-16 to 2025-09-22 (as `raptor assign-range` routes them).
A train's load is its riders on board between two stops, averaged over the weekdays it runs: a train is the same on any date with the same route, direction, first stop, and departure from it.

Produced by `mta-od-data ridership --by trip --month 2025-09 --markdown-out src/mta_od_data/ridership/2025-09/by_trip.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Train | Peak Load, Sep 2025 | Train Length (ft) | Peak per Car\* | Peak Between | Leaving At | Weekdays Run |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| E | 8:27 AM Jamaica Center-Parsons/Archer to World Trade Center | 1,539 | 600 | 154 | Court Sq-23 St to Lexington Av/53 St | 8:51 AM | 22 |
| F | 8:43 AM Jamaica-179 St to Coney Island-Stillwell Av | 1,499 | 600 | 150 | Roosevelt Island to Lexington Av/63 St | 9:10 AM | 22 |
| 5 | 8:00 AM Flatbush Av-Brooklyn College to Eastchester-Dyre Av | 1,324 | 510 | 156 | 14 St-Union Sq to Grand Central-42 St | 8:39 AM | 22 |
| 4 | 4:58 PM Woodlawn to New Lots Av | 1,314 | 510 | 155 | Grand Central-42 St to 14 St-Union Sq | 5:37 PM | 22 |
| 7 | 7:14 AM Flushing-Main St to 34 St-Hudson Yards | 1,283 | 561 | 137 | 82 St-Jackson Hts to 74 St-Broadway | 7:25 AM | 22 |
| L | 5:40 PM 8 Av to Canarsie-Rockaway Pkwy | 1,258 | 480 | 157 | 14 St-Union Sq to 3 Av | 5:44 PM | 22 |
| Q | 8:08 AM Coney Island-Stillwell Av to 96 St | 1,233 | 600 | 123 | DeKalb Av to Canal St | 8:44 AM | 22 |
| B | 5:07 PM Bedford Park Blvd to Brighton Beach | 1,223 | 600 | 122 | 42 St-Bryant Pk to 34 St-Herald Sq | 5:46 PM | 22 |
| A | 7:29 AM Inwood-207 St to Far Rockaway-Mott Av | 1,172 | 600 | 117 | 125 St to 59 St-Columbus Circle | 7:47 AM | 22 |
| N | 8:17 AM Coney Island-Stillwell Av to 96 St | 1,114 | 600 | 111 | Atlantic Av to Canal St | 8:51 AM | 22 |
| D | 7:43 AM Norwood-205 St to Coney Island-Stillwell Av | 1,091 | 600 | 109 | 7 Av to 47-50 Sts-Rockefeller Ctr | 8:17 AM | 22 |
| FX | 4:58 PM Jamaica-179 St to Coney Island-Stillwell Av | 1,086 | 600 | 109 | Broadway-Lafayette St to 2 Av | 5:45 PM | 22 |
| W | 8:50 AM Astoria-Ditmars Blvd to Whitehall St-South Ferry | 1,086 | 600 | 109 | Queensboro Plaza to Lexington Av/59 St | 9:01 AM | 22 |
| 3 | 8:01 AM 145 St to New Lots Av | 988 | 510 | 116 | 34 St-Penn Station to 14 St | 8:21 AM | 22 |
| C | 8:24 AM Euclid Av to 168 St | 979 | 600 | 98 | High St to Fulton St | 8:51 AM | 22 |
| 6 | 8:20 AM Parkchester to Brooklyn Bridge-City Hall | 932 | 510 | 110 | 77 St to 68 St-Hunter College | 8:49 AM | 22 |
| 2 | 7:29 AM Wakefield-241 St to Flatbush Av-Brooklyn College | 924 | 510 | 109 | 72 St to Times Sq-42 St | 8:22 AM | 22 |
| 7X | 5:12 PM 34 St-Hudson Yards to Flushing-Main St | 924 | 561 | 99 | 74 St-Broadway to Junction Blvd | 5:39 PM | 22 |
| 1 | 7:19 AM South Ferry to Van Cortlandt Park-242 St | 918 | 510 | 108 | Times Sq-42 St to 50 St | 7:36 AM | 22 |
| 6X | 8:46 AM Pelham Bay Park to Brooklyn Bridge-City Hall | 913 | 510 | 107 | 3 Av-138 St to 125 St | 9:11 AM | 22 |
| R | 8:04 AM Bay Ridge-95 St to Forest Hills-71 Av | 830 | 600 | 83 | Atlantic Av to DeKalb Av | 8:26 AM | 22 |
| M | 8:32 AM Forest Hills-71 Av to Middle Village-Metropolitan Av | 804 | 480 | 100 | Elmhurst Av to Jackson Hts-Roosevelt Av | 8:41 AM | 22 |
| J | 8:22 AM Jamaica Center-Parsons/Archer to Broad St | 731 | 480 | 91 | Marcy Av to Delancey St-Essex St | 8:59 AM | 22 |
| G | 8:06 AM Church Av to Court Sq | 576 | 300 | 115 | Greenpoint Av to 21 St | 8:38 AM | 22 |
| Z | 7:52 AM Jamaica Center-Parsons/Archer to Broad St | 540 | 480 | 67 | Marcy Av to Delancey St-Essex St | 8:24 AM | 22 |
| GS | 5:31 PM Grand Central-42 St to Times Sq-42 St | 444 | 306 | 87 | Grand Central-42 St to Times Sq-42 St | 5:31 PM | 22 |
| FS | 8:31 AM Franklin Av to Prospect Park | 131 | 150 | 52 | Park Pl to Botanic Garden | 8:33 AM | 22 |
| H | 6:21 AM Rockaway Park-Beach 116 St to Broad Channel | 59 | 300 | 12 | Beach 90 St to Broad Channel | 6:26 AM | 22 |

\* A car is 60 ft of train, about one B Division car's length, so routes with different train lengths compare (`train_lengths.json5`).

</details>

## Charts

### Each route's most crowded train

<details>
<summary>The chart</summary>

![Each route's most crowded train](by_trip-peak-load.svg)

</details>

### Each route's most crowded train, per car\*

<details>
<summary>The chart</summary>

![Each route's most crowded train, per car\*](by_trip-peak-per-car.svg)

</details>
