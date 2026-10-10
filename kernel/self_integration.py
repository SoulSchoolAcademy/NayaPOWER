"""SELF behavior integration (WO5b): verified lessons change behavior patterns.

Two seams, one loop:

1. integrate_verified_lesson() — a VERIFIED lesson from the learning chain
   becomes a versioned entry in the behavior-policy store. The verifier chain
   doer != scorer != verifier is re-validated at the door using the admission
   gate's identity contract; anything failing is refused, never integrated.

2. make_act_experience_hook() — the first production caller of
   SelfNode.record_experience(): after ACT completes an action, the observed
   outcome is preserved as experience in SELF. Wire it to
   kernel.act_pipeline.execute_plan's `on_executed` hook.

Learning-chain shape: integrate_verified_lesson() accepts the lesson record
that the learning pipeline carries — the fields of a learning_evidence row
(status ACTIVE) plus the verifier-chain fields that the verification queue
(B6b claim rule) guarantees. load_active_lessons() maps raw learning_evidence
rows to lesson records; only status == "ACTIVE" rows pass.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from kernel.behavior_policy import BehaviorPolicyStore
from kernel.self_node import SelfNode

# --- verifier-chain identity contract -------------------------------------
# Canonical contract: tools/learning_admission_gate.py on branch
# naya5/learning-admission-round2 (PR #2049) — normalize_identity() and the
# claim rule "the verifier must differ from BOTH the doer and the scorer"
# (tools/learning_verification_queue.py). The gate file is not on main yet,
# so import it when present and mirror the one-line contract until it lands;
# the mirror is deleted the moment the import succeeds in CI.
try:  # pragma: no cover - import path exists only after the gate merges
    from tools.learning_admission_gate import (  # type: ignore[import-not-found]
        normalize_identity as _gate_normalize_identity,
    )

    def normalize_identity(value: Any) -> str:
        return _gate_normalize_identity(value)

    _CONTRACT_SOURCE = "tools/learning_admission_gate.py (canonical)"

except ImportError:  # the gate branch is unmerged; mirror its contract

    def normalize_identity(value: Any) -> str:
        """Canonical identity comparison: case- and whitespace-insensitive."""
        return str(value).strip().casefold()

    _CONTRACT_SOURCE = "local mirror of tools/learning_admission_gate.py contract"

# Admission states the learning chain emits (admission gate round 2).
ADMITTED_CANDIDATE = "CANDIDATE"

# Verdicts the verification queue records.
VERDICT_VERIFIED = "VERIFIED"


class IntegrationError(ValueError):
    """Raised when a lesson cannot be integrated (fail closed, integrate nothing)."""


def validate_verifier_chain(*, doer: str, scorer: str, verifier: str) -> None:
    """Enforce doer != scorer != verifier, identity-normalized.

    Reuses the admission gate's contract (B6b): "Naya-5", "naya-5 " and
    "NAYA-5" are one seat. Raises IntegrationError on any collision.
    """
    if not str(doer or "").strip():
        raise IntegrationError("doer_required")
    if not str(scorer or "").strip():
        raise IntegrationError("scorer_required")
    if not str(verifier or "").strip():
        raise IntegrationError("verifier_required")
    d, s, v = (normalize_identity(x) for x in (doer, scorer, verifier))
    if d == s:
        raise IntegrationError("verifier_chain_broken:doer_equals_scorer")
    if v == d:
        raise IntegrationError("verifier_chain_broken:verifier_equals_doer")
    if v == s:
        raise IntegrationError("verifier_chain_broken:verifier_equals_scorer")


def lesson_from_evidence_row(row: dict[str, Any]) -> dict[str, Any] | None:
    """Map one learning_evidence row to a lesson record, or None when inactive.

    Row shape follows supabase/migrations/20260827213628_create_learner_state_
    and_evidence.sql (claim, status, observed_value jsonb, verification_method,
    ...). The verifier-chain fields ride in observed_value, written by the
    verification queue's claim/record_verdict steps:
        observed_value = {
          "situation": "<situation key>",
          "prescribed_behavior": "<behavior the lesson prescribes>",
          "doer": "...", "scorer": "...", "verifier": "...",
          "verdict": "VERIFIED",
          "admission_admitted_as": "CANDIDATE",
        }
    Only status == "ACTIVE" rows are lessons the system stands behind.
    """
    if not isinstance(row, dict) or row.get("status") != "ACTIVE":
        return None
    observed = row.get("observed_value")
    observed = observed if isinstance(observed, dict) else {}
    return {
        "lesson_id": str(row.get("id") or row.get("lesson_id") or ""),
        "claim": str(row.get("claim") or ""),
        "situation": str(observed.get("situation") or ""),
        "prescribed_behavior": str(observed.get("prescribed_behavior") or ""),
        "doer": str(observed.get("doer") or ""),
        "scorer": str(observed.get("scorer") or ""),
        "verifier": str(observed.get("verifier") or ""),
        "verdict": str(observed.get("verdict") or ""),
        "admission_admitted_as": str(observed.get("admission_admitted_as") or ""),
        "verification_method": str(row.get("verification_method") or ""),
        "level": str(row.get("level") or ""),
    }


def load_active_lessons(fetch_rows: Callable[[], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Pull ACTIVE lessons from the learning_evidence store.

    fetch_rows is the read side of the canonical Supabase query — injected so
    this module stays pure (no credentials, no network):
        supabase.table("learning_evidence").select("*").eq("status", "ACTIVE")
    Returns the mapped lesson records; inactive rows are dropped, never
    integrated.
    """
    lessons: list[dict[str, Any]] = []
    for row in fetch_rows():
        lesson = lesson_from_evidence_row(row)
        if lesson is not None:
            lessons.append(lesson)
    return lessons


