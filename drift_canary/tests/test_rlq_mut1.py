"""RLQ-MUT-1 adversarial mutation tests (SN-0788): every critical
revocation safeguard must be independently falsifiable. Four mutation
families, one boundary each -- baseline first, each mutant independently,
then compounds. Only KILLED meets the detection objective."""
import pytest

from drift_canary.revocation_linearization import (
    MUTATION_FAMILIES,
    COMPOUND_MUTANTS,
    MUTANTS,
    RLQ1Checker,
    AuthoritativeState,
    ProjectionCandidate,
    COMMITTED,
    STALE_DEPENDENCY,
    KILLED,
    BLOCKED_BY_REDUNDANT_GUARD,
    SURVIVED_UNEXPLAINED,
    UNREACHABLE,
    UNKNOWN,
    qualify_mutation,
    prove_redundant_guard,
    find_shortest_violation,
    causally_reduce,
    replay_via_scripts,
    build_receipt,
    reproduce_from_receipt,
    reference_spec_sha,
    rlq1_op_violations,
)

# Targeted activation scripts: each exercises its family's defective branch.
FAMILY_SCRIPTS = {
    "M1": {"w0": ["wread0"], "r": ["revoke0"], "w1": ["wread1", "wpublish1"]},
    "M2": {"v": ["validate"], "r": ["revoke0"], "a": ["act"]},
    "M3": {"r": ["revoke0"]},
    "M4": {"r": ["revoke0"], "j": ["replay0"]},
}

# Compound scripts chosen so every mutated boundary is exercised.
COMPOUND_SCRIPTS = {
    "M1+M3": {"w0": ["wread0"], "r": ["revoke0"], "w1": ["wread1", "wpublish1"]},
    "M1+M4": {"w0": ["wread0"], "r": ["revoke0"], "w1": ["wread1", "wpublish1"],
              "j": ["replay0"]},
    "M2+M3": {"w0": ["wread0"], "r": ["revoke0"], "a": ["act"]},
    "M2+M4": {"r": ["revoke0"], "a": ["act"], "j": ["replay0"]},
    "M1+M2+M4": {"w0": ["wread0"], "r": ["revoke0"],
                 "w1": ["wread1", "wpublish1"], "a": ["act"], "j": ["replay0"]},
}


# --- 1+2. Four families, each KILLED with its expected shape ------------------
@pytest.mark.parametrize("mid", ["M1", "M2", "M3", "M4"])
def test_mut_family_killed(mid):
    """M1 first (smallest model, central boundary), then M2/M3/M4: the
    checker MUST produce a counterexample for each deliberately defective
    implementation. A mutant that passes is a failed specification."""
    res = qualify_mutation(mid, FAMILY_SCRIPTS[mid])
    assert res["verdict"] == KILLED, res
    assert res["property"] == MUTATION_FAMILIES[mid]["expected_property"]
    assert res["exercised"] is True
    assert res["independently_replayed"] is True


def test_m1_shape_stale_publication():
    """M1 history: writer read at rev 17, revocation committed rev 18,
    stale write committed anyway."""
    res = qualify_mutation("M1", FAMILY_SCRIPTS["M1"])
    labels = res["minimal_history"]
    assert labels[0].startswith("R(") and labels[-1].endswith("=committed")
    assert any("wread" in l for l in labels)


def test_m2_shape_action_on_pre_revocation_validation():
    """M2 history: validation qualified before R, revocation fenced,
    action executed on revoked support."""
    res = qualify_mutation("M2", FAMILY_SCRIPTS["M2"])
    assert res["minimal_history"][-1] == "A=committed"


def test_m3_shape_revision_reused():
    """M3 history: the revocation reuses the old revision (ABA) -- the
    invariant is violated even though certification safety holds."""
    res = qualify_mutation("M3", FAMILY_SCRIPTS["M3"])
    assert res["property"] == "S4"
    assert res["minimal_history"] == ("R(ev0)",)


def test_m4_shape_blind_replay_rollback():
    """M4 history: delayed replay of the revocation event rolls back the
    canonical state that moved on."""
    res = qualify_mutation("M4", FAMILY_SCRIPTS["M4"])
    assert res["minimal_history"][-1] == "J(blind-overwrite)"


