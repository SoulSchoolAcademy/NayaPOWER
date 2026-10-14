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
    # R-LIMIT-A (w131): bare prose with tokens after the name is a
    # mention, not a signature — supersedes the old binding assertion.
    assert not ok and "unbound" in detail, detail


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


# --- #2568 fix-pass (Naya Mu, w127): Theta's residuals R1–R5 + E2E ---

def test_mention_before_who_does_not_steal_signature():
    """R1: a mention line ABOVE the WHO line must not steal the
    signature — explicit signature lines take precedence in any order."""
    from post_checker import check_identity
    ok, detail = check_identity(
        "Naya Verity Narzan was quoted above.\nWHO: Naya Mu")
    assert ok and detail == "signed: Naya Mu", detail
    ok, detail = check_identity("Naya 5 did great work.\nWHO: Naya Kappa")
    assert ok and detail == "signed: Naya Kappa", detail
    ok, detail = check_identity(
        "WHO: Naya Mu\nThanks to Naya Verity Narzan.")
    assert ok and detail == "signed: Naya Mu", detail


def test_explicit_line_with_no_name_leaves_identity_unbound():
    """R1 guard: when a WHO line exists but names nobody, a bare
    name-leading line below it must not override the WHO claim."""
    from post_checker import check_identity
    ok, detail = check_identity("WHO: TBD\nNaya Verity Narzan was quoted.")
    assert not ok and "unbound" in detail, detail


def test_bare_lead_plus_punctuation_flagged():
    """R2: a bare lead name plus one punctuation mark is incomplete —
    leads sign with the family name. The leader-prefix branch must run
    before the roster loop, so no punctuation variant falls through."""
    from post_checker import check_identity
    for punct in (".", ";", "!", "?"):
        ok, detail = check_identity(f"WHO: Naya Clarity{punct}\nMISSION: x")
        assert not ok and "Narzan" in detail, (punct, detail)
    # A comma-attached second name is not an agent named "Naya".
    ok, detail = check_identity("WHO: Naya Clarity, Naya Mu\nMISSION: x")
    assert not ok and "incomplete identity" in detail, detail


def test_prose_sentences_with_colons_fail_pulse():
    """R3: prose sentences that start with a field word plus a clause
    plus a colon are prose, not fields — only the separator, an
    `-> ...` suffix, or a `TO` suffix may intervene."""
    from post_checker import check_level
    prose = (
        "WHO are we to judge this: nobody.\n"
        "MISSION is what we do here: work.\n"
        "STATUS of the day is fine: calm.\n"
        "TRUTH is hard to find: still.\n"
        "SCORE of the game was high: nine.\n"
        "BLOCKER in the way was small: pebble.\n"
        "NEXT in line is waiting: patient.\n"
        "SOURCE of the story is old: legend."
    )
    ok, detail = check_level(prose, "PULSE")
    assert not ok, detail
    assert "WHO" in detail and "MISSION" in detail, detail


def test_hyphenated_meaning_word_not_score_meaning():
    """R4: a hyphen-joined meaning word ('held-out') is not score
    meaning — the guard covers ASCII hyphen and Unicode dashes."""
    from post_checker import check_score
    ok, detail = check_score("SCORE: 8/10\nHeld-out test set used.")
    assert not ok and "meaning unstated" in detail, detail
    ok, detail = check_score("SCORE: 8/10\nHeld\u2013out test set used.")
    assert not ok and "meaning unstated" in detail, detail
    ok, detail = check_score("SCORE: 8/10 — ships after one more pass.")
    assert ok, detail


def test_overlong_issue_ref_not_evidence():
    """R5: `#123456` is not a `#NNNNN` ref — REF_RE must not match a
    5-digit prefix of a longer number."""
    from post_checker import check_evidence
    ok, detail = check_evidence("EVIDENCE: see #123456.")
    assert not ok, detail
    ok, detail = check_evidence("EVIDENCE: see #12345.")
    assert ok, detail


def test_adversarial_combo_flags():
    """E2E: R1 + R3 + anchored tip + ships-verb combined must FLAG —
    the residuals compound, so the fix must close them together."""
    e2e = (
        "Naya Verity Narzan was quoted above.\n"
        "WHO are we to judge this: nobody.\n"
        "MISSION is what we do here: work.\n"
        "STATUS of the day is fine: calm.\n"
        "TRUTH is hard to find: still.\n"
        "SCORE of the game was high: nine.\n"
        "BLOCKER in the way was small: pebble.\n"
        "NEXT in line is waiting: patient.\n"
        "SOURCE of the story is old: legend.\n"
        "SOURCE: tip 1234567.\n"
        "SCORE: 9/10 — the shipment ships tomorrow.\n"
    )
    v, findings = check_post(e2e, level="PULSE")
    assert v == "FLAG", describe((v, findings))
    # The FLAG comes from the level gate: the prose sentences are not
    # fields. Identity is UNBOUND here under R-LIMIT-A (w131): the post
    # carries NO eligible explicit WHO:/Signed:/By: line at all, and
    # no eligible line is exactly a name — the first line is mention
    # prose, so the bare fallback does not bind. A post WITH a WHO
    # line always resolves to it (R1).
    assert any(n == "level" and not ok for n, ok, _ in findings)


