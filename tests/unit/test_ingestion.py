from __future__ import annotations

import pandas as pd
import pytest

from causal_app.ingestion.files import InputFileError, read_input_dataset
from causal_app.ingestion.validation import DatasetContractError, validate_input_dataframe


def _valid_input_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "CustomerId": 1001,
                "Surname": "Alice",
                "CreditScore": 650,
                "Geography": "France",
                "Gender": "Female",
                "Age": 35,
                "Tenure": 5,
                "Balance": 1000.0,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 50000.0,
            }
        ]
    )


def test_read_input_dataset_supports_csv_and_xlsx(tmp_path):
    dataframe = _valid_input_frame()
    csv_path = tmp_path / "sample.csv"
    xlsx_path = tmp_path / "sample.xlsx"
    dataframe.to_csv(csv_path, index=False)
    dataframe.to_excel(xlsx_path, index=False)

    csv_loaded = read_input_dataset(csv_path)
    xlsx_loaded = read_input_dataset(xlsx_path)

    assert csv_loaded.to_dict(orient="records") == dataframe.to_dict(orient="records")
    assert xlsx_loaded.to_dict(orient="records") == dataframe.to_dict(orient="records")


def test_read_input_dataset_rejects_empty_file(tmp_path):
    empty_path = tmp_path / "empty.csv"
    _valid_input_frame().head(0).to_csv(empty_path, index=False)

    with pytest.raises(InputFileError, match="contains no data rows"):
        read_input_dataset(empty_path)


def test_validate_input_dataframe_tracks_rejects_and_duplicates():
    dataframe = pd.DataFrame(
        [
            {
                "CustomerId": 1001,
                "Surname": "Alice",
                "CreditScore": 650,
                "Geography": "France",
                "Gender": "Female",
                "Age": 35,
                "Tenure": 5,
                "Balance": 1000.0,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 50000.0,
            },
            {
                "CustomerId": 1001,
                "Surname": "Bob",
                "CreditScore": 700,
                "Geography": "Germany",
                "Gender": "Male",
                "Age": 40,
                "Tenure": 6,
                "Balance": 2000.0,
                "NumOfProducts": 1,
                "HasCrCard": 1,
                "IsActiveMember": 0,
                "EstimatedSalary": 60000.0,
            },
            {
                "CustomerId": 1003,
                "Surname": "Cara",
                "CreditScore": 720,
                "Geography": "Italy",
                "Gender": "Female",
                "Age": 29,
                "Tenure": 2,
                "Balance": 3000.0,
                "NumOfProducts": 1,
                "HasCrCard": "maybe",
                "IsActiveMember": 1,
                "EstimatedSalary": 70000.0,
            },
        ]
    )

    accepted, rejected, summary = validate_input_dataframe(dataframe)

    assert len(accepted) == 1
    assert len(rejected) == 2
    assert summary.accepted_rows == 1
    assert summary.rejected_rows == 2
    assert summary.duplicate_key_column == "CustomerId"
    assert summary.reject_reason_counts == {
        "duplicate_customerid": 1,
        "invalid_geography": 1,
        "invalid_hascrcard": 1,
    }


def test_validate_input_dataframe_missing_required_columns_raises():
    dataframe = _valid_input_frame().drop(columns=["Age"])

    with pytest.raises(DatasetContractError, match="missing required columns"):
        validate_input_dataframe(dataframe)
