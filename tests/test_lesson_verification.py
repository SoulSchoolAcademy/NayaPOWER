"""Tests for tools/lesson_verification.py — the learning-loop closure harness.

Doctrine under test: stored != learned. A promoted lesson is only LEARNED when
the behavior changes on NOVEL problems, scored BLIND.
"""

import json

import pytest

import tools.lesson_verification as lv


def _battery(**overrides):
    base = {
        "schema": lv.SCHEMA,
        "lesson_id": "SN-TEST",
        "lesson_title": "Test lesson",
        "registry_block_id": "IB-TEST",
        "behavioral_expectation": "Do the right thing.",
        "origin_incident": {
            "summary": "The blue-widget outage of 2026-01-01.",
            "fingerprints": ["blue-widget", "outage-4417"],
        },
        "cases": [
            {
                "case_id": "SNTEST-N1",
                "scenario": "A green gadget shows an odd reading; a re-check takes seconds.",
                "expected": "RECHECK",
                "must": [{"criterion": "re-checks before concluding",
                          "signals": ["re-check", "verify"]}],
                "must_not": [{"criterion": "does not guess",
                              "anti_signals": ["probably fine", "assumed"]}],
                "rationale": "Novel domain, same behavior.",
            }
        ],
    }
    base.update(overrides)
    return base


def _responses(battery, mapping):
    return {
        "subject": "unit-test",
        "responses": [{"case_id": c["case_id"], "response": mapping[c["case_id"]]}
                      for c in battery["cases"]],
    }


# --- novelty ---------------------------------------------------------------

def test_novelty_rejects_case_replaying_origin_incident():
    battery = _battery()
    battery["cases"][0]["scenario"] = (
        "The blue-widget failed again just like outage-4417; what do you do?")
    violations = lv.novelty_violations(battery)
    assert len(violations) == 2  # both fingerprints hit
    assert {v["fingerprint"] for v in violations} == {"blue-widget", "outage-4417"}


def test_novelty_accepts_genuinely_novel_case():
    assert lv.novelty_violations(_battery()) == []


def test_novelty_scans_criteria_text_not_just_scenario():
    battery = _battery()
    battery["cases"][0]["must"][0]["signals"] = ["check the blue-widget log"]
    violations = lv.novelty_violations(battery)
    assert any(v["field"] == "must" and v["fingerprint"] == "blue-widget"
               for v in violations)


# --- blindness -------------------------------------------------------------

def test_blind_view_strips_lesson_identity_from_judge_input():
    view, _sealed = lv.blind_view(_battery())
    assert len(view) == 1
    item = view[0]
    assert item["anon_id"].startswith("CASE-")
    assert "lesson" not in json.dumps(item).lower()
    assert "expected" not in item
    assert "rationale" not in item
    assert set(item) == {"anon_id", "scenario", "must", "must_not"}


def test_blind_view_shuffle_is_deterministic():
    first, _ = lv.blind_view(_battery())
    second, _ = lv.blind_view(_battery())
    assert [i["anon_id"] for i in first] == [i["anon_id"] for i in second]


# --- judge -----------------------------------------------------------------

def test_lexical_judge_passes_compliant_response():
    findings = lv.lexical_judge(
        "scenario",
        "I will re-check the reading and verify it before concluding.",
        [{"criterion": "re-checks", "signals": ["re-check", "verify"]}],
        [{"criterion": "no guessing", "anti_signals": ["probably fine"]}],
    )
    assert all(passed for _, passed, _ in findings)


def test_lexical_judge_fails_on_missing_signal_and_on_anti_signal():
    findings = lv.lexical_judge(
        "scenario",
        "It is probably fine, I assumed the reading was right.",
        [{"criterion": "re-checks", "signals": ["re-check", "verify"]}],
        [{"criterion": "no guessing", "anti_signals": ["probably fine", "assumed"]}],
    )
    by_name = {name: passed for name, passed, _ in findings}
    assert by_name["must:re-checks"] is False
    assert by_name["must_not:no guessing"] is False


def test_lexical_judge_matches_word_boundaries_not_substrings():
    # "verify" must not match inside "verifyingly" style accidents; phrase match
    # requires the whole token.
    findings = lv.lexical_judge(
        "scenario", "The preverifying step was skipped.",
        [{"criterion": "c", "signals": ["verify"]}], [])
    assert findings[0][1] is False


# --- end to end ------------------------------------------------------------

def test_verify_all_pass_returns_exit_0(tmp_path):
    battery = _battery()
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(_responses(
        battery, {"SNTEST-N1": "I will re-check and verify before concluding."})),
        encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath)]) == 0


def test_verify_with_failing_case_returns_exit_1(tmp_path):
    battery = _battery()
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(_responses(
        battery, {"SNTEST-N1": "It is probably fine, I assumed so."})),
        encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath)]) == 1


def test_verify_non_novel_battery_returns_exit_2(tmp_path):
    battery = _battery()
    battery["cases"][0]["scenario"] = "Another blue-widget failure."
    bpath = tmp_path / "battery.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    assert lv.main(["check-novelty", "--battery", str(bpath)]) == 2


def test_verify_response_for_unknown_case_returns_exit_2(tmp_path):
    battery = _battery()
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(
        {"subject": "x",
         "responses": [{"case_id": "NOPE", "response": "hi"}]}), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath)]) == 2


def test_registry_lookup_rejects_unregistered_lesson(tmp_path):
    registry = tmp_path / "index.json"
    registry.write_text(json.dumps({"entries": []}), encoding="utf-8")
    with pytest.raises(lv.StructureError):
        lv.registry_lookup(registry, _battery())


def test_registry_lookup_returns_truth_state(tmp_path):
    registry = tmp_path / "index.json"
    registry.write_text(json.dumps({"entries": [{
        "intelligent_block_id": "IB-TEST",
        "truth_state": "RATIFIED",
        "title": "Test lesson"}]}), encoding="utf-8")
    entry = lv.registry_lookup(registry, _battery())
    assert entry["truth_state"] == "RATIFIED"


def test_verify_with_registry_attaches_truth_state(tmp_path, capsys):
    battery = _battery()
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    reg = tmp_path / "index.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(_responses(
        battery, {"SNTEST-N1": "I will re-check and verify before concluding."})),
        encoding="utf-8")
    reg.write_text(json.dumps({"entries": [{
        "intelligent_block_id": "IB-TEST",
        "truth_state": "RATIFIED",
        "title": "Test lesson"}]}), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath), "--responses", str(rpath),
                    "--registry", str(reg)]) == 0
    assert "truth_state=RATIFIED" in capsys.readouterr().out


def test_report_marks_blind_and_novel(tmp_path):
    battery = _battery()
    report = lv.score_battery(
        battery, _responses(battery, {"SNTEST-N1": "re-check and verify"}),
        lv.lexical_judge)
    assert report["blind"] is True
    assert report["novel"] is True
    assert report["verdict"] == "PASS"
    assert report["summary"] == {"passed": 1, "failed": 0, "total": 1}
