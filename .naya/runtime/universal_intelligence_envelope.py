#!/usr/bin/env python3
"""Universal Intelligence Envelope V1: sender normalization before the existing receiver."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SCHEMA = "NAYANET_UNIVERSAL_INTELLIGENCE_ENVELOPE_V1"
MEANINGFULNESS = {"MEANINGFUL", "NOT_MEANINGFUL"}
EPISTEMIC = {"UNKNOWN", "OBSERVED", "VERIFIED"}


@dataclass(frozen=True)
class UniversalIntelligenceEnvelope:
    envelope_id: str
    source: Mapping[str, Any]
    identity: Mapping[str, Any]
    owner_scope: Mapping[str, Any]
    occurred_at: str
    received_at: str
    output: Mapping[str, Any]
    meaningfulness: str
    provenance: Mapping[str, Any]
    epistemic: Mapping[str, Any]
    privacy: Mapping[str, Any]
    authority: Mapping[str, Any]
    context: Mapping[str, Any]
    idempotency_key: str

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "UniversalIntelligenceEnvelope":
        required = (
            "envelope_id", "source", "identity", "owner_scope", "occurred_at",
            "received_at", "output", "meaningfulness", "provenance", "epistemic",
            "privacy", "authority", "context", "idempotency_key",
        )
        missing = [key for key in required if raw.get(key) in (None, "", {}, [])]
        if raw.get("schema") != SCHEMA:
            missing.append("schema")
        if missing:
            raise ValueError("invalid universal intelligence envelope: " + ", ".join(missing))
        if raw["meaningfulness"] not in MEANINGFULNESS:
            raise ValueError("invalid meaningfulness")
        epistemic = raw["epistemic"]
        if not isinstance(epistemic, Mapping) or epistemic.get("status") not in EPISTEMIC:
            raise ValueError("invalid epistemic status")
        privacy = raw["privacy"]
        if not isinstance(privacy, Mapping) or privacy.get("visibility", "PRIVATE") != "PRIVATE":
            raise ValueError("universal envelope requires PRIVATE default visibility")
        provenance = raw["provenance"]
        if not isinstance(provenance, Mapping):
            raise ValueError("provenance must be an object")
        if not any(provenance.get(key) for key in ("source_ref", "source_event_id", "source_path", "source_id")):
            raise ValueError("provenance requires a source identity")
        authority = raw["authority"]
        if not isinstance(authority, Mapping):
            raise ValueError("authority must be an object")
        # Authority is descriptive context here. It cannot grant permission.
        return cls(
            envelope_id=str(raw["envelope_id"]),
            source=raw["source"],
            identity=raw["identity"],
            owner_scope=raw["owner_scope"],
            occurred_at=str(raw["occurred_at"]),
            received_at=str(raw["received_at"]),
            output=raw["output"],
            meaningfulness=str(raw["meaningfulness"]),
            provenance=provenance,
            epistemic=epistemic,
            privacy=privacy,
            authority=authority,
            context=raw["context"],
            idempotency_key=str(raw["idempotency_key"]),
        )

    def receiver_payload(self) -> dict[str, Any]:
        """Return a receiver-neutral payload; persistence remains the existing receiver's job."""
        return {
            "schema": SCHEMA,
            "envelope_id": self.envelope_id,
            "source": dict(self.source),
            "identity": dict(self.identity),
            "owner_scope": dict(self.owner_scope),
            "occurred_at": self.occurred_at,
            "received_at": self.received_at,
            "output": dict(self.output),
            "meaningfulness": self.meaningfulness,
            "provenance": dict(self.provenance),
            "epistemic": dict(self.epistemic),
            "privacy": dict(self.privacy),
            "authority": dict(self.authority),
            "context": dict(self.context),
            "idempotency_key": self.idempotency_key,
        }
