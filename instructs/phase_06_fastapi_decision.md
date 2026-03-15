# Phase 06 FastAPI Decision

## Recommendation

Defer FastAPI implementation now, but prepare for it later.

## Why FastAPI Is Not The Best Immediate Next Step

- Streamlit is currently the only real consumer of the engine
- the app and pipeline are still file-backed and local-demo-oriented
- Postgres is not yet wired into the app flow
- recommendation logic is still based on temporary legacy wrappers
- adding FastAPI now would create a second interface surface before the current one is fully stabilized

## Why It Is Still Worth Preparing For Later

- the engine is now modular enough that an API layer is feasible later
- input/output contracts already exist
- the repo is moving toward reusable local service behavior
- future integration with other UIs or automation may justify an API boundary

## Suggested Future Scope If FastAPI Is Adopted

Start minimal:

- `/health`
- `/runs`
- `/predict/recommend`
- `/exports/{run_id}`

Use the existing engine rather than rewriting logic.

## Trigger Conditions That Would Justify FastAPI Next

- a second client beyond Streamlit needs the same engine
- external automation or another frontend needs HTTP access
- Postgres-backed run persistence becomes real
- the local demo starts behaving more like a shareable internal service

## FastAPI Risk If Added Too Early

- duplicated app logic
- extra maintenance burden
- premature separation before current demo behavior is fully locked down
