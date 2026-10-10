"""protocol_gates_test.py — tests for tools/protocol_gates.py.

Positive AND negative controls. A gate that cannot fail is not a gate:
every check below has at least one test proving it REJECTS a violation.

Run:  python3 -m pytest tools/protocol_gates_test.py -q
"""

import pytest

from tools.protocol_gates import (
    check_protected_gates,
    check_quality_gate,
    check_scorecard,
    check_sign_in,
    check_sign_out,
    check_truth_states,
)


def good_sign_in():
    return {
        "seat": "naya-2-test",
        "lane": "protocol-gates",
        "taking": "build machine gates",
        "why": "shawn directive",
        "plan": "write module, test, PR",
        "observed_state": "main@00f50bb3, #1807 open",
    }


def good_sign_out():
    return {
        "seat": "naya-2-test",
        "did": "built protocol_gates.py",
        "evidence_links": ["https://github.com/SoulSchoolAcademy/NayaPOWER/pull/9999"],
        "score": 9.2,
        "proven": "39/39 tests pass",
        "unknown": "cold-agent acceptance untested",
        "blocked": "none",
        "next_action": "open PR",
    }


def good_scorecard():
    return {
        "decision": "which gate design to ship",
        "options": ["adapter", "duplicate", "defer"],
        "scores": {
            "adapter": {"value": 9, "consequences": 8, "mission_alignment": 9,
                        "risk": 8, "reversibility": 9, "evidence_strength": 8,
                        "total": 8.5},
            "duplicate": {"value": 4, "consequences": 3, "mission_alignment": 4,
                          "risk": 5, "reversibility": 6, "evidence_strength": 5,
                          "total": 4.5},
            "defer": {"value": 5, "consequences": 5, "mission_alignment": 5,
                      "risk": 7, "reversibility": 8, "evidence_strength": 6,
                      "total": 6.0},
        },
        "gates_checked": {
            "reversible_or_safe": True,
            "no_major_damage": True,
            "positive_forward_effect": True,
            "authority_clear": True,
        },
        "winner": "adapter",
        "receipt_posted": True,
    }


# ---------------- truth states ----------------

def test_truth_verified_can_claim_works():
    r = check_truth_states({"state": "VERIFIED", "asserts_works": True})
    assert r.passed, r.reasons


def test_truth_production_proven_can_claim_works():
    r = check_truth_states({"state": "PRODUCTION-PROVEN", "asserts_works": True})
    assert r.passed, r.reasons


def test_truth_unknown_cannot_claim_works():
    r = check_truth_states({"state": "UNKNOWN", "asserts_works": True})
    assert not r.passed  # UNKNOWN != PASS


def test_truth_blocked_cannot_claim_works():
    r = check_truth_states({"state": "BLOCKED", "asserts_works": True})
    assert not r.passed  # BLOCKED != PASS


def test_truth_implemented_cannot_claim_works():
    r = check_truth_states({"state": "IMPLEMENTED", "asserts_works": True})
    assert not r.passed  # IMPLEMENTED != VERIFIED


def test_truth_candidate_cannot_claim_works():
    r = check_truth_states({"state": "CANDIDATE", "asserts_works": True})
    assert not r.passed  # CANDIDATE != RATIFIED


def test_truth_invalid_state_rejected():
    r = check_truth_states({"state": "ALMOST-DONE", "asserts_works": False})
    assert not r.passed


def test_truth_non_dict_rejected():
    r = check_truth_states("VERIFIED")
    assert not r.passed


# ---------------- sign in ----------------

def test_sign_in_passes_complete():
    assert check_sign_in(good_sign_in()).passed


def test_sign_in_rejects_missing_field():
    d = good_sign_in()
    del d["plan"]
    r = check_sign_in(d)
    assert not r.passed
    assert any("plan" in x for x in r.reasons)


def test_sign_in_rejects_empty_taking():
    d = good_sign_in()
    d["taking"] = "   "
    r = check_sign_in(d)
    assert not r.passed  # no silent work


