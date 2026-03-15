from __future__ import annotations

from collections import Counter

import pandas as pd

from causal_app.schemas.contracts import (
    ALLOWED_GENDERS,
    ALLOWED_GEOGRAPHIES,
    OPTIONAL_INPUT_COLUMNS,
    REQUIRED_INPUT_COLUMNS,
    ValidationResult,
)


class DatasetContractError(ValueError):
    """Raised when an uploaded dataset does not satisfy the minimal dataset contract."""


def _normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result.columns = [str(column).strip() for column in result.columns]
    result["_source_row_number"] = result.index + 2
    return result


def _normalize_gender(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip().lower()
    mapping = {"male": "Male", "female": "Female"}
    return mapping.get(text)


def _normalize_geography(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip().lower()
    mapping = {"france": "France", "germany": "Germany", "spain": "Spain"}
    return mapping.get(text)


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _coerce_binary(series: pd.Series) -> pd.Series:
    normalized = series.copy()
    normalized = normalized.replace(
        {
            True: 1,
            False: 0,
            "true": 1,
            "false": 0,
            "True": 1,
            "False": 0,
            "yes": 1,
            "no": 0,
            "Yes": 1,
            "No": 0,
        }
    )
    return pd.to_numeric(normalized, errors="coerce")


def validate_input_dataframe(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, ValidationResult]:
    working = _normalize_columns(dataframe)

    missing_columns = [column for column in REQUIRED_INPUT_COLUMNS if column not in working.columns]
    if missing_columns:
        raise DatasetContractError(
            "Input dataset is missing required columns: " + ", ".join(missing_columns)
        )

    for column in OPTIONAL_INPUT_COLUMNS:
        if column not in working.columns:
            working[column] = pd.NA

    working["_reject_reasons"] = [[] for _ in range(len(working))]

    numeric_columns = [
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "EstimatedSalary",
    ]
    for column in numeric_columns:
        coerced = _coerce_numeric(working[column])
        invalid = coerced.isna()
        working.loc[invalid, "_reject_reasons"] = working.loc[invalid, "_reject_reasons"].apply(
            lambda reasons, col=column: reasons + [f"invalid_{col.lower()}"]
        )
        working[column] = coerced

    binary_columns = ["HasCrCard", "IsActiveMember"]
    for column in binary_columns:
        coerced = _coerce_binary(working[column])
        invalid = coerced.isna() | ~coerced.isin([0, 1])
        working.loc[invalid, "_reject_reasons"] = working.loc[invalid, "_reject_reasons"].apply(
            lambda reasons, col=column: reasons + [f"invalid_{col.lower()}"]
        )
        working[column] = coerced

    working["Gender"] = working["Gender"].map(_normalize_gender)
    invalid_gender = working["Gender"].isna() | ~working["Gender"].isin(ALLOWED_GENDERS)
    working.loc[invalid_gender, "_reject_reasons"] = working.loc[
        invalid_gender, "_reject_reasons"
    ].apply(lambda reasons: reasons + ["invalid_gender"])

    working["Geography"] = working["Geography"].map(_normalize_geography)
    invalid_geography = working["Geography"].isna() | ~working["Geography"].isin(ALLOWED_GEOGRAPHIES)
    working.loc[invalid_geography, "_reject_reasons"] = working.loc[
        invalid_geography, "_reject_reasons"
    ].apply(lambda reasons: reasons + ["invalid_geography"])

    if "Exited" in working.columns:
        exited_present = working["Exited"].notna()
        if exited_present.any():
            coerced = _coerce_binary(working["Exited"])
            invalid = exited_present & (coerced.isna() | ~coerced.isin([0, 1]))
            working.loc[invalid, "_reject_reasons"] = working.loc[
                invalid, "_reject_reasons"
            ].apply(lambda reasons: reasons + ["invalid_exited"])
            working["Exited"] = coerced

    duplicate_key_column = None
    for key_column in ("CustomerId", "id"):
        present_mask = working[key_column].notna()
        if present_mask.any():
            duplicate_mask = present_mask & working[key_column].astype(str).duplicated(keep="first")
            if duplicate_mask.any():
                duplicate_key_column = key_column
                working.loc[duplicate_mask, "_reject_reasons"] = working.loc[
                    duplicate_mask, "_reject_reasons"
                ].apply(lambda reasons, col=key_column: reasons + [f"duplicate_{col.lower()}"])
                break

    accepted_mask = working["_reject_reasons"].map(len) == 0
    accepted = working.loc[accepted_mask].copy()
    rejected = working.loc[~accepted_mask].copy()

    rejected["reject_reasons"] = rejected["_reject_reasons"].map(lambda values: ";".join(values))
    accepted = accepted.drop(columns=["_reject_reasons"])
    rejected = rejected.drop(columns=["_reject_reasons"])

    reject_reason_counts = Counter()
    for values in rejected["reject_reasons"].fillna(""):
        for reason in str(values).split(";"):
            if reason:
                reject_reason_counts[reason] += 1

    summary = ValidationResult(
        accepted_rows=len(accepted),
        rejected_rows=len(rejected),
        duplicate_key_column=duplicate_key_column,
        reject_reason_counts=dict(sorted(reject_reason_counts.items())),
    )
    return accepted.reset_index(drop=True), rejected.reset_index(drop=True), summary
