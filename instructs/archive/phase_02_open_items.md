# Phase 02 Open Items

## Deferred to Phase 3

- Decide which legacy notebooks should become actively maintained notebooks versus pure archive material.
- Extract reusable preprocessing logic from the overlapping notebook 5 and `Save_Model.ipynb`.
- Extract reusable churn, segmentation, and recommendation modules from legacy notebooks.
- Decide how to handle the simulation-based causal stage in the future demo:
  - preserve it as a transparent demo proxy
  - or redesign the pipeline once real intervention data exists
- Promote canonical raw/interim datasets into the new `data/` structure only after confirmation.
- Wire Streamlit pages to actual upload, profiling, run tracking, and export behavior.
- Connect app actions to Postgres tables and `storage/` outputs.

## Ambiguities Still Unresolved

- Which churn pipeline should be considered canonical once migration starts.
- Whether GPU-heavy clustering should remain first-class or become optional.
- Whether `df_causal_ai` should remain a legacy extensionless file or be normalized later.
- Which legacy intermediates should become official runtime artifacts versus historical references only.

## Risks Future Phases Must Remember

- Do not misrepresent the current causal stage as being based on real observed interventions unless that is later verified.
- Do not assume every branch in notebook 3 is part of the intended canonical pipeline.
- Do not silently clean up duplicate or ambiguous CSVs before documenting exactly what is being discarded or reclassified.
- Do not mistake the new Streamlit + Docker + Postgres scaffold for a working end-to-end application.

## Reality Check After Phase 2

- The repo is structurally cleaner.
- The app/runtime foundation is real but minimal.
- The legacy modeling logic still lives in the archived notebook bundle.
- The next major value will come from controlled module extraction, not from more scaffolding.
