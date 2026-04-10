"""
Streamlit recommendation UI for MAHACET FE admission assist (model + heuristics).

Production-oriented defaults: ``@st.cache_data`` for I/O, optional ``MAHA_LOG_LEVEL``,
and lightweight HTML rendering for tier colors (values are HTML-escaped).
"""

from __future__ import annotations

import html as html_module
import json
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings
from model import feature_engineering
from model.predict import load_feature_meta, load_pipeline, predict_batch

SCHOLARSHIP_UI = frozenset({"EWS", "TFWS", "SC", "ST", "OBC", "NT", "EBC"})


def seat_category_mask(series: pd.Series, ui_category: str) -> pd.Series:
    """
    Map coarse UI categories (OPEN, SC, …) to typical CAP ``Seat_Category_Code`` patterns.

    This is a heuristic filter — prefer exact codes from official seat matrix when available.
    """
    s = series.astype(str).str.strip().str.upper()
    u = ui_category.strip().upper()
    if u == "OPEN":
        return s.str.endswith("OPEN") | s.eq("GEN")
    if u == "SC":
        return s.str.contains("SC") & ~s.str.contains("OBC")
    if u == "ST":
        return s.str.contains("ST") & ~s.str.contains("OBC")
    if u == "OBC":
        return s.str.contains("OBC")
    if u == "NT":
        return s.str.contains("NT")
    if u == "EWS":
        return s.str.contains("EWS")
    if u == "EBC":
        return s.str.contains("EBC")
    if u == "TFWS":
        return s.str.contains("TFWS")
    return s.eq(u)


def _cleaning_summary_ts() -> str:
    p = settings.DATA_DIR / "Data_Quality_Logs" / "cleaning_summary.json"
    if not p.is_file():
        return "unknown"
    try:
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        return str(data.get("generated_at_utc", "unknown"))
    except (OSError, json.JSONDecodeError):
        return "unknown"


def _discovered_url() -> str:
    return settings.get_active_portal_url()


@st.cache_data(show_spinner=False)
def _load_cap_tables_cached() -> pd.DataFrame:
    return feature_engineering.load_cap_tables()


@st.cache_data(show_spinner=False)
def _load_college_fees_cached() -> pd.DataFrame:
    p = settings.DATA_DIR / "College_Details"
    if not p.is_dir():
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    for f in p.glob("College_Details_*.csv"):
        if "links" in f.name:
            continue
        try:
            frames.append(pd.read_csv(f, low_memory=False))
        except (OSError, pd.errors.ParserError):
            continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


@st.cache_resource
def _cached_pipe():
    """Load sklearn pipeline once per process."""
    return load_pipeline()


def cutoff_trend_label(df_prog: pd.DataFrame) -> str:
    """Short text trend from last two academic years' mean closing percentile."""
    if df_prog.empty or "Closing_Percentile" not in df_prog.columns:
        return "—"
    g = df_prog.dropna(subset=["Closing_Percentile"])
    if "Academic_Year" in g.columns:
        g = g.sort_values("Academic_Year")
    vals = pd.to_numeric(g["Closing_Percentile"], errors="coerce").dropna()
    if len(vals) < 2:
        return f"{vals.iloc[-1]:.1f}" if len(vals) else "—"
    a, b = float(vals.iloc[-2]), float(vals.iloc[-1])
    if b > a:
        return f"↑ {b:.1f} vs {a:.1f}"
    if b < a:
        return f"↓ {b:.1f} vs {a:.1f}"
    return f"→ {b:.1f}"


def build_prediction_frame(
    cap_df: pd.DataFrame,
    *,
    percentile: float,
    ui_category: str,
    quota: str,
    cap_round: int,
    branch_filters: list[str],
    districts: list[str],
) -> pd.DataFrame:
    """Merge user profile with historical CAP rows for model input."""
    df = feature_engineering.add_rolling_cutoff_features(cap_df.copy())
    m = pd.Series(True, index=df.index)
    if branch_filters and "Program_Branch" in df.columns:
        pat = "|".join(re.escape(b) for b in branch_filters)
        m &= df["Program_Branch"].astype(str).str.contains(pat, case=False, na=False)
    if districts and "Any" not in districts and "District" in df.columns:
        m &= df["District"].astype(str).isin(districts)
    if "Quota_Type" in df.columns:
        m &= df["Quota_Type"].astype(str).str.upper() == quota.upper()
    if "Seat_Category_Code" in df.columns:
        m &= seat_category_mask(df["Seat_Category_Code"], ui_category)
    if "CAP_Round" in df.columns:
        m &= pd.to_numeric(df["CAP_Round"], errors="coerce").fillna(-1) == cap_round

    sub = df.loc[m].copy()
    if sub.empty:
        return sub

    sub["student_percentile"] = float(percentile)
    sub["student_category"] = ui_category.lower()
    sub["preferred_branch"] = sub["Program_Branch"].astype(str)
    sub["CAP_Round"] = int(cap_round)
    sub["Quota_Type"] = quota.upper()
    sub["college_location_district"] = sub["District"].astype(str) if "District" in sub.columns else "unknown"
    sub["seat_availability_ratio"] = 0.85
    sub["vacancy_flag"] = False
    return sub


