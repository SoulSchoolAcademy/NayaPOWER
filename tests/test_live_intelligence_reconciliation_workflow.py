from pathlib import Path

WF = Path(".github/workflows/live-intelligence-commit-proof.yml").read_text(encoding="utf-8")

def test_registry_hash_hit_requires_live_runtime_verification_before_reuse():
    assert "REGISTRY_HASH_HIT_REQUIRES_RUNTIME_VERIFICATION" in WF
    assert "registry-runtime-verification" in WF
    assert "tools/live_intelligence_reconcile.py assess" in WF
    assert "REGISTRY_RUNTIME_CONTENT_DRIFT" in WF

def test_verify_only_drift_is_fail_closed_and_never_routes_to_mutation():
    assert 'verify_only_flag="--verify-only"' in WF
    assert 'if [[ "$action" == "REUSE" ]]' in WF
    assert 'elif [[ "$action" == "FAIL_CLOSED" ]]' in WF
    assert "verify-only mode never mutates" in WF

def test_governed_write_drift_routes_through_existing_supersession_runtime():
    assert 'elif [[ "$action" == "SUPERSEDE" ]]' in WF
    assert "build-supersede" in WF
    assert "validate-supersede" in WF
    assert "supersession-reconciliation" in WF
    assert '"mode":"verify_block"' in WF
