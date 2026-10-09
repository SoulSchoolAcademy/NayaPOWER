#!/usr/bin/env python3
"""Rehearsal tests for the unified activation gate.

These are LOCAL rehearsals against a fixed truth fixture — they prove the
predicate logic, not enforcement. Real proof is the CI workflow run
(.github/workflows/unified-activation-gate.yml), where the protected runner
resolves truth itself and every adversarial case must be REJECTed.
"""

import hashlib
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "/home/hatch/workspace/nayapower-worktrees/unified-gate/tools")
from activation_gate import check, CANONICAL_SOURCES, SCHEMA  # noqa: E402

NOW = datetime(2026, 10, 9, 16, 30, tzinfo=timezone.utc)
MAIN = "2bf25f3e62a71d6001b6796678e04c9fab5d7f5c"
BLOBS = {"design_contract": "a" * 40, "blocks_catalog": "b" * 40}
TRUTH = {"repository": "SoulSchoolAcademy/NayaPOWER", "main_sha": MAIN,
         "source_blobs": BLOBS, "now": NOW}


def make_receipt(**over):
    r = {
        "schema": SCHEMA,
        "status": "ACTIVATED",
        "session_id": "test-session",
        "naya_identity": "test-naya",
        "human_authority": "Shawn",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "job": "test job",
        "gates": ["Usefulness Gate"],
        "proof_plan": "ci run",
        "main_sha": MAIN,
        "activated_at": (NOW - timedelta(hours=1)).isoformat(),
        "loaded": dict(BLOBS),
    }
    r.update(over)
    return r


def deliverable_for(receipt_bytes):
    digest = hashlib.sha256(receipt_bytes).hexdigest()
    return "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></html>" % digest


def run(receipt, truth=TRUTH, deliverable=None):
    rb = json.dumps(receipt, sort_keys=True).encode()
    d = deliverable if deliverable is not None else deliverable_for(rb)
    return check(rb, d, truth)


class TestAcceptanceTable(unittest.TestCase):
    def test_lawful_pass(self):
        v, viols = run(make_receipt())
        self.assertEqual(v, "PASS", viols)

    def test_fabricated_self_asserted_reject(self):
        r = make_receipt(status="ACTIVATED")
        r["main_sha"] = "f" * 40  # plausible-looking but not live main
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_stale_tip_moved_reject(self):
        r = make_receipt(main_sha="0" * 40)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_wrong_repository_reject(self):
        r = make_receipt(repository="evil-corp/stolen-repo")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_REPOSITORY" in x for x in viols), viols)

    def test_abbreviated_sha_reject(self):
        r = make_receipt(main_sha=MAIN[:7])
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SHA_MALFORMED" in x for x in viols), viols)

    def test_missing_receipt_reject(self):
        v, viols = check(b"", "<html></html>", TRUTH)
        self.assertEqual(v, "REJECT")

    def test_tampered_receipt_reject(self):
        r = make_receipt()
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        tampered = rb.replace(b"ACTIVATED", b"ACTIVATED ")
        v, viols = check(tampered, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_DIGEST_MISMATCH" in x for x in viols), viols)

    def test_missing_citation_reject(self):
        r = make_receipt()
        rb = json.dumps(r, sort_keys=True).encode()
        v, viols = check(rb, "<html>no marker here</html>", TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_MISSING" in x for x in viols), viols)

    def test_unregistered_source_closed_world(self):
        loaded = dict(BLOBS)
        loaded["secret_sauce"] = "c" * 40
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_NOT_REGISTERED" in x for x in viols), viols)

    def test_missing_source_reject(self):
        loaded = {"design_contract": "a" * 40}
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_MISSING" in x for x in viols), viols)

    def test_fingerprint_mismatch_reject(self):
        loaded = {"design_contract": "d" * 40, "blocks_catalog": "b" * 40}
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_FINGERPRINT_MISMATCH" in x for x in viols), viols)

    def test_expired_reject(self):
        r = make_receipt(activated_at=(NOW - timedelta(hours=5)).isoformat())
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("ACTIVATION_EXPIRED" in x for x in viols), viols)

    def test_future_reject(self):
        r = make_receipt(activated_at=(NOW + timedelta(hours=1)).isoformat())
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("FUTURE_ACTIVATION" in x for x in viols), viols)

    def test_wrong_schema_v1_reject(self):
        r = make_receipt(schema="naya.activation.receipt.v1")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_SCHEMA" in x for x in viols), viols)

    def test_unactivated_reject(self):
        r = make_receipt(status="PENDING")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("NOT_ACTIVATED" in x for x in viols), viols)

    def test_untrusted_truth_fails_closed(self):
        r = make_receipt()
        rb = json.dumps(r, sort_keys=True).encode()
        v, viols = check(rb, deliverable_for(rb),
                         {"repository": "", "main_sha": "", "source_blobs": {},
                          "now": NOW})
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TRUTH_UNTRUSTED" in x for x in viols), viols)

    def test_repo_case_insensitive(self):
        r = make_receipt(repository="soulschoolacademy/nayapower")
        v, viols = run(r)
        self.assertEqual(v, "PASS", viols)


if __name__ == "__main__":
    unittest.main(verbosity=2)
