"""Regression guard: the causal VERIFIER must not be the EXECUTOR's echo.

FINDING THIS GUARDS
-------------------
Two causal verification paths exist in this repository:

  * `nayanet-causal-verify` (11KB, bound to live-cvo-runtime-proof.yml) - strong.
    It re-reads the durable grant, re-reads BOTH receipts AND BOTH
    nayanet_execution_outcomes, requires both outcomes already independently
    verified, then cross-checks the CVO against the re-read rows.

  * `nayanet-causal-learning-experiment` (bound to
    live-supabase-runtime-proof.yml) - THIS IS THE ONE THAT PRODUCES
    causal-learning-experiment-receipt.json.

Before this guard, the second function's `mode==="verify"` block was
SELF-CERTIFYING. It read the CVO out of the treatment receipt's own
executor-written `evidence` array and then asserted only that the constants
equalled the expected constants and that treatment status was SUCCESS.

Inside that block there were ZERO references to `c.observed_result` and ZERO to
`cevidence`. It never compared the control to the treatment at all. Therefore
it would have returned `ok:true` even if the control and the treatment had
produced IDENTICAL behaviour -- i.e. even when the "learning" demonstrably had
no effect. `causal_assessment:"CAUSAL_SUPPORTED"` was a literal the executor
wrote and the verifier echoed.

Why that matters for NayaPOWER: an executor that can certify its own success is
exactly the boundary the whole system exists to prevent. Committing a receipt
whose `independent_verification: true` was earned this way would convert a real
UNKNOWN into a PASS.

WHAT IS ASSERTED HERE
---------------------
The verify block must be an AUTHORITATIVE RE-READ AND RECOMPUTATION:
it must derive the causal verdict from persisted state it re-read, must require
that recomputation to agree with the executor's declaration, and must not treat
the declaration as evidence.

This is a source-contract test, deliberately. It is a guard against a silent
regression to self-certification, not a substitute for the live OIDC proof, which
is what actually establishes the causal claim. The live run is the proof; this
test is the ratchet that keeps the proof from being quietly hollowed out.
"""

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LEARNING_EXPERIMENT = REPO / "supabase" / "functions" / "nayanet-causal-learning-experiment" / "index.ts"
STRONG_VERIFIER = REPO / "supabase" / "functions" / "nayanet-causal-verify" / "index.ts"


def _verify_block(source: str) -> str:
    """Isolate the `mode==="verify"` branch so assertions cannot be satisfied by
    text that merely exists elsewhere in the function."""
    start = source.find('if(mode==="verify")')
    assert start != -1, "no mode==='verify' branch found in the learning-experiment verifier"
    end = source.find("const causal={", start)
    assert end != -1, "could not delimit the end of the verify branch"
    return source[start:end]


def test_verify_branch_actually_compares_control_to_treatment():
    """The defect: the verify branch never looked at the control's behaviour."""
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert "c.observed_result" in block, (
        "verify branch must re-read and compare the control's observed_result; "
        "without it the verifier cannot detect an absent behavioral delta and is self-certifying"
    )
    assert "c.status" in block, "verify branch must require the control receipt to be SUCCESS, not just the treatment"


def test_verify_branch_recomputes_from_both_sides_evidence():
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert "cevidence" in block, "verify branch must re-read the control evidence condition"
    assert "tevidence" in block, "verify branch must re-read the treatment evidence condition"


def test_verify_branch_requires_recomputation_to_agree_with_executor():
    """The executor's claim must be CORROBORATED, never believed."""
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert "declared_matches_recomputation" in block, (
        "verify branch must require the executor's causal_assessment to match the independently "
        "recomputed assessment"
    )
    assert "recomputed_causal_assessment" in block, "verify branch must publish its own recomputed assessment"
    assert "executor_claim_trusted:false" in block, "verify branch must record that it does not trust the executor claim"


def test_verify_branch_verdict_depends_on_recomputation():
    """If the recomputation fails, the verdict must fail. This is the property
    that makes an identical-behavior control/treatment pair impossible to pass."""
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert "causal_supported" in block, "verify branch must gate its verdict on the recomputed support flag"
    valid_clause = block[block.rfind("const valid="):]
    assert "causal_supported" in valid_clause, (
        "the final verdict must include the recomputed support flag; otherwise the executor's "
        "declaration alone decides the outcome"
    )


