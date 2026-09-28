import json
import os
import urllib.error
import urllib.request
from pathlib import Path


SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
ACCESS_TOKEN = os.environ["SUPABASE_USER_ACCESS_TOKEN"]
PUBLISHABLE_KEY = os.environ["SUPABASE_PUBLISHABLE_KEY"]
REFRESH_TOKEN = os.environ.get("SUPABASE_USER_REFRESH_TOKEN", "")


def _request(url, method="GET", data=None, token=ACCESS_TOKEN):
    headers = {
        "apikey": PUBLISHABLE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode() if data is not None else None,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def authenticated_token():
    status, body = _request(f"{SUPABASE_URL}/auth/v1/user")
    if status == 200 and body.get("id"):
        return ACCESS_TOKEN, body["id"]
    if not REFRESH_TOKEN:
        raise AssertionError(f"owner authentication failed: HTTP {status}: {body}")
    status, body = _request(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token",
        method="POST",
        data={"refresh_token": REFRESH_TOKEN},
        token=REFRESH_TOKEN,
    )
    if status != 200 or not body.get("access_token") or not body.get("user", {}).get("id"):
        raise AssertionError(f"refresh authentication failed: HTTP {status}: {body}")
    return body["access_token"], body["user"]["id"]


def test_fresh_session_decision_is_influenced_by_verified_learning():
    token, owner_id = authenticated_token()
    headers = {"apikey": PUBLISHABLE_KEY, "Authorization": f"Bearer {token}"}

    url = (
        f"{SUPABASE_URL}/rest/v1/learning_evidence"
        "?select=id,target_id,level,status,claim,observed_value,source_event_id,verification_method"
        "&target_id=eq.NAYA-NODE-0001&status=eq.ACTIVE"
        "&order=created_at.desc&limit=1"
    )
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        learning_rows = json.loads(response.read().decode())
    assert learning_rows, "no active verified learning found"
    learning = learning_rows[0]
    assert learning["level"] == "E5_CAN_TEACH"
    assert learning["source_event_id"] == "NAYA-NODE-0001-APPLY"
    assert learning["observed_value"]["behavioral_change"] is True
    assert learning["observed_value"]["control_verified_value"] < learning["observed_value"]["treatment_verified_value"]

    status, decision = _request(
        f"{SUPABASE_URL}/functions/v1/naya-decision-context",
        method="POST",
        data={"target_id": "NAYA-NODE-0001"},
        token=token,
    )
    assert status == 200, f"decision-context failed: HTTP {status}: {decision}"
    assert decision.get("ok") is True, decision
    d = decision["decision"]
    assert d["target_id"] == "NAYA-NODE-0001"
    assert d["influenced"] is True
    assert d["decision"] == "USE_VERIFIED_LEARNING_CONTEXT"
    assert d["context"]["evidence_id"] == learning["id"]
    assert d["context"]["source_event_id"] == "NAYA-NODE-0001-APPLY"

    workflow_context = {
        "github_sha": os.environ.get("GITHUB_SHA", ""),
        "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "github_workflow": os.environ.get("GITHUB_WORKFLOW", ""),
        "github_ref": os.environ.get("GITHUB_REF", ""),
    }
    assert all(workflow_context.values()), f"incomplete GitHub execution provenance: {workflow_context}"

    receipt = {
        "schema": "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1",
        "owner_id": owner_id,
        "target_id": "NAYA-NODE-0001",
        "learning_id": learning["id"],
        "learning_level": learning["level"],
        "source_event_id": learning["source_event_id"],
        "control_verified_value": learning["observed_value"]["control_verified_value"],
        "treatment_verified_value": learning["observed_value"]["treatment_verified_value"],
        "behavioral_change": learning["observed_value"]["behavioral_change"],
        "fresh_session_decision": d["decision"],
        "influenced": d["influenced"],
        "evidence_id_from_decision": d["context"]["evidence_id"],
        "github": workflow_context,
        "status": "PASS",
    }
    Path("learning-influence-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
