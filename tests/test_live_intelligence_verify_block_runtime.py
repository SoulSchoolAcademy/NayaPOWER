from pathlib import Path

RUNTIME = Path("supabase/functions/nayanet-intelligence-commit-runtime/index.ts").read_text(encoding="utf-8")

def test_runtime_exposes_owner_bound_verify_block_mode():
    assert 'if (mode === "verify_block")' in RUNTIME
    assert 'INTELLIGENT_BLOCK_ID_REQUIRED' in RUNTIME
    assert 'read(admin, blockId, "nayanet_intelligent_blocks", "owner_id")' in RUNTIME
    assert '"BLOCK_VERIFIED"' in RUNTIME
    assert 'independent_verification: true' in RUNTIME
