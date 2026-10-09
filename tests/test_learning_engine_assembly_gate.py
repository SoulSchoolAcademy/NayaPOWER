import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.learning_engine_assembly_gate import REQUIRED_CONNECTIONS, assess_assembly

SHA = "a" * 40


def evidence():
    return [{"source_sha": SHA, "independent_verifier": "naya-2", "artifact_sha256": "b" * 64, "verified_at": "2026-10-09T23:00:00Z"}]


def ready_manifest():
    return {
        "schema": "naya.learning-engine-assembly-gate.v1",
        "status": "READY_FOR_END_TO_END",
        "verified_source_sha": SHA,
        "required_connections": [{"id": cid, "status": "PROVEN", "evidence": evidence()} for cid in REQUIRED_CONNECTIONS],
    }


def test_current_blocked_state_does_not_arm_e2e():
    m = ready_manifest()
    m["status"] = "BLOCKED"
    assert not assess_assembly(m, SHA).ready


def test_all_exact_sha_proven_connections_arm_e2e():
    assert assess_assembly(ready_manifest(), SHA).ready


def test_manifest_only_commit_does_not_make_sha_binding_self_referential():
    r = assess_assembly(
        ready_manifest(), "c" * 40,
        changed_paths=["BRAIN/03-KERNEL/ASSEMBLY-STATUS.json"],
        verified_is_ancestor=True,
    )
    assert r.ready


def test_code_change_after_verified_source_blocks_e2e():
    r = assess_assembly(
        ready_manifest(), "c" * 40,
        changed_paths=["supabase/functions/nayanet-act-runtime/index.ts"],
        verified_is_ancestor=True,
    )
    assert not r.ready
    assert any("CODE_CHANGED_AFTER_ASSEMBLY_PROOF" in x for x in r.blockers)


def test_non_ancestor_verified_source_blocks_e2e():
    r = assess_assembly(ready_manifest(), SHA, verified_is_ancestor=False)
    assert not r.ready
    assert any("VERIFIED_SOURCE_NOT_ANCESTOR" in x for x in r.blockers)


def test_missing_connection_blocks_e2e():
    m = ready_manifest()
    m["required_connections"].pop()
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("REQUIRED_CONNECTION_MISSING" in x for x in r.blockers)


def test_unproven_connection_blocks_e2e():
    m = ready_manifest()
    m["required_connections"][0]["status"] = "PARTIAL"
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("CONNECTION_NOT_PROVEN" in x for x in r.blockers)


def test_wrong_source_sha_blocks_e2e():
    m = ready_manifest()
    m["required_connections"][0]["evidence"][0]["source_sha"] = "c" * 40
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("EVIDENCE_SOURCE_SHA_MISMATCH" in x for x in r.blockers)


def test_missing_evidence_blocks_e2e():
    m = ready_manifest()
    m["required_connections"][0]["evidence"] = []
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("CONNECTION_EVIDENCE_MISSING" in x for x in r.blockers)


def test_wrong_evidence_hash_blocks_e2e():
    m = ready_manifest()
    m["required_connections"][0]["evidence"][0]["artifact_sha256"] = "not-a-hash"
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("EVIDENCE_HASH_INVALID" in x for x in r.blockers)


def test_unknown_connection_class_blocks_e2e():
    m = ready_manifest()
    m["required_connections"].append({"id": "UNREGISTERED_NODE", "status": "PROVEN", "evidence": evidence()})
    r = assess_assembly(m, SHA)
    assert not r.ready
    assert any("UNDOCUMENTED_CONNECTION_CLASSES" in x for x in r.blockers)
