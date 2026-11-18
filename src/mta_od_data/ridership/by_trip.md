# Ridership by trip

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (as `raptor assign-range` routes them).
A train's load is its riders on board between two stops, averaged over the weekdays it runs: a train is the same on any date with the same route, direction, first stop, and departure from it.

Produced by `mta-od-data ridership --by trip --markdown-out src/mta_od_data/ridership/by_trip.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Train | Peak Load, Aug-Dec 2025 | Train Length (ft) | Peak per Car\* | Peak Between | Leaving At | Weekdays Run |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| F | 8:43 AM Jamaica-179 St to Coney Island-Stillwell Av | 1,501 | 600 | 150 | Jackson Hts-Roosevelt Av to Queens Plaza | 9:02 AM | 23 |
| E | 8:27 AM Jamaica Center-Parsons/Archer to World Trade Center | 1,350 | 600 | 135 | Court Sq-23 St to Lexington Av/53 St | 8:51 AM | 103 |
| L | 5:40 PM 8 Av to Canarsie-Rockaway Pkwy | 1,232 | 480 | 154 | 14 St-Union Sq to 3 Av | 5:44 PM | 60 |
| 7 | 7:14 AM Flushing-Main St to 34 St-Hudson Yards | 1,189 | 561 | 127 | 82 St-Jackson Hts to 74 St-Broadway | 7:25 AM | 103 |
| 4 | 4:58 PM Woodlawn to New Lots Av | 1,138 | 510 | 134 | Grand Central-42 St to 14 St-Union Sq | 5:37 PM | 103 |
| Q | 8:08 AM Coney Island-Stillwell Av to 96 St | 1,127 | 600 | 113 | DeKalb Av to Canal St | 8:44 AM | 103 |
| 5 | 8:00 AM Flatbush Av-Brooklyn College to Eastchester-Dyre Av | 1,111 | 510 | 131 | 14 St-Union Sq to Grand Central-42 St | 8:39 AM | 103 |
| A | 7:29 AM Inwood-207 St to Far Rockaway-Mott Av | 1,085 | 600 | 109 | 125 St to 59 St-Columbus Circle | 7:47 AM | 60 |
| N | 4:26 PM Astoria-Ditmars Blvd to Coney Island-Stillwell Av | 1,046 | 600 | 105 | 34 St-Herald Sq to 14 St-Union Sq | 4:50 PM | 103 |
| B | 5:07 PM Bedford Park Blvd to Brighton Beach | 1,030 | 600 | 103 | 34 St-Herald Sq to W 4 St-Wash Sq | 5:48 PM | 103 |
| FX | 4:58 PM Jamaica-179 St to Coney Island-Stillwell Av | 1,003 | 600 | 100 | Broadway-Lafayette St to 2 Av | 5:45 PM | 80 |
| W | 8:50 AM Astoria-Ditmars Blvd to Whitehall St-South Ferry | 999 | 600 | 100 | Queensboro Plaza to Lexington Av/59 St | 9:01 AM | 103 |
| 3 | 8:01 AM 145 St to New Lots Av | 947 | 510 | 111 | 34 St-Penn Station to 14 St | 8:21 AM | 60 |
| D | 3:57 PM Norwood-205 St to Coney Island-Stillwell Av | 946 | 600 | 95 | Atlantic Av to 36 St | 4:57 PM | 43 |
| C | 8:24 AM Euclid Av to 168 St | 922 | 600 | 92 | High St to Fulton St | 8:51 AM | 60 |
| 6 | 8:20 AM Parkchester to Brooklyn Bridge-City Hall | 879 | 510 | 103 | 77 St to 68 St-Hunter College | 8:49 AM | 60 |
| 6X | 8:46 AM Pelham Bay Park to Brooklyn Bridge-City Hall | 866 | 510 | 102 | 3 Av-138 St to 125 St | 9:11 AM | 103 |
| 2 | 7:29 AM Wakefield-241 St to Flatbush Av-Brooklyn College | 856 | 510 | 101 | 72 St to Times Sq-42 St | 8:22 AM | 103 |
| M | 3:52 PM Middle Village-Metropolitan Av to Forest Hills-71 Av | 841 | 480 | 105 | Lexington Av/63 St to Roosevelt Island | 4:40 PM | 23 |
| 7X | 4:32 PM 34 St-Hudson Yards to Flushing-Main St | 829 | 561 | 89 | 74 St-Broadway to Junction Blvd | 4:59 PM | 103 |
| 1 | 7:19 AM South Ferry to Van Cortlandt Park-242 St | 822 | 510 | 97 | Times Sq-42 St to 50 St | 7:36 AM | 103 |
| R | 8:04 AM Bay Ridge-95 St to Forest Hills-71 Av | 766 | 600 | 77 | Atlantic Av to DeKalb Av | 8:26 AM | 103 |
| J | 8:22 AM Jamaica Center-Parsons/Archer to Broad St | 696 | 480 | 87 | Marcy Av to Delancey St-Essex St | 8:59 AM | 80 |
| G | 8:06 AM Church Av to Court Sq | 539 | 300 | 108 | Greenpoint Av to 21 St | 8:38 AM | 103 |
| Z | 7:52 AM Jamaica Center-Parsons/Archer to Broad St | 528 | 480 | 66 | Marcy Av to Delancey St-Essex St | 8:24 AM | 80 |
| GS | 5:54 PM Grand Central-42 St to Times Sq-42 St | 427 | 306 | 84 | Grand Central-42 St to Times Sq-42 St | 5:54 PM | 103 |
| FS | 8:41 AM Franklin Av to Prospect Park | 108 | 150 | 43 | Botanic Garden to Prospect Park | 8:45 AM | 103 |
| H | 6:21 AM Rockaway Park-Beach 116 St to Broad Channel | 55 | 300 | 11 | Beach 90 St to Broad Channel | 6:26 AM | 60 |

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
