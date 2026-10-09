"""NayaPOWER SELF node V2: deterministic identity and continuity mechanics."""
from __future__ import annotations
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

class SelfNodeError(ValueError):
    """Raised when SELF cannot establish or restore valid state."""


# Truth states eligible for preservation into SELF continuity. Anything below
# VERIFIED — CANDIDATE, DRAFT, FALSIFIED, or an unresolvable note — cannot
# enter `state.known` through the governed path (Phase 4 / GAP 5).
GOVERNED_TRUTH_STATES = frozenset({"VERIFIED", "RATIFIED", "ACTIVE", "LEARNED"})

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
    # Governed lesson references: one entry per accepted Smart Note,
    # {smart_note_id, truth_state, recorded_at}. Raw text never lands here.
    lesson_refs: list = field(default_factory=list)
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
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            # Unparseable store = corrupt record: isolate, never silently absorb.
            raise SelfNodeError("checkpoint_integrity_failed") from exc
        if not isinstance(payload, dict):
            raise SelfNodeError("checkpoint_integrity_failed")
        stored = payload.get("checkpoint_id")
        # checkpoint_id() is a content hash over the payload excluding the id
        # itself, so the stored id must equal the recomputed hash. Any
        # tampering with mission, known, unknown, blocked, experience count,
        # or the id breaks the match -> fail closed, inherit nothing.
        if stored is None or checkpoint_id(payload) != stored:
            raise SelfNodeError("checkpoint_integrity_failed")
        return _state_from_payload(payload)

def _canonical_payload(state: SelfState) -> dict[str, Any]:
    payload = asdict(state)
    if state.identity is not None:
        payload["identity"] = asdict(state.identity)
    return payload

def checkpoint_id(payload: dict[str, Any]) -> str:
    # Content hash over everything EXCEPT the checkpoint id itself, so a
    # stored id is verifiable: stored_id == checkpoint_id(stored_payload).
    # Hashing the id into its own pre-image would make the stored value
    # unverifiable (the pre-image could never be reconstructed on load).
    content = {k: v for k, v in payload.items() if k != "checkpoint_id"}
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
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
            lesson_refs=list(prior.lesson_refs) if prior is not None else [],
            predecessor_id=prior.identity.actor_id if prior else None,
            checkpoint_id=prior.checkpoint_id if prior else None,
            successor_ready=False,
            experience_count=prior.experience_count if prior else 0,
        )
        self.state.checkpoint_id = checkpoint_id(_canonical_payload(self.state))
        self.store.save(self.state)
        receipt = self.boot_receipt()
        # Observability for the integrity gate: reaching this line means a
        # stored prior (if any) passed checkpoint verification in load().
        receipt["prior_checkpoint_integrity"] = "VERIFIED" if prior is not None else "ABSENT"
        return receipt

    def record_experience(
        self,
        *,
        lesson: str | None = None,
        smart_note_id: str | None = None,
        observed_outcome: str | None = None,
        next_objective: str | None = None,
    ) -> dict[str, Any]:
        """Preserve an experience into SELF continuity (GAP 5 hardened).

        Governed path (preferred): pass ``smart_note_id``. The note's
        ``truth_state`` is read from the Smart Note registry and must be at or
        above VERIFIED (VERIFIED / RATIFIED / ACTIVE / LEARNED). A lower state —
        or a missing/unresolvable note — is REFUSED without touching state.

        Legacy path: pass raw ``lesson`` text. Kept for backward compatibility
        but stored as ``"unverified:<lesson>"`` and returned as
        PRESERVED_UNVERIFIED with a warning, so the unverified path stays
        visible and can never masquerade as governed truth.

        When both are given, the governed Smart Note reference wins.
        ``observed_outcome`` remains required.
        """
        self._require_ready()
        if not observed_outcome:
            raise SelfNodeError("experience_incomplete")
        has_note = bool(smart_note_id)
        has_lesson = bool(lesson)
        if not has_note and not has_lesson:
            raise SelfNodeError("experience_incomplete")
        if has_note:
            return self._record_governed_experience(smart_note_id, observed_outcome, next_objective)
        self._persist_experience(f"unverified:{lesson}", next_objective)
        return {
            "status": "PRESERVED_UNVERIFIED",
            "lesson": lesson,
            "warning": "unverified_lesson_not_governed",
            "observed_outcome": observed_outcome,
            "checkpoint_id": self.state.checkpoint_id,
            "experience_count": self.state.experience_count,
        }

    def _record_governed_experience(
        self, smart_note_id: str, observed_outcome: str, next_objective: str | None
    ) -> dict[str, Any]:
        # Lazy import: tools.smart_note_v2 must never pull kernel at import time.
        from tools.smart_note_v2 import REGISTRY, load_json

        try:
            registry = load_json(REGISTRY)
            entries = registry.get("entries", []) if isinstance(registry, dict) else []
            entry = next(
                (
                    e
                    for e in entries
                    if isinstance(e, dict) and e.get("smart_note_id") == smart_note_id
                ),
                None,
            )
        except Exception:
            # Registry missing or unreadable: fail closed, exactly like an
            # unresolvable note.
            entry = None
        if entry is None:
            return {
                "status": "REFUSED",
                "reason": "note_not_found",
                "smart_note_id": smart_note_id,
                "truth_state": None,
            }
        truth_state = entry.get("truth_state")
        if truth_state not in GOVERNED_TRUTH_STATES:
            return {
                "status": "REFUSED",
                "reason": "truth_state_below_VERIFIED",
                "smart_note_id": smart_note_id,
                "truth_state": truth_state,
            }
        ref = f"sn:{smart_note_id}"
        if ref not in self.state.known:
            self.state.known.append(ref)
        self.state.lesson_refs.append(
            {
                "smart_note_id": smart_note_id,
                "truth_state": truth_state,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._persist_experience(None, next_objective)
        return {
            "status": "PRESERVED",
            "smart_note_id": smart_note_id,
            "truth_state": truth_state,
            "observed_outcome": observed_outcome,
            "checkpoint_id": self.state.checkpoint_id,
            "experience_count": self.state.experience_count,
        }

    def _persist_experience(self, lesson: str | None, next_objective: str | None) -> None:
        """Shared persistence tail for preserved experiences (governed or raw)."""
        if lesson is not None and lesson not in self.state.known:
            self.state.known.append(lesson)
        if next_objective:
            self.state.objective = next_objective
        self.state.experience_count += 1
        self.state.successor_ready = True
        self.state.checkpoint_id = checkpoint_id(_canonical_payload(self.state))
        self.store.save(self.state)

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
        lesson_refs=list(payload.get("lesson_refs", [])),
        predecessor_id=payload.get("predecessor_id"),
        checkpoint_id=payload.get("checkpoint_id"),
        successor_ready=bool(payload.get("successor_ready", False)),
        experience_count=int(payload.get("experience_count", 0)),
    )
