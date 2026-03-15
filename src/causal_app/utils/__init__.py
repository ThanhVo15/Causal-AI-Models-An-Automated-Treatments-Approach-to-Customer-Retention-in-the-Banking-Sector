"""Utility helpers for the local demo scaffold."""

from causal_app.utils.artifacts import write_run_artifact_manifest
from causal_app.utils.demo_repository import (
    RunRecord,
    UploadRecord,
    get_run_record,
    get_upload_record,
    list_run_records,
    list_upload_records,
    load_dataframe_if_exists,
    load_json_if_exists,
    register_existing_input,
    save_uploaded_bytes,
)
from causal_app.utils.logging import attach_file_handler, detach_handler, get_logger
from causal_app.utils.paths import ensure_runtime_directories
from causal_app.utils.status import scaffold_status

__all__ = [
    "RunRecord",
    "UploadRecord",
    "ensure_runtime_directories",
    "get_run_record",
    "get_upload_record",
    "get_logger",
    "list_run_records",
    "list_upload_records",
    "load_dataframe_if_exists",
    "load_json_if_exists",
    "register_existing_input",
    "save_uploaded_bytes",
    "scaffold_status",
    "attach_file_handler",
    "detach_handler",
    "write_run_artifact_manifest",
]
