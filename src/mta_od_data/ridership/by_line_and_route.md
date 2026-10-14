# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The busiest hour is the hour, by when they start, in which the most riders who use it enter the subway (the OD data says when riders enter, not when they pass a place).

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

| Line | Route | Aug-Dec 2025 | 2019 | Busiest Hour | Riders in It, Aug-Dec 2025 |
| --- | --- | ---: | ---: | --- | ---: |
| SAS Phase 1 | Q | 135,111 | 176,349 | 17:00 | 13,804 |
| SAS Phase 1 | N | 5,259 | 6,863 | 16:00 | 2,527 |
| SAS Phase 1 | R | 800 | 1,024 | 07:00 | 771 |
