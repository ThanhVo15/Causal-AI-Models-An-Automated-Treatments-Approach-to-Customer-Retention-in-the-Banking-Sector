# Phase 01 Baseline

## Status

- Phase 1 is an audit/documentation phase only.
- No restructuring, file moves, notebook rewrites, or module extraction were implemented.
- Findings below reflect observed repo state plus user-stated target direction.

## Observed Current Repo Shape

- The workspace root is `/Users/minthanh15/Develop/self-projects/causal-ai`.
- The actual project contents currently live inside a nested repo folder:
  `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`.
- The project is mostly notebooks, CSV exports, a README, an image, and a slide deck.
- No Python package, no tests, no environment manifest, and no API/service layer were observed.

## Current Repo Purpose

- Current observed purpose: a research/demo bundle used to explore and present a causal AI approach to customer retention in banking.
- Current observed flow: business framing -> churn modeling -> clustering -> post-treatment simulation -> causal recommendation/effect analysis.
- The repo is currently much closer to a paper/demo artifact than to a maintainable platform.

## Major Pain Points

- Most logic lives inside notebooks rather than reusable Python modules.
- Paths are hardcoded to Colab, Windows, and Linux environments.
- Reproducibility is weak because notebook execution depends on local state and ad hoc installs.
- Data and intermediate artifacts are committed directly into the repo, including duplicated exports.
- Some evaluation logic appears risky or non-serving-safe:
  - notebook 2 applies SMOTE before train/test split
  - notebook 5 and `Save_Model.ipynb` fit and evaluate on the same dataset
  - notebook 6 trains causal recommendation logic on simulated post-treatment outcomes
- Some notebooks contain hidden-state or dead-code signals:
  - notebook 5 references `df_cai` without defining it inside the notebook
  - notebook 3 references `rfm_data` and contains recorded errors and many empty cells

## Target Product Direction

- User-stated future target: a local Python demo platform, not yet a full production system.
- Expected user flow:
  - upload new customer data
  - validate/profile it
  - run churn prediction
  - run segmentation
  - run recommendation / treatment suggestion
  - show diagnostics and process tracking
  - export results to Excel for sales/business use
- Recorded future local stack direction:
  - Docker
  - Postgres persistence
  - lightweight Python UI such as Streamlit

## What Phase 1 Decided

- The repo should be treated as a research/demo codebase that later needs a clean serving-oriented layer.
- Some notebooks should remain notebooks for research/EDA/reporting.
- Reusable logic should later move into Python modules.
- Research code and future serving code must be separated.
- Future phases should preserve the current workflow meaning before rewriting anything.

## What Phase 1 Did Not Decide

- No final folder move has been executed.
- No final package/module names have been implemented.
- No final artifact registry format has been implemented.
- No final API contract has been implemented.
- No final choice has been made on whether the future demo will keep the current simulation-based causal stage as-is or replace it with real intervention data later.
