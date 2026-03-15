from __future__ import annotations

import pandas as pd
import streamlit as st

from causal_app.utils import get_run_record, list_run_records, load_json_if_exists


@st.cache_data(show_spinner=False)
def _load_stage_table(run_id: str) -> tuple[pd.DataFrame, dict | None]:
    record = get_run_record(run_id)
    if record is None:
        return pd.DataFrame(), None
    diagnostics = load_json_if_exists(record.diagnostics_path)
    return pd.DataFrame(record.stage_results), diagnostics


st.title("Process Tracking")
st.caption("Local file-based run tracking backed by `run_summary.json` and `diagnostics.json`. Postgres tracking is still deferred.")

run_records = list_run_records()
if not run_records:
    st.info("No runs have been recorded yet. Use the Upload page to trigger the pipeline first.")
    st.stop()

default_run_id = st.session_state.get("selected_run_id", run_records[0].run_id)
run_ids = [record.run_id for record in run_records]
if default_run_id not in run_ids:
    default_run_id = run_ids[0]

selected_run_id = st.selectbox(
    "Tracked runs",
    options=run_ids,
    index=run_ids.index(default_run_id),
    format_func=lambda run_id: next(
        (
            f"{record.created_at or 'unknown'} | {record.run_id} | accepted={record.accepted_rows} | rejected={record.rejected_rows}"
            for record in run_records
            if record.run_id == run_id
        ),
        run_id,
    ),
)
st.session_state["selected_run_id"] = selected_run_id
selected_run = next(record for record in run_records if record.run_id == selected_run_id)
stage_table, diagnostics = _load_stage_table(selected_run_id)

metric_columns = st.columns(5)
metric_columns[0].metric("Input Rows", selected_run.input_rows)
metric_columns[1].metric("Accepted Rows", selected_run.accepted_rows)
metric_columns[2].metric("Rejected Rows", selected_run.rejected_rows)
metric_columns[3].metric("Stages", len(selected_run.stage_results))
metric_columns[4].metric("Export Exists", "Yes" if selected_run.export_path.exists() else "No")

st.subheader("Run Metadata")
st.write(
    {
        "run_id": selected_run.run_id,
        "created_at": selected_run.created_at,
        "input_path": str(selected_run.input_path),
        "run_dir": str(selected_run.run_dir),
        "log_path": str(selected_run.log_path),
        "artifact_manifest_path": str(selected_run.artifact_manifest_path),
        "diagnostics_path": str(selected_run.diagnostics_path),
        "export_path": str(selected_run.export_path),
    }
)

st.subheader("Stage Timeline")
if stage_table.empty:
    st.warning("No stage metadata is available for this run.")
else:
    display_table = stage_table[
        [
            "stage_name",
            "status",
            "input_rows",
            "output_rows",
            "duration_seconds",
            "started_at",
            "finished_at",
            "details",
        ]
    ].copy()
    st.dataframe(display_table, use_container_width=True, height=420)

st.subheader("Artifact Availability")
artifact_rows = [
    {"artifact": "run.log", "path": str(selected_run.log_path), "exists": selected_run.log_path.exists()},
    {
        "artifact": "artifact_manifest.json",
        "path": str(selected_run.artifact_manifest_path),
        "exists": selected_run.artifact_manifest_path.exists(),
    },
    {"artifact": "prepared_features.csv", "path": str(selected_run.prepared_features_path), "exists": selected_run.prepared_features_path.exists()},
    {"artifact": "recommendations.csv", "path": str(selected_run.recommendations_path), "exists": selected_run.recommendations_path.exists()},
    {"artifact": "rejected_rows.csv", "path": str(selected_run.rejected_rows_path), "exists": selected_run.rejected_rows_path.exists()},
    {"artifact": "policy_options.csv", "path": str(selected_run.policy_options_path), "exists": selected_run.policy_options_path.exists()},
    {"artifact": "diagnostics.json", "path": str(selected_run.diagnostics_path), "exists": selected_run.diagnostics_path.exists()},
    {"artifact": "export.xlsx", "path": str(selected_run.export_path), "exists": selected_run.export_path.exists()},
]
st.dataframe(pd.DataFrame(artifact_rows), use_container_width=True)

st.subheader("Diagnostics Snapshot")
if diagnostics is None:
    st.warning("No diagnostics file was found for the selected run.")
else:
    st.write(
        {
            "duplicate_key_column": diagnostics.get("duplicate_key_column"),
            "validation_reject_reason_counts": diagnostics.get("validation_reject_reason_counts", {}),
            "cluster_counts": diagnostics.get("cluster_counts", {}),
            "recommended_treatment_counts": diagnostics.get("recommended_treatment_counts", {}),
        }
    )
    reject_reason_counts = diagnostics.get("validation_reject_reason_counts", {})
    if reject_reason_counts:
        st.bar_chart(reject_reason_counts)
