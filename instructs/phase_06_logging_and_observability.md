# Phase 06 Logging And Observability

## Logging Design

Phase 6 introduced lightweight file-backed logging focused on local debugging and run traceability.

### Logger

- logger name: `causal_app.pipeline`
- configurable via `LOG_LEVEL`
- default level: `INFO`

### Log Destinations

- shared pipeline log:
  - `storage/logs/pipeline.log`
- per-run log:
  - `storage/runs/<run-id>/run.log`

## What Gets Logged

- run start
- run completion
- failed stage and error type
- per-stage completion with:
  - `run_id`
  - `stage`
  - `status`
  - `input_rows`
  - `output_rows`
  - `duration_seconds`

## Failure Traceability

On failure, the pipeline now writes:

- exception stack trace to the log file(s)
- `storage/runs/<run-id>/run_failure.json`

The Upload page now surfaces:

- `run_id`
- `run_dir`
- `log_path`
- `failed_stage`

## Successful-Run Traceability

Each successful run now includes:

- `run_summary.json`
- `run.log`
- `artifact_manifest.json`

The Process Tracking page now displays:

- `log_path`
- `artifact_manifest_path`

## Known Limitations

- failed runs are not yet listed as first-class records in the Streamlit tracking view
- Postgres tables are still not used for run/event persistence
- logging is line-oriented, not full structured JSON logging
