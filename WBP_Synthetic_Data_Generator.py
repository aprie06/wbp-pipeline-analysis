"""
WBP_Synthetic_Data_Generator.py
================================
Generates a realistic synthetic dataset for the Workforce Bridge Program
portfolio analysis. Produces WBP_Anonymized.xlsx with six sheets matching
the real program structure.

Run this in Google Colab or locally:
    python WBP_Synthetic_Data_Generator.py

Output: WBP_Anonymized.xlsx (same directory)
"""

import random
import numpy as np
import pandas as pd
from datetime import date, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ── Constants ──────────────────────────────────────────────────────────────────

CAMPUSES = ['Campus A', 'Campus B', 'Campus C', 'Campus D', 'Campus E']

# Employer pool — mix of structured, high-quality, medium, and at-risk
EMPLOYERS = {
    'Accenture':                    {'type': 'structured',  'quality': 'high'},
    'CPS Energy':                   {'type': 'standard',    'quality': 'high'},
    'H-E-B':                        {'type': 'standard',    'quality': 'high'},
    'Methodist Healthcare':         {'type': 'standard',    'quality': 'high'},
    'USAA':                         {'type': 'standard',    'quality': 'high'},
    'Valero Energy':                {'type': 'standard',    'quality': 'high'},
    'City of San Antonio':          {'type': 'standard',    'quality': 'high'},
    'Rackspace Technology':         {'type': 'standard',    'quality': 'medium'},
    'Broadway Bank':                {'type': 'standard',    'quality': 'medium'},
    'iCode':                        {'type': 'standard',    'quality': 'medium'},
    'Security Service FCU':         {'type': 'standard',    'quality': 'medium'},
    'Geekdom':                      {'type': 'standard',    'quality': 'medium'},
    'MIMS Institute':               {'type': 'structured',  'quality': 'high'},
    'Frost Bank':                   {'type': 'standard',    'quality': 'medium'},
    'Bexar County':                 {'type': 'standard',    'quality': 'medium'},
    'Texas A&M San Antonio':        {'type': 'standard',    'quality': 'medium'},
    'Kforce Staffing':              {'type': 'standard',    'quality': 'low'},
    'TechServ Solutions':           {'type': 'standard',    'quality': 'low'},
    'QuickHire Temps':              {'type': 'standard',    'quality': 'low'},
    'Metro Workforce Partners':     {'type': 'standard',    'quality': 'low'},
}

MAJORS = [
    'Business Administration', 'Computer Information Systems',
    'Healthcare Administration', 'Accounting', 'Early Childhood Education',
    'Criminal Justice', 'Information Technology', 'Marketing',
    'Human Resources Management', 'Logistics & Supply Chain',
    'Cybersecurity', 'Medical Billing & Coding',
]

ACADEMIC_YEARS = ['2019-2020', '2020-2021', '2021-2022', '2022-2023', '2023-2024']
SEMESTERS = ['Fall', 'Spring', 'Summer']

REASON_CODES = {
    'Planned Completion': [
        'Internship Term Ended',
        'Graduate',
        'Hired by Employer',
        'Hired by Non-WBP Employer Permanently',
    ],
    'Re-engagement': [
        'Seeking New WBP Assignment',
    ],
    'Student Exit': [
        'Voluntary Withdrawal',
        'Student Ended Assignment',
        'No Call No Show',
        'Did Not Complete Employer Pre-screen',
    ],
    'Employer Exit': [
        'Employer Ended Assignment',
    ],
    'Administrative Exit': [
        'Ineligible-Not Enrolled',
        'WBP Pause',
    ],
}

# Outcome probability weights by employer quality
OUTCOME_WEIGHTS = {
    'structured': {
        'Planned Completion': 0.92,
        'Re-engagement':      0.04,
        'Student Exit':       0.02,
        'Employer Exit':      0.01,
        'Administrative Exit':0.01,
    },
    'high': {
        'Planned Completion': 0.68,
        'Re-engagement':      0.12,
        'Student Exit':       0.10,
        'Employer Exit':      0.06,
        'Administrative Exit':0.04,
    },
    'medium': {
        'Planned Completion': 0.52,
        'Re-engagement':      0.10,
        'Student Exit':       0.24,
        'Employer Exit':      0.09,
        'Administrative Exit':0.05,
    },
    'low': {
        'Planned Completion': 0.34,
        'Re-engagement':      0.06,
        'Student Exit':       0.42,
        'Employer Exit':      0.13,
        'Administrative Exit':0.05,
    },
}

# Campus completion rate modifiers (multiplied against employer weight)
CAMPUS_MODIFIERS = {
    'Campus A': 1.15,
    'Campus B': 1.05,
    'Campus C': 0.98,
    'Campus D': 0.90,
    'Campus E': 0.82,
}

