"""Tests for tools/successor_ingest — pure core, zero network.

The reader and the applier are injected stubs everywhere. The only
network seam (read.fetch_verified_rows) is tested for its fail-closed
contract by code inspection, not by hitting the live store here.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from successor_ingest import ingest, receipt as receipt_mod, select, verify
from successor_ingest.ingest import run_chain
from successor_ingest.models import Applicability, Lesson
from successor_ingest.read import IngestError
from successor_ingest.select import SelectionError


def _row(**kw):
    base = {
        "id": "66122e1e-677b-4ef0-a765-80d08ccfa85b",
        "target_id": "lesson:TIER1-2026-10-08-T14",
        "level": "E5_CAN_TEACH",
        "status": "ACTIVE",
        "provenance": "TRIAL_EVIDENCE",
        "verification_method": "Independent verification by Naya 1: 40/40 vs 28/40",
        "claim": "Never write state files through inline conditional expressions",
        "retrieved_at": "2026-10-09T00:00:00+00:00",
        "query": "SELECT ...",
    }
    base.update(kw)
    return base


def _t14():
    return select.eligible_lessons([_row()])[0]


COMPLIANT = '''def save_state(path, data):
    import json
    if data:
        status = "ok"
    else:
        status = "failed"
    with open(path, "w") as f:
        json.dump({"status": status, "data": data}, f)
    return status
'''

VIOLATING = '''def save_state(path, data):
    import json
    status = "ok" if data else "failed"
    with open(path, "w") as f:
        json.dump({"status": status, "data": data}, f)
    return status
'''

BRIEF = "Write a Python function save_state(path, data) that writes data as JSON state to path."


# ---- selection ---------------------------------------------------------

def test_eligible_accepts_verified_trial_lesson():
    lessons = select.eligible_lessons([_row()])
    assert len(lessons) == 1
    assert lessons[0].target_id == "lesson:TIER1-2026-10-08-T14"


def test_eligible_refuses_candidate():
    with pytest.raises(SelectionError) as e:
        select.eligible_lessons([_row(status="CANDIDATE")])
    assert e.value.code == "NO_VERIFIED_LESSONS"


def test_eligible_refuses_lower_level():
    with pytest.raises(SelectionError) as e:
        select.eligible_lessons([_row(level="E1_UNDERSTANDS")])
    assert e.value.code == "NO_VERIFIED_LESSONS"


def test_eligible_refuses_observation_provenance():
    # The E5 OBSERVATION row is a different kind, not a verified law.
    with pytest.raises(SelectionError) as e:
        select.eligible_lessons([_row(provenance="OBSERVATION")])
    assert e.value.code == "NO_VERIFIED_LESSONS"


def test_eligible_refuses_empty_store():
    with pytest.raises(SelectionError) as e:
        select.eligible_lessons([])
    assert e.value.code == "NO_VERIFIED_LESSONS"


def test_match_task_picks_family_lesson():
    assert select.match_task([_t14()], "state_file").target_id.endswith("T14")


def test_match_task_unknown_family_closed_world():
    with pytest.raises(SelectionError) as e:
        select.match_task([_t14()], "teleportation")
    assert e.value.code == "UNKNOWN_TASK_FAMILY"


def test_match_task_no_transplant_across_families():
    with pytest.raises(SelectionError) as e:
        select.match_task([_t14()], "dispatch")
    assert e.value.code == "NO_APPLICABLE_LESSON"


def test_applicability_applicable():
    a = select.check_applicability(_t14(), "state_file", BRIEF)
    assert a.verdict == "APPLICABLE"


def test_applicability_rejects_brief_without_triggers():
    a = select.check_applicability(_t14(), "state_file", "Write a poem about the sea.")
    assert a.verdict == "NOT_APPLICABLE"


def test_applicability_rejects_transplant():
    t11 = _t14()
    t11 = Lesson(**{**t11.__dict__, "target_id": "lesson:TIER1-2026-10-08-T11"})
    a = select.check_applicability(t11, "state_file", BRIEF)
    assert a.verdict == "NOT_APPLICABLE"


# ---- verify ---------------------------------------------------------------

def test_verifier_passes_compliant_code():
    r = verify.verify("state_file", COMPLIANT)
    assert r.verdict == "PASS"
    assert r.evidence == "ifexp_count=0"


def test_verifier_fails_ternary():
    r = verify.verify("state_file", VIOLATING)
    assert r.verdict == "FAIL"
    assert r.evidence == "ifexp_count=1"


def test_verifier_fails_unparseable():
    r = verify.verify("state_file", "def broken(:")
    assert r.verdict == "FAIL"


def test_verifier_unknown_family():
    r = verify.verify("teleportation", COMPLIANT)
    assert r.verdict == "FAIL"
    assert r.evidence == "no_verifier"


# ---- receipt -----------------------------------------------------------------

def test_receipt_sha_verifies_and_tamper_breaks():
    lesson = _t14()
    app = Applicability("APPLICABLE", "ok")
    vr = verify.verify("state_file", COMPLIANT)
    r = receipt_mod.emit_reuse_receipt(
        lesson=lesson, task_family="state_file", task_brief=BRIEF,
        cold_agent="cold-test", applicability=app,
        application_artifact=COMPLIANT, verify_result=vr,
        reused=True, reuse_reason="test",
    )
    assert r["schema"] == "naya.successor.reuse_receipt.v1"
    assert receipt_mod.verify_receipt_sha(r) is True
    r["successor_reuse"]["reused"] = False  # tamper
    assert receipt_mod.verify_receipt_sha(r) is False


# ---- chain --------------------------------------------------------------------

def _reader(rows=None):
    def _r():
        return rows if rows is not None else [_row()]
    return _r


def test_chain_partial_with_uninstrumented_smart_link():
    report, rcpt = run_chain(
        BRIEF, "state_file", "cold-test",
        reader=_reader(), applier=lambda brief, lesson: COMPLIANT,
    )
    assert [s.stage for s in report.stages] == list(ingest.STAGES)
    states = {s.stage: s.state for s in report.stages}
    assert states["COLD RETRIEVE"] == "PRESENT"
    assert states["INDEPENDENTLY VERIFY"] == "PRESENT"
    assert states["SMART LINK"] == "UNINSTRUMENTED"  # honest corpus gap
    assert report.verdict == "PARTIAL"
    assert rcpt["successor_reuse"]["reused"] is True
    assert receipt_mod.verify_receipt_sha(rcpt) is True


def test_chain_does_not_claim_reuse_on_violation():
    report, rcpt = run_chain(
        BRIEF, "state_file", "cold-test",
        reader=_reader(), applier=lambda brief, lesson: VIOLATING,
    )
    assert rcpt["successor_reuse"]["reused"] is False
    assert "NOT claimed" in rcpt["successor_reuse"]["reason"]
    # stages still all resolve — negative evidence is evidence
    assert report.verdict == "PARTIAL"


def test_chain_fails_closed_on_unreachable_store():
    def _boom():
        raise IngestError("STORE_UNREACHABLE", "nope")
    with pytest.raises(IngestError):
        run_chain(BRIEF, "state_file", "cold-test", reader=_boom,
                  applier=lambda b, l: COMPLIANT)


def test_chain_fails_closed_on_empty_store():
    with pytest.raises(SelectionError) as e:
        run_chain(BRIEF, "state_file", "cold-test", reader=_reader([]),
                  applier=lambda b, l: COMPLIANT)
    assert e.value.code == "NO_VERIFIED_LESSONS"


def test_chain_fails_closed_on_unknown_family():
    with pytest.raises(SelectionError) as e:
        run_chain(BRIEF, "teleportation", "cold-test", reader=_reader(),
                  applier=lambda b, l: COMPLIANT)
    assert e.value.code == "UNKNOWN_TASK_FAMILY"


def test_chain_fails_closed_without_applier():
    with pytest.raises(IngestError) as e:
        run_chain(BRIEF, "state_file", "cold-test", reader=_reader())
    assert e.value.code == "NO_APPLIER"


# ---- portable transport resolution (R2) --------------------------------------

import json as _json
import os as _os
import sys as _sys

from successor_ingest import read as read_mod


def _clean_env(monkeypatch):
    for k in ("NAYA_LESSON_TRANSPORT", "SB_API", "NAYA_LESSON_PROJECT_REF"):
        monkeypatch.delenv(k, raising=False)


def test_resolve_transport_prefers_explicit_env(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("NAYA_LESSON_TRANSPORT", "/tmp/fake-transport")
    monkeypatch.setenv("SB_API", "/tmp/other-transport")
    monkeypatch.setattr(read_mod.shutil, "which", lambda name: "/usr/bin/sb-api")
    path, source = read_mod.resolve_transport()
    assert path == "/tmp/fake-transport"
    assert source == "NAYA_LESSON_TRANSPORT"


def test_resolve_transport_falls_back_to_sb_api_env(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("SB_API", "/tmp/connector-sb-api")
    monkeypatch.setattr(read_mod.shutil, "which", lambda name: "/usr/bin/sb-api")
    path, source = read_mod.resolve_transport()
    assert path == "/tmp/connector-sb-api"
    assert source == "SB_API"


def test_resolve_transport_falls_back_to_path(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setattr(read_mod.shutil, "which", lambda name: "/usr/bin/sb-api")
    path, source = read_mod.resolve_transport()
    assert path == "/usr/bin/sb-api"
    assert source == "PATH"


def test_resolve_transport_refuses_without_hardcoded_path(monkeypatch):
    # No env, nothing on PATH -> STORE_UNREACHABLE naming the prerequisite,
    # NOT a failure on a hardcoded private-machine path.
    _clean_env(monkeypatch)
    monkeypatch.setattr(read_mod.shutil, "which", lambda name: None)
    with pytest.raises(IngestError) as e:
        read_mod.resolve_transport()
    assert e.value.code == "STORE_UNREACHABLE"
    assert "NAYA_LESSON_TRANSPORT" in e.value.detail
    assert "/home/hatch" not in e.value.detail


def test_resolve_project_ref_default_and_override(monkeypatch):
    _clean_env(monkeypatch)
    assert read_mod.resolve_project_ref() == read_mod.DEFAULT_PROJECT_REF
    monkeypatch.setenv("NAYA_LESSON_PROJECT_REF", "otherproj123")
    assert read_mod.resolve_project_ref() == "otherproj123"


def test_fetch_verified_rows_stamps_provenance_via_injected_transport():
    # Pure: injected transport argv, zero network. The fake "store" prints
    # one JSON row; the seam stamps retrieved_at + exact query.
    row = {
        "id": "abc", "target_id": "lesson:TIER1-2026-10-08-T14",
        "level": "E5_CAN_TEACH", "status": "ACTIVE",
        "provenance": "TRIAL_EVIDENCE", "verification_method": "m",
        "claim": "c",
    }
    fake = [_sys.executable, "-c",
            "import json,sys; sys.stdout.write(json.dumps(["
            + _json.dumps(row) + "]))"]
    rows = read_mod.fetch_verified_rows(transport=fake, project_ref="testproj")
    assert len(rows) == 1
    assert rows[0]["retrieved_at"]
    assert rows[0]["query"] == read_mod.QUERY


def test_fetch_verified_rows_refuses_on_bad_transport_output():
    fake = [_sys.executable, "-c", "print('not json')"]
    with pytest.raises(IngestError) as e:
        read_mod.fetch_verified_rows(transport=fake)
    assert e.value.code == "STORE_UNREACHABLE"


def test_fetch_verified_rows_refuses_on_missing_transport_binary():
    with pytest.raises(IngestError) as e:
        read_mod.fetch_verified_rows(transport="/nonexistent/transport-binary")
    assert e.value.code == "STORE_UNREACHABLE"
