#!/usr/bin/env python3
"""Deterministic duplicate/entity-resolution audit for the Naya Power Superbrain.

Canonical events remain the source of truth. This runtime never silently merges
records: high-confidence duplicates are rejected, while ambiguous candidates are
reported as LINK/REVIEW candidates for an explicit decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import timedelta
from pathlib import Path

import smart_notes_v3 as brain

MEMORY = Path(__file__).resolve().parent
REPORT = MEMORY / "DUPLICATE-ENTITY-AUDIT.json"


def norm(value: object) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(value or "").lower()))


def list_values(value):
    if isinstance(value, str):
        return [value]
    return value if isinstance(value, list) else []


def stable_payload(event: dict) -> dict:
    reps = []
    for rep in brain.reps(event):
        reps.append({
            "representation": rep.get("representation"),
            "summary": norm(rep.get("summary")),
            "content": norm(rep.get("content")),
            "lessons": [norm(x) for x in list_values(rep.get("lessons") or rep.get("what_we_learned") or rep.get("learning"))],
            "what_changed": [norm(x) for x in list_values(rep.get("what_changed"))],
            "next_best_actions": [norm(x) for x in list_values(rep.get("next_best_actions"))],
        })
    return {
        "title": norm(event.get("title")),
        "subject": norm(event.get("subject")),
        "project": norm(event.get("project")),
        "event_type": norm(event.get("event_type") or event.get("type")),
        "summary": norm(event.get("summary")),
        "tags": sorted(norm(x) for x in list_values(event.get("tags"))),
        "aliases": sorted(norm(x) for x in list_values(event.get("aliases"))),
        "concepts": sorted(norm(x) for x in list_values(event.get("concepts"))),
        "representations": sorted(reps, key=lambda x: (x.get("representation") or "", x.get("summary") or "")),
    }


def fingerprint(event: dict) -> str:
    raw = json.dumps(stable_payload(event), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def entity_keys(event: dict) -> set[str]:
    keys = set()
    for field in ("subject", "project"):
        value = norm(event.get(field))
        if value:
            keys.add(f"{field}:{value}")
    for field in ("tags", "concepts", "aliases"):
        for value in list_values(event.get(field)):
            value = norm(value)
            if value:
                keys.add(f"{field}:{value}")
    return keys


def token_set(event: dict) -> set[str]:
    return set(brain.tokens(brain.all_text(event)))


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def classify(a: dict, b: dict) -> dict:
    fp_same = fingerprint(a) == fingerprint(b)
    keys_a, keys_b = entity_keys(a), entity_keys(b)
    entity_overlap = len(keys_a & keys_b) / max(1, min(len(keys_a), len(keys_b)))
    lexical = jaccard(token_set(a), token_set(b))
    try:
        ta, tb = brain.parse_time(a["effective_at"]), brain.parse_time(b["effective_at"])
        time_hours = abs((ta - tb).total_seconds()) / 3600.0
    except Exception:
        time_hours = float("inf")
    same_subject = norm(a.get("subject")) == norm(b.get("subject")) and bool(norm(a.get("subject")))
    same_title = norm(a.get("title")) == norm(b.get("title")) and bool(norm(a.get("title")))
    if fp_same:
        decision = "DUPLICATE"
        confidence = 1.0
    elif same_subject and same_title and time_hours <= 24:
        decision = "LINK_OR_REVIEW"
        confidence = min(0.99, 0.65 + 0.20 * entity_overlap + 0.15 * lexical)
    elif entity_overlap >= 0.85 and lexical >= 0.80 and time_hours <= 48:
        decision = "LINK_OR_REVIEW"
        confidence = min(0.95, 0.55 + 0.25 * entity_overlap + 0.20 * lexical)
    else:
        decision = "DISTINCT"
        confidence = max(entity_overlap, lexical) * 0.5
    return {
        "a": a["event_id"],
        "b": b["event_id"],
        "decision": decision,
        "confidence": round(confidence, 4),
        "entity_overlap": round(entity_overlap, 4),
        "lexical_similarity": round(lexical, 4),
        "time_distance_hours": round(time_hours, 3) if time_hours != float("inf") else None,
    }


def audit() -> dict:
    events = [e for _, e in brain.load_events() if not e.get("__parse_error__")]
    pairs = []
    duplicate_ids = []
    for i, a in enumerate(events):
        for b in events[i + 1 :]:
            result = classify(a, b)
            if result["decision"] != "DISTINCT":
                pairs.append(result)
            if result["decision"] == "DUPLICATE":
                duplicate_ids.extend([result["a"], result["b"]])
    duplicate_ids = sorted(set(duplicate_ids))
    status = "GREEN" if not duplicate_ids else "RED"
    report = {
        "schema_version": 1,
        "status": status,
        "canonical_event_count": len(events),
        "exact_duplicate_count": len(duplicate_ids),
        "exact_duplicate_event_ids": duplicate_ids,
        "candidates": sorted(pairs, key=lambda x: (-x["confidence"], x["a"], x["b"])),
        "policy": "Exact duplicate = CI failure. Ambiguous LINK_OR_REVIEW candidates are surfaced, never silently merged.",
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fail-on-ambiguous", action="store_true")
    args = ap.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["exact_duplicate_count"]:
        return 1
    if args.fail_on_ambiguous and any(x["decision"] == "LINK_OR_REVIEW" for x in report["candidates"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
