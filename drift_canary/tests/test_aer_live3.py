"""AER-LIVE-3 tests: Independently Verified Eligibility Witnesses.

Six facts, three verdicts, bidirectional E2.
"""
from drift_canary.aer_live3_eligibility import (
    EligibilityFact,
    EligibilityVerdict,
    EligibilityWitness,
    fixture_all_eligible,
    fixture_law_absent,
    fixture_missing_evidence,
    fixture_starvation,
    make_fact,
    verify_eligibility,
)


def test_all_six_proven_yields_eligible():
    result = verify_eligibility(fixture_all_eligible())
    assert result.verdict == EligibilityVerdict.ELIGIBLE_PROVEN


def test_law_absent_yields_ineligible():
    """Reject false eligibility where LAW was absent."""
    result = verify_eligibility(fixture_law_absent())
    assert result.verdict == EligibilityVerdict.INELIGIBLE_PROVEN
    assert "law" in result.failed_facts
    # E2 direction B: LAW absent while everything else holds flags
    # the false-eligibility pattern (system would have claimed eligible)
    assert result.false_eligibility_suspected is True


def test_starvation_flagged():
    """Catch false ineligibility hiding starvation (bidirectional E2)."""
    result = verify_eligibility(fixture_starvation())
    assert result.verdict == EligibilityVerdict.INELIGIBLE_PROVEN
    assert result.false_ineligibility_suspected is True


def test_missing_evidence_yields_undetermined():
    """UNDETERMINED never collapses to false."""
    result = verify_eligibility(fixture_missing_evidence())
    assert result.verdict == EligibilityVerdict.ELIGIBILITY_UNDETERMINED
    assert "law" in result.missing_evidence
    # Must NOT be ineligible
    assert result.verdict != EligibilityVerdict.INELIGIBLE_PROVEN


def test_missing_evidence_beats_proven_false():
    """Missing evidence takes precedence over a proven-false fact.

    Epistemic honesty: if resources evidence is missing entirely AND law
    is proven false, we cannot claim INELIGIBLE_PROVEN — we cannot prove
    the full picture. Undetermined wins; failed_facts stays empty.
    """
    d = {n: make_fact(n) for n in (
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering")}
    d["law"] = make_fact("law", established=False)
    d["resources"] = make_fact("resources", evidence_missing=True)
    result = verify_eligibility(EligibilityWitness(**d))
    assert result.verdict == EligibilityVerdict.ELIGIBILITY_UNDETERMINED
    assert "resources" in result.missing_evidence
    assert result.failed_facts == ()


def test_all_facts_proven_false_yields_ineligible():
    """All six facts proven false → INELIGIBLE_PROVEN, no E2 flags.

    Both E2 flags only fire when exactly one fact fails while the other
    five hold. Total failure is plain ineligibility — nothing to suspect.
    """
    d = {n: make_fact(n, established=False) for n in (
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering")}
    result = verify_eligibility(EligibilityWitness(**d))
    assert result.verdict == EligibilityVerdict.INELIGIBLE_PROVEN
    assert set(result.failed_facts) == {
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering"}
    assert result.false_ineligibility_suspected is False
    assert result.false_eligibility_suspected is False