def test_mutant_positive_control_baseline_first():
    """Baseline first: the reference implementation is clean on every
    family script -- the violations come from the mutations alone."""
    for mid, scripts in FAMILY_SCRIPTS.items():
        r = RLQ1Checker(defects=frozenset(), max_histories=4000).check(scripts)
        assert r["violations"] == [], f"{mid} baseline: {r['violations']}"


# --- 3. Independent oracle separation ------------------------------------------
def test_oracle_immutable_across_mutants():
    """The mutation NEVER touches the correctness definition: the
    reference spec SHA is identical before, during, and after every
    mutant run, and the per-op oracle is the same function object."""
    before = reference_spec_sha()
    for mid in MUTATION_FAMILIES:
        qualify_mutation(mid, FAMILY_SCRIPTS[mid])
        assert reference_spec_sha() == before
        assert rlq1_op_violations.__module__ == \
            "drift_canary.revocation_linearization"


# --- 4. Reachability + the five verdicts ---------------------------------------
def test_verdict_blocked_by_redundant_guard():
    """M3 on the S1 dimension: exercised, exhaustive, no S1 violation --
    and the guard-removal probe independently verifies the eligibility
    check is what blocks it (distinguished from unexercised/masked)."""
    res = qualify_mutation("M3", FAMILY_SCRIPTS["M1"], property_override="S1")
    assert res["verdict"] == BLOCKED_BY_REDUNDANT_GUARD
    assert "eligibility" in res["redundant_guard"]
    assert res["verification"]["mutant_alone_S1_violations"] == 0
    assert res["verification"]["mutant_plus_guard_removed_S1_violations"] > 0


def test_verdict_survived_unexplained():
    """M1 on the S4 dimension: defect exercised, exhaustive, no violation,
    no redundant guard -- M1 simply does not touch revisions."""
    res = qualify_mutation("M1", FAMILY_SCRIPTS["M1"], property_override="S4")
    assert res["verdict"] == SURVIVED_UNEXPLAINED


def test_verdict_unreachable():
    """M4 with no replay step in the scripts: the defective branch is
    never exercised -- UNREACHABLE, not 'safe'."""
    res = qualify_mutation("M4", {"r": ["revoke0"]})
    assert res["verdict"] == UNREACHABLE


def test_verdict_unknown_on_cap():
    """Exploration cut short by the cap: UNKNOWN, never a clean bill."""
    res = qualify_mutation("M1", FAMILY_SCRIPTS["M1"], max_histories=0)
    assert res["verdict"] == UNKNOWN


# --- 5. Two-stage minimization --------------------------------------------------
def test_minimization_shortest_and_causal():
    """Stage 1 (BFS) finds the shortest violating trace; stage 2 (causal
    reduction) drops irrelevant steps while the violation persists."""
    defects = MUTATION_FAMILIES["M2"]["defects"]
    scripts = {"v": ["validate"], "r": ["revoke0"], "a": ["act"],
               "w": ["wread0", "wpublish0"]}
    steps, infos = find_shortest_violation(scripts, defects, "S3")
    assert steps is not None
    # The minimized trace is genuinely minimal for this fixture.
    assert len(steps) == 2

    # Causal reduction: pad with irrelevant steps, reduce back while the
    # violation persists.
    padded = [("w", "wread0"), ("v", "validate")] + steps
    reduced = causally_reduce(
        padded,
        lambda seq: replay_via_scripts(list(seq), defects, "S3"))
    assert len(reduced) <= len(padded)
    assert replay_via_scripts(list(reduced), defects, "S3")


# --- 7. Counterexample receipts: cold reproduction ------------------------------
def test_receipt_cold_reproduction():
    """A cold successor regenerates the failure from the receipt alone:
    oracle SHA pinned, minimal steps replayed on a fresh instance."""
    for mid in ("M1", "M2", "M3", "M4"):
        res = qualify_mutation(mid, FAMILY_SCRIPTS[mid])
        receipt = build_receipt(res, mid, FAMILY_SCRIPTS[mid])
        assert receipt.qualification == "RLQ-MUT-1"
        assert receipt.verdict == KILLED
        assert receipt.reference_sha == reference_spec_sha()
        assert len(receipt.reference_sha) == 64
        assert reproduce_from_receipt(receipt) is True


