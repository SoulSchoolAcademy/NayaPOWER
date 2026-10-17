"""Battery for the Hive Learning Law (Naya 5, 2026-10-13).

Every gate must refuse what it forbids and admit what it allows.
Fail closed is tested, not asserted.
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "hive_learning_law", ROOT / "hive-learning-law.py")
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)


def _full_lesson():
    l = law.new_lesson(
        trigger="when dispatching workers",
        principle=("Always claim the lane in the truth file before spawning; "
                   "a failed claim means the lane is taken."),
        enforcement=("lane-state.py claim exits non-zero and the dispatcher "
                     "aborts the spawn."),
        evidence=["wave-101 fold: 5/5 claimed cleanly"],
        falsifier=("If a worker spawns onto a claimed lane without the claim "
                   "command failing first, this lesson is wrong."),
        provenance={"by": "Naya 5", "at": "2026-10-13"},
    )
    law.record_trial(l, control="spawned without claim: lane collision",
                     treatment="claimed first: clean spawn", delta=1,
                     notes="wave-101")
    return l


def test_proof_gate_refuses_empty_lesson():
    try:
        law.proof_gate(law.new_lesson("t", "p"))
    except law.ProofGateRefused as e:
        assert "seven_fields" in str(e), e
    else:
        raise AssertionError("gate must refuse fieldless lesson")


def test_proof_gate_refuses_null_falsifier():
    l = _full_lesson()
    l["falsifier"] = "nothing"
    try:
        law.proof_gate(l)
    except law.ProofGateRefused as e:
        assert "falsifier" in str(e), e
    else:
        raise AssertionError("gate must refuse null falsifier")


def test_proof_gate_refuses_duplicate():
    l = _full_lesson()
    try:
        law.proof_gate(l, existing_lesson_texts=[
            "When dispatching workers, always claim the lane in the truth "
            "file before spawning."])
    except law.ProofGateRefused as e:
        assert "duplicate" in str(e), e
    else:
        raise AssertionError("gate must refuse duplicates")


def test_proof_gate_refuses_self_disavowing_lesson():
    # B-48 structurally impossible: disavowing its own trigger.
    l = law.new_lesson(
        trigger="connection pooling",
        principle="Do not use connection pooling in production.",
        enforcement="reviewers reject pooling PRs",
        evidence=["outage-44"], falsifier="If pooling survives burst load, wrong.",
        provenance={"by": "t"})
    law.record_trial(l, "x", "y", True)
    try:
        law.proof_gate(l)
    except law.ProofGateRefused as e:
        assert "stance" in str(e), e
    else:
        raise AssertionError("B-48 class must be structurally refused")


def test_proof_gate_refuses_without_trial_delta():
    l = _full_lesson()
    l["trial"]["delta"] = 0
    try:
        law.proof_gate(l)
    except law.ProofGateRefused as e:
        assert "trial" in str(e), e
    else:
        raise AssertionError("gate must refuse zero-delta trials")


def test_full_lesson_promotes():
    l = law.admit(_full_lesson())
    assert l["state"] == "CANDIDATE"
    law.promote(l)
    assert l["state"] == "VERIFIED"


def test_mechanize_requires_verified():
    l = law.admit(_full_lesson())
    try:
        law.mechanize(l, "tests/test_intake_triage.py::test_trivia_drops")
    except law.MechanizeRefused:
        pass
    else:
        raise AssertionError("must not mechanize CANDIDATE")


def test_adoption_checker_verifies_real_test():
    l = law.admit(_full_lesson())
    law.promote(l)
    law.mechanize(l, "tests/test_intake_triage.py::test_trivia_drops")
    status, reasons = law.check_adoption(l)
    assert status == "ADOPTED", reasons


def test_adoption_checker_fails_missing_check():
    l = law.admit(_full_lesson())
    law.promote(l)
    law.mechanize(l, "tests/test_nope.py::test_missing")
    status, reasons = law.check_adoption(l)
    assert status == "NOT_ADOPTED", reasons


def test_surprise_signal_schema():
    good = {"signal_id": "s1", "emitted_at": "2026-10-13T23:00:00+00:00",
            "emitted_by": "Naya 5", "observed": "collision",
            "expected": "clean spawn", "decision_ref": "d1",
            "context": {"lane": 1}}
    assert law.validate_surprise_signal(good)["signal_id"] == "s1"
    bad = dict(good)
    del bad["expected"]
    try:
        law.validate_surprise_signal(bad)
    except law.SignalRejected as e:
        assert "expected" in str(e)
    else:
        raise AssertionError("must reject missing field")
    same = dict(good, observed="x", expected="x")
    try:
        law.validate_surprise_signal(same)
    except law.SignalRejected as e:
        assert "not a surprise" in str(e)
    else:
        raise AssertionError("observed==expected is not a surprise")


def test_velocity_flags_degraded():
    v = law.learning_velocity([], window_days=7.0)
    assert v["status"] == "DEGRADED", v
    l = law.admit(_full_lesson())
    law.promote(l)
    law.mechanize(l, "x")
    v = law.learning_velocity([l], window_days=1.0, min_adoptions_per_day=1.0)
    assert v["status"] == "OK", v
    assert v["adoptions"] == 1


def test_byte_integrity_holds_on_pinned_file():
    assert law.check_integrity() == "OK", "re-pin after lawful edits (--pin)"
    assert law.law_digest() == law.LAW_SHA256


def test_byte_integrity_refuses_tampered_copy(tmp_path):
    src = (ROOT / "hive-learning-law.py").read_bytes()
    bad = tmp_path / "hive-learning-law.py"
    bad.write_bytes(src.replace(b"Fail closed everywhere.",
                                b"Fail closed everywherf."))
    spec2 = importlib.util.spec_from_file_location("tampered_law", bad)
    m2 = importlib.util.module_from_spec(spec2)
    try:
        spec2.loader.exec_module(m2)
    except SystemExit as e:
        assert "TAMPERED" in str(e), e
    else:
        raise AssertionError("tampered law must refuse to run")


def test_mechanized_never_decays_but_candidate_does():
    l = law.admit(_full_lesson())
    law.promote(l)
    law.mechanize(l, "x")
    assert law.confidence(l, "2030-01-01T00:00:00+00:00") == 1.0
    c = law.new_lesson("t", "p", half_life_days=1.0)
    assert law.confidence(c, "2030-01-01T00:00:00+00:00") < 0.15
    retired = law.sweep([c], now_iso="2030-01-01T00:00:00+00:00")
    assert retired and c["state"] == "RETIRED"
