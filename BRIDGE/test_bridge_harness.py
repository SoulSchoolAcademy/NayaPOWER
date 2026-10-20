#!/usr/bin/env python3
"""Self-verification harness for the bridge backend skeleton.

Tests the ACTUAL seams that changed (server + sync), not a mock of them:
  1. webhook intake fail-closes on a bad HMAC — and stages NOTHING
     (no ledger dir, no partial record) on the bad-signature path
  2. a good HMAC is accepted; replays are idempotent (no duplicate lines)
  3. unknown tools are rejected with E_UNKNOWN_TOOL; known tools dispatch
     from the registry with their explicit contracts
  4. the ledger sync computes a D4-safe plan over REAL ledger data:
     private events are excluded from the public-lane plan
  5. sync apply stays closed without BRIDGE_CAN_WRITE, and — when the switch
     is on — writes only the local feed-state file
  6. the fixture sync's conflict rule: ties flag 'diverged', private filtered

The test key is generated at runtime and never printed, logged, or committed.
Run from this directory:  python3 test_bridge_harness.py
Exit 0 = all green; nonzero = failures printed.
"""

import hashlib
import hmac
import json
import os
import secrets
import sys
import tempfile
import threading
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bridge_server
from bridge_server import build_server, TOOL_REGISTRY
import bridge_sync

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(("PASS" if cond else "FAIL"), "-", name, (":: " + detail if detail and not cond else ""))


