"""Tests for the live-corpus note bridge (tools/note_bridge_live.py).

These tests run against the REAL corpus at BRAIN/05-MEMORY/SMART-NOTES/.
They assert structural properties (parsing, retrieval, gating) rather than
exact corpus size, so new notes don't break them.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from note_bridge_live import (
    load_live_corpus,
    parse_note_file,
    gate_action_live,
    CURATED_CONSTRAINTS,
)


def test_corpus_loads():
    notes, report = load_live_corpus()
    assert report["total_files"] >= 40, f"expected 40+ note files, got {report['total_files']}"
    assert report["parsed"] == report["total_files"], f"parse failures: {report['failed_paths']}"
    assert report["failed"] == 0


def test_every_note_has_id_and_nutshell():
    notes, _ = load_live_corpus()
    for n in notes:
        assert n.id and n.id != "SN-UNKNOWN", f"note missing id: {n.title}"
        assert n.nutshell, f"note {n.id} missing nutshell"
        assert n.keywords, f"note {n.id} has no keywords"


def test_curated_constraints_exist_on_disk():
    notes, report = load_live_corpus()
    ids = {n.id for n in notes}
    for sn_id in CURATED_CONSTRAINTS:
        assert sn_id in ids, f"curated constraint {sn_id} has no note on disk (phantom)"


def test_sn003_blocks_parallel_brain():
    decision, _ = gate_action_live("Create a new separate brain store for this project")
    assert decision.verdict == "BLOCK"
    assert any(v["note_id"] == "SN-003" for v in decision.violations)


def test_sn0408_blocks_deletion():
    decision, _ = gate_action_live("Delete the old branch to clean up")
    assert decision.verdict == "BLOCK"
    assert any(v["note_id"] == "SN-0408" for v in decision.violations)


def test_sn0460_blocks_ratified_jump():
    decision, _ = gate_action_live("Promote this candidate to ratified status now")
    assert decision.verdict == "BLOCK"
    assert any(v["note_id"] == "SN-0460" for v in decision.violations)


def test_benign_action_allows():
    decision, _ = gate_action_live("Write a summary of today's weather")
    assert decision.verdict == "ALLOW"
    assert decision.violations == []


def test_phantom_notes_absent():
    # SN-0518/SN-0521 were cited by the prototype before they existed on disk
    # (the original phantom case). Both have since been genuinely captured with
    # #1354 provenance, so they are no longer phantoms. The guard's intent stands:
    # a phantom is a cited-but-nonexistent note, so every cited id here must
    # resolve to a genuine, fully-structured note in the live corpus.
    notes, _ = load_live_corpus()
    by_id = {n.id: n for n in notes}
    for sn_id in ("SN-0518", "SN-0521"):
        assert sn_id in by_id, f"{sn_id} cited but missing from corpus (phantom)"
        n = by_id[sn_id]
        assert n.title and n.nutshell and n.keywords, f"{sn_id} is not a genuine note"


def test_retrieval_uses_live_notes():
    # Retrieval must surface real disk notes, not the prototype's hardcoded four.
    decision, _ = gate_action_live("Create a new separate brain store for this project")
    assert "SN-003" in decision.notes_retrieved
    assert len(decision.notes_retrieved) >= 3
