import unittest

from governance_contract import AuthorityRegistry, GovernedAction, evaluate_governance
from naya_power_runtime import ActionCandidate, MissionState, choose_next_action


class GovernanceContractTests(unittest.TestCase):
    def registry(self):
        return AuthorityRegistry.from_mapping(
            {
                "protocol": "naya-power-authority-registry/v1",
                "authorities": [
                    {
                        "authority_id": "AUTH-TEST",
                        "name": "Test Authority",
                        "scope": "runtime decision, action planning",
                        "status": "ACTIVE",
                    }
                ],
            }
        )

    def valid_action(self, **overrides):
        values = {
            "authority_id": "AUTH-TEST",
            "authority_scope": "action planning",
        }
        values.update(overrides)
        return GovernedAction(**values)

    def test_registered_authority_can_pass_all_hard_gates(self):
        decision = evaluate_governance(self.valid_action(), self.registry())
        self.assertTrue(decision.eligible)
        self.assertEqual(decision.authority_scope, "runtime decision, action planning")
        self.assertTrue(all(decision.checks.values()))

    def test_authority_scope_must_match_registered_scope(self):
        decision = evaluate_governance(
            self.valid_action(authority_scope="deployment control"), self.registry()
        )
        self.assertFalse(decision.eligible)
        self.assertIn("requested authority scope is outside registered authority scope", decision.reasons)

    def test_inactive_authority_is_ineligible(self):
        registry = AuthorityRegistry.from_mapping(
            {
                "protocol": "naya-power-authority-registry/v1",
                "authorities": [
                    {
                        "authority_id": "AUTH-TEST",
                        "scope": "action planning",
                        "status": "DEPRECATED",
                    }
                ],
            }
        )
        decision = evaluate_governance(self.valid_action(), registry)
        self.assertFalse(decision.eligible)
        self.assertIn("authority is not active", decision.reasons)

    def test_unregistered_authority_is_ineligible_even_with_high_value(self):
        decision = evaluate_governance(
            self.valid_action(authority_id="AUTH-MISSING"), self.registry()
        )
        self.assertFalse(decision.eligible)
        self.assertIn("authority_id is not registered", decision.reasons)

    def test_missing_registry_is_ineligible_even_with_high_value(self):
        decision = evaluate_governance(self.valid_action(), None)
        self.assertFalse(decision.eligible)
        self.assertIn("Authority Registry is required for governed execution", decision.reasons)
        self.assertFalse(decision.checks["authority_registry_present"])

    def test_missing_registry_prevents_action_selection(self):
        state = MissionState(
            project="Naya Power",
            mission="Test governance",
            vision="Governable execution",
            desired_outcome="Only governed actions execute",
            protected_scope=["constitution"],
            known=["registry"],
            last_verified_state="Source verified",
            next_action="governed-action",
            next_action_reason="Test fail-closed registry requirement",
        )
        candidate = ActionCandidate(
            "governed-action",
            "High-value action without supplied registry",
            10,
            authority_id="AUTH-TEST",
            authority_scope="action planning",
        )
        with self.assertRaisesRegex(RuntimeError, "No eligible next action"):
            choose_next_action(state, [candidate])

    def test_consequence_risk_evidence_stop_value_and_human_escalation_are_hard_gates(self):
        cases = [
            ("consequence", self.valid_action(consequence="HIGH", reversible=False)),
            ("risk", self.valid_action(risk="HIGH", risk_acceptable=False)),
            ("evidence", self.valid_action(evidence_ready=False)),
            ("verification", self.valid_action(verification_required=False)),
            ("stop", self.valid_action(stopping_condition_satisfied=False)),
            ("value", self.valid_action(responsible_value_eligible=False)),
            ("human", self.valid_action(requires_human_decision=True)),
            ("decision-state", self.valid_action(decision_state="VERIFY")),
        ]
        for name, action in cases:
            with self.subTest(name=name):
                self.assertFalse(evaluate_governance(action, self.registry()).eligible)

    def test_action_candidate_carries_decision_state_into_governance(self):
        candidate = ActionCandidate(
            "verify-first",
            "Verify evidence before execution",
            10,
            authority_id="AUTH-TEST",
            authority_scope="action planning",
            decision_state="VERIFY",
        )
        decision = candidate.governance_decision(self.registry())
        self.assertFalse(decision.eligible)
        self.assertIn("decision state 'VERIFY' does not permit execution", decision.reasons)

    def test_invalid_is_not_zero_value_in_ranked_selection(self):
        state = MissionState(
            project="Naya Power",
            mission="Test governance",
            vision="Governable execution",
            desired_outcome="Only eligible actions execute",
            protected_scope=["constitution"],
            known=["registry"],
            last_verified_state="Source verified",
            next_action="safe",
            next_action_reason="Highest responsible eligible action",
        )
        plan = choose_next_action(
            state,
            [
                ActionCandidate(
                    "unsafe",
                    "High-value but irreversible",
                    10,
                    consequence="HIGH",
                    reversible=False,
                    authority_id="AUTH-TEST",
                    authority_scope="action planning",
                ),
                ActionCandidate(
                    "safe",
                    "Safe governed action",
                    8,
                    authority_id="AUTH-TEST",
                    authority_scope="action planning",
                ),
            ],
            registry=self.registry(),
        )
        self.assertEqual(plan.action.action_id, "safe")

    def test_capability_does_not_grant_authority(self):
        decision = evaluate_governance(
            self.valid_action(authority_id="AUTH-MISSING"),
            self.registry(),
        )
        self.assertFalse(decision.eligible)


if __name__ == "__main__":
    unittest.main()