def req(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method,
                               headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def sign(key, body):
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return "sha256=" + hmac.new(key.encode(), canonical, hashlib.sha256).hexdigest()


def main():
    # Throwaway key: generated fresh, lives only in this process, never shown.
    test_key = secrets.token_hex(16)
    os.environ["NAYA_BRIDGE_APP_KEY"] = test_key
    ledger = tempfile.mkdtemp(prefix="bridge-ledger-test-")
    events_path = os.path.join(ledger, "events.jsonl")

    bridge_server.BridgeHandler.log_message = lambda self, *a: None  # quiet
    srv = build_server(port=0, ledger=ledger)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = "http://127.0.0.1:%d" % port
    auth = {"Authorization": "Bearer " + test_key}

    try:
        pub = {"event": "note.captured", "owner_scope": "PUBLIC", "note": "hello"}
        sig = sign(test_key, pub)

        # 1. bad HMAC -> 401 E_BAD_SIGNATURE, and NOTHING is staged
        s, b = req("POST", base + "/webhook", pub,
                   {"X-Naya-Signature": "sha256=" + "0" * 64})
        check("bad-hmac-401", s == 401 and b["error"]["code"] == "E_BAD_SIGNATURE", "got %s" % s)
        check("bad-hmac-nothing-staged", not os.path.exists(events_path),
              "ledger file must not exist on the bad-signature path")

        # 2. missing signature -> 401 as well
        s, b = req("POST", base + "/webhook", pub)
        check("missing-sig-401", s == 401 and b["error"]["code"] == "E_BAD_SIGNATURE", "got %s" % s)

        # 3. good HMAC -> received; ledger holds exactly one versioned record
        s, b = req("POST", base + "/webhook", pub, {"X-Naya-Signature": sig})
        check("good-hmac-200", s == 200 and b["state"] == "received", "got %s %s" % (s, b.get("state")))
        seq1 = b["data"]["ledger_seq"]
        with open(events_path, encoding="utf-8") as f:
            lines = f.readlines()
        rec = json.loads(lines[0])
        check("ledger-one-line", len(lines) == 1, "lines=%d" % len(lines))
        check("ledger-record-shape",
              rec.get("contract") == "webhook-ledger/v1" and rec.get("ledger_version") == 1
              and rec.get("owner_scope") == "PUBLIC" and "payload_sha256" in rec)

        # 4. replay -> duplicate, same seq, still one line
        s, b = req("POST", base + "/webhook", pub, {"X-Naya-Signature": sig})
        check("replay-idempotent", s == 200 and b["state"] == "received-duplicate"
              and b["data"]["ledger_seq"] == seq1, "got %s %s" % (s, b.get("state")))
        with open(events_path, encoding="utf-8") as f:
            check("replay-no-duplicate-line", len(f.readlines()) == 1)

        # 5. unknown tool -> 404 E_UNKNOWN_TOOL (fail-closed)
        s, b = req("POST", base + "/tools/launch_missiles", {"x": 1}, auth)
        check("unknown-tool-404", s == 404 and b["error"]["code"] == "E_UNKNOWN_TOOL", "got %s" % s)

        # 6. known tool without auth -> 401; with auth -> registry-contract receipt
        s, b = req("POST", base + "/tools/smart_note_this",
                   {"idempotency_key": "k1", "human_note": "test"})
        check("tool-no-auth-401", s in (401, 503), "got %s" % s)
        s, b = req("POST", base + "/tools/smart_note_this",
                   {"idempotency_key": "k1", "human_note": "test"}, auth)
        check("tool-known-200", s == 200 and b["state"] == "queued"
              and b["data"]["contract"] == TOOL_REGISTRY["smart_note_this"]["contract"],
              "got %s" % s)
        # missing required field -> fail closed, no capture
        s, b = req("POST", base + "/tools/smart_note_this", {"idempotency_key": "k1"}, auth)
        check("tool-missing-field-422", s == 422 and b["error"]["code"] == "E_INVALID_INPUT", "got %s" % s)

        # 7. post a PRIVATE event (accepted into the ledger; D4 says it must
        #    stay private, never re-labelled, and never enter the public lane)
        priv = {"event": "note.captured", "owner_scope": "PRIVATE", "note": "secret"}
        s, b = req("POST", base + "/webhook", priv, {"X-Naya-Signature": sign(test_key, priv)})
        check("private-event-accepted", s == 200 and b["state"] == "received", "got %s" % s)

        # 8. ledger sync dry-run over REAL ledger data: private excluded
        s, b = req("POST", base + "/sync/ledger", {"mode": "dry-run"}, auth)
        plan = b.get("data", {})
        check("ledger-sync-dryrun", s == 200 and b["state"] == "dry-run", "got %s" % s)
        check("ledger-sync-d4", plan.get("events_seen") == 2
              and plan.get("private_excluded_d4") == 1
              and plan.get("publishable") == 1, str({k: plan.get(k) for k in
                                                    ("events_seen", "private_excluded_d4", "publishable")}))
        check("ledger-sync-public-only",
              all(a["id"].startswith("ev-") for a in plan.get("actions", []))
              and len(plan.get("actions", [])) == 1 and plan["actions"][0]["op"] == "create")

        # 9. apply without the switch -> closed
        s, b = req("POST", base + "/sync/ledger", {"mode": "apply"}, auth)
        check("ledger-apply-closed", s == 503 and b["error"]["code"] == "E_NO_CREDENTIALS", "got %s" % s)

        # 10. apply with the switch -> local feed-state write, public items only
        os.environ["BRIDGE_CAN_WRITE"] = "1"
        s, b = req("POST", base + "/sync/ledger", {"mode": "apply"}, auth)
        del os.environ["BRIDGE_CAN_WRITE"]
        plan = b.get("data", {})
        check("ledger-apply-open", s == 200 and b["state"] == "applied"
              and plan.get("writes_performed") == 1, "got %s" % s)
        with open(os.path.join(ledger, "feed-state.json"), encoding="utf-8") as f:
            feed = json.load(f)
        check("feed-state-public-only", len(feed) == 1 and feed[0]["owner_scope"] == "PUBLIC",
              "feed=%s" % feed)

        # 11. fixture sync conflict rule: ties flag diverged, private filtered
        sb = [{"id": "a", "title": "t", "updated_at": "2026-10-16T10:00:00Z", "owner_scope": "PUBLIC"},
              {"id": "p", "title": "x", "updated_at": "2026-10-16T10:00:00Z", "owner_scope": "PRIVATE"}]
        gh = [{"id": "a", "title": "t", "updated_at": "2026-10-16T10:00:00Z"}]
        plan = bridge_sync.sync_supabase_to_github(sb, gh, mode="dry-run")
        ops = {a["id"]: a["op"] for a in plan["actions"]}
        check("conflict-tie-diverged", ops.get("a") == "flag_diverged"
              and plan["private_excluded_d4"] == 1 and "p" not in ops, str(ops))
    finally:
        srv.shutdown()
        os.environ.pop("NAYA_BRIDGE_APP_KEY", None)

    failed = [n for n, ok_, _ in RESULTS if not ok_]
    print("\n%d/%d passed" % (len(RESULTS) - len(failed), len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
