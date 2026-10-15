"""Tests for the Brain Index Regen Habit gate
(tools/protocol/checks/brain_index_freshness.py, law BRAIN-INDEX-FRESHNESS).

The gate is fail-closed: anything it cannot verify fails, and it never
silently checks the wrong tree. These tests hit the actual seam — the
check module delegating to the real regeneration machinery — with the
machinery stubbed only where the test is about the gate's own behavior
(drift mapping, fail-closed records), never where the test is about
freshness itself.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK_PATH = ROOT / "tools" / "protocol" / "checks" / "brain_index_freshness.py"
MANIFEST_PATH = ROOT / "kernel" / "protocol" / "protocol_manifest.json"


def load_gate():
    spec = importlib.util.spec_from_file_location(
        "brain_index_freshness", CHECK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def gate():
    return load_gate()


# ---- the happy path: the real tree is fresh ----

def test_passes_on_fresh_tree(gate):
    """The live checkout's index layer matches the committed tree, so the
    gate passes against the real machinery. (CI enforces the same
    condition, so this cannot rot into a tautology: if the tree drifts,
    the gate and CI fail together.)"""
    res = gate.check({"repo_root": str(ROOT)})
    assert res["pass"] is True, res["reasons"]
    assert res["details"]["law"] == "BRAIN-INDEX-FRESHNESS"
    assert res["details"]["drift_items"] == []


def test_default_repo_root_resolves_to_this_checkout(gate):
    res = gate.check({})
    assert res["pass"] is True, res["reasons"]
    assert Path(res["details"]["repo_root"]) == ROOT


# ---- drift and corruption map to the right failures ----

def test_drift_fails_and_names_the_fix(gate, monkeypatch):
    monkeypatch.setattr(
        gate, "_run_regen_check",
        lambda root: (1, "DRIFT:\n - BRAIN/REAL-TREE.json does not match "
                         "regenerated output"),
    )
    res = gate.check({"repo_root": str(ROOT)})
    assert res["pass"] is False
    blob = " ".join(res["reasons"])
    assert "DRIFT" in blob
    assert "BRAIN/REAL-TREE.json" in blob
    assert "python3 tools/regenerate_brain_index.py" in blob
    assert res["details"]["drift_items"] == [
        "BRAIN/REAL-TREE.json does not match regenerated output"]


def test_floor_violation_routes_to_structural_not_regen_advice(gate, monkeypatch):
    """A deletion (floor violation) must NOT be answered with 'just
    regenerate' — the regen machinery refuses to bless deletions, so the
    gate must say restore-or-deliberately-lower-the-floor instead."""
    monkeypatch.setattr(
        gate, "_run_regen_check",
        lambda root: (1, "DRIFT:\n - domain counts below baseline floor: "
                         "04-INTELLIGENCE: 20 files in tree, floor is 24 "
                         "(4 file(s) removed without a deliberate floor update)"),
    )
    res = gate.check({"repo_root": str(ROOT)})
    assert res["pass"] is False
    blob = " ".join(res["reasons"])
    assert "STRUCTURAL" in blob
    assert "Do NOT regenerate" in blob
    assert "python3 tools/regenerate_brain_index.py" not in blob


def test_structural_corruption_fails_as_corruption_not_drift(gate, monkeypatch):
    monkeypatch.setattr(
        gate, "_run_regen_check",
        lambda root: (2, "error: BRAIN/ files were REMOVED below the "
                         "baseline floor:\n  04-INTELLIGENCE: 20 files in "
                         "tree, floor is 24"),
    )
    res = gate.check({"repo_root": str(ROOT)})
    assert res["pass"] is False
    blob = " ".join(res["reasons"])
    assert "STRUCTURAL" in blob
    # The fix for corruption is restoration, NOT regeneration.
    assert "restore" in blob.lower() or "Do NOT regenerate" in blob


def test_broken_machinery_fails_closed(gate, monkeypatch):
    def boom(root):
        raise RuntimeError("git exploded")
    monkeypatch.setattr(gate, "_run_regen_check", boom)
    res = gate.check({"repo_root": str(ROOT)})
    assert res["pass"] is False
    assert "fails closed" in " ".join(res["reasons"])


# ---- fail-closed on bad records and wrong trees ----

def test_non_dict_record_fails_closed(gate):
    res = gate.check("not-a-record")
    assert res["pass"] is False
    assert "fail closed" in " ".join(res["reasons"]).lower()


def test_non_repo_root_fails_closed(gate, tmp_path):
    res = gate.check({"repo_root": str(tmp_path)})
    assert res["pass"] is False
    blob = " ".join(res["reasons"])
    assert "BRAIN/" in blob or "checkout" in blob


def test_directory_without_git_fails_closed(gate, tmp_path):
    (tmp_path / "BRAIN").mkdir()
    res = gate.check({"repo_root": str(tmp_path)})
    assert res["pass"] is False
    assert ".git" in " ".join(res["reasons"])


def test_empty_repo_root_string_fails_closed(gate):
    res = gate.check({"repo_root": "   "})
    assert res["pass"] is False


# ---- CLI shape (the pattern every protocol check follows) ----

def test_cli_json_pass_shape():
    proc = subprocess.run(
        [sys.executable, str(CHECK_PATH),
         "--record", json.dumps({"repo_root": str(ROOT)}), "--json"],
        capture_output=True, text=True, timeout=120, cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["pass"] is True
    assert isinstance(data["reasons"], list) and data["reasons"]
    assert data["details"]["law"] == "BRAIN-INDEX-FRESHNESS"


def test_cli_fails_on_drift_exit_code(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(CHECK_PATH),
         "--record", json.dumps({"repo_root": str(tmp_path)})],
        capture_output=True, text=True, timeout=60, cwd=ROOT,
    )
    assert proc.returncode == 1
    assert "FAIL" in proc.stdout


# ---- freshness covers the index layer, not its payload schemas ----

# OWNER-FIELD-SPEC-V1 §5: the regen tool is the canonical emitter of
# owner/owner_basis on REAL-TREE entries (schema naya.brain.real_tree.v2).
# This test pins the emission on the working file: a regen that drops owner
# must fail loudly here even before --check drift is consulted.

def test_real_tree_entries_carry_owner_v2():
    """Every REAL-TREE entry carries owner + owner_basis; the corpus schema
    is v2. 1261 entries were 100% ownerless at w186 — this test is the
    regression tripwire."""
    rt = json.loads((ROOT / "BRAIN" / "REAL-TREE.json").read_text())
    assert rt["schema"] == "naya.brain.real_tree.v2", (
        f"expected v2 schema, got {rt.get('schema')}"
    )
    missing = [e["path"] for e in rt["files"]
               if not e.get("owner") or not e.get("owner_basis")]
    assert missing == [], f"{len(missing)} entries without owner: {missing[:10]}"


def test_real_tree_owner_derivation_matches_backfill():
    """The regen's owner emission must agree byte-for-byte with what
    tools/owner_backfill.py --corpus c expects: one shared derivation rule,
    never two. A disagreement here means the two rules drifted apart and
    the backfill would flag the regen output as drift."""
    from owner_backfill import derive_real_tree  # noqa: E402
    rt = json.loads((ROOT / "BRAIN" / "REAL-TREE.json").read_text())
    mismatches = []
    for e in rt["files"]:
        want_owner, want_basis = derive_real_tree(e)
        if e.get("owner") != want_owner or e.get("owner_basis") != want_basis:
            mismatches.append(e["path"])
        if len(mismatches) >= 10:
            break
    assert mismatches == [], f"regen/backfill owner disagreement: {mismatches}"


# ---- the law is registered in the manifest ----

def test_manifest_registers_the_law():
    manifest = json.loads(MANIFEST_PATH.read_text())
    laws = {law["id"]: law for law in manifest["laws"]}
    assert "BRAIN-INDEX-FRESHNESS" in laws, "law missing from manifest"
    law = laws["BRAIN-INDEX-FRESHNESS"]
    assert law["check"] == "tools/protocol/checks/brain_index_freshness.py"
    assert Path(ROOT / law["check"]).exists(), "manifest check path is dead"
    assert "enforcement" in law and law["enforcement"]
