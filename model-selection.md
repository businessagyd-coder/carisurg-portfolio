# Model Selection — Audit Trail (Weeks 6–7)

Every model trained during baseline (Week 6) and optimisation (Week 7),
on the identical 80/20 stratified split (`random_state = 42`) of the
Yale EMMLC ED triage extract. **Recall — ESI 1** is the primary clinical
metric (see the Week 6 final report); accuracy and macro F1 are reported
for context, not as the deciding number.

Full reasoning behind the final pick: [`docs/decisions/2026-week-7-model-choice.md`](decisions/2026-week-7-model-choice.md).

| # | Model | Key hyperparameters | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) | Recall — ESI 1 | Train time | Inference (ms/patient) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dummy (stratified guess) | `strategy="stratified"`, `random_state=42` | 0.375 | — | — | 0.204 | 0.00 | <0.1 s | — |
| 2 | Logistic Regression (Week 6) | `max_iter=1000`, `random_state=42`, scaled features | 0.667 | — | — | 0.492 | 0.25 | 1.8 s | 0.007 |
| 3 | Decision Tree (Week 6) | `max_depth=5`, `random_state=42` | 0.556 | — | — | 0.216 | 0.00 | 0.2 s | 0.000 |
| 4 | Random Forest (Week 7) | `n_estimators=300`, `class_weight="balanced"`, `random_state=42` | 0.641 | — | — | 0.390 | 0.00 | 38.2 s | 0.132 |
| 5 | Random Forest, tuned (Week 7) | `RandomizedSearchCV` (24 candidates, 3-fold CV) → `n_estimators=200`, `min_samples_leaf=8`, `max_features=None`, `max_depth=None` | 0.608 | — | — | 0.475 | 0.31 | 1,099 s | 0.050 |
| 6 | **Gradient Boosting (Week 7) — WINNER** | `HistGradientBoostingClassifier`: `max_depth=6`, `learning_rate=0.1`, `max_iter=300`, `class_weight="balanced"`, `random_state=42` | 0.550 | 0.410 | 0.547 | 0.416 | **0.31** | **7.7 s** | 0.007 |
| 7 | Small MLP (Week 7) | `hidden_layer_sizes=(64, 32)`, `alpha=1e-3`, `max_iter=500`, `random_state=42`, scaled features | 0.638 | — | — | 0.498 | 0.31 | 103.1 s | 0.003 |

## Why row 6 won

Rows 5, 6, and 7 all reach the **same** ESI-1 recall (0.31) — the highest
of any model tried. With clinical benefit tied three ways, the deciding
factor was cost: Gradient Boosting reaches that same recall in 7.7
seconds of training, versus 1,099 seconds (~18 min) for the tuned Random
Forest and 103.1 seconds for the MLP, with inference speed matching the
Week 6 logistic-regression baseline and better interpretability
(feature importances) than the MLP's opaque weights.

## Precision/recall (macro) note

Precision and recall (macro) were only captured in full for the pinned
model (row 6) via `src/model.py::evaluate_model()`. Rows 1–5 and 7 report
macro F1 as recorded in the Week 6/7 notebooks; their precision/recall
(macro) breakdowns were not separately logged at the time and are marked
`—` rather than backfilled with an estimate. This will be closed out
before the Tuesday final submission by re-running each model through the
same `evaluate_model()` function for a fully consistent table.
