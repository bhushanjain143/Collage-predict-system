"""
Load trained model and predict admission probability + chance tier.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings


def load_pipeline() -> Any:
    """Load ``model.pkl`` from artifacts directory."""
    if not settings.MODEL_PKL.is_file():
        raise FileNotFoundError(f"Missing model artifact: {settings.MODEL_PKL}")
    return joblib.load(settings.MODEL_PKL)


def tier_from_probability(p: float) -> str:
    """Map probability to display tier."""
    if p >= 0.70:
        return "High Chance"
    if p >= 0.40:
        return "Medium Chance"
    return "Low Chance"


def predict_row(pipe: Any, features: dict[str, Any]) -> tuple[float, str]:
    """
    Predict admission probability and tier for one student profile row.

    Returns:
        (probability, tier_label).
    """
    X = pd.DataFrame([features])
    proba = float(pipe.predict_proba(X)[0, 1])
    return proba, tier_from_probability(proba)


def predict_batch(pipe: Any, frame: pd.DataFrame) -> pd.DataFrame:
    """Append ``admission_probability`` (alias of model score), ``prediction_proba``, and ``chance_tier``."""
    out = frame.copy()
    probas = pipe.predict_proba(out)[:, 1]
    out["admission_probability"] = probas
    out["prediction_proba"] = probas
    out["chance_tier"] = [tier_from_probability(float(p)) for p in probas]
    return out


def load_feature_meta() -> dict[str, Any]:
    """Read ``features.json`` if present."""
    if not settings.FEATURES_JSON.is_file():
        return {}
    with settings.FEATURES_JSON.open(encoding="utf-8") as f:
        return json.load(f)
