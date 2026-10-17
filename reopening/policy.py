"""Policy versioning for resolutions.

The hard rule: a policy change reassesses FUTURE applicability; it does not
retroactively falsify history. A P1 receipt remains a valid record of what
was decided under P1. Whether the old interpretation may authorize action
NOW is judged under the current policy.

Each resolution records: resolved_at, source_version, policy_version,
evidence_cutoff, effective_scope, review_receipt, supersedes,
retroactivity_rule.

retroactivity_rule:
    "prospective" (default) — the new policy governs future uses only.
    "retroactive"           — the authoritative policy itself declares
                              retroactive effect. Never assumed.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PolicyVersion:
    version_id: str            # e.g. "P1", "P2"
    ratified_at: str
    ratified_by: str           # attributable authority (Shawn / LAW receipt)
    change_summary: str
    retroactive: bool = False  # only True when the policy itself declares it


@dataclass
class PolicyRegistry:
    """Ordered policy history. Current policy governs new assessments."""
    versions: list[PolicyVersion] = field(default_factory=list)

    def current(self) -> PolicyVersion:
        if not self.versions:
            raise ValueError("no policy versions registered")
        return self.versions[-1]

    def get(self, version_id: str) -> PolicyVersion:
        for v in self.versions:
            if v.version_id == version_id:
                return v
        raise ValueError(f"unknown policy version {version_id!r}")


def policy_transition_effect(old: PolicyVersion, new: PolicyVersion,
                             resolution_policy_version: str) -> str:
    """What a P_old -> P_new change means for a resolution issued under
    `resolution_policy_version`.

    - Resolution already under new policy: "UNAFFECTED".
    - New policy declares retroactive effect: "RETROACTIVE_REVIEW"
      (rare; only when the authoritative policy says so).
    - Otherwise: "REASSESS_APPLICABILITY" — history stands, current use
      needs requalification under the new policy.
    """
    if resolution_policy_version == new.version_id:
        return "UNAFFECTED"
    if new.retroactive:
        return "RETROACTIVE_REVIEW"
    return "REASSESS_APPLICABILITY"
