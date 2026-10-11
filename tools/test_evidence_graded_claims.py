#!/usr/bin/env python3
"""Adversarial tests for UD-06 evidence-graded claims.

Positive: well-evidenced claims pass at exactly the right grade.
Negative: every inflation pattern is refused — including unknown->PASS
conversion, staging->production promotion, outvoted counterexamples,
double-counted sources, and summaries that hide their non-claims.
"""
import unittest

from evidence_graded_claims import (
    ClaimRejected, assert_claim, dedupe_evidence, grade_claim, require_nonclaims,
    stamp, strongest_defensible,
)

STAGING = {"environment": "staging", "time": "2026-10-10",
           "population": "synthetic", "runtime": "linux-x64",
           "policy": "default", "provenance": "ci"}


def ev(eid, predicate, scope=None, kind="test_run", supports=True,
       content_hash=None, admissible=True):
    return {"id": eid, "kind": kind, "predicate": predicate,
            "scope": dict(scope or STAGING),
            "content_hash": content_hash or ("hash-" + eid),
            "admissible": admissible, "supports": supports}


def ob(oid, predicate, description, scope=None):
    return {"id": oid, "predicate": predicate, "description": description,
            "required_scope": dict(scope or STAGING)}


class TestPositive(unittest.TestCase):
    def test_fully_evidenced_claim_is_proven(self):
        claim = {"id": "c1", "text": "gate blocks unreviewed merges",
                 "obligations": [ob("o1", "blocks-unreviewed",
                                    "unreviewed merge blocked"),
                                 ob("o2", "blocks-unreviewed",
                                    "unreviewed merge blocked, second path")],
                 "evidence": [ev("e1", "blocks-unreviewed"),
                              ev("e2", "blocks-unreviewed")]}
        v = assert_claim(claim, "PROVEN")
        self.assertEqual(v["grade"], "PROVEN")

    def test_partial_coverage_is_supported_and_narrowed(self):
        claim = {"id": "c2", "text": "all three paths blocked",
                 "obligations": [ob("o1", "pa", "path A blocked"),
                                 ob("o2", "pb", "path B blocked"),
                                 ob("o3", "pc", "path C blocked")],
                 "evidence": [ev("e1", "pa"), ev("e2", "pb")]}
        v = assert_claim(claim, "SUPPORTED")
        self.assertEqual(v["grade"], "SUPPORTED")
        narrow = strongest_defensible(claim)
        self.assertEqual(narrow["holds_for"],
                         ["path A blocked", "path B blocked"])
        self.assertTrue(any("path C" in nc for nc in narrow["does_not_claim"]))

    def test_review_only_caps_at_supported(self):
        claim = {"id": "c3", "text": "design is sound",
                 "obligations": [ob("o1", "p", "reviewed design")],
                 "evidence": [ev("e1", "p", kind="review")]}
        v = assert_claim(claim, "SUPPORTED")
        self.assertEqual(v["grade"], "SUPPORTED")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "PROVEN")

    def test_underclaiming_is_allowed(self):
        claim = {"id": "c4", "text": "gate works",
                 "obligations": [ob("o1", "p", "gate works")],
                 "evidence": [ev("e1", "p")]}
        v = assert_claim(claim, "SUPPORTED")  # below the PROVEN it earned
        self.assertEqual(v["grade"], "PROVEN")


