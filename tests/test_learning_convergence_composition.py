"""Convergence composition seam test: the learning instruments composed end to end.

Exercises the REAL modules on one tree, proving the convergence audit items
compose instead of merely coexisting:

  assembler  tools/learning_lineage_bundle_assembler.py  (B: live-row bundles)
  receipt    tools/learning_lineage_receipt.py           (B: reconstruct)
  D          tools/learning_application_receipt.py       (D: retrieval ->
             application -> outcome + independent verification)
  C          tools/learning_evidence_assembler.py        (C: receipt-driven
             evidence for the ladder)
  ladder     tools/learning_evidence_ladder.py           (C: E0-E7 evaluation)
  scorer     tools/learning_yield_scorer.py              (d: yields/retention/
             mastery over the composed population)
  gate       tools/verified_verdict_gate.py              (VERIFIED verdicts,
             the Pair-C 5-point bar as code)

Composition claims under test:
  1. A bundle assembled from persisted rows scores capture PRESENT end to
     end (assembler -> reconstruct -> scorer).
  2. D receipts attached to that bundle turn retrieval / applicability /
     application / outcome from UNINSTRUMENTED into PRESENT (the B<->D seam),
     and the scorer's application/outcome yields resolve to 1.0 instead of
     None.
  3. A ladder evaluation on C-assembled evidence earns E2 from a real D
     application receipt and E3 from an independently verified outcome
     (the C<->D seam): the ladder accepts what the D instrument emits,
     through the evidence assembler's real mapping.
  4. A gate-VERIFIED verdict receipt feeds the scorer's
     verified_verdict_yield (the d<->gate seam): the scorer keys to the
     published schema contract, and the gate emits it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import learning_application_receipt as d_receipts
import learning_evidence_assembler as evidence
import learning_evidence_ladder as ladder
import learning_lineage_bundle_assembler as assembler
import learning_lineage_receipt as lineage
import learning_yield_scorer as scorer
import verified_verdict_gate as vvg

TS = "2026-10-10T16:00:00Z"
LESSON = "L-COMP-1"


def _rows(**over):
    rows = {
        "learning": {
            "id": LESSON,
            "created_at": TS,
            "target_id": "NAYA-NODE-0001",
            # CANDIDATE, not promoted: the composition claim under test is
            # capture/retrieval/application, not the promotion gate.
            "status": "CANDIDATE",
            "observed_value": {
                "intelligent_block_id": "IB-COMP-207f611c16714130876db60ad70cffb3",
                "source_event_id": "cog-comp-1",
                "commit_receipt_id": "commit-comp-1",
                "lineage_id": "0892ac0e-84ed-4d70-85ab-9ebf2f5beef9",
                "relationship_id": "ea47ace5-bbd9-4950-859f-ad07f02a04ed",
                "index_id": "0ba65341-e7ed-46f1-9293-64da368df7d6",
                "checkpoint_id": "a58dc3f0-5968-43dc-98ad-c31930777096",
            },
        },
        "cognition_event": {
            "id": "cog-comp-1",
            "event_id": "NAYA-FLOW-COMP-207f611c16714130876db60ad70cffb3",
            "type": "intelligence",
            "status": "active",
            "created_at": TS,
        },
        "commit_receipt": {
            "id": "commit-comp-1",
            "action": "intelligence_commit",
            "status": "SUCCESS",
            "created_at": TS,
        },
        "intelligent_block": {
            "intelligent_block_id": "IB-COMP-207f611c16714130876db60ad70cffb3",
            "understanding_state": "LEARNED",
            "status": "DURABLE",
            "created_at": TS,
            "evidence_refs": [
                {"event_id": "cog-comp-1", "receipt_id": "commit-comp-1"},
            ],
            "provenance": {"stage": "CAPTURE+PERSIST", "learning_id": LESSON},
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
    rows.update(over)
    return rows


def _full_d_chain(lesson_id=LESSON, applier="naya-5", verifier="naya-1"):
    """A complete retrieval -> application -> outcome chain with an
    independent verifier (distinct from the applier)."""
    retrieval = d_receipts.emit_retrieval_receipt(
        lesson_id=lesson_id, retriever=applier, retrieved_at=TS,
        query_context="composition check", lesson_content_sha="sha256:comp",
        source_refs=["cog-comp-1"],
    )
    application = d_receipts.emit_application_receipt(
        lesson_id=lesson_id, retrieval_ref=retrieval["receipt_id"],
        task_ref="task-comp-1", applier=applier, applied_at=TS,
        applicability={"relevance_rationale": "direct seam", "task_match": "direct"},
    )
    outcome = d_receipts.emit_outcome_record(
        application_receipt_id=application["receipt_id"], lesson_id=lesson_id,
        task_ref="task-comp-1", measured_effect="stages resolve PRESENT",
        observed_at=TS, outcome_ref="exec-comp-1",
        independent_verification={"verifier": verifier, "verified_at": TS},
    )
    return retrieval, application, outcome


def _passing_verdict_request(scorer_id="naya-1"):
    """A verdict request that earns VERIFIED under the 5-point bar."""
    arms = []
    for task in ("task-a", "task-b", "task-c"):
        arms.append(vvg.Arm(task_name=task, lesson_provided=False,
                            artifact="control-artifact", doer_id="doer-1"))
        arms.append(vvg.Arm(task_name=task, lesson_provided=True,
                            artifact="TREATED: good", doer_id="doer-1"))

    def machine_check(artifact):
        return isinstance(artifact, str) and artifact.startswith("TREATED")

    return vvg.VerdictRequest(
        claim="the treatment causes the check to pass",
        falsifiable="control parses where treatment fails",
        task_family="composition-family",
        success_criterion="machine_check(artifact) is True",
        machine_check=machine_check,
        arms=arms,
        scorer_id=scorer_id,
        blind=True,
        preregistered_at="2026-10-10T00:00:00Z",
        seen_tasks=frozenset(),
    )


def _evaluate(lesson_id, bundle, claimed_level, comprehension=None):
    assembled = evidence.assemble_evidence(
        lesson_id, bundle, comprehension=comprehension)
    return ladder.evaluate({
        "id": lesson_id,
        "claimed_level": claimed_level,
        "evidence": assembled["evidence"],
    })


def _comprehension(verifier="naya-1"):
    """E1 witness: paired control/treatment receipts, independently verified."""
    return {
        "control_receipt": "ctrl-receipt-comp-1",
        "treatment_receipt": "treat-receipt-comp-1",
        "independent_verifier": verifier,
        "verified_at": TS,
    }


# ---------------------------------------------------------------------------
# 1. assembler -> reconstruct -> scorer
# ---------------------------------------------------------------------------

def test_assembled_bundle_scores_capture_present_end_to_end():
    bundle = assembler.assemble_bundle(_rows())
    receipt = lineage.reconstruct(bundle)
    assert receipt["stages"]["capture"]["status"] == "PRESENT", receipt["gaps"]

    score = scorer.score_population({"chains": [bundle], "captured_total": 1})
    assert score["verdict"] in ("PARTIAL", "VERIFIED"), score["verdict"]
    assert score["yield"]["stages"]["capture"]["value"] == 1.0
    assert score["skipped"] == []


def test_assembled_bundle_carries_created_at_to_c_evidence():
    """The B->C composition seam (carry fix): the assembled bundle keeps
    created_at so the C-side evidence assembler has E0 capture evidence."""
    bundle = assembler.assemble_bundle(_rows())
    assert bundle["learning"].get("created_at") == TS


# ---------------------------------------------------------------------------
# 2. B <-> D seam
# ---------------------------------------------------------------------------

def test_d_receipts_resolve_application_stages_from_uninstrumented():
    retrieval, application, outcome = _full_d_chain()
    bundle = d_receipts.attach_to_lineage_bundle(
        assembler.assemble_bundle(_rows()),
        retrieval_receipt=retrieval,
        application_receipt=application,
        outcome_record=outcome,
    )
    receipt = lineage.reconstruct(bundle)
    for stage in ("retrieval", "applicability", "application", "outcome"):
        assert receipt["stages"][stage]["status"] == "PRESENT", (
            stage, receipt["stages"][stage].get("note"), receipt["gaps"])

    score = scorer.score_population({"chains": [bundle], "captured_total": 1})
    assert score["yield"]["headline"]["application_yield"]["value"] == 1.0
    assert score["yield"]["headline"]["outcome_yield"]["value"] == 1.0


def test_d_receipt_without_outcome_leaves_outcome_honestly_uninstrumented():
    retrieval, application, _ = _full_d_chain()
    bundle = d_receipts.attach_to_lineage_bundle(
        assembler.assemble_bundle(_rows()),
        retrieval_receipt=retrieval,
        application_receipt=application,
    )
    score = scorer.score_population({"chains": [bundle], "captured_total": 1})
    assert score["yield"]["headline"]["application_yield"]["value"] == 1.0
    oy = score["yield"]["headline"]["outcome_yield"]
    # No outcome record was ever emitted for this chain: the receipt marks
    # the stage UNINSTRUMENTED and the scorer says None with the reason
    # named -- never a fabricated 0.0 and never a silent gap.
    assert oy["value"] is None
    assert "UNINSTRUMENTED" in oy["reason"]


# ---------------------------------------------------------------------------
# 3. C <-> D seam: the ladder earns levels from real D receipts
# ---------------------------------------------------------------------------

def test_ladder_earns_e2_from_real_d_application_receipt():
    retrieval, application, _ = _full_d_chain()
    bundle = d_receipts.attach_to_lineage_bundle(
        assembler.assemble_bundle(_rows()),
        retrieval_receipt=retrieval,
        application_receipt=application)
    evaluation = _evaluate(LESSON, bundle, "E2_CAN_DO",
                         comprehension=_comprehension())
    assert evaluation["earned_level"] == "E2_CAN_DO", evaluation


def test_ladder_earns_e3_from_independently_verified_outcome():
    retrieval, application, outcome = _full_d_chain()
    bundle = d_receipts.attach_to_lineage_bundle(
        assembler.assemble_bundle(_rows()),
        retrieval_receipt=retrieval,
        application_receipt=application,
        outcome_record=outcome)
    evaluation = _evaluate(LESSON, bundle, "E3_INDEPENDENT",
                         comprehension=_comprehension())
    assert evaluation["earned_level"] == "E3_INDEPENDENT", evaluation


def test_self_attested_outcome_caps_below_e3():
    """The E3 falsifier end to end: verifier == applier earns E2, not E3."""
    retrieval, application, _ = _full_d_chain()
    outcome_self = d_receipts.emit_outcome_record(
        application_receipt_id=application["receipt_id"], lesson_id=LESSON,
        task_ref="task-comp-1", measured_effect="looks good to me",
        observed_at=TS,
        independent_verification={"verifier": "naya-5", "verified_at": TS},
    )
    bundle = d_receipts.attach_to_lineage_bundle(
        assembler.assemble_bundle(_rows()),
        retrieval_receipt=retrieval,
        application_receipt=application,
        outcome_record=outcome_self)
    evaluation = _evaluate(LESSON, bundle, "E3_INDEPENDENT",
                         comprehension=_comprehension())
    assert evaluation["earned_level"] == "E2_CAN_DO", evaluation
    assert evaluation["verdict"] == "REJECTED"


# ---------------------------------------------------------------------------
# 4. d <-> gate seam: gate receipts feed the scorer's verdict yield
# ---------------------------------------------------------------------------

def test_gate_verdict_receipt_feeds_scorer_verdict_yield():
    result = vvg.verdict(_passing_verdict_request())
    assert result["verdict"] == "VERIFIED", result["rule_trace"]
    assert result["schema"] == scorer.VERIFIED_VERDICT_SCHEMA
    assert vvg.verify_receipt(result)

    bundle = assembler.assemble_bundle(_rows())
    score = scorer.score_population(
        {"chains": [bundle], "verdict_receipts": [result], "captured_total": 1})
    assert score["yield"]["headline"]["verified_verdict_yield"]["value"] == 1.0
    assert score["yield"]["headline"]["verified_verdict_receipts"]["valid"] == 1


def test_gate_not_verified_never_counts_as_support():
    bad = vvg.verdict(vvg.VerdictRequest(
        claim="x", falsifiable="y", task_family="z",
        success_criterion="c", machine_check=None, scorer_id="naya-1"))
    assert bad["verdict"] == "NOT_VERIFIED"
    bundle = assembler.assemble_bundle(_rows())
    score = scorer.score_population(
        {"chains": [bundle], "verdict_receipts": [bad], "captured_total": 1})
    assert score["yield"]["headline"]["verified_verdict_yield"]["value"] == 0.0
    assert score["yield"]["headline"]["verified_verdict_receipts"]["valid"] == 1
