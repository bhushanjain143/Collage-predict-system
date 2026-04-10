"""
import_2025_fixed.py
====================
FIXED version of import_2025.py

ROOT CAUSE OF THE BUG THAT WAS FIXED:
  The old extract_city() used only comma-splitting:
      city = college_name.rsplit(',', 1)[-1]
  Any college name WITHOUT a comma (e.g. "COEP Technological University",
  "Sinhgad Institute of Technology", "Sanjay Ghodawat Institute") got
  city = 'Maharashtra' — making them invisible in city-filtered searches.
  44 out of 368 colleges (12%) were affected, including COEP Pune —
  the most important Government college in Pune.

  The fix adds a keyword-scan fallback: if no comma is found, the full
  college name is scanned for known city/district keywords before
  falling back to 'Maharashtra'.

Run once:
    python import_2025_fixed.py

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

# ── Step 0: Ensure schema columns exist ──────────────────────────────────────
cur.execute("""
    ALTER TABLE cutoffs
    ADD COLUMN IF NOT EXISTS round INTEGER DEFAULT 3;
""")
conn.commit()
print("✅ 'round' column ready.")

# ─────────────────────────────────────────────────────────────────────────────
#  CITY EXTRACTION  (FIXED)
# ─────────────────────────────────────────────────────────────────────────────

# Hard overrides — exact college name → city.
# Use these only for truly ambiguous names the keyword scan can't resolve.
CITY_OVERRIDE = {
    # ── previously existing overrides (kept) ──
    'GRAMIN TECHNICAL AND MANAGEMENT CAMPUS NANDED.':                              'Nanded',
    'Rajendra Mane College of Engineering & Technology  Ambav Deorukh':            'Ratnagiri',
    "Phaltan Education Society's College of Engineering Thakurki Tal- Phaltan Dist-Satara": 'Satara',
    "Shree Siddheshwar Women's College Of Engineering Solapur.":                   'Solapur',
    'ISBM College Of Engineering Pune':                                            'Pune',
    'Pune Institute of Computer Technology':                                       'Pune',
    'Rajiv Gandhi College of Engineering Research & Technology  Chandrapur':       'Chandrapur',
    # NOTE: spacing variant from PDF — both kept
    'Rajiv Gandhi College of Engineering Research & Technology  Chandrapur':       'Chandrapur',
    'Rajiv Gandhi College of Engineering Research & Technology Chandrapur':        'Chandrapur',
    'Sant Eknath College of Engineering':                                          'Aurangabad',
    "Svkm's Shri Bhagubhai Mafatlal Polytechnic & College of Engineering":         'Mumbai',
    'Karmayogi Institute of Technology':                                           'Solapur',
    'International Centre Of Excellence In Engineering  and Management (ICEEM)':   'Aurangabad',
    'International Centre Of Excellence In Engineering and Management (ICEEM)':    'Aurangabad',
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
    # ── THE KEY FIX: COEP and other no-comma Pune Government colleges ──
    'COEP Technological University':                                               'Pune',
    'College of Engineering Pune':                                                 'Pune',
    "S K N Sinhgad College of Engineering, Korti Tal. Pandharpur Dist Solapur":   'Solapur',
    "Shri. Balasaheb Mane Shikshan  Prasarak Mandal's, Ashokrao Mane Group of Institutions": 'Kolhapur',
    'Jaywant College of Engineering & Polytechnic , Kille Macchindragad Tal. Walva District- Sangali': 'Sangli',
    'Dattakala Group Of Institutions, Swami - Chincholi Tal. Daund Dist. Pune':   'Pune',
    'Vishwatmak Jangli Maharaj Ashram Trust (Kokamthan), Atma Malik Institute Of Technology & Research': 'Ahmednagar',
    'Hon. Shri. Babanrao Pachpute Vichardhara Trust, Group of Institutions (Integrated Campus)-Parikrama, Kashti Shrigondha,': 'Ahmednagar',
    'MKD Institute of Technology, Nadurbar':                                       'Nandurbar',
    'ISBM College Of Engineering Pune':                                            'Pune',
    'Babasaheb Phadtare Engineering & Technology Kalamb-Walchandnagar Tal Indapur Dist Pune': 'Pune',
    'Dattakala Group Of Institutions, Swami - Chincholi Tal. Daund Dist. Pune':   'Pune',
    'Rajgad Technical Campus':                                                     'Pune',
}

# Normalize raw city strings extracted by comma-split
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
    'Nadurbar':                'Nandurbar',
    'Nandurbar.':              'Nandurbar',
    'Dumbarwadi':              'Pune',
    '444302':                  'Akola',
    'Kille Macchindragad Tal. Walva District- Sangali': 'Sangli',
    'Swami - Chincholi Tal. Daund Dist. Pune':          'Pune',
    'Korti Tal. Pandharpur Dist Solapur':               'Solapur',
    'Atma Malik Institute Of Technology & Research':    'Ahmednagar',
    'Ashokrao Mane Group of Institutions':              'Kolhapur',
    '': 'Maharashtra',
    # ── New additions ──
    'Avasari Khurd':           'Pune',
    'Kashti Shrigondha':       'Ahmednagar',
    'Shirasgon':               'Nashik',
    'Karjat':                  'Raigad',
}

# ── Keyword scan — used when comma-split fails ────────────────────────────────
# Order matters: more specific first (e.g. "Navi Mumbai" before "Mumbai")
CITY_KEYWORDS = [
    ('Navi Mumbai',    'Navi Mumbai'),
    ('NaviMumbai',     'Navi Mumbai'),
    ('Amravati',       'Amravati'),
    ('Nagpur',         'Nagpur'),
    ('Pune',           'Pune'),
    ('Mumbai',         'Mumbai'),
    ('Nashik',         'Nashik'),
    ('Aurangabad',     'Aurangabad'),
    ('Sambhajinagar',  'Aurangabad'),
    ('Kolhapur',       'Kolhapur'),
    ('Solapur',        'Solapur'),
    ('Nanded',         'Nanded'),
    ('Ahmednagar',     'Ahmednagar'),
    ('Thane',          'Thane'),
    ('Ratnagiri',      'Ratnagiri'),
    ('Satara',         'Satara'),
    ('Sangli',         'Sangli'),
    ('Latur',          'Latur'),
    ('Jalgaon',        'Jalgaon'),
    ('Akola',          'Akola'),
    ('Washim',         'Washim'),
    ('Wardha',         'Wardha'),
    ('Yavatmal',       'Yavatmal'),
    ('Chandrapur',     'Chandrapur'),
    ('Gondia',         'Gondia'),
    ('Bhandara',       'Bhandara'),
    ('Gadchiroli',     'Gadchiroli'),
    ('Dhule',          'Dhule'),
    ('Nandurbar',      'Nandurbar'),
    ('Buldhana',       'Buldhana'),
    ('Osmanabad',      'Osmanabad'),
    ('Parbhani',       'Parbhani'),
    ('Hingoli',        'Hingoli'),
    ('Beed',           'Beed'),
    ('Bid',            'Beed'),
    ('Raigad',         'Raigad'),
    ('Sindhudurg',     'Sindhudurg'),
    ('Palghar',        'Palghar'),
    ('Karad',          'Karad'),
    ('Baramati',       'Pune'),
    ('Lonavala',       'Pune'),
    ('Pimpri',         'Pune'),
    ('Chinchwad',      'Pune'),
    ('Talegaon',       'Pune'),
    ('Pirangut',       'Pune'),
    ('Wagholi',        'Pune'),
    ('Bavdhan',        'Pune'),
    ('Kondhwa',        'Pune'),
    ('Narhe',          'Pune'),
    ('Wadgaon',        'Pune'),
    ('Vadgaon',        'Pune'),
    ('Karvenagar',     'Pune'),
    ('Bibwewadi',      'Pune'),
    ('Akurdi',         'Pune'),
    ('Lohgaon',        'Pune'),
    ('Yewalewadi',     'Pune'),
    ('Kothrud',        'Pune'),
    ('Tathawade',      'Pune'),
    ('Ambegaon',       'Pune'),
    ('Katraj',         'Pune'),
    ('Hadapsar',       'Pune'),
    ('Pimpri',         'Pune'),
    ('Kandivali',      'Mumbai'),
    ('Borivali',       'Mumbai'),
    ('Andheri',        'Mumbai'),
    ('Mulund',         'Mumbai'),
    ('Matunga',        'Mumbai'),
    ('Bandra',         'Mumbai'),
    ('Ghansoli',       'Navi Mumbai'),
    ('Nerul',          'Navi Mumbai'),
    ('Belapur',        'Navi Mumbai'),
    ('Kharghar',       'Navi Mumbai'),
    ('Vasai',          'Thane'),
    ('Kalyan',         'Thane'),
    ('Badlapur',       'Thane'),
    ('Ambernath',      'Thane'),
    ('Dombivli',       'Thane'),
    ('Ulhasnagar',     'Thane'),
    ('Shahada',        'Nandurbar'),
    ('Shirpur',        'Dhule'),
    ('Ichalkaranji',   'Kolhapur'),
    ('Kupwad',         'Sangli'),
    ('Miraj',          'Sangli'),
    ('Pandharpur',     'Solapur'),
    ('Barshi',         'Solapur'),
    ('Osmanabad',      'Osmanabad'),
    ('Tuljapur',       'Osmanabad'),
    ('Phaltan',        'Satara'),
    ('Karad',          'Satara'),
    ('Sindhudurg',     'Sindhudurg'),
    ('Kankavli',       'Sindhudurg'),
    ('Kudal',          'Sindhudurg'),
    ('Ratnagiri',      'Ratnagiri'),
    ('Deorukh',        'Ratnagiri'),
    ('Chandrapur',     'Chandrapur'),
    ('Amravati',       'Amravati'),
    ('Shegaon',        'Buldhana'),
    ('Khamgaon',       'Buldhana'),
    ('Malkapur',       'Buldhana'),
    ('Yavatmal',       'Yavatmal'),
    ('Pusad',          'Yavatmal'),
    ('Washim',         'Washim'),
    ('Wardha',         'Wardha'),
    ('Hingoli',        'Hingoli'),
]

def _keyword_city(name: str) -> str:
    """Scan college name for city/district keywords. Returns city or 'Maharashtra'."""
    name_upper = name.upper()
    for keyword, city in CITY_KEYWORDS:
        if keyword.upper() in name_upper:
            return city
    return 'Maharashtra'


def extract_city(college_name: str) -> str:
    """
    FIXED city extractor.

    Strategy (in order):
      1. CITY_OVERRIDE exact match — highest priority
      2. Comma-split: take text after last comma
         • normalize via CITY_NORMALIZE
         • if result still looks like a raw address fragment, try keyword scan
      3. Keyword scan of the full name
      4. Fall back to 'Maharashtra'
    """
    name = str(college_name).strip()

    # 1. Exact override
    if name in CITY_OVERRIDE:
        return CITY_OVERRIDE[name]

    # 2. Comma-split
    if ',' in name:
        raw = name.rsplit(',', 1)[-1].strip().rstrip('.')
        # Reject if too long (it's an address fragment, not a city name)
        if len(raw) <= 30:
            normalized = CITY_NORMALIZE.get(raw, raw)
            # If normalize still returned something not city-like, keyword-scan
            if normalized and normalized != 'Maharashtra':
                return normalized
        # Comma-split gave an unusable fragment — fall through to keyword scan

    # 3. Keyword scan of full name
    return _keyword_city(name)


def normalize_city(raw: str) -> str:
    c = str(raw).strip().rstrip('.')
    return CITY_NORMALIZE.get(c, c)


def classify_type(status_str: str) -> str:
    s = str(status_str).strip()
    if s == 'nan' or not s:          return 'Other'
    if s.startswith('Government'):   return 'Government'
    if 'Deemed' in s:                return 'Deemed University'
    if s.startswith('University') or s == 'University': return 'University'
    if 'Autonomous' in s:            return 'Private Autonomous'
    if s.startswith('Un-Aided'):     return 'Private'
    return 'Other'


# ── PDF Parser ────────────────────────────────────────────────────────────────

def parse_cutoff_pdf(pdf_path: str, year: int, round_num: int) -> list:
    """
    Parse an official MHT-CET Cut Off List PDF.
    Returns list of dicts: college_name, college_code, branch, seat_type,
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
                    cats = line.split()[1:]  # remove 'Stage'

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
                                    i += 1  # consumed percentile line

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
                            break  # end of this category block
                    continue

                i += 1

        print(f"  Parsed {len(records)} raw records from Round {round_num}.", flush=True)
    return records


