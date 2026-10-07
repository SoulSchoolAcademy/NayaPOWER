"""Tests for the runtime proof chain (tools/production_proof_chain.py).

Contract under test:
- chain_receipts binds an ordered receipt sequence into a hash-linked
  bundle; verify_chain recomputes every hash and names the exact broken
  link. Never raises; malformed input is recorded, never invented.
- The chain vouches for EVIDENCE INTEGRITY ONLY. It can never certify
  PROMOTED_AND_PROVEN; that claim stays exclusively with the parent
  deploy-workflow handshake.
- Red->green seam: test_tamper_is_detected and test_reorder_breaks_linkage
  fail against a naive bundle that records receipts without hash linkage,
  and pass once the hash chain is implemented.
"""
import copy
import json

import pytest

from tools.production_proof_chain import (
    CHAIN_SCHEMA,
    GENESIS,
    KNOWN_RECEIPT_SCHEMAS,
    VERIFY_SCHEMA,
    chain_receipts,
    content_hash,
    summarize_chain,
    verify_chain,
)
from tools.production_parity_verdict import build_parity_verdict
from tools.production_promotion_failure_receipt import build_failure_receipt

SHA = "a" * 40
PROMOTED = "b" * 40


def failure_receipt(status_files=None):
    files = {
        "supabase-production-check.json": {"id": 10, "name": "Supabase", "conclusion": "success"},
        "producer-run.json": {"databaseId": 20, "conclusion": "success", "headSha": SHA},
        "proof-run.json": {"databaseId": 30, "conclusion": "failure", "headSha": SHA},
    }
    if status_files:
        files.update(status_files)
    return build_failure_receipt(
        github_sha=SHA,
        production_branch="production",
        promotion_mode="EXPLICIT_HUMAN",
        authorized_source_sha=SHA,
        actor="test",
        workflow_run_id="40",
        env={"DEPLOYMENT_SHA": PROMOTED},
        files=files,
        gates=None,
    )


def parity_verdict():
    return build_parity_verdict(
        promoted_sha=PROMOTED,
        production_tip_sha=PROMOTED,
        functions={
            "nayanet-cold-runtime-proof": {
                "stamp": PROMOTED,
                "source_path": "supabase/functions/nayanet-cold-runtime-proof/index.ts",
                "stamp_is_ancestor_of_promoted": True,
            }
        },
        context={"observed_by": "test"},
    )


def denial_receipt():
    return {
        "schema": "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1",
        "decision": "DENIED",
        "reason": "kernel-tests.yml red at authorized source",
        "source_sha": SHA,
    }


def three_receipt_chain():
    return chain_receipts(
        [failure_receipt(), parity_verdict(), denial_receipt()],
        authorized_source_sha=SHA,
        chained_by="test",
        chain_purpose="production proof bundle for SHA " + SHA[:8],
    )


# ---- happy path ------------------------------------------------------------

def test_chain_round_trip_verifies_intact():
    chain = three_receipt_chain()
    assert chain["schema"] == CHAIN_SCHEMA
    assert chain["link_count"] == 3
    assert chain["genesis"] == GENESIS
    verdict = verify_chain(chain)
    assert verdict["schema"] == VERIFY_SCHEMA
    assert verdict["overall"] == "INTACT"
    assert verdict["integrity_intact"] is True
    assert verdict["chain_head_hash"] == chain["head_hash"]
    assert [l["verdict"] for l in verdict["links"]] == ["INTACT"] * 3
    assert [l["integrity_ok"] for l in verdict["links"]] == [True] * 3


def test_head_hash_is_deterministic():
    assert three_receipt_chain()["head_hash"] == three_receipt_chain()["head_hash"]


def test_genesis_anchors_first_link():
    chain = three_receipt_chain()
    assert chain["links"][0]["prev_link_hash"] == GENESIS
    assert chain["links"][1]["prev_link_hash"] == chain["links"][0]["link_hash"]
    assert chain["links"][2]["prev_link_hash"] == chain["links"][1]["link_hash"]


