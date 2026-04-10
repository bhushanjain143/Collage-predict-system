"""
Discover and download public documents linked from the Maharashtra FE portal homepage.

Uses requests + BeautifulSoup. For JS-heavy pages later, add an optional Selenium path.

Example:
  python scripts/maha_fe_admission/scrape_portal.py \\
    --base-url https://fe2025.mahacet.org/StaticPages/HomePage \\
    --output-dir Maharashtra-FE-Admission-Dataset
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Collage/ (repo root) — two levels up from this file: maha_fe_admission -> scripts -> Collage
REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BASE = "https://fe2025.mahacet.org/StaticPages/HomePage"
USER_AGENT = (
    "Mozilla/5.0 (compatible; MahaFE-DatasetBot/1.0; +https://github.com/) "
    "Academic-research data collection"
)


@dataclass
class DownloadRecord:
    url: str
    saved_path: str
    sha256: str
    category: str
    bytes: int


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def fetch_html(session: requests.Session, url: str, timeout: int = 60) -> str:
    r = session.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def iter_links(html: str, base_url: str) -> Iterable[tuple[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = " ".join(a.get_text(" ", strip=True).split())
        full = urljoin(base_url, href)
        yield full, text


def classify_merit_pdf(url: str) -> tuple[str | None, str | None]:
    """
    Returns (relative_dest_folder_under_Merit_Lists, kind) or (None, None).
    kind is Final | Provisional for filename tagging.
    """
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
        return "CAP_Round_Cutoffs/Round_1"  # default bucket for generic CAP/cutoff docs
    if "vacancy" in u or "vacancy" in link_text.lower():
        return "Vacancy_Data"
    if "allotment" in u or "allot" in link_text.lower():
        return "Allotment_Results"
    if "seat" in u and "matrix" in u:
        return "Seat_Matrix/Institute_wise"
    if "scholar" in blob or "fee waiver" in blob or "tfws" in blob:
        return "Scholarship_Data"
    return None


def classify_college_meta(url: str, link_text: str) -> str | None:
    blob = (url + " " + link_text).lower()
    if "intake" in blob and "college" in blob:
        return "College_Details"
    if "institute" in blob and "list" in blob:
        return "College_Details"
    return None


def destination_for(url: str, link_text: str) -> str:
    parsed = urlparse(url)
    path_lower = (parsed.path or "").lower()

    merit_dir, merit_kind = classify_merit_pdf(url)
    if merit_dir and parsed.path.lower().endswith(".pdf"):
        return merit_dir

    cap_dir = classify_cap_or_cutoff(url, link_text)
    if cap_dir and parsed.path.lower().endswith(".pdf"):
        return cap_dir

    college_dir = classify_college_meta(url, link_text)
    if college_dir and parsed.path.lower().endswith(".pdf"):
        return college_dir

    if "viewpublicdocument" in path_lower:
        return "metadata/raw_documents"

    if parsed.path.lower().endswith(".pdf"):
        return "metadata/raw_documents"

    if parsed.path.lower().endswith((".xlsx", ".xls")):
        return "Seat_Matrix/Institute_wise"

    if parsed.path.lower().endswith(".zip"):
        return "Allotment_Results"

    return ""


def safe_filename_from_url(url: str, kind_prefix: str | None = None) -> str:
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


def download_file(session: requests.Session, url: str, dest: Path, timeout: int = 120) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        n = 0
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
                    n += len(chunk)
    return n


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(
    base_url: str,
    output_dir: Path,
    *,
    dry_run: bool,
    no_download: bool,
    timeout: int,
) -> list[DownloadRecord]:
    output_dir = output_dir.resolve()
    session = _session()
    html = fetch_html(session, base_url, timeout=timeout)
    records: list[DownloadRecord] = []
    unclassified: list[dict[str, str]] = []

    for full_url, text in iter_links(html, base_url):
        dest_rel = destination_for(full_url, text)
        if not dest_rel:
            unclassified.append({"url": full_url, "link_text": text})
            continue
        parsed = urlparse(full_url)
        if parsed.scheme not in ("http", "https"):
            continue

        merit_dir, merit_kind = classify_merit_pdf(full_url)
        fname = safe_filename_from_url(
            full_url, kind_prefix=merit_kind if merit_dir and parsed.path.lower().endswith(".pdf") else None
        )
        rel_path = Path(dest_rel) / fname
        abs_path = output_dir / rel_path

        if dry_run or no_download:
            print(f"[{'DRY' if dry_run else 'SKIP'}] {full_url} -> {rel_path.as_posix()}")
            continue

        if abs_path.exists() and abs_path.stat().st_size > 0:
            print(f"[exists] {abs_path}")
            b = abs_path.stat().st_size
            sha = file_sha256(abs_path)
            tag = dest_rel.split("/")[0]
            records.append(
                DownloadRecord(
                    url=full_url,
                    saved_path=rel_path.as_posix(),
                    sha256=sha,
                    category=tag,
                    bytes=b,
                )
            )
            continue

        try:
            if parsed.path.lower().endswith((".pdf", ".zip", ".xlsx", ".xls")):
                b = download_file(session, full_url, abs_path, timeout=timeout)
                sha = file_sha256(abs_path)
                print(f"[saved] {abs_path} ({b} bytes)")
                records.append(
                    DownloadRecord(
                        url=full_url,
                        saved_path=rel_path.as_posix(),
                        sha256=sha,
                        category=dest_rel.split("/")[0],
                        bytes=b,
                    )
                )
            else:
                # Non-binary document page — record URL only
                meta_path = output_dir / "metadata" / "linked_pages.jsonl"
                meta_path.parent.mkdir(parents=True, exist_ok=True)
                line = json.dumps({"url": full_url, "link_text": text, "suggested_folder": dest_rel})
                with meta_path.open("a", encoding="utf-8") as f:
                    f.write(line + "\n")
                print(f"[meta] {full_url} -> {dest_rel}")
        except requests.RequestException as e:
            print(f"[error] {full_url}: {e}", file=sys.stderr)

    meta_dir = output_dir / "metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)
    with (meta_dir / "unclassified_links.json").open("w", encoding="utf-8") as f:
        json.dump(unclassified, f, indent=2, ensure_ascii=False)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "downloads": [asdict(r) for r in records],
    }
    with (meta_dir / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return records


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Scrape Maharashtra FE portal links and download PDFs.")
    p.add_argument(
        "--base-url",
        default=DEFAULT_BASE,
        help="Homepage or landing page to parse for anchors.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "Maharashtra-FE-Admission-Dataset",
        help="Dataset root (README layout).",
    )
    p.add_argument("--dry-run", action="store_true", help="Print planned downloads only.")
    p.add_argument(
        "--no-download",
        action="store_true",
        help="Parse and write manifests only (no binary downloads).",
    )
    p.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds.")
    args = p.parse_args(argv)

    out = args.output_dir
    if not args.dry_run and not args.no_download:
        out.mkdir(parents=True, exist_ok=True)

    run(
        args.base_url,
        out,
        dry_run=args.dry_run,
        no_download=args.no_download,
        timeout=args.timeout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
