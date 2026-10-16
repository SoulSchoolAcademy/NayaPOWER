#!/usr/bin/env python3
"""Bridge backend SKELETON — the missing machine between Supabase and the Hub.

Stdlib-only HTTP server. No dependencies, no credentials, no production
behavior. This is a contract-implementation skeleton: every route declares
its request/response contract, runs a stubbed happy path, and fails closed.

D4 doctrine enforcement points (see BRIDGE-CONTRACT.md and bridge_sync.py):
  * /sync filters owner_scope=PRIVATE rows before any diff is computed.
  * /webhook never re-labels scope and never commits ledger content to git.
  * Tool endpoints never emit feed rows; they return receipts only.

Config (ENV ONLY, never committed):
  NAYA_BRIDGE_APP_KEY   the app key. Absent -> server starts in local-dev mode
                        where auth-gated routes fail closed with
                        state='not_verified' (no crash, no fake data).
                        The real key injection is engine-team/Shawn territory.
  NAYA_BRIDGE_PORT      port, default 8471
  NAYA_BRIDGE_LEDGER    ledger dir, default ./ledger (append-only, never git'd)
  BRIDGE_CAN_WRITE      '1' to even *consider* a sync apply; without it the
                        apply path is hard-refused. Even with it, this
                        skeleton has no credentials and performs no writes.

The key is NEVER logged, printed, or echoed back.
"""

import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from bridge_sync import sync_supabase_to_github, public_items, CONFLICT_RULE

VERSION = "0.1.0-skeleton"
CONTRACT = "bridge/v1"

# ---- error taxonomy -------------------------------------------------------
# Codes are stable strings, documented in BRIDGE-CONTRACT.md. Every error
# response is {ok:false, state:'error', error:{code, message, doc}}.


def error(code, message, http=400):
    return http, {
        "ok": False,
        "state": "error",
        "error": {"code": code, "message": message, "doc": "BRIDGE-CONTRACT.md#error-taxonomy"},
    }


def ok(data, state="ready"):
    return 200, {"ok": True, "state": state, "data": data}


