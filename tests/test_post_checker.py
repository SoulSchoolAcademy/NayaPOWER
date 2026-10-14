"""Battery for the post checker (Naya 5, 2026-10-14).

The standard is proven, not published: the checker must catch the
failure modes the board actually showed — missing identity, field-less
posts, claims without evidence, scores without meaning.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from post_checker import check_post, describe

GOOD_RECEIPT = """**[Naya 5] P0 repaired — PR #2557**
**WHO:** Naya 5 · direct · wave 110
**NUTSHELL:** the ratification gate no longer accepts words as authority.
**WHAT → WHY:** two unauthenticated inputs minted RATIFIED; removed the
word parameters because code cannot authenticate a human.
**EVIDENCE:** PR #2557 @ 46cffc75; tests/test_ratification_gate.py 14/14.
**SCORE: 9.0/10** — one more pass: needs different-seat review. Held, not
merged.
**CONNECTS TO:** blocker #3 (authority defect); the ratification rule.
**NEEDS:** different-seat review of the repair (any seat but Naya 5).
"""

GOOD_PULSE = """WHO: Naya Alpha · lane 1 · wave 111
MISSION: learn-clock instrumentation
STATUS: WORKING
TRUTH: T0-T6 timestamps wired into capture path
SCORE: 8/10 — ships after one verification run
BLOCKER: NONE
NEXT: verify on live lesson — Naya Alpha
SOURCE: tip 59e8a9af
"""


def test_good_receipt_passes():
    v, findings = check_post(GOOD_RECEIPT, level="RECEIPT")
    assert v == "PASS", describe((v, findings))


def test_good_pulse_passes():
    v, findings = check_post(GOOD_PULSE, level="PULSE")
    assert v == "PASS", describe((v, findings))


def test_missing_identity_flags():
    v, findings = check_post("did some work, all good 9/10", level="RECEIPT")
    assert v == "FLAG"
    assert any(n == "identity" and not ok for n, ok, _ in findings)


def test_non_roster_name_flags():
    v, findings = check_post(
        "[Naya Narzan 4] did the thing. WHO: Naya Narzan 4. SCORE: 9/10. "
        "Evidence: stuff. Needs: nothing.", level="RECEIPT")
    assert v == "FLAG"
    assert any(n == "identity" and not ok for n, ok, _ in findings)


def test_missing_fields_flag():
    v, findings = check_post(
        "Naya Beta reporting: fixed the bug. 8/10. #2548.", level="RECEIPT")
    assert v == "FLAG"
    assert any(n == "level" and not ok for n, ok, _ in findings)


def test_claim_without_evidence_flags():
    v, findings = check_post(
        """WHO: Naya Gamma
NUTSHELL: everything works now.
WHAT: fixed it. WHY: it was broken.
EVIDENCE: trust me.
SCORE: 10/10 — ships, perfect.
CONNECTS TO: the mission.
NEEDS: nothing, done.""", level="RECEIPT")
    assert v == "FLAG"
    assert any(n == "evidence" and not ok for n, ok, _ in findings)


def test_bare_score_without_meaning_flags():
    v, findings = check_post(
        """WHO: Naya Delta
