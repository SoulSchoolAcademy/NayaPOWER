import unittest

from governance_contract import AuthorityRegistry
from naya_power_runtime import (
    ActionCandidate,
    BlockStatus,
    EvidenceState,
    ExecutionReceipt,
    MissionState,
    activation_status,
    choose_next_action,
    cold_start,
    record_result,
)


class MissionStateRuntimeTests(unittest.TestCase):
    def make_registry(self):
        return AuthorityRegistry.from_mapping(
            {
                "protocol": "naya-power-authority-registry/v1",
                "authorities": [
                    {
                        "authority_id": "AUTH-TEST",
                        "scope": "runtime decision",
                        "status": "ACTIVE",
                    }
                ],
            }
        )

    def make_state(self) -> MissionState:
        return MissionState(
            project="Naya Power",
            mission="Turn the operating architecture into a reliable runtime.",
            vision="A fresh Naya restores state, leads the next move, verifies, learns, and continues.",
            desired_outcome="A machine-checkable Mission State + Lead Mode runtime.",
            repository="SoulSchoolAcademy/NayaPOWER",
            branch="main",
            protected_scope=["existing canonical laws", "existing source-of-truth boundaries"],
            known=["Execution Control Plane exists", "Universal Agent Interface exists"],
            last_verified_state="Runtime architecture not yet implemented.",
            next_action="build-runtime",
            next_action_reason="Highest-value executable delta.",
        )

    def candidate(self, action_id, description, value, **kwargs):
        return ActionCandidate(
            action_id,
            description,
            value,
            authority_id="AUTH-TEST",
            authority_scope="runtime decision",
            **kwargs,
        )

    def test_invalid_is_not_zero_value(self):
        state = self.make_state()
        invalid = self.candidate("unsafe", "Destroy protected state", 9, constitutional=False)
        valid = self.candidate("safe", "Implement surgical runtime kernel", 8)
        plan = choose_next_action(state, [invalid, valid], registry=self.make_registry())
        self.assertEqual(plan.action.action_id, "safe")

    def test_exactly_one_next_action_is_selected(self):
        state = self.make_state()
        candidates = [
            self.candidate("a", "Lower-value action", 4),
            self.candidate("b", "Highest-value action", 8),
            self.candidate("c", "Medium-value action", 6),
        ]
        plan = choose_next_action(state, candidates, registry=self.make_registry())
        self.assertEqual(plan.action.action_id, "b")

    def test_cold_start_restores_operational_state(self):
        restored = cold_start(self.make_state())
        self.assertEqual(restored["project"], "Naya Power")
        self.assertEqual(restored["next_action"], "build-runtime")
        self.assertIn("existing canonical laws", restored["protected_scope"])

    def test_verified_requires_verification_evidence(self):
        state = self.make_state()
        state.block_status = BlockStatus.VERIFIED
        state.verified = ["claimed result"]
        self.assertTrue(state.validate())

    def test_verified_receipt_persists_evidence_and_round_trips(self):
        state = self.make_state()
        plan = choose_next_action(
            state,
            [self.candidate("build", "Build runtime", 9)],
            registry=self.make_registry(),
        )
        receipt = ExecutionReceipt(
            action_id="build",
            result="Runtime kernel implemented",
            evidence_state=EvidenceState.VERIFIED,
            observed="Fetched runtime file and confirmed implementation exists.",
            evidence_source="GitHub main branch",
            verified=True,
            next_action="add-live-host-adapter-test",
            commit="runtime-commit",
        )
        record_result(state, plan, receipt)
        self.assertEqual(state.block_status, BlockStatus.VERIFIED)
        self.assertEqual(state.next_action, "add-live-host-adapter-test")
        self.assertIn("Runtime kernel implemented", state.verified)
        self.assertEqual(len(state.evidence), 1)
        self.assertTrue(state.evidence[0].can_support_verified())
        state.assert_valid()

        restored = MissionState.from_mapping(state.to_dict())
        restored.assert_valid()
        self.assertEqual(restored.verified, state.verified)
        self.assertEqual(restored.evidence[0].commit, "runtime-commit")

    def test_activation_status_is_machine_checkable(self):
        status = activation_status(self.make_state())
        self.assertTrue(status["active"])
        self.assertTrue(all(status["checks"].values()))


if __name__ == "__main__":
    unittest.main()
