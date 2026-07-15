# Phase 04 App Test Notes

## What Was Actually Tested

- `python3 -m py_compile $(find src apps -name '*.py' -type f | sort)`
  - passed
- `docker compose config`
  - rendered successfully after Phase 4 changes
- `pyproject.toml` dependency inspection
  - confirmed `streamlit`, `pandas`, `scikit-learn`, and `openpyxl` are declared
- repo inspection
  - confirmed no curated files exist in `data/samples/`
  - confirmed no Phase 3 model artifacts exist yet in `artifacts/models/phase_03`
  - confirmed no run outputs exist yet under `storage/runs/` or `storage/exports/`

## What Passed

- Python syntax compilation for all `src/` and `apps/` files
- Docker Compose configuration rendering
- static inspection of app/page wiring and storage paths

## What Failed

- No code-level failure was observed in the checks that were actually run

## What Was Not Tested

- real Streamlit page rendering in a live browser session
- upload/save interactions
- pipeline execution from the Streamlit UI
- artifact generation on first run
- Excel workbook download from the app
- Dockerized end-to-end app startup with live interaction
- Postgres connectivity from the app, because the app still does not write to Postgres

## Why End-To-End Testing Was Not Completed In-Session

- the current shell environment does not have the runtime dependencies installed
  - `streamlit`
  - `pandas`
  - `scikit-learn`
  - `openpyxl`

## Interpretation Reminder

- Phase 4 produced a real app wiring layer in code
- it was not browser-verified end-to-end in this shell session
