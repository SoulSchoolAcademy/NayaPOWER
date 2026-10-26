#!/usr/bin/env python3
"""Deploy naya-welcome worker + SUPABASE_SERVICE_ROLE_KEY secret + routes.
Adapted from the claim worker's deploy.py (same credential path: the
registered custom.cloudflare surrogate + sb-mgmt connector for the key).
Key values travel only in process memory — never printed, never on disk."""
import json, subprocess, sys, urllib.request, uuid
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
SCRIPT = "naya-welcome"
SB_MGMT = os.environ.get("SB_MGMT_BIN", "sb-mgmt-api")  # seat supplies Supabase mgmt tool path
PROJECT = "dahisasgpfvziswqvmvm"
CODE = os.path.join(os.path.dirname(__file__), "..", "walk", "worker.js")  # repo-relative: HUB/walk/worker.js
PATTERNS = ["nayanet.live/welcome*", "nayanet.live/api/welcome/*", "nayanet.live/world/*"]

def cf_call(method, url, data=None, ctype=None):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": ctype} if ctype else {})
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(req, timeout=60) as resp:
        return read_json_response(resp)

def main():
    # 1. upload worker code (multipart, module syntax)
    code = open(CODE, "rb").read()
    boundary = "----naya" + uuid.uuid4().hex
    meta = json.dumps({"main_module": "worker.js", "compatibility_date": "2024-11-01"})
    body = b""
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n'
    body += meta.encode() + b"\r\n"
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\nContent-Type: application/javascript+module\r\n\r\n'
    body += code + b"\r\n"
    body += ("--" + boundary + "--\r\n").encode()
    out = cf_call("PUT", f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{SCRIPT}",
                  body, "multipart/form-data; boundary=" + boundary)
    print("upload success:", out.get("success"), "script:", (out.get("result") or {}).get("id"),
          "errors:", out.get("errors"))
    assert out.get("success")

    # 2. fetch service_role key via mgmt connector (memory only)
    res = subprocess.run([SB_MGMT, "GET", f"/projects/{PROJECT}/api-keys"],
                         capture_output=True, text=True)
    svc = {k["id"]: k["api_key"] for k in json.loads(res.stdout)}["service_role"]
    assert svc and len(svc) > 20

    # 3. set worker secret
    payload = json.dumps({"name": "SUPABASE_SERVICE_ROLE_KEY", "text": svc,
                          "type": "secret_text"}).encode()
    out = cf_call("PUT", f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{SCRIPT}/secrets",
                  payload, "application/json")
    print("secret set success:", out.get("success"), "errors:", out.get("errors"))
    assert out.get("success")

    # 4. routes (idempotent: create, or update if the pattern exists)
    zones = cf_call("GET", "https://api.cloudflare.com/client/v4/zones?name=nayanet.live")
    zid = zones["result"][0]["id"]
    existing = cf_call("GET", f"https://api.cloudflare.com/client/v4/zones/{zid}/workers/routes")
    by_pattern = {r["pattern"]: r for r in (existing.get("result") or [])}
    for pat in PATTERNS:
        payload = json.dumps({"pattern": pat, "script": SCRIPT}).encode()
        if pat in by_pattern:
            rid = by_pattern[pat]["id"]
            if by_pattern[pat].get("script") == SCRIPT:
                print("route already ours:", pat)
                continue
            out = cf_call("PUT", f"https://api.cloudflare.com/client/v4/zones/{zid}/workers/routes/{rid}",
                          payload, "application/json")
            print("route updated:", pat, "success:", out.get("success"), "errors:", out.get("errors"))
        else:
            out = cf_call("POST", f"https://api.cloudflare.com/client/v4/zones/{zid}/workers/routes",
                          payload, "application/json")
            print("route created:", pat, "success:", out.get("success"), "errors:", out.get("errors"))
        assert out.get("success"), pat

    # 5. confirm routes now point at us
    after = cf_call("GET", f"https://api.cloudflare.com/client/v4/zones/{zid}/workers/routes")
    mine = [(r["pattern"], r.get("script")) for r in (after.get("result") or []) if r["pattern"] in PATTERNS]
    print("routes for welcome:", mine)

if __name__ == "__main__":
    main()
