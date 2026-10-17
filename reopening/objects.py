"""The four objects of the reopening protocol.

Kept separate by design. Confusing them is how systems either freeze on old
answers or silently rewrite history. Each object has exactly one mutability
contract.

    SourceRecord            immutable   what was actually said/recorded
    InterpretationSet       versioned   plausible meanings + their evidence
    ResolutionReceipt       immutable   why THIS meaning won, at THIS time,
                                        under THIS policy
    ApplicabilityAssessment reassessed  can it guide THIS decision, NOW?
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 1. SourceRecord — IMMUTABLE. What was actually said or recorded.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceRecord:
    """The original source. Never mutated, never rewritten.

    A correction from the author is a NEW SourceRecord linked via
    `corrects_id` — the original stays exactly as captured.
    """
    source_id: str
    content_hash: str          # sha256 of the exact source bytes
    captured_at: str           # ISO-8601 UTC
    origin: str                # who/what produced it (identity-normalized)
    corrects_id: str | None = None  # set only on author corrections


def capture_source(source_id: str, content: str, origin: str,
                   captured_at: str,
                   corrects_id: str | None = None) -> SourceRecord:
    """Create an immutable source record. Frozen dataclass: any mutation
    attempt raises. Corrections link; they never edit."""
    return SourceRecord(
        source_id=source_id,
        content_hash=_sha256(content),
        captured_at=captured_at,
        origin=origin,
        corrects_id=corrects_id,
    )


# ---------------------------------------------------------------------------
# 2. InterpretationSet — VERSIONED. Plausible meanings and their evidence.
# ---------------------------------------------------------------------------

@dataclass
class Interpretation:
    """One plausible meaning of the source."""
    interpretation_id: str
    meaning: str                      # the asserted meaning, in plain words
    supporting_evidence: list[str] = field(default_factory=list)  # evidence_refs
    scope: str = ""                   # where/when this meaning applies
    submitted_by: str = ""            # attributable challenger or resolver


@dataclass
class InterpretationSet:
    """The set of plausible meanings for one source, at one version.

    New meanings do not edit old versions — they create a new version.
    Every version keeps its full history.
    """
    set_id: str
    source_id: str
    version: int
    interpretations: list[Interpretation] = field(default_factory=list)
    created_at: str = ""
    created_by: str = ""
    supersedes_version: int | None = None


def new_interpretation_version(previous: InterpretationSet,
                               new_meanings: list[Interpretation],
                               created_at: str,
                               created_by: str) -> InterpretationSet:
    """A successor challenge or new evidence produces a NEW version.
    The previous version is preserved untouched."""
    return InterpretationSet(
        set_id=previous.set_id,
        source_id=previous.source_id,
        version=previous.version + 1,
        interpretations=list(previous.interpretations) + list(new_meanings),
        created_at=created_at,
        created_by=created_by,
        supersedes_version=previous.version,
    )


# ---------------------------------------------------------------------------
# 3. ResolutionReceipt — IMMUTABLE. Why this interpretation won.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ResolutionReceipt:
    """The decision record for one resolution. Immutable.

    Records WHY a particular interpretation was selected AT a particular
    time UNDER a particular policy WITH a particular evidence cutoff.
    A later policy change does not edit this receipt — it triggers a
    reassessment of current applicability (see ApplicabilityAssessment).
    """
    receipt_id: str
    interpretation_set_id: str
    set_version: int
    chosen_interpretation_id: str
    rationale: str                     # why it won, in plain words
    resolved_at: str                   # ISO-8601 UTC
    source_version: str                # which source text was interpreted
    policy_version: str                # which rules governed the decision
    evidence_cutoff: str               # what supporting material was available
    effective_scope: str               # where/when the interpretation applied
    reviewer: str                      # who/what independently qualified it
    retroactivity_rule: str = "prospective"  # "prospective" | "retroactive"
    supersedes_receipt_id: str | None = None


def issue_resolution(receipt_id: str, interp_set: InterpretationSet,
                     chosen_id: str, rationale: str, resolved_at: str,
                     source_version: str, policy_version: str,
                     evidence_cutoff: str, effective_scope: str,
                     reviewer: str,
                     retroactivity_rule: str = "prospective",
                     supersedes_receipt_id: str | None = None) -> ResolutionReceipt:
    """Issue an immutable resolution receipt. The chosen interpretation
    must exist in the set version being resolved."""
    ids = {i.interpretation_id for i in interp_set.interpretations}
    if chosen_id not in ids:
        raise ValueError(f"chosen interpretation {chosen_id!r} not in set "
                         f"{interp_set.set_id} v{interp_set.version}")
    if retroactivity_rule not in ("prospective", "retroactive"):
        raise ValueError("retroactivity_rule must be prospective|retroactive")
    return ResolutionReceipt(
        receipt_id=receipt_id,
        interpretation_set_id=interp_set.set_id,
        set_version=interp_set.version,
        chosen_interpretation_id=chosen_id,
        rationale=rationale,
        resolved_at=resolved_at,
        source_version=source_version,
        policy_version=policy_version,
        evidence_cutoff=evidence_cutoff,
        effective_scope=effective_scope,
        reviewer=reviewer,
        retroactivity_rule=retroactivity_rule,
        supersedes_receipt_id=supersedes_receipt_id,
    )


# ---------------------------------------------------------------------------
# 4. ApplicabilityAssessment — REASSESSED. Can it guide THIS decision now?
# ---------------------------------------------------------------------------

@dataclass
class ApplicabilityAssessment:
    """Whether a resolution may guide a specific current decision.

    Reassessed per decision context — a P1 resolution can be historically
    valid yet inapplicable under P2. The resolution receipt is never edited;
    only this assessment changes.
    """
    assessment_id: str
    resolution_receipt_id: str
    decision_context: str              # the specific decision being gated
    eligible: bool
    restrictions: list[str] = field(default_factory=list)
    assessed_at: str = ""
    policy_version: str = ""           # policy governing THIS assessment
    reason: str = ""


def assess_applicability(assessment_id: str, receipt: ResolutionReceipt,
                         decision_context: str, assessed_at: str,
                         current_policy_version: str) -> ApplicabilityAssessment:
    """Reassess a resolution against the CURRENT policy.

    Rule: a resolution issued under an older policy keeps its historical
    receipt, but its current applicability is judged under the current
    policy. Policy mismatch alone does not falsify history — it narrows
    what the old resolution may authorize now.
    """
    if receipt.policy_version == current_policy_version:
        return ApplicabilityAssessment(
            assessment_id=assessment_id,
            resolution_receipt_id=receipt.receipt_id,
            decision_context=decision_context,
            eligible=True,
            assessed_at=assessed_at,
            policy_version=current_policy_version,
            reason="resolution policy matches current policy",
        )
    return ApplicabilityAssessment(
        assessment_id=assessment_id,
        resolution_receipt_id=receipt.receipt_id,
        decision_context=decision_context,
        eligible=False,
        restrictions=["POLICY_VERSION_MISMATCH: requalification required "
                      f"under {current_policy_version}"],
        assessed_at=assessed_at,
        policy_version=current_policy_version,
        reason=(f"resolved under {receipt.policy_version}; current policy "
                f"is {current_policy_version}; historical receipt preserved, "
                "current applicability withheld pending requalification"),
    )
