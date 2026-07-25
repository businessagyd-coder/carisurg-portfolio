"""
src/model.py

Model factory, training, and evaluation. The pinned Phase 3 model is
Gradient Boosting (HistGradientBoostingClassifier) — the Week 7 decision
(see docs/decisions/2026-week-7-model-choice.md for the full reasoning).

This module deliberately supports only the models actually benchmarked in
Weeks 6-7, so config.yaml's `model.name` can only point at something real:
logistic_regression, decision_tree, random_forest, random_forest_tuned,
gradient_boosting, mlp.
"""
from __future__ import annotations

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

_BUILDERS = {
    "logistic_regression": lambda p: make_pipeline(
        StandardScaler(), LogisticRegression(**p)
    ),
    "decision_tree": lambda p: DecisionTreeClassifier(**p),
    "random_forest": lambda p: RandomForestClassifier(**p),
    "random_forest_tuned": lambda p: RandomForestClassifier(**p),
    "gradient_boosting": lambda p: HistGradientBoostingClassifier(**p),
    "mlp": lambda p: make_pipeline(
        StandardScaler(), MLPClassifier(**p)
    ),
}


def build_model(name: str, params: dict):
    """Construct an (unfitted) model by name, per config.yaml. Raises
    immediately on an unrecognised name rather than silently ignoring it."""
    if name not in _BUILDERS:
        raise ValueError(
            f"Unknown model name {name!r}. Expected one of: {sorted(_BUILDERS)}"
        )
    return _BUILDERS[name](params)


def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model


def recall_esi1(y_true, y_pred) -> float:
    """Recall for the single most critical class (ESI 1). This is the
    primary clinical metric established in the Week 6 final report —
    NOT accuracy, and not macro/weighted F1."""
    r = recall_score(y_true, y_pred, labels=[1], average=None, zero_division=0)
    return float(r[0]) if len(r) else float("nan")


def evaluate_model(model, X_test, y_test) -> dict:
    """Returns the same metric set used in every Week 6/7 benchmark table:
    accuracy, macro precision/recall/F1, and recall for ESI 1 specifically."""
    preds = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, preds, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, preds, average="macro"),
        "recall_ESI1": recall_esi1(y_test, preds),
    }
