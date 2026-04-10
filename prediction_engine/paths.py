from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = REPO_ROOT / "Maharashtra-FE-Admission-Dataset"
RESERVATION_JSON = DATASET_ROOT / "metadata" / "reservation_categories.json"
