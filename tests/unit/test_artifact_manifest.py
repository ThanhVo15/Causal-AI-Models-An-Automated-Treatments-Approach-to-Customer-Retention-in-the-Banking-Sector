from __future__ import annotations

import json

from causal_app.utils.artifacts import write_run_artifact_manifest


def test_write_run_artifact_manifest_records_roles_and_sizes(tmp_path):
    run_dir = tmp_path / "run-001"
    run_dir.mkdir()
    export_path = tmp_path / "exports" / "run-001.xlsx"
    export_path.parent.mkdir()
    export_path.write_text("workbook")
    log_path = run_dir / "run.log"
    log_path.write_text("log")
    recommendations_path = run_dir / "recommendations.csv"
    recommendations_path.write_text("a,b\n1,2\n")

    manifest_path = write_run_artifact_manifest(
        manifest_path=run_dir / "artifact_manifest.json",
        run_id="run-001",
        input_path=tmp_path / "input.csv",
        run_dir=run_dir,
        export_path=export_path,
        log_path=log_path,
        artifacts={"recommendations": recommendations_path, "excel_export": export_path},
        stage_results=[{"stage_name": "excel_export", "status": "completed"}],
        model_artifact_paths=[],
    )

    payload = json.loads(manifest_path.read_text())
    roles = {entry["role"] for entry in payload["artifacts"]}

    assert payload["manifest_version"] == "v1"
    assert payload["run_id"] == "run-001"
    assert roles == {"recommendations", "excel_export"}
    assert payload["log_path"] == str(log_path)
