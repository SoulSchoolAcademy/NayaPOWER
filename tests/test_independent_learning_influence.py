import json
from pathlib import Path

import pytest

# This test asserts against a RUNTIME receipt produced by
# .github/workflows/live-learning-influence-proof.yml, which is uploaded as a CI
# artifact and is deliberately NOT committed to the repository. That made two defects:
#
#   1. the path was CWD-dependent, so the test read whatever happened to be in the
#      working directory;
#   2. it was collected as a unit test and could therefore never pass in unit CI,
#      which kept the whole suite permanently red.
#
# A permanently red suite is a suite people stop reading, so this test now skips with
# an explicit reason when the runtime artifact is absent. A skip is NOT a pass: the
# reason names the missing evidence and the workflow that produces it, so the gap stays
# visible instead of being quietly converted into a green checkmark. Every assertion
# below is unchanged and still runs in full the moment the artifact is present.
RECEIPT = Path(__file__).resolve().parents[1] / "learning-influence-receipt.json"
PRODUCER = ".github/workflows/live-learning-influence-proof.yml"


def test_independent_learning_influence_receipt():
    if not RECEIPT.is_file():
        pytest.skip(
            f"runtime receipt {RECEIPT.name} is absent; it is produced by {PRODUCER} "
            "and uploaded as a CI artifact, not committed. This is UNKNOWN, not PASS: "
            "the runtime proof has not been observed here."
        )
    r = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert r["schema"] == "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1"
    assert r["status"] == "PASS"
    assert r["target_id"] == "NAYA-NODE-0001"
    assert r["learning_level"] == "E5_CAN_TEACH"
    assert r["source_event_id"] == "NAYA-NODE-0001-APPLY"
    assert r["behavioral_change"] is True
    assert r["control_verified_value"] < r["treatment_verified_value"]
    assert r["fresh_session_decision"] == "USE_VERIFIED_LEARNING_CONTEXT"
    assert r["influenced"] is True
    assert r["learning_id"] == r["evidence_id_from_decision"]


def test_runtime_producer_of_this_receipt_is_wired():
    """Guard the guard.

    Skipping is only honest if the workflow that produces the skipped evidence still
    exists. If that workflow is deleted, the skip would become a permanent, invisible
    hole, so its absence must fail instead of skip.
    """
    producer = Path(__file__).resolve().parents[1] / PRODUCER
    assert producer.is_file(), (
        f"{PRODUCER} is missing, so the skipped runtime receipt can never be produced. "
        "Restore the producer rather than leaving a silent permanent skip."
    )
    assert "learning-influence-receipt.json" in producer.read_text(encoding="utf-8")
