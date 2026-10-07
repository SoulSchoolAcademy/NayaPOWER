from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "governed-supabase-production-deploy.yml"

def test_explicit_source_sha_validation_uses_shell_length_and_character_contract():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'authorized_sha="${{ inputs.source_sha }}"' in source
    assert 'if [ "${#authorized_sha}" -ne 40 ]; then' in source
    assert 'case "$authorized_sha" in' in source
    assert '^[0-9a-fA-F]*' in source
    assert "grep -Eq '^[0-9a-f]{40}$'" not in source

def test_explicit_source_sha_validation_preserves_exact_current_sha_fail_closed_gate():
    source = WORKFLOW.read_text(encoding="utf-8")
    block_start = source.index('authorized_sha="${{ inputs.source_sha }}"')
    block_end = source.index('echo "AUTHORIZED_SOURCE_SHA=$authorized_sha"', block_start)
    block = source[block_start:block_end]
    assert 'if [ "$authorized_sha" != "$GITHUB_SHA" ]; then' in block
    assert 'resolved_main="$(git rev-parse origin/main)"' in block
    assert 'if [ "$authorized_sha" != "$resolved_main" ]; then' in block
