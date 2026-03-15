# Phase 5 Reason Logic

## Goal

Generate short, auditable, business-readable explanations without adding LLM dependencies or unsupported freeform claims.

## Why Rule-Based

- current repo does not include GPT/LLM integration for export reasoning
- deterministic output is easier to audit and reproduce
- current recommendation logic is already partial, so explanation logic should stay conservative

## Source Fields Used

- `risk_level`
- `recommended_policy`
- `segment_id`
- `expected_improvement`
- `policy_scope`

## Templates

### Fallback Policy

Used when `policy_scope == overall_fallback`:

- `Fallback policy {recommended_policy} is used because cluster {segment_id} has no cluster-specific support table.`

### No Program

Used when `recommended_policy == No Program`:

- High risk:
  - `High churn risk, but no special program stands out for cluster {segment_id} in the current policy table.`
- Medium risk:
  - `Medium churn risk; no special program is currently prioritized for cluster {segment_id}.`
- Low risk:
  - `Lower churn risk; no special program is currently prioritized for cluster {segment_id}.`

### High Risk With Strong Improvement

Used when `risk_level == High` and `expected_improvement >= 0.03`:

- `High churn risk; {recommended_policy} is prioritized for cluster {segment_id} based on the strongest estimated reduction.`

### High Risk

- `High churn risk; {recommended_policy} is the current top-ranked action for cluster {segment_id}.`

### Medium Risk

- `Medium churn risk; {recommended_policy} is the current recommended next action for cluster {segment_id}.`

### Low Risk

- `Lower churn risk; {recommended_policy} remains the current retention action for cluster {segment_id}.`

## Examples From The Real Sample Export

- `High churn risk; Engage & Elevate is prioritized for cluster 1 based on the strongest estimated reduction.`
- `High churn risk; Reconnect & Reward is the current top-ranked action for cluster 3.`
- `Lower churn risk; Wealth Accumulator Program remains the current retention action for cluster 0.`

## Caveats

- reasons describe current engine outputs; they do not prove causal certainty
- reasons do not include customer value, account tenure strategy, or human sales notes
- sample run `20260315T145700Z-phase5-sample-1b67559c` had no fallback rows and no `No Program` rows, so those templates were implemented but not observed in that sample workbook
