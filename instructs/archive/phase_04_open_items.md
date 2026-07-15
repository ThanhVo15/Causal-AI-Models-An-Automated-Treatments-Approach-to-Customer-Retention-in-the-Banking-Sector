# Phase 04 Open Items

## Unresolved Issues

- The app still relies on the archived legacy bundle for first-run artifact building and recommendation-policy source data.
- No Postgres writes are implemented for uploads, runs, stage logs, or exports.
- No curated demo-safe sample dataset exists under `data/samples/`.
- The dashboard still reflects the limitations of the Phase 3 temporary wrappers.

## Deferred UI / Backend Work

- connect app actions to Postgres foundation tables
- add explicit failed-run persistence and error logs
- add tests around upload registration, run listing, and dashboard loading
- improve profiling beyond the current lightweight dataframe summary
- decide whether to surface policy option details more clearly for business users
- decide whether to add saved charts/images under `artifacts/figures/`

## Phase 5 Priorities

- improve business usability of exports and recommendation presentation
- tighten documentation so a new collaborator can run and understand the app quickly
- add smoke tests or integration tests once runtime dependencies are available
- document the exact limits of the temporary churn/segmentation/recommendation wrappers in user-facing terms
- decide how much of the current simulation-backed recommendation flow should remain in the demo product

## Risks Future Phases Must Remember

- do not present the dashboard as a polished business dashboard; it is a technical demo view
- do not present the recommendation output as production-grade causal inference
- do not assume Docker/runtime parity was verified from the Phase 4 shell session
- do not remove `legacy_snapshot/` until the engine no longer depends on archived CSVs for artifact rebuilding
