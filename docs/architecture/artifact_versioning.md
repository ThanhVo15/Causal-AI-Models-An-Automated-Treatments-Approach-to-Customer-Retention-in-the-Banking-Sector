# Artifact Versioning

## Current Philosophy

This repo does not need a full model registry yet. It does need clear, simple, local conventions so outputs remain traceable.

## Source Of Truth Layers

### Legacy Research Assets

- location: `legacy_snapshot/`
- status: archived source material
- do not edit to support the live demo

### Generated Runtime Outputs

- location: `storage/`
- status: per-run and local runtime outputs
- should be treated as generated artifacts, not hand-edited source files

### Generated Model Wrappers

- location: `artifacts/models/phase_03/`
- status: local generated wrapper artifacts used by the extracted engine
- include JSON metadata beside each wrapper file when available

## Naming Conventions

### Run Id

Pattern:

- `YYYYMMDDTHHMMSSZ-<optional-label>-<short-suffix>`

Examples:

- `20260315T151841Z-phase6-smoke-f09e9a22`
- `20260315T145700Z-phase5-sample-1b67559c`

### Run Directory

- `storage/runs/<run-id>/`

### Export Workbook

- `storage/exports/<run-id>.xlsx`

### Upload File

- `storage/uploads/<upload-id>__<safe-original-name>`

### Upload Metadata

- `storage/uploads/<upload-id>.upload.json`

## Metadata Expectations

### `run_summary.json`

Should capture:

- run id
- input path
- key output paths
- row counts
- stage timing/status

### `artifact_manifest.json`

Should capture:

- manifest version
- run id
- output artifact paths
- file sizes
- model artifact references
- stage results snapshot

### Model Wrapper Metadata

Current wrapper metadata files should capture:

- artifact type
- artifact version
- creation timestamp
- source data path
- traceability note

## Why This Is Enough For Now

- local demo usage is the current priority
- file-based traceability is simpler than introducing a registry too early
- the repo is not yet serving models across multiple apps/services
