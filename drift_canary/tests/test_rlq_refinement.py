"""RLQ-REFINEMENT tests (SN-0789): the real system implements the model.
Traces(C)|relevant ⊆ Traces(A) -- actual commit ordering, not method calls.
The refinement mapping α, differential history checking, the six
boundaries, RLQ-REF-001, certificates, and the acceptance hierarchy."""
import threading

import pytest

from drift_canary.revocation_linearization import (
    AuthoritativeState,
    ProjectionCandidate,
    COMMITTED,
    STALE_DEPENDENCY,
    CURRENT,
    FENCED,
    refinement_fixture,
    alpha,
    alpha_relevant,
    check_establishment_correspondence,
    differential_check,
    DIFFERENTIAL_HOLDS,
    DIFFERENTIAL_FALSIFIED,
    DIFFERENTIAL_INCONCLUSIVE,
    REFINEMENT_BOUNDARIES,
    REFINEMENT_EXCLUSIONS,
    EXTERNAL_GATEWAY_MECHANISMS,
    RefinementCertificate,
    issue_certificate,
    implementation_sha,
    rlq_ref_001,
    acceptance_status,
    ACCEPTANCE_RUNGS,
)


# --- α: the refinement mapping ---------------------------------------------------
def test_alpha_shape():
    a = alpha(refinement_fixture())
    assert len(a.ev) == 3 and len(a.claims) == 2
    # All eligible, rev 1, no fence at fixture build.
    assert all(e[1] and e[2] == -1 for e in a.ev)
    # C1 has the OR shape (E1^E3)vE2; C2 is E1-only.
    assert len(a.claims[0][2]) == 2
    assert len(a.claims[1][2]) == 1


def test_r1_establishment_correspondence():
    """R1: abstract established ⟺ concrete CURRENT -- at build, after
    revocation (E2 path preserves C1), and after requalification."""
    st = refinement_fixture()
    assert check_establishment_correspondence(st) == []
    st.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t")
    assert check_establishment_correspondence(st) == []
    assert st.qualification_standing("c1") == CURRENT   # E2 path
    assert st.qualification_standing("c2") == FENCED    # E1-only


# --- differential checking --------------------------------------------------------
def test_differential_holds_on_honest_history():
    """A concrete revoke-then-stale-publish history maps to a legal
    abstract execution under the immutable oracle."""
    rev_at_read = {}

    def _revoke(s):
        rev_at_read["r"] = s.evidence["e1"].eligibility_revision
        return s.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t")

    def _stale_publish(s):
        h = s.projections["p1"]
        c = ProjectionCandidate(
            "p1", h.projection_revision, "art-0",
            {"c1": s.claims["c1"].qualification_revision,
             "c2": s.claims["c2"].qualification_revision},
            {"e1": rev_at_read["r"],
             "e2": s.evidence["e2"].eligibility_revision,
             "e3": s.evidence["e3"].eligibility_revision},
            "LAW-v3", {"c1": "REQUALIFIED", "c2": "REQUALIFIED"},
            ("certification",), h.fencing_token)
        return s.publish_projection(c)

    st = refinement_fixture()
    h0 = st.projections["p1"]
    snap = (h0.projection_revision, h0.fencing_token,
            (h0.claim_deps["c1"], h0.claim_deps["c2"]),
            (h0.evidence_deps["e1"], h0.evidence_deps["e2"],
             h0.evidence_deps["e3"]), 0)
    r = differential_check([
        (_revoke, ("R", 0), "revoke e1"),
        (_stale_publish, ("P", snap), "stale publish rejected"),
    ])
    assert r["verdict"] == DIFFERENTIAL_HOLDS, r


def test_differential_falsifies_hidden_bookkeeping():
    """AUTHORITY RULE: a concrete op that changes authority state with no
    mapped abstract transition is FALSIFIED -- never assumed benign."""
    def _sneaky(s):
        # Directly mutates authority state outside any mapped operation.
        s.evidence["e1"].eligible = False
        return "sneaky"

    r = differential_check([(_sneaky, None, "unmapped eligibility flip")])
    assert r["verdict"] == DIFFERENTIAL_FALSIFIED
    assert "hidden bookkeeping" in r["reason"]


def test_differential_inconclusive_on_inapplicable_step():
    """A second revocation of already-ineligible evidence is inapplicable
    in the abstract machine -- INCONCLUSIVE, never assumed."""
    def _revoke(s):
        return s.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t")

    def _revoke_again(s):
        # Concrete: second revocation still "commits" (new receipt);
        # abstract: inapplicable (evidence already ineligible).
        return s.commit_revocation("e1", "t2", "s", "p", "LAW-v3", "t")

    r = differential_check([
        (_revoke, ("R", 0), "revoke e1"),
        (_revoke_again, ("R", 0), "revoke e1 again"),
    ])
    assert r["verdict"] == DIFFERENTIAL_INCONCLUSIVE
    assert "inapplicable" in r["reason"]


