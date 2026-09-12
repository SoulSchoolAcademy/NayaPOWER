import tempfile
import unittest
from pathlib import Path

from mission_state_store import LeadModeEngine, MissionStateStore
from naya_power_runtime import (
    ActionCandidate,
    EvidenceState,
    ExecutionReceipt,
    MissionState,
)


class MissionStateStoreTests(unittest.TestCase):
    def make_state(self) -> MissionState:
        return MissionState(
            project="Naya Power",
            mission="Turn the operating architecture into a reliable runtime.",
            vision="Fresh Naya restores state and continuously leads within authority.",
            desired_outcome="Persistent Mission State + Lead Mode.",
            protected_scope=["canonical laws", "source-of-truth boundaries"],
            known=["runtime kernel exists"],
            last_verified_state="Runtime persistence not yet verified.",
            next_action="persist-runtime-state",
            next_action_reason="Highest-value remaining runtime gap.",
        )

    def test_atomic_save_and_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mission-state.json"
            store = MissionStateStore(path)
            state = self.make_state()
            store.save(state)
            restored = store.load()
            self.assertEqual(restored.project, state.project)
            self.assertEqual(restored.next_action, state.next_action)
            self.assertEqual(restored.protected_scope, state.protected_scope)

    def test_lead_mode_persists_verified_result_and_next_move(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MissionStateStore(Path(directory) / "mission-state.json")
            store.save(self.make_state())
            engine = LeadModeEngine(store)
            plan = engine.choose(
                [
                    ActionCandidate("low", "Low-value work", 3),
                    ActionCandidate("runtime", "Implement runtime persistence", 10),
                ]
            )
            self.assertEqual(plan.action.action_id, "runtime")
            updated = engine.accept_execution(
                plan,
                ExecutionReceipt(
                    action_id="runtime",
                    result="Persistent runtime state verified",
                    evidence_state=EvidenceState.VERIFIED,
                    observed="State file saved, reloaded, and validated from disk.",
                    evidence_source="local runtime test",
                    verified=True,
                    next_action="wire-host-executor",
                ),
            )
            self.assertEqual(updated.next_action, "wire-host-executor")
            self.assertEqual(engine.restore()["next_action"], "wire-host-executor")
            self.assertTrue(engine.activate()["active"])


if __name__ == "__main__":
    unittest.main()
