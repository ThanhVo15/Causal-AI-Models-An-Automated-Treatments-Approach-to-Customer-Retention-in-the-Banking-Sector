from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, RobustScaler, StandardScaler


TRACEABILITY_NOTE = (
    "Derived from Save_Model.ipynb cells 4/6/8/10/12/14/16/18 and "
    "5_CAI_P_Post_Generated.ipynb cells 8/10/12/14/16/18/20/22. "
    "Cluster feature projection also uses logic from 3_Clustering Model.ipynb cells 8/9/14/17/23."
)

DROP_METADATA_COLUMNS = ("id", "CustomerId", "Surname")
CHURN_FEATURE_COLUMNS = (
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
)
CAUSAL_FEATURE_COLUMNS = (
    "CreditScore",
    "Gender",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Age_Group",
    "Geography_Germany",
)
CLUSTER_FEATURE_COLUMNS = (
    "Tenure",
    "NumOfProducts",
    "Balance",
    "IsActiveMember",
    "CreditScore",
    "EstimatedSalary",
    "Age",
)


def _age_bin_edges(
    age_50th: float,
    age_75th: float,
    observed_max: float,
    fitted_max: float | None = None,
) -> list[float]:
    upper_edge = max(observed_max, age_75th, fitted_max or age_75th)
    if upper_edge <= age_75th:
        upper_edge = age_75th + 1.0
    return [0, age_50th, age_75th, upper_edge]


def drop_legacy_metadata_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.drop(columns=list(DROP_METADATA_COLUMNS), errors="ignore").copy()


def _prepare_common_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = drop_legacy_metadata_columns(dataframe)
    result = result.copy()
    if "Age" in result.columns:
        result["Age"] = pd.to_numeric(result["Age"], errors="raise").round(0).astype(int)
    for column in ("HasCrCard", "IsActiveMember"):
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="raise").astype(int)
    return result


class DataTypeTransformer(BaseEstimator, TransformerMixin):
    """Notebook-derived type cleanup used before the churn pipeline."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "DataTypeTransformer":
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return _prepare_common_frame(X)


class FeatureEngineering(BaseEstimator, TransformerMixin):
    """Notebook-derived age binning step used before the churn pipeline."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "FeatureEngineering":
        frame = _prepare_common_frame(X)
        self.age_50th_ = frame["Age"].quantile(0.50)
        self.age_75th_ = frame["Age"].quantile(0.75)
        self.age_max_ = frame["Age"].max()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        frame = _prepare_common_frame(X)
        if frame.empty:
            frame["Age_Group"] = pd.Series(dtype="category")
            return frame.drop(columns=["Age"], errors="ignore")
        frame["Age_Group"] = pd.cut(
            frame["Age"],
            bins=_age_bin_edges(
                age_50th=self.age_50th_,
                age_75th=self.age_75th_,
                observed_max=frame["Age"].max(),
                fitted_max=self.age_max_,
            ),
            labels=["Young", "Middle-aged", "Older"],
        )
        frame = frame.drop(columns=["Age"], errors="ignore")
        return frame


class ArrayToDataFrame(BaseEstimator, TransformerMixin):
    """Notebook-derived adapter that restores feature names after ColumnTransformer."""

    def __init__(self, transformer: ColumnTransformer, feature_names: list[str] | None = None) -> None:
        self.transformer = transformer
        self.feature_names = feature_names

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "ArrayToDataFrame":
        self.feature_names_ = self.get_feature_names()
        return self

    def transform(self, X) -> pd.DataFrame:
        return pd.DataFrame(X, columns=self.feature_names_)

    def get_feature_names(self) -> list[str]:
        categorical_names = (
            self.transformer.named_transformers_["categorical"].get_feature_names_out().tolist()
        )
        numerical_names = ["CreditScore", "Balance", "EstimatedSalary", "Tenure"]
        ordinal_names = ["Age_Group"]
        passthrough_names = ["NumOfProducts", "HasCrCard", "IsActiveMember"]
        return categorical_names + numerical_names + ordinal_names + passthrough_names


class ColumnDropper(BaseEstimator, TransformerMixin):
    """Notebook-derived column dropper used to remove `Geography_Spain`."""

    def __init__(self, columns_to_drop: Iterable[str]) -> None:
        self.columns_to_drop = list(columns_to_drop)

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "ColumnDropper":
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.drop(columns=self.columns_to_drop, errors="ignore")


def build_legacy_churn_preprocessor() -> Pipeline:
    categorical_features = ["Gender", "Geography"]
    numerical_features = ["CreditScore", "Balance", "EstimatedSalary", "Tenure"]

    column_transformer = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(drop="first"), categorical_features),
            ("numerical_standard", StandardScaler(), numerical_features[:3]),
            ("numerical_minmax", StandardScaler(), ["Tenure"]),
            (
                "ordinal_age_group",
                OrdinalEncoder(categories=[["Young", "Middle-aged", "Older"]]),
                ["Age_Group"],
            ),
        ],
        remainder="passthrough",
    )

    return Pipeline(
        [
            ("data_type_transform", DataTypeTransformer()),
            ("feature_engineering", FeatureEngineering()),
            ("preprocess", column_transformer),
            ("to_dataframe", ArrayToDataFrame(column_transformer)),
            ("drop_columns", ColumnDropper(columns_to_drop=["Geography_Spain"])),
        ]
    )


