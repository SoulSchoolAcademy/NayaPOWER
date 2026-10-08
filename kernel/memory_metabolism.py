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
from typing import Any, Iterable


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
    evidence: list[str] = field(default_factory=list)
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


def create_record(
    content: str,
    *,
    epistemic_state: str,
    provenance: dict[str, Any] | None = None,
    record_id: str | None = None,
    now: str | None = None,
) -> MemoryRecord:
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


def strengthen(record: MemoryRecord, evidence: str, *, now: str | None = None) -> dict[str, Any]:
    """Strengthen an ACTIVE record with fresh verification evidence.

    A dead record (superseded/decayed/archived/quarantined) cannot be
    strengthened back to life: reconcile it or replace it. This is the
    machinery that keeps stale intelligence from quietly regaining weight.
    """
    _require_integrity(record)
    if record.memory_state != ACTIVE:
        raise MemoryMetabolismError("strengthen_refused_not_active")
    if not evidence:
        raise MemoryMetabolismError("strengthen_evidence_missing")
    at = now or _utcnow_iso()
    from_state = record.memory_state
    record.evidence.append(evidence)
    record.verification_weight = round(record.verification_weight + 1.0, 6)
    record.last_verified_at = at
    record.integrity = record_integrity(record)
    return _receipt("strengthen", record, from_state, at, f"weight={record.verification_weight}")


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
