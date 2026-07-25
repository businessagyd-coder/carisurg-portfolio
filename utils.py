"""
src/utils.py

Small shared helpers used by more than one module. Nothing clever on
purpose — this file should stay boring.
"""
from __future__ import annotations

import time
from pathlib import Path

import joblib
import yaml


def load_config(path: str) -> dict:
    """Read config.yaml into a plain dict."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def timed(fn, *args, **kwargs):
    """Run fn(*args, **kwargs), returning (result, elapsed_seconds).
    Used to keep training/inference timing consistent with the Week 7
    benchmark methodology (wall-clock time.time(), not CPU time)."""
    t0 = time.time()
    result = fn(*args, **kwargs)
    return result, time.time() - t0


def save_model(model, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: str):
    return joblib.load(path)
