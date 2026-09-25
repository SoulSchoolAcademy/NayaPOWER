#!/usr/bin/env python3
"""Machine-testable enforcement for the canonical Smart Note / Intelligent Block operation.

This is a thin admission boundary beside Smart Notes v3. It does not replace
the canonical event architecture or rewrite historical events. New Smart Note
claims can be admitted only when the canonical IB identity, canonical human
perspectives, evidence chain, lineage, and governance gate are present.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GOVERNANCE = Path(__file__).resolve().parents[1] / "governance"
if str(GOVERNANCE) not in sys.path:
    sys.path.insert(0, str(GOVERNANCE))
from governance_kernel import Authority, DecisionObject, Epistemic, Risk, VerificationPlan, evaluate  # noqa: E402

SMART_NOTE_REQUEST_RE = re.compile(
    r"(?:\bsmart[- ]note\s+(?:this|it|that)\b|\bnaya\s+note\s+this\b|\bnote\s+this\b|\bmake\s+(?:a\s+)?note\b|\bnote\s+it\b|\block\s+(?:this|it)\s+in\b)",
    re.IGNORECASE,
)
EVENT_RE = re.compile(r"^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)

REQUIRED_REPRESENTATIONS = ("human", "child", "grandma", "naya", "machine")
REQUIRED_RECEIPT_LINKS = ("canonical_event_url", "index_url", "feed_url")


class SmartNoteEnforcementError(ValueError):
    """Raised when a Smart Note claim is incomplete or unverifiable."""


def detect_smart_note_request(text: str) -> bool:
    """Return True only when the input explicitly requests Smart Note capture."""
    return bool(SMART_NOTE_REQUEST_RE.search(text or ""))


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set)):
        return bool(value) and all(_nonempty(v) for v in value)
    if isinstance(value, dict):
        return bool(value)
    return True


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SmartNoteEnforcementError(f"unparseable JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SmartNoteEnforcementError(f"JSON object required: {path}")
    return value


def _event_path(root: Path, event_id: str, effective_at: str) -> Path:
    if not EVENT_RE.match(event_id):
        raise SmartNoteEnforcementError("invalid canonical event_id")
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):", effective_at or "")
    if not match:
        raise SmartNoteEnforcementError("effective_at must be ISO timestamp with YYYY-MM-DDTHH")
    y, m, d, h = match.groups()
    return root / ".naya" / "memory" / "events" / y / m / d / h / f"{event_id}.json"


def _validate_governance_gate(operation: dict[str, Any]) -> list[str]:
    governance = operation.get("governance")
    if not isinstance(governance, dict):
        return ["canonical governance decision/authority is missing"]
    decision = governance.get("decision")
    authority = governance.get("authority")
    if not isinstance(decision, dict) or not isinstance(authority, dict):
        return ["canonical governance decision/authority is incomplete"]
    try:
        permissions = frozenset(str(x) for x in authority.get("permissions", []) if str(x).strip())
        scopes = authority.get("scope", [])
        scope = str(scopes[0] if isinstance(scopes, list) and scopes else scopes or "").strip()
        risk = decision.get("risk") if isinstance(decision.get("risk"), dict) else {}
        verification = decision.get("verification_plan", [])
        if isinstance(verification, str):
            verification = [verification]
        stop_conditions = decision.get("stop_conditions", [])
        if isinstance(stop_conditions, str):
            stop_conditions = [stop_conditions]
        auth = Authority(
            authority_id=str(authority.get("authority_id", "")),
            principal_id=str(authority.get("holder") or authority.get("actor") or ""),
            purpose=str(authority.get("purpose", "")),
            scope=scope,
            granted_actions=permissions,
            expires_at=authority.get("expires_at"),
            revoked=bool(authority.get("revoked_at")),
        )
        dec = DecisionObject(
            decision_id=str(decision.get("decision_id", "SMART-NOTE")),
            mission=str(decision.get("mission", "smart-note-capture")),
            actor_id=str(decision.get("actor") or authority.get("holder") or ""),
            action=str(decision.get("action") or decision.get("required_permission") or "smart_note_capture"),
            purpose=str(decision.get("purpose", "smart-note-capture")),
            scope=scope,
            current_truth=str(decision.get("current_truth", "canonical Smart Note capture requested")),
            gap=str(decision.get("gap") or "canonical Smart Note capture must cross the canonical receiver"),
            evidence=tuple(str(x) for x in decision.get("evidence", []) if str(x).strip()),
            epistemic=frozenset({Epistemic.OBSERVED}),
            consequence=str(decision.get("consequence", "smart-note mutation")),
            reversible=bool(decision.get("reversible", True)),
            risk=Risk(
                uncertainty=int(risk.get("uncertainty", decision.get("uncertainty", 1))),
                consequence=int(risk.get("consequence", 1)),
                irreversibility=int(risk.get("irreversibility", decision.get("reversibility", 1))),
            ),
            alternatives=tuple(str(x) for x in decision.get("alternatives", []) if str(x).strip()),
            expected_value=str((decision.get("value") or {}).get("responsible", True)),
            required_permission=str(decision.get("required_permission", "")),
            verification=VerificationPlan(
                observation=str(verification[0] if verification else "read back canonical intelligence"),
                success_criteria=str(verification[1] if len(verification) > 1 else "canonical IB/event lineage verified"),
                stop_conditions=tuple(str(x) for x in stop_conditions if str(x).strip()),
            ),
            necessary_power=permissions,
            requested_power=permissions,
        )
        result = evaluate(dec, auth, now=datetime.now(timezone.utc).isoformat())
        if not result.allowed:
            return [f"canonical governance gate rejected Smart Note mutation: {reason}" for reason in result.reasons]
    except Exception as exc:
        return [f"canonical governance gate rejected Smart Note mutation: {exc}"]
    return []


def validate_smart_note_operation(
    operation: dict[str, Any],
    *,
    root: Path | str,
    repo: str = "SoulSchoolAcademy/NayaPOWER",
) -> list[str]:
    """Return all enforcement failures; an empty list means GREEN."""
    root = Path(root)
    errors: list[str] = []

    errors.extend(_validate_governance_gate(operation))

    if not operation.get("request_detected"):
        errors.append("Smart Note request was not detected")

    event_id = str(operation.get("event_id", ""))
    intelligent_block = operation.get("intelligent_block")
    if not isinstance(intelligent_block, dict):
        errors.append("canonical Intelligent Block identity is missing")
        intelligent_block = {}
    ib_id = str(intelligent_block.get("intelligent_block_id", ""))
    if not re.fullmatch(r"IB-[0-9]{6}", ib_id):
        errors.append("invalid intelligent_block.intelligent_block_id")
    source_event_ids = intelligent_block.get("source_event_ids", [])
    if isinstance(source_event_ids, str):
        source_event_ids = [source_event_ids]
    if event_id and event_id not in source_event_ids:
        errors.append("Intelligent Block provenance does not preserve the canonical event lineage")
    if not EVENT_RE.match(event_id):
        errors.append("invalid operation.event_id")

    event = operation.get("event")
    if not isinstance(event, dict):
        errors.append("canonical Note Event payload is missing")
        event = {}

    if event.get("event_id") != event_id:
        errors.append("event_id is not bound to the canonical Note Event")

    reps = event.get("representations")
    if not isinstance(reps, dict):
        errors.append("Shawn/Naya/Machine representations are missing")
        reps = {}
    for name in REQUIRED_REPRESENTATIONS:
        rep = reps.get(name)
        if not isinstance(rep, dict) or not _nonempty(rep.get("id")) or not _nonempty(rep.get("content", rep.get("summary"))):
            errors.append(f"missing or empty {name} representation")
            continue
        if rep.get("canonical_event_id") != event_id:
            errors.append(f"{name} representation is not bound to canonical event")
        if not _nonempty(rep.get("smart_link")):
            errors.append(f"{name} representation missing Smart Link")
    rep_ids = [reps[n].get("id") for n in REQUIRED_REPRESENTATIONS if isinstance(reps.get(n), dict)]
    if len(rep_ids) == len(REQUIRED_REPRESENTATIONS) and len(set(rep_ids)) != len(rep_ids):
        errors.append("canonical representation IDs must be distinct")

    effective_at = str(event.get("effective_at", ""))
    event_path = None
    if EVENT_RE.match(event_id) and effective_at:
        try:
            event_path = _event_path(root, event_id, effective_at)
            if not event_path.is_file():
                errors.append("canonical Note Event is not persisted at the required path")
            else:
                persisted = _load_json(event_path)
                if persisted.get("event_id") != event_id:
                    errors.append("persisted Note Event does not match claimed event_id")
                if persisted.get("effective_at") != effective_at:
                    errors.append("persisted Note Event does not match claimed effective_at")
                if persisted.get("representations") != event.get("representations"):
                    errors.append("persisted Note Event representations do not match the claimed operation")
        except SmartNoteEnforcementError as exc:
            errors.append(str(exc))
    else:
        errors.append("canonical event persistence path cannot be derived")

    index_path = root / ".naya" / "memory" / "events" / "INDEX.json"
    if not index_path.is_file():
        errors.append("canonical event INDEX.json is missing")
    else:
        try:
            index = _load_json(index_path)
            rows = index.get("events", [])
            match = next((row for row in rows if isinstance(row, dict) and row.get("event_id") == event_id), None)
            if match is None:
                errors.append("canonical event is not registered in events/INDEX.json")
            elif event_path is not None:
                expected = str(event_path.relative_to(root / ".naya" / "memory" / "events"))
                if Path(str(match.get("path", ""))).as_posix() != Path(expected).as_posix():
                    errors.append("INDEX registration path does not match canonical event path")
        except SmartNoteEnforcementError as exc:
            errors.append(str(exc))

    feed_path = root / ".naya" / "INTELLIGENT-FEED.md"
    if not feed_path.is_file():
        errors.append("Intelligent Feed is missing")
    elif event_id not in feed_path.read_text(encoding="utf-8"):
        errors.append("canonical event is not linked from the Intelligent Feed")

    receipt = operation.get("receipt")
    if not isinstance(receipt, dict):
        errors.append("receipt is missing")
        receipt = {}
    if str(receipt.get("status", "")).upper() != "VERIFIED":
        errors.append("receipt.status must be VERIFIED")
    commits = receipt.get("commit_shas", [])
    if isinstance(receipt.get("commit_sha"), str):
        commits = list(commits) + [receipt["commit_sha"]]
    if not commits or not all(isinstance(c, str) and COMMIT_RE.match(c) for c in commits):
        errors.append("receipt must contain at least one valid 40-character commit SHA")
    for link in REQUIRED_RECEIPT_LINKS:
        if not _nonempty(receipt.get(link)):
            errors.append(f"receipt missing {link}")
    if receipt.get("repository") != repo:
        errors.append("receipt.repository does not identify the canonical repository")
    if receipt.get("branch") != "main":
        errors.append("receipt.branch must be main")

    pis = operation.get("pis_propagation")
    if pis is not None:
        if not isinstance(pis, dict):
            errors.append("pis_propagation must be an object when supplied")
        elif str(pis.get("status", "")).upper() == "VERIFIED":
            if not _nonempty(pis.get("evidence")) or not _nonempty(pis.get("receipt")):
                errors.append("PIS propagation marked VERIFIED without separate PIS evidence and receipt")
    if operation.get("pis_propagated") is True and not (
        isinstance(pis, dict) and str(pis.get("status", "")).upper() == "VERIFIED"
        and _nonempty(pis.get("evidence")) and _nonempty(pis.get("receipt"))
    ):
        errors.append("PIS propagation claim is invalid without separately verified PIS evidence")

    return errors


def enforce_smart_note_claim(operation: dict[str, Any], *, root: Path | str, repo: str = "SoulSchoolAcademy/NayaPOWER") -> dict[str, Any]:
    """Reject an incomplete Smart Note claim or return a verified admission receipt."""
    errors = validate_smart_note_operation(operation, root=root, repo=repo)
    if errors:
        raise SmartNoteEnforcementError("Smart Note claim rejected: " + " | ".join(errors))
    return {
        "status": "VERIFIED",
        "operation": "SMART_NOTE",
        "intelligent_block_id": operation["intelligent_block"]["intelligent_block_id"],
        "event_id": operation["event_id"],
        "pis_propagation": "SEPARATE_EVIDENCE_REQUIRED",
        "receipt": operation["receipt"],
    }
