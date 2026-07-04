# Feasibility Memo — Outline (Interim Draft)
**AI-Assisted Triage Validation in a Caribbean Emergency Department: A 12-Week Pilot at Mercer General Hospital**
Prepared for: ED Board · Supervisor: Dr. De Freitas
Author: Aiden Daniel · CariSurg MedTech Pathways 2026 · Week 5

---

## (a) One-sentence verdict
**Proceed to baseline modelling, with named caveats** — the dataset is large (55,121 encounters, 225 features) and clinically coherent, but it is a US, single-country, multi-site sample with no missing data (a signal that needs explaining before we trust it), and several features cannot be used as-is.

## (b) Dataset summary
- 55,121 ED encounters, 226 raw columns (225 features + target `esi`).
- Target: `esi` (Emergency Severity Index, 1=most urgent … 5=least urgent), fully populated — no rows lack a triage label.
- Feature families: 7 vital signs, 9 demographic fields, 5 admin/arrival fields, 2 outcome-only (leakage) fields, and 200 binary chief-complaint flags.
- Sourced from 3 EDs (Site A ≈ 63%, Site B ≈ 25%, Site C ≈ 12% of encounters) — not single-site.
- Class balance: ESI 3 (49%) and 2 (33%) dominate; ESI 1 (most urgent) is rare (0.1%, 77 patients).

## (c) Top 3 quality concerns
1. **Zero missing values across all 226 columns.** For a raw ED export this is very unusual and suggests upstream imputation or a pre-cleaned extract — we cannot yet tell which values are "real" vs filled in. *Action: confirm provenance with the data provider before Week 6 modelling.*
2. **External validity.** This is a US, non-Caribbean sample with a race/ethnicity mix (majority White/Black, ~18% Hispanic/Latino) that does not resemble Saint Lucia or the Mercer General catchment. A model that performs well here may not transfer.
3. **Feature usability gaps.** 149 of 200 chief-complaint flags fire on fewer than 0.5% of patients (too sparse to model reliably); 2 fields (`disposition`, `previousdispo`) are outcome-only and must be excluded to avoid leakage; a handful of vitals contain clinically impossible values (e.g. 4 implausible respiratory rates, 25 implausible glucose readings) that need recoding, not deletion.

## (d) Top 3 reasons to proceed
1. **Scale.** 55k labelled encounters is more than enough to train and validate a baseline multiclass model, even after dropping sparse features.
2. **Clinical coherence.** Vitals and chief complaints move with acuity in the expected direction (e.g. low oxygen saturation, chest pain, altered mental status, and suicidality all associate with more urgent ESI levels) — a basic sanity check that the labels and features are internally consistent.
3. **Governed access.** Data access came through the Mercer Research Ethics Committee with a clear pilot scope, so the project already has an ethics and oversight structure in place.

## (e) Caveats
- Findings and any future model are **not yet validated for a Caribbean population** — recommend a local pilot cohort for external validation before deployment.
- The apparent "completeness" of the data must be clarified before Week 6; if it reflects hidden imputation, our own median-fill strategy may compound an already-adjusted dataset.
- Multi-site pooling should be checked for site effects (does ESI assignment differ by site?) before treating the data as one homogeneous cohort.
- This is a feasibility read, not a validated clinical tool — no output from this pilot should influence real triage decisions.

---

## Supporting figures (see `/docs/figs/` and `/notebooks/figs/`)
1. `01_missingness.png` — missingness map (structured columns; confirms the zero-missing finding)
2. `02_esi_age.png` — ESI class balance + age distribution
3. `03_demographics.png` — race and ethnicity distribution (equity lens)
4. `04_chief_complaints.png` — top 15 chief complaints by frequency
5. `05_vitals_by_esi.png` — vitals by ESI level (box plots)
6. `06_correlation.png` — vitals + ESI correlation heatmap

## Draft top-10 feature shortlist (to finalise for final submission)
Ranked by clinical intuition + observed correlation with `esi`:
1. `triage_vital_o2` (oxygen saturation) — strongest vital correlation (r ≈ 0.18); hypoxia is a core acuity driver.
2. `cc_chestpain` — strongest complaint correlation (r ≈ -0.16); classic high-acuity presentation (cardiac/pulmonary risk).
3. `cc_shortnessofbreath` — respiratory distress, r ≈ -0.15.
4. `cc_suicidal` — psychiatric emergency, mandates urgent evaluation regardless of vitals.
5. `cc_alcoholintoxication` — airway/behavioural risk, r ≈ -0.14.
6. `cc_alteredmentalstatus` — broad marker of neurological/metabolic emergency, r ≈ -0.13.
7. `triage_vital_hr` (heart rate) — tachycardia/bradycardia both flag instability.
8. `triage_vital_rr` (respiratory rate) — abnormal rates track acuity, r ≈ -0.10.
9. `cc_psychiatricevaluation` — resourcing/urgency marker, r ≈ -0.10.
10. `triage_glucose` — metabolic derangement (DKA/hypoglycemia) drives urgent triage.

*(Each item still needs its one-sentence clinical justification written out in full prose for the final memo — draft above.)*
