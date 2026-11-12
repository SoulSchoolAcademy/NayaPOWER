"""Calibration identity: bind every reopening/eligibility decision to the exact
conditions under which it was qualified.

A changed fingerprint triggers an impact assessment — not an automatic rollback.
The fingerprint covers more than software versions: rubric, feature definitions,
source eligibility rules, review-selection mechanism, authorization policy.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict


@dataclass(frozen=True)
class CalibrationFingerprint:
    """Immutable identity of the conditions behind a calibration decision."""
    policy_version: str          # ratified policy version + SHA
    policy_sha: str
    model_version: str           # model + prompt versions
    prompt_version: str
    verifier_id: str             # reviewer identity
    rubric_version: str          # evaluation rubric version
    runtime_version: str         # runtime/tools commit SHA
    corpus_id: str               # evidence corpus identifier
    corpus_hash: str             # sha256 of the corpus snapshot
    evidence_cutoff: str         # ISO timestamp: newest evidence admitted
    calibration_dataset: str     # dataset id + version used for calibration
    calibration_params_hash: str # sha256 of the parameter set

    def digest(self) -> str:
        canonical = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def changed_fields(self, other: "CalibrationFingerprint") -> tuple[str, ...]:
        """Which fields differ — a changed fingerprint triggers impact assessment."""
        a, b = asdict(self), asdict(other)
        return tuple(k for k in a if a[k] != b[k])


# Drift types are SEPARATE signals. Never collapse into one composite score —
# a composite can hide a catastrophic miss behind excellent average accuracy.
DRIFT_TYPES = (
    "policy",       # governing requirements changed
    "model",        # model/prompt update changed classification behavior
    "reviewer",     # verifiers changed standards or share new biases
    "environment",  # runtime, retrieval corpus, or schema changed
    "outcome",      # previously reliable thresholds miss new errors
    "population",   # the kinds of challenges arriving have changed
)


@dataclass
class DriftSignal:
    """One typed drift observation. Never a bare number without context."""
    drift_type: str              # one of DRIFT_TYPES
    indicator: str               # which of the ten indicators fired
    observed_at: str             # ISO timestamp
    baseline_fingerprint: str    # fingerprint digest this signal is measured against
    current_fingerprint: str     # fingerprint digest at observation time
    evidence_ref: str            # receipt/artifact backing the signal
    severity_hint: str = "watch" # watch | investigate | contain (advisory only)

    def __post_init__(self):
        assert self.drift_type in DRIFT_TYPES, f"unknown drift type {self.drift_type}"
