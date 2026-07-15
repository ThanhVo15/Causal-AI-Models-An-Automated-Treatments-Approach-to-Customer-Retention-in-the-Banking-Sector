# Phase 5 Priority Logic

## Goal

Provide a deterministic ranking that sales/business users can sort and act on without inventing unsupported business meaning.

## Source Fields Used

- `churn_probability`
- `expected_absolute_change`

Derived fields:

- `expected_improvement = max(-expected_absolute_change, 0.0)`
- `priority_score = churn_probability * 100`
- `risk_level`
- `priority_band`

## Exact Rules

### Risk Level

- `High` if `churn_probability >= 0.75`
- `Medium` if `churn_probability >= 0.50`
- `Low` otherwise

### Priority Band

- `P1` if `risk_level == High` and `expected_improvement >= 0.03`
- `P2` if `risk_level == High`
- `P2` if `risk_level == Medium` and `expected_improvement >= 0.02`
- `P3` otherwise

### Priority Score

- `priority_score = churn_probability * 100`

### Action List Sorting

Rows are sorted by:

1. `priority_band` in order `P1`, `P2`, `P3`
2. `priority_score` descending
3. `expected_improvement` descending

## Why This Is The Current Rule Set

- `churn_probability` is the strongest currently available row-level risk signal
- `expected_absolute_change` is already produced by the existing recommendation wrapper
- no verified customer-value score is currently available
- no verified confidence score is currently available

## Caveats

- `expected_improvement` still depends on the temporary recommendation wrapper derived from simulated legacy policy data
- `priority_score` is intentionally simple; it is not a revenue-weighted business score
- this logic is for demo/business triage, not for production prioritization policy

## Sample Run Snapshot

From sample run `20260315T145700Z-phase5-sample-1b67559c`:

- `P1`: 971
- `P2`: 2031
- `P3`: 16696
