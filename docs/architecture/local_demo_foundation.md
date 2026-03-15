# Local Demo Foundation

Phase 2 established the local-only foundation with:

- root-level repo structure
- `src/causal_app/` package skeleton
- Streamlit scaffold
- Postgres bootstrap
- Docker Compose startup path
- persistent `storage/` directories

Phase 3 added the first extracted engine modules under `src/causal_app/`:

- `ingestion/` for CSV/XLSX reading and dataset validation
- `preprocessing/legacy_bank.py` for notebook-derived feature preparation
- `models/churn/legacy_churn.py` for a temporary churn shim trained from legacy `train.csv`
- `models/segmentation/legacy_segmentation.py` for a temporary segmenter built from `df_cluster.csv`
- `models/recommendation/legacy_policy.py` for a temporary policy wrapper built from simulated `df_causal_ai`
- `models/diagnostics/summary.py` for structured diagnostic outputs
- `export/excel.py` for multi-sheet Excel export
- `pipeline/engine.py` and `pipeline/run_pipeline.py` for non-notebook execution

Phase 4 added the first usable Streamlit demo flow on top of that engine:

- upload registration into `storage/uploads/`
- lightweight profiling from the saved input file
- local file-based process tracking from run JSON outputs
- dashboard views backed by real diagnostics and recommendation files
- export downloads backed by generated workbook and CSV artifacts

Phase 5 improved the business handoff layer:

- business-friendly workbook sheets
- deterministic priority logic
- deterministic short business reasons
- reject-report detail mapping

Phase 6 added polish and extension-readiness:

- practical pytest coverage for ingestion, business output shaping, manifest writing, and workbook generation
- per-run logging to `run.log`
- shared pipeline logging to `storage/logs/pipeline.log`
- `artifact_manifest.json` for output traceability
- minor in-process caching for repeated local runs

## Explicitly Not Yet Connected

- database-backed upload flow
- real profiling engine
- verified parity with notebook metrics
- production-ready model artifacts or causal serving contracts

Important caveat:

- the app is usable locally as a data-scientist demo
- it is still not a production-grade service UI or persistence layer

This document should still be read as an incremental local-demo architecture, not feature completion.
