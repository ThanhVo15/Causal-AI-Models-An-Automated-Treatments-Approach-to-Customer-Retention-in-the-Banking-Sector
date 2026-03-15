from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
from typing import Any
from uuid import uuid4

import pandas as pd

from causal_app.config import AppSettings, get_settings
from causal_app.utils.paths import ensure_runtime_directories


UPLOAD_METADATA_SUFFIX = ".upload.json"


@dataclass(frozen=True)
class UploadRecord:
    upload_id: str
    original_name: str
    stored_name: str
    storage_path: Path
    metadata_path: Path
    uploaded_at: str
    size_bytes: int
    source: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UploadRecord":
        return cls(
            upload_id=str(payload["upload_id"]),
            original_name=str(payload["original_name"]),
            stored_name=str(payload["stored_name"]),
            storage_path=Path(payload["storage_path"]),
            metadata_path=Path(payload["metadata_path"]),
            uploaded_at=str(payload["uploaded_at"]),
            size_bytes=int(payload["size_bytes"]),
            source=str(payload["source"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "upload_id": self.upload_id,
            "original_name": self.original_name,
            "stored_name": self.stored_name,
            "storage_path": str(self.storage_path),
            "metadata_path": str(self.metadata_path),
            "uploaded_at": self.uploaded_at,
            "size_bytes": self.size_bytes,
            "source": self.source,
        }


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    run_dir: Path
    input_path: Path
    export_path: Path
    log_path: Path
    artifact_manifest_path: Path
    diagnostics_path: Path
    recommendations_path: Path
    rejected_rows_path: Path
    prepared_features_path: Path
    policy_options_path: Path
    input_rows: int
    accepted_rows: int
    rejected_rows: int
    created_at: str | None
    stage_results: list[dict[str, Any]]

    @classmethod
    def from_summary(cls, payload: dict[str, Any]) -> "RunRecord":
        stage_results = payload.get("stage_results", [])
        created_at = None
        if stage_results:
            created_at = stage_results[0].get("started_at") or stage_results[0].get("finished_at")
        return cls(
            run_id=str(payload["run_id"]),
            run_dir=Path(payload["run_dir"]),
            input_path=Path(payload["input_path"]),
            export_path=Path(payload["export_path"]),
            log_path=Path(payload.get("log_path", Path(payload["run_dir"]) / "run.log")),
            artifact_manifest_path=Path(
                payload.get("artifact_manifest_path", Path(payload["run_dir"]) / "artifact_manifest.json")
            ),
            diagnostics_path=Path(payload["diagnostics_path"]),
            recommendations_path=Path(payload["recommendations_path"]),
            rejected_rows_path=Path(payload["rejected_rows_path"]),
            prepared_features_path=Path(payload["prepared_features_path"]),
            policy_options_path=Path(payload["policy_options_path"]),
            input_rows=int(payload["input_rows"]),
            accepted_rows=int(payload["accepted_rows"]),
            rejected_rows=int(payload["rejected_rows"]),
            created_at=created_at,
            stage_results=stage_results,
        )


def _json_load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "dataset"


def _timestamp_id() -> str:
    return f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"


def save_uploaded_bytes(
    file_name: str,
    content: bytes,
    *,
    settings: AppSettings | None = None,
    source: str = "user_upload",
) -> UploadRecord:
    settings = settings or get_settings()
    runtime_dirs = ensure_runtime_directories()
    uploads_dir = runtime_dirs["uploads"]

    upload_id = _timestamp_id()
    safe_name = _safe_name(file_name)
    stored_name = f"{upload_id}__{safe_name}"
    storage_path = uploads_dir / stored_name
    metadata_path = uploads_dir / f"{upload_id}{UPLOAD_METADATA_SUFFIX}"

    storage_path.write_bytes(content)
    record = UploadRecord(
        upload_id=upload_id,
        original_name=file_name,
        stored_name=stored_name,
        storage_path=storage_path,
        metadata_path=metadata_path,
        uploaded_at=datetime.now(timezone.utc).isoformat(),
        size_bytes=len(content),
        source=source,
    )
    metadata_path.write_text(json.dumps(record.to_dict(), indent=2))
    return record


def register_existing_input(
    source_path: str | Path,
    *,
    label: str | None = None,
    settings: AppSettings | None = None,
    source: str = "existing_file",
) -> UploadRecord:
    path = Path(source_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Cannot register missing input file: {path}")

    settings = settings or get_settings()
    runtime_dirs = ensure_runtime_directories()
    uploads_dir = runtime_dirs["uploads"]

    upload_id = _timestamp_id()
    original_name = label or path.name
    safe_name = _safe_name(path.name)
    stored_name = f"{upload_id}__{safe_name}"
    storage_path = uploads_dir / stored_name
    metadata_path = uploads_dir / f"{upload_id}{UPLOAD_METADATA_SUFFIX}"

    shutil.copy2(path, storage_path)
    record = UploadRecord(
        upload_id=upload_id,
        original_name=original_name,
        stored_name=stored_name,
        storage_path=storage_path,
        metadata_path=metadata_path,
        uploaded_at=datetime.now(timezone.utc).isoformat(),
        size_bytes=storage_path.stat().st_size,
        source=source,
    )
    metadata_path.write_text(json.dumps(record.to_dict(), indent=2))
    return record


def list_upload_records(settings: AppSettings | None = None) -> list[UploadRecord]:
    settings = settings or get_settings()
    uploads_dir = ensure_runtime_directories()["uploads"]
    records: list[UploadRecord] = []

    for metadata_path in sorted(uploads_dir.glob(f"*{UPLOAD_METADATA_SUFFIX}"), reverse=True):
        try:
            record = UploadRecord.from_dict(_json_load(metadata_path))
        except Exception:
            continue
        if record.storage_path.exists():
            records.append(record)
    return sorted(records, key=lambda record: record.uploaded_at, reverse=True)


def get_upload_record(upload_id: str, settings: AppSettings | None = None) -> UploadRecord | None:
    settings = settings or get_settings()
    uploads_dir = ensure_runtime_directories()["uploads"]
    metadata_path = uploads_dir / f"{upload_id}{UPLOAD_METADATA_SUFFIX}"
    if not metadata_path.exists():
        return None
    try:
        record = UploadRecord.from_dict(_json_load(metadata_path))
    except Exception:
        return None
    return record if record.storage_path.exists() else None


def list_run_records(settings: AppSettings | None = None) -> list[RunRecord]:
    settings = settings or get_settings()
    runs_dir = ensure_runtime_directories()["runs"]
    records: list[RunRecord] = []

    for summary_path in sorted(runs_dir.glob("*/run_summary.json"), reverse=True):
        try:
            record = RunRecord.from_summary(_json_load(summary_path))
        except Exception:
            continue
        records.append(record)
    return sorted(records, key=lambda record: record.created_at or "", reverse=True)


def get_run_record(run_id: str, settings: AppSettings | None = None) -> RunRecord | None:
    for record in list_run_records(settings=settings):
        if record.run_id == run_id:
            return record
    return None


def load_json_if_exists(path: str | Path) -> dict[str, Any] | None:
    resolved = Path(path)
    if not resolved.exists():
        return None
    return _json_load(resolved)


def load_dataframe_if_exists(path: str | Path) -> pd.DataFrame | None:
    resolved = Path(path)
    if not resolved.exists():
        return None
    suffix = resolved.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(resolved)
    if suffix == ".xlsx":
        return pd.read_excel(resolved)
    return None
