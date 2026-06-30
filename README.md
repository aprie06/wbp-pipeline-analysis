# Workforce Bridge Program — Intern Pipeline Analysis

**People analytics investigation of internship placement data from a multi-campus public community college district, covering Spring 2022 through present (2026).**

Built from operational experience managing a workforce development program across five campuses. Every analytical decision in this project — the outcome classification framework, the structured-program handling, the full-term completion benchmark, the cost modeling, the fiscal-year budget reconstruction, and the deep-dive analyses below — reflects domain knowledge about how the program actually worked, not assumptions from the outside.

---

## The Problem

Workforce internship programs track placement starts well. What they rarely track is what happens after: which students exit early, which employer partnerships are expensive relative to what they produce, how dependent the pipeline is on a handful of partnerships, whether students who "complete" are going the full distance or stopping early, whether placement volume is trending or just noisy, what it actually costs per fiscal year to fully fund the program, and whether the program's own internal scoring of employer quality actually holds up statistically.

This analysis answers eight questions the program's standard reporting could not:

1. At what stage do students exit, and how early?
2. Of students who complete, how many reach the full 9-month placement length versus completing early?
3. Which employer partners produce the best outcomes — and at what cost?
4. What does a successful placement actually cost, by employer?
5. Is placement volume growing, shrinking, or seasonal?
6. How dependent is the pipeline on a small number of employer-role pairings?
7. What would the fiscal-year budget have needed to be to fully fund every placement actually attempted?
8. Does the quality scoring model actually measure something real, and how does a specific high-volume employer segment (Generic County) compare to the program overall?

---

## What the Analysis Found

