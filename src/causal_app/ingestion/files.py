from __future__ import annotations

from pathlib import Path

import pandas as pd


SUPPORTED_INPUT_SUFFIXES = {".csv", ".xlsx"}


class InputFileError(ValueError):
    """Raised when an uploaded dataset cannot be read safely."""


def read_input_dataset(input_path: str | Path) -> pd.DataFrame:
    path = Path(input_path).expanduser().resolve()
    if not path.exists():
        raise InputFileError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise InputFileError(f"Input path is not a file: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_INPUT_SUFFIXES:
        raise InputFileError(
            f"Unsupported file format '{suffix or '<no suffix>'}'. Supported formats: CSV, XLSX."
        )

    try:
        if suffix == ".csv":
            dataframe = pd.read_csv(path)
        else:
            dataframe = pd.read_excel(path)
    except Exception as exc:  # pragma: no cover - exercised only with real dependencies/files
        raise InputFileError(f"Failed to read input file '{path.name}': {exc}") from exc

    if dataframe.empty:
        raise InputFileError(f"Input file '{path.name}' contains no data rows.")

    return dataframe
