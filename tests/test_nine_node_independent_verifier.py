from copy import deepcopy

import pytest

from tools.verify_nine_node_independent import verify_bundle


def bundle():
    return {
        "executor": {
            "source_revision": "SOURCE-1",
            "token_jti": "EXECUTOR-JTI",
            "independent_verification": True,
        },
        "cold": {
            "deployed_source_revision": "SOURCE-1",
            "receipt": {
                "naya_id": "NAYA-NODE-0001",
                "owner_id": "OWNER-1",
                "runtime_identity": "github-actions-oidc",
                "workflow_ref": "WORKFLOW-1",
                "token_jti": "EXECUTOR-JTI",
            },
        },
        "graph": {
            "source_revision": "SOURCE-1",
            "control": {"receipt_id": "CONTROL-1", "behavior": "BASELINE"},
            "treatment": {"receipt_id": "TREATMENT-1", "behavior": "PRESERVE_PROVENANCE"},
            "behavioral_delta": {"changed": True},
        },
        "graph_verify": {
            "source_revision": "SOURCE-1",
            "ok": True,
            "verification": {
                "independently_reconstructed": True,
                "persisted_pair_re_read": True,
                "treatment_relationships_verified": True,
            },
            "receipts": {
                "control": {
                    "id": "CONTROL-1",
                    "observed_result": "BASELINE",
                    "evidence": {
                        "condition": "OFF",
                        "relationship_context_enabled": False,
                        "task_id": "GRAPH-TASK-1",
                        "task_class": "provenance_sensitive",
                        "intelligent_block_id": "IB-1",
                    },
                },
                "treatment": {
                    "id": "TREATMENT-1",
                    "observed_result": "PRESERVE_PROVENANCE",
                    "evidence": {
                        "condition": "ON",
                        "relationship_context_enabled": True,
                        "task_id": "GRAPH-TASK-1",
                        "task_class": "provenance_sensitive",
                        "intelligent_block_id": "IB-1",
                        "selected_relationships": [{"relationship_id": "REL-1"}],
                    },
                },
            },
            "relationships": [{
                "relationship_id": "REL-1",
                "source_id": "SOURCE-1",
                "target_id": "IB-1",
                "relationship_type": "VERIFIED_BY",
                "epistemic_state": "VERIFIED",
                "status": "ACTIVE",
                "provenance": {"source": "CVO-1"},
                "evidence_refs": ["CVO-1"],
                "applicability": {"state": "APPLICABLE", "task_classes": ["provenance_sensitive"]},
            }],
        },
        "promotion": {
            "source_revision": "SOURCE-1",
            "result": {"learning": {"id": "LEARNING-1", "status": "ACTIVE"}},
            "verification_record": {"verified": True},
            "integration": {"progressive_intelligence_lock_in": True},
        },
        "reread": {
            "source_revision": "SOURCE-1",
            "independent_reread": True,
            "learning": {"id": "LEARNING-1", "status": "ACTIVE"},
            "integration": {"intelligent_block_state": "LEARNED"},
        },
        "evolve": {
            "source_revision": "SOURCE-1",
            "independent_verification": True,
            "authority_inherited": False,
            "related_task": {"task_id": "RELATED-1", "behavior": "REUSE_LESSON"},
            "unrelated_task": {"task_id": "UNRELATED-1", "correct_refusal": True, "behavior": "NO_APPLICABLE_RETAINED_INTELLIGENCE"},
        },
    }


def test_independent_verifier_recomputes_and_requires_distinct_identity():
    result = verify_bundle(bundle(), verifier_jti="VERIFIER-JTI")
    assert result["ok"] is True
    assert result["independent_verification"] is True
    assert result["executor_claim_trusted"] is False
    assert result["verifier_runtime_jti"] == "VERIFIER-JTI"
    assert result["executor_runtime_jti"] == "EXECUTOR-JTI"
    assert result["evidence_refs"]["ACT"] == ["CONTROL-1", "TREATMENT-1"]
    assert result["recomputed"]["source_revision_consistent"] is True


@pytest.mark.parametrize("executor_jti,verifier_jti", [("", "VERIFIER-JTI"), ("EXECUTOR-JTI", ""), ("SAME-JTI", "SAME-JTI")])
def test_missing_or_reused_verifier_identity_is_red(executor_jti, verifier_jti):
    b = bundle()
    b["executor"]["token_jti"] = executor_jti
    result = verify_bundle(b, verifier_jti=verifier_jti)
    assert result["ok"] is False
    assert result["independent_verification"] is False
    assert "verifier_identity" in result["errors"]


