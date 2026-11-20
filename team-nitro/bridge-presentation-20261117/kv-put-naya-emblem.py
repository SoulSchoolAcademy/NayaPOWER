#!/usr/bin/env python3
"""Upload the official emblem (NAYA_ICON.png, verbatim) to the
WELCOME_ASSETS KV namespace as wbf-naya-emblem.png, so the
naya-walk-beginning-staging worker serves it at /naya-emblem.png for
the bridge corners (bridge presentation round, 2026-11-17).

Grounded in the Cloudflare connector doc
(~/workspace/custom-connectors/custom.cloudflare/CONNECTOR.md):
api.cloudflare.com only, Bearer via the registered custom.cloudflare
connection (dynamic_credentials surrogate), redirects disabled.
Account NayaPOWER + namespace id are the project's own standing
values (WELCOME_ASSETS). The KV value PUT is the standard Cloudflare
v4 endpoint: PUT /accounts/{id}/storage/kv/namespaces/{ns}/values/{key}
with the raw bytes as the body. Prints key, bytes, sha256 — never the
credential. Verifies by GETting the value back and sha-matching it.
"""
import hashlib, sys, urllib.request
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
KEY = "wbf-naya-emblem.png"
SRC = "/home/hatch/workspace/user/media_library/image/NAYA_ICON.png"
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

data = open(SRC, "rb").read()
sha = hashlib.sha256(data).hexdigest()
print(f"source: {SRC} {len(data)} B sha256={sha}")
url = f"{BASE}/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{KEY}"
try:
    with authed(url, data, "PUT", "image/png") as r:
        print(f"PUT {KEY}: HTTP {r.status} {r.read().decode()[:200]}")
except urllib.error.HTTPError as e:
    print(f"PUT {KEY}: HTTP {e.code} {e.read().decode()[:300]}")
    raise SystemExit(1)
# read-back verify
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
print("OK: emblem in KV")
