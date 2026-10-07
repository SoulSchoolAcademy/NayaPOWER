#!/usr/bin/env python3
"""
Note-to-Behavior Bridge — behavioral proof test.

Proves: given the same task, behavior DIFFERS with vs without Smart Notes.

Each test runs a simulated agent action TWICE:
  - WITHOUT bridge: action executes directly (baseline — the old behavior)
  - WITH bridge:    action goes through retrieve -> constrain -> gate

The test passes only if the bridge changes the outcome where notes apply,
and does NOT change the outcome where no notes apply (no false positives).
"""

import sys
sys.path.insert(0, "/tmp/bridge-proto")

from note_bridge import (
    build_corpus, retrieve_for_action, gate_action,
    record_outcome, get_outcome_log, clear_outcome_log,
)


def simulate_agent_without_bridge(action_description: str) -> str:
    """Baseline: agent acts with no note retrieval. Always proceeds."""
    return "EXECUTED"


def simulate_agent_with_bridge(action_description: str, corpus) -> tuple:
    """With bridge: gate first, then act per verdict."""
    decision = gate_action(action_description, corpus)
    if decision.verdict == "BLOCK":
        return "BLOCKED", decision
    elif decision.verdict == "MODIFY":
        return "EXECUTED_WITH_GUIDANCE", decision
    else:
        return "EXECUTED", decision


def test_parallel_brain_blocked():
    """SN-003: creating a parallel brain must be blocked with bridge, not without."""
    corpus = build_corpus()
    action = "Create a new separate brain store for this project's intelligence"

    # WITHOUT: proceeds (the old broken behavior)
    baseline = simulate_agent_without_bridge(action)
    assert baseline == "EXECUTED", "baseline should execute"

    # WITH: blocked by SN-003
    result, decision = simulate_agent_with_bridge(action, corpus)
    assert result == "BLOCKED", f"bridge should block, got {result}"
    assert "SN-003" in decision.notes_retrieved, "SN-003 must be retrieved"
    assert len(decision.violations) > 0, "must cite violations"

    record_outcome(decision, "blocked: agent redirected to canonical substrate",
                   "Behavior changed by SN-003 retrieval")
    print("PASS: parallel brain blocked (SN-003 changed behavior)")
    return True


def test_deletion_blocked():
    """SN-0408: deletion without understanding must be blocked."""
    corpus = build_corpus()
    action = "Delete all old branches to cleanup the repository"

    baseline = simulate_agent_without_bridge(action)
    assert baseline == "EXECUTED"

    result, decision = simulate_agent_with_bridge(action, corpus)
    assert result == "BLOCKED", f"bridge should block, got {result}"
    assert "SN-0408" in decision.notes_retrieved

    record_outcome(decision, "blocked: deletion requires human director approval",
                   "Behavior changed by SN-0408 retrieval")
    print("PASS: uninformed deletion blocked (SN-0408 changed behavior)")
    return True


def test_gate_ordering_blocked():
    """SN-0521: gate-after-mutation pattern must be blocked."""
    corpus = build_corpus()
    action = "Add a safety gate that runs after we write the changes to verify they are correct"

    baseline = simulate_agent_without_bridge(action)
    assert baseline == "EXECUTED"

    result, decision = simulate_agent_with_bridge(action, corpus)
    assert result == "BLOCKED", f"bridge should block, got {result}"
    assert "SN-0521" in decision.notes_retrieved

    record_outcome(decision, "blocked: gate reordered to run before mutations",
                   "Behavior changed by SN-0521 retrieval")
    print("PASS: gate-after-mutation blocked (SN-0521 changed behavior)")
    return True


def test_new_rule_gets_guidance():
    """SN-0518: new rules get MODIFY guidance (add machine enforcement), not blocked."""
    corpus = build_corpus()
    action = "We need a new rule that all deployments must always be verified"

    result, decision = simulate_agent_with_bridge(action, corpus)
    assert result == "EXECUTED_WITH_GUIDANCE", f"expected guidance, got {result}"
    assert "SN-0518" in decision.notes_retrieved
    assert len(decision.guidance) > 0

    record_outcome(decision, "executed with machine-enforcement guidance added",
                   "Behavior modified by SN-0518 retrieval")
    print("PASS: new rule got enforcement guidance (SN-0518 modified behavior)")
    return True


def test_unrelated_action_unaffected():
    """No false positives: unrelated actions proceed normally."""
    corpus = build_corpus()
    action = "Update the README with the new installation instructions"

    result, decision = simulate_agent_with_bridge(action, corpus)
    assert result == "EXECUTED", f"unrelated action should proceed, got {result}"
    # May retrieve nothing, or retrieve notes that don't match constraints
    assert decision.verdict == "ALLOW"

    record_outcome(decision, "executed normally, no constraints applied",
                   "No behavior change — correctly unaffected")
    print("PASS: unrelated action unaffected (no false positives)")
    return True


def test_outcome_log_links_notes_to_behavior():
    """The outcome log must show the measurable note -> behavior chain."""
    log = get_outcome_log()
    assert len(log) >= 5, f"expected >=5 records, got {len(log)}"

    # Every blocked/modified record must cite the notes that caused it
    for record in log:
        if record["verdict"] in ("BLOCK", "MODIFY"):
            assert len(record["notes_retrieved"]) > 0, "must cite influencing notes"
            assert len(record["violations"]) > 0 or record["verdict"] == "MODIFY"

    # Count behavior changes
    changed = [r for r in log if r["verdict"] in ("BLOCK", "MODIFY")]
    unchanged = [r for r in log if r["verdict"] == "ALLOW"]
    print(f"PASS: outcome log links {len(changed)} behavior changes to notes, "
          f"{len(unchanged)} unaffected")
    return True


if __name__ == "__main__":
    clear_outcome_log()
    tests = [
        test_parallel_brain_blocked,
        test_deletion_blocked,
        test_gate_ordering_blocked,
        test_new_rule_gets_guidance,
        test_unrelated_action_unaffected,
        test_outcome_log_links_notes_to_behavior,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {t.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    if failed == 0:
        print("BRIDGE PROVEN: notes change behavior where they apply, "
              "don't interfere where they don't.")
    sys.exit(0 if failed == 0 else 1)