def test_forged_executor_independent_claim_cannot_create_verification():
    b = bundle()
    b["executor"]["independent_verification"] = True
    result = verify_bundle(b, verifier_jti="VERIFIER-JTI")
    assert result["ok"] is True
    assert result["executor_claim_trusted"] is False


@pytest.mark.parametrize(
    "mutator,expected_error",
    [
        (lambda b: b["graph"]["behavioral_delta"].update(changed=False), "behavioral_delta"),
        (lambda b: b["graph_verify"]["verification"].update(persisted_pair_re_read=False), "graph_reconstruction"),
        (lambda b: b["promotion"]["result"]["learning"].update(id="LEARNING-2"), "learning_lineage"),
        (lambda b: b["cold"].update(deployed_source_revision="STALE"), "source_revision_consistency"),
        (lambda b: b["promotion"]["verification_record"].update(verified=False), "learning_verification"),
        (lambda b: b["evolve"].update(authority_inherited=True), "authority_noninheritance"),
        (lambda b: b["evolve"]["unrelated_task"].update(correct_refusal=False), "unrelated_refusal"),
    ],
)
def test_mutated_authoritative_evidence_is_red(mutator, expected_error):
    b = bundle()
    mutator(b)
    result = verify_bundle(b, verifier_jti="VERIFIER-JTI")
    assert result["ok"] is False
    assert expected_error in result["errors"]


def test_missing_authoritative_source_receipt_is_red():
    b = bundle()
    del b["cold"]
    result = verify_bundle(b, verifier_jti="VERIFIER-JTI")
    assert result["ok"] is False
    assert "cold" in result["errors"]


def test_stale_lineage_between_components_is_red():
    b = bundle()
    b["reread"]["source_revision"] = "STALE"
    result = verify_bundle(b, verifier_jti="VERIFIER-JTI")
    assert result["ok"] is False
    assert "source_revision_consistency" in result["errors"]


def test_verifier_rejects_assertion_only_graph_proof_without_raw_receipts():
    b = bundle()
    # A producer can make every summary flag look valid while omitting the raw persisted
    # receipts and relationships that an independent verifier must inspect.
    b["graph_verify"]["verification"] = {
        "independently_reconstructed": True,
        "persisted_pair_re_read": True,
        "treatment_relationships_verified": True,
    }
    del b["graph_verify"]["receipts"]
    del b["graph_verify"]["relationships"]
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "graph_raw_evidence" in result["errors"]


def test_verifier_recomputes_graph_delta_from_raw_observed_results():
    b = bundle()
    # Keep all summary assertions green while changing the raw treatment observation.
    # The independent verifier must derive the delta from the raw pair itself.
    b["graph_verify"]["receipts"]["treatment"]["observed_result"] = "BASELINE"
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "graph_raw_evidence" in result["errors"]


def test_executor_self_attestation_fields_are_ignored():
    b = bundle()
    forged = deepcopy(b["executor"])
    forged["independent_verification"] = True
    forged["verifier_runtime_jti"] = "FORGED-SELF-VERIFIER"
    b["executor"] = forged
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI-SECOND",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is True
    assert result["executor_claim_trusted"] is False
    assert result["verifier_runtime_jti"] == "VERIFIER-JTI-SECOND"
    assert result["recomputed"]["verification_basis"] == "INDEPENDENT_COMPONENT_RECOMPUTATION"


def test_consistently_stale_bundle_is_red_when_expected_source_is_current():
    b = bundle()
    b["executor"]["source_revision"] = "STALE"
    b["cold"]["deployed_source_revision"] = "STALE"
    for name in ("graph", "graph_verify", "promotion", "reread", "evolve"):
        b[name]["source_revision"] = "STALE"
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "source_revision_consistency" in result["errors"]


def test_missing_component_source_binding_is_red():
    b = bundle()
    del b["graph"]["source_revision"]
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "source_revision_missing" in result["errors"]


def test_executor_identity_must_match_authoritative_cold_receipt():
    b = bundle()
    b["cold"]["receipt"]["token_jti"] = "DIFFERENT-EXECUTOR"
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "executor_identity_binding" in result["errors"]


def test_missing_control_receipt_is_red():
    b = bundle()
    b["graph"]["control"]["receipt_id"] = ""
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is False
    assert "behavioral_delta" in result["errors"]


@pytest.mark.parametrize("claim", [True, False, "FORGED", None])
def test_executor_verification_claim_never_changes_verdict(claim):
    b = bundle()
    b["executor"]["independent_verification"] = claim
    result = verify_bundle(
        b,
        verifier_jti="VERIFIER-JTI",
        expected_source_revision="SOURCE-1",
    )
    assert result["ok"] is True
    assert result["independent_verification"] is True
    assert result["executor_claim_trusted"] is False
