#!/usr/bin/env python3
import copy
import unittest
from datetime import datetime, timedelta, timezone

from cct_intelligent_block import make_block
from cct004_adversarial import validate_block_semantics


class CCT004Tests(unittest.TestCase):
    def setUp(self):
        self.parent = make_block(
            block_id="CCT004-A", producer="NAYA-A",
            content={"learning": "verified reusable lesson"},
            evidence=[{"kind": "test", "ref": "cct004"}],
            permissions={"consumers": ["NAYA-B"], "purposes": ["consume"]},
            verification="VERIFIED",
        )
        self.child = make_block(
            block_id="CCT004-B", producer="NAYA-B",
            content={"learning": "derived lesson"},
            evidence=[{"kind": "test", "ref": "cct004"}],
            permissions={"consumers": ["NAYA-B"], "purposes": ["consume"]},
            verification="SUPPORTED", parent="CCT004-A",
            derivation="independent-consumption",
        )

    def test_replay_and_duplicate_identity_denied(self):
        self.assertFalse(validate_block_semantics(self.parent, consumer="NAYA-B", known_ids={"CCT004-A"})[0])

    def test_forged_provenance_denied(self):
        b = copy.deepcopy(self.parent); b["provenance"]["origin"] = "NAYA-Z"
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B")[0])

    def test_wrong_parent_denied(self):
        b = copy.deepcopy(self.child); b["provenance"]["parent"] = "OTHER"
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B", parent=self.parent)[0])

    def test_revoked_parent_denied(self):
        p = copy.deepcopy(self.parent); p["lifecycle"] = "REVOKED"
        self.assertFalse(validate_block_semantics(self.child, consumer="NAYA-B", parent=p)[0])

    def test_superseded_parent_denied(self):
        p = copy.deepcopy(self.parent); p["lifecycle"] = "SUPERSEDED"
        self.assertFalse(validate_block_semantics(self.child, consumer="NAYA-B", parent=p)[0])

    def test_contradictory_verified_claim_denied(self):
        b = copy.deepcopy(self.parent); b["evidence"] = [{"kind": "test", "contradicts": True}]
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B")[0])

    def test_fake_independence_denied(self):
        b = copy.deepcopy(self.child); b["provenance"]["origin"] = "NAYA-A"
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B", parent=self.parent)[0])

    def test_permission_escalation_denied(self):
        b = copy.deepcopy(self.child); b["permissions"]["consumers"] = ["*"]
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B", parent=self.parent)[0])

    def test_circular_lineage_denied(self):
        b = copy.deepcopy(self.child); b["provenance"]["parent"] = "CCT004-B"
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B", parent=self.parent)[0])

    def test_stale_block_denied(self):
        b = copy.deepcopy(self.parent)
        b["valid_until"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B")[0])

    def test_oversized_payload_denied(self):
        b = copy.deepcopy(self.parent); b["content"] = {"x": "A" * 40000}
        b["integrity"]["content_hash"] = __import__("cct_intelligent_block").content_hash(b)
        self.assertFalse(validate_block_semantics(b, consumer="NAYA-B")[0])

    def test_valid_child_accepted(self):
        self.assertTrue(validate_block_semantics(self.child, consumer="NAYA-B", parent=self.parent)[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
