#!/usr/bin/env python3
"""PUT the welcome video MP4 into WELCOME_ASSETS KV (key naya-welcome-video)
so the v3 staging worker serves it at /naya-video.mp4. Uses the registered
custom.cloudflare connection; never touches a raw token."""
import sys, urllib.request, urllib.error, hashlib
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
KEY = "naya-welcome-video"
SRC = "/home/hatch/workspace/user/media_library/video/c8/c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c.mp4"
data = open(SRC, "rb").read()
print("video bytes", len(data), "sha256", hashlib.sha256(data).hexdigest())
assert len(data) == 7368202
assert hashlib.sha256(data).hexdigest() == "c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c"
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{KEY}"
req = urllib.request.Request(url, data=data, method="PUT", headers={"Content-Type": "video/mp4"})
add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
try:
    with urllib.request.urlopen(req, timeout=300) as resp:
        print("HTTP", resp.status, resp.read().decode()[:500])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:1000])
