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
                        "scope": "runtime decision",
                        "status": "ACTIVE",
                    }
                ],
            }
        )

    def test_registered_authority_can_pass_all_hard_gates(self):
        decision = evaluate_governance(
            GovernedAction(authority_id="AUTH-TEST"), self.registry()
        )
        self.assertTrue(decision.eligible)
        self.assertEqual(decision.authority_scope, "runtime decision")

    def test_unregistered_authority_is_ineligible_even_with_high_value(self):
        decision = evaluate_governance(
            GovernedAction(authority_id="AUTH-MISSING"), self.registry()
        )
        self.assertFalse(decision.eligible)
        self.assertIn("authority_id is not registered", decision.reasons)

    def test_consequence_risk_evidence_and_stop_are_hard_gates(self):
        cases = [
            ("consequence", GovernedAction(authority_id="AUTH-TEST", consequence="HIGH", reversible=False)),
            ("risk", GovernedAction(authority_id="AUTH-TEST", risk="HIGH", risk_acceptable=False)),
            ("evidence", GovernedAction(authority_id="AUTH-TEST", evidence_ready=False)),
            ("verification", GovernedAction(authority_id="AUTH-TEST", verification_required=False)),
            ("stop", GovernedAction(authority_id="AUTH-TEST", stopping_condition_satisfied=False)),
            ("value", GovernedAction(authority_id="AUTH-TEST", responsible_value_eligible=False)),
        ]
        for name, action in cases:
            with self.subTest(name=name):
                self.assertFalse(evaluate_governance(action, self.registry()).eligible)

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
                ),
                ActionCandidate(
                    "safe",
                    "Safe governed action",
                    8,
                    authority_id="AUTH-TEST",
                ),
            ],
            registry=self.registry(),
        )
        self.assertEqual(plan.action.action_id, "safe")

    def test_capability_does_not_grant_authority(self):
        decision = evaluate_governance(
            GovernedAction(
                authority_id="AUTH-MISSING",
                capability_available=True,
            ),
            self.registry(),
        )
        self.assertFalse(decision.eligible)


if __name__ == "__main__":
    unittest.main()
