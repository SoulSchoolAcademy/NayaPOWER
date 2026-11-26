#!/usr/bin/env python3
"""KV PUT the fixed v25 agreement file for the R6e staging worker, then read
it back and verify bytes + sha. Uses the registered custom.cloudflare
connection exactly like cf-worker.py (add_surrogate_to_request); never
touches a raw token. Value is ~23 MB, under the 25 MB KV limit.
Usage: kv-put-r6e.py [put|get]"""
import sys, hashlib, urllib.request, urllib.error
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
KEY = "agreement-v25-r6.html"
FILE = "/home/hatch/workspace/team-nitro/portal-frontpage-fix-20261125/round-6/maker/agreement-v25-fixed-r6.html"

def authed(url, method="GET", data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    return req

def run(req):
    with urllib.request.build_opener().open(req, timeout=300) as resp:
        return resp.status, resp.read()

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "put"
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{KEY}"
    if cmd == "put":
        data = open(FILE, "rb").read()
        print(f"local {len(data)} B sha256={hashlib.sha256(data).hexdigest()}")
        try:
            status, body = run(authed(url, method="PUT", data=data,
                                       headers={"Content-Type": "text/html; charset=utf-8"}))
            print("PUT HTTP", status, body.decode()[:500])
        except urllib.error.HTTPError as e:
            print("PUT HTTP", e.code, e.read().decode()[:1000]); sys.exit(1)
    # read back + verify
    try:
        status, body = run(authed(url))
        print(f"GET HTTP {status} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}")
        local = open(FILE, "rb").read()
        print("MATCH" if body == local else "MISMATCH", "local sha256=" + hashlib.sha256(local).hexdigest())
    except urllib.error.HTTPError as e:
        print("GET HTTP", e.code, e.read().decode()[:500]); sys.exit(1)

if __name__ == "__main__":
    main()
