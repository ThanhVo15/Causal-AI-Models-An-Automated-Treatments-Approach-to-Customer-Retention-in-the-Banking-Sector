# Phase 04 App Summary

## Status

- Phase 4 turned the Streamlit shell into a usable local demo app for a data scientist.
- The app is wired to the extracted Phase 3 engine where that engine already exists.
- The app remains honest about partial components and does not present the current recommendation logic as production-grade causal serving.

## Alignment With Phase 3

- Phase 3 said Streamlit wiring was deferred.
- Phase 4 wires Streamlit to:
  - storage-backed uploads
  - Phase 3 validation
  - Phase 3 pipeline execution
  - Phase 3 diagnostics/run outputs
  - Phase 3 Excel export artifacts
- Phase 3 also said run persistence was not DB-backed.
- Phase 4 keeps that constraint and uses local files under `storage/` and `storage/runs/` instead of pretending Postgres integration is done.

## App Pages That Now Exist

- `apps/streamlit/app.py`
  - Phase 4 overview page with capability map and latest activity
- `apps/streamlit/pages/01_Upload.py`
  - upload registration, validation preview, and run trigger
- `apps/streamlit/pages/02_Data_Profiling.py`
  - lightweight profiling from the saved input file
- `apps/streamlit/pages/03_Process_Tracking.py`
  - run metadata, stage durations, artifact availability
- `apps/streamlit/pages/04_Dashboard.py`
  - diagnostics-backed charts and recommendation tables
- `apps/streamlit/pages/05_Export.py`
  - workbook/CSV download page

## Fully Wired In Phase 4

- storage-backed upload registration into `storage/uploads/`
- upload preview and validation using the extracted ingestion contract
- pipeline trigger through `run_pipeline(...)`
- reading run summaries from `storage/runs/*/run_summary.json`
- reading diagnostics from `diagnostics.json`
- dashboard counts and charts from real run outputs
- download access to generated workbook and CSV files

## Partial In Phase 4

- profiling is lightweight and dataframe-based, not a full profiling report system
- process tracking is local-file-backed, not DB-backed
- dashboard outputs are real but limited to what the Phase 3 engine emits
- recommendation outputs remain tied to temporary legacy wrappers

## Placeholder-Only In Phase 4

- Postgres-backed app metadata writes
- multi-user audit/history behavior
- full business-facing dashboard polish

## Still Deferred

- verified parity with legacy notebook results
- production-ready artifact registry and serving behavior
- notebook-6 causal estimator serving
- curated sample datasets under `data/samples/`

## Important Honesty Notes

- No Phase 3 artifacts were present before Phase 4 started.
- The app can create them on first successful run.
- The local shell used during Phase 4 still does not have runtime dependencies installed, so the app was not executed end-to-end in-session.
