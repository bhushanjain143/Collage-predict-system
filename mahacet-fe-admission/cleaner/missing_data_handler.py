"""
Step 2 — Handle missing values with thresholds; emit ``missing_data_report.csv``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

NULL_TOKENS = frozenset(
    {
        "",
        " ",
        "n/a",
        "na",
        "not applicable",
        "-",
        "--",
        "none",
        "null",
    }
)


def normalize_string_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Map common textual null tokens to ``NaN`` (string columns only)."""
    out = df.copy()
    for col in out.columns:
        if out[col].dtype == object or pd.api.types.is_string_dtype(out[col]):
            s = out[col].astype(str).str.strip().str.lower()
            out.loc[s.isin(NULL_TOKENS), col] = np.nan
    return out


def missing_fraction(series: pd.Series) -> float:
    """Return fraction of nulls in ``series``."""
    if len(series) == 0:
        return 0.0
    return float(series.isna().mean())


def run_step(
    df: pd.DataFrame,
    report_path: Path | None = None,
    *,
    source_file: str | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Apply missing-data rules and optional report CSV.

    Returns:
        (dataframe, metrics including unreliable columns and imputation counts).
    """
    metrics: dict[str, Any] = {
        "imputed_numeric": 0,
        "imputed_categorical": 0,
        "rows_dropped_low_missing": 0,
    }
    out = normalize_string_nulls(df.copy())
    fracs = {str(c): missing_fraction(out[c]) for c in out.columns}
    report_rows = [{"column": c, "missing_pct": round(fracs[c] * 100, 4)} for c in fracs]

    unreliable = [c for c, f in fracs.items() if f > 0.30]
    low_cols = [c for c, f in fracs.items() if 0 < f < 0.05]
    mid_cols = [c for c, f in fracs.items() if 0.05 <= f <= 0.30]

    imputed_mask = pd.Series(False, index=out.index)

    if low_cols:
        before = len(out)
        out = out.dropna(subset=low_cols)
        metrics["rows_dropped_low_missing"] = before - len(out)

    for col in mid_cols:
        if pd.api.types.is_numeric_dtype(out[col]):
            mask = out[col].isna()
            med = out[col].median()
            out.loc[mask, col] = med
            metrics["imputed_numeric"] += int(mask.sum())
            imputed_mask |= mask
        else:
            mask = out[col].isna()
            mode = out[col].mode(dropna=True)
            fill = mode.iloc[0] if len(mode) else ""
            out.loc[mask, col] = fill
            metrics["imputed_categorical"] += int(mask.sum())
            imputed_mask |= mask

    out = out.reset_index(drop=True)
    imputed_mask = imputed_mask.reindex(out.index, fill_value=False)
    out["data_quality_flag"] = imputed_mask.astype(bool)
    metrics["unreliable_columns"] = unreliable

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        rep = pd.DataFrame(report_rows)
        if source_file:
            rep.insert(0, "source_file", source_file)
        if report_path.is_file():
            old = pd.read_csv(report_path)
            rep = pd.concat([old, rep], ignore_index=True)
        rep.to_csv(report_path, index=False)
        logger.info("Updated missing data report: %s", report_path)

    return out, metrics
