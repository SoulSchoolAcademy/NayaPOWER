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
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from learn_clock import LearnClock  # noqa: E402

STAGE_NAMES = ["T0_EVENT", "T1_CAPTURED", "T2_TRIAGED", "T3_DISTILLED",
               "T4_INJECTED", "T5_APPLIED", "T6_VERIFIED", "T7_COMPOUNDED"]
# Repo home (learn-clock graduation F-3): the meta log is runtime data in
# BRAIN/07-LEARNING/learn-clock/, next to the clock log — never in the
# code tree, never in scratch. No logic changed in the carry except the
# path; the F-3 fix (meta `ts` == clock event `ts`) rides along verbatim.
_REPO_ROOT = Path(__file__).resolve().parents[3]
META_LOG = _REPO_ROOT / "BRAIN" / "07-LEARNING" / "learn-clock" / "learn-lessons.jsonl"


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


def _meta_write(lesson_id, stage, title, evidence, event_ts=None,
                meta_log=None, **extra):
    """Append a meta row. `ts` is the EVENT time (== the clock row's ts);
    `written_ts` is the log-append time. Rows written before the 2026-10-14
    fix carried ts == write time (pre-fix); the clock JSONL is authoritative
    for event times on those rows. `extra` carries typed evidence fields.
    `meta_log` is a test seam (tests redirect writes to a tmp path);
    production callers leave it None and write to META_LOG."""
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
    target = Path(meta_log) if meta_log is not None else META_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def main(argv=None, *, clock_path=None, meta_log=None):
    """CLI entry. `clock_path` / `meta_log` are test seams (tests redirect
    both logs to tmp paths); production callers pass neither, and the
    hook writes to the repo log paths (DEFAULT_LOG / META_LOG)."""
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
    args = ap.parse_args(argv)

    stage = stages[args.stage]
    clock = LearnClock(path=clock_path) if clock_path is not None else LearnClock()

    if stage == 0:
        if not args.title:
            ap.error("t0 requires --title")
        if args.lesson_id:
            ap.error("t0 generates its own lesson id; do not pass one")
        lesson_id = _next_lesson_id(clock)
        title = args.title
    else:
        if not args.lesson_id:
            ap.error(f"{args.stage} requires the lesson id printed by t0")
        lesson_id = args.lesson_id
        title = None  # title was set at t0; meta log carries the stage evidence

    rec = clock.emit(lesson_id, stage, ts=args.ts)
    _meta_write(lesson_id, stage, title, args.evidence, event_ts=rec["ts"],
                meta_log=meta_log)
    print(json.dumps(rec, indent=2))
    if stage == 0:
        print(f"LESSON_ID={lesson_id}  (use this for t1..t7)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
