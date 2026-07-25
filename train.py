#!/usr/bin/env python3
"""
scripts/train.py

Single entry point: reads config.yaml, trains the pinned model, prints
the same metrics used in every Week 6/7 benchmark table, and saves the
fitted model to disk.

Usage:
    python scripts/train.py --config config.yaml

DRAFT NOTE (Week 8 interim): this wires src/data.py, src/features.py, and
src/model.py together end-to-end and runs correctly, but has not yet been
exercised by the tests/ sanity checks (Task 4, due with the Tuesday final
submission) — treat it as a working draft, not the audited final version.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as `python scripts/train.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import load_raw, split_data
from src.features import add_clinical_features
from src.model import build_model, evaluate_model, train_model
from src.utils import load_config, save_model, timed


def main(config_path: str) -> None:
    cfg = load_config(config_path)

    print(f"[1/4] Loading data from {cfg['data']['path']} ...")
    df = load_raw(cfg["data"]["path"])
    X_train, X_test, y_train, y_test = split_data(
        df,
        test_size=cfg["data"]["test_size"],
        random_state=cfg["data"]["random_state"],
    )

    if cfg.get("features", {}).get("engineered", False):
        print("[2/4] Applying clinical feature engineering ...")
        X_train = add_clinical_features(X_train)
        X_test = add_clinical_features(X_test)
    else:
        print("[2/4] Skipping feature engineering (features.engineered = false)")

    print(f"[3/4] Training {cfg['model']['name']} ...")
    model = build_model(cfg["model"]["name"], cfg["model"]["params"])
    model, train_time = timed(train_model, model, X_train, y_train)
    print(f"      Training time: {train_time:.2f}s")

    print("[4/4] Evaluating on held-out test set ...")
    metrics, infer_time = timed(evaluate_model, model, X_test, y_test)
    per_patient_ms = (infer_time / len(y_test)) * 1000

    print("\n--- Results ---")
    for k, v in metrics.items():
        print(f"  {k}: {v:.3f}")
    print(f"  inference_ms_per_patient: {per_patient_ms:.4f}")

    save_model(model, cfg["output"]["model_path"])
    print(f"\nModel saved to {cfg['output']['model_path']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the pinned Phase 3 triage model.")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()
    main(args.config)
