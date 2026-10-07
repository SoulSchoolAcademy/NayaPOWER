import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"

def _job_block(source: str, job: str) -> str:
    match = re.search(rf"(?ms)^  {re.escape(job)}:\n(.*?)(?=^  [A-Za-z0-9_-]+:\n|\Z)", source)
    assert match, f"job not found: {job}"
    return match.group(1)

def test_downstream_proof_jobs_do_not_override_failed_needs_with_always():
    source = WORKFLOW.read_text(encoding="utf-8")
    for job in ("cold-successor", "cold-successor-verification", "independent-connect-verification"):
        block = _job_block(source, job)
        assert "if: ${{ always() }}" not in block

def test_cold_successor_requires_retained_learning_reread_success():
    source = WORKFLOW.read_text(encoding="utf-8")
    block = _job_block(source, "cold-successor")
    assert "needs: independent-retained-learning-reread" in block
    assert "if: ${{ always() }}" not in block

def test_cold_successor_verification_requires_cold_successor_success():
    source = WORKFLOW.read_text(encoding="utf-8")
    block = _job_block(source, "cold-successor-verification")
    assert "needs: cold-successor" in block
    assert "if: ${{ always() }}" not in block