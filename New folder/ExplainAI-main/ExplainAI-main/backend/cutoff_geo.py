"""City and college-type helpers for CAP PDF imports (matches app.py college_type rules)."""
from __future__ import annotations

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


def classify_college_type(status_str: str) -> str:
    s = str(status_str).strip()
    if not s or s == 'nan':
        return 'Other'
    if s.startswith('Government-Aided'):
        return 'Government-Aided'
    if s.startswith('Government'):
        return 'Government'
    if 'Deemed' in s:
        return 'Deemed University'
    if s.startswith('University'):
        return 'University'
    if s.startswith('Un-Aided') and 'Autonomous' in s:
        return 'Private Autonomous'
    if s.startswith('Un-Aided'):
        return 'Private'
    return 'Other'
