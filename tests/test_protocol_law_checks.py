"""Tests for the Team Naya executable law checks.

Covers all five check modules plus the manifest/gate foundation:
  - tip_freshness.py  (SN-0493)
  - quality_gate.py   (SN-0526)
  - decision_log.py   (SN-0522)
  - scorecard.py      (SN-0523)
  - action_log.py     (SN-0575, SN-DONT-WAIT)

Runnable with plain python3 (no pytest required):
    python3 tests/test_protocol_law_checks.py
Also pytest-compatible (plain assert functions).
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import tip_freshness, quality_gate, decision_log, scorecard, action_log, forward_header_gate  # noqa: E402


def _dims(weight=1 / 7):
    return {d: {"weight": weight, "higher_is_better": True} for d in [
        "objective_alignment", "evidence_strength", "effect_size", "risk",
        "reversibility", "cost_of_inaction", "authority_clearance"]}


def _opt(val):
    return {d: val for d in [
        "objective_alignment", "evidence_strength", "effect_size", "risk",
        "reversibility", "cost_of_inaction", "authority_clearance"]}


# ---------------------------------------------------------------- tip_freshness
def test_tip_freshness_rejects_malformed_sha():
    r = tip_freshness.check({"claimed_sha": "deadbeef"})
    assert r["pass"] is False
    assert any("malformed" in x for x in r["reasons"])


def test_tip_freshness_rejects_missing_sha():
    r = tip_freshness.check({})
    assert r["pass"] is False
    assert any("missing" in x for x in r["reasons"])


def test_tip_freshness_rejects_stale_sha():
    r = tip_freshness.check({"claimed_sha": "0" * 40})
    assert r["pass"] is False
    assert any("STALE" in x for x in r["reasons"])


def test_tip_freshness_accepts_current_tip():
    tip = subprocess.run(["git", "ls-remote", "origin", "main"],
                         capture_output=True, text=True, timeout=30,
                         cwd=ROOT).stdout.split()[0]
    r = tip_freshness.check({"claimed_sha": tip})
    assert r["pass"] is True, r["reasons"]


# ---------------------------------------------------------------- quality_gate
def _good_deliverable(**over):
    rec = {
        "deliverable": "test-widget",
        "build_evidence": "branch naya5/x @ abc123",
        "verification_evidence": "11/11 tests green",
        "scorecard": {"score": 9.2, "scorer": "naya5"},
        "gates": [{"name": "unit", "result": "pass"}],
    }
    rec.update(over)
    return rec


def test_quality_gate_passes_complete_record():
    r = quality_gate.check(_good_deliverable())
    assert r["pass"] is True, r["reasons"]


def test_quality_gate_rejects_missing_build():
    r = quality_gate.check(_good_deliverable(build_evidence=""))
    assert r["pass"] is False


def test_quality_gate_rejects_missing_verification():
    r = quality_gate.check(_good_deliverable(verification_evidence=None))
    assert r["pass"] is False
    assert any("implemented != verified" in x for x in r["reasons"])


def test_quality_gate_rejects_sub_9_score():
    r = quality_gate.check(_good_deliverable(
        scorecard={"score": 8.9, "scorer": "naya5"}))
    assert r["pass"] is False
    assert any("8.9" in x and "9.0" in x for x in r["reasons"])


def test_quality_gate_accepts_exactly_9():
    r = quality_gate.check(_good_deliverable(
        scorecard={"score": 9.0, "scorer": "naya5"}))
    assert r["pass"] is True, r["reasons"]


def test_quality_gate_rejects_anonymous_scorer():
    r = quality_gate.check(_good_deliverable(
        scorecard={"score": 9.5, "scorer": "  "}))
    assert r["pass"] is False


def test_quality_gate_rejects_failing_gate():
    r = quality_gate.check(_good_deliverable(
        gates=[{"name": "unit", "result": "fail"}]))
    assert r["pass"] is False


def test_quality_gate_rejects_empty_gates():
    r = quality_gate.check(_good_deliverable(gates=[]))
    assert r["pass"] is False


# ---------------------------------------------------------------- decision_log
def _good_decision(**over):
    rec = {
        "decision": "pick lane",
        "options": [{"id": "a", "description": "x"}, {"id": "b", "description": "y"}],
        "scores": {"a": 7.5, "b": 8.2},
        "winner": "b",
        "authority": {"admissible": True, "protected_gate_hit": False,
                      "gates_checked": ["GATE-1", "GATE-2", "GATE-3", "GATE-4", "GATE-5"]},
        "decided_at": "2026-10-08T04:00:00Z",
        "decider": "naya5",
    }
    rec.update(over)
    return rec


def test_decision_log_passes_clean_record():
    r = decision_log.check(_good_decision())
    assert r["pass"] is True, r["reasons"]


def test_decision_log_rejects_single_option():
    r = decision_log.check(_good_decision(
        options=[{"id": "a", "description": "x"}],
        scores={"a": 7.5}, winner="a"))
    assert r["pass"] is False


def test_decision_log_rejects_wrong_winner_without_override():
    r = decision_log.check(_good_decision(winner="a"))
    assert r["pass"] is False
    assert any("override_rationale" in x for x in r["reasons"])


def test_decision_log_accepts_override_with_rationale():
    r = decision_log.check(_good_decision(
        winner="a", override_rationale="b scores higher but needs Shawn's gate; a is admissible now"))
    assert r["pass"] is True, r["reasons"]


def test_decision_log_rejects_unchecked_gates():
    rec = _good_decision()
    rec["authority"]["gates_checked"] = ["GATE-1"]
    r = decision_log.check(rec)
    assert r["pass"] is False
    assert any("GATE-5" in x for x in r["reasons"])


def test_decision_log_fail_closed_on_gate_hit():
    rec = _good_decision()
    rec["authority"]["protected_gate_hit"] = True
    r = decision_log.check(rec)
    assert r["pass"] is False
    assert any("fail closed" in x for x in r["reasons"])


def test_decision_log_allows_refusal_on_gate_hit():
    rec = _good_decision(
        options=[{"id": "a", "description": "x"}, {"id": "refuse", "description": "stop"}],
        scores={"a": 8.0, "refuse": 9.0}, winner="refuse")
    rec["authority"]["protected_gate_hit"] = True
    r = decision_log.check(rec)
    assert r["pass"] is True, r["reasons"]


def test_decision_log_rejects_anonymous_decider():
    r = decision_log.check(_good_decision(decider=""))
    assert r["pass"] is False


# ---------------------------------------------------------------- scorecard
def _good_scorecard(**over):
    a = _opt(7)
    b = _opt(8)
    total_a = round(sum((1 / 7) * 7 for _ in range(7)), 6)  # 7.0
    total_b = round(sum((1 / 7) * 8 for _ in range(7)), 6)  # 8.0
    rec = {
        "scorecard_for": "lane pick",
        "dimensions": _dims(),
        "options": {"a": a, "b": b},
        "claimed_totals": {"a": total_a, "b": total_b},
        "claimed_winner": "b",
        "scorer": "naya5",
    }
    rec.update(over)
    return rec


def test_scorecard_passes_clean_record():
    r = scorecard.check(_good_scorecard())
    assert r["pass"] is True, r["reasons"]


def test_scorecard_rejects_missing_dimension():
    dims = _dims()
    del dims["risk"]
    r = scorecard.check(_good_scorecard(dimensions=dims))
    assert r["pass"] is False
    assert any("risk" in x for x in r["reasons"])


def test_scorecard_rejects_bad_weight_sum():
    dims = _dims(weight=0.2)  # sums to 1.4
    r = scorecard.check(_good_scorecard(dimensions=dims))
    assert r["pass"] is False
    assert any("1.0" in x for x in r["reasons"])


def test_scorecard_rejects_out_of_range_score():
    rec = _good_scorecard()
    rec["options"]["a"]["risk"] = 11
    r = scorecard.check(rec)
    assert r["pass"] is False


def test_scorecard_catches_arithmetic_fraud():
    rec = _good_scorecard()
    rec["claimed_totals"] = {"a": 9.9, "b": 9.8}  # fabricated
    r = scorecard.check(rec)
    assert r["pass"] is False
    assert any("recomputed" in x for x in r["reasons"])


def test_scorecard_rejects_wrong_winner():
    r = scorecard.check(_good_scorecard(claimed_winner="a"))
    assert r["pass"] is False
    assert any("math decides" in x for x in r["reasons"])


# ---------------------------------------------------------------- action_log
def _good_action(**over):
    rec = {
        "action": "fixed null pointer",
        "kind": "repair",
        "what_was_broken": "crash on empty input",
        "authority_basis": "SN-0575",
        "what_was_done": "added empty guard",
        "verification": "repro test now passes",
        "reported_to": "#1354",
        "protected_gate_touched": False,
    }
    rec.update(over)
    return rec


def test_action_log_passes_repair():
    r = action_log.check(_good_action())
    assert r["pass"] is True, r["reasons"]


def test_action_log_rejects_missing_verification():
    r = action_log.check(_good_action(verification=""))
    assert r["pass"] is False


def test_action_log_rejects_missing_report():
    r = action_log.check(_good_action(reported_to=""))
    assert r["pass"] is False
    assert any("report" in x.lower() for x in r["reasons"])


def test_action_log_hard_fail_gate_without_approval():
    r = action_log.check(_good_action(protected_gate_touched=True))
    assert r["pass"] is False
    assert any("HARD FAIL" in x for x in r["reasons"])


def test_action_log_passes_gate_with_approval():
    r = action_log.check(_good_action(
        protected_gate_touched=True, shawn_approval="2026-10-08: go"))
    assert r["pass"] is True, r["reasons"]


def test_action_log_takeover_requires_owner_notified():
    r = action_log.check(_good_action(
        kind="takeover", original_owner="naya4",
        stall_evidence="no activity 48h", owner_notified=False))
    assert r["pass"] is False


def test_action_log_takeover_requires_stall_evidence():
    r = action_log.check(_good_action(
        kind="takeover", original_owner="naya4", owner_notified=True,
        stall_evidence=""))
    assert r["pass"] is False
    assert any("ACTIVE work" in x for x in r["reasons"])


def test_action_log_passes_clean_takeover():
    r = action_log.check(_good_action(
        kind="takeover", original_owner="naya4", owner_notified=True,
        stall_evidence="no feed activity in 48h; blocker flagged with no response"))
    assert r["pass"] is True, r["reasons"]


# ---------------------------------------------------------------- forward_header_gate
# Fixtures are VERBATIM tonight headers with real comment IDs (the 04:40Z
# compounding audit's NOT-COMPOUNDED class: ~71 forward-dated headers since
# 00:00Z, 8 post-law).

def _header(claim_text, posted_at, source_ref="lane-fixture"):
    return forward_header_gate.check(
        {"claim_text": claim_text, "posted_at": posted_at,
         "source_ref": source_ref})


def test_forward_header_gate_rejects_2min_forward_dated_scorecard():
    # comment 6117821928: "## [Naya 5 | BUILDER | scorecard 2026-10-12 04:38 UTC]"
    # posted 2026-10-12T04:35:28Z (~152s early)
    r = _header("## [Naya 5 | BUILDER | scorecard 2026-10-12 04:38 UTC]\nLayer 4 final fix",
                "2026-10-12T04:35:28Z", "lane-1713:6117821928")
    assert r["pass"] is False, r["reasons"]
    assert r["details"]["offenders"][0]["drift_seconds"] == 152


def test_forward_header_gate_rejects_10min_forward_dated_signout():
    # comment 6117884246: "[NAYA 5] SIGN-OUT ... Naya Mu (Human Value) -
    # 2026-10-12 ~04:52 UTC" posted 2026-10-12T04:42:18Z (~582s early)
    r = _header("[NAYA 5] SIGN-OUT - gamma lane #1715 - Naya Mu (Human Value) - "
                "2026-10-12 ~04:52 UTC",
                "2026-10-12T04:42:18Z", "lane-1715:6117884246")
    assert r["pass"] is False, r["reasons"]
    assert r["details"]["offenders"][0]["drift_seconds"] == 582


def test_forward_header_gate_rejects_12min_forward_dated_signout():
    # comment 6117864326: "## [Naya 5 · VALIDATOR | sign-out 2026-10-12 04:52 UTC]"
    # posted 2026-10-12T04:40:06Z (~714s early)
    r = _header("## [Naya 5 · VALIDATOR | sign-out 2026-10-12 04:52 UTC] "
                "Layer 2 fix-pass #4",
                "2026-10-12T04:40:06Z", "lane-1714:6117864326")
    assert r["pass"] is False, r["reasons"]
    assert r["details"]["offenders"][0]["drift_seconds"] == 714


def test_forward_header_gate_rejects_no_date_prefix_time():
    # "04:42 UTC" header posted at 04:33:33Z (5th/6th instance, 04:42Z pass)
    # -> ~507s early. No date prefix: anchored to the post's date.
    r = _header("[naya5-iv2-intent-parser | SIGN-OUT 04:42 UTC] Layer 2 fix-pass",
                "2026-10-12T04:33:33Z")
    assert r["pass"] is False, r["reasons"]
    assert r["details"]["offenders"][0]["drift_seconds"] == 507


def test_forward_header_gate_rejects_z_suffixed_time():
    # "~03:10Z" posted 02:36:16Z -> ~2024s early
    r = _header("## [SIGN-OUT ~03:10Z] freshness check complete",
                "2026-10-12T02:36:16Z")
    assert r["pass"] is False, r["reasons"]


def test_forward_header_gate_accepts_honest_second_level_roundup():
    # comment 6117945693: "**[NAYA · VALIDATOR | sign-in 2026-10-12 04:49 UTC]**"
    # posted 2026-10-12T04:48:48Z — 12s early, within the 60s grace -> PASS
    r = _header("**[NAYA · VALIDATOR | sign-in 2026-10-12 04:49 UTC]** Final IV",
                "2026-10-12T04:48:48Z", "lane-1715:6117945693")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_accepts_same_minute_header():
    # comment 6117829250: "~04:36 UTC" posted 04:36:15Z — header minute is in
    # the past relative to posting -> PASS (past-dating is out of scope)
    r = _header("**[NAYA · VALIDATOR | sign-in 2026-10-12 ~04:36 UTC]** Final delta",
                "2026-10-12T04:36:15Z", "lane-1715:6117829250")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_accepts_header_without_timestamp():
    r = _header("[STAND-DOWN] superseded mission, no further work",
                "2026-10-12T04:50:05Z")
    assert r["pass"] is True, r["reasons"]
    assert "does not apply" in r["reasons"][0]


def test_forward_header_gate_ignores_bare_time_without_tz_marker():
    # "04:52" with no UTC/Z marker: timezone unknown, gate refuses to guess.
    r = _header("[sign-in 04:52] starting work", "2026-10-12T04:50:05Z")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_midnight_boundary_wrap():
    # "23:58 UTC" posted at 00:03Z is yesterday's 23:58, not a future claim.
    r = _header("## SIGN-OUT 23:58 UTC — work complete", "2026-10-12T00:03:00Z")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_grace_boundary_60s_passes():
    r = _header("[SIGN-IN 04:53 UTC]", "2026-10-12T04:52:00Z")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_grace_boundary_61s_fails():
    r = _header("[SIGN-IN 04:53 UTC]", "2026-10-12T04:51:59Z")
    assert r["pass"] is False, r["reasons"]
    assert r["details"]["offenders"][0]["drift_seconds"] == 61


def test_forward_header_gate_ignores_timestamp_beyond_five_lines():
    # A future time mentioned deeper in the body is not a header claim
    # (documented limit).
    body = "\n".join(["[SIGN-OUT] done"] + [""] * 5 +
                     ["The next check runs at 2026-10-12 09:00 UTC."])
    r = _header(body, "2026-10-12T04:50:05Z")
    assert r["pass"] is True, r["reasons"]


def test_forward_header_gate_quotes_offender_in_details():
    r = _header("## [Naya 5 | BUILDER | scorecard 2026-10-12 04:38 UTC]",
                "2026-10-12T04:35:28Z", "lane-1713:6117821928")
    assert r["pass"] is False
    assert r["details"]["offenders"][0]["line"] == 1
    assert "04:38 UTC" in r["details"]["offenders"][0]["quote"]
    assert "152" in r["reasons"][0]


def test_forward_header_gate_fail_closed_on_missing_posted_at():
    r = forward_header_gate.check({"claim_text": "[SIGN-IN 04:52 UTC]"})
    assert r["pass"] is False
    assert "posted_at" in r["reasons"][0]


def test_forward_header_gate_fail_closed_on_empty_claim():
    r = forward_header_gate.check({"claim_text": "  ",
                                   "posted_at": "2026-10-12T04:52:00Z"})
    assert r["pass"] is False


def test_forward_header_gate_fail_closed_on_nul_bytes():
    r = _header("[SIGN-IN 04:52 UTC]\x00hidden", "2026-10-12T04:52:00Z")
    assert r["pass"] is False


def test_forward_header_gate_fail_closed_on_bad_posted_at():
    r = _header("[SIGN-IN 04:52 UTC]", "not-a-timestamp")
    assert r["pass"] is False
    assert "posted_at" in r["reasons"][0]


# ---------------------------------------------------------------- runner
def main() -> int:
    fns = sorted((n, f) for n, f in globals().items()
                 if n.startswith("test_") and callable(f))
    failures = []
    for name, fn in fns:
        try:
            fn()
            print(f"  ok {name}")
        except AssertionError as e:
            failures.append(name)
            print(f"  FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - len(failures)}/{len(fns)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
