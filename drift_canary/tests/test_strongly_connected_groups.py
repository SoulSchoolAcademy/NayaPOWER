"""Tests for D65 / AER-LIVE-10: strongly connected invariant groups.

Every property the verifier claims is COMPUTED from the presented
transition relation -- the suite's negative controls prove the verifier
cannot be talked into a verdict: sabotage the model and the verdict must
change. The naive spec baseline (PR #2209) is proven wrong, not inherited.
"""

import pytest

from drift_canary.strongly_connected_groups import (
    KIND_COMPLETE,
    KIND_ORDINARY,
    KIND_REPLENISH,
    KIND_RESERVE,
    JointDeclaration,
    JointTransition,
    JointVerdict,
    Verdict,
    _NaiveJointProof,
    _NaiveSCCGroup,
    _NaiveSCCVerdict,
    canonical_model_encoding,
    condensation_order,
    make_declaration,
    model_digest_of,
    naive_verify_scc,
    tarjan_scc,
    verify_joint,
)

BUDGET = "budget"
RESOURCE = "resource"
REPLENISH = "replenishment"
LIFECYCLE = "lifecycle"
MEMBERS = (BUDGET, RESOURCE, REPLENISH, LIFECYCLE)

# Circular prerequisite topology: budget->lifecycle->replenishment->resource->budget.
CYCLE_PREREQ = {
    BUDGET: (LIFECYCLE,),
    RESOURCE: (BUDGET,),
    REPLENISH: (RESOURCE,),
    LIFECYCLE: (REPLENISH,),
}

S0 = "s0_allocated"
S1 = "s1_drawn"
S2 = "s2_replenished"
S3 = "s3_released"
S4 = "s4_exited"


def cycle_transitions(progress=1, with_exit=True, auth="treasury:auth-001"):
    ts = [
        JointTransition(S0, S1, KIND_ORDINARY, progress),
        JointTransition(S1, S2, KIND_REPLENISH, progress, authorization=auth),
        JointTransition(S2, S3, KIND_ORDINARY, progress),
        JointTransition(S3, S0, KIND_ORDINARY, progress),
    ]
    if with_exit:
        ts.append(JointTransition(S3, S4, KIND_COMPLETE, progress))
    return ts


def good_declaration(**over):
    kw = dict(
        name="AER-LIVE-010-SCC",
        members=MEMBERS,
        declared_by="treasury",
        prereq=CYCLE_PREREQ,
        initial_states={S0},
        authorized_initial={S0},
        transitions=cycle_transitions(),
        exit_states={S4},
    )
    kw.update(over)
    return make_declaration(**kw)


# ---------------------------------------------------------------------------
# Tarjan SCC: the verifier's own decomposition
# ---------------------------------------------------------------------------

def test_tarjan_finds_the_4_cycle():
    sccs = tarjan_scc(CYCLE_PREREQ)
    assert sccs == [frozenset(MEMBERS)]


def test_tarjan_disjoint_cycles():
    g = {"a": ("b",), "b": ("a",), "c": ("d",), "d": ("c",)}
    sccs = tarjan_scc(g)
    assert sorted(map(sorted, sccs)) == [["a", "b"], ["c", "d"]]


def test_tarjan_chain_gives_singletons():
    g = {"a": ("b",), "b": ("c",), "c": ()}
    sccs = tarjan_scc(g)
    assert sorted(map(sorted, sccs)) == [["a"], ["b"], ["c"]]


def test_tarjan_self_loop_is_a_cycle():
    assert tarjan_scc({"solo": ("solo",)}) == [frozenset({"solo"})]


def test_tarjan_includes_dep_only_nodes():
    sccs = tarjan_scc({"a": ("ghost",)})
    assert frozenset({"ghost"}) in sccs


def test_tarjan_deterministic():
    g = {"x": ("y", "z"), "y": ("z",), "z": ("x",), "w": ("x",)}
    assert tarjan_scc(g) == tarjan_scc(g)


# ---------------------------------------------------------------------------
# Condensation order: prerequisites first, never ranking within a component
# ---------------------------------------------------------------------------

def test_condensation_prerequisites_first():
    g = {"a": ("b",), "b": ("c",), "c": ("b",)}  # {b,c} cycle, a depends on it
    order = condensation_order(g)
    assert order == [frozenset({"b", "c"}), frozenset({"a"})]


