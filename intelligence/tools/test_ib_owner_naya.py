#!/usr/bin/env python3
"""System ownership tests for the Intelligent Blocks canonical contract.

Proves Shawn's 2026-10-11 ~22:34Z decision is recorded OPERATIONALLY:
- every seed block is owned by NAYA (the collective system), exactly;
- any other owner — empty or a per-block human — fails loudly;
- the ownership authority path (verification/promotion gates) is exercised,
  positive and negative, gate by gate.

Stdlib + unittest, matching test_ib_reconcile.py conventions.
"""
import copy
import glob
import json
import os
import sys
import unittest

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(TOOLS_DIR))
BLOCKS_DIR = os.path.join(REPO_ROOT, "intelligence", "blocks")
REGISTRY_PATH = os.path.join(BLOCKS_DIR, "REGISTRY.json")

sys.path.insert(0, TOOLS_DIR)
sys.path.insert(0, REPO_ROOT)

from ib_reconcile import (  # noqa: E402
    OWNER_NAYA,
    OWNERSHIP_AUTHORITY_PATH,
    SYSTEM_OWNERSHIP_DECISION,
    from_persisted_row,
    run_authority_path,
    to_persisted_row,
    validate_system_owned,
    validate_v11,
)
from kernel.supabase_intelligent_blocks import IntelligentBlock  # noqa: E402


def seed_files():
    return sorted(glob.glob(os.path.join(BLOCKS_DIR, "IB-0*.json")))