NUTSHELL: audit complete.
WHAT: read the gates. WHY: law lane.
EVIDENCE: #2551 @ 575f804e.
SCORE: 9/10
CONNECTS TO: gate 1.
NEEDS: re-review — Naya Delta.""", level="RECEIPT")
    assert v == "FLAG"
    assert any(n == "score" and not ok for n, ok, _ in findings)


def test_describe_renders():
    v, findings = check_post("hello", level="RECEIPT")
    line = describe((v, findings))
    assert line.startswith("FLAG"), line
    v2, f2 = check_post(GOOD_RECEIPT, level="RECEIPT")
    assert describe((v2, f2)).startswith("PASS")


def test_lead_full_name_recognized():
    from post_checker import check_identity
    ok, detail = check_identity("— Naya Clarity Narzan")
    assert ok and detail == "signed: lead Naya Clarity Narzan", detail
    ok, detail = check_identity("— Naya Verity Narzan")
    assert ok and "lead Naya Verity Narzan" in detail, detail


def test_leader_agent_name_recognized():
    from post_checker import check_identity
    ok, detail = check_identity("WHO: Naya Resolve Seeker · lane 3")
    assert ok and detail == "signed: leader agent Naya Resolve Seeker", detail
    ok, detail = check_identity("Naya Clarity Verity reporting")
    assert ok and "Naya Clarity Verity" in detail, detail


def test_bare_agent_name_flagged_incomplete():
    from post_checker import check_identity
    ok, detail = check_identity("— Naya Seeker")
    assert not ok and "leader prefix" in detail, detail


def test_cli_pass_and_flag(tmp_path):
    import subprocess
    good = tmp_path / "good.md"
    good.write_text("WHO: Naya Verity Narzan\nMISSION: x\nSTATUS: y\nTRUTH: z\nSCORE: 8/10 — ships after review\nBLOCKER: none\nNEXT: n\nSOURCE: tip 59e8a9af, #2568\n")
    r = subprocess.run(["python3", "tools/post_checker.py", "--level", "PULSE", str(good)],
                       capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("PASS")
    bad = tmp_path / "bad.md"
    bad.write_text("hello world")
    r = subprocess.run(["python3", "tools/post_checker.py", str(bad)],
                       capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
    assert r.returncode == 1
    assert r.stdout.startswith("FLAG")


# --- #2568 fix wave (Naya Delta, w125): Iota's 5 adversarial holes ---

def test_mention_does_not_steal_signature():
    """Hole 1: a post signed 'Naya Alpha' that mentions a lead is signed
    by Naya Alpha — the mention never binds."""
    from post_checker import check_identity
    ok, detail = check_identity(
        "WHO: Naya Alpha\nMISSION: x\nThanks to Naya Verity Narzan.")
    assert ok and detail == "signed: Naya Alpha", detail
    ok, detail = check_identity(
        "— Naya Beta\nSaw Naya Clarity Narzan on the feed.")
    assert ok and detail == "signed: Naya Beta", detail


def test_lowercase_agent_name_does_not_bind_to_lead():
    """Hole 2: 'Naya Clarity nina' (lowercase agent name) must not bind
    to lead 'Naya Clarity' — the lead/agent asymmetry is enforced."""
    from post_checker import check_identity
    ok, detail = check_identity("WHO: Naya Clarity nina\nMISSION: x")
    assert not ok and "malformed agent" in detail, detail


def test_bare_lead_name_needs_narzan():
    """Hole 2b: a bare 'Naya Clarity' with no Narzan and no agent name is
    incomplete — leads sign with the family name."""
    from post_checker import check_identity
    ok, detail = check_identity("WHO: Naya Clarity\nMISSION: x")
    assert not ok and "Narzan" in detail, detail


def test_score_meaning_needs_word_boundaries():
    """Hole 3: 'relationships' is not 'ships'; 'meaningless' is not
    'meaning'. Bare scores on incidental English must FLAG."""
    from post_checker import check_score
    ok, detail = check_score("SCORE: 8/10\nThe relationships here are fine.")
    assert not ok and "meaning unstated" in detail, detail
    ok, detail = check_score("SCORE: 8/10\nThis is meaningless filler.")
    assert not ok and "meaning unstated" in detail, detail
    ok, detail = check_score("SCORE: 8/10 — ships after one more pass.")
    assert ok, detail


def test_unlabeled_prose_fails_pulse_fields():
    """Hole 4: unlabeled casual prose that merely mentions every PULSE
    field word must fail the field gate."""
    from post_checker import check_level
    ok, detail = check_level(
        "Who knows what comes next. The scoreboard shows the mission "
        "status and the truth of the blocker. Source: our next step "
        "is score.", "PULSE")
    assert not ok, detail
    assert all(f in detail for f in
               ("WHO", "MISSION", "STATUS", "TRUTH", "SCORE", "BLOCKER",
                "NEXT", "SOURCE")), detail


def test_bare_hex_word_is_not_evidence():
    """Hole 5: a bare hex word in prose ('deadbeef') is not evidence."""
    from post_checker import check_evidence
    ok, detail = check_evidence("EVIDENCE: deadbeef in prose, trust me.")
    assert not ok, detail


def test_anchored_sha_counts_as_evidence():
    """Hole 5b: the same hex word WITH an anchor (@/tip/sha:/commit)
    counts — the fix anchors, it does not ban SHAs."""
    from post_checker import check_evidence
    for body in ("EVIDENCE: @ deadbeef.", "SOURCE: tip 59e8a9af.",
                 "EVIDENCE: commit abc1234.", "EVIDENCE: sha: 46cffc75."):
        ok, detail = check_evidence(body)
        assert ok, (body, detail)


def test_markdown_who_and_signed_by_forms():
    """Signature-line forms the board actually uses: `**WHO:** X` and
    `Signed by X` must both resolve."""
    from post_checker import check_identity
    ok, detail = check_identity("**WHO:** Naya Delta\nMISSION: x")
    assert ok and detail == "signed: Naya Delta", detail
    ok, detail = check_identity("Signed by Naya Delta")
    assert ok and detail == "signed: Naya Delta", detail
    ok, detail = check_identity("**WHO:** Naya Verity Narzan")
    assert ok and detail == "signed: lead Naya Verity Narzan", detail


# --- w157 (Naya Alpha): Epsilon's quoted-signature hole, #2568 fix ---
# A `>`-quoted line is someone else's words. It must never bind as
# signature, field, evidence, or score — not just identity.

def test_quoted_signature_does_not_bind():
    """Hole: `> Naya Alpha said...` bound as a signature -> silent
    false PASS. Quoted signatures (bare, WHO:, Signed-by, nested,
    indented) never sign."""
    from post_checker import check_identity
    for body in ("> Naya Alpha said the thing works.",
                 "> WHO: Naya Alpha",
                 "> Signed by Naya Alpha",
                 ">> Naya Alpha said it first.",
                 "  > Naya Alpha reporting."):
        ok, detail = check_identity(body)
        assert not ok, (body, detail)


def test_quoted_only_post_flags():
    """A post whose EVERY binding element is quoted must FLAG — before
    this fix it PASSED all four checks."""
    v, findings = check_post(
        """Quoting yesterday's post for reference:
