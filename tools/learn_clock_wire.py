#!/usr/bin/env python3
"""learn_clock_wire.py — the wire between the dispatcher's live fold flow and the learn-clock.

The clock measures; the dispatcher IS the intake. At fold time the dispatcher reads
each worker's sign-out and decides PROMOTE / LOG / DROP — that decision IS the T2
triage verdict. This wire stamps it at the moment it becomes true, with the fold
entry as evidence. It never manufactures: --evidence is required, stages arrive in
order (the clock enforces OutOfOrderError), and a retroactive --ts is used ONLY
with the verdict's true timestamp from the fold entry (the spec's retroactive
bootstrap, WIRING.md).

Commands:
  capture --title ... --evidence ... [--ts-event ISO]   # T0 (event) + T1 (captured)
  triage <lesson_id> --verdict PROMOTE|LOG|DROP --evidence ... [--ts ISO]  # T2
  verify <lesson_id> --evidence ... [--ts ISO]             # T6 (dispatcher fold: lesson independently VERIFIED by a different seat)
  compound <lesson_id> --evidence ... [--ts ISO]           # T7 (director review: lesson ADOPTED, later mechanism references it)
  status                                                 # dashboard: complete_through, lags, VERIFIED count

LIVE OWNERS (who calls the T6/T7 leg in production):
  T6 verify: the dispatcher at fold time — ONLY when the folded sign-out carries
  evidence that a DIFFERENT seat independently verified the lesson (verifier named
  + receipt). --evidence names that sign-out comment id. Never manufactured.
  T7 compound: the director's weekly review — when a lesson earns adopted_utc in
  lessons.jsonl because a later mechanism references it. --evidence names the
  review note.

T3+ stay on the hook CLI until their paths carry LC- ids: T3 needs a Smart Note
that names the LC- id; T4 needs briefs that name the LC- ids of T3 lessons.
BROADCAST-WATERMARK CHECK (Naya Eta, w175 — mirroring Alpha's w174
capture-side check): before cmd_capture mints a lesson id, it consults
t0-broadcast-watermark.json via learn_hook.capture_t0. If this event's T0 is
already broadcast, no duplicate is minted — the existing lesson id is returned
and the fold flow continues it at T1 (or reports honestly if the lesson is
already past T1). A malformed --ts-event fails closed: refuse to mint, mint
nothing, write nothing. On a fresh mint the fingerprint is recorded, so an
identical retry is idempotent. Fingerprint convention is the broadcast wire's:
content:<kind>:<at>:<sha16(title)>; --kind defaults to CAPTURE (the capture
path's kind). LEARN_CLOCK_WATERMARK overrides the watermark path (tests).

Today (w125) the broadcast/inject paths carry ZERO LC- ids — that namespace gap
is the next wire, not this one. This wire closes the T0/T1/T2 leg, which is the
leg the dispatcher owns outright.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from learn_clock import LearnClock, OutOfOrderError  # noqa: E402
from learn_hook import WATERMARK_PATH, capture_t0, _meta_write  # noqa: E402
from learn_hook import MalformedTimestampError  # noqa: E402

VERDICTS = ("PROMOTE", "LOG", "DROP")
WATERMARK_ENV = "LEARN_CLOCK_WATERMARK"


def _watermark_path():
    """The broadcast watermark path; env override exists for tests."""
    return Path(os.environ.get(WATERMARK_ENV, str(WATERMARK_PATH)))


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _all_lesson_ids(clock):
    if not clock.path.exists():
        return []
    seen = []
    with open(clock.path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lid = json.loads(line)["lesson_id"]
                if lid not in seen:
                    seen.append(lid)
    return seen


def cmd_capture(args):
    clock = LearnClock()
    kind = getattr(args, "kind", None) or "CAPTURE"
    try:
        res = capture_t0(clock, _watermark_path(), title=args.title,
                         evidence=args.evidence, ts=args.ts_event, kind=kind)
    except MalformedTimestampError as e:
        print(f"MALFORMED_TS: {e} (refused to mint: fail-closed)",
              file=sys.stderr)
        return 3
    lesson_id = res["lesson_id"]
    if res["duplicate_prevented"]:
        # T0 was already broadcast: do NOT re-mint it. The fold flow
        # continues the existing lesson; T1 is the fold's own capture record.
        out = {"lesson_id": lesson_id, "duplicate_prevented": True,
               "fingerprint": res["fingerprint"], "evidence": args.evidence}
        try:
            rec1 = clock.emit(lesson_id, 1)
            _meta_write(lesson_id, 1, args.title, args.evidence,
                        event_ts=rec1["ts"])
            out["stages"] = ["T1_CAPTURED (T0 reused, no duplicate minted)"]
        except OutOfOrderError as e:
            out["stages"] = []
            out["note"] = f"T1 not emitted: lesson already past T1 ({e})"
        print(json.dumps(out, indent=2))
        print(f"LESSON_ID={lesson_id}  (existing — T0 reused, no duplicate)")
        return 0
    rec0_ts = res["ts"]
    _meta_write(lesson_id, 0, args.title, args.evidence, event_ts=rec0_ts)
    rec1 = clock.emit(lesson_id, 1)
    _meta_write(lesson_id, 1, args.title, args.evidence, event_ts=rec1["ts"])
    print(json.dumps({"lesson_id": lesson_id, "stages": ["T0_EVENT", "T1_CAPTURED"],
                      "duplicate_prevented": False,
                      "evidence": args.evidence}, indent=2))
    print(f"LESSON_ID={lesson_id}  (use this for triage)")
    return 0


def cmd_triage(args):
    clock = LearnClock()
    rec = clock.emit(args.lesson_id, 2, ts=args.ts)
    _meta_write(args.lesson_id, 2, None,
                f"VERDICT={args.verdict} :: {args.evidence}",
                event_ts=rec["ts"], verdict=args.verdict)
    print(json.dumps({"lesson_id": args.lesson_id, "stage": "T2_TRIAGED",
                      "verdict": args.verdict, "evidence": args.evidence}, indent=2))
    return 0


def cmd_verify(args):
    """T6 VERIFIED — dispatcher fold: lesson independently verified by a different seat."""
    clock = LearnClock()
    rec = clock.emit(args.lesson_id, 6, ts=args.ts)
    _meta_write(args.lesson_id, 6, None,
                f"VERIFIED :: {args.evidence}",
                event_ts=rec["ts"])
    print(json.dumps({"lesson_id": args.lesson_id, "stage": "T6_VERIFIED",
                      "evidence": args.evidence}, indent=2))
    return 0


def cmd_compound(args):
    """T7 COMPOUNDED — director review: lesson adopted by a later mechanism."""
    clock = LearnClock()
    rec = clock.emit(args.lesson_id, 7, ts=args.ts)
    _meta_write(args.lesson_id, 7, None,
                f"COMPOUNDED :: {args.evidence}",
                event_ts=rec["ts"])
    print(json.dumps({"lesson_id": args.lesson_id, "stage": "T7_COMPOUNDED",
                      "evidence": args.evidence}, indent=2))
    return 0


def cmd_status(_args):
    clock = LearnClock()
    rows = []
    for lid in sorted(_all_lesson_ids(clock)):
        st = clock.status(lid)
        lags = clock.lags(lid)
        rows.append({"lesson_id": lid, "complete_through": st["complete_through"],
                     "missing": st["missing"], "latency_min": clock.latency(lid),
                     "meets_60min": clock.meets_target(lid), "lags": lags})
    verified = sum(1 for r in rows if "T6_VERIFIED" not in r["missing"])
    print(json.dumps({"lessons": rows, "total": len(rows),
                      "verified_T6": verified}, indent=2))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="wire the dispatcher fold flow to the learn-clock")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("capture", help="T0+T1 at fold time")
    p.add_argument("--title", required=True, help="lesson title")
    p.add_argument("--evidence", required=True, help="sign-out comment id / log line (required, fail-closed)")
    p.add_argument("--ts-event", default=None, help="ISO UTC timestamp of the observed event (retroactive only)")
    p.add_argument("--kind", default="CAPTURE",
                   help="fingerprint kind (must match the broadcast item's kind to dedupe)")
    p.set_defaults(fn=cmd_capture)

    p = sub.add_parser("triage", help="T2 at fold time")
    p.add_argument("lesson_id")
    p.add_argument("--verdict", required=True, choices=VERDICTS)
    p.add_argument("--evidence", required=True, help="fold entry naming the verdict (required, fail-closed)")
    p.add_argument("--ts", default=None, help="ISO UTC timestamp of the verdict (retroactive only)")
    p.set_defaults(fn=cmd_triage)

    p = sub.add_parser("verify", help="T6 at dispatcher fold (different-seat independent verification)")
    p.add_argument("lesson_id")
    p.add_argument("--evidence", required=True, help="verifier's sign-out comment id / receipt (required, fail-closed)")
    p.add_argument("--ts", default=None, help="ISO UTC timestamp of the verification (retroactive only)")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("compound", help="T7 at director review (lesson adopted by a later mechanism)")
    p.add_argument("lesson_id")
    p.add_argument("--evidence", required=True, help="director review note naming the adopting mechanism (required, fail-closed)")
    p.add_argument("--ts", default=None, help="ISO UTC timestamp of the adoption (retroactive only)")
    p.set_defaults(fn=cmd_compound)

    p = sub.add_parser("status", help="learning dashboard")
    p.set_defaults(fn=cmd_status)

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except OutOfOrderError as e:
        print(f"OUT_OF_ORDER: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
