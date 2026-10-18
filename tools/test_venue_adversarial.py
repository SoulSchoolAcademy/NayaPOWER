#!/usr/bin/env python3
"""Adversarial test for the VENUE_PATTERN gapclose (ACT w405, Naya Gamma).

PART A proves the edge against the tool's OWN extractor bytes at the live
tip (commit 8cac435a052d21ed74f8f2c2b8fec0bdaff455c7, PR #2744 merged):
  - prose-order miss: "The live board is #2721." -> None (false hold)
  - stale-number hijack: "Board #2641 was the live board until succession." -> '2641'
    (the extractor returns the ARCHIVED board as the live board)
PART B verifies the fixed extractor (sibling file succession_read_before_fire.py):
canonical link shape only; prose mentions of stale boards must never match.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

live = load("gate_live_tip", "/tmp/extractor-live-tip.py")          # tip bytes, 8cac435a
fixed = load("gate_fixed", os.path.join(HERE, "succession_read_before_fire.py"))

CASES = {
    "canonical-link": "[#2721 \u2014 Team coordination feed \u2014 live board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721)",
    "real-1599-line": "**Live coordination board:** [#2721 \u2014 Team coordination feed \u2014 live board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721) (successor to #2641 \u2014 ARCHIVED 2026-10-17)",
    "link-prose-order": "[live board is #2721](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721)",
    "stale-prose": "Board #2641 was the live board until the 2,300-comment succession.",
    "stale-before-words": "#2641 (the old live board) is archived; read-only.",
    "bare-prose-order": "The live board is #2721 as of 2026-10-17 ~06:47Z.",
}

# PART A: prove the edge against the live-tip extractor's own behavior.
a1 = live.extract_live_board(CASES["bare-prose-order"])
a2 = live.extract_live_board(CASES["stale-prose"])
assert a1 is None, f"expected prose-order miss, got {a1!r}"
assert a2 == "2641", f"expected stale hijack '2641', got {a2!r}"
print("PART A (edge proven against live-tip extractor):")
print(f"  prose-order miss: {CASES['bare-prose-order']!r} -> {a1!r}")
print(f"  stale hijack:     {CASES['stale-prose']!r} -> {a2!r}")

# PART B: the fix — canonical link shape only.
expect = {
    "canonical-link": "2721",
    "real-1599-line": "2721",
    "link-prose-order": "2721",
    "stale-prose": None,
    "stale-before-words": None,
    "bare-prose-order": None,   # fail-closed: venue must be the canonical machine-written line
}
fails = []
for name, want in expect.items():
    got = fixed.extract_live_board(CASES[name])
    ok = got == want
    print(f"PART B [{'PASS' if ok else 'FAIL'}] {name}: got {got!r}, want {want!r}")
    if not ok:
        fails.append(name)
if fails:
    print("FAILED:", fails); sys.exit(1)
print("PART B: all 6 adversarial cases pass on the fixed extractor.")
