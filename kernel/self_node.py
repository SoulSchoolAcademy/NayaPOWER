"""NayaPOWER SELF node V2: deterministic identity and continuity mechanics."""
from __future__ import annotations
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

class SelfNodeError(ValueError):
    """Raised when SELF cannot establish or restore valid state."""

@dataclass(frozen=True)
class RuntimeIdentity:
    actor_id: str
    system_id: str
    role: str

@dataclass
class SelfState:
    node_id: str = "NAYA-KERNEL-SELF"
    state: str = "UNINITIALIZED"
    identity: RuntimeIdentity | None = None
    mission: str = ""
    objective: str = ""
    scope: str = ""
    known: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    predecessor_id: str | None = None
    checkpoint_id: str | None = None
    successor_ready: bool = False
    experience_count: int = 0

class JsonContinuityStore:
    """Minimal deterministic persistence boundary; replaceable by governed durable storage."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, state: SelfState) -> str:
        payload = _canonical_payload(state)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return checkpoint_id(payload)

    def load(self) -> SelfState:
        if not self.path.exists():
            raise SelfNodeError("continuity_missing")
        return _state_from_payload(json.loads(self.path.read_text(encoding="utf-8")))

def _canonical_payload(state: SelfState) -> dict[str, Any]:
    payload = asdict(state)
    if state.identity is not None:
        payload["identity"] = asdict(state.identity)
    return payload

def checkpoint_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "CHK-" + hashlib.sha256(encoded).hexdigest()[:24]

class SelfNode:
    """SELF is continuity, not authority and not a claim of consciousness."""

    def __init__(self, store: JsonContinuityStore):
        self.store = store
        self.state = SelfState()

    def cold_boot(
        self,
        runtime_identity: RuntimeIdentity,
        mission: str,
        objective: str,
        scope: str,
        *,
        predecessor_id: str | None = None,
        known: list[str] | None = None,
        unknown: list[str] | None = None,
        blocked: list[str] | None = None,
    ) -> dict[str, Any]:
        if not runtime_identity.actor_id or not runtime_identity.system_id:
            raise SelfNodeError("identity_missing")
        if not mission:
            raise SelfNodeError("mission_missing")
        if not objective:
            raise SelfNodeError("objective_missing")

        prior = self.store.load() if self.store.path.exists() else None
        if prior is not None:
            if prior.identity is None:
                raise SelfNodeError("stored_identity_missing")
            if prior.identity.system_id != runtime_identity.system_id:
                raise SelfNodeError("system_identity_mismatch")
            if predecessor_id is not None and prior.identity.actor_id != predecessor_id:
                raise SelfNodeError("predecessor_identity_mismatch")

        self.state = SelfState(
            state="READY",
            identity=runtime_identity,
            mission=mission if prior is None else prior.mission,
            objective=objective if prior is None else prior.objective,
            scope=scope if prior is None else prior.scope,
            known=list(known if known is not None else ([] if prior is None else prior.known)),
            unknown=list(unknown if unknown is not None else ([] if prior is None else prior.unknown)),
            blocked=list(blocked if blocked is not None else ([] if prior is None else prior.blocked)),
            predecessor_id=prior.identity.actor_id if prior else None,
            checkpoint_id=prior.checkpoint_id if prior else None,
            successor_ready=False,
            experience_count=prior.experience_count if prior else 0,
        )
        self.state.checkpoint_id = checkpoint_id(_canonical_payload(self.state))
        self.store.save(self.state)
        return self.boot_receipt()

    def record_experience(self, *, lesson: str, observed_outcome: str, next_objective: str | None = None) -> dict[str, Any]:
        self._require_ready()
        if not lesson or not observed_outcome:
            raise SelfNodeError("experience_incomplete")
        if lesson not in self.state.known:
            self.state.known.append(lesson)
        if next_objective:
            self.state.objective = next_objective
        self.state.experience_count += 1
        self.state.successor_ready = True
        self.state.checkpoint_id = checkpoint_id(_canonical_payload(self.state))
        self.store.save(self.state)
        return {
            "status": "PRESERVED",
            "lesson": lesson,
            "observed_outcome": observed_outcome,
            "checkpoint_id": self.state.checkpoint_id,
            "experience_count": self.state.experience_count,
        }

    def successor_packet(self) -> dict[str, Any]:
        self._require_ready()
        if not self.state.successor_ready:
            raise SelfNodeError("successor_not_ready")
        return {
            "schema": "naya.self.successor.v2",
            "source_node_id": self.state.node_id,
            "predecessor_id": self.state.identity.actor_id if self.state.identity else None,
            "system_id": self.state.identity.system_id if self.state.identity else None,
            "mission": self.state.mission,
            "objective": self.state.objective,
            "scope": self.state.scope,
            "known": list(self.state.known),
            "unknown": list(self.state.unknown),
            "blocked": list(self.state.blocked),
            "checkpoint_id": self.state.checkpoint_id,
            "experience_count": self.state.experience_count,
        }

    def boot_successor(self, runtime_identity: RuntimeIdentity, packet: dict[str, Any]) -> dict[str, Any]:
        if packet.get("schema") != "naya.self.successor.v2":
            raise SelfNodeError("invalid_successor_packet")
        if packet.get("system_id") != runtime_identity.system_id:
            raise SelfNodeError("system_identity_mismatch")
        if not packet.get("predecessor_id"):
            raise SelfNodeError("successor_predecessor_missing")
        receipt = self.cold_boot(
            runtime_identity,
            packet["mission"],
            packet["objective"],
            packet["scope"],
            predecessor_id=packet["predecessor_id"],
            known=packet.get("known", []),
            unknown=packet.get("unknown", []),
            blocked=packet.get("blocked", []),
        )
        self.state.successor_ready = True
        self.store.save(self.state)
        receipt["inherited_checkpoint_id"] = packet.get("checkpoint_id")
        receipt["inherited_experience_count"] = packet.get("experience_count", 0)
        return receipt

    def boot_receipt(self) -> dict[str, Any]:
        self._require_ready()
        return {
            "schema": "naya.self.boot-receipt.v2",
            "node_id": self.state.node_id,
            "state": self.state.state,
            "actor_id": self.state.identity.actor_id if self.state.identity else None,
            "system_id": self.state.identity.system_id if self.state.identity else None,
            "mission": self.state.mission,
            "objective": self.state.objective,
            "checkpoint_id": self.state.checkpoint_id,
            "known_count": len(self.state.known),
            "unknown_count": len(self.state.unknown),
            "successor_ready": self.state.successor_ready,
        }

    def _require_ready(self) -> None:
        if self.state.state != "READY" or self.state.identity is None:
            raise SelfNodeError("self_not_ready")

def _state_from_payload(payload: dict[str, Any]) -> SelfState:
    identity = payload.get("identity")
    return SelfState(
        node_id=payload.get("node_id", "NAYA-KERNEL-SELF"),
        state=payload.get("state", "UNINITIALIZED"),
        identity=RuntimeIdentity(**identity) if identity else None,
        mission=payload.get("mission", ""),
        objective=payload.get("objective", ""),
        scope=payload.get("scope", ""),
        known=list(payload.get("known", [])),
        unknown=list(payload.get("unknown", [])),
        blocked=list(payload.get("blocked", [])),
        predecessor_id=payload.get("predecessor_id"),
        checkpoint_id=payload.get("checkpoint_id"),
        successor_ready=bool(payload.get("successor_ready", False)),
        experience_count=int(payload.get("experience_count", 0)),
    )
