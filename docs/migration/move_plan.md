# Phase 2 Move Plan

This move plan is defined before Phase 2 restructuring is applied.

## Guiding Principle

- Preserve the legacy research bundle intact.
- Create a clean root-level structure for future runtime/app code.
- Prefer explicit archival and traceable relocation over destructive renaming.

## Planned Moves

| Old path | Proposed new path | Action | Reason |
| --- | --- | --- | --- |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | move | Archive the full legacy bundle intact and clean the root for the new platform structure. |
| `instructs/` | `instructs/` | no move | Persistent project memory must remain stable at the repo root. |
| legacy notebooks/data inside the archived bundle | remain under archived bundle for now | no internal move yet | Avoid partial migration that could break traceability or silently alter behavior. |
| new runtime/app/package files | root-level standardized directories | scaffold | Create a clean Phase 2 foundation without claiming migrated model logic. |

## Explicit Non-Moves in Phase 2

- No notebook-to-module extraction yet.
- No data canonicalization yet.
- No attempt to normalize or rename files inside the archived legacy bundle.
- No deletion of duplicate or ambiguous legacy files.

## Why This Plan

- Phase 1 established that the current repo is not yet serving-ready.
- A full logic migration would be premature in Phase 2.
- Archiving the existing bundle first creates a safe boundary between:
  - preserved historical research assets
  - new local Dockerized demo foundation
