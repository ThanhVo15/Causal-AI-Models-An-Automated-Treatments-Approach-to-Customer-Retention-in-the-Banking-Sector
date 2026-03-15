# Demo Workflow

## Recommended Local Workflow

This project is currently optimized for a local demo flow used by a data scientist or technical reviewer.

## Option 1: Python Virtual Environment

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

Then open:

- `http://localhost:8501`

## Option 2: Docker Compose

```bash
docker compose up --build
```

Then open:

- `http://localhost:8501`

## In-App Flow

1. Go to `Upload`
2. Upload a CSV/XLSX file or register the archived legacy `test.csv`
3. Review validation counts and reject reasons
4. Run the pipeline
5. Inspect `Process Tracking`
6. Inspect `Dashboard`
7. Download the business workbook from `Export`

## What A Successful Run Produces

Per run:

- `storage/runs/<run-id>/prepared_features.csv`
- `storage/runs/<run-id>/recommendations.csv`
- `storage/runs/<run-id>/rejected_rows.csv`
- `storage/runs/<run-id>/policy_options.csv`
- `storage/runs/<run-id>/diagnostics.json`
- `storage/runs/<run-id>/run_summary.json`
- `storage/runs/<run-id>/run.log`
- `storage/runs/<run-id>/artifact_manifest.json`

Cross-run outputs:

- `storage/exports/<run-id>.xlsx`
- `storage/logs/pipeline.log`

## Known Limits

- Postgres is still scaffolded but not used for app-side run persistence.
- Recommendation output remains tied to the temporary legacy policy wrapper.
- The archived legacy bundle is still required for first-run artifact rebuilding.
