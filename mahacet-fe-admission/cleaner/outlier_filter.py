"""
Step 4 — IQR and Z-score based outlier handling with audit log.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

IQR_COLS = ("cutoff_rank", "percentile", "Closing_Percentile", "open_rank", "category_rank")
Z_COLS = ("annual_fees_inr", "total_intake", "annual_fees", "fees")


def _find_col(df: pd.DataFrame, names: tuple[str, ...]) -> str | None:
    lower = {c.lower(): c for c in df.columns}
    for n in names:
        if n in df.columns:
            return n
        if n.lower() in lower:
            return lower[n.lower()]
    return None


def iqr_bounds(series: pd.Series) -> tuple[float, float] | None:
    """Return (lower, upper) for 1.5 * IQR rule; None if not computable."""
    s = series.dropna()
    if len(s) < 4:
        return None
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    if not np.isfinite(iqr) or iqr == 0:
        return None
    return float(q1 - 1.5 * iqr), float(q3 + 1.5 * iqr)


def apply_iqr(
    df: pd.DataFrame,
    col: str,
    file_name: str,
    log_rows: list[dict[str, Any]],
) -> pd.DataFrame:
    """Cap/remove outliers for ``col`` using IQR; append to ``log_rows``."""
    out = df.copy()
    bounds = iqr_bounds(pd.to_numeric(out[col], errors="coerce"))
    if bounds is None:
        return out
    lo, hi = bounds
    vals = pd.to_numeric(out[col], errors="coerce")
    for idx in out.index:
        v = vals.loc[idx]
        if pd.isna(v):
            continue
        if v < lo or v > hi:
            # Heuristic: extreme far from bounds → remove; mild → cap
            if v < lo - 2 * (lo if lo != 0 else 1) or v > hi + 2 * (hi if hi != 0 else 1):
                action = "removed"
                out.loc[idx, col] = np.nan
            else:
                action = "capped"
                out.loc[idx, col] = lo if v < lo else hi
            log_rows.append(
                {
                    "file_name": file_name,
                    "row_index": int(idx),
                    "column": col,
                    "original_value": float(v),
                    "action_taken": action,
                    "method": "IQR",
                }
            )
    return out


def apply_zscore(
    df: pd.DataFrame,
    col: str,
    file_name: str,
    log_rows: list[dict[str, Any]],
) -> pd.DataFrame:
    """Flag/cap Z-score outliers for fee/intake columns."""
    out = df.copy()
    vals = pd.to_numeric(out[col], errors="coerce")
    s = vals.dropna()
    if len(s) < 3:
        return out
    mu = s.mean()
    sigma = s.std(ddof=0)
    if sigma == 0 or not np.isfinite(sigma):
        return out
    z = (vals - mu) / sigma
    for idx in out.index:
        zz = z.loc[idx]
        if pd.isna(zz) or abs(zz) <= 3:
            continue
        v = float(vals.loc[idx])
        cap = mu + 3 * sigma * np.sign(zz)
        action = "capped" if abs(zz) < 6 else "removed"
        if action == "capped":
            out.loc[idx, col] = cap
        else:
            out.loc[idx, col] = np.nan
        log_rows.append(
            {
                "file_name": file_name,
                "row_index": int(idx),
                "column": col,
                "original_value": v,
                "action_taken": action,
                "method": "ZSCORE",
            }
        )
    return out


def run_step(
    df: pd.DataFrame,
    file_name: str,
    log_path: Path | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Apply IQR / Z-score rules and optionally append to ``outlier_log.csv``.

    Returns:
        (dataframe, metrics).
    """
    log_rows: list[dict[str, Any]] = []
    out = df.copy()

    for group in IQR_COLS:
        col = _find_col(out, (group,))
        if col:
            out = apply_iqr(out, col, file_name, log_rows)

    for group in Z_COLS:
        col = _find_col(out, (group,))
        if col:
            out = apply_zscore(out, col, file_name, log_rows)

    if log_path is not None and log_rows:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        new = pd.DataFrame(log_rows)
        if log_path.is_file():
            old = pd.read_csv(log_path)
            pd.concat([old, new], ignore_index=True).to_csv(log_path, index=False)
        else:
            new.to_csv(log_path, index=False)
        logger.info("Appended %s outlier log entries to %s", len(log_rows), log_path)

    return out, {"outlier_events": len(log_rows)}
