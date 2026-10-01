"""Adversarial tests for the nine-node activation ladder tracker (#864).

The tracker's job is to make per-node proof-ladder rung state visible, not
tribal — and fail-closed: a rung is only honored when the evidence its tier
requires is named. UNKNOWN != PASS.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_nine_node_activation_ladder",
    ROOT / "tools" / "validate_nine_node_activation_ladder.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
failures = _mod.failures
EXPECTED_ORDER = _mod.EXPECTED_ORDER
LADDER = _mod.LADDER

FIXTURE = ROOT / "BRAIN/03-KERNEL/0005-NINE-NODE-ACTIVATION-LADDER-V1.json"


@pytest.fixture()
def tracker():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_real_tracker_validates_green(tracker):
    assert failures(tracker) == []


def test_fractional_rung_rejected(tracker):
    tracker["nodes"]["SELF"]["current_rung"] = "CONTRACT.5"
    fails = failures(tracker)
    assert any("INVALID_RUNG" in f for f in fails)


def test_unknown_rung_string_rejected(tracker):
    tracker["nodes"]["LAW"]["current_rung"] = "contract"
    fails = failures(tracker)
    assert any("INVALID_RUNG" in f for f in fails)


def test_unit_claim_without_unit_evidence_rejected(tracker):
    tracker["nodes"]["ACT"]["current_rung"] = "UNIT"
    tracker["nodes"]["ACT"]["missing_rung"] = "INTEGRATION"
    fails = failures(tracker)
    assert any("EVIDENCE_MISSING_FOR_RUNG UNIT" in f for f in fails)


def test_ladder_prefix_rule_blocks_gap_claims(tracker):
    # Claims UNIT with UNIT evidence but silently drops CONTRACT evidence:
    # the prefix rule must reject the gap.
    node = tracker["nodes"]["KNOW"]
    node["current_rung"] = "UNIT"
    node["missing_rung"] = "INTEGRATION"
    node["evidence"]["UNIT"] = ["tests/test_know_unit.py"]
    del node["evidence"]["CONTRACT"]
    fails = failures(tracker)
    assert any("EVIDENCE_MISSING_FOR_RUNG CONTRACT" in f for f in fails)


def test_production_claim_without_receipts_rejected(tracker):
    node = tracker["nodes"]["PROVE"]
    node["current_rung"] = "PRODUCTION"
    node["missing_rung"] = "SUCCESSOR"
    fails = failures(tracker)
    # Missing UNIT/INTEGRATION/BEHAVIORAL/OUTCOME/PRODUCTION evidence tiers all fire.
    assert any("EVIDENCE_MISSING_FOR_RUNG PRODUCTION" in f for f in fails)
    assert any("EVIDENCE_MISSING_FOR_RUNG OUTCOME" in f for f in fails)


def test_missing_rung_must_be_exactly_next(tracker):
    tracker["nodes"]["CONNECT"]["missing_rung"] = "PRODUCTION"
    fails = failures(tracker)
    assert any("MISSING_RUNG_WRONG" in f for f in fails)


def test_canonical_status_without_ratification_rejected(tracker):
    tracker["status"] = "CANONICAL"
    fails = failures(tracker)
    assert any("STATUS_NOT_PROPOSED_CANONICAL" in f for f in fails)


def test_missing_node_rejected(tracker):
    del tracker["nodes"]["EVOLVE"]
    fails = failures(tracker)
    assert any("NODE_KEYS_MISMATCH" in f for f in fails)


def test_node_order_must_match_organism_contract(tracker):
    tracker["node_order"] = list(reversed(EXPECTED_ORDER))
    fails = failures(tracker)
    assert any("NODE_ORDER_MISMATCH" in f for f in fails)


def test_as_of_must_be_pinned_sha(tracker):
    tracker["as_of"] = "main"
    fails = failures(tracker)
    assert any("AS_OF_NOT_PINNED_SHA" in f for f in fails)


def test_blank_evidence_string_rejected(tracker):
    tracker["nodes"]["VERIFY"]["evidence"]["CONTRACT"] = [" "]
    fails = failures(tracker)
    assert any("EVIDENCE_MISSING_FOR_RUNG CONTRACT" in f for f in fails)


def test_tampered_ladder_rejected(tracker):
    tracker["proof_ladder"] = LADDER + ["TRANSCENDENT"]
    fails = failures(tracker)
    assert any("PROOF_LADDER_MISMATCH" in f for f in fails)


def test_successor_is_terminal(tracker):
    node = tracker["nodes"]["LEARN"]
    for rung in LADDER:
        node["evidence"][rung] = [f"receipts/{rung.lower()}.json"]
    node["current_rung"] = "SUCCESSOR"
    node["missing_rung"] = None
    fails = failures(tracker)
    assert fails == []


def test_mutated_copy_does_not_corrupt_fixture(tracker):
    mutated = copy.deepcopy(tracker)
    mutated["nodes"]["SELF"]["current_rung"] = "9.5"
    assert failures(mutated) != []
    assert failures(tracker) == []
