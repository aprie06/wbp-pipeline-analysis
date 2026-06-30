"""
WBP_Synthetic_Data_Generator.py — v3
======================================
Rebuilt from real employer/role/campus data, with all institution-identifying
values replaced. Reflects actual top 7 employers, actual top 7 roles, and
actual real role-employer pairings observed in the source data.

Compensation and scheduling parameters:
  - Pay rate: $18.00/hour (flat, no role-based variation — matches real program)
  - Max hours/week: 20
  - Average hours/week: 17
  - Max placement duration: 9 months (270 days)
  - Coverage: Fall 2021 through Summer 2026 (real term range observed)
"""

import random
import numpy as np
import pandas as pd
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

# ── Anonymized campus mapping ────────────────────────────────────────────────
CAMPUSES = ['Campus C', 'Campus NW', 'Campus SP', 'Campus E', 'Campus NE']
CAMPUS_WEIGHTS = [436, 247, 231, 216, 93]  # real relative volumes observed

# ── Top 7 employers (anonymized) with real role distributions ──────────────
# quality tier drives completion-rate behavior; structured = fixed-length program
EMPLOYERS = {
    'Generic ISD': {
        'quality': 'medium', 'type': 'standard',
        'roles': {
            'Information Technology Intern': 0.65,
            'IT Help Desk Intern':           0.10,
            'IT Software Development Intern':0.08,
            'IT Networking Intern':          0.05,
            'IT Hardware Intern':            0.05,
            'Public Service Intern':         0.07,
        }
    },
    'Altus Hospice': {
        'quality': 'high', 'type': 'standard',
        'roles': {
            'Healthcare Intern':             0.90,
            'Nursing Intern':                0.06,
            'Medical Office Clerk Intern':   0.02,
            'Business Development Intern':   0.02,
        }
    },
    'Accenture Federal Services': {
        'quality': 'high', 'type': 'structured',   # 9-week structured program
        'roles': {
            'Apprentice in Training':        0.78,
            'IT Help Desk Intern':           0.10,
            'IT-Apprentice in Training':      0.06,
            'IT Cyber Security Intern':       0.03,
            'Customer Support Network Intern':0.03,
        }
    },
    'SAMSAT': {
        'quality': 'medium', 'type': 'standard',
        'roles': {
            'STEM Intern':                   0.76,
            'Esports Intern':                0.17,
            'Education Intern':              0.05,
            'IT Software Development Intern':0.02,
        }
    },
    'Generic County IT': {
        'quality': 'high', 'type': 'standard',
        'roles': {
            'Information Technology Intern': 0.71,
            'Information Systems Intern':    0.24,
            'Public Service Intern':         0.03,
            'IT Help Desk Intern':           0.02,
        }
    },
    'Somerset Academy': {
        'quality': 'low', 'type': 'standard',
        'roles': {
            'IT Help Desk Intern':           0.81,
            'Information Technology Intern': 0.14,
            'Education Intern':              0.05,
        }
    },
    'Quantum Institute Fellows, Inc': {
        'quality': 'high', 'type': 'structured',   # fixed-length fellowship
        'roles': {
            'Quantum Computing Research Intern': 1.00,
        }
    },
}

EMPLOYER_NAMES   = list(EMPLOYERS.keys())
EMPLOYER_WEIGHTS = [127, 121, 85, 82, 62, 42, 37]  # real relative volumes

# Top 7 roles overall — used for cross-cutting role analysis in the notebook
TOP_7_ROLES = [
    'Healthcare Intern', 'Public Service Intern', 'Information Technology Intern',
    'Business Development Intern', 'Vet Tech Intern', 'IT Help Desk Intern',
    'STEM Intern',
]

# A small pool of additional employers (lower volume, fills out the long tail)
OTHER_EMPLOYERS = {
    'Southwest Voter Registration Education Project': {'quality':'medium','type':'standard',
        'roles': {'Public Service Intern': 0.85, 'Communications Associate Intern': 0.15}},
    'Education Service Center, Region 20': {'quality':'medium','type':'standard',
        'roles': {'Education Intern': 0.6, 'Public Service Intern': 0.4}},
    'San Antonio Botanical Gardens': {'quality':'high','type':'standard',
        'roles': {'Horticulture Intern': 0.9, 'Marketing Intern': 0.1}},
    'San Pedro Playhouse': {'quality':'medium','type':'standard',
        'roles': {'Production Intern': 1.0}},
    'Generic County Justice Services': {'quality':'medium','type':'standard',
        'roles': {'Public Service Intern': 0.7, 'Business Development Intern': 0.3}},
    "Millio's Youth and Outreach Services": {'quality':'low','type':'standard',
        'roles': {'Non-Profit Management Intern': 1.0}},
    'Bario Aviation Services': {'quality':'medium','type':'standard',
        'roles': {'Aviation Intern': 1.0}},
    'Generic County Public Health': {'quality':'high','type':'standard',
        'roles': {'Public Service Intern': 1.0}},
    'Union Pacific Railroad': {'quality':'high','type':'standard',
        'roles': {'Manufacturing Intern': 0.6, 'Business Development Intern': 0.4}},
    'USAA': {'quality':'high','type':'standard',
        'roles': {'Business Development Intern': 0.5, 'IT Cyber Security Intern': 0.3,
                  'Marketing Intern': 0.2}},
    'American Red Cross': {'quality':'high','type':'standard',
        'roles': {'Non-Profit Management Intern': 0.7, 'Public Service Intern': 0.3}},
    'Chak Therapy': {'quality':'medium','type':'standard',
        'roles': {'Healthcare Intern': 0.8, 'Business Development Intern': 0.2}},
    'Generic ISD - North': {'quality':'medium','type':'standard',
        'roles': {'Education Intern': 0.6, 'IT Help Desk Intern': 0.4}},
    'Tekgration LLC': {'quality':'medium','type':'standard',
        'roles': {'IT Software Development Intern': 0.7, 'IT Cyber Security Intern': 0.3}},
}

