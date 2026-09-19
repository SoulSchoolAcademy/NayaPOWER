"""Minimal deterministic Smart Ledger / CCT vertical slice V1.

CREATE SMART NOTE -> CREATE LEDGER EVENT -> VERIFY -> VALUE -> POINTS -> LEVEL -> SMART LINK
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Optional
from uuid import uuid4


_RUNTIME_DIR = Path(__file__).resolve().parent
_IDENTITY_PATH = _RUNTIME_DIR / "intelligence_identity.py"


def _load_canonical_identity():
    private_name = "naya_canonical_intelligence_identity"
    cached = sys.modules.get(private_name)
    if cached is not None:
        return cached
    if not _IDENTITY_PATH.is_file():
        raise RuntimeError("canonical intelligence identity module is missing")
    spec = importlib.util.spec_from_file_location(private_name, _IDENTITY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical intelligence identity module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[private_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(private_name, None)
        raise
    return module


IDENTITY = _load_canonical_identity()
identity_fingerprint = IDENTITY.identity_fingerprint
identity_binding_fingerprint = IDENTITY.identity_binding_fingerprint

POINTS = {
    "meaningful_like": 1, "helpful_reaction": 1, "save_useful_intelligence": 2,
    "helpful_connection_action": 2, "useful_comment": 3,
    "meaningful_smart_space_participation": 3, "high_quality_reply": 5,
    "useful_share": 5, "smart_note": 5, "smart_list": 5, "valuable_curation": 5,
    "valuable_smart_space": 10, "exceptionally_valuable_smart_note": 10,
    "verified_downstream_application": 10, "verified_positive_outcome": 25,
}

LEVELS = (
    (1, "Awakening Member", 0), (2, "Emerging Member", 50),
    (3, "Developing Member", 150), (4, "Advancing Member", 400),
    (5, "Five-Star Member", 1000), (6, "Mastering Member", 2500),
    (7, "Catalyst Member", 6000), (8, "Luminary Member", 15000),
    (9, "Visionary Member", 35000), (10, "Ten-Star Member", 75000),
)

@dataclass(frozen=True)
class SmartNote:
    note_id: str
    title: str
    content: str
    created_at: str

@dataclass(frozen=True)
class LedgerEvent:
    ledger_event_id: str
    schema_version: str
    event_type: str
    event_at: str
    created_at: str
    actor_ref: Optional[str]
    object_ref: str
    parent_event_id: Optional[str]
    evidence_ref: str
    verification_receipt_ref: Optional[str]
    integrity_hash: str
    previous_integrity_hash: Optional[str]
    privacy_class: str
    status: str
    execution_authorization_binding_hash: Optional[str] = None
    identity_id: Optional[str] = None
    identity_fingerprint: Optional[str] = None
    identity_binding_hash: Optional[str] = None

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _ledger_payload(event: LedgerEvent) -> dict:
    return {
        "ledger_event_id": event.ledger_event_id, "schema_version": event.schema_version,
        "event_type": event.event_type, "event_at": event.event_at, "created_at": event.created_at,
        "actor_ref": event.actor_ref, "object_ref": event.object_ref,
        "parent_event_id": event.parent_event_id, "evidence_ref": event.evidence_ref,
        "privacy_class": event.privacy_class, "status": "evidence_available",
        "execution_authorization_binding_hash": event.execution_authorization_binding_hash,
        "identity_id": event.identity_id,
        "identity_fingerprint": event.identity_fingerprint,
        "identity_binding_hash": event.identity_binding_hash,
    }

def _hash_event(payload: dict, previous_hash: Optional[str]) -> str:
    canonical = "|".join(f"{key}={payload[key]}" for key in sorted(payload))
    canonical += f"|previous_integrity_hash={previous_hash or ''}"
    return sha256(canonical.encode("utf-8")).hexdigest()

def create_smart_note(title: str, content: str, *, note_id: Optional[str] = None) -> SmartNote:
    if not title.strip() or not content.strip():
        raise ValueError("A Smart Note requires a non-empty title and content.")
    return SmartNote(note_id or f"note_{uuid4().hex}", title.strip(), content.strip(), utc_now())

def create_ledger_event(note: SmartNote, *, actor_ref: Optional[str] = None,
                        previous: Optional[LedgerEvent] = None,
                        execution_authorization_binding_hash: Optional[str] = None,
                        identity_id: Optional[str] = None,
                        identity_fingerprint: Optional[str] = None,
                        identity_binding_hash: Optional[str] = None) -> LedgerEvent:
    event_id = f"ledger_{uuid4().hex}"
    payload = {
        "ledger_event_id": event_id, "schema_version": "1.0", "event_type": "SMART_NOTE_CREATED",
        "event_at": note.created_at, "created_at": utc_now(), "actor_ref": actor_ref,
        "object_ref": note.note_id, "parent_event_id": previous.ledger_event_id if previous else None,
        "evidence_ref": f"note:{note.note_id}", "privacy_class": "protected" if actor_ref else "private",
        "status": "evidence_available",
        "execution_authorization_binding_hash": execution_authorization_binding_hash,
        "identity_id": identity_id,
        "identity_fingerprint": identity_fingerprint,
        "identity_binding_hash": identity_binding_hash,
    }
    return LedgerEvent(**payload, verification_receipt_ref=None,
                       integrity_hash=_hash_event(payload, previous.integrity_hash if previous else None),
                       previous_integrity_hash=previous.integrity_hash if previous else None)

def verify_event(event: LedgerEvent) -> tuple[LedgerEvent, dict]:
    if not event.evidence_ref or not event.integrity_hash:
        raise ValueError("Cannot verify a ledger event without evidence and integrity proof.")
    expected = _hash_event(_ledger_payload(event), event.previous_integrity_hash)
    if event.integrity_hash != expected:
        raise ValueError("Ledger integrity verification failed: event content does not match its hash.")
    receipt = {
        "receipt_id": f"receipt_{uuid4().hex}", "schema_version": "1.0",
        "event_id": event.ledger_event_id, "verification_state": "verified", "verified_at": utc_now(),
        "method": "evidence_reference_and_sha256_integrity_match", "evidence_ref": event.evidence_ref,
        "verifier_ref": "smart-ledger-engine-v1", "reason": "Evidence exists and the deterministic integrity hash matches.",
        "execution_authorization_binding_hash": event.execution_authorization_binding_hash,
        "identity_id": event.identity_id,
        "identity_fingerprint": event.identity_fingerprint,
        "identity_binding_hash": event.identity_binding_hash,
    }
    return LedgerEvent(**{**asdict(event), "verification_receipt_ref": receipt["receipt_id"], "status": "verified"}), receipt

def record_authorized_execution(
    gate: Any,
    authorization: Any,
    identity_envelope: Mapping[str, Any],
    *,
    action_ref: str,
    evidence_ref: str,
    outcome_ref: str,
    previous: Optional[LedgerEvent] = None,
) -> tuple[LedgerEvent, dict]:
    """Record an execution only after the exact gate authorization verifies."""
    if not action_ref.strip() or not evidence_ref.strip() or not outcome_ref.strip():
        raise ValueError("action_ref, evidence_ref, and outcome_ref are required")

    ok, reasons = gate.verify(authorization, identity_envelope, consequential=True)
    if not ok:
        raise ValueError("execution authorization verification failed: " + "; ".join(reasons))

    identity_fp = identity_fingerprint(identity_envelope)
    execution_binding = {
        "authority_id": authorization.authority_id,
        "decision_id": authorization.decision_id,
        "action_id": authorization.action_id,
        "action_type": authorization.action_type,
        "target": authorization.target,
        "actor_id": authorization.actor_id,
        "scope": authorization.scope,
        "permission": authorization.permission,
    }
    identity_bound_hash = identity_binding_fingerprint(identity_envelope, execution_binding)
    if authorization.identity_fingerprint != identity_fp:
        raise ValueError("authorization identity fingerprint does not match receipt identity")
    if authorization.identity_binding_hash != identity_bound_hash:
        raise ValueError("authorization identity binding does not match receipt identity/action")

    now = utc_now()
    event_id = f"ledger_exec_{uuid4().hex}"
    payload = {
        "ledger_event_id": event_id,
        "schema_version": "1.0",
        "event_type": "CONSEQUENTIAL_ACTION_EXECUTED",
        "event_at": now,
        "created_at": now,
        "actor_ref": str(identity_envelope["identity_id"]),
        "object_ref": authorization.target,
        "parent_event_id": previous.ledger_event_id if previous else None,
        "evidence_ref": evidence_ref,
        "privacy_class": "protected",
        "status": "evidence_available",
        "execution_authorization_binding_hash": authorization.binding_hash,
        "identity_id": str(identity_envelope["identity_id"]),
        "identity_fingerprint": identity_fp,
        "identity_binding_hash": identity_bound_hash,
    }
    event = LedgerEvent(
        **payload,
        verification_receipt_ref=None,
        integrity_hash=_hash_event(payload, previous.integrity_hash if previous else None),
        previous_integrity_hash=previous.integrity_hash if previous else None,
    )
    verified_event, receipt = verify_event(event)
    receipt.update({
        "execution_id": authorization.action_id,
        "action_ref": action_ref,
        "outcome_ref": outcome_ref,
        "authority_id": authorization.authority_id,
        "decision_id": authorization.decision_id,
        "target": authorization.target,
        "permission": authorization.permission,
    })
    return verified_event, receipt


def calculate_value(event: LedgerEvent, event_type: str = "smart_note") -> dict:
    if event.status != "verified":
        raise ValueError("Value can only be calculated from a verified ledger event.")
    points = POINTS.get(event_type)
    if points is None:
        raise ValueError(f"Unknown value event type: {event_type}")
    value_score = 5 if points <= 5 else 7 if points <= 10 else 9
    return {
        "value_event_id": f"value_{uuid4().hex}", "schema_version": "1.0",
        "ledger_event_id": event.ledger_event_id, "verification_state": "verified",
        "value_class": event_type, "value_score": value_score, "points": points,
        "calculation_version": "value-engine-v1",
        "reason": "Points are derived from the locked V1 value-event input after verification.",
    }

def determine_level(cumulative_points: int) -> dict:
    if cumulative_points < 0:
        raise ValueError("Cumulative points cannot be negative; displayed points use a zero floor.")
    selected = LEVELS[0]
    for level in LEVELS:
        if cumulative_points >= level[2]: selected = level
        else: break
    level_no, name, _ = selected
    next_level = LEVELS[level_no] if level_no < len(LEVELS) else None
    return {"level": level_no, "name": name, "points": cumulative_points,
            "next_level": next_level[1] if next_level else None,
            "points_to_next": next_level[2] - cumulative_points if next_level else 0}

def generate_smart_link(target_type: str, target_ref: str, *, access_class: str = "authorized") -> dict:
    if target_type not in {"smart_note", "ledger_event", "value_event", "collective_intelligence"}:
        raise ValueError("Unsupported Smart Link target type.")
    if access_class not in {"public", "authorized"}:
        raise ValueError("Unsupported Smart Link access class.")
    return {"smart_link_id": f"slink_{uuid4().hex}", "schema_version": "1.0",
            "target_type": target_type, "target_ref": target_ref, "access_class": access_class,
            "label": f"Open verified {target_type.replace('_', ' ')}"}

def run_vertical_slice(title: str, content: str, *, actor_ref: Optional[str] = None,
                      cumulative_points_before: int = 0) -> dict:
    note = create_smart_note(title, content)
    ledger = create_ledger_event(note, actor_ref=actor_ref)
    verified_ledger, receipt = verify_event(ledger)
    value = calculate_value(verified_ledger, "smart_note")
    total = max(0, cumulative_points_before + value["points"])
    return {"smart_note": asdict(note), "ledger_event": asdict(verified_ledger),
            "verification_receipt": receipt, "value_event": value,
            "member": determine_level(total),
            "smart_link": generate_smart_link("ledger_event", verified_ledger.ledger_event_id)}
