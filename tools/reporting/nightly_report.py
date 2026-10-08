#!/usr/bin/env python3
"""Nightly report wrapper (23:00 UTC).

Covers the full day: since 00:00 UTC. Emphasis: full-day summary,
intelligence learned, score movements, tomorrow's plan.

Usage:
    python3 nightly_report.py [--save-dir DIR] [--no-save]

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

REPORT_TYPE = "nightly"
DEFAULT_SAVE_DIR = Path.home() / "workspace" / "reports"


def main() -> int:
    ap = argparse.ArgumentParser(description="Team Naya nightly report")
    ap.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = now.replace(hour=0, minute=0, second=0, microsecond=0)

    gen = ReportGenerator()
    report = gen.generate(REPORT_TYPE, since, now)

    if not args.no_save:
        outdir = Path(args.save_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        fname = f"nightly-{now.strftime('%Y%m%d')}.md"
        (outdir / fname).write_text(report, encoding="utf-8")
        print(f"[saved: {outdir / fname}]", file=sys.stderr)

    save_watermark(REPORT_TYPE, now)
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