ALL_EMPLOYERS = {**EMPLOYERS, **OTHER_EMPLOYERS}
ALL_EMP_NAMES = list(ALL_EMPLOYERS.keys())
ALL_EMP_WEIGHTS = EMPLOYER_WEIGHTS + [random.randint(10, 36) for _ in OTHER_EMPLOYERS]

# ── Outcome model ─────────────────────────────────────────────────────────────
REASON_CODES = {
    'Planned Completion': [
        'Internship Term Ended', 'Graduate', 'Hired by Employer',
        'Hired by Non-WBP Employer', 'Offered Role by Employer',
    ],
    'Re-engagement': ['Seeking New WBP Assignment'],
    'Student Exit': [
        'Student Ended Assignment', 'Job Abandonment',
        'Did Not Complete Employer Pre-screen', 'Voluntary Withdrawal',
    ],
    'Employer Exit': ['Employer Ended Assignment'],
    'Administrative Exit': ['Ineligible-Not Enrolled', 'WBP Pause', 'Ineligible for Rehire'],
}

OUTCOME_WEIGHTS = {
    'structured': {'Planned Completion':0.90,'Re-engagement':0.04,'Student Exit':0.03,
                   'Employer Exit':0.02,'Administrative Exit':0.01},
    'high':       {'Planned Completion':0.62,'Re-engagement':0.11,'Student Exit':0.16,
                   'Employer Exit':0.07,'Administrative Exit':0.04},
    'medium':     {'Planned Completion':0.48,'Re-engagement':0.09,'Student Exit':0.27,
                   'Employer Exit':0.10,'Administrative Exit':0.06},
    'low':        {'Planned Completion':0.30,'Re-engagement':0.05,'Student Exit':0.44,
                   'Employer Exit':0.15,'Administrative Exit':0.06},
}

CAMPUS_MODIFIERS = {
    'Campus C':  1.10,   # highest volume, most established
    'Campus NW': 1.04,
    'Campus SP': 0.98,
    'Campus E':  0.92,
    'Campus NE': 0.85,   # lowest volume, newest
}

PAY_RATE = 18.00
MAX_HOURS_WEEK = 20
AVG_HOURS_WEEK = 17
MAX_DURATION_DAYS = 270  # 9 months

TERMS = []
for year in range(2021, 2027):
    for season, (mo, day) in [('Spring',(1,15)), ('Summer',(6,1)), ('Fall',(9,1))]:
        if year == 2026 and season != 'Spring':
            continue  # data runs through present (June 2026)
        TERMS.append((f'{season} {year}', date(year, mo, day)))

def pick_outcome(employer_name, campus):
    info = ALL_EMPLOYERS[employer_name]
    quality = info['quality']
    emp_type = info['type']
    key = 'structured' if emp_type == 'structured' else quality
    w = OUTCOME_WEIGHTS[key].copy()

    mod = CAMPUS_MODIFIERS.get(campus, 1.0)
    completion = min(w['Planned Completion'] * mod, 0.95)
    delta = w['Planned Completion'] - completion
    w['Planned Completion'] = completion
    w['Student Exit'] += delta * 0.7
    w['Employer Exit'] += delta * 0.3

    outcomes = list(w.keys())
    probs = list(w.values())
    total = sum(probs)
    probs = [p/total for p in probs]
    return random.choices(outcomes, weights=probs, k=1)[0]

def tenure_for_outcome(outcome, emp_type):
    if emp_type == 'structured':
        return random.randint(40, 47)  # ~6 weeks (Accenture-style structured program)
    if outcome == 'Planned Completion':
        # Bucket into discrete month-ranges first, THEN pick a day within that
        # bucket. The final bucket's range (270-285) sits entirely AT or ABOVE
        # the 9-month (270-day) threshold, so picking that bucket reliably
        # produces a "reached full term" completion — not a 1-in-30 edge case.
        month_buckets = [
            (30, 60), (60, 90), (90, 120), (120, 150),
            (150, 180), (180, 210), (210, 240), (270, 285),
        ]
        bucket = random.choice(month_buckets)
        return random.randint(bucket[0], bucket[1])
    if outcome == 'Re-engagement':
        return random.randint(75, 240)
    if outcome == 'Student Exit':
        r = random.random()
        if r < 0.50: return random.randint(1, 30)
        elif r < 0.75: return random.randint(31, 60)
        elif r < 0.92: return random.randint(61, 120)
        else: return random.randint(121, 200)
    if outcome == 'Employer Exit':
        return random.randint(14, 150)
    return random.randint(7, 90)  # Administrative