def test_condensation_chain_order():
    order = condensation_order({"a": ("b",), "b": ("c",), "c": ()})
    assert order == [frozenset({"c"}), frozenset({"b"}), frozenset({"a"})]


def test_condensation_keeps_component_together():
    # The SCC is never split or internally ranked: one entry, all members.
    order = condensation_order(CYCLE_PREREQ)
    assert order == [frozenset(MEMBERS)]


# ---------------------------------------------------------------------------
# AER-LIVE-010 decisive pair: same topology, different initial conditions
# ---------------------------------------------------------------------------

def test_scc01_no_authorized_initial_refuses_with_minimal_obstruction():
    decl = good_declaration(authorized_initial=frozenset())
    v = verify_joint(decl)
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    # Minimal: exactly the failed grounding facts, nothing else.
    assert set(v.obstruction) == {
        "no authorized initial allocation: the joint cycle cannot start",
        "initial state(s) lack authorization: s0_allocated",
    }
    assert v.exhibited_cycle == ()
    assert v.deadlock_state is None


def test_scc02_authorized_initial_proves_strategy_and_exhibits_exit():
    v = verify_joint(good_declaration())
    assert v.verdict == Verdict.EXIT_POSSIBLE_NOT_GUARANTEED
    # The strategy is proven: a positive-progress cycle in the kernel.
    assert v.exhibited_cycle
    assert v.exhibited_cycle[0] == v.exhibited_cycle[-1]
    assert set(v.exhibited_cycle[:-1]) <= set(v.kernel)
    assert v.cycle_progress > 0
    # ...and the exit is constructed, not merely claimed.
    assert v.exit_path[0] in v.kernel
    assert v.exit_path[-1] == S4
    assert v.deadlock_state is None
    assert not v.safety_violations


def test_closed_cycle_without_exit_is_repeatable_proven():
    decl = good_declaration(
        transitions=cycle_transitions(with_exit=False), exit_states=frozenset())
    v = verify_joint(decl)
    assert v.verdict == Verdict.REPEATABLE_PROVEN
    assert v.cycle_progress > 0
    assert v.exit_path == ()


def test_verdict_qualifies_the_model():
    v = verify_joint(good_declaration())
    assert v.model_digest == model_digest_of(good_declaration())
    assert len(v.model_digest) == 64


# ---------------------------------------------------------------------------
# Liveness: deadlock in scope, livelock counterexample
# ---------------------------------------------------------------------------

def test_deadlock_in_scope_names_the_state():
    ts = [
        JointTransition(S0, S1, KIND_ORDINARY, 1),
        JointTransition(S1, S2, KIND_REPLENISH, 1, authorization="treasury:a"),
    ]  # S2: reachable, no outgoing, not an exit.
    v = verify_joint(good_declaration(transitions=ts, exit_states=frozenset()))
    assert v.verdict == Verdict.DEADLOCK_IN_SCOPE
    assert v.deadlock_state == S2


def test_declared_exit_is_not_a_deadlock():
    v = verify_joint(good_declaration())  # S4 terminal AND declared exit
    assert v.verdict != Verdict.DEADLOCK_IN_SCOPE


def test_zero_progress_spin_is_livelock_not_repeatable():
    decl = good_declaration(
        transitions=cycle_transitions(progress=0, with_exit=False),
        exit_states=frozenset(),
    )
    v = verify_joint(decl)
    assert v.verdict == Verdict.LIVELOCK_COUNTEREXAMPLE
    assert v.exhibited_cycle  # the counterexample: it spins without advancing
    assert v.cycle_progress <= 0


def test_kernel_excludes_terminal_branches():
    v = verify_joint(good_declaration())
    assert S4 not in v.kernel  # terminal: eliminated by the GFP
    assert set(v.kernel) == {S0, S1, S2, S3}


# ---------------------------------------------------------------------------
# Safety closure: cross-relationships no member can hold alone
# ---------------------------------------------------------------------------

def test_replenish_without_authorization_violates_safety():
    ts = cycle_transitions(auth=None)
    v = verify_joint(good_declaration(transitions=ts))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("without authorization" in s for s in v.safety_violations)


def test_replenish_authorized_by_a_member_violates_safety():
    ts = cycle_transitions(auth="budget:self-issued")
    v = verify_joint(good_declaration(transitions=ts))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("must be external" in s for s in v.safety_violations)


