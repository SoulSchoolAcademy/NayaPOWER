import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".naya" / "specifications" / "NAYA-MASTER-NODE-KERNEL-V1.json"
RUNTIME = ROOT / "supabase" / "functions" / "nayanet-compound-intelligence" / "index.ts"


def test_master_kernel_declares_explicit_system_authenticated_scope():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scope = data["access_scope"]
    assert scope["mode"] == "SYSTEM_AUTHENTICATED"
    assert scope["visibility"] == "AUTHENTICATED_RUNTIME_ONLY"
    assert scope["owner_id_role"] == "PROVENANCE_ONLY"
    assert scope["caller_owner_equality_required"] is False
    assert scope["mutation_authority"] == "SEPARATE_GOVERNED_AUTHORITY"
    assert scope["fail_closed_when_scope_missing_or_mismatched"] is True


def test_runtime_loader_uses_admin_system_scope_and_not_requester_owner_scope():
    source = RUNTIME.read_text(encoding="utf-8")
    assert 'const MASTER_NODE_ACCESS_SCOPE = "SYSTEM_AUTHENTICATED";' in source
    assert 'admin.from("nayanet_intelligent_blocks")' in source
    assert '.eq("owner_scope", MASTER_NODE_ACCESS_SCOPE)' in source
    assert 'node.content?.classification === "system_intelligence"' in source
    loader_start = source.index("async function loadMasterNodeKernel")
    loader_end = source.index("async function restore", loader_start)
    loader = source[loader_start:loader_end]
    assert '.eq("owner_id", userId)' not in loader
