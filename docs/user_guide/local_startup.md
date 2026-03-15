# Local Startup

## Docker Compose

The intended local startup path remains:

```bash
docker compose up --build
```

Optional first step:

```bash
cp .env.example .env
```

Then open:

- Streamlit: `http://localhost:8501`
- Postgres: `localhost:${POSTGRES_PORT:-5432}`

## Local Python Environment

Verified local path in Phase 6:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

## What You Should Expect From Docker Right Now

- The Streamlit app should boot with usable pages for upload, profiling, process tracking, dashboard, and export.
- Postgres should initialize the minimal foundation tables from `db/init/001_foundation.sql`.
- The app currently uses storage-backed local files for run state.
- The app does not write upload/run/export metadata into Postgres yet.

## Demo App Workflow

The Streamlit app is designed for this local flow:

1. Upload a CSV/XLSX file or register the archived legacy `test.csv`
2. Review validation results on the Upload page
3. Inspect profiling summaries on the Data Profiling page
4. Trigger the pipeline run
5. Review run stages on Process Tracking
6. Review output summaries on Dashboard
7. Download the workbook or CSV outputs on Export

## Run The Extracted Pipeline Locally

Phase 3 added a notebook-derived pipeline entrypoint:

```bash
pip install -e .
python -m causal_app.pipeline.run_pipeline --input <path-to-csv-or-xlsx>
```

Example using the legacy holdout-style file:

```bash
python -m causal_app.pipeline.run_pipeline \
  --input legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv \
  --run-label local-smoke
```

Expected outputs:

- `storage/runs/<run-id>/prepared_features.csv`
- `storage/runs/<run-id>/recommendations.csv`
- `storage/runs/<run-id>/rejected_rows.csv`
- `storage/runs/<run-id>/policy_options.csv`
- `storage/runs/<run-id>/diagnostics.json`
- `storage/runs/<run-id>/run_summary.json`
- `storage/runs/<run-id>/run.log`
- `storage/runs/<run-id>/artifact_manifest.json`
- `storage/logs/pipeline.log`
- `storage/exports/<run-id>.xlsx`

The workbook now targets a business handoff flow with these sheets:

- `Summary`
- `Customer_Action_List`
- `Reject_Report`
- `Run_Metadata`
- `Field_Definitions`

`Customer_Action_List` is the business-facing sheet. It includes deterministic `priority_band`, `priority_score`, and `reason_short` columns derived from real pipeline outputs.

For field-level details, see:

- `docs/user_guide/business_export.md`

## Known Limitation In The Current Shell

- The repo can be run successfully from a local `.venv`, but a plain shell still requires dependencies to be installed first.
- `docker compose config` is verified, but a full Dockerized browser walkthrough was not re-run in this phase.
- Postgres is still not used by the Streamlit app for run persistence.
