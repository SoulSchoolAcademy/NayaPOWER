"""DB-path held-out evidence contract — the READER/GATE side.

Phase 3B of the epistemic wiring (Shawn's directive 2026-10-10: "wire it into
the live system immediately").

THE GAP (Phase 2's finding): strengthen(), apply_retained_intelligence() and
integrate_verified_lesson() have ZERO production callers on main. The LIVE
learning pipeline is the Supabase path:

    tools/learning_admission_gate.py        (design gate — pure)
      -> tools/learning_verification_queue.py (worked queue — pure)
      -> learning_evidence table            (status, observed_value jsonb, ...)

The verification queue writes NO held-out markers into observed_value, so the
independence gate cannot verify held-out evaluation on the DB path. This module
closes the READER side of that gap: given a learning_evidence row, return the
Phase-2 eligibility verdict using the SAME predicate logic.

HELD-OUT EVIDENCE CONTRACT — what the writer must record in
observed_value.held_out_evidence (the WRITER is not implemented here; it is a
production DB write path and needs Shawn's per-statement word — see the Phase
3B report for the exact proposal):

    observed_value.held_out_evidence = {
      "schema": "naya.held-out-evidence.v1",
      "recorded_at": "<ISO-8601 UTC>",
      "recorded_by": "<seat or service that wrote the markers>",
      "evidence_families": [
        {"family_id": "treatment-arm",
         "independent_of_lesson": true,
         "basis": "machine measurement against the pre-registered criterion"},
        {"family_id": "verifier-held-out",
         "independent_of_lesson": true,
         "basis": "different-seat re-measurement on held-out task instances"}
      ],
      "held_out_evaluation": {
        "evaluation_id": "HO-<uuid>",
        "evaluator": "<normalized identity>",
        "evaluator_role": "verifier | independent-seat | machine",
        "verdict": "VERIFIED | NOT_VERIFIED",
        "measured_at": "<ISO-8601 UTC>",
        "support_arm_ids": ["<the lesson's own supporting evidence>"],
        "evaluation_arm_ids": ["<arms the evaluation actually used>"],
        "overlap_with_support": false,
        "held_out_from_support": true
      },
      # Revocation / uncertainty in Phase 2's vocabulary, verbatim:
      "revocation_verdict":
        "UNAFFECTED | REQUALIFIED | DOWNGRADED | INSUFFICIENT_DATA | SUSPENDED | REVOKED",
      "uncertainty_assessment":
        "independently_cleared | unassessed | possibly_compromised | confirmed_compromised",
      "incident_id": "<id> | null"
    }

READER SEMANTICS (db_row_eligibility):

  1. row.status != "ACTIVE" -> INELIGIBLE_NOT_ACTIVE. Only ACTIVE rows are
     lessons the system stands behind (matches lesson_from_evidence_row,
     which maps ACTIVE rows only).
  2. No held_out_evidence block (absent) -> "no incident on record" ->
     ELIGIBLE for ACTIVE rows. This matches Phase 2's test_no_markers_eligible
     EXACTLY: absent markers are NOT "unassessed under an incident". The four
     assessment states classify families WITHIN a known incident; inventing an
     incident where none is recorded would make the DB path dead on arrival.
  3. held_out_evidence present but not a dict -> malformed marker block ->
     INELIGIBLE_UNCERTAIN (fail closed).
  4. Self-certification check on held_out_evaluation (when present):
       - held_out_from_support is False            -> INELIGIBLE_UNCERTAIN
       - overlap_with_support is True              -> INELIGIBLE_UNCERTAIN
       - evaluator (normalized) == doer or scorer  -> INELIGIBLE_UNCERTAIN
         (the "held-out" evaluation was performed by the lesson's own
         author/scorer — the verifier-chain fields in observed_value)
       - held_out_evaluation present but malformed, or evaluator
         empty/unverifiable                        -> INELIGIBLE_UNCERTAIN
         (unknown independence is not proven independence)
     The evaluator MAY equal the verifier: the verifier is the independent
     party (doer != scorer != verifier is the admission contract).
  5. Otherwise the revocation/uncertainty vocabulary is delegated to
     kernel.memory_metabolism.act_eligibility via a record adapter — the SAME
     predicate logic, not a copy. Phase 2's semantics hold verbatim:
       REVOKED / SUSPENDED / INSUFFICIENT_DATA refuse;
       DOWNGRADED / REQUALIFIED / UNAFFECTED retain;
       confirmed_compromised / possibly_compromised refuse;
       unassessed + incident_id refuses; unassessed without incident retains;
       independently_cleared retains; unrecognized values fail closed.

The function is pure: no DB, no network. Evaluate at the moment of use
(Freshness Law) — callers must re-evaluate, never cache the verdict.
"""

from __future__ import annotations

from typing import Any, Callable

from kernel.memory_metabolism import (
    ELIGIBLE,
    INELIGIBLE_NOT_ACTIVE,
    INELIGIBLE_UNCERTAIN,
    act_eligibility,
)

