#!/usr/bin/env python3
"""learn_hook.py — the wiring between live work and the learn-clock.

The clock (learn_clock.py) measures; it does not change behavior. This hook
is the call site a worker or dispatcher uses AT THE EXACT MOMENT a stage
becomes true — never earlier (manufactured green), never in bulk at the end
(manufactured history).

Usage:
    learn_hook.py t0 --title "..." --evidence "..."     # observe an event; prints lesson id
    learn_hook.py t1 LC-20261014-001 --evidence "..."   # capture
    learn_hook.py t2 LC-20261014-001 --evidence "..."   # triage
    ... through t7.

Stage map (what evidence looks like):
    T0 EVENT      the failure/win/surprise is observed       e.g. "test went red", "403 landed", "watcher fired mid-wave"
    T1 CAPTURED   a capture candidate exists                 e.g. "win+why in sign-out", "wave log entry"
    T2 TRIAGED    intake returns a verdict                    e.g. "PROMOTE: every worker pushes"
    T3 DISTILLED  one-sentence principle + enforcement        e.g. "Smart Note filed with enforcement named"
    T4 INJECTED   principle is in a worker's live thinking context
    T5 APPLIED    a worker acted differently because of it
    T6 VERIFIED   control vs treatment proves it (different seat judges)
    T7 COMPOUNDED the machinery changed (briefing/law/checker updated)

Fail-closed: --evidence is REQUIRED for every emit. Stages must arrive in
order (the clock enforces this and raises loudly). A lesson id is generated
for T0 as LC-YYYYMMDD-NNN; later stages take the id printed at T0.

This file writes to the same append-only JSONL as learn_clock.py and adds a
companion meta log (learn-lessons.jsonl) carrying titles and evidence. It
never modifies the core clock module.

BROADCAST-WATERMARK CHECK (Naya Alpha, w174 — Eta's w173 Next): before the
t0 path mints a lesson id, it consults t0-broadcast-watermark.json — the
store the broadcast wire uses for fingerprint->lesson_id. If this event's T0
is already broadcast, no duplicate is minted: the existing lesson id is
returned for t1..t7 continuation. A malformed --ts fails closed (refuse to
mint; the timestamp is never guessed). On a fresh mint the fingerprint is
recorded, so a retry of the same capture is idempotent.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from learn_clock import LearnClock  # noqa: E402

STAGE_NAMES = ["T0_EVENT", "T1_CAPTURED", "T2_TRIAGED", "T3_DISTILLED",
               "T4_INJECTED", "T5_APPLIED", "T6_VERIFIED", "T7_COMPOUNDED"]
META_LOG = HERE / "learn-lessons.jsonl"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _next_lesson_id(clock):
    """LC-YYYYMMDD-NNN, NNN = today's next sequence."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"LC-{today}-"
    if not clock.path.exists():
        return prefix + "001"
    seen = set()
    with open(clock.path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seen.add(json.loads(line)["lesson_id"])
    n = 1
    while f"{prefix}{n:03d}" in seen:
        n += 1
    return f"{prefix}{n:03d}"


class MalformedTimestampError(ValueError):
    """--ts could not be parsed: fail closed, mint nothing."""


WATERMARK_PATH = HERE / "t0-broadcast-watermark.json"


def _canonical_event_ts(raw):
    """Strict event-time parse — the same convention as the broadcast wire
    (learn_clock_broadcast_wire._event_ts): ISO 8601 with timezone required;
    date-only (YYYY-MM-DD) means noon UTC. Anything else -> None: the
    timestamp is never guessed, and the caller fails closed."""
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
            dt = dt.replace(hour=12, minute=0, second=0, tzinfo=timezone.utc)
        else:
            return None
    return dt.astimezone(timezone.utc).isoformat()


def _at_variants(raw):
    """The exact-match serializations of one instant: as-passed, the +00:00
    canonical form, and the Z canonical form. The broadcast wire fingerprints
    the RAW at string, and collectors emit both Z and +00:00 styles — so the
    lookup enumerates every attested serialization. All three denote the same
    instant; nothing is guessed."""
    canon = _canonical_event_ts(raw)
    variants = []
    for v in (raw, canon):
        if v and v not in variants:
            variants.append(v)
    if canon and canon.endswith("+00:00"):
        zform = canon[:-6] + "Z"
        if zform not in variants:
            variants.append(zform)
    return variants


def _capture_fingerprint(kind, at, title):
    """The broadcast wire's fingerprint convention, applied to a capture-path
    event: content:<kind>:<at>:<sha16(title)>. For a hit against an
    already-broadcast item, kind/at/title must reproduce the broadcast
    item's kind/at/text exactly — pass --kind/--ts/--title accordingly."""
    h = hashlib.sha256((title or "").encode("utf-8")).hexdigest()[:16]
    return f"content:{kind}:{at}:{h}"


def _load_watermark(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _record_watermark(path, fingerprints, lesson_id):
    """Record fingerprint->lesson_id so a retry of the same capture (or a
    later broadcast pass) does not mint a second lesson for the same event."""
    path = Path(path)
    try:
        wm = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        wm = {}
    for fp in fingerprints:
        wm[fp] = lesson_id
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(wm, indent=1) + "\n", encoding="utf-8")


def capture_t0(clock, watermark_path, *, title, evidence, ts=None, kind="CAPTURE"):
    """T0 with broadcast-watermark dedup (Eta w173 Next).

    Before minting a lesson id, consult the broadcast watermark: if this
    event's T0 is already broadcast, return the existing lesson id and mint
    nothing (the fold flow continues that id at t1..t7). A malformed --ts
    raises MalformedTimestampError — fail closed, no mint, no clock row.
    On a fresh mint the fingerprint is recorded, making retries idempotent.
    """
    if ts is None:
        event_ts = _now_iso()
    else:
        event_ts = ts.strip()
        if not event_ts:
            raise MalformedTimestampError(
                "--ts was empty: refusing to mint a lesson id (fail-closed)")
    canon = _canonical_event_ts(event_ts)
    if canon is None:
        raise MalformedTimestampError(
            f"cannot parse --ts {ts!r}: refusing to mint a lesson id "
            f"(fail-closed)")
    fps = [_capture_fingerprint(kind, v, title) for v in _at_variants(event_ts)]
    wm = _load_watermark(watermark_path)
    for fp in fps:
        if fp in wm:
            return {"lesson_id": wm[fp], "stage": 0, "stage_name": "T0_EVENT",
                    "ts": canon, "emitted": False, "duplicate_prevented": True,
                    "fingerprint": fp}
    lesson_id = _next_lesson_id(clock)
    rec = clock.emit(lesson_id, 0, ts=canon)
    try:
        _record_watermark(watermark_path, fps, lesson_id)
    except Exception as e:  # the T0 happened; say so loudly, don't hide it
        print(f"WARNING: T0 emitted for {lesson_id} but watermark write "
              f"failed: {e}", file=sys.stderr)
    return {"lesson_id": lesson_id, "stage": 0, "stage_name": "T0_EVENT",
            "ts": rec["ts"], "emitted": True, "duplicate_prevented": False,
            "fingerprint": fps[0]}


def _meta_write(lesson_id, stage, title, evidence, event_ts=None, **extra):
    """Append a meta row. `ts` is the EVENT time (== the clock row's ts);
    `written_ts` is the log-append time. Rows written before the 2026-10-14
    fix carried ts == write time (pre-fix); the clock JSONL is authoritative
    for event times on those rows. `extra` carries typed evidence fields."""
    now = _now_iso()
    row = {
        "lesson_id": lesson_id,
        "stage": stage,
        "stage_name": STAGE_NAMES[stage],
        "ts": event_ts or now,
        "written_ts": now,
        "title": title,
        "evidence": evidence,
    }
    row.update(extra)
    META_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(META_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def main(argv=None):
    stages = {f"t{i}": i for i in range(8)}
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stage", choices=list(stages),
                    help="stage to stamp (t0..t7)")
    ap.add_argument("lesson_id", nargs="?",
                    help="lesson id (required for t1..t7, printed by t0)")
    ap.add_argument("--title",
                    help="lesson title (required for t0)")
    ap.add_argument("--evidence", required=True,
                    help="what actually happened / where the proof lives (required, fail-closed)")
    ap.add_argument("--ts", default=None,
                    help="ISO UTC timestamp (retroactive reconstruction only)")
    ap.add_argument("--kind", default="CAPTURE",
                    help="event kind for the broadcast-watermark fingerprint "
                         "(t0 only; default CAPTURE; use the broadcast kind — "
                         "DIARY, DRILL, VERIFIED FIX, TOOLS, DOCK — with the "
                         "broadcast's --ts/--title to dedup an already-"
                         "broadcast item)")
    args = ap.parse_args(argv)

    stage = stages[args.stage]
    clock = LearnClock()

    if stage == 0:
        if not args.title:
            ap.error("t0 requires --title")
        if args.lesson_id:
            ap.error("t0 generates its own lesson id; do not pass one")
        try:
            rep = capture_t0(clock, WATERMARK_PATH, title=args.title,
                             evidence=args.evidence, ts=args.ts, kind=args.kind)
        except MalformedTimestampError as e:
            ap.error(str(e))
        if rep["emitted"]:
            _meta_write(rep["lesson_id"], 0, args.title, args.evidence,
                        event_ts=rep["ts"])
            print(json.dumps(
                {"lesson_id": rep["lesson_id"], "stage": rep["stage"],
                 "stage_name": rep["stage_name"], "ts": rep["ts"]}, indent=2))
            print(f"LESSON_ID={rep['lesson_id']}  (use this for t1..t7)")
        else:
            print(json.dumps(rep, indent=2))
            print(f"LESSON_ID={rep['lesson_id']}  (already broadcast — "
                  f"reusing, no duplicate minted)")
        return 0

    if not args.lesson_id:
        ap.error(f"{args.stage} requires the lesson id printed by t0")
    lesson_id = args.lesson_id
    rec = clock.emit(lesson_id, stage, ts=args.ts)
    _meta_write(lesson_id, stage, None, args.evidence, event_ts=rec["ts"])
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
