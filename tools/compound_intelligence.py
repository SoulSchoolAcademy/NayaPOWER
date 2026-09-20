#!/usr/bin/env python3
"""NayaPOWER Compounding Intelligence Bridge v1.

Canonical path:
INTELLIGENCE EVENT → SMART NOTE → LEARNING EVENT → EVIDENCE →
DAILY LEARNING → INTELLIGENCE FEED / COLLECTIVE PROJECTION.

This application layer reuses the existing promotion and Adaptive Learning
engines. It does not train model weights or create a second memory system.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_EVENT_DIR = ROOT / ".naya/memory/events"
# Canonical Note Events are the authoritative compounding input. EVENT_DIR is
# retained as the test-injection seam used by the existing bridge tests.
EVENT_DIR = CANONICAL_EVENT_DIR
LEARNING_DIR = ROOT / "MASTER-NOTES/ADAPTIVE-LEARNING"
DAILY_DIR = LEARNING_DIR / "DAILY"
COLLECTIVE_DIR = LEARNING_DIR / "COLLECTIVE"
FEED_DIR = ROOT / "MASTER-NOTES/INTELLIGENCE-FEED"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adaptive_learning as al  # noqa: E402

VERIFIED_RANK = al.evidence_rank("VERIFIED")


def load_events() -> list[dict[str, Any]]:
    """Load canonical SE-* events, or a flat injected test directory.

    The production path is deliberately recursive because canonical events are
    stored in YEAR/MONTH/DAY/HOUR buckets by canonical_event_store.py. A flat
    directory remains supported only for the existing deterministic unit tests.
    """
    events: list[dict[str, Any]] = []
    if not EVENT_DIR.exists():
        return events
    canonical_mode = EVENT_DIR == CANONICAL_EVENT_DIR
    paths = sorted(EVENT_DIR.rglob("SE-*.json")) if canonical_mode else sorted(EVENT_DIR.glob("*.json"))
    for path in paths:
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: invalid JSON: {exc}") from exc
        if not isinstance(event, dict) or not str(event.get("event_id", "")).startswith("SE-"):
            continue
        try:
            event["_path"] = str(path.relative_to(EVENT_DIR))
        except ValueError:
            event["_path"] = str(path)
        events.append(event)
    return events


def _first_smart_note_id(event: dict[str, Any]) -> str:
    explicit = event.get("smart_note_id")
    if isinstance(explicit, str) and explicit.startswith("SN-"):
        return explicit
    representations = event.get("representations") or {}
    if isinstance(representations, dict):
        for representation in representations.values():
            if isinstance(representation, dict):
                note_id = representation.get("id")
                if isinstance(note_id, str) and note_id.startswith("SN-"):
                    return note_id
    return ""


def _lesson_from_canonical_event(event: dict[str, Any]) -> str:
    direct = str(event.get("lesson", "")).strip()
    if direct:
        return direct
    learning = event.get("learning")
    if isinstance(learning, dict):
        for key in ("principle", "lesson", "problem"):
            value = str(learning.get(key, "")).strip()
            if value:
                return value
        lessons = learning.get("lessons")
        if isinstance(lessons, list) and lessons:
            return str(lessons[0]).strip()
    representations = event.get("representations") or {}
    if isinstance(representations, dict):
        for representation in representations.values():
            if not isinstance(representation, dict):
                continue
            lessons = representation.get("lessons")
            if isinstance(lessons, list) and lessons:
                return str(lessons[0]).strip()
            value = str(representation.get("lesson", "")).strip()
            if value:
                return value
    return ""


def _evidence_for_learning(event: dict[str, Any]) -> list[Any]:
    evidence = event.get("evidence")
    if isinstance(evidence, list) and evidence:
        return evidence
    verification = event.get("verification")
    if isinstance(verification, dict) and isinstance(verification.get("evidence"), list):
        return verification["evidence"]
    evidence_ids = event.get("evidence_ids")
    return evidence_ids if isinstance(evidence_ids, list) else []


def _evidence_state_for_learning(event: dict[str, Any]) -> str:
    explicit = str(event.get("evidence_state", "")).strip()
    if explicit in al.EVIDENCE_STATES:
        return explicit
    # This is a schema bridge, not a file-existence inference: VERIFIED is
    # accepted only when the canonical event itself carries VERIFIED status and
    # non-empty verification evidence. Otherwise the state remains UNKNOWN.
    verification = event.get("verification")
    if isinstance(verification, dict) and str(verification.get("status", "")).upper() == "VERIFIED" and verification.get("evidence"):
        return "VERIFIED"
    return "UNKNOWN"


def canonical_to_learning_input(event: dict[str, Any]) -> dict[str, Any]:
    """Normalize a canonical SE event into the existing learning-engine schema."""
    event_id = str(event.get("event_id", ""))
    if not event_id.startswith("SE-"):
        raise ValueError("canonical compounding input must use an SE-* event_id")
    note_id = _first_smart_note_id(event)
    lesson = _lesson_from_canonical_event(event)
    verification = event.get("verification") if isinstance(event.get("verification"), dict) else {}
    source = event.get("source")
    provenance = event.get("provenance")
    if not isinstance(provenance, dict):
        provenance = {"canonical_source": source, "canonical_event_id": event_id}
    normalized = dict(event)
    normalized["lesson"] = lesson
    normalized["learning"] = lesson
    normalized["smart_note_id"] = note_id
    normalized["evidence"] = _evidence_for_learning(event)
    normalized["evidence_state"] = _evidence_state_for_learning(event)
    normalized["provenance"] = provenance
    normalized["canonical_event_id"] = event_id
    normalized["verification"] = verification
    return normalized


def event_date(event: dict[str, Any]) -> str:
    value = str(event.get("timestamp") or event.get("effective_at") or event.get("created_at") or "")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return "UNKNOWN"


def has_collective_consent(event: dict[str, Any]) -> bool:
    return event.get("collective_consent") is True or event.get("visibility") == "COLLECTIVE_CONSENT"


def build_candidate(event: dict[str, Any]) -> dict[str, Any] | None:
    if str(event.get("event_id", "")).startswith("SE-"):
        event = canonical_to_learning_input(event)
    if not str(event.get("lesson", "")).strip():
        return None
    outcome = {
        "intent": event.get("intent", event.get("what_happened", "")),
        "action": event.get("action", ""),
        "expected_outcome": event.get("expected_outcome", ""),
        "actual_outcome": event.get("actual_outcome", ""),
        "lesson": event.get("lesson", ""),
        "root_cause": event.get("root_cause", ""),
        "recommendation": event.get("recommendation", event.get("next_action", "")),
        "evidence": event.get("evidence", []),
        "evidence_state": event.get("evidence_state", "UNKNOWN"),
        "learning_state": event.get("learning_state", "PROPOSED"),
        "smart_note_id": event.get("smart_note_id", event["event_id"]),
        "smart_link": event.get("smart_link", f"intelligence-event:{event['event_id']}"),
        "preflight": event.get("preflight", event.get("successor_instruction", "")),
    }
    learning = al.build_learning_event(event, outcome)
    learning["collective_consent"] = has_collective_consent(event)
    learning["visibility"] = "COLLECTIVE" if learning["collective_consent"] else "PRIVATE"
    learning["source_event_path"] = event.get("_path", "")
    learning["canonical_event_id"] = event.get("canonical_event_id", event.get("event_id", ""))
    learning["provenance"] = event.get("provenance", {})
    learning["verification"] = event.get("verification", {})
    return learning


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")


def upsert_learning(learning: dict[str, Any]) -> Path:
    path = LEARNING_DIR / f"{learning['learning_event_id']}.json"
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if al.evidence_rank(existing.get("evidence_state", "UNKNOWN")) > al.evidence_rank(learning.get("evidence_state", "UNKNOWN")):
                learning["evidence_state"] = existing["evidence_state"]
            if existing.get("learning_state") == "OPERATIONAL":
                learning["learning_state"] = "OPERATIONAL"
            if existing.get("created_at"):
                learning["created_at"] = existing["created_at"]
        except json.JSONDecodeError:
            pass
    write_json(path, learning)
    return path


def daily_synthesis(events: list[dict[str, Any]], learnings: list[dict[str, Any]], day: str, generated_at: str | None = None) -> dict[str, Any]:
    day_learnings = [x for x in learnings if event_date(x) == day]
    verified = [x for x in day_learnings if al.evidence_rank(x.get("evidence_state", "UNKNOWN")) >= VERIFIED_RANK]
    collective = [x for x in verified if x.get("collective_consent") is True]
    private = [x for x in verified if x.get("collective_consent") is not True]
    lessons = [{
        "learning_event_id": item["learning_event_id"],
        "source_event_id": item["source_event_id"],
        "lesson": item["lesson"],
        "evidence_state": item["evidence_state"],
        "smart_note_id": item.get("smart_note_id", ""),
        "smart_link": item.get("smart_link", ""),
        "visibility": item.get("visibility", "PRIVATE"),
    } for item in verified]
    return {
        "report_id": f"DAILY-LEARNING-{day}",
        "date": day,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "title": "What We Learned Today",
        "counts": {
            "intelligence_events": len([e for e in events if event_date(e) == day]),
            "learning_candidates": len(day_learnings),
            "verified_lessons": len(verified),
            "collective_lessons": len(collective),
            "private_lessons": len(private),
        },
        "lessons": lessons,
        "collective_lessons": [x for x in lessons if x["visibility"] == "COLLECTIVE"],
        "private_lessons_count": len(private),
        "privacy_rule": "PRIVATE BY DEFAULT; SHARED BY CHOICE; COLLECTIVE BY CONSENT; PUBLIC BY DECISION",
        "lineage": "CANONICAL SE EVENT → SMART NOTE → INTELLIGENT BLOCK → LEARNING EVENT → EVIDENCE → DAILY LEARNING",
    }


def write_collective_projection(report: dict[str, Any], day: str) -> str:
    lines = [
        f"# 🧠 What We Learned Today — {day}",
        "",
        f"**Verified collective lessons:** {report['counts']['collective_lessons']}",
        "",
        "> Collective wisdom is published only when the source event explicitly grants collective consent and the learning has verified evidence.",
        "",
    ]
    for item in report["collective_lessons"]:
        lines += [
            f"## {item['lesson']}",
            "",
            f"- Learning Event: `{item['learning_event_id']}`",
            f"- Smart Note: `{item['smart_note_id']}`",
            f"- Smart Link: `{item['smart_link']}`",
            f"- Evidence: `{item['evidence_state']}`",
            "",
        ]
    COLLECTIVE_DIR.mkdir(parents=True, exist_ok=True)
    path = COLLECTIVE_DIR / f"{day}.md"
    text = "\n".join(lines) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return str(path.relative_to(ROOT))


def write_feed_projection(report: dict[str, Any], day: str) -> str:
    """Project the public-safe daily learning into the existing feed namespace."""
    FEED_DIR.mkdir(parents=True, exist_ok=True)
    path = FEED_DIR / f"WHAT-WE-LEARNED-{day}.json"
    projection = {
        "feed_item_id": report["report_id"],
        "feed_type": "DAILY_COLLECTIVE_LEARNING",
        "date": day,
        "title": report["title"],
        "counts": report["counts"],
        "items": report["collective_lessons"],
        "lineage": report["lineage"],
        "privacy_rule": report["privacy_rule"],
    }
    write_json(path, projection)
    return str(path.relative_to(ROOT))


def run(day: str | None = None) -> dict[str, Any]:
    events = load_events()
    learnings: list[dict[str, Any]] = []
    for event in events:
        candidate = build_candidate(event)
        if candidate is None:
            continue
        upsert_learning(candidate)
        learnings.append(candidate)

    target_day = day or datetime.now(timezone.utc).date().isoformat()
    daily_path = DAILY_DIR / f"{target_day}.json"
    prior_generated_at = None
    if daily_path.exists():
        try:
            prior_generated_at = json.loads(daily_path.read_text(encoding="utf-8")).get("generated_at")
        except json.JSONDecodeError:
            pass
    report = daily_synthesis(events, learnings, target_day, prior_generated_at)
    write_json(daily_path, report)
    report["collective_projection_path"] = write_collective_projection(report, target_day)
    report["feed_projection_path"] = write_feed_projection(report, target_day)
    return report


if __name__ == "__main__":
    result = run(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(result, indent=2))
