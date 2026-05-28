# carisurg-portfolio
Week 0 · 
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
