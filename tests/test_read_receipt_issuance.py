"""Run-attested read-receipt issuance (option C, Shawn's word 2026-10-11).

The unkeyed SHA-256 in read_receipt.py proves INTEGRITY, not ISSUANCE.
These tests prove the new layer:

  (a) a forged/self-minted receipt is REJECTED by verify_issuance
  (b) a properly attested receipt PASSES verify_issuance (API mocked)
  (c) the 6-check boot gate works with the new attested path
  (d) the original forgery from the decision packet still passes the OLD
      integrity check but FAILS the new issuance check — the gap is closed

HONEST CAVEAT (in the code, not just here): attestation proves the trusted
runner ran, not which agent it ran for.
"""
import hashlib
import io
import json
import zipfile
from unittest import mock

import pytest

from kernel.protocol.read_receipt import (
    ReadReceipt,
    issue_receipt,
    PROTOCOL_VERSION,
)
from kernel.protocol.read_receipt_issuance import (
    MINT_WORKFLOW_PATH,
    MINT_ARTIFACT_PREFIX,
    SCHEMA,
    verify_issuance,
    envelope_from_receipt,
)
from kernel.protocol.cold_start_gate import (
    ColdStartState,
    run_cold_start,
    run_cold_start_attested,
)

CORRECT = {
    "q1": "Shawn Vibert",
    "q2": "production deploys, credentials and money, destructive actions, ratification, security and privacy",
    "q3": "No, never",
    "q4": "9.0",
    "q5": "independent evidence and proof",
}

REPO = "SoulSchoolAcademy/NayaPOWER"
TOKEN = "test-token"
RUN_ID = 12345678


def _receipt_dict(agent_id="naya-test"):
    r = issue_receipt(agent_id, CORRECT)
    assert r.passed
    return {
        "agent_id": r.agent_id,
        "protocol_version": r.protocol_version,
        "answers": r.answers,
        "passed": r.passed,
        "issued_at": r.issued_at,
        "receipt_hash": r.receipt_hash,
    }


def _attestation(run_id=RUN_ID):
    return {
        "workflow": MINT_WORKFLOW_PATH,
        "run_id": run_id,
        "run_attempt": 1,
        "minted_at": "2026-10-11T14:00:00Z",
        "_note": "test fixture",
    }


def _good_envelope(agent_id="naya-test", run_id=RUN_ID):
    return envelope_from_receipt(_receipt_dict(agent_id), _attestation(run_id))


def _mock_api_ok(envelope_bytes):
    """Mock _api/_download_bytes for a fully valid attested run."""
    run_payload = {
        "event": "workflow_dispatch",
        "path": MINT_WORKFLOW_PATH,
        "conclusion": "success",
        "head_repository": {"full_name": REPO},
    }
    arts_payload = {"artifacts": [
        {"name": "%s%d" % (MINT_ARTIFACT_PREFIX, RUN_ID),
         "archive_download_url": "https://api.github.com/fake.zip"},
    ]}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("receipt.json", envelope_bytes)
    blob = buf.getvalue()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return arts_payload
        return run_payload

    def fake_download(url, token):
        return blob

    return mock.patch(
        "kernel.protocol.read_receipt_issuance._api", side_effect=fake_api), \
        mock.patch(
        "kernel.protocol.read_receipt_issuance._download_bytes",
        side_effect=fake_download)


# ---------- (a) forgeries are rejected ----------

def test_self_minted_receipt_rejected_no_attestation():
    """The exact old-world forgery: correct answers, valid hash, no attestation."""
    envelope, raw = envelope_from_receipt(_receipt_dict(), attestation=None)
    # envelope_from_receipt with None attestation -> attestation key present but None
    violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert violations, "self-minted receipt must not pass issuance"
    assert any("ISSUANCE_UNATTESTED" in v for v in violations)


def test_envelope_without_attestation_key_rejected():
    envelope = {"schema": SCHEMA, "receipt": _receipt_dict()}
    raw = json.dumps(envelope, sort_keys=True).encode()
    violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_UNATTESTED" in v for v in violations)


def test_wrong_schema_rejected():
    envelope, raw = _good_envelope()
    envelope["schema"] = "naya/something-else-v1"
    violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_WRONG_SCHEMA" in v for v in violations)


def test_unpassed_receipt_rejected():
    rd = _receipt_dict()
    rd["passed"] = False
    envelope, raw = envelope_from_receipt(rd, _attestation())
    violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_NOT_PASSED" in v for v in violations)


def test_fake_run_id_rejected_unverifiable():
    envelope, raw = _good_envelope(run_id=99999999)

    def fake_api(method, path, token, body=None):
        raise RuntimeError("GitHub API GET -> 404")

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_UNVERIFIABLE" in v for v in violations)


