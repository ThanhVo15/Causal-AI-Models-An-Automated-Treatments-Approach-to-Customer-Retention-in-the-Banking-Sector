# Phase 06 Docs And Runbook

## Docs Improved In Phase 6

- `README.md`
- `docs/user_guide/local_startup.md`
- `docs/user_guide/business_export.md`
- `docs/architecture/local_demo_foundation.md`

## Docs Added In Phase 6

- `docs/user_guide/demo_workflow.md`
- `docs/architecture/artifact_versioning.md`

## Current Recommended Run Paths

### Local Python

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

### Docker

```bash
docker compose up --build
```

## Current Practical User Flow

1. Start the app
2. Upload a CSV/XLSX file or register the archived legacy `test.csv`
3. Review validation summary
4. Run the pipeline
5. Inspect Process Tracking
6. Inspect Dashboard
7. Download the workbook

## Architecture Summary

- Streamlit remains the main local UI
- `src/causal_app/` remains the execution source of truth
- `storage/` remains the source of truth for local runtime outputs
- Postgres remains scaffolded but not yet used by the Streamlit app

## Business Output Usage

- use `Customer_Action_List` as the primary business-facing sheet
- use `Reject_Report` to fix bad input rows
- keep `Run_Metadata`, `run_summary.json`, and `artifact_manifest.json` for internal traceability

## Known Limitations To Keep Visible

- temporary legacy churn / segmentation / recommendation wrappers remain in use
- recommendation outputs still rely on simulated legacy policy data
- full notebook-parity validation has still not been completed
