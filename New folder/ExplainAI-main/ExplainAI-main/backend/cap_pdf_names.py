"""Filename → (year, CAP round) for MHT-CET engineering cutoff PDFs. No Flask import."""
from __future__ import annotations

import os
import re

_SKIP_MARKERS = (
    "seatmatrix",
    "meritlist",
    "merit_list",
    "pcmai",
    "pcmjk",
    "pcmmh",
)


def skip_pdf_filename(name: str) -> bool:
    n = name.lower().replace(" ", "")
    return any(m in n for m in _SKIP_MARKERS)


def infer_year_round_from_path(path: str) -> tuple[int, int] | None:
    base = os.path.basename(path)
    if skip_pdf_filename(base):
        return None

    m = re.search(
        r"(20\d{2})\s*ENGG\s*_?\s*CAP\s*([1-4])\s*_?\s*(?:AI\s*_?)?CutOff",
        base,
        re.I,
    )
    if m:
        return int(m.group(1)), int(m.group(2))

    m = re.search(r"CAP[_\s]?Round[_\s]?([1-4])[_\s]?2025[_\s]?2026", base, re.I)
    if m:
        return 2025, int(m.group(1))

    m = re.search(r"(20\d{2})[_\s]+round[_\s]*([1-4])", base, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))

    return None
