"""Tests for tools/operating_state.py — emitter, validator, cold proof.

Negative controls (required):
  * a malformed state file FAILS schema validation, and every failure is a
    cure line (MISSING: ... — CURE: ... (owner: ...)), never a bare error;
  * the publisher REFUSES a state whose tip does not match the live ref —
    a stale state can never ride the publish.
Plus the derivation rules from the ratified drain order, and a cold-proof
fixture proving the five activation answers come from the artifacts alone.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import operating_state as os_mod  # noqa: E402

STATE_SCHEMA = json.loads((Path(__file__).parent / "operating_state.schema.json").read_text())
QUEUE_SCHEMA = json.loads((Path(__file__).parent / "queue_contract.schema.json").read_text())

GAUGE_OK = {"source": "files/balanced-machine/GAUGE-READ-2026-10-21.md",
            "read_anchor": "2026-10-21 22:41:48Z", "paperwork_block_rate_pct": 51.5,
            "time_to_merge_median_hours": {"A": 11.3, "B": 5.9, "C": 15.3},
            "escape_rate_proxy_pct": 3.9, "feed_freshness": "outside band"}
LAWS_OK = {"source": "~/AGENTS.md", "iteration": 205, "latest_laws": ["L608", "L609"]}


def row(number, tier="B", action="MERGE-NOW"):
    return {"number": number, "title": f"PR {number}", "tier": tier, "action": action,
            "cure": "dock merges", "owner": "dock", "head": "a" * 40}


def test_valid_artifacts_pass():
    queue = [row(1), row(1130, tier="C", action="HOLD-HUMAN")]
    state = os_mod.build_state("b" * 40, "2026-10-21T23:00:00Z", queue, ["test"], GAUGE_OK, LAWS_OK)
    contract = os_mod.build_queue_contract("b" * 40, "2026-10-21T23:00:00Z", queue)
    assert os_mod.validate(state, STATE_SCHEMA) == []
    assert os_mod.validate(contract, QUEUE_SCHEMA) == []
    assert state["hold_human"] == [1130]
    assert state["queue_by_tier_action"] == {"B": {"MERGE-NOW": 1}, "C": {"HOLD-HUMAN": 1}}


def test_malformed_state_fails_with_cure_lines():
    bad = {"schema": "naya.operating-state/1", "tip": 42}  # wrong type + missing fields
    errors = os_mod.validate(bad, STATE_SCHEMA)
    assert errors, "a malformed state must fail validation"
    assert all(e.startswith("MISSING:") and "— CURE:" in e and "(owner:" in e for e in errors)


def test_bad_action_enum_fails():
    contract = os_mod.build_queue_contract("b" * 40, "t", [row(1, action="WHATEVER")])
    errors = os_mod.validate(contract, QUEUE_SCHEMA)
    assert any("enum" in e or "one of" in e for e in errors)


def test_publish_refuses_stale_tip(tmp_path):
    queue = [row(1)]
    state = os_mod.build_state("b" * 40, "t", queue, [], GAUGE_OK, LAWS_OK)
    contract = os_mod.build_queue_contract("b" * 40, "t", queue)
    with pytest.raises(SystemExit) as exc:
        os_mod.publish(state, contract, tmp_path, "c" * 40, STATE_SCHEMA, QUEUE_SCHEMA)
    assert "does not match the live ref" in str(exc.value)
    assert not (tmp_path / "OPERATING-STATE.json").exists()


def test_publish_writes_valid_pair(tmp_path):
    queue = [row(1)]
    state = os_mod.build_state("b" * 40, "t", queue, [], GAUGE_OK, LAWS_OK)
    contract = os_mod.build_queue_contract("b" * 40, "t", queue)
    paths = os_mod.publish(state, contract, tmp_path, "b" * 40, STATE_SCHEMA, QUEUE_SCHEMA)
    assert len(paths) == 2 and all(p.exists() for p in paths)


def test_hold_human_wins_over_green_checks():
    d = os_mod.derive_action(1130, "C", "clean", [], [])
    assert d["action"] == "HOLD-HUMAN" and d["owner"] == "Shawn"


def test_dirty_branch_is_a_cure_not_a_merge():
    d = os_mod.derive_action(999, "B", "dirty", [], [])
    assert d["action"] == "CURE" and "rebases" in d["cure"]


def test_content_red_blocks_merge_now():
    d = os_mod.derive_action(999, "B", "blocked", ["completeness"], ["test"])
    assert d["action"] == "CURE" and "completeness" in d["cure"]


def test_inherited_base_red_is_not_charged_as_content():
    # `test` red at the head AND already red at the merge-base: the cure is
    # a branch update, not an author content fix (the keystone pattern).
    d = os_mod.derive_action(999, "B", "blocked", ["test"], ["test"])
    assert d["action"] == "CURE" and "inherited from its merge-base" in d["cure"]


def test_red_absent_at_base_is_charged_to_the_pr():
    d = os_mod.derive_action(999, "B", "blocked", ["test"], [])
    assert d["action"] == "CURE" and "PR-caused" in d["cure"]


def test_tier_c_paperwork_only_is_merge_now():
    d = os_mod.derive_action(999, "C", "blocked", ["Team review + scorecard receipt"], [])
    assert d["action"] == "MERGE-NOW"


def test_tier_b_paperwork_only_cure_names_the_floor():
    d = os_mod.derive_action(999, "B", "blocked", ["Receipt gate (evidence or it didn't happen)"], [])
    assert d["action"] == "CURE" and "8.0" in d["cure"]


def test_cold_proof_answers_from_artifacts_only(tmp_path):
    queue = [row(7), row(1130, tier="C", action="HOLD-HUMAN")]
    state = os_mod.build_state("b" * 40, "2026-10-21T23:00:00Z", queue, [], GAUGE_OK, LAWS_OK)
    contract = os_mod.build_queue_contract("b" * 40, "2026-10-21T23:00:00Z", queue)
    sp, qp = tmp_path / "OPERATING-STATE.json", tmp_path / "QUEUE-CONTRACT.json"
    sp.write_text(json.dumps(state))
    qp.write_text(json.dumps(contract))
    out = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "operating_state.py"),
         "cold", "--state", str(sp), "--queue", str(qp)],
        capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "1. Tip: " + "b" * 40 in out.stdout
    assert "MERGE-NOW): [7]" in out.stdout
    assert "HOLD-HUMAN): [1130]" in out.stdout
    assert "tip is green" in out.stdout
    assert "51.5%" in out.stdout
