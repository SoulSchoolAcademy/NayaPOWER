"""Meaning-preserving atomic claim extraction — claim model.

Governing rule: atomic does not mean short. Atomic means independently
evaluable, with every qualifier necessary to determine truth preserved.

A Claim is two inseparable parts:
- nucleus: the particular proposition being asserted.
- meaning envelope: the context/constraints determining when it is true.

Spec only — not wired into production retrieval paths.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


# --- Meaning envelope dimensions (Shawn's 8, 2026-10-10) -------------------

POLARITIES = ("POSITIVE", "NEGATIVE")
MODALITIES = ("OBSERVED", "POSSIBLE", "NECESSARY", "CONDITIONAL", "PERMITTED", "REPORTED")
EPISTEMIC_STATES = ("REPORTED", "OBSERVED", "INFERRED", "UNPROVEN")


@dataclass(frozen=True)
class MeaningEnvelope:
    """Every qualifier necessary to determine the truth of the nucleus.

    All fields default to the least committal value that preserves the
    source meaning — the extractor must EARN each specific value from
    explicit source text, never assume it.
    """
    polarity: str = "POSITIVE"          # POSITIVE | NEGATIVE
    quantifier: str = "UNSPECIFIED"      # e.g. "all", "3-of-5", "not-all", "UNSPECIFIED"
    scope: str = "UNSPECIFIED"          # domain the claim is asserted over
    time_relation: str = "UNSPECIFIED"  # e.g. AFTER(x,y), BEFORE(x,y), AT(t)
    condition: str = "NONE"             # gating condition, or NONE
    exceptions: tuple = ()              # explicit carve-outs
    modality: str = "OBSERVED"          # OBSERVED|POSSIBLE|NECESSARY|CONDITIONAL|PERMITTED|REPORTED
    attribution: str = "NONE"           # who reported it, or NONE (= own observation)
    epistemic: str = "OBSERVED"         # REPORTED|OBSERVED|INFERRED|UNPROVEN

    def __post_init__(self):
        assert self.polarity in POLARITIES, self.polarity
        assert self.modality in MODALITIES, self.modality
        assert self.epistemic in EPISTEMIC_STATES, self.epistemic


@dataclass(frozen=True)
class Claim:
    """One atomic, independently evaluable proposition + its meaning envelope."""
    claim_id: str
    parent_source_id: str
    source_content_hash: str            # sha256 of the exact source bytes
    text_span: tuple                    # (start, end) offsets into source
    nucleus: str                        # the proposition, plain words
    envelope: MeaningEnvelope = field(default_factory=MeaningEnvelope)
    relations: tuple = ()               # ((edge, target_claim_id), ...)

    @staticmethod
    def content_hash(source_text: str) -> str:
        return hashlib.sha256(source_text.encode("utf-8")).hexdigest()


# --- Claim record (machine-readable manifest) --------------------------------

def claim_record(claim: Claim, *, extraction_version: str,
                 faithfulness: str = "PENDING",
                 verdict: str = "CANDIDATE",
                 application: str = "REVIEW_REQUIRED") -> dict:
    """The canonical manifest for one extracted claim."""
    return {
        "claim_id": claim.claim_id,
        "parent_source_id": claim.parent_source_id,
        "source_content_hash": claim.source_content_hash,
        "text_span": list(claim.text_span),
        "nucleus": claim.nucleus,
        "meaning_envelope": {
            "polarity": claim.envelope.polarity,
            "quantifier": claim.envelope.quantifier,
            "scope": claim.envelope.scope,
            "time_relation": claim.envelope.time_relation,
            "condition": claim.envelope.condition,
            "exceptions": list(claim.envelope.exceptions),
            "modality": claim.envelope.modality,
            "attribution": claim.envelope.attribution,
            "epistemic": claim.envelope.epistemic,
        },
        "relations": [{"edge": e, "target": t} for e, t in claim.relations],
        "extraction": {"version": extraction_version, "faithfulness": faithfulness},
        "truth": {"verdict": verdict, "application": application},
    }
