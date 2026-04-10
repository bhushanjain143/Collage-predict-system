# ExplainAI — MHT-CET college predictor & counselling

**What this is:** a web app for **Maharashtra MHT-CET engineering admissions** — cutoff-backed college lists, counselling-style filters, scholarship hints, **saved prediction runs** (SQLite), and **optional AI explanations** when you configure an API key on the server.

**What it is not:** a black-box “guaranteed seat” engine. Lists use **published CAP-style cutoff data** you import into the DB; always confirm on **CET Cell** notices.

The product name **ExplainAI** refers to **explainable suggestions** (per-college “Why?” modals) plus **optional LLM text** (`/api/ai/explain`) when `OPENAI_API_KEY` or `GEMINI_API_KEY` is set.

---

## Features (recruiter-friendly)

| Area | Details |
|------|--------|
| **Data** | `Cutoff` rows in SQLite (or Postgres) from CAP PDFs via `import_cap_pdfs.py` |
| **Backend** | Flask JSON APIs: recommend, scholarships, auth, likes, **`/api/config`**, **`/api/ai/explain`**, **`/api/predictions`** |
| **Frontend** | Static `index.html` + `script.js`; college search on results; PDF export includes last AI/offline summary when present |
| **Auth** | Register / login; **save a full prediction run** to the dashboard |
| **AI (optional)** | Server-side OpenAI or Gemini; UI shows buttons only when `GET /api/config` reports `ai_enabled` |

---

## Quick start (local)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r ../requirements.txt
python app.py
```

- **API + UI on one port:** open `http://127.0.0.1:5000/` — Flask serves `index.html` and static assets from the parent folder.
- **Live Server (port 5500):** keep `python app.py` running; the frontend uses `http://127.0.0.1:5000` for APIs automatically.

Copy `backend/.env.example` to `backend/.env` and set secrets locally (do not commit `.env`). For LLM features add **`OPENAI_API_KEY`** or **`GEMINI_API_KEY`**.

---

## Cutoff data (import into SQLite)

- **CAP cutoff PDFs** (e.g. from [jroshani281/data-](https://github.com/jroshani281/data-)): clone that repo, then from the `backend` folder run:

  ```bash
  python import_cap_pdfs.py --pdf-dir "C:\path\to\data-" --replace-years 2025 2024
  ```

  Useful files: `*ENGG_CAP*_CutOff*.pdf`, `CAP_Round_*_2025_2026.pdf`, `*_round*.pdf`. Seat matrix and merit-list PDFs are skipped (different format).

- **Legacy:** `import_csv.py` / `import_2025_fixed.py` target **PostgreSQL**; prefer `import_cap_pdfs.py` for the default SQLite app.

---

## Deploy (Render)

See `render.yaml` at this folder level. Set environment variables on the dashboard (**`SECRET_KEY`**, optional **`OPENAI_API_KEY`** / **`GEMINI_API_KEY`**). After first deploy, run PDF import or attach a DB with cutoffs populated.

**Zip hygiene:** when sharing the project, **do not include a `.git` folder** inside the zip unless you intend to ship full history.

---

## Author

Roshnai