def test_receipt_rejects_oracle_drift():
    """If the reference oracle drifts, the receipt refuses to reproduce --
    never certify against a different correctness definition."""
    res = qualify_mutation("M1", FAMILY_SCRIPTS["M1"])
    receipt = build_receipt(res, "M1", FAMILY_SCRIPTS["M1"])
    drifted = receipt.__class__(**{**receipt.__dict__,
                                   "reference_sha": "0" * 64})
    assert reproduce_from_receipt(drifted) is False


# --- 8. Compound mutations -------------------------------------------------------
@pytest.mark.parametrize("cid", sorted(COMPOUND_MUTANTS))
def test_compound_mutant_violates(cid):
    """After isolated pass: M1+M3, M1+M4, M2+M3, M2+M4, M1+M2+M4 --
    coverage per mutated boundary, targeted scenarios."""
    defects = COMPOUND_MUTANTS[cid]
    scripts = COMPOUND_SCRIPTS[cid]
    r = RLQ1Checker(defects=defects, max_histories=4000).check(scripts)
    assert r["exhausted"]
    assert r["violations"], f"{cid}: compound produced no violation"
    # Every mutated boundary in the compound is covered by at least one
    # violated property family.
    props = {v[0] for v in r["violations"]}
    if "M1_no_publish_guard" in defects or "M2_no_action_fence" in defects:
        assert props & {"S1", "S3"}, f"{cid}: {props}"
    if "M5_rev_reuse" in defects:
        assert "S4" in props, f"{cid}: {props}"
    if "M4_blind_replay" in defects:
        assert "S5" in props or "S4" in props, f"{cid}: {props}"


# --- 9. Runtime integration: pause-and-release against actual storage ------------
def _runtime_state():
    st = AuthoritativeState()
    st.register_evidence("e1", "s", "p", "LAW-v3", "test")
    st.commit_qualification("c1", "REQUALIFIED", {"e1": 1}, "s", "p", "LAW-v3")
    st.register_projection("p1", "art-0", {"c1": 1}, {"e1": 1})
    return st


def _candidate_for(st):
    head = st.projections["p1"]
    return ProjectionCandidate(
        projection_id="p1", expected_head_revision=head.projection_revision,
        artifact_id="art-0", claim_deps={"c1": 1}, evidence_manifest={"e1": 1},
        policy_revision="LAW-v3", asserted_claims={"c1": "REQUALIFIED"},
        intended_uses=("certification",), fencing_token=head.fencing_token)


def test_runtime_pause_writer_release_after_revoke():
    """Pause-and-release 1: writer builds its candidate (read at rev 17),
    PAUSES; revocation commits (rev 18); writer released -- the stale
    candidate is rejected, never committed."""
    st = _runtime_state()
    cand = _candidate_for(st)  # read at rev 17 -- then PAUSE
    st.commit_revocation("e1", "test", "s", "p", "LAW-v3", "test")  # rev 18
    outcome, detail = st.publish_projection(cand)  # RELEASE
    assert outcome == STALE_DEPENDENCY, (outcome, detail)


def test_runtime_pause_validate_release_after_revoke():
    """Pause-and-release 2: validation qualified before R; after R the
    action boundary revalidates -- the action is rejected."""
    st = _runtime_state()
    standing, _ = st.validate_current("c1", "certification")
    assert standing == "CURRENT_QUALIFIED"  # PAUSE on this verdict
    st.commit_revocation("e1", "test", "s", "p", "LAW-v3", "test")
    outcome, detail = st.commit_action("a1", ["c1"], True)  # RELEASE
    assert outcome == "REJECTED", (outcome, detail)


def test_runtime_pause_action_release_after_revoke():
    """Pause-and-release 3: action authorized pre-revocation in the
    caller's head; revocation lands first; commit re-checks at the
    boundary -- rejected."""
    st = _runtime_state()
    st.commit_revocation("e1", "test", "s", "p", "LAW-v3", "test")
    outcome, _ = st.commit_action("a1", ["c1"], True)
    assert outcome == "REJECTED"
    # Positive control: without the revocation the same action authorizes.
    st2 = _runtime_state()
    outcome2, _ = st2.commit_action("a1", ["c1"], True)
    assert outcome2 == "AUTHORIZED"


