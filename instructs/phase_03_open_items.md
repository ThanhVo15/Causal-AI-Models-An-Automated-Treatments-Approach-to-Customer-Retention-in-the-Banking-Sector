# Phase 03 Open Items

## Unresolved Ambiguities

- No original saved churn model artifact was found in the repo.
- No original saved clustering artifact was found in the repo.
- The recommendation stage still depends on a simulated legacy causal table rather than verified real intervention outcomes.
- The intended long-term canonical churn pipeline is still ambiguous between:
  - `Save_Model.ipynb`
  - duplicated logic in `5_CAI_P_Post_Generated.ipynb`
  - a future clean reimplementation
- The long-term role of the GPU/embedding clustering branches from notebook 3 is still unresolved.

## Important Assumptions Carried Forward

- `Data/train.csv` and `Data/test.csv` inside the archived bundle remain the clearest canonical raw legacy inputs.
- `df_cluster.csv` is being used as the best available legacy segmentation label source, not as proof that the original clustering artifact survived.
- `df_causal_ai` is being used as the best available legacy recommendation-policy source, but it must still be treated as simulation-backed.
- The Phase 3 engine is now the future runtime source of truth for extracted behavior, while the notebooks remain the research source of context.

## Risks Of Misinterpretation

- Do not describe Phase 3 recommendation outputs as production-grade causal effect estimates.
- Do not describe Phase 3 segmentation as the original notebook-3 embedding model.
- Do not describe the churn shim as a recovered original artifact.
- Do not assume notebook metrics and Phase 3 engine outputs are identical until they are explicitly compared.
- Do not remove the legacy bundle yet; it is still required for artifact rebuilding and traceability.

## Intentional Temporary Deviations From Raw Notebook Behavior

- Age-group binning now preserves a fitted upper-edge fallback to avoid inference-time failures on narrow batches.
- Empty accepted-batch handling was added so the pipeline can complete with `skipped` model stages instead of crashing.

## Deferred To Phase 4

- wire the extracted engine into Streamlit pages
- persist dataset/run/export metadata into Postgres
- add user-facing profiling summaries and process tracking views
- decide whether to surface policy options and diagnostics directly in the UI
- add tests around validation, preprocessing, and pipeline orchestration
- decide whether to add stable artifact versioning beyond the current Phase 3 temporary files

## Practical Reminder For Future Prompts

- Re-read all files in `instructs/` before continuing.
- Treat `legacy_snapshot/` as a required dependency until the engine no longer needs to rebuild from legacy CSV exports.