# --- the decisive obligation: concurrent R/P, no third case ------------------------
def test_decisive_obligation_concurrent_rp():
    """Every concurrent R/P pair yields P<R or R<P -- no third case.
    Commit-seq order is the witness; the commit lock is the mechanism."""
    for _ in range(50):
        st = refinement_fixture()
        results = {}

        def pub():
            h = st.projections["p1"]
            c = ProjectionCandidate(
                "p1", h.projection_revision, "art-0",
                {"c1": st.claims["c1"].qualification_revision,
                 "c2": st.claims["c2"].qualification_revision},
                {"e1": st.evidence["e1"].eligibility_revision,
                 "e2": st.evidence["e2"].eligibility_revision,
                 "e3": st.evidence["e3"].eligibility_revision},
                "LAW-v3", {"c1": "REQUALIFIED", "c2": "REQUALIFIED"},
                ("certification",), h.fencing_token)
            results["pub"] = st.publish_projection(c)[0]

        def rev():
            st.commit_revocation("e1", "race", "s", "p", "LAW-v3", "t")
            results["rev"] = "committed"

        t1, t2 = threading.Thread(target=pub), threading.Thread(target=rev)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        pubs = [op for op in st.linearization_log
                if op.op_type == "P" and "reject" not in op.summary]
        revs = [op for op in st.linearization_log
                if op.op_type == "R"]
        assert revs, "revocation must commit"
        if results["pub"] == COMMITTED:
            assert pubs and pubs[0].seq < revs[0].seq, "P<R violated"
        else:
            # R<P: the publication lost the race and was rejected.
            assert results["pub"] in (STALE_DEPENDENCY, "WRITE_CONFLICT")


# --- RLQ-REF-001 ---------------------------------------------------------------------
def test_rlq_ref_001_certificate():
    """The full RLQ-REF-001 procedure executes: pause, revoke, resume,
    inspect, map, mutant falsified, restore -- and yields the certificate."""
    cert = rlq_ref_001()
    assert isinstance(cert, RefinementCertificate)
    assert cert.certificate_id == "RLQ-REFINEMENT-1/RLQ-REF-001"
    assert len(cert.implementation_sha) == 64
    assert cert.implementation_sha == implementation_sha()
    assert cert.exclusions, "every certificate states its exclusions"
    assert any("Durability" in e for e in cert.exclusions)
    assert any("external effect" in e for e in cert.exclusions)
    # Candidate until a different seat reviews.
    assert cert.reviewer_identities == ()
    assert cert.verdict == "CANDIDATE_PENDING_REVIEW"
    assert len(cert.traces) >= 6


# --- six boundaries: separate, honest obligations ---------------------------------------
def test_six_boundaries_tabled_honestly():
    assert set(REFINEMENT_BOUNDARIES) == {
        "database_state", "transaction_engine", "scheduler",
        "recovery", "read_time_validation", "external_action_gateway"}
    for name, b in REFINEMENT_BOUNDARIES.items():
        assert b["status"] in ("PROVEN", "ARGUMENT", "ASSUMPTION", "EXCLUDED"), name
        assert b["claim"] and b["mechanism"] and b["evidence"], name
    # The two non-PROVEN boundaries say so explicitly.
    assert REFINEMENT_BOUNDARIES["recovery"]["status"] == "ARGUMENT"
    assert REFINEMENT_BOUNDARIES["external_action_gateway"]["status"] == "ARGUMENT"
    # The gateway mechanisms table distinguishes what each covers.
    assert set(EXTERNAL_GATEWAY_MECHANISMS) == {
        "fencing_tokens", "cooperating_gateways", "drain_barriers",
        "cancellation_limits"}


def test_external_gateway_honest_qualification():
    """'No new external request authorized after revocation' (gateway) is
    NOT 'no external effect can occur after revocation' -- the latter is
    excluded unless independently established."""
    st = refinement_fixture()
    outcome, detail = st.commit_action("a1", ["c1", "c2"], True, external=True)
    assert outcome == "AUTHORIZED_VIA_GATEWAY"
    assert "gateway boundary only" in detail
    # After revocation, even the gateway refuses new authorizations.
    st.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t")
    st.commit_revocation("e2", "t", "s", "p", "LAW-v3", "t")
    outcome2, _ = st.commit_action("a2", ["c1"], True, external=True)
    assert outcome2 == "REJECTED"


# --- acceptance hierarchy: no earlier rung proves a later one --------------------------
def test_acceptance_hierarchy():
    status = acceptance_status()
    assert tuple(r for r in status if r.startswith("RUNG_")) == ACCEPTANCE_RUNGS
    assert status["RUNG_1_ABSTRACT_PROVED"]["claimed"] is True
    assert status["RUNG_2_MAPPING_ESTABLISHED"]["claimed"] is True
    assert status["RUNG_3_SEMANTICS_VALIDATED"]["claimed"] is True
    # Rung 4 is NOT claimed: needs a different seat + production config.
    assert status["RUNG_4_PRODUCTION_QUALIFIED"]["claimed"] is False
    assert "different seat" in status["RUNG_4_PRODUCTION_QUALIFIED"]["evidence"]
    assert status["law"] == "no earlier rung proves a later one"


def test_three_layers_none_stands_alone():
    """Model-only green does not imply refinement: the guard-removal
    mutant passes every abstract model test yet is FALSIFIED at the
    refinement layer. Each layer is necessary; none is sufficient."""
    # The mutant is a concrete-system defect: abstract model tests (which
    # run the reference) stay green by construction...
    from drift_canary.revocation_linearization import RLQ1Checker
    r = RLQ1Checker(defects=frozenset(), max_histories=2000).check(
        {"r": ["revoke0"]})
    assert r["violations"] == []
    # ...but rlq_ref_001 falsifies the concrete mutant (asserts internally).
    cert = rlq_ref_001()
    assert any("FALSIFIED" in t for t in cert.traces)
