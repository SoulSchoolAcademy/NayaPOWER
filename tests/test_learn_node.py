"""Proof tests for the LEARN node — the inheritance mechanism.

What these prove (and what they don't):
- PROVEN: only VERIFY-admitted lessons enter the usable set (rejected,
  NOT_VERIFIED, and raw candidates are refused loudly); admitted lessons are
  frozen with full provenance; a FRESH LearnNode process (never saw the
  admission) inherits every lesson from the durable store; serve() retrieves
  by intent overlap (not ID lookup); every serving is recorded; a candidate
  smuggled into the store is quarantined and never served; supersession
  retires old versions without rewriting history.
- NOT PROVEN here: that a decision APPLIED the served lesson (WO4/WO5b
  territory — LEARN records the serving, the handoff point); semantic
  understanding (intent matching is structured overlap, honestly bounded).

Shawn's law under test: verified lessons are frozen at 10 and every new Naya
is BORN with them — not taught, inherited.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from orchestrator.learn_node import (  # noqa: E402
    LEARN_SCHEMA,
    LearnAdmissionRefused,
    LearnNode,
    intent_match_score,
)
from orchestrator import NodeOrchestrator, RunStatus, StageStatus  # noqa: E402
from orchestrator.executors import LocalExecutor  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "tools"))
from learning_admission_gate import ADMISSION_SCHEMA  # noqa: E402


# --------------------------------------------------------------------------
# Fixtures: a VERIFY-admitted lesson and the verdict that admitted it.
# --------------------------------------------------------------------------

def make_lesson(lesson_id="SN-LEARN-001", **overrides):
    lesson = {
        "lesson_id": lesson_id,
        "version": 1,
        "lesson_text": (
            "A learning candidate must carry a falsifiable claim with a "
            "substantive falsification condition. A negation-paraphrase of "
            "the claim is a tautology wearing a costume — it can never fail "
            "independently of the claim itself, so it proves nothing."
        ),
        "intent_signature": {
            "domains": ["learning", "verification", "admission"],
            "situations": [
                "admission-gate",
                "candidate-design",
                "falsification-check",
                "tautology-detection",
            ],
            "decision_types": ["admit", "reject", "validate"],
        },
    }
    lesson.update(overrides)
    return lesson


def make_verify_result(**overrides):
    """A VERIFY stage output for a lesson VERIFY admitted as CANDIDATE."""
    result = {
        "admitted": True,
        "admitted_as": "CANDIDATE",
        "reason_codes": [],
        "correlation_id": "corr-verify-001",
        "falsification_condition": (
            "If a candidate with a negation-paraphrase falsification condition "
            "is admitted, the claim is wrong."
        ),
        "doer": "naya-5",
        "scorer": "naya-2",
        "measurement_method": "machine",
    }
    result.update(overrides)
    return result


def make_candidate(lesson_id="SN-LEARN-001"):
    """A candidate that passes the real admission gate."""
    return {
        "schema": ADMISSION_SCHEMA,
        "claim": (
            "Candidates with negation-paraphrase falsification conditions "
            "are tautologies and must be rejected at the admission door."
        ),
        "falsification_condition": (
            "Admit a candidate whose falsification restates the claim with "
            "negations stripped, then check whether the gate rejects it."
        ),
        "task": "learn-node-proof",
        "lesson_id": lesson_id,
        "success_criterion": "The gate rejects the tautological candidate with TAUTOLOGICAL_FALSIFICATION.",
        "criterion_independent_of_lesson": True,
        "criterion_registered_at": "2026-10-09T09:00:00Z",
        "doer": "naya-5",
        "scorer": "naya-2",
        "measurement": {"method": "machine", "detail": "gate verdict inspection"},
        "arms": {
            "treatment": {"observable": "tautological candidate submitted", "measured_at": "2026-10-09T10:00:00Z"},
            "control": {"observable": "substantive candidate submitted", "measured_at": "2026-10-09T10:05:00Z"},
        },
        "asserts_behavioral_change": True,
        "behavioral_measure": "gate rejection with reason code",
        "outcome": "pending",
    }


def make_capture_with_lesson(lesson_id="SN-LEARN-001"):
    return {
        "lesson_id": lesson_id,
        "owner_id": "owner-1",
        "naya_id": "naya-1",
        "identity": {"actor_id": "naya-1", "system_id": "nayapower", "role": "learner"},
        "mission": "prove the learning loop",
        "objective": "admit a lesson through the orchestrator and inherit it",
        "candidate": make_candidate(lesson_id),
        "lesson": make_lesson(lesson_id),
    }


# --------------------------------------------------------------------------
# 1. THE INHERITANCE PROOF: admit through the orchestrator, serve from a
#    fresh process that never saw the admission.
# --------------------------------------------------------------------------

def test_inheritance_admit_through_orchestrator_serve_from_fresh_process(tmp_path):
    learn_store = tmp_path / "learn_store"
    executor = LocalExecutor(
        continuity_dir=tmp_path / "continuity",
        learn_store_dir=learn_store,
    )
    orch = NodeOrchestrator(executor, store_root=tmp_path / "orchestrator")

    capture = make_capture_with_lesson("SN-LEARN-INHERIT")
    event_id = orch.commit_capture(
        capture["lesson_id"],
        json.dumps(capture["candidate"], sort_keys=True)[:200],
    )
    record = orch.run(event_id, capture)

    # LEARN executed through the orchestrator — no longer NOT_IMPLEMENTED.
    learn_rec = record.stages["LEARN"]
    assert learn_rec.status == StageStatus.COMPLETED.value, (
        f"{learn_rec.status} {learn_rec.error_message}"
    )
    receipt = executor._learn_node().get_lesson("SN-LEARN-INHERIT")
    assert receipt is not None
    assert receipt.frozen is True
    assert receipt.status == "ACTIVE"

    # FRESH PROCESS: a new LearnNode on the same store. It never called
    # admit(). It never saw the lesson. It is born with it.
    fresh_node = LearnNode(learn_store)
    assert fresh_node.active_lesson_count() == 1
    inherited = fresh_node.get_lesson("SN-LEARN-INHERIT")
    assert inherited is not None
    assert inherited.provenance["admitted_by"] == "VERIFY"
    assert inherited.provenance["admitted_as"] == "CANDIDATE"

    # A fresh DECISION CONTEXT: a situation the lesson covers. NO lesson ID
    # anywhere in the context — the lesson must arrive by intent.
    context = {
        "correlation_id": "fresh-decision-ctx-001",
        "intent": {
            "domains": ["learning", "verification"],
            "situation": (
                "I am designing a learning candidate and need to check whether "
                "my falsification condition is substantive or a tautology"
            ),
            "situation_keywords": ["candidate-design", "falsification-check"],
            "decision_type": "validate",
        },
    }
    assert "SN-LEARN-INHERIT" not in json.dumps(context)

    result = fresh_node.serve(context)

    # The lesson arrives — by intent, with its full provenance.
    assert len(result["served"]) == 1
    served = result["served"][0]
    assert served["lesson_id"] == "SN-LEARN-INHERIT"
    assert served["match_score"] >= 0.5
    assert "tautology" in served["lesson_text"]
    assert served["provenance"]["admitted_by"] == "VERIFY"
    assert served["provenance"]["doer"] == "naya-5"
    assert served["provenance"]["scorer"] == "naya-2"

    # The serving is recorded — the handoff point for WO4/WO5b.
    servings = fresh_node.servings()
    assert len(servings) == 1
    assert servings[0]["decision_correlation_id"] == "fresh-decision-ctx-001"
    assert servings[0]["lessons_served"][0]["lesson_id"] == "SN-LEARN-INHERIT"


def test_unrelated_situation_gets_no_lesson(tmp_path):
    """Intent matching is real: a situation the lesson doesn't cover gets nothing."""
    node = LearnNode(tmp_path / "store")
    node.admit(make_verify_result(), make_lesson("SN-LEARN-UNRELATED"))

    context = {
        "correlation_id": "ctx-unrelated-001",
        "intent": {
            "domains": ["interface", "design"],
            "situation": "choosing button colors for the hub",
            "situation_keywords": ["button-colors", "visual-design"],
            "decision_type": "design",
        },
    }
    result = node.serve(context)
    assert result["served"] == []
    assert result["lessons_considered"] == 1
    assert result["lessons_below_threshold"] == 1


