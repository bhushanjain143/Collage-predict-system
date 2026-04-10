"""
NOTE: For PDFs from https://github.com/jroshani281/data- (or any CAP cutoff PDFs)
into the Flask/SQLite `cutoffs` table, use:

    python import_cap_pdfs.py --pdf-dir "C:\\path\\to\\cloned\\data-" --replace-years 2025 2024

The rest of this file is a legacy PostgreSQL + pdfplumber pipeline (import_2025 style).
=============
Reads the 4 official MHT-CET 2025 Cut Off List PDFs and imports every
Stage-I closing percentile into the PostgreSQL cutoffs table.

Run once:
    python import_2025.py

Requirements:
    pip install pdfplumber psycopg2-binary
"""

import re
import pdfplumber
import psycopg2

# ── Database connection ───────────────────────────────────────────────────────
conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="explainai_db", user="postgres", password="postgres"
)
cur = conn.cursor()

# ── Step 0: Add 'round' column if it doesn't exist yet ───────────────────────
cur.execute("""
    ALTER TABLE cutoffs
    ADD COLUMN IF NOT EXISTS round INTEGER DEFAULT 3;
""")
conn.commit()
print("✅ 'round' column ready.")

# ── City extraction (same logic as import_csv.py) ────────────────────────────

CITY_OVERRIDE = {
    'GRAMIN TECHNICAL AND MANAGEMENT CAMPUS NANDED.':                              'Nanded',
    'Rajendra Mane College of Engineering & Technology  Ambav Deorukh':            'Ratnagiri',
    "Phaltan Education Society's College of Engineering Thakurki Tal- Phaltan Dist-Satara": 'Satara',
    "Shree Siddheshwar Women's College Of Engineering Solapur.":                   'Solapur',
    'ISBM College Of Engineering Pune':                                            'Pune',
    'Pune Institute of Computer Technology':                                       'Pune',
    'Rajiv Gandhi College of Engineering Research & Technology  Chandrapur':       'Chandrapur',
    'Sant Eknath College of Engineering':                                          'Aurangabad',
    "Svkm's Shri Bhagubhai Mafatlal Polytechnic & College of Engineering":         'Mumbai',
    'Karmayogi Institute of Technology':                                           'Solapur',
    'International Centre Of Excellence In Engineering  and Management (ICEEM)':   'Aurangabad',
    'Dr. V.K. Patil College of Engineering & Technology':                          'Ahmednagar',
    'Mangaldeep College of Engineering':                                           'Aurangabad',
    'K J Somaiya Institute of Technology':                                         'Mumbai',
    'Yadavrao Tasgaonkar College of Engineering & Management':                     'Karjat',
    'YASHWANTRAO BHONSALE INSTITUTE OF TECHNOLOGY':                                'Sindhudurg',
    'Devi Mahalaxmi College of Engineering and Technology':                        'Ratnagiri',
    'Sinhgad Institute of Technology':                                             'Pune',
    'Pravin Rohidas Patil College of Engineering & Technology':                    'Thane',
    'Sanjeevan Group of Institutions':                                             'Kolhapur',
    'Sanjay Ghodawat Institute':                                                   'Kolhapur',
    "Navsahyadri Education Society's Group of Institutions":                       'Pune',
    'Samarth College of Engineering and Management':                               'Pune',
    'COEP Technological University':                                               'Pune',
    "S K N Sinhgad College of Engineering, Korti Tal. Pandharpur Dist Solapur":   'Solapur',
    "Shri. Balasaheb Mane Shikshan  Prasarak Mandal's, Ashokrao Mane Group of Institutions": 'Kolhapur',
    'Jaywant College of Engineering & Polytechnic , Kille Macchindragad Tal. Walva District- Sangali': 'Sangli',
    'Dattakala Group Of Institutions, Swami - Chincholi Tal. Daund Dist. Pune':   'Pune',
    'Vishwatmak Jangli Maharaj Ashram Trust (Kokamthan), Atma Malik Institute Of Technology & Research': 'Ahmednagar',
    'Hon. Shri. Babanrao Pachpute Vichardhara Trust, Group of Institutions (Integrated Campus)-Parikrama, Kashti Shrigondha,': 'Ahmednagar',
    'MKD Institute of Technology, Nadurbar': 'Nandurbar',
}

