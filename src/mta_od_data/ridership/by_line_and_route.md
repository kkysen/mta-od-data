# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The busiest hour is the hour, by when it starts, with the most riders in the Aug-Dec 2025 column on its trains there (getting on or off at a place, boarding a route, or joining a line), and those riders.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

| Line | Route | Aug-Dec 2025 | 2019 | Busiest Hour | Riders in It, Aug-Dec 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| SAS Phase 1 | Q | 135,111 | 176,349 | 8:00 AM | 13,264 |
| SAS Phase 1 | N | 5,259 | 6,863 | 4:00 PM | 2,513 |
| SAS Phase 1 | R | 800 | 1,024 | 7:00 AM | 800 |
