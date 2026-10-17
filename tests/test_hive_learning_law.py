import importlib.util
import hashlib
import subprocess
import sys
from pathlib import Path
import pytest

LAW_PATH = Path(__file__).resolve().parents[1] / "tools" / "hive-learning-law.py"
spec = importlib.util.spec_from_file_location("hive_learning_law", LAW_PATH)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)


def lesson(**overrides):
    item = {
        "lesson_id": "L-001", "source_ref": "capture:abc", "essence": "Preserve provenance",
        "why_it_matters": "Prevents false attribution", "applicability": ["capture", "retrieval"],
        "evidence_refs": ["receipt:123"], "behavioral_probe": "Can a cold successor retrieve source?",
        "falsifier": {"condition": "source receipt missing", "observable_failure": "successor cannot resolve source", "measurement": "retrieval receipt absent"},
    }
    item.update(overrides)
    return item


def test_lesson_requires_all_seven_fields_and_specific_falsifier():
    bad = lesson(); del bad["applicability"]
    with pytest.raises(law.LawViolation, match="LESSON_REQUIRED_FIELDS_MISSING"):
        law.validate_lesson(bad)
    bad = lesson(falsifier={"condition": "wrong", "observable_failure": "fails"})
    with pytest.raises(law.LawViolation, match="FALSIFIER_MEASUREMENT"):
        law.validate_lesson(bad)


def test_duplicate_id_and_duplicate_content_block():
    item = lesson()
    with pytest.raises(law.LawViolation, match="DUPLICATE_LESSON_ID"):
        law.validate_lesson(item, [lesson(lesson_id="l-001")])
    with pytest.raises(law.LawViolation, match="DUPLICATE_LESSON_CONTENT"):
        law.validate_lesson(item, [lesson(lesson_id="L-002")])


def test_adoption_requires_behavior_outcome_independent_verification_and_cold_successor():
    record = {"lesson_id":"L-1", "canonical_lesson_ref":"ib:1", "retrieval_receipt_id":"r:1",
              "task_id":"task:2", "control_behavior_hash":"a", "treatment_behavior_hash":"b",
              "outcome_evidence_ref":"outcome:1", "independent_verifier":"verifier-b",
              "verification_receipt_id":"verify:1", "cold_successor_ref":"successor:1",
              "actor":"worker-a", "cold_successor_verified":True, "outcome_improved":True}
    assert law.validate_adoption(record)["adopted"] is True
    with pytest.raises(law.LawViolation, match="SELF_VERIFICATION"):
        law.validate_adoption({**record, "independent_verifier":"worker-a"})
    with pytest.raises(law.LawViolation, match="NO_BEHAVIOR_DELTA"):
        law.validate_adoption({**record, "treatment_behavior_hash":"a"})
    with pytest.raises(law.LawViolation, match="COLD_SUCCESSOR"):
        law.validate_adoption({**record, "cold_successor_verified":False})


def test_velocity_marks_degraded_and_unknown_without_faking_zero():
    report = law.velocity_report([{"eligible":True,"adoption_verified":False}], minimum_rate=0.5)
    assert report["status"] == "DEGRADED" and report["adoption_rate"] == 0
    report = law.velocity_report([{"eligible":False}], minimum_rate=0.5)
    assert report["status"] == "UNKNOWN" and report["adoption_rate"] is None


def test_surprise_signal_is_schema_bound_and_cannot_promote_or_grant_authority():
    signal = {"schema":law.SURPRISE_SCHEMA,"signal_id":"s1","worker_id":"w1","observed_at":"2026-10-13T00:00:00Z",
              "source_ref":"event:1","expected":"A","observed":"B","surprise_type":"CONTRADICTION",
              "impact":"HIGH","evidence_refs":["receipt:1"],"proposed_lesson_id":"L-1"}
    assert law.validate_surprise_signal(signal)["status"] == "PASS"
    with pytest.raises(law.LawViolation, match="CANNOT_GRANT_AUTHORITY"):
        law.validate_surprise_signal({**signal,"promote_lesson":True})


def test_integrity_manifest_detects_tampering(tmp_path):
    target = tmp_path / "law.py"; target.write_bytes(LAW_PATH.read_bytes())
    manifest = tmp_path / "law.sha256"; manifest.write_text(law.sha256_bytes(target.read_bytes()) + "\n")
    assert law.verify_byte_integrity(target, manifest)["status"] == "PASS"
    target.write_bytes(target.read_bytes() + b"# tampered\n")
    with pytest.raises(law.LawViolation, match="INTEGRITY_MISMATCH"):
        law.verify_byte_integrity(target, manifest)


def test_learning_promotion_requires_exactly_one_valid_lesson_object():
    entry = {"category":"LEARNING", "learning_law_required":True}
    with pytest.raises(law.LawViolation, match="EXACTLY_ONE"):
        law.validate_learning_promotion(entry, [])
    result = law.validate_learning_promotion(entry, [{"lesson":lesson()}])
    assert result["status"] == "PASS"


def test_cli_refuses_to_run_when_law_bytes_are_tampered(tmp_path):
    root = tmp_path
    tools_dir = root / "tools"; tools_dir.mkdir()
    governance = root / ".naya" / "governance"; governance.mkdir(parents=True)
    script = tools_dir / "hive-learning-law.py"
    original = LAW_PATH.read_bytes()
    script.write_bytes(original)
    manifest = governance / "HIVE-LEARNING-LAW.sha256"
    manifest.write_text(hashlib.sha256(original).hexdigest() + "  tools/hive-learning-law.py\\n", encoding="ascii")
    script.write_bytes(original + b"# tampered\\n")
    lesson_path = root / "lesson.json"; lesson_path.write_text("{}", encoding="utf-8")
    result = subprocess.run([sys.executable, str(script), "validate-lesson", "--lesson", str(lesson_path)],
                           cwd=root, capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "LAW_BYTE_INTEGRITY_MISMATCH" in result.stderr