def test_reserve_without_capacity_and_ownership_violates_safety():
    ts = list(cycle_transitions(with_exit=False)) + [
        JointTransition(S0, S1, KIND_RESERVE, 1),  # no capacity, no owner
    ]
    v = verify_joint(good_declaration(transitions=ts, exit_states=frozenset()))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("capacity and ownership" in s for s in v.safety_violations)


def test_reserve_with_capacity_and_ownership_passes():
    ts = list(cycle_transitions(with_exit=False)) + [
        JointTransition(S0, S1, KIND_RESERVE, 1, capacity="10", owner="ops"),
    ]
    v = verify_joint(good_declaration(transitions=ts, exit_states=frozenset()))
    assert v.verdict == Verdict.REPEATABLE_PROVEN


def test_unknown_transition_kind_violates_safety():
    ts = [JointTransition(S0, S1, "teleport", 1)]
    decl = make_declaration(
        name="weird", members=("a",), declared_by="ext",
        prereq={"a": ("a",)}, initial_states={"s"}, authorized_initial={"s"},
        transitions=[JointTransition("s", "t", "teleport", 0)],
        exit_states=frozenset(),
    )
    v = verify_joint(decl)
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("unknown kind" in s for s in v.safety_violations)


def test_declared_exit_must_be_terminal():
    ts = cycle_transitions() + [JointTransition(S4, S0, KIND_ORDINARY, 0)]
    v = verify_joint(good_declaration(transitions=ts))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("not terminal" in o for o in v.obstruction)


# ---------------------------------------------------------------------------
# The group never establishes its own external facts
# ---------------------------------------------------------------------------

def test_authority_may_not_be_a_member():
    v = verify_joint(good_declaration(declared_by=BUDGET))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("would establish its own external facts" in o for o in v.obstruction)


def test_digest_mismatch_refuses():
    honest = good_declaration()
    tampered = JointDeclaration(
        **{**honest.__dict__,
           "transitions": honest.transitions + (JointTransition(S0, S4, KIND_COMPLETE, 9),)})
    # digest still the honest one: the model drifted under the authorization.
    v = verify_joint(tampered)
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("digest mismatch" in o for o in v.obstruction)


def test_empty_membership_refused():
    decl = make_declaration(
        name="empty", members=(), declared_by="ext", prereq={},
        initial_states=set(), authorized_initial=set(), transitions=(),
    )
    v = verify_joint(decl)
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert v.obstruction == ("empty membership: a joint group needs at least one member",)


def test_spurious_joint_not_an_scc_refused():
    v = verify_joint(good_declaration(members=(BUDGET, RESOURCE)))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("not one strongly connected component" in o for o in v.obstruction)


def test_singleton_without_self_loop_is_no_joint_cycle():
    decl = make_declaration(
        name="single", members={"budget"}, declared_by="ext",
        prereq={"budget": (), "other": ("budget",)},
        initial_states={"s"}, authorized_initial={"s"},
        transitions=[JointTransition("s", "s", KIND_ORDINARY, 1)],
    )
    v = verify_joint(decl)
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert any("no self-dependency" in o for o in v.obstruction)


def test_self_loop_singleton_is_a_joint_cycle():
    decl = make_declaration(
        name="solo", members={"solo"}, declared_by="ext",
        prereq={"solo": ("solo",)},
        initial_states={"s"}, authorized_initial={"s"},
        transitions=[JointTransition("s", "s", KIND_ORDINARY, 2)],
    )
    v = verify_joint(decl)
    assert v.verdict == Verdict.REPEATABLE_PROVEN


def test_canonical_encoding_is_byte_stable():
    a = canonical_model_encoding(good_declaration())
    b = canonical_model_encoding(good_declaration())
    assert a == b


# ---------------------------------------------------------------------------
# The naive spec baseline is proven wrong, not inherited
# ---------------------------------------------------------------------------

def test_naive_trusts_caller_booleans_with_no_transition_relation():
    # No transition relation exists anywhere in this call -- yet the naive
    # verifier certifies the cycle repeatable on the caller's bare booleans.
    group = _NaiveSCCGroup(
        members=MEMBERS,
        initial_state_authorized=True, transitions_valid=True,
        replenishment_lawful=True, resource_conserved=True, lifecycle_valid=True,
    )
    assert naive_verify_scc(group, _NaiveJointProof(True, True, True, True)) == \
        _NaiveSCCVerdict.REPEATABLE_CYCLE_PROVEN


