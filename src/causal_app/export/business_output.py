from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


HIGH_RISK_THRESHOLD = 0.75
MEDIUM_RISK_THRESHOLD = 0.50
P1_IMPROVEMENT_THRESHOLD = 0.03
P2_IMPROVEMENT_THRESHOLD = 0.02


REJECT_REASON_DETAILS = {
    "invalid_creditscore": "CreditScore could not be parsed as a numeric value.",
    "invalid_age": "Age could not be parsed as a numeric value.",
    "invalid_tenure": "Tenure could not be parsed as a numeric value.",
    "invalid_balance": "Balance could not be parsed as a numeric value.",
    "invalid_numofproducts": "NumOfProducts could not be parsed as a numeric value.",
    "invalid_estimatedsalary": "EstimatedSalary could not be parsed as a numeric value.",
    "invalid_hascrcard": "HasCrCard must be 0/1, true/false, or yes/no.",
    "invalid_isactivemember": "IsActiveMember must be 0/1, true/false, or yes/no.",
    "invalid_gender": "Gender must normalize to Female or Male.",
    "invalid_geography": "Geography must normalize to France, Germany, or Spain.",
    "invalid_exited": "Exited must be 0/1 if provided.",
    "duplicate_customerid": "CustomerId was duplicated in the uploaded file.",
    "duplicate_id": "id was duplicated in the uploaded file.",
}


def _safe_float(value: object, default: float = 0.0) -> float:
    if pd.isna(value):
        return default
    return float(value)


def _choose_customer_id(row: pd.Series) -> tuple[str, str]:
    customer_id = row.get("CustomerId")
    if pd.notna(customer_id):
        return str(customer_id), "CustomerId"
    fallback_id = row.get("id")
    if pd.notna(fallback_id):
        return str(fallback_id), "id"
    return "", "unavailable"


def _risk_level(churn_probability: float) -> str:
    if churn_probability >= HIGH_RISK_THRESHOLD:
        return "High"
    if churn_probability >= MEDIUM_RISK_THRESHOLD:
        return "Medium"
    return "Low"


def _priority_band(churn_probability: float, expected_improvement: float) -> str:
    risk_level = _risk_level(churn_probability)
    if risk_level == "High" and expected_improvement >= P1_IMPROVEMENT_THRESHOLD:
        return "P1"
    if risk_level == "High":
        return "P2"
    if risk_level == "Medium" and expected_improvement >= P2_IMPROVEMENT_THRESHOLD:
        return "P2"
    return "P3"


def _warning_note(policy_scope: str) -> str:
    if policy_scope == "overall_fallback":
        return "Fallback recommendation used because cluster-specific policy support was unavailable."
    return ""


def _reason_short(
    risk_level: str,
    recommended_policy: str,
    segment_id: object,
    expected_improvement: float,
    policy_scope: str,
) -> str:
    segment_text = f"cluster {segment_id}"
    if policy_scope == "overall_fallback":
        return f"Fallback policy {recommended_policy} is used because {segment_text} has no cluster-specific support table."
    if recommended_policy == "No Program":
        if risk_level == "High":
            return f"High churn risk, but no special program stands out for {segment_text} in the current policy table."
        if risk_level == "Medium":
            return f"Medium churn risk; no special program is currently prioritized for {segment_text}."
        return f"Lower churn risk; no special program is currently prioritized for {segment_text}."
    if risk_level == "High" and expected_improvement >= P1_IMPROVEMENT_THRESHOLD:
        return f"High churn risk; {recommended_policy} is prioritized for {segment_text} based on the strongest estimated reduction."
    if risk_level == "High":
        return f"High churn risk; {recommended_policy} is the current top-ranked action for {segment_text}."
    if risk_level == "Medium":
        return f"Medium churn risk; {recommended_policy} is the current recommended next action for {segment_text}."
    return f"Lower churn risk; {recommended_policy} remains the current retention action for {segment_text}."


def _reason_detail(reject_reason_codes: str) -> str:
    details: list[str] = []
    for reason in str(reject_reason_codes or "").split(";"):
        reason = reason.strip()
        if not reason:
            continue
        details.append(REJECT_REASON_DETAILS.get(reason, reason.replace("_", " ").capitalize() + "."))
    return " | ".join(details)


