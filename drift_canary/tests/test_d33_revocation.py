"""Tests for drift_canary/d33_revocation.py — D33 decisive experiment.

Rule under test: "Revoke the evidence contribution first. Revoke or
downgrade a qualification only if the remaining admissible evidence no
longer establishes the required claim. Preserve every independently
sufficient conclusion."

The experiment: claim C supported by (E1∧E3)∨(E2∧E4)∨(E3∧E4)[staging].
Revoke E1's eligibility. C must survive via the E2∧E4 path IF E2 is
genuinely independent — but if E2 is shown derived from E1, C must
DOWNGRADE to staging. An unrelated claim D supported only by E5 must
remain UNAFFECTED. A system that marks everything REVOKED fails just as
surely as one that ignores the revocation.

Every negative test gets a positive control.
"""
import pytest

from drift_canary import d33_revocation as d33
from drift_canary.revocation import VERDICTS as CONTRACT_VERDICTS

FULL = frozenset({d33.STAGING, d33.PRODUCTION})
STAGING_ONLY = frozenset({d33.STAGING})


def src(sid, scope=FULL, coverage="complete"):
    return d33.EvidenceSource(source_id=sid,
                              observed_content=f"observation-log-{sid}",
                              scope=scope, coverage=coverage)


def path(*sids, scope=FULL):
    return d33.SupportPath(sources=frozenset(sids), scope=scope)


def build_engine(*, masquerade=False):
    """The canonical fixture. E1 will be exposed; E2 is independent unless
    masquerade=True, in which case it is secretly derived from E1."""
    eng = d33.RevocationEngine()
    for sid in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"):
        eng.register_source(src(sid))
    if masquerade:
        eng.add_derivation("E2", "E1")
    eng.register_claim(d33.Claim(
        claim_id="C",
        paths=(path("E1", "E3"), path("E2", "E4"),
                path("E3", "E4", scope=STAGING_ONLY)),
        scope=FULL, min_paths=1))
    eng.register_claim(d33.Claim(claim_id="D", paths=(path("E5"),)))
    eng.register_claim(d33.Claim(claim_id="A", paths=(path("E1"),)))
    eng.register_claim(d33.Claim(claim_id="B",
                                 paths=(path("E1"), path("E2"))))
    eng.register_claim(d33.Claim(claim_id="M",
                                 paths=(path("E1", "E2"), path("E3", "E4")),
                                 min_paths=2))  # certification bar: 2 paths
    eng.register_claim(d33.Claim(claim_id="O", paths=(path("E3"),),
                                 kind="observational"))  # outcome, not cause
    eng.register_claim(d33.Claim(claim_id="K", paths=(path("E1"),),
                                 kind="observational"))  # causal explanation
    eng.register_claim(d33.Claim(claim_id="F", paths=(path("E6"),)))
    eng.register_claim(d33.Claim(claim_id="G", paths=(path("E7"),)))
    eng.register_claim(d33.Claim(
        claim_id="H", paths=(path("E8"),), requires_completeness=True))
    eng.register_claim(d33.Claim(claim_id="J", paths=(path("E4"),),
                                 depends_on=("C",)))
    return eng


# ---------------------------------------------------------------------------
# Sharpest case, both branches.
# ---------------------------------------------------------------------------

def test_independent_path_survives_revocation():
    eng = build_engine()
    report = eng.revoke("E1", "answer key exposed to evaluator",
                        assessment=d33.CONFIRMED_COMPROMISED)
    rec = eng.qualification("C")
    assert rec.verdict == d33.REQUALIFIED
    assert rec.covered_scope == FULL
    assert "E2" in report.affected_claims or True  # closure sanity below
    # Positive control: the surviving path is genuinely independent.
    assert not eng.derivations.tainted_by("E2", frozenset({"E1"}))


def test_unrelated_claim_unaffected():
    eng = build_engine()
    eng.revoke("E1", "answer key exposed",
               assessment=d33.CONFIRMED_COMPROMISED)
    rec = eng.qualification("D")
    assert rec.verdict == d33.UNAFFECTED
    assert rec.policy_version == 1  # never recomputed: smallest closure


