# Workforce Bridge Program — Intern Pipeline Analysis

**People analytics project built on synthetic, BLS/EEOC-modeled public data.**  
A full-stack workforce analysis covering pipeline attrition, employer quality scoring, cost modeling, volume trends, concentration risk, early exit prediction, and fiscal year budget reconstruction.

---

## Project Overview

This project analyzes a simulated intern placement pipeline across five campuses and multiple employer partners spanning Spring 2022 through Summer 2026 (~1,223 placements). All data is synthetic and modeled after publicly available BLS and EEOC distributions. No real student, employer, or institutional data is used.

**Analytical sections:**

| Part | Focus |
|---|---|
| 1 | Outcome classification and pipeline funnel |
| 1B | Full-term (9-month) completion rate analysis |
| 2 | Employer quality scoring (composite, 0–100) |
| 3 | Cost per completed placement by employer |
| 4 | Term-to-term volume trend with rolling average |
| 5 | Role concentration risk (HHI-style index) |
| 6 | Early exit prediction model (3 ML classifiers) |
| 6B | Fiscal year budget reconstruction |
| 7 | Policy recommendations |
| 8 | Deep-dive on high-volume employer partners |

---

## Key Findings

- **Employer quality score** correlates with planned completion rate at Pearson r = 0.968
- **Early exit prediction** best AUC: 0.590 across Logistic Regression, Random Forest, and Gradient Boosting (5-fold stratified CV) — interpretable baseline, not production-grade
- **At-risk threshold:** employer partners with > 30% student exit rate are flagged for review
- **HHI concentration:** role-employer pairings scored as LOW (< 1,500), MODERATE (1,500–2,500), or HIGH (> 2,500)
- **Cost model** uses $18.00/hour flat rate, 17 avg hours/week, 270-day max placement duration, plus $75k coordinator overhead and 8% admin load

---

## Figures Generated

The notebook produces 11 figures saved to the working directory:

| File | Description |
|---|---|
| `fig1_outcome_distribution.png` | Overall outcome distribution |
| `fig2_exit_timing.png` | Attrition timing histogram + CDF |
| `fig3_outcome_by_campus.png` | Completion rate by campus (stacked bar) |
| `fig3b_full_term_completion.png` | Full-term completion distribution |
| `fig3c_full_term_by_employer.png` | Full-term rate by employer |
| `fig4_employer_quality.png` | Employer quality scores |
| `fig5_cost_per_completion.png` | Cost per completion by employer |
| `fig6_term_volume_trend.png` | Term-to-term volume trend |
| `fig7_top_roles.png` | Top 7 roles by placement volume |
| `fig8_role_concentration.png` | Role concentration index |
| `fig10_fiscal_year_budget.png` | Fiscal year budget requirement |

---

## Data

The notebook reads from a local Excel file (`WBP_Anonymized.xlsx`) with three sheets:

- `Total Placements`
- `ARCHIVED-Ended Assignments`
- `PLACED-No Call and No Shows`

This file is **not included in the repository** — it is synthetic data stored separately. To run the notebook, mount your Google Drive and place the file at:

```
/content/drive/MyDrive/workforce_bridge/WBP_Anonymized.xlsx
```

---

## Tech Stack

| Tool | Use |
|---|---|
| Python 3.10 | Core language |
| pandas / numpy | Data manipulation |
| matplotlib / seaborn | Visualization |
| scikit-learn | ML models (Logistic Regression, Random Forest, Gradient Boosting) |
| scipy | Pearson and point-biserial correlations |
| openpyxl | Excel file parsing |
| Google Colab | Notebook runtime |
| Google Drive | Data file mount |

---

## Setup

```bash
pip install -r requirements.txt
```

Then open `WBP_Pipeline_Analysis.ipynb` in Google Colab or Jupyter and mount your Drive when prompted.

---

## Employer Quality Score

The composite quality score (0–100) is weighted as:

- **50%** — completion rate
- **30%** — retention rate
- **20%** — re-engagement rate

Only employer partners with 5 or more placements are included in scoring.

---

## Early Exit Prediction Model

- **Target:** `early_exit` = 1 if student exited within 60 days
- **Features:** campus (label-encoded), employer quality tier, season, hours
- **Evaluation:** 5-fold stratified cross-validation, ROC-AUC
- **Note:** AUC results reflect limited feature availability in a synthetic dataset. This section demonstrates methodology, not a deployable model.

---

## Notes

- All employer names are anonymized (e.g., "Generic County IT", "Generic County Public Health")
- Structured placement programs (Accenture Federal Services, Quantum Institute Fellows, Inc) are excluded from attrition timing analysis due to known program design differences
- All metrics are computed from synthetic data and should not be interpreted as real institutional outcomes

---

## Author

Alexis Prieto  
MS Computer Science — Texas A&M University San Antonio (December 2025)  
SHRM-CP | People Analytics | HR Systems and Automation
