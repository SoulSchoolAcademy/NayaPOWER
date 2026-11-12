"""Three-layer canary system + evaluation firewall (spec).

Layers (complementary, not interchangeable):
  FIXED       — frozen regression memory. Known failure modes + critical rules,
                run unchanged across qualified releases.
  ROLLING     — reality awareness. Continuously refreshed representative sample
                of current challenges, environments, policies, reviewers.
  ADVERSARIAL — unknown-weakness discovery. Independently developed red-team
                cases: loopholes, correlated evidence, answer leakage,
                authority confusion, new attack strategies.

Visibility classes:
  OPEN   — workers may access cases AND expected results. For development,
           debugging, preventing known regressions. Once a test has directly
           influenced development it must NOT be treated as blind assessment.
  SEALED — evaluation service + authorized independent reviewers ONLY.
           Answer keys hidden. Measures generalization and honest improvement.

SEALED fixtures live OUTSIDE this repository by law. Only SHA-256 commitments
may appear here. (Precedent: QUAL-20261010-CIQ-001 sealed key, 2026-10-10.)
"""
from __future__ import annotations

from dataclasses import dataclass, field

LAYERS = ("fixed", "rolling", "adversarial")
VISIBILITY = ("open", "sealed")

# The ten canary families. Each needs: positive control, negative control,
# adversarial variation, explicit source-of-truth reference.
CANARY_FAMILIES = (
    "negation_scope",            # meaning changes during claim extraction
    "ambiguous_authority",       # uncertainty creating unauthorized permission
    "circular_evidence",         # self-generated agreement as fake proof
    "mixed_validity",            # good claims surviving alongside contaminated ones
    "independent_corroboration", # derivative sources counted as independent
    "interpretation_reopening",  # genuine contradictory evidence reopens decisions
    "risk_quarantine",           # dangerous use stops while safe work continues
    "policy_model_drift",        # outdated qualification detected
    "concurrent_eligibility",    # ACT refuses newly quarantined dependency
    "cold_successor_transfer",   # fresh Naya preserves understanding + boundaries
)


@dataclass(frozen=True)
class CanaryCase:
    """One canary fixture (OPEN visibility — safe to ship in-repo)."""
    case_id: str
    family: str                  # one of CANARY_FAMILIES
    layer: str                   # fixed | rolling | adversarial
    visibility: str = "open"
    source_family: str = ""      # lineage family for disjoint-split enforcement
    positive_control: str = ""   # what must PASS
    negative_control: str = ""   # what must FAIL / be refused
    adversarial_variation: str = ""
    truth_reference: str = ""    # explicit source-of-truth reference
    retired: bool = False        # retired holdouts keep history, leave blind sets

    def __post_init__(self):
        assert self.family in CANARY_FAMILIES
        assert self.layer in LAYERS
        assert self.visibility in VISIBILITY


@dataclass(frozen=True)
class SealedCommitment:
    """In-repo commitment to a SEALED fixture held outside the repo.
    The evaluated worker sees the commitment, never the answers."""
    case_id: str
    family: str
    corpus_version: str
    sha256: str                  # hash of the sealed fixture bundle
    holder: str                  # evaluation service identity (not the builder)


# --- Evaluation firewall (machine-enforceable rules) ---
FIREWALL_RULES = (
    "evaluated worker receives: task + information legitimately available at "
    "decision time. NOTHING ELSE.",
    "no sealed answers, hidden rubrics, future outcomes, or evaluator internal "
    "reasoning may reach the evaluated worker.",
    "independent evaluator returns TWO outputs: (1) detailed access-controlled "
    "receipt to governance/proof; (2) bounded approved feedback package to "
    "learning (failure category, principles, safe direction — NO sealed answers).",
    "feedback must not allow the builder to infer hidden answer keys through "
    "repeated detailed failure reports.",
    "if the confidentiality boundary fails: mark evaluation COMPROMISED, "
    "preserve the historical result, replace with a fresh lineage-disjoint "
    "holdout. NEVER promote from compromised tests.",
)


# --- Tiered schedule: cheap checks often, expensive reviews on changes ---
TIERED_SCHEDULE = (
    ("relevant code/schema/policy change", "targeted fixed canaries"),
    ("model or evaluator change", "anchor replay + sealed comparison"),
    ("routine monitoring interval", "stratified rolling sample"),
    ("new serious incident or attack class", "adversarial expansion"),
    ("before consequential promotion", "fixed + representative + sealed qualification"),
    ("after deployment, when authorized", "outcome monitoring + successor checks"),
)
