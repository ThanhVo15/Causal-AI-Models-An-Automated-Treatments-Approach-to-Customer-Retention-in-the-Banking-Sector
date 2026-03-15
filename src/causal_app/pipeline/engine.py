from __future__ import annotations

import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import pandas as pd

from causal_app.config import AppSettings, get_settings
from causal_app.export.excel import export_pipeline_results
from causal_app.ingestion.files import read_input_dataset
from causal_app.ingestion.validation import validate_input_dataframe
from causal_app.models.churn.legacy_churn import LegacyChurnModel
from causal_app.models.diagnostics.summary import build_run_diagnostics
from causal_app.models.recommendation.legacy_policy import LegacyPolicyRecommender
from causal_app.models.segmentation.legacy_segmentation import LegacySegmenter
from causal_app.preprocessing.legacy_bank import CAUSAL_FEATURE_COLUMNS, LegacyCausalFeatureProjector
from causal_app.schemas.contracts import PipelineRunResult, StageResult
from causal_app.utils.artifacts import write_run_artifact_manifest
from causal_app.utils.logging import attach_file_handler, detach_handler, get_logger
from causal_app.utils.paths import ensure_runtime_directories


class PipelineExecutionError(RuntimeError):
    """Raised when a pipeline run fails after a run id and log path are already available."""

    def __init__(
        self,
        *,
        run_id: str,
        run_dir: Path,
        log_path: Path,
        failed_stage: str,
        original_exception: Exception,
    ) -> None:
        self.run_id = run_id
        self.run_dir = run_dir
        self.log_path = log_path
        self.failed_stage = failed_stage
        self.original_exception = original_exception
        super().__init__(
            f"Pipeline run '{run_id}' failed during stage '{failed_stage}'. "
            f"See log at '{log_path}'. Original error: {original_exception}"
        )


def _run_id(label: str | None = None) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid4().hex[:8]
    if label:
        safe_label = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in label).strip("-")
        return f"{timestamp}-{safe_label}-{suffix}" if safe_label else f"{timestamp}-{suffix}"
    return f"{timestamp}-{suffix}"


def _save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _stage_clock_start() -> tuple[str, float]:
    return datetime.now(timezone.utc).isoformat(), perf_counter()


@lru_cache(maxsize=2)
def _load_cached_causal_projector(train_path: str) -> LegacyCausalFeatureProjector:
    train_df = pd.read_csv(train_path)
    return LegacyCausalFeatureProjector().fit(train_df)


def _phase_03_artifact_paths(settings: AppSettings) -> list[Path]:
    artifact_dir = settings.artifacts_root / "models" / "phase_03"
    if not artifact_dir.exists():
        return []
    return sorted(path for path in artifact_dir.glob("*") if path.is_file())


def _build_stage_result(
    stage_name: str,
    status: str,
    input_rows: int,
    output_rows: int,
    details: dict | None = None,
    started_at: str | None = None,
    started_perf: float | None = None,
) -> StageResult:
    finished_at = datetime.now(timezone.utc).isoformat()
    duration_seconds = round(perf_counter() - started_perf, 6) if started_perf is not None else 0.0
    return StageResult(
        stage_name=stage_name,
        status=status,
        input_rows=input_rows,
        output_rows=output_rows,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=duration_seconds,
        details=details or {},
    )


def _log_stage_result(logger, run_id: str, stage_result: StageResult) -> None:
    logger.info(
        "run_id=%s stage=%s status=%s input_rows=%s output_rows=%s duration_seconds=%s",
        run_id,
        stage_result.stage_name,
        stage_result.status,
        stage_result.input_rows,
        stage_result.output_rows,
        stage_result.duration_seconds,
    )


def _empty_prepared_features() -> pd.DataFrame:
    return pd.DataFrame(columns=["source_row_number", *CAUSAL_FEATURE_COLUMNS])


