import json
from pathlib import Path

from tools.learning_engine_assembly_gate import assess_assembly

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"
ASSEMBLY = ROOT / "BRAIN" / "03-KERNEL" / "ASSEMBLY-STATUS.json"


def test_production_learning_experiment_is_held_until_assembly_is_proven():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    manifest = json.loads(ASSEMBLY.read_text(encoding="utf-8"))
    assert "  assembly-gate:" in workflow
    assert "tools/learning_engine_assembly_gate.py" in workflow
    for job in ("cold-runtime-1", "cold-runtime-2", "live-connect", "learning-influence-experiment"):
        start = workflow.index(f"  {job}:")
        next_job = workflow.find("\n  ", start + 4)
        block = workflow[start: next_job if next_job >= 0 else len(workflow)]
        assert "needs.assembly-gate.outputs.ready == 'true'" in block, job
    verdict = assess_assembly(manifest, manifest["source_main_sha"])
    assert verdict.ready is False
    assert any("ASSEMBLY_STATUS_NOT_READY" in item for item in verdict.blockers)


def test_only_unit_contract_job_remains_available_while_e2e_is_held():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    start = workflow.index("  contract:")
    end = workflow.index("\n  cold-runtime-1:", start)
    block = workflow[start:end]
    assert "needs: [source-integrity]" in block
    assert "assembly-gate" not in block
