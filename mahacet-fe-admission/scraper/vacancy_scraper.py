"""
Collect vacancy-related documents and write ``Vacancy_Data`` manifests.
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
from scraper.html_extract import classify_cap_or_cutoff, destination_for, iter_links, safe_filename_from_url
from scraper.scraper_utils import fetch_with_retry

logger = logging.getLogger(__name__)


def scrape_vacancy(
    portal_url: str,
    year: int | None = None,
    *,
    html: str | None = None,
) -> list[dict[str, Any]]:
    """
    Download vacancy PDFs when linked from the homepage and write manifests.
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
        logger.exception("Vacancy scrape failed: %s", exc)
        return []

    rows: list[dict[str, Any]] = []
    root = settings.DATA_DIR

    for full_url, text in iter_links(html, portal_url):
        d1 = destination_for(full_url, text)
        d2 = classify_cap_or_cutoff(full_url, text)
        if d1 != "Vacancy_Data" and d2 != "Vacancy_Data":
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https") or not parsed.path.lower().endswith(".pdf"):
            continue
        fname = safe_filename_from_url(full_url)
        rel = Path("Vacancy_Data") / fname
        abs_path = root / rel
        row = {"year": y, "url": full_url, "link_text": text, "relative_path": rel.as_posix()}
        try:
            with session.get(full_url, stream=True, timeout=settings.REQUEST_TIMEOUT_SEC) as r:
                r.raise_for_status()
                abs_path.parent.mkdir(parents=True, exist_ok=True)
                n = 0
                with abs_path.open("wb") as f:
                    for chunk in r.iter_content(256 * 1024):
                        if chunk:
                            f.write(chunk)
                            n += len(chunk)
            row["bytes"] = n
            row["status"] = "downloaded"
            logger.info("Vacancy PDF saved: %s", abs_path)
        except Exception as exc:  # noqa: BLE001
            row["status"] = f"error: {exc}"
            logger.warning("Vacancy download failed: %s", full_url)
        rows.append(row)

    mdir = root / "Vacancy_Data" / "manifests"
    mdir.mkdir(parents=True, exist_ok=True)
    if rows:
        csv_p = mdir / f"Vacancy_manifest_{y}.csv"
        json_p = mdir / f"Vacancy_manifest_{y}.json"
        with csv_p.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with json_p.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
    else:
        logger.info("No vacancy PDFs linked from homepage.")

    return rows
