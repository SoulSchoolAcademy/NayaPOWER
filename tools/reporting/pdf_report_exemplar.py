#!/usr/bin/env python3
"""Hourly PDF entry point — shim (2026-10-09).

The 2026-10-08 "exemplar edition" renderer was retired with the hourly
report rebuild: it stamped the nine-team template and read as an ops
dump. The instrument renderer in pdf_report.py is now the single PDF
path for all report types. This module keeps the old CLI contract
(--type/--hours/--out) working by delegating to it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdf_report import build_pdf  # noqa: E402
from report_generator import ReportGenerator  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Team Naya PDF report (shim)")
    ap.add_argument("--type", default="hourly",
                    choices=["hourly", "morning", "nightly"])
    ap.add_argument("--hours", type=float, default=1.0)
    ap.add_argument("--out", default="/tmp/naya-report.pdf")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(hours=args.hours)
    gen = ReportGenerator()
    data = gen.collect(args.type, since, now)
    print(build_pdf(data, args.type, args.out))


if __name__ == "__main__":
    main()
