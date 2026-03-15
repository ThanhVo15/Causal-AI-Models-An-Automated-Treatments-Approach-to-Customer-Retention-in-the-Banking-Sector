from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from causal_app.config import AppSettings, get_settings
from causal_app.preprocessing.legacy_bank import TRACEABILITY_NOTE
from causal_app.schemas.contracts import TREATMENT_OPTIONS


class LegacyPolicyRecommender:
    """Temporary recommendation policy built from the simulated legacy `df_causal_ai` table."""

    ARTIFACT_DIRNAME = "phase_03"
    ARTIFACT_FILENAME = "legacy_policy_summary.csv"
    METADATA_FILENAME = "legacy_policy_summary.json"
    _MEMORY_CACHE: dict[tuple[str, str], "LegacyPolicyRecommender"] = {}

    def __init__(self, policy_table: pd.DataFrame) -> None:
        self.policy_table = policy_table.sort_values(["cluser_label", "Treatment"]).reset_index(drop=True)
        self.cluster_policy_tables = {
            int(cluster_id): frame.reset_index(drop=True)
            for cluster_id, frame in self.policy_table.groupby("cluser_label", dropna=False)
        }
        self.overall_policy = (
            self.policy_table.groupby("Treatment")
            .agg(
                sample_size=("sample_size", "sum"),
                mean_p_pre=("mean_p_pre", "mean"),
                mean_p_post=("mean_p_post", "mean"),
                mean_delta=("mean_delta", "mean"),
            )
            .reset_index()
        )
        self.best_policy_by_cluster = {
            cluster_id: self._select_best_policy(frame)
            for cluster_id, frame in self.cluster_policy_tables.items()
        }
        self.best_overall_policy = self._select_best_policy(self.overall_policy)

    @staticmethod
    def _select_best_policy(policy_frame: pd.DataFrame) -> pd.Series:
        ordered = policy_frame.copy()
        ordered["treatment_rank"] = ordered["Treatment"].apply(
            lambda name: TREATMENT_OPTIONS.index(name) if name in TREATMENT_OPTIONS else len(TREATMENT_OPTIONS)
        )
        return ordered.sort_values(
            ["mean_delta", "sample_size", "treatment_rank"],
            ascending=[True, False, True],
        ).iloc[0]

    @classmethod
    def load_or_build(
        cls,
        settings: AppSettings | None = None,
        force_rebuild: bool = False,
    ) -> "LegacyPolicyRecommender":
        settings = settings or get_settings()
        artifact_dir = settings.artifacts_root / "models" / cls.ARTIFACT_DIRNAME
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / cls.ARTIFACT_FILENAME
        metadata_path = artifact_dir / cls.METADATA_FILENAME
        cache_key = (str(artifact_path), str(settings.legacy_causal_path))

        if not force_rebuild and cache_key in cls._MEMORY_CACHE:
            return cls._MEMORY_CACHE[cache_key]

        if artifact_path.exists() and not force_rebuild:
            wrapper = cls(pd.read_csv(artifact_path))
            cls._MEMORY_CACHE[cache_key] = wrapper
            return wrapper

        causal_df = pd.read_csv(settings.legacy_causal_path)
        causal_df["mean_delta"] = causal_df["p_churn_post"] - causal_df["p_pre"]
        policy_table = (
            causal_df.groupby(["cluser_label", "Treatment"], dropna=False)
            .agg(
                sample_size=("Treatment", "size"),
                mean_p_pre=("p_pre", "mean"),
                mean_p_post=("p_churn_post", "mean"),
                mean_delta=("mean_delta", "mean"),
            )
            .reset_index()
            .sort_values(["cluser_label", "Treatment"])
            .reset_index(drop=True)
        )
        policy_table.to_csv(artifact_path, index=False)

        metadata = {
            "artifact_type": "temporary_wrapper",
            "artifact_version": "phase_03_local_demo",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "note": "This is a cluster-level policy summary derived from the simulated legacy causal table. It is not an exported econml artifact and should not be presented as production-ready causal recommendation logic.",
            "traceability": TRACEABILITY_NOTE + " Recommendation policy also depends on 6_CAI_Model.ipynb cells 23/26/28/29/32/39/40/41/42/44/45.",
            "source_rows": int(len(causal_df)),
            "source_data_path": str(settings.legacy_causal_path),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2))
        wrapper = cls(policy_table=policy_table)
        cls._MEMORY_CACHE[cache_key] = wrapper
        return wrapper

    def recommend(
        self,
        cluster_ids: pd.Series,
        churn_probabilities: pd.Series,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        if cluster_ids.empty:
            empty_recommendations = pd.DataFrame(
                columns=[
                    "source_row_index",
                    "assigned_cluster",
                    "churn_probability",
                    "recommended_treatment",
                    "estimated_post_churn",
                    "expected_absolute_change",
                    "policy_scope",
                    "policy_sample_size",
                ]
            )
            empty_policy_options = pd.DataFrame(
                columns=[
                    "cluser_label",
                    "Treatment",
                    "sample_size",
                    "mean_p_pre",
                    "mean_p_post",
                    "mean_delta",
                    "estimated_post_churn",
                    "expected_absolute_change",
                    "source_row_index",
                    "input_cluster",
                    "input_churn_probability",
                    "policy_scope",
                ]
            )
            return empty_recommendations, empty_policy_options

        recommendation_rows: list[dict[str, object]] = []
        option_rows: list[dict[str, object]] = []

        for row_index, (cluster_id, churn_probability) in enumerate(zip(cluster_ids, churn_probabilities)):
            cluster_id = int(cluster_id)
            churn_probability = float(churn_probability)
            cluster_policy = self.cluster_policy_tables.get(cluster_id)
            if cluster_policy is None or cluster_policy.empty:
                cluster_policy = self.overall_policy.copy()
                cluster_policy["cluser_label"] = cluster_id
                best_row = self.best_overall_policy
                policy_scope = "overall_fallback"
            else:
                cluster_policy = cluster_policy.copy()
                best_row = self.best_policy_by_cluster[cluster_id]
                policy_scope = "cluster_specific"

            cluster_policy["estimated_post_churn"] = np.clip(
                churn_probability + cluster_policy["mean_delta"], 0.0, 1.0
            )
            cluster_policy["expected_absolute_change"] = (
                cluster_policy["estimated_post_churn"] - churn_probability
            )
            cluster_policy["source_row_index"] = int(row_index)
            cluster_policy["input_cluster"] = int(cluster_id)
            cluster_policy["input_churn_probability"] = float(churn_probability)
            cluster_policy["policy_scope"] = policy_scope
            option_rows.extend(cluster_policy.to_dict(orient="records"))

            estimated_post_churn = float(np.clip(churn_probability + float(best_row["mean_delta"]), 0.0, 1.0))
            recommendation_rows.append(
                {
                    "source_row_index": int(row_index),
                    "assigned_cluster": int(cluster_id),
                    "churn_probability": float(churn_probability),
                    "recommended_treatment": best_row["Treatment"],
                    "estimated_post_churn": estimated_post_churn,
                    "expected_absolute_change": float(estimated_post_churn - churn_probability),
                    "policy_scope": policy_scope,
                    "policy_sample_size": int(best_row["sample_size"]),
                }
            )

        recommendations = pd.DataFrame(recommendation_rows)
        policy_options = pd.DataFrame(option_rows)
        return recommendations, policy_options
