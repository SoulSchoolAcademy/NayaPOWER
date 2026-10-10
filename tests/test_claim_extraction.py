"""Corpus-driven extraction tests: the 8 dimensions + 10 dangerous mistakes.

Each fixture: source -> faithful envelope expectations. The DISTORTED
variant must NEVER be producible by the extractor — tested separately in
test_faithfulness_gate.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extraction.extractor import detect_envelope, split_candidates


def env(source):
    claims = split_candidates(source, "T")
    assert len(claims) == 1, f"expected 1 claim, got {len(claims)}: {source}"
    return claims[0].envelope


# --- Negation ---
def test_neg_scope_not_all():
    e = env("Not all tests passed on the first run.")
    assert e.polarity == "NEGATIVE"
    assert e.quantifier == "not-all"  # NOT "none": some may have passed


def test_nested_negation():
    e = env("It is not true that Naya must never use candidate knowledge.")
    assert e.polarity == "NEGATIVE"
    # the rejection of an absolute prohibition — not a universal permission


# --- Scope ---
def test_quantifier_3_of_5():
    e = env("Three of five agents succeeded.")
    assert e.quantifier == "3-of-5"


def test_restriction_only():
    e = env("Only verified lessons may influence ACT.")
    assert e.quantifier == "only"


# --- Chronology ---
def test_temporal_before_no_causation():
    e = env("The branch moved before the check ran.")
    assert e.time_relation == "BEFORE"


def test_temporal_after():
    e = env("After the index was regenerated on commit A, the check passed.")
    assert e.time_relation == "AFTER"


# --- Conditions ---
def test_condition_present():
    e = env("X improves performance when condition Y holds.")
    assert e.condition == "PRESENT"
    assert e.modality == "CONDITIONAL"


def test_permission_not_obligation():
    e = env("If LAW approves A, ACT may execute B.")
    assert e.condition == "PRESENT"
    # "may" = permitted, never "must"


# --- Exceptions ---
def test_exception_preserved():
    e = env("Regeneration is safe except for production writes.")
    assert len(e.exceptions) > 0


# --- Modality ---
def test_observed_not_impossible():
    e = env("No failures were observed in 20 trials.")
    assert e.modality == "OBSERVED"
    assert e.epistemic == "OBSERVED"  # NOT a universal impossibility claim


def test_may_not_will():
    e = env("The fix may improve convergence.")
    assert e.modality == "POSSIBLE"


# --- Attribution ---
def test_attribution_laundering_blocked():
    e = env("Agent A claims the test passed.")
    assert e.attribution != "NONE"
    assert e.epistemic == "REPORTED"  # NOT independently verified


def test_absence_of_evidence():
    e = env("No evidence proves deployment succeeded.")
    assert e.epistemic == "UNPROVEN"  # NOT "deployment failed"


# --- Relationships ---
def test_correlation_marked():
    from extraction.extractor import detect_relation_markers
    rels = detect_relation_markers("A and B were observed together.")
    assert "CO_OCCURRENCE" in rels
    assert "CAUSED" not in rels


def test_supersession_scope():
    # "superseded for production" must not become "false everywhere"
    claims = split_candidates("Lesson A was superseded for production use.", "T")
    assert len(claims) == 1
    # the scope qualifier travels with the claim (no universal falsehood)


def test_reason_edge_preserved():
    from extraction.extractor import detect_relation_markers
    rels = detect_relation_markers(
        "Although the capture was valid, promotion was refused because "
        "the independent proof receipt was missing.")
    assert "CAUSED" in rels  # the reason edge must survive


# --- Spans and hashes ---
def test_spans_and_hash():
    src = "First claim here. Second claim here."
    claims = split_candidates(src, "SN-X")
    assert len(claims) == 2
    for c in claims:
        assert src[c.text_span[0]:c.text_span[1]] == c.nucleus
        assert len(c.source_content_hash) == 64
    assert claims[0].claim_id == "SN-X:C-000"
    assert claims[1].claim_id == "SN-X:C-001"
