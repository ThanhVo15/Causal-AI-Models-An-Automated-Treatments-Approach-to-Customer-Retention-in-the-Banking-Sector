# Phase 06 Test Strategy

## What Tests Existed Before Phase 6

- No meaningful automated tests existed
- Prior phases relied on syntax checks, manual inspection, and selective smoke runs

## What Was Added In Phase 6

### Unit Tests

- `tests/unit/test_ingestion.py`
  - CSV/XLSX reading
  - empty-file rejection
  - validation reject handling
  - required-column enforcement
- `tests/unit/test_business_output.py`
  - deterministic priority logic
  - deterministic short-reason logic
  - reject-report detail mapping
- `tests/unit/test_artifact_manifest.py`
  - manifest structure and recorded artifact roles

### Integration Test

- `tests/integration/test_excel_export.py`
  - workbook creation
  - expected sheet names
  - expected business/export headers

## What Was Actually Run

- `python3 -m py_compile $(find src apps tests -name '*.py' -type f | sort)`
- `.venv/bin/pytest`

Observed result:

- `8 passed`

## Additional Practical Verifications Run In Phase 6

- `.venv/bin/python -m causal_app.pipeline.run_pipeline --input .../Data/test.csv --run-label phase6-smoke`
- `.venv/bin/streamlit run apps/streamlit/app.py --server.headless true --server.port 8765 --server.fileWatcherType none`
- `docker compose config`

## Critical Gaps Still Open

- no automated end-to-end browser test for Streamlit interactions
- no automated test for failed-run surfacing in the app
- no regression test around the full legacy-backed pipeline outputs
- no Dockerized integration test
- no business-user acceptance test for workbook usability
