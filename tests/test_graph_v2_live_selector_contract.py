from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARN = (ROOT / "supabase/functions/nayanet-learning-verify/index.ts").read_text(encoding="utf-8")
COLD = (ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github/workflows/live-supabase-runtime-proof.yml").read_text(encoding="utf-8")


def test_verified_learning_lock_in_populates_graph_v2_semantics():
    assert "deriveGraphApplicability" in LEARN
    assert '"provenance_sensitive", "learning_reuse", "contextual_retrieval"' in LEARN
    assert '"repository_correction", "learning_reuse", "contextual_retrieval"' in LEARN
    assert 'evidence_refs: relationshipEvidenceRefs' in LEARN
    assert 'applicability: graphApplicability' in LEARN
    assert 'reason_codes: relationshipReasonCodes' in LEARN
    assert 'status: "ACTIVE"' in LEARN
    assert 'visibility: "PRIVATE"' in LEARN
    assert '"APPLICABILITY_UNCLASSIFIED"' in LEARN


def test_graph_behavior_requires_v2_current_evidenced_applicable_edges():
    for text in [
        'r.status !== "ACTIVE"',
        'r.epistemic_state !== "VERIFIED"',
        'r.evidence_refs.length === 0',
        'supersededIds.has',
        'r.valid_from',
        'r.valid_until',
        'r.visibility === "DERIVED_SHARED" && !r.consent_ref',
        'app.state !== "APPLICABLE"',
        '!app.task_classes.includes(taskClass)',
    ]:
        assert text in COLD
    assert 'schema: "NAYANET_COLD_GRAPH_BEHAVIOR_V2"' in COLD


def test_graph_behavior_is_bound_to_fresh_block_not_legacy_constant():
    graph_start = COLD.index('if (mode === "graph-behavior")')
    graph_end = COLD.index('if (mode === "cold-successor")', graph_start)
    block = COLD[graph_start:graph_end]
    assert 'const blockId = String(body?.intelligent_block_id || "")' in block
    assert 'target_id=eq." + encodeURIComponent(blockId)' in block
    assert 'target_id=eq." + encodeURIComponent(BLOCK_ID)' not in block


def test_graph_verifier_independently_rereads_relationship_rows():
    start = COLD.index('if (mode === "graph-verify")')
    end = COLD.index('if (mode === "graph-behavior")', start)
    block = COLD[start:end]
    assert "relationship_rows_re_read: true" in block
    assert "nayanet_brain_relationships" in block
    assert "graphRelationshipEligible" in block
    assert "GRAPH_CONTROL_TREATMENT_INPUT_MISMATCH" in block


def test_workflow_graph_proof_waits_for_verified_learning_and_uses_producer_block():
    marker = "  cold-graph-control-treatment:"
    start = WORKFLOW.index(marker)
    end = WORKFLOW.index("  independent-cold-graph-verification:", start)
    block = WORKFLOW[start:end]
    assert "needs: learning-promotion" in block
    assert "name: smart-note-lineage" in block
    assert "run-id: ${{ env.PRODUCER_RUN_ID }}" in block
    assert 'open("graph-block-id.txt","w").write(block_id)' in block
    assert '"intelligent_block_id"' in block
    assert '"provenance_sensitive"' in block
    assert "NAYANET_COLD_GRAPH_BEHAVIOR_V2" in block
