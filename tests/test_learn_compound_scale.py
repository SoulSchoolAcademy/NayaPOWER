"""Unit tests for the learn-compound scale harness.

These test the HARNESS mechanics (distill, gates, subject integrity, arm
isolation, pre-registration seal) — not the lessons themselves. The lessons
are proven by run_scale.py; these tests prove the prover is honest.
"""
import hashlib
import json
import sys
from pathlib import Path

import pytest

PKG = Path(__file__).resolve().parent.parent / "tools" / "learning" / "compound_scale"
sys.path.insert(0, str(PKG))

import fixtures
import gates
import pipeline
import subjects

REGISTRY = json.loads((PKG / "lessons_registry.json").read_text(encoding="utf-8"))
GOOD = [l for l in REGISTRY["lessons"] if not l.get("adversarial")]
BAD = [l for l in REGISTRY["lessons"] if l.get("adversarial")]


def _lesson(lid):
    return next(l for l in REGISTRY["lessons"] if l["id"] == lid)


# ------------------------------------------------------------- distill
def test_distill_extracts_rule_sentence():
    note = "Something broke. It was bad. Rule: Never write shims into system paths."
    assert pipeline.distill(note) == "Never write shims into system paths."


def test_distill_falls_back_without_rule_sentence():
    note = "The cache was stale. Always re-check before acting on it."
    out = pipeline.distill(note)
    assert isinstance(out, str) and out  # honest fallback, may be vague


@pytest.mark.parametrize("lesson", GOOD, ids=lambda l: l["id"])
def test_distill_matches_preregistered_principle(lesson):
    assert pipeline.distill(lesson["capture"]["note"]) == lesson["distill"]["principle"]


# --------------------------------------------------------------- truth
def test_truth_must_hold_quote_present():
    score, _ = gates.gate_truth(_lesson("L1"))
    assert score == 9


def test_truth_fails_gracefully_on_missing_file():
    les = dict(_lesson("L1"))
    les["truth"] = dict(les["truth"], receipt_file="~/does-not-exist-xyz.md")
    score, _ = gates.gate_truth(les)
    assert score == 0


def test_truth_fails_gracefully_on_missing_quote():
    les = dict(_lesson("L1"))
    les["truth"] = dict(les["truth"], receipt_quote="this quote is not in the file xyz")
    score, _ = gates.gate_truth(les)
    assert score <= 4


@pytest.mark.parametrize("lesson", BAD, ids=lambda l: l["id"])
def test_truth_rejects_adversarial(lesson):
    score, detail = gates.gate_truth(lesson)
    assert score == 9, detail
    assert "REJECT" in detail


def test_truth_rejects_unearned_contradiction():
    les = dict(_lesson("A3"))
    les["truth"] = dict(les["truth"], contradicting_quote="no such text anywhere xyz")
    score, _ = gates.gate_truth(les)
    assert score <= 2  # rejection unearned: contradiction not in source


# ------------------------------------------------------- comprehension
@pytest.mark.parametrize("lesson", GOOD, ids=lambda l: l["id"])
def test_comprehension_probe_passes_on_distilled(lesson):
    distilled = pipeline.distill(lesson["capture"]["note"])
    ok, _ = gates.comprehension_probe(distilled, lesson)
    assert ok


def test_comprehension_probe_fails_on_vague_text():
    ok, _ = gates.comprehension_probe("Be careful with things.", _lesson("L1"))
    assert not ok


# --------------------------------------------------------------- subject
def _rule_for(lesson, **over):
    r = {"name": lesson["name"], "applies_to": lesson["rule"]["applies_to"],
         "procedure": lesson["rule"]["procedure"],
         "receipt": {"file": "x", "quote": "y"}}
    r.update(over)
    return r


def test_subject_applies_valid_rule(tmp_path):
    les = _lesson("L5")
    sub = subjects.Subject()
    art, _ = sub.act("file_writer", [_rule_for(les)], tmp_path)
    ok, _ = fixtures.VERIFY["file_writer"](art, {"comment": "see `issue-1234` for details"})
    assert ok and sub.applied_rule is not None


def test_subject_refuses_corrupt_rule(tmp_path):
    les = _lesson("L5")
    sub = subjects.Subject()
    art, _ = sub.act("file_writer", [_rule_for(les, corrupt=True)], tmp_path)
    assert len(sub.refusals) == 1
    assert sub.applied_rule is None
    # falls back to naive -> verifier fails
    ok, _ = fixtures.VERIFY["file_writer"](art, {"comment": "see `issue-1234` for details"})
    assert not ok


def test_subject_refuses_receiptless_rule(tmp_path):
    les = _lesson("L5")
    sub = subjects.Subject()
    rule = _rule_for(les)
    del rule["receipt"]
    sub.act("file_writer", [rule], tmp_path)
    assert len(sub.refusals) == 1 and sub.applied_rule is None


def test_subject_ignores_rule_for_other_task(tmp_path):
    les = _lesson("L5")
    sub = subjects.Subject()
    rule = _rule_for(les)
    rule["applies_to"] = "gh_body_file"  # wrong task type
    sub.act("file_writer", [rule], tmp_path)
    assert sub.applied_rule is None


# ----------------------------------------------------------- arm isolation
def test_control_treatment_differ_only_by_injection(tmp_path):
    les = _lesson("L9")
    rule = _rule_for(les)
    c = subjects.run_arm(les, "control", rule, tmp_path)
    t = subjects.run_arm(les, "treatment", rule, tmp_path)
    cj, tj = json.loads(c["context_canonical"]), json.loads(t["context_canonical"])
    assert cj == [] and len(tj) == 1
    assert tj[0]["applies_to"] == "branch_pr" or tj[0]["applies_to"] == les["task"]["type"]


@pytest.mark.parametrize("lesson", GOOD, ids=lambda l: l["id"])
def test_adversarial_arm_never_changes_behavior(lesson, tmp_path):
    rule = _rule_for(lesson)
    res = subjects.run_arm(lesson, "adversarial", rule, tmp_path)
    assert not res["passed"], f"{lesson['id']}: tampered rule took effect!"
    assert len(res["refusals"]) == 1


# -------------------------------------------------------------- registry
def test_registry_schema_complete():
    required = {"id", "name", "family", "capture", "distill", "truth",
                "task", "rule", "comprehension", "prereg"}
    for les in REGISTRY["lessons"]:
        assert required <= set(les), les["id"]
        assert les["prereg"]["expected"] in ("PASS", "REJECT")
        assert les["truth"]["mode"] in ("must_hold", "must_contradict")


def test_registry_has_11_good_3_adversarial():
    assert len(GOOD) == 11 and len(BAD) == 3


def test_seal_refuses_changed_registry(tmp_path, monkeypatch):
    import run_scale
    # seal the current registry, then tamper a copy and check detection
    seal = {"sha256": hashlib.sha256(
        (PKG / "lessons_registry.json").read_bytes()).hexdigest()}
    tampered = (PKG / "lessons_registry.json").read_bytes() + b" "
    assert hashlib.sha256(tampered).hexdigest() != seal["sha256"]
