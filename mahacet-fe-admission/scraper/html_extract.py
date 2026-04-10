"""
Parse anchor tags from HTML and classify MAHACET portal links.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def iter_links(html: str, base_url: str) -> Iterable[tuple[str, str]]:
    """Yield (absolute_url, link_text) for each anchor with href."""
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        href = str(a["href"]).strip()
        text = " ".join(a.get_text(" ", strip=True).split())
        yield urljoin(base_url, href), text


def safe_filename_from_url(url: str, kind_prefix: str | None = None) -> str:
    """Build a filesystem-safe filename; disambiguate generic ASPX handlers."""
    parsed = urlparse(url)
    name = parsed.path.rsplit("/", 1)[-1] or "download.bin"
    low = name.lower()
    if low in ("viewpublicdocument.aspx", "viewpublicdocument"):
        qs = parse_qs(parsed.query)
        mid = (qs.get("MenuId") or qs.get("menuid") or [""])[0]
        if mid:
            name = f"ViewPublicDocument_MenuId_{mid}.aspx"
        else:
            tail = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
            name = f"ViewPublicDocument_{tail}.bin"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "download.bin"
    if kind_prefix:
        return f"{kind_prefix}_{name}"
    return name


def classify_merit_pdf(url: str) -> tuple[str | None, str | None]:
    """Return (Merit_Lists/... subpath under data, Final|Provisional|Other) or (None, None)."""
    u = url
    low = u.lower()
    if "meritlistfiles" not in low:
        return None, None
    if "/final/" in low or "meritlist_final" in low:
        kind = "Final"
    elif "/provisional/" in low or "meritlist_provisional" in low:
        kind = "Provisional"
    else:
        kind = "Other"

    if any(x in u for x in ("PCMMH", "PCBMH")):
        return "Merit_Lists/MH_State", kind
    if any(x in u for x in ("PCMAI", "PCBAI")):
        return "Merit_Lists/All_India", kind
    if any(x in u for x in ("PCMJK", "PCBJK")):
        return "Merit_Lists/JK_Candidates", kind
    return None, None


def classify_cap_or_cutoff(url: str, link_text: str) -> str | None:
    """Map CAP / cutoff / vacancy / allotment URLs to a folder under ``data/``."""
    u = url.lower()
    blob = (url + " " + link_text).lower()
    if "cutoff" in blob or "cut off" in blob or "cap" in blob:
        m = re.search(r"cap\s*[_-]?\s*round\s*([1-5])", blob)
        if not m:
            m = re.search(r"cap\s*([1-5])\b", blob)
        if m:
            rnd = int(m.group(1))
            return f"CAP_Round_Cutoffs/Round_{rnd}"
        if "round i" in blob or "round 1" in blob or "cap-i" in blob or "cap1" in blob:
            return "CAP_Round_Cutoffs/Round_1"
        if "round ii" in blob or "round 2" in blob or "cap-ii" in blob or "cap2" in blob:
            return "CAP_Round_Cutoffs/Round_2"
        if "round iii" in blob or "round 3" in blob or "cap-iii" in blob or "cap3" in blob:
            return "CAP_Round_Cutoffs/Round_3"
        if "round iv" in blob or "round 4" in blob or "cap-iv" in blob or "cap4" in blob:
            return "CAP_Round_Cutoffs/Round_4"
        if "vacancy" in blob:
            return "Vacancy_Data"
        if "allotment" in blob or "allot" in blob:
            return "Allotment_Results"
        if "seat" in blob and "matrix" in blob:
            return "Seat_Matrix/Institute_wise"
        return "CAP_Round_Cutoffs/Round_1"
    if "vacancy" in u or "vacancy" in link_text.lower():
        return "Vacancy_Data"
    if "allotment" in u or "allot" in link_text.lower():
        return "Allotment_Results"
    if "seat" in u and "matrix" in u:
        return "Seat_Matrix/Institute_wise"
    if "scholar" in blob or "fee waiver" in blob or "tfws" in blob:
        return "Scholarship_Data"
    return None


def destination_for(url: str, link_text: str) -> str:
    """Relative path under ``data/`` for a resource, or empty string if unknown."""
    parsed = urlparse(url)
    path_lower = (parsed.path or "").lower()

    merit_dir, _merit_kind = classify_merit_pdf(url)
    if merit_dir and path_lower.endswith(".pdf"):
        return merit_dir

    cap_dir = classify_cap_or_cutoff(url, link_text)
    if cap_dir and path_lower.endswith(".pdf"):
        return cap_dir

    blob = (url + " " + link_text).lower()
    if "intake" in blob and "college" in blob:
        if path_lower.endswith(".pdf"):
            return "College_Details"

    if "viewpublicdocument" in path_lower:
        return "metadata/raw_documents"

    if path_lower.endswith(".pdf"):
        return "metadata/raw_documents"

    if path_lower.endswith((".xlsx", ".xls")):
        return "Seat_Matrix/Institute_wise"

    if path_lower.endswith(".zip"):
        return "Allotment_Results"

    return ""