def build_legacy_churn_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", build_legacy_churn_preprocessor()),
            (
                "classifier",
                GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=3,
                    random_state=42,
                ),
            ),
        ]
    )


@dataclass
class LegacyCausalFeatureProjector:
    """Projects raw customer rows into the legacy processed feature schema used by `df_train_clean`."""

    scaler: StandardScaler | None = None
    age_50th: float | None = None
    age_75th: float | None = None
    age_max: float | None = None

    def fit(self, dataframe: pd.DataFrame) -> "LegacyCausalFeatureProjector":
        frame = _prepare_common_frame(dataframe)
        self.age_50th = frame["Age"].quantile(0.50)
        self.age_75th = frame["Age"].quantile(0.75)
        self.age_max = frame["Age"].max()
        self.scaler = StandardScaler()
        self.scaler.fit(frame[["CreditScore", "Balance", "EstimatedSalary", "Tenure"]])
        return self

    def transform(self, dataframe: pd.DataFrame, include_exited: bool = False) -> pd.DataFrame:
        if self.scaler is None or self.age_50th is None or self.age_75th is None:
            raise RuntimeError("LegacyCausalFeatureProjector must be fitted before transform().")

        frame = _prepare_common_frame(dataframe)
        ordered_columns = list(CAUSAL_FEATURE_COLUMNS)
        if include_exited:
            ordered_columns.insert(8, "Exited")
        if frame.empty:
            return pd.DataFrame(columns=ordered_columns, index=frame.index)
        age_group = pd.cut(
            frame["Age"],
            bins=_age_bin_edges(
                age_50th=self.age_50th,
                age_75th=self.age_75th,
                observed_max=frame["Age"].max(),
                fitted_max=self.age_max,
            ),
            labels=["Young", "Middle-aged", "Older"],
        )
        scaled = self.scaler.transform(frame[["CreditScore", "Balance", "EstimatedSalary", "Tenure"]])
        projected = pd.DataFrame(
            {
                "CreditScore": scaled[:, 0],
                "Gender": frame["Gender"].map({"Female": 0, "Male": 1}).astype(int),
                "Tenure": scaled[:, 3],
                "Balance": scaled[:, 1],
                "NumOfProducts": pd.to_numeric(frame["NumOfProducts"], errors="raise").astype(int),
                "HasCrCard": frame["HasCrCard"].astype(int),
                "IsActiveMember": frame["IsActiveMember"].astype(int),
                "EstimatedSalary": scaled[:, 2],
                "Age_Group": age_group.map({"Young": 0.0, "Middle-aged": 1.0, "Older": 2.0}).astype(float),
                "Geography_Germany": (frame["Geography"] == "Germany").astype(float),
            },
            index=frame.index,
        )
        if include_exited and "Exited" in frame.columns:
            projected["Exited"] = pd.to_numeric(frame["Exited"], errors="raise").astype(int)
        return projected[ordered_columns]


@dataclass
class LegacyClusterFeatureProjector:
    """Projects raw customer rows into the scaled feature space used to derive legacy cluster labels."""

    robust_scaler: RobustScaler | None = None
    standard_scaler: StandardScaler | None = None

    def fit(self, dataframe: pd.DataFrame) -> "LegacyClusterFeatureProjector":
        frame = _prepare_common_frame(dataframe)
        self.robust_scaler = RobustScaler()
        self.robust_scaler.fit(frame[["Balance", "NumOfProducts"]])
        self.standard_scaler = StandardScaler()
        self.standard_scaler.fit(frame[["CreditScore", "Age", "Tenure", "EstimatedSalary"]])
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if self.robust_scaler is None or self.standard_scaler is None:
            raise RuntimeError("LegacyClusterFeatureProjector must be fitted before transform().")

        frame = _prepare_common_frame(dataframe)
        if frame.empty:
            return pd.DataFrame(columns=list(CLUSTER_FEATURE_COLUMNS), index=frame.index)
        robust_scaled = self.robust_scaler.transform(frame[["Balance", "NumOfProducts"]])
        standard_scaled = self.standard_scaler.transform(
            frame[["CreditScore", "Age", "Tenure", "EstimatedSalary"]]
        )
        projected = pd.DataFrame(
            {
                "Tenure": standard_scaled[:, 2],
                "NumOfProducts": robust_scaled[:, 1],
                "Balance": robust_scaled[:, 0],
                "IsActiveMember": frame["IsActiveMember"].astype(int),
                "CreditScore": standard_scaled[:, 0],
                "EstimatedSalary": standard_scaled[:, 3],
                "Age": standard_scaled[:, 1],
            },
            index=frame.index,
        )
        return projected[list(CLUSTER_FEATURE_COLUMNS)]