def test_wrong_workflow_rejected():
    envelope, raw = _good_envelope()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return {"artifacts": []}
        return {"event": "workflow_dispatch",
                "path": ".github/workflows/some-other.yml",
                "conclusion": "success",
                "head_repository": {"full_name": REPO}}

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_WRONG_WORKFLOW" in v for v in violations)


def test_wrong_event_rejected():
    envelope, raw = _good_envelope()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return {"artifacts": []}
        return {"event": "push",
                "path": MINT_WORKFLOW_PATH,
                "conclusion": "success",
                "head_repository": {"full_name": REPO}}

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_WRONG_EVENT" in v for v in violations)


def test_failed_run_rejected():
    envelope, raw = _good_envelope()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return {"artifacts": []}
        return {"event": "workflow_dispatch",
                "path": MINT_WORKFLOW_PATH,
                "conclusion": "failure",
                "head_repository": {"full_name": REPO}}

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_RUN_NOT_SUCCESS" in v for v in violations)


def test_foreign_repo_run_rejected():
    envelope, raw = _good_envelope()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return {"artifacts": []}
        return {"event": "workflow_dispatch",
                "path": MINT_WORKFLOW_PATH,
                "conclusion": "success",
                "head_repository": {"full_name": "EvilOrg/NayaPOWER"}}

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_FOREIGN_RUN" in v for v in violations)


def test_tampered_bytes_rejected():
    """Attestation points to a real run, but presented bytes differ."""
    envelope, raw = _good_envelope()
    tampered = dict(envelope)
    tampered["receipt"] = dict(envelope["receipt"], agent_id="rogue-seat")
    tampered_raw = json.dumps(tampered, sort_keys=True).encode()
    api_patch, dl_patch = _mock_api_ok(raw)  # artifact holds the ORIGINAL bytes
    with api_patch, dl_patch:
        violations = verify_issuance(tampered, tampered_raw, TOKEN, REPO)
    assert any("ISSUANCE_BYTES_MISMATCH" in v for v in violations)


def test_missing_artifact_rejected():
    envelope, raw = _good_envelope()

    def fake_api(method, path, token, body=None):
        if path.endswith("/artifacts"):
            return {"artifacts": []}
        return {"event": "workflow_dispatch",
                "path": MINT_WORKFLOW_PATH,
                "conclusion": "success",
                "head_repository": {"full_name": REPO}}

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_ARTIFACT_MISSING" in v for v in violations)


# ---------- (b) valid issuance passes ----------

def test_valid_attested_receipt_passes():
    envelope, raw = _good_envelope()
    api_patch, dl_patch = _mock_api_ok(raw)
    with api_patch, dl_patch:
        violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert violations == [], violations


# ---------- (d) the packet's forgery: old verify passes, new issuance fails ----------

def test_packet_forgery_old_verify_passes_new_issuance_fails():
    """Reproduces the decision packet's demonstration: a hand-rolled
    hashlib.sha256 mint verifies under the OLD integrity check but carries
    no attestation, so the NEW issuance check rejects it."""
    forged = ReadReceipt(
        agent_id="rogue-seat",
        protocol_version=PROTOCOL_VERSION,
        answers={q["id"]: True for q in
                 __import__("kernel.protocol.read_receipt",
                            fromlist=["AUTHORITY_QUESTIONS"]).AUTHORITY_QUESTIONS},
        passed=True,
    ).sign()
    assert forged.verify(), "old integrity check passes on the forgery (the hole)"

    envelope = {"schema": SCHEMA,
                "receipt": {"agent_id": forged.agent_id,
                            "protocol_version": forged.protocol_version,
                            "answers": forged.answers,
                            "passed": forged.passed,
                            "issued_at": forged.issued_at,
                            "receipt_hash": forged.receipt_hash}}
    raw = json.dumps(envelope, sort_keys=True).encode()
    violations = verify_issuance(envelope, raw, TOKEN, REPO)
    assert any("ISSUANCE_UNATTESTED" in v for v in violations), \
        "new issuance check must reject the unattested forgery"


# ---------- (c) boot gate with the new path ----------

def _attested_state(agent_id="naya-9", run_id=RUN_ID, envelope=None, raw=None):
    if envelope is None or raw is None:
        envelope, raw = _good_envelope(agent_id, run_id)
    return ColdStartState(
        agent_id=agent_id,
        human_director="Shawn Vibert",
        lane="verify",
        authority_summary="Protected gates: production deploys, credentials/money, "
                          "destructive actions, ratification, security/privacy.",
        current_truth_location="coordination feed #1354 and current main",
        next_action="re-anchor on live main and check the board",
        receipt=issue_receipt(agent_id, CORRECT),
        receipt_envelope=envelope,
        receipt_envelope_bytes=raw,
    )