# --- R-LIMIT-A (Naya Alpha, w129 decision; Naya Theta, w131 fix-pass) ---

def test_limit_a_bare_prose_does_not_bind():
    """R-LIMIT-A pass 2: a bare line with ANY token after the name is
    prose, not a signature — it must not bind, and scanning continues."""
    from post_checker import check_identity
    for body in (
        "Naya Verity Narzan was quoted above.",      # L1 mention-prose
        "Naya Mu: shipped the fix",                   # L3 name + colon + prose
        "Naya Mu and Naya Kappa shipped it",          # L9 multi-name prose
        "Naya Mu, Naya Kappa",                        # L10 multi-name comma
        "Naya Mu (lane 1)",                           # L12 name + qualifier
        "Naya Clarity Verity reporting",              # L13 bare prose (supersedes
        # the old test_leader_agent_name_recognized 'reporting' assertion)
    ):
        ok, detail = check_identity(body)
        assert not ok and "unbound" in detail, (body, detail)


def test_limit_a_quoted_lines_never_bind():
    """R-LIMIT-A eligibility: lines starting with '>' are quotes — they
    never bind in either pass, bare or explicit."""
    from post_checker import check_identity
    for body in (
        "> Naya Verity Narzan was quoted above.",     # L5 quoted prose
        "> Naya Mu",                                  # L6 quoted bare name
        "> WHO: Naya Mu",                             # L14 quoted explicit
    ):
        ok, detail = check_identity(body)
        assert not ok and "unbound" in detail, (body, detail)


def test_limit_a_fenced_lines_never_bind():
    """R-LIMIT-A eligibility: lines inside fenced code blocks (``` / ~~~,
    with or without info string, unclosed swallows to EOF) never bind."""
    from post_checker import check_identity
    for body in (
        "```\nNaya Mu\n```",                          # L7 fenced bare
        "```\nNaya Verity Narzan was quoted.\n```",   # L8 fenced prose
        "~~~\nNaya Mu\n~~~",                          # L15 tilde fence
        "```text\nNaya Mu\n```",                      # L19 info string
        "```\nNaya Mu",                               # L20 unclosed fence
        "```\nWHO: Naya Mu\n```",                     # L25 fenced explicit
    ):
        ok, detail = check_identity(body)
        assert not ok and "unbound" in detail, (body, detail)


def test_limit_a_bare_name_only_still_binds():
    """R-LIMIT-A pass 2 preserves legitimate bare sign-offs: after
    marker-stripping, EXACTLY a name + trailing punctuation binds."""
    from post_checker import check_identity
    for body in (
        "\u2014 Naya Mu",                             # L2 em-dash sign-off
        "Naya Mu:",                                   # L4 name + colon only
        "Naya Mu \u2014",                             # L11 name + trailing dash
        "Naya Mu\nSaw Naya Verity Narzan.",           # L17 name-only + mention
        "**Naya Mu**",                                # L18 bold name-only
        "Naya Mu\n\nThanks to Naya Verity Narzan.",   # L23 name-only first
        "Naya Mu\n```\nNaya Verity Narzan\n```",      # L24 name-only, fenced later
        "Thanks to everyone.\nNaya Mu",               # L26 name-only last
    ):
        ok, detail = check_identity(body)
        assert ok and detail == "signed: Naya Mu", (body, detail)


def test_limit_a_explicit_forms_all_bind():
    """R-LIMIT-A pass 1: the explicit recognizer covers EVERY documented
    signature form — plain / dash / TO / arrow+label+colon / Signed(:) / By."""
    from post_checker import check_identity
    for body in (
        "WHO: Naya Mu",                               # L21 plain
        "WHO - Naya Mu",                              # G7 dash
        "WHO TO: Naya Mu",                            # G2 TO form
        "WHO -> SIGNER: Naya Mu",                     # G1' arrow + label
        "WHO \u2192 SIGNER: Naya Mu",                 # G4' unicode arrow + label
        "WHO -> Lane 1: Naya Mu",                     # G8 arrow, multiword label
        "Signed: Naya Mu",                            # G3 Signed-colon
        "Signed by Naya Mu",                          # G6 Signed-by
        "By: Naya Mu",                                # G5 By-colon
    ):
        ok, detail = check_identity(body)
        assert ok and detail == "signed: Naya Mu", (body, detail)


def test_limit_a_arrow_without_separator_stays_unbound():
    """Precedence pin: 'WHO -> Naya Mu' has NO second separator, so the
    arrow form does not match; the dash reading leaves '> Naya Mu', which
    resolves to no candidate — unbound. Same for unicode arrow without
    separator (not a WHO field at all). Neither is a signature."""
    from post_checker import check_identity
    for body in ("WHO -> Naya Mu", "WHO \u2192 Naya Mu"):
        ok, detail = check_identity(body)
        assert not ok and "unbound" in detail, (body, detail)


def test_limit_a_explicit_seen_without_name_stays_unbound():
    """Preserved Mu guard: an explicit line naming nobody leaves identity
    unbound — bare lines never override an explicit claim."""
    from post_checker import check_identity
    ok, detail = check_identity("WHO: TBD\nNaya Verity Narzan was quoted.")
    assert not ok and "unbound" in detail, detail
