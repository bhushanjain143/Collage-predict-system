"""Tests for ``cleaner.missing_data_handler``."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import missing_data_handler


def test_normalize_string_nulls() -> None:
    df = pd.DataFrame({"x": ["N/A", "ok", "-"]})
    out = missing_data_handler.normalize_string_nulls(df)
    assert pd.isna(out.loc[0, "x"])
    assert out.loc[1, "x"] == "ok"


def test_run_step_imputation(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "num": [1.0, 2.0, None, 4.0],
            "cat": ["a", "b", None, "a"],
        }
    )
    rep = tmp_path / "miss.csv"
    out, m = missing_data_handler.run_step(df, report_path=rep, source_file="t.csv")
    assert rep.is_file()
    assert "data_quality_flag" in out.columns
