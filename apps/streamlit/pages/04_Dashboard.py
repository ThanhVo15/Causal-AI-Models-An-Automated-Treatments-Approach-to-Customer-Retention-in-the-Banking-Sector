from __future__ import annotations

import pandas as pd
import streamlit as st

from causal_app.utils import get_run_record, list_run_records, load_dataframe_if_exists, load_json_if_exists


@st.cache_data(show_spinner=False)
def _load_dashboard_bundle(run_id: str):
    record = get_run_record(run_id)
    if record is None:
        return None
    return {
        "diagnostics": load_json_if_exists(record.diagnostics_path),
        "recommendations": load_dataframe_if_exists(record.recommendations_path),
        "rejected_rows": load_dataframe_if_exists(record.rejected_rows_path),
        "policy_options": load_dataframe_if_exists(record.policy_options_path),
    }


def _series_from_mapping(mapping: dict) -> pd.Series:
    if not mapping:
        return pd.Series(dtype=float)
    return pd.Series(mapping).sort_index()


st.title("Dashboard")
st.caption("Real run outputs only. No fabricated business metrics are shown here.")

st.warning(
    """
Recommendation outputs shown here come from the temporary Phase 3 policy wrapper.

- they are traceable to archived legacy data
- they are useful for a local demo
- they are not yet a production-grade causal recommendation service
"""
)

run_records = list_run_records()
if not run_records:
    st.info("No pipeline runs are available yet. Use the Upload page first.")
    st.stop()

default_run_id = st.session_state.get("selected_run_id", run_records[0].run_id)
run_ids = [record.run_id for record in run_records]
if default_run_id not in run_ids:
    default_run_id = run_ids[0]

selected_run_id = st.selectbox(
    "Runs for dashboard review",
    options=run_ids,
    index=run_ids.index(default_run_id),
    format_func=lambda run_id: next(
        (
            f"{record.created_at or 'unknown'} | {record.run_id}"
            for record in run_records
            if record.run_id == run_id
        ),
        run_id,
    ),
)
st.session_state["selected_run_id"] = selected_run_id
bundle = _load_dashboard_bundle(selected_run_id)
if bundle is None:
    st.error("The selected run could not be loaded.")
    st.stop()

diagnostics = bundle["diagnostics"] or {}
recommendations = bundle["recommendations"]
rejected_rows = bundle["rejected_rows"]
policy_options = bundle["policy_options"]

metric_columns = st.columns(5)
metric_columns[0].metric("Input Rows", diagnostics.get("input_rows", 0))
metric_columns[1].metric("Accepted Rows", diagnostics.get("accepted_rows", 0))
metric_columns[2].metric("Rejected Rows", diagnostics.get("rejected_rows", 0))
metric_columns[3].metric(
    "Mean Churn",
    round(float(diagnostics.get("churn_probability_summary", {}).get("mean", 0.0)), 4),
)
metric_columns[4].metric(
    "Recommended Treatments",
    int(sum(diagnostics.get("recommended_treatment_counts", {}).values())),
)

chart_left, chart_right = st.columns(2)
with chart_left:
    st.subheader("Assigned Cluster Distribution")
    cluster_series = _series_from_mapping(diagnostics.get("cluster_counts", {}))
    if cluster_series.empty:
        st.info("No cluster counts are available for this run.")
    else:
        st.bar_chart(cluster_series)

with chart_right:
    st.subheader("Recommended Treatment Distribution")
    treatment_series = _series_from_mapping(diagnostics.get("recommended_treatment_counts", {}))
    if treatment_series.empty:
        st.info("No treatment counts are available for this run.")
    else:
        st.bar_chart(treatment_series)

st.subheader("Churn Probability Distribution")
if recommendations is None or recommendations.empty or "churn_probability" not in recommendations.columns:
    st.info("No churn probability distribution is available for this run.")
else:
    distribution = (
        recommendations["churn_probability"]
        .clip(0, 1)
        .pipe(lambda series: pd.cut(series, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True))
        .value_counts()
        .sort_index()
    )
    st.bar_chart(distribution)

if recommendations is not None and not recommendations.empty:
    st.subheader("Top Recommended Actions")
    display_columns = [
        column
        for column in [
            "source_row_number",
            "CustomerId",
            "Surname",
            "churn_probability",
            "assigned_cluster",
            "recommended_treatment",
            "estimated_post_churn",
            "expected_absolute_change",
            "policy_scope",
            "policy_sample_size",
        ]
        if column in recommendations.columns
    ]
    top_actions = recommendations.sort_values("churn_probability", ascending=False).head(100)
    st.dataframe(top_actions[display_columns], use_container_width=True, height=420)
else:
    st.info("The selected run did not produce any accepted recommendations.")

lower_left, lower_right = st.columns(2)
with lower_left:
    st.subheader("Reject Summary")
    reject_reason_series = _series_from_mapping(diagnostics.get("validation_reject_reason_counts", {}))
    if reject_reason_series.empty:
        st.success("No rejected rows were recorded for this run.")
    else:
        st.bar_chart(reject_reason_series)
        if rejected_rows is not None and not rejected_rows.empty:
            st.dataframe(rejected_rows.head(50), use_container_width=True)

with lower_right:
    st.subheader("Policy Options Snapshot")
    if policy_options is None or policy_options.empty:
        st.info("No policy options file is available for this run.")
    else:
        st.dataframe(policy_options.head(100), use_container_width=True, height=420)
