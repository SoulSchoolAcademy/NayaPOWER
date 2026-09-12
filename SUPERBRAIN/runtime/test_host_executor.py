import tempfile
import unittest
from pathlib import Path

from host_executor import HostExecutorBridge
from mission_state_store import LeadModeEngine, MissionStateStore
from naya_power_runtime import (
    ActionCandidate,
    EvidenceState,
    ExecutionReceipt,
    MissionState,
)
from quality_gate import OscarReview, Scorecard


class HostExecutorBridgeTests(unittest.TestCase):
    def make_state(self):
        return MissionState(
            project="Naya Power",
            mission="Close the runtime execution loop.",
            vision="Fresh Naya executes the next responsible action automatically.",
            desired_outcome="Authorized execution with verified continuation.",
            protected_scope=["constitution", "source of truth"],
            known=["runtime kernel", "persistence", "quality gate"],
            last_verified_state="Host bridge not yet verified.",
            next_action="bridge",
            next_action_reason="Highest-value remaining gap.",
        )

    def test_cycle_executes_verifies_scores_and_persists_next_action(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MissionStateStore(Path(directory) / "mission-state.json")
            store.save(self.make_state())
            engine = LeadModeEngine(store)

            executed = []

            def candidates(_restored):
                return [ActionCandidate("bridge", "Execute bridge", 10)]

            def executor(plan):
                executed.append(plan.action.action_id)
                return ExecutionReceipt(
                    action_id=plan.action.action_id,
                    result="Bridge execution verified",
                    evidence_state=EvidenceState.VERIFIED,
                    observed="Authorized executor ran and returned an independently recorded result.",
                    evidence_source="host test executor",
                    verified=True,
                    next_action="integration-test",
                )

            def scorecard(_state, _receipt):
                return Scorecard({"truth": 10.0, "quality": 10.0, "continuity": 10.0}, 10.0)

            def oscar(_state, _receipt, _scorecard):
                return OscarReview()

            bridge = HostExecutorBridge(engine, candidates, executor, scorecard, oscar)
            result = bridge.cycle()

            self.assertEqual(result.status, "CONTINUE")
            self.assertEqual(executed, ["bridge"])
            self.assertEqual(engine.restore()["next_action"], "integration-test")
            self.assertTrue(engine.activate()["active"])

    def test_no_eligible_action_produces_handoff_instead_of_fake_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MissionStateStore(Path(directory) / "mission-state.json")
            store.save(self.make_state())
            engine = LeadModeEngine(store)
            bridge = HostExecutorBridge(
                engine,
                lambda _restored: [
                    ActionCandidate(
                        "human",
                        "Make irreversible decision",
                        10,
                        requires_human_decision=True,
                    )
                ],
                lambda _plan: self.fail("executor must not run"),
            )
            result = bridge.cycle()
            self.assertEqual(result.status, "HUMAN_OR_EXTERNAL_INPUT_REQUIRED")
            self.assertIsNotNone(result.handoff)


if __name__ == "__main__":
    unittest.main()
