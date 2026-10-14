# Ridership by line

Average weekday riders with fare evaders, over 103 weekdays from 2025-08-19 to 2025-12-22 (`data/raptor/manifest.csv`).
The 2019 column scales the OD data on these dates to 2019's counted station entries.
The busiest hour is the hour, by when they start, in which the most riders who use it enter the subway (the OD data says when riders enter, not when they pass a place).

Produced by `mta-od-data ridership --by line --markdown-out src/mta_od_data/ridership/by_line.md`.

| Line | Aug-Dec 2025 | 2019 | Busiest Hour | Riders in It, Aug-Dec 2025 |
| --- | ---: | ---: | --- | ---: |
| SAS Phase 1 | 141,144 | 184,197 | 17:00 | 14,656 |