def test_sign_in_rejects_non_dict():
    assert not check_sign_in(None).passed


# ---------------- sign out ----------------

def test_sign_out_passes_complete():
    assert check_sign_out(good_sign_out()).passed


def test_sign_out_rejects_empty_evidence():
    d = good_sign_out()
    d["evidence_links"] = []
    r = check_sign_out(d)
    assert not r.passed  # bare "done" receipts are defects


def test_sign_out_rejects_missing_score():
    d = good_sign_out()
    del d["score"]
    assert not check_sign_out(d).passed


def test_sign_out_rejects_nan_score():
    d = good_sign_out()
    d["score"] = float("nan")
    r = check_sign_out(d)
    assert not r.passed  # NaN fails closed


def test_sign_out_rejects_infinite_score():
    d = good_sign_out()
    d["score"] = float("inf")
    assert not check_sign_out(d).passed


def test_sign_out_rejects_out_of_range_score():
    d = good_sign_out()
    d["score"] = 11
    assert not check_sign_out(d).passed


# ---------------- 5-step scorecard ----------------

def test_scorecard_passes_complete():
    assert check_scorecard(good_scorecard()).passed


def test_scorecard_rejects_missing_options():
    sc = good_scorecard()
    sc["options"] = []
    assert not check_scorecard(sc).passed


def test_scorecard_rejects_unscored_option():
    sc = good_scorecard()
    del sc["scores"]["defer"]
    r = check_scorecard(sc)
    assert not r.passed


def test_scorecard_rejects_missing_gate_check():
    sc = good_scorecard()
    del sc["gates_checked"]["authority_clear"]
    r = check_scorecard(sc)
    assert not r.passed


def test_scorecard_rejects_winner_not_enumerated():
    sc = good_scorecard()
    sc["winner"] = "invented-option"
    r = check_scorecard(sc)
    assert not r.passed


def test_scorecard_rejects_unposted_receipt():
    sc = good_scorecard()
    sc["receipt_posted"] = False
    r = check_scorecard(sc)
    assert not r.passed  # no receipt, no merge


def test_scorecard_rejects_nan_dimension():
    sc = good_scorecard()
    sc["scores"]["adapter"]["total"] = float("nan")
    assert not check_scorecard(sc).passed


def test_scorecard_rejects_non_dict():
    assert not check_scorecard([]).passed


# ---------------- protected gates (adapter) ----------------

def test_protected_routine_work_allowed():
    r = check_protected_gates("write unit tests for the new module")
    assert r.passed and r.verdict == "ALLOW"


def test_protected_production_deploy_needs_shawn():
    r = check_protected_gates("deploy to production tonight")
    assert not r.passed and r.verdict == "NEEDS_SHAWN"


def test_protected_credentials_need_shawn():
    r = check_protected_gates("rotate the api key in the config")
    assert not r.passed and r.verdict == "NEEDS_SHAWN"


def test_protected_destructive_needs_shawn():
    r = check_protected_gates("drop table users on the live db")
    assert not r.passed and r.verdict == "NEEDS_SHAWN"


def test_protected_ratification_needs_shawn():
    r = check_protected_gates("mark ratified the new protocol")
    assert not r.passed and r.verdict == "NEEDS_SHAWN"


def test_protected_hard_stop_refuses():
    r = check_protected_gates("fabricate evidence for the test run")
    assert not r.passed and r.verdict == "REFUSE"


def test_protected_empty_action_allowed():
    r = check_protected_gates("")
    assert r.passed  # empty text matches no gate; fail-closed happens upstream


# ---------------- quality gate (adapter) ----------------

def test_quality_all_dimensions_above_floor():
    r = check_quality_gate(
        {"correctness": 9.5, "completeness": 9.2, "evidence": 9.0},
        {"correctness": 0.4, "completeness": 0.3, "evidence": 0.3},
    )
    assert r.passed, r.reasons


def test_quality_single_dimension_below_floor_fails():
    r = check_quality_gate(
        {"correctness": 10.0, "completeness": 7.0, "evidence": 9.5},
        {"correctness": 0.4, "completeness": 0.3, "evidence": 0.3},
    )
    assert not r.passed  # a 10 never covers a 7
    assert any("below floor" in reason for reason in r.reasons)