def test_intent_score_is_honest_overlap():
    """The score measures declared-intent overlap — documented, not magic."""
    sig = make_lesson()["intent_signature"]
    full = {
        "domains": ["learning", "verification", "admission"],
        "situation": "admission-gate candidate-design falsification-check tautology-detection",
        "decision_type": "admit",
    }
    assert intent_match_score(sig, full) >= 0.8
    empty: dict = {}
    assert intent_match_score(sig, empty) == 0.0
    assert intent_match_score({}, full) == 0.0


# --------------------------------------------------------------------------
# 2. NEGATIVE: a candidate smuggled into the store is never served.
# --------------------------------------------------------------------------

def test_candidate_in_store_is_quarantined_never_served(tmp_path):
    store = tmp_path / "store"
    lessons_dir = store / "lessons"
    lessons_dir.mkdir(parents=True)

    # Smuggle a raw candidate directly into the store, bypassing admit().
    # It has no admission schema, no provenance, no frozen flag.
    smuggled = {
        "lesson_id": "SN-SMUGGLED-001",
        "lesson_text": "I was never verified but I look like a lesson.",
        "intent_signature": make_lesson()["intent_signature"],
    }
    (lessons_dir / "SN-SMUGGLED-001.v1.json").write_text(json.dumps(smuggled))

    # Also smuggle one WITH the schema but WITHOUT VERIFY provenance.
    fake = {
        "schema": LEARN_SCHEMA,
        "lesson_id": "SN-FAKE-001",
        "version": 1,
        "lesson_text": "I claim the schema but was never admitted.",
        "intent_signature": make_lesson()["intent_signature"],
        "provenance": {"admitted_by": "NOBODY", "admitted_as": "CANDIDATE"},
        "supersedes": None,
        "superseded_by": None,
        "frozen": True,
        "status": "ACTIVE",
        "admitted_at": "2026-10-10T00:00:00Z",
        "checksum": "deadbeef",
    }
    (lessons_dir / "SN-FAKE-001.v1.json").write_text(json.dumps(fake))

    node = LearnNode(store)

    # Neither was loaded. Both were quarantined — loudly, not silently.
    assert node.active_lesson_count() == 0
    assert len(node.ignored_files) == 2
    assert any("SN-SMUGGLED-001" in f for f in node.ignored_files)
    assert any("SN-FAKE-001" in f for f in node.ignored_files)
    # The files were moved to quarantine, not left in place.
    assert list((store / "quarantine").glob("*.quarantined"))

    # A matching intent serves NOTHING — the candidates are not servable.
    context = {
        "correlation_id": "ctx-smuggle-001",
        "intent": {
            "domains": ["learning", "verification", "admission"],
            "situation": "admission-gate candidate-design falsification-check",
            "decision_type": "admit",
        },
    }
    result = node.serve(context)
    assert result["served"] == []


