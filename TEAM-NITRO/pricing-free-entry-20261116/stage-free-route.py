#!/usr/bin/env python3
"""Stage the pricing free-entry route worker (F4) — PUT only, never live.
Worker: naya-pricing-free-staging. PUTs free-staging-worker.js (built by
build-free-staging-worker.py) with the WELCOME_ASSETS KV binding, enables
the workers.dev route, then verifies by HTTP + sha:
  GET /            -> free index (sha == free-index.html)
  GET /free        -> free entry (sha == free-entry.html)
  GET /free/walk   -> walk free (sha == walk-free.html)
  GET /free/hub    -> 302 to https://nayanet.app/
  POST /api/welcome/complete (test alias) -> reveal with pages
  GET  /api/welcome/complete?alias=<test> -> the stored record
  GET  /<test-alias> -> 302 to a live nayanet.app page
The test alias is f4test<random> — never a real citizen alias. The KV
record it leaves (complete_f4test…) is a test row in the shared namespace;
named in the record. No live worker is touched.
"""
import hashlib
import json
import os
import random
import string
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
WORKER = "naya-pricing-free-staging"
HOST = f"https://{WORKER}.nayapower.workers.dev"
BASE = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts"
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused")


def api(method, path, body=None, headers=None):
    req = urllib.request.Request(BASE + path, method=method, data=body)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    add_surrogate_to_request(req, "custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=120) as resp:
        return resp.status, resp.read()


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or UA, method="GET")
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def post_json(url, obj):
    data = json.dumps(obj).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json", **UA})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    worker = open(os.path.join(HERE, "free-staging-worker.js"), "rb").read()
    meta = json.load(open(os.path.join(HERE, "worker-meta.json")))
    print(f"worker: {len(worker)} B sha256={sha(worker)}")
    assert b"nayanet_free_entry" in worker, "free flag missing from worker"
    assert b"/free/walk" in worker and b"/free/hub" in worker
    assert b"SB_KEY" in worker
    # PUT multipart (metadata + application/javascript+module), per TOOLS.md.
    bnd = "----mt" + os.urandom(8).hex()
    meta_json = json.dumps({"main_module": "worker.js",
                            "compatibility_date": "2024-01-01",
                            "bindings": meta["bindings"]})
    body = (
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
        f"Content-Type: application/json\r\n\r\n{meta_json}\r\n"
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"worker.js\"; "
        f"filename=\"worker.js\"\r\nContent-Type: application/javascript+module\r\n\r\n"
    ).encode() + worker + f"\r\n--{bnd}--\r\n".encode()
    status, resp = api("PUT", f"/{WORKER}", body=body,
                       headers={"Content-Type": f"multipart/form-data; boundary={bnd}"})
    print(f"PUT status: {status}")
    print(resp[:400].decode("utf-8", "replace"))
    assert status in (200, 201), f"PUT failed: {status}"
    # New workers ship with the workers.dev route DISABLED (404 error 1042)
    # — enable it (POST, not PATCH: PATCH is 405 on this endpoint).
    status, resp = api("POST", f"/{WORKER}/subdomain",
                       body=json.dumps({"enabled": True}).encode(),
                       headers={"Content-Type": "application/json"})
    print(f"subdomain enable: {status} {resp[:200].decode('utf-8', 'replace')}")
    # Verify the deployed script reads back identical.
    status, raw = api("GET", f"/{WORKER}")
    assert status == 200, f"GET worker: {status}"
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "dn", os.path.expanduser("~/workspace/ninaya/integration/deploy-ninaya.py"))
    _dn = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_dn)
    _, wb, _ = _dn.split_multipart(raw)
    assert wb == worker, "read-back worker differs from what was PUT — STOP"
    print(f"read-back worker sha256={sha(wb)} — MATCH")
    # Verify the served routes.
    for path, fname in [("/", "free-index.html"), ("/free", "free-entry.html"),
                        ("/free/walk", "walk-free.html")]:
        want = open(os.path.join(HERE, fname), "rb").read()
        st, _, got = get(HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got == want, f"GET {path}: served bytes != {fname} — STOP"
        print(f"GET {path}: 200, {len(got)} B sha256={sha(got)[:12]}… == {fname} MATCH")
    st, hdrs, _ = get(HOST + "/free/hub")
    assert st in (301, 302), f"GET /free/hub: {st}"
    assert hdrs.get("Location") == "https://nayanet.app/", \
        f"/free/hub Location: {hdrs.get('Location')}"
    print("GET /free/hub: 302 -> https://nayanet.app/ (the Hub) MATCH")
    alias = "f4test" + "".join(random.choices(string.ascii_lowercase, k=8))
    payload = {"alias": alias, "name": "F4 Test",
               "answers": {"about": "free-entry route test"},
               "topics": ["test"],
               "pageNames": {"personal": {"title": "F4 Test"}}}
    st, out = post_json(HOST + "/api/welcome/complete", payload)
    assert st == 200, f"POST /api/welcome/complete: {st} {out[:200]}"
    rev = json.loads(out.decode())
    assert rev.get("pages", {}).get("personal") == "/" + alias, f"reveal: {rev}"
    assert rev["pages"]["dashboard"].startswith("https://nayanet.app/dashboard")
    print(f"POST /api/welcome/complete ({alias}): 200, reveal pages OK")
    st, out = get(HOST + f"/api/welcome/complete?alias={alias}")
    assert st == 200, f"GET /api/welcome/complete: {st}"
    rec = json.loads(out.decode())
    assert rec["alias"] == alias
    print("GET /api/welcome/complete: stored record reads back MATCH")
    st, hdrs, _ = get(HOST + "/" + alias)
    assert st in (301, 302), f"GET /{alias}: {st}"
    assert hdrs.get("Location", "").startswith("https://nayanet.app/personal?"), \
        f"alias Location: {hdrs.get('Location')}"
    print(f"GET /{alias}: 302 -> live personal page MATCH")
    print(f"FREE ROUTE STAGED: {HOST}")
    print(f"  entry: {HOST}/free")
    print(f"  walk:  {HOST}/free/walk")
    print(f"  hub:   {HOST}/free/hub")
    print(f"  test alias left in KV: complete_{alias}")


if __name__ == "__main__":
    main()
