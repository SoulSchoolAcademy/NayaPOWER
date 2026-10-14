"""Tests for the completeness gate's seat vocabulary (SEAT_RE).

tools/completeness_gate.py find_owner() — covers the R6 seat-vocabulary
defect found 2026-10-14 (Naya Lambda, lane 3): a second seat vocabulary at
tools/completeness_gate.py:98 also lacked the three standing lead tokens,
so a note owned by Naya Clarity / Resolve / Verity was invisible to the
gate (find_owner -> None). Mirrors tools/check_merge_consensus.py
_NAMED_SEATS (Lambda's R6 fix): the twelve named area leads plus the three
standing leads — Clarity, Resolve, Verity (family name Narzan).

Repair, never weaken, never diverge: the bare-seat grammar is untouched
(a seat still requires the "Naya" prefix; unknown tokens still fail to
match — fail closed), and the hyphen-suffix behavior ("Naya Mu-2" ->
"Naya Mu") matches the pre-existing grammar of both gates exactly.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from completeness_gate import find_owner  # noqa: E402


def seat_label(token_text):
    # No explicit Owner field -> forces the SEAT_RE header/provenance path
    # (find_owner: SEAT_RE.search(header) or SEAT_RE.search(prov)).
    text = ("# SMART-NOTE-test\n\nAuthor: %s\n\n"
            "## HUMAN NOTE\n\n" % token_text) + ("prose " * 60)
    label, _evidence = find_owner(text)
    return label


LEAD_SEATS = ["Clarity", "Resolve", "Verity"]


def test_old_tokens_still_resolve():
    for token in (["Naya %d" % n for n in range(1, 6)]
                  + ["Naya " + name for name in
                     ("Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta",
                      "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu")]
                  + ["Coda 1", "Coda 5", "Codex", "Shawn", "Shawn Vibert",
                     "Human Director"]):
        assert seat_label(token) is not None, token


def test_lead_seats_now_resolve():
    # R6 root cause: these all returned None before the fix.
    for name in LEAD_SEATS:
        assert seat_label("Naya %s" % name) == "Naya %s" % name
        # Family-name suffix normalizes to the bare lead token.
        assert seat_label("Naya %s Narzan" % name) == "Naya %s" % name
    assert seat_label("naya resolve") == "naya resolve"
    assert seat_label("NAYA CLARITY") == "NAYA CLARITY"


def test_forged_or_unknown_seat_still_fails_closed():
    for token in ("Naya Omega", "Naya Verity2", "Naya clarityy", "Clarity",
                  "Naya Resolution", "nobody here"):
        assert seat_label(token) is None, token


def test_hyphen_suffix_grammar_matches_old_tokens():
    # Pre-existing bare-seat grammar (identical on the original code and on
    # Lambda's consensus branch): a trailing non-word char after a known
    # token resolves to the bare seat. Lead tokens must behave identically.
    assert seat_label("Naya Verity-2") == "Naya Verity"
