"""The five-state review machine + the risk-based three decisions.

States (layered on truth states, not competing with them):

    RESOLVED    one interpretation has sufficient recorded support
    CHALLENGED  an attributable objection with evidence is registered.
                Eligibility UNCHANGED — a challenge alone revokes nothing.
    REOPENED    the objection met the reassessment threshold. Risk-based
                containment applies ONLY to materially dependent uses.
    REQUALIFIED a new receipt is issued (uphold / replace / narrow).
                Supersedes the prior receipt; history preserved.
    UNRESOLVED  evidence insufficient for one interpretation. Consequential
                use HELD; everything preserved; review stays open.

The three risk-based decisions (separate questions, separate answers):

    1. ADMIT the challenge?   concrete, non-duplicate, evidenced basis?
    2. CONTAIN the usage?     could continued reliance cause material harm?
    3. REQUALIFY the meaning? old meaning / new meaning / no single meaning?

Reopening never grants permission to change production, delete evidence,
or override LAW. It only changes what a resolution may authorize.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .objects import ResolutionReceipt, issue_resolution, InterpretationSet


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------

RESOLVED = "RESOLVED"
CHALLENGED = "CHALLENGED"
REOPENED = "REOPENED"
REQUALIFIED = "REQUALIFIED"
UNRESOLVED = "UNRESOLVED"

_REVIEW_STATES = (RESOLVED, CHALLENGED, REOPENED, REQUALIFIED, UNRESOLVED)

# Legal transitions. Note: CHALLENGED never jumps to REQUALIFIED (a
# challenge must pass the reopen threshold first), and UNRESOLVED can
# return to REOPENED when new evidence arrives (never silently to RESOLVED).
_TRANSITIONS = {
    RESOLVED: (CHALLENGED,),
    CHALLENGED: (REOPENED, RESOLVED),      # dismissed -> back to RESOLVED
    REOPENED: (REQUALIFIED, UNRESOLVED),
    REQUALIFIED: (CHALLENGED,),            # new challenge starts a new cycle
    UNRESOLVED: (REOPENED,),
}


class ReviewError(ValueError):
    """Illegal review-state transition or malformed review."""


@dataclass
class Review:
    """One review incident for one interpretation set."""
    review_id: str
    interpretation_set_id: str
    state: str = RESOLVED
    resolution_receipt_id: str | None = None
    challenge_ids: list[str] = field(default_factory=list)
    containment: str = "NONE"            # NONE | RESTRICT_DEPENDENT | SUSPEND
    history: list[tuple[str, str, str]] = field(default_factory=list)
    # (from_state, to_state, reason) — append-only audit trail


def transition(review: Review, to_state: str, reason: str) -> Review:
    """Move a review between states. Illegal transitions raise — the
    machine cannot be shortcut (no CHALLENGED -> REQUALIFIED)."""
    if to_state not in _REVIEW_STATES:
        raise ReviewError(f"unknown review state {to_state!r}")
    if to_state not in _TRANSITIONS[review.state]:
        raise ReviewError(
            f"illegal transition {review.state} -> {to_state}: {reason}")
    review.history.append((review.state, to_state, reason))
    review.state = to_state
    return review


# ---------------------------------------------------------------------------
# Decision 1: ADMIT the challenge?
# ---------------------------------------------------------------------------

ADMITTED = "ADMITTED"
DUPLICATE = "DUPLICATE"
INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class Challenge:
    """A challenge must carry evidence or a reproducible reasoning defect.
    A different opinion, unattributed, is not a challenge."""
    challenge_id: str
    interpretation_set_id: str
    trigger_type: str
    evidence_refs: tuple[str, ...]
    reasoning_defect: str | None      # reproducible defect description, or None
    challenger: str                   # attributable identity
    submitted_at: str


def admit_challenge(challenge: Challenge,
                    seen_challenge_ids: set[str]) -> str:
    """Decision 1: is there a concrete, non-duplicate, evidenced basis?

    DUPLICATE: same challenge seen before (idempotent — one incident).
    INSUFFICIENT: no evidence refs AND no reproducible reasoning defect,
                  or no attributable challenger.
    ADMITTED: otherwise.
    """
    if challenge.challenge_id in seen_challenge_ids:
        return DUPLICATE
    if not challenge.challenger:
        return INSUFFICIENT
    if not challenge.evidence_refs and not challenge.reasoning_defect:
        return INSUFFICIENT
    return ADMITTED


# ---------------------------------------------------------------------------
# Decision 2: CONTAIN the usage?
# ---------------------------------------------------------------------------

CONTINUE = "CONTINUE"                    # no material harm plausibly follows
RESTRICT_DEPENDENT = "RESTRICT_DEPENDENT"  # block materially dependent uses
SUSPEND = "SUSPEND"                      # halt the affected path, escalate


def determine_containment(challenge: Challenge,
                          material_harm_plausible: bool,
                          sole_authority_premise: bool) -> str:
    """Decision 2: could continued reliance cause material harm?

    - No plausible material harm -> CONTINUE (low-risk uses stay visible
      but qualified during review).
    - Plausible harm, alternative support exists -> RESTRICT_DEPENDENT
      (only materially dependent uses blocked; independent work continues).
    - The disputed interpretation is the SOLE authority premise for a
      consequential action -> SUSPEND that action path, escalate via LAW.
    """
    if sole_authority_premise:
        return SUSPEND
    if material_harm_plausible:
        return RESTRICT_DEPENDENT
    return CONTINUE


# ---------------------------------------------------------------------------
# Decision 3: REQUALIFY the meaning?
# ---------------------------------------------------------------------------

UPHELD = "UPHELD"        # old meaning stands; new receipt confirms
REPLACED = "REPLACED"    # a different meaning now wins
NARROWED = "NARROWED"    # old meaning holds only in reduced scope
NO_SINGLE = "NO_SINGLE"  # evidence supports no single meaning -> UNRESOLVED


def requalify(review: Review, interp_set: InterpretationSet,
              outcome: str, chosen_id: str | None,
              rationale: str, resolved_at: str,
              source_version: str, policy_version: str,
              evidence_cutoff: str, effective_scope: str,
              reviewer: str) -> tuple[Review, ResolutionReceipt | None]:
    """Decision 3: does the new total evidence support the old meaning,
    a different meaning, or no single meaning?

    UPHELD/REPLACED/NARROWED -> REQUALIFIED with a NEW immutable receipt
    that supersedes the prior one (history preserved, never rewritten).
    NO_SINGLE -> UNRESOLVED (hold consequential use; review stays open).
    """
    if review.state != REOPENED:
        raise ReviewError("requalification requires REOPENED state")
    if outcome not in (UPHELD, REPLACED, NARROWED, NO_SINGLE):
        raise ReviewError(f"unknown requalification outcome {outcome!r}")
    if outcome == NO_SINGLE:
        transition(review, UNRESOLVED,
                   "evidence supports no single interpretation; held")
        return review, None
    if not chosen_id:
        raise ReviewError("UPHELD/REPLACED/NARROWED require a chosen interpretation")
    prior_receipt = review.resolution_receipt_id
    receipt = issue_resolution(
        receipt_id=f"RES-{review.review_id}-{interp_set.version}",
        interp_set=interp_set,
        chosen_id=chosen_id,
        rationale=rationale,
        resolved_at=resolved_at,
        source_version=source_version,
        policy_version=policy_version,
        evidence_cutoff=evidence_cutoff,
        effective_scope=effective_scope if outcome != NARROWED else effective_scope,
        reviewer=reviewer,
        supersedes_receipt_id=prior_receipt,
    )
    review.resolution_receipt_id = receipt.receipt_id
    transition(review, REQUALIFIED, f"{outcome}: {rationale}")
    return review, receipt
