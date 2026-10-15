#!/usr/bin/env python3
"""Translated battery for tools/post_checker.py (Naya Gamma, w181).

The tip's 427-line battery pinned the superseded comm-standard vocabulary
(WHO/MISSION/STATUS/TRUTH/... fields, check_post). It was translated, not
copied: the FAILURE-MODE COVERAGE was ported to the canonical three-level
protocol schema — quoted/fenced lines never bind (w157/w164 hole class),
ROSTER identity, anchored-SHA evidence, score-meaning rigor.

Run: python3 -m pytest tests/test_post_checker.py -q  (from the repo root)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.post_checker import check, check_event, _unquoted  # noqa: E402

GOOD_RECEIPT = (
    "[Naya Gamma · SIGN-OUT] VERDICT: DONE — conflict resolved.\n"
    "score: 9.5/10 — ships, verified on the merged tree.\n"
    "Why it worked: the merge rehearsed both sides before the ref moved.\n"
    "evidence: head ce6a396f388722a0bbe84899dd23123e2259e574."
)

SHA40 = "ce6a396f388722a0bbe84899dd23123e2259e574"
RUNID = "115834058324"
_EVID = "\nevidence: head " + SHA40 + "."


def fresh_log():
    d = tempfile.mkdtemp(prefix="postlog-")
    return str(Path(d) / "post-log.jsonl")


# --- w157 hole class translated: `>`-quoted lines never bind ---

def test_quoted_verdict_does_not_bind():
    """A VERDICT that exists only inside a `>` quote must not bind."""
    text = (
        "Quoting the prior receipt for reference:\n"
        "> [Naya Gamma · SIGN-OUT] VERDICT: DONE — conflict resolved.\n"
        "My own update: starting the rebase now, will report back."
    )
    flags, _ = check("RECEIPT", text)
    assert any("verdict" in f for f in flags), flags


def test_quoted_identity_does_not_bind():
    """A seat name that exists only inside a `>` quote must not satisfy
    the naming law — the author's own bare 'Naya' still flags."""
    text = (
        "> Naya Alpha\n"
        "Naya here — VERDICT: DONE — fixed the parser.\n"
        "score: 9/10 — ships, verified."
    )
    flags, _ = check("RECEIPT", text)
    assert any("naming-law" in f for f in flags), flags


def test_quoted_only_post_flags():
    """A post whose every binding element is quoted must FLAG."""
    text = (
        "> [Naya Alpha · SIGN-OUT] VERDICT: DONE — all green.\n"
        "> score: 9/10 — ships, verified.\n"
        "> Evidence: head " + SHA40 + "."
    )
    flags, _ = check("RECEIPT", text)
    assert flags, flags


def test_legit_post_with_quote_block_still_passes():
    """Control: a complete UNQUOTED receipt that also quotes someone
    else's post must still PASS."""
    text = GOOD_RECEIPT + (
        "\nQuoting the prior post for reference:\n"
        "> [Naya Beta · SIGN-OUT] VERDICT: DONE — other work.\n"
        "> score: 10/10 — perfect, ships.\n"
    )
    flags, _ = check("RECEIPT", text)
    assert flags == [], flags


# --- w164 hole class translated: fenced blocks never bind ---

def test_fenced_evidence_does_not_bind():
    """Evidence pasted inside a fence is not the author's live read —
    a claim with fence-only evidence must FLAG on claim-check."""
    text = (
        "[MERGE INTENT] CI 16/16 green on the head.\n"
        "Evidence pasted below:\n"
        "```\n"
        "head " + SHA40 + "\n"
        "check-run " + RUNID + "\n"
        "```"
    )
    flags, _ = check("EVENT", text, fresh_log())
    assert any("claim-check" in f for f in flags), flags


