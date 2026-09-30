from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
COLD = ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts"
WORKFLOW = ROOT / ".github/workflows/live-supabase-runtime-proof.yml"
VERIFIER = ROOT / "tests/verify_cold_graph_behavior.py"
OBJECT = ROOT / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-CONNECT.json"
REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"

def test_existing_connect_seam_is_bound_without_inventing_a_second_graph():
    source = COLD.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    verifier = VERIFIER.read_text(encoding="utf-8")
    obj = json.loads(OBJECT.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert 'mode === "graph-behavior"' in source
    assert 'mode === "graph-verify"' in source
    assert "nayanet_brain_relationships" in source
    assert "relationship_context_enabled" in source
    assert "selected_relationship_paths" in source
    assert "epistemic_state === \"VERIFIED\"" in source
    assert "r.provenance" in source

    assert "COLD-NAYA-GRAPH-HELDOUT-001" in workflow
    assert "relationship_context" in workflow
    assert "mode=graph-verify" in workflow
    assert "independently_reconstructed" in verifier

    assert obj["proof"]["proof_run"] == 36516790588
    assert obj["proof"]["proof_source_revision"] == "c9b31890c93f4f5f7d60bb8cd346093c11ab427f"
    assert obj["proof"]["current_main_production_proof"] if "current_main_production_proof" in obj["proof"] else True
    assert "GENERAL CONNECT SEMANTICS NOT_PROVEN" in obj["proof"]["relationships_status"]

    binding = registry["node_runtime_bindings"]["CONNECT"]
    assert binding["entrypoint"] == "supabase/functions/nayanet-cold-runtime-proof/index.ts"
    assert binding["modes"] == ["graph-behavior", "graph-verify"]
    assert binding["current_main_production_proof"] == "NOT_PROVEN"
    assert binding["full_contract"] == "NOT_PROVEN"
    assert binding["authority_rule"] == "relationship context never grants authority"

def test_connect_truth_does_not_overclaim_full_contract():
    obj = json.loads(OBJECT.read_text(encoding="utf-8"))
    proof = obj["proof"]
    assert proof["production_status"] == "HISTORICAL_EXACT_REVISION_C9_ONLY_CURRENT_MAIN_NOT_PROVEN"
    assert proof["organism_binding"].endswith("FULL CONNECT NODE RUNTIME CONTRACT NOT_PROVEN")
    limitations = " ".join(proof["limitations"]).lower()
    assert "multi-hop" in limitations
    assert "cycle" in limitations
    assert "freshness" in limitations
    assert "contradiction" in limitations
    assert "supersession" in limitations
    assert "current main" in limitations
    assert "authority" in limitations
