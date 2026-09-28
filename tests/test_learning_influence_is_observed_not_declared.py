"""RED tests for the learning-influence contract.

The current `nayanet-cold-runtime-proof` mode `learning-influence` does not
measure behavior. It INSERTS two execution receipts whose `observed_result` is a
hardcoded string, then reports `behavioral_change: true` and
`behavioral_delta: { changed: true }` as literals. No Naya executes anything, so
there is nothing to observe and no difference that was actually produced.

These tests encode what must be true instead. They fail against the current
implementation by design. Do not weaken them to make the suite green.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts"


def source() -> str:
    return RUNTIME.read_text(encoding="utf-8")


def test_behavioral_change_is_computed_not_declared():
    """behavioral_change must be derived from a comparison, never a literal."""
    s = source()
    assert "behavioral_change: true" not in s, (
        "behavioral_change is hardcoded true. It must be computed from the two "
        "observed results, or the system asserts intelligence influence it never observed."
    )
    assert "changed: true" not in s, (
        "behavioral_delta.changed is hardcoded true. Same defect: declaration, not observation."
    )


def test_observed_result_is_a_captured_return_value_not_a_literal():
    """Each arm's observed_result must come from executing something real."""
    s = source()
    for literal in (
        "without the fresh retained lesson",
        "applied the fresh lesson and preserved provenance",
    ):
        assert literal not in s, (
            f"observed_result still contains the hardcoded literal {literal!r}. "
            f"The arm did not execute anything; it was written."
        )


def test_both_arms_execute_a_real_decision_surface():
    """The arms must call the real decision function, twice, with and without context."""
    s = source()
    assert "naya-decision-context" in s, (
        "learning-influence must execute the real decision surface "
        "(naya-decision-context) in both arms rather than inserting declared receipts."
    )
    calls = s.count("naya-decision-context")
    assert calls >= 2, f"expected a real execution in both arms, found {calls} reference(s)"


def test_executor_and_verifier_agree_on_evidence_vocabulary():
    """The executor writes evidence the independent verifier actually requires."""
    s = source()
    # The reconciler in graph-verify demands these exact fields. If the executor
    # does not write them, the proof can never reconcile and the gate is correct
    # to fail.
    assert 'relationship_context_enabled' in s, (
        "executor never writes relationship_context_enabled, which the independent "
        "verifier requires. Executor and verifier disagree."
    )
    for value in ('"OFF"', '"ON"'):
        assert value in s, f"evidence condition {value} is never written by the executor"
