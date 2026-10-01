"""Adversarial tests for the EVOLUTION self-optimization loop spec (#864, thicken-domains).

The loop's job is to make the 09-EVOLUTION loop machine-checkable:
a stage claim is honored only when the evidence that stage's gate requires
is present. Self-building without self-authorizing; no rollback plan, no
advance; improvement that cannot be measured cannot be adopted; the loop
closes into 07-LEARNING, not at ADOPT. UNKNOWN != PASS.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_evolution_self_optimization",
    ROOT / "tools" / "validate_evolution_self_optimization.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
failures = _mod.failures
STAGES = _mod.STAGES

FIXTURE = ROOT / "BRAIN/09-EVOLUTION/0002-EVOLUTION-SELF-OPTIMIZATION-V1.json"


def valid_proposal_at(stage, proposal_id="EV-TEST-001"):
    idx = STAGES.index(stage)
    return {
        "proposal_id": proposal_id,
        "stage": stage,
        "stage_history": STAGES[: idx + 1],
        "outcome": "ACTIVE",
        "observation_ref": "verified gap: duplicate graph seams return divergent answers",
        "diagnosis": "two selectors compute the same function from divergent roots",
        "proposal": "reconcile CONNECT into one canonical seam pinned at an exact revision",
        "impact_assessment": {
            "dependencies": ["graph selector", "registry"],
            "blast_radius": "docs + selector wiring only; no runtime behavior change",
            "rollback_plan": "revert the reconciliation commit (single git revert)",
        },
        "authority_check": {
            "authority": "standing autonomy for bounded reversible build-loop work",
            "changes_authority": False,
            "note": "no authority implications",
        },
        "build_record": "reconciled seam committed on branch brain-build/connect-seam",
        "test_evidence": ["6/6 seam regression tests green on exact pushed bytes"],
        "verification_evidence": ["independent reviewer confirmed single canonical seam"],
        "measurement": {"measured": True, "before": "2 divergent answers", "after": "1 answer"},
        "adoption_record": "merged PR #1218 note: adoption of the canonical seam text",
        "learning_record": "07-LEARNING record EV-loop closure reference",
        "rejection_reason": None,
        "rollback_record": None,
        "superseded_by": None,
    }


@pytest.fixture()
def evolution():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def evolution_with(evolution, proposals):
    data = copy.deepcopy(evolution)
    data["proposals"] = proposals
    return data


def test_fixture_passes_validation(evolution):
    assert failures(evolution) == []


def test_loop_is_eleven_stages_in_contract_order(evolution):
    assert evolution["stages"] == [
        "OBSERVE", "DIAGNOSE", "PROPOSE", "IMPACT-CHECK", "AUTHORIZE",
        "BUILD", "TEST", "VERIFY", "MEASURE", "ADOPT", "LEARN",
    ]


def test_status_must_remain_proposed_canonical(evolution):
    bad = copy.deepcopy(evolution)
    bad["status"] = "CANONICAL"
    fails = failures(bad)
    assert any("STATUS_NOT_PROPOSED_CANONICAL" in f for f in fails)


def test_wrong_schema_rejected(evolution):
    bad = copy.deepcopy(evolution)
    bad["schema"] = "naya.evolution-self-optimization.v99"
    fails = failures(bad)
    assert any("SCHEMA_MISMATCH" in f for f in fails)


def test_as_of_must_be_pinned_sha(evolution):
    bad = copy.deepcopy(evolution)
    bad["as_of"] = "latest"
    fails = failures(bad)
    assert any("AS_OF_NOT_PINNED_SHA" in f for f in fails)


def test_skip_a_stage_fails(evolution):
    bad = valid_proposal_at("PROPOSE")
    bad["stage_history"] = ["OBSERVE", "PROPOSE"]  # skipped DIAGNOSE
    fails = failures(evolution_with(evolution, [bad]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_backward_move_fails(evolution):
    bad = valid_proposal_at("BUILD")
    bad["stage"] = "DIAGNOSE"  # history still claims BUILD-depth
    fails = failures(evolution_with(evolution, [bad]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_missing_observation_ref_fails(evolution):
    bad = valid_proposal_at("OBSERVE")
    bad["observation_ref"] = "   "
    fails = failures(evolution_with(evolution, [bad]))
    assert any("OBSERVE_EVIDENCE_MISSING" in f for f in fails)


def test_missing_diagnosis_fails(evolution):
    bad = valid_proposal_at("DIAGNOSE")
    del bad["diagnosis"]
    fails = failures(evolution_with(evolution, [bad]))
    assert any("DIAGNOSE_EVIDENCE_MISSING" in f for f in fails)


def test_vague_proposal_fails(evolution):
    bad = valid_proposal_at("PROPOSE")
    bad["proposal"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("PROPOSE_EVIDENCE_MISSING" in f for f in fails)


def test_missing_rollback_plan_fails(evolution):
    bad = valid_proposal_at("IMPACT-CHECK")
    bad["impact_assessment"]["rollback_plan"] = "TBD"
    fails = failures(evolution_with(evolution, [bad]))
    assert any("IMPACT_INCOMPLETE" in f for f in fails)


def test_missing_blast_radius_fails(evolution):
    bad = valid_proposal_at("IMPACT-CHECK")
    bad["impact_assessment"]["blast_radius"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("IMPACT_INCOMPLETE" in f for f in fails)


def test_unnamed_authority_fails(evolution):
    bad = valid_proposal_at("AUTHORIZE")
    bad["authority_check"]["authority"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("AUTHORITY_UNNAMED" in f for f in fails)


def test_authority_change_rejected(evolution):
    bad = valid_proposal_at("AUTHORIZE")
    bad["authority_check"]["changes_authority"] = True
    fails = failures(evolution_with(evolution, [bad]))
    assert any("AUTHORITY_CHANGE_REJECTED" in f for f in fails)


def test_self_authorization_rejected(evolution):
    bad = valid_proposal_at("AUTHORIZE")
    bad["authority_check"]["authority"] = "authorized by this loop itself"
    fails = failures(evolution_with(evolution, [bad]))
    assert any("SELF_AUTHORIZATION_REJECTED" in f for f in fails)


def test_adoption_without_measurement_fails(evolution):
    bad = valid_proposal_at("ADOPT")
    bad["measurement"]["measured"] = False
    fails = failures(evolution_with(evolution, [bad]))
    assert any("ADOPTION_UNMEASURED" in f for f in fails)


def test_adoption_without_before_after_fails(evolution):
    bad = valid_proposal_at("MEASURE")
    bad["measurement"]["after"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("MEASURE_EVIDENCE_MISSING" in f for f in fails)


def test_learn_requires_learning_record(evolution):
    bad = valid_proposal_at("LEARN")
    bad["learning_record"] = None
    fails = failures(evolution_with(evolution, [bad]))
    assert any("LEARN_EVIDENCE_MISSING" in f for f in fails)


def test_empty_test_evidence_fails(evolution):
    bad = valid_proposal_at("TEST")
    bad["test_evidence"] = []
    fails = failures(evolution_with(evolution, [bad]))
    assert any("TEST_EVIDENCE_MISSING" in f for f in fails)


def test_rejected_needs_rejection_reason(evolution):
    bad = valid_proposal_at("PROPOSE")
    bad["outcome"] = "REJECTED"
    bad["rejection_reason"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("REJECTION_REASON_MISSING" in f for f in fails)


def test_rolled_back_needs_rollback_record(evolution):
    bad = valid_proposal_at("VERIFY")
    bad["outcome"] = "ROLLED_BACK"
    bad["rollback_record"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("ROLLBACK_RECORD_MISSING" in f for f in fails)


def test_superseded_needs_superseded_by(evolution):
    bad = valid_proposal_at("PROPOSE")
    bad["outcome"] = "SUPERSEDED"
    bad["superseded_by"] = ""
    fails = failures(evolution_with(evolution, [bad]))
    assert any("SUPERSEDED_BY_MISSING" in f for f in fails)


def test_duplicate_proposal_ids_rejected(evolution):
    a = valid_proposal_at("OBSERVE", "EV-DUP")
    b = valid_proposal_at("DIAGNOSE", "EV-DUP")
    fails = failures(evolution_with(evolution, [a, b]))
    assert any("PROPOSAL_ID_DUPLICATE" in f for f in fails)


def test_worked_example_is_fully_evidenced(evolution):
    ex = next(
        p for p in evolution["proposals"] if p["proposal_id"] == "EV-2026-09-30-ghapi-backtick-quoting"
    )
    assert ex["stage"] == "LEARN"
    assert ex["outcome"] == "ADOPTED"
    assert ex["stage_history"] == STAGES
    assert ex["authority_check"]["changes_authority"] is False
    assert ex["measurement"]["measured"] is True
    assert ex["learning_record"]
    # The full gate chain applies to the worked example too.
    fails = failures(evolution_with(evolution, [ex]))
    assert fails == []
