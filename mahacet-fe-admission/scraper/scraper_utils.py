"""
Shared HTTP helpers: retries, exponential backoff, random delays, logging.
"""

from __future__ import annotations

import logging
import random
import sys
import time
from pathlib import Path
from typing import Any

import requests
from requests import Response

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings

logger = logging.getLogger(__name__)


def polite_delay() -> None:
    """Sleep a random interval between requests to reduce rate-limit risk."""
    low = settings.SCRAPER_DELAY_MIN_SEC
    high = settings.SCRAPER_DELAY_MAX_SEC
    if high < low:
        low, high = high, low
    t = random.uniform(low, high)
    logger.debug("Sleeping %.2fs before next request", t)
    time.sleep(t)


def fetch_with_retry(
    url: str,
    *,
    session: requests.Session | None = None,
    timeout: int | None = None,
    max_retries: int | None = None,
) -> Response:
    """
    GET ``url`` with retries and exponential backoff on HTTP errors and timeouts.

    Returns:
        Successful ``requests.Response``.

    Raises:
        requests.RequestException: If all retries fail.
    """
    sess = session or requests.Session()
    sess.headers.setdefault(
        "User-Agent",
        "MahacetFE-Pipeline/1.0 (+https://github.com/) academic dataset collection",
    )
    retries = max_retries if max_retries is not None else settings.MAX_HTTP_RETRIES
    timeout_sec = timeout if timeout is not None else settings.REQUEST_TIMEOUT_SEC
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            polite_delay()
            resp = sess.get(url, timeout=timeout_sec)
            if resp.status_code >= 500:
                raise requests.HTTPError(f"Server error {resp.status_code} for {url}")
            resp.raise_for_status()
            return resp
        except (requests.RequestException, OSError) as exc:
            last_exc = exc
            wait = 2**attempt + random.uniform(0, 0.5)
            logger.warning(
                "Request failed (attempt %s/%s) for %s: %s — retry in %.1fs",
                attempt + 1,
                retries,
                url,
                exc,
                wait,
            )
            time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def get_text(url: str, session: requests.Session | None = None) -> str:
    """Return response body decoded as text."""
    return fetch_with_retry(url, session=session).text


def merge_json_lists(path: Any, key: str, item: dict[str, Any]) -> None:
    """Append ``item`` to a JSON list file on disk (create if missing)."""
    import json
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data: list[Any] = []
    if p.is_file():
        try:
            with p.open(encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except (OSError, json.JSONDecodeError):
            data = []
    data.append(item)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