# ── Helper functions ───────────────────────────────────────────────────────────

def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))

def fy_date_range(academic_year: str, semester: str):
    year = int(academic_year.split('-')[0])
    ranges = {
        'Fall':   (date(year,      9,  1), date(year,     12, 15)),
        'Spring': (date(year + 1,  1, 15), date(year + 1,  5, 15)),
        'Summer': (date(year + 1,  6,  1), date(year + 1,  8, 15)),
    }
    return ranges[semester]

def pick_outcome(employer_name: str, campus: str) -> str:
    emp_info = EMPLOYERS[employer_name]
    emp_type = emp_info['type']
    quality  = emp_info['quality']

    key = 'structured' if emp_type == 'structured' else quality
    weights_dict = OUTCOME_WEIGHTS[key].copy()

    # Apply campus modifier to completion rate
    mod = CAMPUS_MODIFIERS.get(campus, 1.0)
    completion = weights_dict['Planned Completion'] * mod
    completion = min(completion, 0.95)

    # Redistribute delta proportionally to exits
    delta = weights_dict['Planned Completion'] - completion
    weights_dict['Planned Completion'] = completion
    weights_dict['Student Exit'] += delta * 0.7
    weights_dict['Employer Exit'] += delta * 0.3

    outcomes = list(weights_dict.keys())
    probs    = list(weights_dict.values())
    total    = sum(probs)
    probs    = [p / total for p in probs]

    return random.choices(outcomes, weights=probs, k=1)[0]

def tenure_for_outcome(outcome: str, emp_type: str) -> int:
    if emp_type == 'structured':
        return random.randint(58, 68)   # ~9 weeks
    if outcome == 'Planned Completion':
        return random.randint(75, 180)
    if outcome == 'Re-engagement':
        return random.randint(60, 160)
    if outcome == 'Student Exit':
        # Heavy early skew
        if random.random() < 0.55:
            return random.randint(1, 30)
        elif random.random() < 0.75:
            return random.randint(31, 60)
        else:
            return random.randint(61, 120)
    if outcome == 'Employer Exit':
        return random.randint(14, 90)
    return random.randint(7, 60)    # Administrative

def pick_reason(outcome: str) -> str:
    return random.choice(REASON_CODES[outcome])

def student_id_gen():
    counter = 1
    while True:
        yield f'STU{counter:04d}'
        counter += 1

# ── Generate records ───────────────────────────────────────────────────────────

