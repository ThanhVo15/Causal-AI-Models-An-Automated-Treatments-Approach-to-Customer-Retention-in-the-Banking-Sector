# Causal AI Local Demo Foundation

This repository is being modernized from a student-era causal AI research bundle into a local Python demo platform.

## Current Phase

- Phase 6 status: the local demo has been smoke-tested, business export is in place, and the repo now includes practical tests, run logs, and artifact manifests.
- Legacy research assets are preserved under:
  [`legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`](./legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/)
- The extracted engine and demo app are intentionally partial and traceable:
  - churn scoring is a temporary notebook-derived shim
  - segmentation is a wrapper built from exported cluster labels
  - recommendation is derived from the simulated legacy `df_causal_ai` table
  - Streamlit is wired to local file-based runs, not to a DB-backed app service yet

## What Exists Now

- Root-level repo structure for runtime code, docs, data, tests, storage, and artifacts
- Persistent phase memory under [`instructs/`](./instructs/)
- Migration baseline under [`docs/migration/`](./docs/migration/)
- Python core engine modules under [`src/causal_app/`](./src/causal_app/)
- Streamlit demo app under [`apps/streamlit/`](./apps/streamlit/) with pages for upload, profiling, tracking, dashboard, and export
- Docker + Postgres local foundation via `Dockerfile` and `docker-compose.yml`
- Minimal Postgres bootstrap SQL under [`db/init/`](./db/init/)
- Pipeline CLI entrypoint at [`src/causal_app/pipeline/run_pipeline.py`](./src/causal_app/pipeline/run_pipeline.py)
- Pytest coverage for critical deterministic flows under [`tests/`](./tests/)

## What Is Not Yet Implemented

- Database-backed dataset upload persistence flow
- Full parity verification against notebook outputs
- Database-backed run persistence
- Production-ready serving or orchestration

## Quick Start

1. Optional: copy `.env.example` to `.env` and adjust values.
2. Choose either the local Python path or Docker path.

Local Python path:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

Docker path:

```bash
docker compose up --build
```

3. Open the Streamlit shell at `http://localhost:8501`.

## Use The Demo App

The Phase 4 Streamlit app supports a local data-scientist workflow:

- `Upload`: save CSV/XLSX files into `storage/uploads/`, preview them, validate them, and trigger the pipeline
- `Data Profiling`: inspect schema presence, missing values, duplicates, and lightweight summaries
- `Process Tracking`: inspect per-stage status, duration, and artifact locations from completed runs
- `Dashboard`: inspect real diagnostics, churn distribution, cluster distribution, and treatment counts
- `Export`: download the generated Excel workbook plus CSV outputs

Phase 5 extends the workbook toward a business handoff format:

- `Summary`: run volumes, priority mix, policy mix, reject counts, and limitations
- `Customer_Action_List`: business-friendly action table with `priority_band`, `priority_score`, and deterministic `reason_short`
- `Reject_Report`: row-level rejection reasons for data-fix follow-up
- `Run_Metadata`: run id, source file, and stage timing snapshot
- `Field_Definitions`: lightweight field dictionary for workbook consumers

There is no curated sample file in `data/samples/` yet. For smoke testing, the app can register the archived legacy `test.csv`.

## Run The Extracted Pipeline

Once dependencies are installed locally, you can run the first extracted pipeline without opening notebooks:

```bash
pip install -e .
python -m causal_app.pipeline.run_pipeline \
  --input legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv \
  --run-label smoke-test
```

Expected outputs:

- per-run files under `storage/runs/<run-id>/`
- Excel export under `storage/exports/<run-id>.xlsx`

The Excel workbook is intended to be shareable with business stakeholders, but it still inherits Phase 3 limitations:

- churn scoring is based on the temporary legacy wrapper
- segmentation is based on the temporary legacy cluster wrapper
- recommendation and expected improvement values are still traceable to simulated legacy policy data
- `reason_short` is deterministic template logic, not LLM-generated commentary

Important honesty note:

- this command was originally added in Phase 3
- by Phase 6 it has been rerun successfully from a local `.venv` against the archived `test.csv`
- the current app and engine remain demo-grade, not production-grade

## Verification Snapshot

Actually verified in the Phase 6 workspace:

- `python3 -m py_compile $(find src apps tests -name '*.py' -type f | sort)`
- `.venv/bin/pytest`
- `.venv/bin/python -m causal_app.pipeline.run_pipeline --input .../Data/test.csv --run-label phase6-smoke`
- `.venv/bin/streamlit run apps/streamlit/app.py --server.headless true --server.port 8765`
- `docker compose config`

New traceability outputs now include:

- per-run `run.log`
- per-run `artifact_manifest.json`
- shared `storage/logs/pipeline.log`

## Local Stack Direction

- Streamlit for a lightweight Python-only demo UI
- Postgres for local persistence
- Docker Compose for one-command local startup
- `storage/` for persisted uploads, run logs, profiles, exports, and app-side runtime files

## Repository Layout

- `apps/streamlit/`: local demo app wired to storage-backed uploads and Phase 3 run outputs
- `src/causal_app/`: extracted engine plus future reusable application code
- `db/init/`: initial Postgres bootstrap SQL
- `storage/`: persisted local runtime outputs
- `docs/migration/`: audit baseline and move plan
- `legacy_snapshot/`: untouched archived research bundle
- `instructs/`: persistent phase memory for future modernization work

## Legacy Research Bundle

The original notebook-heavy project was intentionally archived without internal rewrites in Phase 2.

- Legacy bundle: [`legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`](./legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/)
- Legacy README: [`legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/README.md`](./legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/README.md)

## Where To Read Context First

- Phase memory: [`instructs/`](./instructs/)
- Migration baseline: [`docs/migration/phase_1_audit_baseline.md`](./docs/migration/phase_1_audit_baseline.md)
- Local startup notes: [`docs/user_guide/local_startup.md`](./docs/user_guide/local_startup.md)
- Demo workflow: [`docs/user_guide/demo_workflow.md`](./docs/user_guide/demo_workflow.md)
- Business export guide: [`docs/user_guide/business_export.md`](./docs/user_guide/business_export.md)
- Artifact versioning: [`docs/architecture/artifact_versioning.md`](./docs/architecture/artifact_versioning.md)
- Phase 3 runbook: [`instructs/phase_03_runbook.md`](./instructs/phase_03_runbook.md)
- Phase 4 app notes: [`instructs/phase_04_local_run_guide.md`](./instructs/phase_04_local_run_guide.md)
