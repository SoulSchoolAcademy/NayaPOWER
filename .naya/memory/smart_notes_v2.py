#!/usr/bin/env python3
"""Canonical Smart Notes v2 runtime.

Provides deterministic validation, chronological indexing, semantic retrieval,
and Daily Intelligence Report synthesis over Note Events. It never claims that a
product feed was posted; feed publication remains an integration boundary.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / ".naya" / "memory"
NOTES = MEMORY / "notes"
INDEX = MEMORY / "INDEX.json"
EVENT_RE = re.compile(r"^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
NOTE_RE = re.compile(r"^SN-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
REQUIRED = {"id","type","title","status","created_at","effective_at","source","summary","what_happened","what_we_learned","why_it_matters","what_changed","next_best_action","tags","aliases","relationships"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_notes():
    return [(p, load(p)) for p in sorted(NOTES.glob("*.json"))]


def parse_time(value):
    value = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timezone required")
    return dt


def validate_note(note, path):
    errors = []
    missing = REQUIRED - set(note)
    if missing:
        errors.append(f"{path}: missing {sorted(missing)}")
    if not NOTE_RE.match(note.get("id", "")):
        errors.append(f"{path}: invalid note id")
    if note.get("event_id") and not EVENT_RE.match(note["event_id"]):
        errors.append(f"{path}: invalid event id")
    for key in ("created_at", "effective_at"):
        try:
            parse_time(note[key])
        except Exception as exc:
            errors.append(f"{path}: invalid {key}: {exc}")
    if not isinstance(note.get("tags"), list) or not note["tags"]:
        errors.append(f"{path}: tags must be non-empty")
    if not isinstance(note.get("aliases"), list):
        errors.append(f"{path}: aliases must be a list")
    verification = note.get("verification")
    if verification and verification.get("status") == "VERIFIED" and not verification.get("canonical_url"):
        errors.append(f"{path}: verified note requires canonical_url")
    return errors


def validate():
    errors = []
    by_id = {}
    events = defaultdict(list)
    for path, note in all_notes():
        errors.extend(validate_note(note, path))
        nid = note.get("id")
        if nid in by_id:
            errors.append(f"duplicate note id: {nid}")
        by_id[nid] = path
        if note.get("event_id"):
            events[note["event_id"]].append(note)
    for event_id, members in events.items():
        reps = {m.get("representation") for m in members}
        if "NAYA" in reps and "HUMAN" in reps:
            timestamps = {m.get("created_at") for m in members}
            if len(timestamps) != 1:
                errors.append(f"{event_id}: paired representations must share created_at")
    try:
        idx = load(INDEX)
        indexed = set(idx.get("notes", []))
        actual = set(by_id)
        if indexed != actual:
            errors.append("INDEX.json does not exactly match note IDs")
    except Exception as exc:
        errors.append(f"INDEX.json invalid: {exc}")
    return errors


def temporal_index():
    buckets = defaultdict(list)
    for _, note in all_notes():
        dt = parse_time(note["effective_at"])
        key = dt.strftime("%Y/%m/%d/%H")
        buckets[key].append(note["id"])
    return {k: sorted(v) for k, v in sorted(buckets.items())}


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query, limit=10):
    q = tokens(query)
    results = []
    for _, note in all_notes():
        fields = [note.get("title", ""), note.get("summary", ""), note.get("why_it_matters", ""), " ".join(note.get("tags", [])), " ".join(note.get("aliases", []))]
        score = len(q & tokens(" ".join(fields)))
        if score:
            score += 2 if note.get("verification", {}).get("status") == "VERIFIED" else 0
            results.append((score, note))
    results.sort(key=lambda x: (-x[0], x[1].get("effective_at", ""), x[1].get("id", "")))
    return results[:limit]


def daily_report(day):
    start = datetime.fromisoformat(day + "T00:00:00+00:00")
    end = start + timedelta(days=1)
    selected = []
    for _, note in all_notes():
        dt = parse_time(note["effective_at"]).astimezone(start.tzinfo)
        if start <= dt < end:
            selected.append(note)
    return {
        "report_type": "DAILY_INTELLIGENCE_REPORT",
        "period": day,
        "generated_from_note_events": [n["id"] for n in selected],
        "event_count": len(selected),
        "wins": [n["title"] for n in selected if n.get("type") == "milestone"],
        "learning": [x for n in selected for x in n.get("what_we_learned", [])],
        "changes": [x for n in selected for x in n.get("what_changed", [])],
        "next_best_actions": [n.get("next_best_action") for n in selected if n.get("next_best_action")],
        "open_loops": [n["id"] for n in selected if n.get("status") in {"CONFLICTED", "STALE"}],
        "source_event_ids": [n.get("event_id", n["id"]) for n in selected],
        "verification_required": True,
        "feed_receipt_required_when_supported": True
    }


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("temporal-index")
    r = sub.add_parser("retrieve"); r.add_argument("query"); r.add_argument("--limit", type=int, default=10)
    d = sub.add_parser("daily-report"); d.add_argument("day", help="YYYY-MM-DD")
    args = ap.parse_args()
    if args.cmd == "validate":
        errors = validate()
        print("PASS — Smart Notes v2 is structurally valid" if not errors else "FAIL\n" + "\n".join(f"- {e}" for e in errors))
        return 0 if not errors else 1
    if args.cmd == "temporal-index":
        print(json.dumps(temporal_index(), indent=2, ensure_ascii=False)); return 0
    if args.cmd == "retrieve":
        for score, note in retrieve(args.query, args.limit):
            print(f"{score:3} {note['id']} | {note['title']} | {note['status']}")
        return 0
    print(json.dumps(daily_report(args.day), indent=2, ensure_ascii=False)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
