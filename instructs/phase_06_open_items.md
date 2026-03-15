# Phase 06 Open Items

## Remaining Rough Edges

- Streamlit still does not treat failed runs as first-class records
- Postgres is still not wired into the app run lifecycle
- recommendation output still inherits the limitations of the legacy simulation-backed wrapper
- no curated demo-safe sample dataset exists in `data/samples/`

## Testing Gaps

- no browser automation for Streamlit
- no Dockerized integration test
- no regression test for the full heavy pipeline output on the archived sample
- no unit tests yet for every model-wrapper edge case

## Observability Gaps

- logs are file-backed, not queryable via DB
- no app page yet for browsing log content directly
- no structured JSON logging

## Product / Architecture Gaps

- no DB-backed run/export history
- no CRM-ready export variant
- no agreed business interpretation for `policy_support_rows`
- no revenue-weighted prioritization

## Recommended Focus For Phase 7 Or Later

- decide whether to expose failed runs and logs more explicitly in the app
- decide whether to wire Postgres into uploads/runs/exports
- add a small set of regression tests around the real archived sample run
- only introduce FastAPI when a second consumer or real service boundary appears
