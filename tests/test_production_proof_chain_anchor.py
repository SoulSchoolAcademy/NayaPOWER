"""Tests for tools/production_proof_chain_anchor.py.

The anchor is the public commitment for a proof chain: it publishes the
chain head hash and receipt sequence so the whole team can detect later
bundle substitution. The anchor certifies evidence integrity only --
never promotion.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import production_proof_chain as ppc
import production_proof_chain_anchor as anchor


def _receipt(schema, status):
    return {"schema": schema, "status": status, "source_sha": "a" * 40}


def _built_chain_and_verification():
    chain = ppc.chain_receipts(
        [
            _receipt("NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1", "BLOCKED"),
            _receipt("NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1", "STALE"),
        ],
        authorized_source_sha="b" * 40,
        chained_by="naya5/prod-proof-builder",
        chain_purpose="test",
    )
    return chain, ppc.verify_chain(chain)


def test_anchor_happy_path():
    chain, ver = _built_chain_and_verification()
    assert ver["overall"] == "INTACT"
    a = anchor.build_anchor(
        chain, ver,
        {"authorized_source_sha": "b" * 40, "workflow_run_id": 37994773730,
         "anchored_by": "naya5/prod-proof-builder", "anchored_at": "2026-10-09T21:45:00Z"},
    )
    assert a["schema"] == anchor.ANCHOR_SCHEMA
    assert a["status"] == "ANCHORED"
    assert a["anchor_id"] and a["anchor_id"].startswith("pca-")
    assert a["head_hash"] == chain["head_hash"]
    assert a["link_count"] == 2
    assert len(a["links"]) == 2
    assert a["links"][0]["receipt_status"] == {"status": "BLOCKED"}
    assert a["links"][1]["receipt_status"] == {"status": "STALE"}
    # authority boundary is explicit and denies promotion certification
    ab = a["authority_boundary"]
    assert ab["certifies_evidence_integrity_only"] is True
    assert ab["certifies_promotion"] is False
    assert ab["authorizes_deployment"] is False


def test_verify_anchor_intact():
    chain, ver = _built_chain_and_verification()
    a = anchor.build_anchor(chain, ver, {"workflow_run_id": 1})
    result = anchor.verify_anchor(a, chain)
    assert result["verdict"] == "INTACT"
    assert result["mismatched_fields"] == []


def test_verify_anchor_detects_tampering():
    chain, ver = _built_chain_and_verification()
    a = anchor.build_anchor(chain, ver, {"workflow_run_id": 1})
    tampered = json.loads(json.dumps(chain))
    tampered["links"][0]["receipt"]["status"] = "PROMOTED_AND_PROVEN"
    result = anchor.verify_anchor(a, tampered)
    assert result["verdict"] == "TAMPERED"
    # Layer 1 (bundle re-verification) catches the edited receipt before
    # field comparison runs: the receipt hash no longer matches.
    assert "bundle_integrity" in result["mismatched_fields"]


def test_verify_anchor_detects_dropped_link():
    chain, ver = _built_chain_and_verification()
    a = anchor.build_anchor(chain, ver, {"workflow_run_id": 1})
    dropped = json.loads(json.dumps(chain))
    dropped["links"] = dropped["links"][:1]
    result = anchor.verify_anchor(a, dropped)
    assert result["verdict"] == "TAMPERED"
    assert "link_count" in result["mismatched_fields"]


def test_anchor_refuses_non_intact_chain():
    chain, _ = _built_chain_and_verification()
    bad_ver = {"overall": "BROKEN", "chain_head_hash": chain["head_hash"]}
    a = anchor.build_anchor(chain, bad_ver, {"workflow_run_id": 1})
    assert a["status"] == "NOT_ANCHORABLE"
    assert a["anchor_id"] is None
    assert a["anchor_reason"]


def test_anchor_refuses_head_hash_mismatch():
    chain, ver = _built_chain_and_verification()
    ver2 = dict(ver)
    ver2["chain_head_hash"] = "0" * 64
    a = anchor.build_anchor(chain, ver2, {"workflow_run_id": 1})
    assert a["status"] == "NOT_ANCHORABLE"


def test_anchor_never_raises_on_malformed_input():
    for bad_chain in (None, "nope", {"links": "notalist"}, {}):
        a = anchor.build_anchor(bad_chain, None, None)
        assert a["schema"] == anchor.ANCHOR_SCHEMA
        assert a["status"] in ("NOT_ANCHORABLE", "INVALID_INPUT")
    r = anchor.verify_anchor(None, None)
    assert r["verdict"] == "UNKNOWN"
    r2 = anchor.verify_anchor({"schema": "WRONG"}, {"head_hash": "x"})
    assert r2["verdict"] == "UNKNOWN"


def test_verify_anchor_rejects_non_anchored_record():
    chain, _ = _built_chain_and_verification()
    a = anchor.build_anchor(chain, {"overall": "BROKEN"}, {})
    r = anchor.verify_anchor(a, chain)
    assert r["verdict"] == "UNKNOWN"


def test_summarize_anchor():
    chain, ver = _built_chain_and_verification()
    a = anchor.build_anchor(chain, ver, {"workflow_run_id": 37994773730})
    s = anchor.summarize_anchor(a)
    assert s["status"] == "ANCHORED"
    assert s["head_short"] == chain["head_hash"][:12]
    assert s["link_count"] == 2
    assert s["workflow_run_id"] == 37994773730
