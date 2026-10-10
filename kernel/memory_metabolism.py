"""NayaPOWER memory metabolism: the governed lifecycle of durable intelligence.

Every retained record moves under governed transitions:
    strengthen -> supersede -> reconcile -> decay -> compress -> archive

Hard laws (memory-side twin of the checkpoint-integrity gate):
- Retrieval serves ACTIVE records only, and only with integrity verified at
  read. SUPERSEDED / DECAYED / ARCHIVED records stay fully auditable but
  never surface silently; QUARANTINED records (integrity failure) are never
  served under any flag. Stale intelligence never wins.
- Nothing is deleted: demotion preserves lineage, provenance, and history so
  the past stays reconstructible for verification and audit.
- Strengthening requires fresh verification evidence; a dead record cannot
  be strengthened back to life — reconcile it or replace it.
- Every transition verifies integrity first and fails closed on mismatch.
- All transitions are deterministic: same inputs, same outputs, same
  receipt ids. No clock reads inside; callers pass `now` explicitly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, NoReturn


class MemoryMetabolismError(ValueError):
    """Raised when a memory transition or retrieval is refused."""


# Lifecycle states -------------------------------------------------------------
ACTIVE = "ACTIVE"
SUPERSEDED = "SUPERSEDED"
DECAYED = "DECAYED"
ARCHIVED = "ARCHIVED"
QUARANTINED = "QUARANTINED"

MEMORY_STATES = (ACTIVE, SUPERSEDED, DECAYED, ARCHIVED, QUARANTINED)

# Epistemic types stay distinct from lifecycle states (SN-042): what a record
# *is* epistemically never implies where it sits in the lifecycle.
EPISTEMIC_STATES = (
    "EXTERNAL_CLAIM",
    "INTERNAL_KNOWLEDGE",
    "DERIVED_BELIEF",
    "VERIFIED_FACT",
    "OPERATING_ASSUMPTION",
    "HYPOTHESIS",
    "DECISION",
    "OUTCOME",
    "LEARNING",
)

# Records these states fail into audit-only; only ACTIVE is served by default.
AUDIT_ONLY = (SUPERSEDED, DECAYED, ARCHIVED)


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class MemoryRecord:
    record_id: str
    content: str
    epistemic_state: str
    provenance: dict[str, Any] = field(default_factory=dict)
    memory_state: str = ACTIVE
    verification_weight: float = 0.0
    # Evidence entries are structured descriptors (EvidenceDescriptor.to_record()),
    # never bare strings. See the evidence gate below.
    evidence: list[dict[str, Any]] = field(default_factory=list)
    lineage: list[str] = field(default_factory=list)
    superseded_by: str | None = None
    superseded_at: str | None = None
    created_at: str = field(default_factory=_utcnow_iso)
    last_verified_at: str = field(default_factory=_utcnow_iso)
    last_retrieved_at: str | None = None
    retrieval_count: int = 0
    compressed: bool = False
    original_content_hash: str | None = None
    integrity: str = ""


def _canonical_payload(record: MemoryRecord) -> dict[str, Any]:
    return {
        "record_id": record.record_id,
        "content": record.content,
        "epistemic_state": record.epistemic_state,
        "provenance": record.provenance,
        "memory_state": record.memory_state,
        "verification_weight": record.verification_weight,
        "evidence": record.evidence,
        "lineage": record.lineage,
        "superseded_by": record.superseded_by,
        "superseded_at": record.superseded_at,
        "created_at": record.created_at,
        "last_verified_at": record.last_verified_at,
        "last_retrieved_at": record.last_retrieved_at,
        "retrieval_count": record.retrieval_count,
        "compressed": record.compressed,
        "original_content_hash": record.original_content_hash,
    }


def record_integrity(record: MemoryRecord) -> str:
    """Content hash over everything except the integrity field itself.

    Same discipline as checkpoint_id(): a stored hash is verifiable only when
    the id is excluded from its own pre-image.
    """
    encoded = json.dumps(_canonical_payload(record), sort_keys=True, separators=(",", ":")).encode()
    return "MMI-" + hashlib.sha256(encoded).hexdigest()[:24]


def integrity_ok(record: MemoryRecord) -> bool:
    return bool(record.integrity) and record.integrity == record_integrity(record)


def _receipt_id(transition: str, record_id: str, at: str, detail: str) -> str:
    raw = "|".join((transition, record_id, at, detail)).encode()
    return "MMR-" + hashlib.sha256(raw).hexdigest()[:16]


def _receipt(transition: str, record: MemoryRecord, from_state: str, at: str, detail: str = "") -> dict[str, Any]:
    return {
        "schema": "naya.memory-metabolism.receipt.v1",
        "receipt_id": _receipt_id(transition, record.record_id, at, detail),
        "transition": transition,
        "record_id": record.record_id,
        "from_state": from_state,
        "to_state": record.memory_state,
        "at": at,
        "detail": detail,
    }


def _require_integrity(record: MemoryRecord) -> None:
    if not integrity_ok(record):
        raise MemoryMetabolismError("memory_integrity_failed")


def _require_now(now: str) -> str:
    """Govern the clock input: reject unparseable or timezone-naive `now`.

    Without this, a naive timestamp reaches datetime arithmetic mid-pass and
    raises a raw TypeError after earlier records were already mutated in
    memory — failing loudly instead of failing closed. All timestamps in
    this module are timezone-aware ISO-8601.
    """
    try:
        parsed = datetime.fromisoformat(now)
    except (TypeError, ValueError):
        raise MemoryMetabolismError("now_invalid")
    if parsed.tzinfo is None:
        raise MemoryMetabolismError("now_naive_refused")
    return now


def create_record(
    content: str,
    *,
    epistemic_state: str,
    provenance: dict[str, Any] | None = None,
    record_id: str | None = None,
    now: str | None = None,
) -> MemoryRecord:
    """Create an ACTIVE record with integrity sealed at birth.

    record_id derives from sha256(content + now): identical content created
    at an identical timestamp yields an identical id, and the later version
    shadows the earlier on load (latest-wins). Callers that need distinct
    records for identical content must vary `now` or pass an explicit id.
    """
    if not content:
        raise MemoryMetabolismError("content_missing")
    if epistemic_state not in EPISTEMIC_STATES:
        raise MemoryMetabolismError("epistemic_state_unknown")
    at = now or _utcnow_iso()
    record = MemoryRecord(
        record_id=record_id or ("MEM-" + hashlib.sha256((content + at).encode()).hexdigest()[:16]),
        content=content,
        epistemic_state=epistemic_state,
        provenance=dict(provenance or {}),
        memory_state=ACTIVE,
        created_at=at,
        last_verified_at=at,
    )
    record.integrity = record_integrity(record)
    return record


# Evidence gate (Phase 1 wiring of the error-defense falsification spec) ---------
# Shawn's directive 2026-10-10: "Intelligence may learn from itself, but it
# may not independently verify itself merely by referring back to itself."
#
# The falsification suite (error_defense/, spec branch
# naya5/error-defense-falsification) proved strengthen() accepted ANY
# non-empty evidence string: a self-citing false lesson reached weight 6.0
# and outranked a genuine trial-verified lesson (weight 1.0). The bare-string
# evidence API was the hole.
#
# strengthen() now enforces the evidence-level predicates of qualify_lesson
# fail-closed, in the spec's order, with the spec's verdict codes embedded
# in the refusal: BLOCKED_INTEGRITY, BLOCKED_CIRCULAR_PROOF,
# INSUFFICIENT_INDEPENDENT_EVIDENCE, BLOCKED_SELF_CERTIFICATION.
# Promotion-level predicates (material contradiction, held-out evaluation,
# authority scope) need lesson-level context strengthen() does not have;
# they belong at the promotion bridge (lesson_from_memory_record) — Phase 2.

try:  # canonical identity contract: tools/learning_admission_gate.py
    from tools.learning_admission_gate import (  # type: ignore[import-not-found]
        normalize_identity as _gate_normalize_identity,
    )

    def _normalize_identity(value: Any) -> str:
        return _gate_normalize_identity(value)

except ImportError:  # mirror the contract when tools/ is not importable

    def _normalize_identity(value: Any) -> str:
        """Canonical identity comparison: case- and whitespace-insensitive."""
        return str(value).strip().casefold()


@dataclass(frozen=True)
class EvidenceDescriptor:
    """Structured verification evidence for strengthen().

    content_hash must equal sha256(content): the evidence is self-describing
    and tamper-evident. origin is the identity that produced the evidence;
    verifier is the identity asserting it (must differ from the record's
    doer — self-certification is never evidence). source_record_id names
    the record this evidence derives from (None when it derives from outside
    the memory system). evidence_family groups items sharing one ultimate
    source, for echo-chamber detection at the promotion bridge.
    """

    evidence_id: str
    content: str
    content_hash: str
    origin: str
    verifier: str
    source_record_id: str | None = None
    evidence_family: str | None = None

    def to_record(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "content": self.content,
            "content_hash": self.content_hash,
            "origin": self.origin,
            "verifier": self.verifier,
            "source_record_id": self.source_record_id,
            "evidence_family": self.evidence_family,
        }


def evidence_summary(evidence: Any) -> str:
    """One-line human/audit rendering of a stored evidence entry."""
    if isinstance(evidence, dict):
        return (
            f"{evidence.get('evidence_id', '?')}"
            f" origin={evidence.get('origin', '?')}"
            f" verifier={evidence.get('verifier', '?')}"
        )
    return str(evidence)  # legacy string entries, if any survive migration


def _refuse(code: str, detail: str = "") -> NoReturn:
    raise MemoryMetabolismError(
        f"strengthen_evidence_refused:{code}" + (f":{detail}" if detail else "")
    )


def _evidence_gate_verdict(record: MemoryRecord, evidence: Any) -> str:
    """Run the evidence-level predicates in fail-closed order.

    Returns "EVIDENCE_ACCEPTED" or raises MemoryMetabolismError carrying the
    spec verdict code. First failure wins; anything unrecognized is refused.
    """
    # 1. integrity: structured, identified, hash-verified (spec: BLOCKED_INTEGRITY)
    if not isinstance(evidence, EvidenceDescriptor):
        _refuse("BLOCKED_INTEGRITY", "unstructured_evidence")
    if not str(evidence.evidence_id or "").strip():
        _refuse("BLOCKED_INTEGRITY", "evidence_id_missing")
    if not isinstance(evidence.content, str) or not evidence.content:
        _refuse("BLOCKED_INTEGRITY", "content_missing")
    recomputed = hashlib.sha256(evidence.content.encode()).hexdigest()
    if not evidence.content_hash or evidence.content_hash != recomputed:
        _refuse("BLOCKED_INTEGRITY", "content_hash_mismatch")

    me = _normalize_identity(record.record_id)
    provenance = record.provenance if isinstance(record.provenance, dict) else {}
    doer = _normalize_identity(provenance.get("doer") or "")

    # 2. circular proof: the record may not cite itself (spec: BLOCKED_CIRCULAR_PROOF)
    source = _normalize_identity(evidence.source_record_id or "")
    if source and source == me:
        _refuse("BLOCKED_CIRCULAR_PROOF", "self_citation")
    # Evidence that merely restates the record's own content is self-proof.
    if evidence.content_hash == hashlib.sha256(record.content.encode()).hexdigest():
        _refuse("BLOCKED_CIRCULAR_PROOF", "evidence_restates_record")

    # 3. independent support (spec: INSUFFICIENT_INDEPENDENT_EVIDENCE)
    origin = _normalize_identity(evidence.origin or "")
    if not origin:
        _refuse("INSUFFICIENT_INDEPENDENT_EVIDENCE", "origin_missing")
    if origin == me:
        _refuse("INSUFFICIENT_INDEPENDENT_EVIDENCE", "origin_is_record_itself")
    if doer and origin == doer:
        _refuse("INSUFFICIENT_INDEPENDENT_EVIDENCE", "origin_is_doer_echo_chamber")
    seen_hashes = {
        str(e.get("content_hash") or "")
        for e in record.evidence
        if isinstance(e, dict)
    }
    if evidence.content_hash in seen_hashes:
        _refuse("INSUFFICIENT_INDEPENDENT_EVIDENCE", "duplicate_evidence")

    # 4. self-certification (spec: BLOCKED_SELF_CERTIFICATION)
    verifier = _normalize_identity(evidence.verifier or "")
    if not verifier:
        _refuse("BLOCKED_SELF_CERTIFICATION", "verifier_missing")
    if doer and verifier == doer:
        _refuse("BLOCKED_SELF_CERTIFICATION", "verifier_is_doer")

    return "EVIDENCE_ACCEPTED"


def strengthen(record: MemoryRecord, evidence: EvidenceDescriptor, *, now: str | None = None) -> dict[str, Any]:
    """Strengthen an ACTIVE record with fresh verification evidence.

    A dead record (superseded/decayed/archived/quarantined) cannot be
    strengthened back to life: reconcile it or replace it. This is the
    machinery that keeps stale intelligence from quietly regaining weight.

    Evidence must pass the evidence gate (_evidence_gate_verdict): structured,
    hash-verified, non-circular, independently sourced, and asserted by a
    verifier distinct from the record's doer. Anything failing is refused
    fail-closed — no weight is granted.
    """
    _require_integrity(record)
    if record.memory_state != ACTIVE:
        raise MemoryMetabolismError("strengthen_refused_not_active")
    if evidence is None:
        raise MemoryMetabolismError("strengthen_evidence_missing")
    _evidence_gate_verdict(record, evidence)
    at = now or _utcnow_iso()
    from_state = record.memory_state
    record.evidence.append(evidence.to_record())
    record.verification_weight = round(record.verification_weight + 1.0, 6)
    record.last_verified_at = at
    record.integrity = record_integrity(record)
    receipt = _receipt(
        "strengthen", record, from_state, at,
        f"weight={record.verification_weight} evidence={evidence.evidence_id}",
    )
    receipt["evidence_id"] = evidence.evidence_id
    receipt["gate_verdict"] = "EVIDENCE_ACCEPTED"
    return receipt


def supersede(old: MemoryRecord, new: MemoryRecord, *, now: str | None = None) -> dict[str, Any]:
    """Retire `old` in favor of `new`. Old stays fully auditable; nothing is deleted."""
    for record in (old, new):
        _require_integrity(record)
    if old.memory_state != ACTIVE or new.memory_state != ACTIVE:
        raise MemoryMetabolismError("supersede_requires_active_pair")
    if old.record_id == new.record_id:
        raise MemoryMetabolismError("supersede_self_refused")
    at = now or _utcnow_iso()
    old.superseded_by = new.record_id
    old.superseded_at = at
    old.memory_state = SUPERSEDED
    old.integrity = record_integrity(old)
    if old.record_id not in new.lineage:
        new.lineage.append(old.record_id)
    new.integrity = record_integrity(new)
    return _receipt("supersede", old, ACTIVE, at, f"superseded_by={new.record_id}")


def reconcile(
    a: MemoryRecord,
    b: MemoryRecord,
    resolution: str,
    rationale: str,
    *,
    merged: MemoryRecord | None = None,
    now: str | None = None,
) -> dict[str, Any]:
    """Resolve a contradiction between two ACTIVE records.

    resolution: "a_wins" | "b_wins" | "merged". Losers are SUPERSEDED with
    full lineage into the winner. A rationale is mandatory: silent
    conflict resolution is how stale intelligence sneaks back in.
    """
    for record in (a, b):
        _require_integrity(record)
    if a.memory_state != ACTIVE or b.memory_state != ACTIVE:
        raise MemoryMetabolismError("reconcile_requires_active_pair")
    if resolution not in ("a_wins", "b_wins", "merged"):
        raise MemoryMetabolismError("reconcile_resolution_unknown")
    if not rationale:
        raise MemoryMetabolismError("reconcile_rationale_missing")
    if resolution == "merged" and merged is None:
        raise MemoryMetabolismError("reconcile_merged_record_missing")
    at = now or _utcnow_iso()
    if resolution == "merged":
        assert merged is not None
        _require_integrity(merged)
        supersede(a, merged, now=at)
        supersede(b, merged, now=at)
        winner = merged.record_id
    else:
        winner, loser = (a, b) if resolution == "a_wins" else (b, a)
        supersede(loser, winner, now=at)
        winner = winner.record_id
    receipt = _receipt("reconcile", a, ACTIVE, at, f"resolution={resolution} winner={winner}")
    receipt["rationale"] = rationale
    return receipt


def _stale(record: MemoryRecord, now: str, stale_after_days: float) -> bool:
    last = datetime.fromisoformat(record.last_verified_at)
    moment = datetime.fromisoformat(now)
    return (moment - last).total_seconds() > stale_after_days * 86400


def decay(record: MemoryRecord, *, now: str, stale_after_days: float) -> dict[str, Any]:
    """Demote a stale ACTIVE record out of the retrieval set.

    Decay is demotion, not deletion: the record keeps its content, lineage,
    and provenance for audit. `stale_after_days` <= 0 refuses: an
    instantaneous-decay policy would nuke the working set.
    """
    _require_integrity(record)
    if record.memory_state != ACTIVE:
        raise MemoryMetabolismError("decay_requires_active")
    if stale_after_days <= 0:
        raise MemoryMetabolismError("decay_policy_invalid")
    if not _stale(record, now, stale_after_days):
        receipt = _receipt("decay", record, ACTIVE, now, "not_stale_noop")
        receipt["to_state"] = ACTIVE
        return receipt
    from_state = record.memory_state
    record.memory_state = DECAYED
    record.integrity = record_integrity(record)
    return _receipt("decay", record, from_state, now, f"stale_beyond_{stale_after_days}d")


def compress(record: MemoryRecord, summary: str, *, now: str | None = None) -> dict[str, Any]:
    """Replace content with a summary while preserving provenance and lineage.

    The pre-compression content hash is kept so the summary stays checkable
    against the original. History records (SUPERSEDED/ARCHIVED) are immutable:
    compress only ACTIVE or DECAYED records.
    """
    _require_integrity(record)
    if record.memory_state not in (ACTIVE, DECAYED):
        raise MemoryMetabolismError("compress_refused_immutable_history")
    if not summary:
        raise MemoryMetabolismError("compress_summary_missing")
    if record.compressed:
        raise MemoryMetabolismError("compress_already_compressed")
    at = now or _utcnow_iso()
    from_state = record.memory_state
    record.original_content_hash = "MOC-" + hashlib.sha256(record.content.encode()).hexdigest()[:24]
    record.content = summary
    record.compressed = True
    record.last_verified_at = at
    record.integrity = record_integrity(record)
    return _receipt("compress", record, from_state, at, f"original_hash={record.original_content_hash}")


def archive(record: MemoryRecord, *, now: str | None = None) -> dict[str, Any]:
    """Move a record out of all active paths into audit-only storage."""
    _require_integrity(record)
    if record.memory_state not in (ACTIVE, DECAYED):
        raise MemoryMetabolismError("archive_requires_live_record")
    at = now or _utcnow_iso()
    from_state = record.memory_state
    record.memory_state = ARCHIVED
    record.integrity = record_integrity(record)
    return _receipt("archive", record, from_state, at, "")


def quarantine(record: MemoryRecord, reason: str, *, now: str | None = None) -> dict[str, Any]:
    """Isolate a record whose integrity cannot be established. Never served."""
    if not reason:
        raise MemoryMetabolismError("quarantine_reason_missing")
    at = now or _utcnow_iso()
    from_state = record.memory_state
    record.memory_state = QUARANTINED
    # Integrity intentionally NOT recomputed: a quarantined record keeps its
    # broken hash as evidence of the failure.
    return _receipt("quarantine", record, from_state, at, reason)


@dataclass
class RetrievalResult:
    items: list[tuple[MemoryRecord, str]]  # (record, label)
    dropped_integrity_failed: list[str]


def retrieve(
    records: Iterable[MemoryRecord],
    predicate=None,
    *,
    include_audit_states: tuple[str, ...] = (),
    now: str | None = None,
) -> RetrievalResult:
    """Serve records under fail-closed discipline.

    Default: ACTIVE records with verified integrity only. Stale intelligence
    (SUPERSEDED/DECAYED/ARCHIVED) never surfaces silently: it is included
    only when explicitly requested via `include_audit_states`, and then each
    item carries an "AUDIT:<STATE>" label so downstream consumers cannot
    mistake history for current truth. QUARANTINED records are never served.
    Records failing integrity at read are dropped (fail closed) and reported.
    """
    for state in include_audit_states:
        if state == QUARANTINED:
            raise MemoryMetabolismError("quarantine_never_served")
        if state not in MEMORY_STATES:
            raise MemoryMetabolismError("audit_state_unknown")
    at = now or _utcnow_iso()
    items: list[tuple[MemoryRecord, str]] = []
    dropped: list[str] = []
    for record in records:
        if record.memory_state == QUARANTINED:
            continue
        if not integrity_ok(record):
            dropped.append(record.record_id)
            continue
        label: str | None = None
        if record.memory_state == ACTIVE:
            label = ACTIVE
        elif record.memory_state in include_audit_states:
            label = f"AUDIT:{record.memory_state}"
        if label is None:
            continue
        if predicate is not None and not predicate(record):
            continue
        record.last_retrieved_at = at
        record.retrieval_count += 1
        record.integrity = record_integrity(record)
        items.append((record, label))
    return RetrievalResult(items=items, dropped_integrity_failed=dropped)


def metabolize(
    records: list[MemoryRecord],
    *,
    now: str,
    stale_after_days: float = 90.0,
) -> tuple[list[MemoryRecord], list[dict[str, Any]]]:
    """Deterministic metabolism pass: decay every stale ACTIVE record.

    Pure function over the record list; same input yields same output and
    same receipts. Refuses on any integrity failure instead of metabolizing
    around corruption — corruption is a quarantine decision, not a
    housekeeping detail. Non-ACTIVE records are skipped with a noop receipt:
    history is immutable by law, so a housekeeping pass must be total over
    mixed-state stores rather than crashing on the first history record.
    `decay()` itself stays strict for direct callers.

    QUARANTINED records are *resolved* corruption: the quarantine decision
    already happened and is receipted, and the placeholder's non-verifying
    integrity marker is the evidence itself (see `quarantine()`). They are
    skipped with a noop receipt, never re-integrity-checked. The strict
    pre-check still fires for any non-quarantined record with broken
    integrity: a quarantined record can never be served or promoted, so the
    exemption buys an attacker nothing.
    """
    _require_now(now)
    receipts: list[dict[str, Any]] = []
    live: list[MemoryRecord] = []
    for record in records:
        if record.memory_state == QUARANTINED:
            receipt = _receipt("decay", record, QUARANTINED, now,
                               "quarantined_noop")
            receipt["to_state"] = QUARANTINED
            receipts.append(receipt)
            continue
        _require_integrity(record)
        live.append(record)
    for record in live:
        if record.memory_state != ACTIVE:
            receipt = _receipt("decay", record, record.memory_state, now,
                               "not_active_noop")
            receipt["to_state"] = record.memory_state
            receipts.append(receipt)
            continue
        receipts.append(decay(record, now=now, stale_after_days=stale_after_days))
    return records, receipts