def generate_dataset(n_total: int = 1193):
    """Generate all six sheets of WBP data."""

    id_gen = student_id_gen()

    # Employer sampling weights (larger employers get more placements)
    emp_names  = list(EMPLOYERS.keys())
    emp_pop    = [
        40 if EMPLOYERS[e]['type'] == 'structured'
        else 25 if EMPLOYERS[e]['quality'] == 'high'
        else 15 if EMPLOYERS[e]['quality'] == 'medium'
        else 8
        for e in emp_names
    ]

    placements_rows   = []
    ended_curr_rows   = []
    ended_arch_rows   = []
    on_assign_rows    = []
    daily_hired_rows  = []
    ncns_rows         = []

    # Year weights — program grew over time
    year_weights = [0.10, 0.15, 0.20, 0.25, 0.30]

    # Cutoff: records from last two years go to ended_curr; older go to archive
    ARCHIVE_CUTOFF = '2021-2022'

    for _ in range(n_total):
        student_id   = next(id_gen)
        student_code = f'WBP{random.randint(10000,99999)}'
        system_id    = f'B{random.randint(100000,999999)}'
        campus       = random.choice(CAMPUSES)
        employer     = random.choices(emp_names, weights=emp_pop, k=1)[0]
        major        = random.choice(MAJORS)
        academic_year= random.choices(ACADEMIC_YEARS, weights=year_weights, k=1)[0]
        semester     = random.choices(SEMESTERS, weights=[0.40, 0.40, 0.20], k=1)[0]
        hours_pw     = random.choice([10, 15, 20])

        start_dt, end_range = fy_date_range(academic_year, semester)
        start_date = random_date(start_dt, end_range - timedelta(days=30))

        emp_info = EMPLOYERS[employer]
        outcome  = pick_outcome(employer, campus)
        tenure   = tenure_for_outcome(outcome, emp_info['type'])
        end_date = start_date + timedelta(days=tenure)
        reason   = pick_reason(outcome)

        # Build the Total Placements row
        placements_rows.append({
            'Student ID':     student_id,
            'Student Name':   f'Student_{student_id}',
            'ACES ID':        student_code,
            'Banner ID':      system_id,
            'College':        campus,
            'Employer':       employer,
            'Major':          major,
            'Start Date':     start_date,
            'End Date':       end_date,
            'Status':         'Ended' if outcome != 'On Assignment' else 'Active',
            'Reason':         reason,
            'Semester':       semester,
            'Academic Year':  academic_year,
            'Hours Per Week': hours_pw,
        })

        ended_row = {
            'Student ID':    student_id,
            'Student Name':  f'Student_{student_id}',
            'ACES ID':       student_code,
            'College':       campus,
            'Employer':      employer,
            'Start Date':    start_date,
            'End Date':      end_date,
            'Reason':        reason,
            'Semester':      semester,
            'Academic Year': academic_year,
        }

        if academic_year <= ARCHIVE_CUTOFF:
            ended_arch_rows.append(ended_row)
        else:
            ended_curr_rows.append(ended_row)

        # Daily hired report — just placement start info
        daily_hired_rows.append({
            'Student ID':    student_id,
            'Student Name':  f'Student_{student_id}',
            'ACES ID':       student_code,
            'College':       campus,
            'Employer':      employer,
            'Start Date':    start_date,
            'Semester':      semester,
            'Academic Year': academic_year,
        })

        # No Call No Shows (~4% of student exits)
        if outcome == 'Student Exit' and reason == 'No Call No Show':
            ncns_rows.append({
                'Student ID':   student_id,
                'Student Name': f'Student_{student_id}',
                'ACES ID':      student_code,
                'College':      campus,
                'Employer':     employer,
                'Start Date':   start_date,
                'Flagged Date': start_date + timedelta(days=random.randint(1, 14)),
            })

    # Currently on assignment — small slice of most recent semester
    n_active = random.randint(45, 70)
    active_start = date(2024, 1, 15)
    for i in range(n_active):
        student_id   = next(id_gen)
        student_code = f'WBP{random.randint(10000,99999)}'
        campus       = random.choice(CAMPUSES)
        employer     = random.choices(emp_names, weights=emp_pop, k=1)[0]
        start_date   = random_date(active_start, date(2024, 3, 1))
        on_assign_rows.append({
            'Student ID':    student_id,
            'Student Name':  f'Student_{student_id}',
            'ACES ID':       student_code,
            'College':       campus,
            'Employer':      employer,
            'Start Date':    start_date,
            'Status':        'Active',
            'Semester':      'Spring',
            'Academic Year': '2023-2024',
        })

    return {
        'Total Placements':            pd.DataFrame(placements_rows),
        'Daily Hired Report':          pd.DataFrame(daily_hired_rows),
        'Ended Assignments':           pd.DataFrame(ended_curr_rows),
        'ARCHIVED-Ended Assignments':  pd.DataFrame(ended_arch_rows),
        'Data Currently on Assignment':pd.DataFrame(on_assign_rows),
        'PLACED-No Call and No Shows': pd.DataFrame(ncns_rows),
    }

# ── Write to Excel ─────────────────────────────────────────────────────────────

def write_excel(sheets: dict, path: str):
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            # Auto-fit columns
            ws = writer.sheets[sheet_name]
            for col in ws.columns:
                max_len = max(
                    len(str(col[0].value)) if col[0].value else 0,
                    *(len(str(cell.value)) if cell.value else 0 for cell in col[1:])
                )
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 40)

    print(f"Written: {path}")

if __name__ == '__main__':
    print("Generating Workforce Bridge Program synthetic dataset...")
    sheets = generate_dataset(n_total=1193)

    print("\nRecord counts:")
    for name, df in sheets.items():
        print(f"  {name:<35} {len(df):>5} rows")

    # Quick outcome distribution check
    ended = pd.concat([
        sheets['Ended Assignments'],
        sheets['ARCHIVED-Ended Assignments']
    ], ignore_index=True)

    reason_map = {
        'Internship Term Ended': 'Planned Completion',
        'Graduate': 'Planned Completion',
        'Hired by Employer': 'Planned Completion',
        'Hired by Non-WBP Employer Permanently': 'Planned Completion',
        'Seeking New WBP Assignment': 'Re-engagement',
        'Voluntary Withdrawal': 'Student Exit',
        'Student Ended Assignment': 'Student Exit',
        'No Call No Show': 'Student Exit',
        'Did Not Complete Employer Pre-screen': 'Student Exit',
        'Employer Ended Assignment': 'Employer Exit',
        'Ineligible-Not Enrolled': 'Administrative Exit',
        'WBP Pause': 'Administrative Exit',
    }
    ended['outcome'] = ended['Reason'].map(reason_map).fillna('Other')

    print("\nOutcome distribution:")
    counts = ended['outcome'].value_counts()
    for outcome, count in counts.items():
        print(f"  {outcome:<25} {count:>4}  ({count/len(ended)*100:.1f}%)")

    out_path = '/mnt/user-data/outputs/WBP_Anonymized.xlsx'
    write_excel(sheets, out_path)
    print(f"\nDone. Upload WBP_Anonymized.xlsx to Colab alongside the notebook.")

