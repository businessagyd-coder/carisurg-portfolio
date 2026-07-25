"""
src/data.py

Loading and cleaning functions for the Mercer / Yale EMMLC ED triage dataset.

This module owns exactly one job: turn the raw CSV into a clean
(X_train, X_test, y_train, y_test) split. It does NOT do feature
engineering (see src/features.py) or model training (see src/model.py).

Column-exclusion logic is unchanged from the Week 6/7 notebooks —
this is a straight refactor, not a redesign.
"""
from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split

TARGET = "esi"

DEMOGRAPHICS = [
    "age", "gender", "ethnicity", "race", "lang", "religion",
    "maritalstatus", "employstatus", "insurance_status",
]
ADMIN = ["dep_name", "arrivalmode", "arrivalmonth", "arrivalday", "arrivalhour_bin"]
LEAKAGE = ["disposition", "previousdispo"]
# Housekeeping columns that carry no clinical signal (e.g. the old row index):
NON_FEATURES = ["Unnamed: 0"]


def load_raw(path: str) -> pd.DataFrame:
    """Load the cleaned Week 5 CSV from disk. Raises if the file is missing
    or empty, so a bad path fails loudly instead of silently."""
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Loaded an empty dataframe from {path!r}")
    return df


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """Every column that is safe to train on: not the target, not
    demographics, not admin metadata, not a leakage/outcome field, and not
    a housekeeping column. Matches the Week 6/7 FEATURES definition exactly."""
    excluded = set([TARGET, *LEAKAGE, *ADMIN, *DEMOGRAPHICS, *NON_FEATURES])
    return [c for c in df.columns if c not in excluded]


def split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """80/20 stratified split on the target (ESI), matching every notebook
    since Week 6. Returns (X_train, X_test, y_train, y_test)."""
    features = get_feature_columns(df)
    X, y = df[features], df[TARGET]
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)


def load_and_split(path: str, test_size: float = 0.2, random_state: int = 42):
    """Convenience wrapper: load_raw() + split_data() in one call."""
    df = load_raw(path)
    return split_data(df, test_size=test_size, random_state=random_state)
