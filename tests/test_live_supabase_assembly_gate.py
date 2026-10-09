import json
import re
from pathlib import Path

from tools.learning_engine_assembly_gate import assess_assembly

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"
ASSEMBLY = ROOT / "BRAIN" / "03-KERNEL" / "ASSEMBLY-STATUS.json"


def _job_block(workflow: str, job: str) -> str:
    match = re.search(rf"(?ms)^  {re.escape(job)}:\n(.*?)(?=^  [a-z0-9_-]+:|\Z)", workflow)
    assert match is not None, f"missing job {job}"
    return match.group(1)


def test_production_learning_experiment_is_held_until_assembly_is_proven():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    manifest = json.loads(ASSEMBLY.read_text(encoding="utf-8"))
    assert "  assembly-gate:" in workflow
    assert "tools/learning_engine_assembly_gate.py" in workflow
    for job in ("cold-runtime-1", "cold-runtime-2", "live-connect", "learning-influence-experiment"):
        block = _job_block(workflow, job)
        assert "needs.assembly-gate.outputs.ready == 'true'" in block, job
    verdict = assess_assembly(manifest, manifest["source_main_sha"])
    assert verdict.ready is False
    assert any("ASSEMBLY_STATUS_NOT_READY" in item for item in verdict.blockers)


def test_only_unit_contract_job_remains_available_while_e2e_is_held():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    block = _job_block(workflow, "contract")
    assert "needs: [source-integrity]" in block
    assert "assembly-gate" not in block
