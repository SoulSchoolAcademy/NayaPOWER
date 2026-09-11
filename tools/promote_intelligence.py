#!/usr/bin/env python3
"""NayaPOWER Promotion Engine v1.

Turns canonical Intelligence Events into durable, auditable intelligence.
The engine is deliberately deterministic and dependency-free so CI can run it
without installing a third-party package.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "MASTER-NOTES/INTELLIGENCE-EVENTS"
RECEIPT_DIR = ROOT / "MASTER-NOTES/INTELLIGENCE-PROMOTIONS"
NAYA_DIR = ROOT / "MASTER-NOTES/NAYA-NOTES"
SHAWN_DIR = ROOT / "MASTER-NOTES/SHAWN-NOTES"
FEED_DIR = ROOT / "MASTER-NOTES/INTELLIGENCE-FEED"
HUB_PATH = ROOT / "MASTER-NOTES/PRIMARY-INTELLIGENCE-HUB.md"
SCHEMA_PATH = ROOT / ".naya/intelligence/intelligence-event.schema.json"

REQUIRED = {"event_id", "timestamp", "project", "lesson", "source", "evidence_state", "promotion_status"}
EVIDENCE_STATES = {"UNKNOWN", "IMPLEMENTED", "TESTED", "VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"}
PROMOTION_STATES = {"NOT_REQUIRED", "PROPOSED", "WRITTEN", "TESTED", "VERIFIED", "CANONICAL", "BLOCKED", "FAILED", "UNKNOWN"}
HOMES = {"LAW", "GUARDRAIL", "MACHINE_CONTRACT", "TEST", "PROCEDURE", "MISSION_STATE", "ARCHITECTURE", "SPECIFICATION", "NAYA_NOTE", "HUMAN_SMART_NOTE"}
AUTO_HOMES = {"NAYA_NOTE", "HUMAN_SMART_NOTE", "PROCEDURE", "ARCHITECTURE", "SPECIFICATION"}
AUTHORITY_HOMES = {"LAW", "GUARDRAIL", "MACHINE_CONTRACT", "TEST", "MISSION_STATE"}
STOPWORDS = {"the", "and", "that", "this", "with", "from", "into", "must", "should", "when", "then", "than", "for", "are", "was", "were", "not", "only", "every", "next", "naya", "system"}


def normalize(text: str) -> str:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return " ".join(t for t in tokens if t not in STOPWORDS and len(t) > 2)


def fingerprint(event: dict[str, Any]) -> str:
    basis = "|".join(normalize(str(event.get(k, ""))) for k in ("project", "lesson", "root_cause", "recommendation"))
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def similarity(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def load_events() -> list[tuple[Path, dict[str, Any]]]:
    events = []
    for path in sorted(EVENT_DIR.glob("*.json")):
        try:
            events.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    return events


def validate_event(event: dict[str, Any], path: Path) -> list[str]:
    errors = []
    missing = sorted(REQUIRED - set(event))
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")
        return errors
    if len(str(event["event_id"])) < 8:
        errors.append(f"{path}: event_id must be at least 8 characters")
    if not str(event["project"]).strip() or not str(event["lesson"]).strip():
        errors.append(f"{path}: project and lesson must be non-empty")
    if not isinstance(event["source"], list):
        errors.append(f"{path}: source must be an array")
    if event["evidence_state"] not in EVIDENCE_STATES:
        errors.append(f"{path}: invalid evidence_state={event['evidence_state']}")
    if event["promotion_status"] not in PROMOTION_STATES:
        errors.append(f"{path}: invalid promotion_status={event['promotion_status']}")
    for home in event.get("candidate_homes", []):
        if home not in HOMES:
            errors.append(f"{path}: invalid candidate home={home}")
    try:
        datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: timestamp is not ISO-8601 date-time")
    return errors


def classify(event: dict[str, Any]) -> tuple[list[str], str]:
    explicit = [x for x in event.get("candidate_homes", []) if x in HOMES]
    if explicit:
        homes = list(dict.fromkeys(explicit))
    else:
        text = " ".join(str(event.get(k, "")) for k in ("lesson", "what_happened", "root_cause", "recommendation")).lower()
        homes = []
        if any(x in text for x in ("law", "constitutional", "governance", "universal")):
            homes.append("LAW")
        if any(x in text for x in ("repeat", "regression", "prevent", "guardrail")):
            homes.append("GUARDRAIL")
        if any(x in text for x in ("test", "assert", "machine contract", "automate")):
            homes.append("TEST")
        if not homes:
            homes.append("NAYA_NOTE")
    restricted = any(h in AUTHORITY_HOMES for h in homes)
    return homes, ("PROMOTION_PROPOSAL_REQUIRES_AUTHORITY" if restricted else "AUTO_PROMOTE_APPROVED_DESTINATIONS")


def display_path(path: Path) -> str:
    """Return a stable path for repository writes and isolated test fixtures."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_note(event: dict[str, Any], target: Path, heading: str) -> str:
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{event['event_id']}.md"
    content = f"""# 🔱 {heading}

**Event:** {event['event_id']}
**Timestamp:** {event['timestamp']}
**Project:** {event['project']}
**Promotion fingerprint:** `{fingerprint(event)}`

## WHAT HAPPENED
{event.get('what_happened', '')}

## WHAT WE LEARNED
{event['lesson']}

## VALUE
{event.get('value', '')}

## WHAT CHANGED
{event.get('actual_outcome', '')}

## EVIDENCE STATE
`{event['evidence_state']}`

## EVIDENCE
""" + "\n".join(f"- `{x}`" for x in event.get("evidence", [])) + f"""

## NEXT ACTION
{event.get('next_action', '')}

## SUCCESSOR / HUMAN GUIDANCE
{event.get('successor_instruction', '')}

## PROVENANCE
Source event: `{event['event_id']}`
Source: {', '.join(event.get('source', []))}
"""
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
    return display_path(path)


