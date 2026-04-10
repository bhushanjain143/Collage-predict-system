"""
Step 3 — Standardize string casing, categories, dates, numeric ranks/fees, booleans.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

BOOL_TRUE = frozenset({"yes", "y", "true", "1", "t"})
BOOL_FALSE = frozenset({"no", "n", "false", "0", "f"})


def lowercase_strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip whitespace for object/string columns."""
    out = df.copy()
    for col in out.columns:
        if col == "data_quality_flag":
            continue
        if out[col].dtype == object or pd.api.types.is_string_dtype(out[col]):
            out[col] = (
                out[col]
                .astype(str)
                .map(lambda x: x.strip().lower() if x not in ("nan", "NaT") else x)
            )
            out[col] = out[col].replace({"nan": pd.NA})
    return out


def normalize_college_names(series: pd.Series) -> pd.Series:
    """Normalize punctuation and common honorifics in institute names."""
    s = series.astype(str)
    s = s.str.replace(r"\.", "", regex=True)
    s = s.str.replace(r"\s+", " ", regex=True)
    s = s.str.strip().str.lower()
    s = s.str.replace(r"^dr\.?\s+", "dr ", regex=True)
    s = s.str.replace(r"\bi\.?\s*i\.?\s*t\.?\b", "iit", regex=True)
    return s


def normalize_category_codes(series: pd.Series) -> pd.Series:
    """Map common category spellings to canonical lowercase tokens."""
    m = {
        "o.b.c": "obc",
        "obc": "obc",
        "open": "open",
        "general": "open",
        "gen": "open",
        "gopen": "open",
        "lopen": "open",
        "sc": "sc",
        "st": "st",
        "ews": "ews",
        "tfws": "tfws",
    }
    out = series.astype(str).str.strip().str.lower()
    return out.replace(m)


def parse_dates(series: pd.Series) -> pd.Series:
    """Coerce parsable date strings to ``datetime64[ns]``."""
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def cast_rank_percentile(df: pd.DataFrame, cols: tuple[str, ...]) -> pd.DataFrame:
    """Cast known rank/percentile columns to numeric."""
    out = df.copy()
    lower = {c.lower(): c for c in out.columns}
    for name in cols:
        col = name if name in out.columns else lower.get(name.lower())
        if col and col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def normalize_fees(series: pd.Series) -> pd.Series:
    """Strip INR symbols/commas and cast to float."""
    s = series.astype(str).str.replace(r"[₹,]", "", regex=True)
    s = s.str.replace(r"[^\d.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def normalize_booleans(series: pd.Series) -> pd.Series:
    """Map yes/no variants to bool; leave unmapped as NA."""
    s = series.astype(str).str.strip().str.lower()
    out = pd.Series(pd.NA, index=s.index, dtype="boolean")
    out = out.mask(s.isin(BOOL_TRUE), True)
    out = out.mask(s.isin(BOOL_FALSE), False)
    return out


def run_step(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Apply standardization transforms."""
    metrics: dict[str, Any] = {"columns_date_parsed": [], "columns_fee_parsed": []}
    out = lowercase_strip_strings(df)

    name_cols = [c for c in out.columns if "institute" in c.lower() or "college" in c.lower()]
    for c in name_cols:
        if c != "data_quality_flag":
            out[c] = normalize_college_names(out[c])

    cat_cols = [c for c in out.columns if "category" in c.lower() or c.lower() in ("quota_type",)]
    for c in cat_cols:
        out[c] = normalize_category_codes(out[c])

    date_cols = [c for c in out.columns if "date" in c.lower()]
    for c in date_cols:
        out[c] = parse_dates(out[c])
        metrics["columns_date_parsed"].append(c)

    out = cast_rank_percentile(
        out,
        (
            "Closing_Merit",
            "Closing_Percentile",
            "cutoff_rank",
            "percentile",
            "open_rank",
            "category_rank",
        ),
    )

    fee_cols = [c for c in out.columns if "fee" in c.lower()]
    for c in fee_cols:
        out[c] = normalize_fees(out[c])
        metrics["columns_fee_parsed"].append(c)

    bool_cols = [c for c in out.columns if "hostel" in c.lower() or "eligible" in c.lower()]
    for c in bool_cols:
        out[c] = normalize_booleans(out[c])

    return out, metrics
