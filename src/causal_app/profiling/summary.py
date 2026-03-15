from __future__ import annotations

from typing import Any

import pandas as pd

from causal_app.schemas.contracts import OPTIONAL_INPUT_COLUMNS, REQUIRED_INPUT_COLUMNS


def build_profile_summary(dataframe: pd.DataFrame) -> dict[str, Any]:
    total_rows = int(len(dataframe))
    total_columns = int(len(dataframe.columns))

    column_summary = pd.DataFrame(
        {
            "column": dataframe.columns,
            "dtype": [str(dtype) for dtype in dataframe.dtypes],
            "non_null_rows": dataframe.notna().sum().values,
            "missing_rows": dataframe.isna().sum().values,
            "missing_pct": [
                round((count / total_rows) * 100, 2) if total_rows else 0.0
                for count in dataframe.isna().sum().values
            ],
            "unique_values": dataframe.nunique(dropna=False).values,
        }
    ).sort_values(["missing_rows", "column"], ascending=[False, True])

    schema_status_rows: list[dict[str, object]] = []
    for column in REQUIRED_INPUT_COLUMNS:
        schema_status_rows.append({"column": column, "kind": "required", "present": column in dataframe.columns})
    for column in OPTIONAL_INPUT_COLUMNS:
        schema_status_rows.append({"column": column, "kind": "optional", "present": column in dataframe.columns})
    schema_status = pd.DataFrame(schema_status_rows)

    duplicate_rows: list[dict[str, object]] = []
    for key_column in ("CustomerId", "id"):
        if key_column in dataframe.columns:
            duplicate_count = int(dataframe[key_column].dropna().astype(str).duplicated(keep="first").sum())
            duplicate_rows.append({"column": key_column, "duplicate_rows": duplicate_count})
    duplicate_summary = pd.DataFrame(duplicate_rows)

    numeric_columns = dataframe.select_dtypes(include=["number"]).columns.tolist()
    numeric_summary = (
        dataframe[numeric_columns].describe().transpose().reset_index().rename(columns={"index": "column"})
        if numeric_columns
        else pd.DataFrame()
    )

    return {
        "row_count": total_rows,
        "column_count": total_columns,
        "column_summary": column_summary.reset_index(drop=True),
        "missing_summary": column_summary.loc[column_summary["missing_rows"] > 0].reset_index(drop=True),
        "schema_status": schema_status,
        "duplicate_summary": duplicate_summary,
        "numeric_summary": numeric_summary,
    }