def load_prior_event_index(events: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    by_id = {e["event_id"]: e for _, e in events}
    normalized = {eid: normalize(str(e.get("lesson", ""))) for eid, e in by_id.items()}
    return {"by_id": by_id, "normalized": normalized}


def find_duplicate(event: dict[str, Any], index: dict[str, Any]) -> tuple[str | None, float]:
    exact = fingerprint(event)
    for eid, prior in index["by_id"].items():
        if eid == event["event_id"]:
            continue
        if fingerprint(prior) == exact:
            return eid, 1.0
    current = normalize(str(event.get("lesson", "")))
    best_id, best_score = None, 0.0
    for eid, lesson in index["normalized"].items():
        if eid == event["event_id"]:
            continue
        score = similarity(current, lesson)
        if score > best_score:
            best_id, best_score = eid, score
    return (best_id, best_score) if best_score >= 0.82 else (None, best_score)


def write_feed_entry(event: dict[str, Any], homes: list[str], decision: str, duplicate_of: str | None, status: str) -> str:
    FEED_DIR.mkdir(parents=True, exist_ok=True)
    path = FEED_DIR / f"{event['event_id']}.md"
    duplicate = f"`{duplicate_of}`" if duplicate_of else "None"
    content = f"""# 🔱 Intelligence Feed — {event.get('title', event['event_id'])}

**Event:** `{event['event_id']}`  
**Timestamp:** {event['timestamp']}  
**Project:** {event['project']}  
**Promotion:** `{status}`  
**Decision:** `{decision}`  
**Durable homes:** {', '.join(f'`{h}`' for h in homes)}  
**Duplicate / related prior event:** {duplicate}

## LESSON
{event['lesson']}

## VALUE / IMPACT
{event.get('value', '')}

## SOURCE
""" + "\n".join(f"- `{x}`" for x in event.get("source", [])) + f"""

## EVIDENCE STATE
`{event['evidence_state']}`

## SUCCESSOR INSTRUCTION
{event.get('successor_instruction', '')}

## PROMOTION
This entry is append-oriented intelligence. It does not override canonical governance or verified project truth.
"""
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
    return display_path(path)


def update_hub(summary: list[dict[str, Any]]) -> None:
    if not HUB_PATH.exists():
        return
    marker_start = "<!-- PROMOTION-ENGINE-V1:START -->"
    marker_end = "<!-- PROMOTION-ENGINE-V1:END -->"
    existing = HUB_PATH.read_text(encoding="utf-8")
    block = [marker_start, "", "## 🔱 PROMOTION ENGINE V1 — CURRENT OPERATIONAL STATE", "", "The Promotion Engine processes canonical Intelligence Events into durable, verified intelligence. This managed section is generated from the current event corpus; it does not replace the Hub's canonical synthesis.", ""]
    for item in summary[-10:]:
        block.append(f"- `{item['event_id']}` — **{item['status']}** — homes: {', '.join(item['homes'])}; duplicate: {item['duplicate_of'] or 'none'}; verification: `{item['evidence_state']}`")
    block += ["", "**Current invariant:** `EVENT → DEDUP → CLASSIFY → PROMOTE → VERIFY → HUB → SUCCESSOR`", "", marker_end]
    new_block = "\n".join(block)
    if marker_start in existing and marker_end in existing:
        prefix = existing.split(marker_start, 1)[0]
        suffix = existing.split(marker_end, 1)[1]
        updated = prefix + new_block + suffix
    else:
        updated = existing.rstrip() + "\n\n" + new_block + "\n"
    if updated != existing:
        HUB_PATH.write_text(updated, encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    events = load_events()
    for path, event in events:
        errors.extend(validate_event(event, path))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    index = load_prior_event_index(events)
    receipts: list[dict[str, Any]] = []
    for path, event in events:
        homes, decision = classify(event)
        duplicate_of, similarity_score = find_duplicate(event, index)
        promoted = list(event.get("promoted_artifacts", []))
        auto_homes = [h for h in homes if h in AUTO_HOMES]
        restricted_homes = [h for h in homes if h in AUTHORITY_HOMES]

        if "NAYA_NOTE" in auto_homes:
            promoted.append(write_note(event, NAYA_DIR, "NAYA NOTE / AI INTELLIGENCE"))
        if "HUMAN_SMART_NOTE" in auto_homes:
            promoted.append(write_note(event, SHAWN_DIR, "SHAWN NOTE / HUMAN RECEIPT"))

        if duplicate_of:
            status = "DUPLICATE_REVIEW"
        elif restricted_homes:
            status = "PROMOTION_PROPOSAL_REQUIRES_AUTHORITY"
        elif auto_homes:
            status = "PROMOTED_WRITTEN"
        else:
            status = "CLASSIFIED_ONLY"

        feed_path = write_feed_entry(event, homes, decision, duplicate_of, status)
        promoted.append(feed_path)
        receipts.append({
            "event_id": event["event_id"],
            "source_event": display_path(path),
            "fingerprint": fingerprint(event),
            "candidate_homes": homes,
            "auto_promotable_homes": auto_homes,
            "authority_gated_homes": restricted_homes,
            "decision": decision,
            "duplicate_of": duplicate_of,
            "duplicate_similarity": round(similarity_score, 4),
            "evidence_state": event["evidence_state"],
            "source_promotion_status": event["promotion_status"],
            "promotion_status": status,
            "promoted_artifacts": list(dict.fromkeys(promoted)),
            "verification_required": bool(auto_homes or restricted_homes),
            "verified": False,
            "rule": "NO_FILE_WRITE_ALONE_COUNTS_AS_VERIFICATION",
        })

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    receipt = {
        "engine": "Promotion Engine v1",
        "generated_at": now,
        "event_count": len(receipts),
        "receipts": receipts,
        "verification_summary": {
            "implemented": True,
            "tested": False,
            "verified": False,
            "runtime_proven": False,
            "production_proven": False,
            "note": "CI test/verification stage must close these states; the promoter never self-certifies verification from file writes.",
        },
    }
    (RECEIPT_DIR / "LATEST-PROMOTION-RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    update_hub(receipts)
    print(f"Promotion Engine v1 processed {len(receipts)} event(s); receipt and feed/hub state written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