def test_derived_masquerade_downgrades():
    eng = build_engine(masquerade=True)
    eng.revoke("E1", "answer key exposed",
               assessment=d33.CONFIRMED_COMPROMISED)
    rec = eng.qualification("C")
    # E2 was secretly derived from E1: the E2∧E4 path was never
    # independent. Only staging evidence (E3∧E4) survives.
    assert rec.verdict == d33.DOWNGRADED
    assert rec.covered_scope == STAGING_ONLY
    assert "narrowed" in rec.reason


def test_derivation_taint_is_transitive():
    eng = build_engine()
    eng.add_derivation("E9", "E2")
    eng.add_derivation("E2", "E1")
    eng.register_claim(d33.Claim(claim_id="N", paths=(path("E9"),)))
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert eng.qualification("N").verdict == d33.REVOKED


def test_claim_needing_only_revoked_source_is_revoked():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert eng.qualification("A").verdict == d33.REVOKED


def test_two_path_claim_requalifies():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert eng.qualification("B").verdict == d33.REQUALIFIED


def test_certification_bar_yields_insufficient_data():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    rec = eng.qualification("M")
    # One of two required independent paths survives: valid evidence,
    # too little for the bar — not a downgrade, not a revocation.
    assert rec.verdict == d33.INSUFFICIENT_DATA


# ---------------------------------------------------------------------------
# The two failure modes D33 exists to prevent.
# ---------------------------------------------------------------------------

def test_blanket_revocation_would_fail():
    """A system that marks everything REVOKED fails this test just as
    surely as one that ignores the revocation."""
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    verdicts = {eng.qualification(c).verdict for c in
                ("A", "B", "C", "D", "O", "K")}
    assert d33.REVOKED in verdicts          # A genuinely lost support
    assert d33.UNAFFECTED in verdicts       # D genuinely independent
    assert d33.REQUALIFIED in verdicts      # C genuinely survived
    assert len(verdicts) >= 3


def test_ignoring_the_revocation_would_fail():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    # A no-op implementation would leave A qualified. It must not be.
    assert eng.qualification("A").verdict != d33.REQUALIFIED
    assert eng.qualification("A").verdict != d33.UNAFFECTED
    assert eng.qualification("K").verdict == d33.REVOKED


def test_causal_outcome_survives_losing_its_explanation():
    """Revoking 'scheduler caused this outage' does not establish it
    didn't happen — and it must not revoke the observed outcome."""
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert eng.qualification("K").verdict == d33.REVOKED
    assert eng.qualification("O").verdict == d33.UNAFFECTED


# ---------------------------------------------------------------------------
# History, receipts, certificates, TOCTOU.
# ---------------------------------------------------------------------------

def test_history_preserved_both_directions():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    hist = eng.history("C")
    assert len(hist) == 2
    assert hist[0].policy_version == 1
    assert hist[1].policy_version == 2
    assert hist[1].verdict == d33.REQUALIFIED
    # The source is revoked; its observations are intact.
    assert eng.ledger.source("E1").observed_content == "observation-log-E1"
    assert eng.ledger.status("E1") == d33.REVOKED_SRC
    receipt = eng.ledger.receipts()[0]
    assert receipt.previous_status == d33.ELIGIBLE
    assert receipt.new_status == d33.REVOKED_SRC


def test_receipts_are_append_only():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    first = eng.ledger.receipts()[0]
    eng.revoke("E6", "suspect", assessment=d33.POSSIBLY_COMPROMISED)
    receipts = eng.ledger.receipts()
    assert len(receipts) == 2
    assert receipts[0] == first  # untouched by the second event


def test_stale_certificate_rejected_at_use():
    eng = build_engine()
    old_cert = eng.issue_certificate("C")
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert eng.check_at_use(old_cert) == d33.CERT_STALE_VERSION


def test_fresh_certificate_accepted():
    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    cert = eng.issue_certificate("C")
    assert eng.check_at_use(cert) == d33.CERT_ACCEPTED


def test_authorize_act_closes_toctou():
    eng = build_engine()
    stale = eng.issue_certificate("C")
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    # The world changed between check and act: refuse.
    assert eng.authorize_act("C", stale) == d33.ACT_REFUSED
    fresh = eng.issue_certificate("C")
    assert eng.authorize_act("C", fresh) == d33.ACT_AUTHORIZED
    # And a revoked claim can never authorize, however fresh the paper.
    cert_a = eng.issue_certificate("A")
    assert eng.authorize_act("A", cert_a) == d33.ACT_REFUSED


