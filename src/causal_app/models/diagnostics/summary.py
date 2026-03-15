from __future__ import annotations

from collections import Counter
from typing import Any

import pandas as pd

from causal_app.schemas.contracts import StageResult, ValidationResult


def build_run_diagnostics(
    input_rows: int,
    validation: ValidationResult,
    recommendations: pd.DataFrame,
    rejected_rows: pd.DataFrame,
    stage_results: list[StageResult],
) -> dict[str, Any]:
    cluster_counts = (
        recommendations["assigned_cluster"].value_counts().sort_index().to_dict()
        if "assigned_cluster" in recommendations.columns and not recommendations.empty
        else {}
    )
    treatment_counts = (
        recommendations["recommended_treatment"].value_counts().sort_index().to_dict()
        if "recommended_treatment" in recommendations.columns and not recommendations.empty
        else {}
    )
    churn_summary = (
        recommendations["churn_probability"].agg(["min", "mean", "max"]).to_dict()
        if "churn_probability" in recommendations.columns and not recommendations.empty
        else {}
    )

    rejected_reason_counts = Counter()
    if not rejected_rows.empty and "reject_reasons" in rejected_rows.columns:
        for reasons in rejected_rows["reject_reasons"].fillna(""):
            for reason in str(reasons).split(";"):
                if reason:
                    rejected_reason_counts[reason] += 1

    return {
        "input_rows": int(input_rows),
        "accepted_rows": int(validation.accepted_rows),
        "rejected_rows": int(validation.rejected_rows),
        "duplicate_key_column": validation.duplicate_key_column,
        "validation_reject_reason_counts": dict(sorted(validation.reject_reason_counts.items())),
        "diagnostic_reject_reason_counts": dict(sorted(rejected_reason_counts.items())),
        "cluster_counts": cluster_counts,
        "recommended_treatment_counts": treatment_counts,
        "churn_probability_summary": {key: float(value) for key, value in churn_summary.items()},
        "stage_results": [stage.to_dict() for stage in stage_results],
    }


def diagnostics_to_summary_frame(diagnostics: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for key in ("input_rows", "accepted_rows", "rejected_rows", "duplicate_key_column"):
        rows.append({"metric": key, "value": diagnostics.get(key)})
    for key, value in diagnostics.get("churn_probability_summary", {}).items():
        rows.append({"metric": f"churn_probability_{key}", "value": value})
    for key, value in diagnostics.get("cluster_counts", {}).items():
        rows.append({"metric": f"cluster_{key}_count", "value": value})
    for key, value in diagnostics.get("recommended_treatment_counts", {}).items():
        rows.append({"metric": f"treatment_{key}_count", "value": value})
    for key, value in diagnostics.get("validation_reject_reason_counts", {}).items():
        rows.append({"metric": f"reject_reason_{key}", "value": value})
    return pd.DataFrame(rows)
