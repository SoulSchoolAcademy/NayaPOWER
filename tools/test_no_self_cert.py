#!/usr/bin/env python3
"""Adversarial tests for UD-02 — NOTHING MAY CERTIFY ITSELF.

Positive: genuinely independent verifiers are accepted (PASS and FAIL).
Negative: self-certification, shared-context, parroting, derivative-only,
circular-provenance, and empty-evidence certifications are refused.

Run: python3 test_no_self_cert.py  (stdlib only)
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from no_self_cert import (  # noqa: E402
    Artifact, Certification, Evidence, Identity, Ledger,
    REJECT_CIRCULAR, REJECT_CONTEXT, REJECT_DERIVATIVE, REJECT_NO_EVIDENCE,
    REJECT_NO_VERDICT, REJECT_PARROT, REJECT_SELF, certify, jaccard, _shingles,
)

DOER = Identity(seat="naya-4", session_id="sess-doer", context_fingerprint="ctx-doer",
                agent_id="agent-doer")
OTHER = Identity(seat="naya-2", session_id="sess-other", context_fingerprint="ctx-other",
                 agent_id="agent-other")

CLAIMS = [
    "the fencing token binds authority via a monotonic UUID",
    "a dead authority's token cannot validate at a recycled address",
]


def make_artifact(doer=DOER, claims=CLAIMS):
    return Artifact.from_content("art-1", "fencing token implementation bytes",
                                 doer, claims=claims)


def good_evidence():
    return [Evidence(
        text=("ran the adversarial fencing suite locally: recycled-address "
              "token rejected, fresh authority accepted, 14/14 green"),
        sources=["test-run:tools/test_fencing_adversarial.py"],
        derived_from=[])]


class TestIndependentVerifier(unittest.TestCase):
    def test_independent_pass_accepted(self):
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=good_evidence()))
        self.assertTrue(d.accepted, d.detail)
        self.assertEqual(d.reasons, [])

    def test_independent_fail_accepted(self):
        # A FAIL from an independent verifier is a valid certification too.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="FAIL",
            evidence=[Evidence(
                text=("recycled-address token was ACCEPTED by the build under "
                      "test; reproduced twice, see attached log"),
                sources=["test-run:tools/test_fencing_adversarial.py::recycled"],
                derived_from=[])]))
        self.assertTrue(d.accepted, d.detail)

    def test_partial_overlap_with_independent_observation_accepted(self):
        # Some shared vocabulary is fine when real independent work exists.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=[Evidence(
                text=("checked the fencing token path: implementation reads "
                      "the monotonic UUID from the authority record and the "
                      "adversarial suite passes 14/14 on this head"),
                sources=["file:tools/fencing.py", "test-run:adversarial"],
                derived_from=[])]))
        self.assertTrue(d.accepted, d.detail)


class TestSelfCertification(unittest.TestCase):
    def test_same_seat_rejected(self):
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=DOER, verdict="PASS",
            evidence=good_evidence()))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_SELF, d.reasons)

    def test_same_agent_new_seat_label_rejected(self):
        # Renaming the seat does not create independence.
        impostor = Identity(seat="naya-9", session_id="sess-x",
                            context_fingerprint="ctx-x", agent_id="agent-doer")
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=impostor, verdict="PASS",
            evidence=good_evidence()))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_SELF, d.reasons)

    def test_shared_session_rejected(self):
        # Different seat, same session: the same mind.
        impostor = Identity(seat="naya-9", session_id="sess-doer",
                            context_fingerprint="ctx-x", agent_id="agent-x")
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=impostor, verdict="PASS",
            evidence=good_evidence()))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_CONTEXT, d.reasons)

    def test_shared_context_fingerprint_rejected(self):
        impostor = Identity(seat="naya-9", session_id="sess-x",
                            context_fingerprint="ctx-doer", agent_id="agent-x")
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=impostor, verdict="PASS",
            evidence=good_evidence()))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_CONTEXT, d.reasons)


class TestEvidenceQuality(unittest.TestCase):
    def test_parrot_rejected(self):
        # Verbatim restatement of the doer's claims is not evidence.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=[Evidence(
                text=("the fencing token binds authority via a monotonic UUID; "
                      "a dead authority's token cannot validate at a recycled "
                      "address"),
                sources=["test-run:some-suite"],
                derived_from=[])]))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_PARROT, d.reasons)

    def test_derivative_only_rejected(self):
        # All sources are just the doer's own claims wearing labels.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=[Evidence(
                text="I reviewed the implementation and it is correct",
                sources=["doer-claims", "the doer's summary"],
                derived_from=[])]))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_DERIVATIVE, d.reasons)

    def test_circular_provenance_rejected(self):
        # Evidence derived from the artifact it certifies: the claim
        # supporting itself.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=[Evidence(
                text="independent test run confirms the token behavior",
                sources=["test-run:external-suite"],
                derived_from=["art-1"])]))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_CIRCULAR, d.reasons)

    def test_transitive_circular_provenance_rejected(self):
        # evidence:1 -> evidence:0 -> the artifact: still circular.
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS",
            evidence=[
                Evidence(text="baseline measurement notes",
                         sources=["lab-notebook:page-3"],
                         derived_from=["art-1"]),
                Evidence(text="cross-checked the baseline independently",
                         sources=["test-run:external-suite"],
                         derived_from=["evidence:0"]),
            ]))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_CIRCULAR, d.reasons)

    def test_empty_evidence_rejected(self):
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="PASS", evidence=[]))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_NO_EVIDENCE, d.reasons)

    def test_missing_verdict_rejected(self):
        d = certify(make_artifact(), Certification(
            artifact_id="art-1", verifier=OTHER, verdict="MAYBE",
            evidence=good_evidence()))
        self.assertFalse(d.accepted)
        self.assertIn(REJECT_NO_VERDICT, d.reasons)


class TestLedger(unittest.TestCase):
    def test_ledger_records_refusals_and_acceptances(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "ledger.jsonl")
            ledger = Ledger(path)
            art = make_artifact()
            refused = certify(art, Certification(
                artifact_id="art-1", verifier=DOER, verdict="PASS",
                evidence=good_evidence()), ledger=ledger)
            accepted = certify(art, Certification(
                artifact_id="art-1", verifier=OTHER, verdict="PASS",
                evidence=good_evidence()), ledger=ledger)
            self.assertFalse(refused.accepted)
            self.assertTrue(accepted.accepted)
            again = Ledger(path)
            self.assertEqual(len(again.entries), 2)
            by_verdict = {e["accepted"] for e in again.entries}
            self.assertEqual(by_verdict, {True, False})
            refused_entry = [e for e in again.entries if not e["accepted"]][0]
            self.assertIn(REJECT_SELF, refused_entry["reasons"])


class TestPrimitives(unittest.TestCase):
    def test_jaccard_identical_is_one(self):
        t = "the quick brown fox jumps over the lazy dog near the river bank"
        self.assertEqual(jaccard(_shingles(t), _shingles(t)), 1.0)

    def test_jaccard_disjoint_is_zero(self):
        self.assertEqual(
            jaccard(_shingles("alpha beta gamma delta epsilon zeta eta"),
                    _shingles("one two three four five six seven")), 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
