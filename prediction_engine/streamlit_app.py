"""
Streamlit UI: Maharashtra FE cutoff–based college suggestions (heuristic tiers + optional ML).

Run from repository root (Collage/):

  streamlit run prediction_engine/streamlit_app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from prediction_engine.data_loader import (
    latest_rows_per_program,
    load_cutoff_csvs,
    normalize_cutoffs,
    trend_for_selection,
)
from prediction_engine.paths import DATASET_ROOT, RESERVATION_JSON
from prediction_engine.tier_model import (
    TierConfig,
    attach_tiers,
    predict_next_year_closing,
    train_closing_regressor,
)


def _load_reservation_notes() -> dict:
    if RESERVATION_JSON.is_file():
        with RESERVATION_JSON.open(encoding="utf-8") as f:
            return json.load(f)
    return {}


def main() -> None:
    st.set_page_config(page_title="Maharashtra FE — Admission helper", layout="wide")
    st.title("Maharashtra FE — cutoff-based suggestions")
    st.caption(
        "Uses CSV files under `Maharashtra-FE-Admission-Dataset/CAP_Round_Cutoffs/`. "
        "Replace sample rows with official CAP data before relying on outputs."
    )

    raw = load_cutoff_csvs(DATASET_ROOT)
    if raw.empty:
        st.error(f"No cutoff CSV files found under `{DATASET_ROOT / 'CAP_Round_Cutoffs'}`.")
        st.stop()

    df = normalize_cutoffs(raw)

    with st.sidebar:
        st.header("Student profile")
        pct = st.slider("MHT-CET percentile (or mapped score)", 0.0, 100.0, 90.0, 0.1)
        category = st.text_input("Seat category code (e.g. GOPEN)", "GOPEN")
        quota = st.selectbox("Quota", ["MH", "AI"], index=0)
        cap_round = st.selectbox("CAP round", [1, 2, 3, 4], index=0)
        branch_q = st.text_input("Branch keyword filter", "Computer")
        district_q = st.text_input("District keyword filter (optional)", "")
        high_m = st.number_input("High-chance margin (percentile pts)", 0.0, 10.0, 2.0, 0.1)
        med_m = st.number_input("Medium band width (percentile pts)", 0.0, 10.0, 1.0, 0.1)
        st.divider()
        st.markdown("### Reservation reference")
        res = _load_reservation_notes()
        for item in res.get("categories", [])[:8]:
            st.markdown(f"**{item.get('code','')}** — {item.get('summary','')}")
        if res.get("disclaimer"):
            st.caption(res["disclaimer"])

    m = pd.Series(True, index=df.index)
    if "Seat_Category_Code" in df.columns and category.strip():
        m &= df["Seat_Category_Code"].astype(str).str.upper() == category.strip().upper()
    if "Quota_Type" in df.columns:
        m &= df["Quota_Type"].astype(str).str.upper() == quota.upper()
    if "CAP_Round" in df.columns:
        m &= pd.to_numeric(df["CAP_Round"], errors="coerce").fillna(-1) == cap_round
    if branch_q.strip() and "Program_Branch" in df.columns:
        m &= df["Program_Branch"].astype(str).str.contains(branch_q, case=False, na=False)
    if district_q.strip() and "District" in df.columns:
        m &= df["District"].astype(str).str.contains(district_q, case=False, na=False)

    filtered = df.loc[m].copy()
    if filtered.empty:
        st.warning("No rows match the current filters.")
        st.stop()

    latest = latest_rows_per_program(filtered)
    cfg = TierConfig(high_margin_pct=float(high_m), medium_low_pct=float(med_m))
    latest_scored = attach_tiers(latest, float(pct), cfg)

    st.subheader("Latest-year rows (per programme) with tiers")
    show_cols = [
        c
        for c in [
            "Academic_Year",
            "CAP_Round",
            "Quota_Type",
            "Institute_Name",
            "Program_Branch",
            "Seat_Category_Code",
            "District",
            "Closing_Percentile",
            "Tier",
            "__source_file",
        ]
        if c in latest_scored.columns
    ]
    st.dataframe(latest_scored[show_cols], use_container_width=True, hide_index=True)

    st.subheader("Trend chart (filtered history)")
    chart_df = trend_for_selection(df, m)
    if not chart_df.empty and "Closing_Percentile" in chart_df.columns:
        xcol = "__year_start" if "__year_start" in chart_df.columns else "Academic_Year"
        work = chart_df[[c for c in (xcol, "Closing_Percentile", "Institute_Name") if c in chart_df.columns]].copy()
        work = work.dropna(subset=["Closing_Percentile"])
        if "Institute_Name" in work.columns:
            top_names = work["Institute_Name"].value_counts().head(5).index.tolist()
            work = work[work["Institute_Name"].isin(top_names)]
            wide = work.pivot_table(
                index=xcol,
                columns="Institute_Name",
                values="Closing_Percentile",
                aggfunc="mean",
            ).sort_index()
            st.line_chart(wide)
        else:
            st.line_chart(work.set_index(xcol)["Closing_Percentile"].sort_index())

    st.subheader("Optional ML assist (trend regression)")
    pipe = train_closing_regressor(filtered, min_rows=10)
    if pipe is None:
        st.info("Not enough numeric rows to train the regressor (increase rows or relax filters).")
    else:
        pick = latest_scored.iloc[0]
        try:
            last_y = int(str(pick.get("Academic_Year", "2025-26")).split("-")[0])
            pred = predict_next_year_closing(pipe, pick, last_y + 1)
            st.write(
                f"Rough next-year closing estimate for **{pick.get('Institute_Name','?')}** / "
                f"**{pick.get('Program_Branch','?')}**: **{pred:.2f}** percentile (model assist only)."
            )
            st.caption(
                "This is a statistical assist on whatever CSV history is loaded — not an official forecast."
            )
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Could not produce ML projection: {exc}")


if __name__ == "__main__":
    main()
