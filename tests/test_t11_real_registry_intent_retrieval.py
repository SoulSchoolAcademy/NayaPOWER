"""Cold-intent T11 retrieval smoke test against real canonical repo files.

Unlike stubbed fixture retrieval, this imports the actual Smart Note selector
and reads the committed registry and persisted human projection. This proves
index discoverability only; LAW access and ACT behavior require separate proof.
"""
import hashlib
from pathlib import Path

import pytest

from tools import smart_note_v2 as sn

SN_ID = "SN-782"
IB_ID = "IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical"
SHA256 = "9ce231bbe2eac3cfe4642e84dc5f5a3b33d20f0ae3dd906c6d75b40800e90032"


def _t11():
    entries = [e for e in sn.load_json(sn.REGISTRY)["entries"] if e.get("smart_note_id") == SN_ID]
    assert len(entries) == 1, "T11 ID missing or ambiguous in canonical registry"
    entry = entries[0]
    assert entry["intelligent_block_id"] == IB_ID
    assert entry["content_hash"] == SHA256
    assert entry["projection_status"] == "GITHUB_BRAIN_PUBLISHED"
    assert entry["smart_link_status"] == "ACTIVE_AUTH_GATED"
    assert entry["truth_state"] == "CANDIDATE"
    assert entry["scope"] == "PRIVATE"
    return entry


def test_fresh_selector_retrieves_t11_from_real_intent_without_handoff():
    """Tests the ranking path in the actual repo, not the chat or a stub."""
    _t11()
    answer = sn.retrieve("scored dispatch reserve rule when two priorities are close")
    found = answer["retrieved"]
    assert answer["source"] == "repository_projection_index"
    assert answer["original_conversation_supplied"] is False
    assert found["smart_note_id"] == SN_ID, found
    assert found["intelligent_block_id"] == IB_ID
    assert found["truth_state"] == "CANDIDATE", "Retrieval must not imply promotion"
    assert "0.5" in answer["explanation"]
    assert (sn.ROOT / found["projection_path"]).is_file()


def test_unrelated_domain_never_selects_t11():
    """A website accessibility question is not scored dispatch with reserve."""
    _t11()
    try:
        answer = sn.retrieve("keyboard accessibility colors responsive typography")
    except SystemExit as error:
        assert str(error) == "NO_RELEVANT_INTELLIGENCE"
    else:
        assert answer["retrieved"]["smart_note_id"] != SN_ID, answer


def test_selector_does_not_change_or_promote_registry_bytes():
    _t11()
    before = hashlib.sha256(Path(sn.REGISTRY).read_bytes()).hexdigest()
    sn.retrieve("scored dispatch reserve rule")
    after = hashlib.sha256(Path(sn.REGISTRY).read_bytes()).hexdigest()
    assert before == after
    assert _t11()["truth_state"] == "CANDIDATE"