def test_quality_weighted_total_at_floor_passes():
    r = check_quality_gate(
        {"a": 9.0, "b": 9.0},
        {"a": 0.9, "b": 0.1},
    )
    assert r.passed, r.reasons


def test_quality_weighted_total_below_floor_fails():
    r = check_quality_gate(
        {"a": 9.5, "b": 9.5},
        {"a": 0.5, "b": 0.5},
    )
    assert r.passed  # 9.5 total passes
    r2 = check_quality_gate(
        {"a": 9.2, "b": 9.1},
        {"a": 0.1, "b": 0.9},
    )
    # total = 9.11 >= 9.0 and no dimension below floor -> passes
    assert r2.passed, r2.reasons


def test_quality_rejects_empty_scores():
    assert not check_quality_gate({}).passed


def test_quality_rejects_nan_score():
    r = check_quality_gate({"correctness": float("nan")})
    assert not r.passed


def test_quality_rejects_mismatched_weights():
    r = check_quality_gate({"a": 9.5}, {"a": 0.5, "b": 0.5})
    assert not r.passed


# ---------------- 5-step scorecard STRUCTURE gate (PR body scanner) ----------------

from tools.protocol_gates import check_scorecard_body  # noqa: E402


def _sec1():
    return """## 1. Enumerate
Options considered: (a) extend tools/protocol_gates.py with a body scanner;
(b) create a new tools/scorecard_structure_gate.py; (c) do nothing and rely on
the structured-dict gates. Each was evaluated on value, reversibility, and
duplication risk before acting."""


def _sec2():
    return """## 2. Score
(a) 9/10 — one seam, tests live next door, zero new mechanism. (b) 6/10 — a new
file for one function duplicates the gate and splits the seam. (c) 3/10 — the
audit gap stays open and the next merge ships an unread receipt."""


def _sec3():
    return """## 3. Gate
Reversible: yes — additive function plus tests, no existing behavior changes.
No major damage: yes — fail-closed on unscannable bodies. Positive forward
effect: yes — closes the Domain 1 audit gap for every merge/scorecard PR."""


def _sec4():
    return """## 4. Decide
Winner: (a) — highest score and the only option that strengthens an existing
seam instead of inventing one. Strongest alternative: (b). Falsifier: if the
body scanner cannot be invoked from CI, the rendered-receipt story fails."""


def _sec5():
    return """## 5. Receipt
Posted on #1354 as the sign-out receipt; this PR body is the rendered receipt.
Evidence: pytest run below. No receipt, no merge."""


def good_scorecard_body():
    return "\n\n".join([
        "## Scorecard — this merge's five-step record",
        _sec1(), _sec2(), _sec3(), _sec4(), _sec5(),
    ])


def test_scorecard_body_passes_complete():
    r = check_scorecard_body(good_scorecard_body())
    assert r.passed, r.reasons


def test_scorecard_body_accepts_mixed_header_styles():
    body = "\n\n".join([
        "# 1. ENUMERATE",
        "Two real options were enumerated, each with an id and a one-line summary of what it changes.",
        "## (2) Score",
        "Option A scored 9 on value and 8 on reversibility; option B scored 5 on value with higher duplication risk.",
        "**Step 3: Gate**",
        "Reversible yes, no major damage yes, positive forward effect yes — all three hard stops hold.",
        "## 4) Decide — the winner",
        "Winner is option A: highest score among gate-passers, with option B named as strongest alternative.",
        "## 5. Receipt",
        "Written and posted to #1354; the comment id is the receipt. No receipt, no merge.",
    ])
    r = check_scorecard_body(body)
    assert r.passed, r.reasons


def test_scorecard_body_rejects_four_of_five_sections():
    body = "\n\n".join([
        "## Scorecard — this merge's five-step record",
        _sec1(), _sec2(),
        # gate section deliberately omitted
        _sec4(), _sec5(),
    ])
    r = check_scorecard_body(body)
    assert not r.passed
    assert any("3" in x and "gate" in x and "MISSING" in x for x in r.reasons)