def test_runtime_pause_replay_release_after_second_revoke():
    """Pause-and-release 4: recovery holds a revocation event; a second
    revocation advances canonical state; the delayed event reconciles to
    current -- never rolls back. Honest limitation: successful traces are
    evidence, not universal safety; the model + refinement argument
    carries the general claim."""
    st = _runtime_state()
    r1 = st.commit_revocation("e1", "first", "s", "p", "LAW-v3", "test")
    rev_after_first = st.evidence["e1"].eligibility_revision
    st.register_evidence("e2", "s", "p", "LAW-v3", "test")
    st.commit_revocation("e2", "second", "s", "p", "LAW-v3", "test")
    # The delayed first-revocation event replays now (out-of-order/dup).
    outcome, _ = st.replay_event({"event_id": r1.event_id, "kind": "revocation",
                                  "evidence_id": "e1", "scope": "s",
                                  "purpose": "p", "seq": 1,
                                  "eligibility_revision":
                                      r1.eligibility_revision})
    assert st.evidence["e1"].eligibility_revision >= rev_after_first
    assert outcome in ("NOOP_DUPLICATE", "RECONCILED", "NOOP_CURRENT",
                       "NOOP_STALE")


# --- 10. Hard-gate scorecard: no averaging ---------------------------------------
def test_hard_gate_scorecard():
    """Ten gates, each pass/fail independently -- no averaging. One NO
    anywhere and the qualification does not ship."""
    gates = {}

    # G1: reference oracle immutable across all mutant runs.
    sha = reference_spec_sha()
    for mid in MUTATION_FAMILIES:
        qualify_mutation(mid, FAMILY_SCRIPTS[mid])
    gates["G1_oracle_immutable"] = (reference_spec_sha() == sha)

    # G2-G5: M1..M4 KILLED, minimal, independently replayed.
    for i, mid in enumerate(["M1", "M2", "M3", "M4"], start=2):
        res = qualify_mutation(mid, FAMILY_SCRIPTS[mid])
        gates[f"G{i}_{mid}_killed_replayed"] = (
            res["verdict"] == KILLED and res["exercised"]
            and res["independently_replayed"])

    # G6: redundant-guard blocking distinguished from unexercised/masked.
    res = qualify_mutation("M3", FAMILY_SCRIPTS["M1"], property_override="S1")
    gates["G6_redundant_guard_distinguished"] = (
        res["verdict"] == BLOCKED_BY_REDUNDANT_GUARD
        and res["verification"]["mutant_plus_guard_removed_S1_violations"] > 0)

    # G7: compound coverage -- every boundary violated somewhere.
    covered = set()
    for cid, defects in COMPOUND_MUTANTS.items():
        r = RLQ1Checker(defects=defects,
                        max_histories=4000).check(COMPOUND_SCRIPTS[cid])
        covered |= {v[0] for v in r["violations"]}
    gates["G7_compound_coverage"] = {"S1", "S3", "S4", "S5"} <= covered

    # G8: no fairness/recovery assumptions in the safety checker -- the
    # safety entry points take no scheduler/fairness parameter, and
    # liveness lives in a separate function.
    import inspect
    sig = inspect.signature(RLQ1Checker.check)
    sig2 = inspect.signature(find_shortest_violation)
    params = (list(sig.parameters) + list(sig2.parameters))
    gates["G8_no_fairness_assumptions"] = not any(
        p in ("fair", "fairness", "scheduler", "assume_recovery")
        for p in params)

    # G9: receipts regenerable by a cold successor.
    ok = True
    for mid in MUTATION_FAMILIES:
        res = qualify_mutation(mid, FAMILY_SCRIPTS[mid])
        ok = ok and reproduce_from_receipt(build_receipt(
            res, mid, FAMILY_SCRIPTS[mid]))
    gates["G9_receipts_reproducible"] = ok

    # G10: baseline clean -- mutants are the only source of violations.
    ok = True
    for scripts in list(FAMILY_SCRIPTS.values()) + \
            list(COMPOUND_SCRIPTS.values()):
        r = RLQ1Checker(defects=frozenset(), max_histories=4000).check(scripts)
        ok = ok and (r["violations"] == [])
    gates["G10_baseline_clean"] = ok

    failed = [g for g, passed in gates.items() if not passed]
    assert not failed, f"hard gates failed (no averaging): {failed}"
    assert len(gates) == 10
