#!/usr/bin/env python3
"""NayaPOWER Adaptive Learning Engine v1.

Persistent application-level learning layer over canonical Intelligence Events.
It does not change model weights. It converts verified outcomes into durable
lessons, proposes/promotes operational rules, and runs preflight checks so
known mistakes can influence future actions.

Dependency-free and deterministic so CI can execute it without third-party
packages. The canonical event/evidence store remains the source of truth.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEARNING_DIR = ROOT / "MASTER-NOTES/ADAPTIVE-LEARNING"
EVENT_DIR = ROOT / "MASTER-NOTES/INTELLIGENCE-EVENTS"
RULE_DIR = LEARNING_DIR / "RULES"
PREFLIGHT_DIR = LEARNING_DIR / "PREFLIGHT"
RECEIPT_DIR = LEARNING_DIR / "RECEIPTS"

LEARNING_STATES = {"OBSERVED", "PROPOSED", "CONFIRMED", "OPERATIONAL", "SUPERSEDED"}
EVIDENCE_STATES = {"UNKNOWN", "IMPLEMENTED", "TESTED", "VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"}
PROMOTION_STATES = {"NOT_REQUIRED", "PROPOSED", "WRITTEN", "TESTED", "VERIFIED", "CANONICAL", "BLOCKED", "FAILED", "UNKNOWN"}
STOPWORDS = {"the", "and", "that", "this", "with", "from", "into", "must", "should", "when", "then", "than", "for", "are", "was", "were", "not", "only", "every", "next", "naya", "system"}


def normalize(text: str) -> str:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return " ".join(t for t in tokens if t not in STOPWORDS and len(t) > 2)


def fingerprint(*parts: str) -> str:
    basis = "|".join(normalize(p) for p in parts)
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def evidence_rank(state: str) -> int:
    return {
        "UNKNOWN": 0,
        "IMPLEMENTED": 1,
        "TESTED": 2,
        "VERIFIED": 3,
        "RUNTIME-PROVEN": 4,
        "PRODUCTION-PROVEN": 5,
    }.get(state, 0)


def validate_learning_event(event: dict[str, Any]) -> list[str]:
    required = {"learning_event_id", "timestamp", "source_event_id", "lesson", "evidence_state", "learning_state"}
    errors = []
    missing = sorted(required - set(event))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if event.get("learning_state") not in LEARNING_STATES:
        errors.append("learning_state must be one of OBSERVED, PROPOSED, CONFIRMED, OPERATIONAL, SUPERSEDED")
    if event.get("evidence_state") not in EVIDENCE_STATES:
        errors.append("invalid evidence_state")
    try:
        datetime.fromisoformat(str(event.get("timestamp", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("timestamp is not ISO-8601")
    return errors


def build_learning_event(intelligence_event: dict[str, Any], outcome: dict[str, Any]) -> dict[str, Any]:
    """Convert an observed outcome into a durable Learning Event candidate."""
    event_id = str(intelligence_event["event_id"])
    lesson = str(outcome.get("lesson") or intelligence_event.get("lesson") or "").strip()
    root_cause = str(outcome.get("root_cause") or intelligence_event.get("root_cause") or "").strip()
    recommendation = str(outcome.get("recommendation") or intelligence_event.get("recommendation") or "").strip()
    evidence_state = str(outcome.get("evidence_state") or intelligence_event.get("evidence_state") or "UNKNOWN")
    requested_state = str(outcome.get("learning_state") or "PROPOSED")
    # Never allow caller input to bypass the evidence boundary.
    learning_state = requested_state if requested_state in LEARNING_STATES else "PROPOSED"
    if learning_state == "OPERATIONAL" and evidence_rank(evidence_state) < evidence_rank("VERIFIED"):
        learning_state = "CONFIRMED"
    learning_id = f"LRN-{fingerprint(event_id, lesson, root_cause, recommendation)}"
    return {
        "learning_event_id": learning_id,
        "timestamp": outcome.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "source_event_id": event_id,
        "project": intelligence_event.get("project", ""),
        "intent": outcome.get("intent", intelligence_event.get("what_happened", "")),
        "action": outcome.get("action", ""),
        "expected_outcome": outcome.get("expected_outcome", ""),
        "actual_outcome": outcome.get("actual_outcome", intelligence_event.get("actual_outcome", "")),
        "lesson": lesson,
        "root_cause": root_cause,
        "recommendation": recommendation,
        "evidence": list(dict.fromkeys(outcome.get("evidence", intelligence_event.get("evidence", [])))),
        "evidence_state": evidence_state,
        "learning_state": learning_state,
        "source": list(dict.fromkeys(intelligence_event.get("source", []))),
        "smart_note_id": outcome.get("smart_note_id", event_id),
        "smart_link": outcome.get("smart_link", ""),
        "preflight": outcome.get("preflight", ""),
        "verification_required": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def save_learning_event(event: dict[str, Any]) -> Path:
    errors = validate_learning_event(event)
    if errors:
        raise ValueError("Invalid Learning Event: " + "; ".join(errors))
    LEARNING_DIR.mkdir(parents=True, exist_ok=True)
    path = LEARNING_DIR / f"{event['learning_event_id']}.json"
    path.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
    return path


def propose_rule(event: dict[str, Any]) -> dict[str, Any]:
    """Create a rule proposal. Promotion to OPERATIONAL is evidence-gated."""
    rule_id = f"RULE-{fingerprint(event['learning_event_id'], event['lesson'], event.get('recommendation', ''))}"
    return {
        "rule_id": rule_id,
        "learning_event_id": event["learning_event_id"],
        "source_event_id": event["source_event_id"],
        "project": event.get("project", ""),
        "lesson": event["lesson"],
        "rule": event.get("recommendation") or event["lesson"],
        "preflight": event.get("preflight") or f"Check for prior lesson: {event['lesson']}",
        "evidence": event.get("evidence", []),
        "evidence_state": event["evidence_state"],
        "state": "OPERATIONAL" if evidence_rank(event["evidence_state"]) >= evidence_rank("VERIFIED") else "PROPOSED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": None,
    }


def save_rule(rule: dict[str, Any]) -> Path:
    RULE_DIR.mkdir(parents=True, exist_ok=True)
    path = RULE_DIR / f"{rule['rule_id']}.json"
    path.write_text(json.dumps(rule, indent=2) + "\n", encoding="utf-8")
    return path


def load_operational_rules() -> list[dict[str, Any]]:
    if not RULE_DIR.exists():
        return []
    rules = []
    for path in sorted(RULE_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("state") == "OPERATIONAL":
            rules.append(data)
    return rules


def preflight(context: str, rules: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Retrieve applicable operational lessons before a consequential action."""
    rules = rules if rules is not None else load_operational_rules()
    normalized_context = normalize(context)
    matches = []
    for rule in rules:
        lesson_text = normalize(str(rule.get("lesson", "")))
        rule_text = normalize(str(rule.get("rule", "")))
        lesson_tokens = set(lesson_text.split())
        context_tokens = set(normalized_context.split())
        rule_tokens = set(rule_text.split())
        overlap = max(
            len(lesson_tokens & context_tokens) / len(lesson_tokens | context_tokens) if lesson_tokens and context_tokens else 0.0,
            len(rule_tokens & context_tokens) / len(rule_tokens | context_tokens) if rule_tokens and context_tokens else 0.0,
        )
        if overlap >= 0.18:
            matches.append({
                "rule_id": rule["rule_id"],
                "lesson": rule["lesson"],
                "rule": rule["rule"],
                "preflight": rule["preflight"],
                "match_score": round(overlap, 4),
            })
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "context": context,
        "matched_rules": matches,
        "blocked": False,
        "required_checks": [m["preflight"] for m in matches],
    }
    PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    report_id = f"PREFLIGHT-{fingerprint(context, result['checked_at'])}"
    result["preflight_id"] = report_id
    (PREFLIGHT_DIR / f"{report_id}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def record_outcome(learning_event: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    """Close the learning loop without self-certifying verification."""
    verified = bool(verification.get("independent_observation")) and bool(verification.get("evidence")) and bool(verification.get("verified"))
    result = {
        "learning_event_id": learning_event["learning_event_id"],
        "verified": verified,
        "independent_observation": verification.get("independent_observation", ""),
        "evidence": verification.get("evidence", []),
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "next_state": "OPERATIONAL" if verified else learning_event["learning_state"],
        "rule_promotion_allowed": verified,
    }
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    (RECEIPT_DIR / f"{learning_event['learning_event_id']}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print("Adaptive Learning Engine v1 — library/protocol module. Use the canonical event pipeline to invoke it.")
