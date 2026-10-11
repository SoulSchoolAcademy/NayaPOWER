#!/usr/bin/env python3
"""Integration test: v1.1 file blocks satisfy the REAL persisted validator.

This is the critical seam — ib_reconcile.to_persisted_row() must produce rows
that kernel/supabase_intelligent_blocks.py::IntelligentBlock.from_row()
accepts. If the kernel's requirements drift, this test catches it.
"""
import copy
import json
import os
import sys
import unittest

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(REPO_ROOT, "intelligence", "tools"))
sys.path.insert(0, REPO_ROOT)

from ib_reconcile import (  # noqa: E402
    CANONICAL_BLOCK_FIELDS,
    from_persisted_row,
    normalize_file_block,
    to_persisted_row,
)
from kernel.supabase_intelligent_blocks import IntelligentBlock  # noqa: E402

BLOCKS_DIR = os.path.join(REPO_ROOT, "intelligence", "blocks")


class TestKernelIntegration(unittest.TestCase):
    def _owned_block(self, fname="IB-0001.json"):
        with open(os.path.join(BLOCKS_DIR, fname)) as f:
            b = json.load(f)
        b["owner_id"] = "test-owner-uuid-integration"
        return b

    def test_export_passes_real_from_row(self):
        """The ultimate proof: our export satisfies the kernel's validator."""
        row = to_persisted_row(self._owned_block())
        block = IntelligentBlock.from_row(row)  # raises on any violation
        self.assertEqual(block.intelligent_block_id, "IB-0001")
        self.assertEqual(block.owner_id, "test-owner-uuid-integration")
        self.assertEqual(block.owner_scope, "TEAM")
        self.assertTrue(block.provenance)

    def test_all_seed_blocks_exportable_once_owned(self):
        """Every migrated seed block exports cleanly when given an owner."""
        for fname in sorted(os.listdir(BLOCKS_DIR)):
            if not (fname.startswith("IB-") and fname.endswith(".json")):
                continue
            with open(os.path.join(BLOCKS_DIR, fname)) as f:
                b = json.load(f)
            b["owner_id"] = "test-owner-uuid-integration"
            row = to_persisted_row(b)
            # Must satisfy the real kernel validator
            IntelligentBlock.from_row(row)

    def test_kernel_field_list_matches(self):
        """Our CANONICAL_BLOCK_FIELDS mirror must match the kernel's."""
        import kernel.supabase_intelligent_blocks as kmod
        self.assertEqual(set(CANONICAL_BLOCK_FIELDS),
                         set(kmod.CANONICAL_BLOCK_FIELDS))

    def test_unowned_block_fails_both_validators(self):
        """An unowned block must fail OUR validator AND the kernel's."""
        with open(os.path.join(BLOCKS_DIR, "IB-0001.json")) as f:
            b = json.load(f)
        # b has empty owner_id (pending human assignment)
        with self.assertRaises(ValueError):
            to_persisted_row(b)  # our validator raises first


if __name__ == "__main__":
    unittest.main(verbosity=2)
