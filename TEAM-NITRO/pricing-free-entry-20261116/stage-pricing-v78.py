#!/usr/bin/env python3
"""Stage pricing v78 (F4) — PUT only to the STAGING worker, never live.
Mirrors pricing/v77/stage-verify-v77.py, then PUTs the spliced worker to
naya-pricing-f4-staging and verifies the staged URL by HTTP + Node.
  1. GET live naya-model-pricing — it must still serve v77 byte-exact
     (the live base is untouched; this round stages, never goes live).
  2. Splice the v78 PAGE in with set_page_value; Node fetch-handler check
     vs the v78 file (byte-exact) + markers.
  3. PUT to naya-pricing-f4-staging (bindings: [] — live has none),
     enable the workers.dev route, GET read-back, Node check vs v78.
  4. curl the staged URL (browser UA — urllib's default UA 403s on
     workers.dev with error 1010) and follow the free button's href.
No PUT to the live worker anywhere in this script.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))
from dynamic_credentials import add_surrogate_to_request
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "deploy_ninaya", os.path.expanduser("~/workspace/ninaya/integration/deploy-ninaya.py"))
_dn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_dn)
split_multipart, set_page_value = _dn.split_multipart, _dn.set_page_value
_bv = importlib.util.spec_from_file_location(
    "bv78", os.path.expanduser("~/workspace/team-nitro/pricing-free-entry-20261116/build-v78.py"))
_bvm = importlib.util.module_from_spec(_bv)
_bv.loader.exec_module(_bvm)
shell_write = _bvm.shell_write

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
LIVE_WORKER = "naya-model-pricing"
STAGE_WORKER = "naya-pricing-f4-staging"
STAGE_HOST = f"https://{STAGE_WORKER}.nayapower.workers.dev"
BASE = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts"
V77 = os.path.expanduser("~/workspace/team-nitro/pricing/v77/pricing-v77.html")
V77_SHA = "b043167b2fa9a863a18216cdd2d282a20dcf5ff4159ac93e0da28ddea1635577"
V78 = os.path.expanduser("~/workspace/team-nitro/pricing/v78/pricing-v78.html")
CHECKS_DIR = os.path.expanduser("~/workspace/team-nitro/pricing/v78")
SRC_MJS = "/tmp/pricing-worker-src.mjs"
FREE_URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
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


def run_node(args):
    r = subprocess.run(["node"] + args, capture_output=True, text=True, timeout=120)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        raise SystemExit("node step failed: " + " ".join(args))


def main():
    for name in ("check-worker.mjs", "check-worker-markers.mjs"):
        dst = os.path.join("/tmp", name)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(CHECKS_DIR, name), dst)
            print(f"restored {dst} from {CHECKS_DIR}")
    v77 = open(V77, encoding="utf-8").read()
    assert hashlib.sha256(v77.encode()).hexdigest() == V77_SHA, "v77 sha mismatch — STOP"
    v78 = open(V78, encoding="utf-8").read()
    v78_sha = hashlib.sha256(v78.encode()).hexdigest()
    print(f"v78 source: {len(v78.encode())} bytes sha256={v78_sha}")
    assert v78_sha != V77_SHA
    assert 'id="freeEntry"' in v78 and FREE_URL in v78

    # 1. Live worker must still serve v77 byte-exact.
    status, raw = api("GET", f"/{LIVE_WORKER}")
    assert status == 200, f"GET live worker: {status}"
    _, worker_bytes, _ = split_multipart(raw)
    worker_src = worker_bytes.decode("utf-8")
    print(f"live worker: {len(worker_src)} bytes "
          f"sha256={hashlib.sha256(worker_src.encode()).hexdigest()}")
    print("live worker serves (expect v77, byte-exact):")
    shell_write(SRC_MJS, worker_bytes.decode("utf-8"))
    run_node(["/tmp/check-worker.mjs", V77])

    # 2. Splice v78; the spliced worker must serve v78 byte-exact.
    new_worker = set_page_value(worker_src, v78)
    print(f"staged worker: {len(new_worker)} bytes "
          f"sha256={hashlib.sha256(new_worker.encode()).hexdigest()}")
    shell_write("/tmp/pricing-worker-v78-staged.mjs", new_worker)
    r = subprocess.run(["node", "--check", "/tmp/pricing-worker-v78-staged.mjs"],
                       capture_output=True, text=True, timeout=120)
    print("node --check staged worker rc:", r.returncode, r.stderr.strip())
    assert r.returncode == 0, "node --check FAILED — STOP"
    shell_write(SRC_MJS, new_worker)
    print("staged worker serves (expect v78):")
    run_node(["/tmp/check-worker.mjs", V78])
    run_node(["/tmp/check-worker-markers.mjs",
              json.dumps(['id="freeEntry"', FREE_URL, "Enter free",
                          "Zero cost, zero risk",
                          "Nine days free on every plan — nothing is charged for 9 days. Day 10, you&rsquo;re charged for the level you&rsquo;re on.",
                          '<span class="plan-free">Nine days free</span>',
                          "or continue with Naya Free",
                          "The first thousand founders get half price",
                          "Plug in your AI", "WANT THE FULL PICTURE",
                          "If PayPal holds a payment",
                          "nayanet.app/power-monthly", "nayanet.app/power-quarterly",
                          "nayanet.app/power-yearly", "nayanet.app/pro-monthly",
                          "nayanet.app/pro-quarterly", "nayanet.app/pro-yearly",
                          "nayanet.app/max-monthly", "nayanet.app/max-quarterly",
                          "nayanet.app/max-yearly", "openChooser"]),
              json.dumps(["bonus", "bottomStart", "blockchain",
                          "Welcome in — you"])])

    # 3. PUT to the STAGING worker (bindings: []), enable workers.dev.
    bnd = "----mt" + os.urandom(8).hex()
    meta = json.dumps({"main_module": "worker.js",
                       "compatibility_date": "2024-01-01", "bindings": []})
    body = (
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
        f"Content-Type: application/json\r\n\r\n{meta}\r\n"
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"worker.js\"; "
        f"filename=\"worker.js\"\r\nContent-Type: application/javascript+module\r\n\r\n"
    ).encode() + new_worker.encode() + f"\r\n--{bnd}--\r\n".encode()
    status, resp = api("PUT", f"/{STAGE_WORKER}", body=body,
                       headers={"Content-Type": f"multipart/form-data; boundary={bnd}"})
    print(f"PUT staging status: {status}")
    print(resp[:400].decode("utf-8", "replace"))
    assert status in (200, 201), f"PUT staging failed: {status}"
    status, resp = api("POST", f"/{STAGE_WORKER}/subdomain",
                       body=json.dumps({"enabled": True}).encode(),
                       headers={"Content-Type": "application/json"})
    print(f"subdomain enable: {status} {resp[:200].decode('utf-8', 'replace')}")
    status, raw2 = api("GET", f"/{STAGE_WORKER}")
    assert status == 200
    _, wb2, _ = split_multipart(raw2)
    assert wb2.decode("utf-8") == new_worker, "read-back differs from PUT — STOP"
    print(f"read-back staging worker sha256={hashlib.sha256(wb2).hexdigest()} — MATCH")
    shell_write(SRC_MJS, wb2.decode("utf-8"))
    print("read-back staging worker serves (expect v78):")
    run_node(["/tmp/check-worker.mjs", V78])

    # 4. curl the staged URL (browser UA) + follow the free button's href.
    req = urllib.request.Request(STAGE_HOST + "/", headers=UA, method="GET")
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
        staged = resp.read()
    assert staged.decode("utf-8") == v78, "staged URL bytes != v78 file — STOP"
    print(f"GET {STAGE_HOST}/ : 200, {len(staged)} B, sha256={hashlib.sha256(staged).hexdigest()[:12]}… == v78 MATCH")
    req = urllib.request.Request(FREE_URL, headers=UA, method="GET")
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
        free = resp.read()
    assert resp.status == 200 and b"Enter free" in free and b"freeEye" in free
    print(f"GET {FREE_URL} (the free button's href): 200, {len(free)} B — the route answers")
    print(f"PRICING v78 STAGED: {STAGE_HOST}/")
    print(f"  free button -> {FREE_URL}")


if __name__ == "__main__":
    main()
