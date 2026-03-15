from __future__ import annotations

from pathlib import Path

import pandas as pd

from causal_app.export.business_output import build_customer_action_list, build_reject_report


def test_customer_action_list_priority_and_reason_logic():
    recommendations = pd.DataFrame(
        [
            {
                "source_row_number": 2,
                "CustomerId": 1001,
                "Surname": "Alpha",
                "Geography": "Germany",
                "Age": 45,
                "Balance": 10000.0,
                "NumOfProducts": 1,
                "churn_probability": 0.91,
                "assigned_cluster": 1,
                "recommended_treatment": "Engage & Elevate",
                "estimated_post_churn": 0.85,
                "expected_absolute_change": -0.06,
                "policy_scope": "cluster_specific",
                "policy_sample_size": 42,
            },
            {
                "source_row_number": 3,
                "CustomerId": 1002,
                "Surname": "Beta",
                "Geography": "France",
                "Age": 39,
                "Balance": 5000.0,
                "NumOfProducts": 2,
                "churn_probability": 0.81,
                "assigned_cluster": 3,
                "recommended_treatment": "Reconnect & Reward",
                "estimated_post_churn": 0.80,
                "expected_absolute_change": -0.01,
                "policy_scope": "cluster_specific",
                "policy_sample_size": 18,
            },
            {
                "source_row_number": 4,
                "CustomerId": 1003,
                "Surname": "Gamma",
                "Geography": "Spain",
                "Age": 32,
                "Balance": 0.0,
                "NumOfProducts": 2,
                "churn_probability": 0.22,
                "assigned_cluster": 2,
                "recommended_treatment": "No Program",
                "estimated_post_churn": 0.22,
                "expected_absolute_change": 0.0,
                "policy_scope": "cluster_specific",
                "policy_sample_size": 5,
            },
            {
                "source_row_number": 5,
                "CustomerId": 1004,
                "Surname": "Delta",
                "Geography": "France",
                "Age": 28,
                "Balance": 500.0,
                "NumOfProducts": 1,
                "churn_probability": 0.51,
                "assigned_cluster": 9,
                "recommended_treatment": "Starter Growth Plan",
                "estimated_post_churn": 0.49,
                "expected_absolute_change": -0.02,
                "policy_scope": "overall_fallback",
                "policy_sample_size": 7,
            },
        ]
    )

    action_list = build_customer_action_list(recommendations, run_id="demo-run")

    assert list(action_list["priority_band"][:3]) == ["P1", "P2", "P2"]
    assert action_list.iloc[0]["reason_short"].startswith("High churn risk; Engage & Elevate is prioritized")
    assert "no special program" in action_list[action_list["customer_id"] == "1003"].iloc[0]["reason_short"].lower()
    fallback_row = action_list[action_list["customer_id"] == "1004"].iloc[0]
    assert fallback_row["warning_note"] != ""
    assert fallback_row["reason_short"].startswith("Fallback policy Starter Growth Plan")


def test_reject_report_maps_reason_details():
    rejected_rows = pd.DataFrame(
        [
            {
                "_source_row_number": 10,
                "CustomerId": 2001,
                "Surname": "Reject",
                "Geography": "France",
                "reject_reasons": "duplicate_customerid;invalid_geography",
            }
        ]
    )

    reject_report = build_reject_report(rejected_rows, run_id="demo-run", input_path=Path("input.csv"))

    assert reject_report.iloc[0]["rejection_status"] == "Rejected"
    assert "CustomerId was duplicated" in reject_report.iloc[0]["reject_reason_detail"]
    assert "Geography must normalize" in reject_report.iloc[0]["reject_reason_detail"]
