# Handover Document — Mercer ED Triage Model (Phase 3)

**Prepared for:** Martina Griffith (Clinical IT Lead), Dr De Freitas
**Prepared by:** Aiden Daniel, CariSurg MedTech Pathways 2026
**Status:** Development-stage baseline. **Not approved for clinical use.**

## 1. Project Summary

This project explores whether a machine-learning model can assist ED
triage decisions at Mercer General Hospital by predicting Emergency
Severity Index (ESI) level from a patient's vital signs and chief
complaint at the point of intake. It uses the Yale EMMLC triage dataset
(55,121 historical visits) as a stand-in for Mercer's own data during
development. Over Weeks 6–7, two baseline models and four more complex
models were built, benchmarked, and compared honestly against each other
on the metric that actually matters clinically — recall on the most
critical patients — rather than on overall accuracy, which is misleading
on a dataset this imbalanced. This document exists so that anyone
picking up the project after this handover — a new team member, IT
Governance, or a future version of the author — can understand what was
built, why, and exactly how to run it, without re-reading eight weeks of
notebooks.

## 2. Final Model Decision

**Gradient Boosting** (`HistGradientBoostingClassifier`) is the pinned
Phase 3 model, committed in `config.yaml`.

**Why, in one sentence:** three different model families (tuned Random
Forest, Gradient Boosting, and a small neural network) all reached the
identical recall on critical patients, and Gradient Boosting reached it
in 7.7 seconds of training versus 1,099 seconds (~18 minutes) for the
next-best alternative, with no loss in clinical benefit.

Full reasoning: [`docs/decisions/2026-week-7-model-choice.md`](decisions/2026-week-7-model-choice.md).
Full comparison across every model tried: [`docs/model-selection.md`](model-selection.md).

**This model is not deployable as-is.** Its recall on the most critical
patients (ESI 1) is 0.31 — it still misses roughly two in three of the
sickest patients in testing. It is the best option produced so far, not
a finished product. See Section 5.

## 3. How to Run

Requirements: Python 3.10 or later, `pip`, and a copy of the dataset CSV
(see Section 4 — it is not included in this repository).

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/carisurg.git
cd carisurg

# 2. Install dependencies (pinned versions — see requirements.txt)
pip install -r requirements.txt

# 3. Place the dataset at the expected path
#    (see config.yaml -> data.path; not committed to this repo — see Section 4)
mkdir -p data
cp /path/to/yaleemmlc_admissionprediction_triage.csv data/

# 4. Run the pipeline
python scripts/train.py --config config.yaml

# 5. Run the sanity tests
pytest tests/ -v
```

Expected output from step 4: training and evaluation logs, ending with
accuracy, precision, recall, F1, and ESI-1 recall printed to the
terminal, and a fitted model saved to `models/gradient_boosting_v1.joblib`.

All hyperparameters, the data path, the train/test split ratio, and the
random seed are controlled from the single `config.yaml` file — nothing
else needs to be edited to reproduce the reported numbers.

## 4. Where the Data Lives (and Governance Status)

The dataset used throughout this project is the **Yale EMMLC** ED triage
extract, used as a development stand-in while Mercer's own data
governance approval is pending. It is **not committed to this
repository** (`data/*.csv` is excluded via `.gitignore`) because this
repository is public and the file contains patient-level records.

**Governance status:** development/training use only, under the terms
the dataset was originally obtained for this coursework project. This
model has **not** been reviewed or approved for use with real Mercer
patient data, and no Mercer patient data has been used at any point in
this project to date. Before this pipeline is pointed at any real
hospital data, that requires separate governance sign-off that is
outside the scope of this handover and has not yet happened.

Anyone who needs the dataset to run this pipeline should request it
through the project supervisor (Dr De Freitas) rather than expecting it
to be present in the repository.

## 5. Known Limitations

- **Recall on the most critical patients (ESI 1) is 0.31 at best**,
  across every model tried in Weeks 6–7. That means roughly two in
  three of the sickest patients in testing were not correctly flagged
  as critical. This is the single biggest reason this model is not
  deployable — it is a development-stage result, not a clinical one.
- **No subgroup fairness audit has been run.** Random Forest performance
  measurably shifts when demographic features are added to the model
  (see the Week 7 notebook, Section 7), but no model in this project has
  been checked for uneven performance across demographic groups. This
  should be treated as an open deployment blocker, independent of which
  model is eventually chosen.
- **Near-miss severity has not been fully characterised for the Week 7
  models.** The Week 6 report found that under-triage misses can land
  one level off (less dangerous) or two levels off (more dangerous) from
  a patient's true ESI category, but this breakdown has not been re-run
  for Random Forest, Gradient Boosting, or the MLP — only aggregate
  recall is currently reported for those models.

---
*For the full audit trail of every model considered and why this one was
chosen, see `docs/model-selection.md` and
`docs/decisions/2026-week-7-model-choice.md`.*
