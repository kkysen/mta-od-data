# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

| Line | Route | Aug-Dec 2025 | 2019 |
| --- | --- | ---: | ---: |
| SAS Phase 1 | Q | 135,111 | 176,349 |
| SAS Phase 1 | N | 5,259 | 6,863 |
| SAS Phase 1 | R | 800 | 1,024 |
