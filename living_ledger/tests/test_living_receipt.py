"""Tests for living_ledger.receipt.LivingReceipt.

Negative controls first: every envelope violation must refuse at
construction. Positive controls prove the mapping onto the ledger writer.
"""
import json

import pytest

from living_ledger.receipt import (
    LivingReceipt,
    SCOPES,
    SCOPE_TO_PRIVACY,
    SOURCE_TABLE,
)


def _good(**overrides):
    base = dict(
        actor="naya2/build-lane",
        action="shipped D51 first slice",
        evidence=("spec:D51-LIVING-LEDGER-V1.md", "tests:27 green"),
        timestamp="2026-10-11T10:50:28Z",
        scope="team",
    )
    base.update(overrides)
    return LivingReceipt(**base)


# --- negative controls: construction refuses -----------------------------

def test_empty_evidence_refused():
    with pytest.raises(ValueError):
        _good(evidence=())


def test_evidence_list_coerced_but_empty_list_refused():
    with pytest.raises(ValueError):
        _good(evidence=[])


def test_blank_evidence_item_refused():
    with pytest.raises(ValueError):
        _good(evidence=("  ",))


def test_non_string_evidence_item_refused():
    with pytest.raises(ValueError):
        _good(evidence=(123,))


def test_empty_actor_refused():
    with pytest.raises(ValueError):
        _good(actor="   ")


def test_empty_action_refused():
    with pytest.raises(ValueError):
        _good(action="")


def test_malformed_timestamp_refused():
    with pytest.raises(ValueError):
        _good(timestamp="yesterday afternoon")


def test_empty_timestamp_refused():
    with pytest.raises(ValueError):
        _good(timestamp="")


def test_unknown_scope_refused():
    with pytest.raises(ValueError):
        _good(scope="everyone")


def test_non_dict_metadata_refused():
    with pytest.raises(ValueError):
        _good(metadata=["not", "a", "dict"])


# --- positive controls ----------------------------------------------------

def test_well_formed_receipt_constructs():
    receipt = _good()
    assert receipt.actor == "naya2/build-lane"
    assert receipt.scope == "team"
    assert receipt.evidence == ("spec:D51-LIVING-LEDGER-V1.md", "tests:27 green")


def test_timestamp_z_and_offset_both_accepted():
    assert _good(timestamp="2026-10-11T10:50:28Z").timestamp.endswith("Z")
    assert _good(timestamp="2026-10-11T10:50:28+00:00").timestamp.endswith("+00:00")


def test_receipt_id_deterministic():
    assert _good().receipt_id == _good().receipt_id


def test_receipt_id_changes_with_action():
    assert _good().receipt_id != _good(action="did something else").receipt_id


def test_receipt_id_changes_with_evidence():
    assert _good().receipt_id != _good(evidence=("other proof",)).receipt_id


def test_receipt_id_is_sha256_hex():
    rid = _good().receipt_id
    assert len(rid) == 64
    int(rid, 16)  # raises if not hex


def test_scope_to_privacy_mapping_covers_all_scopes():
    assert set(SCOPE_TO_PRIVACY) == set(SCOPES)
    assert SCOPE_TO_PRIVACY == {
        "self": "PRIVATE",
        "team": "SHARED",
        "collective": "COLLECTIVE",
        "public": "PUBLIC",
    }


def test_to_ledger_params_maps_every_field():
    receipt = _good(metadata={"lane": "build"})
    params = receipt.to_ledger_params(owner_id="owner-123")
    assert params["p_owner_id"] == "owner-123"
    assert params["p_event_type"] == "shipped D51 first slice"
    assert params["p_source_table"] == SOURCE_TABLE
    assert params["p_source_id"] == receipt.receipt_id
    assert params["p_event_at"] == "2026-10-11T10:50:28Z"
    assert params["p_privacy_classification"] == "SHARED"
    assert params["p_status"] == "RECORDED"
    assert params["p_evidence_refs"] == [
        "spec:D51-LIVING-LEDGER-V1.md", "tests:27 green"]
    assert params["p_metadata"]["actor"] == "naya2/build-lane"
    assert params["p_metadata"]["scope"] == "team"
    assert params["p_metadata"]["lane"] == "build"


def test_to_ledger_params_scope_drives_privacy():
    assert _good(scope="self").to_ledger_params("o")[
        "p_privacy_classification"] == "PRIVATE"
    assert _good(scope="public").to_ledger_params("o")[
        "p_privacy_classification"] == "PUBLIC"


def test_to_ledger_params_refuses_empty_owner():
    with pytest.raises(ValueError):
        _good().to_ledger_params(owner_id="  ")


def test_to_json_round_trip():
    receipt = _good()
    data = json.loads(receipt.to_json())
    assert data["receipt_id"] == receipt.receipt_id
    assert data["evidence"] == list(receipt.evidence)
    assert data["scope"] == "team"


def test_receipt_is_frozen():
    receipt = _good()
    with pytest.raises(Exception):
        receipt.action = "rewrote history"