def _empty_recommendations_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "source_row_number",
            "CreditScore",
            "Geography",
            "Gender",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
            "id",
            "CustomerId",
            "Surname",
            "Exited",
            "churn_probability",
            "assigned_cluster",
            "recommended_treatment",
            "estimated_post_churn",
            "expected_absolute_change",
            "policy_scope",
            "policy_sample_size",
        ]
    )


def run_pipeline(
    input_path: str | Path,
    run_label: str | None = None,
    output_dir: str | Path | None = None,
    settings: AppSettings | None = None,
) -> PipelineRunResult:
    settings = settings or get_settings()
    runtime_dirs = ensure_runtime_directories()
    pipeline_run_id = _run_id(run_label)

    run_dir = Path(output_dir).resolve() if output_dir else runtime_dirs["runs"] / pipeline_run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "run.log"
    artifact_manifest_path = run_dir / "artifact_manifest.json"
    logger = get_logger("causal_app.pipeline", settings.log_level)
    shared_log_handler = attach_file_handler(logger, runtime_dirs["logs"] / "pipeline.log", settings.log_level)
    run_log_handler = attach_file_handler(logger, log_path, settings.log_level)

    stage_results: list[StageResult] = []
    resolved_input_path = Path(input_path).expanduser().resolve()
    current_stage = "initialize"

    logger.info(
        "run_id=%s event=run_started input_path=%s run_dir=%s",
        pipeline_run_id,
        resolved_input_path,
        run_dir,
    )

    try:
        current_stage = "read_input"
        stage_started_at, stage_started_perf = _stage_clock_start()
        input_df = read_input_dataset(resolved_input_path)
        stage_results.append(
            _build_stage_result(
                stage_name="read_input",
                status="completed",
                input_rows=len(input_df),
                output_rows=len(input_df),
                details={"input_path": resolved_input_path, "columns": list(input_df.columns)},
                started_at=stage_started_at,
                started_perf=stage_started_perf,
            )
        )
        _log_stage_result(logger, pipeline_run_id, stage_results[-1])

        current_stage = "validate_input"
        stage_started_at, stage_started_perf = _stage_clock_start()
        accepted_df, rejected_df, validation_summary = validate_input_dataframe(input_df)
        stage_results.append(
            _build_stage_result(
                stage_name="validate_input",
                status="completed",
                input_rows=len(input_df),
                output_rows=len(accepted_df),
                details={
                    "rejected_rows": len(rejected_df),
                    "duplicate_key_column": validation_summary.duplicate_key_column,
                    "reject_reason_counts": validation_summary.reject_reason_counts,
                },
                started_at=stage_started_at,
                started_perf=stage_started_perf,
            )
        )
        _log_stage_result(logger, pipeline_run_id, stage_results[-1])

        if accepted_df.empty:
            prepared_features = _empty_prepared_features()
            churn_scores = pd.Series(dtype=float, name="churn_probability")
            assigned_clusters = pd.Series(dtype=int, name="assigned_cluster")
            recommendation_frame = pd.DataFrame(
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
            policy_options = pd.DataFrame(
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
            final_recommendations = _empty_recommendations_frame()
            for skipped_stage in ("preprocess", "churn_prediction", "segmentation", "recommendation"):
                stage_results.append(
                    _build_stage_result(
                        stage_name=skipped_stage,
                        status="skipped",
                        input_rows=0,
                        output_rows=0,
                        details={"reason": "no_valid_rows_after_validation"},
                        started_at=None,
                        started_perf=None,
                    )
                )
                _log_stage_result(logger, pipeline_run_id, stage_results[-1])
        else:
            current_stage = "preprocess"
            stage_started_at, stage_started_perf = _stage_clock_start()
            causal_projector = _load_cached_causal_projector(str(settings.legacy_train_path))
            prepared_features = causal_projector.transform(accepted_df)
            prepared_features.insert(0, "source_row_number", accepted_df["_source_row_number"].values)
            stage_results.append(
                _build_stage_result(
                    stage_name="preprocess",
                    status="completed",
                    input_rows=len(accepted_df),
                    output_rows=len(prepared_features),
                    details={"prepared_feature_columns": list(prepared_features.columns)},
                    started_at=stage_started_at,
                    started_perf=stage_started_perf,
                )
            )
            _log_stage_result(logger, pipeline_run_id, stage_results[-1])

            current_stage = "churn_prediction"
            stage_started_at, stage_started_perf = _stage_clock_start()
            churn_model = LegacyChurnModel.load_or_build(settings=settings)
            churn_scores = churn_model.predict_proba(accepted_df)
            stage_results.append(
                _build_stage_result(
                    stage_name="churn_prediction",
                    status="completed",
                    input_rows=len(accepted_df),
                    output_rows=len(churn_scores),
                    details={"artifact_source": "temporary_shim_trained_from_legacy_train_csv"},
                    started_at=stage_started_at,
                    started_perf=stage_started_perf,
                )
            )
            _log_stage_result(logger, pipeline_run_id, stage_results[-1])

            current_stage = "segmentation"
            stage_started_at, stage_started_perf = _stage_clock_start()
            segmenter = LegacySegmenter.load_or_build(settings=settings)
            assigned_clusters = segmenter.predict(accepted_df)
            stage_results.append(
                _build_stage_result(
                    stage_name="segmentation",
                    status="completed",
                    input_rows=len(accepted_df),
                    output_rows=len(assigned_clusters),
                    details={"artifact_source": "temporary_wrapper_from_df_cluster_labels"},
                    started_at=stage_started_at,
                    started_perf=stage_started_perf,
                )
            )
            _log_stage_result(logger, pipeline_run_id, stage_results[-1])

            current_stage = "recommendation"
            stage_started_at, stage_started_perf = _stage_clock_start()
            recommender = LegacyPolicyRecommender.load_or_build(settings=settings)
            recommendation_frame, policy_options = recommender.recommend(assigned_clusters, churn_scores)
            stage_results.append(
                _build_stage_result(
                    stage_name="recommendation",
                    status="completed",
                    input_rows=len(accepted_df),
                    output_rows=len(recommendation_frame),
                    details={"artifact_source": "cluster_level_policy_from_simulated_df_causal_ai"},
                    started_at=stage_started_at,
                    started_perf=stage_started_perf,
                )
            )
            _log_stage_result(logger, pipeline_run_id, stage_results[-1])

            final_recommendations = accepted_df.reset_index(drop=True).copy()
            final_recommendations.insert(0, "source_row_number", final_recommendations.pop("_source_row_number"))
            final_recommendations["churn_probability"] = churn_scores.reset_index(drop=True)
            final_recommendations["assigned_cluster"] = assigned_clusters.reset_index(drop=True)
            final_recommendations = final_recommendations.merge(
                recommendation_frame.drop(columns=["assigned_cluster", "churn_probability"]),
                left_index=True,
                right_on="source_row_index",
                how="left",
            ).drop(columns=["source_row_index"])

        current_stage = "diagnostics"
        stage_started_at, stage_started_perf = _stage_clock_start()
        diagnostics = build_run_diagnostics(
            input_rows=len(input_df),
            validation=validation_summary,
            recommendations=final_recommendations,
            rejected_rows=rejected_df,
            stage_results=stage_results,
        )
        stage_results.append(
            _build_stage_result(
                stage_name="diagnostics",
                status="completed",
                input_rows=len(final_recommendations),
                output_rows=len(final_recommendations),
                details={"diagnostic_sections": list(diagnostics.keys())},
                started_at=stage_started_at,
                started_perf=stage_started_perf,
            )
        )
        _log_stage_result(logger, pipeline_run_id, stage_results[-1])

        prepared_features_path = run_dir / "prepared_features.csv"
        recommendations_path = run_dir / "recommendations.csv"
        rejected_rows_path = run_dir / "rejected_rows.csv"
        policy_options_path = run_dir / "policy_options.csv"
        diagnostics_path = run_dir / "diagnostics.json"
        run_summary_path = run_dir / "run_summary.json"
        export_path = runtime_dirs["exports"] / f"{pipeline_run_id}.xlsx"

        prepared_features.to_csv(prepared_features_path, index=False)
        final_recommendations.to_csv(recommendations_path, index=False)
        rejected_df.to_csv(rejected_rows_path, index=False)
        policy_options.to_csv(policy_options_path, index=False)

        current_stage = "excel_export"
        stage_started_at, stage_started_perf = _stage_clock_start()
        export_pipeline_results(
            export_path=export_path,
            diagnostics=diagnostics,
            recommendations=final_recommendations,
            rejected_rows=rejected_df,
            policy_options=policy_options,
            run_id=pipeline_run_id,
            input_path=resolved_input_path,
        )
        stage_results.append(
            _build_stage_result(
                stage_name="excel_export",
                status="completed",
                input_rows=len(final_recommendations),
                output_rows=len(final_recommendations),
                details={"export_path": export_path},
                started_at=stage_started_at,
                started_perf=stage_started_perf,
            )
        )
        _log_stage_result(logger, pipeline_run_id, stage_results[-1])
        diagnostics["stage_results"] = [stage.to_dict() for stage in stage_results]
        _save_json(diagnostics_path, diagnostics)

        result = PipelineRunResult(
            run_id=pipeline_run_id,
            input_path=resolved_input_path,
            run_dir=run_dir,
            export_path=export_path,
            log_path=log_path,
            artifact_manifest_path=artifact_manifest_path,
            input_rows=len(input_df),
            accepted_rows=len(final_recommendations),
            rejected_rows=len(rejected_df),
            stage_results=stage_results,
            diagnostics_path=diagnostics_path,
            recommendations_path=recommendations_path,
            rejected_rows_path=rejected_rows_path,
            prepared_features_path=prepared_features_path,
            policy_options_path=policy_options_path,
        )
        _save_json(run_summary_path, result.to_dict())
        write_run_artifact_manifest(
            manifest_path=artifact_manifest_path,
            run_id=pipeline_run_id,
            input_path=resolved_input_path,
            run_dir=run_dir,
            export_path=export_path,
            log_path=log_path,
            artifacts={
                "prepared_features": prepared_features_path,
                "recommendations": recommendations_path,
                "rejected_rows": rejected_rows_path,
                "policy_options": policy_options_path,
                "diagnostics": diagnostics_path,
                "run_summary": run_summary_path,
                "excel_export": export_path,
            },
            stage_results=[stage.to_dict() for stage in stage_results],
            model_artifact_paths=_phase_03_artifact_paths(settings),
        )
        logger.info(
            "run_id=%s event=run_completed accepted_rows=%s rejected_rows=%s export_path=%s manifest_path=%s",
            pipeline_run_id,
            result.accepted_rows,
            result.rejected_rows,
            result.export_path,
            result.artifact_manifest_path,
        )
        return result
    except Exception as exc:
        failure_summary_path = run_dir / "run_failure.json"
        logger.exception(
            "run_id=%s event=run_failed failed_stage=%s error_type=%s error=%s",
            pipeline_run_id,
            current_stage,
            type(exc).__name__,
            exc,
        )
        _save_json(
            failure_summary_path,
            {
                "run_id": pipeline_run_id,
                "failed_stage": current_stage,
                "occurred_at_utc": datetime.now(timezone.utc).isoformat(),
                "input_path": str(resolved_input_path),
                "run_dir": str(run_dir),
                "log_path": str(log_path),
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )
        raise PipelineExecutionError(
            run_id=pipeline_run_id,
            run_dir=run_dir,
            log_path=log_path,
            failed_stage=current_stage,
            original_exception=exc,
        ) from exc
    finally:
        detach_handler(logger, run_log_handler)
        detach_handler(logger, shared_log_handler)
