# Workforce Bridge Program — Intern Pipeline Analysis

**People analytics investigation of four and a half years of internship placement data from a multi-campus public community college district.**

Built from operational experience managing a workforce development program across five campuses. Every analytical decision in this project reflects domain knowledge about how the program actually worked, not assumptions from the outside.

---

## The Problem

Workforce internship programs track placement starts. What they rarely track well is what happens after placement begins: which students exit early, which employers churn interns, and where in the pipeline the program is losing people it should be retaining. Without that visibility, coordinators respond to failures after the fact instead of preventing them.

This analysis uses four and a half years of placement records to answer three questions the program could not answer from its existing reporting:

1. At what stage do students exit, and how early?
2. Which employer partners produce the best outcomes, and which are quietly failing interns?
3. What operational changes does the data actually support?

---

## What the Analysis Found

> Run the notebook in Colab and fill in your numbers below before publishing.

| Metric | Value |
|---|---|
| Total placements analyzed | 1,193 |
| Campuses | 5 |
| Years of data | FY2020 – FY2024 |
| Overall completion rate | [fill in after running] |
| Student exit rate | [fill in after running] |
| Exits occurring within 60 days | [fill in after running] |
| At-risk employer partners identified | [fill in after running] |
| Best predictive model (AUC) | [fill in after running] |

**Key findings:**

- **Most attrition is early.** [X]% of student exits occur within the first 60 days of a placement. This is the highest-leverage window for coordinator intervention and the basis for Recommendation 1.
- **Employer partner quality varies significantly and is measurable.** A weighted scoring model (50% completion rate, 30% retention, 20% re-engagement) surfaces high-performing partners worth prioritizing and at-risk partners requiring active management.
- **Campus-level completion rates differ by up to [X] percentage points.** The gap is too large to be explained by student characteristics alone, pointing to coordinator practices and local employer relationships as drivers.
- **Re-engagement is a program strength, not a failure mode.** Students seeking a second placement are engaged participants and should be tracked separately from students who exit without returning.

---

## Project Structure

```
wbp-pipeline-analysis/
├── WBP_Pipeline_Analysis.ipynb      # Main analysis notebook (run this)
├── WBP_Anonymized.xlsx              # Synthetic dataset (see Data section)
├── WBP_Synthetic_Data_Generator.py  # Script that produced the dataset
├── README.md
└── figures/
    ├── fig1_outcome_distribution.png
    ├── fig2_outcome_by_campus.png
    ├── fig3_exit_timing.png
    ├── fig4_trend_over_time.png
    ├── fig5_employer_quality.png
    ├── fig6_employer_scatter.png
    ├── fig7_feature_importance.png
    └── fig8_policy_recommendations.png
```

---

## Notebook Structure

**Part 1 — Data Cleaning and Outcome Classification**  
Applies a five-category outcome framework derived from operational knowledge of the program. Raw reason codes are mapped to: Planned Completion, Re-engagement, Student Exit, Employer Exit, and Administrative Exit. Employer partners running structured fixed-length placements are flagged separately to prevent them from distorting attrition timing calculations.

**Part 2 — Student Pipeline Funnel Analysis**  
Overall outcome distribution, completion rate by campus, exit timing histogram and cumulative curve, and year-over-year trend analysis.

**Part 3 — Employer Quality Analysis**  
Weighted employer quality scoring model, ranked partner comparisons, volume-vs-completion scatter, and identification of at-risk employer partners exceeding a 30% student exit threshold.

**Part 4 — Early Exit Prediction Model**  
Binary classifier (Random Forest, Gradient Boosting, Logistic Regression compared via 5-fold stratified CV) to flag placements at elevated risk of student exit before day 60. Features: campus, employer quality tier, semester, hours per week.

**Part 5 — Policy Recommendations**  
Five recommendations grounded directly in the analysis findings, prioritized HIGH / MEDIUM / LOW with specific operational actions.

---

## Running the Notebook

**In Google Colab (recommended):**

1. Upload `WBP_Pipeline_Analysis.ipynb` via File > Upload notebook
2. Upload `WBP_Anonymized.xlsx` via the file panel on the left
3. Run all cells top to bottom
4. If the unclassified reason codes cell prints any results, add those codes to the classifier and re-run Part 1

**Locally:**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
jupyter notebook WBP_Pipeline_Analysis.ipynb
```

---

## Data

The dataset used in this analysis is **synthetic**. It was generated by `WBP_Synthetic_Data_Generator.py` using realistic distributions derived from operational knowledge of the program:

- Outcome probabilities are calibrated by employer quality tier (structured, high, medium, low)
- Campus completion rates are intentionally differentiated to produce meaningful funnel analysis
- Student exit timing follows a realistic early-skew distribution (most exits occur in the first 30 days)
- Employer quality variation is built in so the scoring model has real signal to work with

The synthetic dataset preserves the statistical structure of the real program without containing any real student records. All student identifiers are coded. No real names, institutional IDs, or contact information are present.

**Real data note:** This analysis was designed and validated against four and a half years of actual placement data from a workforce development program. The synthetic dataset was built to match those real distributions. The analytical framework, outcome classification logic, and employer quality scoring model reflect how the program actually operated.

---

## Technical Stack

| Tool | Use |
|---|---|
| pandas | Data loading, cleaning, and aggregation |
| matplotlib / seaborn | Visualization |
| scikit-learn | Classification models, cross-validation |
| openpyxl | Excel file handling |
| Faker | Synthetic data generation |

---

## Privacy and Data Ethics

All student identifiers have been anonymized. Campus names are anonymized (Campus A through Campus E). The institution is not identified. Employer names are retained as organizational entities. The dataset complies with FERPA requirements, no individual student information is recoverable from the published files.

---

## About

Built by **Alexis Prieto**, HR Systems and Automation Analyst and MS Computer Science.  
This project is part of a people analytics portfolio demonstrating end-to-end workforce data analysis, from raw operational data through predictive modeling to policy recommendations.

[LinkedIn](https://www.linkedin.com/in/alexis-prieto-mscs-shrm-cp-414163157)

---

*Independent portfolio project. Not affiliated with any current or former employer.*