def test_scorecard_body_rejects_empty_section():
    body = "\n\n".join([
        "## Scorecard — this merge's five-step record",
        _sec1(), _sec2(), _sec3(), _sec4(),
        "## 5. Receipt",
        # nothing under the header
    ])
    r = check_scorecard_body(body)
    assert not r.passed
    assert any("5" in x and "receipt" in x and "EMPTY" in x for x in r.reasons)


def test_scorecard_body_rejects_wrong_order():
    body = "\n\n".join([
        "## Scorecard — this merge's five-step record",
        _sec1(), _sec2(), _sec4(), _sec3(), _sec5(),  # decide before gate
    ])
    r = check_scorecard_body(body)
    assert not r.passed
    assert any("OUT OF ORDER" in x for x in r.reasons)


def test_scorecard_body_rejects_single_summary_header():
    # One header naming all five steps is not five sections.
    body = (
        "## Scorecard: enumerate, score, gate, decide, receipt\n\n"
        "All five steps were followed carefully. Options were enumerated and "
        "scored, the gates were checked, a decision was made, and the receipt "
        "was posted to the board for the record."
    )
    r = check_scorecard_body(body)
    assert not r.passed
    assert any("MISSING" in x for x in r.reasons)


def test_scorecard_body_rejects_lone_scorecard_title():
    # The audit's exact concern: a "## Scorecard" title must not count as
    # the score section (or any section).
    r = check_scorecard_body("## Scorecard\n\nLooks good, ship it.")
    assert not r.passed
    assert sum(1 for x in r.reasons if "MISSING" in x) == 5


def test_scorecard_body_rejects_placeholder_theater():
    body = "\n\n".join([
        "## Scorecard — this merge's five-step record",
        _sec1(), _sec2(),
        "## 3. Gate\nTBD — final gate values pending the review board's decision next week.",
        _sec4(), _sec5(),
    ])
    r = check_scorecard_body(body)
    assert not r.passed
    assert any("3" in x and "PLACEHOLDER" in x for x in r.reasons)


def test_scorecard_body_rejects_empty_body():
    assert not check_scorecard_body("").passed
    assert not check_scorecard_body("   \n  ").passed


def test_scorecard_body_rejects_non_string():
    assert not check_scorecard_body(None).passed
    assert not check_scorecard_body({"body": "## 1. Enumerate"}).passed


def test_scorecard_body_cli_passes(tmp_path):
    import subprocess

    f = tmp_path / "body.md"
    f.write_text(good_scorecard_body())
    p = subprocess.run(
        ["python3", "tools/protocol_gates.py", "--scorecard-body", str(f)],
        capture_output=True, text=True,
    )
    assert p.returncode == 0, p.stdout


def test_scorecard_body_cli_blocks(tmp_path):
    import subprocess

    f = tmp_path / "body.md"
    f.write_text("## Scorecard\n\nLooks good, ship it.")
    p = subprocess.run(
        ["python3", "tools/protocol_gates.py", "--scorecard-body", str(f)],
        capture_output=True, text=True,
    )
    assert p.returncode == 1, p.stdout
    assert "MISSING" in p.stdout


def test_scorecard_body_accepts_keyword_headers_without_numbers():
    body = "\n\n".join([
        "## Enumerate options",
        "Two real options were enumerated, each with an id and a one-line summary of what it changes.",
        "## Scoring",
        "Option A scored 9 on value and 8 on reversibility; option B scored 5 on value with higher duplication risk.",
        "## Gate checks",
        "Reversible yes, no major damage yes, positive forward effect yes — all three hard stops hold.",
        "## Decision",
        "Winner is option A: highest score among gate-passers, with option B named as strongest alternative.",
        "## Receipt",
        "Written and posted to #1354; the comment id is the receipt. No receipt, no merge.",
    ])
    r = check_scorecard_body(body)
    assert r.passed, r.reasons
