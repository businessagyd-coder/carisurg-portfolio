# Feasibility Memo

## AI-Assisted Triage Validation: Is the Yale EMMLC Dataset Good Enough to Build On?

**Prepared for:** Dr. De Freitas and the Mercer General Hospital ED Board
**Prepared by:** Aiden Daniel, CariSurg MedTech Pathways 2026
**Date:** 7 July 2026

---

## Verdict

**Proceed to baseline modelling, with named caveats.** The dataset (55,121 encounters, 225 features, Yale EMMLC extract) is large, clinically coherent, and internally consistent enough to build a Week 6 baseline model on, but it is a United States, multi-site, non-Caribbean sample with at least one likely data-entry shortcut and a measurable equity pattern in the triage label itself — both of which must be disclosed alongside any model output, not fixed silently.

## Dataset Summary

The dataset covers 55,121 emergency department (ED) encounters across three sites (Site A 63%, Site B 25%, Site C 12%) with 225 candidate features per patient: seven triage vital signs, nine demographic fields, five arrival/administrative fields, two outcome-only fields that must be excluded from modelling to avoid leakage (`disposition`, `previousdispo`), and 200 binary chief-complaint flags. The target is the Emergency Severity Index (ESI), a five-level acuity scale (1 = most urgent) that is the established standard for ED triage.<sup>1</sup>

![Figure 1: ESI class balance and age distribution](media/fig1_esi_age.png)

*Figure 1. ESI class balance is heavily skewed toward the middle acuity bands (ESI 3 = 49%, ESI 2 = 33%); ESI 1 (most urgent) accounts for only 0.1% of encounters. Age is broadly distributed 18–95+, peaking in the 45–65 range.*

Every encounter has a recorded ESI value, so no rows need to be dropped for a missing label — an encouraging starting point for a baseline classifier.

## Top 3 Data-Quality Concerns

### 1. The dataset's "perfect" completeness is itself a quality flag

All 226 columns have zero missing cells across all 55,121 rows. For a raw ED export this is very unusual, and my own check ruled out the simplest explanation (row duplication: 0 exact duplicate rows found). The more likely explanation is upstream imputation or a pre-cleaned research extract, which we cannot yet confirm with the data provider. Compounding this, a follow-up check of value spikes found that respiratory rate (RR) is recorded as exactly 18 for 46.9% of all patients — far beyond what real physiology would produce — and this default-charting pattern is markedly less common in the most urgent patients (28.6% at ESI 1) than in routine ones (47–49% at ESI 2–5). This matches a well-documented EHR phenomenon in which a plausible-looking default is charted instead of a genuine reading, more often for stable patients.<sup>2</sup>

![Figure 2: Value-preference check across vitals](media/fig2_value_preference.png)

*Figure 2. Share of patients recorded at each vital's single most common value. Respiratory rate and oxygen saturation stand out as likely default-charted rather than individually measured for a large share of patients.*

Practical implication: RR should be treated as a lower-confidence feature for Week 6 modelling than its raw correlation with ESI suggests, since a large share of its "signal" may be an artefact of charting habit rather than physiology.

### 2. Feature usability gaps

149 of the 200 chief-complaint flags fire on fewer than 0.5% of patients — too sparse to model reliably and better reserved for descriptive statistics than as individual model inputs. Separately, 9 of the 200 chief-complaint columns are not strictly binary (they contain a stray value such as 2 in a single row each), which the standard "fill blanks with 0" cleaning step does not catch — these need an explicit clip to {0,1} before Week 6. Two impossible-value clusters were also found and should be recoded to missing rather than capped: 4 implausible respiratory-rate readings and 25 implausible glucose readings.

### 3. External validity to a Caribbean ED is unproven

This is a US sample; race, ethnicity, and site mix do not resemble the Mercer General catchment, and none of the three sites are Caribbean. Any model built on this data is a feasibility exercise, not a validated tool for Saint Lucia — a local pilot cohort would be needed before any deployment conversation.

## Top 3 Reasons to Proceed

### 1. Scale and label completeness

55,121 labelled encounters is comfortably enough to train and validate a multiclass baseline, even after dropping the sparse chief-complaint columns, and there are no missing-label rows to discard.

### 2. The label behaves the way a real triage label should

Two independent checks confirm ESI is clinically coherent rather than noise. First, oxygen saturation and several acute chief complaints (chest pain, shortness of breath, suicidality, altered mental status) correlate with higher acuity in the expected direction. Second, arrival mode passes a sanity check I ran independently of the tutorial material: ambulance and wheelchair arrivals have a lower (more urgent) mean ESI than car or walk-in arrivals, exactly as clinical practice would predict.

