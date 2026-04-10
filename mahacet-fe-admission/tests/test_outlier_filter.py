"""Tests for ``cleaner.outlier_filter``."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import outlier_filter


def test_apply_iqr_logs(tmp_path: Path) -> None:
    df = pd.DataFrame({"Closing_Percentile": [10.0, 12.0, 11.0, 11.5, 100.0]})
    log: list[dict] = []
    out = outlier_filter.apply_iqr(df, "Closing_Percentile", "f.csv", log)
    assert len(log) >= 1
    assert "Closing_Percentile" in out.columns