# ---- fixtures used by the dry-run sketch (clearly labelled, never real) ----
FIXTURE_SUPABASE_ROWS = [
    {"id": "ib-001", "title": "Public note", "updated_at": "2026-10-16T10:00:00Z", "owner_scope": "PUBLIC"},
    {"id": "ib-002", "title": "Private note", "updated_at": "2026-10-16T11:00:00Z", "owner_scope": "PRIVATE"},
    {"id": "ib-003", "title": "Collective note", "updated_at": "2026-10-16T09:00:00Z", "owner_scope": "COLLECTIVE"},
]
FIXTURE_GITHUB_ROWS = [
    {"id": "ib-001", "title": "Public note", "updated_at": "2026-10-15T10:00:00Z"},
    {"id": "ib-003", "title": "Collective note", "updated_at": "2026-10-16T09:00:00Z"},
]


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "NayaBridge/" + VERSION

    # -- helpers -----------------------------------------------------------
    def _json(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None, True  # malformed length -> treated as invalid input
        if length <= 0 or length > 1_000_000:
            return None, True
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8")), False
        except (ValueError, UnicodeDecodeError):
            return None, True

    def _app_key(self):
        return self.server.bridge_app_key

    def _authed(self):
        # Bearer <key>. Compared in constant time. Absent key -> local-dev
        # mode: every auth-gated route fails closed, never passes open.
        configured = self._app_key()
        if not configured:
            return False
        auth = self.headers.get("Authorization") or ""
        if not auth.startswith("Bearer "):
            return False
        return hmac.compare_digest(auth[len("Bearer "):], configured)

    def _require_auth(self):
        if not self._app_key():
            return (503, {"ok": False, "state": "not_verified",
                          "message": "bridge runs in local-dev mode: no app key configured; "
                                     "auth-gated routes are closed until the engine injects NAYA_BRIDGE_APP_KEY"})
        if not self._authed():
            return error("E_UNAUTHENTICATED", "missing or invalid bearer token", 401)
        return None

    def log_message(self, fmt, *args):
        # Scrub anything that could carry a secret from the access log.
        line = fmt % args
        if "Bearer" in line:
            line = line.split("Bearer")[0] + "Bearer [redacted]"
        super().log_message("%s", line.replace(self._app_key() or "\x00", "[key-redacted]"))

    # -- routes -------------------------------------------------------------
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/health":
            mode = "live" if self._app_key() else "local-dev"
            self._json(*ok({"contract": CONTRACT, "version": VERSION, "mode": mode,
                            "lanes": ["webhook-intake", "tool-endpoints", "sync-sketch"],
                            "d4_doctrine": "owner_scope=PRIVATE rows never enter the public lane"}))
        elif path == "/tools/get_daily_report":
            fail = self._require_auth()
            if fail:
                self._json(*fail)
                return
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            date = (q.get("date") or [""])[0]
            # STUB: honest empty, never invented report content. The real
            # generator (directive #7 pipeline) feeds this route later.
            self._json(*ok({"contract": "report/v1", "period": "daily", "date": date or "today",
                            "status": "unavailable — stub: generator not wired",
                            "sections": [], "stub": True}, state="not_verified"))
        else:
            self._json(*error("E_NOT_FOUND", "unknown route", 404))

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/webhook":
            self._webhook()
        elif path == "/tools/smart_note_this":
            self._tool_smart_note_this()
        elif path == "/tools/build_page":
            self._tool_build_page()
        elif path == "/sync":
            self._sync()
        else:
            self._json(*error("E_NOT_FOUND", "unknown route", 404))

    # -- webhook intake -> append-only ledger (fail-closed) ------------------
    def _webhook(self):
        body, malformed = self._read_json()
        # Fail closed: no JSON, no ledger write, no partial handling.
        if malformed or not isinstance(body, dict):
            self._json(*error("E_INVALID_INPUT", "webhook body must be a JSON object", 400))
            return
        # HMAC signature over the canonical payload. In local-dev mode the
        # key is absent, so verification cannot pass -> closed, not open.
        sig = self.headers.get("X-Naya-Signature") or ""
        key = self._app_key()
        if not key:
            self._json(*error("E_UNVERIFIED", "no app key configured; webhook intake disabled in local-dev mode", 401))
            return
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        expect = "sha256=" + hmac.new(key.encode(), canonical, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expect):
            self._json(*error("E_BAD_SIGNATURE", "X-Naya-Signature mismatch", 401))
            return
        # Append-only ledger. scope is recorded but NEVER re-labelled here;
        # private rows entering the ledger stay private (D4).
        ledger_dir = self.server.bridge_ledger
        os.makedirs(ledger_dir, exist_ok=True)
        record = {"seq": int(time.time() * 1000), "received_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "event": body.get("event"), "owner_scope": body.get("owner_scope", "UNKNOWN"),
                  "payload_sha256": hashlib.sha256(canonical).hexdigest()}
        with open(os.path.join(ledger_dir, "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        self._json(*ok({"ledger_seq": record["seq"], "event": record["event"]}, state="received"))

    # -- tool endpoints ------------------------------------------------------
    def _tool_smart_note_this(self):
        fail = self._require_auth()
        if fail:
            self._json(*fail)
            return
        body, malformed = self._read_json()
        if malformed or not isinstance(body, dict):
            self._json(*error("E_INVALID_INPUT", "body must be a JSON object", 422))
            return
        for field in ("idempotency_key", "human_note"):
            if not body.get(field):
                # Fail closed: no idempotency key, no capture. Never guess.
                self._json(*error("E_INVALID_INPUT", "missing required field: " + field, 422))
                return
        # STUB happy path: receipt only. The live path calls the v7 RPC
        # (hop 1 of the Hub Contract) once the engine wires credentials.
        receipt = {"idempotency_key": body["idempotency_key"],
                   "note_id": "stub-" + secrets.token_hex(6),
                   "stage": "captured-stub",
                   "next": "v7_create_smart_note (stubbed — engine wires the RPC)",
                   "topics": body.get("topics", []), "stub": True}
        self._json(*ok(receipt, state="queued"))

    def _tool_build_page(self):
        fail = self._require_auth()
        if fail:
            self._json(*fail)
            return
        body, malformed = self._read_json()
        if malformed or not isinstance(body, dict):
            self._json(*error("E_INVALID_INPUT", "body must be a JSON object", 422))
            return
        page_type = body.get("page_type")
        pieces = body.get("pieces")
        if page_type not in ("landing", "feed", "report", "library"):
            self._json(*error("E_INVALID_INPUT", "page_type must be one of: landing, feed, report, library", 422))
            return
        if not isinstance(pieces, list) or not pieces:
            self._json(*error("E_INVALID_INPUT", "pieces must be a non-empty array of piece ids", 422))
            return
        # STUB happy path: receipt echoes the contract. The Composer
        # (directive #4) owns real assembly; this route hands it the job.
        self._json(*ok({"page_type": page_type, "pieces": pieces,
                        "title": body.get("title", ""),
                        "status": "accepted — stub: assembly owned by the Composer",
                        "stub": True}, state="queued"))

    # -- sync sketch ---------------------------------------------------------
    def _sync(self):
        fail = self._require_auth()
        if fail:
            self._json(*fail)
            return
        body, malformed = self._read_json()
        if malformed or not isinstance(body, dict):
            body = {}
        mode = body.get("mode", "dry-run")
        if mode not in ("dry-run", "apply"):
            self._json(*error("E_INVALID_INPUT", "mode must be 'dry-run' or 'apply'", 422))
            return
        if mode == "apply":
            # Hard gate: the skeleton has no credentials and performs no
            # writes, ever. Apply stays closed until the engine enables it.
            self._json(*error("E_NO_CREDENTIALS",
                              "sync apply is closed in the skeleton: no credentials are configured and "
                              "BRIDGE_CAN_WRITE is not the engine's enabled path", 503))
            return
        # Dry-run against labelled fixtures. public_items() is the D4 gate:
        # PRIVATE rows cannot reach the plan.
        plan = sync_supabase_to_github(FIXTURE_SUPABASE_ROWS, FIXTURE_GITHUB_ROWS, mode="dry-run")
        plan["fixture"] = True
        self._json(*ok(plan, state="dry-run"))


def build_server(port=None, ledger=None):
    port = port or int(os.environ.get("NAYA_BRIDGE_PORT", "8471"))
    server = HTTPServer(("127.0.0.1", port), BridgeHandler)
    server.bridge_app_key = os.environ.get("NAYA_BRIDGE_APP_KEY") or ""
    server.bridge_ledger = ledger or os.environ.get("NAYA_BRIDGE_LEDGER") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ledger")
    return server


if __name__ == "__main__":
    srv = build_server()
    mode = "live" if srv.bridge_app_key else "local-dev (no app key — auth routes closed)"
    print("bridge %s on 127.0.0.1:%d — %s" % (VERSION, srv.server_address[1], mode))
    print("ledger:", srv.bridge_ledger)
    srv.serve_forever()
