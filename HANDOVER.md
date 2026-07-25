# Handover Document — OUTLINE (Week 8 Interim Draft)

> Status: skeleton only. Each section below has the heading and a short
> note on what will go there — full prose is due with the Tuesday final
> submission, once tests/ (Task 4) confirm the pipeline actually breaks
> loudly instead of silently.

## 1. Project Summary
*(one paragraph — TODO Tuesday)*
Note to self: cover what the model predicts (ESI level at triage), the
dataset (Yale EMMLC extract via Mercer), and the one-line project
purpose (a defensible, explainable baseline for AI-assisted triage —
not a replacement for clinical judgement).

## 2. Final Model Decision
*(which model won, one sentence why — TODO Tuesday)*
Note to self: Gradient Boosting, pinned in `config.yaml`. One sentence:
matches the best available recall on critical (ESI 1) patients at a
small fraction of the training cost of the alternatives. Link to
`docs/model-selection.md` and `docs/decisions/2026-week-7-model-choice.md`
for the full reasoning — don't re-litigate it here.

## 3. How to Run
*(TODO Tuesday — draft below already works, needs a written walkthrough)*
```bash
pip install -r requirements.txt
python scripts/train.py --config config.yaml
```
Note to self: confirm this is genuinely a clean-machine, 30-minute,
new-hire-Monday experience before calling it done — that's the actual
bar, not just "it runs on my machine."

## 4. Where the Data Lives (and Governance Status)
*(TODO Tuesday)*
Note to self: this needs an honest answer, not a placeholder — where is
`yaleemmlc_admissionprediction_triage.csv` actually stored for Mercer
(not just this repo's `data/` folder), what governance/access approval
covers it, and who owns that approval. Flag to self: do not commit
patient-level data to a public GitHub repo — check `.gitignore` covers
`data/*.csv` before the final submission.

## 5. Known Limitations
*(3 bullets — TODO Tuesday, draft candidates below)*
- Recall for ESI 1 is 0.31 at best across every model tried — roughly
  two in three critical patients are still missed. Not deployable.
- No subgroup fairness audit has been run on any model (carried over
  from the Week 7 memo's Risks & Unknowns — still open).
- Near-miss severity (how far off an under-triage lands, not just
  whether it's wrong) has not been re-checked for any Week 7 model.

---
*Draft outline only — see `docs/model-selection.md` for the metrics
this document will summarise, and `config.yaml` for the pinned model
this document will describe.*
