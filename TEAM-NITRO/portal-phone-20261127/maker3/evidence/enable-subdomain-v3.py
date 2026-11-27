#!/usr/bin/env python3
"""Enable workers.dev subdomain for the R4 staging worker (new workers ship
with the route disabled -> 404 error 1042). Uses the registered
custom.cloudflare connection; never touches a raw token."""
import json, sys, urllib.request, urllib.error
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NAME = "portal-phone-v3-staging"
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{NAME}/subdomain"
data = json.dumps({"enabled": True}).encode()
req = urllib.request.Request(url, data=data, method="POST",
                             headers={"Content-Type": "application/json"})
add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        print("HTTP", resp.status, resp.read().decode()[:500])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:500])
