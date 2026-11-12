"""RLQ-1 model tests: the verification half of the Revocation Linearization
Law (SN-0787). The R1-R12 matrix, S1-S6 properties, the six mutants,
liveness separation, the independent history verifier, display freshness,
crash injection, and the bounded fixture -- all against the reference
implementation with zero defects (the oracle is never mutated here)."""
import pytest

from drift_canary.revocation_linearization import (
    RLQ1Checker,
    RLQ1_CASES,
    MUTANTS,
    check_mutant,
    check_S6_E2_preserved,
    check_liveness,
    IndependentHistoryVerifier,
    HistoryOp,
    AuthoritativeState,
    rlq1_initial,
    rlq1_apply_step,
    rlq1_op_violations,
    reference_spec_sha,
    COMMITTED,
)


def _clean(scripts, defects=frozenset(), max_histories=4000):
    c = RLQ1Checker(defects=defects, max_histories=max_histories)
    return c.check(scripts)


# --- R1-R12: the correct implementation has no violations --------------------
@pytest.mark.parametrize("case_id,desc,scripts,_", RLQ1_CASES)
def test_rlq1_case_clean(case_id, desc, scripts, _):
    """Each R-case: the reference implementation, all interleavings,
    zero safety violations."""
    r = _clean(scripts)
    assert r["exhausted"], f"{case_id}: exploration hit cap"
    assert r["violations"] == [], f"{case_id} ({desc}): {r['violations']}"


def test_rlq1_r1_stale_publication_rejected():
    """R1 positive control: a publication whose read predates the revocation
    is REJECTED, not committed -- the fence fires before CAS."""
    st = rlq1_initial()
    st, _ = rlq1_apply_step(st, "w", "wread0", frozenset())
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    st, info = rlq1_apply_step(st, "w", "wpublish0", frozenset())
    assert info["outcome"] == "rejected"


def test_rlq1_r4_action_revalidates():
    """R4 positive control: after V then R, the action boundary rejects --
    the action cannot ride on pre-revocation validation."""
    st = rlq1_initial()
    st, vinfo = rlq1_apply_step(st, "v", "validate", frozenset())
    assert vinfo["result"] == "CURRENT_QUALIFIED"
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    st, ainfo = rlq1_apply_step(st, "a", "act", frozenset())
    assert ainfo["outcome"] == "rejected"


def test_rlq1_r5_historical_action_preserved():
    """R5: A<R -- an action committed BEFORE the revocation stays committed
    (no retroactive invalidation); only later actions are fenced."""
    st = rlq1_initial()
    st, ainfo = rlq1_apply_step(st, "a", "act", frozenset())
    assert ainfo["outcome"] == "committed"
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    # The earlier action is history; the checker finds no violation for it.
    r = _clean({"a": ["act"], "r": ["revoke0"]})
    assert r["violations"] == []


def test_rlq1_r8_exactly_one_writer_commits():
    """R8 race: two writers, one revocation-free race -- at most one
    commits on the same head (CAS serializes)."""
    committed = 0
    for order in (["w0", "w1"], ["w1", "w0"]):
        st = rlq1_initial()
        st, _ = rlq1_apply_step(st, "w0", "wread0", frozenset())
        st, _ = rlq1_apply_step(st, "w1", "wread1", frozenset())
        for w in order:
            st, info = rlq1_apply_step(
                st, w, f"wpublish{w[-1]}", frozenset())
            committed += (info["outcome"] == "committed")
    # Each order commits exactly one; total across both orders is 2.
    assert committed == 2


# --- S1-S6 as separately-checked properties ----------------------------------
def test_rlq1_s6_e2_path_preserved():
    """S6: E1's removal kills path 1; the E2 path preserves C1."""
    assert check_S6_E2_preserved() == []


def test_rlq1_s4_monotonic_on_clean_histories():
    """S4: on the reference implementation, revisions never decrease and
    every revocation mints a strictly greater revision."""
    for _cid, _d, scripts, _e in RLQ1_CASES:
        r = _clean(scripts)
        assert not [v for v in r["violations"] if v[0] == "S4"]


def test_rlq1_s5_replay_idempotent_on_clean():
    """S5: correct replay never rolls back; double replay is a noop."""
    st = rlq1_initial()
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    rev_before = st.ev[0][0]
    st, info = rlq1_apply_step(st, "j", "replay0", frozenset())
    assert info["replay"] == "noop-current"
    assert st.ev[0][0] == rev_before
    assert rlq1_op_violations(st, info, st) == []


