from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import json
import os
import urllib.error
import urllib.request


URL = os.environ.get("RUNTIME_FUNCTION", "https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-intelligence-commit-runtime").rstrip("/")
TOKEN = os.environ.get("NAYA_RUNTIME_OIDC_TOKEN", "")
GRANT = os.environ.get("NAYANET_INTELLIGENCE_COMMIT_GRANT_ID", "")


def request(payload, token=TOKEN):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(URL, headers=headers, method="POST", data=json.dumps(payload).encode())
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def test_fresh_lesson_intelligence_commit_uses_naya_runtime_and_persists_connected_checkpoint():
    if not TOKEN or not GRANT:
        import pytest
        pytest.skip("short-lived Naya runtime identity and durable intelligence_commit grant are required")

    status, result = request({
        "mode": "execute",
        "p_authority_grant_id": GRANT,
        "p_event_id": "TEST-FRESH-LESSON",
        "p_title": "Fresh canonical lesson",
        "p_content": "A meaningful lesson for proving durable connected intelligence.",
        "p_category": "COLLECTIVE_INTELLIGENCE",
        "p_topic": "COMPOUNDING_INTELLIGENCE",
        "p_target_id": "NAYA-NODE-0001",
        "p_project_id": "NayaNET",
    })
    assert status == 200 and result.get("ok") is True, (status, result)
    assert result["runtime_identity"] == "naya-node-oidc"

    lineage = result["result"]
    for key in ("receipt_id","event_id","intelligent_block_id","lineage_id","relationship_id","index_id","checkpoint_id"):
        assert lineage.get(key), (key, lineage)

    status, verify = request({"mode": "verify", **{k: lineage[k] for k in (
        "receipt_id","event_id","intelligent_block_id","lineage_id","relationship_id","index_id","checkpoint_id"
    )}})
    assert status == 200 and verify.get("ok") is True, (status, verify)
    assert verify["status"] == "LINEAGE_VERIFIED"
    assert verify["independent_verification"] is True
    assert all(verify["checks"].values()), verify


def test_runtime_commit_uses_direct_postgrest_rpc_boundary():
    from pathlib import Path

    source = (
        Path(__file__).resolve().parents[1]
        / "supabase"
        / "functions"
        / "nayanet-intelligence-commit-runtime"
        / "index.ts"
    ).read_text(encoding="utf-8")

    call_commit = source.split("async function callCommit", 1)[1].split("const idColumn", 1)[0]
    assert '"/rest/v1/rpc/nayanet_intelligence_commit_runtime"' in call_commit
    assert "admin.rpc(" not in call_commit


def test_fresh_lesson_enters_existing_runtime_and_independent_verification_path():
    workflow = (ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml").read_text(encoding="utf-8")
    assert "fresh-lesson:" in workflow
    assert "independent-verification:" in workflow
    assert 'mode":"execute"' in workflow
    assert 'mode":"verify"' in workflow
    assert "nayanet-intelligence-commit-runtime" in workflow
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" in workflow
    assert "intelligent_block_id" in workflow
    assert "lineage_id" in workflow
    assert "relationship_id" in workflow
    assert "checkpoint_id" in workflow
    assert "independent_verification" in workflow


def test_independent_verifier_downloads_the_produced_lineage_before_reading_it():
    import yaml

    workflow = yaml.safe_load((ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text(encoding="utf-8"))
    producer = workflow["jobs"]["fresh-lesson"]["steps"]
    uploads = [step["with"] for step in producer if step.get("uses", "").startswith("actions/upload-artifact@")]
    artifact = next(item for item in uploads if "fresh-lesson-lineage-ids.json" in item["path"])
    steps = workflow["jobs"]["independent-verification"]["steps"]
    reader = next(i for i, step in enumerate(steps) if 'open("fresh-lesson-lineage-ids.json")' in step.get("run", ""))
    assert any(step.get("uses", "").startswith("actions/download-artifact@") and step.get("with", {}).get("name") == artifact["name"] for step in steps[:reader])