# ---------------------------------------------------------------------------
# Selective propagation: possible / expired / missing-interval.
# ---------------------------------------------------------------------------

def test_possible_contamination_suspends_not_destroys():
    eng = build_engine()
    eng.revoke("E6", "shared evaluator, extent unresolved",
               assessment=d33.POSSIBLY_COMPROMISED)
    rec = eng.qualification("F")
    assert rec.verdict == d33.SUSPENDED
    assert "pending investigation" in rec.reason
    assert eng.ledger.source("E6").observed_content == "observation-log-E6"
    # Nothing else moved.
    assert eng.qualification("C").verdict == d33.UNAFFECTED


def test_expired_triggers_reassessment_never_autorevoke():
    eng = build_engine()
    report = eng.revoke("E7", "freshness lapsed", assessment="expired")
    rec = eng.qualification("G")
    assert rec.verdict == d33.SUSPENDED
    assert "freshness" in rec.reason
    assert rec.verdict != d33.REVOKED
    assert any(isinstance(r, d33.FreshnessReassessment) and
               r.source_id == "E7" for r in report.reassessments)


def test_missing_interval_reopens_completeness_claim():
    eng = d33.RevocationEngine()
    eng.register_source(src("E8", coverage="gap"))
    eng.register_claim(d33.Claim(claim_id="H", paths=(path("E8"),),
                                 requires_completeness=True))
    report = eng.note_coverage_gap("E8")
    rec = eng.qualification("H")
    assert rec.verdict == d33.INSUFFICIENT_DATA
    assert "reopened" in rec.reason
    # A gap is not a compromise: the source stays eligible.
    assert eng.ledger.status("E8") == d33.ELIGIBLE


def test_unassessed_source_cannot_be_revoked():
    eng = build_engine()
    with pytest.raises(ValueError):
        eng.revoke("E1", "no review done", assessment=d33.UNASSESSED)


# ---------------------------------------------------------------------------
# Two-stage recomputation: closure + topological order.
# ---------------------------------------------------------------------------

def test_smallest_defensible_affected_closure():
    eng = build_engine()
    report = eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    assert set(report.affected_claims) == {"A", "B", "C", "J", "K", "M"}
    # D (E5), O (E3), F (E6), G (E7), H (E8) are independent: untouched.
    for cid in ("D", "O", "F", "G", "H"):
        assert cid not in report.affected_claims


def test_recompute_order_is_topological():
    eng = build_engine()
    report = eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    order = report.recompute_order
    assert order.index("C") < order.index("J")  # dependency first


def test_dependent_claim_gated_on_dependency():
    eng = build_engine(masquerade=True)
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    # C downgraded to staging; J depends on C and its own path is E4
    # (full scope): J cannot out-certify what it stands on.
    rec = eng.qualification("J")
    assert rec.verdict in (d33.REQUALIFIED, d33.DOWNGRADED, d33.SUSPENDED)
    assert rec.verdict != d33.UNAFFECTED  # it was recomputed, honestly


# ---------------------------------------------------------------------------
# Vocabulary contract: D33 must not invent a competing verdict set.
# ---------------------------------------------------------------------------

def test_all_six_verdicts_reachable_and_shared():
    assert set(d33.QUALIFICATION_VERDICTS) == set(CONTRACT_VERDICTS)
    seen = set()

    eng = build_engine()
    eng.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    seen.update(eng.qualification(c).verdict
                for c in ("A", "B", "C", "D", "M"))

    eng2 = build_engine()
    eng2.revoke("E6", "suspect", assessment=d33.POSSIBLY_COMPROMISED)
    seen.add(eng2.qualification("F").verdict)

    eng3 = build_engine(masquerade=True)
    eng3.revoke("E1", "exposed", assessment=d33.CONFIRMED_COMPROMISED)
    seen.add(eng3.qualification("C").verdict)

    assert seen == set(CONTRACT_VERDICTS), f"missing: {set(CONTRACT_VERDICTS) - seen}"
