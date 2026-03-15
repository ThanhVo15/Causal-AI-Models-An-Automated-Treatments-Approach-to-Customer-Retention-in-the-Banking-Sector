from __future__ import annotations

from pathlib import Path

from causal_app.config import get_settings


RUNTIME_SUBDIRECTORIES = ("uploads", "runs", "profiles", "exports", "logs")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def ensure_runtime_directories() -> dict[str, Path]:
    settings = get_settings()
    base = settings.storage_root
    base.mkdir(parents=True, exist_ok=True)

    paths: dict[str, Path] = {"storage_root": base}
    for name in RUNTIME_SUBDIRECTORIES:
        path = base / name
        path.mkdir(parents=True, exist_ok=True)
        paths[name] = path
    return paths
