"""INTEGRATION RUNG — SELF -> LAW -> KNOW -> ACT composed in one governed call.

The ladder gate reports INTEGRATION as MISSING: nothing in the tree tests nodes
working together. Every rung above it (BEHAVIORAL, OUTCOME, CAUSAL, PRODUCTION,
SUCCESSOR) silently assumes composition works.

This asserts that the real runtime composes all four concerns in a single
governed call, in order, and that ACT is correctly BOUNDED by LAW rather than
unblocked. It reads the runtime source; it does not mock, and it does not claim a
live run. Live composition is proven by invoking the function with a real OIDC
identity, which is a separate step and is not asserted here.

A composition test that permitted execution would prove nothing about
governance. The correct composed outcome is: identity established, authority
resolved, intelligence retrieved, action REFUSED by LAW.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts"


def _connect_branch() -> str:
    s = RUNTIME.read_text(encoding="utf-8")
    start = s.index('mode === "connect"')
    end = s.index('mode === "graph-verify"')
    return s[start:end]


def test_composition_runs_in_one_governed_call():
    branch = _connect_branch()
    for concern, marker in (
        ("SELF", "runtime_identity"),
        ("LAW", "authorization_binding"),
        ("KNOW", "relationships"),
        ("ACT", "behavior"),
    ):
        assert marker in branch, f"{concern} concern ({marker}) is absent from the composed call"


def test_authority_is_presented_before_intelligence_in_the_response():
    """Order in what the consumer sees: LAW before KNOW."""
    branch = _connect_branch()
    response = branch[branch.index("return json(") :]
    assert response.index("authorization_binding") < response.index("relationships"), (
        "the composed response must present the authority binding before the "
        "relationships it bounds."
    )


def test_intelligence_is_not_retrieved_before_authority_is_resolved():
    """RED. KNOW currently executes before LAW.

    Found by this composition test on 2026-09-28. In the connect branch the
    runtime fetches relationships (KNOW) and only then resolves and validates the
    durable authorization binding (LAW). The action is still refused, so no
    unauthorized CONSEQUENCE occurs, and retrieval never equals authorization. But
    the stronger property - authorize, then retrieve - is not implemented, and
    this tree's own law does not require it yet.

    Do not weaken this test to make the suite green. Either the runtime reorders
    so LAW resolves before KNOW fetches, or a human ratifies the current order
    explicitly. Both are authority decisions.
    """
    branch = _connect_branch()
    fetch = branch.index("const relationships = await get")
    binding = branch.index("const binding =")
    assert binding < fetch, (
        "KNOW retrieves intelligence before LAW resolves authority. Retrieval is "
        "not authorization and the action remains refused, but authorize-then-"
        "retrieve is the safer composition and is not yet implemented."
    )


def test_act_is_bounded_by_law_not_enabled_by_retrieval():
    """The decisive composition property: retrieval must not authorize action."""
    branch = _connect_branch()
    assert "connect_grants_authority: false" in branch, (
        "the composed call must state that CONNECT does not grant authority"
    )
    assert "consequential_actions_authorized: false" in branch
    assert "blocked_by: \"LAW\"" in branch, (
        "a consequential action in the composed call must be blocked by LAW, not merely "
        "unexecuted. Silent non-execution is not a governance boundary."
    )
    assert "production_mutation_performed: false" in branch
    assert "rls_changed: false" in branch


def test_composition_asserts_owner_and_block_alignment():
    """KNOW must confirm the block belongs to the resolved owner."""
    branch = _connect_branch()
    assert "block_owner_match" in branch, "composition must verify the block belongs to the owner"
    assert "block_understanding_state" in branch
