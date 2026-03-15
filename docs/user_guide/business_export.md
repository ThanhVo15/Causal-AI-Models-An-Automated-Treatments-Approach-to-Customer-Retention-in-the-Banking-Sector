# Business Export Workbook

## Purpose

The Phase 5 workbook is a practical handoff package for business and sales review. It is built only from real pipeline outputs produced by the extracted local engine.

Important limitation:

- the recommendation layer still comes from the temporary legacy policy wrapper
- expected improvement values remain traceable to simulated legacy policy data
- `reason_short` is deterministic template logic, not LLM-generated text

## Workbook Structure

### `Summary`

Business-oriented run summary:

- uploaded, valid, and rejected row counts
- priority-band distribution
- risk-level distribution
- recommended-policy distribution
- cluster distribution
- rejection reason counts
- run limitations

### `Customer_Action_List`

Main business action sheet. Typical columns:

- `customer_id`
- `churn_probability`
- `risk_level`
- `segment_id`
- `recommended_policy`
- `expected_improvement`
- `priority_score`
- `priority_band`
- `reason_short`
- `warning_note`

### `Reject_Report`

Operational follow-up sheet for invalid rows:

- source row number
- available customer identifier
- rejection codes
- rejection detail
- rejection stage

### `Run_Metadata`

Traceability sheet with:

- run id
- input file
- export path
- per-stage status and duration snapshot

### `Field_Definitions`

Lightweight field dictionary for the business workbook.

## Traceability Additions In Phase 6

Each successful run now also produces:

- `run_summary.json`
- `run.log`
- `artifact_manifest.json`

These stay outside the workbook, but they make the exported file easier to audit and explain.

## Priority Logic

Current deterministic rules:

- `risk_level = High` if `churn_probability >= 0.75`
- `risk_level = Medium` if `churn_probability >= 0.50`
- otherwise `Low`
- `priority_band = P1` if risk is High and `expected_improvement >= 0.03`
- `priority_band = P2` if risk is High
- `priority_band = P2` if risk is Medium and `expected_improvement >= 0.02`
- otherwise `priority_band = P3`
- `priority_score = churn_probability * 100`

No customer-value score, uplift confidence score, or LLM narrative is added in this phase.

## Reason Logic

`reason_short` is generated from deterministic templates using:

- `risk_level`
- `recommended_policy`
- `segment_id`
- `expected_improvement`
- `policy_scope`

Examples:

- `High churn risk; Premium Balance Rewards is the current top-ranked action for cluster 2.`
- `Fallback policy No Program is used because cluster 1 has no cluster-specific support table.`

## Recommended Use

1. Review `Summary` for overall file quality and recommended action mix.
2. Use `Customer_Action_List` as the primary sales action sheet.
3. Use `Reject_Report` to fix upload quality issues before rerunning the pipeline.
4. Keep `Run_Metadata` when sharing the workbook internally so the run remains traceable.
