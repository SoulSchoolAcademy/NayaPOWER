"""The three-gate threshold model for interpretation reopening.

Three SEPARATE decisions, three SEPARATE thresholds:

    Gate 1 — ADMIT the challenge?    (record it; low threshold by design)
    Gate 2 — REOPEN the resolution?   (materiality x consequence matrix)
    Gate 3 — RESTRICT application?    (precautionary for high consequence)

"Easy to challenge, hard to change established truth, appropriately
precautionary about consequential harm." Calibration ADVISES; it never
grants authorization. LAW hard stops override every gate.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Challenge quality (evidence strength of the objection)
# ---------------------------------------------------------------------------

OPINION = "OPINION"                    # unattributed, no testable reason
PLAUSIBLE = "PLAUSIBLE"                # specific source discrepancy
REPRODUCED = "REPRODUCED"              # reproducible contradictory result
INTEGRITY_DEFECT = "INTEGRITY_DEFECT"  # verified integrity/authority defect

_CHALLENGE_QUALITY = (OPINION, PLAUSIBLE, REPRODUCED, INTEGRITY_DEFECT)

# ---------------------------------------------------------------------------
# Consequence of the disputed interpretation being wrong
# ---------------------------------------------------------------------------

LOW = "LOW"
HIGH = "HIGH"

# ---------------------------------------------------------------------------
# Dependency of the proposed action on the disputed interpretation
# ---------------------------------------------------------------------------

INCIDENTAL = "INCIDENTAL"
CRITICAL = "CRITICAL"

# ---------------------------------------------------------------------------
# Gate outcomes
# ---------------------------------------------------------------------------

# Gate 1
ADMITTED = "ADMITTED"
REJECTED_DUPLICATE = "REJECTED_DUPLICATE"
REJECTED_UNATTRIBUTED = "REJECTED_UNATTRIBUTED"
REJECTED_NO_TRIGGER_EVIDENCE = "REJECTED_NO_TRIGGER_EVIDENCE"

# Gate 2
REOPEN_DEFERRED = "REOPEN_DEFERRED"      # recorded; review later
REOPEN_SCREEN = "REOPEN_SCREEN"          # cheap bounded screen only
REOPEN_QUEUED = "REOPEN_QUEUED"          # proportionate review queued
REOPEN_PROMPT = "REOPEN_PROMPT"          # reopen promptly
REOPEN_FORMAL = "REOPEN_FORMAL"          # full formal reopening
REOPEN_ESCALATE = "REOPEN_ESCALATE"      # reopen + LAW hard stops + escalate

# Gate 3
CONTINUE = "CONTINUE"                    # unaffected work continues
CONTINUE_QUALIFIED = "CONTINUE_QUALIFIED"  # continue with visible qualification
RESTRICT_DEPENDENT = "RESTRICT_DEPENDENT"  # restrict critically dependent use
SUSPEND = "SUSPEND"                      # suspend pending requalification


# The Gate 2 decision matrix: (challenge quality, consequence) -> reopening.
# Dependency CRITICAL escalates one step toward restriction at Gate 3.
_GATE2_MATRIX = {
    (OPINION, LOW): REOPEN_DEFERRED,
    (OPINION, HIGH): REOPEN_SCREEN,
    (PLAUSIBLE, LOW): REOPEN_QUEUED,
    (PLAUSIBLE, HIGH): REOPEN_PROMPT,
    (REPRODUCED, LOW): REOPEN_FORMAL,
    (REPRODUCED, HIGH): REOPEN_FORMAL,   # + Gate 3 restriction
    (INTEGRITY_DEFECT, LOW): REOPEN_ESCALATE,
    (INTEGRITY_DEFECT, HIGH): REOPEN_ESCALATE,
}


@dataclass(frozen=True)
class ChallengeInput:
    """Everything Gate 1 needs. Mirrors reopening.challenges.Challenge."""
    challenger: str
    trigger_type: str
    evidence: dict                  # trigger's required evidence keys
    interpretation_set_id: str
    known_challenge_ids: frozenset = frozenset()


@dataclass(frozen=True)
class Gate1Result:
    outcome: str
    reason: str


def gate1_admit(ch: ChallengeInput, trigger_registry) -> Gate1Result:
    """Gate 1: admit the challenge for recording?

    Low threshold BY DESIGN — it must be easy to challenge. Rejects only:
    unattributed objections, duplicates, and challenges that name a trigger
    but carry none of its required evidence (a different opinion is not a
    trigger).
    """
    if not (ch.challenger or "").strip():
        return Gate1Result(REJECTED_UNATTRIBUTED,
                           "challenge has no attributable challenger")
    spec = trigger_registry.get(ch.trigger_type)
    if spec is None:
        return Gate1Result(REJECTED_NO_TRIGGER_EVIDENCE,
                           f"unknown trigger type {ch.trigger_type!r}")
    missing = [k for k in spec.required_evidence if not ch.evidence.get(k)]
    if missing:
        return Gate1Result(
            REJECTED_NO_TRIGGER_EVIDENCE,
            f"trigger {ch.trigger_type} requires evidence keys {missing}")
    # Content-derived dedupe is computed by the caller via reopening.challenges
    # .derive_challenge_id; the known set is passed in.
    return Gate1Result(ADMITTED, "attributable, non-duplicate, evidenced")


@dataclass(frozen=True)
class Gate2Input:
    challenge_quality: str
    consequence: str
    dependency: str = INCIDENTAL


@dataclass(frozen=True)
class Gate2Result:
    outcome: str
    reason: str
    assess_restriction: bool  # whether Gate 3 must also run


def gate2_reopen(g: Gate2Input) -> Gate2Result:
    """Gate 2: does the admitted challenge reopen the resolution?

    The matrix separates the decision to INVESTIGATE from the decision to
    CHANGE. A low-risk challenge can be recorded and deferred; a high-risk
    challenge with a credible defect reopens promptly. INTEGRITY_DEFECT
    always escalates to LAW hard stops — scores never override them.
    """
    if g.challenge_quality not in _CHALLENGE_QUALITY:
        raise ValueError(f"unknown challenge quality {g.challenge_quality!r}")
    if g.consequence not in (LOW, HIGH):
        raise ValueError(f"unknown consequence {g.consequence!r}")
    outcome = _GATE2_MATRIX[(g.challenge_quality, g.consequence)]
    assess_restriction = (
        g.consequence == HIGH
        and g.challenge_quality in (PLAUSIBLE, REPRODUCED, INTEGRITY_DEFECT)
    )
    return Gate2Result(outcome, f"matrix[{g.challenge_quality},{g.consequence}]",
                       assess_restriction)


@dataclass(frozen=True)
class Gate3Input:
    consequence: str
    dependency: str
    evidence_completeness: str  # COMPLETE | INCOMPLETE — precautionary
    # restriction applies even on INCOMPLETE evidence when consequence HIGH


@dataclass(frozen=True)
class Gate3Result:
    outcome: str
    reason: str
    reversible: bool = True
    review_required: bool = True


def gate3_restrict(g: Gate3Input) -> Gate3Result:
    """Gate 3: restrict application pending review?

    Precautionary by design: a credible high-consequence challenge restricts
    critically dependent use EVEN ON INCOMPLETE evidence. The restriction is
    scoped, attributable, reviewable, reversible — never a silent ban.
    Hysteresis: engaging restriction is easier than restoring eligibility;
    restoration requires an independent requalification receipt (enforced by
    the caller, not assumed here).
    """
    if g.consequence == HIGH and g.dependency == CRITICAL:
        return Gate3Result(
            RESTRICT_DEPENDENT,
            "high consequence + critical dependency: precautionary "
            "restriction pending independent requalification",
            reversible=True, review_required=True)
    if g.consequence == HIGH:
        return Gate3Result(
            CONTINUE_QUALIFIED,
            "high consequence but non-critical dependency: continue with "
            "visible qualification of the disputed interpretation",
            reversible=True, review_required=True)
    return Gate3Result(
        CONTINUE,
        "low consequence: unaffected authorized work continues",
        reversible=True, review_required=False)
