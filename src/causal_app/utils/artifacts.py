from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANIFEST_VERSION = "v1"


def _file_entry(role: str, path: Path) -> dict[str, Any]:
    resolved = Path(path)
    exists = resolved.exists()
    return {
        "role": role,
        "path": str(resolved),
        "exists": exists,
        "size_bytes": int(resolved.stat().st_size) if exists and resolved.is_file() else None,
    }


def write_run_artifact_manifest(
    *,
    manifest_path: Path,
    run_id: str,
    input_path: Path,
    run_dir: Path,
    export_path: Path,
    log_path: Path,
    artifacts: dict[str, Path],
    stage_results: list[dict[str, Any]],
    model_artifact_paths: list[Path],
) -> Path:
    payload = {
        "manifest_version": MANIFEST_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "input_path": str(input_path),
        "run_dir": str(run_dir),
        "export_path": str(export_path),
        "log_path": str(log_path),
        "artifacts": [_file_entry(role, path) for role, path in artifacts.items()],
        "model_artifacts": [_file_entry("model_artifact", path) for path in model_artifact_paths],
        "stage_results": stage_results,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2))
    return manifest_path
