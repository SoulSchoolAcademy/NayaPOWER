"""D51 canonical receipt envelope.

Every action that matters emits a receipt: actor, action, evidence,
timestamp, scope. The envelope unifies the domain-specific receipts
(CanaryReceipt, LivenessReceipt, ...) at the ledger boundary - it does
not replace them.

Hard rules (fail-closed at construction):
  * actor, action: non-empty strings.
  * evidence: non-empty - a receipt with no evidence is a claim, not a receipt.
  * timestamp: ISO-8601.
  * scope: one of self | team | collective | public.

`to_ledger_params(owner_id)` maps the envelope onto the exact arguments of
the database writer `nayanet_record_ledger_event()`. It builds the call; it
never executes it - database writes stay behind the human-only gate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from datetime import datetime, timezone

SCOPES = ("self", "team", "collective", "public")

# D51 scope -> nayanet_smart_ledger privacy_classification.
SCOPE_TO_PRIVACY = {
    "self": "PRIVATE",
    "team": "SHARED",
    "collective": "COLLECTIVE",
    "public": "PUBLIC",
}

# Source table stamped on every living-ledger emission.
SOURCE_TABLE = "living_ledger"


def _parse_timestamp(value: str) -> datetime:
    """Parse ISO-8601; refuse anything else. Naive input is assumed UTC."""
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    text = value.strip()
    candidate = text[:-1] + "+00:00" if text.endswith(("Z", "z")) else text
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        raise ValueError("timestamp must be ISO-8601, got %r" % (value,))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _canonical_envelope(actor: str, action: str, evidence: tuple,
                        timestamp: str, scope: str) -> str:
    """Deterministic encoding feeding receipt_id."""
    payload = {
        "actor": actor,
        "action": action,
        "evidence": list(evidence),
        "timestamp": timestamp,
        "scope": scope,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class LivingReceipt:
    """One D51 receipt: who did what, with what proof, when, for whom.

    Frozen: a receipt is history the moment it exists. Construction
    refuses (ValueError) on any envelope violation - there is no
    "draft receipt".
    """
    actor: str
    action: str
    evidence: tuple = field(default_factory=tuple)
    timestamp: str = ""
    scope: str = "self"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.actor, str) or not self.actor.strip():
            raise ValueError("actor must be a non-empty string")
        if not isinstance(self.action, str) or not self.action.strip():
            raise ValueError("action must be a non-empty string")
        ev = self.evidence
        if isinstance(ev, list):
            object.__setattr__(self, "evidence", tuple(ev))
            ev = self.evidence
        if not isinstance(ev, tuple) or not ev:
            raise ValueError("evidence must be a non-empty tuple/list")
        for item in ev:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("every evidence item must be a non-empty string")
        if not isinstance(self.timestamp, str) or not self.timestamp.strip():
            raise ValueError("timestamp must be a non-empty ISO-8601 string")
        _parse_timestamp(self.timestamp)  # raises on malformed input
        if self.scope not in SCOPES:
            raise ValueError("scope must be one of %s, got %r"
                             % ("/".join(SCOPES), self.scope))
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dict")

    @property
    def receipt_id(self) -> str:
        """Deterministic id: sha256 over the canonical envelope encoding."""
        canonical = _canonical_envelope(
            self.actor.strip(), self.action.strip(), self.evidence,
            self.timestamp.strip(), self.scope,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @property
    def privacy_classification(self) -> str:
        return SCOPE_TO_PRIVACY[self.scope]

    def to_ledger_params(self, owner_id: str) -> dict:
        """Exact arguments for `nayanet_record_ledger_event()`.

        Builds the stored-procedure call; never executes it.
        """
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("owner_id must be a non-empty string")
        meta = dict(self.metadata)
        meta["actor"] = self.actor.strip()
        meta["scope"] = self.scope
        return {
            "p_owner_id": owner_id.strip(),
            "p_event_type": self.action.strip(),
            "p_source_table": SOURCE_TABLE,
            "p_source_id": self.receipt_id,
            "p_event_at": self.timestamp.strip(),
            "p_privacy_classification": self.privacy_classification,
            "p_status": "RECORDED",
            "p_evidence_refs": list(self.evidence),
            "p_metadata": meta,
        }

    def to_json(self) -> str:
        return json.dumps(
            {
                "receipt_id": self.receipt_id,
                "actor": self.actor,
                "action": self.action,
                "evidence": list(self.evidence),
                "timestamp": self.timestamp,
                "scope": self.scope,
                "metadata": self.metadata,
            },
            sort_keys=True,
            indent=1,
        )
