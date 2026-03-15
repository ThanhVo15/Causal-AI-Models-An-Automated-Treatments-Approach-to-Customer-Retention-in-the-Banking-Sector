# Phase 5 Excel Design

## Intended Users

- Primary: sales or business users who need a customer action list
- Secondary: data scientists and analysts who need traceability for the generated workbook

## Workbook Structure

### `Summary`

Purpose:

- provide a compact business overview of the run
- show how many rows were usable
- show what action mix was recommended
- show what data-quality issues blocked rows

Current sections:

- `Run`
- `Volume`
- `Priority`
- `Risk`
- `Policy`
- `Segment`
- `Rejects`
- `Limitations`

### `Customer_Action_List`

Purpose:

- serve as the main sheet for business follow-up
- give one row per accepted customer record
- sort rows by business priority

Current columns:

- `run_id`
- `customer_id`
- `customer_id_source`
- `source_row_number`
- `customer_surname`
- `geography`
- `age`
- `balance`
- `num_products`
- `churn_probability`
- `risk_level`
- `segment_id`
- `recommended_policy`
- `expected_post_churn`
- `expected_improvement`
- `priority_score`
- `priority_band`
- `reason_short`
- `recommendation_scope`
- `policy_support_rows`
- `warning_note`

### `Reject_Report`

Purpose:

- help operations or data owners fix the input file
- preserve row-level rejection traceability

Current columns:

- `run_id`
- `source_file`
- `source_row_number`
- `customer_id`
- `customer_id_source`
- `customer_surname`
- `geography`
- `rejection_status`
- `rejection_stage`
- `reject_reason_codes`
- `reject_reason_detail`

### `Run_Metadata`

Purpose:

- preserve traceability for the workbook
- capture input source and stage timing snapshot

Current structure:

- one `item`, `value` table
- includes stage status lines like `stage::<stage_name>::<status>`

### `Field_Definitions`

Purpose:

- make the workbook self-explanatory for downstream consumers
- preserve mapping from internal engine fields to workbook meaning

## Column Design Principles

- prefer business-readable names in the workbook
- keep enough traceability back to internal engine outputs
- avoid unsupported confidence or value fields
- expose limitations rather than hiding them

## Current Formatting

- frozen header row
- autofilter on each sheet
- styled header row
- bounded auto-sized column widths

## Important Limitations

- the action list is business-friendly, but still built on the temporary Phase 3 recommendation engine
- no explicit revenue score, CLV, or uplift-confidence column exists yet
- `policy_options.csv` remains a technical support file outside the workbook
