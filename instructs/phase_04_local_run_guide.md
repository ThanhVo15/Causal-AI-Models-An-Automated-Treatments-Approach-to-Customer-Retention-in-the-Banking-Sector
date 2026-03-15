# Phase 04 Local Run Guide

## Purpose

Phase 4 makes the Streamlit app locally usable on top of the extracted Phase 3 engine.

## Required Dependencies

- Python 3.11+
- dependencies from `pyproject.toml`
  - `streamlit`
  - `pandas`
  - `scikit-learn`
  - `openpyxl`

## Local Python Run

```bash
pip install -e .
streamlit run apps/streamlit/app.py
```

Then open:

- `http://localhost:8501`

## Docker Run

```bash
docker compose up --build
```

Then open:

- `http://localhost:8501`

## Phase 4 App Flow

1. Go to `Upload`
2. Upload a CSV/XLSX file or click `Register Legacy test.csv`
3. Review the validation summary
4. Click `Run Pipeline On Selected Input`
5. Go to `Process Tracking` to inspect stage durations and artifact paths
6. Go to `Dashboard` to inspect real output charts/tables
7. Go to `Export` to download the workbook and CSV outputs

## Existing Example Input

- There is still no curated sample file in `data/samples/`
- The app can register the archived legacy file:
  - `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv`

## Environment Notes

- `STORAGE_ROOT` controls where uploads/runs/exports are written
- Docker currently bind-mounts `./storage` into the app container
- the app reads legacy training/intermediate files from `legacy_snapshot/`

## Expected Runtime Outputs

After a successful run, expect:

- `storage/uploads/<upload-id>__<filename>`
- `storage/uploads/<upload-id>.upload.json`
- `storage/runs/<run-id>/prepared_features.csv`
- `storage/runs/<run-id>/recommendations.csv`
- `storage/runs/<run-id>/rejected_rows.csv`
- `storage/runs/<run-id>/policy_options.csv`
- `storage/runs/<run-id>/diagnostics.json`
- `storage/runs/<run-id>/run_summary.json`
- `storage/exports/<run-id>.xlsx`

## Known Issues / Limits

- the app is not yet writing to Postgres
- first run may take longer because Phase 3 artifacts may be built from archived legacy CSVs
- churn/segmentation/recommendation still use temporary legacy wrappers
- no curated sample dataset has been promoted into `data/samples/`
- local end-to-end execution was not verified in the Phase 4 shell session because runtime dependencies were missing
