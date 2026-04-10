from __future__ import annotations

from pathlib import Path

import pandas as pd

from prediction_engine.paths import DATASET_ROOT


def _academic_year_start(y: str) -> int:
    if not isinstance(y, str):
        return -1
    parts = y.strip().split("-")
    if len(parts) >= 1 and parts[0].isdigit():
        return int(parts[0])
    return -1


def load_cutoff_csvs(dataset_root: Path | None = None) -> pd.DataFrame:
    root = dataset_root or DATASET_ROOT
    cap_dir = root / "CAP_Round_Cutoffs"
    if not cap_dir.is_dir():
        return pd.DataFrame()

    frames: list[pd.DataFrame] = []
    for path in sorted(cap_dir.rglob("*.csv")):
        if path.name.startswith("."):
            continue
        try:
            df = pd.read_csv(path, dtype=str)
        except (OSError, UnicodeDecodeError, pd.errors.ParserError):
            continue
        df["__source_file"] = path.as_posix()
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)
    out.columns = [str(c).strip() for c in out.columns]
    return out


def normalize_cutoffs(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    d = df.copy()
    if "Closing_Percentile" in d.columns:
        d["Closing_Percentile"] = pd.to_numeric(d["Closing_Percentile"], errors="coerce")
    if "Closing_Merit" in d.columns:
        d["Closing_Merit"] = pd.to_numeric(d["Closing_Merit"], errors="coerce")
    if "CAP_Round" in d.columns:
        d["CAP_Round"] = pd.to_numeric(d["CAP_Round"], errors="coerce")
    if "Academic_Year" in d.columns:
        d["__year_start"] = d["Academic_Year"].map(_academic_year_start)
    return d


def latest_rows_per_program(
    df: pd.DataFrame,
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Keep the newest academic year per institute + branch + category + quota + round."""
    if df.empty:
        return df
    d = normalize_cutoffs(df)
    if "__year_start" not in d.columns:
        d["__year_start"] = d.get("Academic_Year", "").map(_academic_year_start)  # type: ignore[arg-type]
    gc = group_cols or [
        c
        for c in [
            "Institute_Code",
            "Institute_Name",
            "Program_Branch",
            "Seat_Category_Code",
            "Quota_Type",
            "CAP_Round",
            "District",
        ]
        if c in d.columns
    ]
    if not gc:
        return d.sort_values("__year_start").iloc[-1:].reset_index(drop=True)

    idx = d.groupby(gc, dropna=False)["__year_start"].idxmax()
    return d.loc[idx].reset_index(drop=True)


def trend_for_selection(df: pd.DataFrame, mask: pd.Series) -> pd.DataFrame:
    """Rows for charting: sorted academic years for a filtered subset."""
    sub = df.loc[mask].copy()
    if sub.empty:
        return sub
    sub = normalize_cutoffs(sub)
    sub = sub.sort_values("__year_start" if "__year_start" in sub.columns else "Academic_Year")
    return sub
