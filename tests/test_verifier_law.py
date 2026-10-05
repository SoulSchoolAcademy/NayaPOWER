"""Tests for the executable six verifier properties.

Each test is the negative control: it fails when the property is violated.
A law with no failing test is prose.
"""

from tools.verifier_law import Claim, verify, is_independent


def _good(**kw) -> Claim:
    base = dict(text="the gate validates typed values", ref="main",
                is_main=True, citations=[], citations_resolve={},
                substance_holds=True, security_tier=False,
                adversarial_test_exists=False, security_score=None,
                command=None, exit_status=None, search_scope=None,
                claims_absence=False, builder="naya4",
                independent_verifier="coda1", verification_state=None,
                grants_authority=False)
    base.update(kw)
    return Claim(**base)


def test_fully_specified_claim_is_certified():
    v = verify(_good())
    assert v.certified and v.state == "CERTIFIED", v.failures + v.unknowns


def test_P1_branch_is_not_main_is_rejected():
    v = verify(_good(is_main=False, ref="feature/x"))
    assert v.state == "REJECTED" and any("P1" in f for f in v.failures)


def test_P2_bad_citation_fails_even_when_substance_holds():
    """The exact Super Brain case: substance true, citations false."""
    v = verify(_good(citations=["SN-0288"], citations_resolve={"SN-0288": False},
                     substance_holds=True))
    assert v.state == "REJECTED" and any("P2" in f for f in v.failures)


def test_P2_unresolved_citation_is_unknown_not_rejected():
    v = verify(_good(citations=["SN-9999"], substance_holds=True))
    assert v.state == "NOT_PROVEN" and any("P2" in u for u in v.unknowns)


def test_P3_untested_security_blocks_certification():
    """THE load-bearing test: a claimed defense never attacked."""
    v = verify(_good(text="the immune system rollback is secure",
                     security_tier=True, adversarial_test_exists=False,
                     security_score=9.0))
    assert not v.certified and any("P3" in f for f in v.failures)


def test_P3_tested_security_with_score_can_certify():
    v = verify(_good(text="rollback security verified", security_tier=True,
                     adversarial_test_exists=True, security_score=9.5))
    assert v.certified, v.failures + v.unknowns


def test_P4_absence_without_evidence_is_rejected():
    v = verify(_good(claims_absence=True))
    assert v.state == "REJECTED" and any("P4" in f for f in v.failures)


def test_P4_absence_with_command_exit_and_scope_passes():
    v = verify(_good(claims_absence=True,
                     command="git grep -l X origin/main -- '*.py'",
                     exit_status=1, search_scope="*.py on origin/main"))
    assert v.certified, v.failures + v.unknowns


def test_P5_builder_report_without_verifier_is_rejected():
    v = verify(_good(independent_verifier=None))
    assert v.state == "REJECTED" and any("P5" in f for f in v.failures)


def test_P5_self_verification_is_rejected():
    """Coda 1's own conflict of interest, encoded permanently."""
    v = verify(_good(builder="coda1", independent_verifier="coda1"))
    assert v.state == "REJECTED" and any("P5" in f for f in v.failures)


def test_P6_verified_must_not_grant_authority():
    v = verify(_good(verification_state="VERIFIED", grants_authority=True))
    assert v.state == "REJECTED" and any("P6" in f for f in v.failures)


def test_verification_without_authority_is_fine():
    v = verify(_good(verification_state="VERIFIED", grants_authority=False))
    assert v.certified, v.failures + v.unknowns


def test_is_independent_helper():
    assert is_independent("naya4", "coda1")
    assert not is_independent("coda1", "coda1")
    assert not is_independent("naya4", None)
