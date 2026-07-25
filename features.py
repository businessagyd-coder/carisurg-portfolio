"""
src/features.py

Clinical feature engineering, unchanged from the Week 7 notebook —
this is a straight refactor of the add_clinical_features() cell into
a reusable, importable function.
"""
from __future__ import annotations

import pandas as pd


def add_clinical_features(data: pd.DataFrame) -> pd.DataFrame:
    """Adds vital-sign ratios and clinical "red flag" indicators on top of
    the raw features. Applied identically to train and test sets so there
    is no leakage between them (each row is transformed independently)."""
    out = data.copy()

    # --- ratios & combinations ---
    out["shock_index"] = out["triage_vital_hr"] / out["triage_vital_sbp"]        # HR / SBP
    out["pulse_pressure"] = out["triage_vital_sbp"] - out["triage_vital_dbp"]    # SBP - DBP
    out["spo2_rr_ratio"] = out["triage_vital_o2"] / out["triage_vital_rr"]       # oxygen vs. effort

    # --- red-flag indicators (do NOT use blood pressure) ---
    out["is_tachypneic"] = (out["triage_vital_rr"] > 20).astype(int)
    out["is_hypoxic"] = (out["triage_vital_o2"] < 92).astype(int)
    out["is_febrile"] = (out["triage_vital_temp"] >= 100.4).astype(int)

    # --- severity score: how many red flags fire at once ---
    out["red_flag_count"] = out[["is_tachypneic", "is_hypoxic", "is_febrile"]].sum(axis=1)

    return out
