"""
Train admission model (XGBoost or RandomForest) with 5-fold CV; save ``model.pkl`` + ``features.json``.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings
from model import feature_engineering

logger = logging.getLogger(__name__)

try:
    from xgboost import XGBClassifier

    _HAS_XGB = True
except ImportError:
    _HAS_XGB = False


def build_estimator() -> Any:
    """Return an sklearn-compatible classifier."""
    if _HAS_XGB:
        return XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            tree_method="hist",
            random_state=42,
            eval_metric="logloss",
        )
    return RandomForestClassifier(
        n_estimators=400,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )


def make_pipeline(feature_names: list[str]) -> Pipeline:
    """Create preprocessing + classifier pipeline for mixed feature types."""
    numeric = [
        c
        for c in feature_names
        if c
        in (
            "student_percentile",
            "historical_cutoff_mean_3yr",
            "historical_cutoff_std_3yr",
            "seat_availability_ratio",
            "CAP_Round",
        )
    ]
    categorical = [c for c in feature_names if c not in numeric]
    transformers: list[tuple[str, Any, list[str]]] = []
    if numeric:
        transformers.append(
            ("num", SimpleImputer(strategy="median"), numeric),
        )
    if categorical:
        transformers.append(
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("oh", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        )
    pre = ColumnTransformer(transformers, remainder="drop")
    return Pipeline([("prep", pre), ("clf", build_estimator())])


def cross_validate_model(X: pd.DataFrame, y: pd.Series, pipe: Pipeline) -> dict[str, float]:
    """
    Run stratified k-fold CV (prefer **5** folds per product spec).

    Falls back to ``min(5, class_min_count)`` when a class has fewer than five samples.
    """
    counts = y.value_counts()
    if len(counts) < 2 or counts.min() < 2:
        logger.warning("Skipping CV — need at least two classes with 2+ rows each.")
        return {
            "cv_accuracy_mean": float("nan"),
            "cv_auc_mean": float("nan"),
            "cv_folds_used": 0,
            "cv_folds_requested": 5,
        }
    n_splits = int(min(5, int(counts.min())))
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    accs: list[float] = []
    aucs: list[float] = []
    for tr, va in skf.split(X, y):
        X_tr, X_va = X.iloc[tr], X.iloc[va]
        y_tr, y_va = y.iloc[tr], y.iloc[va]
        pipe.fit(X_tr, y_tr)
        proba = pipe.predict_proba(X_va)[:, 1]
        pred = (proba >= 0.5).astype(int)
        accs.append(accuracy_score(y_va, pred))
        try:
            aucs.append(roc_auc_score(y_va, proba))
        except ValueError:
            aucs.append(float("nan"))
    return {
        "cv_accuracy_mean": float(np.nanmean(accs)),
        "cv_auc_mean": float(np.nanmean(aucs)),
        "cv_folds_used": n_splits,
        "cv_folds_requested": 5,
    }


def train_and_save(data_root: Path | None = None) -> dict[str, Any]:
    """
    Train on engineered features and persist artifacts.

    Returns:
        Metrics dict.
    """
    X, y, feats = feature_engineering.build_feature_matrix(data_root)
    if X.empty or len(y) < 10:
        logger.error("Not enough rows to train — add CAP CSV data under data/CAP_Round_Cutoffs/.")
        return {"error": "insufficient_data"}
    if y.nunique() < 2:
        logger.error("Single-class label after augmentation — check cutoff CSV content.")
        return {"error": "single_class"}

    pipe = make_pipeline(feats)
    cv_metrics = cross_validate_model(X, y, pipe)
    logger.info("CV metrics: %s", cv_metrics)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    try:
        auc_h = float(roc_auc_score(y_test, proba))
    except ValueError:
        auc_h = float("nan")
    holdout = {
        "holdout_accuracy": float(accuracy_score(y_test, pred)),
        "holdout_auc": auc_h,
    }

    pipe.fit(X, y)

    settings.MODEL_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, settings.MODEL_PKL)
    feature_meta = {
        "feature_columns": feats,
        "target_interpretation": (
            "Binary classifier; positive-class predict_proba is exposed as admission_probability (0..1)."
        ),
        **cv_metrics,
        **holdout,
    }
    with settings.FEATURES_JSON.open("w", encoding="utf-8") as f:
        json.dump(feature_meta, f, indent=2)
    logger.info("Saved model to %s", settings.MODEL_PKL)
    return {**cv_metrics, **holdout}


def main(argv: list[str] | None = None) -> int:
    lvl = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Train MAHACET FE admission model.")
    p.add_argument("--data-dir", type=Path, default=None)
    args = p.parse_args(argv)
    train_and_save(args.data_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