def test_chain_embeds_exactly_what_was_hashed():
    fr = failure_receipt()
    chain = chain_receipts([fr])
    link = chain["links"][0]
    assert link["receipt"] == fr
    assert link["receipt_hash"] == content_hash(fr)


def test_caller_mutation_after_chaining_does_not_alter_chain():
    fr = failure_receipt()
    chain = chain_receipts([fr])
    fr["status"] = "MUTATED_AFTER_CHAINING"
    assert verify_chain(chain)["overall"] == "INTACT"


# ---- the red->green seam: tamper and reorder detection ----------------------

def test_tamper_is_detected():
    chain = three_receipt_chain()
    tampered = copy.deepcopy(chain)
    # Alter one receipt payload after chaining: flip a proof-leg status.
    tampered["links"][1]["receipt"]["functions"]["nayanet-cold-runtime-proof"]["verdict"] = "DRIFT"
    verdict = verify_chain(tampered)
    assert verdict["overall"] == "BROKEN"
    assert verdict["integrity_intact"] is False
    assert verdict["links"][1]["verdict"] == "TAMPERED"
    assert verdict["links"][1]["integrity_ok"] is False
    # Untouched links still verify.
    assert verdict["links"][0]["verdict"] == "INTACT"
    assert verdict["links"][2]["verdict"] == "INTACT"


def test_envelope_tamper_is_detected():
    chain = three_receipt_chain()
    tampered = copy.deepcopy(chain)
    tampered["links"][0]["prev_link_hash"] = "forged"
    verdict = verify_chain(tampered)
    assert verdict["links"][0]["verdict"] in ("TAMPERED", "BROKEN_LINK")
    assert verdict["overall"] == "BROKEN"


def test_reorder_breaks_linkage():
    chain = three_receipt_chain()
    reordered = copy.deepcopy(chain)
    reordered["links"][0], reordered["links"][1] = reordered["links"][1], reordered["links"][0]
    verdict = verify_chain(reordered)
    assert verdict["overall"] == "BROKEN"
    assert verdict["integrity_intact"] is False
    broken = [l["verdict"] for l in verdict["links"]]
    assert "SEQUENCE_BREAK" in broken or "BROKEN_LINK" in broken


def test_dropped_link_breaks_chain():
    chain = three_receipt_chain()
    dropped = copy.deepcopy(chain)
    del dropped["links"][1]
    verdict = verify_chain(dropped)
    assert verdict["overall"] == "BROKEN"
    assert verdict["links"][1]["verdict"] in ("BROKEN_LINK", "SEQUENCE_BREAK")


# ---- honest degradation -----------------------------------------------------

def test_malformed_receipts_recorded_not_raised():
    chain = chain_receipts([failure_receipt(), "not-a-dict", None, 42])
    assert chain["link_count"] == 4
    verdict = verify_chain(chain)
    assert verdict["overall"] == "BROKEN"
    assert verdict["links"][0]["verdict"] == "INTACT"
    assert [l["verdict"] for l in verdict["links"][1:]] == ["MALFORMED_RECEIPT"] * 3
    # The chain mechanics are still sound: successors committed to the
    # malformed links honestly.
    assert verdict["integrity_intact"] is True


def test_unknown_schema_flagged_but_integrity_holds():
    odd = {"schema": "SOMETHING_ELSE_V9", "data": [1, 2, 3]}
    chain = chain_receipts([failure_receipt(), odd])
    verdict = verify_chain(chain)
    assert verdict["links"][1]["verdict"] == "UNKNOWN_SCHEMA"
    assert verdict["links"][1]["integrity_ok"] is True
    assert verdict["overall"] == "BROKEN"
    assert verdict["integrity_intact"] is True


