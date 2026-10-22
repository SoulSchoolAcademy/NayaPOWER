#!/usr/bin/env python3
"""build_rows.py — build the 26 Daily Intelligence rows for Nitro's package.

Reads the filed editions in ./sources/ (downloaded byte-exact from
SoulSchoolAcademy/NayaPOWER main @ f289672e, 2026-10-22) and emits:
  rows.json       — one object per day, newest data identical to the SQL
  rows-seed.sql   — INSERTs into public.hub_daily_intelligence_reports
                    (dollar-quoted bodies, ON CONFLICT re-runnable)

Row shape follows the 2026-10-21 edition's format:
  headline        — LEARNING-EVENT days: the day's first lesson title.
                    IB-DIR days: "The major intelligence of the day" /
                    "The big shift" line, else the briefing subtitle,
                    else the first bold span of the intro.
  lessons_summary — LEARNING-EVENT days: the "## THE DAILY INTELLIGENCE"
                    section verbatim (lessons + declared behavior changes).
                    IB-DIR days: the SURVIVE / REMEMBER / TORCH sections
                    verbatim, else the first two sections.
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
SOURCE_PATHS = {
    "2026-09-27": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/09/27/IB-DIR-NAYAPOWER-20260927-001.md",
    "2026-09-28": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/09/28/IB-DIR-NAYAPOWER-20260928-001.md",
    "2026-09-29": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/09/29/IB-DIR-NAYAPOWER-20260929-001.md",
    "2026-09-30": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/09/30/IB-DIR-NAYAPOWER-20260930-001.md",
    "2026-10-01": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/01/IB-DIR-NAYAPOWER-20261001-001.md",
    "2026-10-02": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/02/IB-DIR-NAYAPOWER-20261002-001.md",
    "2026-10-03": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/03/IB-DIR-NAYANET-20261003-001.md",
    "2026-10-04": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026-10-04-LEARNING-EVENT.md",
    "2026-10-05": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/05/IB-DIR-NAYAPOWER-20261005-001.md",
    "2026-10-06": "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/06/IB-DIR-NAYAPOWER-20261006-001.md",
}
for d in range(7, 23):
    SOURCE_PATHS[f"2026-10-{d:02d}"] = (
        f"BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026-10-{d:02d}-LEARNING-EVENT.md")


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


def headline_for(text: str, is_le: bool) -> str:
    if is_le:
        m = re.search(r"(?m)^### 1\.\s*(.+)$", text)
        if m:
            return strip_md(m.group(1))
    for pat in (r"\*\*The major intelligence of the day:\*\*\s*(.+)",
                r"\*\*The big shift:\*\*\s*(.+)"):
        m = re.search(pat, text)
        if m:
            return strip_md(m.group(1))
    m = re.search(r"big picture is:\s*\*\*(.+?)\*\*", text)  # 2026-10-01 form
    if m:
        return strip_md(m.group(1))
    m = re.search(r"(?ms)^## Current Signal\s*\n\*\*(.+?)\*\*", text)  # 2026-10-03 form
    if m:
        return strip_md(m.group(1))
    m = re.search(r"(?m)^# [^\n]*Briefing — [^\n]*—\s*([^\n]{3,120})$", text)
    if m:
        return strip_md(m.group(1))
    m = re.search(r"\*\*([^*]{25,180})\*\*", text)
    if m:
        return strip_md(m.group(1))
    raise ValueError("no headline extractable")


def lessons_for(text: str, is_le: bool) -> str:
    secs = sections(text)
    if is_le:
        for h, block in secs:
            if h.upper().startswith("## THE DAILY INTELLIGENCE"):
                return block.strip()
        # Pre-standardization formats: 2026-10-09 keeps lessons under
        # "## Distilled intelligence", 2026-10-11 under "## Distilled
        # lessons (each changes what a Naya does tomorrow)" — same
        # ### N. item shape, same declared-change discipline.
        for h, block in secs:
            if h.startswith("## Distilled"):
                return block.strip()
        raise ValueError("LEARNING-EVENT without a lessons section")
    keep_idx = [i for i, (h, _) in enumerate(secs)
                if re.search(r"SURVIVE|REMEMBER|TORCH|DESERVES", h, re.I)]
    if keep_idx:
        # Contiguous span, first kept section → last kept section: a
        # verbatim slice of the body (blocks are consecutive by split).
        span = "".join(b for _, b in secs[keep_idx[0]:keep_idx[-1] + 1])
        return span.strip()
    if len(secs) >= 2:
        return "".join(b for _, b in secs[:2]).strip()
    return text.strip()


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
        text = f.read_text(encoding="utf-8")
        is_le = "LEARNING-EVENT" in SOURCE_PATHS[d] and "IB-DIR" not in SOURCE_PATHS[d]
        rows.append({
            "report_date": d,
            "report_id": report_id_for(text, d),
            "headline": headline_for(text, is_le),
            "lessons_summary": lessons_for(text, is_le),
            "body_md": text,
            "source_path": SOURCE_PATHS[d],
        })
    (HERE / "rows.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "-- rows-seed.sql — Daily Intelligence Reports seed, 26 rows, 2026-09-27 → 2026-10-22.",
        "-- Generated by build_rows.py from the filed editions on NayaPOWER main",
        "-- @ f289672e78c2b314cbb76a6f08d8f7c273a58b88 (sources in ./sources/).",
        "-- Run AFTER schema.sql. Re-runnable: ON CONFLICT refreshes the row.",
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
        print(f"  {r['report_date']}  [{r['report_id']}]  {r['headline'][:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
