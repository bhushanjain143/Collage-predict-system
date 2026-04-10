"""
Build model feature matrix from cleaned cutoff CSVs under ``data/CAP_Round_Cutoffs``.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings

logger = logging.getLogger(__name__)


def _year_start(s: Any) -> int:
    parts = str(s).split("-")
    return int(parts[0]) if parts and parts[0].isdigit() else 0


def load_cap_tables(data_root: Path | None = None) -> pd.DataFrame:
    """Load and concatenate all CAP cutoff CSV files."""
    root = data_root or settings.DATA_DIR
    cap_dir = root / "CAP_Round_Cutoffs"
    if not cap_dir.is_dir():
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    for p in sorted(cap_dir.rglob("*.csv")):
        if "manifest" in p.parts:
            continue
        try:
            frames.append(pd.read_csv(p, low_memory=False))
        except (OSError, pd.errors.ParserError):
            continue
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out.columns = [str(c).strip() for c in out.columns]
    return out


def add_rolling_cutoff_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add ``historical_cutoff_mean_3yr`` and ``historical_cutoff_std_3yr`` per programme group.

    Uses ``Closing_Percentile`` when present; otherwise attempts ``cutoff_rank`` inverted
    (not applied — requires domain-specific mapping).
    """
    if df.empty or "Closing_Percentile" not in df.columns:
        df = df.copy()
        df["historical_cutoff_mean_3yr"] = np.nan
        df["historical_cutoff_std_3yr"] = np.nan
        return df

    d = df.copy()
    if "Academic_Year" in d.columns:
        d["__y0"] = d["Academic_Year"].map(_year_start)
    else:
        d["__y0"] = 0

    group_cols = [
        c
        for c in (
            "Institute_Code",
            "Institute_Name",
            "Program_Branch",
            "Seat_Category_Code",
            "Quota_Type",
            "CAP_Round",
        )
        if c in d.columns
    ]
    if not group_cols:
        d["historical_cutoff_mean_3yr"] = d["Closing_Percentile"]
        d["historical_cutoff_std_3yr"] = 0.0
        return d

    d["Closing_Percentile"] = pd.to_numeric(d["Closing_Percentile"], errors="coerce")
    d = d.sort_values(["__y0"])
    g = d.groupby(group_cols, dropna=False)["Closing_Percentile"]
    d["historical_cutoff_mean_3yr"] = g.transform(lambda s: s.rolling(3, min_periods=1).mean())
    d["historical_cutoff_std_3yr"] = g.transform(lambda s: s.rolling(3, min_periods=1).std())
    return d


def augment_student_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create synthetic training rows with ``student_percentile`` and binary admission label.

    Label is ``1`` when synthetic percentile is at/above the programme closing percentile,
    else ``0``, with small jitter for separability.
    """
    if df.empty:
        return df
    base = add_rolling_cutoff_features(df)
    if "Closing_Percentile" not in base.columns:
        logger.warning("No Closing_Percentile column — cannot augment training rows.")
        return pd.DataFrame()

    rows: list[pd.Series] = []
    for _, r in base.iterrows():
        close = r["Closing_Percentile"]
        if pd.isna(close):
            continue
        close = float(close)
        for noise in (-6.0, -1.0, 2.0, 8.0):
            sp = float(np.clip(close + noise, 0.0, 100.0))
            rr = r.copy()
            rr["student_percentile"] = sp
            rr["student_category"] = rr.get("Seat_Category_Code", "open")
            rr["preferred_branch"] = rr.get("Program_Branch", "unknown")
            rr["college_location_district"] = rr.get("District", "unknown")
            rr["seat_availability_ratio"] = 0.85
            rr["vacancy_flag"] = bool(rr.get("vacancy_flag", False))
            rr["admission_label"] = int(sp >= close - 0.5)
            rows.append(rr)
    return pd.DataFrame(rows)


def build_feature_matrix(
    data_root: Path | None = None,
) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Build ``X`` (numeric + categorical columns for encoding downstream) and ``y``.

    Returns:
        (features_df, y_series, feature_column_names).
    """
    raw = load_cap_tables(data_root)
    aug = augment_student_rows(raw)
    if aug.empty:
        return pd.DataFrame(), pd.Series(dtype=int), []

    feature_cols = [
        "student_percentile",
        "student_category",
        "preferred_branch",
        "CAP_Round",
        "Quota_Type",
        "college_location_district",
        "historical_cutoff_mean_3yr",
        "historical_cutoff_std_3yr",
        "seat_availability_ratio",
        "vacancy_flag",
    ]
    present = [c for c in feature_cols if c in aug.columns]
    X = aug[present].copy()
    y = aug["admission_label"].astype(int)
    return X, y, present


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry: build the feature matrix and log shapes (used in CI before ``train_model``).
    """
    import argparse

    lvl = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Build MAHACET FE model feature matrix.")
    p.add_argument("--data-dir", type=Path, default=None, help="Override data root.")
    args = p.parse_args(argv)
    X, y, cols = build_feature_matrix(args.data_dir)
    logger.info("Built features: X.shape=%s y.len=%s columns=%s", getattr(X, "shape", None), len(y), cols)
    return 0 if not X.empty else 1


if __name__ == "__main__":
    raise SystemExit(main())
