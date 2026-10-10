"""Idempotent challenge handling + the machine-readable reopening receipt.

The same challenge submitted twice creates ONE review incident, not two.
Challenge identity is content-derived: the same challenger, trigger,
evidence, and interpretation set always hash to the same challenge_id.

The reopening receipt is a versioned review event in the existing
provenance vocabulary: it references (never rewrites) the prior receipt.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .review import Challenge


def derive_challenge_id(challenger: str, trigger_type: str,
                        evidence_refs: tuple[str, ...],
                        interpretation_set_id: str) -> str:
    """Content-derived challenge identity. Deterministic: identical
    inputs always produce the identical id, so repeats deduplicate."""
    canonical = json.dumps({
        "challenger": challenger,
        "trigger_type": trigger_type,
        "evidence_refs": sorted(evidence_refs),
        "interpretation_set_id": interpretation_set_id,
    }, sort_keys=True, separators=(",", ":"))
    return "CH-" + hashlib.sha256(canonical.encode()).hexdigest()[:12]


def make_challenge(challenger: str, trigger_type: str,
                   evidence_refs: tuple[str, ...],
                   interpretation_set_id: str,
                   reasoning_defect: str | None,
                   submitted_at: str) -> Challenge:
    """Build a challenge with its derived id."""
    return Challenge(
        challenge_id=derive_challenge_id(
            challenger, trigger_type, evidence_refs, interpretation_set_id),
        interpretation_set_id=interpretation_set_id,
        trigger_type=trigger_type,
        evidence_refs=evidence_refs,
        reasoning_defect=reasoning_defect,
        challenger=challenger,
        submitted_at=submitted_at,
    )


@dataclass
class ChallengeRegistry:
    """Tracks admitted challenges. Repeat submissions of the same
    content-derived id are acknowledged, not re-registered."""
    seen: set[str] = field(default_factory=set)
    incidents: dict[str, str] = field(default_factory=dict)  # challenge_id -> review_id

    def register(self, challenge: Challenge, review_id: str) -> str:
        """Returns 'REGISTERED' on first sight, 'DUPLICATE' on repeat."""
        if challenge.challenge_id in self.seen:
            return "DUPLICATE"
        self.seen.add(challenge.challenge_id)
        self.incidents[challenge.challenge_id] = review_id
        return "REGISTERED"


@dataclass(frozen=True)
class ReopeningReceipt:
    """Machine-readable review event. Immutable. References the prior
    receipt; never rewrites it."""
    event_type: str            # always "INTERPRETATION_REOPENED"
    interpretation_set_id: str
    previous_resolution_id: str | None
    challenge_id: str
    trigger: str
    evidence_refs: tuple[str, ...]
    previous_policy_version: str
    current_policy_version: str
    affected_scope: tuple[str, ...]
    review_state: str
    application_policy: str    # CONTINUE | RESTRICT_DEPENDENT | SUSPEND
    new_resolution_id: str | None
    independent_verification: str  # PENDING | VERIFIED | FAILED


def issue_reopening_receipt(review_id: str, set_id: str,
                            previous_resolution_id: str | None,
                            challenge: Challenge,
                            previous_policy_version: str,
                            current_policy_version: str,
                            affected_scope: tuple[str, ...],
                            review_state: str,
                            application_policy: str) -> ReopeningReceipt:
    return ReopeningReceipt(
        event_type="INTERPRETATION_REOPENED",
        interpretation_set_id=set_id,
        previous_resolution_id=previous_resolution_id,
        challenge_id=challenge.challenge_id,
        trigger=challenge.trigger_type,
        evidence_refs=challenge.evidence_refs,
        previous_policy_version=previous_policy_version,
        current_policy_version=current_policy_version,
        affected_scope=affected_scope,
        review_state=review_state,
        application_policy=application_policy,
        new_resolution_id=None,
        independent_verification="PENDING",
    )
