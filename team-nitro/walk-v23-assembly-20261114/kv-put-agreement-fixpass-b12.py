#!/usr/bin/env python3
"""Fix pass: upload the one still-unused face-library picture that has no
KV key — Naya_Profile_Black.jpg -> wbf-agmt-b12.jpg — so the staging
worker can serve /agmt-b12.jpg same-origin. New key only; never overwrites
a live key. Pattern from kv-put-agreement-v4.py. Prints status + bytes +
sha256, never the credential."""
import hashlib
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

BASE = "https://api.cloudflare.com/client/v4"
ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
PATH = "/home/hatch/workspace/user/media_library/image/Naya_Profile_Black.jpg"
KEY = "wbf-agmt-b12.jpg"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


data = open(PATH, "rb").read()
print(f"local: {len(data)} B sha256={hashlib.sha256(data).hexdigest()}")
assert hashlib.sha256(data).hexdigest().startswith("2a38bb8898f6"), "not the face-library file"
url = f"{BASE}/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{KEY}"
req = urllib.request.Request(url, data=data, method="PUT",
                             headers={"Content-Type": "image/jpeg"})
add_surrogate_to_request(req, "custom.cloudflare",
                         allowed_hosts=["api.cloudflare.com"])
try:
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=120) as r:
        print(f"{KEY}: HTTP {r.status} {r.read().decode()[:200]}")
except urllib.error.HTTPError as e:
    print(f"{KEY}: HTTP {e.code} {e.read().decode()[:300]}")
    raise SystemExit(1)
print("OK: wbf-agmt-b12.jpg in KV")
