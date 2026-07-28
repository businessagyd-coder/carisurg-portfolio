"""
tests/test_train_smoke.py

Sanity check #2 (Task 4b): runs the full pipeline — feature engineering,
model build, train, evaluate — on a tiny (~50 row) slice of real data.
This is a SMOKE test, not an accuracy test: it does not assert the model
is any good, only that the pipeline runs to completion and returns the
shapes/types it promises. Its job is to catch "the pipeline is broken"
before Martina's new hire finds out the hard way.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import get_feature_columns, load_raw
from src.features import add_clinical_features
from src.model import build_model, evaluate_model, train_model
from sklearn.model_selection import train_test_split as sk_train_test_split

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "yaleemmlc_admissionprediction_triage.csv"
SMOKE_TEST_PARAMS = {
    # Deliberately tiny and fast — this is not meant to reproduce the real
    # benchmark numbers, only to prove the plumbing works end-to-end.
    "max_depth": 3,
    "learning_rate": 0.1,
    "max_iter": 20,
    "random_state": 42,
}


@pytest.mark.skipif(not DATA_PATH.exists(), reason="Dataset not present locally (expected — it's gitignored)")
def test_pipeline_runs_end_to_end_on_small_sample():
    df = load_raw(str(DATA_PATH)).sample(n=50, random_state=42).reset_index(drop=True)

    # NOTE: deliberately NOT using src.data.split_data() here — its stratified
    # split is correct for real training, but a 50-row sample can easily land
    # a triage class with only 1 patient, which a stratified split rejects.
    # A smoke test just needs the pipeline to run; a plain split is enough.
    features = get_feature_columns(df)
    X, y = df[features], df["esi"]
    X_train, X_test, y_train, y_test = sk_train_test_split(X, y, test_size=0.3, random_state=42)
    assert len(X_train) + len(X_test) == 50

    X_train_fe = add_clinical_features(X_train)
    X_test_fe = add_clinical_features(X_test)
    # Feature engineering should only ADD columns, never drop or reorder rows.
    assert len(X_train_fe) == len(X_train)
    assert X_train_fe.shape[1] > X_train.shape[1]

    model = build_model("gradient_boosting", SMOKE_TEST_PARAMS)
    model = train_model(model, X_train_fe, y_train)

    metrics = evaluate_model(model, X_test_fe, y_test)

    # We are not asserting these are GOOD numbers — a 50-row sample with a
    # tiny model tells you nothing about real performance. We are only
    # asserting the pipeline produced the metrics it promised, in range.
    expected_keys = {"accuracy", "precision_macro", "recall_macro", "f1_macro", "recall_ESI1"}
    assert expected_keys.issubset(metrics.keys())
    for key in expected_keys:
        assert 0.0 <= metrics[key] <= 1.0, f"{key} = {metrics[key]!r} is out of a valid [0, 1] range"


def test_build_model_rejects_unknown_model_name():
    """If config.yaml has a typo in model.name, this should fail loudly at
    build time, not train silently on the wrong (default) model."""
    with pytest.raises(ValueError):
        build_model("definitely_not_a_real_model", {})