def test_unclosed_fence_drops_tail():
    """An UNCLOSED fence drops everything after it (fail-closed): the
    fenced signature must not bind, so the author's own bare 'Naya'
    still flags."""
    text = (
        "Naya here — VERDICT: DONE — fixed the parser.\n"
        "score: 9/10 — ships, verified.\n"
        "```\n"
        "[Naya Gamma · SIGN-OUT] appendix carrying the signature"
    )
    flags, _ = check("RECEIPT", text)
    assert any("naming-law" in f for f in flags), flags


def test_legit_post_with_fenced_appendix_still_passes():
    """Control: claim + evidence in the author's own lines with a
    fenced decoy appendix must still PASS."""
    text = (
        "[MERGE INTENT] PR #2600 at head " + SHA40
        + " — CI 19/19 green, check-run " + RUNID + ". VERDICT: ready.\n"
        "Log appendix (do not bind):\n"
        "```\n"
        "CI 0/0 green, head deadbeef\n"
        "```"
    )
    flags, append = check("EVENT", text, fresh_log())
    assert flags == [], flags
    assert append


def test_inline_code_spans_do_not_strip():
    """Inline `code` spans are formatting, not blocks."""
    text = GOOD_RECEIPT + "\nNote: ran `pytest` on `tools/post_checker.py`.\n"
    flags, _ = check("RECEIPT", text)
    assert flags == [], flags


# --- ROSTER identity translated: roster names folded into SEAT_RE ---

def test_numbered_seat_signs():
    flags, _ = check(
        "RECEIPT",
        "[Naya 4 · SIGN-OUT] VERDICT: DONE — opened the PR.\n"
        "score: 9/10 — ships, verified." + _EVID,
    )
    assert flags == [], flags


def test_lead_narzan_signs():
    flags, _ = check(
        "RECEIPT",
        "Naya Verity Narzan — VERDICT: DONE — repaired the gate.\n"
        "score: 9.5/10 — ships, verified." + _EVID,
    )
    assert flags == [], flags


def test_leader_agent_signs():
    flags, _ = check(
        "RECEIPT",
        "Naya Clarity Seeker reporting — VERDICT: DONE — mapped the seam.\n"
        "score: 8/10 — ships after one more pass." + _EVID,
    )
    assert flags == [], flags


def test_bare_agent_flags():
    """'Naya Seeker' with no leader prefix is incomplete identity."""
    flags, _ = check(
        "RECEIPT",
        "Naya Seeker reporting — VERDICT: DONE — mapped the seam.\n"
        "score: 8/10 — ships.",
    )
    assert any("naming-law" in f for f in flags), flags


def test_non_roster_name_flags():
    flags, _ = check(
        "RECEIPT",
        "Naya Narzan 4 did the thing. VERDICT: DONE.\n"
        "score: 9/10 — ships.",
    )
    assert any("naming-law" in f for f in flags), flags


# --- Score-meaning rigor translated (RECEIPT: no bare numbers, ever) ---

def test_receipt_requires_score():
    flags, _ = check(
        "RECEIPT",
        "[Naya Alpha · SIGN-OUT] VERDICT: DONE — fixed the parser.\n"
        "Why it worked: read the live seat list.",
    )
    assert any("n/10" in f for f in flags), flags


def test_bare_score_flags():
    flags, _ = check(
        "RECEIPT",
        "[Naya Delta · SIGN-OUT] VERDICT: DONE — audit complete.\n"
        "SCORE: 9/10\n"
        "NEEDS: re-review — Naya Delta.",
    )
    assert any("meaning unstated" in f for f in flags), flags


def test_meaning_word_boundaries():
    """'relationships' is not 'ships'; 'meaningless' is not 'meaning'."""
    flags, _ = check(
        "RECEIPT",
        "[Naya Alpha · SIGN-OUT] VERDICT: DONE — x.\n"
        "SCORE: 8/10 — the relationships here are fine.",
    )
    assert any("meaning unstated" in f for f in flags), flags
    flags, _ = check(
        "RECEIPT",
        "[Naya Alpha · SIGN-OUT] VERDICT: DONE — x.\n"
        "SCORE: 8/10 — this is meaningless filler.",
    )
    assert any("meaning unstated" in f for f in flags), flags
    flags, _ = check(
        "RECEIPT",
        "[Naya Alpha · SIGN-OUT] VERDICT: DONE — x.\n"
        "SCORE: 8/10 — ships after one more pass." + _EVID,
    )
    assert flags == [], flags


