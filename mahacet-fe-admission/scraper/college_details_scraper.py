"""
Collect college / intake related document links and placeholder structured CSV.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings
from scraper.html_extract import destination_for, iter_links, safe_filename_from_url
from scraper.scraper_utils import fetch_with_retry

logger = logging.getLogger(__name__)


def scrape_college_details(
    portal_url: str,
    year: int | None = None,
    *,
    html: str | None = None,
) -> list[dict[str, Any]]:
    """
    Record links related to college intake lists and write ``College_Details_{year}.csv`` link table.

    Full tabular college attributes usually require PDF/XLSX parsing — this step captures URLs.
    """
    y = year if year is not None else settings.ADMISSION_PORTAL_YEAR
    import requests

    session = requests.Session()
    session.headers.setdefault(
        "User-Agent",
        "MahacetFE-Pipeline/1.0 (+https://github.com/) academic dataset collection",
    )

    try:
        if html is None:
            html = fetch_with_retry(portal_url, session=session).text
    except Exception as exc:  # noqa: BLE001
        logger.exception("College details scrape failed: %s", exc)
        return []

    rows: list[dict[str, Any]] = []
    root = settings.DATA_DIR

    for full_url, text in iter_links(html, portal_url):
        d = destination_for(full_url, text)
        if d != "College_Details":
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https"):
            continue
        fname = safe_filename_from_url(full_url)
        rel = Path(d) / fname
        abs_path = root / rel
        row = {
            "year": y,
            "url": full_url,
            "link_text": text,
            "relative_path": rel.as_posix(),
        }
        if parsed.path.lower().endswith(".pdf"):
            try:
                with session.get(full_url, stream=True, timeout=settings.REQUEST_TIMEOUT_SEC) as r:
                    r.raise_for_status()
                    abs_path.parent.mkdir(parents=True, exist_ok=True)
                    with abs_path.open("wb") as f:
                        for chunk in r.iter_content(256 * 1024):
                            if chunk:
                                f.write(chunk)
                row["status"] = "downloaded"
            except Exception as exc:  # noqa: BLE001
                row["status"] = f"error: {exc}"
                logger.warning("College details doc failed: %s", full_url)
        else:
            row["status"] = "skipped_non_pdf"
        rows.append(row)

    out_csv = root / "College_Details" / f"College_Details_links_{y}.csv"
    out_json = root / "College_Details" / f"College_Details_links_{y}.json"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with out_json.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        logger.info("College details link manifest: %s", out_csv)

    template = root / "College_Details" / f"College_Details_{y}.csv"
    if not template.is_file():
        headers = [
            "college_code",
            "college_name",
            "college_type",
            "district",
            "city",
            "annual_fees_inr",
            "hostel_available",
            "placement_pct",
            "scholarship_eligible",
        ]
        with template.open("w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f).writerow(headers)
        logger.info("Wrote empty college details template %s (fill from official sources).", template)

    return rows
