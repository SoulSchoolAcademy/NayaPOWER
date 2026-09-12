import unittest

from governance_kernel import (
    Authority,
    AuthorityRegistry,
    DecisionObject,
    Epistemic,
    GovernanceState,
    Risk,
    VerificationPlan,
    assert_not_verified_without_observation,
    evaluate,
    receipt_requirements,
    transition,
)


class GovernanceKernelTests(unittest.TestCase):
    def setUp(self):
        self.authority = Authority(
            authority_id="AUTH-001",
            principal_id="human-001",
            purpose="repair governed system",
            scope="repo:NayaPOWER",
            granted_actions=frozenset({"modify_source"}),
        )
        self.decision = DecisionObject(
            decision_id="DEC-001",
            mission="restore governance integrity",
            actor_id="human-001",
            action="modify_source",
            purpose="repair governed system",
            scope="repo:NayaPOWER",
            current_truth="a derived index is stale before validation",
            gap="validation executes before index reconstruction",
            evidence=("observed failing enforcement run",),
            epistemic=frozenset({Epistemic.OBSERVED}),
            consequence="CI governance gate can reject valid canonical state",
            reversible=True,
            risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
            alternatives=("move existing index rebuild earlier",),
            expected_value="restore deterministic validation ordering",
            required_permission="modify_source",
            verification=VerificationPlan(
                observation="workflow run at exact repair SHA",
                success_criteria="Smart Brain v3 enforcement passes",
                stop_conditions=("new failure requires first-failure diagnosis",),
            ),
            necessary_power=frozenset({"repo_read", "repo_write"}),
            requested_power=frozenset({"repo_read", "repo_write"}),
        )

    def test_registry_requires_explicit_known_id(self):
        registry = AuthorityRegistry({self.authority.authority_id: self.authority})
        self.assertIs(registry.resolve("AUTH-001"), self.authority)
        self.assertIsNone(registry.resolve("AUTH-FABRICATED"))

    def test_valid_decision_is_authorized(self):
        result = evaluate(self.decision, self.authority)
        self.assertTrue(result.allowed)
        self.assertEqual(result.decision.value, "EXECUTE")
        self.assertEqual(result.state, GovernanceState.AUTHORIZED)

    def test_missing_authority_fails_closed(self):
        result = evaluate(self.decision, None)
        self.assertFalse(result.allowed)
        self.assertNotEqual(result.state, GovernanceState.AUTHORIZED)
        self.assertIn("no authority object supplied", result.reasons)

    def test_wrong_scope_cannot_self_authorize(self):
        wrong = Authority(
            authority_id="AUTH-002",
            principal_id="human-001",
            purpose="repair governed system",
            scope="repo:OTHER",
            granted_actions=frozenset({"modify_source"}),
        )
        result = evaluate(self.decision, wrong)
        self.assertFalse(result.allowed)
        self.assertIn("authority does not permit this actor/action/scope", result.reasons)

    def test_expired_authority_fails_closed(self):
        expired = Authority(
            authority_id="AUTH-003",
            principal_id="human-001",
            purpose="repair governed system",
            scope="repo:NayaPOWER",
            granted_actions=frozenset({"modify_source"}),
            expires_at="2026-09-12T13:00:00Z",
        )
        result = evaluate(
            self.decision,
            expired,
            now="2026-09-12T14:00:00Z",
        )
        self.assertFalse(result.allowed)
        self.assertIn("authority does not permit this actor/action/scope or is inactive", result.reasons)

    def test_unknown_or_assumed_state_blocks_execution(self):
        decision = self.decision.__class__(**{
            **self.decision.__dict__,
            "epistemic": frozenset({Epistemic.OBSERVED, Epistemic.UNKNOWN}),
        })
        result = evaluate(decision, self.authority)
        self.assertFalse(result.allowed)
        self.assertIn("material epistemic uncertainty remains", result.reasons)

    def test_high_risk_requires_verified_evidence(self):
        decision = self.decision.__class__(**{
            **self.decision.__dict__,
            "risk": Risk(uncertainty=8, consequence=8, irreversibility=8),
        })
        result = evaluate(decision, self.authority)
        self.assertFalse(result.allowed)
        self.assertIn("high-risk action lacks verified epistemic state", result.reasons)

    def test_least_power_blocks_excess_scope(self):
        decision = self.decision.__class__(**{
            **self.decision.__dict__,
            "requested_power": frozenset({"repo_read", "repo_write", "production_admin"}),
        })
        result = evaluate(decision, self.authority)
        self.assertFalse(result.allowed)
        self.assertIn("requested power exceeds necessary power", result.reasons)

    def test_invalid_verified_promotion_is_rejected(self):
        with self.assertRaises(ValueError):
            transition(GovernanceState.EXECUTED, GovernanceState.VERIFIED)

    def test_valid_execution_path_transitions(self):
        state = transition(GovernanceState.PROPOSED, GovernanceState.READY_FOR_DECISION)
        state = transition(state, GovernanceState.AUTHORIZED)
        state = transition(state, GovernanceState.EXECUTING)
        state = transition(state, GovernanceState.EXECUTED)
        state = transition(state, GovernanceState.OBSERVED)
        state = transition(state, GovernanceState.VERIFIED)
        self.assertEqual(state, GovernanceState.VERIFIED)

    def test_stop_is_terminal(self):
        self.assertEqual(
            transition(GovernanceState.AUTHORIZED, GovernanceState.STOPPED),
            GovernanceState.STOPPED,
        )
        with self.assertRaises(ValueError):
            transition(GovernanceState.STOPPED, GovernanceState.EXECUTING)

    def test_verified_requires_observation(self):
        with self.assertRaises(AssertionError):
            assert_not_verified_without_observation(
                GovernanceState.VERIFIED, observed=False, verified=True
            )

    def test_receipt_is_required_for_success_and_block(self):
        allowed = evaluate(self.decision, self.authority)
        blocked = evaluate(self.decision, None)
        self.assertIn("verification", receipt_requirements(allowed))
        self.assertIn("failure_or_block_reason", receipt_requirements(blocked))


if __name__ == "__main__":
    unittest.main()