def build_customer_action_list(recommendations: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if recommendations.empty:
        return pd.DataFrame(
            columns=[
                "run_id",
                "customer_id",
                "customer_id_source",
                "source_row_number",
                "customer_surname",
                "geography",
                "age",
                "balance",
                "num_products",
                "churn_probability",
                "risk_level",
                "segment_id",
                "recommended_policy",
                "expected_post_churn",
                "expected_improvement",
                "priority_score",
                "priority_band",
                "reason_short",
                "recommendation_scope",
                "policy_support_rows",
                "warning_note",
            ]
        )

    rows: list[dict[str, Any]] = []
    for _, row in recommendations.iterrows():
        customer_id, customer_id_source = _choose_customer_id(row)
        churn_probability = round(_safe_float(row.get("churn_probability")), 4)
        expected_post_churn = round(_safe_float(row.get("estimated_post_churn")), 4)
        expected_improvement = round(max(-_safe_float(row.get("expected_absolute_change")), 0.0), 4)
        risk_level = _risk_level(churn_probability)
        policy_scope = str(row.get("policy_scope") or "unknown")
        recommended_policy = str(row.get("recommended_treatment") or "No Program")
        segment_id = row.get("assigned_cluster")

        rows.append(
            {
                "run_id": run_id,
                "customer_id": customer_id,
                "customer_id_source": customer_id_source,
                "source_row_number": row.get("source_row_number"),
                "customer_surname": row.get("Surname", ""),
                "geography": row.get("Geography", ""),
                "age": row.get("Age", ""),
                "balance": row.get("Balance", ""),
                "num_products": row.get("NumOfProducts", ""),
                "churn_probability": churn_probability,
                "risk_level": risk_level,
                "segment_id": segment_id,
                "recommended_policy": recommended_policy,
                "expected_post_churn": expected_post_churn,
                "expected_improvement": expected_improvement,
                "priority_score": round(churn_probability * 100, 1),
                "priority_band": _priority_band(churn_probability, expected_improvement),
                "reason_short": _reason_short(
                    risk_level=risk_level,
                    recommended_policy=recommended_policy,
                    segment_id=segment_id,
                    expected_improvement=expected_improvement,
                    policy_scope=policy_scope,
                ),
                "recommendation_scope": policy_scope,
                "policy_support_rows": row.get("policy_sample_size", ""),
                "warning_note": _warning_note(policy_scope),
            }
        )

    action_list = pd.DataFrame(rows)
    priority_order = {"P1": 1, "P2": 2, "P3": 3}
    action_list["_priority_sort"] = action_list["priority_band"].map(priority_order).fillna(99)
    action_list = action_list.sort_values(
        ["_priority_sort", "priority_score", "expected_improvement"],
        ascending=[True, False, False],
    ).drop(columns=["_priority_sort"])
    return action_list.reset_index(drop=True)


def build_reject_report(rejected_rows: pd.DataFrame, run_id: str, input_path: Path) -> pd.DataFrame:
    if rejected_rows.empty:
        return pd.DataFrame(
            columns=[
                "run_id",
                "source_file",
                "source_row_number",
                "customer_id",
                "customer_id_source",
                "customer_surname",
                "geography",
                "rejection_status",
                "rejection_stage",
                "reject_reason_codes",
                "reject_reason_detail",
            ]
        )

    rows: list[dict[str, Any]] = []
    for _, row in rejected_rows.iterrows():
        customer_id, customer_id_source = _choose_customer_id(row)
        reject_reason_codes = str(row.get("reject_reasons") or "")
        rows.append(
            {
                "run_id": run_id,
                "source_file": input_path.name,
                "source_row_number": row.get("_source_row_number"),
                "customer_id": customer_id,
                "customer_id_source": customer_id_source,
                "customer_surname": row.get("Surname", ""),
                "geography": row.get("Geography", ""),
                "rejection_status": "Rejected",
                "rejection_stage": "validate_input",
                "reject_reason_codes": reject_reason_codes,
                "reject_reason_detail": _reason_detail(reject_reason_codes),
            }
        )
    return pd.DataFrame(rows)


def build_summary_sheet(
    diagnostics: dict[str, Any],
    action_list: pd.DataFrame,
    reject_report: pd.DataFrame,
    run_id: str,
    input_path: Path,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {"section": "Run", "metric": "run_id", "value": run_id, "notes": ""},
        {"section": "Run", "metric": "input_file", "value": input_path.name, "notes": ""},
        {
            "section": "Run",
            "metric": "export_generated_at_utc",
            "value": datetime.now(timezone.utc).isoformat(),
            "notes": "",
        },
        {"section": "Volume", "metric": "uploaded_rows", "value": diagnostics.get("input_rows", 0), "notes": ""},
        {"section": "Volume", "metric": "valid_rows", "value": diagnostics.get("accepted_rows", 0), "notes": ""},
        {"section": "Volume", "metric": "rejected_rows", "value": diagnostics.get("rejected_rows", 0), "notes": ""},
    ]

    if not action_list.empty:
        for band, count in action_list["priority_band"].value_counts().sort_index().items():
            rows.append({"section": "Priority", "metric": f"{band}_count", "value": int(count), "notes": ""})
        for level, count in action_list["risk_level"].value_counts().sort_index().items():
            rows.append({"section": "Risk", "metric": f"{level}_risk_count", "value": int(count), "notes": ""})
        for policy, count in action_list["recommended_policy"].value_counts().sort_index().items():
            rows.append({"section": "Policy", "metric": f"{policy}_count", "value": int(count), "notes": ""})
        for segment, count in action_list["segment_id"].value_counts().sort_index().items():
            rows.append({"section": "Segment", "metric": f"cluster_{segment}_count", "value": int(count), "notes": ""})
    else:
        rows.append(
            {
                "section": "Action List",
                "metric": "status",
                "value": "No accepted recommendation rows were generated.",
                "notes": "",
            }
        )

    reject_reason_counts = diagnostics.get("validation_reject_reason_counts", {})
    for reason, count in reject_reason_counts.items():
        rows.append({"section": "Rejects", "metric": reason, "value": int(count), "notes": _reason_detail(reason)})

    rows.extend(
        [
            {
                "section": "Limitations",
                "metric": "recommendation_logic",
                "value": "Current policy recommendations are derived from a temporary legacy wrapper.",
                "notes": "The source policy table ultimately comes from simulated legacy causal data.",
            },
            {
                "section": "Limitations",
                "metric": "priority_logic",
                "value": "Priority is based on churn probability with deterministic banding rules.",
                "notes": "No customer value score or LLM-based explanation is used.",
            },
        ]
    )

    return pd.DataFrame(rows)


def build_run_metadata_sheet(
    diagnostics: dict[str, Any],
    run_id: str,
    input_path: Path,
    export_path: Path,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {"item": "run_id", "value": run_id},
        {"item": "input_file", "value": input_path.name},
        {"item": "input_path", "value": str(input_path)},
        {"item": "export_path", "value": str(export_path)},
    ]
    for stage in diagnostics.get("stage_results", []):
        rows.append(
            {
                "item": f"stage::{stage.get('stage_name')}::{stage.get('status')}",
                "value": f"input_rows={stage.get('input_rows')} output_rows={stage.get('output_rows')} duration_seconds={stage.get('duration_seconds')}",
            }
        )
    return pd.DataFrame(rows)


def build_field_definitions_sheet() -> pd.DataFrame:
    rows = [
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "customer_id",
            "source_field": "CustomerId or id",
            "description": "Best available customer identifier from the uploaded file.",
            "derivation": "Use CustomerId when present; otherwise use id.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "churn_probability",
            "source_field": "churn_probability",
            "description": "Predicted churn probability from the current Phase 3 churn shim.",
            "derivation": "Direct carry-through from recommendations.csv.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "risk_level",
            "source_field": "churn_probability",
            "description": "Simple risk band for business triage.",
            "derivation": "High if >= 0.75, Medium if >= 0.50, else Low.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "segment_id",
            "source_field": "assigned_cluster",
            "description": "Cluster identifier from the temporary segmentation wrapper.",
            "derivation": "Direct carry-through from recommendations.csv.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "recommended_policy",
            "source_field": "recommended_treatment",
            "description": "Current top-ranked retention policy for the record.",
            "derivation": "Direct carry-through from recommendations.csv.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "expected_improvement",
            "source_field": "expected_absolute_change",
            "description": "Estimated reduction in churn probability for the selected policy.",
            "derivation": "max(-expected_absolute_change, 0.0).",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "priority_score",
            "source_field": "churn_probability",
            "description": "Simple business sorting score for the action list.",
            "derivation": "churn_probability * 100.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "priority_band",
            "source_field": "churn_probability, expected_improvement",
            "description": "Priority bucket for action-taking.",
            "derivation": "P1/P2/P3 deterministic rules documented in phase_05_priority_logic.md.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "reason_short",
            "source_field": "risk_level, recommended_policy, segment_id, expected_improvement, policy_scope",
            "description": "Short rule-based business explanation.",
            "derivation": "Deterministic template logic documented in phase_05_reason_logic.md.",
        },
        {
            "sheet_name": "Customer_Action_List",
            "column_name": "recommendation_scope",
            "source_field": "policy_scope",
            "description": "Shows whether the recommendation came from a cluster-specific or fallback policy table.",
            "derivation": "Direct carry-through from recommendations.csv.",
        },
        {
            "sheet_name": "Reject_Report",
            "column_name": "reject_reason_codes",
            "source_field": "reject_reasons",
            "description": "Raw rejection reason codes from validation.",
            "derivation": "Direct carry-through from rejected_rows.csv.",
        },
        {
            "sheet_name": "Reject_Report",
            "column_name": "reject_reason_detail",
            "source_field": "reject_reason_codes",
            "description": "Human-readable explanation of the rejection codes.",
            "derivation": "Mapped from deterministic code-to-detail rules.",
        },
    ]
    return pd.DataFrame(rows)
