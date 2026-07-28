"""
tests/test_data.py

Sanity check #1 (Task 4a): confirms the data-loading step returns what the
rest of the pipeline assumes it returns. This is NOT a test that the model
is "correct" — it exists so that a bad CSV, a renamed column, or a moved
file fails loudly here, at load time, instead of silently three steps
later inside model training.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import TARGET, get_feature_columns, load_raw, split_data

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "yaleemmlc_admissionprediction_triage.csv"


@pytest.mark.skipif(not DATA_PATH.exists(), reason="Dataset not present locally (expected — it's gitignored)")
def test_load_raw_returns_nonempty_dataframe():
    df = load_raw(str(DATA_PATH))
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0


@pytest.mark.skipif(not DATA_PATH.exists(), reason="Dataset not present locally (expected — it's gitignored)")
def test_target_column_present_and_valid():
    df = load_raw(str(DATA_PATH))
    assert TARGET in df.columns
    # ESI is a 5-level triage scale; anything outside 1-5 means the wrong
    # column or a corrupted export got loaded.
    observed_levels = set(df[TARGET].dropna().unique())
    assert observed_levels.issubset({1, 2, 3, 4, 5, 1.0, 2.0, 3.0, 4.0, 5.0})


@pytest.mark.skipif(not DATA_PATH.exists(), reason="Dataset not present locally (expected — it's gitignored)")
def test_feature_columns_exclude_leakage_and_housekeeping():
    df = load_raw(str(DATA_PATH))
    features = get_feature_columns(df)

    assert TARGET not in features
    assert "disposition" not in features, "outcome-only field leaked into features"
    assert "previousdispo" not in features, "outcome-only field leaked into features"
    assert "Unnamed: 0" not in features, "housekeeping row-index column leaked into features"
    assert len(features) > 0


def test_data_module_exposes_expected_names():
    """This one runs even without the CSV present — it just confirms the
    module's public surface hasn't silently changed shape."""
    import src.data as data_module

    for name in ("load_raw", "get_feature_columns", "split_data", "load_and_split", "TARGET"):
        assert hasattr(data_module, name), f"src.data is missing expected name: {name}"
