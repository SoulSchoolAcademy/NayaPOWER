"""Truth-state poisoning guard.

THE HOLE (Naya 3, PR #1463)
---------------------------
The structural poison battery catches SHAPE. It misses MEANING.

`tools/smart_note_v2.py` has a legitimate `promote()` that validates authority
and evidence and writes a promotion receipt. But nothing stops a DIRECT EDIT to
`.naya/memory/smart-notes/index.json` setting:

    "truth_state": "CANDIDATE"  ->  "truth_state": "RATIFIED"

The structural audit sees a well-formed registry with correct hashes. It cannot
see that the note was escalated without anyone holding promotion authority, and
without a single piece of promotion evidence.

THE INVARIANT IMPLEMENTED HERE
------------------------------
Truth-state ELEVATION requires BOTH:

  1. valid promotion AUTHORITY  -- a named, authorised promoter
  2. valid promotion EVIDENCE  -- a receipt whose hash recomputes and whose
                                  evidence hashes match

No authority + evidence => the write is REJECTED, not recorded.

ELEVATION ORDER (monotonic). Lowering a state is never an escalation and is
never blocked here, because demotion must always be possible -- that is how a
poisoned note gets contained.

    CANDIDATE < TESTING < VERIFIED < RATIFIED < ACTIVE < LEARNED

ELEVATION IS CUMULATIVE AND PROVENANCE-BEARING. `ACTIVE` cannot be asserted
without a verified predecessor; `LEARNED` cannot be asserted without recorded
BEHAVIORAL evidence. Both are semantic claims, not labels.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

# Monotonic elevation ladder. Index order defines authority.
TRUTH_STATES: tuple[str, ...] = (
    "CANDIDATE", "TESTING", "VERIFIED", "RATIFIED", "ACTIVE", "LEARNED",
)
BASE_STATE = "CANDIDATE"

# States that may not be asserted without a proven predecessor.
REQUIRES_PREDECESSOR: dict[str, str] = {
    "ACTIVE": "VERIFIED",
    "LEARNED": "RATIFIED",
}


def rank(state: str) -> int:
    """Elevation rank. Unknown states rank 0 -- never above CANDIDATE."""
    try:
        return TRUTH_STATES.index(str(state).upper())
    except ValueError:
        return 0


def is_escalation(current: str, proposed: str) -> bool:
    """True only when the proposed state is strictly above the current one."""
    return rank(proposed) > rank(current)


@dataclass
class GuardResult:
    allowed: bool
    state: str
    reasons: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.allowed


def _hash_receipt(receipt: dict) -> str:
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def evidence_is_valid(receipt: dict | None, evidence_bundle: list[dict] | None) -> bool:
    """Receipt integrity + evidence agreement, recomputed not trusted.

    An unkeyed seal proves the receipt was not altered. It does not prove who
    promoted -- that is `authority_is_valid`'s job, and the separation is
    deliberate.
    """
    if not isinstance(receipt, dict) or not isinstance(evidence_bundle, list):
        return False
    if receipt.get("schema") != "naya.promotion-receipt.v1":
        return False
    if receipt.get("receipt_hash") != _hash_receipt(receipt):
        return False
    if not evidence_bundle:
        return False
    return [e.get("content_hash") for e in evidence_bundle] == \
        receipt.get("evidence_hashes")


def authority_is_valid(authority: dict | None) -> bool:
    """Named, authorised promoter. Absent or blank authority is never valid."""
    if not isinstance(authority, dict):
        return False
    who = str(authority.get("promoter") or "").strip()
    scope = str(authority.get("scope") or "").strip()
    return bool(who) and bool(scope)


def check_elevation(
    current_state: str,
    proposed_state: str,
    authority: dict | None = None,
    receipt: dict | None = None,
    evidence_bundle: list[dict] | None = None,
    behavioral_evidence: list[dict] | None = None,
) -> GuardResult:
    """The write-time invariant. Returns allowed/rejected; never raises."""
    cur = str(current_state or BASE_STATE).upper()
    new = str(proposed_state or "").upper()

    if not is_escalation(cur, new):
        # Not an escalation. Demotion and no-op are always permitted so a
        # poisoned note can always be contained.
        return GuardResult(True, new, reasons=["not an escalation"])

    res = GuardResult(False, new)

    if not authority_is_valid(authority):
        res.missing.append("promotion_authority")
    if not evidence_is_valid(receipt, evidence_bundle):
        res.missing.append("promotion_evidence")

    need = REQUIRES_PREDECESSOR.get(new)
    if need and rank(cur) < rank(need):
        res.missing.append(f"proven_predecessor:{need}")

    if new == "LEARNED" and not behavioral_evidence:
        res.missing.append("behavioral_evidence")

    if res.missing:
        res.reasons = [
            f"truth_state elevation to {new} rejected: missing "
            + ", ".join(res.missing)
        ]
        return res

    return GuardResult(True, new, reasons=["authority and evidence present"])


def recorded_authority(entry: dict) -> dict | None:
    """Authority AS THE CANONICAL WRITER RECORDS IT.

    `smart_note_v2.promote_note` (line ~723) writes:
        entry["promotion_receipt"] = {promoted_at, promoter, receipt_hash,
                                      threshold_version}
    It does NOT write a `promotion_authority` object. An earlier version of this
    guard looked for one and would therefore have flagged every legitimately
    promoted note as a semantic escalation -- a false-positive generator living
    in the safety layer. Fixed to read the real shape.

    `promotion_authority` is still accepted, for entries that carry the richer
    form written by `apply_elevation`.
    """
    if isinstance(entry.get("promotion_authority"), dict):
        return entry["promotion_authority"]
    rcpt = entry.get("promotion_receipt")
    if isinstance(rcpt, dict) and str(rcpt.get("promoter") or "").strip():
        return {
            "promoter": rcpt.get("promoter"),
            "scope": rcpt.get("scope") or rcpt.get("threshold_version") or "promote",
            "promoted_at": rcpt.get("promoted_at"),
            "receipt_hash": rcpt.get("receipt_hash"),
        }
    return None


def recorded_receipt_hash(entry: dict) -> str | None:
    rcpt = entry.get("promotion_receipt")
    if isinstance(rcpt, dict):
        h = rcpt.get("receipt_hash")
        if h:
            return str(h)
    return None


def audit_registry_semantics(registry: dict) -> list[str]:
    """Detect semantic escalation in an already-written registry.

    The READ side of the same law. A note found above VERIFIED with no recorded
    promotion authority has been escalated by hand, because the legitimate path
    always records one.

    Reads the field shape the canonical writer actually produces, so a
    correctly-promoted note is not flagged.
    """
    problems: list[str] = []
    for entry in registry.get("entries", []):
        sid = entry.get("smart_note_id") or entry.get("intelligent_block_id") or "?"
        state = str(entry.get("truth_state", BASE_STATE)).upper()
        if rank(state) <= rank("VERIFIED"):
            continue
        if not authority_is_valid(recorded_authority(entry)):
            problems.append(
                f"{sid}: truth_state={state} with NO recorded promotion "
                "authority -- semantic escalation"
            )
        if not recorded_receipt_hash(entry):
            problems.append(
                f"{sid}: truth_state={state} with NO promotion receipt hash -- "
                "meaning asserted without evidence"
            )
        if state == "LEARNED" and not entry.get("behavioral_evidence"):
            problems.append(
                f"{sid}: truth_state=LEARNED with NO behavioral evidence"
            )
        if entry.get("superseded_by") and recorded_authority(entry) \
                and not entry.get("authority_history"):
            problems.append(
                f"{sid}: superseded but authority history erased -- "
                "supersession must not erase who promoted it"
            )
    return problems


def new_state_needs_evidence(state: str) -> bool:
    return rank(state) > rank("VERIFIED")


def apply_elevation(
    entry: dict,
    proposed_state: str,
    authority: dict | None = None,
    receipt: dict | None = None,
    evidence_bundle: list[dict] | None = None,
    behavioral_evidence: list[dict] | None = None,
) -> GuardResult:
    """Apply an elevation to a registry entry, or refuse and leave it untouched.

    Refusal must not record anything. A rejected write is a non-event.
    """
    current = str(entry.get("truth_state", BASE_STATE)).upper()
    res = check_elevation(current, proposed_state, authority, receipt,
                          evidence_bundle, behavioral_evidence)
    if not res.allowed:
        return res

    if is_escalation(current, res.state):
        history = list(entry.get("authority_history") or [])
        if authority:
            history.append({
                "from": current, "to": res.state,
                "promoter": authority.get("promoter"),
                "scope": authority.get("scope"),
            })
            entry["promotion_authority"] = authority
        if receipt:
            # SAME SHAPE as smart_note_v2.promote_note writes. Two writers with
            # two shapes is the drift class this guard exists to stop -- so the
            # guard must not introduce a third shape.
            entry["promotion_receipt"] = {
                "promoted_at": receipt.get("promoted_at"),
                "promoter": authority.get("promoter") if authority else None,
                "receipt_hash": receipt.get("receipt_hash"),
                "threshold_version": receipt.get("threshold_version"),
            }
        if behavioral_evidence:
            entry["behavioral_evidence"] = behavioral_evidence
        entry["authority_history"] = history
        entry["truth_state"] = res.state
    else:
        entry["truth_state"] = res.state
    return res