def results_to_html_table(df: pd.DataFrame) -> str:
    """Render a compact HTML table with row background by chance tier."""
    cols = list(df.columns)
    headers = "".join(f"<th>{html_module.escape(c)}</th>" for c in cols)
    rows_html: list[str] = []
    tier_col = "Chance" if "Chance" in df.columns else None
    for _, row in df.iterrows():
        tier = str(row[tier_col]) if tier_col else ""
        if "High" in tier:
            bg = "#d3f9d8"
        elif "Medium" in tier:
            bg = "#fff3bf"
        else:
            bg = "#ffe3e3"
        cells = "".join(f"<td>{html_module.escape(str(row[c]))}</td>" for c in cols)
        rows_html.append(f"<tr style='background-color:{bg}'>{cells}</tr>")
    return (
        "<div style='overflow-x:auto;width:100%'>"
        f"<table style='border-collapse:collapse;font-size:14px;width:100%'>"
        f"<thead><tr>{headers}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody></table></div>"
    )


def try_build_pdf_bytes(df: pd.DataFrame) -> bytes | None:
    """Build a minimal PDF table if ``fpdf2`` is installed."""
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=8)
    pdf.add_page()
    pdf.set_font("Helvetica", size=7)
    for _, row in df.head(40).iterrows():
        line = " | ".join(str(x)[:40] for x in row.values)
        pdf.multi_cell(0, 4, line)
    raw = pdf.output(dest="S")
    if isinstance(raw, str):
        return raw.encode("latin-1", errors="replace")
    return bytes(raw)


