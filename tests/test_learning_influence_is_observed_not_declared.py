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
    """The executor must write the evidence the independent verifier requires.

    Scoped to the learning-influence branch only. A previous version of this test
    searched the whole file and passed merely because the VERIFIER mentioned
    relationship_context_enabled, which made it vacuous. This version requires
    the EXECUTOR to write the fields, and requires the two vocabularies to
    actually agree.
    """
    s = source()
    start = s.index('mode === "learning-influence"')
    executor = s[start : s.index('if (mode === "connect")')]

    # The independent verifier (graph-verify) requires these exact fields.
    assert "relationship_context_enabled" in executor, (
        "the learning-influence EXECUTOR never writes relationship_context_enabled, "
        "which the independent verifier requires. Executor and verifier disagree, so "
        "the proof can never reconcile."
    )
    assert '"OFF"' in executor and '"ON"' in executor, (
        "the executor must write evidence condition OFF for control and ON for "
        "treatment, matching what the verifier asserts."
    )
    for literal in ('"CONTROL"', '"TREATMENT"'):
        assert literal not in executor, (
            f"executor writes condition {literal} but the verifier requires "
            f"OFF/ON. The two vocabularies must be identical."
        )