CITY_NORMALIZE = {
    'Navi  Mumbai':            'Navi Mumbai',
    'Navimumbai':              'Navi Mumbai',
    'Chhatrapati Sambhajinagar': 'Aurangabad',
    'Sambhajinagar':           'Aurangabad',
    'Bandra,Mumbai':           'Mumbai',
    'Bandra':                  'Mumbai',
    'Kandivali':               'Mumbai',
    'Matunga':                 'Mumbai',
    'Andheri':                 'Mumbai',
    'Mulund':                  'Mumbai',
    'Borivali':                'Mumbai',
    'Ghansoli':                'Navi Mumbai',
    'Nerul':                   'Navi Mumbai',
    'Nerul, Navi Mumbai':      'Navi Mumbai',
    'Lonavala':                'Pune',
    'Bibwewadi':               'Pune',
    'Akurdi':                  'Pune',
    'Pimpri':                  'Pune',
    'Wakad':                   'Pune',
    'Bavdhan':                 'Pune',
    'Baner':                   'Pune',
    'Kondhwa':                 'Pune',
    'Ambegaon':                'Pune',
    'Talegaon':                'Pune',
    'Wagholi':                 'Pune',
    'Uruli Kanchan':           'Pune',
    'Pirangut':                'Pune',
    'Korti':                   'Pune',
    'Nanded City':             'Pune',
    'Narhe (Ambegaon)':        'Pune',
    'Dist-Pune':               'Pune',
    'Baramati Dist.Pune':      'Pune',
    'Yadrav(Ichalkaranji)':    'Kolhapur',
    'Dist Kolhapur':           'Kolhapur',
    'Chincholi Dist. Nashik':  'Nashik',
    '(Nashik)':                'Nashik',
    'Chas Dist. Ahmednagar':   'Ahmednagar',
    'Dist.Ahmednagar':         'Ahmednagar',
    'Bota Sangamner':          'Ahmednagar',
    'District Nanded':         'Nanded',
    'Dist Wardha':             'Wardha',
    'Dist Thane':              'Thane',
    'Dist.Thane':              'Thane',
    'Thane (E)':               'Thane',
    'Badlapur(W)':             'Thane',
    'Khalapur Dist Raigad':    'Raigad',
    'Tal Dist Dhule':          'Dhule',
    'Dondaicha':               'Dhule',
    'Solapur(North)':          'Solapur',
    'Kaman Dist. Palghar':     'Palghar',
    'Sindhi(Meghe)':           'Nagpur',
    'Dist. Nandurbar':         'Nandurbar',
    'Nadurbar':                'Nandurbar',   # PDF typo — MKD Institute uses this spelling
    'Nandurbar.':              'Nandurbar',
    'Dumbarwadi':              'Pune',
    '444302':                  'Akola',
    'Kille Macchindragad Tal. Walva District- Sangali': 'Sangli',
    'Swami - Chincholi Tal. Daund Dist. Pune':          'Pune',
    'Korti Tal. Pandharpur Dist Solapur':               'Solapur',
    'Atma Malik Institute Of Technology & Research':    'Ahmednagar',
    'Ashokrao Mane Group of Institutions':              'Kolhapur',
    '': 'Maharashtra',
}

def extract_city(college_name):
    name = str(college_name).strip()
    if name in CITY_OVERRIDE:
        return CITY_OVERRIDE[name]
    if ',' in name:
        city = name.rsplit(',', 1)[-1].strip().rstrip('.')
        if len(city) > 30:
            return 'Maharashtra'
        return city
    return 'Maharashtra'

def normalize_city(raw):
    c = str(raw).strip().rstrip('.')
    return CITY_NORMALIZE.get(c, c)

