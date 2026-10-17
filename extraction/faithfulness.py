"""Faithfulness gate: forward entailment + coverage.

Three complementary evaluations (Shawn's framework):
1. Forward entailment: does the source support every extracted proposition,
   including its qualifiers?
2. Coverage: does the claim set preserve all decision-relevant meaning?
   (A gate that passes by extracting only the easy parts is a lie.)
3. Reconstruction challenge: would flipping a qualifier change the verdict?
   (Implemented as the adversarial corpus — the gate must reject every
   DISTORTED fixture.)

Fail-closed: a materially unfaithful or ambiguous claim gets
faithfulness=REJECTED and may not be used consequentially.
"""
from __future__ import annotations

from .claim import Claim


# Qualifier tokens that, if present in source but absent from the claim's
# envelope/nucleus, constitute a coverage failure.
_COVERAGE_MARKERS = {
    "negation": ["not", "never", "no ", "n't", "without", "none"],
    "scope": ["only", "all ", "every ", "three of five", "not all"],
    "condition": ["if ", "when ", "unless ", "provided "],
    "exception": ["except", "other than"],
    "modality": ["may ", "might ", "could ", "must ", "necessarily "],
    "attribution": ["claims", "reported", "according to", "says"],
    "temporal": ["after ", "before "],
}


def _norm(s: str) -> str:
    return " " + s.lower() + " "


def forward_entailment(source_text: str, claim: Claim) -> tuple:
    """Check the source supports the claim's nucleus + envelope.

    Returns (passes: bool, reasons: list). Conservative: any qualifier in
    the envelope that cannot be grounded in the source span fails.
    """
    reasons = []
    span_text = source_text[claim.text_span[0]:claim.text_span[1]]
    norm_span = _norm(span_text)
    env = claim.envelope

    # The nucleus must be substantially present in its own span
    nucleus_words = [w for w in claim.nucleus.lower().split() if len(w) > 3]
    if nucleus_words:
        hit = sum(1 for w in nucleus_words if w.strip(".,;:!?\"'") in norm_span)
        if hit / len(nucleus_words) < 0.5:
            reasons.append("NUCLEUS_NOT_GROUNDED_IN_SPAN")

    # Envelope qualifiers must be earned from the span text
    if env.polarity == "NEGATIVE" and not any(
            m.strip() in norm_span for m in _COVERAGE_MARKERS["negation"]):
        reasons.append("NEGATION_UNGROUNDED")
    if env.condition != "NONE" and not any(
            m.strip() in norm_span for m in _COVERAGE_MARKERS["condition"]):
        reasons.append("CONDITION_UNGROUNDED")
    if env.exceptions and not any(
            m.strip() in norm_span for m in _COVERAGE_MARKERS["exception"]):
        reasons.append("EXCEPTION_UNGROUNDED")
    if env.attribution != "NONE" and not any(
            m.strip() in norm_span for m in _COVERAGE_MARKERS["attribution"]):
        reasons.append("ATTRIBUTION_UNGROUNDED")
    if env.time_relation != "UNSPECIFIED" and not any(
            m.strip() in norm_span for m in _COVERAGE_MARKERS["temporal"]):
        reasons.append("TEMPORAL_UNGROUNDED")

    return (len(reasons) == 0, reasons)


def coverage_check(source_text: str, claims: list) -> tuple:
    """Check the claim set preserves decision-relevant meaning.

    Fails when a qualifier marker appears in the source but in NO claim's
    envelope or nucleus — meaning the extraction silently dropped it.
    """
    norm_src = _norm(source_text)
    # Union of what the claims preserve. Markers carry their own word
    # boundaries (leading/trailing spaces) — never strip them, or "no"
    # false-matches inside "not".
    preserved = set()
    for c in claims:
        blob = _norm(c.nucleus + " " + " ".join([
            c.envelope.polarity, c.envelope.quantifier, c.envelope.scope,
            c.envelope.time_relation, c.envelope.condition,
            " ".join(c.envelope.exceptions), c.envelope.modality,
            c.envelope.attribution, c.envelope.epistemic,
        ]))
        for dim, markers in _COVERAGE_MARKERS.items():
            for m in markers:
                if m in blob:
                    preserved.add((dim, m))
    missing = []
    for dim, markers in _COVERAGE_MARKERS.items():
        for m in markers:
            if m in norm_src and (dim, m) not in preserved:
                missing.append(f"{dim}:{m.strip()}")
    return (len(missing) == 0, missing)


def gate_claim(source_text: str, claim: Claim, all_claims: list) -> dict:
    """Run the full faithfulness gate on one claim.

    Returns a verdict dict. faithfulness is one of
    FAITHFUL | REJECTED | NEEDS_REVIEW.
    """
    ent_ok, ent_reasons = forward_entailment(source_text, claim)
    cov_ok, cov_missing = coverage_check(source_text, all_claims)

    if not ent_ok:
        verdict = "REJECTED"
    elif not cov_ok:
        # Coverage is a set-level property: flag review, don't silently pass
        verdict = "NEEDS_REVIEW"
    else:
        verdict = "FAITHFUL"

    return {
        "claim_id": claim.claim_id,
        "faithfulness": verdict,
        "entailment": {"passes": ent_ok, "reasons": ent_reasons},
        "coverage": {"passes": cov_ok, "missing": cov_missing},
        "consequential_use_allowed": verdict == "FAITHFUL",
    }
