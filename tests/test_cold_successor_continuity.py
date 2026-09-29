"""Regression guard for the cold-successor (Hole D) proof.

WHAT THIS GUARDS
----------------
`learning-influence-receipt.json` proves a fresh OWNER SESSION is influenced by
persisted verified learning. That receipt is BLOCKED on a rotated credential and
is not a continuity proof anyway: an owner session already has authority, so it
cannot show what a SUCCESSOR does or does not inherit.

Hole D is a different and harder claim:

    A cold Naya, with no local memory of the prior execution, reconstructs the
    persisted intelligence through the canonical retrieval path, USES it, and
    does NOT inherit the prior Naya's authority.

The load-bearing property is NON-INHERITANCE. The durable grant is identity-scoped
to NAYA-NODE-0001. A successor is a different identity. Therefore a successor
that has successfully retrieved the intelligence must still be refused a
consequential action, because knowledge and retrieval confer nothing.

These tests guard the three ways that proof can be hollowed out:

  1. by letting the caller HAND the successor the intelligence, so "reconstruction"
     is really delivery;
  2. by hardcoding the refusal instead of deriving it from the grant table, so the
     refusal survives nothing and proves nothing;
  3. by letting the verifier trust the successor's own receipt.

Source-contract tests, deliberately. The live OIDC run is the actual proof; these
are the ratchet that keeps it from being quietly hollowed out.
"""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FUNCTION = REPO / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"
WORKFLOW = REPO / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def _source() -> str:
    return FUNCTION.read_text(encoding="utf-8")


def _block(marker: str, end: str) -> str:
    src = _source()
    start = src.find(marker)
    assert start != -1, f"{marker} not found"
    stop = src.find(end, start)
    assert stop != -1, f"could not delimit {marker}"
    return src[start:stop]


def _successor() -> str:
    return _block('if (mode === "cold-successor")', 'if (mode === "cold-successor-verify")')


def _verify() -> str:
    return _block('if (mode === "cold-successor-verify")', 'if (req.method !== "GET" || mode !== "cold")')


# --- 1. The successor must not be handed the intelligence ---------------------

def test_cold_successor_accepts_only_a_learning_id():
    """If the caller can supply the lesson or the behaviour, 'reconstruction' is
    just delivery wearing a receipt."""
    block = _successor()
    assert 'searchParams.get("learning_id")' in block
    assert 'searchParams.get("lesson")' not in block
    assert 'searchParams.get("behavior")' not in block
    assert 'searchParams.get("claim")' not in block
    assert "intelligence_content_accepted_as_input: false" in block


def test_cold_successor_derives_behavior_from_the_retrieved_block_not_from_input():
    block = _successor()
    assert 'const lesson = successorBlock.content?.lesson' in block
    assert "PRESERVE_PROVENANCE_BEFORE_APPLY" in block
    assert "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE" in block


# --- 2. Non-inheritance must be COMPUTED, not declared -----------------------

def test_successor_is_a_distinct_identity_from_the_original_node():
    block = _successor()
    assert 'const successorId = "NAYA-NODE-0001-SUCCESSOR-COLD-01"' in block
    assert 'successor_grant_scope_target: successorId' in block
    assert "node0001_grant_scope_target: NAYA_ID" in block


def test_authority_verdict_is_derived_from_the_grant_table():
    """The refusal must fall out of the durable grant's identity scope. A hardcoded
    `authorized:false` would prove nothing."""
    block = _successor()
    assert 'grantRows.filter((g: any) => g.scope?.target === successorId)' in block
    assert "const consequentialAuthorized = successorGrantsAction.length > 0" in block
    assert "const authorityResolved = successorGrants.length > 0" in block
    assert "consequential_actions_authorized: consequentialAuthorized" in block


def test_successor_never_executes_a_consequential_action():
    block = _successor()
    assert "executed: false" in block or "const executed = false" in block
    assert "consequential: true" in block
    assert "allowed: false" in block
    assert 'knowledge_creates_authority: false' in block
    assert 'retrieval_creates_authority: false' in block
    assert "authority_inherited: false" in block


# --- 3. The verifier must re-read and recompute, not trust the receipt -------

def test_verifier_does_not_trust_the_successor_receipt():
    verify = _verify()
    assert "executor_claim_trusted: false" in verify
    assert "AUTHORITATIVE_REREAD_AND_RECOMPUTATION" in verify
    # It must re-read the learning and the relationships itself.
    assert "rest/v1/learning_evidence?id=eq." in verify
    assert "status=eq.ACTIVE" in verify
    assert "target_id=eq." in verify
    assert "nayanet_brain_relationships?owner_id=eq." in verify


