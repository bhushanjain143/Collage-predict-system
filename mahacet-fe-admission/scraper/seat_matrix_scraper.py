"""
Collect seat matrix documents (PDF/XLSX) linked from the portal.
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


def _download(session: Any, url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, stream=True, timeout=settings.REQUEST_TIMEOUT_SEC) as r:
        r.raise_for_status()
        n = 0
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=256 * 1024):
                if chunk:
                    f.write(chunk)
                    n += len(chunk)
    return n


def scrape_seat_matrix(
    portal_url: str,
    year: int | None = None,
    *,
    html: str | None = None,
) -> list[dict[str, Any]]:
    """
    Download seat-matrix-like files and write ``Seat_Matrix_*_{year}`` manifests.
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
        logger.exception("Seat matrix scrape failed: %s", exc)
        return []

    rows: list[dict[str, Any]] = []
    root = settings.DATA_DIR

    for full_url, text in iter_links(html, portal_url):
        d = destination_for(full_url, text)
        if not d or not d.startswith("Seat_Matrix"):
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https"):
            continue
        suf = parsed.path.lower()
        if not (suf.endswith(".pdf") or suf.endswith(".xlsx") or suf.endswith(".xls")):
            continue
        fname = safe_filename_from_url(full_url)
        rel = Path(d) / fname
        abs_path = root / rel
        row = {
            "year": y,
            "url": full_url,
            "link_text": text,
            "relative_path": rel.as_posix(),
            "canonical_name": f"Seat_Matrix_Institute_wise_{y}{Path(fname).suffix}",
        }
        try:
            row["bytes"] = _download(session, full_url, abs_path)
            row["status"] = "downloaded"
            logger.info("Seat matrix file saved: %s", abs_path)
        except Exception as exc:  # noqa: BLE001
            row["status"] = f"error: {exc}"
            logger.warning("Seat matrix download failed: %s", full_url)
        rows.append(row)

    mdir = root / "Seat_Matrix" / "manifests"
    mdir.mkdir(parents=True, exist_ok=True)
    if rows:
        csv_p = mdir / f"Seat_Matrix_manifest_{y}.csv"
        json_p = mdir / f"Seat_Matrix_manifest_{y}.json"
        with csv_p.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with json_p.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
    else:
        logger.info("No seat matrix binaries found on homepage.")

    return rows
