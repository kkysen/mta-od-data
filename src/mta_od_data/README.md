# The `mta-od-data` package

The CLI's subcommands are overviewed in the [top-level `README.md`](../../README.md).
`analyze`'s are detailed in [`analyze/README.md`](analyze/README.md),
and `raptor`'s and `ridership`'s in [`raptor/README.md`](../../raptor/README.md).

## `prepare`

The Parquet comes out considerably smaller than the extract it's built from
(1.5GB to 358MB for 2025), losslessly:

- The origin/destination name, latitude, longitude, and point columns are dropped:
  each is functionally determined by the complex ID beside it,
  so they are the station reference CSVs repeated once per row,
  and `analyze` joins them by complex ID instead.
- `Timestamp` is dropped too:
  it holds one synthesized label per (year, month, day of week, hour) group,
  which `DayCoverage` reconstructs from those columns.
- Ridership is stored as `DECIMAL(9, 4)`,
  exact for every value in the extract,
  and packed as an integer rather than as a `DOUBLE` that never compresses.
- Rows are sorted by origin/destination pair,
  which runs the ID columns into long constant stretches: ~190MB by itself.
