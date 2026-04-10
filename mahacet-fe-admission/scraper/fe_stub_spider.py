"""
Optional Scrapy spider stub — verify portal reachability and HTML size.

Run from project root with ``PYTHONPATH=.``::

    scrapy runspider scraper/fe_stub_spider.py -s LOG_LEVEL=INFO
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Iterator

import scrapy

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings

logger = logging.getLogger(__name__)


class FePortalStubSpider(scrapy.Spider):
    """Minimal spider: fetch configured FE homepage and log response metrics."""

    name = "fe_portal_stub"
    custom_settings = {"ROBOTSTXT_OBEY": True, "DOWNLOAD_DELAY": 2.5}

    def start_requests(self) -> Iterator[scrapy.Request]:
        url = settings.get_active_portal_url()
        yield scrapy.Request(url, callback=self.parse, errback=self.on_error, dont_filter=True)

    def parse(self, response: Any) -> None:
        """Log successful fetch."""
        logger.info("Fetched %s — status=%s bytes=%s", response.url, response.status, len(response.body))

    def on_error(self, failure: Any) -> None:
        """Log transport / HTTP errors without raising."""
        logger.error("Request failed: %s", failure.getErrorMessage())
