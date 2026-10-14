# Ridership by trip

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
A train's load is its riders on board between two stops, averaged over the weekdays it runs: a train is the same on any date with the same route, direction, first stop, and departure from it.

Produced by `mta-od-data ridership --by trip --markdown-out src/mta_od_data/ridership/by_trip.md`.

| Route | Train | Peak Load, Aug-Dec 2025 | Peak Between | Leaving At | Weekdays Run |
| --- | --- | ---: | --- | --- | ---: |
| F | 08:43 Jamaica-179 St to Coney Island-Stillwell Av | 1,360 | Court Sq-23 St to Lexington Av/53 St | 09:09 | 23 |
| 7 | 15:56 34 St-Hudson Yards to Flushing-Main St | 1,211 | 74 St-Broadway to 82 St-Jackson Hts | 16:22 | 103 |
| A | 07:29 Inwood-207 St to Far Rockaway-Mott Av | 1,185 | 125 St to 59 St-Columbus Circle | 07:47 | 60 |
| L | 17:51 8 Av to Canarsie-Rockaway Pkwy | 1,179 | 14 St-Union Sq to 3 Av | 17:54 | 60 |
| E | 08:32 Jamaica Center-Parsons/Archer to World Trade Center | 1,166 | Court Sq-23 St to Lexington Av/53 St | 08:57 | 103 |
| 5 | 08:00 Flatbush Av-Brooklyn College to Eastchester-Dyre Av | 1,065 | 14 St-Union Sq to Grand Central-42 St | 08:39 | 103 |
| 4 | 17:17 Woodlawn to Crown Hts-Utica Av | 1,022 | Grand Central-42 St to 14 St-Union Sq | 17:54 | 103 |
| W | 08:50 Astoria-Ditmars Blvd to Whitehall St-South Ferry | 1,021 | Queensboro Plaza to Lexington Av/59 St | 09:01 | 103 |
| N | 08:17 Coney Island-Stillwell Av to 96 St | 978 | Atlantic Av to Canal St | 08:51 | 103 |
| Q | 16:58 96 St to Coney Island-Stillwell Av | 945 | Canal St to DeKalb Av | 17:19 | 103 |
| 6 | 08:20 Parkchester to Brooklyn Bridge-City Hall | 929 | 51 St to Grand Central-42 St | 08:54 | 60 |
| FX | 16:58 Jamaica-179 St to Coney Island-Stillwell Av | 928 | Broadway-Lafayette St to 2 Av | 17:45 | 80 |
| D | 15:57 Norwood-205 St to Coney Island-Stillwell Av | 916 | Broadway-Lafayette St to Grand St | 16:43 | 43 |
| B | 08:41 Brighton Beach to Bedford Park Blvd | 915 | 7 Av to Atlantic Av | 09:00 | 103 |
| 2 | 16:19 Flatbush Av-Brooklyn College to Wakefield-241 St | 908 | Times Sq-42 St to 72 St | 17:05 | 103 |
| C | 17:31 Euclid Av to 168 St | 884 | 14 St to 23 St | 18:08 | 60 |
| 6X | 08:46 Pelham Bay Park to Brooklyn Bridge-City Hall | 881 | 3 Av-138 St to 125 St | 09:11 | 103 |
| 1 | 07:19 South Ferry to Van Cortlandt Park-242 St | 872 | Times Sq-42 St to 50 St | 07:36 | 103 |
| 3 | 17:23 New Lots Av to Harlem-148 St | 868 | 14 St to 34 St-Penn Station | 18:10 | 103 |
| M | 15:52 Middle Village-Metropolitan Av to Forest Hills-71 Av | 852 | Lexington Av/63 St to Roosevelt Island | 16:40 | 23 |
| 7X | 16:56 34 St-Hudson Yards to Flushing-Main St | 801 | 74 St-Broadway to Junction Blvd | 17:23 | 103 |
| R | 06:58 Bay Ridge-95 St to 96 St | 750 | Lexington Av/63 St to 72 St | 07:57 | 103 |
| J | 08:22 Jamaica Center-Parsons/Archer to Broad St | 737 | Marcy Av to Delancey St-Essex St | 08:59 | 80 |
| G | 08:06 Church Av to Court Sq | 558 | Greenpoint Av to 21 St | 08:38 | 103 |
| Z | 07:52 Jamaica Center-Parsons/Archer to Broad St | 533 | Marcy Av to Delancey St-Essex St | 08:24 | 80 |
| GS | 16:59 Grand Central-42 St to Times Sq-42 St | 333 | Grand Central-42 St to Times Sq-42 St | 16:59 | 103 |
| FS | 16:41 Franklin Av to Prospect Park | 100 | Park Pl to Botanic Garden | 16:43 | 103 |
| H | 06:21 Rockaway Park-Beach 116 St to Broad Channel | 54 | Beach 90 St to Broad Channel | 06:26 | 60 |
