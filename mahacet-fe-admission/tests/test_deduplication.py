"""Tests for ``cleaner.deduplication``."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import deduplication


def test_deduplicate_rows_removes_dupes() -> None:
    df = pd.DataFrame(
        {
            "Institute_Code": ["1", "1"],
            "Seat_Category_Code": ["GOPEN", "GOPEN"],
            "CAP_Round": [1, 1],
            "Academic_Year": ["2024-25", "2024-25"],
            "Program_Branch": ["CSE", "CSE"],
            "v": [1, 2],
        }
    )
    out, n = deduplication.deduplicate_rows(df)
    assert len(out) == 1
    assert n == 1


def test_drop_sparse_columns() -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [None, None]})
    out, dropped = deduplication.drop_sparse_columns(df, null_threshold=0.5)
    assert "b" in dropped
    assert "a" in out.columns
