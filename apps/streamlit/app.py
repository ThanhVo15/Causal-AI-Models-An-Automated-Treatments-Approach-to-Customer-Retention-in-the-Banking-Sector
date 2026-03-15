from __future__ import annotations

from pathlib import Path

import streamlit as st

from causal_app.config import get_settings
from causal_app.utils import list_run_records, list_upload_records
from causal_app.utils.paths import ensure_runtime_directories
from causal_app.utils.status import scaffold_status


st.set_page_config(page_title="Causal AI Local Demo", page_icon=":bar_chart:", layout="wide")

settings = get_settings()
runtime_paths = ensure_runtime_directories()
status = scaffold_status()
uploads = list_upload_records()
runs = list_run_records()
phase_03_artifact_dir = settings.artifacts_root / "models" / "phase_03"
phase_03_artifacts = sorted(path.name for path in phase_03_artifact_dir.glob("*")) if phase_03_artifact_dir.exists() else []
export_files = sorted(runtime_paths["exports"].glob("*.xlsx"))

st.title(settings.app_name)
st.caption("Phase 6 local demo app: runnable, traceable, and still explicit about what remains partial.")

st.warning(
    """
The current recommendation flow is still based on temporary legacy wrappers:

- churn is retrained from archived `train.csv` if no Phase 3 artifact exists
- segmentation is inferred from exported `df_cluster.csv` labels
- recommendation policy is derived from simulated legacy `df_causal_ai`
"""
)

metric_columns = st.columns(4)
metric_columns[0].metric("Saved Uploads", len(uploads))
metric_columns[1].metric("Pipeline Runs", len(runs))
metric_columns[2].metric("Excel Exports", len(export_files))
metric_columns[3].metric("Phase 3 Artifacts", len(phase_03_artifacts))

overview_left, overview_right = st.columns([1.4, 1.0])

with overview_left:
    st.subheader("Runtime Context")
    st.write(
        {
            "app_env": settings.app_env,
            "log_level": settings.log_level,
            "storage_root": str(settings.storage_root),
            "legacy_bundle_root": str(settings.legacy_bundle_root),
            "legacy_test_path": str(settings.legacy_test_path),
            "database_url": settings.database_url,
        }
    )

    st.subheader("Current Capability Map")
    for section, items in status.items():
        st.markdown(f"**{section.replace('_', ' ').title()}**")
        for item in items:
            st.write(f"- {item}")

with overview_right:
    st.subheader("Runtime Directories")
    st.write({name: str(path) for name, path in runtime_paths.items()})

    st.subheader("Phase 3 Artifacts")
    if phase_03_artifacts:
        for artifact_name in phase_03_artifacts:
            st.write(f"- {artifact_name}")
    else:
        st.info("No Phase 3 artifacts have been built yet. The first successful pipeline run will create them.")

st.subheader("Latest Activity")
if runs:
    latest_run = runs[0]
    st.write(
        {
            "run_id": latest_run.run_id,
            "created_at": latest_run.created_at,
            "input_rows": latest_run.input_rows,
            "accepted_rows": latest_run.accepted_rows,
            "rejected_rows": latest_run.rejected_rows,
            "input_path": str(latest_run.input_path),
            "export_path_exists": latest_run.export_path.exists(),
        }
    )
else:
    st.info("No pipeline runs are recorded yet. Start from the Upload page to register an input file and trigger the engine.")

st.subheader("Where To Go Next")
st.markdown(
    """
- `Upload`: save a CSV/XLSX input, preview it, validate it, and trigger a run
- `Data Profiling`: inspect schema, missing values, duplicates, and lightweight profile summaries
- `Process Tracking`: inspect stage-by-stage run metadata and artifact locations
- `Dashboard`: review real diagnostics, churn/cluster/treatment summaries, and output tables
- `Export`: download the generated Excel workbook and CSV outputs
"""
)

st.subheader("Useful Repo Paths")
st.write(
    {
        "phase_memory": str(Path("instructs").resolve()),
        "migration_docs": str(Path("docs/migration").resolve()),
        "local_run_guide": str(Path("docs/user_guide/local_startup.md").resolve()),
    }
)
