# carisurg-portfolio
# Week 0 

# DAY 1 — Environment Setup & Gender Column Cleaning
CariSurg MedTech Pathways | Mercer General Hospital
A hands-on intro to Python and data cleaning using a dirty emergency triage dataset. Trainees set up Google Colab, learn the basics, and standardise the Gender column as their Day 1 challenge.
What's covered

Google Colab setup + Python fundamentals (variables, loops, functions)
Loading a CSV with pandas
Cleaning a messy categorical column using .map()

Dataset
EmergencyTriageDataset_Reduced_Dirty.csv — a sample triage dataset with intentionally inconsistent values to mimic real clinical data.


# DAY 2 - Tutorial 2 — Advanced Data Cleaning
CariSurg MedTech Pathways | Mercer General Hospital
Advanced cleaning techniques on the emergency triage dataset — understanding clinical meaning before deciding how to clean.
What's covered

Pandas inspection commands + clinical reference ranges
Type conversion, outlier detection, and imputation (mean/median/mode)
Unit inconsistency handling (e.g. °C vs °F in Temp)

Breakout Challenge
Each group cleans one assigned column (DBP, pulse, RR, Fio2, or MAP) and presents their approach.


# DAY 3 - Tutorial 3 — Data Visualisation
CariSurg MedTech Pathways | Mercer General Hospital
Turning the cleaned triage dataset into clinically meaningful plots. The rule: every plot must answer a specific clinical question — not just look nice.
What's covered

Bar plots, histograms, scatter plots, and box plots with matplotlib
Adding clinical reference lines (e.g. GCS ≤ 8, bradycardia/tachycardia thresholds)
Saving and sharing plots

# Day 4 — Vital Sign Write-up
CariSurg MedTech Pathways | Mercer General Hospital
A short plain-language write-up on one vital sign from the Mercer General triage dataset.
Task
Pick one vital sign (pulse, temperature, respiratory rate, SBP, or SpO2) and write one paragraph covering:

- What it is
- What the normal range looks like
- Why a triage nurse would care


# Day 5 — Other Metrics Write-up
CariSurg MedTech Pathways | Mercer General Hospital
A short reflective paragraph on clinical metrics that exist beyond the Mercer General triage dataset and why they matter.
Task
Write one paragraph covering metrics not included in the current dataset — what they are, why they are clinically relevant at triage, and what their absence means for our analysis.


# Day 6 — At-Risk Patient Logic Pseudocode
CariSurg MedTech Pathways | Mercer General Hospital
Pseudocode for a function that evaluates a patient's pulse and flags them as at-risk if their reading falls outside a defined safe range.
Logic

Critical Low: pulse < 20 bpm — near-absent cardiac output
Normal: 20–250 bpm — functional range covering athletic and paediatric cases
Critical High: pulse > 250 bpm — exceeds survivable arrhythmia rates

Thresholds are set at extremes to minimise false positives. Standard bradycardia (<60 bpm) and tachycardia (>100 bpm) are candidates for a secondary warning tier.

# Week 1 

The Week 1 deliverable is a preliminary research proposal for a 12-week pilot at Mercer General Hospital testing whether AI can improve emergency department triage in a Caribbean context.

What was done:
Five recent papers on AI-assisted ED triage were reviewed and summarised across four dimensions — problem, method, outcome, and limitation. Two gaps were identified from the literature: no existing AI triage model has been validated on Caribbean patient data, and no equity evidence exists for AI triage in resource-constrained settings. These gaps anchor a proposed pilot that retrains the TriageIntelli stacking ensemble on de-identified Mercer ED records and measures whether inter-rater triage disagreement drops by at least 15%.

Outputs produced: a filled preliminary proposal (.docx), a plain literature summary (.pdf), and a GitHub README (.md) — all consistent with the rubric criteria and project brief.

# CariSurg MedTech Pathways 2026 — Project README

**Project:** AI-assisted triage validation for a fictional Caribbean emergency
department (Mercer General Hospital), using the Yale EMMLC ED triage dataset.
**Supervisor:** Dr De Freitas · **Clinical reviewer:** Dr Reyes · **Clinical IT
Lead:** Martina Griffith
**Author:** Aiden Daniel

> Note on how this document was compiled: built from saved project memory plus
> full detail from this chat's Weeks 6–8 work — not a live search of every past
> conversation. If something from Weeks 2–5 is thin or missing below, it's
> because it wasn't captured in a memory note at the time, not because it
> didn't happen.

---

## Week 2 — Repository Setup & Conventions

- Restructured the `carisurg-portfolio` GitHub repository (web UI only, no
  command line) into a professional folder layout, using feature branches and
  pull requests.
- Set up Zotero-managed references in IEEE style.
- Established the document conventions used for the rest of the project:
  Arial font, British English, navy/teal headings, IEEE superscript
  citations, stratified 80/20 train/test splits, `random_state = 42`.

## Week 3 — Workflow & System Design

- Produced a Mercer ED triage workflow diagram showing where an AI model
  could plug into the existing clinical process.
