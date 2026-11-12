"""Machine-falsifiable tests for the canonical learning-lineage receipt.

Every test exercises the REAL reconstructor (tools/learning_lineage_receipt.py),
not a mirror. Fixture shapes are taken from the production writer:
supabase/functions/nayanet-learning-verify/index.ts (candidate insert and
promotion path). A behavior change to the receipt must update this matrix.

Fail-closed contract under test:
  - complete honest chain      -> PARTIAL (5 stages uninstrumented on main)
  - broken link anywhere       -> BROKEN, gap names the exact hop
  - promoted without CVO       -> BROKEN (SN-0340: UNKNOWN != PASS)
  - receipt alone as authority  -> DENIED, always (the #1712 lesson)
  - no forbidden authority fields ever appear on a receipt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from learning_lineage_receipt import (
    FORBIDDEN_AUTHORITY_FIELDS,
    SCHEMA,
    STAGES,
    reconstruct,
    satisfies_authority,
    summarize,
)


def _candidate_bundle(**overrides):
    """Bundle shaped exactly like the learning-verify writer emits."""
    bundle = {
        "cognition_event": {"id": "evt-001", "event_id": "EVT-001", "receipt_id": "rcpt-001"},
        "commit_receipt": {"id": "rcpt-001", "action": "intelligence_commit", "evidence": {}},
        "intelligent_block": {
            "intelligent_block_id": "IB-LEARN-001",
            "understanding_state": "CANDIDATE",
            "evidence_refs": [{"event_id": "evt-001", "receipt_id": "rcpt-001"}],
            "provenance": {},
        },
        "learning": {
            "id": "learn-001",
            "status": "CANDIDATE",
            "level": "E1_UNDERSTANDS",
            "provenance": "OBSERVATION",
            "target_id": "NAYA-NODE-0001",
            "verification_method": "Pending independent causal verification of the persisted chain.",
            "observed_value": {
                "intelligent_block_id": "IB-LEARN-001",
                "source_event_id": "evt-001",
                "source_event_key": "EVT-001",
                "commit_receipt_id": "rcpt-001",
                "lineage_id": "lin-001",
                "relationship_id": "rel-001",
                "index_id": "idx-001",
                "checkpoint_id": "chk-001",
                "checkpoint_provenance": "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT",
                "provenance_preserved": True,
            },
        },
        "relationship": {"relationship_id": "rel-001"},
        "checkpoint": {"id": "chk-001"},
    }
    bundle.update(overrides)
    return bundle


def test_honest_candidate_chain_is_partial_not_broken():
    """A truthful candidate chain: no gaps, but 5 stages are uninstrumented
    on current main -> PARTIAL, never COMPLETE (honest instrumentation gap)."""
    receipt = reconstruct(_candidate_bundle())
    assert receipt["schema"] == SCHEMA
    assert receipt["verdict"] == "PARTIAL", receipt["gaps"]
    assert receipt["gaps"] == []
    assert len(receipt["uninstrumented"]) == 7  # retrieval..successor minus none
    assert set(receipt["stages"].keys()) == set(STAGES)
    assert receipt["stages"]["capture"]["status"] == "PRESENT"
    assert receipt["stages"]["retention"]["status"] == "PRESENT"
    assert receipt["stages"]["verification"]["status"] == "PENDING"
    assert receipt["stages"]["promotion"]["status"] == "PENDING"
    assert "learning.observed_value.intelligent_block_id -> block.intelligent_block_id" in receipt["links_verified"]


def test_broken_relationship_link_fails_closed_with_named_hop():
    bundle = _candidate_bundle()
    bundle["relationship"] = {"relationship_id": "rel-999"}
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("RELATIONSHIP_LINK_BROKEN" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["capture"]["status"] == "PRESENT"  # unaffected stages stay honest


def test_missing_checkpoint_row_fails_closed():
    bundle = _candidate_bundle()
    del bundle["checkpoint"]
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("CHECKPOINT_LINK_BROKEN" in g for g in receipt["gaps"]), receipt["gaps"]


def test_missing_block_fails_closed():
    bundle = _candidate_bundle()
    del bundle["intelligent_block"]
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert "RETENTION_BLOCK_MISSING" in receipt["gaps"]
    assert receipt["stages"]["retention"]["status"] == "GAP"


def test_promotion_without_verification_is_broken():
    """LEARNED/ACTIVE with no CVO evidence -> BROKEN. This is the SN-0340
    UNKNOWN != PASS gate: promotion is not verification."""
    bundle = _candidate_bundle()
    bundle["learning"]["status"] = "ACTIVE"
    bundle["learning"]["provenance"] = "VERIFICATION"
    bundle["intelligent_block"]["understanding_state"] = "LEARNED"
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("PROMOTION_WITHOUT_VERIFICATION" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["verification"]["status"] == "GAP"


def test_promotion_with_cvo_evidence_is_present():
    bundle = _candidate_bundle()
    bundle["learning"]["status"] = "ACTIVE"
    bundle["learning"]["provenance"] = "VERIFICATION"
    bundle["learning"]["verification_method"] = "Independent causal verification CVO-42."
    bundle["intelligent_block"]["understanding_state"] = "LEARNED"
    bundle["intelligent_block"]["evidence_refs"] = [
        {"learning_verification_ref": "CVO-42"},
        {"learning_id": "learn-001", "causal_verification_id": "CVO-42", "receipt_id": "rcpt-001"},
    ]
    bundle["verification"] = {"cvo_id": "CVO-42", "method": "independent causal verification"}
    receipt = reconstruct(bundle)
    assert receipt["stages"]["verification"]["status"] == "PRESENT"
    assert receipt["stages"]["promotion"]["status"] == "PRESENT"
    assert receipt["verdict"] == "PARTIAL"  # later stages still uninstrumented


def test_receipt_alone_never_satisfies_authority():
    """The #1712 lesson, machine-enforced: a fabricated 'perfect' receipt
    with no grant is DENIED. Receipts are evidence, never authority."""
    receipt = reconstruct(_candidate_bundle())
    assert satisfies_authority(receipt) is False
    assert satisfies_authority(receipt, grant=None) is False
    assert satisfies_authority(receipt, grant={}) is False
    # A non-human-rooted grant also denies: the grant is judged, not the receipt.
    assert satisfies_authority(receipt, grant={"human_rooted": False, "grant_id": "g-1"}) is False
    # Only a Human-rooted grant with an id satisfies -- decided by the GRANT.
    assert satisfies_authority(receipt, grant={"human_rooted": True, "grant_id": "g-1"}) is True


def test_receipt_carries_no_forbidden_authority_fields():
    for bundle in (_candidate_bundle(), {}):
        receipt = reconstruct(bundle)
        assert not (FORBIDDEN_AUTHORITY_FIELDS & set(receipt.keys())), receipt.keys()
        for stage in receipt["stages"].values():
            assert not (FORBIDDEN_AUTHORITY_FIELDS & set(stage.keys()))


def test_authority_refs_are_links_only():
    bundle = _candidate_bundle(authority_ref_links=["grant-57d83ce5"])
    receipt = reconstruct(bundle)
    assert receipt["authority_refs"] == ["grant-57d83ce5"]
    # ...yet the receipt alone still satisfies nothing.
    assert satisfies_authority(receipt) is False


def test_malformed_bundle_fails_closed():
    receipt = reconstruct({})
    assert receipt["verdict"] == "BROKEN"
    assert "BUNDLE_MISSING_LEARNING" in receipt["gaps"]
    receipt2 = reconstruct({"learning": "not-a-dict"})
    assert receipt2["verdict"] == "BROKEN"


def test_summarize_is_honest_one_liner():
    receipt = reconstruct(_candidate_bundle())
    line = summarize(receipt)
    assert "learn-001" in line and "PARTIAL" in line and "links only" in line