def main() -> None:
    st.set_page_config(page_title="MAHACET FE — Recommendations", layout="wide", initial_sidebar_state="expanded")
    st.markdown(
        "<style>section[data-testid='stSidebar']>div:first-child{padding-top:0.5rem}</style>",
        unsafe_allow_html=True,
    )
    st.title("Maharashtra FE — college suggestions")
    st.caption(
        f"Data last cleaned (UTC): **{_cleaning_summary_ts()}** · "
        f"Active portal: `{_discovered_url()}` · "
        f"Year label: **{settings.ADMISSION_PORTAL_YEAR}**"
    )

    cap = _load_cap_tables_cached()
    if cap.empty:
        st.error("No CAP CSV data found under `data/CAP_Round_Cutoffs/`. Run the scraper and cleaner first.")
        st.stop()

    branches = sorted({str(x) for x in cap["Program_Branch"].dropna().unique()}) if "Program_Branch" in cap.columns else []
    dists = sorted({str(x) for x in cap["District"].dropna().unique()}) if "District" in cap.columns else []

    with st.sidebar:
        st.header("Student profile")
        pct = st.slider("MHT-CET percentile", 0.0, 100.0, 90.0, 0.05)
        jee = st.number_input("JEE Main rank (optional)", min_value=0, value=0, step=1)
        ui_cat = st.selectbox(
            "Category",
            ["OPEN", "SC", "ST", "OBC", "NT", "EWS", "EBC", "TFWS"],
            index=0,
        )
        branch_sel = st.multiselect("Preferred branch (multi)", branches, default=branches[:1] if branches else [])
        district_sel = st.multiselect("District preference", ["Any"] + dists, default=["Any"])
        quota = st.selectbox("Quota type", ["MH State", "All India"], index=0)
        quota_code = "MH" if quota.startswith("MH") else "AI"
        rnd = st.selectbox("CAP round", [1, 2, 3, 4], index=0)

    fee_df = _load_college_fees_cached()

    try:
        pipe = _cached_pipe()
    except FileNotFoundError:
        st.warning("Trained model not found. Run `python model/train_model.py` after adding data.")
        st.stop()

    dsel = [d for d in district_sel if d != "Any"]
    pred_input = build_prediction_frame(
        cap,
        percentile=pct,
        ui_category=ui_cat,
        quota=quota_code,
        cap_round=int(rnd),
        branch_filters=branch_sel,
        districts=dsel,
    )
    if pred_input.empty:
        st.warning("No rows match filters — relax branch, district, or category filters.")
        st.stop()

    feat_meta = load_feature_meta()
    feat_cols = feat_meta.get("feature_columns")
    if not feat_cols:
        st.error("features.json missing feature_columns. Retrain the model.")
        st.stop()

    X = pred_input.reindex(columns=list(feat_cols))
    for c in ("historical_cutoff_mean_3yr", "historical_cutoff_std_3yr"):
        if c in X.columns:
            X[c] = pd.to_numeric(X[c], errors="coerce").fillna(0.0)
    if "CAP_Round" in X.columns:
        X["CAP_Round"] = pd.to_numeric(X["CAP_Round"], errors="coerce").fillna(int(rnd)).astype(int)
    if "student_percentile" in X.columns:
        X["student_percentile"] = pd.to_numeric(X["student_percentile"], errors="coerce")
    if "seat_availability_ratio" in X.columns:
        X["seat_availability_ratio"] = pd.to_numeric(X["seat_availability_ratio"], errors="coerce").fillna(0.85)

    out = predict_batch(pipe, X)
    merged = pred_input.reset_index(drop=True).join(
        out[["admission_probability", "prediction_proba", "chance_tier"]],
    )
    merged = merged.sort_values("admission_probability", ascending=False)

    ctype_col = None
    for c in ("college_type", "College_Type", "institute_type"):
        if c in fee_df.columns:
            ctype_col = c
            break
    if ctype_col and "Institute_Code" in merged.columns and "college_code" in fee_df.columns:
        fees = fee_df.rename(columns={"college_code": "Institute_Code"})
        keep = ["Institute_Code", ctype_col] + (
            ["annual_fees_inr"] if "annual_fees_inr" in fees.columns else []
        )
        merged = merged.merge(fees[[c for c in keep if c in fees.columns]], on="Institute_Code", how="left")
        merged.rename(columns={ctype_col: "College_Type"}, inplace=True)
    else:
        merged["College_Type"] = "—"

    fee_col = "annual_fees_inr" if "annual_fees_inr" in merged.columns else None

    trend_labels: list[str] = []
    for _, r in merged.iterrows():
        sub = cap
        if "Institute_Name" in cap.columns:
            sub = sub[sub["Institute_Name"] == r.get("Institute_Name")]
        if "Program_Branch" in sub.columns:
            sub = sub[sub["Program_Branch"] == r.get("Program_Branch")]
        trend_labels.append(cutoff_trend_label(sub))
    merged["Cutoff_Trend"] = trend_labels

    sch = ui_cat in SCHOLARSHIP_UI
    merged["Scholarship_Eligible"] = sch

    view = pd.DataFrame(
        {
            "College Name": merged.get("Institute_Name", "—"),
            "Branch": merged.get("Program_Branch", "—"),
            "District": merged.get("District", "—"),
            "Type": merged.get("College_Type", "—"),
            "Cutoff Trend": merged.get("Cutoff_Trend", "—"),
            "Prediction": merged["admission_probability"].round(3),
            "Chance": merged["chance_tier"],
            "Fees": merged[fee_col] if fee_col else "—",
            "Scholarship Eligible": merged["Scholarship_Eligible"],
        }
    )

    st.subheader("Ranked suggestions")
    st.markdown(results_to_html_table(view), unsafe_allow_html=True)

    if sch:
        st.markdown("**Scholarship:** likely relevant schemes — verify on [CET Cell](https://cetcell.mahacet.org/). 🏷️")

    st.subheader("Reservation quota (summary)")
    st.markdown(
        "- **OPEN / SC / ST / OBC / NT / EWS / EBC / TFWS** map heuristically to CAP seat codes in your CSV.\n"
        "- Minority / institute / defence / PWD sub-quotas follow the **official brochure** only."
    )

    if jee > 0:
        st.info("JEE rank stored for your records; the bundled model uses MHT-CET percentile + CAP history.")

    names = merged["Institute_Name"].dropna().unique().tolist() if "Institute_Name" in merged.columns else []
    branches_pick = merged["Program_Branch"].dropna().unique().tolist() if "Program_Branch" in merged.columns else []
    if names and branches_pick:
        c1, c2 = st.columns(2)
        with c1:
            pick = st.selectbox("College for trend chart", names)
        with c2:
            bpick = st.selectbox("Branch for trend chart", branches_pick)
        sub_trend = cap[(cap["Institute_Name"] == pick) & (cap["Program_Branch"] == bpick)]
        if not sub_trend.empty and "Closing_Percentile" in sub_trend.columns and "Academic_Year" in sub_trend.columns:
            g = sub_trend.assign(__y=sub_trend["Academic_Year"].astype(str))
            chart = g.groupby("__y", as_index=False)["Closing_Percentile"].mean()
            st.line_chart(chart.set_index("__y"))

    csv_bytes = merged.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Export CSV", data=csv_bytes, file_name="mahacet_fe_suggestions.csv", mime="text/csv")

    pdf_bytes = try_build_pdf_bytes(view)
    if pdf_bytes:
        st.download_button("Export PDF (summary)", data=pdf_bytes, file_name="mahacet_fe_suggestions.pdf", mime="application/pdf")
    else:
        st.caption("Install `fpdf2` (`pip install fpdf2`) to enable PDF export.")


if __name__ == "__main__":
    main()