def pick_role(employer_name):
    info = ALL_EMPLOYERS[employer_name]
    roles = list(info['roles'].keys())
    weights = list(info['roles'].values())
    return random.choices(roles, weights=weights, k=1)[0]

def hours_per_week():
    # Centered tightly around 17, capped at 20, floor around 8
    val = np.random.normal(17, 2.2)
    return round(min(max(val, 8), MAX_HOURS_WEEK), 1)


def generate_dataset(n_total=1223):
    placements_rows = []
    ended_rows = []
    ncns_rows = []

    counter = [0]
    def next_id():
        counter[0] += 1
        return f'STU{counter[0]:04d}'

    for _ in range(n_total):
        student_id = next_id()
        campus = random.choices(CAMPUSES, weights=CAMPUS_WEIGHTS, k=1)[0]
        employer = random.choices(ALL_EMP_NAMES, weights=ALL_EMP_WEIGHTS, k=1)[0]
        role = pick_role(employer)
        term_label, term_start = random.choice(TERMS)

        outcome = pick_outcome(employer, campus)
        tenure = tenure_for_outcome(outcome, ALL_EMPLOYERS[employer]['type'])
        start_date = term_start + timedelta(days=random.randint(0, 10))
        end_date = start_date + timedelta(days=tenure)
        reason = random.choice(REASON_CODES[outcome])
        hrs_wk = hours_per_week()
        total_hours = round((tenure / 7) * hrs_wk, 1)
        total_pay = round(total_hours * PAY_RATE, 2)

        placements_rows.append({
            'Student ID':       student_id,
            'College':          campus,
            'Employer':         employer,
            'Title':            role,
            'Placement Term':   term_label,
            'Start Date':       start_date,
            'End Date':         end_date,
            'Hours Per Week':   hrs_wk,
            'Pay Rate':         PAY_RATE,
            'Total Hours':      total_hours,
            'Total Pay':        total_pay,
        })

        ended_rows.append({
            'Student ID':       student_id,
            'Employer':         employer,
            'Title':            role,
            'College':          campus,
            'Start Date':       start_date,
            'End Date':         end_date,
            'Reason for ended assignment': reason,
            'Placement Term':   term_label,
        })

        if outcome == 'Student Exit' and reason == 'Job Abandonment':
            ncns_rows.append({
                'Student ID':     student_id,
                'Employer':       employer,
                'Title':          role,
                'College':        campus,
                'Scheduled Start Date': start_date,
                'Notes':          'No call, no show on scheduled start',
            })

    return {
        'Total Placements':           pd.DataFrame(placements_rows),
        'ARCHIVED-Ended Assignments': pd.DataFrame(ended_rows),
        'PLACED-No Call and No Shows':pd.DataFrame(ncns_rows),
    }


def write_excel(sheets, path):
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
            ws = writer.sheets[name]
            for col in ws.columns:
                max_len = max(
                    len(str(col[0].value)) if col[0].value else 0,
                    *(len(str(c.value)) if c.value else 0 for c in col[1:])
                )
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 42)
    print(f"Written: {path}")


if __name__ == '__main__':
    print("Generating Workforce Bridge Program synthetic dataset (v3 — real-data-driven)...")
    sheets = generate_dataset(n_total=1223)

    print("\nRecord counts:")
    for name, df in sheets.items():
        print(f"  {name:<32} {len(df):>5} rows")

    ended = sheets['ARCHIVED-Ended Assignments']
    reason_map = {}
    for outcome, codes in REASON_CODES.items():
        for c in codes:
            reason_map[c] = outcome
    ended['outcome'] = ended['Reason for ended assignment'].map(reason_map)

    print("\nOutcome distribution:")
    counts = ended['outcome'].value_counts()
    for o, c in counts.items():
        print(f"  {o:<25} {c:>4}  ({c/len(ended)*100:.1f}%)")

    print("\nTop 7 employers in generated data:")
    print(sheets['Total Placements']['Employer'].value_counts().head(7))

    print("\nTop 7 roles in generated data:")
    print(sheets['Total Placements']['Title'].value_counts().head(7))

    print(f"\nAvg hours/week: {sheets['Total Placements']['Hours Per Week'].mean():.1f}")
    print(f"Max hours/week: {sheets['Total Placements']['Hours Per Week'].max():.1f}")
    print(f"Avg total pay per placement: ${sheets['Total Placements']['Total Pay'].mean():,.2f}")

    out_path = '/mnt/user-data/outputs/WBP_Anonymized.xlsx'
    write_excel(sheets, out_path)
