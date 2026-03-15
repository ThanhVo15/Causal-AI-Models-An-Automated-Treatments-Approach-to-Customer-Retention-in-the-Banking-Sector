from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


LEGACY_BUNDLE_NAME = "Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector"


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_env: str
    log_level: str
    streamlit_port: int
    storage_root: Path
    artifacts_root: Path
    database_url: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    legacy_bundle_root: Path
    legacy_data_root: Path
    legacy_train_path: Path
    legacy_test_path: Path
    legacy_cluster_path: Path
    legacy_causal_path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@lru_cache
def get_settings() -> AppSettings:
    root = repo_root()
    default_storage = root / "storage"
    legacy_bundle_root = root / "legacy_snapshot" / LEGACY_BUNDLE_NAME
    legacy_data_root = legacy_bundle_root / "Data"
    return AppSettings(
        app_name=os.getenv("APP_NAME", "Causal AI Local Demo"),
        app_env=os.getenv("APP_ENV", "local"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
        storage_root=Path(os.getenv("STORAGE_ROOT", str(default_storage))),
        artifacts_root=root / "artifacts",
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://causal_ai:causal_ai@postgres:5432/causal_ai",
        ),
        postgres_host=os.getenv("POSTGRES_HOST", "postgres"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        postgres_db=os.getenv("POSTGRES_DB", "causal_ai"),
        postgres_user=os.getenv("POSTGRES_USER", "causal_ai"),
        legacy_bundle_root=legacy_bundle_root,
        legacy_data_root=legacy_data_root,
        legacy_train_path=legacy_data_root / "train.csv",
        legacy_test_path=legacy_data_root / "test.csv",
        legacy_cluster_path=legacy_data_root / "data from remote sever" / "df_cluster.csv",
        legacy_causal_path=legacy_data_root / "data from remote sever" / "df_causal_ai",
    )
