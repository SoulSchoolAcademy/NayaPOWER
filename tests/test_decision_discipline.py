"""Tests for the Decision Discipline Engine.

Proves: typed comparability never invents exchange rates, the hierarchy
protects rights first, escalation routing is precise, evidence and
authority stay separated, sequencing is safe, and escalation packets
are compact and complete.
"""
import pytest

from kernel.protocol.decision_discipline import (
    # Comparability
    DOMINATES, INCOMPARABLE, UNKNOWN, PROHIBITED,
    OutcomeDimension, DecisionOption,
    compare_options, eliminate_dominated,
    # Evidence / Authority
    NEEDS_EVIDENCE, NEEDS_AUTHORITY, NEEDS_BOTH,
    EVIDENCE_PENDING, EVIDENCE_SUFFICIENT, EVIDENCE_STALE,
    AUTHORITY_MISSING, AUTHORITY_GRANTED, AUTHORITY_EXPIRED,
    assess_requirements, execution_gate,
    # Sequencing
    SEQ_AUTHORITY_FIRST, SEQ_EVIDENCE_FIRST, SEQ_PARALLEL,
    SEQ_CONTAIN_ESCALATE,
    SequenceCase, choose_sequence,
    # Routing
    ROUTE_ACT, ROUTE_READ_MORE, ROUTE_ACT_EXPERIMENT, ROUTE_ASK,
    ROUTE_REFUSE, ROUTE_HOLD,
    RoutingCase, route_decision,
    five_question_routing,
    # Hierarchy
    STAGE_PROTECT_RIGHTS, STAGE_ELIMINATE_DOMINATED,
    STAGE_APPLY_PRIORITIES, STAGE_ESCALATE,
    run_decision_hierarchy,
    # Packets
    build_escalation_packet,
)
from kernel.protocol.typed_action import TypedAction, ADMISSIBLE


def _dim(name, lower, upper):
    return OutcomeDimension(name=name, lower=lower, upper=upper)


def _opt(oid, dims, action=None):
    return DecisionOption(option_id=oid, dimensions=tuple(dims),
                          law11_action=action)


def _clean_action(operation="read", environment="development",
                  resource="test_resource"):
    return TypedAction(
        actor_id="test", operation=operation, environment=environment,
        resource=resource, rights_safe=True, safety_safe=True,
        privacy_safe=True, consent_obtained=True,
    )


# ---------------------------------------------------------------------------
# 1. TYPED COMPARABILITY
# ---------------------------------------------------------------------------

