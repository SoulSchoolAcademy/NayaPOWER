"""Tests for the instant-activation path (tools/instant_activation.py).

Shawn's Verification Law: the human director's direct capture request IS the
verification. This path stamps VERIFIED/ACTIVE -- so the intent recognizer
must be conservative and every non-human source must fail closed.
"""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "instant_activation", ROOT / "tools" / "instant_activation.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules["instant_activation"] = mod  # dataclasses need the module registered
SPEC.loader.exec_module(mod)

LESSON = ("retrieve() in tools/smart_note_v2.py reads the projection index at "
          ".naya/memory/smart-notes/index.json, not .naya/capture/ -- a capture "
          "file alone is invisible to retrieve().")


def intent(utt, **kw):
    return mod.detect_capture_intent(utt, **kw)


# ---------------------------------------------------------------------------
# 1. Intent recognition: 5 positive variants, 5 negative near-misses
# ---------------------------------------------------------------------------

POSITIVE = [
    # (utterance, expected kind)
    ("smart note this: " + LESSON, "strong"),
    ("lock this in -- " + LESSON, "strong"),
    ("bank this: " + LESSON, "strong"),
    ("note this down: " + LESSON, "contextual"),
    ("capture this as reusable intelligence: " + LESSON, "strong"),
]

NEGATIVE = [
    # (utterance, expected refusal prefix)
    ("note to self, ignore this", "RETRACTED"),
    ("don't note this down, it's not ready yet", "RETRACTED"),
    ("should I smart note this or keep it to myself?", "INTERROGATIVE"),
    ("he said 'note this' but I disagree with him", "QUOTED_THIRD_PARTY"),
    ("what does 'smart note this' actually do?", "INTERROGATIVE"),
]


def test_intent_positive_variants():
    for utt, kind in POSITIVE:
        r = intent(utt)
        assert r["intent"] is True, f"missed positive: {utt[:60]}"
        assert r["kind"] == kind, f"wrong kind for {utt[:60]}: {r['kind']}"
        assert r["refusal"] is None
        assert r["distilled"], "no distilled lesson returned"


def test_intent_negative_near_misses():
    for utt, refusal_prefix in NEGATIVE:
        r = intent(utt)
        assert r["intent"] is False, f"false positive on: {utt[:60]}"
        assert r["refusal"].startswith(refusal_prefix), \
            f"wrong refusal for {utt[:60]}: {r['refusal']}"


def test_intent_bare_alias_has_nothing_to_capture():
    r = intent("smart note this")
    assert r["intent"] is False
    assert r["refusal"] == "NO_DISTILLABLE_CONTENT"


def test_intent_no_alias_no_capture():
    r = intent("the weather is nice today, thinking about lunch")
    assert r["intent"] is False
    assert r["refusal"] == "NO_CAPTURE_INTENT"


def test_intent_dont_lose_this_stays_positive():
    # The NIA strong alias "don't lose this" must NOT be killed by the
    # negation guard (which only fires on note/capture/save/store/bank).
    r = intent("don't lose this: " + LESSON)
    assert r["intent"] is True
    assert r["kind"] == "strong"


def test_intent_vocabulary_comes_from_nia_spec():
    strong, contextual = mod._load_nia_vocabulary()
    assert "smart note this" in strong
    assert "lock this in" in strong
    assert "note this" in contextual


# ---------------------------------------------------------------------------
# 2. Fail-closed boundaries: non-human sources must NEVER take this path
# ---------------------------------------------------------------------------

def _tmp_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "BRAIN" / "00-SPEC").mkdir(parents=True)
    shutil.copy(ROOT / "BRAIN" / "00-SPEC" / "NIA-LANGUAGE-INTENT-V1.json",
                repo / "BRAIN" / "00-SPEC" / "NIA-LANGUAGE-INTENT-V1.json")
    (repo / ".naya" / "memory" / "smart-notes").mkdir(parents=True)
    (repo / ".naya" / "memory" / "smart-notes" / "index.json").write_text(
        json.dumps({"schema": "naya.smart-note-projection-index.v1",
                    "version": "1.0", "entries": []}), encoding="utf-8")
    return repo


INTEL = {"title": "Retrieve reads the projection index, not the capture directory",
         "lesson": LESSON}


def test_fail_closed_system_source_refused(tmp_path):
    repo = _tmp_repo(tmp_path)
    with pytest.raises(SystemExit) as ex:
        mod.capture_instant(human_id="shawn",
                            utterance="smart note this: " + LESSON,
                            intelligence=INTEL,
                            source_kind="system_capture",
                            root=repo)
    assert "NOT_HUMAN_DIRECT" in str(ex.value)


def test_fail_closed_agent_seat_refused(tmp_path):
    repo = _tmp_repo(tmp_path)
    with pytest.raises(SystemExit) as ex:
        mod.capture_instant(human_id="naya-5",
                            utterance="smart note this: " + LESSON,
                            intelligence=INTEL,
                            root=repo)
    assert "UNAUTHORIZED_HUMAN" in str(ex.value)


