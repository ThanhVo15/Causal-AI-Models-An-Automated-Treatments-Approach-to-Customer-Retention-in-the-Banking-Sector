# Phase 06 Artifact Versioning

## Current Versioning Discipline

The repo still uses simple file-based versioning rather than a model registry.

That is intentional for the current local-demo scope.

## Naming Rules

### Run Id

- format: `YYYYMMDDTHHMMSSZ-<optional-label>-<short-suffix>`

### Runtime Outputs

- run directory:
  - `storage/runs/<run-id>/`
- workbook export:
  - `storage/exports/<run-id>.xlsx`
- upload file:
  - `storage/uploads/<upload-id>__<safe-original-name>`

## Manifest / Metadata Rules

### `run_summary.json`

Source of truth for:

- run id
- input path
- main artifact paths
- row counts
- stage timing

### `artifact_manifest.json`

Source of truth for:

- manifest version
- output artifact paths
- file sizes
- model artifact references
- stage snapshot

### Model Wrapper Metadata

Phase 6 extended model-wrapper metadata to include:

- `artifact_version`
- `created_at_utc`
- `source_data_path`

## Folder Convention

- `legacy_snapshot/`
  - archived historical source material
- `artifacts/models/phase_03/`
  - generated local wrapper artifacts
- `storage/runs/`
  - run-level generated outputs
- `storage/exports/`
  - shareable workbook outputs
- `storage/logs/`
  - cross-run logs

## Why No Full Registry Yet

- only one local app currently consumes the engine
- there is no external API contract yet
- file-based traceability is enough for the current demo scope