- Rendered via Graphviz (Mermaid CLI wasn't available in the working
  environment), formatted for direct GitHub web upload.

## Week 4 — Risk & Governance

- Produced a 10-item risk register for the project.
- Wrote up the IBM Watson for Oncology case study as a cautionary example of
  AI-in-healthcare harm.

## Week 5 — Data Exploration & Feasibility

- Executed tutorial notebooks against the Yale EMMLC dataset (55,121 rows,
  226 columns), generating the required figures.
- Produced an independent analysis notebook with original findings,
  including:
  - A respiratory-rate default-charting pattern — RR = 18 recorded for
    ~47% of patients, suggesting a default/placeholder value rather than a
    measured one.
  - An equity analysis of ESI (Emergency Severity Index) assignment across
    patient demographics.
- Rebuilt the feasibility memo as a polished Word document (IEEE-style
  superscript citations, Arial/navy/teal styling, British English).
- Established the `\notebooks` and `\docs\figs` GitHub folder convention
  used in every week since.

## Week 6 — Baseline Models

**Interim & final submission completed.**

- Built two baseline classifiers on the Week 5 cleaned dataset: logistic
  regression and a depth-bounded decision tree (`max_depth=5`).
- Compared both against a stratified random-guess baseline.
- Established **recall for ESI 1** (the most critical triage class) as the
  primary clinical metric — not accuracy — because of severe class
  imbalance and the asymmetric clinical cost of under-triage.
- Headline finding: the decision tree correctly flagged **zero of 16**
  truly critical (ESI 1) patients in the test set; logistic regression
  caught 4 of 16 (recall 0.25).
- Deliverables: two executed tutorial notebooks, a two-page final report
  (results, metric justification, failure-mode reflection), and a script
  for a 1-minute clinician-facing Loom video.

| Model | Accuracy | Macro F1 | Recall — ESI 1 |
|---|---|---|---|
| Dummy (stratified guess) | 0.375 | 0.204 | 0.00 |
| Logistic Regression | 0.667 | 0.492 | 0.25 |
| Decision Tree (depth 5) | 0.556 | 0.216 | 0.00 |

## Week 7 — Model Optimisation & Cost-Benefit Analysis

**Interim & final submission completed.**

- Built three more complex model families on top of the Week 6 baselines:
  Random Forest (untuned), Random Forest tuned via `RandomizedSearchCV`,
  Gradient Boosting (`HistGradientBoostingClassifier`), and a small MLP.
- Added engineered clinical features (shock index, pulse pressure, an
  oxygen-to-respiratory-rate ratio, and a "red flag" vitals count).
- Benchmarked all models against the Week 6 baselines on six axes
  (accuracy, precision, recall, F1, training time, inference time) plus a
  seventh, qualitative axis: interpretability.
- Key finding: three model families (tuned Random Forest, Gradient
  Boosting, MLP) converge on the **same** ESI-1 recall (0.31) — but the
  training cost to reach it ranges from 7.7 seconds (Gradient Boosting) to
  1,099 seconds / ~18 minutes (tuned Random Forest).
- **Decision: Gradient Boosting recommended for Phase 3** — same clinical
  benefit as the alternatives, ~140× cheaper to train than the tuned
  Random Forest, and more interpretable than the MLP.
- Deliverables: full benchmark notebook, a 3-page cost-benefit memo (for
  Dr De Freitas, the ED Board, and Martina Griffith), and a decision
  journal entry.

| Model | Accuracy | Macro F1 | Recall — ESI 1 | Train time | Interpretability |
|---|---|---|---|---|---|
| Random Forest | 0.641 | 0.390 | 0.00 | 38.2 s | Medium |
| Random Forest (tuned) | 0.608 | 0.475 | 0.31 | 1,099 s | Medium |
| **Gradient Boosting (winner)** | 0.550 | 0.416 | 0.31 | 7.7 s | Medium-Low |
| Small MLP | 0.638 | 0.498 | 0.31 | 103.1 s | Low |

## Week 8 — Reproducibility & Modular Project Design

**Interim submission completed. Final submission still in progress.**

Goal: refactor the project from notebooks into an audit-ready,
"new-hire-Monday-runnable" codebase, per Martina Griffith's handover
standard.

Completed so far:
- Draft `src/` layout: `data.py` (loading/cleaning), `features.py`
  (clinical feature engineering), `model.py` (model factory,
  training, evaluation), `utils.py` (shared helpers).
- `config.yaml` pinning the Week 7 decision: Gradient Boosting, exact
  hyperparameters, seed 42 — one file drives the whole pipeline.
- `scripts/train.py` — single entry point (`python scripts/train.py
  --config config.yaml`), verified end-to-end against the real dataset,
  reproducing the exact Week 7 numbers.
- `docs/model-selection.md` and `.csv` — full audit-trail comparison
  table across every model tried in Weeks 6–7, winner marked, linked to
  the Week 7 decision journal.
- `docs/HANDOVER.md` — outline/skeleton only so far.
- `requirements.txt` — pinned library versions.

