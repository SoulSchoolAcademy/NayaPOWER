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
        # F-2 seat fixtures: scorer (battery author) distinct from the
        # default doer (responses) and judge (verify --judge-seat).
        "scorer_seat": "Naya Beta",
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


def _responses(battery, mapping, subject_seat="Naya Eta"):
    return {
        "subject": "unit-test",
        # F-2: the doer seat — the seat that produced the responses.
        # Distinct from the battery's scorer_seat ("Naya Beta") and from
        # the judge seat used in verify tests ("Naya Gamma").
        "subject_seat": subject_seat,
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
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 0


def test_verify_with_failing_case_returns_exit_1(tmp_path):
    battery = _battery()
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(_responses(
        battery, {"SNTEST-N1": "It is probably fine, I assumed so."})),
        encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 1


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
                    "--registry", str(reg),
                    "--judge-seat", "Naya Gamma"]) == 0
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


# --- T6 judge-seat guard (graduation F-2) -----------------------------------
# Spec: w140 packet §2-T6, confirmed by Epsilon's w143 targeted re-check.
# Seats: doer = responses `subject_seat`, scorer = battery `scorer_seat`,
# judge = verify `--judge-seat`. `--judge` (callable) is never a seat;
# free-text `subject` is display-only and never used for the comparison.

def test_assert_independent_judge_accepts_distinct_seats():
    lv.assert_independent_judge("Naya Eta", "Naya Beta", "Naya Gamma")


def test_assert_independent_judge_rejects_judge_equals_doer():
    with pytest.raises(lv.StructureError, match="SEAT_INDEPENDENCE_FAIL"):
        lv.assert_independent_judge("Naya Eta", "Naya Beta", "Naya Eta")


def test_assert_independent_judge_rejects_judge_equals_scorer():
    with pytest.raises(lv.StructureError, match="SEAT_INDEPENDENCE_FAIL"):
        lv.assert_independent_judge("Naya Eta", "Naya Beta", "Naya Beta")


@pytest.mark.parametrize("doer,scorer,judge", [
    ("", "Naya Beta", "Naya Gamma"),
    (None, "Naya Beta", "Naya Gamma"),
    ("   ", "Naya Beta", "Naya Gamma"),
    ("Naya Eta", "", "Naya Gamma"),
    ("Naya Eta", None, "Naya Gamma"),
    ("Naya Eta", "Naya Beta", ""),
    ("Naya Eta", "Naya Beta", None),
])
def test_assert_independent_judge_rejects_missing_seat(doer, scorer, judge):
    with pytest.raises(lv.StructureError, match="SEAT_MISSING"):
        lv.assert_independent_judge(doer, scorer, judge)


def test_assert_independent_judge_strips_whitespace_before_comparison():
    # Judgment call, pinned: " Naya Eta " is the same seat as "Naya Eta".
    with pytest.raises(lv.StructureError, match="SEAT_INDEPENDENCE_FAIL"):
        lv.assert_independent_judge("Naya Eta", "Naya Beta", "  Naya Eta  ")


def test_assert_independent_judge_rejects_non_string_seat():
    # Judgment call, pinned: seat identities are strings; a non-string
    # value is malformed, and fail-closed means it counts as missing.
    with pytest.raises(lv.StructureError, match="SEAT_MISSING"):
        lv.assert_independent_judge(5, "Naya Beta", "Naya Gamma")


def test_assert_independent_judge_does_not_assert_doer_equals_scorer():
    # Disclosed boundary: battery self-authorship is a separate concern
    # for the wiring PR, not this guard.
    lv.assert_independent_judge("Naya Eta", "Naya Eta", "Naya Gamma")


def test_assert_independent_judge_error_strings_match_spec():
    with pytest.raises(lv.StructureError) as exc:
        lv.assert_independent_judge("Naya Eta", "Naya Beta", "Naya Eta")
    assert str(exc.value) == (
        "SEAT_INDEPENDENCE_FAIL: judge_seat 'Naya Eta' must differ from "
        "doer_seat 'Naya Eta' and scorer_seat 'Naya Beta' — self-verification "
        "is not verification (Inviolable); no T6 emit."
    )
    with pytest.raises(lv.StructureError) as exc:
        lv.assert_independent_judge("Naya Eta", "Naya Beta", "")
    assert str(exc.value) == (
        "SEAT_MISSING: judge_seat is required for T6 — no judge seat ⇒ no T6"
    )


def _verify_files(tmp_path, battery, responses):
    bpath = tmp_path / "battery.json"
    rpath = tmp_path / "responses.json"
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(responses), encoding="utf-8")
    return bpath, rpath


