import unittest

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

    def test_invalid_is_not_zero_value(self):
        state = self.make_state()
        invalid = ActionCandidate(
            action_id="unsafe",
            description="Destroy protected state",
            value=9,
            constitutional=False,
        )
        valid = ActionCandidate(
            action_id="safe",
            description="Implement surgical runtime kernel",
            value=8,
        )
        plan = choose_next_action(state, [invalid, valid])
        self.assertEqual(plan.action.action_id, "safe")

    def test_exactly_one_next_action_is_selected(self):
        state = self.make_state()
        candidates = [
            ActionCandidate("a", "Lower-value action", 4),
            ActionCandidate("b", "Highest-value action", 8),
            ActionCandidate("c", "Medium-value action", 6),
        ]
        plan = choose_next_action(state, candidates)
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

    def test_verified_receipt_promotes_state(self):
        state = self.make_state()
        plan = choose_next_action(
            state,
            [ActionCandidate("build", "Build runtime", 9)],
        )
        receipt = ExecutionReceipt(
            action_id="build",
            result="Runtime kernel implemented",
            evidence_state=EvidenceState.VERIFIED,
            observed="Fetched runtime file and confirmed implementation exists.",
            evidence_source="GitHub main branch",
            verified=True,
            next_action="add-live-host-adapter-test",
        )
        record_result(state, plan, receipt)
        self.assertEqual(state.block_status, BlockStatus.VERIFIED)
        self.assertEqual(state.next_action, "add-live-host-adapter-test")
        self.assertIn("Runtime kernel implemented", state.verified)

    def test_activation_status_is_machine_checkable(self):
        status = activation_status(self.make_state())
        self.assertTrue(status["active"])
        self.assertTrue(all(status["checks"].values()))


if __name__ == "__main__":
    unittest.main()