class TestComparability:
    def test_dominates_all_dimensions_better(self):
        a = _opt("A", [_dim("speed", 4, 5), _dim("access", 1, 2)])
        b = _opt("B", [_dim("speed", 1, 2), _dim("access", 0, 0)])
        r = compare_options(a, b)
        assert r.verdict == DOMINATES
        assert r.winner_id == "A"

    def test_dominates_requires_strictly_better_on_one(self):
        # Identical exact values on all dimensions: no dominance, tie.
        # (Identical *intervals* would be UNKNOWN — honest uncertainty.)
        a = _opt("A", [_dim("speed", 2, 2)])
        b = _opt("B", [_dim("speed", 2, 2)])
        r = compare_options(a, b)
        assert r.verdict == INCOMPARABLE
        assert r.winner_id is None

    def test_identical_intervals_are_unknown_not_tie(self):
        # [2,3] vs [2,3]: true values could differ either way.
        # Claiming "tie" would be manufacturing certainty.
        a = _opt("A", [_dim("speed", 2, 3)])
        b = _opt("B", [_dim("speed", 2, 3)])
        r = compare_options(a, b)
        assert r.verdict == UNKNOWN

    def test_incomparable_distinct_advantages(self):
        # The canonical example: A faster, B more accessible.
        # Must NOT invent an exchange rate.
        a = _opt("A", [_dim("speed", 4, 4), _dim("access", 0, 0)])
        b = _opt("B", [_dim("speed", 2, 2), _dim("access", 3, 3)])
        r = compare_options(a, b)
        assert r.verdict == INCOMPARABLE
        assert r.winner_id is None
        assert "speed" in r.a_better
        assert "access" in r.b_better

    def test_unknown_on_overlapping_intervals(self):
        # Favorable point estimate with wide interval != dominance.
        a = _opt("A", [_dim("speed", 0, 10)])
        b = _opt("B", [_dim("speed", 4, 5)])
        r = compare_options(a, b)
        assert r.verdict == UNKNOWN
        assert "speed" in r.unknown_dims

    def test_unknown_on_missing_bounds(self):
        a = _opt("A", [OutcomeDimension(name="speed", lower=None, upper=5)])
        b = _opt("B", [_dim("speed", 1, 2)])
        r = compare_options(a, b)
        assert r.verdict == UNKNOWN

    def test_unknown_on_missing_dimension(self):
        a = _opt("A", [_dim("speed", 5, 6)])
        b = _opt("B", [_dim("other", 1, 2)])
        r = compare_options(a, b)
        assert r.verdict == UNKNOWN

    def test_prohibited_option_cannot_win(self):
        bad_action = TypedAction(
            actor_id="t", operation="harm", environment="development",
            resource="x", rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        a = _opt("A", [_dim("speed", 100, 100)], action=bad_action)
        b = _opt("B", [_dim("speed", 1, 1)], action=_clean_action())
        r = compare_options(a, b)
        assert r.verdict == PROHIBITED
        assert r.winner_id is None

    def test_eliminate_dominated_keeps_incomparable(self):
        a = _opt("A", [_dim("speed", 4, 4), _dim("access", 0, 0)])
        b = _opt("B", [_dim("speed", 2, 2), _dim("access", 3, 3)])
        c = _opt("C", [_dim("speed", 1, 1), _dim("access", 0, 0)])
        survivors = eliminate_dominated([a, b, c])
        ids = {s.option_id for s in survivors}
        # C dominated by A (A >= C everywhere, strictly better on speed).
        assert "C" not in ids
        # A and B incomparable: both survive.
        assert ids == {"A", "B"}

    def test_eliminate_dominated_never_eliminates_on_unknown(self):
        a = _opt("A", [_dim("speed", 0, 100)])
        b = _opt("B", [_dim("speed", 1, 2)])
        survivors = eliminate_dominated([a, b])
        assert {s.option_id for s in survivors} == {"A", "B"}


# ---------------------------------------------------------------------------
# 2. EVIDENCE vs AUTHORITY
# ---------------------------------------------------------------------------

class TestEvidenceAuthority:
    def test_both_satisfied_admissible(self):
        r = assess_requirements(evidence_status=EVIDENCE_SUFFICIENT,
                                authority_status=AUTHORITY_GRANTED)
        assert r.state == ADMISSIBLE

    def test_evidence_cannot_create_authority(self):
        # Sufficient evidence + missing authority -> NEEDS_AUTHORITY.
        r = assess_requirements(evidence_status=EVIDENCE_SUFFICIENT,
                                authority_status=AUTHORITY_MISSING)
        assert r.state == NEEDS_AUTHORITY

    def test_authority_cannot_replace_evidence(self):
        # Granted authority + pending evidence -> NEEDS_EVIDENCE.
        r = assess_requirements(evidence_status=EVIDENCE_PENDING,
                                authority_status=AUTHORITY_GRANTED)
        assert r.state == NEEDS_EVIDENCE

    def test_needs_both(self):
        r = assess_requirements(evidence_status=EVIDENCE_PENDING,
                                authority_status=AUTHORITY_MISSING)
        assert r.state == NEEDS_BOTH

    def test_stale_evidence_blocks(self):
        r = assess_requirements(evidence_status=EVIDENCE_STALE,
                                authority_status=AUTHORITY_GRANTED)
        assert r.state == NEEDS_EVIDENCE

    def test_expired_authority_blocks(self):
        r = assess_requirements(evidence_status=EVIDENCE_SUFFICIENT,
                                authority_status=AUTHORITY_EXPIRED)
        assert r.state == NEEDS_AUTHORITY

    def test_prohibited_overrides_everything(self):
        bad = TypedAction(
            actor_id="t", operation="harm", environment="development",
            resource="x", rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        r = assess_requirements(evidence_status=EVIDENCE_SUFFICIENT,
                                authority_status=AUTHORITY_GRANTED,
                                law11_action=bad)
        assert r.state == PROHIBITED

    def test_execution_gate_requires_fresh(self):
        r = execution_gate(EVIDENCE_SUFFICIENT, AUTHORITY_GRANTED)
        assert r.state == ADMISSIBLE
        r2 = execution_gate(EVIDENCE_STALE, AUTHORITY_GRANTED)
        assert r2.state == NEEDS_EVIDENCE
        r3 = execution_gate(EVIDENCE_SUFFICIENT, AUTHORITY_EXPIRED)
        assert r3.state == NEEDS_AUTHORITY


# ---------------------------------------------------------------------------
# 3. SEQUENCING
# ---------------------------------------------------------------------------

class TestSequencing:
    def test_immediate_harm_contain_escalate(self):
        c = SequenceCase(immediate_harm_occurring=True)
        assert choose_sequence(c) == SEQ_CONTAIN_ESCALATE

    def test_evidence_needs_authority_first(self):
        c = SequenceCase(evidence_gathering_needs_authority=True)
        assert choose_sequence(c) == SEQ_AUTHORITY_FIRST

    def test_parallel_when_delay_risky_and_safe(self):
        c = SequenceCase(delay_creates_material_risk=True,
                         parallel_safe=True)
        assert choose_sequence(c) == SEQ_PARALLEL

    def test_parallel_not_safe_falls_to_evidence_first(self):
        c = SequenceCase(delay_creates_material_risk=True,
                         parallel_safe=False)
        assert choose_sequence(c) == SEQ_EVIDENCE_FIRST

    def test_default_evidence_first(self):
        assert choose_sequence(SequenceCase()) == SEQ_EVIDENCE_FIRST

    def test_harm_beats_all_other_routes(self):
        c = SequenceCase(immediate_harm_occurring=True,
                         evidence_gathering_needs_authority=True,
                         delay_creates_material_risk=True,
                         parallel_safe=True)
        assert choose_sequence(c) == SEQ_CONTAIN_ESCALATE


# ---------------------------------------------------------------------------
# 4. FIVE-WAY ROUTING
# ---------------------------------------------------------------------------

class TestRouting:
    def test_refuse_on_hard_law(self):
        c = RoutingCase(violates_hard_law=True,
                        requires_protected_authority=True)
        assert route_decision(c) == ROUTE_REFUSE

    def test_ask_on_protected_authority(self):
        c = RoutingCase(requires_protected_authority=True,
                        has_applicable_approved_priority=True)
        assert route_decision(c) == ROUTE_ASK

    def test_act_on_approved_priority(self):
        c = RoutingCase(has_applicable_approved_priority=True)
        assert route_decision(c) == ROUTE_ACT

    def test_read_more_when_safe_path(self):
        c = RoutingCase(material_facts_missing=True,
                        safe_evidence_path_available=True)
        assert route_decision(c) == ROUTE_READ_MORE

    def test_ask_when_facts_missing_consequential_no_path(self):
        c = RoutingCase(material_facts_missing=True,
                        safe_evidence_path_available=False,
                        consequential=True)
        assert route_decision(c) == ROUTE_ASK

    def test_hold_when_facts_missing_not_consequential_no_path(self):
        c = RoutingCase(material_facts_missing=True,
                        safe_evidence_path_available=False,
                        consequential=False)
        assert route_decision(c) == ROUTE_HOLD

    def test_act_experiment(self):
        c = RoutingCase(authorized_bounded_experiment_available=True)
        assert route_decision(c) == ROUTE_ACT_EXPERIMENT

    def test_ask_on_value_conflict(self):
        c = RoutingCase(unresolved_material_value_conflict=True)
        assert route_decision(c) == ROUTE_ASK

    def test_default_act(self):
        assert route_decision(RoutingCase()) == ROUTE_ACT

    def test_five_questions_refuse(self):
        assert five_question_routing(allowed=False, understood=True,
                                     safe_test_available=False,
                                     belongs_to_human=False) == ROUTE_REFUSE

    def test_five_questions_ambiguous_authority_asks(self):
        # Ambiguous authority: never assume permission.
        assert five_question_routing(allowed=None, understood=True,
                                     safe_test_available=False,
                                     belongs_to_human=False) == ROUTE_ASK

    def test_five_questions_investigate(self):
        assert five_question_routing(allowed=True, understood=False,
                                     safe_test_available=False,
                                     belongs_to_human=False) == ROUTE_READ_MORE

    def test_five_questions_test(self):
        assert five_question_routing(allowed=True, understood=True,
                                     safe_test_available=True,
                                     belongs_to_human=False) == ROUTE_ACT_EXPERIMENT

    def test_five_questions_ask(self):
        assert five_question_routing(allowed=True, understood=True,
                                     safe_test_available=False,
                                     belongs_to_human=True) == ROUTE_ASK

    def test_five_questions_act(self):
        assert five_question_routing(allowed=True, understood=True,
                                     safe_test_available=False,
                                     belongs_to_human=False) == ROUTE_ACT


# ---------------------------------------------------------------------------
# 5. DECISION HIERARCHY
# ---------------------------------------------------------------------------

class TestHierarchy:
    def test_prohibited_eliminated_first(self):
        bad = TypedAction(
            actor_id="t", operation="harm", environment="development",
            resource="x", rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        a = _opt("A", [_dim("speed", 1, 1)], action=bad)
        b = _opt("B", [_dim("speed", 1, 1)], action=_clean_action())
        r = run_decision_hierarchy([a, b])
        assert r.stage_reached == STAGE_ELIMINATE_DOMINATED
        assert [s.option_id for s in r.survivors] == ["B"]
        assert any("A:PROHIBITED" in e for e in r.eliminated)

    def test_all_prohibited_refuses(self):
        bad = TypedAction(
            actor_id="t", operation="harm", environment="development",
            resource="x", rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        r = run_decision_hierarchy([_opt("A", [], action=bad)])
        assert r.stage_reached == STAGE_PROTECT_RIGHTS
        assert r.route == ROUTE_REFUSE
        assert r.survivors == []

    def test_single_survivor_acts(self):
        a = _opt("A", [_dim("speed", 5, 5)], action=_clean_action())
        b = _opt("B", [_dim("speed", 1, 1)], action=_clean_action())
        r = run_decision_hierarchy([a, b])
        assert r.stage_reached == STAGE_ELIMINATE_DOMINATED
        assert [s.option_id for s in r.survivors] == ["A"]
        assert r.route == ROUTE_ACT

    def test_approved_priority_resolves(self):
        a = _opt("A", [_dim("speed", 4, 4), _dim("access", 0, 0)],
                 action=_clean_action())
        b = _opt("B", [_dim("speed", 2, 2), _dim("access", 3, 3)],
                 action=_clean_action())
        r = run_decision_hierarchy([a, b],
                                   approved_priority="accessibility_first")
        assert r.stage_reached == STAGE_APPLY_PRIORITIES
        assert r.route == ROUTE_ACT
        assert len(r.survivors) == 2

    def test_unresolved_conflict_escalates_with_packet(self):
        a = _opt("A", [_dim("speed", 4, 4), _dim("access", 0, 0)],
                 action=_clean_action())
        b = _opt("B", [_dim("speed", 2, 2), _dim("access", 3, 3)],
                 action=_clean_action())
        r = run_decision_hierarchy([a, b], conflict_id="test-001")
        assert r.stage_reached == STAGE_ESCALATE
        assert r.route == ROUTE_ASK
        assert r.escalation_packet is not None
        assert r.escalation_packet.conflict_id == "test-001"


# ---------------------------------------------------------------------------
# 6. ESCALATION PACKETS
# ---------------------------------------------------------------------------

class TestEscalationPackets:
    def test_packet_has_two_options_tradeoff_recommendation(self):
        a = _opt("A", [_dim("speed", 4, 4), _dim("access", 0, 0)],
                 action=_clean_action())
        b = _opt("B", [_dim("speed", 2, 2), _dim("access", 3, 3)],
                 action=_clean_action())
        p = build_escalation_packet(survivors=[a, b],
                                    conflict_id="pkt-1",
                                    route=ROUTE_ASK)
        assert p.option_a_id == "A"
        assert p.option_b_id == "B"
        assert "speed" in p.tradeoff_summary
        assert "access" in p.tradeoff_summary
        assert p.recommendation != ""
        assert p.exact_authority_sought != ""
        assert p.why_naya_cannot_decide != ""
        assert len(p.while_waiting) > 0
        assert p.created_utc != ""

    def test_packet_empty_survivors(self):
        p = build_escalation_packet(survivors=[], conflict_id="pkt-2",
                                    route=ROUTE_REFUSE)
        assert p.option_a_id == "none"


# ---------------------------------------------------------------------------
# 7. ADVERSARIAL
# ---------------------------------------------------------------------------

class TestAdversarial:
    def test_no_exchange_rate_invention(self):
        # A tempting trap: A has higher SUM (4+0=4) than B (2+3=5)?
        # No — must not sum at all. Incomparable stands.
        a = _opt("A", [_dim("speed", 10, 10), _dim("access", 0, 0)])
        b = _opt("B", [_dim("speed", 1, 1), _dim("access", 1, 1)])
        r = compare_options(a, b)
        assert r.verdict == INCOMPARABLE
        assert r.winner_id is None

    def test_reworded_prohibited_still_prohibited(self):
        # Description text never influences the verdict.
        bad = TypedAction(
            actor_id="t", operation="harm", environment="development",
            resource="x", rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
            description="a totally harmless routine optimization",
        )
        r = assess_requirements(evidence_status=EVIDENCE_SUFFICIENT,
                                authority_status=AUTHORITY_GRANTED,
                                law11_action=bad)
        assert r.state == PROHIBITED

    def test_routing_never_defaults_to_ask_for_solvable_facts(self):
        # Solvable evidence problem must not escalate.
        c = RoutingCase(material_facts_missing=True,
                        safe_evidence_path_available=True,
                        consequential=True)
        assert route_decision(c) == ROUTE_READ_MORE

    def test_hierarchy_never_acts_on_prohibited(self):
        bad = TypedAction(
            actor_id="t", operation="destroy_evidence",
            environment="development", resource="x",
            rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        opts = [_opt("X", [_dim("v", 999, 999)], action=bad)]
        r = run_decision_hierarchy(opts)
        assert r.route == ROUTE_REFUSE


# ---------------------------------------------------------------------------
# 8. INTEGRATION WITH LAW 11 GATE
# ---------------------------------------------------------------------------

class TestLaw11Integration:
    def test_hierarchy_respects_law11_prohibition(self):
        # A high-scoring but prohibited option is eliminated at Stage 1,
        # before any comparability assessment.
        from kernel.protocol.typed_action import TypedAction
        bad = TypedAction(
            actor_id="t", operation="fabricate_evidence",
            environment="development", resource="x",
            rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        good = TypedAction(
            actor_id="t", operation="read",
            environment="development", resource="docs",
            rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
        )
        a = DecisionOption("A", (_dim("value", 999, 999),), law11_action=bad)
        b = DecisionOption("B", (_dim("value", 1, 1),), law11_action=good)
        r = run_decision_hierarchy([a, b])
        # A eliminated at Stage 1 despite higher value. B survives alone.
        assert [s.option_id for s in r.survivors] == ["B"]
        assert r.route == ROUTE_ACT

    def test_evidence_authority_with_law11_action(self):
        from kernel.protocol.typed_action import TypedAction
        prod_deploy = TypedAction(
            actor_id="t", operation="deploy",
            environment="production", resource="nayapower",
            rights_safe=True, safety_safe=True,
            privacy_safe=True, consent_obtained=True,
            authority_ref=None,  # no authority
        )
        # Law 11 says NEEDS_AUTHORITY for production deploy without grant.
        r = assess_requirements(
            evidence_status=EVIDENCE_SUFFICIENT,
            authority_status=AUTHORITY_MISSING,
            law11_action=prod_deploy,
        )
        # Law 11 gate returns NEEDS_AUTHORITY (not PROHIBITED), so the
        # assessment derives from statuses: evidence ok + authority missing.
        assert r.state in (NEEDS_AUTHORITY, NEEDS_BOTH)

    def test_full_flow_incomparable_to_escalation(self):
        # End-to-end: two admissible options, incomparable, no priority
        # -> hierarchy escalates with a complete packet.
        from kernel.protocol.typed_action import TypedAction
        def clean(op="read"):
            return TypedAction(
                actor_id="t", operation=op, environment="development",
                resource="docs", rights_safe=True, safety_safe=True,
                privacy_safe=True, consent_obtained=True,
            )
        a = DecisionOption("fast", (_dim("speed", 4, 4),
                                    _dim("access", 0, 0)),
                           law11_action=clean())
        b = DecisionOption("accessible", (_dim("speed", 2, 2),
                                          _dim("access", 3, 3)),
                           law11_action=clean())
        r = run_decision_hierarchy([a, b], conflict_id="e2e-001")
        assert r.stage_reached == STAGE_ESCALATE
        assert r.route == ROUTE_ASK
        pkt = r.escalation_packet
        assert pkt.conflict_id == "e2e-001"
        assert pkt.option_a_id in ("fast", "accessible")
        assert pkt.option_b_id in ("fast", "accessible")
        assert pkt.option_a_id != pkt.option_b_id
        # Evidence/authority check on the escalation itself.
        req = assess_requirements(
            evidence_status=EVIDENCE_SUFFICIENT,
            authority_status=AUTHORITY_MISSING,
        )
        assert req.state == NEEDS_AUTHORITY