# --- verifier-chain identity contract --------------------------------------
# Canonical contract: tools/learning_admission_gate.py — normalize_identity()
# ("Naya-5", "naya-5 " and "NAYA-5" are one seat). Prefer the canonical import;
# the local mirror below is a defensive fallback for contexts where tools/ is
# not importable, not a parallel contract (same pattern as
# kernel/self_integration.py).
try:  # pragma: no cover - fallback path: canonical import unavailable
    from tools.learning_admission_gate import (  # type: ignore[import-not-found]
        normalize_identity as _gate_normalize_identity,
    )

    def normalize_identity(value: Any) -> str:
        return _gate_normalize_identity(value)

except ImportError:  # canonical import unavailable; mirror its contract

    def normalize_identity(value: Any) -> str:
        """Canonical identity comparison: case- and whitespace-insensitive."""
        return str(value).strip().casefold()


# --- contract constants ------------------------------------------------------
HELD_OUT_EVIDENCE_SCHEMA = "naya.held-out-evidence.v1"
_HELD_OUT_KEY = "held_out_evidence"
_ACTIVE_STATUS = "ACTIVE"


class _RowRecord:
    """Adapter: a learning_evidence row -> act_eligibility's record shape.

    act_eligibility reads record.memory_state and record.provenance
    {revocation_verdict, uncertainty_assessment, incident_id}. The adapter
    carries the row's status and the marker block's vocabulary verbatim, so
    the predicates run unchanged.
    """

    __slots__ = ("memory_state", "provenance")

    def __init__(self, memory_state: str, provenance: dict[str, Any]) -> None:
        self.memory_state = memory_state
        self.provenance = provenance


def _self_certified(held: dict[str, Any], observed: dict[str, Any]) -> bool:
    """True when the recorded 'held-out' evaluation is self-certification.

    A held-out evaluation certifies independence only when it is genuinely
    outside the lesson's own support: named evaluator, no arm overlap with
    the lesson's supporting evidence, and an evaluator who is neither the
    doer nor the scorer. Anything less is not held out — it is the lesson
    certifying itself.
    """
    hoe = held.get("held_out_evaluation")
    if hoe is None:
        return False
    if not isinstance(hoe, dict):
        return True  # malformed: independence unverifiable -> fail closed
    if hoe.get("held_out_from_support") is False:
        return True
    if hoe.get("overlap_with_support") is True:
        return True
    evaluator = normalize_identity(hoe.get("evaluator") or "")
    if not evaluator:
        return True  # unnamed evaluator: independence unverifiable
    doer = normalize_identity(observed.get("doer") or "")
    scorer = normalize_identity(observed.get("scorer") or "")
    # The evaluator may equal the verifier (the independent party); it must
    # never be the doer or the scorer.
    if evaluator == doer or evaluator == scorer:
        return True
    return False


def db_row_eligibility(row: Any) -> str:
    """Phase-2 eligibility verdict for one learning_evidence row.

    Returns ELIGIBLE or one of the INELIGIBLE_* codes, reusing
    kernel.memory_metabolism.act_eligibility's predicate logic exactly.
    Pure: no DB, no network. Evaluate at use time; never cache.
    """
    if not isinstance(row, dict):
        return INELIGIBLE_NOT_ACTIVE
    if row.get("status") != _ACTIVE_STATUS:
        return INELIGIBLE_NOT_ACTIVE
    observed = row.get("observed_value")
    observed = observed if isinstance(observed, dict) else {}

    held = observed.get(_HELD_OUT_KEY)
    if held is None:
        # No markers: "no incident on record" — NOT "unassessed under an
        # incident". Matches Phase 2's test_no_markers_eligible exactly.
        return act_eligibility(_RowRecord(_ACTIVE_STATUS, {}))
    if not isinstance(held, dict):
        return INELIGIBLE_UNCERTAIN  # malformed marker block: fail closed
    if _self_certified(held, observed):
        # Uncertain independence can certify nothing.
        return INELIGIBLE_UNCERTAIN

    provenance = {
        "revocation_verdict": held.get("revocation_verdict"),
        "uncertainty_assessment": held.get("uncertainty_assessment"),
        "incident_id": held.get("incident_id"),
    }
    return act_eligibility(_RowRecord(_ACTIVE_STATUS, provenance))


def db_lesson_eligibility_hook(
    rows_by_id: dict[str, dict[str, Any]],
) -> Callable[[str], str]:
    """Build an apply_retained_intelligence lesson_eligibility hook from rows.

    Maps lesson_id -> db_row_eligibility(row). A lesson_id with no row on
    record fails closed: an unverifiable lesson certifies nothing.
    """
    def hook(lesson_id: str) -> str:
        row = rows_by_id.get(str(lesson_id))
        if row is None:
            return INELIGIBLE_UNCERTAIN
        return db_row_eligibility(row)

    return hook
