from pathlib import Path

RUNTIME = Path("supabase/functions/nayanet-intelligence-commit-runtime/index.ts").read_text(encoding="utf-8")

def test_runtime_exposes_owner_bound_verify_block_mode():
    assert 'if (mode === "verify_block")' in RUNTIME
    assert 'INTELLIGENT_BLOCK_ID_REQUIRED' in RUNTIME
    assert 'read(admin, blockId, "nayanet_intelligent_blocks", "owner_id")' in RUNTIME
    assert '"BLOCK_VERIFIED"' in RUNTIME
    verify_block = RUNTIME.split('if (mode === "verify_block")', 1)[1].split('if (mode === "verify")', 1)[0]
    assert 'ok: Boolean(block)' in verify_block
    assert 'independent_verification: Boolean(block)' in verify_block
    assert 'independent_verification: true' not in verify_block
