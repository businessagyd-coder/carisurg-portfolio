# Risk Register — AI-Assisted Triage Validation Pilot
**Project:** AI-Assisted Triage Validation at Mercer General Hospital  
**Author:** Aiden Daniel  
**Programme:** CariSurg MedTech Pathways 2026 · Week 4  
**Prepared for:** Dr. De Freitas & Saint Cedric Ministry of Health  
**Version:** 1.0 (Interim — Saturday Submission)  
**Date:** June 2026  

---

## Purpose

This register documents eight named risks arising from the proposed 12-week AI-assisted triage validation pilot at Mercer General Hospital. It is submitted in response to the Ministry's request for input on a potential nationwide rollout of AI-assisted triage across the public hospital network. Risks are grouped into four categories — AI-Technical, Operational, Ethical, and Equity — and each entry carries a likelihood rating, impact rating, specific mitigation, and a measurable signal of success.

Where no defensible mitigation currently exists, this is stated plainly, in keeping with Dr. De Freitas's direction: *"Do not flinch."*

---

## Risk Register

| # | Risk Name | Category | Likelihood | Impact | Mitigation | Signal of Success |
|---|-----------|----------|------------|--------|------------|-------------------|
| 1 | **Distribution Shift at New Deployment Sites** | AI-Technical | M | H | Re-evaluate model performance against a held-out local validation set at each new hospital before go-live. Retraining triggered if Level 1 recall drops >3 percentage points below Mercer baseline. | Quarterly performance reports per site confirm Level 1 recall within ±3 pp of the Mercer training baseline; no silent degradation across a rollout cycle. |
| 2 | **Overfitting to Single-Site Training Data** | AI-Technical | H | H | Require external validation on data from at least one additional Caribbean ED before nationwide rollout is approved. Current n=2,200 from a single urban site is insufficient for generalisation. No mitigation that avoids multi-site validation is considered defensible at this stage. | External validation cohort achieves Level 1 sensitivity ≥85% (matching Mercer performance) before Ministry approves rollout beyond pilot site. |
| 3 | **Data Leakage via Post-Triage Features** | AI-Technical | M | H | Pre-deployment feature audit conducted by a clinician-engineer pair. Any feature unavailable at the moment the triage nurse first assesses the patient is excluded from the model. Audit documented and signed off before pilot launch. | Signed feature-audit checklist on file; model performance on prospective live data is within ±2 pp of offline validation performance. |
| 4 | **Alert Fatigue Eroding Clinical Adherence** | Operational | H | H | Set alert firing threshold to achieve a positive predictive value ≥70% before go-live. Review alert action rate weekly in the first month and monthly thereafter. If the proportion of alerts triggering a clinical action falls below 60%, the alert threshold is re-calibrated before the following shift. | Weekly alert action rate remains above 60% across all triage shifts throughout the 12-week pilot. |
| 5 | **Clinician Over-Reliance (Automation Bias)** | Operational | M | H | Integrate a mandatory one-sentence prompt on the triage interface requiring the nurse to record their own independent acuity assessment before the model's recommendation is displayed. Override logging is automatic. | Triage nurses demonstrate correct independent override in ≥90% of structured simulation scenarios conducted at the six-week pilot review; override rate in live data remains within the clinically expected range (neither zero nor excessive). |
| 6 | **EHR Integration Failure Leaving Triage Without Decision Support** | Operational | M | M | Document and test a paper-based fallback triage protocol that does not depend on the model. Fallback drill conducted at least once during the 12-week pilot. Staff trained on fallback before go-live. | Fallback protocol drill completed and documented within the first two weeks of the pilot; all triage staff can execute paper-based triage unassisted within the expected time standard. |
| 7 | **Absence of Informed Consent for AI-Assisted Triage** | Ethical | H | H | Draft patient-facing disclosure language (plain English and Creole where applicable) describing that an AI tool contributes to triage prioritisation and that clinical staff retain full decision-making authority. Disclosure reviewed by a patient advocate representative before pilot launch. Right to request human-only triage is documented. | Patient-facing disclosure language signed off by patient advocate group and posted at the triage point before the first patient is seen under the pilot. No complaint of undisclosed AI use recorded during the 12-week pilot. |
| 8 | **Accountability Ambiguity When the Model Causes Harm** | Ethical | M | H | Name a single clinical owner (consultant grade or above) responsible for the model's performance throughout the pilot. A case-review standard operating procedure (SOP) is written and approved before go-live, specifying who reviews adverse events, within what timeframe, and what triggers a model suspension. | Named clinical owner documented in the pilot governance record; case-review SOP exercised in a tabletop drill before pilot launch and available to all triage staff. |
| 9 | **Under-Representation of Elderly and Walk-In Patients in Training Data** | Equity | H | H | Disaggregate model performance by age band (under 18, 18–49, 50–69, 70+) and by arrival method (EMS vs. walk-in) before rollout approval. If sensitivity for any subgroup falls more than 5 percentage points below overall sensitivity, deployment is paused pending retraining or supplementary data collection. | Performance metrics disaggregated by age and arrival method are included in the pilot's six-week and twelve-week review reports; no subgroup gap exceeds 5 pp without a documented response plan. |
| 10 | **Rural Infrastructure Disparity Making Urban Model Non-Transferable** | Equity | H | H | A site readiness checklist (connectivity, hardware, staffing, maintenance capacity) must be completed and approved by the Ministry before each new deployment site is activated. An offline fallback mode is specified in the system design and tested at each site. No deployment to a site that fails the readiness checklist. | Site readiness checklist on file for each activated site; offline fallback tested and documented before each go-live date. No site activated without Ministry sign-off. |