# --------------------------------------------------------------------------
# 3. NEGATIVE: admit() refuses anything but a VERIFY-admitted lesson.
# --------------------------------------------------------------------------

def test_rejected_lesson_cannot_be_admitted(tmp_path):
    node = LearnNode(tmp_path / "store")
    rejected = make_verify_result(admitted=False, admitted_as="REJECTED",
                                  reason_codes=["TAUTOLOGICAL_FALSIFICATION"])
    with pytest.raises(LearnAdmissionRefused) as exc_info:
        node.admit(rejected, make_lesson("SN-REJECTED-001"))
    assert exc_info.value.reason_code == "VERIFY_DID_NOT_ADMIT"
    assert node.active_lesson_count() == 0


def test_not_verified_null_cannot_be_admitted(tmp_path):
    """An honest null is admitted by the gate but is not a lesson to inherit."""
    node = LearnNode(tmp_path / "store")
    null_result = make_verify_result(admitted_as="NOT_VERIFIED")
    with pytest.raises(LearnAdmissionRefused) as exc_info:
        node.admit(null_result, make_lesson("SN-NULL-001"))
    assert exc_info.value.reason_code == "NOT_A_LESSON_CANDIDATE"
    assert node.active_lesson_count() == 0


def test_non_verify_result_cannot_be_admitted(tmp_path):
    node = LearnNode(tmp_path / "store")
    with pytest.raises(LearnAdmissionRefused) as exc_info:
        node.admit({"admitted": True}, make_lesson("SN-NOVERIFY-001"))
    assert exc_info.value.reason_code == "NOT_A_LESSON_CANDIDATE"
    with pytest.raises(LearnAdmissionRefused):
        node.admit("not-a-dict", make_lesson("SN-NOVERIFY-002"))
    assert node.active_lesson_count() == 0


