import pytest

from tools.score_round2_trials import ARMS, score_trials


@pytest.fixture(autouse=True)
def real_transcript(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "t.json").write_text('{"raw": "test transcript fixture"}', encoding="utf-8")


def _trial(trial_id, arm, correct=True, cited=True, order=1.0, count=10,
           consistent=True, nt=False, transcript="logs/t.json"):
    return {
        "trial_id": trial_id,
        "arm": arm,
        "negative_transfer": nt,
        "verdict_correct": correct,
        "cited_lesson": cited,
        "diagnostic_order": order,
        "tool_call_count": count,
        "consistent": consistent,
        "transcript_path": transcript,
    }


def _battery(treatment_correct=5, treatment_total=6, control_correct=2,
             wrong_correct=2, nt_per_arm=5):
    trials = []
    for i in range(treatment_total):
        trials.append(_trial(f"T{i}", "TREATMENT", correct=i < treatment_correct))
    for i in range(treatment_total):
        trials.append(_trial(f"C{i}", "CONTROL", correct=i < control_correct,
                             cited=False))
    for i in range(treatment_total):
        trials.append(_trial(f"W{i}", "WRONG_LESSON", correct=i < wrong_correct,
                             cited=False))
    for arm in ARMS:
        for i in range(nt_per_arm):
            trials.append(_trial(f"N-{arm}-{i}", arm, correct=True, nt=True))
    return trials


def test_pass_battery_meets_bar():
    result = score_trials(_battery())
    assert result.verdict == "PASS", result.reasons
    assert result.arm_accuracy["TREATMENT"] > result.arm_accuracy["CONTROL"]
    assert result.cost_ratio_treatment_vs_control == pytest.approx(1.0)


def test_negative_transfer_flip_is_hard_fail():
    trials = _battery()
    trials.append(_trial("N-X", "TREATMENT", correct=False, nt=True))
    result = score_trials(trials)
    assert result.verdict == "FAIL"
    assert any("NT_HARD_GATE" in r for r in result.reasons)


def test_ceiling_effect_is_inconclusive_not_pass():
    trials = _battery(treatment_correct=6, control_correct=6)
    result = score_trials(trials)
    assert result.verdict == "INCONCLUSIVE"
    assert any("CEILING" in r for r in result.reasons)


def test_unattributed_win_is_inconclusive():
    trials = _battery(treatment_correct=5, wrong_correct=5)
    for t in trials:
        if t["arm"] == "TREATMENT":
            t["cited_lesson"] = False
    result = score_trials(trials)
    assert result.verdict == "INCONCLUSIVE"
    assert any("ATTRIBUTION" in r for r in result.reasons)


def test_missing_tool_count_voids_trial():
    trials = _battery()
    trials[0].pop("tool_call_count")
    result = score_trials(trials)
    assert result.verdict == "FAIL"
    assert any("void trial" in r for r in result.reasons)


def test_summary_without_transcript_does_not_count():
    trials = _battery()
    for t in trials:
        t["transcript_path"] = ""
    with pytest.raises(ValueError, match="NO_VALID_TRIALS"):
        score_trials(trials)


def test_missing_arm_fails():
    trials = [t for t in _battery() if t["arm"] != "WRONG_LESSON"]
    result = score_trials(trials)
    assert result.verdict == "FAIL"
    assert any("MISSING_ARM" in r for r in result.reasons)


def test_cost_overrun_penalizes_treatment_score():
    trials = _battery()
    for t in trials:
        if t["arm"] == "TREATMENT":
            t["tool_call_count"] = 20
    result = score_trials(trials)
    assert result.verdict == "PASS"
    assert result.cost_ratio_treatment_vs_control == pytest.approx(2.0)
    assert result.arm_scores["TREATMENT"] < 1.0


def test_three_trials_cannot_pass_round2_minimums():
    trials = [_trial("T", "TREATMENT"),
              _trial("C", "CONTROL", correct=False),
              _trial("W", "WRONG_LESSON", correct=False)]
    result = score_trials(trials)
    assert result.verdict == "FAIL"
    assert any("MINIMUM_FIVE_TRIALS_PER_ARM" in r for r in result.reasons)


def test_absent_negative_transfer_is_not_a_vacuous_pass():
    result = score_trials(_battery(nt_per_arm=0))
    assert result.verdict == "FAIL"
    assert any("MINIMUM_FIVE_NEGATIVE_TRANSFER_TRIALS" in r for r in result.reasons)


def test_duplicate_trial_ids_cannot_pad_the_battery():
    trials = _battery()
    trials[0]["trial_id"] = trials[1]["trial_id"]
    assert score_trials(trials).verdict == "FAIL"


def test_missing_transcript_file_cannot_count_as_evidence():
    trials = _battery()
    for trial in trials:
        trial["transcript_path"] = "logs/nonexistent.json"
    with pytest.raises(ValueError, match="NO_VALID_TRIALS"):
        score_trials(trials)


def test_empty_transcript_file_cannot_count_as_evidence():
    from pathlib import Path
    Path("logs/t.json").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="NO_VALID_TRIALS"):
        score_trials(_battery())


@pytest.mark.parametrize("key,value", [
    ("verdict_correct", "false"), ("cited_lesson", "true"),
    ("consistent", 1), ("negative_transfer", "false"),
    ("tool_call_count", True), ("diagnostic_order", True),
    ("trial_id", None), ("transcript_path", None),
])
def test_malformed_trial_fields_cannot_receive_pass(key, value):
    trials = _battery()
    trials[0][key] = value
    assert score_trials(trials).verdict == "FAIL"


def test_malformed_trial_cannot_be_silently_dropped():
    assert score_trials(_battery() + [None]).verdict == "FAIL"


def test_four_negative_transfer_trials_do_not_meet_the_floor():
    trials = _battery(nt_per_arm=0)
    trials.extend(_trial(f"N{i}", "TREATMENT", nt=True) for i in range(4))
    assert score_trials(trials).verdict == "FAIL"


def test_five_negative_transfer_trials_meet_the_declared_floor():
    trials = _battery(nt_per_arm=0)
    trials.extend(_trial(f"N{i}", "TREATMENT", nt=True) for i in range(5))
    assert score_trials(trials).verdict == "PASS"
