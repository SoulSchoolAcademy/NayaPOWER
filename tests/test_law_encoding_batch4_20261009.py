"""Tests for the 2026-10-09 law-encoding BATCH 4.

Every law encoded this batch gets the same proof contract:
  - a VIOLATING fixture makes the check FAIL (the encoding fires), and
  - an HONORING fixture makes the check PASS (the encoding stays quiet).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch4_20261009.py
Also pytest-compatible (plain assert functions).

Covers:
  - two_layer.py          (Two-Layer Law + LITERAL-FIRST refinement, slot 10)
  - base_lineage.py       (Base-Lineage Rule, slot 13)
  - falsification_first.py (Falsification-First Verification Standard, slot 14)

Decision receipt (why these three):
  - LITERAL-FIRST: verified unencoded — neither main's two_layer.py nor the
    batch-2-hardened re-validator screens the literal layer for machine
    exhaust. Encoded as a module UPGRADE of two_layer.py (not a new slot):
    the literal layer already has an owner, and a second owner would be the
    maintenance fork INVENTORY FIRST warns about.
  - BASE-LINEAGE: verified unencoded on main and on every hardened branch.
  - FALSIFICATION-FIRST: verified unencoded on main and on every hardened
    branch.
  - Considered and deferred: SN-0732 (identity/ethics; only its capture
    clause is machine-testable and that overlaps slot-9 SN-PROACTIVE-DOC),
    decision-receipt / wisest-choice / merge-authority (already encoded on
    the in-flight batch-3 branches — re-encoding would fork the lane).
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import (  # noqa: E402
    base_lineage,
    falsification_first,
    two_layer,
)


# ---------------------------------------------------------------- fixtures
def _base_two_layer_report():
    return {
        "report_type": "deliverable_report",
        "title": "Batch 4 encoded",
        "technical": (
            "Extended tools/protocol/checks/two_layer.py with the literal-first "
            "purity screen: SHA-like hex, #NNNN refs, test-count patterns, and "
            "CI-state markers in the literal layer now fail the check. Added "
            "tools/protocol/checks/base_lineage.py and falsification_first.py "
            "as manifest slots 13 and 14."
        ),
        "plain_human": (
            "Literally what I'm saying: the computer now refuses to send a "
            "report whose plain-words section is polluted with jargon like "
            "code fingerprints or build-system chatter. Think of it like a "
            "cleanliness rule for the part he actually reads — the plain "
            "part must sound like a person talking, not a log file."
        ),
        "audience": "shawn",
        "seat": "naya-5",
    }


def _base_falsification_report():
    return {
        "claim": "the new purity screen fires on SHA-like hex",
        "verifier": "naya-5",
        "builder_battery": [
            "clean literal layer passes",
            "technicals-only report fails",
        ],
        "verifier_attacks": [
            {
                "input": "a seven-character hex fingerprint buried mid-sentence",
                "outcome": "held",
            },
            {
                "input": "a pure-digit build number that must NOT trip the screen",
                "outcome": "held",
            },
        ],
        "verdict": "verified",
        "attacks_tried": True,
    }


# ---------------------------------------------------------------- two_layer: literal-first refinement
def test_literal_first_sha_in_plain_human_fails():
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the fix landed in commit 8c9a44ab and "
        "the report is now clean. Think of it like a letter home that "
        "arrived without any stamps missing — plain words, nothing else."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "machine exhaust" in out["reasons"][0] and "hex" in out["reasons"][0]


def test_literal_first_pr_ref_in_plain_human_fails():
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the work from PR #2013 is now merged "
        "and live. Think of it like a chapter finally bound into the book "
        "— the story continues without interruption."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "PR" in out["reasons"][0] or "issue" in out["reasons"][0]


def test_literal_first_test_count_in_plain_human_fails():
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the suite shows 1620 tests passed and "
        "the report is ready. Think of it like a finished harvest — every "
        "basket counted and stacked in the barn."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "test count" in out["reasons"][0]


def test_literal_first_ci_state_in_plain_human_fails():
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: CI is green and the build passed this "
        "morning. Think of it like a green traffic light — the road ahead "
        "is clear and we can keep driving."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "CI" in out["reasons"][0]


def test_literal_first_dirty_full_text_literal_portion_fails():
    r = _base_two_layer_report()
    r["plain_human"] = _base_two_layer_report()["plain_human"]  # clean field
    r["full_text"] = (
        "THE TECHNICAL: extended the purity screen. "
        "LITERALLY WHAT I'M SAYING: think of it like a clean letter home; "
        "the change is recorded under 63c157423 and nothing else matters."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "literal portion" in out["reasons"][0]


def test_literal_first_clean_plain_human_passes():
    out = two_layer.check(_base_two_layer_report())
    assert out["pass"], out


def test_literal_first_plain_numbers_stay_legal():
    # The law bans SHAs, not numbers: a plain date and a plain count pass.
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: as of October 9 the whole crew of "
        "fourteen agents is running around the clock. Think of it like a "
        "kitchen with every burner lit — the meal is cooking on all sides."
    )
    out = two_layer.check(r)
    assert out["pass"], out


def test_literal_first_chopped_sha_fails():
    # HOLE 2 regression (2026-10-09): chopping a SHA into sub-7-char chunks
    # does not launder it — it stays reassembleable machine exhaust, and
    # any human reader can put it back together. The purity screen measures
    # reassembleable exhaust, not just contiguous runs.
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the turning point arrived quietly, like "
        "a key sliding into a lock. Think of it as commit "
        "8ce2f fc015 f89feb af9045 52f81f — the moment everything snapped "
        "into place for you, basically a fresh start."
    )
    out = two_layer.check(r)
    assert not out["pass"], out
    assert "reassembled" in out["reasons"][0]


def test_literal_first_hex_words_in_prose_stay_legal():
    # The reassembly heuristic is tuned for machine exhaust, not English:
    # incidental hex-words ("beef", "face") carry no digits and pass.
    # A single sub-7-char hex word alone is not flagged either.
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the kitchen is finally stocked, like a "
        "pantry after market day. Think of it as beef and face paint at the "
        "county fair — simply put, basically a good honest day for the crew."
    )
    out = two_layer.check(r)
    assert out["pass"], out


def _literal_attack_report(body):
    r = _base_two_layer_report()
    r["plain_human"] = (
        "Literally what I'm saying: the work finished cleanly, like a "
        "letter sealed and sent. Think of it as a quiet handoff — "
        + body + " simply put, basically done."
    )
    return r


def test_literal_first_word_interleaved_chop_fails():
    # RESIDUAL 2 hardened (2026-10-09): the screen measures EFFECTIVE hex
    # content, not contiguity. Junk words interleaved between chunks
    # ("01c2 and ab90 and ...") no longer launder the exhaust.
    out = two_layer.check(_literal_attack_report(
        "the receipt lists 01c2 and ab90 and 7a6c and 52d3 for the record"
    ))
    assert not out["pass"], out
    assert "machine exhaust" in out["reasons"][0]


def test_literal_first_single_char_interleave_fails():
    # Single characters interleaved between chunks ("0 x 1 x c x 2") are
    # still mechanically reassembleable exhaust.
    out = two_layer.check(_literal_attack_report(
        "chunks read 0 x 1 x c x 2 x a x b x 9 x 0 in the log"
    ))
    assert not out["pass"], out
    assert "machine exhaust" in out["reasons"][0]


def test_literal_first_fullwidth_hex_fails():
    # Full-width hex is the same exhaust in a different costume
    # (cross-lane with the homograph residual): NFKC folds it first.
    out = two_layer.check(_literal_attack_report(
        "the code ０１ｃ２ and ａｂ９０ and ７ａ６ｃ was here"
    ))
    assert not out["pass"], out
    assert "machine exhaust" in out["reasons"][0]


def test_literal_first_segregated_long_chop_fails():
    # A chop that deliberately segregates digits from letters ("01 23 45
    # ab cd ef ...") is still 20 hex chars of exhaust a reader reassembles;
    # tier B catches long segregated runs without a mixed chunk.
    out = two_layer.check(_literal_attack_report(
        "chunks 01 23 45 ab cd ef 67 89 aa bb logged for reference"
    ))
    assert not out["pass"], out
    assert "machine exhaust" in out["reasons"][0]


def test_literal_first_hex_word_number_prose_stays_legal():
    # The mixed-chunk tuning keeps honest prose legal: hex-words next to
    # numbers ("the cafe added 12 tables", "face 1234") are not exhaust —
    # no single chunk mixes digits and letters the way a real SHA fragment
    # does. (The pre-hardening contiguous rule false-positived on these.)
    for body in (
        "the cafe added 12 tables this morning",
        "we face 1234 angry badgers daily",
    ):
        out = two_layer.check(_literal_attack_report(body))
        assert out["pass"], (body, out)


def test_literal_first_documented_residual_bounds():
    # NAMED RESIDUALS, pinned as documented bounds (not hidden): single
    # hex chars separated by whole words, and short (<12-char)
    # digit/letter-segregated fragments, are maximally conspicuous
    # word-salad — closing them re-opens list-prose false positives
    # (measured in batch4-residual-evidence/). The human seat stays in
    # the loop for these. If a future change closes them, update the
    # HONEST BOUND in two_layer.py alongside this test.
    for body in (
        "0 and 1 and c and 2 and a and b and 9 and 0 logged",
        "see chunks 01 23 ab cd here",
    ):
        out = two_layer.check(_literal_attack_report(body))
        assert out["pass"], (body, out)


def test_literal_first_technicals_keep_their_exhaust():
    # The technical layer may carry SHAs/PRs/counts — purity is about the
    # LITERAL layer only.
    r = _base_two_layer_report()
    r["technical"] = (
        "Merged via #2013 at 74a5cb20e; 309 tests passed, CI green. The "
        "purity screen lives in tools/protocol/checks/two_layer.py."
    )
    out = two_layer.check(r)
    assert out["pass"], out


# ---------------------------------------------------------------- base_lineage
def _git(cwd, *args):
    env = dict(
        os.environ,
        GIT_AUTHOR_NAME="t",
        GIT_AUTHOR_EMAIL="t@t",
        GIT_COMMITTER_NAME="t",
        GIT_COMMITTER_EMAIL="t@t",
    )
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, env=env,
        timeout=30,
    )


def _fixture_repo():
    """A lineage fixture repo with a known shape.

    main:    A -- B   (B adds repair marker 'repair2.txt')
    branch:  A -- C   (C DELETES marker 'repair1.txt')
    """
    d = tempfile.mkdtemp(prefix="lineage-")
    _git(d, "init", "-q", "-b", "main", ".")
    _git(d, "config", "commit.gpgsign", "false")
    Path(d, "repair1.txt").write_text("prior repair one")
    _git(d, "add", ".")
    _git(d, "commit", "-qm", "A: first repair lands")
    _git(d, "checkout", "-qb", "work")
    Path(d, "repair1.txt").unlink()
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "C: work branch silently drops repair1")
    _git(d, "checkout", "-q", "main")
    Path(d, "repair2.txt").write_text("prior repair two")
    _git(d, "add", ".")
    _git(d, "commit", "-qm", "B: second repair lands on main")
    sha = lambda ref: _git(d, "rev-parse", ref).stdout.strip()
    return d, {"A": sha("main~1"), "B": sha("main"), "C": sha("work")}


def _lineage_record(repo, tip, markers, **kw):
    rec = {"branch_tip": tip, "live_line": "main", "repo": repo,
           "required_markers": markers}
    rec.update(kw)
    return rec


def test_base_lineage_silent_discard_fails():
    d, s = _fixture_repo()
    out = base_lineage.check(
        _lineage_record(d, s["C"], ["repair1.txt"]))
    assert not out["pass"], out
    assert "silently discarded" in out["reasons"][0]


def test_base_lineage_wrong_ancestor_fails():
    d, s = _fixture_repo()
    # Branch forked at A; main has since moved to B with repair2.txt.
    # Claiming to build on repair2 while forked at A is the wrong ancestor.
    out = base_lineage.check(
        _lineage_record(d, s["C"], ["repair2.txt"]))
    assert not out["pass"], out
    assert "wrong ancestor" in out["reasons"][0]


def test_base_lineage_dishonest_claimed_base_fails():
    d, s = _fixture_repo()
    out = base_lineage.check(
        _lineage_record(d, s["C"], ["repair1.txt"], claimed_base=s["B"]))
    assert not out["pass"], out
    assert "true fork point" in out["reasons"][0]


def test_base_lineage_honest_lineage_passes():
    d, s = _fixture_repo()
    # Fresh branch honestly forked at B, keeps both markers, adds work.
    _git(d, "checkout", "-qb", "fresh", "main")
    Path(d, "new.txt").write_text("new work")
    _git(d, "add", ".")
    _git(d, "commit", "-qm", "D: new work on current base")
    tip = _git(d, "rev-parse", "fresh").stdout.strip()
    out = base_lineage.check(
        _lineage_record(d, tip, ["repair1.txt", "repair2.txt"],
                        claimed_base=s["B"]))
    assert out["pass"], out
    assert out["details"]["fork_point"] == s["B"]


def test_base_lineage_unresolvable_tip_fails_closed():
    d, s = _fixture_repo()
    out = base_lineage.check(
        _lineage_record(d, "deadbeef" * 5, ["repair1.txt"]))
    assert not out["pass"], out


def test_base_lineage_missing_shape_fails_closed():
    out = base_lineage.check({"branch_tip": "abc123"})
    assert not out["pass"], out


# ---------------------------------------------------------------- falsification_first
def test_falsification_copied_builder_battery_fails():
    r = _base_falsification_report()
    r["verifier_attacks"] = [
        {"input": "Clean literal layer passes", "outcome": "held"},
    ]
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "relabel" in out["reasons"][0]


def test_falsification_claimed_attacks_but_none_listed_fails():
    r = _base_falsification_report()
    r["verifier_attacks"] = []
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "no attack inputs" in out["reasons"][0]


def test_falsification_unknown_outcome_fails_closed():
    r = _base_falsification_report()
    r["verifier_attacks"] = [{"input": "fuzzing the boundary values", "outcome": "unknown"}]
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "not honest" in out["reasons"][0]


def test_falsification_broken_claim_cannot_be_verified():
    r = _base_falsification_report()
    r["verifier_attacks"] = [
        {"input": "a seven-character hex fingerprint buried mid-sentence",
         "outcome": "broke"},
    ]
    r["verdict"] = "verified"
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "contradiction" in out["reasons"][0]


def test_falsification_undeclared_gap_fails():
    r = _base_falsification_report()
    r["attacks_tried"] = False
    r["verifier_attacks"] = []
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "must say why" in out["reasons"][0]


def test_falsification_honest_attacks_all_held_passes():
    out = falsification_first.check(_base_falsification_report())
    assert out["pass"], out
    assert out["details"]["strength"] == "falsification-attempted-all-held"


def test_falsification_broken_claim_honest_verdict_passes():
    r = _base_falsification_report()
    r["verifier_attacks"] = [
        {"input": "a seven-character hex fingerprint buried mid-sentence",
         "outcome": "broke"},
    ]
    r["verdict"] = "not-verified"
    out = falsification_first.check(r)
    assert out["pass"], out
    assert out["details"]["strength"] == "falsification-attempted-claim-broken"


def test_falsification_declared_gap_passes_as_declared():
    r = _base_falsification_report()
    r["attacks_tried"] = False
    r["verifier_attacks"] = []
    r["no_attacks_reason"] = (
        "time-boxed smoke check only; full falsification scheduled next shift"
    )
    r["verdict"] = "provisional"
    out = falsification_first.check(r)
    assert out["pass"], out
    assert out["details"]["strength"] == "declared-not-falsification-tested"


def test_falsification_missing_claim_fails_closed():
    r = _base_falsification_report()
    del r["claim"]
    out = falsification_first.check(r)
    assert not out["pass"], out


def test_falsification_attack_without_input_fails():
    r = _base_falsification_report()
    r["verifier_attacks"] = [{"input": "x", "outcome": "held"}]
    out = falsification_first.check(r)
    assert not out["pass"], out
    assert "no real attack input" in out["reasons"][0]


def test_falsification_separator_relabel_fails():
    # HOLE 1 regression (2026-10-09): normalization FOLDS punctuation to a
    # common separator — it never deletes it. Underscores, dashes, and dots
    # all fold to the same separator as a plain space, so the most natural
    # relabel there is (snake_case battery -> spaced words) is a caught
    # copy, not a distinct attack.
    battery = ["test_literal_first_sha_fails"]
    for relabel in (
        "test literal first sha fails",   # underscore -> space
        "test-literal-first-sha-fails",   # underscore -> dash
        "test.literal.first.sha.fails",   # underscore -> dot
        "Test Literal First Sha Fails",   # case + spaces
    ):
        r = _base_falsification_report()
        r["builder_battery"] = battery
        r["verifier_attacks"] = [{"input": relabel, "outcome": "held"}]
        out = falsification_first.check(r)
        assert not out["pass"], (relabel, out)
        assert "relabel" in out["reasons"][0]


def test_falsification_folded_norm_keeps_distinct_attacks():
    # Folding must not over-collapse: battery entries that differ only in
    # words stay distinct, and a genuinely different attack still passes.
    r = _base_falsification_report()
    r["builder_battery"] = ["test_login_happy_path", "test_login_sad_path"]
    r["verifier_attacks"] = [
        {"input": "null bytes smuggled into the name field", "outcome": "held"},
    ]
    out = falsification_first.check(r)
    assert out["pass"], out


def test_falsification_homograph_relabel_fails():
    # RESIDUAL 1 hardened (2026-10-09): the confusable skeleton folds
    # full-width, circled, math-bold, Cyrillic and Greek lookalikes to the
    # same identity a human reader sees. A battery entry wearing
    # confusable characters is a relabel, not a new attack.
    def sub(s, table):
        return "".join(table.get(ch, ch) for ch in s)

    def fullwidth(s):
        return "".join(chr(ord(ch) + 0xFEE0) if "!" <= ch <= "~" else ch for ch in s)

    canon = "snake_case_probe_alpha"
    cyr = {"a": "а", "e": "е", "o": "о", "p": "р",
           "c": "с", "x": "х", "s": "ѕ", "h": "һ"}
    # Table-grounded Greek twins (Unicode confusables.txt, UTS #39 v18,
    # via tools/protocol/checks/confusables_table.py): α→a, Ε→E, ο→o,
    # ρ→p, ι→i. U+03B5 (Greek SMALL epsilon) is deliberately NOT a twin
    # here — confusables.txt maps it to U+A793, not 'e' — so the capital
    # Ε carries the e-twin. Hand-written twins are not ground truth;
    # the shared table is.
    grk = {"a": "α", "e": "Ε", "o": "ο", "p": "ρ", "i": "ι"}
    relabels = [
        fullwidth(canon),                                            # full-width Latin
        "".join(chr(0x24D0 + ord(c) - 97) if c.isalpha() else c      # circled
                for c in canon),
        "".join(chr(0x1D41A + ord(c) - 97) if c.isalpha() else c     # math bold
                for c in canon),
        sub(canon, cyr),                                            # Cyrillic mix
        sub(canon, grk),                                            # Greek mix
        sub(fullwidth(canon), cyr),                                 # mixed costumes
        canon.replace("e", "é"),                                    # combining acute
    ]
    for relabel in relabels:
        r = _base_falsification_report()
        r["builder_battery"] = [canon]
        r["verifier_attacks"] = [{"input": relabel, "outcome": "held"}]
        out = falsification_first.check(r)
        assert not out["pass"], (relabel, out)
        assert "relabel" in out["reasons"][0]


def test_falsification_compatibility_relabel_fails():
    # NFKC folds compatibility characters before the skeleton is compared:
    # ligatures, roman numerals, eszett and superscripts are the same
    # identifier in a different costume.
    pairs = [
        ("official_filter_test", "oﬃcial_ﬁlter_test"),
        ("test_IV_probe", "test_Ⅳ_probe"),
        ("test_strasse_probe", "test_straße_probe"),
        ("test_2_probe", "test_²_probe"),
    ]
    for canon, relabel in pairs:
        r = _base_falsification_report()
        r["builder_battery"] = [canon]
        r["verifier_attacks"] = [{"input": relabel, "outcome": "held"}]
        out = falsification_first.check(r)
        assert not out["pass"], (canon, relabel, out)


def test_falsification_skeleton_nfkc_shadow_residual_closed():
    # NFKC-shadow residual (2026-10-09): the shared table is NFKC-consistent,
    # so the skeleton folds every shadowed entry to what a human reads --
    # identically in both lanes. Lunate sigmas include the direct NFKC
    # outputs an attacker can type by hand (the fix2 closure, ported here).
    sk = falsification_first._skeleton
    for twin in ("\u03f2oda-1", "\u03f9oda-1", "\u03c2oda-1", "\u03a3oda-1"):
        assert sk(twin) == "coda-1", f"sigma twin {twin!r} -> {sk(twin)!r}"
    assert sk("\u017fin-1") == "sin-1"          # LONG S -> 's', not 'f'
    for twin in ("\u2110ook-1", "\u2111ook-1", "\u2160ook-1", "\uff29ook-1"):
        assert sk(twin) == "iook-1", f"I twin {twin!r} -> {sk(twin)!r}"
    assert sk("naya-\U0001d7ce") == "naya-0"       # digits stay digits
    assert sk("naya-\U0001d7cf") == "naya-1"


def test_falsification_skeleton_keeps_honest_unicode_attacks():
    # The skeleton must not over-collapse: genuinely different attacks that
    # happen to carry non-ASCII (accents, German, emoji) stay distinct and
    # pass. Folding merges only what a human reads as identical.
    r = _base_falsification_report()
    r["builder_battery"] = ["null_byte_injection", "oversized-payload-boundary"]
    r["verifier_attacks"] = [
        {"input": "naïve résumé parsing with unicode edge cases", "outcome": "held"},
        {"input": "Größe des Puffers prüfen mit Umlauten", "outcome": "held"},
    ]
    out = falsification_first.check(r)
    assert out["pass"], out


def test_falsification_allcaps_canonical_matches_lowercase_relabel():
    # casefold("I") is "ı" (dotless i): without the ı→i fold, an ALL-CAPS
    # canonical would normalize apart from its lowercase twin — a relabel
    # lane through case alone.
    r = _base_falsification_report()
    r["builder_battery"] = ["KILIT_KONTROL"]
    r["verifier_attacks"] = [{"input": "kilit_kontrol", "outcome": "held"}]
    out = falsification_first.check(r)
    assert not out["pass"], out


# ---------------------------------------------------------------- manifest integrity
def test_manifest_batch4_slots():
    import json

    d = json.loads((ROOT / "kernel" / "protocol" / "protocol_manifest.json").read_text())
    laws = d["laws"]
    by_id = {l["id"]: (i, l) for i, l in enumerate(laws)}
    # Slot 10 amended with the literal-first refinement.
    assert "LITERAL-FIRST" in by_id["TWO-LAYER-LAW"][1]["statement"], by_id
    # Slots 13, 14 appended after the batch-2 tail.
    assert by_id["BASE-LINEAGE-LAW"][0] == 13
    assert by_id["FALSIFICATION-FIRST-LAW"][0] == 14
    assert by_id["BASE-LINEAGE-LAW"][1]["check"] == "tools/protocol/checks/base_lineage.py"
    assert by_id["FALSIFICATION-FIRST-LAW"][1]["check"] == "tools/protocol/checks/falsification_first.py"
    # The batch-2 tail is untouched: no renumbering, no slot theft.
    assert by_id["TWO-LAYER-LAW"][0] == 10
    assert by_id["BLOCKER-SURFACING"][0] == 11
    assert by_id["FAIL-CLOSED-SHAPE"][0] == 12


if __name__ == "__main__":
    fns = sorted(
        (n, f) for n, f in list(globals().items())
        if n.startswith("test_") and callable(f)
    )
    failed = 0
    for name, fn in fns:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
        else:
            print(f"ok {name}")
    print(f"{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
