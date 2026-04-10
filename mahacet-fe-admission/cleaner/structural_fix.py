"""
Step 5 — Structural fixes: null unification, college types, branch synonyms, code validation.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

BRANCH_MAP = {
    "computer engg": "computer engineering",
    "computer engineering": "computer engineering",
    "comp": "computer engineering",
    "ce": "computer engineering",
    "cse": "computer engineering",
    "information technology": "information technology",
    "information tech": "information technology",
    "info tech": "information technology",
    "it": "information technology",
    "mechanical engg": "mechanical engineering",
    "mechanical engineering": "mechanical engineering",
    "mech": "mechanical engineering",
}

COLLEGE_TYPE_MAP = {
    "pvt": "private",
    "private": "private",
    "govt": "government",
    "government": "government",
    "govt.": "government",
    "auto": "autonomous",
    "autonomous": "autonomous",
}


def unify_null_representations(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize assorted textual nulls to ``NaN``."""
    out = df.copy()
    tokens = {"", "n/a", "na", "not applicable", "-", "--", " ", "none"}
    for col in out.columns:
        if col == "data_quality_flag":
            continue
        if out[col].dtype == object or pd.api.types.is_string_dtype(out[col]):
            s = out[col].astype(str).str.strip().str.lower()
            out.loc[s.isin(tokens), col] = np.nan
    return out


def fix_college_types(series: pd.Series) -> pd.Series:
    """Normalize college type labels."""
    s = series.astype(str).str.strip().str.lower()
    return s.replace(COLLEGE_TYPE_MAP)


def fix_branch_names(series: pd.Series) -> pd.Series:
    """Map common branch abbreviations to canonical phrases."""
    s = series.astype(str).str.strip().str.lower()
    return s.replace(BRANCH_MAP)


def validate_college_codes(
    df: pd.DataFrame,
    master_csv: Path,
    errors_csv: Path,
    *,
    source_file: str = "",
) -> int:
    """
    Compare ``college_code`` / ``Institute_Code`` against ``master_csv``.

    Returns:
        Number of mismatches logged.
    """
    code_col = None
    for c in df.columns:
        if c.lower() in ("college_code", "institute_code"):
            code_col = c
            break
    if code_col is None or not master_csv.is_file():
        return 0
    master = pd.read_csv(master_csv, dtype=str)
    if "college_code" not in master.columns or master.empty:
        return 0
    valid = set(master["college_code"].astype(str).str.strip())
    if not valid:
        return 0
    bad_rows: list[dict[str, Any]] = []
    for idx, val in df[code_col].items():
        v = str(val).strip()
        if pd.isna(val) or v == "" or v in valid:
            continue
        bad_rows.append({"source_file": source_file, "row_index": int(idx), "invalid_code": v})
    if bad_rows:
        errors_csv.parent.mkdir(parents=True, exist_ok=True)
        new = pd.DataFrame(bad_rows)
        if errors_csv.is_file():
            old = pd.read_csv(errors_csv)
            new = pd.concat([old, new], ignore_index=True)
        new.to_csv(errors_csv, index=False)
        logger.warning("Logged %s structural code issues to %s", len(bad_rows), errors_csv)
    return len(bad_rows)


def run_step(
    df: pd.DataFrame,
    master_csv: Path,
    errors_csv: Path,
    *,
    source_file: str = "",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Apply structural normalization and validation."""
    metrics: dict[str, Any] = {}
    out = unify_null_representations(df)
    type_cols = [c for c in out.columns if "type" in c.lower() and "college" in c.lower()]
    for c in type_cols:
        out[c] = fix_college_types(out[c])
    branch_cols = [c for c in out.columns if "branch" in c.lower() or "program" in c.lower()]
    for c in branch_cols:
        if c != "data_quality_flag":
            out[c] = fix_branch_names(out[c])
    metrics["code_mismatches"] = validate_college_codes(
        out, master_csv, errors_csv, source_file=source_file
    )
    return out, metrics