def test_verifier_recomputes_the_behavior_independently():
    verify = _verify()
    assert "behavior_recomputed: vBehavior" in verify
    assert 'recomputed.behavior_recomputed === "PRESERVE_PROVENANCE_BEFORE_APPLY"' in verify


def test_verdict_requires_zero_successor_grants():
    """The non-inheritance claim is only true if the successor genuinely has no
    grant. If one ever existed, this must fail closed rather than pass."""
    verify = _verify()
    assert "recomputed.successor_grant_count === 0" in verify
    assert "recomputed.authority_recomputed === false" in verify
    assert 'recomputed.recomputed_blocked_by === "IDENTITY_SCOPE"' in verify


def test_verifier_states_its_limitation():
    verify = _verify()
    assert "limitation:" in verify
    assert "not general successor capability" in verify


# --- 4. The proof must actually be wired into a live OIDC workflow -----------

def test_workflow_proves_cold_successor_in_a_separate_fresh_runtime():
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert "cold-successor" in wf, "the cold-successor proof is not wired into any live workflow"
    assert "cold-successor-verify" in wf, "the independent cold-successor verifier is not wired in"
    assert "causal-learning-experiment-receipt" in wf
    assert "needs: independent-retained-learning-reread" in wf
    assert "mode=cold-successor&learning_id=${learning_id}" in wf


def test_workflow_separates_executor_from_verifier_jobs():
    """Builder/verifier separation: a separate job, hence a separate runner and a
    separate OIDC token, must perform verification."""
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert "cold-successor-successor-receipt" in wf or "cold-successor-receipt" in wf
    assert "cold-successor-verification:" in wf or "cold-successor-verification" in wf


def test_committed_receipt_proves_non_inheritance():
    """The committed receipt is the evidence. Guard its load-bearing claims so a later
    edit cannot quietly turn a non-inheritance result into an inheritance one."""
    import json

    receipt = json.loads(
        (REPO / "cold-successor-receipt-verified.json").read_text(encoding="utf-8")
    )
    assert receipt["schema"] == "NAYANET_COLD_SUCCESSOR_RECEIPT_V1"
    assert receipt["authority_inherited"] is False
    assert receipt["successor_grant_count"] == 0
    assert receipt["consequential_actions_authorized"] is False
    assert receipt["executed"] is False
    assert receipt["blocked_by"] == "IDENTITY_SCOPE"
    # Genuine reconstruction, not delivery.
    assert receipt["learning_id"] and receipt["intelligent_block_id"]
    assert len(receipt["verified_relationships"]) > 0
    assert all(r["epistemic_state"] == "VERIFIED" for r in receipt["verified_relationships"])
    assert all(r.get("provenance") for r in receipt["verified_relationships"])
    # Material use, and an honest scope claim.
    assert receipt["behavior"] == "PRESERVE_PROVENANCE_BEFORE_APPLY"
    assert receipt["materially_attributable"] is True
    assert "not general successor capability" in receipt["limitation"]
    # Verification was independent of the executor.
    assert receipt["independent_verification"] is True
    assert receipt["executor_runtime_jti"] != receipt["verifier_runtime_jti"]


def test_runtime_still_refuses_non_canonical_branches():
    """The runtime binds the OIDC token's workflow_ref to refs/heads/main, so a PR
    branch cannot invoke it. Run 36455994970 failed with WORKFLOW_BINDING_MISMATCH for
    exactly this reason. That refusal is governance, not a bug: the proof must be
    produced on main. Widening this would let any branch drive the runtime."""
    src = _source()
    assert 'const REF = "refs/heads/main"' in src
    assert 'throw new Error("WORKFLOW_BINDING_MISMATCH")' in src
    assert 'payload.ref !== REF' in src


def test_cold_successor_is_gated_on_verified_fresh_learning():
    """The successor must consume the exact learning that passed independent causal verification,
    not a historical specimen or an unrelated CONNECT receipt."""
    import yaml

    jobs = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]
    needs = jobs["cold-successor"].get("needs")
    needs = [needs] if isinstance(needs, str) else (needs or [])
    assert "independent-retained-learning-reread" in needs
    assert "live-connect" not in needs
    promotion_needs = jobs["learning-promotion"].get("needs")
    promotion_needs = [promotion_needs] if isinstance(promotion_needs, str) else (promotion_needs or [])
    assert "independent-learning-influence-verification" in promotion_needs
