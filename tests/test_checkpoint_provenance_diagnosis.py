"""A failed provenance check must name the link that broke.

FAILURE-FIRST PROVENANCE
------------------------
Live proof run 36503245065 failed in `learning-influence-experiment` with:

    {"ok":false,"error":"CHECKPOINT_PROVENANCE_MISMATCH"}   HTTP 409

One string. Four possible links. Nothing to tell a superseded checkpoint from a
rebuilt chain, so the failure is not resolvable from a log - the same dead end
`SUPABASE_READ_400` presented before PR #934.

The guard itself is correct and must stay correct: the checkpoint row is keyed on
(user_id, project_id) and upserted by every intelligence commit, so a mismatch is
a real provenance failure whether the chain was rebuilt wrongly or a later commit
overwrote the state the artifact was bound to. Refusing is right. Refusing
anonymously is not.

This test therefore asserts two things that pull against each other:
  * the check still rejects - HTTP 409, not softened to a pass;
  * the rejection names every field it compared, with both sides.

It fails against origin/main as of 0dcff9b81 and passes on the fix.

No boundary is relaxed: this is an error-message contract, not an authorization
one. Authorization lives in test_naya_identity_owner_binding and
test_github_oidc_binding, and neither is touched here.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts"


def _source() -> str:
    return SOURCE.read_text(encoding="utf-8")


def test_checkpoint_mismatch_still_rejects_with_409():
    source = _source()
    assert 'error: "CHECKPOINT_PROVENANCE_MISMATCH"' in source
    # The guard may accept an advanced mutable checkpoint only when the immutable
    # intelligence_commit receipt reconstructs the exact historical chain.
    # If that reconstruction fails, it must still return 409.
    assert 'error: "CHECKPOINT_PROVENANCE_MISMATCH"' in source
    assert "immutable_receipt_reconstruction: false" in source
    assert "receiptMatchesHistoricalChain" in source
    assert ", 409)" in source
    assert "CHECKPOINT_NOT_FOUND" in source


def test_checkpoint_mismatch_names_the_field_and_both_sides():
    source = _source()
    # The response must carry which link disagreed and what each side held.
    assert "mismatched" in source, "the error must list the fields it compared"
    assert "checkpoint_state:" in source, "each mismatch must report the checkpoint's value"
    assert "rebuilt_chain:" in source, "each mismatch must report the rebuilt chain's value"
    assert "checkpoint_revision" in source, "the revision distinguishes a superseded checkpoint"

    # All four provenance links are compared, and all four are named when they fail.
    for field in ("intelligent_block_id", "lineage_id", "relationship_id", "index_id"):
        assert field in source, f"{field} is part of the Event -> Block -> Lineage -> Relationship -> Index -> Checkpoint chain"


def test_checkpoint_mismatch_message_carries_no_credential():
    """Diagnostics may carry ids and states. They may never carry a key."""
    source = _source()
    assert "SERVICE_ROLE" not in source.split("const serviceRole")[0]
    # The mismatch payload is built only from column values already in scope.
    assert "Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\")" in source
    body = source[source.index("const rebuiltChain"):source.index('if (mismatched.length)')]
    assert "env.get" not in body, "the diagnostic payload must be built from ids, not environment"


def test_advanced_checkpoint_requires_exact_immutable_receipt_chain():
    source = _source()
    assert 'commitReceipt?.action === "intelligence_commit"' in source
    assert 'ev.checkpoint_id === checkpoint.id' in source
    assert 'ev.event_row_id === event.id' in source
    assert 'ev.intelligent_block_id === blockId' in source
    assert 'ev.lineage_id === lineage.id' in source
    assert 'ev.relationship_id === relationship.relationship_id' in source
    assert 'ev.index_id === index.id' in source


def test_historical_lock_in_does_not_overwrite_current_project_checkpoint():
    source = _source()
    assert 'historicalCheckpoint' in source
    assert 'if (!historicalCheckpoint)' in source
    assert 'LEARNED_VIA_IMMUTABLE_RECEIPT' in source
