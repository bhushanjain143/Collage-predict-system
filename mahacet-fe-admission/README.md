# Maharashtra MAHACET FE Admission — Automated Pipeline & Prediction

End-to-end toolkit to **discover** the yearly FE admission portal, **scrape** public documents, **clean** CSV datasets, **train** an ML classifier for rough admission chances, and serve a **Streamlit** UI.

## Auto-detected source URL and year

- **Primary pattern:** `https://fe{YEAR}.mahacet.org/StaticPages/HomePage` (year from env `MAHA_FE_YEAR` or current calendar year).
- **Discovery output:** `config/discovered_portal_url.json` (canonical) plus importable **`config/discovered_runtime.py`** (auto-generated; gitignored) consumed via `settings.get_active_portal_url()`.
- **Failure log:** `data/Data_Quality_Logs/url_discovery_log.json`.

Official publisher: [State CET Cell, Maharashtra](https://cetcell.mahacet.org/). This project is **not** affiliated with the government; data must be verified from primary PDFs/notices.

## Folder structure

```text
mahacet-fe-admission/
  .github/workflows/annual_data_refresh.yml
  scraper/          # url_discovery, modular scrapers, scraper_main, fe_stub_spider (Scrapy)
  cleaner/          # dedupe, missing data, format, outliers, structural fixes
  data/             # Merit lists, CAP cutoffs, seat matrix, college details, …
  model/            # feature_engineering, train_model, predict, model_artifacts/
  app/streamlit_app.py
  config/settings.py
  tests/
  requirements.txt
  README.md
```

## File naming convention (examples)

| Example | Meaning |
| --- | --- |
| `CAP_Cutoff_MH_2024_Round1.csv` | CAP MH cutoff table (CSV after PDF extraction) |
| `CAP_Cutoff_AI_2024_Round2.csv` | CAP AI cutoff |
| `Merit_List_MH_Final_2024.csv` | Merit manifest / extracted table |
| `Seat_Matrix_Institute_wise_2024.csv` | Seat matrix |
| `College_Details_2024.csv` | College attributes |
| `Vacancy_Data_2024_Round3.csv` | Vacancy snapshot |

Scrapers also write per-year **manifest** CSV/JSON under `manifests/` beside downloads.

## Data organization

- **Year-wise:** academic year column (e.g. `2025-26`) in cutoff CSVs.
- **Round-wise:** `data/CAP_Round_Cutoffs/Round_1` … `Round_4`.
- **Category-wise:** `Seat_Category_Code` column (GOPEN, EWS, …).
- **Branch-wise:** `Program_Branch` column.

## Cleaning pipeline (order)

1. **Deduplication** — composite keys (`Institute_Code` + category + round + year + branch when present); drop >90% null columns; strip index-like columns.
2. **Missing data** — `<5%` drop rows (union of low-null columns); `5–30%` median/mode impute; `>30%` flagged unreliable; `data_quality_flag` column; `missing_data_report.csv`.
3. **Format standardizer** — lowercase strings; category synonyms; dates; numeric ranks/percentiles/fees; boolean normalization.
4. **Outlier filter** — IQR on percentiles/ranks; Z-score on fees/intake; append `outlier_log.csv`.
5. **Structural fix** — null tokens; college type synonyms; branch synonyms; optional `master_college_list.csv` validation → `structural_errors.csv`.

Summary written to `data/Data_Quality_Logs/cleaning_summary.json` (includes **`duplicates_removed_total`** across files).

## How to run manually

Set working directory to `mahacet-fe-admission/` and ensure `PYTHONPATH` includes the project root (`.`).

**Windows (PowerShell):**

```powershell
cd mahacet-fe-admission
$env:PYTHONPATH = "."
python scraper/url_discovery.py
python scraper/scraper_main.py --skip-discovery --years-back 4
python cleaner/cleaner_main.py
python model/feature_engineering.py
python model/train_model.py
streamlit run app/streamlit_app.py
```

Use **`--years-back 0`** for a single-host scrape only. Default **`--years-back 4`** attempts five admission years (`fe{Y}…`) when each host responds.

**Optional Selenium (Chrome + chromedriver on PATH):**

```powershell
python scraper/scraper_main.py --skip-discovery --selenium --years-back 4
```

**Optional Scrapy smoke check:**

```powershell
scrapy runspider scraper/fe_stub_spider.py -s LOG_LEVEL=INFO
```

## Retrain the model

```powershell
python model/train_model.py
```

Artifacts: `model/model_artifacts/model.pkl`, `model/model_artifacts/features.json`.

Training uses **synthetic augmentation** around historical closing percentiles when student-level labels are not available — replace with real labelled data for production quality.

## GitHub Actions cron

Workflow: `.github/workflows/annual_data_refresh.yml`

- **Schedule:** `0 0 1 8 *` — 1 August 00:00 UTC yearly.
- **Steps:** `url_discovery` → `scraper_main` → `cleaner_main` → `feature_engineering.py` → `train_model.py` (each may `continue-on-error` so logs are collected).
- **Notifications:** enable GitHub Actions failure notifications for the repo.
- **Auto-push:** commented out; requires `contents:write` and a suitable token.

## Tests

```powershell
pytest tests/
```

## Contributing / reporting data issues

- Open an issue describing the **official PDF/URL**, expected columns, and a sample row.
- If scrapers break after a portal HTML change, attach the homepage HTML snippet or link.

## License & disclaimer

Data is sourced from **public** MAHACET / CET Cell pages. This software is provided as-is for research and planning. **Admissions are decided only through official CAP rounds** — never rely on model output alone.

Environment variables (optional): `MAHA_FE_YEAR`, `MAHA_FE_HTTP_TIMEOUT`, `MAHA_FE_HTTP_RETRIES`, `MAHA_FE_DELAY_MIN`, `MAHA_FE_DELAY_MAX`, `MAHA_LOG_LEVEL`, `GOOGLE_CSE_API_KEY`, `GOOGLE_CSE_CX`.

## Production build (optimized)

- **Docker:** `docker build -t mahacet-fe .` then `docker run -p 8501:8501 mahacet-fe` — image uses `PYTHONDONTWRITEBYTECODE`, `PIP_NO_CACHE_DIR`, `compileall`, and `MAHA_LOG_LEVEL=WARNING` by default.
- **Streamlit:** `.streamlit/config.toml` sets headless defaults, caps upload size, disables usage stats, enables fast reruns in dev.
- **App runtime:** `@st.cache_data` / `@st.cache_resource` in `app/streamlit_app.py` to avoid reloading CSVs and the sklearn pipeline on every interaction.
- **Training:** XGBoost uses `tree_method="hist"` where available for faster boosting iterations.

**PDF export** in the UI requires `fpdf2` (already listed in `requirements.txt`).
