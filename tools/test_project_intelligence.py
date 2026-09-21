#!/usr/bin/env python3
"""Acceptance tests for rebuildable Project Intelligence Context v1."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "project_intelligence.py"


def load_module():
    spec = importlib.util.spec_from_file_location("project_intelligence", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        control = root / "control-plane"
        events = root / "events"
        learning = root / "learning"
        pis = root / "pis"
        control.mkdir()
        events.mkdir()
        learning.mkdir()
        pis.mkdir()

        module.ROOT = root
        module.CONTROL = control
        module.PROJECT_PATH = root / "CURRENT-PROJECT.md"
        module.ONE_SHOT = root / "NAYAPOWER-ONE-SHOT.md"
        module.MACHINE_CONTRACT = root / "machine.json"
        module.SYSTEM_MAP = root / "system.mmd"
        module.START_HERE = root / "START-HERE.md"
        module.EVENT_DIR = events
        module.PIS_DIR = pis
        module.LEARNING_DIR = learning

        state = {
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "mission": "Make extraordinary things easier for ordinary humans.",
            "north_star": "Maximum verified human value per unit of effort.",
            "priority": "P0",
            "status": "LIVE_BOUND",
            "current_head": {"source": "git:HEAD", "recorded_head_is_not_authoritative": True},
            "current_block": "TEST-BLOCK",
            "current_block_status": "ACTIVE",
            "single_next_action": "Execute one verified frontier.",
            "bottleneck": "TEST_TARGET",
            "unknown": ["One thing remains unverified."],
            "protected_boundaries": ["Never weaken fail-closed behavior."],
            "verified_evidence": {"known": ["Canonical event identity is verified."]},
        }
        (control / "STATE.json").write_text(json.dumps(state), encoding="utf-8")
        (control / "MAP.json").write_text(json.dumps({
            "mission": state["mission"],
            "north_star": state["north_star"],
            "truth_owners": {"source": "GitHub"},
            "protected": ["One source of truth"],
            "execution_map": {"definition_of_done": "TEST_TARGET"},
        }), encoding="utf-8")
        (control / "BLOCKS.json").write_text(json.dumps({
            "active_block": {
                "id": "TEST-BLOCK",
                "status": "ACTIVE",
                "next_action": "Execute one verified frontier.",
                "target_state": "TEST_TARGET",
            }
        }), encoding="utf-8")
        (control / "PROOF.json").write_text(json.dumps({
            "current_evidence": {"test": {"status": "VERIFIED"}}
        }), encoding="utf-8")

        (root / "CURRENT-PROJECT.md").write_text(
            "# NayaPOWER — CURRENT PROJECT\n\n## MISSION\n"
            "Make extraordinary things easier for ordinary humans.\n\n"
            "## CURRENT STATE\n- canonical substrate exists\n",
            encoding="utf-8",
        )
        (root / "NAYAPOWER-ONE-SHOT.md").write_text("# One Shot\n", encoding="utf-8")
        (root / "machine.json").write_text(json.dumps({
            "engine": ["CAPTURE", "LEARN", "VERIFY"],
            "human_surface": ["SEE", "ACT"],
        }), encoding="utf-8")
        (root / "system.mmd").write_text("flowchart TD\n", encoding="utf-8")
        (root / "START-HERE.md").write_text("# Start\n", encoding="utf-8")

        event = {
            "event_id": "SE-20260920-200000-project-context",
            "project_id": "NayaPOWER",
            "lesson": "Verified project intelligence must remain reconstructable.",
            "evidence_state": "VERIFIED",
            "actual_outcome": "Projection reconstructed.",
            "next_action": "Continue the next responsible frontier.",
        }
        (events / "event.json").write_text(json.dumps(event), encoding="utf-8")
        (learning / "LRN-test.json").write_text(json.dumps({
            "learning_event_id": "LRN-test",
            "project": "NayaPOWER",
            "lesson": "Preserve evidence and uncertainty during distillation.",
            "evidence_state": "VERIFIED",
            "learning_state": "OPERATIONAL",
            "recommendation": "Keep provenance.",
        }), encoding="utf-8")
        (pis / "SN-test.json").write_text("{}", encoding="utf-8")

        result = module.build_project_intelligence()

        assert result["schema"] == "naya/project-intelligence-context/v1"
        assert result["status"] == "REBUILDABLE_DERIVED_PROJECTION"
        assert result["mission"] == state["mission"]
        assert result["vision"]
        assert result["purpose"]
        assert result["goals"]
        assert result["requirements"]
        assert result["constraints"]
        assert result["constitution"]["core_laws"]
        assert result["architecture"]["model"]
        assert result["authority"]["human"]
        assert result["canonical_sources"]["control_plane"]
        assert result["current_state"]["active_block"] == "TEST-BLOCK"
        assert any(item.get("event_id") == event["event_id"] for item in result["verified"])
        assert result["learning"]["recent_project_learning"][0]["learning_event_id"] == "LRN-test"
        assert result["unknown"] == []
        assert result["open_loops"]
        assert result["definition_of_done"] == "TEST_TARGET"
        assert result["next_action"] == "Execute one verified frontier."
        assert result["team_handoff"]["assignment"] == "Execute one verified frontier."
        assert result["cold_restore_answers"]["WHAT"] == "NayaPOWER — CURRENT PROJECT"
        assert result["source_lineage"]["event_count"] == 1
        assert result["source_lineage"]["pis_note_count"] == 1

    print("PASS — Project Intelligence Context v1")
    print("PROJECT_INTELLIGENCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
