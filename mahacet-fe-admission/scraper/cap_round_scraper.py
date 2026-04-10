"""
Discover CAP round cutoff / allotment related PDFs and record metadata under ``data/CAP_Round_Cutoffs``.
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
from scraper.html_extract import classify_cap_or_cutoff, iter_links, safe_filename_from_url
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


def scrape_cap_rounds(
    portal_url: str,
    year: int | None = None,
    *,
    html: str | None = None,
) -> list[dict[str, Any]]:
    """
    Collect CAP-related PDFs linked from the portal homepage.

    Returns:
        Manifest rows for each attempted download.
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
        logger.exception("CAP round scrape failed to load portal: %s", exc)
        return []

    rows: list[dict[str, Any]] = []
    root = settings.DATA_DIR

    for full_url, text in iter_links(html, portal_url):
        dest_rel = classify_cap_or_cutoff(full_url, text)
        if not dest_rel or not dest_rel.startswith("CAP_Round_Cutoffs"):
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https"):
            continue
        if not parsed.path.lower().endswith(".pdf"):
            continue

        fname = safe_filename_from_url(full_url)
        rel = Path(dest_rel) / fname
        abs_path = root / rel
        round_part = dest_rel.split("/")[-1].replace("Round_", "")
        row = {
            "year": y,
            "cap_round": round_part,
            "url": full_url,
            "link_text": text,
            "relative_path": rel.as_posix(),
            "suggested_csv_name": f"CAP_Cutoff_MH_{y}_Round{round_part}.csv",
        }
        try:
            b = _download(session, full_url, abs_path)
            row["bytes"] = b
            row["status"] = "downloaded"
            logger.info("CAP PDF saved: %s", abs_path)
        except Exception as exc:  # noqa: BLE001
            row["status"] = f"error: {exc}"
            logger.warning("CAP PDF failed %s: %s", full_url, exc)
        rows.append(row)

    out_dir = root / "CAP_Round_Cutoffs" / "manifests"
    out_dir.mkdir(parents=True, exist_ok=True)
    if rows:
        csv_p = out_dir / f"CAP_round_manifest_{y}.csv"
        json_p = out_dir / f"CAP_round_manifest_{y}.json"
        with csv_p.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with json_p.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        logger.info("Wrote CAP manifests to %s", out_dir)
    else:
        logger.info("No CAP PDF links detected on homepage (may require deeper crawl).")

    return rows
