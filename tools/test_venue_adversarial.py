#!/usr/bin/env python3
"""Adversarial test for the VENUE_PATTERN gapclose (ACT w405, Naya Gamma).

PART A proves the edge against the tool's OWN extractor bytes at the live
tip (commit 8cac435a052d21ed74f8f2c2b8fec0bdaff455c7, PR #2744 merged),
vendored hermetically as tools/fixtures/extractor-live-tip-8cac435a.py
(sha256 d1243e376e35d730b229a40537c76291e4ef766db89c9b4ea31b49988b487555,
git object 406370fe6e27ef76972c41d1cfe85eb962c212d3 — the exact tip tree
bytes; no /tmp path, no network, no tip-decay):
  - prose-order miss: "The live board is #2721." -> None (false hold)
  - stale-number hijack: "Board #2641 was the live board until succession." -> '2641'
    (the extractor returns the ARCHIVED board as the live board)
PART B verifies the fixed extractor (sibling file succession_read_before_fire.py):
canonical link shape only; prose mentions of stale boards must never match.

Hermetic: both extractor modules load from repo-relative paths. A clean
checkout with no /tmp/extractor-live-tip.py collects and passes (the
2026-10-18 red CI on PR #2756 was FileNotFoundError on that /tmp path).
"""
import importlib.util
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


live = load("gate_live_tip",                                        # tip bytes, 8cac435a
            os.path.join(HERE, "fixtures", "extractor-live-tip-8cac435a.py"))
fixed = load("gate_fixed", os.path.join(HERE, "succession_read_before_fire.py"))

CASES = {
    "canonical-link": "[#2721 \u2014 Team coordination feed \u2014 live board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721)",
    "real-1599-line": "**Live coordination board:** [#2721 \u2014 Team coordination feed \u2014 live board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721) (successor to #2641 \u2014 ARCHIVED 2026-10-17)",
    "link-prose-order": "[live board is #2721](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721)",
    "stale-prose": "Board #2641 was the live board until the 2,300-comment succession.",
    "stale-before-words": "#2641 (the old live board) is archived; read-only.",
    "bare-prose-order": "The live board is #2721 as of 2026-10-17 ~06:47Z.",
}


def test_part_a_prose_order_miss_against_pinned_tip():
    got = live.extract_live_board(CASES["bare-prose-order"])
    assert got is None, f"expected prose-order miss, got {got!r}"


def test_part_a_stale_hijack_against_pinned_tip():
    got = live.extract_live_board(CASES["stale-prose"])
    assert got == "2641", f"expected stale hijack '2641', got {got!r}"


@pytest.mark.parametrize("name,want", [
    ("canonical-link", "2721"),
    ("real-1599-line", "2721"),
    ("link-prose-order", "2721"),
    ("stale-prose", None),
    ("stale-before-words", None),
    ("bare-prose-order", None),   # fail-closed: venue must be the canonical machine-written line
])
def test_part_b_fixed_extractor(name, want):
    got = fixed.extract_live_board(CASES[name])
    assert got == want, f"{name}: got {got!r}, want {want!r}"
