"""
Step 1 — Remove duplicate rows and ultra-sparse columns.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

KEY_CANDIDATES = [
    ("college_code", "Institute_Code", "institute_code"),
    ("Seat_Category_Code", "seat_category_code", "category"),
    ("CAP_Round", "cap_round", "round"),
    ("Academic_Year", "academic_year", "year"),
    ("Program_Branch", "program_branch", "branch_code", "branch"),
]


def _pick_col(df: pd.DataFrame, names: tuple[str, ...]) -> str | None:
    """Return the first existing column name from ``names``."""
    lower = {c.lower(): c for c in df.columns}
    for n in names:
        if n in df.columns:
            return n
        if n.lower() in lower:
            return lower[n.lower()]
    return None


def build_composite_key(df: pd.DataFrame) -> list[str]:
    """Resolve composite-key columns present in ``df``."""
    keys: list[str] = []
    for group in KEY_CANDIDATES:
        c = _pick_col(df, group)
        if c:
            keys.append(c)
    return keys


def drop_sparse_columns(df: pd.DataFrame, null_threshold: float = 0.9) -> tuple[pd.DataFrame, list[str]]:
    """
    Drop columns where more than ``null_threshold`` fraction of values are null.

    Returns:
        (dataframe, list of dropped column names).
    """
    if df.empty:
        return df, []
    dropped: list[str] = []
    keep: list[str] = []
    n = len(df)
    for col in df.columns:
        frac = df[col].isna().mean() if n else 0.0
        if frac > null_threshold:
            dropped.append(str(col))
        else:
            keep.append(col)
    if dropped:
        logger.info("Dropping sparse columns (>%.0f%% null): %s", null_threshold * 100, dropped)
    return df[keep].copy(), dropped


def drop_index_like_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Remove obvious auto-index columns."""
    patterns = ("unnamed", "index", "serial", "s.no", "sr no")
    drop: list[str] = []
    for c in df.columns:
        cl = str(c).strip().lower()
        if any(p in cl for p in patterns):
            drop.append(c)
    if drop:
        logger.info("Dropping index-like columns: %s", drop)
    return df.drop(columns=drop, errors="ignore").copy(), drop


def deduplicate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Drop exact duplicate rows using composite key when possible, else all columns.

    Returns:
        (cleaned dataframe, number of duplicate rows removed).
    """
    if df.empty:
        return df, 0
    keys = build_composite_key(df)
    before = len(df)
    if keys:
        dedup = df.drop_duplicates(subset=keys, keep="first")
    else:
        dedup = df.drop_duplicates(keep="first")
    removed = before - len(dedup)
    if removed:
        logger.info("Removed %s duplicate rows (keys=%s)", removed, keys or "all-columns")
    return dedup.reset_index(drop=True), removed


def run_step(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Run deduplication and sparsity pruning.

    Returns:
        (dataframe, metrics dict).
    """
    metrics: dict[str, Any] = {}
    out, dropped_sparse = drop_sparse_columns(df)
    out, dropped_idx = drop_index_like_columns(out)
    out, dup_removed = deduplicate_rows(out)
    metrics["duplicates_removed"] = dup_removed
    metrics["sparse_columns_dropped"] = dropped_sparse
    metrics["index_columns_dropped"] = dropped_idx
    return out, metrics
