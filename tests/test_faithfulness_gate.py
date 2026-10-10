"""Faithfulness gate tests: faithful passes, distorted fails closed.

The 10 dangerous mistakes as negative controls: each DISTORTED extraction
fed to the gate must come back REJECTED (never FAITHFUL).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extraction.claim import Claim, MeaningEnvelope
from extraction.extractor import split_candidates
from extraction.faithfulness import gate_claim, forward_entailment, coverage_check


def make_claim(source, claim_id, nucleus, envelope):
    h = Claim.content_hash(source)
    span = (source.find(nucleus[:20]), source.find(nucleus[:20]) + len(nucleus))
    return Claim(claim_id=claim_id, parent_source_id="T",
                 source_content_hash=h, text_span=span,
                 nucleus=nucleus, envelope=envelope)


def test_faithful_claim_passes():
    src = "Not all tests passed on the first run."
    claims = split_candidates(src, "T")
    verdict = gate_claim(src, claims[0], claims)
    assert verdict["faithfulness"] == "FAITHFUL"
    assert verdict["consequential_use_allowed"]


def test_distorted_negation_rejected():
    # MISTAKE 1: "Not all tests passed" -> "No tests passed"
    src = "Not all tests passed on the first run."
    bad = make_claim(src, "T:C-000", "No tests passed",
                     MeaningEnvelope(polarity="NEGATIVE", quantifier="none"))
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"
    assert not verdict["consequential_use_allowed"]


def test_distorted_scope_rejected():
    # MISTAKE 6: "Three of five agents succeeded" -> "All agents succeeded"
    src = "Three of five agents succeeded."
    bad = make_claim(src, "T:C-000", "All agents succeeded",
                     MeaningEnvelope(quantifier="all"))
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"


def test_distorted_condition_dropped_rejected():
    # MISTAKE 5: "X improves performance when condition Y holds" -> "X always improves"
    src = "X improves performance when condition Y holds."
    bad = make_claim(src, "T:C-000", "X always improves performance",
                     MeaningEnvelope(condition="NONE"))
    verdict = gate_claim(src, bad, [bad])
    # coverage must flag the dropped conditional
    assert verdict["coverage"]["passes"] is False or \
        verdict["faithfulness"] != "FAITHFUL"


def test_distorted_attribution_rejected():
    # MISTAKE 7: "Agent A claims the test passed" -> "The test passed" (as fact)
    src = "Agent A claims the test passed."
    bad = make_claim(src, "T:C-000", "The test passed",
                     MeaningEnvelope(attribution="NONE", epistemic="OBSERVED"))
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"


def test_distorted_causation_rejected():
    # MISTAKE 10: "A and B were observed together" -> "A causes B"
    src = "A and B were observed together."
    bad = make_claim(src, "T:C-000", "A causes B",
                     MeaningEnvelope())
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"


def test_distorted_modality_rejected():
    # MISTAKE 9: "No failures were observed in 20 trials" -> "Failure is impossible"
    src = "No failures were observed in 20 trials."
    bad = make_claim(src, "T:C-000", "Failure is impossible",
                     MeaningEnvelope(modality="NECESSARY"))
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"


def test_coverage_catches_dropped_exception():
    # extraction that keeps the nucleus but drops "except production writes"
    src = "Regeneration is safe except for production writes."
    claims = split_candidates(src, "T")
    # simulate a claim whose envelope lost the exception
    stripped = Claim(claim_id=claims[0].claim_id,
                     parent_source_id="T",
                     source_content_hash=claims[0].source_content_hash,
                     text_span=claims[0].text_span,
                     nucleus="Regeneration is safe",
                     envelope=MeaningEnvelope())
    verdict = gate_claim(src, stripped, [stripped])
    assert verdict["coverage"]["passes"] is False
    assert verdict["faithfulness"] == "NEEDS_REVIEW"


def test_nested_negation_not_universal_permission():
    src = "It is not true that Naya must never use candidate knowledge."
    bad = make_claim(src, "T:C-000",
                     "Naya may use candidate knowledge for every action",
                     MeaningEnvelope(modality="PERMITTED", quantifier="all"))
    verdict = gate_claim(src, bad, [bad])
    assert verdict["faithfulness"] != "FAITHFUL"
