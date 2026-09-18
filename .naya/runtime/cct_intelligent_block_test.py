#!/usr/bin/env python3
"""Executable, dependency-free acceptance tests for the first CCT boundary."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

PATH = Path(__file__).with_name("cct_intelligent_block.py")
spec = importlib.util.spec_from_file_location("cct_intelligent_block", PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class CCTIntelligentBlockTests(unittest.TestCase):
    def block(self):
        return module.make_block(
            block_id="IB-A-0001",
            producer="NAYA-A",
            content={"lesson": "verified useful lesson", "value": "reusable"},
            evidence=[{"kind": "test", "id": "proof-1", "result": "PASS"}],
            permissions={"consumers": ["NAYA-B"], "purposes": ["consume"]},
            verification="VERIFIED",
        )

    def test_valid_block_is_accepted(self):
        self.assertTrue(module.verify_block(self.block(), consumer="NAYA-B").allowed)

    def test_unverified_block_is_denied(self):
        block = self.block(); block["verification"] = "UNVERIFIED"
        block["integrity"]["content_hash"] = module.content_hash(block)
        self.assertFalse(module.verify_block(block, consumer="NAYA-B").allowed)

    def test_missing_evidence_is_denied(self):
        block = self.block(); block["evidence"] = []
        block["integrity"]["content_hash"] = module.content_hash(block)
        self.assertFalse(module.verify_block(block, consumer="NAYA-B").allowed)

    def test_tampering_is_denied(self):
        block = self.block(); block["content"]["lesson"] = "tampered"
        self.assertFalse(module.verify_block(block, consumer="NAYA-B").allowed)

    def test_wrong_consumer_is_denied(self):
        self.assertFalse(module.verify_block(self.block(), consumer="NAYA-C").allowed)

    def test_revoked_parent_is_denied(self):
        block = self.block(); block["lifecycle"] = "REVOKED"
        block["integrity"]["content_hash"] = module.content_hash(block)
        self.assertFalse(module.verify_block(block, consumer="NAYA-B").allowed)

    def test_wrong_provenance_is_denied(self):
        block = self.block(); block["provenance"]["origin"] = "NAYA-C"
        block["integrity"]["content_hash"] = module.content_hash(block)
        self.assertFalse(module.verify_block(block, consumer="NAYA-B").allowed)

    def test_derivation_preserves_parent_lineage(self):
        parent = self.block()
        child = module.derive_block(
            parent, consumer="NAYA-B", block_id="IB-B-0001",
            content={"lesson": "derived reusable lesson"},
            evidence=[{"kind": "derivation", "parent": "IB-A-0001"}],
        )
        self.assertEqual(child["provenance"]["parent"], "IB-A-0001")
        self.assertEqual(child["provenance"]["origin"], "NAYA-B")
        self.assertEqual(child["provenance"]["derivation"], "independent-consumption")
        self.assertTrue(module.verify_block(child, consumer="NAYA-B").allowed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
