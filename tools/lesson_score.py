#!/usr/bin/env python3
"""Lesson Injection Loop — Phase B scorer (spec v1 §6.2, §6.3).

Folds behavioral verdicts into the lesson store: updates hit/miss/injection
counters, then reports promotion and retirement candidates per the weekly
review thresholds. `unclear` verdicts are not counted. A worker's
`lesson_dispute` counts as a miss AND flags the lesson for director
rewrite review.

Portable: no hardcoded paths. Store and fold judgments passed as arguments.

Usage:
    python3 tools/lesson_score.py --store lessons.jsonl --fold judgments.json

Judgments file: JSON array (or JSON-lines) of:
    {"lesson_id": "L-...", "verdict": "hit"|"miss"|"unclear", "dispute": true|false}

Spec §6.2 thresholds:
  - Promote:  hits/(hits+misses) >= 0.80 AND injections >= 5  -> doctrine candidate
  - Retire:   hits/(hits+misses) <  0.30 AND injections >= 5  -> rewrite or retire
  - Trial:    injections < 3 -> unscored (still injected)

Counter updates are always written back. Status flips are REPORTED only;
pass --apply to flip candidate statuses (director's call, never automatic).
"""

import argparse
import copy
import json
import sys

VALID_VERDICTS = ("hit", "miss", "unclear")


