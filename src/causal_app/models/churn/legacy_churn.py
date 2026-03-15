from __future__ import annotations

import json
import pickle
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.exceptions import NotFittedError

from causal_app.config import AppSettings, get_settings
from causal_app.preprocessing.legacy_bank import (
    CHURN_FEATURE_COLUMNS,
    TRACEABILITY_NOTE,
    build_legacy_churn_pipeline,
)


class LegacyChurnModel:
    """Temporary runnable churn engine derived from the legacy notebook pipeline."""

    ARTIFACT_DIRNAME = "phase_03"
    ARTIFACT_FILENAME = "legacy_churn_pipeline.pkl"
    METADATA_FILENAME = "legacy_churn_pipeline.json"
    _MEMORY_CACHE: dict[tuple[str, str], "LegacyChurnModel"] = {}

    def __init__(self, pipeline) -> None:
        self.pipeline = pipeline

    @staticmethod
    def _is_usable_pipeline(pipeline, sample_frame: pd.DataFrame) -> bool:
        try:
            if sample_frame.empty:
                return False
            candidate = sample_frame[list(CHURN_FEATURE_COLUMNS)].head(1).copy()
            pipeline.predict_proba(candidate)
        except (AttributeError, KeyError, NotFittedError, ValueError, TypeError):
            return False
        return True

    @classmethod
    def load_or_build(
        cls,
        settings: AppSettings | None = None,
        force_retrain: bool = False,
    ) -> "LegacyChurnModel":
        settings = settings or get_settings()
        artifact_dir = settings.artifacts_root / "models" / cls.ARTIFACT_DIRNAME
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / cls.ARTIFACT_FILENAME
        metadata_path = artifact_dir / cls.METADATA_FILENAME

        train_df = pd.read_csv(settings.legacy_train_path)
        X = train_df[list(CHURN_FEATURE_COLUMNS)].copy()
        y = pd.to_numeric(train_df["Exited"], errors="raise").astype(int)
        cache_key = (str(artifact_path), str(settings.legacy_train_path))

        if not force_retrain and cache_key in cls._MEMORY_CACHE:
            return cls._MEMORY_CACHE[cache_key]

        if artifact_path.exists() and not force_retrain:
            with artifact_path.open("rb") as handle:
                loaded_pipeline = pickle.load(handle)
            if cls._is_usable_pipeline(loaded_pipeline, X):
                model = cls(loaded_pipeline)
                cls._MEMORY_CACHE[cache_key] = model
                return model

        pipeline = build_legacy_churn_pipeline()
        pipeline.fit(X, y)

        with artifact_path.open("wb") as handle:
            pickle.dump(pipeline, handle)

        metadata = {
            "artifact_type": "temporary_shim",
            "artifact_version": "phase_03_local_demo",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "note": "No original saved churn artifact was found in the repo. This artifact is trained from legacy train.csv using notebook-derived preprocessing and GradientBoostingClassifier.",
            "traceability": TRACEABILITY_NOTE,
            "training_rows": int(len(train_df)),
            "feature_columns": list(CHURN_FEATURE_COLUMNS),
            "source_data_path": str(Path(settings.legacy_train_path)),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2))
        model = cls(pipeline)
        cls._MEMORY_CACHE[cache_key] = model
        return model

    def predict_proba(self, raw_dataframe: pd.DataFrame) -> pd.Series:
        if raw_dataframe.empty:
            return pd.Series(dtype=float, index=raw_dataframe.index, name="churn_probability")
        model_frame = raw_dataframe[list(CHURN_FEATURE_COLUMNS)].copy()
        probabilities = self.pipeline.predict_proba(model_frame)[:, 1]
        return pd.Series(probabilities, index=raw_dataframe.index, name="churn_probability")