def test_attested_boot_gate_passes_valid_issuance():
    envelope, raw = _good_envelope("naya-9")
    api_patch, dl_patch = _mock_api_ok(raw)
    with api_patch, dl_patch:
        res = run_cold_start_attested(
            _attested_state("naya-9", RUN_ID, envelope, raw), TOKEN, REPO)
    assert res.passed, res.failures


def test_attested_boot_gate_rejects_self_minted():
    """No envelope at all -> the attested gate fails closed."""
    s = _attested_state()
    s.receipt_envelope = None
    s.receipt_envelope_bytes = None
    # The plain gate still passes (integrity layer) — the hole, documented.
    assert run_cold_start(s).passed
    # The attested gate fails closed.
    res = run_cold_start_attested(s, TOKEN, REPO)
    assert not res.passed
    assert any("attestation" in f.lower() for f in res.failures)


def test_attested_boot_gate_rejects_forged_attestation():
    s = _attested_state(run_id=99999999)

    def fake_api(method, path, token, body=None):
        raise RuntimeError("GitHub API GET -> 404")

    with mock.patch("kernel.protocol.read_receipt_issuance._api",
                     side_effect=fake_api):
        res = run_cold_start_attested(s, TOKEN, REPO)
    assert not res.passed
    assert any("ISSUANCE_UNVERIFIABLE" in f for f in res.failures)


def test_attested_boot_gate_keeps_all_six_standard_checks():
    """The attested path runs the standard 6 checks too — a bad state
    fails even with a valid envelope."""
    s = _attested_state()
    s.human_director = "someone else"  # breaks check 2
    envelope, raw = _good_envelope("naya-9")
    api_patch, dl_patch = _mock_api_ok(raw)
    with api_patch, dl_patch:
        res = run_cold_start_attested(s, TOKEN, REPO)
    assert not res.passed
    assert any("Shawn" in f for f in res.failures)


# ---------- mint script ----------

def test_mint_refuses_without_run_id(tmp_path):
    """The mint script refuses outside the trusted runner."""
    import subprocess, sys, os
    out = tmp_path / "receipt.json"
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_RUN_ID"}
    r = subprocess.run(
        [sys.executable, "tools/read_receipt_mint.py",
         "--agent-id", "naya-test",
         "--answers", json.dumps(CORRECT),
         "--out", str(out)],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert r.returncode == 2
    assert "GITHUB_RUN_ID" in r.stderr
    assert not out.exists()


def test_mint_refuses_wrong_answers(tmp_path):
    import subprocess, sys, os
    out = tmp_path / "receipt.json"
    env = dict(os.environ, GITHUB_RUN_ID="12345", GITHUB_RUN_ATTEMPT="1")
    bad = dict(CORRECT, q3="yes, scores override gates")
    r = subprocess.run(
        [sys.executable, "tools/read_receipt_mint.py",
         "--agent-id", "naya-test",
         "--answers", json.dumps(bad),
         "--out", str(out)],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert r.returncode == 2
    assert "failed grading" in r.stderr
    assert not out.exists()


def test_mint_produces_attested_envelope(tmp_path):
    import subprocess, sys, os
    out = tmp_path / "receipt.json"
    env = dict(os.environ, GITHUB_RUN_ID="12345", GITHUB_RUN_ATTEMPT="1")
    r = subprocess.run(
        [sys.executable, "tools/read_receipt_mint.py",
         "--agent-id", "naya-test",
         "--answers", json.dumps(CORRECT),
         "--out", str(out)],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert r.returncode == 0, r.stderr
    envelope = json.loads(out.read_text())
    assert envelope["schema"] == SCHEMA
    assert envelope["receipt"]["passed"] is True
    assert envelope["receipt"]["agent_id"] == "naya-test"
    assert envelope["attestation"]["run_id"] == 12345
    assert envelope["attestation"]["workflow"] == MINT_WORKFLOW_PATH
    # The minted receipt passes the integrity check (fail-fast at mint).
    rc = ReadReceipt(
        agent_id=envelope["receipt"]["agent_id"],
        protocol_version=envelope["receipt"]["protocol_version"],
        answers=envelope["receipt"]["answers"],
        passed=envelope["receipt"]["passed"],
        issued_at=envelope["receipt"]["issued_at"],
        receipt_hash=envelope["receipt"]["receipt_hash"],
    )
    assert rc.verify()
