#!/usr/bin/env python3
"""Upload the die-cut emblem PNG (from stdin) to WELCOME_ASSETS KV as
wbf-naya-emblem-cut.png, so the staging worker serves it at
/naya-emblem-cut.png for the bridge corners.

Grounded in the Cloudflare connector doc
(~/workspace/custom-connectors/custom.cloudflare/CONNECTOR.md):
api.cloudflare.com only, Bearer via the registered custom.cloudflare
connection (dynamic_credentials surrogate), redirects disabled.
Account NayaPOWER + namespace id are the project's standing values.
KV value PUT: PUT /accounts/{id}/storage/kv/namespaces/{ns}/values/{key}
with the raw bytes as the body. Prints key, bytes, sha256 — never the
credential. Verifies by GETting the value back and sha-matching it.

Usage: python3 die-cut-emblem.py | python3 kv-put-emblem-cut.py
"""
import hashlib, sys, urllib.request
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
KEY = "wbf-naya-emblem-cut.png"
BASE = "https://api.cloudflare.com/client/v4"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")

def authed(url, data, method, ctype):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": ctype})
    add_surrogate_to_request(req, "custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    return urllib.request.build_opener(NoRedirect()).open(req, timeout=180)

data = sys.stdin.buffer.read()
sha = hashlib.sha256(data).hexdigest()
print(f"stdin: {len(data)} B sha256={sha}", file=sys.stderr)
url = f"{BASE}/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{KEY}"
try:
    with authed(url, data, "PUT", "image/png") as r:
        print(f"PUT {KEY}: HTTP {r.status} {r.read().decode()[:200]}")
except urllib.error.HTTPError as e:
    print(f"PUT {KEY}: HTTP {e.code} {e.read().decode()[:300]}")
    raise SystemExit(1)
try:
    with authed(url, None, "GET", "application/octet-stream") as r:
        back = r.read()
    bsha = hashlib.sha256(back).hexdigest()
    print(f"GET {KEY}: {len(back)} B sha256={bsha} match={bsha == sha}")
    if bsha != sha:
        raise SystemExit(1)
except urllib.error.HTTPError as e:
    print(f"GET {KEY}: HTTP {e.code} {e.read().decode()[:300]}")
    raise SystemExit(1)
print("OK: die-cut emblem in KV")
