#!/usr/bin/env python3
"""Deploy the Smart Factory to its permanent home:
   worker `smartfactory` -> smartfactory.nayapower.workers.dev
   + custom domain smartfactory.nayanet.live (never changes)."""
import json, os, sys, urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
BASE = "https://api.cloudflare.com/client/v4"
WORKER = "smartfactory"
HOSTNAME = "smartfactory.nayanet.live"
HTML_PATH = os.path.expanduser("~/workspace/team-nitro/smart-builder/factory/Smart_factory_smarttabs.html")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused")

def call(method, path, data=None, ctype="application/json"):
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", ctype)
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
            body = resp.read()
    except urllib.request.HTTPError as e:
        body = e.read()
        print(f"HTTP {e.code} on {method} {path}: {body[:300]}")
        return {"success": False, "http": e.code, "raw": body[:300]}
    try:
        return json.loads(body)
    except Exception:
        return {"raw": body[:200]}

def main():
    html = open(HTML_PATH, "rb").read()
    print("html bytes:", len(html))
    worker_js = ("const HTML = %s;\n"
                 "export default { fetch() { return new Response(HTML, "
                 "{headers: {'content-type': 'text/html;charset=utf-8', "
                 # no-cache: the factory is a living tool — Shawn must never
                 # see a stale copy and give feedback on an old version.
                 "'cache-control': 'no-store, no-cache, must-revalidate'}}); } };\n"
                 % json.dumps(html.decode("utf-8"))).encode()
    metadata = json.dumps({"main_module": "worker.js", "compatibility_date": "2024-01-01"}).encode()
    boundary = "----nayaformdata7d3f9a1c"
    b = boundary.encode()
    body = (b"--" + b + b"\r\n"
            b'Content-Disposition: form-data; name="metadata"\r\n'
            b"Content-Type: application/json\r\n\r\n" + metadata + b"\r\n"
            b"--" + b + b"\r\n"
            b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n'
            b"Content-Type: application/javascript+module\r\n\r\n" + worker_js + b"\r\n"
            b"--" + b + b"--\r\n")
    r = call("PUT", f"/accounts/{ACCT}/workers/scripts/{WORKER}", body,
             ctype=f"multipart/form-data; boundary={boundary}")
    assert r.get("success"), "worker upload failed"
    print("worker deployed")
    r = call("POST", f"/accounts/{ACCT}/workers/scripts/{WORKER}/subdomain", b'{"enabled":true}')
    print("workers.dev:", "enabled" if r.get("success") else r)
    # permanent home: smartfactory.nayanet.live
    r = call("POST", f"/accounts/{ACCT}/workers/domains",
             json.dumps({"hostname": HOSTNAME, "service": WORKER}).encode())
    if r.get("success"):
        print("custom domain LIVE:", HOSTNAME)
    else:
        print("custom domain NOT attached:", json.dumps(r)[:300])
    print("URLS:")
    print("  https://" + WORKER + ".nayapower.workers.dev/")
    print("  https://" + HOSTNAME + "/")

main()