def _passing_pair(tmp_path):
    battery = _battery()
    responses = _responses(
        battery, {"SNTEST-N1": "I will re-check and verify before concluding."})
    return battery, responses, _verify_files(tmp_path, battery, responses)


def test_verify_judge_equals_doer_returns_exit_2(tmp_path):
    _battery, _responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Eta"]) == 2


def test_verify_judge_equals_scorer_returns_exit_2(tmp_path):
    _battery, _responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Beta"]) == 2


def test_verify_missing_judge_seat_returns_exit_2(tmp_path):
    _battery, _responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath)]) == 2


def test_verify_missing_doer_seat_returns_exit_2(tmp_path):
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    del responses["subject_seat"]
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(responses), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 2


def test_verify_missing_scorer_seat_returns_exit_2(tmp_path):
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    del battery["scorer_seat"]
    bpath.write_text(json.dumps(battery), encoding="utf-8")
    rpath.write_text(json.dumps(responses), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 2


def test_verify_distinct_seats_pass(tmp_path):
    _battery, _responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 0


def test_verify_gate_runs_before_scoring(tmp_path):
    # A failing response + an ineligible judge must return 2 (gate), not 1
    # (score) — and must write no report, proving scoring never ran.
    battery = _battery()
    responses = _responses(
        battery, {"SNTEST-N1": "It is probably fine, I assumed so."})
    bpath, rpath = _verify_files(tmp_path, battery, responses)
    report = tmp_path / "report.json"
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Eta",
                    "--report", str(report)]) == 2
    assert not report.exists()


def test_verify_subject_display_never_used_for_gate(tmp_path):
    # `subject` is display-only: even when it names the judge seat, the
    # gate reads `subject_seat` — so this passes.
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    responses["subject"] = "Naya Gamma"
    rpath.write_text(json.dumps(responses), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma"]) == 0


def test_verify_subject_display_cannot_launder_collision(tmp_path):
    # And the reverse: a harmless-looking `subject` cannot hide a real
    # subject_seat == judge_seat collision.
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    responses["subject"] = "someone-else"
    rpath.write_text(json.dumps(responses), encoding="utf-8")
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Eta"]) == 2


def test_verify_cli_judge_seat_flag_end_to_end(tmp_path):
    # Proves the argparse wiring, not just lv.main: the real CLI accepts
    # --judge-seat and the gate fires through the process boundary.
    import subprocess
    import sys
    from pathlib import Path
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    root = Path(__file__).resolve().parent.parent
    proc = subprocess.run(
        [sys.executable, "tools/lesson_verification.py", "verify",
         "--battery", str(bpath), "--responses", str(rpath),
         "--judge-seat", "Naya Eta"],
        cwd=root, capture_output=True, text=True)
    assert proc.returncode == 2
    assert "SEAT_INDEPENDENCE_FAIL" in proc.stderr
    assert "STRUCTURE ERROR" in proc.stderr


def test_verify_custom_judge_callable_coexists_with_judge_seat(tmp_path):
    # Claim (2), end to end: --judge module:function is the SCORING callable
    # and is independent of the --judge-seat identity — both ride one
    # verify invocation without interfering.
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma",
                    "--judge", "tools.lesson_verification:lexical_judge"]) == 0


def test_verify_judge_without_colon_returns_exit_2(tmp_path):
    # Claim (2) negative: the callable spec must be module:function.
    battery, responses, (bpath, rpath) = _passing_pair(tmp_path)
    assert lv.main(["verify", "--battery", str(bpath),
                    "--responses", str(rpath),
                    "--judge-seat", "Naya Gamma",
                    "--judge", "notacallable"]) == 2


def test_scaffold_writes_scorer_seat(tmp_path):
    out = tmp_path / "battery.json"
    assert lv.main(["scaffold", "--lesson-id", "SN-X", "--out", str(out),
                    "--scorer-seat", "Naya Beta"]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["scorer_seat"] == "Naya Beta"


def test_scaffold_defaults_scorer_seat_empty(tmp_path):
    out = tmp_path / "battery.json"
    assert lv.main(["scaffold", "--lesson-id", "SN-X", "--out", str(out)]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["scorer_seat"] == ""


def test_score_does_not_assert_seats(tmp_path):
    # cmd_score is diagnostic-only: no seat fields, no --judge-seat, still
    # scores. Only cmd_verify carries the T6 gate.
    battery = _battery()
    del battery["scorer_seat"]
    responses = _responses(
        battery, {"SNTEST-N1": "I will re-check and verify before concluding."})
    del responses["subject_seat"]
    bpath, rpath = _verify_files(tmp_path, battery, responses)
    assert lv.main(["score", "--battery", str(bpath),
                    "--responses", str(rpath)]) == 0
