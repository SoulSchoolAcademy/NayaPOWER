import unittest

from quality_gate import QualityGateInput, evaluate_quality


class TuneInQualityGateTests(unittest.TestCase):
    def good(self):
        return QualityGateInput(
            intent_understood=True,
            context_complete=True,
            material_unknowns=(),
            consequence=5,
            quality_ready=True,
            evidence_ready=True,
        )

    def test_pass_requires_all_predicates(self):
        result = evaluate_quality(self.good())
        self.assertTrue(result.allowed)
        self.assertEqual(result.state, "TUNE_IN_PASS")

    def test_intent_failure_forces_deepen(self):
        g = self.good()
        result = evaluate_quality(g.__class__(**{**g.__dict__, "intent_understood": False}))
        self.assertFalse(result.allowed)
        self.assertEqual(result.state, "DEEPEN_INSPECT_REQUIRED")
        self.assertIn("intent understanding predicate is false", result.reasons)

    def test_context_failure_forces_deepen(self):
        g = self.good()
        result = evaluate_quality(g.__class__(**{**g.__dict__, "context_complete": False}))
        self.assertFalse(result.allowed)
        self.assertIn("context completeness predicate is false", result.reasons)

    def test_material_unknown_forces_deepen(self):
        g = self.good()
        result = evaluate_quality(g.__class__(**{**g.__dict__, "material_unknowns": ("deployment target",)}))
        self.assertFalse(result.allowed)
        self.assertIn("material unknowns remain", result.reasons)

    def test_quality_not_ready_forces_inspect(self):
        g = self.good()
        result = evaluate_quality(g.__class__(**{**g.__dict__, "quality_ready": False}))
        self.assertFalse(result.allowed)
        self.assertIn("quality readiness predicate is false", result.reasons)

    def test_evidence_not_ready_blocks_consequential_work(self):
        g = self.good()
        result = evaluate_quality(g.__class__(**{**g.__dict__, "evidence_ready": False}))
        self.assertFalse(result.allowed)
        self.assertIn("evidence readiness predicate is false", result.reasons)

    def test_non_consequential_work_can_answer_without_evidence(self):
        g = self.good()
        g = g.__class__(**{**g.__dict__, "evidence_ready": False})
        result = evaluate_quality(g, consequential=False)
        self.assertTrue(result.allowed)

    def test_consequence_is_bounded(self):
        with self.assertRaises(ValueError):
            QualityGateInput(True, True, (), 11, True, True)

    def test_no_dimension_is_averaged_away(self):
        g = self.good()
        for field in ("intent_understood", "context_complete", "quality_ready", "evidence_ready"):
            result = evaluate_quality(g.__class__(**{**g.__dict__, field: False}))
            self.assertFalse(result.allowed)


if __name__ == "__main__":
    unittest.main()
