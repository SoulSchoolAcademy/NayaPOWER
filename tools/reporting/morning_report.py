#!/usr/bin/env python3
"""Morning report wrapper (06:00 UTC).

Covers the overnight window: since the last nightly report (or 23:00 UTC
previous day if no watermark). Emphasis: overnight summary + today's
top priorities + current scores.

Usage:
    python3 morning_report.py [--save-dir DIR] [--no-save] [--print-only]

Output: markdown report to stdout, and saved under --save-dir
(default ~/workspace/reports/) unless --no-save.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_generator import (  # noqa: E402
    ReportGenerator,
    load_watermarks,
    save_watermark,
)

REPORT_TYPE = "morning"
DEFAULT_SAVE_DIR = Path.home() / "workspace" / "reports"


def overnight_since(now: dt.datetime) -> dt.datetime:
    marks = load_watermarks()
    nightly = marks.get("nightly")
    if nightly:
        try:
            return dt.datetime.fromisoformat(nightly)
        except ValueError:
            pass
    # Fallback: 23:00 UTC previous day.
    prev = now - dt.timedelta(days=1)
    return prev.replace(hour=23, minute=0, second=0, microsecond=0)


def main() -> int:
    ap = argparse.ArgumentParser(description="Team Naya morning report")
    ap.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = overnight_since(now)

    gen = ReportGenerator()
    report = gen.generate(REPORT_TYPE, since, now)

    if not args.no_save:
        outdir = Path(args.save_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        fname = f"morning-{now.strftime('%Y%m%d-%H%M')}.md"
        (outdir / fname).write_text(report, encoding="utf-8")
        print(f"[saved: {outdir / fname}]", file=sys.stderr)

    save_watermark(REPORT_TYPE, now)
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
