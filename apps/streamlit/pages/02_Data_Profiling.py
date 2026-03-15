from __future__ import annotations

from pathlib import Path

import streamlit as st

from causal_app.ingestion.files import InputFileError, read_input_dataset
from causal_app.ingestion.validation import DatasetContractError, validate_input_dataframe
from causal_app.profiling import build_profile_summary
from causal_app.utils import list_upload_records


@st.cache_data(show_spinner=False)
def _load_profile_bundle(path_str: str):
    dataframe = read_input_dataset(Path(path_str))
    profile = build_profile_summary(dataframe)
    accepted, rejected, validation = validate_input_dataframe(dataframe)
    return dataframe, profile, accepted, rejected, validation.to_dict()


st.title("Data Profiling")
st.caption("Lightweight profiling from the actual saved input file. This is not a full profiling-report engine.")

upload_records = list_upload_records()
if not upload_records:
    st.info("No saved uploads are available yet. Use the Upload page first.")
    st.stop()

default_upload_id = st.session_state.get("selected_upload_id", upload_records[0].upload_id)
upload_ids = [record.upload_id for record in upload_records]
if default_upload_id not in upload_ids:
    default_upload_id = upload_ids[0]

selected_upload_id = st.selectbox(
    "Profile a saved upload",
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

try:
    raw_df, profile, accepted_df, rejected_df, validation = _load_profile_bundle(str(selected_record.storage_path))
except (InputFileError, DatasetContractError) as exc:
    st.error(f"Profiling could not be generated: {exc}")
    st.stop()
except Exception as exc:
    st.error(f"Unexpected profiling error: {exc}")
    st.stop()

metric_columns = st.columns(5)
metric_columns[0].metric("Rows", profile["row_count"])
metric_columns[1].metric("Columns", profile["column_count"])
metric_columns[2].metric(
    "Required Present",
    int(profile["schema_status"].query("kind == 'required' and present == True").shape[0]),
)
metric_columns[3].metric("Accepted Rows", validation["accepted_rows"])
metric_columns[4].metric("Rejected Rows", validation["rejected_rows"])

st.subheader("Schema Status")
st.dataframe(profile["schema_status"], use_container_width=True)

columns_left, columns_right = st.columns(2)
with columns_left:
    st.subheader("Column Summary")
    st.dataframe(profile["column_summary"], use_container_width=True, height=420)

with columns_right:
    st.subheader("Missing Value Summary")
    if profile["missing_summary"].empty:
        st.success("No missing values were detected in the current file preview.")
    else:
        st.dataframe(profile["missing_summary"], use_container_width=True, height=420)

st.subheader("Duplicate Summary")
if profile["duplicate_summary"].empty:
    st.info("No duplicate-key check was available because neither `CustomerId` nor `id` is present.")
else:
    st.dataframe(profile["duplicate_summary"], use_container_width=True)

st.subheader("Validation Readiness")
st.write(validation)
reject_reason_counts = validation.get("reject_reason_counts", {})
if reject_reason_counts:
    st.bar_chart(reject_reason_counts)

with st.expander("Numeric Summary"):
    if profile["numeric_summary"].empty:
        st.info("No numeric summary is available because the dataframe has no numeric columns after parsing.")
    else:
        st.dataframe(profile["numeric_summary"], use_container_width=True)

with st.expander("Raw Data Preview"):
    st.dataframe(raw_df.head(50), use_container_width=True)

if not rejected_df.empty:
    with st.expander("Rejected Rows Preview"):
        st.dataframe(rejected_df.head(50), use_container_width=True)

if not accepted_df.empty:
    with st.expander("Accepted Rows Preview"):
        st.dataframe(accepted_df.head(50), use_container_width=True)
