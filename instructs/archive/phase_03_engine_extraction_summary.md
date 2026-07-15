# Phase 03 Engine Extraction Summary

## Status

- Phase 3 extracted the first runnable Python core engine from the archived notebook bundle.
- Legacy notebooks remain preserved under `legacy_snapshot/` and were not deleted or rewritten.
- No claim of notebook-result parity is made in this phase.

## Phase 1 And Phase 2 Constraints Honored

- Phase 1 said the repo was a research/demo bundle, not a maintainable platform.
- Phase 2 said the legacy bundle must stay intact and the new root should become the future source-of-truth runtime layer.
- Phase 3 therefore extracted only the clearest reusable logic needed for a local demo engine and left exploratory notebook logic in place.

## What Was Extracted Into `src/causal_app/`

- `ingestion/files.py`
  - CSV/XLSX reading with path and empty-file checks
- `ingestion/validation.py`
  - minimal dataset contract validation, normalization, duplicate detection, reject tracking
- `preprocessing/legacy_bank.py`
  - notebook-derived preprocessing classes and feature projectors
- `models/churn/legacy_churn.py`
  - temporary churn artifact loader/builder derived from legacy `train.csv`
- `models/segmentation/legacy_segmentation.py`
  - temporary cluster wrapper derived from exported `df_cluster.csv`
- `models/recommendation/legacy_policy.py`
  - temporary recommendation wrapper derived from simulated `df_causal_ai`
- `models/diagnostics/summary.py`
  - structured run summaries
- `export/excel.py`
  - Excel workbook export
- `pipeline/engine.py`
  - end-to-end orchestration
- `pipeline/run_pipeline.py`
  - CLI entrypoint
- `schemas/contracts.py`
  - core input/output and stage contracts

## What Stayed In Notebooks

- `1_Estimated_Loss_Profit_by_Churn.ipynb`
  - business framing and economics narrative
- `4_Clustering_Analyst.ipynb`
  - descriptive reporting and narrative cluster interpretation
- most EDA, SHAP, PDP, causal graph exploration, and report-like analysis from notebooks 2, 3, 5, and 6

## What Was Wrapped Temporarily Instead Of Fully Migrated

- Churn scoring
  - real Python interface
  - temporary shim because no original saved model artifact was found in the repo
- Segmentation
  - real Python interface
  - temporary wrapper because the original embedding-based clustering artifact was not found
- Recommendation
  - real Python interface
  - temporary wrapper because the observed recommendation stage depends on simulated post-treatment data in `df_causal_ai`

## What Was Deferred

- full extraction of notebook 2 experimentation and evaluation logic
- full extraction of notebook 3 embedding/GPU branches
- full extraction of notebook 6 econml/causal-estimator training flow
- Streamlit wiring to the extracted engine
- Postgres-backed run persistence
- parity verification against notebook outputs
- canonical dataset promotion into `data/`

## Real vs Partial vs Stubbed

### Real in Phase 3

- file reading for CSV/XLSX
- validation and reject tracking
- notebook-derived preprocessing classes
- pipeline orchestration
- diagnostics JSON/table generation
- Excel export layer

### Partial but runnable in principle

- churn prediction via notebook-derived retraining shim
- segmentation via nearest-centroid wrapper trained from exported cluster labels
- recommendation via cluster-level summary built from simulated legacy causal table

### Still not implemented

- original saved model/artifact loading from legacy work
- database-backed pipeline metadata writes
- Streamlit-triggered execution
- production-ready serving contracts

## Deliberate Temporary Shims Added In Phase 3

- Age-group binning now keeps a fitted upper-edge fallback so narrow inference batches do not fail when their max age is below the training quantiles.
  - This is a serving-safety shim around notebook-derived logic.
- The pipeline now handles the case where all uploaded rows are rejected.
  - Model stages are marked `skipped` and the run still emits diagnostics and export files.

## Checks Actually Run

- `python3 -m py_compile $(find src apps -name '*.py' -type f | sort)` -> passed
- Legacy dataset headers and row counts were inspected using the Python standard library
- The local shell does not currently have `pandas`, `scikit-learn`, or `openpyxl`
  - therefore the pipeline was not executed end-to-end in this session

## Important Honesty Notes

- The Phase 3 engine is traceable and structurally real, but not yet notebook-parity verified.
- The recommendation layer must still be described as simulation-backed legacy policy logic, not production-grade causal serving.
