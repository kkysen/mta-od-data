# Ridership by line and route

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
Each scaled column scales the OD data to a year's counted station entries.

Produced by `mta-od-data ridership --by line --by route --markdown-out src/mta_od_data/ridership/by_line_and_route.md`.

| line | route | scaled to 2025 | scaled to 2019 |
| --- | --- | ---: | ---: |
| SAS Phase 1 | Q | 137,460 | 176,349 |
| SAS Phase 1 | N | 5,354 | 6,863 |
| SAS Phase 1 | R | 813 | 1,024 |
