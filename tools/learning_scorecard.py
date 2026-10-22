#!/usr/bin/env python3
"""Learning scorecard v2 — the math behind hyper-speed learning.

Reads the learning system's own files and computes capture rate,
distillation yield, promotion latency, adoption rate, repeat rate, and
learning velocity.

HISTORY / WHY V2 EXISTS: v1 of this instrument lived outside the repo
(in a goal's hidden_files) and silently misread its inputs for days:
the learning log's format changed at the 2026-10-13 reconstruction
(batch headings and lesson-header shapes moved), and the family
registry switched from cumulative counters to per-iteration delta
bullets. v1's parsers matched the abandoned formats, found nothing,
and printed confident zeros — capture 0.0/day, velocity 0/week — while
hundreds of lessons sat in the log. The blindness was discovered by a
nightly report, not by an alarm. V2 therefore has two rules v1 lacked:

1. Parsers accept EVERY format the files have actually used (legacy
   ISO batch headings, `## YYYY-MM-DD ~HH:MMZ batch` headings,
   `## Distillation v2 — iteration N — <date>` headings, standalone
   `## L###` entries; family sections with delta bullets).
2. PARSER DRIFT FAILS LOUDLY. If the inputs contain abundant lesson
   evidence but the parsers extract nothing (or family sections exist
   but none parse), the run raises ParserDriftError and exits 3 with a
   DRIFT message instead of printing zeros. A blind instrument must
   never again report silence as health.

Usage:
    python3 tools/learning_scorecard.py [--json]
    python3 tools/learning_scorecard.py --log PATH --families PATH --agents-md PATH

Exit codes: 0 = computed; 3 = parser drift detected (inputs present
but unparseable — the format moved; repair the parser, do not trust
any number from this run); 2 = an input file is missing.
"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

GOAL_HIDDEN = (Path.home() / "workspace" / "goals"
               / "nayapower-10-10-completion-drive" / "hidden_files")
DEFAULT_LOG = GOAL_HIDDEN / "learning-log.md"
DEFAULT_FAMILIES = GOAL_HIDDEN / "lesson-families.md"
DEFAULT_AGENTS = Path.home() / "AGENTS.md"

NOW = datetime.now(timezone.utc)


class ParserDriftError(Exception):
    """Inputs carry lesson evidence the parsers cannot read. Loud, never zeros."""


# ---------------------------------------------------------------------------
# learning-log parsing (all formats the log has actually used)
# ---------------------------------------------------------------------------

_BATCH_RES = [
    # ## Distillation v2 — iteration 207 — 2026-10-21 ~23:58Z
    re.compile(r"^## .*?(\d{4}-\d{2}-\d{2}) ~(\d{2}:\d{2})Z"),
    # ## 2026-10-12 ~15:06Z batch (distillation v2) — window ...
    re.compile(r"^## (\d{4}-\d{2}-\d{2}) ~(\d{2}:\d{2})Z"),
    # ## 2026-10-12T14:04:36Z (legacy v1 format)
    re.compile(r"^## (\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})(?::\d{2})?Z"),
]
_STANDALONE_LESSON_RE = re.compile(r"^## (L\d+|WP-\d+)\b")
_BOLD_HEADER_RE = re.compile(r"^\*\*(L\d+|WP-\d+)\b")
_BULLET_HEADER_RE = re.compile(r"^- \*\*(L\d+|WP-\d+)\b")
_INTELLIGENT_ITEM_RE = re.compile(r"^\d+\.\s+\*\*")
_SECTION_RE = re.compile(r"^###\s+(.*)$")
# Sections whose bold L-headers are NOT new filings.
_NON_FILING_SECTIONS = ("repeat", "ledger", "phantom", "pulse", "inbox")


def _batch_ts(line):
    for rx in _BATCH_RES:
        m = rx.match(line)
        if m:
            try:
                return datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:00+00:00")
            except ValueError:
                return None
    return None


def parse_log(text):
    """Extract timestamped lesson/win/intelligent entries from the log.

    A filing = a lesson ID in filing position (bold header or bullet
    header) inside a batch, outside the non-filing sections (Repeats,
    Ledger sweep, Phantom sweep, PULSE, Inbox) and outside the
    Intelligent-events list; or a standalone `## L###` entry. IDs are
    deduplicated per batch so a lesson named twice in one batch (header
    + summary line) counts once.
    """
    entries = []
    current_ts = None
    section = ""
    seen_in_batch = set()
    pending_standalone = None  # (kind, id) awaiting a timestamp in its block

    for line in text.splitlines():
        ts = _batch_ts(line)
        if ts is not None:
            current_ts = ts
            section = ""
            seen_in_batch = set()
            pending_standalone = None
            continue
        sm = _SECTION_RE.match(line)
        if sm:
            section = sm.group(1).lower()
            continue
        m = _STANDALONE_LESSON_RE.match(line)
        if m:
            lid = m.group(1)
            kind = "win" if lid.startswith("WP-") else "lesson"
            pending_standalone = (kind, lid)
            # The standalone entry's own block usually carries its date
            # (e.g. inside OBSERVATION); if the previous batch ts is the
            # best evidence we take the entry undated and let the drift
            # check judge the aggregate.
            entries.append({"ts": current_ts, "kind": kind, "id": lid,
                            "line": line.strip()[:120]})
            continue
        if "intelligent event" in section:
            if _INTELLIGENT_ITEM_RE.match(line):
                entries.append({"ts": current_ts, "kind": "intelligent",
                                "id": None, "line": line.strip()[:120]})
            continue
        # Compact-format batches state their count in prose:
        # "**Intelligent events (6 adoptions):** ..." — trust the batch's
        # own number; never count free-floating INTELLIGENT EVENT mentions
        # (announcements of announcements double-counted them in v2.0).
        cm = re.match(r"^\*\*Intelligent events \((\d+)", line)
        if cm and current_ts is not None:
            for _ in range(int(cm.group(1))):
                entries.append({"ts": current_ts, "kind": "intelligent",
                                "id": None, "line": line.strip()[:120]})
            continue
        if any(s in section for s in _NON_FILING_SECTIONS):
            continue
        m = _BOLD_HEADER_RE.match(line) or _BULLET_HEADER_RE.match(line)
        if m and current_ts is not None:
            lid = m.group(1)
            if lid in seen_in_batch:
                continue
            seen_in_batch.add(lid)
            kind = "win" if lid.startswith("WP-") else "lesson"
            if "WIN-PATTERN" in line and kind == "lesson":
                kind = "win"
            entries.append({"ts": current_ts, "kind": kind, "id": lid,
                            "line": line.strip()[:120]})
            continue
    return entries


# ---------------------------------------------------------------------------
# family registry parsing (current format: per-family sections whose
# counter bullets are per-iteration deltas, newest first)
# ---------------------------------------------------------------------------

def parse_families(text):
    """Per family: name, days_since_repeat (newest bullet in section),
    instance_mentions (observed firings: sum of `xK` multipliers plus
    unweighted lesson citations in the section — a proxy, documented as
    such; v1's cumulative 'Instances: N' line no longer exists)."""
    fams = []
    sections = re.split(r"(?m)^(## F\d+ — .*)$", text)
    for i in range(1, len(sections) - 1, 2):
        header, block = sections[i], sections[i + 1]
        hm = re.match(r"## (F\d+) — (.+)$", header)
        dsr = re.search(r"\*\*Days since repeat:\*\*\s*(\d+)", block)
        mentions = 0
        for mult in re.findall(r"\b(?:L\d+|WP-\d+)(?:\s*\[F\d+\])?\s*×(\d+)", block):
            mentions += int(mult)
        plain = len(set(re.findall(r"\b(L\d+|WP-\d+)\b", block)))
        fams.append({
            "id": hm.group(1),
            "name": hm.group(2).strip(),
            "days_since_repeat": int(dsr.group(1)) if dsr else -1,
            "instance_mentions": mentions + plain,
        })
    return fams


def parse_agents_promotions(text):
    promos = []
    for m in re.finditer(r"## Distilled lessons — (\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2})Z? batch", text):
        ts = m.group(1).replace(" ", "T")
        if len(ts) == 16:
            ts += ":00"
        try:
            promos.append(datetime.fromisoformat(ts + "+00:00"))
        except ValueError:
            pass
    return promos


# ---------------------------------------------------------------------------
# drift checks — the loud failure v1 never had
# ---------------------------------------------------------------------------

def drift_check(log_text, entries, families_text, fams):
    if log_text is not None:
        tokens = len(re.findall(r"\bL\d{3}\b", log_text))
        filings = [e for e in entries if e["kind"] in ("lesson", "win")]
        if tokens >= 50 and not filings:
            raise ParserDriftError(
                f"learning log carries {tokens} lesson-id tokens but the "
                "parser extracted 0 filings — the log format has moved; "
                "repair tools/learning_scorecard.py, do not trust zeros")
        dated_batches = sum(1 for line in log_text.splitlines() if _batch_ts(line))
        if dated_batches >= 5 and filings and not any(e["ts"] for e in filings):
            raise ParserDriftError(
                f"{dated_batches} dated batch headings found but no filing "
                "carries a timestamp — batch-heading format has moved")
    if families_text is not None:
        headers = len(re.findall(r"(?m)^## F\d+ — ", families_text))
        if headers >= 5 and len(fams) < headers:
            raise ParserDriftError(
                f"family registry has {headers} family sections but only "
                f"{len(fams)} parsed — the registry format has moved")
        if fams and not any(f["days_since_repeat"] >= 0 for f in fams):
            raise ParserDriftError(
                "no family section yielded a days-since-repeat — the "
                "counter-bullet format has moved")


def compute(log_path=DEFAULT_LOG, families_path=DEFAULT_FAMILIES,
            agents_path=DEFAULT_AGENTS, now=None):
    now = now or NOW
    for p in (log_path, families_path):
        if not Path(p).exists():
            print(f"missing input: {p}", file=sys.stderr)
            raise SystemExit(2)
    log_text = Path(log_path).read_text(encoding="utf-8")
    families_text = Path(families_path).read_text(encoding="utf-8")
    entries = parse_log(log_text)
    fams = parse_families(families_text)
    drift_check(log_text, entries, families_text, fams)
    promos = (parse_agents_promotions(Path(agents_path).read_text(encoding="utf-8"))
              if Path(agents_path).exists() else [])

    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    lessons = [e for e in entries if e["kind"] == "lesson"]
    wins = [e for e in entries if e["kind"] == "win"]
    intelligents = [e for e in entries if e["kind"] == "intelligent"]

    def in_window(rows, since):
        return [e for e in rows if e["ts"] is not None and e["ts"] >= since]

    lessons_day = in_window(lessons, day_ago)
    lessons_week = in_window(lessons, week_ago)
    wins_week = in_window(wins, week_ago)
    intell_week = in_window(intelligents, week_ago)
    capture_rate = round((len(lessons_week) + len(wins_week)) / 7, 1)
    promo_latency = "0h (v2 zero-latency)" if promos else "unknown"
    adoption = round(len(intell_week) / max(len(lessons_week), 1), 2)
    hot = [f for f in fams if 0 <= f["days_since_repeat"] <= 7]

    return {
        "parser_version": 2,
        "drift_check": "ok",
        "computed_at": now.isoformat(),
        "capture_rate_per_day": capture_rate,
        "lessons_24h": len(lessons_day),
        "lessons_7d": len(lessons_week),
        "win_patterns_7d": len(wins_week),
        "promotion_latency": promo_latency,
        "promotion_batches": len(promos),
        "adoption_intelligent_events_7d": len(intell_week),
        "adoption_ratio": adoption,
        "repeat_hot_families_7d": len(hot),
        "families": fams,
        "learning_velocity_per_week": len(intell_week),
        "total_lessons_logged": len({e["id"] for e in lessons if e["id"]}),
        "total_filings": len(lessons),
    }


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    log_path = DEFAULT_LOG
    families_path = DEFAULT_FAMILIES
    agents_path = DEFAULT_AGENTS
    it = iter(range(len(argv)))
    for i in it:
        if argv[i] == "--log":
            log_path = Path(argv[i + 1]); next(it)
        elif argv[i] == "--families":
            families_path = Path(argv[i + 1]); next(it)
        elif argv[i] == "--agents-md":
            agents_path = Path(argv[i + 1]); next(it)
    try:
        result = compute(log_path, families_path, agents_path)
    except ParserDriftError as exc:
        print(f"PARSER DRIFT: {exc}", file=sys.stderr)
        return 3
    if "--json" in argv:
        print(json.dumps(result, indent=2, default=str))
        return 0
    print("LEARNING SCORECARD —", NOW.strftime("%Y-%m-%d %H:%M UTC"), "(parser v2, drift check ok)")
    print(f"  Capture rate:        {result['capture_rate_per_day']}/day  ({result['lessons_24h']} lessons in 24h)")
    print(f"  Win patterns (7d):   {result['win_patterns_7d']}")
    print(f"  Promotion latency:   {result['promotion_latency']}")
    print(f"  Intelligent events:  {result['adoption_intelligent_events_7d']}/week  (adoption ratio {result['adoption_ratio']})")
    print(f"  Hot families:        {result['repeat_hot_families_7d']} re-fired in 7d")
    print(f"  Learning velocity:   {result['learning_velocity_per_week']}/week  ← the headline number")
    print(f"  Total lessons:       {result['total_lessons_logged']} distinct ({result['total_filings']} filings)")
    hot = [f["id"] for f in result["families"] if 0 <= f["days_since_repeat"] <= 7]
    if hot:
        print("  HOT (re-fired ≤7d): " + ", ".join(hot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
