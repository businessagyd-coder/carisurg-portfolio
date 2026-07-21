# Decision Journal — Week 7: Model Choice for Phase 3

**Date:** Week 7, CariSurg MedTech Pathways 2026
**Decision owner:** Aiden Daniel

## Context

- The Week 6 baseline (logistic regression) caught only 1 in 4 truly critical (ESI 1) patients; the ED Board and Martina Griffith asked whether a more complex model justifies its added compute cost before Phase 3.
- Three complex model families were built and benchmarked against the Week 6 baselines on the same train/test split: Random Forest (untuned and tuned), Gradient Boosting, and a small MLP.

## Alternatives Considered

- **Tuned Random Forest** — reached the best recall of the week (0.31 for ESI 1) via a 24-candidate `RandomizedSearchCV`, but that search cost 1,099 seconds (~18 minutes) of compute for no benefit over the two options below.
- **Small MLP (neural network)** — matched the same 0.31 recall, but took 103 seconds to train and is the least interpretable model of the six benchmarked — hardest to defend in a one-minute clinician explanation.
- **Gradient Boosting** — matched the same 0.31 recall in 7.7 seconds, with fast inference and feature importances that give a workable (if imperfect) explanation.

## Decision

Carry Gradient Boosting forward as the Phase 3 development track, and do not pursue further Random Forest tuning or the MLP at this stage.

## Reasoning

- All three complex models plateaued at the identical ESI-1 recall (0.31), so the deciding factor was cost, not clinical benefit — Gradient Boosting reaches that plateau roughly 140× cheaper than the tuned Random Forest and ~13× cheaper than the MLP.
- Gradient Boosting's interpretability (feature importances) is weaker than the Week 6 baseline but meaningfully stronger than the MLP's opaque weights, keeping the model defensible to Dr Reyes without extra tooling (SHAP/LIME) that has not yet been requested or set up.
- Complexity has visibly plateaued: three different model families converge on the same 0.31 recall ceiling, which means the next real gain is more likely to come from addressing class imbalance directly (cost-sensitive weighting, resampling) than from a more complex model.

## Things I Do Not Yet Know

- How far off the ESI-1 misses land for each Week 7 model — the Week 6 report's most worrying failure mode (patients under-triaged by two levels, not one) has not been re-checked for Random Forest, Gradient Boosting, or the MLP.
- Whether any of this week's models perform unevenly across demographic subgroups — no fairness audit has been run yet, and it could change or block this recommendation regardless of raw recall.
