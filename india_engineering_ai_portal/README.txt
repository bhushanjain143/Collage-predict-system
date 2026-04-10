India Engineering AI Portal (demo)
====================================

Based on: AI_ML_College_Portal_v2.md — keep a copy under this Collage repo (e.g. docs/) if you want it versioned with the code.

Quick start (from the Collage repo root only)
----------------------------------------------
  cd india_engineering_ai_portal
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  python app.py

Open: http://127.0.0.1:5050/

What this demo includes
-----------------------
  - Flask JSON APIs: /api/colleges, /api/recommend, /api/predict, /api/compare,
    /api/scholarships, /api/cap-hint, /api/chat
  - Single-page UI: explore, rule-based admission chance, cosine-style
    recommendations, scholarship rules, CAP heuristic, FAQ chat, compare.

Data is a small curated subset (data_seed.py) — not full AICTE / JoSAA dumps.
Fees and cutoffs are indicative only (per your spec disclaimer).

Next steps (from your roadmap)
------------------------------
  - Wire MySQL + real datasets
  - Train sklearn / XGBoost on historical features
  - Replace FAQ chat with OpenAI or Rasa
