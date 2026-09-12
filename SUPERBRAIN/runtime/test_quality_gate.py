import unittest

from naya_power_runtime import Evidence, EvidenceState, MissionState
from quality_gate import (
    MINIMUM_RESPONSIBLE_SCORE,
    OscarReview,
    Scorecard,
    apply_quality_decision,
    evaluate_quality,
)


class QualityGateTests(unittest.TestCase):
    def make_state(self):
        return MissionState(
            project="Naya Power",
            mission="Run the continuous operating model.",
            vision="Lead without false completion.",
            desired_outcome="A verified continuation decision.",
            protected_scope=["constitution"],
            known=["runtime exists"],
            next_action="continue",
            next_action_reason="Current mission gap.",
            evidence=[
                Evidence(
                    evidence_id="e1",
                    claim="execution completed",
                    state=EvidenceState.VERIFIED,
                    observation="Observed the result directly.",
                    source="test",
                )
            ],
        )

    def test_blocking_oscar_defect_prevents_promotion(self):
        decision = evaluate_quality(
            self.make_state(),
            Scorecard({"truth": 10.0, "quality": 10.0}, 10.0),
            OscarReview(blocking_defects=("release parity unproven",), repair_actions=("verify-runtime",)),
            "continue",
        )
        self.assertFalse(decision.promoted)
        self.assertEqual(decision.next_action, "verify-runtime")

    def test_subthreshold_score_prevents_promotion(self):
        decision = evaluate_quality(
            self.make_state(),
            Scorecard({"truth": 9.0, "quality": 9.0}, 9.0),
            OscarReview(),
            "continue",
        )
        self.assertFalse(decision.promoted)
        self.assertIn(f"score below {MINIMUM_RESPONSIBLE_SCORE}", decision.blocking_reasons)

    def test_passing_gate_promotes_next_action(self):
        state = self.make_state()
        decision = evaluate_quality(
            state,
            Scorecard({"truth": 10.0, "quality": 9.8, "continuity": 9.7}, 9.8),
            OscarReview(),
            "continue",
        )
        self.assertTrue(decision.promoted)
        apply_quality_decision(state, decision)
        self.assertEqual(state.next_action, "continue")
        self.assertIn("Quality gate passed", state.decisions[-1])


if __name__ == "__main__":
    unittest.main()
