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

from checks import tip_freshness, quality_gate, decision_log, scorecard, action_log  # noqa: E402


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
