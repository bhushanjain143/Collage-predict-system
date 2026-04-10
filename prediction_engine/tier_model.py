from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

try:
    from xgboost import XGBRegressor

    _HAS_XGB = True
except ImportError:
    _HAS_XGB = False


@dataclass
class TierConfig:
    high_margin_pct: float = 2.0
    medium_low_pct: float = 1.0


def heuristic_tier(student_percentile: float, closing_percentile: float, cfg: TierConfig) -> str:
    """
    Compare student MHT-CET percentile to published closing percentile.

    Higher student percentile is better in typical MHT-CET percentile scales used in CAP tables
    (always confirm against the official document for the exact metric).
    """
    if closing_percentile is None or (isinstance(closing_percentile, float) and np.isnan(closing_percentile)):
        return "Unknown"
    if student_percentile >= closing_percentile + cfg.high_margin_pct:
        return "High chance"
    if student_percentile >= closing_percentile - cfg.medium_low_pct:
        return "Medium chance"
    return "Low chance"


def attach_tiers(
    df: pd.DataFrame,
    student_percentile: float,
    cfg: TierConfig | None = None,
) -> pd.DataFrame:
    cfg = cfg or TierConfig()
    out = df.copy()
    if "Closing_Percentile" not in out.columns:
        out["Tier"] = "Unknown"
        return out

    out["Tier"] = [
        heuristic_tier(student_percentile, float(x) if pd.notna(x) else float("nan"), cfg)
        for x in out["Closing_Percentile"]
    ]
    return out


def train_closing_regressor(df: pd.DataFrame, min_rows: int = 24) -> Pipeline | None:
    """
    Predict Closing_Percentile from history features (rough trend assist).

    Returns None if there is not enough clean data.
    """
    d = df.copy()
    if "Closing_Percentile" not in d.columns or "Academic_Year" not in d.columns:
        return None
    d["Closing_Percentile"] = pd.to_numeric(d["Closing_Percentile"], errors="coerce")
    d = d.dropna(subset=["Closing_Percentile"])
    if len(d) < min_rows:
        return None

    def year_start(s: str) -> int:
        parts = str(s).split("-")
        return int(parts[0]) if parts and parts[0].isdigit() else 0

    d["__y0"] = d["Academic_Year"].map(year_start)
    d["CAP_Round"] = pd.to_numeric(d.get("CAP_Round", 1), errors="coerce").fillna(1)

    cat_cols = [c for c in ("Quota_Type", "Seat_Category_Code", "Program_Branch") if c in d.columns]
    num_cols = ["__y0", "CAP_Round"]
    X = d[cat_cols + num_cols].copy()
    y = d["Closing_Percentile"].astype(float)

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )
    if _HAS_XGB:
        model = XGBRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
        )
    else:
        model = RandomForestRegressor(
            n_estimators=400,
            max_depth=8,
            random_state=42,
            n_jobs=-1,
        )

    pipe = Pipeline([("prep", pre), ("reg", model)])
    pipe.fit(X, y)
    return pipe


def predict_next_year_closing(pipe: Pipeline, template_row: pd.Series, next_year_start: int) -> float:
    """Use one representative row to project closing for a future academic year start (e.g. 2026 for 2026-27)."""
    cat_cols = [c for c in ("Quota_Type", "Seat_Category_Code", "Program_Branch") if c in template_row.index]
    num_cols = ["__y0", "CAP_Round"]
    row = {c: template_row.get(c, "") for c in cat_cols}
    row["__y0"] = int(next_year_start)
    row["CAP_Round"] = int(pd.to_numeric(template_row.get("CAP_Round", 1), errors="coerce") or 1)
    Xp = pd.DataFrame([row])
    return float(pipe.predict(Xp)[0])
