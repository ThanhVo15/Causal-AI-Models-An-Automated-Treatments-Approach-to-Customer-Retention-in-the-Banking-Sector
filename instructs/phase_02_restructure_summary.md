# Phase 02 Restructure Summary

## Purpose

Phase 2 created a clean repo foundation for a future local causal AI demo platform while preserving the original notebook-heavy project as a legacy snapshot.

## What Changed

- Created a root-level repo structure for:
  - app code
  - package code
  - docs
  - migration records
  - storage
  - database bootstrap
  - tests
  - artifacts
- Moved the original nested research bundle from:
  - `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`
  - to `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`
- Preserved the nested legacy `.git` inside the archived bundle.
- Added baseline migration docs under `docs/migration/`.
- Added a root `README.md` aligned with the new structure and honest Phase 2 scope.
- Added `pyproject.toml`, `.env.example`, `.gitignore`, `.dockerignore`, `Dockerfile`, and `docker-compose.yml`.
- Added a minimal `src/causal_app/` package skeleton.
- Added a minimal Streamlit scaffold under `apps/streamlit/`.
- Added a minimal Postgres bootstrap SQL under `db/init/001_foundation.sql`.
- Added runtime persistence directories under `storage/`.

## What Was Intentionally Not Changed

- No notebook code was rewritten.
- No model logic was extracted from notebooks yet.
- No dataset was promoted into the new `data/` directories yet.
- No real upload, profiling, inference, recommendation, or export workflow was wired.
- No legacy files were deleted.

## Alignment With Phase 1

- Phase 1 said the repo was a research/demo bundle, not a maintainable platform.
- Phase 2 preserved that bundle intact instead of pretending it was already migrated.
- Phase 1 required separation of research and future serving code.
- Phase 2 established that separation structurally:
  - archived legacy bundle in `legacy_snapshot/`
  - new runtime/app foundation at repo root
- Phase 1 identified Docker + Postgres + Streamlit as the preferred local direction.
- Phase 2 scaffolded that direction honestly without fabricating full functionality.

## Observed vs Scaffolded vs Not Yet Implemented

### Observed legacy

- notebook-heavy project bundle
- legacy data exports
- presentation assets
- nested `.git` inside the original bundle

### Scaffolded in Phase 2

- root repo layout
- package skeleton
- Streamlit shell
- Docker Compose stack
- Postgres foundation tables
- storage directory strategy
- migration and phase-memory docs

### Not yet implemented

- reusable preprocessing and model modules
- end-to-end upload/inference flow
- pipeline tracking persistence from the app
- Excel export generation

## Checks Actually Run

- Python syntax compilation of new `src/` and `apps/` files: passed (`compiled_ok=22`)
- `pyproject.toml` parse using `tomllib`: passed
- `docker compose config`: rendered successfully

## Important Repo State Difference vs Phase 1 Baseline

- Phase 1 correctly described the legacy bundle as being at the repo root at that time.
- After Phase 2, that legacy bundle is no longer at the root; it now lives under `legacy_snapshot/`.
- This was an intentional structural change, not a contradiction in the Phase 1 audit.