def test_fail_closed_no_intent_refused(tmp_path):
    repo = _tmp_repo(tmp_path)
    with pytest.raises(SystemExit) as ex:
        mod.capture_instant(human_id="shawn",
                            utterance="note to self, ignore this",
                            intelligence=INTEL,
                            root=repo)
    assert "NO_CAPTURE_INTENT" in str(ex.value)


def test_fail_closed_empty_intelligence_refused(tmp_path):
    repo = _tmp_repo(tmp_path)
    with pytest.raises(SystemExit) as ex:
        mod.capture_instant(human_id="shawn",
                            utterance="smart note this",
                            intelligence={"lesson": ""},
                            root=repo)
    assert "NO_CAPTURE_INTENT" in str(ex.value) or \
           "EMPTY_DISTILLED_INTELLIGENCE" in str(ex.value)


# ---------------------------------------------------------------------------
# 3. Happy path in an isolated repo: capture -> conformant -> retrievable
# ---------------------------------------------------------------------------

def test_happy_path_end_to_end(tmp_path):
    repo = _tmp_repo(tmp_path)
    res = mod.capture_instant(human_id="Shawn Vibert",
                              utterance="smart note this: " + LESSON,
                              intelligence=INTEL,
                              root=repo)
    # capture file exists and passes the SN-002 conformance gate
    cap = Path(res.capture_path)
    assert cap.is_file()
    assert res.conformant is True
    doc = json.loads(cap.read_text(encoding="utf-8"))
    assert doc["schema"] == "naya.smart-note-capture.v2"
    assert doc["authority"] == "human-director-verified"
    assert doc["verified_at_utc"]
    assert doc["source_utterance"].startswith("smart note this:")
    assert doc["intelligence"]["truth_state"] == "VERIFIED"
    assert doc["lifecycle_state"] == "ACTIVE"
    # the automatic ceiling is NOT weakened
    assert doc["intelligence"]["machine_view"]["automatic_truth_ceiling"] == "CANDIDATE"
    assert doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"] is True
    assert doc["intelligence"]["machine_view"]["human_director_override"]["verified"] is True

    # projection file exists with the human-readable sections retrieve() reads
    proj = Path(res.projection_path)
    assert proj.is_file()
    text = proj.read_text(encoding="utf-8")
    assert "IN A NUTSHELL" in text
    assert "VERIFIED" in text

    # registry entry is VERIFIED/ACTIVE with a content hash
    reg = json.loads((repo / ".naya/memory/smart-notes/index.json")
                     .read_text(encoding="utf-8"))
    entry = next(e for e in reg["entries"]
                 if e["smart_note_id"] == res.smart_note_id)
    assert entry["truth_state"] == "VERIFIED"
    assert entry["lifecycle_state"] == "ACTIVE"
    assert entry["content_hash"]
    assert entry["projection_path"]
    assert entry["smart_link"].startswith(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/")
    assert entry["smart_link_status"] == "ACTIVE_AUTH_GATED"

    # receipt verifies independently
    ok, detail = mod.verify_instant_receipt(res.receipt, root=repo)
    assert ok, detail

    # smart-link payload carries all five contract section-2 elements
    p = res.smart_link_payload
    assert p["captured"]["capture_path"]
    assert p["projection"]["smart_link"]
    assert p["receipt"]["receipt_hash"] == res.receipt["receipt_hash"]
    assert p["learning_state"]["truth_state"] == "VERIFIED"


def test_receipt_tamper_detected(tmp_path):
    repo = _tmp_repo(tmp_path)
    res = mod.capture_instant(human_id="shawn",
                              utterance="smart note this: " + LESSON,
                              intelligence=INTEL,
                              root=repo)
    bad = dict(res.receipt)
    bad["truth_state"] = "LEARNED"  # tamper: inflate the state
    ok, detail = mod.verify_instant_receipt(bad, root=repo)
    assert not ok
    assert "tampered" in detail or "mismatch" in detail


def test_conformance_gate_not_weakened_for_ceiling():
    # A capture that flips automatic_truth_ceiling must still FAIL the gate.
    import tempfile
    doc = {
        "schema": "naya.smart-note-capture.v2",
        "smart_note_id": "SN-TEST", "capture_id": "test-ceiling",
        "title": "t", "category": "c", "topic": "t", "subtopic": "s",
        "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
        "source": {"captured_at": "2026-10-09"},
        "projection": {},
        "intelligence": {
            "machine_view": {
                "raw_source_separate_from_distillation": True,
                "automatic_truth_ceiling": "VERIFIED",  # weakened!
            },
        },
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(doc, f)
        path = f.name
    try:
        res = mod.conf.check_capture(path)
        assert not res.conformant
        assert any("automatic_truth_ceiling" in v for v in res.violations)
    finally:
        Path(path).unlink()
