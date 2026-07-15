# Phase 03 I/O Contracts

## Supported Input File Types

- `.csv`
- `.xlsx`

Unsupported suffixes and empty files raise `InputFileError`.

## Input Dataset Contract

### Required columns

- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`

### Optional columns

- `id`
- `CustomerId`
- `Surname`
- `Exited`

## Validation And Normalization Rules

- column names are stripped of surrounding whitespace
- an internal `_source_row_number` column is added using spreadsheet-style row numbering (`index + 2`)
- numeric coercion is attempted for:
  - `CreditScore`
  - `Age`
  - `Tenure`
  - `Balance`
  - `NumOfProducts`
  - `EstimatedSalary`
- binary coercion is attempted for:
  - `HasCrCard`
  - `IsActiveMember`
  - `Exited` when present
- `Gender` is normalized to:
  - `Female`
  - `Male`
- `Geography` is normalized to:
  - `France`
  - `Germany`
  - `Spain`
- duplicate detection is attempted on:
  - `CustomerId` first
  - `id` second

## Reject Reason Codes Observed In Phase 3

- `invalid_creditscore`
- `invalid_age`
- `invalid_tenure`
- `invalid_balance`
- `invalid_numofproducts`
- `invalid_estimatedsalary`
- `invalid_hascrcard`
- `invalid_isactivemember`
- `invalid_gender`
- `invalid_geography`
- `invalid_exited`
- `duplicate_customerid`
- `duplicate_id`

## Accepted Row Contract

Accepted rows continue through the engine with:

- normalized raw columns
- optional legacy identifier columns when present
- internal `_source_row_number`

The accepted raw rows are the basis for:

- preprocessing
- churn scoring
- segmentation
- recommendation

## Prepared Feature Contract

`prepared_features.csv` contains:

- `source_row_number`
- `CreditScore`
- `Gender`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`
- `Age_Group`
- `Geography_Germany`

Important note:

- this schema is aligned to the legacy processed tables such as `df_train_clean.csv` and `df_causal_ai`
- it is not yet a finalized long-term public API schema

## Rejected Row Contract

`rejected_rows.csv` contains the original row values that failed validation plus:

- `_source_row_number`
- `reject_reasons`

## Stage Result Contract

Each pipeline stage records:

- `stage_name`
- `status`
- `input_rows`
- `output_rows`
- `details`

Current statuses observed in Phase 3:

- `completed`
- `skipped`

## Final Recommendation Output Contract

`recommendations.csv` contains:

- `source_row_number`
- normalized raw customer columns that survived validation
- optional `id`, `CustomerId`, `Surname`, `Exited` when present in input
- `churn_probability`
- `assigned_cluster`
- `recommended_treatment`
- `estimated_post_churn`
- `expected_absolute_change`
- `policy_scope`
- `policy_sample_size`

## Policy Options Contract

`policy_options.csv` contains row-level candidate treatments considered by the temporary policy wrapper:

- `cluser_label`
- `Treatment`
- `sample_size`
- `mean_p_pre`
- `mean_p_post`
- `mean_delta`
- `estimated_post_churn`
- `expected_absolute_change`
- `source_row_index`
- `input_cluster`
- `input_churn_probability`
- `policy_scope`

Important note:

- `cluser_label` retains the legacy spelling from `df_causal_ai`
- this was intentionally preserved for traceability in Phase 3

## Diagnostics Contract

`diagnostics.json` currently includes:

- input/accepted/rejected row counts
- duplicate-key column used for rejection, if any
- validation reject reason counts
- recommendation counts by treatment
- assigned cluster counts
- churn probability summary
- stage results

## Excel Export Contract

The Excel workbook contains these sheets:

- `Summary`
- `Recommendations`
- `RejectedRows`
- `PolicyOptions`

## Pipeline Result Contract

The in-code `PipelineRunResult` records:

- `run_id`
- `input_path`
- `run_dir`
- `export_path`
- `input_rows`
- `accepted_rows`
- `rejected_rows`
- `stage_results`
- `diagnostics_path`
- `recommendations_path`
- `rejected_rows_path`
- `prepared_features_path`
- `policy_options_path`
