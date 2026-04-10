from __future__ import annotations

from pathlib import Path

# Repository root: Collage/
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_ROOT = REPO_ROOT / "Maharashtra-FE-Admission-Dataset"
DEFAULT_MANIFEST = DEFAULT_DATASET_ROOT / "metadata" / "manifest.json"
