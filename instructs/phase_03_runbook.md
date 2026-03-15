# Phase 03 Runbook

## Purpose

Phase 3 introduced the first non-notebook pipeline entrypoint for the local demo engine.

## Prerequisites

- Python 3.11+
- package dependencies installed from `pyproject.toml`
- access to the archived legacy bundle under `legacy_snapshot/`

## Local Install

```bash
pip install -e .
```

## Run The Pipeline Locally

```bash
python -m causal_app.pipeline.run_pipeline --input <path-to-csv-or-xlsx>
```

Example using the archived legacy holdout-style file:

```bash
python -m causal_app.pipeline.run_pipeline \
  --input legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv \
  --run-label local-smoke
```

## Optional Docker-Oriented Command

If the Docker image is built and dependencies are available inside the container:

```bash
docker compose run --rm app python -m causal_app.pipeline.run_pipeline \
  --input /app/legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv \
  --run-label docker-smoke
```

## Expected Outputs

Per run, the engine writes:

- `storage/runs/<run-id>/prepared_features.csv`
- `storage/runs/<run-id>/recommendations.csv`
- `storage/runs/<run-id>/rejected_rows.csv`
- `storage/runs/<run-id>/policy_options.csv`
- `storage/runs/<run-id>/diagnostics.json`
- `storage/runs/<run-id>/run_summary.json`
- `storage/exports/<run-id>.xlsx`

## What The Current Engine Actually Does

1. reads CSV/XLSX input
2. validates columns and values
3. prepares legacy-style features
4. loads or builds the temporary churn shim
5. loads or builds the temporary segmentation wrapper
6. loads or builds the temporary policy wrapper
7. writes diagnostics and Excel export

## What It Does Not Yet Do

- write run metadata into Postgres
- expose the pipeline through Streamlit actions
- guarantee parity with legacy notebook metrics
- load original saved legacy model artifacts

## Known Limitations

- churn is rebuilt from legacy `train.csv` on first use if the Phase 3 artifact does not yet exist
- segmentation is approximated from exported `df_cluster.csv`, not the original embedding artifact
- recommendation is derived from simulated `df_causal_ai`
- the local shell used during Phase 3 did not have `pandas`, `scikit-learn`, or `openpyxl`, so this runbook was not executed end-to-end in-session

## Checks Actually Performed During Phase 3

- source files compiled successfully with `py_compile`
- `pyproject.toml` parsed successfully
- legacy file headers and notebook traceability were inspected directly
