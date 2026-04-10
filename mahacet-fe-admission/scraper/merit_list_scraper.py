"""
Download merit list PDFs (MH, AI, J&K) and write CSV/JSON manifests.
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
from scraper.html_extract import classify_merit_pdf, iter_links, safe_filename_from_url
from scraper.scraper_utils import fetch_with_retry

logger = logging.getLogger(__name__)


def _download_binary(session: Any, url: str, dest: Path, timeout: int) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        n = 0
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=256 * 1024):
                if chunk:
                    f.write(chunk)
                    n += len(chunk)
    return n


def scrape_merit_lists(
    portal_url: str,
    year: int | None = None,
    *,
    html: str | None = None,
) -> list[dict[str, Any]]:
    """
    Parse ``portal_url`` for merit list PDFs, download them, and write manifests.

    Args:
        portal_url: Confirmed portal homepage URL.
        year: Label for manifests.
        html: Optional pre-rendered HTML (e.g. from Selenium).

    Returns:
        List of manifest row dicts.
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
        logger.exception("Merit list scrape failed to load portal: %s", exc)
        return []

    rows: list[dict[str, Any]] = []
    data_root = settings.DATA_DIR
    manifest_dir = data_root / "Merit_Lists" / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    for full_url, text in iter_links(html, portal_url):
        merit_dir, merit_kind = classify_merit_pdf(full_url)
        if not merit_dir:
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https") or not parsed.path.lower().endswith(".pdf"):
            continue

        fname = safe_filename_from_url(full_url, kind_prefix=merit_kind)
        rel_under_data = Path(merit_dir) / fname
        abs_path = data_root / rel_under_data

        quota = "MH" if "MH_State" in merit_dir else "AI" if "All_India" in merit_dir else "JK"
        list_type = (merit_kind or "Unknown").lower()
        canonical_name = f"Merit_List_{quota}_{list_type}_{y}.pdf"
        row = {
            "year": y,
            "url": full_url,
            "link_text": text,
            "quota": quota,
            "list_type": merit_kind,
            "relative_path": rel_under_data.as_posix(),
            "canonical_csv_name": f"Merit_List_{quota}_{merit_kind}_{y}.csv",
        }
        try:
            n = _download_binary(session, full_url, abs_path, settings.REQUEST_TIMEOUT_SEC)
            row["bytes"] = n
            row["status"] = "downloaded"
            logger.info("Merit PDF saved: %s (%s bytes)", abs_path, n)
        except Exception as exc:  # noqa: BLE001
            row["status"] = f"error: {exc}"
            logger.warning("Merit PDF download failed %s: %s", full_url, exc)
        rows.append(row)

    csv_path = manifest_dir / f"Merit_List_manifest_{y}.csv"
    json_path = manifest_dir / f"Merit_List_manifest_{y}.json"
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        logger.info("Wrote merit manifests: %s, %s", csv_path, json_path)
    else:
        logger.warning("No merit list links found on portal page.")

    return rows
