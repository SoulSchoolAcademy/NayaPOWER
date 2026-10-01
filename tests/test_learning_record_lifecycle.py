"""Adversarial tests for the LEARN record lifecycle spec (#864, thicken-domains).

The lifecycle's job is to make the 07-LEARNING pipeline machine-checkable:
a stage claim is honored only when the evidence that stage's gate requires
is present. A stored note is not learning; a candidate is not verified
learning; compounding without measured behavioral effect is rejected;
learning never changes authority. UNKNOWN != PASS.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_learning_record_lifecycle",
    ROOT / "tools" / "validate_learning_record_lifecycle.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
failures = _mod.failures
STAGES = _mod.STAGES

FIXTURE = ROOT / "BRAIN/07-LEARNING/0002-LEARNING-RECORD-LIFECYCLE-V1.json"


def valid_record_at(stage, record_id="LR-TEST-001"):
    idx = STAGES.index(stage)
    return {
        "record_id": record_id,
        "stage": stage,
        "stage_history": STAGES[: idx + 1],
        "outcome": "ACTIVE",
        "preserved": True,
        "observation_ref": "test observation",
        "reconciliation_note": "test reconciliation",
        "applicability_conditions": ["condition a"],
        "verification_evidence": ["evidence 1"],
        "adoption_record": "test adoption",
        "authority_check": {"changes_authority": False, "note": "no authority implications"},
        "behavioral_effect": {"measured": True, "before": "before-x", "after": "after-x"},
        "compounding_record": "test compounding",
        "contradicted_by": None,
        "rejection_reason": None,
    }


@pytest.fixture()
def lifecycle():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def lifecycle_with(lifecycle, records):
    data = copy.deepcopy(lifecycle)
    data["records"] = records
    return data


def test_real_lifecycle_file_validates_green(lifecycle):
    assert failures(lifecycle) == []


def test_stage_skip_rejected(lifecycle):
    rec = valid_record_at("OBSERVE")
    rec["stage"] = "VERIFY"
    rec["stage_history"] = ["OBSERVE", "VERIFY"]
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_backward_transition_rejected(lifecycle):
    # A record that was at VERIFY cannot re-appear at CANDIDATE: the frozen
    # history no longer matches the claimed stage, and the mismatch fires.
    rec = valid_record_at("VERIFY")
    rec["stage"] = "CANDIDATE"
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_fractional_stage_rejected(lifecycle):
    rec = valid_record_at("MEASURE")
    rec["stage"] = "MEASURE.5"
    rec["stage_history"] = STAGES[: STAGES.index("MEASURE") + 1]
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("STAGE_INVALID" in f for f in fails)


def test_unknown_stage_rejected(lifecycle):
    rec = valid_record_at("OBSERVE")
    rec["stage"] = "LEARN"
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("STAGE_INVALID" in f for f in fails)


def test_stage_history_mismatch_rejected(lifecycle):
    rec = valid_record_at("MEASURE")
    rec["stage_history"] = ["OBSERVE", "MEASURE"]
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_note_without_observation_ref_rejected(lifecycle):
    # A stored note is not learning: OBSERVE requires an observation ref.
    rec = valid_record_at("OBSERVE")
    rec["observation_ref"] = ""
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("OBSERVE_EVIDENCE_MISSING" in f for f in fails)


def test_candidate_without_applicability_rejected(lifecycle):
    rec = valid_record_at("CANDIDATE")
    rec["applicability_conditions"] = []
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("CANDIDATE_EVIDENCE_MISSING" in f for f in fails)


def test_compound_without_measurement_rejected(lifecycle):
    # Measurement is the only promotion path from MEASURE to COMPOUND.
    rec = valid_record_at("COMPOUND")
    rec["behavioral_effect"]["measured"] = False
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("MEASURE_EVIDENCE_MISSING" in f for f in fails)


def test_compound_without_compounding_record_rejected(lifecycle):
    rec = valid_record_at("COMPOUND")
    rec["compounding_record"] = "  "
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("COMPOUND_EVIDENCE_MISSING" in f for f in fails)


def test_authority_claim_rejected(lifecycle):
    # Learning never changes authority: changes_authority == true is a
    # hard rejection, not a learning record.
    rec = valid_record_at("ADOPT")
    rec["authority_check"]["changes_authority"] = True
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("AUTHORITY_CLAIM_REJECTED" in f for f in fails)


def test_adopt_without_adoption_record_rejected(lifecycle):
    rec = valid_record_at("ADOPT")
    rec["adoption_record"] = ""
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("ADOPT_EVIDENCE_MISSING" in f for f in fails)


def test_contradicted_without_preserved_rejected(lifecycle):
    # Contradicted learnings are preserved and marked, never deleted.
    rec = valid_record_at("MEASURE")
    rec["outcome"] = "CONTRADICTED"
    rec["contradicted_by"] = "LR-OTHER-001"
    rec["preserved"] = False
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("CONTRADICTION_NOT_PRESERVED" in f for f in fails)


def test_contradicted_without_contradicted_by_rejected(lifecycle):
    rec = valid_record_at("MEASURE")
    rec["outcome"] = "CONTRADICTED"
    rec["preserved"] = True
    rec["contradicted_by"] = None
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("CONTRADICTION_NOT_PRESERVED" in f for f in fails)


def test_rejected_without_reason_rejected(lifecycle):
    rec = valid_record_at("CANDIDATE")
    rec["outcome"] = "REJECTED"
    rec["rejection_reason"] = None
    fails = failures(lifecycle_with(lifecycle, [rec]))
    assert any("REJECTION_REASON_MISSING" in f for f in fails)


def test_duplicate_record_id_rejected(lifecycle):
    recs = [valid_record_at("OBSERVE", "LR-DUP"), valid_record_at("CANDIDATE", "LR-DUP")]
    fails = failures(lifecycle_with(lifecycle, recs))
    assert any("RECORD_ID_DUPLICATE" in f for f in fails)


def test_canonical_status_without_ratification_rejected(lifecycle):
    data = lifecycle_with(lifecycle, [valid_record_at("OBSERVE")])
    data["status"] = "CANONICAL"
    fails = failures(data)
    assert any("STATUS_NOT_PROPOSED_CANONICAL" in f for f in fails)


def test_as_of_must_be_pinned_sha(lifecycle):
    data = lifecycle_with(lifecycle, [valid_record_at("OBSERVE")])
    data["as_of"] = "main"
    fails = failures(data)
    assert any("AS_OF_NOT_PINNED_SHA" in f for f in fails)


def test_schema_mismatch_rejected(lifecycle):
    data = lifecycle_with(lifecycle, [valid_record_at("OBSERVE")])
    data["schema"] = "naya.other.v1"
    fails = failures(data)
    assert any("SCHEMA_MISMATCH" in f for f in fails)
