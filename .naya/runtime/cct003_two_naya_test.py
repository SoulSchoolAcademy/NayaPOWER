#!/usr/bin/env python3
"""CCT-003 local integration proof: producer -> isolated consumer -> lineage."""
import unittest
from cct_intelligent_block import make_block, verify_block, derive_block


class CCT003Tests(unittest.TestCase):
    def setUp(self):
        self.source_conversation = "PRIVATE-NAYA-A-CONVERSATION-MUST-NOT-TRAVEL"
        self.block_a = make_block(
            block_id="IB-CCT003-A",
            producer="NAYA-A",
            content={"learning": "A verified lesson can be safely packaged for an explicitly authorized consumer."},
            evidence=[{"kind": "test", "ref": "cct-003-fixture"}],
            permissions={"consumers": ["NAYA-B"], "purposes": ["consume"]},
            verification="VERIFIED",
        )

    def test_a_produces_authorized_block(self):
        decision = verify_block(self.block_a, consumer="NAYA-B")
        self.assertTrue(decision.allowed)

    def test_b_receives_artifact_without_source_conversation(self):
        delivered = {"block": self.block_a, "protocol": {"consumer": "NAYA-B"}}
        self.assertNotIn("source_conversation", delivered)
        self.assertNotIn(self.source_conversation, str(delivered))

    def test_b_independently_consumes_and_derives_b(self):
        decision = verify_block(self.block_a, consumer="NAYA-B")
        self.assertTrue(decision.allowed)
        block_b = derive_block(
            self.block_a,
            consumer="NAYA-B",
            block_id="IB-CCT003-B",
            content={"learning": "The receiving Naya can derive a new artifact without receiving the private source conversation."},
            evidence=[{"kind": "test", "ref": "cct-003-fixture"}],
        )
        self.assertEqual(block_b["provenance"]["parent"], self.block_a["block_id"])
        self.assertEqual(block_b["provenance"]["origin"], "NAYA-B")
        self.assertEqual(block_b["provenance"]["derivation"], "independent-consumption")
        self.assertTrue(verify_block(block_b, consumer="NAYA-B").allowed)

    def test_unauthorized_consumer_is_denied(self):
        self.assertFalse(verify_block(self.block_a, consumer="NAYA-C").allowed)

    def test_tampered_parent_cannot_be_derived(self):
        tampered = dict(self.block_a)
        tampered["content"] = {"learning": "ALTERED"}
        with self.assertRaises(ValueError):
            derive_block(tampered, consumer="NAYA-B", block_id="IB-CCT003-B2", content={"x": 1}, evidence=[{"kind": "test"}])

    def test_fake_independence_is_not_claimed(self):
        block_b = derive_block(self.block_a, consumer="NAYA-B", block_id="IB-CCT003-B3", content={"x": 1}, evidence=[{"kind": "test"}])
        self.assertEqual(block_b["provenance"]["parent"], self.block_a["block_id"])
        self.assertNotEqual(block_b["provenance"]["origin"], self.block_a["provenance"]["origin"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