def load_block(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_registry():
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def registry_ctx(registry=None):
    return {"registry": registry or load_registry()}


class TestSeedBlocksSystemOwned(unittest.TestCase):
    def test_twenty_seed_files_exist(self):
        self.assertEqual(len(seed_files()), 20)

    def test_every_seed_block_owned_by_naya(self):
        for path in seed_files():
            b = load_block(path)
            with self.subTest(block=os.path.basename(path)):
                self.assertEqual(b["owner_id"], OWNER_NAYA)
                self.assertEqual(validate_v11(b), [])
                self.assertIsNone(validate_system_owned(b))

    def test_owner_lock_recorded_in_provenance(self):
        for path in seed_files():
            b = load_block(path)
            with self.subTest(block=os.path.basename(path)):
                lock = b["provenance"].get("owner_lock")
                self.assertIsNotNone(lock, "owner_lock decision record missing")
                self.assertEqual(lock["owner_id"], OWNER_NAYA)
                self.assertEqual(lock["decided_by"], "Shawn")
                self.assertFalse(b["provenance"].get("owner_assignment_pending"),
                                 "owner_assignment_pending must be resolved")

    def test_decision_record_is_machine_readable(self):
        self.assertEqual(SYSTEM_OWNERSHIP_DECISION["owner_id"], OWNER_NAYA)
        self.assertEqual(SYSTEM_OWNERSHIP_DECISION["decided_by"], "Shawn")
        self.assertIn("bottleneck", SYSTEM_OWNERSHIP_DECISION["decision"])


class TestOwnershipRejects(unittest.TestCase):
    def test_empty_owner_fails_loudly(self):
        b = load_block(seed_files()[0])
        b["owner_id"] = ""
        problems = validate_v11(b)
        self.assertTrue(any("owner_id" in p for p in problems),
                        f"validate_v11 must fail loudly on empty owner: {problems}")
        self.assertIsNotNone(validate_system_owned(b))

    def test_per_block_human_owner_rejected(self):
        # Shawn explicitly declined per-block ownership: it recreates the bottleneck.
        for human in ("Shawn", "Naya 5", "naya-alpha"):
            b = load_block(seed_files()[0])
            b["owner_id"] = human
            with self.subTest(owner=human):
                problem = validate_system_owned(b)
                self.assertIsNotNone(problem)
                self.assertIn("bottleneck", problem)

    def test_normalize_still_never_invents_owner(self):
        # The pre-existing guarantee stands: normalization must not invent
        # an owner to make validation pass — the word comes from Shawn, not code.
        from ib_reconcile import normalize_file_block
        raw = {"id": "IB-9999", "title": "x", "principle": "One sentence."}
        b = normalize_file_block(raw, default_owner_id="")
        self.assertEqual(b["owner_id"], "")
        self.assertIsNotNone(validate_system_owned(b))


class TestAuthorityPath(unittest.TestCase):
    def test_path_has_six_gates(self):
        names = [name for name, _, _ in OWNERSHIP_AUTHORITY_PATH]
        self.assertEqual(names, [
            "ownership-locked", "envelope-identity", "epistemic-consistency",
            "verification-ladder-evidence", "graduation-path", "registry-integrity",
        ])

    def test_every_gate_described(self):
        for name, _, exercises in OWNERSHIP_AUTHORITY_PATH:
            self.assertTrue(exercises, f"gate {name} has no description")

    def test_positive_every_seed_block_all_gates(self):
        ctx = registry_ctx()
        for path in seed_files():
            b = load_block(path)
            results = run_authority_path(b, ctx)
            failed = [(g, p) for g, p in results if p is not None]
            with self.subTest(block=os.path.basename(path)):
                self.assertEqual(failed, [], f"gates failed: {failed}")

    def test_negative_ownership_locked(self):
        from ib_reconcile import check_ownership_locked
        b = load_block(seed_files()[0])
        bad = copy.deepcopy(b); bad["owner_id"] = ""
        self.assertIsNotNone(check_ownership_locked(bad))
        bad2 = copy.deepcopy(b); bad2["owner_id"] = "Shawn"
        self.assertIsNotNone(check_ownership_locked(bad2))

    def test_negative_envelope_identity(self):
        from ib_reconcile import check_envelope_identity
        b = load_block(seed_files()[0])
        bad = copy.deepcopy(b); bad["owner_id"] = ""
        self.assertIsNotNone(check_envelope_identity(bad))

    def test_negative_epistemic_consistency(self):
        from ib_reconcile import check_epistemic_consistency
        b = load_block(seed_files()[0])  # APPLIED -> CANDIDATE/DURABLE
        bad = copy.deepcopy(b); bad["understanding_state"] = "VERIFIED"
        self.assertIsNotNone(check_epistemic_consistency(bad))
        bad2 = copy.deepcopy(b); bad2["status"] = "DRAFT"
        self.assertIsNotNone(check_epistemic_consistency(bad2))

    def test_negative_ladder_evidence(self):
        from ib_reconcile import check_ladder_evidence
        b = load_block(seed_files()[0])
        bad = copy.deepcopy(b); bad["evidence"] = []
        self.assertIsNotNone(check_ladder_evidence(bad))

    def test_negative_graduation(self):
        from ib_reconcile import check_graduation
        b = load_block(seed_files()[0])
        bad = copy.deepcopy(b); bad["graduation"]["stage"] = "production"
        self.assertIsNotNone(check_graduation(bad))
        bad2 = copy.deepcopy(b)
        bad2["graduation"] = {"stage": "code-gate", "next_step": "x", "enforced_by": None}
        self.assertIsNotNone(check_graduation(bad2))

    def test_negative_registry_integrity(self):
        from ib_reconcile import check_registry_consistency
        b = load_block(seed_files()[0])
        # block absent from the registry
        self.assertIsNotNone(check_registry_consistency(b, {"registry": {"blocks": []}}))
        # registry entry claims a different owner
        reg = load_registry()
        bid = b["intelligent_block_id"]
        for e in reg["blocks"]:
            if e["id"] == bid:
                e["owner_id"] = "Shawn"
        self.assertIsNotNone(check_registry_consistency(b, {"registry": reg}))


class TestOwnerSurvivesPersistence(unittest.TestCase):
    def test_round_trip_preserves_system_owner(self):
        b = load_block(seed_files()[0])
        row = to_persisted_row(b)
        self.assertEqual(row["owner_id"], OWNER_NAYA)
        back = from_persisted_row(row)
        self.assertEqual(back["owner_id"], OWNER_NAYA)

    def test_kernel_envelope_accepts_system_owner(self):
        b = load_block(seed_files()[0])
        row = to_persisted_row(b)
        ib = IntelligentBlock.from_row(row)
        self.assertEqual(ib.owner_id, OWNER_NAYA)

    def test_kernel_envelope_still_raises_on_empty_owner(self):
        row = to_persisted_row(load_block(seed_files()[0]))
        row["owner_id"] = ""
        with self.assertRaises(ValueError):
            IntelligentBlock.from_row(row)


class TestRegistryCarriesOwner(unittest.TestCase):
    def test_all_registry_entries_owned_by_naya(self):
        reg = load_registry()
        self.assertEqual(reg["count"], 20)
        for e in reg["blocks"]:
            with self.subTest(id=e["id"]):
                self.assertEqual(e["owner_id"], OWNER_NAYA)


class TestIbCliOwnershipBehavior(unittest.TestCase):
    def test_ib_validate_is_general_schema(self):
        # ib validate requires a DECLARED owner, any declared owner. The
        # NAYA-only rule is the seed-corpus rule (validate_system_owned),
        # enforced on intelligence/blocks/ by the seed-corpus tests — the
        # generic authoring flow is not restricted.
        sys.path.insert(0, TOOLS_DIR)
        import ib as ib_cli
        b = load_block(seed_files()[0])
        self.assertEqual(ib_cli.validate_block(b), [])
        other = copy.deepcopy(b); other["owner_id"] = "owner-uuid-test"
        self.assertEqual(ib_cli.validate_block(other), [])
        empty = copy.deepcopy(b); empty["owner_id"] = ""
        self.assertTrue(any("owner_id" in p for p in ib_cli.validate_block(empty)))

    def test_create_defaults_owner_to_naya(self):
        # Shawn's word covers all future blocks: the CLI births them
        # system-owned unless a non-system context explicitly overrides.
        sys.path.insert(0, TOOLS_DIR)
        import ib as ib_cli
        args = ib_cli.build_parser().parse_args([
            "create", "--title", "T", "--principle", "One plain sentence.",
            "--who", "tester", "--when", "2026-10-11", "--context", "cli test",
        ])
        self.assertEqual(args.owner_id, "NAYA")


if __name__ == "__main__":
    unittest.main()
