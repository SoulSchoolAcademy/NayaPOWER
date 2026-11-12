#!/usr/bin/env python3
"""
Tests for the Gap-2 activation pre-gate.
Run: python3 -m pytest tools/test_activation_pregate.py -v
     (or: python3 tools/test_activation_pregate.py)
"""

import hashlib
import json
import os
import sys
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from activation_pregate import (
    check_activation_receipt,
    ActivationRefused,
    REPO,
)

# Fixed trusted state for tests (never hits the network)
TRUSTED = {
    "main_sha": "a" * 40,
    "design_blob": "b" * 40,
    "blocks_blob": "c" * 40,
    "goals_digest": "d" * 64,
    "feed_digest": "e" * 64,
}


def make_receipt(**overrides):
    now = datetime.now(timezone.utc)
    receipt = {
        "schema": "naya.activation.receipt.v2",
        "status": "ACTIVATED",
        "session_id": "sess-test-001",
        "naya_identity": "naya-test-doer",
        "human_authority": "Shawn Vibert",
        "repository": REPO,
        "job": "gap2-pregate-test",
        "gates": ["activation", "design"],
        "proof_plan": "unit tests",
        "main_sha": TRUSTED["main_sha"],
        "loaded": {
            "design_blob": TRUSTED["design_blob"],
            "blocks_blob": TRUSTED["blocks_blob"],
            "goals_digest": TRUSTED["goals_digest"],
            "feed_digest": TRUSTED["feed_digest"],
        },
        "activated_at": (now - timedelta(minutes=30)).isoformat(),
    }
    receipt.update(overrides)
    return receipt


def receipt_digest(receipt):
    return hashlib.sha256(
        json.dumps(receipt, sort_keys=True).encode()
    ).hexdigest()


def html_with_citation(receipt):
    return (
        "<!DOCTYPE html><html><head><title>t</title></head><body>"
        f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{receipt_digest(receipt)} -->"
        "</body></html>"
    )


class TestPreGate(unittest.TestCase):
    def test_valid_receipt_passes(self):
        r = make_receipt()
        ok, violations, digest = check_activation_receipt(
            r, TRUSTED, html_with_citation(r)
        )
        self.assertTrue(ok)
        self.assertEqual(violations, [])
        self.assertEqual(digest, receipt_digest(r))

    def test_missing_receipt_refuses(self):
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(None, TRUSTED, "<html></html>")
        self.assertIn("RECEIPT_MISSING", cm.exception.violations)

    def test_missing_trusted_state_refuses(self):
        r = make_receipt()
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, None, html_with_citation(r))
        self.assertIn("TRUSTED_STATE_MISSING", cm.exception.violations)

    def test_wrong_schema_refuses(self):
        r = make_receipt(schema="naya.activation.receipt.v1")
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("WRONG_SCHEMA_OR_STATE", cm.exception.violations)

    def test_unactivated_status_refuses(self):
        r = make_receipt(status="PENDING")
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("WRONG_SCHEMA_OR_STATE", cm.exception.violations)

    def test_incomplete_identity_refuses(self):
        r = make_receipt(naya_identity=None)
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("IDENTITY_INCOMPLETE", cm.exception.violations)

    def test_wrong_repository_refuses(self):
        r = make_receipt(repository="evil-corp/forged-repo")
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("REPOSITORY_MISMATCH", cm.exception.violations)

    def test_missing_job_gates_refuses(self):
        r = make_receipt(gates=[])
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("JOB_GATES_PROOF_MISSING", cm.exception.violations)

    def test_stale_main_sha_refuses(self):
        r = make_receipt(main_sha="f" * 40)  # old tip
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("MAIN_STALE_OR_MISMATCH", cm.exception.violations)

    def test_stale_design_blob_refuses(self):
        r = make_receipt()
        r["loaded"]["design_blob"] = "0" * 40
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("DOC_MISMATCH_DESIGN_BLOB", cm.exception.violations)

    def test_stale_feed_digest_refuses(self):
        r = make_receipt()
        r["loaded"]["feed_digest"] = "0" * 64
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("CONTEXT_MISMATCH_FEED_DIGEST", cm.exception.violations)

    def test_expired_activation_refuses(self):
        old = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        r = make_receipt(activated_at=old)
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("ACTIVATION_EXPIRED", cm.exception.violations)

    def test_future_activation_refuses(self):
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        r = make_receipt(activated_at=future)
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html_with_citation(r))
        self.assertIn("FUTURE_ACTIVATION", cm.exception.violations)

    def test_missing_citation_refuses(self):
        r = make_receipt()
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, "<html><body>no citation</body></html>")
        self.assertIn("DELIVERABLE_RECEIPT_CITATION_MISSING", cm.exception.violations)

    def test_tampered_receipt_breaks_citation(self):
        # Builder modifies receipt after "activation" — the citation in the
        # HTML no longer matches the recomputed digest.
        r = make_receipt()
        html = html_with_citation(r)
        r["main_sha"] = TRUSTED["main_sha"]  # same, but...
        r["job"] = "tampered-job"  # ...content changed -> digest changes
        with self.assertRaises(ActivationRefused) as cm:
            check_activation_receipt(r, TRUSTED, html)
        self.assertIn("DELIVERABLE_RECEIPT_CITATION_MISSING", cm.exception.violations)


if __name__ == "__main__":
    unittest.main(verbosity=2)
