"""Machine-falsifiable tests for the live-row lineage bundle assembler.

The money test (test_real_live_bundle_reconstructs_partial_with_zero_gaps)
runs the REAL receipt reconstructor over a bundle assembled from REAL
production rows captured read-only 2026-10-09 -- not hand-shaped fixtures.
If the assembler drifts from live shapes, or the receipt's contract drifts
from the assembler, this test goes red. That is the convergence-B claim
made falsifiable: end-to-end lineage reconstructability on live data.

Live source (sb-api, read-only, 2026-10-09 ~21:50Z):
  learning 37dfeec3-f120-42e0-a971-5aee95f0b537 (ACTIVE / E1_UNDERSTANDS /
    VERIFICATION, target NAYA-NODE-0001) with observed_value link set
  event 73a2c4a8-64cb-4e92-9fbf-8be38646b4cb (NAYA-FLOW-LESSON-207f...)
  execution receipt e94cd65b-17c9-47b1-8623-cfd87593b410 (intelligence_commit)
  block IB-NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3 (LEARNED/DURABLE)
  relationship ea47ace5-bbd9-4950-859f-ad07f02a04ed (PRODUCES)
  checkpoint a58dc3f0-5968-43dc-98ad-c31930777096 (COGNITIVE_CHECKPOINT)
  lineage 0892ac0e-84ed-4d70-85ab-9ebf2f5beef9 (CREATED_INTELLIGENT_BLOCK)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from learning_lineage_bundle_assembler import (
    SCHEMA as ASSEMBLY_SCHEMA,
    assemble_bundle,
    summarize_assembly,
)
from learning_lineage_receipt import reconstruct


def _live_rows(**overrides):
    """Rows exactly as the production tables returned them 2026-10-09."""
    rows = {
        "learning": {
            "id": "37dfeec3-f120-42e0-a971-5aee95f0b537",
            "target_id": "NAYA-NODE-0001",
            "level": "E1_UNDERSTANDS",
            "provenance": "VERIFICATION",
            "status": "ACTIVE",
            "verification_method": (
                "Independent causal-learning runtime verification: "
                "control/treatment outcome delta recomputed from persisted receipts."
            ),
            "observed_value": {
                "intelligent_block_id": "IB-NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3",
                "source_event_id": "73a2c4a8-64cb-4e92-9fbf-8be38646b4cb",
                "source_event_key": "NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3",
                "commit_receipt_id": "e94cd65b-17c9-47b1-8623-cfd87593b410",
                "lineage_id": "0892ac0e-84ed-4d70-85ab-9ebf2f5beef9",
                "relationship_id": "ea47ace5-bbd9-4950-859f-ad07f02a04ed",
                "index_id": "0ba65341-e7ed-46f1-9293-64da368df7d6",
                "checkpoint_id": "a58dc3f0-5968-43dc-98ad-c31930777096",
                "checkpoint_provenance": "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT",
                "provenance_preserved": True,
            },
        },
        "cognition_event": {
            "id": "73a2c4a8-64cb-4e92-9fbf-8be38646b4cb",
            "event_id": "NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3",
            "type": "intelligence",
            "status": "active",
        },
        "commit_receipt": {
            "id": "e94cd65b-17c9-47b1-8623-cfd87593b410",
            "action": "intelligence_commit",
            "status": "SUCCESS",
        },
        "intelligent_block": {
            "intelligent_block_id": "IB-NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3",
            "understanding_state": "LEARNED",
            "status": "DURABLE",
            "evidence_refs": [
                {"event_id": "73a2c4a8-64cb-4e92-9fbf-8be38646b4cb",
                 "receipt_id": "e94cd65b-17c9-47b1-8623-cfd87593b410"},
                {"causal_verification_id": "CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-09-28"},
            ],
            "provenance": {
                "stage": "CAPTURE+PERSIST",
                "learning_id": "37dfeec3-f120-42e0-a971-5aee95f0b537",
                "law_authority_refs": ["fc1a4311-ede1-443b-9824-5bf140fda8a0"],
            },
        },
        "relationship": {
            "relationship_id": "ea47ace5-bbd9-4950-859f-ad07f02a04ed",
            "relationship_type": "PRODUCES",
            "status": "ACTIVE",
        },
        "checkpoint": {
            "checkpoint_id": "a58dc3f0-5968-43dc-98ad-c31930777096",
            "checkpoint_type": "COGNITIVE_CHECKPOINT",
            "status": "LEARNED",
        },
    }
    rows.update(overrides)
    return rows


def test_real_live_bundle_reconstructs_partial_with_zero_gaps():
    """The convergence-B proof on live data: a real learning's real rows
    assemble into a bundle the real receipt reconstructs with NO gaps.
    PARTIAL is the honest ceiling -- retrieval..outcome and
    reuse..successor have no emitters yet (7 uninstrumented)."""
    bundle = assemble_bundle(_live_rows())
    assert bundle["assembly_schema"] == ASSEMBLY_SCHEMA
    assert bundle["assembly_notes"] == [], bundle["assembly_notes"]

    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "PARTIAL", receipt["gaps"]
    assert receipt["gaps"] == []
    assert len(receipt["uninstrumented"]) == 7
    assert receipt["stages"]["capture"]["status"] == "PRESENT"
    assert receipt["stages"]["retention"]["status"] == "PRESENT"
    assert receipt["stages"]["verification"]["status"] == "PRESENT"
    assert receipt["stages"]["promotion"]["status"] == "PRESENT"
    assert receipt["stages"]["verification"]["refs"]["ref"] == \
        "CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-09-28"
    assert "fc1a4311-ede1-443b-9824-5bf140fda8a0" in receipt["authority_refs"]
    # authority_refs are links only -- the receipt never becomes authority
    assert "learning.observed_value.source_event_id -> cognition_event.id" in \
        receipt["links_verified"]


def test_checkpoint_id_rename_is_the_seam():
    """The checkpoint table's PK is checkpoint_id; the receipt reads
    bundle['checkpoint']['id']. The assembler owns that rename."""
    bundle = assemble_bundle(_live_rows())
    assert bundle["checkpoint"] == {"id": "a58dc3f0-5968-43dc-98ad-c31930777096"}
    receipt = reconstruct(bundle)
    assert not any("CHECKPOINT" in g for g in receipt["gaps"]), receipt["gaps"]


def test_missing_checkpoint_row_is_honest_gap_not_fabrication():
    """The reader never invents a row to satisfy the receipt: omit the
    checkpoint row and the bundle says so; the receipt reports the exact
    broken hop."""
    rows = _live_rows()
    del rows["checkpoint"]
    bundle = assemble_bundle(rows)
    assert "checkpoint" not in bundle
    assert any("ROW_ABSENT" in n and "checkpoint" in n for n in bundle["assembly_notes"]), \
        bundle["assembly_notes"]
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("CHECKPOINT_LINK_BROKEN" in g for g in receipt["gaps"]), receipt["gaps"]


def test_tier1_row_without_links_assembles_learning_only():
    """Tier-1 rows (E5_CAN_TEACH, Naya-1-verified 2026-10-08) carry zero
    lineage links in observed_value. The assembler passes the learning
    through, notes every absent row, and fabricates nothing."""
    rows = {
        "learning": {
            "id": "tier1-T14",
            "status": "ACTIVE",
            "level": "E5_CAN_TEACH",
            "target_id": "lesson:TIER1-2026-10-08-T14",
            "provenance": "VERIFICATION",
            "verification_method": "Independent verification by Naya 1.",
            "observed_value": {
                "n": 20, "trial": "Trial-14", "tier_s": "MET",
                "p_value": 0.0007, "cohens_h": 1.1,
            },
        }
    }
    bundle = assemble_bundle(rows)
    assert bundle["learning"]["id"] == "tier1-T14"
    assert "cognition_event" not in bundle
    assert "intelligent_block" not in bundle
    absent = [n for n in bundle["assembly_notes"] if n.startswith("ROW_ABSENT")]
    assert len(absent) == 5, bundle["assembly_notes"]  # every expected table row
    # ("verification" is caller-supplied and optional -- its absence is the
    # normal path, not a gap, so it is never a ROW_ABSENT note.)
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("LINEAGE_ID_MISSING_FROM_OBSERVED_VALUE" in g for g in receipt["gaps"])


def test_malformed_input_never_raises():
    for bad in (None, "rows", 42, [], {"learning": "not-a-dict"},
                {"learning": {"id": "x"}},  # observed_value missing
                _live_rows(cognition_event="not-a-dict")):
        bundle = assemble_bundle(bad)
        assert isinstance(bundle["assembly_notes"], list)
        assert bundle["assembly_notes"], bad  # something was said about it
        receipt = reconstruct(bundle)  # must not raise either
        assert receipt["verdict"] == "BROKEN"


def test_d_receipts_pass_through_untouched():
    """D-shaped receipts ride the bundle to the receipt, which verifies
    their digests -- the assembler never rewrites them."""
    retrieval = [{"schema": "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1",
                  "receipt_id": "RET-abc", "lesson_id": "37dfeec3-f120-42e0-a971-5aee95f0b537"}]
    bundle = assemble_bundle(_live_rows(retrieval_receipts=retrieval))
    assert bundle["retrieval_receipts"] == retrieval
    assert bundle["retrieval_receipts"][0] is retrieval[0]  # identical object

    bundle2 = assemble_bundle(_live_rows(application_receipts="not-a-list"))
    assert "application_receipts" not in bundle2
    assert any("D_KEY_NOT_LIST" in n for n in bundle2["assembly_notes"])


def test_verification_row_passthrough():
    bundle = assemble_bundle(_live_rows(
        verification={"cvo_id": "CVO-1", "method": "independent"}))
    assert bundle["verification"] == {"cvo_id": "CVO-1", "method": "independent"}

    # empty cvo_id: the row carries nothing -> omitted, receipt falls back
    # to block evidence_refs
    bundle2 = assemble_bundle(_live_rows(verification={"cvo_id": "", "method": "x"}))
    assert "verification" not in bundle2
    assert any("VERIFICATION_ROW_EMPTY" in n for n in bundle2["assembly_notes"])

    # cvo_id key entirely absent: malformed row, named as such
    bundle3 = assemble_bundle(_live_rows(verification={"method": "x"}))
    assert "verification" not in bundle3
    assert any("ROW_FIELD_MISSING" in n and "verification.cvo_id" in n
               for n in bundle3["assembly_notes"])


def test_authority_refs_shape_checked():
    bundle = assemble_bundle(_live_rows(authority_ref_links=["grant-1"]))
    assert bundle["authority_ref_links"] == ["grant-1"]
    bundle2 = assemble_bundle(_live_rows(authority_ref_links="grant-1"))
    assert "authority_ref_links" not in bundle2
    assert any("AUTHORITY_REFS_MALFORMED" in n for n in bundle2["assembly_notes"])


def test_summarize_assembly():
    bundle = assemble_bundle(_live_rows())
    line = summarize_assembly(bundle)
    assert "37dfeec3-f120-42e0-a971-5aee95f0b537" in line
    assert "0 assembly note(s)" in line
    line2 = summarize_assembly(assemble_bundle({"learning": {"id": "x"}}))
    assert "x" in line2 and "assembly note(s)" in line2


def _live_rows_with_timestamps():
    """The live fixture plus the created_at columns the real tables carry
    (the 2026-10-09 capture used a column subset; these are the live values
    for the same rows, fetched read-only 2026-10-10)."""
    rows = _live_rows()
    rows["cognition_event"] = dict(rows["cognition_event"],
                                   created_at="2026-10-08T03:05:02.663586+00:00")
    rows["commit_receipt"] = dict(rows["commit_receipt"],
                                  created_at="2026-10-08T03:05:03.100000+00:00")
    rows["intelligent_block"] = dict(rows["intelligent_block"],
                                     created_at="2026-10-08T03:05:02.663586+00:00")
    return rows


def test_created_at_carried_when_present():
    """The C-side evidence assembler needs a capture timestamp on the
    event/commit rows (E0 evidence). The reader carries it when the source
    row has it."""
    bundle = assemble_bundle(_live_rows_with_timestamps())
    assert bundle["assembly_notes"] == [], bundle["assembly_notes"]
    assert bundle["cognition_event"]["created_at"] == \
        "2026-10-08T03:05:02.663586+00:00"
    assert bundle["commit_receipt"]["created_at"] == \
        "2026-10-08T03:05:03.100000+00:00"
    assert bundle["intelligent_block"]["created_at"] == \
        "2026-10-08T03:05:02.663586+00:00"


def test_created_at_absent_is_silent_not_a_gap():
    """created_at is optional carry, not a required receipt field: rows
    without it assemble cleanly (the money test's notes==[] assertion
    already pins this; this test names the rule)."""
    bundle = assemble_bundle(_live_rows())  # no created_at anywhere
    assert bundle["assembly_notes"] == []
    assert "created_at" not in bundle["cognition_event"]
    assert "created_at" not in bundle["commit_receipt"]


def test_b_to_c_composition_earns_e0_on_live_shaped_rows():
    """THE convergence seam, made falsifiable: B's reader -> B's receipt ->
    C's evidence assembler -> C's ladder. With capture timestamps carried,
    a live-shaped learning earns E0_EXPOSED (capture proven). Without them
    the ladder honestly caps at UNPROVEN -- the exact failure the 2026-10-10
    live exercise found (143/143 UNPROVEN before the carry fix)."""
    import learning_evidence_assembler as evassembler
    import learning_evidence_ladder as ladder

    bundle = assemble_bundle(_live_rows_with_timestamps())
    receipt = reconstruct(bundle)
    assert receipt["stages"]["capture"]["status"] == "PRESENT"

    lid = "37dfeec3-f120-42e0-a971-5aee95f0b537"
    ev = evassembler.assemble_evidence(lid, bundle)
    assert ev["evidence"].get("capture_receipt", {}).get(
        "intelligent_block_id") == \
        "IB-NAYA-FLOW-LESSON-207f611c16714130876db60ad70cffb3"

    record = {"id": lid, "target": "NAYA-NODE-0001",
              "producer_id": "member-1", "claimed_level": "E1_UNDERSTANDS",
              "evidence": ev["evidence"]}
    evaluation = ladder.evaluate(record)
    assert evaluation["earned_level"] == "E0_EXPOSED", evaluation
    # E1 stays unproven: live evidence_refs carry no control/treatment
    # verification records -- the ladder caps honestly, not silently.
    assert "E1_UNDERSTANDS" not in evaluation["proven_chain"]


def test_b_to_c_composition_without_timestamps_is_honestly_unproven():
    """Without capture timestamps the C evidence assembler finds no E0
    evidence and the ladder reports UNPROVEN -- a named honest cap, not a
    crash and not a silent pass."""
    import learning_evidence_assembler as evassembler
    import learning_evidence_ladder as ladder

    bundle = assemble_bundle(_live_rows())  # no created_at anywhere
    lid = "37dfeec3-f120-42e0-a971-5aee95f0b537"
    ev = evassembler.assemble_evidence(lid, bundle)
    assert "capture_receipt" not in ev["evidence"]
    record = {"id": lid, "claimed_level": "E1_UNDERSTANDS",
              "evidence": ev["evidence"]}
    evaluation = ladder.evaluate(record)
    assert evaluation["earned_level"] == "UNPROVEN"
    assert evaluation["verdict"] == "UNPROVEN"