def test_schema_absent_flagged():
    chain = chain_receipts([{"no_schema_field": True}])
    verdict = verify_chain(chain)
    assert verdict["links"][0]["verdict"] == "UNKNOWN_SCHEMA"
    assert verdict["overall"] == "BROKEN"


def test_unserializable_receipt_cannot_be_proven():
    chain = chain_receipts([{"schema": "NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1", "bad": object()}])
    assert chain["links"][0]["schema"] == "MALFORMED_RECEIPT"
    assert chain["links"][0]["receipt"] is None
    verdict = verify_chain(chain)
    assert verdict["links"][0]["verdict"] == "MALFORMED_RECEIPT"


def test_empty_chain_proves_nothing():
    verdict = verify_chain(chain_receipts([]))
    assert verdict["overall"] == "UNKNOWN"
    assert verdict["reason"] == "EMPTY_CHAIN_PROVES_NOTHING"


def test_verify_rejects_garbage_without_raising():
    for bad in (None, "chain", 42, [], {}, {"schema": "WRONG"}):
        verdict = verify_chain(bad)
        assert verdict["overall"] == "UNKNOWN", bad
        assert verdict["schema"] == VERIFY_SCHEMA


def test_chain_rejects_garbage_input_without_raising():
    for bad in (None, "receipts", 42, {"not": "a list"}):
        chain = chain_receipts(bad)
        assert chain["schema"] == CHAIN_SCHEMA
        assert chain["link_count"] == 0


def test_known_schemas_registry_matches_production_receipts():
    assert "NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1" in KNOWN_RECEIPT_SCHEMAS
    assert "NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1" in KNOWN_RECEIPT_SCHEMAS
    assert "NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1" in KNOWN_RECEIPT_SCHEMAS
    assert "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1" in KNOWN_RECEIPT_SCHEMAS
    assert "NAYAPOWER_PRODUCTION_READINESS_CHECKLIST_V1" in KNOWN_RECEIPT_SCHEMAS


# ---- authority boundary: integrity only, never promotion --------------------

def _collect_claims(obj):
    """Collect every (path, value) pair from a nested structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield (k, v)
            yield from _collect_claims(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _collect_claims(v)


def test_chain_certifies_nothing_about_promotion():
    fr = failure_receipt()
    # PROMOTED_BUT_UNPROVEN: the fixture deploys but a proof leg failed --
    # the strongest honest case for this test.
    assert fr["status"] in ("DEPLOY_FAILED", "PROMOTED_BUT_UNPROVEN")
    chain = chain_receipts([fr], authorized_source_sha=SHA)
    assert verify_chain(chain)["overall"] == "INTACT"
    assert chain["authority_boundary"]["certifies_promotion"] is False
    assert chain["authority_boundary"]["certifies_evidence_integrity_only"] is True
    # No receipt embedded in the chain may carry the promotion claim as a
    # *value*: the chain may name the term in its boundary note (to
    # disclaim it, as the sibling modules do), but it must never assert it.
    for key, value in _collect_claims(chain["links"]):
        assert value != "PROMOTED_AND_PROVEN", f"chain asserts promotion at {key}"
    for link in chain["links"]:
        receipt = link["receipt"]
        if isinstance(receipt, dict):
            assert receipt.get("status") != "PROMOTED_AND_PROVEN"


def test_summarize_chain_restates_claims_without_verifying():
    chain = three_receipt_chain()
    summary = summarize_chain(chain)
    assert summary["chain_id"] == chain["chain_id"]
    assert summary["head_short"] == chain["head_hash"][:12]
    assert summary["link_count"] == 3
    assert summary["schemas"] == [
        "NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1",
        "NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1",
        "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1",
    ]
    assert summarize_chain({"nope": True})["error"] == "NOT_A_PROOF_CHAIN"


def test_chain_is_deterministic_and_pure():
    c1 = three_receipt_chain()
    c2 = three_receipt_chain()
    assert c1 == c2
