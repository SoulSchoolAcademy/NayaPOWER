"""Canary run receipt — minimum machine-readable record for every canary run.

Protect sensitive model/reviewer/corpus metadata as appropriate. A hash gives
integrity binding, not confidentiality, and not proof of evaluator independence.
For random samples also preserve sampling frame, inclusion probability, and
nonresponse status (essential for bias-adjusted estimates).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json


@dataclass(frozen=True)
class CanaryReceipt:
    run_id: str
    set_type: str            # fixed | rolling | adversarial
    visibility: str          # open | sealed
    corpus_version: str
    corpus_hash: str         # sha256 of the corpus bundle
    sample_family_id: str
    policy_version: str      # policy SHA governing the run
    model_version: str
    runtime_version: str     # commit SHA under evaluation
    evaluation_cutoff: str   # ISO timestamp: newest evidence admitted
    reviewer_id: str         # independent reviewer (sealed) or "self" (open)
    outcome: str = "PENDING" # PENDING | PASS | FAIL | COMPROMISED
    leakage_check: str = "PENDING"  # PENDING | PASS | FAIL
    evidence_receipt: str | None = None
    # random-sample extras (empty for fixed sets)
    sampling_frame: str = ""
    inclusion_probability: str = ""
    nonresponse_status: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=1)

    def compromised(self) -> "CanaryReceipt":
        """Firewall breach: preserve history, mark compromised, never promote."""
        from dataclasses import replace
        return replace(self, outcome="COMPROMISED",
                       evidence_receipt=(self.evidence_receipt or "")
                       + "; firewall breach recorded; replaced by fresh "
                         "lineage-disjoint holdout; not usable for promotion")