---

## Top Three Risks — Plain Language Summary

The following is a summary of the three risks judged most likely to affect patient safety or programme credibility during the pilot, written for a hospital board or Ministry audience without ML background.

### 1. The model may perform worse than expected at hospitals it was not trained on

The AI was trained on approximately 2,200 patient records from Mercer General Hospital. If it is rolled out to other hospitals — which see different patient populations, different seasonal illness patterns, or different staffing and documentation practices — it may give less accurate triage recommendations without anyone noticing immediately. This is not a hypothetical: it is one of the most consistently documented failure modes in healthcare AI. **The proposed mitigation** is to require that the model is tested locally at each new hospital before patients are exposed to it, and that a clear performance threshold must be met before it is switched on. **The signal that this is working** is a quarterly performance report confirming the model is still performing within an acceptable range at every active site.

### 2. Staff may stop paying attention to alerts if the system fires too often

If the AI flags too many patients as high-acuity, triage nurses will — quite rationally — begin to discount the alerts. This phenomenon is well-documented in clinical settings and is called alert fatigue. The danger is that when the model correctly identifies a genuinely critical patient, the alert is ignored because nurses have learned that most alerts are low-value. **The proposed mitigation** is to calibrate the alert threshold before the pilot opens so that most alerts are clinically meaningful, and to monitor whether staff are acting on alerts each week. If the action rate drops, the threshold is recalibrated. **The signal** is that the proportion of alerts leading to a clinical action stays above 60% throughout the pilot.

### 3. Patients are not told that an AI is involved in their care

Patients presenting to the Mercer Emergency Department during the pilot period would receive a triage classification that is partly informed by an AI model. Under the WHO ethical framework for health AI, patients have the right to know when automated systems contribute to decisions about their care, and the right to request that a human clinician makes the decision independently. At present, no patient-facing disclosure mechanism is in place. **The proposed mitigation** is to create plain-language disclosure notices (in English and in Creole where needed) that are displayed at the triage point and reviewed by a patient advocate before the pilot begins. **The signal** is that the disclosure language has received patient advocate sign-off and that no patient complaint related to undisclosed AI use is received during the 12-week period.

---

## Residual Risk Statement

One risk in this register does not yet have a fully defensible mitigation: **overfitting to single-site training data** (Risk 2). The current dataset originates from a single urban hospital, and no external validation dataset from another Caribbean ED has been collected or agreed upon. Until such a dataset exists and the model has been validated against it, this register cannot confirm that the system is safe for deployment beyond Mercer General Hospital. **The pilot should proceed at Mercer only**, with multi-site external validation as a hard prerequisite for any nationwide rollout recommendation.

---

## References

This register draws on the following sources in its risk formulation:

1. Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. 2019;366(6464):447–453.
2. World Health Organization. *Ethics and governance of artificial intelligence for health: WHO guidance*. Geneva: WHO; 2021.
3. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. *Nat Med*. 2019;25(1):44–56.

Full references for the proposal's expanded literature review are maintained in Zotero and will be included in the Week 4 proposal update.
