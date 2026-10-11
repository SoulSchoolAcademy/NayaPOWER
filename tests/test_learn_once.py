"""Machine-falsifiable tests for the Learn-Once Loop.

The loop's central claim: a lesson is learned only when behavior changes
permanently without being told again. These tests falsify the machinery
itself — each one describes a way the loop could lie, and asserts it cannot.

Falsifiers:
  * a re-tell that does NOT fail the loop        -> test_retell_is_loop_failure
  * an unencoded lesson that passes verification -> test_unencoded_lesson_cannot_verify
  * a regressed behavior the loop misses         -> test_behavioral_regression_detected
  * encoding that is only a note                 -> test_encoding_not_just_a_note
  * stages skipped out of order                  -> test_stage_order_enforced
  * a shallow IB accepted as understanding       -> test_ib_requires_three_perspectives
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.learn_once import LearnOnceLoop
from tools.learn_once import encoding as enc_mod
from tools.learn_once.distill import distill
from tools.learn_once.encoding import EncodingRecord, EncodingTarget, checklist_issues, encode
from tools.learn_once.intake import capture
from tools.learn_once.models import Stage
from tools.learn_once.verify import audit, register_check

ROOT = Path(__file__).resolve().parents[1]


@register_check("always_pass")
def _always_pass():
    return True, "synthetic pass"


@register_check("always_fail")
def _always_fail():
    return False, "synthetic fail"


def _loop(tmp_path) -> LearnOnceLoop:
    return LearnOnceLoop(tmp_path / "lessons.jsonl")


def _teaching() -> str:
    return (
        "A lesson isn't learned when it's noted. It's learned when behavior "
        "changes permanently without being told again."
    )


def _perspectives() -> dict:
    return {
        "human": "silence is the test",
        "learner": "knowledge must become automatic",
        "machine": "lifecycle record with re-tell metric",
    }


def _distilled(loop, lesson=None):
    lesson = lesson or loop.capture(_teaching(), teacher="Shawn", source="test")
    return loop.distill(
        lesson,
        essence="Behavior change without repetition is the only proof of learning.",
        perspectives=_perspectives(),
        actionable_rule="Run every teaching through the five-stage loop.",
        machine_check="verify.py exits 0",
    )


def _encoded(loop, lesson=None, check_name="always_pass"):
    lesson = _distilled(loop, lesson)
    rec = enc_mod.make_encoding(
        test_location="tests/test_learn_once.py",
        gate="tools/learn_once/verify.py",
        manifest_entry="kernel/protocol/protocol_manifest.json#SN-LEARN-ONCE",
    )
    lesson = loop.encode(lesson, rec)
    lesson.check = {"kind": "python", "name": check_name}
    from tools.learn_once import registry as reg

    reg.upsert(loop.registry_path, lesson)
    return lesson


# ---- the metric: zero re-tells --------------------------------------------


def test_retell_is_loop_failure(tmp_path):
    """The core falsifier: teacher repeats an encoded lesson -> FAILED + bug."""
    loop = _loop(tmp_path)
    lesson = _encoded(loop)
    assert lesson.stage == Stage.ENCODED.value

    result = loop.record_retell(lesson.lesson_id, repeated_by="Shawn",
                                note="had to say it again")

    assert result["outcome"] == "LOOP_FAILURE"
    assert result["bug"]["bug"] == f"LEARN-ONCE-FAILURE/{lesson.lesson_id}"
    updated = loop.get(lesson.lesson_id)
    assert updated.stage == Stage.FAILED.value
    assert updated.re_tells == 1
    assert result["bug"]["bug"] in updated.bug_refs


def test_retell_before_encoding_is_not_loop_failure(tmp_path):
    """A repeat while still CAPTURED is unfortunate, not a loop failure —
    the loop never had the lesson yet."""
    loop = _loop(tmp_path)
    lesson = loop.capture(_teaching(), teacher="Shawn", source="test")
    result = loop.record_retell(lesson.lesson_id, repeated_by="Shawn")
    assert result["outcome"] == "REPEATED_BEFORE_ENCODING"
    assert loop.get(lesson.lesson_id).stage == Stage.CAPTURED.value


def test_unknown_teaching_routes_to_intake(tmp_path):
    """A re-tell for something never captured must not fabricate a failure."""
    loop = _loop(tmp_path)
    result = loop.record_retell("LO-9999", repeated_by="Shawn")
    assert result["outcome"] == "UNKNOWN_TEACHING"


def test_promote_refused_with_retells(tmp_path):
    """A repeated teaching can never be ACTIVE, even if its check passes."""
    loop = _loop(tmp_path)
    lesson = _encoded(loop)
    loop.verify(lesson.lesson_id)
    loop.record_retell(lesson.lesson_id, repeated_by="Shawn")
    with pytest.raises(ValueError, match="requires VERIFIED"):
        loop.promote(lesson.lesson_id)


# ---- verification honesty --------------------------------------------------


def test_unencoded_lesson_cannot_verify(tmp_path):
    loop = _loop(tmp_path)
    lesson = _distilled(loop)  # DISTILLED, never encoded
    with pytest.raises(ValueError, match="requires an encoded lesson"):
        loop.verify(lesson.lesson_id)


def test_behavioral_regression_detected(tmp_path):
    """A VERIFIED lesson whose check starts failing must become REGRESSED,
    and the audit must name it unlearned."""
    loop = _loop(tmp_path)
    lesson = _encoded(loop, check_name="always_pass")
    passed, _ = loop.verify(lesson.lesson_id)
    assert passed
    assert loop.get(lesson.lesson_id).stage == Stage.VERIFIED.value

    # the world changed: the check now fails
    lesson = loop.get(lesson.lesson_id)
    lesson.check = {"kind": "python", "name": "always_fail"}
    from tools.learn_once import registry as reg

    reg.upsert(loop.registry_path, lesson)

    passed, _ = loop.verify(lesson.lesson_id)
    assert not passed
    assert loop.get(lesson.lesson_id).stage == Stage.REGRESSED.value

    report = loop.audit()
    assert not report["ok"]
    assert any(r["lesson_id"] == lesson.lesson_id for r in report["failures"])


def test_zero_retells_full_loop_learned(tmp_path):
    """The happy path: capture -> distill -> encode -> verify -> promote,
    zero re-tells, audit reports LEARNED."""
    loop = _loop(tmp_path)
    lesson = _encoded(loop, check_name="always_pass")
    passed, _ = loop.verify(lesson.lesson_id)
    assert passed
    loop.promote(lesson.lesson_id)
    assert loop.get(lesson.lesson_id).stage == Stage.ACTIVE.value
    report = loop.audit()
    assert report["ok"]
    assert report["learned"] == 1


# ---- encoding honesty: not just a note -------------------------------------


def test_encoding_requires_behavioral_test(tmp_path):
    loop = _loop(tmp_path)
    lesson = _distilled(loop)
    rec = EncodingRecord()
    rec.test = EncodingTarget(kind="test", status="TODO")
    rec.gate = EncodingTarget(kind="gate", location="tools/learn_once/verify.py",
                              status="DONE")
    with pytest.raises(ValueError, match="behavioral test is mandatory"):
        loop.encode(lesson, rec)


def test_encoding_not_just_a_note(tmp_path):
    """Test DONE but nothing in the machine -> refused. Prose is not learning."""
    loop = _loop(tmp_path)
    lesson = _distilled(loop)
    rec = EncodingRecord()
    rec.test = EncodingTarget(kind="test", location="tests/test_learn_once.py",
                              status="DONE")
    # every machine target NA: the lesson would exist only as prose
    for kind in ("law_file", "gate", "cron_body", "manifest_entry"):
        setattr(rec, kind, EncodingTarget(kind=kind, status="NA",
                                          note="not applicable here"))
    issues = checklist_issues(rec)
    assert any("must live in the machine" in i for i in issues)
    with pytest.raises(ValueError, match="must live in the machine"):
        loop.encode(lesson, rec)


def test_na_requires_reason(tmp_path):
    rec = enc_mod.make_encoding(test_location="tests/test_learn_once.py",
                                gate="tools/learn_once/verify.py")
    rec.cron_body = EncodingTarget(kind="cron_body", status="NA")  # no reason
    issues = checklist_issues(rec)
    assert any("cron_body" in i and "no reason" in i for i in issues)


# ---- stage order and distillation depth -------------------------------------


def test_stage_order_enforced(tmp_path):
    loop = _loop(tmp_path)
    lesson = loop.capture(_teaching(), teacher="Shawn", source="test")
    rec = enc_mod.make_encoding(test_location="t", gate="g")
    with pytest.raises(ValueError, match="requires stage DISTILLED"):
        loop.encode(lesson, rec)  # CAPTURED -> encode is illegal
    # distill once (legal), then distill again -> illegal, already DISTILLED
    lesson = loop.distill(
        lesson,
        essence="Behavior change without repetition proves learning, permanently.",
        perspectives=_perspectives(),
        actionable_rule="Run every teaching through the five-stage loop.",
        machine_check="verify.py",
    )
    assert lesson.stage == Stage.DISTILLED.value
    with pytest.raises(ValueError, match="requires stage CAPTURED"):
        loop.distill(
            lesson,
            essence="Behavior change without repetition proves learning, permanently.",
            perspectives=_perspectives(),
            actionable_rule="Run every teaching through the five-stage loop.",
            machine_check="verify.py",
        )


def test_ib_requires_three_perspectives(tmp_path):
    """Taught != understood: a shallow IB (missing perspectives) is refused."""
    loop = _loop(tmp_path)
    lesson = loop.capture(_teaching(), teacher="Shawn", source="test")
    with pytest.raises(ValueError, match="perspectives"):
        distill(lesson,
                essence="Behavior change without repetition proves learning.",
                perspectives={"human": "only one view"},  # missing learner/machine
                actionable_rule="Run every teaching through the loop.",
                machine_check="verify.py")


def test_capture_rejects_empty_or_unattributed(tmp_path):
    with pytest.raises(ValueError, match="must not be empty"):
        capture("", teacher="Shawn", source="test")
    with pytest.raises(ValueError, match="must be named"):
        capture(_teaching(), teacher="  ", source="test")


# ---- registry ----------------------------------------------------------------


def test_registry_roundtrip(tmp_path):
    loop = _loop(tmp_path)
    lesson = _encoded(loop)
    reloaded = loop.get(lesson.lesson_id)
    assert reloaded.title == lesson.title
    assert reloaded.stage == Stage.ENCODED.value
    assert reloaded.ib["essence"]
    assert reloaded.encoding["test"]["status"] == "DONE"
    # file is JSONL: one object per line
    lines = (tmp_path / "lessons.jsonl").read_text().strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["lesson_id"] == lesson.lesson_id


# ---- integration: the manifest carries the law ---------------------------------


def test_manifest_entry_present():
    """SN-LEARN-ONCE is a ratified law in protocol_manifest.json, machine-checkable."""
    manifest = json.loads(
        (ROOT / "kernel" / "protocol" / "protocol_manifest.json").read_text()
    )
    laws = {l["id"]: l for l in manifest["laws"]}
    assert "SN-LEARN-ONCE" in laws, "Learn-Once Loop missing from protocol manifest"
    entry = laws["SN-LEARN-ONCE"]
    assert entry.get("status") == "RATIFIED"
    assert entry.get("check") == "tools/learn_once/verify.py"
    assert entry.get("enforcement") == "learn_once_gate"
    assert "re-tell" in entry.get("statement", "")


def test_manifest_ids_still_unique():
    manifest = json.loads(
        (ROOT / "kernel" / "protocol" / "protocol_manifest.json").read_text()
    )
    ids = [l["id"] for l in manifest["laws"]]
    assert len(ids) == len(set(ids))


def test_verify_cli_gate(tmp_path):
    """The manifest check target: exit 0 clean, exit 1 on loop failure.

    Uses a shell check because the CLI runs as a fresh process — named
    python checks registered in this test process are not visible to it.
    """
    loop = _loop(tmp_path)
    lesson = _encoded(loop, check_name="always_pass")
    # swap to a process-independent shell check for the CLI run
    lesson.check = {"kind": "shell", "cmd": "true"}
    from tools.learn_once import registry as reg

    reg.upsert(loop.registry_path, lesson)
    reg_path = str(loop.registry_path)

    ok = subprocess.run(
        [sys.executable, "tools/learn_once/verify.py", "--registry", reg_path],
        capture_output=True, text=True, timeout=120, cwd=ROOT,
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # now break it: record a re-tell -> FAILED
    loop.record_retell(lesson.lesson_id, repeated_by="Shawn")
    bad = subprocess.run(
        [sys.executable, "tools/learn_once/verify.py", "--registry", reg_path],
        capture_output=True, text=True, timeout=120, cwd=ROOT,
    )
    assert bad.returncode == 1
    assert "FAILED" in bad.stdout or "FAILURES" in bad.stdout
