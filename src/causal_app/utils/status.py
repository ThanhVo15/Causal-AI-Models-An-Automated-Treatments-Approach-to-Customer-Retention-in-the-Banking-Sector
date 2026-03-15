from __future__ import annotations

from causal_app.config import get_settings


def scaffold_status() -> dict[str, list[str]]:
    settings = get_settings()
    return {
        "ready_to_wire_now": [
            "storage-backed upload registration",
            "CSV/XLSX parsing through the Phase 3 ingestion layer",
            "real validation summaries and rejected-row tracking",
            "real pipeline execution through src/causal_app/pipeline/engine.py",
            "real diagnostics, CSV outputs, and Excel export files",
            "per-run log files and artifact manifests for successful runs",
        ],
        "wire_with_partial_support": [
            "lightweight data profiling summaries",
            "local file-based process tracking from run_summary.json and diagnostics.json",
            "dashboard outputs backed by Phase 3 recommendation and diagnostics files",
            "temporary churn, segmentation, and recommendation wrappers from legacy data exports",
        ],
        "placeholder_only": [
            "Postgres foundation tables exist but the Streamlit app does not write to them yet",
            "no full notebook-parity guarantee for model outputs",
            "no curated demo dataset has been promoted into data/samples/",
            "failed runs are logged to files but are not yet surfaced as first-class records in the app",
        ],
        "deferred": [
            "production-ready artifact registry",
            "full causal estimator serving from notebook 6 logic",
            "DB-backed multi-run history and audit logging",
            f"legacy bundle remains a required dependency at: {settings.legacy_bundle_root}",
        ],
    }
