"""
Cleaning pipeline orchestrator — runs dedupe → missing → format → outliers → structural fixes.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cleaner import deduplication, format_standardizer, missing_data_handler, outlier_filter, structural_fix
from config import settings

logger = logging.getLogger(__name__)


def iter_data_csv_files(data_root: Path) -> list[Path]:
    """List CSV files under ``data_root`` excluding quality logs and manifests."""
    skip_parts = {"Data_Quality_Logs", "manifests", "metadata"}
    out: list[Path] = []
    for p in sorted(data_root.rglob("*.csv")):
        if any(part in skip_parts for part in p.parts):
            continue
        out.append(p)
    return out


def clean_one_file(path: Path, summary: dict[str, Any], data_root: Path) -> None:
    """Run the ordered pipeline on a single CSV path."""
    rel = path.relative_to(data_root).as_posix()
    logger.info("Cleaning %s", rel)
    try:
        df = pd.read_csv(path, dtype=str, low_memory=False)
    except (OSError, pd.errors.ParserError) as exc:
        logger.error("Skip unreadable %s: %s", path, exc)
        summary["files"].append({"file": rel, "error": str(exc)})
        return

    file_entry: dict[str, Any] = {"file": rel, "steps": {}}

    d1, m1 = deduplication.run_step(df)
    file_entry["steps"]["deduplication"] = m1

    miss_report = data_root / "Data_Quality_Logs" / "missing_data_report.csv"
    d2, m2 = missing_data_handler.run_step(d1, report_path=miss_report, source_file=rel)
    file_entry["steps"]["missing_data"] = m2

    d3, m3 = format_standardizer.run_step(d2)
    file_entry["steps"]["format"] = m3

    out_log = data_root / "Data_Quality_Logs" / "outlier_log.csv"
    d4, m4 = outlier_filter.run_step(d3, rel, log_path=out_log)
    file_entry["steps"]["outliers"] = m4

    err_csv = data_root / "Data_Quality_Logs" / "structural_errors.csv"
    master = data_root / "College_Details" / "master_college_list.csv"
    if not master.is_file():
        master.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=["college_code", "college_name"]).to_csv(master, index=False)

    d5, m5 = structural_fix.run_step(d4, master, err_csv, source_file=rel)
    file_entry["steps"]["structural"] = m5

    d5.to_csv(path, index=False)
    summary["files"].append(file_entry)


def run_pipeline(data_root: Path | None = None) -> dict[str, Any]:
    """
    Execute cleaning for all eligible CSV files.

    Returns:
        Summary dict written to ``cleaning_summary.json``.
    """
    root = data_root or settings.DATA_DIR
    logs = root / "Data_Quality_Logs"
    logs.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_root": root.as_posix(),
        "files": [],
        "duplicates_removed_total": 0,
    }

    for csv_path in iter_data_csv_files(root):
        clean_one_file(csv_path, summary, root)

    total_dupes = 0
    for fe in summary.get("files", []):
        if isinstance(fe, dict):
            d = (fe.get("steps") or {}).get("deduplication") or {}
            total_dupes += int(d.get("duplicates_removed", 0) or 0)
    summary["duplicates_removed_total"] = total_dupes

    summary_path = root / "Data_Quality_Logs" / "cleaning_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info("Wrote cleaning summary: %s", summary_path)
    return summary


def main(argv: list[str] | None = None) -> int:
    lvl = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Run MAHACET FE data cleaning pipeline.")
    p.add_argument(
        "--data-dir",
        type=Path,
        default=settings.DATA_DIR,
        help="Root data directory (default: project data/).",
    )
    args = p.parse_args(argv)
    run_pipeline(args.data_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
