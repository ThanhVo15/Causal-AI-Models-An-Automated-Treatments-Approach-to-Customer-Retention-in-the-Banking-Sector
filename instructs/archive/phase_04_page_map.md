# Phase 04 Page Map

## Page-By-Page Map

| Page | Purpose | Inputs | Outputs | Engine dependencies | Known limitations |
| --- | --- | --- | --- | --- | --- |
| `apps/streamlit/app.py` | Overview, capability map, latest activity | local storage state, artifact directory | runtime context, counts, capability notes | `list_upload_records`, `list_run_records`, `scaffold_status` | overview only; no run action |
| `apps/streamlit/pages/01_Upload.py` | Register inputs and trigger pipeline | uploaded CSV/XLSX or archived legacy `test.csv` | saved upload metadata, preview, validation summary, run trigger result | `save_uploaded_bytes`, `register_existing_input`, `read_input_dataset`, `validate_input_dataframe`, `run_pipeline` | no Postgres dataset registration; run failures are shown in-page only |
| `apps/streamlit/pages/02_Data_Profiling.py` | Lightweight dataset profiling | saved upload selection | schema status, missing summary, duplicates, numeric summary, previews | `read_input_dataset`, `build_profile_summary`, `validate_input_dataframe` | not a full profiling report engine |
| `apps/streamlit/pages/03_Process_Tracking.py` | Inspect run metadata and stage flow | saved run selection | stage table, durations, artifact existence, diagnostics snapshot | `list_run_records`, `get_run_record`, `load_json_if_exists` | local file-based only; no DB-backed history |
| `apps/streamlit/pages/04_Dashboard.py` | Review real pipeline results | saved run selection | counts, churn distribution, cluster/treatment charts, recommendation table, reject summary | `list_run_records`, `get_run_record`, `load_json_if_exists`, `load_dataframe_if_exists` | only shows what the Phase 3 engine already emits; recommendation remains simulation-backed |
| `apps/streamlit/pages/05_Export.py` | Download generated outputs | saved run selection | workbook/CSV download buttons | `list_run_records`, `get_run_record` | no DB export metadata; no polished separate business-report export |

## Capability Classification

### Ready to wire now

- Upload
- Process Tracking
- Export

### Wire with partial support

- Data Profiling
- Dashboard

### Placeholder only

- Postgres-backed metadata persistence

### Deferred

- multi-run DB audit trail
- richer business visualizations beyond current engine outputs
- notebook-parity comparison UI
