"""Machine-falsifiable tests for the learning yield / retention / mastery scorer.

Every test exercises the REAL scorer (tools/learning_yield_scorer.py), the
REAL lineage reconstructor, and (for ladder fixtures) the REAL ladder
evaluator -- not mirrors. A behavior change to any of them must update
this matrix.

Fail-closed contract under test:
  - empty population        -> INSUFFICIENT_DATA, never 0.0
  - full honest chain       -> stage yields 1.0 over instrumented stages;
                               reuse/generalization/successor stay None
                               (UNINSTRUMENTED), population verdict PARTIAL
  - broken chain            -> BROKEN, exact stage yields below 1.0
  - zero denominators       -> None + named reason, never a ratio
  - malformed entries       -> skipped + named, scorer never raises
  - mastery                 -> earned_level wins over claimed_level;
                               advancements count only with ladder evidence
  - tamper                  -> score_id changes with the inputs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import learning_evidence_ladder as ladder
import learning_lineage_receipt as llr
import learning_yield_scorer as scorer


# --------------------------------------------------------------------------
# Fixture builders (shapes follow the real contracts)
# --------------------------------------------------------------------------

def _d_receipt(kind, **fields):
    rec = {"schema": llr._EVIDENCE_SCHEMA[kind]}
    rec.update(fields)
    rec[llr._EVIDENCE_ID_FIELD[kind]] = llr._recompute_evidence_id(kind, rec)
    return rec


def _full_bundle(lid="L-1"):
    """A bundle whose B receipt has every instrumented stage PRESENT."""
    retr = _d_receipt(
        "retrieval", lesson_id=lid, retriever="naya-test",
        retrieved_at="2026-10-05T00:00:00Z", query_context="q",
        lesson_content_sha="abc")
    app = _d_receipt(
        "application", lesson_id=lid, retrieval_ref=retr["receipt_id"],
        task_ref="task-1", applier="naya-test", applied_at="2026-10-06T00:00:00Z",
        applicability={"relevance_rationale": "matches", "task_match": "high"})
    out = _d_receipt(
        "outcome", lesson_id=lid, application_receipt_id=app["receipt_id"],
        task_ref="task-1", measured_effect={"delta": 0.5},
        observed_at="2026-10-07T00:00:00Z",
        independent_verification={"verifier": "naya-blind", "method": "paired"})
    return {
        "learning": {
            "id": lid, "status": "ACTIVE", "level": "E1_UNDERSTANDS",
            "observed_value": {
                "source_event_id": "evt-1", "commit_receipt_id": "cr-1",
                "intelligent_block_id": "IB-1", "lineage_id": "lin-1",
                "relationship_id": "rel-1", "index_id": "idx-1",
                "checkpoint_id": "chk-1"}},
        "cognition_event": {"id": "evt-1", "event_id": "EVT-1"},
        "commit_receipt": {"id": "cr-1", "action": "intelligence_commit"},
        "intelligent_block": {
            "intelligent_block_id": "IB-1", "understanding_state": "LEARNED",
            "evidence_refs": [{"causal_verification_id": "CVO-1"}]},
        "relationship": {"relationship_id": "rel-1"},
        "checkpoint": {"id": "chk-1"},  # B contract: bundle rows carry id
                                       # (assembler's checkpoint.checkpoint_id -> id rename)
        "retrieval_receipts": [retr],
        "application_receipts": [app],
        "outcome_records": [out],
    }


def _ladder_eval(lid, evidence, claimed):
    return ladder.evaluate({
        "id": lid, "target": "NAYA-NODE-0001", "producer_id": "prod-1",
        "evidence": evidence, "claimed_level": claimed})


_E1_EVIDENCE = {
    "capture_receipt": {"intelligent_block_id": "ib", "captured_at": "2026-10-01T00:00:00Z"},
    "comprehension": {"control_receipt": "c", "treatment_receipt": "t",
                      "independent_verifier": "verifier-x", "verified_at": "2026-10-02T00:00:00Z"},
}
_E2_EVIDENCE = dict(_E1_EVIDENCE, application_receipt={
    "retrieval_ref": "r", "task_ref": "t", "applied_at": "2026-10-03T00:00:00Z",
    "applier": "naya-test"})


def _verdict_receipt(lid, verdict="VERIFIED"):
    return {"schema": scorer.VERIFIED_VERDICT_SCHEMA, "learning_id": lid,
            "verdict": verdict}


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_empty_population_is_insufficient_data():
    s1 = scorer.score_population({})
    s2 = scorer.score_population({"chains": []})
    for s in (s1, s2):
        assert s["schema"] == scorer.SCHEMA
        assert s["verdict"] == "INSUFFICIENT_DATA"
        assert "yield" not in s  # no ratios manufactured from nothing
    assert s1["score_id"] == s2["score_id"]  # deterministic


def test_full_chain_yields_one_over_instrumented():
    pop = {
        "chains": [_full_bundle("L-1")],
        "ladder_evaluations": [_ladder_eval("L-1", _E2_EVIDENCE, "E2_CAN_DO")],
        "verdict_receipts": [_verdict_receipt("L-1")],
    }
    s = scorer.score_population(pop)
    stages = s["yield"]["stages"]
    for stage in ("capture", "retention", "retrieval", "applicability",
                  "application", "outcome", "verification", "promotion"):
        assert stages[stage]["value"] == 1.0, stage
    # Uninstrumented stages never get a ratio.
    for stage in ("reuse", "generalization", "successor"):
        assert stages[stage]["value"] is None, stage
        assert "UNINSTRUMENTED" in stages[stage]["reason"], stage
    h = s["yield"]["headline"]
    assert h["verification_yield"]["value"] == 1.0
    assert h["application_yield"]["value"] == 1.0
    assert h["outcome_yield"]["value"] == 1.0
    assert h["reuse_yield"]["value"] is None
    assert h["verified_verdict_yield"]["value"] == 1.0
    # Population can never be COMPLETE while successor lanes lack emitters.
    assert s["verdict"] == "PARTIAL"


def test_broken_chain_is_broken_with_honest_stage_yields():
    broken = _full_bundle("L-2")
    del broken["cognition_event"]  # capture GAP
    s = scorer.score_population({"chains": [_full_bundle("L-1"), broken]})
    assert s["verdict"] == "BROKEN"
    assert s["yield"]["stages"]["capture"]["value"] == 0.5
    assert s["yield"]["stages"]["capture"]["numerator"] == 1
    assert s["yield"]["stages"]["capture"]["denominator"] == 2
    assert s["yield"]["stages"]["application"]["value"] == 1.0


def test_malformed_entries_are_skipped_not_raised():
    # Non-dict bundles are the B receipt's own jurisdiction: reconstruct
    # scores them BROKEN (BUNDLE_MISSING_LEARNING) rather than raising, so
    # the scorer counts them as scored-with-verdict -- consistent delegation.
    s = scorer.score_population({
        "chains": ["not-a-bundle", 42, _full_bundle("L-1")],
        "ladder_evaluations": [{"nope": True}],
        "verdict_receipts": [{"schema": "WRONG", "learning_id": "L-1"}],
        "level_transitions": ["garbage"],
    })
    assert s["population"]["chains_scored"] == 3
    assert s["verdict"] == "BROKEN"
    assert any("ladder_evaluations[0]" in x for x in s["skipped"])
    assert any("verdict_receipts[0]" in x for x in s["skipped"])
    assert any("level_transitions[0]" in x for x in s["skipped"])
    # And a bundle-shaped-but-garbage dict never raises either.
    s2 = scorer.score_population({"chains": [{"learning": "nope"}]})
    assert s2["verdict"] == "BROKEN"


def test_mastery_uses_earned_level_not_claimed():
    overclaim = _ladder_eval("L-1", _E1_EVIDENCE, "E2_CAN_DO")
    assert overclaim["earned_level"] == "E1_UNDERSTANDS"
    assert overclaim["verdict"] == "REJECTED"
    s = scorer.score_population({
        "chains": [_full_bundle("L-1")],
        "ladder_evaluations": [overclaim, _ladder_eval("L-2", _E2_EVIDENCE, "E2_CAN_DO")],
    })
    dist = s["mastery"]["distribution"]
    assert dist["E1_UNDERSTANDS"] == 1
    assert dist["E2_CAN_DO"] == 1
    assert s["mastery"]["claimed_above_earned"] == 1
    assert s["mastery"]["evaluated"] == 2


def test_advancements_count_only_with_ladder_evidence():
    s = scorer.score_population({
        "chains": [_full_bundle("L-1"), _full_bundle("L-2")],
        "ladder_evaluations": [
            _ladder_eval("L-1", _E2_EVIDENCE, "E2_CAN_DO"),   # earned E2
            _ladder_eval("L-2", _E1_EVIDENCE, "E1_UNDERSTANDS"),  # earned E1
        ],
        "level_transitions": [
            {"learning_id": "L-1", "from_level": "E1_UNDERSTANDS",
             "to_level": "E2_CAN_DO", "evidence_ref": "r1"},   # counts
            {"learning_id": "L-2", "from_level": "E1_UNDERSTANDS",
             "to_level": "E2_CAN_DO", "evidence_ref": "r2"},   # does NOT count
            {"learning_id": "L-3", "from_level": "E0_EXPOSED",
             "to_level": "E1_UNDERSTANDS", "evidence_ref": "r3"},  # no eval: skipped
        ],
    })
    adv = s["mastery"]["advancements"]
    assert adv["counted"] == 1
    assert adv["claims"] == 2
    assert adv["share"]["value"] == 0.5
    assert any("L-3" in x for x in s["skipped"])


def test_retention_fresh_decayed_unknown():
    pop = {
        "chains": [_full_bundle("L-1"), _full_bundle("L-2"), _full_bundle("L-3")],
        "activity": {
            "L-1": {"last_evidence_at": "2026-10-09T00:00:00Z"},  # 1 day old
            "L-2": {"last_evidence_at": "2026-08-01T00:00:00Z"},  # 70 days old
            # L-3: no timestamp -> UNKNOWN, never assumed decayed
        },
        "as_of": "2026-10-10T00:00:00Z",
        "retention_window_days": 30,
    }
    r = scorer.score_population(pop)["retention"]
    assert r["retained"] == 1 and r["decayed"] == 1 and r["unknown"] == 1
    assert r["retention_share"]["value"] == 0.5
    assert r["retention_share"]["denominator"] == 2


def test_no_timestamps_means_unscorable_not_zero():
    r = scorer.score_population({"chains": [_full_bundle("L-1")]})["retention"]
    assert r["unknown"] == 1
    assert r["retention_share"]["value"] is None
    assert "unscorable" in r["retention_share"]["reason"]


def test_score_id_is_tamper_evident_and_stable():
    pop = {"chains": [_full_bundle("L-1")]}
    a = scorer.score_population(pop)
    b = scorer.score_population(pop)
    assert a["score_id"] == b["score_id"]
    tampered = {"chains": [_full_bundle("L-1")]}
    tampered["chains"][0]["learning"]["status"] = "RETIRED"
    c = scorer.score_population(tampered)
    assert c["score_id"] != a["score_id"]
    assert c["score_id"].startswith("YLD-")


def test_captured_total_sets_headline_denominators():
    pop = {"chains": [_full_bundle("L-1")], "captured_total": 10,
           "verdict_receipts": [_verdict_receipt("L-1")]}
    s = scorer.score_population(pop)
    h = s["yield"]["headline"]
    assert h["verification_yield"]["denominator"] == 10
    assert h["verification_yield"]["value"] == 0.1
    assert h["verified_verdict_yield"]["denominator"] == 10
    assert s["population"]["denominator_basis"] == "captured_total"
    # Stage yields stay over scored chains, not the population.
    assert s["yield"]["stages"]["capture"]["denominator"] == 1


def test_summarize_is_one_line():
    s = scorer.score_population({"chains": [_full_bundle("L-1")]})
    line = scorer.summarize(s)
    assert "\n" not in line
    assert s["score_id"] in line
    assert "PARTIAL" in line
