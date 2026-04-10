"""
Parse official MHT-CET engineering CAP cutoff PDFs (text layout used by CET Cell).
Used by import_cap_pdfs.py — no database side effects.
"""
from __future__ import annotations

import re
from typing import Any

import pdfplumber


def parse_cutoff_pdf(pdf_path: str, year: int, round_num: int) -> list[dict[str, Any]]:
    """
    Returns dicts: college_name, college_code, branch, seat_type, closing_percentile,
                  status_raw, year, round
    """
    records: list[dict[str, Any]] = []
    current_college = None
    current_college_code = None
    current_branch = None
    current_status = None

    print(f"  Parsing {pdf_path} ...", flush=True)

    with pdfplumber.open(pdf_path) as pdf:
        print(f"  Total pages: {len(pdf.pages)}", flush=True)
        for page in pdf.pages:
            try:
                text = page.extract_text()
            except Exception:
                continue
            if not text:
                continue

            lines = text.split("\n")
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                m = re.match(r"^(\d{5})\s+-\s+(.+)", line)
                if m:
                    current_college_code = m.group(1).strip()
                    current_college = m.group(2).strip()
                    i += 1
                    continue

                m = re.match(r"^(\d{9,10}T?)\s+-\s+(.+)", line)
                if m:
                    current_branch = m.group(2).strip()
                    i += 1
                    continue

                if line.startswith("Status:"):
                    current_status = line[7:].strip()
                    i += 1
                    continue

                if re.match(r"^Stage\s+[A-Z]", line):
                    cats = line.split()[1:]
                    while i + 1 < len(lines):
                        nxt = lines[i + 1].strip()
                        if (
                            nxt
                            and not re.match(
                                r"^(I{1,3}V?|IV|Legends|Maharashtra|"
                                r"Home|Other|State|All\s)",
                                nxt,
                            )
                            and not re.search(r"\d", nxt[:3])
                        ):
                            cats += nxt.split()
                            i += 1
                        else:
                            break

                    i += 1
                    while i < len(lines):
                        dline = lines[i].strip()
                        dm = re.match(r"^(I{1,4}|IV)\s+([\d\s]+)", dline)
                        if dm:
                            stage = dm.group(1)
                            pcts: list[float] = []
                            if i + 1 < len(lines):
                                pl = lines[i + 1]
                                pcts = [float(x) for x in re.findall(r"\((\d+\.\d+)\)", pl)]
                                if pcts:
                                    i += 1

                            if stage == "I" and current_college and current_branch:
                                for j, cat in enumerate(cats):
                                    cat = cat.strip()
                                    if j < len(pcts) and pcts[j] > 0:
                                        records.append(
                                            {
                                                "college_name": current_college,
                                                "college_code": current_college_code or "",
                                                "branch": current_branch,
                                                "seat_type": cat,
                                                "closing_percentile": pcts[j],
                                                "status_raw": current_status or "",
                                                "year": year,
                                                "round": round_num,
                                            }
                                        )
                            i += 1
                        else:
                            break
                    continue

                i += 1

        print(f"  Parsed {len(records)} raw records (round {round_num}).", flush=True)
    return records
