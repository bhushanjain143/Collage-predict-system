# Maharashtra FE Admission Dataset

This folder mirrors the intended layout for a **public GitHub dataset repository** (`Maharashtra-FE-Admission-Dataset`). It stores CSV/JSON exports derived from the official **Maharashtra First Year (FE) Engineering** admission portal and related CET Cell publications.

## Official source

- **Primary portal (academic year varies by hostname):** [Maharashtra FE Admission Portal](https://fe2025.mahacet.org/StaticPages/HomePage)
- **Publisher:** State Common Entrance Test Cell, Maharashtra — [https://cetcell.mahacet.org/](https://cetcell.mahacet.org/)

The portal hostname changes by cycle (for example `fe2024…`, `fe2025…`). Point the scraper `BASE_URL` at the current year’s FE portal homepage when collecting data.

## Dataset overview and structure

| Folder | Contents |
| --- | --- |
| `Merit_Lists/` | Maharashtra State, All India, and J&K merit lists (provisional/final). Typically **PDF** from the portal; a JSON manifest records URLs and checksums. |
| `CAP_Round_Cutoffs/` | CAP I–IV MH and AI quota cutoffs (usually **PDF** on the portal; CSV here after extraction or manual curation). |
| `Seat_Matrix/` | Institute-wise and category-wise seat matrices (PDF/XLSX from official notices). |
| `College_Details/` | College metadata (type, district, fees, hostel, placements where published). |
| `Allotment_Results/` | Institute-wise allotment lists per round (often PDF/ZIP). |
| `Vacancy_Data/` | Vacancy positions after each CAP round. |
| `Scholarship_Data/` | Scholarship / fee waiver notices (links + extracted tables where applicable). |

Supporting files:

- `metadata/manifest.json` — last sync time, downloaded URLs, file paths (written by `scripts/maha_fe_admission/scrape_portal.py`).
- `metadata/reservation_categories.json` — reference list of category codes used in CAP (for filtering and UI); **not** legal advice.

## Collection method

1. **Automated (this repo):** Python script `scripts/maha_fe_admission/scrape_portal.py` uses `requests` + **BeautifulSoup** to parse the static homepage, classify links, and **download PDFs** (merit lists and other linked documents) into the folders above.  
2. **Dynamic pages:** If a future portal page is heavily JavaScript-rendered, extend the scraper with **Selenium** (optional dependency) using the same output layout.  
3. **CAP cutoff tables:** Many cutoffs are distributed as **PDFs** with layout that changes yearly. Use CET Cell PDFs as the source of truth; convert to CSV using your preferred PDF table tool (e.g. `pdfplumber`) or controlled manual extraction. **Do not invent** closing merits or percentiles.

## File naming convention

Use predictable names so year, round, and quota are obvious:

| Pattern | Example |
| --- | --- |
| CAP MH cutoff | `CAP_Round{N}_MH_Cutoff_{YYYY}.csv` |
| CAP AI cutoff | `CAP_Round{N}_AI_Cutoff_{YYYY}.csv` |
| Merit list (manifest entry) | `FE{YYYY}_PCMMH_MeritList_Final.pdf` (as published) |
| Seat matrix | `Seat_Matrix_InstituteWise_{YYYY}.csv` |
| Vacancy | `Vacancy_CAP_Round{N}_{YYYY}.csv` |

Use **four-digit calendar year** or **academic year** consistently in your team (document the choice in commit messages).

## Organization logic

- **Year-wise:** Prefer one file per (academic year, round, document type) unless files become too large; then shard by institute code range.
- **Round-wise:** Subfolders `CAP_Round_Cutoffs/Round_1` … `Round_4` (and `Round_5` if published).
- **Category-wise:** Columns such as `Seat_Category_Code` (e.g. GOPEN, LOPEN, …) in CSV; do not split into separate files unless needed for size.
- **Branch-wise:** Column `Program_Branch` (or official programme name from seat matrix).

## Update process and frequency

- **Manual:** After each CET Cell publication, download or re-run the scraper and commit changes.
- **CI:** Workflow `.github/workflows/maha_fe_data_sync.yml` runs on a **weekly** schedule (and `workflow_dispatch`) to refresh downloadable artifacts and the manifest. **GitHub Actions cannot push** to the default branch unless you configure a PAT or use a bot account; the workflow includes comments for enabling `git commit` + push.

## How this data supports prediction

The **Streamlit** app under `prediction_engine/` loads normalized cutoff CSVs (see sample under `CAP_Round_Cutoffs/`). It:

1. Filters rows by **quota** (MH vs AI), **seat category**, and optional **branch** / **district** text match.
2. Classifies **High / Medium / Low** chance by comparing the student’s **MHT-CET percentile** (or a mapped score) to historical **closing percentiles** with configurable margins.
3. Optionally fits a **scikit-learn** model on numeric history to smooth trends and surface a simple “expected closing” for the latest year (see `prediction_engine/tier_model.py`).

Scholarship and reservation notes are **informational**; always verify with official notices and eligibility rules.

## Local commands (this monorepo)

From the `Collage/` repository root:

```text
pip install -r requirements.txt
python scripts/maha_fe_admission/scrape_portal.py --base-url https://fe2025.mahacet.org/StaticPages/HomePage --output-dir Maharashtra-FE-Admission-Dataset
streamlit run prediction_engine/streamlit_app.py
```

Use `--dry-run` on the scraper to preview destinations without downloading.

## Disclaimer

This dataset and tooling are **not** affiliated with CET Cell or the Government of Maharashtra. Admission decisions are made only through official channels. Use published documents for final choices.
