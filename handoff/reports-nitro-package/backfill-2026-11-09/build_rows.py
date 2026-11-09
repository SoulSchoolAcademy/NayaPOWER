#!/usr/bin/env python3
"""build_rows.py — build the 17 Daily Intelligence backfill rows (2026-10-24 → 2026-11-09).

Continuation of handoff/reports-nitro-package/build_rows.py (2026-10-22,
26 rows, 2026-09-27 → 2026-10-22). Same row shape, same transforms
(strip_md / sections / report_id_for / dq carried over verbatim), same
outputs:

  rows.json       — one object per day, identical content to the SQL
  rows-seed.sql   — INSERTs into public.hub_daily_intelligence_reports
                    (dollar-quoted bodies, ON CONFLICT re-runnable)

Sources: ./sources/<date>.md, downloaded byte-exact from
SoulSchoolAcademy/NayaPOWER main @ 3127852d09934f2fc5a67b81312a8ebc00f6dba4,
EXCEPT 2026-11-07, which does not exist on main: fetched byte-exact from
open PR #3295's head @ 21af3b9ad50f3bdbfb3560816655b9f76c6631dc
(branch resolve/dir-2026-11-07). Its source_path is the same repo path;
its provenance is the PR head, not main.

Format adaptation (this range's editions are the post-2026-10-24 DIR
format — neither LEARNING-EVENT nor IB-DIR, so the original headline /
lessons heading names do not occur; the package's shaping semantics are
applied to this format's own sections, verbatim slices only):

  headline        — the record's own one-line summary, DIR-mode per the
                    original README ("the record's own major intelligence
                    line"): "**The day in one line:**" (9 rows), else
                    "**Arc of the day:**" (5 rows, 2026-11-05 → 11-09),
                    else — the 3 rows carrying neither line
                    (2026-10-31, 2026-11-01, 2026-11-02) — the day's
                    first lesson title, the original default mode.
                    strip_md applied exactly as in the original.
  lessons_summary — the day's lessons section verbatim: the
                    "## 4. TOP 10 LESSONS…" block, present in all 17
                    editions in one consistent shape (the analogue of
                    the LE "## THE DAILY INTELLIGENCE" block and of the
                    honored pre-standardization variants, e.g.
                    "## Distilled intelligence"). The original IB-DIR
                    fallback (first two sections) was NOT used: it would
                    have put IN A NUTSHELL + THE DAY IN NUMBERS into
                    lessons_summary — not lessons.
  report_id       — report_id_for() unchanged: no edition in this range
                    carries a "Report ID:" line, so all 17 fall back to
                    DIR-NAYAPOWER-<date>, exactly as the original did.
  body_md         — the filed edition, byte-identical. Nothing re-authored.

Stdlib only. No network, no database writes — files only.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SOURCES = HERE / "sources"
TABLE = "hub_daily_intelligence_reports"
MAIN_TIP = "3127852d09934f2fc5a67b81312a8ebc00f6dba4"
PR3295_HEAD = "21af3b9ad50f3bdbfb3560816655b9f76c6631dc"

DATES = [
    "2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28",
    "2026-10-29", "2026-10-30", "2026-10-31", "2026-11-01", "2026-11-02",
    "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06", "2026-11-07",
    "2026-11-08", "2026-11-09",
]
SOURCE_PATHS = {
    d: f"BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/{d}-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md"
    for d in DATES
}


def strip_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s.strip().rstrip(".")


def sections(text: str):
    """Split into [(heading, block)] on ^## lines (block includes heading)."""
    parts = re.split(r"(?m)^(## .+)$", text)
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i] + parts[i + 1]))
    return out


def headline_for(text: str) -> str:
    # This format's own one-line summary lines (DIR-mode headline).
    for pat in (r"\*\*The day in one line:\*\*\s*(.+)",
                r"\*\*Arc of the day:\*\*\s*(.+)"):
        m = re.search(pat, text)
        if m:
            return strip_md(m.group(1))
    # Default mode (original LE rule, adapted to this format's numbered
    # bold lesson items): the day's first lesson title.
    m = re.search(r"(?ms)^## .*LESSONS.*?^\d+\.\s*\*\*(.+?)\*\*", text)
    if m:
        return strip_md(m.group(1))
    raise ValueError("no headline extractable")


def lessons_for(text: str) -> str:
    secs = sections(text)
    for h, block in secs:
        if re.match(r"## \d+\. TOP 10 LESSONS", h):
            return block.strip()
    raise ValueError("no ## N. TOP 10 LESSONS section")


def report_id_for(text: str, d: str) -> str:
    m = re.search(r"Report ID:\s*`?(DIR-[A-Z]+-\d{4}-\d{2}-\d{2})`?", text)
    return m.group(1) if m else f"DIR-NAYAPOWER-{d}"


def dq(s: str, tag: str) -> str:
    assert tag not in s, f"dollar-quote tag {tag} collides with body"
    return f"${tag}${s}${tag}$"


def main():
    rows = []
    for d in sorted(SOURCE_PATHS):
        f = SOURCES / f"{d}.md"
        if not f.exists():
            print(f"MISSING SOURCE: {d}", file=sys.stderr)
            return 1
        raw = f.read_bytes()
        text = raw.decode("utf-8")
        assert text.encode("utf-8") == raw, f"{d}: decode round-trip not byte-exact"
        rows.append({
            "report_date": d,
            "report_id": report_id_for(text, d),
            "headline": headline_for(text),
            "lessons_summary": lessons_for(text),
            "body_md": text,
            "source_path": SOURCE_PATHS[d],
        })
    (HERE / "rows.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "-- rows-seed.sql — Daily Intelligence Reports seed, 17 rows, 2026-10-24 → 2026-11-09.",
        "-- Generated by build_rows.py from the filed editions on NayaPOWER main",
        f"-- @ {MAIN_TIP} (sources in ./sources/), except 2026-11-07,",
        f"-- fetched from open PR #3295 head @ {PR3295_HEAD} (not on main).",
        "-- Portable form in the original package's shape, for Nitro's room build to ingest.",
        "-- Run AFTER schema.sql (if the table route is used). Re-runnable: ON CONFLICT refreshes the row.",
        "-- Bodies are dollar-quoted verbatim — the filed edition, byte-identical.",
        "",
        f"insert into public.{TABLE}",
        "  (report_date, report_id, headline, lessons_summary, body_md, source_path)",
        "values",
    ]
    vals = []
    for i, r in enumerate(rows):
        tag = f"naya{i}"
        vals.append(
            "  ('{d}', {rid}, {h}, {ls}, {b}, {sp})".format(
                d=r["report_date"],
                rid=dq(r["report_id"], tag + "r"),
                h=dq(r["headline"], tag + "h"),
                ls=dq(r["lessons_summary"], tag + "l"),
                b=dq(r["body_md"], tag + "b"),
                sp=dq(r["source_path"], tag + "s")))
    lines.append(",\n".join(vals))
    lines.append("on conflict (report_date) do update set")
    lines.append("  report_id = excluded.report_id, headline = excluded.headline,")
    lines.append("  lessons_summary = excluded.lessons_summary, body_md = excluded.body_md,")
    lines.append("  source_path = excluded.source_path, updated_at = now();")
    lines.append("")
    (HERE / "rows-seed.sql").write_text("\n".join(lines), encoding="utf-8")

    print(f"rows: {len(rows)}  range: {rows[0]['report_date']} → {rows[-1]['report_date']}")
    for r in rows:
        print(f"  {r['report_date']}  [{r['report_id']}]  {r['headline'][:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
