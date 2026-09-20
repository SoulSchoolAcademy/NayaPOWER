#!/usr/bin/env python3
import unittest
from smart_note_candidate import build_candidate

E = {"schema":"naya-power-evidence/v1","execution_id":"exec-1","evidence_id":"ev-1","commit_sha":"abc123"}
L = {"what_mattered":"The contract caught a bad handoff","what_was_learned":"Evidence must remain tied to execution","future_action":"Require provenance before promotion"}

class SmartNoteCandidateTests(unittest.TestCase):
    def test_valid_candidate(self):
        n = build_candidate(E, L, note_type="lesson")
        self.assertEqual(n["promotion_state"], "CANDIDATE")
        self.assertEqual(n["source"]["execution_id"], "exec-1")

    def test_no_evidence(self):
        with self.assertRaises(ValueError): build_candidate({}, L, note_type="lesson")

    def test_noncanonical_evidence(self):
        with self.assertRaises(ValueError): build_candidate({**E, "schema":"fake"}, L, note_type="lesson")

    def test_missing_learning(self):
        with self.assertRaises(ValueError): build_candidate(E, {"what_mattered":"x"}, note_type="lesson")

    def test_noise_rejected(self):
        with self.assertRaises(ValueError): build_candidate(E, {"what_mattered":"","what_was_learned":"","future_action":""}, note_type="lesson")

    def test_invalid_type(self):
        with self.assertRaises(ValueError): build_candidate(E, L, note_type="transcript")

    def test_provenance_preserved(self):
        n = build_candidate(E, L, note_type="decision")
        self.assertEqual(n["source"], {"execution_id":"exec-1","evidence_id":"ev-1","commit_sha":"abc123"})

    def test_candidate_is_not_authority(self):
        n = build_candidate(E, L, note_type="insight")
        self.assertEqual(n["promotion_state"], "CANDIDATE")
        self.assertNotIn("canonical", n)

if __name__ == "__main__": unittest.main()