def test_verify_branch_enforces_task_equivalence():
    """Hole B: a control/treatment difference only supports a causal claim if the
    task was otherwise equivalent. Both sides must reference the same learning."""
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert "task_equivalence" in block, "verify branch must establish that control and treatment ran the same task"
    assert "same_source_event" in block, "verify branch must confirm both sides reference the same source event"


def test_verify_branch_does_not_declare_independence_it_does_not_have():
    """The executor writes the CVO. It must not label its own object as the
    product of an independent re-read."""
    source = LEARNING_EXPERIMENT.read_text(encoding="utf-8")
    assert "independent-runtime-reread-of-persisted-treatment-receipt" not in source, (
        "the executor-written CVO must not claim an independent re-read; that label was a false "
        "claim of independence by the very component that later gets 'verified'"
    )
    assert "executor-declared-cvo-pending-independent-runtime-reverification" in source


def test_strong_verifier_remains_the_reference_pattern():
    """Guard the reference implementation the fix mirrors, so the two do not
    silently diverge in strength."""
    source = STRONG_VERIFIER.read_text(encoding="utf-8")
    assert "nayanet_execution_outcomes" in source, "the strong verifier must re-read persisted outcomes"
    assert "treatmentOutcome.verified" in source and "controlOutcome.verified" in source, (
        "the strong verifier must require BOTH outcomes to already be independently verified"
    )
    assert "causal.observed_change === treatment.observed_result" in source, (
        "the strong verifier must cross-check the CVO against state re-read from the database"
    )


def test_cvo_write_preserves_the_treatment_evidence_conditions():
    """SECOND DEFECT, found by the strengthened verifier refusing to certify.

    The CVO write built its update as
        [...(Array.isArray(t.evidence) ? t.evidence : []).filter(...), {causal_verification}]
    but the treatment receipt's evidence is an OBJECT, so the spread produced
    nothing and the update replaced the evidence with [{causal_verification}].
    That silently DESTROYED condition, retained_intelligence_used, learning_id,
    source_event_id and intelligence_id on the treatment receipt.

    The old self-certifying verifier never noticed because it never read
    tevidence. Any verifier that does read it sees an empty object and must
    correctly refuse to certify."""
    source = LEARNING_EXPERIMENT.read_text(encoding="utf-8")
    assert "...(Array.isArray(t.evidence)?t.evidence:[]).filter" not in source, (
        "the CVO write must not discard the original treatment evidence; spreading an object "
        "yields nothing and replaces the evidence with the CVO alone"
    )
    assert "const updatedEvidence={...(tevidence as any)" in source, (
        "the CVO write must merge the CVO into the existing treatment evidence object"
    )


def test_evidence_reading_tolerates_both_shapes():
    """Evidence is an object on write, but historical receipts hold an array
    (the shape the old CVO write produced). A verifier must read both."""
    source = LEARNING_EXPERIMENT.read_text(encoding="utf-8")
    assert "Array.isArray(t.evidence)?t.evidence.filter" in source, (
        "array-shaped evidence must be merged rather than silently read as empty"
    )
    block = _verify_block(source)
    assert "Array.isArray(t.evidence)?" in block, (
        "the CVO must be locatable in both the object and the array evidence shape"
    )


@pytest.mark.parametrize(
    "required",
    [
        "behavioral_delta_present",
        "control_observed_result",
        "treatment_observed_result",
        "both_success",
        "control_condition",
        "treatment_condition",
        "task_equivalence",
        "provenance_present",
    ],
)
def test_recomputation_publishes_every_fact_a_cold_successor_needs(required):
    """Directive section 7: the receipt must let a cold successor reconstruct the
    causal claim without trusting the executor."""
    block = _verify_block(LEARNING_EXPERIMENT.read_text(encoding="utf-8"))
    assert required in block, f"recomputation must publish {required} so the verdict is auditable"