def test_naive_cannot_express_who_grounded_the_group():
    import dataclasses
    fields = {f.name for f in dataclasses.fields(_NaiveSCCGroup)}
    assert "declared_by" not in fields  # self-certification is unpreventable
    # ...while the real verifier refuses a self-declared authority.
    v = verify_joint(good_declaration(declared_by=RESOURCE))
    assert v.verdict == Verdict.JOINT_UNDETERMINED


def test_naive_has_no_progress_check():
    group = _NaiveSCCGroup(
        members=MEMBERS,
        initial_state_authorized=True, transitions_valid=True,
        replenishment_lawful=True, resource_conserved=True, lifecycle_valid=True,
    )
    assert naive_verify_scc(group, _NaiveJointProof(True, True, True, True)) == \
        _NaiveSCCVerdict.REPEATABLE_CYCLE_PROVEN
    # The same shape with a zero-progress cycle is livelock, not repeatable.
    decl = good_declaration(
        transitions=cycle_transitions(progress=0, with_exit=False),
        exit_states=frozenset(),
    )
    assert verify_joint(decl).verdict == Verdict.LIVELOCK_COUNTEREXAMPLE


def test_naive_conflates_exit_with_repeatable():
    group = _NaiveSCCGroup(
        members=MEMBERS,
        initial_state_authorized=True, transitions_valid=True,
        replenishment_lawful=True, resource_conserved=True, lifecycle_valid=True,
    )
    # repeatability AND exit viability -> naive swallows the exit dimension.
    assert naive_verify_scc(group, _NaiveJointProof(True, True, True, True)) == \
        _NaiveSCCVerdict.REPEATABLE_CYCLE_PROVEN
    # The real verdicts stay separate: the exit is exhibited, never guaranteed.
    v = verify_joint(good_declaration())
    assert v.verdict == Verdict.EXIT_POSSIBLE_NOT_GUARANTEED
    assert v.exit_path


def test_naive_refusal_carries_no_obstruction():
    group = _NaiveSCCGroup(
        members=MEMBERS,
        initial_state_authorized=False,  # SCC-01: no authorized initial
        transitions_valid=True, replenishment_lawful=True,
        resource_conserved=True, lifecycle_valid=True,
    )
    result = naive_verify_scc(group, _NaiveJointProof(True, True, True, True))
    assert result == _NaiveSCCVerdict.JOINT_PROOF_UNDETERMINED
    # A bare enum: nothing names what is missing. The real refusal is minimal
    # AND explicit.
    v = verify_joint(good_declaration(authorized_initial=frozenset()))
    assert v.verdict == Verdict.JOINT_UNDETERMINED
    assert len(v.obstruction) == 2


# ---------------------------------------------------------------------------
# Sabotage controls: break the model, the verdict must move
# ---------------------------------------------------------------------------

def test_sabotage_kill_progress_turns_repeatable_into_livelock():
    honest = verify_joint(good_declaration(
        transitions=cycle_transitions(with_exit=False), exit_states=frozenset()))
    assert honest.verdict == Verdict.REPEATABLE_PROVEN
    sabotaged = verify_joint(good_declaration(
        transitions=cycle_transitions(progress=0, with_exit=False),
        exit_states=frozenset()))
    assert sabotaged.verdict == Verdict.LIVELOCK_COUNTEREXAMPLE


def test_sabotage_drop_authorization_turns_exit_into_undetermined():
    honest = verify_joint(good_declaration())
    assert honest.verdict == Verdict.EXIT_POSSIBLE_NOT_GUARANTEED
    sabotaged = verify_joint(good_declaration(transitions=cycle_transitions(auth=None)))
    assert sabotaged.verdict == Verdict.JOINT_UNDETERMINED
    assert sabotaged.safety_violations


def test_sabotage_break_the_cycle_turns_joint_into_deadlock():
    ts = [
        JointTransition(S0, S1, KIND_ORDINARY, 1),
        JointTransition(S1, S2, KIND_REPLENISH, 1, authorization="treasury:a"),
        # S2->S3 removed: the joint cycle no longer closes.
    ]
    v = verify_joint(good_declaration(transitions=ts, exit_states=frozenset()))
    assert v.verdict == Verdict.DEADLOCK_IN_SCOPE
    assert v.deadlock_state == S2