def classify_type(status_str):
    """
    Maps official DTE Maharashtra PDF status strings to our college_type values.
    All real status values found in 2025 PDFs are covered below.
    ORDER MATTERS: 'Government-Aided' must be checked before 'Government'
    because 'Government-Aided Autonomous'.startswith('Government') is True.
    """
    s = str(status_str).strip()
    if not s or s == 'nan':
        return 'Other'
    # Must check Government-Aided BEFORE Government
    if s.startswith('Government-Aided'):
        return 'Government-Aided'       # e.g. VJTI = "Government-Aided Autonomous"
    if s.startswith('Government'):
        return 'Government'             # "Government", "Government Autonomous",
                                        # "Government Home University : ..."
    if 'Deemed' in s:
        return 'Deemed University'      # "Deemed to be University Autonomous"
    if s.startswith('University'):
        return 'University'             # "University Autonomous" (COEP),
                                        # "University Department", "University Managed..."
    if s.startswith('Un-Aided') and 'Autonomous' in s:
        return 'Private Autonomous'     # "Un-Aided Autonomous", "Un-Aided Autonomous Linguistic..."
    if s.startswith('Un-Aided'):
        return 'Private'               # "Un-Aided", "Un-Aided Home University...",
                                        # "Un-Aided Linguistic/Religious Minority..."
    return 'Other'


# ── PDF Parser ────────────────────────────────────────────────────────────────

def parse_cutoff_pdf(pdf_path, year, round_num):
    """
    Parse an official MHT-CET Cut Off List PDF.
    Returns list of dicts: college_name, branch, seat_type,
                           closing_percentile, status_raw, year, round
    """
    records = []
    current_college      = None
    current_college_code = None
    current_branch       = None
    current_status       = None

    print(f"  Parsing {pdf_path} ...", flush=True)

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"  Total pages: {total_pages}", flush=True)

        for pi, page in enumerate(pdf.pages):
            try:
                text = page.extract_text()
            except Exception:
                continue
            if not text:
                continue

            lines = text.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                # ── College code + name ──────────────────────────────────────
                m = re.match(r'^(\d{5})\s+-\s+(.+)', line)
                if m:
                    current_college_code = m.group(1).strip()
                    current_college      = m.group(2).strip()
                    i += 1
                    continue

                # ── Branch code + name ───────────────────────────────────────
                m = re.match(r'^(\d{9,10}T?)\s+-\s+(.+)', line)
                if m:
                    current_branch = m.group(2).strip()
                    i += 1
                    continue

                # ── Status ───────────────────────────────────────────────────
                if line.startswith('Status:'):
                    current_status = line[7:].strip()
                    i += 1
                    continue

                # ── Category header: "Stage GOPENS GSCS GSTS ..." ───────────
                if re.match(r'^Stage\s+[A-Z]', line):
                    cats = line.split()[1:]     # remove 'Stage'

                    # Handle multi-line headers (rare wrapping)
                    while i + 1 < len(lines):
                        nxt = lines[i + 1].strip()
                        if (nxt and
                                not re.match(
                                    r'^(I{1,3}V?|IV|Legends|Maharashtra|'
                                    r'Home|Other|State|All\s)', nxt) and
                                not re.search(r'\d', nxt[:3])):
                            cats += nxt.split()
                            i += 1
                        else:
                            break

                    # ── Data rows below the header ───────────────────────────
                    i += 1
                    while i < len(lines):
                        dline = lines[i].strip()
                        dm = re.match(r'^(I{1,4}|IV)\s+([\d\s]+)', dline)
                        if dm:
                            stage = dm.group(1)
                            pcts = []
                            if i + 1 < len(lines):
                                pl = lines[i + 1]
                                pcts = [float(x)
                                        for x in re.findall(r'\((\d+\.\d+)\)', pl)]
                                if pcts:
                                    i += 1   # consumed percentile line

                            # Only Stage I = closing cutoff we care about
                            if stage == 'I' and current_college and current_branch:
                                for j, cat in enumerate(cats):
                                    cat = cat.strip()
                                    if j < len(pcts) and pcts[j] > 0:
                                        records.append({
                                            'college_name':       current_college,
                                            'college_code':       current_college_code or '',
                                            'branch':             current_branch,
                                            'seat_type':          cat,
                                            'closing_percentile': pcts[j],
                                            'status_raw':         current_status or '',
                                            'year':               year,
                                            'round':              round_num,
                                        })
                            i += 1
                        else:
                            break   # end of this category block
                    continue

                i += 1

        print(f"  Parsed {len(records)} raw records from Round {round_num}.", flush=True)
    return records


