#!/usr/bin/env python3
"""Hourly report wrapper (08:00–22:00 UTC).

Covers the window since the last report of any type (hourly, morning, or
nightly). The Usefulness Gate (2026-10-09): only window-fresh,
timestamped items appear — stale or untimestamped items are dropped,
never recycled. One headline, What moved, Scoreboard (claim vs
authoritative, delta vs previous window), Needs from Shawn, Evidence.

Usage:
    python3 hourly_report.py [--save-dir DIR] [--no-save]

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
    STATE_DIR,
    load_watermarks,
    save_watermark,
)
import json  # noqa: E402

REPORT_TYPE = "hourly"
DEFAULT_SAVE_DIR = Path.home() / "workspace" / "reports"


def last_report_since(now: dt.datetime) -> dt.datetime:
    marks = load_watermarks()
    latest: dt.datetime | None = None
    for key in ("hourly", "morning", "nightly"):
        raw = marks.get(key)
        if not raw:
            continue
        try:
            ts = dt.datetime.fromisoformat(raw)
        except ValueError:
            continue
        if latest is None or ts > latest:
            latest = ts
    if latest is not None:
        return latest
    # Fallback: one hour ago.
    return now - dt.timedelta(hours=1)


def main() -> int:
    ap = argparse.ArgumentParser(description="Team Naya hourly report")
    ap.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = last_report_since(now)

    gen = ReportGenerator()
    report = gen.generate(REPORT_TYPE, since, now)

    if not args.no_save:
        outdir = Path(args.save_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        fname = f"hourly-{now.strftime('%Y%m%d-%H%M')}.md"
        (outdir / fname).write_text(report, encoding="utf-8")
        print(f"[saved: {outdir / fname}]", file=sys.stderr)

    save_watermark(REPORT_TYPE, now)
    # The PDF step must cover exactly this window — record it for
    # pdf_report.py --since so the two artifacts never disagree.
    (STATE_DIR / "last_window.json").write_text(
        json.dumps({"since": since.isoformat(),
                    "generated_at": now.isoformat()}),
        encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
