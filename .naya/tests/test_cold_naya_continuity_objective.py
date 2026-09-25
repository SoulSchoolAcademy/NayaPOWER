"""Cold-Naya continuity objective guard.

This is a behavioral contract test for the boot path. It deliberately keeps the
future product front door separate from the current Superbrain rehabilitation
frontier.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

BOOTSTRAP = ROOT / ".naya/memory/BOOTSTRAP.md"
BRAIN_MAP = ROOT / ".naya/memory/NAYAPOWER-BRAIN-MAP.md"
CONTINUATION = ROOT / ".naya/operations/NAYA-CONTINUATION-PROMPT-2026-09-25.md"
CURRENT = ROOT / ".naya/projects/CURRENT-PROJECT.md"
START = ROOT / "SUPERBRAIN/AI-BOOT/START-HERE.md"
STATE = ROOT / ".naya/control-plane/STATE.json"
BLOCKS = ROOT / ".naya/control-plane/BLOCKS.json"
PROOF = ROOT / ".naya/control-plane/PROOF.json"


def read(path):
    return path.read_text(encoding="utf-8")


def test_cold_naya_boot_path_names_superbrain_continuity_as_current_frontier():
    continuation = read(CONTINUATION)
    current = read(CURRENT)
    start = read(START)

    assert "Superbrain" in continuation
    assert "cold-Naya" in continuation
    assert "continuity" in continuation.lower()

    # The current frontier is the intelligence substrate, not the future front door.
    assert "No NINA login" in continuation
    assert "Welcome" in continuation
    assert "future front door" in current
    assert "Superbrain" in current

    # The bootloader must tell a cold Naya to build the brain before the door.
    assert "Build the brain before the door" in start


def test_cold_naya_boot_order_contains_the_authoritative_memory_chain():
    bootstrap = read(BOOTSTRAP)
    brain_map = read(BRAIN_MAP)

    for required in (
        ".naya/memory/NAYAPOWER-BRAIN-MAP.md",
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/MAP.json",
        ".naya/control-plane/PROOF.json",
        ".naya/control-plane/BATON.json",
        ".naya/memory/RETRIEVAL-MANIFEST.json",
        ".naya/memory/smart-notes/REGISTRY.json",
    ):
        assert required in bootstrap

    assert "RESTORE → FIND THE RIGHT AUTHORITY → READ THE MINIMUM REQUIRED SOURCE → RECONCILE LIVE EVIDENCE → ACT → VERIFY → PRESERVE LEARNING" in brain_map


def test_control_plane_agrees_on_the_same_superbrain_next_action():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    blocks = json.loads(BLOCKS.read_text(encoding="utf-8"))
    proof = json.loads(PROOF.read_text(encoding="utf-8"))

    actions = {
        state["single_next_action"],
        blocks["next_action"],
        proof["next_action"]["next_action"],
    }
    assert len(actions) == 1
    action = next(iter(actions))
    assert "Superbrain" in action
    assert "BOOTSTRAP" in action
    assert "RETRIEVAL-MANIFEST" in action
    assert "handoff/next-action" in action
    assert "NINA login" in action
    assert "Welcome/front-door" in action
