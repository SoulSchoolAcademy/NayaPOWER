from pathlib import Path
import ast
import re
import textwrap
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
LEARN = (ROOT / "supabase/functions/nayanet-learning-verify/index.ts").read_text(encoding="utf-8")
COLD = (ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github/workflows/live-supabase-runtime-proof.yml").read_text(encoding="utf-8")


def test_verified_learning_lock_in_populates_graph_v2_semantics():
    # H8-7 repair: applicability is provenance-governed, not text-derived.
    # The test pins the governed contract, not the old regex triplets.
    assert "deriveGraphApplicability" in LEARN
    assert "TASK_CLASS_REGISTRY" in LEARN
    assert "provenance_sensitive:" in LEARN
    assert "repository_correction:" in LEARN
    assert "active_intelligence_sensitive:" in LEARN
    assert "learning_reuse:" in LEARN
    assert "contextual_retrieval:" in LEARN
    assert '"TASK_APPLICABILITY_GOVERNED_DECLARATION"' in LEARN
    assert '"TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION"' in LEARN
    assert '"TASK_APPLICABILITY_DERIVED_FROM_VERIFIED_LESSON"' not in LEARN
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


def test_fallback_capture_declares_provenance_sensitive_task_class():
    source = (ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml").read_text(encoding="utf-8")
    # Execute request expressions from the actual embedded producers. Selecting
    # the first request only can silently test the batch path as the fallback.
    fixture = {
        "os": SimpleNamespace(environ={"GRANT_ID": "LOCAL-FIXTURE-GRANT"}),
        "capture": {"capture_id": "ordinary-note", "title": "ordinary", "topic": "ordinary"},
        "distilled": "ordinary content",
        "resolved_connections": [],
        "lesson_key": "LOCAL-FALLBACK",
        "lesson_content": "fixture content",
    }
    requests = []
    for match in re.finditer(r"<<'PY'[^\n]*\n(.*?)^          PY\s*$", source, re.M | re.S):
        embedded = textwrap.dedent(match.group(1))
        tree = ast.parse(embedded)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "request"
                for target in node.targets
            ):
                expression = compile(ast.Expression(node.value), "<workflow-request>", "eval")
                requests.append(eval(expression, {"__builtins__": {}}, fixture))

    ordinary = [r for r in requests if r["p_event_id"] == "SMART-NOTE-ordinary-note"]
    fallback = [r for r in requests if r["p_event_id"] == "LOCAL-FALLBACK"]
    assert len(requests) == 3, "batch, single-capture and fallback must all be exercised"
    assert len(ordinary) == 2
    assert len(fallback) == 1
    assert fallback[0].get("declared_task_classes") == ["provenance_sensitive"]
    assert all("declared_task_classes" not in r for r in ordinary), (
        "ordinary captures must not inherit a proof-fixture task declaration"
    )
