"""Fail-closed repeat-learning gate.

This module turns the Repeat Tracker v1.1 contract into a pure, deterministic
decision function. It is intentionally independent of storage and transport:
the caller supplies the already-read ledger and evidence/authority references.

Contract:
- unresolved known repeat => LEARNING_HOLD, never DONE;
- missing/unreadable/ambiguous evidence => BLOCKED, never PASS;
- release requires later behavioral verification or an explicitly authorized
  governed exception;
- exceptions never mutate fix_status to VERIFIED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import time
from typing import Any


UNRESOLVED_STATUSES = {"PROPOSED", "BUILT", "WIRED"}
TERMINAL_STATUS = "VERIFIED"
COMPLETION_DECISIONS = {"DONE", "SIGN_OUT_COMPLETE"}
BLOCKED = "BLOCKED"
LEARNING_HOLD = "LEARNING_HOLD"
PASS = "PASS"


@dataclass(frozen=True)
class LearningReceipt:
    directive_id: str
    fix_status_before: str
    decision: str
    evidence_refs: tuple[str, ...]
    authority_ref: str
    timestamp: float
    reason: str


@dataclass
class LearningGateResult:
    passed: bool
    decision: str
    receipts: list[LearningReceipt] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    matched_ids: tuple[str, ...] = ()


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9_-]{2,}", (text or "").lower())
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "into", "before",
        "after", "must", "never", "same", "does", "not", "was", "has", "have",
        "had", "should", "when", "then", "without", "every", "work", "done",
    }
    return {w for w in words if w not in stop}


def _matches(topic: str, action: str, entry: dict[str, Any]) -> bool:
    essence = entry.get("directive_essence")
    if not isinstance(essence, str) or not essence.strip():
        return False
    query = _tokens(topic) | _tokens(action)
    if not query:
        return False
    # Prefer an explicit topic list when present; otherwise use distinctive
    # essence-token overlap. The caller must still treat >1 unresolved match
    # as ambiguous rather than guessing.
    explicit = entry.get("topics")
    if isinstance(explicit, list) and explicit:
        normalized = {_tokens(str(x)) for x in explicit}
        return any(q and q <= query for q in normalized)
    essence_tokens = _tokens(essence)
    overlap = query & essence_tokens
    return bool(overlap)


def _receipt(
    entry: dict[str, Any],
    decision: str,
    evidence_refs: tuple[str, ...],
    authority_ref: str,
    timestamp: float,
    reason: str,
) -> LearningReceipt:
    return LearningReceipt(
        directive_id=str(entry.get("id", "")),
        fix_status_before=str(entry.get("fix_status", "")),
        decision=decision,
        evidence_refs=evidence_refs,
        authority_ref=authority_ref,
        timestamp=timestamp,
        reason=reason,
    )


def evaluate_learning_gate(
    *,
    topic: str,
    action: str,
    ledger: list[dict[str, Any]] | None,
    evidence_refs: list[str] | tuple[str, ...] | None = None,
    authority_ref: str = "",
    timestamp: float | None = None,
) -> LearningGateResult:
    """Evaluate whether a completion event may pass the repeat-learning gate.

    The function is fail-closed. A completion event with no resolvable ledger
    or evidence is BLOCKED. A uniquely matched unresolved repeat is held.
    A uniquely matched VERIFIED repeat may pass only with a later behavioral
    receipt in evidence_refs.
    """
    evidence = tuple(str(x) for x in (evidence_refs or ()) if str(x).strip())
    ts = time.time() if timestamp is None else timestamp

    if not isinstance(ledger, list):
        return LearningGateResult(
            passed=False, decision=BLOCKED,
            reasons=["repeat ledger missing or unreadable — UNKNOWN/BLOCKED, never PASS"],
        )

    matches = [e for e in ledger if isinstance(e, dict) and _matches(topic, action, e)]
    unresolved = [
        e for e in matches
        if str(e.get("fix_status", "")).upper() in UNRESOLVED_STATUSES
    ]

    if len(unresolved) > 1:
        ids = tuple(str(e.get("id", "")) for e in unresolved)
        return LearningGateResult(
            passed=False, decision=BLOCKED, matched_ids=ids,
            reasons=["ambiguous unresolved directive match — BLOCKED, never PASS"],
        )

    if len(unresolved) == 1:
        e = unresolved[0]
        rec = _receipt(
            e, LEARNING_HOLD, evidence, authority_ref, ts,
            "known lesson is unresolved; completion cannot emit DONE",
        )
        return LearningGateResult(
            passed=False, decision=LEARNING_HOLD,
            receipts=[rec], matched_ids=(str(e.get("id", "")),),
            reasons=["unresolved known lesson requires LEARNING_HOLD"],
        )

    verified = [
        e for e in matches
        if str(e.get("fix_status", "")).upper() == TERMINAL_STATUS
    ]
    if len(verified) > 1:
        ids = tuple(str(e.get("id", "")) for e in verified)
        return LearningGateResult(
            passed=False, decision=BLOCKED, matched_ids=ids,
            reasons=["ambiguous verified directive match — BLOCKED, never PASS"],
        )

    if len(verified) == 1:
        if not evidence:
            e = verified[0]
            rec = _receipt(
                e, BLOCKED, evidence, authority_ref, ts,
                "missing later behavioral evidence for release",
            )
            return LearningGateResult(
                passed=False, decision=BLOCKED,
                receipts=[rec], matched_ids=(str(e.get("id", "")),),
                reasons=["missing behavioral evidence — BLOCKED, never PASS"],
            )
        e = verified[0]
        rec = _receipt(
            e, PASS, evidence, authority_ref, ts,
            "later behavioral evidence supplied for verified fix",
        )
        return LearningGateResult(
            passed=True, decision=PASS,
            receipts=[rec], matched_ids=(str(e.get("id", "")),),
        )

    # No known repeat for this topic/action. This gate does not invent a hold.
    return LearningGateResult(
        passed=True, decision=PASS,
        reasons=["no matching repeat entry"],
    )


def release_learning_hold(
    *,
    entry: dict[str, Any],
    later_behavioral_evidence: list[str] | tuple[str, ...] | None = None,
    authorized_exception: dict[str, Any] | None = None,
    timestamp: float | None = None,
) -> LearningGateResult:
    """Release a hold only through verified behavior or governed exception."""
    ts = time.time() if timestamp is None else timestamp
    evidence = tuple(str(x) for x in (later_behavioral_evidence or ()) if str(x).strip())
    status = str(entry.get("fix_status", "")).upper()

    if status == TERMINAL_STATUS and evidence:
        rec = _receipt(
            entry, PASS, evidence, "", ts,
            "hold released by later behavioral verification",
        )
        return LearningGateResult(True, PASS, [rec], matched_ids=(str(entry.get("id", "")),))

    ex = authorized_exception if isinstance(authorized_exception, dict) else None
    if ex and ex.get("authorized") is True:
        if all(isinstance(ex.get(k), str) and ex[k].strip() for k in ("reason", "scope", "expiry")):
            rec = _receipt(
                entry, PASS, evidence, str(ex.get("authority_ref", "")), ts,
                "governed exception released hold; fix_status remains unchanged",
            )
            return LearningGateResult(True, PASS, [rec], matched_ids=(str(entry.get("id", "")),))

    return LearningGateResult(
        False, BLOCKED,
        reasons=["hold release lacks later behavioral verification or governed exception"],
        matched_ids=(str(entry.get("id", "")),),
    )