class TestNegative(unittest.TestCase):
    def test_verified_without_artifact_rejected(self):
        claim = {"id": "n1", "text": "verified: gate is safe",
                 "obligations": [ob("o1", "p", "gate safe")],
                 "evidence": []}
        with self.assertRaises(ClaimRejected) as cm:
            assert_claim(claim, "PROVEN")
        self.assertIn("UNKNOWN", str(cm.exception))

    def test_unknown_never_becomes_pass(self):
        claim = {"id": "n2", "text": "maybe fine",
                 "obligations": [ob("o1", "p", "fine")],
                 "evidence": []}
        v = grade_claim(claim)
        self.assertEqual(v["grade"], "UNKNOWN")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "SUPPORTED")

    def test_staging_does_not_prove_production(self):
        prod = dict(STAGING, environment="production")
        claim = {"id": "n3", "text": "production is safe",
                 "obligations": [ob("o1", "p", "production safe",
                                    scope=prod)],
                 "evidence": [ev("e1", "p", scope=STAGING)]}
        v = grade_claim(claim)
        self.assertEqual(v["grade"], "UNKNOWN")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "PROVEN")

    def test_eight_of_nine_is_not_nine(self):
        obligations = [ob("o%d" % i, "node-%d" % i, "node %d verified" % i)
                       for i in range(9)]
        claim = {"id": "n4", "text": "all nine nodes verified",
                 "obligations": obligations,
                 "evidence": [ev("e%d" % i, "node-%d" % i) for i in range(8)]}
        v = assert_claim(claim, "SUPPORTED")
        self.assertEqual(v["grade"], "SUPPORTED")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "PROVEN")

    def test_counterexample_cannot_be_outvoted(self):
        claim = {"id": "n5", "text": "all merges blocked",
                 "obligations": [ob("o1", "p", "merges blocked")],
                 "evidence": [ev("e%d" % i, "p") for i in range(8)]
                 + [ev("bad", "p", supports=False)]}
        v = grade_claim(claim)
        self.assertEqual(v["grade"], "CONTESTED")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "PROVEN")
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "SUPPORTED")

    def test_incompatible_contexts_block_composition(self):
        prod = dict(STAGING, environment="production")
        claim = {"id": "n6", "text": "both parts hold together",
                 "obligations": [ob("o1", "p", "part A holds"),
                                 ob("o2", "p", "part B holds",
                                    scope=prod)],
                 "evidence": [ev("e1", "p", scope=STAGING),
                              ev("e2", "p", scope=prod)]}
        v = assert_claim(claim, "SUPPORTED")
        self.assertEqual(v["grade"], "SUPPORTED")
        self.assertTrue(any("incompatible" in nc for nc in v["non_claims"]))
        with self.assertRaises(ClaimRejected):
            assert_claim(claim, "PROVEN")

    def test_overlapping_sources_not_double_counted(self):
        claim = {"id": "n7", "text": "gate works",
                 "obligations": [ob("o1", "p", "gate works"),
                                 ob("o2", "p", "gate works again")],
                 "evidence": [ev("e1", "p", content_hash="same"),
                              ev("e2", "p", content_hash="same")]}
        kept, dropped = dedupe_evidence(claim["evidence"])
        self.assertEqual(len(kept), 1)
        self.assertEqual(dropped, ["e2"])
        v = grade_claim(claim)
        self.assertTrue(any("counted once" in nc for nc in v["non_claims"]))

    def test_inadmissible_evidence_does_not_cover(self):
        claim = {"id": "n8", "text": "gate works",
                 "obligations": [ob("o1", "p", "gate works")],
                 "evidence": [ev("e1", "p", admissible=False)]}
        v = grade_claim(claim)
        self.assertEqual(v["grade"], "UNKNOWN")


class TestStamping(unittest.TestCase):
    def test_stamp_always_carries_non_claims(self):
        claim = {"id": "s1", "text": "gate works",
                 "obligations": [ob("o1", "p", "gate works")],
                 "evidence": [ev("e1", "p")]}
        out = stamp(grade_claim(claim))
        self.assertIn("DOES NOT CLAIM", out)

    def test_stamp_names_partial_coverage(self):
        claim = {"id": "s2", "text": "both hold",
                 "obligations": [ob("o1", "pa", "A holds"),
                                 ob("o2", "pb", "B holds")],
                 "evidence": [ev("e1", "pa")]}
        out = stamp(grade_claim(claim))
        self.assertIn("DOES NOT CLAIM", out)
        self.assertIn("B holds", out)

    def test_summary_without_nonclaims_rejected(self):
        with self.assertRaises(ValueError):
            require_nonclaims("All tests passed. The gate is fully verified.")

    def test_summary_with_nonclaims_accepted(self):
        require_nonclaims("All staging tests passed. Does not claim "
                          "production safety — production is unknown.")


if __name__ == "__main__":
    unittest.main()
