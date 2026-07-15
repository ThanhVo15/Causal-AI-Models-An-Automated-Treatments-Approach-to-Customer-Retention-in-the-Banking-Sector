# Phase 5 Export Test Notes

## What Was Actually Tested

- Python syntax check:
  - `python3 -m py_compile $(find src apps -name '*.py' -type f | sort)`
- Local dependency install:
  - `.venv/bin/pip install -e .`
- Real pipeline run:
  - `.venv/bin/python -m causal_app.pipeline.run_pipeline --input legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv --run-label phase5-sample`
- Manual workbook review using `openpyxl`
- Manual CSV/JSON review for the generated run

## What Failed First

Initial sample run failed with:

- `sklearn.exceptions.NotFittedError`

Observed cause:

- the notebook-derived churn preprocessing wrapper used custom sklearn transformers that did not expose fitted attributes in the way current scikit-learn expects

Fix applied:

- added fitted-state attributes to custom transformers in `src/causal_app/preprocessing/legacy_bank.py`
- added artifact usability validation and rebuild fallback in:
  - `src/causal_app/models/churn/legacy_churn.py`
  - `src/causal_app/models/segmentation/legacy_segmentation.py`

This was a runtime compatibility fix to make the extracted engine runnable. It did not intentionally change the transformation rules or model choice.

## Docker Attempt

Tried:

- `docker compose run --rm app python -m causal_app.pipeline.run_pipeline ...`

Result:

- failed because the local Docker daemon was not running in this environment

## Successful Sample Run

Run id:

- `20260315T145700Z-phase5-sample-1b67559c`

Generated artifacts:

- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/prepared_features.csv`
- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/recommendations.csv`
- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/rejected_rows.csv`
- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/policy_options.csv`
- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/diagnostics.json`
- `storage/runs/20260315T145700Z-phase5-sample-1b67559c/run_summary.json`
- `storage/exports/20260315T145700Z-phase5-sample-1b67559c.xlsx`

Observed run summary:

- input rows: `110023`
- accepted rows: `19698`
- rejected rows: `90325`
- dominant reject reason: `duplicate_customerid`

## Workbook Manual Review Notes

Verified directly:

- workbook exists
- sheet names are:
  - `Summary`
  - `Customer_Action_List`
  - `Reject_Report`
  - `Run_Metadata`
  - `Field_Definitions`
- `Customer_Action_List` includes:
  - `priority_score`
  - `priority_band`
  - `reason_short`
- `Reject_Report` includes human-readable `reject_reason_detail`
- `Summary` includes business-usable totals and limitation notes

Observed sample counts:

- priority distribution:
  - `P1 = 971`
  - `P2 = 2031`
  - `P3 = 16696`
- risk distribution:
  - `High = 1457`
  - `Medium = 1567`
  - `Low = 16674`
- fallback recommendation rows:
  - `0`
- `No Program` rows:
  - `0`

## What Still Needs Improvement

- review workbook usability with a business stakeholder, not only technical inspection
- test a file that triggers more than duplicate-based rejects
- test a file that exercises fallback policy behavior
