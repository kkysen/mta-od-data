# Ridership by trip

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
A train's load is its riders on board between two stops, averaged over the weekdays it runs: a train is the same on any date with the same route, direction, first stop, and departure from it.

Produced by `mta-od-data ridership --by trip --markdown-out src/mta_od_data/ridership/by_trip.md`.

| Route | Train | Peak Load, Aug-Dec 2025 | Train Length (ft) | Peak per Car\* | Peak Between | Leaving At | Weekdays Run |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| F | 8:43 AM Jamaica-179 St to Coney Island-Stillwell Av | 1,360 | 600 | 136 | Court Sq-23 St to Lexington Av/53 St | 9:09 AM | 23 |
| 7 | 3:56 PM 34 St-Hudson Yards to Flushing-Main St | 1,211 | 561 | 130 | 74 St-Broadway to 82 St-Jackson Hts | 4:22 PM | 103 |
| A | 7:29 AM Inwood-207 St to Far Rockaway-Mott Av | 1,185 | 600 | 118 | 125 St to 59 St-Columbus Circle | 7:47 AM | 60 |
| L | 5:51 PM 8 Av to Canarsie-Rockaway Pkwy | 1,179 | 480 | 147 | 14 St-Union Sq to 3 Av | 5:54 PM | 60 |
| E | 8:32 AM Jamaica Center-Parsons/Archer to World Trade Center | 1,166 | 600 | 117 | Court Sq-23 St to Lexington Av/53 St | 8:57 AM | 103 |
| 5 | 8:00 AM Flatbush Av-Brooklyn College to Eastchester-Dyre Av | 1,065 | 510 | 125 | 14 St-Union Sq to Grand Central-42 St | 8:39 AM | 103 |
| 4 | 5:17 PM Woodlawn to Crown Hts-Utica Av | 1,022 | 510 | 120 | Grand Central-42 St to 14 St-Union Sq | 5:54 PM | 103 |
| W | 8:50 AM Astoria-Ditmars Blvd to Whitehall St-South Ferry | 1,021 | 600 | 102 | Queensboro Plaza to Lexington Av/59 St | 9:01 AM | 103 |
| N | 8:17 AM Coney Island-Stillwell Av to 96 St | 978 | 600 | 98 | Atlantic Av to Canal St | 8:51 AM | 103 |
| Q | 4:58 PM 96 St to Coney Island-Stillwell Av | 945 | 600 | 95 | Canal St to DeKalb Av | 5:19 PM | 103 |
| 6 | 8:20 AM Parkchester to Brooklyn Bridge-City Hall | 929 | 510 | 109 | 51 St to Grand Central-42 St | 8:54 AM | 60 |
| FX | 4:58 PM Jamaica-179 St to Coney Island-Stillwell Av | 928 | 600 | 93 | Broadway-Lafayette St to 2 Av | 5:45 PM | 80 |
| D | 3:57 PM Norwood-205 St to Coney Island-Stillwell Av | 916 | 600 | 92 | Broadway-Lafayette St to Grand St | 4:43 PM | 43 |
| B | 8:41 AM Brighton Beach to Bedford Park Blvd | 915 | 600 | 91 | 7 Av to Atlantic Av | 9:00 AM | 103 |
| 2 | 4:19 PM Flatbush Av-Brooklyn College to Wakefield-241 St | 908 | 510 | 107 | Times Sq-42 St to 72 St | 5:05 PM | 103 |
| C | 5:31 PM Euclid Av to 168 St | 884 | 600 | 88 | 14 St to 23 St | 6:08 PM | 60 |
| 6X | 8:46 AM Pelham Bay Park to Brooklyn Bridge-City Hall | 881 | 510 | 104 | 3 Av-138 St to 125 St | 9:11 AM | 103 |
| 1 | 7:19 AM South Ferry to Van Cortlandt Park-242 St | 872 | 510 | 103 | Times Sq-42 St to 50 St | 7:36 AM | 103 |
| 3 | 5:23 PM New Lots Av to Harlem-148 St | 868 | 510 | 102 | 14 St to 34 St-Penn Station | 6:10 PM | 103 |
| M | 3:52 PM Middle Village-Metropolitan Av to Forest Hills-71 Av | 852 | 480 | 107 | Lexington Av/63 St to Roosevelt Island | 4:40 PM | 23 |
| 7X | 4:56 PM 34 St-Hudson Yards to Flushing-Main St | 801 | 561 | 86 | 74 St-Broadway to Junction Blvd | 5:23 PM | 103 |
| R | 6:58 AM Bay Ridge-95 St to 96 St | 750 | 600 | 75 | Lexington Av/63 St to 72 St | 7:57 AM | 103 |
| J | 8:22 AM Jamaica Center-Parsons/Archer to Broad St | 737 | 480 | 92 | Marcy Av to Delancey St-Essex St | 8:59 AM | 80 |
| G | 8:06 AM Church Av to Court Sq | 558 | 300 | 112 | Greenpoint Av to 21 St | 8:38 AM | 103 |
| Z | 7:52 AM Jamaica Center-Parsons/Archer to Broad St | 533 | 480 | 67 | Marcy Av to Delancey St-Essex St | 8:24 AM | 80 |
| GS | 4:59 PM Grand Central-42 St to Times Sq-42 St | 333 | 306 | 65 | Grand Central-42 St to Times Sq-42 St | 4:59 PM | 103 |
| FS | 4:41 PM Franklin Av to Prospect Park | 100 | 150 | 40 | Park Pl to Botanic Garden | 4:43 PM | 103 |
| H | 6:21 AM Rockaway Park-Beach 116 St to Broad Channel | 54 | 300 | 11 | Beach 90 St to Broad Channel | 6:26 AM | 60 |

\* A car is 60 ft of train, about one B Division car's length, so routes with different train lengths compare (`train_lengths.json5`).

![Each route's most crowded train](by_trip-peak-load.svg)

![Each route's most crowded train, per car\*](by_trip-peak-per-car.svg)
