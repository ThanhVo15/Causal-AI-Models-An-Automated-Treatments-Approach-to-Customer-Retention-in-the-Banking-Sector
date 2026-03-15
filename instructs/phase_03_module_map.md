# Phase 03 Module Map

## Extraction Classification

### Extract now

- `src/causal_app/ingestion/files.py`
- `src/causal_app/ingestion/validation.py`
- `src/causal_app/preprocessing/legacy_bank.py`
- `src/causal_app/models/churn/legacy_churn.py`
- `src/causal_app/models/segmentation/legacy_segmentation.py`
- `src/causal_app/models/recommendation/legacy_policy.py`
- `src/causal_app/models/diagnostics/summary.py`
- `src/causal_app/export/excel.py`
- `src/causal_app/pipeline/engine.py`
- `src/causal_app/pipeline/run_pipeline.py`
- `src/causal_app/schemas/contracts.py`

### Wrap temporarily

- legacy churn artifact behavior
- legacy segmentation artifact behavior
- legacy recommendation policy behavior

### Keep in notebook

- notebook 1 business framing
- notebook 4 cluster storytelling/reporting
- exploratory SHAP/PDP/plotting from notebook 2
- experimental clustering branches and narrative plots from notebook 3
- exploratory causal graph and estimator comparison sections from notebook 6

### Defer

- original model artifact recovery
- notebook 6 full causal training extraction
- GPU/embedding clustering path normalization
- Streamlit/UI wiring
- DB persistence layer wiring

## Module Responsibility Map

| Module | Responsibility | Source notebook(s) / data | Status | Notes |
| --- | --- | --- | --- | --- |
| `src/causal_app/ingestion/files.py` | Read CSV/XLSX uploads with basic safety checks | no direct notebook source | implemented | New service-layer code, not notebook-derived logic. |
| `src/causal_app/ingestion/validation.py` | Enforce minimal upload contract and capture rejected rows | inferred from legacy raw `train.csv` / `test.csv` schema | implemented | New service-layer code; avoids inventing extra business rules. |
| `src/causal_app/preprocessing/legacy_bank.py` | Notebook-derived preprocessing classes and feature projection | `Save_Model.ipynb`, `5_CAI_P_Post_Generated.ipynb`, `3_Clustering Model.ipynb` | implemented | Primary extraction point for reusable legacy transformations. |
| `src/causal_app/models/churn/legacy_churn.py` | Load or build churn scorer | `Save_Model.ipynb`, `5_CAI_P_Post_Generated.ipynb`, legacy `Data/train.csv` | temporary shim | Retrains from legacy `train.csv` because no original saved artifact was found. |
| `src/causal_app/models/segmentation/legacy_segmentation.py` | Assign clusters to new rows | `3_Clustering Model.ipynb`, legacy `Data/data from remote sever/df_cluster.csv` | temporary wrapper | Uses `NearestCentroid`; not the original embedding artifact. |
| `src/causal_app/models/recommendation/legacy_policy.py` | Recommend treatment/program options | `5_CAI_P_Post_Generated.ipynb`, `6_CAI_Model.ipynb`, legacy `df_causal_ai` | temporary wrapper | Uses cluster-level summary from simulated legacy causal table. |
| `src/causal_app/models/diagnostics/summary.py` | Build structured diagnostics outputs | no direct notebook source | implemented | New runtime-friendly summary layer. |
| `src/causal_app/export/excel.py` | Export workbook sheets for business use | no direct notebook source | implemented | Real export layer using confirmed pipeline outputs only. |
| `src/causal_app/pipeline/engine.py` | Orchestrate full non-notebook run | all extracted modules | implemented | Handles read -> validate -> preprocess -> churn -> segment -> recommend -> diagnostics -> export. |
| `src/causal_app/pipeline/run_pipeline.py` | CLI entrypoint | no direct notebook source | implemented | Current run path is `python -m causal_app.pipeline.run_pipeline`. |
| `src/causal_app/schemas/contracts.py` | Stable I/O contracts | inferred from Phase 3 engine needs | implemented | Keeps current engine explicit about required fields and outputs. |

## Notebook Traceability Notes

- `Save_Model.ipynb`
  - supplied the clearest churn preprocessing and classifier pipeline
- `5_CAI_P_Post_Generated.ipynb`
  - supplied the duplicate churn pipeline, treatment naming, and simulated post-treatment logic
- `3_Clustering Model.ipynb`
  - supplied the selected clustering features and scaling steps
- `6_CAI_Model.ipynb`
  - informed treatment naming and downstream recommendation framing, but its full estimator training flow was not extracted
- `2_Predict Churn Model.ipynb`
  - informed problem framing only in Phase 3; its evaluation/training path was not extracted because it is more EDA-heavy and has leakage risk
