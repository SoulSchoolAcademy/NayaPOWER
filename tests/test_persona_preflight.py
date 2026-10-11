"""Tests for tools/persona_preflight.py -- the SELF node preflight binding.

Positive control: against the live repo tree the preflight exits 0 with a
valid PASS receipt.

Negative controls:
  - canonical source missing -> exit 2 (HALT, the contract's failure state).
  - canonical pins mutated (name='Maya') -> exit 1 (FAIL).
  - tone pin mutated -> exit 1 (FAIL).

The subprocess path is used deliberately: the preflight is an operational
artifact, and these tests prove its real CLI behavior, not a library call.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = REPO_ROOT / "tools" / "persona_preflight.py"
CANONICAL = REPO_ROOT / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json"


def run_preflight(canonical: Path | None) -> "subprocess.CompletedProcess[str]":
    env = dict(os.environ)
    cmd = [sys.executable, str(PREFLIGHT)]
    if canonical is None:
        env.pop("PERSONA_PREFLIGHT_CANONICAL", None)
    else:
        env["PERSONA_PREFLIGHT_CANONICAL"] = str(canonical)
    return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)


def test_preflight_passes_on_live_tree():
    proc = run_preflight(None)
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
    receipt = json.loads(proc.stdout)
    assert receipt["check"] == "persona_preflight"
    assert receipt["result"] == "PASS"
    assert receipt["name"] == "Naya"
    assert receipt["tone"] == [
        "warm",
        "direct",
        "enthusiastic",
        "truthful",
        "practical",
        "clear",
    ]
    # The preflight never claims RATIFIED; only Shawn ratifies.
    assert receipt["canonical_status"] in ("CANDIDATE", "RATIFIED")
    assert receipt["ratified_claim"] is False
    # Seat stays a designation, never absorbed into identity.
    assert "naya-4" in receipt["presentation_sample"]
    assert "not my identity" in receipt["presentation_sample"]


def test_preflight_honest_receipt_fields():
    proc = run_preflight(None)
    assert proc.returncode == 0
    receipt = json.loads(proc.stdout)
    assert receipt["repo_sha"] and len(receipt["repo_sha"]) >= 7
    assert receipt["canonical"].endswith("NAYA-PERSONA-V1.json")
    assert "ts" in receipt


@pytest.fixture()
def mutated_object(tmp_path: Path) -> Path:
    obj = json.loads(CANONICAL.read_text(encoding="utf-8"))
    target = tmp_path / "NAYA-PERSONA-V1.json"
    target.write_text(json.dumps(obj), encoding="utf-8")
    return target


def test_preflight_halts_when_canonical_missing(tmp_path: Path):
    proc = run_preflight(tmp_path / "does-not-exist.json")
    assert proc.returncode == 2, f"expected HALT(2), got {proc.returncode}: {proc.stderr}"
    assert "HALT" in proc.stderr
    assert "never improvise" in proc.stderr


def test_preflight_fails_when_name_pin_moves(mutated_object: Path):
    obj = json.loads(mutated_object.read_text(encoding="utf-8"))
    obj["ai_view"]["name"] = "Maya"
    mutated_object.write_text(json.dumps(obj), encoding="utf-8")
    proc = run_preflight(mutated_object)
    assert proc.returncode == 1, f"expected FAIL(1), got {proc.returncode}"
    assert "name pin moved" in proc.stderr


def test_preflight_fails_when_tone_pin_moves(mutated_object: Path):
    obj = json.loads(mutated_object.read_text(encoding="utf-8"))
    obj["ai_view"]["tone"] = ["bubbly", "casual"]
    mutated_object.write_text(json.dumps(obj), encoding="utf-8")
    proc = run_preflight(mutated_object)
    assert proc.returncode == 1, f"expected FAIL(1), got {proc.returncode}"
    assert "tone pin moved" in proc.stderr


def test_preflight_fails_when_source_unreadable(tmp_path: Path):
    bad = tmp_path / "NAYA-PERSONA-V1.json"
    bad.write_text("{not valid json", encoding="utf-8")
    proc = run_preflight(bad)
    # Unreadable canonical source is the halt state, not a soft fail.
    assert proc.returncode == 2, f"expected HALT(2), got {proc.returncode}"
    assert "HALT" in proc.stderr


def test_preflight_cli_flag_overrides_env(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PERSONA_PREFLIGHT_CANONICAL", str(tmp_path / "missing.json"))
    proc = subprocess.run(
        [sys.executable, str(PREFLIGHT), "--canonical", str(CANONICAL)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