# ── Files to process ──────────────────────────────────────────────────────────
#
# Put all 4 PDF files in the SAME folder as this script.
# Adjust filenames below if yours are named differently.
#
PDF_FILES = [
    ('CAP_Round_1_2025_2026.pdf', 2025, 1),
    ('cap_Round_2_2025_2026.pdf', 2025, 2),
    ('CAP_Round_3_2025_2026.pdf', 2025, 3),
    ('cap_round_4_2025_2026.pdf', 2025, 4),
]


# ── Main import ───────────────────────────────────────────────────────────────

all_records = []
for fname, year, rnd in PDF_FILES:
    recs = parse_cutoff_pdf(fname, year, rnd)
    all_records.extend(recs)

print(f"\nTotal raw records across all rounds: {len(all_records)}")

# ── Enrich: city + college_type ───────────────────────────────────────────────
for r in all_records:
    raw_city = extract_city(r['college_name'])
    r['city']         = normalize_city(raw_city)
    r['college_type'] = classify_type(r['status_raw'])

# ── Deduplicate: keep best cutoff per (college, branch, seat_type, year, round) ──
# Within each round, if a seat_type appears twice keep the highest percentile
seen = {}
deduped = []
for r in sorted(all_records, key=lambda x: -x['closing_percentile']):
    key = (r['college_name'], r['branch'], r['seat_type'], r['year'], r['round'])
    if key not in seen:
        seen[key] = True
        deduped.append(r)

print(f"After dedup: {len(deduped)} records to import")

# Category breakdown
cats_summary = {}
for r in deduped:
    st = r['seat_type']
    if 'ST' in st and 'PWD' not in st and 'DEF' not in st:
        cats_summary['ST'] = cats_summary.get('ST', 0) + 1
    elif 'SC' in st and 'PWD' not in st:
        cats_summary['SC'] = cats_summary.get('SC', 0) + 1
    elif 'OBC' in st and 'PWD' not in st:
        cats_summary['OBC'] = cats_summary.get('OBC', 0) + 1
    elif 'NT' in st and 'PWD' not in st:
        cats_summary['NT'] = cats_summary.get('NT', 0) + 1
    elif 'OPEN' in st and 'PWD' not in st:
        cats_summary['OPEN'] = cats_summary.get('OPEN', 0) + 1
print("Category counts:", cats_summary)

# ── Clear existing 2025 data and insert fresh ────────────────────────────────
cur.execute("DELETE FROM cutoffs WHERE year = 2025")
conn.commit()
print("Cleared existing 2025 rows.")

total = len(deduped)
for idx, r in enumerate(deduped):
    cur.execute("""
        INSERT INTO cutoffs
            (college_name, college_code, branch, seat_type, closing_percentile,
             year, round, city, college_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        r['college_name'],
        r.get('college_code', ''),
        r['branch'],
        r['seat_type'],
        float(r['closing_percentile']),
        r['year'],
        r['round'],
        r['city'],
        r['college_type'],
    ))
    if (idx + 1) % 1000 == 0:
        conn.commit()
        print(f"  Inserted {idx+1}/{total}...")
conn.commit()
cur.close()
conn.close()
print(f"\n✅ Done! {total} rows imported for 2025 (Rounds 1-4).")