def integrate_verified_lesson(
    lesson: dict[str, Any],
    policy_store: BehaviorPolicyStore,
    *,
    self_node: SelfNode | None = None,
) -> dict[str, Any]:
    """Integrate one verified lesson into the behavior-policy store.

    Gates (all must hold; anything failing raises IntegrationError and the
    store is untouched):
      1. lesson completeness — lesson_id, claim, situation,
         prescribed_behavior all present and non-empty.
      2. verdict == VERIFIED — only independently verified lessons change
         behavior (UNKNOWN != VERIFIED, NOT_VERIFIED != VERIFIED).
      3. verifier chain — doer != scorer != verifier, identity-normalized
         per the admission gate contract.
      4. admission — the lesson must carry an admission record admitted_as
         CANDIDATE (the admission gate's choke point). A missing, empty, or
         non-CANDIDATE record is refused: the choke point has no omit-field
         bypass, so lessons that never passed the admission gate can never
         reach the behavior store.

    On success the lesson's prescribed behavior becomes the policy for its
    situation at a new store version; optionally the integration itself is
    preserved as SELF experience. Returns the integration receipt.
    """
    if not isinstance(lesson, dict):
        raise IntegrationError("lesson_must_be_object")

    missing = [
        key
        for key in ("lesson_id", "claim", "situation", "prescribed_behavior")
        if not str(lesson.get(key) or "").strip()
    ]
    if missing:
        raise IntegrationError(f"lesson_incomplete:missing={','.join(missing)}")

    if str(lesson.get("verdict") or "").strip().upper() != VERDICT_VERIFIED:
        raise IntegrationError(
            f"lesson_not_verified:verdict={lesson.get('verdict')!r}"
        )

    validate_verifier_chain(
        doer=lesson.get("doer", ""),
        scorer=lesson.get("scorer", ""),
        verifier=lesson.get("verifier", ""),
    )

    admitted_as = str(lesson.get("admission_admitted_as") or "").strip()
    # Fail closed: the admission gate is the choke point — a missing,
    # empty, or non-CANDIDATE admission record is refused. An omitted field
    # must never be a bypass around the gate.
    if admitted_as != ADMITTED_CANDIDATE:
        raise IntegrationError(f"lesson_not_admitted:admitted_as={admitted_as!r}")

    prior_version = policy_store.current_version
    new_version = policy_store.integrate(
        situation=str(lesson["situation"]).strip(),
        behavior=str(lesson["prescribed_behavior"]).strip(),
        lesson_id=str(lesson["lesson_id"]).strip(),
        note=f"WO5b: integrated verified lesson {lesson['lesson_id']!r}",
    )

    experience_receipt: dict[str, Any] | None = None
    if self_node is not None:
        experience_receipt = self_node.record_experience(
            lesson=str(lesson["claim"]).strip(),
            observed_outcome=(
                f"verified lesson integrated as behavior policy "
                f"v{new_version} for situation {lesson['situation']!r}"
            ),
        )

    return {
        "status": "INTEGRATED",
        "lesson_id": lesson["lesson_id"],
        "situation": lesson["situation"],
        "policy_version": new_version,
        "prior_version": prior_version,
        "verifier_chain": "doer!=scorer!=verifier OK",
        "contract_source": _CONTRACT_SOURCE,
        "integrated_at": datetime.now(timezone.utc).isoformat(),
        "experience_receipt": experience_receipt,
    }


def make_act_experience_hook(self_node: SelfNode) -> Callable[[Any, Any], None]:
    """Build the ACT post-execution hook — record_experience()'s production caller.

    Pass the result as `on_executed` to kernel.act_pipeline.execute_plan().
    Only EXECUTION_COMPLETED receipts with executed=True are recorded; refused
    or failed executions carry no completed outcome and record nothing.
    """
    def _hook(plan: Any, receipt: Any) -> None:
        if getattr(receipt, "phase", "") != "EXECUTION_COMPLETED":
            return
        if not getattr(receipt, "executed", False):
            return
        chosen = getattr(plan, "chosen", None)
        expected = getattr(chosen, "expected_outcome", "") if chosen else ""
        self_node.record_experience(
            lesson=(
                f"ACT executed '{getattr(plan, 'action', '?')}' "
                f"(plan {getattr(plan, 'plan_id', '?')}): "
                f"expected '{expected}'"
            ),
            observed_outcome=str(getattr(receipt, "observed_outcome", None) or "no observed outcome recorded"),
        )

    return _hook
