# Phase 5 Open Items

## Business Ambiguities Still Open

- No verified customer-value or revenue proxy is available yet for priority logic.
- It is still unclear whether sales users want one single action list or separate lists by geography/segment/policy.
- `policy_support_rows` is available, but there is no agreed business interpretation for it yet.

## Source-Field Gaps

- no customer value score
- no uplift-confidence score
- no retention-cost estimate
- no downstream revenue outcome
- no explicit human-review notes field

## Export Gaps

- workbook history is still file-backed, not stored in Postgres
- `policy_options.csv` is still technical and remains outside the workbook
- no workbook styling beyond basic usability formatting
- no conditional formatting, color bands, or business template branding

## App/Workflow Gaps

- Streamlit does not yet preview the business-shaped `Customer_Action_List` inside the app
- Export page downloads files correctly in code, but no additional business guidance is shown per run
- no DB-backed audit trail for who generated which workbook

## Testing Gaps

- no automated test coverage yet for priority logic
- no automated test coverage yet for `reason_short`
- no export regression snapshot tests
- Docker path was not verified in this phase because the Docker daemon was unavailable

## Recommended Focus For Phase 6 Or Later

- add unit tests for business-output shaping
- expose the business-shaped action list in Streamlit before download
- evaluate whether a revenue-weighted priority extension is justified
- consider optional human note columns or CRM-ready export formats
- only consider LLM-assisted explanations after the deterministic business contract is stable
