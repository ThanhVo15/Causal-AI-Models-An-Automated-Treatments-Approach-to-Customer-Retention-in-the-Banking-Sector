from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_INPUT_COLUMNS = (
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
)

OPTIONAL_INPUT_COLUMNS = (
    "id",
    "CustomerId",
    "Surname",
    "Exited",
)

ALLOWED_GENDERS = ("Female", "Male")
ALLOWED_GEOGRAPHIES = ("France", "Germany", "Spain")
TREATMENT_OPTIONS = (
    "No Program",
    "Wealth Accumulator Program",
    "Engage & Elevate",
    "Starter Growth Plan",
    "Reconnect & Reward",
    "Premium Balance Rewards",
)
EXPORT_SHEETS = (
    "Summary",
    "Customer_Action_List",
    "Reject_Report",
    "Run_Metadata",
    "Field_Definitions",
)


@dataclass
class StageResult:
    stage_name: str
    status: str
    input_rows: int
    output_rows: int
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["details"] = {
            key: str(value) if isinstance(value, Path) else value
            for key, value in self.details.items()
        }
        return data


@dataclass
class ValidationResult:
    accepted_rows: int
    rejected_rows: int
    duplicate_key_column: str | None
    reject_reason_counts: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineRunResult:
    run_id: str
    input_path: Path
    run_dir: Path
    export_path: Path
    log_path: Path
    artifact_manifest_path: Path
    input_rows: int
    accepted_rows: int
    rejected_rows: int
    stage_results: list[StageResult]
    diagnostics_path: Path
    recommendations_path: Path
    rejected_rows_path: Path
    prepared_features_path: Path
    policy_options_path: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "input_path": str(self.input_path),
            "run_dir": str(self.run_dir),
            "export_path": str(self.export_path),
            "log_path": str(self.log_path),
            "artifact_manifest_path": str(self.artifact_manifest_path),
            "input_rows": self.input_rows,
            "accepted_rows": self.accepted_rows,
            "rejected_rows": self.rejected_rows,
            "diagnostics_path": str(self.diagnostics_path),
            "recommendations_path": str(self.recommendations_path),
            "rejected_rows_path": str(self.rejected_rows_path),
            "prepared_features_path": str(self.prepared_features_path),
            "policy_options_path": str(self.policy_options_path),
            "stage_results": [stage.to_dict() for stage in self.stage_results],
        }
