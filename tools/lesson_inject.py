#!/usr/bin/env python3
"""Lesson Injection Loop — Phase B injector (spec v1 §6.1).

Matches lessons to a mission like a key to a lock, ranks by Laplace-smoothed
hit rate, and emits the top lessons in one-line brief format.

Portable: no hardcoded paths. The lesson store is passed via --store.

Usage:
    python3 tools/lesson_inject.py --store lessons.jsonl \\
        --areas wave-dispatcher --mission-classes dispatch \\
        --failure-signatures void-dispatch

Spec §6.1:
  1. Filter: injectable status AND (area in applies_when.areas
     OR mission_class in applies_when.mission_classes
     OR any failure_signature matches the mission context).
  2. Rank: score = (hits + 1) / (injections + 2)  (Laplace smoothing).
  3. Select: top 5 by score; guarantee >= 1 exploration slot
     (injections < 3) whenever matching candidates exist.
  4. Format: `- [lesson] -> [changes] (lesson_id, hits/injections)`

Store format tolerance: accepts a JSON array OR JSON-lines; accepts both
`injections` and `injection_count` counter names; status normalized
case-insensitively. Lessons missing applies_when or enforcement are skipped
(spec §6.3 bounce rule: incomplete lessons never enter the store).
"""

import argparse
import json
import sys

CAP_DEFAULT = 5


def load_store(path):
    """Load a lesson store. Accepts a JSON array or JSON-lines."""
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read().strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        # A single JSON object (e.g. a one-line store) is valid JSONL.
    except json.JSONDecodeError:
        pass
    lessons = []
    for i, line in enumerate(raw.split("\n"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            lessons.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"store line {i}: invalid JSON: {exc}") from exc
    if not lessons:
        raise ValueError("store root must be a JSON array or JSON-lines")
    return lessons


def norm_status(lesson):
    return str(lesson.get("status", "active")).strip().lower()


def is_injectable(lesson):
    """Retired lessons never inject. Everything else active-ish injects."""
    return norm_status(lesson) not in ("retired",)


def counters(lesson):
    inj = lesson.get("injections", lesson.get("injection_count", 0))
    try:
        inj = int(inj)
    except (TypeError, ValueError):
        inj = 0
    try:
        hits = int(lesson.get("hits", 0))
    except (TypeError, ValueError):
        hits = 0
    try:
        misses = int(lesson.get("misses", 0))
    except (TypeError, ValueError):
        misses = 0
    return inj, hits, misses


def laplace(hits, injections):
    return (hits + 1) / (injections + 2)


def matches(lesson, areas, mission_classes, failure_signatures):
    """OR-match across applies_when tags. Failure signatures match against
    the union of the mission's own tags (the mission context)."""
    aw = lesson.get("applies_when")
    if not isinstance(aw, dict):
        return False
    if not lesson.get("enforcement"):
        return False  # bounce rule: incomplete lessons never inject
    lesson_areas = set(aw.get("areas") or [])
    lesson_classes = set(aw.get("mission_classes") or [])
    lesson_sigs = set(aw.get("failure_signatures") or [])
    mission_context = set(areas) | set(mission_classes) | set(failure_signatures)
    return bool(
        (lesson_areas & set(areas))
        or (lesson_classes & set(mission_classes))
        or (lesson_sigs & mission_context)
    )


def format_line(lesson, inj, hits):
    statement = str(lesson.get("lesson_statement", "")).strip()
    changes = str(lesson.get("enforcement", "")).strip()
    # One line each — brief bloat is the enemy. Cap the changes clause.
    if len(changes) > 160:
        changes = changes[:157].rstrip() + "..."
    lid = lesson.get("lesson_id", "?")
    return f"- {statement} → {changes} ({lid}, {hits}/{inj})"


def inject(lessons, areas, mission_classes, failure_signatures, cap=CAP_DEFAULT):
    matched = [l for l in lessons if is_injectable(l)
               and matches(l, areas, mission_classes, failure_signatures)]
    scored = []
    for lesson in matched:
        inj, hits, _misses = counters(lesson)
        scored.append((laplace(hits, inj), inj, hits, lesson))
    # Highest score first; ties broken by fewest injections (favor the untried).
    scored.sort(key=lambda t: (-t[0], t[1]))
    selected = scored[:cap]
    # Exploration guarantee: >=1 trial slot (injections < 3) when candidates exist.
    if scored and not any(t[1] < 3 for t in selected):
        trial = next((t for t in scored[cap:] if t[1] < 3), None)
        if trial is not None and selected:
            selected[-1] = trial
            selected.sort(key=lambda t: (-t[0], t[1]))
    return selected


def main(argv=None):
    ap = argparse.ArgumentParser(description="LIL Phase B injector (spec §6.1)")
    ap.add_argument("--store", required=True, help="Path to lessons store (JSON array or JSONL)")
    ap.add_argument("--areas", default="", help="Comma-separated mission areas")
    ap.add_argument("--mission-classes", default="", help="Comma-separated mission classes")
    ap.add_argument("--failure-signatures", default="", help="Comma-separated failure signatures")
    ap.add_argument("--top", type=int, default=CAP_DEFAULT, help="Max lessons to emit (default 5)")
    ap.add_argument("--format", choices=("text", "json"), default="text",
                    help="Output format (default text)")
    args = ap.parse_args(argv)

    def split(s):
        return [p.strip() for p in s.split(",") if p.strip()]

    areas = split(args.areas)
    mission_classes = split(args.mission_classes)
    failure_signatures = split(args.failure_signatures)

    try:
        lessons = load_store(args.store)
    except (OSError, ValueError) as exc:
        print(f"lesson_inject: error: {exc}", file=sys.stderr)
        return 2

    selected = inject(lessons, areas, mission_classes, failure_signatures, cap=args.top)

    if args.format == "json":
        out = [
            {
                "lesson_id": lesson.get("lesson_id"),
                "score": round(score, 4),
                "injections": inj,
                "hits": hits,
                "line": format_line(lesson, inj, hits),
            }
            for score, inj, hits, lesson in selected
        ]
        print(json.dumps(out, indent=2))
    else:
        for score, inj, hits, lesson in selected:
            print(format_line(lesson, inj, hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