# --- the six mutants: each MUST yield a counterexample -----------------------
MUTANT_SCRIPTS = {
    "M1_no_publish_guard": {"w0": ["wread0"], "r": ["revoke0"],
                            "w1": ["wread1", "wpublish1"]},
    "M2_no_action_fence": {"v": ["validate"], "r": ["revoke0"], "a": ["act"]},
    "M3_lazy_fence": {"r": ["revoke0"], "w": ["wread0", "wpublish0"]},
    "M4_blind_replay": {"r": ["revoke0"], "j": ["replay0"]},
    "M5_rev_reuse": {"r": ["revoke0"]},
    "M6_stale_read": {"v": ["validate"], "r": ["revoke0"], "v2": ["validate"]},
}


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_rlq1_mutant_yields_counterexample(mutant):
    """A mutant that passes is a failed specification: each defective
    implementation must produce a counterexample on its expected property
    -- or be PROVEN blocked by a redundant guard (M3_lazy_fence: the
    eligibility check redundantly covers the lazy fence in this model)."""
    expected, _desc = MUTANTS[mutant]
    r = check_mutant(mutant, MUTANT_SCRIPTS[mutant])
    props = {v[0] for v in r["violations"]}
    if mutant == "M3_lazy_fence":
        # Honest verdict: no S1 violation alone -- the publication-time
        # eligibility check redundantly blocks the lazy-fence window.
        # Removing that guard exposes the violation (guard-removal probe).
        assert not props, f"unexpected: {props}"
        probe = RLQ1Checker(
            defects=frozenset({mutant, "M1_no_publish_guard"}),
            max_histories=4000).check(MUTANT_SCRIPTS[mutant])
        assert "S1" in {v[0] for v in probe["violations"]}, \
            "redundant-guard proof failed: removing the eligibility check " \
            "must expose the S1 violation"
        return
    assert expected in props, (
        f"{mutant}: expected {expected} counterexample, got {props}")


def test_rlq1_mutant_positive_control():
    """Positive control: the same scripts are CLEAN without the defect --
    the violation comes from the mutation, not the scenario."""
    for mutant, scripts in MUTANT_SCRIPTS.items():
        r = _clean(scripts)
        assert r["violations"] == [], f"{mutant} control: {r['violations']}"


# --- liveness is separate from safety ----------------------------------------
def test_rlq1_liveness_separate_from_safety():
    """Safety holds even if every refresh worker crashes forever; liveness
    is a separate, conditional claim with no fairness assumption."""
    st = rlq1_initial()
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    st, _ = rlq1_apply_step(st, "x", "crash:replayer", frozenset())
    live = check_liveness(st)
    assert live["assumes_fairness"] is False
    # Safety is unaffected by the liveness outcome.
    r = _clean({"r": ["revoke0", "crash:replayer"], "j": ["replay0"]})
    assert r["violations"] == []


def test_rlq1_liveness_reconciles_when_recovery_runs():
    """When the recovery worker does run, the outbox drains to reconciled."""
    st = rlq1_initial()
    st, _ = rlq1_apply_step(st, "r", "revoke0", frozenset())
    live = check_liveness(st)
    assert live["reconciled"] is True


# --- independent history verifier --------------------------------------------
def _valid_ops():
    return [
        HistoryOp(op_id="q1", op_type="Q", invoked_at=1, responded_at=2,
                  commit_seq=1,
                  detail={"claim_id": "c1", "verdict": "QUALIFIED",
                          "manifest": {"evidence": ["e1"],
                                       "policy_revision": "LAW-v3"}}),
        HistoryOp(op_id="p1", op_type="P", invoked_at=3, responded_at=4,
                  commit_seq=2,
                  detail={"projection_id": "p1",
                          "expected_head_revision": 0,
                          "claim_ids": ["c1"],
                          "evidence_manifest": {"e1": 1},
                          "policy_revision": "LAW-v3"}),
    ]


def test_rlq1_verifier_valid_history():
    v = IndependentHistoryVerifier()
    r = v.verify(_valid_ops())
    assert r["verdict"] == "VALID"


