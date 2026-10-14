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
