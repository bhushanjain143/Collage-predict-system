"""
Phase 0 — Discover the active MAHACET FE portal URL for the admission cycle.

Tries the canonical ``fe{YEAR}.mahacet.org`` pattern first, then DuckDuckGo search
(and optional Google CSE if env vars are set), validates page content, and
persists the result under ``config/discovered_portal_url.json``.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings
from scraper.scraper_utils import fetch_with_retry, get_text

logger = logging.getLogger(__name__)


def _log_discovery_failure(reason: str, details: dict[str, Any]) -> None:
    """Append a failure record to ``url_discovery_log.json``."""
    settings.URL_DISCOVERY_LOG.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        **details,
    }
    history: list[Any] = []
    if settings.URL_DISCOVERY_LOG.is_file():
        try:
            with settings.URL_DISCOVERY_LOG.open(encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except (OSError, json.JSONDecodeError):
            history = []
    history.append(payload)
    with settings.URL_DISCOVERY_LOG.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    logger.error("URL discovery failed: %s — logged to %s", reason, settings.URL_DISCOVERY_LOG)


def validate_portal_page(html: str) -> bool:
    """
    Return True if ``html`` looks like an official FE / CET Cell portal page.

    Expects at least two of: CAP Round, Merit List, Seat Matrix, CET CELL.
    """
    low = html.lower()
    patterns = [
        "cap" in low and "round" in low,
        "merit" in low and "list" in low,
        "seat" in low and "matrix" in low,
        "cet" in low and "cell" in low,
    ]
    return sum(1 for p in patterns if p) >= 2


def try_primary_url(year: int) -> str | None:
    """
    Attempt to load the canonical portal URL for ``year``.

    Returns:
        URL string if HTTP 200 and content validates; otherwise ``None``.
    """
    url = settings.default_portal_url(year)
    try:
        text = get_text(url)
        if validate_portal_page(text):
            logger.info("Primary portal URL validated: %s", url)
            return url
        logger.warning("Primary URL loaded but failed content validation: %s", url)
    except requests.RequestException as exc:
        logger.warning("Primary URL unavailable (%s): %s", url, exc)
    return None


def search_candidate_urls(year: int) -> list[str]:
    """
    Collect candidate URLs from DuckDuckGo text search and optional Google CSE.

    Returns:
        Ordered list of unique http(s) URLs mentioning mahacet.org or mahacet.
    """
    found: list[str] = []
    queries = [q.format(year=year) for q in settings.SEARCH_QUERIES_TEMPLATE]

    try:
        from duckduckgo_search import DDGS

        for q in queries:
            try:
                with DDGS() as ddgs:
                    for r in ddgs.text(q, max_results=8):
                        href = r.get("href") or r.get("url") or ""
                        if isinstance(href, str) and href.startswith("http"):
                            found.append(href.split("#")[0])
            except Exception as exc:  # noqa: BLE001
                logger.warning("DuckDuckGo query failed (%s): %s", q, exc)
    except ImportError:
        logger.warning("duckduckgo-search not installed; skipping DDG search.")

    if settings.GOOGLE_CSE_API_KEY and settings.GOOGLE_CSE_CX:
        for q in queries:
            try:
                gurl = "https://www.googleapis.com/customsearch/v1"
                resp = requests.get(
                    gurl,
                    params={
                        "key": settings.GOOGLE_CSE_API_KEY,
                        "cx": settings.GOOGLE_CSE_CX,
                        "q": q,
                        "num": 8,
                    },
                    timeout=settings.REQUEST_TIMEOUT_SEC,
                )
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("items", []) or []:
                    link = item.get("link")
                    if isinstance(link, str):
                        found.append(link.split("#")[0])
            except requests.RequestException as exc:
                logger.warning("Google CSE query failed (%s): %s", q, exc)

    # Prefer mahacet.org hosts
    out: list[str] = []
    seen: set[str] = set()
    for u in found:
        host = urlparse(u).netloc.lower()
        if "mahacet" not in host and "mahacet.org" not in u.lower():
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def discover_confirmed_url(year: int | None = None) -> str:
    """
    Discover and persist the FE portal homepage URL.

    Returns:
        ``confirmed_url`` string.

    Raises:
        RuntimeError: If no valid URL could be confirmed.
    """
    y = year if year is not None else settings.ADMISSION_PORTAL_YEAR
    logger.info("Starting URL discovery for year=%s", y)

    primary = try_primary_url(y)
    if primary:
        meta = {
            "confirmed_url": primary,
            "year": y,
            "source": "primary_template",
            "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        settings.save_discovered_portal_meta(meta)
        return primary

    candidates = search_candidate_urls(y)
    # Add homepage guesses for nearby years if list empty
    if not candidates:
        for dy in (y, y - 1, y + 1):
            candidates.append(settings.default_portal_url(dy))

    session = requests.Session()
    for cand in candidates:
        # Normalize to StaticPages/HomePage when we land on a bare host
        parsed = urlparse(cand)
        if parsed.path in ("", "/"):
            cand = f"{parsed.scheme}://{parsed.netloc}/StaticPages/HomePage"
        try:
            text = fetch_with_retry(cand, session=session).text
            if not validate_portal_page(text):
                continue
            # Prefer URLs that look like FE static homepage
            if "StaticPages" in cand or "HomePage" in cand or "fe" in parsed.netloc.lower():
                meta = {
                    "confirmed_url": cand,
                    "year": y,
                    "source": "search_validation",
                    "validated_at_utc": datetime.now(timezone.utc).isoformat(),
                }
                settings.save_discovered_portal_meta(meta)
                logger.info("Confirmed portal URL via search: %s", cand)
                return cand
        except requests.RequestException as exc:
            logger.warning("Candidate URL failed: %s (%s)", cand, exc)
            continue

    _log_discovery_failure(
        "no_valid_url",
        {"year": y, "candidates_tried": candidates[:20]},
    )
    raise RuntimeError(
        f"Could not discover a valid MAHACET FE portal URL for {y}. "
        f"See {settings.URL_DISCOVERY_LOG}"
    )


def main() -> int:
    lvl = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")
    url = discover_confirmed_url()
    logger.info("Confirmed portal URL: %s", url)
    print(url, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
