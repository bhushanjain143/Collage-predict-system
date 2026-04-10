"""
Import MHT-CET engineering CAP cutoff PDFs into the ExplainAI `cutoffs` table.

Designed for PDFs from:
  https://github.com/jroshani281/data-

Clone the repo locally, then run (from this `backend` folder):

  pip install pdfplumber
  python import_cap_pdfs.py --pdf-dir "C:\\path\\to\\data-"

Optional:
  --replace-years 2025 2024   Delete existing rows for those years before insert
  --dry-run                   Only print which PDFs would be parsed

USEFUL files in that repo for this app:
  • *ENGG_CAP*_CutOff*.pdf  — official-style cutoff lists (best match)
  • *CAP*Round*2025*2026*.pdf, *cap*round*2025*2026*.pdf — 2025 rounds
  • *_round[1-4].pdf — alternate naming (e.g. 2024_round3.pdf)

LESS useful for the current college predictor (different structure / use case):
  • *SeatMatrix* — seat counts, not closing percentiles per college-branch-seat
  • *MeritList* / FE2025_*Merit* — candidate merit lists, not CAP cutoffs
"""
from __future__ import annotations

import argparse
import os
import sys

from cap_pdf_names import infer_year_round_from_path, skip_pdf_filename
from cutoff_geo import classify_college_type, extract_city, normalize_city
from pdf_cutoff_parser import parse_cutoff_pdf


def _dedupe_records(records: list[dict]) -> list[dict]:
    """Keep highest closing percentile per (college, branch, seat_type, year, round)."""
    seen: dict[tuple, dict] = {}
    for r in sorted(records, key=lambda x: -x["closing_percentile"]):
        key = (r["college_name"], r["branch"], r["seat_type"], r["year"], r["round"])
        if key not in seen:
            seen[key] = r
    return list(seen.values())


def _enrich(r: dict) -> None:
    raw_city = extract_city(r["college_name"])
    r["city"] = normalize_city(raw_city)
    r["college_type"] = classify_college_type(r.get("status_raw") or "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import CAP cutoff PDFs into cutoffs table")
    parser.add_argument(
        "--pdf-dir",
        required=True,
        help="Folder containing PDFs (e.g. cloned jroshani281/data- repo)",
    )
    parser.add_argument(
        "--replace-years",
        nargs="*",
        type=int,
        default=[],
        help="Delete existing cutoffs for these years before import",
    )
    parser.add_argument("--dry-run", action="store_true", help="List PDFs only, no DB writes")
    args = parser.parse_args()

    pdf_dir = os.path.abspath(args.pdf_dir)
    if not os.path.isdir(pdf_dir):
        print(f"Not a directory: {pdf_dir}", file=sys.stderr)
        return 1

    jobs: list[tuple[str, int, int]] = []
    for fn in sorted(os.listdir(pdf_dir)):
        if not fn.lower().endswith(".pdf"):
            continue
        path = os.path.join(pdf_dir, fn)
        meta = infer_year_round_from_path(path)
        if meta:
            jobs.append((path, meta[0], meta[1]))
            print(f"  OK  {fn}  ->  year={meta[0]}  round={meta[1]}")
        else:
            if not skip_pdf_filename(fn):
                print(f"  --- skip (unmatched name): {fn}")

    if not jobs:
        print("No matching CAP cutoff PDFs found.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"\nDry run: {len(jobs)} file(s). No database changes.")
        return 0

    all_raw: list[dict] = []
    for path, year, rnd in jobs:
        try:
            all_raw.extend(parse_cutoff_pdf(path, year, rnd))
        except Exception as e:
            print(f"ERROR parsing {path}: {e}", file=sys.stderr)
            return 1

    for r in all_raw:
        _enrich(r)

    deduped = _dedupe_records(all_raw)
    print(f"\nTotal raw: {len(all_raw)}  ->  after dedupe: {len(deduped)}")

    from app import app, db, Cutoff

    with app.app_context():
        if args.replace_years:
            for y in args.replace_years:
                n = Cutoff.query.filter_by(year=y).delete()
                db.session.commit()
                print(f"Deleted {n} existing row(s) for year {y}.")

        batch = 400
        for i in range(0, len(deduped), batch):
            chunk = deduped[i : i + batch]
            for r in chunk:
                db.session.add(
                    Cutoff(
                        college_name=(r["college_name"] or "")[:200],
                        college_code=(r.get("college_code") or "")[:20],
                        branch=(r["branch"] or "")[:300],
                        seat_type=(r["seat_type"] or "")[:30],
                        closing_percentile=float(r["closing_percentile"]),
                        year=int(r["year"]),
                        round=int(r["round"]),
                        city=(r.get("city") or "")[:500],
                        college_type=(r.get("college_type") or "Other")[:500],
                    )
                )
            db.session.commit()
            print(f"  Inserted {min(i + batch, len(deduped))}/{len(deduped)}...")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
