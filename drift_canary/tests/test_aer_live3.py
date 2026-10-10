"""AER-LIVE-3 tests: Independently Verified Eligibility Witnesses.

Six facts, three verdicts, bidirectional E2.
"""
import sys
sys.path.insert(0, "drift_canary")

from aer_live3_eligibility import (
    EligibilityVerdict,
    fixture_all_eligible,
    fixture_law_absent,
    fixture_missing_evidence,
    fixture_starvation,
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
