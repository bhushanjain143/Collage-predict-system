"""
Emit reference reservation / seat-category codes (CSV + JSON) under ``data/Scholarship_Data``.

Official CAP codes and seat splits vary by year; this file is a **reference template**
for UI filtering and documentation — always verify against the current Information Brochure.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings

logger = logging.getLogger(__name__)

REFERENCE_ROWS: list[dict[str, Any]] = [
    {"code": "OPEN", "cap_examples": "GOPEN, LOPEN", "notes": "General / open category patterns"},
    {"code": "SC", "cap_examples": "GSC, LSC, …", "notes": "Scheduled Caste — subcodes per brochure"},
    {"code": "ST", "cap_examples": "GST, LST, …", "notes": "Scheduled Tribe"},
    {"code": "VJ", "cap_examples": "GVJ, …", "notes": "Vimukta Jati / DT(A) per state rules"},
    {"code": "NT-A", "cap_examples": "GNTA, …", "notes": "Nomadic Tribe A"},
    {"code": "NT-B", "cap_examples": "GNTB, …", "notes": "Nomadic Tribe B"},
    {"code": "NT-C", "cap_examples": "GNTC, …", "notes": "Nomadic Tribe C"},
    {"code": "NT-D", "cap_examples": "GNTD, …", "notes": "Nomadic Tribe D"},
    {"code": "OBC", "cap_examples": "GOBC, LOBC, …", "notes": "Other Backward Classes"},
    {"code": "SBC", "cap_examples": "GSBC, …", "notes": "Special Backward Class (if applicable)"},
    {"code": "EWS", "cap_examples": "EWS, …", "notes": "Economically Weaker Section"},
    {"code": "EBC", "cap_examples": "…", "notes": "Economically Backward Class (if applicable)"},
    {"code": "TFWS", "cap_examples": "TFWS", "notes": "Tuition Fee Waiver Scheme"},
    {"code": "MI", "cap_examples": "MI-*", "notes": "Minority institute / minority seat patterns"},
    {"code": "DEF", "cap_examples": "DEF*, …", "notes": "Defence subcategories"},
    {"code": "PWD", "cap_examples": "PWD*, …", "notes": "Persons with disability — subcategories per brochure"},
]


def write_reservation_reference(year: int | None = None) -> Path:
    """
    Write ``Reservation_Codes_{year}.csv`` and ``.json`` into ``data/Scholarship_Data/``.

    Returns:
        Path to the written CSV file.
    """
    y = year if year is not None else settings.ADMISSION_PORTAL_YEAR
    out_dir = settings.DATA_DIR / "Scholarship_Data"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"Reservation_Codes_{y}.csv"
    json_path = out_dir / f"Reservation_Codes_{y}.json"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(REFERENCE_ROWS[0].keys()))
        w.writeheader()
        w.writerows(REFERENCE_ROWS)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"year": y, "disclaimer": "Reference only — not legal advice.", "codes": REFERENCE_ROWS},
            f,
            indent=2,
            ensure_ascii=False,
        )
    logger.info("Wrote reservation reference: %s", csv_path)
    return csv_path