def test_score_with_meaning_passes():
    flags, _ = check("RECEIPT", GOOD_RECEIPT)
    assert flags == [], flags


# --- Anchored-SHA evidence translated (claim-check) ---

def test_anchored_short_sha_counts():
    """A 7-40 hex word WITH an anchor (@/tip/sha:/commit) is evidence."""
    for body in (
        "[MERGE INTENT] CI 16/16 green, tip 59e8a9af observed.",
        "Tests 45/45 green — evidence: commit abc1234.",
        "[MERGE INTENT] CI 16/16 green. EVIDENCE: @ deadbeef01.",
    ):
        flags, _ = check("EVENT", body, fresh_log())
        assert flags == [], (body, flags)


def test_bare_hex_word_is_not_evidence():
    """Hole 5 translated: a bare hex word in prose is not evidence."""
    flags, _ = check(
        "EVENT",
        "[MERGE INTENT] CI 16/16 green. Evidence: deadbeef in prose.",
        fresh_log(),
    )
    assert any("claim-check" in f for f in flags), flags


def test_claim_without_evidence_still_flags():
    """The #2597 incident shape: claim, no cited live read."""
    flags, _ = check(
        "EVENT",
        "[MERGE INTENT] PR #2597 — CI 16/16 required green, "
        "all checks passing. Ready to merge.",
        fresh_log(),
    )
    assert any("claim-check" in f for f in flags), flags


# --- CLI translated to the current --level-first shape ---

