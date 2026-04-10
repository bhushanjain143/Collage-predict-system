"""
Main scraping orchestrator: optional Selenium render, then modular dataset collectors.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import settings
from scraper import (
    cap_round_scraper,
    college_details_scraper,
    merit_list_scraper,
    seat_matrix_scraper,
    vacancy_scraper,
)
from scraper import reservation_catalog
from scraper.scraper_utils import get_text

logger = logging.getLogger(__name__)


def fetch_portal_html(portal_url: str, *, use_selenium: bool) -> str:
    """
    Load portal HTML, preferring Selenium when ``use_selenium`` is True.

    Falls back to ``requests`` if WebDriver is unavailable or fails.
    """
    if use_selenium:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            opts = Options()
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=opts)
            try:
                driver.set_page_load_timeout(settings.REQUEST_TIMEOUT_SEC)
                driver.get(portal_url)
                html = driver.page_source
                logger.info("Loaded portal via Selenium: %s", portal_url)
                return html
            finally:
                driver.quit()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Selenium path failed (%s); falling back to HTTP GET.", exc)

    return get_text(portal_url)


def run_all(portal_url: str, year: int | None, *, use_selenium: bool) -> dict[str, Any]:
    """
    Execute all scraper modules sequentially; log and continue on section failures.

    Returns:
        Summary dict with keys per scraper and any errors.
    """
    y = year if year is not None else settings.ADMISSION_PORTAL_YEAR
    summary: dict[str, Any] = {"year": y, "portal_url": portal_url, "sections": {}}

    html: str | None = None
    if use_selenium:
        try:
            html = fetch_portal_html(portal_url, use_selenium=True)
        except Exception as exc:  # noqa: BLE001
            summary["selenium_error"] = str(exc)
            logger.warning("Selenium HTML fetch failed; modules will use HTTP.")

    for name, fn in (
        ("merit_lists", merit_list_scraper.scrape_merit_lists),
        ("cap_rounds", cap_round_scraper.scrape_cap_rounds),
        ("seat_matrix", seat_matrix_scraper.scrape_seat_matrix),
        ("college_details", college_details_scraper.scrape_college_details),
        ("vacancy", vacancy_scraper.scrape_vacancy),
    ):
        try:
            summary["sections"][name] = {"rows": len(fn(portal_url, y, html=html))}
        except Exception as exc:  # noqa: BLE001
            logger.exception("Scraper section %s failed", name)
            summary["sections"][name] = {"error": str(exc)}

    return summary


def run_multi_year_portals(
    primary_portal: str,
    base_year: int,
    years_back: int,
    *,
    use_selenium: bool,
) -> dict[str, Any]:
    """
    Attempt to scrape ``years_back`` prior admission-cycle portals (inclusive of ``base_year``).

    Each cycle uses ``https://fe{year}.mahacet.org/...`` when reachable; failures are logged
    and skipped so the rest of the pipeline can continue.
    """
    out: dict[str, Any] = {"base_year": base_year, "years_back": years_back, "years": {}}
    for offset in range(0, max(0, years_back) + 1):
        dy = int(base_year) - offset
        portal_url = primary_portal if offset == 0 else settings.default_portal_url(dy)
        try:
            get_text(portal_url)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Skipping year %s portal (%s): %s", dy, portal_url, exc)
            out["years"][str(dy)] = {"skipped": True, "reason": str(exc)}
            continue
        try:
            out["years"][str(dy)] = run_all(portal_url, dy, use_selenium=use_selenium)
            logger.info("Completed scrape pass for admission year label %s", dy)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Scrape pass failed for year %s", dy)
            out["years"][str(dy)] = {"error": str(exc)}
    return out


def main(argv: list[str] | None = None) -> int:
    lvl = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="MAHACET FE data scraper orchestrator.")
    p.add_argument("--portal-url", type=str, default="", help="Override portal homepage URL.")
    p.add_argument("--year", type=int, default=None, help="Admission portal year label for filenames.")
    p.add_argument(
        "--years-back",
        type=int,
        default=int(os.environ.get("MAHA_YEARS_BACK", "4")),
        help="Also scrape fe{year-1}.. when reachable (0 = current host only). Override with env MAHA_YEARS_BACK.",
    )
    p.add_argument(
        "--skip-discovery",
        action="store_true",
        help="Do not run url_discovery; use saved URL or --portal-url.",
    )
    p.add_argument(
        "--selenium",
        action="store_true",
        help="Use Selenium Chrome (headless) when possible.",
    )
    args = p.parse_args(argv)

    portal = args.portal_url.strip()
    if not portal and args.skip_discovery:
        portal = settings.get_active_portal_url(args.year) or settings.get_confirmed_portal_url() or ""
    if not portal:
        from scraper.url_discovery import discover_confirmed_url

        try:
            portal = discover_confirmed_url(args.year)
        except RuntimeError as exc:
            logger.error("%s", exc)
            return 1
    if not portal:
        logger.error("No portal URL available.")
        return 1

    base_y = args.year if args.year is not None else settings.ADMISSION_PORTAL_YEAR
    try:
        reservation_catalog.write_reservation_reference(base_y)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Reservation catalog export failed: %s", exc)

    if args.years_back <= 0:
        run_all(portal, base_y, use_selenium=args.selenium)
    else:
        run_multi_year_portals(portal, base_y, args.years_back, use_selenium=args.selenium)

    logger.info("Scraper run finished (primary portal %s)", portal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
