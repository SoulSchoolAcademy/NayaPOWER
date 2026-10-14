#!/usr/bin/env python3
"""learn_clock_broadcast_wire.py — honest T0 at the hive's observation point.

THE GAP: the fold wire (learn_clock_wire.py) stamps T0 at fold time. Live
evidence (2026-10-14): 5 of 6 lessons carry T0 == capture time, not event
time — manufactured history, exactly what WIRING.md forbids ("never in bulk
at the end"). Every latency number built on those T0s understates reality.

THIS WIRE: the broadcast collect pass
(hyper-speed-learning-mastery/hidden_files/broadcast.py --collect) fires
every wave and observes real events — fresh VERIFIED fixes, diary learnings,
drill results, TOOLS.md standing notes, dock NEW HIVE LESSON lines. For each
carried item this wire emits T0 with the ITEM'S OWN timestamp (the evidence's
time, never now) — the WIRING.md retroactive bootstrap made automatic.

Idempotent: a watermark (item fingerprint -> lesson_id) gives each real event
exactly one T0; re-runs emit nothing. Fail-closed: an item whose timestamp
cannot be parsed is skipped and counted, never guessed.

T1 is deliberately NOT emitted here — the fold flow owns T1 and can continue
the SAME lesson_id via this watermark (which also fixes the fold wire's
duplicate-id flaw for these items). Next wire: teach the fold flow to look
the watermark up before minting a new id.

This module never modifies broadcast.py: it imports its collectors.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLOCK_DIR = HERE  # placement: modules are co-located in tools/ (was _scratch)
BROADCAST_DIR = (Path.home() / "workspace" / "goals"
                 / "hyper-speed-learning-mastery" / "hidden_files")
sys.path.insert(0, str(CLOCK_DIR))
sys.path.insert(0, str(BROADCAST_DIR))
sys.path.insert(0, str(HERE))

from learn_clock import LearnClock  # noqa: E402
from learn_hook import _meta_write, _next_lesson_id  # noqa: E402

T0_WATERMARK = CLOCK_DIR / "t0-broadcast-watermark.json"


def _fingerprint(item):
    """Stable identity for a carried item. The broadcast _wm tag when the
    collector supplied one (tools/dock); otherwise kind+at+text hash."""
    tag = item.get("_wm")
    if tag:
        return "wm:" + ":".join(str(p) for p in tag)
    h = hashlib.sha256(item.get("text", "").encode("utf-8")).hexdigest()[:16]
    return f"content:{item.get('kind', '?')}:{item.get('at', '?')}:{h}"


def _event_ts(item):
    """The event's own timestamp as ISO UTC, or None (fail-closed).

    Date-only evidence (TOOLS.md sections, dock lines) carries day
    granularity: noon UTC, the same convention broadcast.py uses for
    freshness. Anything unparseable -> None: never guessed.
    """
    raw = (item.get("at") or "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        # date-only (YYYY-MM-DD): day granularity -> noon UTC convention
        if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
            dt = dt.replace(hour=12, minute=0, second=0,
                            tzinfo=timezone.utc)
        else:
            return None
    return dt.astimezone(timezone.utc).isoformat()


def _load_watermark(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_watermark(path, wm):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(wm, indent=1) + "\n", encoding="utf-8")


def wire_fresh_t0(items, clock=None, watermark_path=None, meta_writer=None):
    """Emit T0 for each carried item not already wired. Returns a report.

    items: collector-shaped dicts (at/kind/text/why, optional _wm).
    clock: LearnClock (defaults to the live clock).
    watermark_path: fingerprint->lesson_id store (defaults to live).
    meta_writer: defaults to learn_hook._meta_write; pass a fake in tests.
    """
    clock = clock or LearnClock()
    watermark_path = Path(watermark_path or T0_WATERMARK)
    meta_writer = meta_writer or _meta_write
    wm = _load_watermark(watermark_path)
    report = {"emitted": [], "already": [], "skipped": []}
    for item in items or []:
        fp = _fingerprint(item)
        if fp in wm:
            report["already"].append(
                {"fingerprint": fp, "lesson_id": wm[fp]})
            continue
        ts = _event_ts(item)
        if ts is None:
            report["skipped"].append(
                {"fingerprint": fp, "reason": "unparseable at",
                 "at": item.get("at")})
            continue
        lesson_id = _next_lesson_id(clock)
        rec = clock.emit(lesson_id, 0, ts=ts)
        kind, text = item.get("kind", "?"), item.get("text", "")
        meta_writer(lesson_id, 0, text[:80],
                    f"[{kind}] {text} | why: {item.get('why', '')} "
                    f"| source=broadcast-collect",
                    event_ts=rec["ts"])
        wm[fp] = lesson_id
        report["emitted"].append(
            {"fingerprint": fp, "lesson_id": lesson_id, "ts": rec["ts"],
             "kind": kind, "text": text[:80]})
    _save_watermark(watermark_path, wm)
    return report


def _is_t0_event(item):
    """T0 = a failure/win/surprise was OBSERVED. Passed drill rounds are
    routine practice, not learning events — emitting T0 for them would fill
    the clock with orphans that can never reach T6 (noise, not signal).
    Failed drills, verified fixes, diary learnings, mechanized TOOLS.md
    notes, and dock lessons all clear the bar."""
    if item.get("kind") == "DRILL":
        return "FAILED" in item.get("text", "")
    return True


def collect_fresh_items(broadcast_mod=None):
    """Every collector broadcast.py defines, minus the bus write, filtered
    to genuine T0 events (see _is_t0_event). Collectors are discovered
    dynamically (collect_* callables) so a new broadcast source is wired
    automatically — no silent omission when the bus grows a source."""
    if broadcast_mod is None:
        import broadcast as broadcast_mod  # noqa: E402
    collectors = sorted(
        name for name in vars(broadcast_mod)
        if name.startswith("collect_") and callable(vars(broadcast_mod)[name]))
    items = []
    for name in collectors:
        items.extend(vars(broadcast_mod)[name]())
    items = [i for i in items if _is_t0_event(i)]
    items.sort(key=lambda i: i.get("at", ""), reverse=True)
    return items


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="wire honest T0s from the broadcast collect pass")
    ap.add_argument("--run", action="store_true",
                    help="collect fresh items and emit missing T0s")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be emitted, emit nothing")
    args = ap.parse_args(argv)
    if not (args.run or args.dry_run):
        ap.print_help()
        return 1
    items = collect_fresh_items()
    if args.dry_run:
        clock = LearnClock()
        wm = _load_watermark(T0_WATERMARK)
        for i in items:
            fp = _fingerprint(i)
            print(("ALREADY " if fp in wm else "WOULD-EMIT ")
                  + fp + " at=" + str(i.get("at")))
        return 0
    report = wire_fresh_t0(items)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
