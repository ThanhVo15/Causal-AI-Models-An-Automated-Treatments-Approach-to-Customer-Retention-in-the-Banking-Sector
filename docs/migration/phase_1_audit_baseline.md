# Phase 1 Audit Baseline

This document formalizes the Phase 1 audit baseline before any Phase 2 restructuring.
Source of truth: files in [`instructs/`](../../instructs/).

## Current Repo Purpose

- Observed current repo purpose: a research/demo bundle for a causal AI approach to banking customer retention.
- Observed workflow: business framing -> churn modeling -> clustering -> post-treatment simulation -> causal recommendation/effect analysis.
- The repo is not yet a maintainable platform or serving-ready application.

## Key Pain Points

- Most logic lives inside notebooks.
- No real `src/` package, tests, dependency manifest, or serving structure were observed in the legacy bundle.
- Multiple hardcoded execution environments exist: Colab, Windows, and Linux server paths.
- Reproducibility is weak because notebook execution depends on local state and ad hoc `pip install` usage.
- Intermediate CSVs are committed directly to the repo, including duplicated exports.
- Some notebook behavior appears risky for downstream serving use:
  - SMOTE before split in notebook 2
  - same-dataset fit/evaluate behavior in notebook 5 and `Save_Model.ipynb`
  - simulated post-treatment outcomes feeding the causal stage

## Future Direction Established in Phase 1

- Future direction: a local Python demo platform.
- Expected flow:
  - upload new customer data
  - validate/profile it
  - run preprocessing + churn scoring + segmentation + recommendation
  - show diagnostics and process tracking
  - export Excel for sales
- Preferred local foundation:
  - Docker
  - Postgres persistence
  - lightweight Python UI, likely Streamlit

## Phase 1 Decisions to Preserve

- Treat the existing project as a research/demo codebase.
- Preserve legacy meaning before rewriting logic.
- Keep some notebooks for research/reporting.
- Later move reusable logic into Python modules.
- Separate research code from future serving/runtime code.

## Not Yet Decided in Phase 1

- Final canonical module boundaries.
- Final API contract.
- Final artifact layout.
- Whether the future demo will preserve the current simulation-based causal stage as-is.
