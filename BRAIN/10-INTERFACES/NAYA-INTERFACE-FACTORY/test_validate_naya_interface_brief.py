#!/usr/bin/env python3
"""Regression tests for the Naya Interface Brief semantic gate."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from validate_naya_interface_brief import validate_brief  # noqa: E402


def load_sample():
    return json.loads((HERE / "PERSONAL-WORLD-EXAMPLE-BRIEF.json").read_text(encoding="utf-8"))


def load_pieces():
    path = HERE.parent / "SMART-FACTORY-CANON" / "pieces.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


class InterfaceBriefGateTests(unittest.TestCase):
    def setUp(self):
        self.sample = load_sample()
        self.pieces = load_pieces()

    def test_example_brief_passes_prebuild_gate(self):
        errors = validate_brief(self.sample, self.pieces, stage="prebuild")
        self.assertEqual([], errors, "\n".join(errors))

    def test_example_does_not_claim_release_readiness(self):
        errors = validate_brief(self.sample, self.pieces, stage="release")
        self.assertTrue(any("must be true before release" in item for item in errors))

    def test_missing_project_intelligence_reference_blocks(self):
        brief = copy.deepcopy(self.sample)
        brief["project"]["pi_ref"] = ""
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("project.pi_ref" in item for item in errors))

    def test_unknown_data_cannot_be_presented_as_live(self):
        brief = copy.deepcopy(self.sample)
        brief["screens"][0]["states"].append({
            "state": "live",
            "presentation": "Live items",
            "recovery": "Refresh"
        })
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("unproven data" in item for item in errors))

    def test_duplicate_screen_route_blocks(self):
        brief = copy.deepcopy(self.sample)
        brief["screens"][1]["route"] = brief["screens"][0]["route"]
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("duplicate screen route" in item for item in errors))

    def test_first_view_support_is_bounded(self):
        brief = copy.deepcopy(self.sample)
        brief["screens"][0]["first_view"]["supporting_items"] = ["a", "b", "c", "d"]
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("more than three supporting items" in item for item in errors))

    def test_screen_requires_exactly_one_focal_section(self):
        brief = copy.deepcopy(self.sample)
        brief["screens"][0]["sections"][0]["priority"] = "supporting"
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("exactly one focal section" in item for item in errors))

    def test_action_requires_recovery_contract(self):
        brief = copy.deepcopy(self.sample)
        del brief["screens"][0]["actions"][0]["failure_recovery"]
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("failure_recovery" in item for item in errors))

    def test_naya_target_size_floor_is_44(self):
        brief = copy.deepcopy(self.sample)
        brief["screens"][0]["accessibility"]["minimum_target_px"] = 32
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("44px Naya house rule" in item for item in errors))

    def test_unknown_piece_fails_when_registry_is_supplied(self):
        brief = copy.deepcopy(self.sample)
        brief["component_manifest"][0]["piece_id"] = "NAYA-HRO-999"
        errors = validate_brief(brief, self.pieces or {})
        self.assertTrue(any("does not resolve" in item for item in errors))

    def test_missing_narrow_viewport_blocks(self):
        brief = copy.deepcopy(self.sample)
        brief["viewport_matrix"] = [v for v in brief["viewport_matrix"] if v["width"] > 320]
        errors = validate_brief(brief, self.pieces)
        self.assertTrue(any("320 CSS px" in item for item in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