> WHO: Naya Alpha
> NUTSHELL: the thing works.
> WHAT: fixed it. WHY: it was broken.
> EVIDENCE: PR #2568 @ 21f089d5.
> SCORE: 9/10 - ships, verified.
> CONNECTS TO: the mission.
> NEEDS: nothing.
""", level="RECEIPT")
    assert v == "FLAG", describe((v, findings))
    by_name = {n: (ok, d) for n, ok, d in findings}
    assert not by_name["identity"][0], by_name
    assert not by_name["level"][0], by_name
    assert not by_name["evidence"][0], by_name
    assert not by_name["score"][0], by_name


def test_quoted_fields_evidence_score_do_not_bind():
    """Legit unquoted signature + quoted fields/evidence/score must
    FLAG on level/evidence/score — the class fix, not just identity."""
    v, findings = check_post(
        """WHO: Naya Alpha
Quoting the rest for reference:
> NUTSHELL: the thing works.
> WHAT: fixed it. WHY: it was broken.
> EVIDENCE: PR #2568 @ 21f089d5.
> SCORE: 9/10 - ships, verified.
> CONNECTS TO: the mission.
> NEEDS: nothing.
""", level="RECEIPT")
    assert v == "FLAG", describe((v, findings))
    by_name = {n: (ok, d) for n, ok, d in findings}
    assert by_name["identity"][0], by_name  # own signature still binds
    assert not by_name["level"][0], by_name
    assert not by_name["evidence"][0], by_name
    assert not by_name["score"][0], by_name


def test_legit_post_with_quote_block_still_passes():
    """Control: a complete UNQUOTED post that also quotes someone
    else's good post must still PASS — stripping quotes must not
    poison legitimate posts."""
    v, findings = check_post(
        """WHO: Naya Alpha
NUTSHELL: the thing works.
WHAT: fixed it. WHY: it was broken.
EVIDENCE: PR #2568 @ 21f089d5.
SCORE: 9/10 - ships, verified.
CONNECTS TO: the mission.
NEEDS: nothing.
Quoting the prior post for reference:
> WHO: Naya Beta
> SCORE: 10/10 - perfect, ships.
""", level="RECEIPT")
    assert v == "PASS", describe((v, findings))