def test_cli_receipt_pass_and_flag(tmp_path):
    good = tmp_path / "good.md"
    good.write_text(GOOD_RECEIPT)
    r = subprocess.run(
        [sys.executable, "tools/post_checker.py", "--level", "RECEIPT",
         str(good)],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("PASS")
    bad = tmp_path / "bad.md"
    bad.write_text("hello world")
    r = subprocess.run(
        [sys.executable, "tools/post_checker.py", "--level", "RECEIPT",
         str(bad)],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 1
    assert r.stdout.startswith("FLAG")


def test_cli_event_anchored_sha_passes(tmp_path):
    post = tmp_path / "post.md"
    post.write_text(
        "[MERGE INTENT] CI 16/16 green, tip 59e8a9af observed. "
        "VERDICT: ready.")
    r = subprocess.run(
        [sys.executable, "tools/post_checker.py", "--level", "EVENT",
         "--post-log", str(tmp_path / "log.jsonl"), "--no-append",
         str(post)],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("PASS")


# --- _unquoted unit behavior (ported verbatim from the tip) ---

def test_unquoted_strips_quotes_and_fences():
    body = (
        "My own line.\n"
        "> quoted line\n"
        "```\n"
        "fenced line\n"
        "```\n"
        "Another own line."
    )
    assert _unquoted(body) == "My own line.\nAnother own line."


def test_unquoted_tilde_fence():
    body = "Own.\n~~~\nfenced\n~~~\nOwn2."
    assert _unquoted(body) == "Own.\nOwn2."


def test_unquoted_lazy_continuation_kept():
    """Quote continuation without a leading `>` is the author's prose."""
    body = "> quoted\ncontinuation without marker"
    assert _unquoted(body) == "continuation without marker"


# --- w202: claim-check extended to PULSE and RECEIPT (Gamma) ---
# The #2597 class is level-agnostic: a RECEIPT or PULSE can overstate
# just as an EVENT can. The gate fires only when a quantitative claim
# is present — claim-free posts are unaffected.

NO_EVID_RECEIPT = (
    "[Naya Gamma · SIGN-OUT] VERDICT: DONE — conflict resolved.\n"
    "score: 9.5/10 — ships, verified on the merged tree.\n"
    "Why it worked: the merge rehearsed both sides before the ref moved."
)


def test_pulse_quant_claim_without_evidence_flags():
    text = (
        "[PULSE] Naya Gamma | lane 4 | wiring the gate\n"
        "state: doing — 2/2 suites green so far"
    )
    flags, _ = check("PULSE", text)
    assert any("claim-check" in f for f in flags), flags


def test_pulse_quant_claim_with_runid_passes():
    text = (
        "[PULSE] Naya Gamma | lane 4 | starting the wiring\n"
        "state: doing — 2/2 suites green so far, run 115834058324"
    )
    flags, _ = check("PULSE", text)
    assert flags == [], flags


def test_pulse_without_quant_claim_unaffected():
    """A claim-free PULSE needs no evidence — the gate is conditional."""
    text = (
        "[PULSE] Naya Gamma | lane 4 | starting the build\n"
        "state: doing — opening the worktree"
    )
    flags, _ = check("PULSE", text)
    assert flags == [], flags


def test_receipt_scorecard_numbers_without_evidence_flag():
    """A scored receipt with no cited live read is the #2597 shape."""
    flags, _ = check("RECEIPT", NO_EVID_RECEIPT)
    assert any("claim-check" in f for f in flags), flags


def test_receipt_with_evidence_passes():
    """Control: the same receipt with an anchored SHA passes."""
    flags, _ = check("RECEIPT", GOOD_RECEIPT)
    assert flags == [], flags


def test_receipt_world_claim_with_runid_passes():
    text = (
        "[Naya Gamma · SIGN-OUT] VERDICT: DONE — gate wired.\n"
        "score: 9/10 — ships, one more adversarial pass owed.\n"
        "evidence: 13/13 fixtures green, run 115834058324."
    )
    flags, _ = check("RECEIPT", text)
    assert flags == [], flags


def test_claim_check_identical_across_levels():
    """Same claim, same flag text on EVENT and RECEIPT — one gate,
    not three dialects."""
    claim = "merge intent: 16/16 required green."
    f_event, _ = check("EVENT", "[EVENT] Naya Gamma\n" + claim, fresh_log())
    f_receipt, _ = check(
        "RECEIPT",
        "[Naya Gamma · SIGN-OUT] VERDICT: DONE — x.\n"
        "score: 9/10 — ships.\n" + claim,
    )
    ev = [f for f in f_event if f.startswith("claim-check")]
    rc = [f for f in f_receipt if f.startswith("claim-check")]
    # Same gate, same advisory on both levels. The enumerated claims
    # differ (the RECEIPT's own score is itself a fraction claim) —
    # what must be identical is the gate header and the live-read
    # advisory. That is the "one gate, not three dialects" property.
    header = "claim-check: quantitative claim(s) with no cited live read"
    advisory = "Never from memory of an earlier check"
    assert ev and rc, (ev, rc)
    for f in (ev[0], rc[0]):
        assert f.startswith(header), f
        assert f.endswith(advisory), f


def test_slash_item_list_is_not_a_claim():
    """'items 1/5/7' is enumeration, not a quantitative claim — the
    standard tag-off format must not trip claim-check (w202)."""
    text = (
        "[PULSE] Naya Gamma | lane 4 | starting the wiring\n"
        "state: doing — items 1/5/7 routed as un-doable this shift"
    )
    flags, _ = check("PULSE", text)
    assert flags == [], flags


def test_true_fraction_still_flags():
    """Control: a real fraction claim still fires (the #2597 shape)."""
    text = (
        "[PULSE] Naya Gamma | lane 4 | starting the merge\n"
        "state: doing — 16/16 required green"
    )
    flags, _ = check("PULSE", text)
    assert any("claim-check" in f for f in flags), flags
