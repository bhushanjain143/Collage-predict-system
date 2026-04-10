"""Tests for ``cleaner.format_standardizer``."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import format_standardizer


def test_normalize_category_codes() -> None:
    s = pd.Series(["OBC", "General", "GOPEN"])
    out = format_standardizer.normalize_category_codes(s)
    assert "obc" in out.tolist()
    assert "open" in out.tolist()


def test_normalize_fees() -> None:
    s = pd.Series(["₹1,23,456", "90000"])
    out = format_standardizer.normalize_fees(s)
    assert out.iloc[0] > 100000