# ── Files to process ──────────────────────────────────────────────────────────
#
# Put all 4 PDF files in the SAME folder as this script.
# Filenames must match exactly (case-sensitive on Linux).
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
city_debug = {}  # track what city each college got — for verification
for r in all_records:
    name = r['college_name']
    raw_city  = extract_city(name)
    final_city = normalize_city(raw_city)
    r['city']         = final_city
    r['college_type'] = classify_type(r['status_raw'])
    city_debug[name]  = final_city

# ── Debug: show any Government college still getting Maharashtra ──────────────
print("\n⚠️  Government colleges still mapped to Maharashtra (check these manually):")
found_any = False
for r in all_records:
    if r['college_type'] == 'Government' and r['city'] == 'Maharashtra':
        if r['college_name'] not in city_debug or city_debug[r['college_name']] == 'Maharashtra':
            print(f"   [{r.get('college_code','')}] {r['college_name']}")
            found_any = True
if not found_any:
    print("   None — all Government colleges have a proper city. ✅")

# ── Deduplicate: keep best cutoff per (college, branch, seat_type, year, round) ──
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

# ── Verify Pune Government college count before inserting ────────────────────
pune_govt = [r for r in deduped if r['city'] == 'Pune' and r['college_type'] == 'Government']
pune_govt_names = set(r['college_name'] for r in pune_govt)
print(f"\nPune Government colleges to be inserted: {len(pune_govt_names)}")
for n in sorted(pune_govt_names):
    print(f"   • {n}")

# ── Clear existing 2025 data and insert fresh ─────────────────────────────────
cur.execute("DELETE FROM cutoffs WHERE year = 2025")
conn.commit()
print("\nCleared existing 2025 rows.")

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
        print(f"  Inserted {idx + 1}/{total}...")

conn.commit()
cur.close()
conn.close()
print(f"\n✅ Done! {total} rows imported for 2025 (Rounds 1-4).")

