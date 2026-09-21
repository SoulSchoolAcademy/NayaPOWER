#!/usr/bin/env python3
"""NayaPOWER Project Identity resolver.

PI-01 only: derive project identity from the existing canonical Intelligence
Event substrate and its existing PIS/index projections. This is a rebuildable
projection, not a second project database.

Authority order:
1. canonical Intelligence Event fields (project_id, then project)
2. existing PIS event relationship/index
3. no identity inferred

The resolver deliberately returns UNKNOWN when the canonical substrate cannot
establish an identity. It never invents a project.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "MASTER-NOTES" / "INTELLIGENCE-EVENTS"
PIS_DIR = ROOT / ".naya" / "memory" / "notes"
INDEX_PATH = ROOT / ".naya" / "memory" / "INDEX.json"


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def canonical_project(event: dict[str, Any]) -> str:
    project_id = str(event.get("project_id") or "").strip()
    if project_id:
        return project_id
    project = str(event.get("project") or "").strip()
    return project


def load_events() -> list[dict[str, Any]]:
    if not EVENT_DIR.exists():
        return []
    result: list[dict[str, Any]] = []
    for path in sorted(EVENT_DIR.glob("*.json")):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        identity = canonical_project(event)
        if not identity or not event.get("event_id"):
            continue
        result.append({**event, "_path": str(path.relative_to(ROOT))})
    return result


def load_index() -> dict[str, Any]:
    if not INDEX_PATH.exists():
        return {}
    try:
        value = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def resolve(project_id: str) -> dict[str, Any]:
    requested = str(project_id or "").strip()
    if not requested:
        return {
            "status": "UNKNOWN",
            "project_id": None,
            "reason": "PROJECT_ID_REQUIRED",
            "canonical_events": [],
            "pis_notes": [],
        }

    requested_norm = normalize(requested)
    events = load_events()
    matched = [
        event for event in events
        if normalize(canonical_project(event)) == requested_norm
    ]

    index = load_index()
    event_index = index.get("event_index", {})
    pis_notes: list[str] = []
    for event in matched:
        note_id = event_index.get(event["event_id"])
        if note_id:
            pis_notes.append(str(note_id))
        elif (PIS_DIR / f"SN-{event['event_id']}.json").exists():
            pis_notes.append(f"SN-{event['event_id']}")

    if not matched:
        return {
            "status": "UNKNOWN",
            "project_id": requested,
            "reason": "NO_CANONICAL_EVENT_BOUND_TO_PROJECT",
            "canonical_events": [],
            "pis_notes": [],
        }

    unique_events = list(dict.fromkeys(str(event["event_id"]) for event in matched))
    unique_notes = list(dict.fromkeys(pis_notes))
    identities = list(dict.fromkeys(canonical_project(event) for event in matched))

    if len(identities) != 1:
        return {
            "status": "CONFLICTED",
            "project_id": requested,
            "reason": "CANONICAL_EVENTS_RESOLVE_TO_MULTIPLE_PROJECT_IDENTITIES",
            "canonical_projects": identities,
            "canonical_events": unique_events,
            "pis_notes": unique_notes,
        }

    return {
        "status": "VERIFIED",
        "project_id": identities[0],
        "canonical_events": unique_events,
        "pis_notes": unique_notes,
        "source": "MASTER-NOTES/INTELLIGENCE-EVENTS",
        "projection": "derived-from-canonical-events-and-existing-pis-index",
        "rebuildable": True,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Resolve canonical NayaPOWER project identity.")
    parser.add_argument("project_id")
    args = parser.parse_args()
    result = resolve(args.project_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
