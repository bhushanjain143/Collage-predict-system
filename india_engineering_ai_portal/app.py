"""
India Engineering AI Portal — Flask backend (demo).
Serves SPA-style UI + JSON APIs for predict, recommend, compare, scholarships, chat FAQ.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from data_seed import COLLEGES

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

STATS = {
    "total_engineering": "8,876+",
    "private": "6,611+",
    "government": "2,265+",
    "iits": 23,
    "nits": 31,
    "iiits": 26,
}

FAQ_RESPONSES: list[tuple[str, str]] = [
    (r"best.*computer|CSE.*college", "Top picks depend on your rank/percentile, budget, and home state. Use **Recommend** with your JEE/MHT-CET scores and filter by branch CSE. Always verify on JoSAA / state CET sites."),
    (r"government.*82|82.*percentile|govt.*percentile", "82 percentile competitiveness varies by exam and category. Try **Admission chance** with your exact exam + category; add safer choices in **Recommend** with a higher max fee / broader state filter."),
    (r"scholarship", "Use **Scholarships**: select category, income band, and gender for rule-based hints. Final eligibility is only on the official scheme / college notice."),
    (r"CAP|cap round|round 2", "CAP (e.g. Maharashtra) is multi-round counselling. Later rounds can have seat movement; use official CET cell CAP PDFs for cutoffs. Our **CAP guide** gives a conservative rule-based hint only."),
    (r"document|documents", "Common documents: rank card, category certificate, domicile, income (if applicable), photo ID. Exact list is on your state CET / JoSAA portal for that year."),
    (r"fee|fees", "All fees in this demo are **indicative** from the sample dataset. Confirm on the college website or prospectus."),
    (r"hello|hi\b", "Hello — ask about admissions, CAP rounds, scholarships, or comparison, or use the tools above."),
]


def category_adjustment(category: str) -> float:
    c = (category or "General").upper()
    if "SC" in c or "ST" in c:
        return 12.0
    if "OBC" in c or "EWS" in c:
        return 4.0
    if "PWD" in c or "PwD" in c:
        return 6.0
    return 0.0


def predict_chance(jee_pct: float, college: dict, category: str) -> tuple[str, str, float]:
    """Rule-based demo: compare effective percentile to college cutoff_score."""
    adj = category_adjustment(category)
    effective = jee_pct + adj
    need = float(college["cutoff_score"])
    delta = effective - need
    if delta >= 2:
        return "High Chance", "Your profile is above the indicative cutoff band for this demo row.", min(0.95, 0.65 + delta / 40)
    if delta >= -1:
        return "Medium Chance", "Borderline vs indicative cutoff — fill choices carefully and watch official rounds.", max(0.35, 0.45 + delta / 20)
    return "Low Chance", "Below indicative cutoff for this demo — consider safer options or category-specific lists.", max(0.08, 0.25 + delta / 25)


def college_vector(c: dict) -> list[float]:
    fee = max(c["fees_per_year"], 1)
    return [
        c["placement_percent"] / 100.0,
        min(c["avg_package_lpa"] / 30.0, 1.0),
        1.0 - min(fee / 600000.0, 1.0),
        1.0 if c["college_type"] == "IIT" else 0.85 if c["college_type"] == "NIT" else 0.75 if c["college_type"] == "IIIT" else 0.65,
    ]


def student_vector(prefs: dict) -> list[float]:
    w_pl = float(prefs.get("weight_placement", 0.35))
    w_pkg = float(prefs.get("weight_package", 0.35))
    w_fee = float(prefs.get("weight_affordability", 0.3))
    tier = prefs.get("college_type_pref", "any")
    tier_bonus = 1.0 if tier == "any" else 0.95
    return [
        w_pl * tier_bonus,
        w_pkg * tier_bonus,
        w_fee * tier_bonus,
        0.8,
    ]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def filter_colleges(
    q: str | None,
    college_type: str | None,
    state: str | None,
    branch: str | None,
) -> list[dict]:
    rows = list(COLLEGES)
    if college_type and college_type.lower() not in ("all", "any"):
        rows = [c for c in rows if c["college_type"].lower() == college_type.lower()]
    if state and state.lower() not in ("all", "any"):
        rows = [c for c in rows if state.lower() in c["state"].lower()]
    if branch and branch.lower() not in ("all", "any"):
        b = branch.lower()
        rows = [c for c in rows if b in c["branch"].lower() or b in c["branch_code"].lower()]
    if q:
        ql = q.lower()
        rows = [
            c
            for c in rows
            if ql in c["college_name"].lower()
            or ql in c["city"].lower()
            or ql in c["branch"].lower()
        ]
    return rows


@app.route("/")
def index():
    return render_template("index.html", stats=STATS)


@app.route("/api/stats")
def api_stats():
    return jsonify(STATS)


@app.route("/api/colleges")
def api_colleges():
    q = request.args.get("q", "").strip()
    college_type = request.args.get("type", "all")
    state = request.args.get("state", "all")
    branch = request.args.get("branch", "all")
    return jsonify(filter_colleges(q or None, college_type, state, branch))


@app.route("/api/college/<int:cid>")
def api_college(cid):
    for c in COLLEGES:
        if c["id"] == cid:
            return jsonify(c)
    return jsonify({"error": "not found"}), 404


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json(force=True, silent=True) or {}
    prefs = {
        "weight_placement": float(data.get("weight_placement", 0.4)),
        "weight_package": float(data.get("weight_package", 0.35)),
        "weight_affordability": float(data.get("weight_affordability", 0.25)),
        "college_type_pref": (data.get("college_type_pref") or "any").strip(),
    }
    max_fee = int(data.get("max_fee_per_year") or 600000)
    state_pref = (data.get("state_pref") or "").strip().lower()
    branch_pref = (data.get("branch_pref") or "").strip().lower()
    jee = float(data.get("jee_percentile") or 0)

    ct = prefs["college_type_pref"] if prefs["college_type_pref"].lower() != "any" else "all"
    cand = filter_colleges(None, ct, "all", "all")
    if state_pref:
        cand = [c for c in cand if state_pref in c["state"].lower()]
    if branch_pref:
        cand = [
            c
            for c in cand
            if branch_pref in c["branch"].lower() or branch_pref in c["branch_code"].lower()
        ]
    cand = [c for c in cand if c["fees_per_year"] <= max_fee]

    if not cand:
        cand = list(COLLEGES)

    sv = student_vector(prefs)
    scored = []
    for c in cand:
        if jee > 0 and c["cutoff_score"] > jee + 5:
            continue
        sc = cosine(sv, college_vector(c))
        if prefs["college_type_pref"] != "any" and c["college_type"].lower() != prefs["college_type_pref"].lower():
            sc *= 0.85
        scored.append((sc, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [dict(c, match_score=round(s, 4)) for s, c in scored[:25]]
    return jsonify(top)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True, silent=True) or {}
    jee = float(data.get("jee_percentile") or 0)
    mht = float(data.get("mht_percentile") or 0)
    use = max(jee, mht)
    category = data.get("category") or "General"
    cid = int(data.get("college_id") or 0)
    college = next((c for c in COLLEGES if c["id"] == cid), None)
    if not college:
        return jsonify({"error": "college_id required / invalid"}), 400
    label, detail, prob = predict_chance(use, college, category)
    return jsonify(
        {
            "result": label,
            "detail": detail,
            "probability": round(prob, 3),
            "used_percentile": use,
            "category_adjustment": category_adjustment(category),
            "disclaimer": "Demo rule-based model — not trained ML. Verify with official cutoffs.",
        }
    )


@app.route("/api/compare", methods=["POST"])
def api_compare():
    data = request.get_json(force=True, silent=True) or {}
    ids = data.get("ids") or []
    if not isinstance(ids, list) or len(ids) < 2:
        return jsonify({"error": "send ids: [id1, id2, ...] at least 2"}), 400
    out = []
    for i in ids[:4]:
        c = next((x for x in COLLEGES if x["id"] == int(i)), None)
        if c:
            out.append(c)
    if len(out) < 2:
        return jsonify({"error": "invalid ids"}), 400
    # Simple AI-style blurb
    best_pl = max(out, key=lambda x: x["placement_percent"])
    best_fee = min(out, key=lambda x: x["fees_per_year"])
    blurb = (
        f"{best_pl['college_name']} leads on indicative placement ({best_pl['placement_percent']}%). "
        f"{best_fee['college_name']} has the lowest annual fee in this selection (₹{best_fee['fees_per_year']:,}). "
        "Confirm fees and placements on official sites."
    )
    return jsonify({"colleges": out, "suggestion": blurb})


@app.route("/api/scholarships", methods=["POST"])
def api_scholarships():
    data = request.get_json(force=True, silent=True) or {}
    cat = (data.get("category") or "General").upper()
    income = (data.get("income_band") or "above_8L").lower()
    gender = (data.get("gender") or "any").lower()
    tips: list[str] = []
    if "SC" in cat or "ST" in cat:
        tips.append("Central / state SC-ST fee reimbursement & post-matric scholarships — check National Scholarship Portal and your state SC welfare portal.")
    if "OBC" in cat:
        tips.append("State OBC scholarships (income limits apply) — verify current income slabs.")
    if "EWS" in cat:
        tips.append("EWS quota documentation (income/asset certificate) for admission & possible fee relief in some institutions.")
    if income in ("below_2.5l", "below_8l"):
        tips.append("Merit-cum-means (MCM) and institute need-based aid — apply through college at admission.")
    if gender == "female":
        tips.append("Explore AICTE Pragati / state girls' scholarship schemes where eligible.")
    if not tips:
        tips.append("Browse National Scholarship Portal (scholarships.gov.in) and the college's scholarship page.")
    return jsonify({"matches": tips})


@app.route("/api/cap-hint", methods=["POST"])
def api_cap_hint():
    data = request.get_json(force=True, silent=True) or {}
    pct = float(data.get("mht_percentile") or 0)
    if pct >= 99:
        rnd = "Likely CAP I–II for top autonomous institutes (Maharashtra) — still verify CAP PDFs."
    elif pct >= 95:
        rnd = "Often CAP II–IV depending on branch; keep flexible options in later rounds."
    else:
        rnd = "Plan for later CAP rounds and private / broader state options; monitor seat release each round."
    return jsonify(
        {
            "hint": rnd,
            "disclaimer": "Not a model on historical allotment — heuristic text only. Use cetcell.mahacet.org PDFs.",
        }
    )


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify({"reply": "Type a question about admissions, CAP, scholarships, or documents."})
    low = msg.lower()
    for pattern, reply in FAQ_RESPONSES:
        if re.search(pattern, low, re.I):
            return jsonify({"reply": reply})
    return jsonify(
        {
            "reply": "I match simple FAQ patterns only (demo). Try: “scholarship”, “CAP round 2”, “documents”, or use the tools in the page. For GPT-style answers, plug an API key later per your spec.",
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
