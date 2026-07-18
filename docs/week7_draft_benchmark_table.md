# Week 7 — Draft Six-Axis Benchmark (Interim)

| model                          |   accuracy |   precision_macro |   recall_macro |   f1_macro |   recall_ESI1 |   train_time_s |   inference_ms_per_patient | interpretability                                                                |
|:-------------------------------|-----------:|------------------:|---------------:|-----------:|--------------:|---------------:|---------------------------:|:--------------------------------------------------------------------------------|
| Week 6 — Logistic Regression   |      0.667 |             0.582 |          0.463 |      0.492 |         0.25  |          2.012 |                      0.008 | High — signed coefficients per feature, explainable in <1 min                   |
| Week 6 — Decision Tree         |      0.556 |             0.265 |          0.245 |      0.216 |         0     |          0.203 |                      0.001 | High — single traceable path of if/else splits                                  |
| Week 7 — Random Forest         |      0.641 |             0.469 |          0.369 |      0.39  |         0     |         42.343 |                      0.133 | Medium — feature importances only; no single traceable path (300 trees)         |
| Week 7 — Random Forest (tuned) |      0.608 |             0.452 |          0.519 |      0.475 |         0.312 |          0     |                      0.052 | Medium — same as above                                                          |
| Week 7 — Gradient Boosting     |      0.55  |             0.41  |          0.547 |      0.416 |         0.312 |          7.432 |                      0.007 | Medium-Low — feature importances only; sequential trees harder to unpick        |
| Week 7 — Small MLP             |      0.638 |             0.526 |          0.482 |      0.498 |         0.312 |        122.273 |                      0.004 | Low — weights are not human-readable; needs SHAP/LIME to explain one prediction |