def test_lesson_without_intent_signature_refused(tmp_path):
    node = LearnNode(tmp_path / "store")
    bad_lesson = make_lesson("SN-NO-INTENT-001")
    del bad_lesson["intent_signature"]
    with pytest.raises(LearnAdmissionRefused) as exc_info:
        node.admit(make_verify_result(), bad_lesson)
    assert exc_info.value.reason_code == "INTENT_SIGNATURE_REQUIRED"


# --------------------------------------------------------------------------
# 4. Durability: frozen, idempotent, checksum-guarded, supersession.
# --------------------------------------------------------------------------

def test_admit_is_idempotent(tmp_path):
    node = LearnNode(tmp_path / "store")
    r1 = node.admit(make_verify_result(), make_lesson("SN-IDEM-001"))
    r2 = node.admit(make_verify_result(), make_lesson("SN-IDEM-001"))
    assert r1["duplicate"] is False
    assert r2["duplicate"] is True
    assert node.active_lesson_count() == 1


def test_admitted_lesson_is_frozen_on_disk(tmp_path):
    store = tmp_path / "store"
    node = LearnNode(store)
    node.admit(make_verify_result(), make_lesson("SN-FROZEN-001"))

    # The file on disk carries the frozen flag, schema, and checksum.
    files = list((store / "lessons").glob("*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data["schema"] == LEARN_SCHEMA
    assert data["frozen"] is True
    assert data["provenance"]["admitted_by"] == "VERIFY"
    assert len(data["checksum"]) == 32

    # Tampering with the file is detected on load: quarantined, not served.
    data["lesson_text"] = "I rewrote history."
    files[0].write_text(json.dumps(data))
    fresh = LearnNode(store)
    assert fresh.active_lesson_count() == 0
    assert any("checksum" in f for f in fresh.ignored_files)


def test_supersession_retires_old_version_without_rewriting_history(tmp_path):
    node = LearnNode(tmp_path / "store")
    node.admit(make_verify_result(), make_lesson("SN-SUPER-001", version=1))
    v2 = make_lesson("SN-SUPER-001", version=2, supersedes="SN-SUPER-001")
    v2["lesson_text"] = "Updated: the falsification condition must also be independent of the measurement method."
    node.admit(make_verify_result(), v2)

    v1 = node.get_lesson("SN-SUPER-001", version=1)
    assert v1.status == "SUPERSEDED"
    assert v1.superseded_by == "SN-SUPER-001.v2"
    # History preserved: v1's text is untouched.
    assert "tautology wearing a costume" in v1.lesson_text

    # Only the active version is served.
    context = {
        "correlation_id": "ctx-super-001",
        "intent": {
            "domains": ["learning", "verification"],
            "situation": "candidate-design falsification-check",
            "decision_type": "validate",
        },
    }
    result = node.serve(context)
    assert len(result["served"]) == 1
    assert result["served"][0]["version"] == 2


# --------------------------------------------------------------------------
# 5. Orchestrator binding: LEARN refuses loudly when the lesson is missing.
# --------------------------------------------------------------------------

def test_orchestrator_learn_fails_closed_without_lesson(tmp_path):
    """A capture with no lesson content fails LEARN loudly — never silently."""
    executor = LocalExecutor(
        continuity_dir=tmp_path / "continuity",
        learn_store_dir=tmp_path / "learn_store",
    )
    orch = NodeOrchestrator(executor, store_root=tmp_path / "orchestrator")

    capture = make_capture_with_lesson("SN-NOLEsson-001")
    del capture["lesson"]  # malformed for the learning pipeline
    event_id = orch.commit_capture(
        capture["lesson_id"],
        json.dumps(capture["candidate"], sort_keys=True)[:200],
    )
    record = orch.run(event_id, capture)

    learn_rec = record.stages["LEARN"]
    assert learn_rec.status == StageStatus.FAILED.value
    assert "lesson" in learn_rec.error_message.lower()
    assert record.status == RunStatus.FAILED.value