| Metric | Value |
|---|---|
| Total placements analyzed | 1,223 |
| Campuses | 5 |
| Coverage | Spring 2022 – Summer 2026 |
| Pay structure | $18.00/hour flat rate, avg 17 hrs/week, max 20 hrs/week |
| Placement length | Up to 9 months (structured employer programs run ~6 weeks) |
| Overall completion rate | 55.2% |
| Exits occurring within 30 days | 45.7% of all student exits |
| Exits occurring within 60 days | 70.3% of all student exits |
| **Completions reaching the full 9-month term** | **14.6%** of non-structured completions |
| Campus completion rate gap | 15.5 percentage points (Campus C: 60.4% vs. Campus NE: 44.9%) |
| At-risk employer partners (>30% exit rate) | 5 |
| Cheapest completion (cost per placement) | $2,177 (Quantum Institute Fellows, Inc) |
| Most expensive completion | $17,461 (Millio's Youth and Outreach Services) |
| Program-wide blended cost per completion | $8,599 |
| Pipeline concentration index (HHI-style) | 514 — low risk, well diversified |
| Early-exit prediction model (best, 5-fold CV ROC-AUC) | 0.590 — Logistic Regression |
| **5-year average fiscal-year budget required** | **$1,210,694** (intern wages: $1,051,569 + estimated overhead) |
| **Quality score correlation with completion rate** | **r = 0.968** (p < 0.001) — statistically strong validation |
| **Generic County segment (130 placements)** | 76.9% of exits within 60 days vs. 70.3% program-wide |

**Key findings:**

- **Most attrition is early.** 70.3% of student exits happen within 60 days of placement start, and nearly half (45.7%) happen within just 30 days. This is the highest-leverage window for coordinator intervention.
- **Completion and full-term retention are different things.** 55.2% of placements end in Planned Completion, but only 14.6% of those completions actually reach the full 9-month mark — the majority of "successful" placements end well before the maximum term.
- **Employer partner quality and cost are not the same thing.** A partner can have a reasonable completion rate while still costing far more per successful outcome than alternatives. The gap between the most and least efficient partner is roughly 8x ($2,177 vs. $17,461 per completion).
- **The quality scoring model is statistically validated, not arbitrary.** The Pearson correlation between employer quality score and Planned Completion rate is 0.968 (p < 0.001), and the correlation with Student Exit rate is -0.935 (p < 0.001). This confirms the weighted scoring formula in Part 2 is actually measuring a coherent underlying signal, not producing noise dressed up as a metric.
- **Campus-level completion rates differ by 15.5 points.** This is a meaningful gap — large enough to justify investigating coordinator practices, local employer relationships, and intake processes at the lower-performing campuses.
- **The pipeline is well diversified, not fragile.** A concentration index of 514 (employer-role pairing HHI) indicates the program is not structurally dependent on a small number of partnerships, despite five at-risk partners requiring active management.
- **A focused segment (Generic County employers) shows a more acute early-attrition pattern than the program overall** — 76.9% of exits at these three related employers happen within 60 days, compared to 70.3% program-wide. The most common reason for exit at the lowest-performing of the high-risk employers was failure to complete the employer's own pre-screen process, not voluntary withdrawal — a distinction with direct implications for whether the intervention belongs at the program level or the employer's intake process.
- **The early-exit prediction model is honestly modest (AUC 0.590).** Campus, employer quality tier, season, and hours-per-week are real but imperfect predictors of early exit, reported here at face value rather than overstated.
- **Fiscal-year budget requirements declined roughly 21% over five years** — from $1,324,842 in FY2022 to $1,066,188 in FY2026 — tracking with the declining placement volume identified in the term-trend analysis.

---

## Project Structure

```
wbp-pipeline-analysis/
├── README.md
├── WBP_Pipeline_Analysis.ipynb      # Main analysis notebook
├── WBP_Anonymized.xlsx              # Dataset (see Data section)
├── WBP_Synthetic_Data_Generator.py  # Script that produced the dataset
└── figures/
    └── (generated when the notebook is run)
```

---

## Notebook Structure

**Part 1 — Outcome Classification & Pipeline Funnel**
Five-category outcome framework: Planned Completion, Re-engagement, Student Exit, Employer Exit, Administrative Exit. Structured fixed-length placements (~6-week programs) are flagged separately.

**Part 1B — Full-Term Completion Rate (9-Month Benchmark)**
Of students who reach Planned Completion, how many actually go the full 9 months versus completing earlier? Includes a by-employer breakdown of full-term retention.

**Part 2 — Employer Quality Analysis**
Weighted scoring model (50% completion, 30% retention, 20% re-engagement). Identifies at-risk partners exceeding a 30% student exit rate.

**Part 3 — Cost Per Completed Placement**
Total wages paid divided by completions, per employer — the dollar-denominated companion to the quality score.

**Part 4 — Term-to-Term Volume Trend**
Placement volume by term with a 3-term rolling average and seasonal averaging.

**Part 5 — Role Concentration Risk**
Top roles and top employer-role pairings, plus a Herfindahl-Hirschman-style concentration index.

**Part 6 — Early Exit Prediction Model**
Binary classifier comparison (Logistic Regression, Random Forest, Gradient Boosting) via 5-fold stratified CV.

**Part 6B — Fiscal Year Budget Requirement**
Retroactive calculation of what the program's budget would have needed to be each fiscal year (Sept 1 – Aug 31) to fully fund every placement actually attempted. Wages are allocated proportionally by calendar day across fiscal year boundaries and reconcile exactly to the source data.

**Part 7 — Policy Recommendations**
Six recommendations tied directly to specific findings, prioritized HIGH / MEDIUM / LOW.

**Part 8 — Deep-Dive Analyses**
- **Generic County employer segment analysis:** Isolates three related employers (Generic County IT, Generic County Public Health, Generic County Justice Services) and compares their outcome distribution, attrition timing, quality scores, and cost-per-completion against program-wide averages.
- **High-risk employer exit-reason breakdown:** For the three lowest-performing employer partners, breaks down *why* students exited (pre-screen failure vs. voluntary withdrawal vs. job abandonment vs. coordinator-initiated end), since these point to different root causes and different fixes.
- **Tenure-by-outcome analysis at high-risk employers:** Compares typical placement duration across outcome categories specifically at the flagged employers.
- **IT vs. non-IT role analysis:** Separates IT-related placements (Information Technology Intern, IT Help Desk Intern, etc.) from all other roles to identify the top employer-role pairings within each category.
- **Quality score statistical validation:** Pearson correlation testing confirms the Part 2 quality scoring model is significantly correlated with both completion rate (r = 0.968) and (inversely) exit rate (r = -0.935), establishing the metric isn't arbitrary.
- **ISD-specific quality and cost comparison:** Isolates school-district employers for a focused quality-versus-cost view.

---

## Running the Notebook

**In Google Colab (recommended):**

1. Upload `WBP_Pipeline_Analysis.ipynb` via File > Upload notebook
2. Upload `WBP_Anonymized.xlsx` via the file panel on the left, in the **same directory** the notebook expects (the notebook reads `WBP_Anonymized.xlsx` directly — if you store it elsewhere, e.g. Google Drive, update the `FILE` variable in the data-loading cell accordingly)
3. Run all cells top to bottom — verified to execute cleanly with no errors

**Locally:**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy openpyxl
jupyter notebook WBP_Pipeline_Analysis.ipynb
```

**To regenerate the dataset from scratch:**

```bash
pip install pandas numpy openpyxl
python WBP_Synthetic_Data_Generator.py
```

---

## Data

The dataset used in this analysis is **synthetic, built to mirror the real structure of the program**: real top-7 employer partners (anonymized), real employer-role pairings, real campus volume distribution, and real compensation parameters ($18/hour, 17hr average week, 20hr max, 9-month max placement length, ~6-week structured programs). Outcome probabilities, exit timing, and cost figures are modeled, not copied from real records.

`WBP_Synthetic_Data_Generator.py` documents exactly how every value was constructed. Nothing in the dataset is a black box; the generation logic is fully inspectable.

All student identifiers are coded (e.g. `STU0001`). Employer names that would identify the specific institution, county, or city have been replaced with generic equivalents (e.g. "Generic ISD," "Generic County IT"). National organizations and ambiguous acronyms are retained as-is. Campus names are anonymized. The institution itself is not identified.

**A note on the fiscal-year budget figures:** the intern wage allocation is exact — every dollar in the dataset's `Total Pay` column is accounted for and the calculation reconciles to the cent. The coordinator overhead ($75,000/year) and admin/misc overhead (8% of wage spend) are explicitly labeled placeholder estimates, not measured figures.

---

## Technical Stack

| Tool | Use |
|---|---|
| pandas | Data loading, cleaning, aggregation, fiscal-year day-allocation logic |
| matplotlib / seaborn | Visualization |
| scikit-learn | Classification models, cross-validation |
| scipy | Statistical correlation testing (Pearson) |
| openpyxl | Excel file handling |
| NumPy | Synthetic data generation, statistical distributions |

---

## Privacy and Data Ethics

All student identifiers are anonymized. Campus names are anonymized. The institution is not identified. Employer names identifying the specific county or city have been generalized. The dataset complies with FERPA requirements — no individual student information is recoverable from the published files.

---

## About

Built by **Alexis Prieto**, HR Systems and Automation Analyst, MS Computer Science.
Part of a people analytics portfolio demonstrating end-to-end workforce data analysis — from a parameterized synthetic data model through predictive modeling to dollar-denominated policy and budget recommendations, validated with formal statistical testing.

[LinkedIn](https://www.linkedin.com/in/alexis-prieto-mscs-shrm-cp-414163157)

---

*Independent portfolio project. Not affiliated with any current or former employer.*