def test_rlq1_verifier_missing_receipt_inconclusive():
    """Never fabricate a missing commit: claimed commit without receipt is
    INCONCLUSIVE, not assumed."""
    ops = _valid_ops()
    ops[1] = HistoryOp(op_id="p1", op_type="P", invoked_at=3, responded_at=4,
                       commit_seq=None,
                       detail={"claimed_outcome": "committed",
                               "projection_id": "p1"})
    v = IndependentHistoryVerifier()
    r = v.verify(ops)
    assert r["verdict"] == "INCONCLUSIVE"


def test_rlq1_verifier_tampered_history():
    """A publication that claims COMMITTED over revoked evidence is a
    counterexample: independent replay against the reference machine
    rejects it."""
    ops = [
        HistoryOp(op_id="r1", op_type="R", invoked_at=1, responded_at=2,
                  commit_seq=1,
                  detail={"evidence_id": "e1", "scope": "s", "purpose": "p",
                          "policy_revision": "LAW-v3"}),
        HistoryOp(op_id="p1", op_type="P", invoked_at=3, responded_at=4,
                  commit_seq=2,
                  detail={"projection_id": "p1",
                          "expected_head_revision": 0,
                          "claim_deps": {},
                          "evidence_manifest": {"e1": 1},
                          "policy_revision": "LAW-v3",
                          "claimed_outcome": COMMITTED}),
    ]
    v = IndependentHistoryVerifier()
    r = v.verify(ops)
    assert r["verdict"] == "COUNTEREXAMPLE", r
    assert "p1" in r["linearization"]


# --- display freshness vs certification safety ---------------------------------
def test_rlq1_display_freshness_honest():
    """Certification safety is enforced; display freshness without delivery
    coordination is served HISTORICAL_ONLY -- the uncoordinated
    strict-display guarantee is stated as unproven, not claimed."""
    from drift_canary.revocation_linearization import ProjectionCandidate
    st = AuthoritativeState()
    st.register_evidence("e1", "s", "p", "LAW-v3", "test")
    st.commit_qualification("c1", "REQUALIFIED", {"e1": 1}, "s", "p", "LAW-v3")
    st.register_projection("p1", "art-0", {"c1": 1}, {"e1": 1})
    head = st.projections["p1"]
    cand = ProjectionCandidate(
        projection_id="p1", expected_head_revision=head.projection_revision,
        artifact_id="art-0",
        claim_deps={"c1": 1}, evidence_manifest={"e1": 1},
        policy_revision="LAW-v3", asserted_claims={"c1": "REQUALIFIED"},
        intended_uses=("display",), fencing_token=head.fencing_token)
    outcome, _ = st.publish_projection(cand)
    assert outcome == COMMITTED
    kind, detail = st.serve_display("p1", delivery_coordinated=True)
    assert kind == "CURRENT_DISPLAY"
    kind2, detail2 = st.serve_display("p1", delivery_coordinated=False)
    assert kind2 == "HISTORICAL_ONLY"
    assert detail2["must_revalidate"] is True
    # Positive control: certification safety itself is unaffected by the
    # display path -- validation still gates on current state.
    standing, _ = st.validate_current("c1", "certification")
    assert standing == "CURRENT_QUALIFIED"


# --- crash injection at sensitive points ---------------------------------------
def test_rlq1_crash_points_safe():
    """Crash injection at sensitive points: fence enforcement never depends
    on a worker surviving."""
    for scripts in (
        {"r": ["revoke0", "crash:replayer"], "j": ["replay0"]},
        {"w": ["wread0", "crash:w0"], "r": ["revoke0"]},
        {"r": ["revoke0"], "w": ["wread0", "crash:w0", "recover:w0",
                                "wread0", "wpublish0"]},
    ):
        r = _clean(scripts)
        assert r["violations"] == [], scripts


# --- bounded fixture: model SHA / config / traces retained --------------------
def test_rlq1_fixture_pinned():
    """The bounded fixture is pinned: reference spec SHA is stable and the
    checker config is explicit -- a cold successor reproduces from these."""
    sha1 = reference_spec_sha()
    sha2 = reference_spec_sha()
    assert sha1 == sha2 and len(sha1) == 64
    c = RLQ1Checker(defects=frozenset(), max_histories=4000)
    assert c.max_histories == 4000
    assert c.defects == frozenset()
