from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def _workflow() -> str:
    assert WORKFLOW.exists(), 'live Supabase runtime proof workflow missing'
    return WORKFLOW.read_text(encoding='utf-8')


def test_cold_runtime_proof_has_explicit_source_sha_input_for_manual_dispatch():
    workflow = _workflow()
    assert 'expected_source_sha:' in workflow
    assert "description: \"Exact main SHA whose runtime is being proven\"" in workflow
    assert 'required: true' in workflow


def test_cold_runtime_proof_fails_closed_if_refs_heads_main_moves():
    workflow = _workflow()
    assert "Verify resolved source matches SOURCE_SHA" in workflow
    assert 'resolved="$(gh api "repos/${{ github.repository }}/git/ref/heads/main" --jq .object.sha)"' in workflow
    assert 'if [ "${SOURCE_SHA}" != "${resolved}" ]; then' in workflow
    assert "SOURCE_SHA_MISMATCH" in workflow


def test_all_consequential_jobs_depend_on_source_integrity_gate():
    workflow = _workflow()
    assert "needs: [source-integrity]" in workflow
