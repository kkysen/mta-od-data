# Ridership by trip

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
A train's load is its riders on board between two stops, averaged over the weekdays it runs: a train is the same on any date with the same route, direction, first stop, and departure from it.

Produced by `mta-od-data ridership --by trip --markdown-out src/mta_od_data/ridership/by_trip.md`.

## Table

<details open>
<summary>The table</summary>

| Route | Train | Peak Load, Aug-Dec 2025 | Train Length (ft) | Peak per Car\* | Peak Between | Leaving At | Weekdays Run |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| F | 8:32 AM Jamaica-179 St to Coney Island-Stillwell Av | 1,467 | 600 | 147 | Court Sq-23 St to Lexington Av/53 St | 8:59 AM | 23 |
| E | 8:27 AM Jamaica Center-Parsons/Archer to World Trade Center | 1,354 | 600 | 135 | Court Sq-23 St to Lexington Av/53 St | 8:51 AM | 103 |
| 7 | 3:56 PM 34 St-Hudson Yards to Flushing-Main St | 1,193 | 561 | 128 | 74 St-Broadway to 82 St-Jackson Hts | 4:22 PM | 103 |
| L | 5:51 PM 8 Av to Canarsie-Rockaway Pkwy | 1,156 | 480 | 145 | 14 St-Union Sq to 3 Av | 5:54 PM | 60 |
| Q | 8:08 AM Coney Island-Stillwell Av to 96 St | 1,124 | 600 | 112 | DeKalb Av to Canal St | 8:44 AM | 103 |
| A | 7:29 AM Inwood-207 St to Far Rockaway-Mott Av | 1,112 | 600 | 111 | 125 St to 59 St-Columbus Circle | 7:47 AM | 60 |
| 5 | 8:00 AM Flatbush Av-Brooklyn College to Eastchester-Dyre Av | 1,032 | 510 | 121 | 14 St-Union Sq to Grand Central-42 St | 8:39 AM | 103 |
| W | 8:50 AM Astoria-Ditmars Blvd to Whitehall St-South Ferry | 1,000 | 600 | 100 | Queensboro Plaza to Lexington Av/59 St | 9:01 AM | 103 |
| 3 | 8:01 AM 145 St to New Lots Av | 989 | 510 | 116 | 34 St-Penn Station to 14 St | 8:21 AM | 60 |
| 4 | 4:22 PM Crown Hts-Utica Av to Woodlawn | 986 | 510 | 116 | 14 St-Union Sq to Grand Central-42 St | 4:49 PM | 103 |
| B | 4:46 PM Bedford Park Blvd to Brighton Beach | 971 | 600 | 97 | 34 St-Herald Sq to W 4 St-Wash Sq | 5:27 PM | 60 |
| FX | 4:58 PM Jamaica-179 St to Coney Island-Stillwell Av | 967 | 600 | 97 | Broadway-Lafayette St to 2 Av | 5:45 PM | 80 |
| D | 3:57 PM Norwood-205 St to Coney Island-Stillwell Av | 949 | 600 | 95 | Broadway-Lafayette St to Grand St | 4:43 PM | 43 |
| C | 8:24 AM Euclid Av to 168 St | 926 | 600 | 93 | High St to Fulton St | 8:51 AM | 60 |
| N | 4:16 PM Astoria-Ditmars Blvd to Coney Island-Stillwell Av | 907 | 600 | 91 | 36 St to 59 St | 5:05 PM | 103 |
| 2 | 7:29 AM Wakefield-241 St to Flatbush Av-Brooklyn College | 898 | 510 | 106 | 72 St to Times Sq-42 St | 8:22 AM | 103 |
| 6 | 8:20 AM Parkchester to Brooklyn Bridge-City Hall | 886 | 510 | 104 | 77 St to 68 St-Hunter College | 8:49 AM | 60 |
| 6X | 8:46 AM Pelham Bay Park to Brooklyn Bridge-City Hall | 868 | 510 | 102 | 3 Av-138 St to 125 St | 9:11 AM | 103 |
| M | 3:52 PM Middle Village-Metropolitan Av to Forest Hills-71 Av | 807 | 480 | 101 | Lexington Av/63 St to Roosevelt Island | 4:40 PM | 23 |
| 7X | 4:56 PM 34 St-Hudson Yards to Flushing-Main St | 805 | 561 | 86 | 74 St-Broadway to Junction Blvd | 5:23 PM | 103 |
| R | 8:29 AM Bay Ridge-95 St to Forest Hills-71 Av | 785 | 600 | 78 | Atlantic Av to DeKalb Av | 8:51 AM | 103 |
| 1 | 4:46 PM South Ferry to Van Cortlandt Park-242 St | 779 | 510 | 92 | 96 St to 103 St | 5:15 PM | 103 |
| J | 8:22 AM Jamaica Center-Parsons/Archer to Broad St | 728 | 480 | 91 | Marcy Av to Delancey St-Essex St | 8:59 AM | 80 |
| G | 8:06 AM Church Av to Court Sq | 551 | 300 | 110 | Greenpoint Av to 21 St | 8:38 AM | 103 |
| Z | 7:52 AM Jamaica Center-Parsons/Archer to Broad St | 527 | 480 | 66 | Marcy Av to Delancey St-Essex St | 8:24 AM | 80 |
| GS | 4:59 PM Grand Central-42 St to Times Sq-42 St | 341 | 306 | 67 | Grand Central-42 St to Times Sq-42 St | 4:59 PM | 103 |
| FS | 4:41 PM Franklin Av to Prospect Park | 105 | 150 | 42 | Park Pl to Botanic Garden | 4:43 PM | 103 |
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
