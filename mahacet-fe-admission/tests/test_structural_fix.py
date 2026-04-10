"""Tests for ``cleaner.structural_fix``."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import structural_fix


def test_unify_null_representations() -> None:
    df = pd.DataFrame({"x": ["N/A", "ok", "--"]})
    out = structural_fix.unify_null_representations(df)
    assert pd.isna(out.loc[0, "x"])
    assert pd.isna(out.loc[2, "x"])


def test_fix_branch_names() -> None:
    s = pd.Series(["Mech", "IT"])
    out = structural_fix.fix_branch_names(s)
    assert "mechanical engineering" in out.tolist()
    assert "information technology" in out.tolist()
