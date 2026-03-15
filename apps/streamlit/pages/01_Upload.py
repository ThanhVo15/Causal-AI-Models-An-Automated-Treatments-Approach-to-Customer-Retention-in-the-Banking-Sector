from __future__ import annotations

from pathlib import Path

import streamlit as st

from causal_app.config import get_settings
from causal_app.ingestion.files import InputFileError, read_input_dataset
from causal_app.ingestion.validation import DatasetContractError, validate_input_dataframe
from causal_app.pipeline.engine import PipelineExecutionError, run_pipeline
from causal_app.utils import list_upload_records, register_existing_input, save_uploaded_bytes


settings = get_settings()


@st.cache_data(show_spinner=False)
def _validate_preview(path_str: str):
    dataframe = read_input_dataset(Path(path_str))
    accepted, rejected, summary = validate_input_dataframe(dataframe)
    return dataframe, accepted, rejected, summary.to_dict()


st.title("Upload")
st.caption("Register a real input dataset, preview it, validate it, and trigger the Phase 3 pipeline.")

st.info(
    """
This page is wired to the real Phase 3 engine.

- uploads are persisted under `storage/uploads/`
- validation uses the extracted ingestion contract
- pipeline runs call `src/causal_app/pipeline/engine.py`
- Postgres dataset registration is still deferred
"""
)

with st.expander("Input contract"):
    st.markdown(
        """
Required columns:

- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`

Optional columns:

- `id`
- `CustomerId`
- `Surname`
- `Exited`
"""
    )

uploaded_file = st.file_uploader("Upload a CSV or XLSX dataset", type=["csv", "xlsx"])
action_columns = st.columns([1.2, 1.0, 1.2])

with action_columns[0]:
    if uploaded_file is not None:
        st.write(
            {
                "file_name": uploaded_file.name,
                "size_bytes": uploaded_file.size,
                "content_type": uploaded_file.type,
            }
        )
        if st.button("Save Uploaded File", type="primary", use_container_width=True):
            record = save_uploaded_bytes(uploaded_file.name, uploaded_file.getvalue(), source="streamlit_upload")
            st.session_state["selected_upload_id"] = record.upload_id
            st.success(f"Saved upload as `{record.stored_name}`")
            st.rerun()

with action_columns[1]:
    st.markdown("**Archived example**")
    st.caption("No curated sample file exists in `data/samples/`, but the archived legacy `test.csv` can be registered for smoke testing.")
    if st.button("Register Legacy test.csv", use_container_width=True):
        record = register_existing_input(
            settings.legacy_test_path,
            label="legacy_test.csv",
            source="archived_legacy_example",
        )
        st.session_state["selected_upload_id"] = record.upload_id
        st.success(f"Registered archived legacy example as `{record.stored_name}`")
        st.rerun()

with action_columns[2]:
    st.markdown("**Run note**")
    st.caption("The first run may take longer because temporary Phase 3 artifacts can be built from archived legacy CSVs.")

upload_records = list_upload_records()
if not upload_records:
    st.warning("No saved uploads are available yet. Upload a file above or register the archived legacy example.")
    st.stop()

default_upload_id = st.session_state.get("selected_upload_id", upload_records[0].upload_id)
upload_ids = [record.upload_id for record in upload_records]
if default_upload_id not in upload_ids:
    default_upload_id = upload_ids[0]

selected_upload_id = st.selectbox(
    "Saved uploads",
    options=upload_ids,
    index=upload_ids.index(default_upload_id),
    format_func=lambda upload_id: next(
        (
            f"{record.uploaded_at} | {record.original_name} | {record.source}"
            for record in upload_records
            if record.upload_id == upload_id
        ),
        upload_id,
    ),
)
st.session_state["selected_upload_id"] = selected_upload_id
selected_record = next(record for record in upload_records if record.upload_id == selected_upload_id)

st.subheader("Selected Upload Metadata")
st.write(
    {
        "upload_id": selected_record.upload_id,
        "original_name": selected_record.original_name,
        "stored_path": str(selected_record.storage_path),
        "uploaded_at": selected_record.uploaded_at,
        "size_bytes": selected_record.size_bytes,
        "source": selected_record.source,
    }
)

try:
    preview_df, accepted_df, rejected_df, validation_summary = _validate_preview(str(selected_record.storage_path))
except (InputFileError, DatasetContractError) as exc:
    st.error(f"Validation could not run on the selected input: {exc}")
    st.stop()
except Exception as exc:
    st.error(f"Unexpected error while reading the selected input: {exc}")
    st.stop()

metric_columns = st.columns(4)
metric_columns[0].metric("Input Rows", len(preview_df))
metric_columns[1].metric("Accepted Rows", validation_summary["accepted_rows"])
metric_columns[2].metric("Rejected Rows", validation_summary["rejected_rows"])
metric_columns[3].metric("Columns", len(preview_df.columns))

preview_columns = st.columns(2)
with preview_columns[0]:
    st.subheader("Preview")
    st.dataframe(preview_df.head(25), use_container_width=True)

with preview_columns[1]:
    st.subheader("Validation Summary")
    st.write(validation_summary)
    reject_reason_counts = validation_summary.get("reject_reason_counts", {})
    if reject_reason_counts:
        st.bar_chart(reject_reason_counts)
    else:
        st.success("No validation rejects were detected on the selected input.")

if not rejected_df.empty:
    with st.expander("Rejected Row Preview"):
        st.dataframe(rejected_df.head(50), use_container_width=True)

st.subheader("Run Pipeline")
st.caption("This triggers the extracted Phase 3 engine against the selected saved input file.")
if st.button("Run Pipeline On Selected Input", type="primary"):
    try:
        with st.spinner("Running pipeline..."):
            result = run_pipeline(
                input_path=selected_record.storage_path,
                run_label=selected_record.upload_id,
            )
        st.session_state["selected_run_id"] = result.run_id
        st.success(f"Pipeline completed for run `{result.run_id}`")
        st.write(
            {
                "run_dir": str(result.run_dir),
                "export_path": str(result.export_path),
                "log_path": str(result.log_path),
                "artifact_manifest_path": str(result.artifact_manifest_path),
                "accepted_rows": result.accepted_rows,
                "rejected_rows": result.rejected_rows,
            }
        )
    except PipelineExecutionError as exc:
        st.error(str(exc))
        st.write(
            {
                "run_id": exc.run_id,
                "run_dir": str(exc.run_dir),
                "log_path": str(exc.log_path),
                "failed_stage": exc.failed_stage,
            }
        )
    except Exception as exc:
        st.error(f"Pipeline execution failed: {exc}")
