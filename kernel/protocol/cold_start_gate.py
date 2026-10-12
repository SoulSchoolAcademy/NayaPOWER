"""
cold_start_gate.py — Machine law: mandatory boot sequence for fresh agents.

A fresh agent may not begin governed work until it can demonstrate:
1. Valid protocol read receipt (read_receipt.py)
2. Identity: who it is, who the human director is
3. Authority: what it may and may not do
4. Navigation: where current truth lives
5. Next action: exactly one executable next step
6. Activation checklist: all 14 thinking lessons + Operating Code V2
   machine-verified present, complete, current, and byte-faithful to
   canonical sources (tools/activation_checklist.py) — fail closed.

This is the machine twin of the ACTIVATION ACCEPTANCE contract.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field

from .read_receipt import ReadReceipt


def _default_repo_root() -> str:
    # kernel/protocol/cold_start_gate.py -> repo root.
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class ColdStartState:
    agent_id: str
    human_director: str
    lane: str
    authority_summary: str
    current_truth_location: str
    next_action: str
    receipt: ReadReceipt | None = None
    # Checkout holding NAYA-ACTIVATION/ and BRAIN/. Defaults to the repo
    # this module lives in. Tests point it at fixture trees.
    repo_root: str | None = None
    # Optional agent activation checklist claim, verified against canonical
    # bytes (see tools/activation_checklist.py). None = self-audit of the
    # canonical artifacts only. May carry a "comprehension" map of
    # {lesson_id: self-attested score}, checked for internal consistency
    # (see _check_comprehension_attestation — NOT proof of comprehension).
    activation_claim: dict | None = None


@dataclass
class ColdStartResult:
    passed: bool
    failures: list = field(default_factory=list)


REQUIRED_TRUTH_MARKERS = ["#2154", "main"]


EXPECTED_ACTIVATION_LESSON_IDS = frozenset("L%d" % i for i in range(1, 15))


def _check_comprehension_attestation(canonical: dict, claim: dict) -> list:
    """Internal-consistency check on a claim's self-attested comprehension
    scores — NOT a proof of comprehension.

    If the claim carries "comprehension": {lesson_id: score}, every claimed
    score must meet the curriculum's per-lesson minimum (default 7).
    This blocks a claim that ADMITS failure (score below the bar) — it
    cannot verify that a passing score reflects real understanding.
    Behavioral proof (novel problem, blind scored >= 7 per the curriculum's
    verification protocol) is the ritual side of the provision and lives
    outside this machine gate. Score claims are self-attested, never
    verified proof."""
    failures = []
    comp = claim.get("comprehension")
    if comp is None:
        return failures
    if not isinstance(comp, dict):
        return ["COMPREHENSION_ATTESTATION_MALFORMED: claim.comprehension "
                "must be an object of {lesson_id: score}"]
    minimum = (canonical.get("curriculum", {}).get("pass_policy") or {}
               ).get("per_lesson_minimum", 7)
    for lid, score in comp.items():
        if lid not in EXPECTED_ACTIVATION_LESSON_IDS:
            failures.append(
                "COMPREHENSION_ATTESTATION_UNKNOWN_LESSON: %r is not one of "
                "the 14 canonical lessons" % (lid,))
            continue
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            failures.append(
                "COMPREHENSION_ATTESTATION_MALFORMED: %s score %r is not a "
                "number" % (lid, score))
        elif score < minimum:
            failures.append(
                "COMPREHENSION_ATTESTATION_BELOW_THRESHOLD: %s claimed score "
                "%s < per-lesson minimum %s — the claim itself admits the "
                "comprehension requirement is not met" % (lid, score, minimum))
    return failures


def run_cold_start(state: ColdStartState,
                   current_protocol_version: str | None = None,
                   current_source_sha: str | None = None) -> ColdStartResult:
    failures: list[str] = []

    # 1. Read receipt must exist and verify.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the protocol, answer the authority questions.")
    elif not state.receipt.verify():
        failures.append("Read receipt invalid or failed grading. Re-read the protocol.")
    else:
        # Law 12 (ACTIVE): a cryptographically valid receipt is not enough —
        # it must be fresh. Current world state auto-resolves when the
        # caller does not supply it, so this check fires on every boot, not
        # only for callers that opt in. If the protocol version moved since
        # the receipt was issued, the agent read a different protocol:
        # re-read required. (The receipt does not record the read-time tip,
        # so no tip dependency is fabricated — the version check is the
        # precise, honest signal.)
        from .proof_expiry import (
            proof_from_read_receipt, validate_proof, resolve_current_state,
        )
        current_state = resolve_current_state()
        if current_protocol_version is not None:
            current_state["policy_ref"] = current_protocol_version
        if current_source_sha is not None:
            current_state["source_sha"] = current_source_sha
        proof = proof_from_read_receipt(state.receipt)
        validation = validate_proof(proof, current_state)
        if not validation.is_current:
            failures.append(
                f"Read receipt stale (Law 12): {validation.reason()}. "
                "Re-read the current protocol.")

    # 2. Identity.
    if not state.agent_id.strip():
        failures.append("No agent identity declared.")
    if "shawn" not in state.human_director.lower():
        failures.append("Human director not identified as Shawn.")

    # 3. Authority summary must name at least one protected gate and
    # acknowledge Law 11 (do no harm) as the only hard law.
    auth = state.authority_summary.lower()
    if not any(k in auth for k in ["production", "credential", "money",
                                    "destructive", "ratif", "privacy", "security"]):
        failures.append("Authority summary does not name protected gates.")
    if "do no harm" not in auth and "law 11" not in auth:
        failures.append(
            "Authority summary does not acknowledge Law 11 (do no harm) "
            "as the only hard law."
        )

    # 4. Navigation: must reference the mission-state feed and current main.
    nav = state.current_truth_location.lower()
    if not all(m in nav for m in REQUIRED_TRUTH_MARKERS):
        failures.append(
            "Truth location must reference the mission-state feed (#2154) "
            "and current main — the board alone is not the entire source of truth. "
            "(#1354 is archived; sign in/out on #1713/#1714/#1715.)"
        )

    # 5. Exactly one next action.
    if not state.next_action.strip():
        failures.append("No next executable action declared.")

    # 6. Activation checklist (Gate 1): the 14 thinking lessons +
    # Operating Code V2 must be machine-verified present, complete,
    # current, and byte-faithful to canonical sources. FAIL CLOSED:
    # an unreadable canonical artifact or a REJECT verdict blocks
    # activation — never a warning, never a bypass.
    #
    # WHAT THIS GUARANTEES: (a) the canonical artifacts themselves are
    # readable and intact — exactly 14 lessons (ids L1..L14), curriculum
    # flagged mandatory, per-lesson pass policy >= 7, lesson bytes matching
    # the pinned fingerprints, human/machine twin consistency, and the
    # three V2 files present with current pinned bytes; (b) when the agent
    # supplies an activation claim, the claim names exactly the 14
    # canonical lessons with fingerprints equal to RECOMPUTED canonical
    # bytes (no fake ids, no partial loading, no forged/stale content).
    # Any missing lesson, stale hash, drifted V2, or unreadable canonical
    # file REJECTS the boot.
    #
    # WHAT THIS DOES NOT GUARANTEE: comprehension. Matching canonical
    # content proves INTEGRITY — that the right bytes are in front of the
    # agent — not that the agent internalized the lessons. Behavioral
    # proof (novel problem, blind scored >= 7 per the curriculum's
    # verification protocol) is the ritual side of the same provision and
    # lives outside this machine gate. A claim's self-attested
    # comprehension scores are checked only for internal consistency
    # (every claimed score must meet the per-lesson minimum); the scores
    # themselves are self-attested, never verified proof. "A Smart Link
    # proves where intelligence can be found. It does not prove Naya
    # learned." — the same holds for this checklist.
    # The verifier is trusted code shipped with this gate: import it from
    # the checkout this module lives in. The canonical ARTIFACTS under
    # verification come from state.repo_root (the data under test), which
    # may be a fixture tree — a fixture carries data, never the verifier.
    verifier_root = _default_repo_root()
    _known = {os.path.abspath(p) for p in sys.path if p}
    if os.path.abspath(verifier_root) not in _known:
        # tools/ has no __init__.py (namespace package); the repo root must
        # be importable for the cold start gate to reach the verifier.
        sys.path.insert(0, verifier_root)
    try:
        from tools.activation_checklist import check_checklist, load_canonical
    except ImportError as exc:
        failures.append("Activation checklist verifier unavailable — "
                        "fail closed: %s" % (exc,))
    else:
        artifact_root = os.path.abspath(state.repo_root) \
            if state.repo_root else verifier_root
        canonical, err = load_canonical(artifact_root)
        if canonical is None:
            failures.append("Activation checklist canonical artifacts "
                            "unreadable — fail closed: %s" % (err,))
        else:
            verdict, violations = check_checklist(canonical,
                                                  state.activation_claim)
            if verdict != "CHECKLIST-VERIFIED":
                failures.append("Activation checklist REJECT — activation "
                                "blocked: %s" % "; ".join(violations))
            elif state.activation_claim is not None:
                failures.extend(_check_comprehension_attestation(
                    canonical, state.activation_claim))

    return ColdStartResult(passed=not failures, failures=failures)
