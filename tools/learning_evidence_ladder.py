"""Evidence-driven E0-E7 learning-level evaluator (convergence item C).

SN-0546 law: a learning level is not earned until a governed, observable
runtime transition proves it. Schema capacity (E0-E7 fields) is not
attainment. The canonical E0-E7 vocabulary comes from the learner-state
schema (supabase/migrations/20260827213628_create_learner_state_and_evidence.sql).

This module is the GOVERNED TRANSITION MACHINE for that law. It is pure:
no DB, no network. A reader assembles the evidence bundle from rows the
runtime already persists; this module computes the EARNED level from
observable evidence and audits a CLAIMED level against it.

Fail-closed rules (never rounded up, never assumed):
  - claimed level above earned level  -> REJECTED (LEVEL_NOT_EARNED),
    naming the first unproven level.
  - any conflicting evidence          -> FALSIFIED, earned capped at E0.
  - stale evidence                     -> earned capped at E1 (application,
    transfer and retention require fresh evidence).
  - verifier == producer/applier at a level that requires independent
    witness                            -> that level unproven (self-attestation
    is not verification).
  - no capture evidence                -> UNPROVEN (not E0; E0 still requires
    a capture receipt).

A receipt/evaluation is evidence, never authority (the #1712 lesson): this
module exposes no field any authority gate may accept as a grant.

The ladder itself lives in learning_evidence_ladder.json (executable data).
The predicates below implement each level's transition; LEVELS in that JSON
declare the required evidence fields. test_learning_evidence_ladder.py
asserts the two stay in sync so the law cannot drift from the code.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
LADDER_PATH = HERE.with_name("learning_evidence_ladder.json")

SCHEMA = "NAYANET_LEARNING_EVIDENCE_LADDER_EVALUATION_V1"

LEVEL_ORDER: tuple[str, ...] = (
    "E0_EXPOSED",
    "E1_UNDERSTANDS",
    "E2_CAN_DO",
    "E3_INDEPENDENT",
    "E4_TRANSFER",
    "E5_CAN_TEACH",
    "E6_RETAINED",
    "E7_MASTERED",
)


def load_ladder() -> dict[str, Any]:
    """Load the executable ladder data. Raises FileNotFoundError if the law file is missing."""
    return json.loads(LADDER_PATH.read_text(encoding="utf-8"))


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has(obj: Any, *fields: str) -> bool:
    """All named fields present; dotted names traverse dicts."""
    if not isinstance(obj, dict):
        return False
    for field in fields:
        node: Any = obj
        for part in field.split("."):
            if not isinstance(node, dict) or not _is_nonempty_str(node.get(part)):
                return False
            node = node[part]
    return True


def _transition_e0(ev: dict[str, Any]) -> tuple[bool, str]:
    cap = ev.get("capture_receipt")
    if _has(cap, "intelligent_block_id", "captured_at"):
        return True, ""
    return False, "E0_EXPOSED unproven: missing capture_receipt.intelligent_block_id/captured_at"


def _transition_e1(ev: dict[str, Any]) -> tuple[bool, str]:
    comp = ev.get("comprehension")
    if not isinstance(comp, dict):
        return False, "E1_UNDERSTANDS unproven: missing comprehension evidence"
    if not _has(comp, "control_receipt", "treatment_receipt", "independent_verifier", "verified_at"):
        return False, "E1_UNDERSTANDS unproven: comprehension missing control/treatment receipt or independent verifier"
    if str(comp.get("independent_verifier")) == str(ev.get("_producer_id") or ""):
        return False, "E1_UNDERSTANDS unproven: verifier is the producer (self-attestation)"
    return True, ""


def _transition_e2(ev: dict[str, Any]) -> tuple[bool, str]:
    app = ev.get("application_receipt")
    if _has(app, "retrieval_ref", "task_ref", "applied_at", "applier"):
        return True, ""
    return False, "E2_CAN_DO unproven: missing application_receipt (retrieval_ref/task_ref/applied_at/applier)"


def _transition_e3(ev: dict[str, Any]) -> tuple[bool, str]:
    out = ev.get("outcome")
    if not isinstance(out, dict):
        return False, "E3_INDEPENDENT unproven: missing outcome evidence"
    if not _has(out, "measured_effect"):
        return False, "E3_INDEPENDENT unproven: outcome has no measured_effect"
    iv = out.get("independent_verification")
    if not _has(iv, "verifier", "verified_at"):
        return False, "E3_INDEPENDENT unproven: outcome lacks independent_verification.verifier/verified_at"
    applier = str((ev.get("application_receipt") or {}).get("applier") or "")
    if applier and str(iv.get("verifier")) == applier:
        return False, "E3_INDEPENDENT unproven: verifier is the applier (executor-owned observation)"
    return True, ""


def _transition_e4(ev: dict[str, Any]) -> tuple[bool, str]:
    transfer = ev.get("transfer")
    if not isinstance(transfer, list) or not transfer:
        return False, "E4_TRANSFER unproven: no transfer evidence"
    app_task = str((ev.get("application_receipt") or {}).get("task_ref") or "")
    for t in transfer:
        if not isinstance(t, dict):
            continue
        task_ref = str(t.get("task_ref") or "")
        if app_task and task_ref == app_task:
            continue  # same-task repetition is not transfer (anti-memorization)
        if _has(t, "measured_effect") and _has(t.get("independent_verification"), "verifier"):
            return True, ""
    return False, "E4_TRANSFER unproven: no held-out task with measured effect and independent verification"


def _transition_e5(ev: dict[str, Any]) -> tuple[bool, str]:
    uses = ev.get("successor_use")
    if not isinstance(uses, list) or not uses:
        return False, "E5_CAN_TEACH unproven: no cold-successor application evidence"
    producer = str(ev.get("_producer_id") or "")
    applier = str((ev.get("application_receipt") or {}).get("applier") or "")
    for u in uses:
        if not isinstance(u, dict):
            continue
        sid = str(u.get("successor_id") or "")
        if not sid or (producer and sid == producer) or (applier and sid == applier):
            continue  # not cold
        if _has(u, "task_ref") and _has(u.get("independent_verification"), "verifier"):
            return True, ""
    return False, "E5_CAN_TEACH unproven: no cold successor (distinct identity) with verified outcome"


def _transition_e6(ev: dict[str, Any]) -> tuple[bool, str]:
    ret = ev.get("retention")
    if _has(ret, "revalidated_at", "revalidation_receipt"):
        return True, ""
    return False, "E6_RETAINED unproven: missing retention.revalidated_at/revalidation_receipt"


def _transition_e7(ev: dict[str, Any]) -> tuple[bool, str]:
    master = ev.get("mastery")
    if not isinstance(master, dict):
        return False, "E7_MASTERED unproven: missing mastery compound evidence"
    verifiers = master.get("distinct_verifiers")
    domains = master.get("distinct_transfer_domains")
    if not isinstance(verifiers, int) or verifiers < 2:
        return False, "E7_MASTERED unproven: fewer than 2 distinct independent verifiers"
    if not isinstance(domains, int) or domains < 2:
        return False, "E7_MASTERED unproven: fewer than 2 distinct transfer domains"
    if ev.get("conflicts"):
        return False, "E7_MASTERED unproven: conflicts present"
    if ev.get("stale") is True:
        return False, "E7_MASTERED unproven: evidence stale"
    return True, ""


_TRANSITIONS: dict[str, Any] = {
    "E0_EXPOSED": _transition_e0,
    "E1_UNDERSTANDS": _transition_e1,
    "E2_CAN_DO": _transition_e2,
    "E3_INDEPENDENT": _transition_e3,
    "E4_TRANSFER": _transition_e4,
    "E5_CAN_TEACH": _transition_e5,
    "E6_RETAINED": _transition_e6,
    "E7_MASTERED": _transition_e7,
}


def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    """Compute the EARNED level for a learning record from observable evidence.

    record keys (all optional except evidence content):
      id, target, producer_id, status, claimed_level,
      evidence: {capture_receipt, comprehension, application_receipt,
                 outcome, transfer, successor_use, retention, mastery,
                 conflicts, stale}

    Returns the evaluation object with schema
    NAYANET_LEARNING_EVIDENCE_LADDER_EVALUATION_V1. Never raises on
    malformed input: malformed evidence is unproven, not an exception.
    """
    record = record if isinstance(record, dict) else {}
    ev = record.get("evidence")
    ev = ev if isinstance(ev, dict) else {}
    # Record-level identity is needed for self-attestation checks; inject it
    # into the evidence bundle under an explicit internal key so the
    # transitions can see it without a signature change.
    ev = dict(ev)
    ev["_producer_id"] = record.get("producer_id")

    ladder = load_ladder()
    honest_labels = ladder.get("honest_labels", {})

    proven: list[str] = []
    unproven: list[str] = []
    falsified = bool(ev.get("conflicts"))
    stale = ev.get("stale") is True

    for level in LEVEL_ORDER:
        # Cumulative: stop at the first unproven level; higher levels are
        # unreachable without the full chain below them.
        if unproven:
            unproven.append(f"{level}: unreachable (lower level unproven)")
            continue
        ok, reason = _TRANSITIONS[level](ev)
        if ok:
            proven.append(level)
        else:
            unproven.append(reason)

    if falsified:
        # Any conflict collapses the chain to E0: the evidence disagrees
        # with itself, so nothing above exposure can be trusted.
        earned = "E0_EXPOSED" if "E0_EXPOSED" in proven else "UNPROVEN"
        cap_note = "conflicts present: earned capped at E0_EXPOSED"
    elif stale and proven:
        # Stale evidence cannot prove application/transfer/retention.
        earned = "E1_UNDERSTANDS" if "E1_UNDERSTANDS" in proven else (
            proven[-1] if proven else "UNPROVEN")
        cap_note = "stale evidence: earned capped at E1_UNDERSTANDS" if earned == "E1_UNDERSTANDS" else ""
    else:
        earned = proven[-1] if proven else "UNPROVEN"
        cap_note = ""

    claimed = record.get("claimed_level")
    claimed_rank = LEVEL_ORDER.index(claimed) if claimed in LEVEL_ORDER else None
    earned_rank = LEVEL_ORDER.index(earned) if earned in LEVEL_ORDER else -1

    if falsified:
        verdict, code = "FALSIFIED", "EVIDENCE_CONFLICT"
    elif not proven:
        verdict, code = "UNPROVEN", "NO_CAPTURE_EVIDENCE"
    elif claimed_rank is None:
        verdict, code = "REJECTED", "UNKNOWN_CLAIMED_LEVEL"
    elif claimed_rank > earned_rank:
        verdict, code = "REJECTED", "LEVEL_NOT_EARNED"
    elif claimed_rank == earned_rank:
        verdict, code = "ACCEPTED", "CLAIM_MATCHES_EVIDENCE"
    else:
        verdict, code = "UNDERCLAIMED", "EVIDENCE_EXCEEDS_CLAIM"

    return {
        "schema": SCHEMA,
        "learning_id": record.get("id"),
        "target": record.get("target"),
        "claimed_level": claimed,
        "earned_level": earned,
        "honest_label": honest_labels.get(earned, earned),
        "proven_chain": proven,
        "unproven": unproven,
        "verdict": verdict,
        "verdict_code": code,
        "cap_note": cap_note,
        # Explicit: evaluation is evidence, never authority. No grant fields.
        "authority": "NONE — this evaluation is evidence only; it authorizes nothing",
    }