def load_store(path):
    """Load a lesson store, remembering whether it was a JSON array or JSONL."""
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    stripped = raw.strip()
    if not stripped:
        return [], "array"
    try:
        data = json.loads(stripped)
        if isinstance(data, list):
            return data, "array"
        # A single JSON object (e.g. a one-line store) is valid JSONL.
    except json.JSONDecodeError:
        pass
    lessons = []
    for i, line in enumerate(stripped.split("\n"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            lessons.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"store line {i}: invalid JSON: {exc}") from exc
    if not lessons:
        raise ValueError("store root must be a JSON array or JSON-lines")
    return lessons, "jsonl"


def load_judgments(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read().strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        out = []
        for i, line in enumerate(raw.split("\n"), 1):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"judgments line {i}: invalid JSON: {exc}") from exc
        return out


def get_injections(lesson):
    for key in ("injections", "injection_count"):
        if key in lesson:
            try:
                return int(lesson[key])
            except (TypeError, ValueError):
                return 0
    return 0


def set_injections(lesson, value):
    # Preserve the store's own counter field name.
    if "injection_count" in lesson and "injections" not in lesson:
        lesson["injection_count"] = value
    else:
        lesson["injections"] = value


def hit_rate(lesson):
    try:
        hits = int(lesson.get("hits", 0))
    except (TypeError, ValueError):
        hits = 0
    try:
        misses = int(lesson.get("misses", 0))
    except (TypeError, ValueError):
        misses = 0
    total = hits + misses
    return (hits / total) if total else None


def score_store(lessons, judgments):
    """Apply fold judgments. Returns (deltas, disputes, unknown_ids,
    invalid_verdicts, applied, unclear_skipped).

    deltas: {lesson_id: {"hits": +n, "misses": +n, "injections": +n}}
    `unclear` verdicts are not counted. Disputes are NEVER silently dropped:
    a dispute counts as a miss AND flags the lesson for rewrite review,
    unconditionally (§6.2) — even when the verdict is `unclear` or malformed.
    Disagreement is data.
    """
    by_id = {l.get("lesson_id"): l for l in lessons}
    deltas = {}
    disputes = []
    unknown_ids = []
    invalid_verdicts = []
    applied = 0
    unclear_skipped = 0
    for j in judgments:
        lid = j.get("lesson_id")
        verdict = str(j.get("verdict", "")).strip().lower()
        disputed = bool(j.get("dispute"))
        lesson = by_id.get(lid)
        if lesson is None:
            unknown_ids.append(lid)  # surfaced, never silent — counters have no home
            continue
        if verdict not in VALID_VERDICTS and not disputed:
            invalid_verdicts.append({"lesson_id": lid, "verdict": j.get("verdict")})
            continue
        if verdict == "unclear" and not disputed:
            unclear_skipped += 1
            continue  # not counted, per spec
        d = deltas.setdefault(lid, {"hits": 0, "misses": 0, "injections": 0})
        if disputed:
            # §6.2 unconditional: dispute = miss + rewrite-review flag.
            # A dispute is data, never dropped — even on unclear/invalid verdict.
            d["misses"] += 1
            d["injections"] += 1
            lesson["needs_rewrite_review"] = True
            disputes.append(lid)
        elif verdict == "hit":
            d["hits"] += 1
            d["injections"] += 1
        else:  # miss
            d["misses"] += 1
            d["injections"] += 1
        applied += 1
    for lid, d in deltas.items():
        lesson = by_id[lid]
        lesson["hits"] = int(lesson.get("hits", 0)) + d["hits"]
        lesson["misses"] = int(lesson.get("misses", 0)) + d["misses"]
        set_injections(lesson, get_injections(lesson) + d["injections"])
    return deltas, disputes, unknown_ids, invalid_verdicts, applied, unclear_skipped


def review(lessons):
    """Weekly review scoring (spec §6.2). Returns candidate lists; the
    director decides, the script never auto-flips (unless --apply)."""
    promote, retire, trial = [], [], []
    for lesson in lessons:
        if str(lesson.get("status", "")).strip().lower() == "retired":
            continue
        inj = get_injections(lesson)
        rate = hit_rate(lesson)
        lid = lesson.get("lesson_id")
        if inj < 3:
            trial.append(lid)
            continue
        if rate is None or inj < 5:
            continue  # scored only at >= 5 injections with verdicts
        entry = {"lesson_id": lid, "hit_rate": round(rate, 4), "injections": inj,
                 "hits": lesson.get("hits", 0), "misses": lesson.get("misses", 0)}
        if rate >= 0.80:
            promote.append(entry)
        elif rate < 0.30:
            retire.append(entry)
    return promote, retire, trial


def write_store(path, lessons, fmt):
    with open(path, "w", encoding="utf-8") as fh:
        if fmt == "array":
            json.dump(lessons, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        else:
            for lesson in lessons:
                fh.write(json.dumps(lesson, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="LIL Phase B scorer (spec §6.2/§6.3)")
    ap.add_argument("--store", required=True, help="Path to lessons store (JSON array or JSONL)")
    ap.add_argument("--fold", required=True, help="Path to fold judgments (JSON array or JSONL)")
    ap.add_argument("--apply", action="store_true",
                    help="Flip candidate statuses (director's call; default: report only)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Compute everything but do not write the store")
    args = ap.parse_args(argv)

    try:
        lessons, fmt = load_store(args.store)
        judgments = load_judgments(args.fold)
    except (OSError, ValueError) as exc:
        print(f"lesson_score: error: {exc}", file=sys.stderr)
        return 2

    before = {l.get("lesson_id"): (get_injections(l), l.get("hits", 0), l.get("misses", 0))
              for l in lessons}
    deltas, disputes, unknown_ids, invalid_verdicts, applied, unclear_skipped = \
        score_store(lessons, judgments)
    promote, retire, trial = review(lessons)

    flipped = []
    if args.apply:
        for entry in promote:
            for lesson in lessons:
                if lesson.get("lesson_id") == entry["lesson_id"]:
                    lesson["status"] = "promoted"
                    flipped.append(entry["lesson_id"])
        for entry in retire:
            for lesson in lessons:
                if lesson.get("lesson_id") == entry["lesson_id"]:
                    lesson["status"] = "retired"
                    flipped.append(entry["lesson_id"])

    if not args.dry_run:
        try:
            write_store(args.store, lessons, fmt)
        except OSError as exc:
            print(f"lesson_score: error writing store: {exc}", file=sys.stderr)
            return 2

    after = {l.get("lesson_id"): (get_injections(l), l.get("hits", 0), l.get("misses", 0))
             for l in lessons}
    report = {
        "judgments_applied": applied,  # only judgments that actually moved counters
        "judgments_unclear_skipped": unclear_skipped,
        "unknown_lesson_ids": unknown_ids,
        "invalid_verdicts": invalid_verdicts,
        "disputes_flagged_rewrite_review": disputes,
        "counter_deltas": deltas,
        "promote_candidates": promote,
        "retire_candidates": retire,
        "trial_unscored": trial,
        "statuses_flipped": flipped if args.apply else [],
        "dry_run": args.dry_run,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