![Figure 3: Mean ESI by arrival mode](media/fig3_arrivalmode_esi.png)

*Figure 3. Mean ESI by arrival mode — ambulance and wheelchair arrivals are more urgent (lower mean ESI) than self-presenting patients, consistent with expected triage behaviour.*

### 3. Governed access and a clear pilot scope

Data access was secured through the Mercer Research Ethics Committee with an explicit feasibility scope, so the project already sits inside an ethics and oversight structure rather than being an ungoverned experiment.

## Caveats

The most important caveat concerns the label itself, not just the features. ESI assignment differs measurably by race in this dataset: White patients are assigned the most urgent bands (ESI 1–2) roughly 37% of the time versus roughly 29% for Black or African American patients, while Black patients receive the least urgent band (ESI 4) roughly 1.6x as often (20.5% vs 12.8%).

![Figure 4: ESI distribution within each race category](media/fig4_esi_by_race.png)

*Figure 4. ESI distribution within each race category. White patients are over-represented in the most urgent bands relative to Black patients, a pattern that mirrors published triage-equity research.*

This work aligns with a 2023 multicentre study finding that Black and Hispanic ED patients are systematically assigned less-acute ESI scores than White patients for comparable presentations.<sup>3</sup>

This is an association in the raw label, not proof of cause in this dataset alone — site mix, complaint mix, and unmeasured severity could all contribute — but it means a model trained directly on ESI risks learning and reproducing this pattern rather than correcting it. Any Week 6 model must be evaluated for performance by race/ethnicity subgroup, not only in aggregate. Additional caveats: this is a feasibility read, not a validated clinical tool, and no output from this pilot should influence real triage decisions; multi-site pooling should be checked for site effects before treating the sample as homogeneous.

## Top-10 Feature Shortlist

Ranked by clinical intuition and correlation with ESI (Figure 5), with the RR/O2 default-charting risk (Concern 1) factored into ranking — respiratory rate is included but ranked lower than its raw correlation alone would suggest.

![Figure 5: Vitals + ESI correlation matrix](media/fig5_correlation.png)

*Figure 5. Vitals + ESI correlation matrix. Oxygen saturation shows the strongest single-vital association with acuity.*

| # | Feature | Justification |
|---|---------|----------------|
| 1 | **triage_vital_o2** | Strongest vital correlation with ESI (r ≈ 0.18); hypoxia is a primary driver of urgent triage. |
| 2 | **cc_chestpain** | Strongest chief-complaint correlation (r ≈ -0.16); classic high-acuity cardiac/pulmonary presentation. |
| 3 | **cc_shortnessofbreath** | Respiratory distress (r ≈ -0.15); a leading acute-presentation flag. |
| 4 | **cc_suicidal** | Psychiatric emergency that mandates urgent evaluation independent of vital signs. |
| 5 | **cc_alteredmentalstatus** | Broad marker of neurological or metabolic emergency (r ≈ -0.13). |
| 6 | **cc_alcoholintoxication** | Airway and behavioural risk requiring close monitoring (r ≈ -0.14). |
| 7 | **triage_vital_hr** | Tachycardia or bradycardia both flag haemodynamic instability. |
| 8 | **arrivalmode (ambulance flag)** | Independently validated proxy for pre-hospital acuity assessment (Figure 3). |
| 9 | **triage_glucose** | Metabolic derangement (e.g. DKA, hypoglycaemia) is a common urgent-triage driver. |
| 10 | **triage_vital_rr** | Tracks acuity (r ≈ -0.10) but flagged lower-confidence due to the default-charting pattern in Concern 1; keep for Week 6 but interpret with caution. |

## References

[1] N. Gilboy, P. Tanabe, D. Travers, and A. M. Rosenau, *Emergency Severity Index (ESI): A Triage Tool for Emergency Department Care, Version 4, Implementation Handbook, 2012 Edition*. Rockville, MD: Agency for Healthcare Research and Quality, AHRQ Publication No. 12-0014, 2011.

[2] N. Jackson, J. Woods, P. Watkinson, A. Brent, T. E. A. Peto, A. S. Walker, and D. W. Eyre, "The quality of vital signs measurements and value preferences in electronic medical records varies by hospital, specialty, and patient demographics," *Sci. Rep.*, vol. 13, p. 3858, 2023.

[3] J. W. Joseph, M. Kennedy, A. M. Landry, R. H. Marsh, D. E. Baymon, D. E. Im, P. C. Chen, M. E. Samuels-Kalow, L. M. Nentwich, N. Elhadad, and L. D. Sánchez, "Race and ethnicity and primary language in emergency department triage," *JAMA Netw. Open*, vol. 6, no. 10, p. e2337557, 2023.
