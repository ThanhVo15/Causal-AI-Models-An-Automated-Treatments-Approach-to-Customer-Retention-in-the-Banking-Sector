from __future__ import annotations

import json
import pickle
from datetime import datetime, timezone

import pandas as pd
from sklearn.neighbors import NearestCentroid
from sklearn.exceptions import NotFittedError

from causal_app.config import AppSettings, get_settings
from causal_app.preprocessing.legacy_bank import (
    CLUSTER_FEATURE_COLUMNS,
    LegacyClusterFeatureProjector,
    TRACEABILITY_NOTE,
)


class LegacySegmenter:
    """Temporary cluster assignment wrapper built from exported legacy cluster labels."""

    ARTIFACT_DIRNAME = "phase_03"
    ARTIFACT_FILENAME = "legacy_cluster_segmenter.pkl"
    METADATA_FILENAME = "legacy_cluster_segmenter.json"
    _MEMORY_CACHE: dict[tuple[str, str], "LegacySegmenter"] = {}

    def __init__(self, projector: LegacyClusterFeatureProjector, model: NearestCentroid) -> None:
        self.projector = projector
        self.model = model

    @staticmethod
    def _is_usable_wrapper(
        projector: LegacyClusterFeatureProjector,
        model: NearestCentroid,
        sample_frame: pd.DataFrame,
    ) -> bool:
        try:
            if sample_frame.empty:
                return False
            projected = projector.transform(sample_frame.head(1))
            model.predict(projected)
        except (AttributeError, KeyError, NotFittedError, ValueError, TypeError, RuntimeError):
            return False
        return True

    @classmethod
    def load_or_build(
        cls,
        settings: AppSettings | None = None,
        force_retrain: bool = False,
    ) -> "LegacySegmenter":
        settings = settings or get_settings()
        artifact_dir = settings.artifacts_root / "models" / cls.ARTIFACT_DIRNAME
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / cls.ARTIFACT_FILENAME
        metadata_path = artifact_dir / cls.METADATA_FILENAME

        cluster_df = pd.read_csv(settings.legacy_cluster_path)
        cache_key = (str(artifact_path), str(settings.legacy_cluster_path))

        if not force_retrain and cache_key in cls._MEMORY_CACHE:
            return cls._MEMORY_CACHE[cache_key]

        if artifact_path.exists() and not force_retrain:
            with artifact_path.open("rb") as handle:
                projector, model = pickle.load(handle)
            if cls._is_usable_wrapper(projector=projector, model=model, sample_frame=cluster_df):
                wrapper = cls(projector=projector, model=model)
                cls._MEMORY_CACHE[cache_key] = wrapper
                return wrapper

        projector = LegacyClusterFeatureProjector().fit(cluster_df)
        X = projector.transform(cluster_df)
        y = pd.to_numeric(cluster_df["Cluster"], errors="raise").astype(int)

        model = NearestCentroid()
        model.fit(X, y)

        with artifact_path.open("wb") as handle:
            pickle.dump((projector, model), handle)

        metadata = {
            "artifact_type": "temporary_wrapper",
            "artifact_version": "phase_03_local_demo",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "note": "No original segmentation artifact was found. This wrapper learns nearest centroids from legacy df_cluster.csv labels and is not the original embedding-based clustering artifact.",
            "traceability": TRACEABILITY_NOTE,
            "training_rows": int(len(cluster_df)),
            "feature_columns": list(CLUSTER_FEATURE_COLUMNS),
            "source_data_path": str(settings.legacy_cluster_path),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2))
        wrapper = cls(projector=projector, model=model)
        cls._MEMORY_CACHE[cache_key] = wrapper
        return wrapper

    def predict(self, raw_dataframe: pd.DataFrame) -> pd.Series:
        if raw_dataframe.empty:
            return pd.Series(dtype=int, index=raw_dataframe.index, name="assigned_cluster")
        projected = self.projector.transform(raw_dataframe)
        clusters = self.model.predict(projected)
        return pd.Series(clusters, index=raw_dataframe.index, name="assigned_cluster").astype(int)
