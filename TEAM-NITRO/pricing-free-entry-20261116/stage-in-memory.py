#!/usr/bin/env python3
"""Stage F4 (pricing v78 + free-entry route) ENTIRELY IN MEMORY — no disk
writes for the big files, because the EPERM flake is blocking all VM
filesystem writes (python/shell/node/cp, 2026-11-17 ~00:11Z onward).
  1. Build v78 bytes + free-worker bytes in memory (same code as
     build-v78.py / build-free-staging-worker.py — the builders, imported).
  2. GET the live pricing worker (API, in memory) and prove it still serves
     v77 byte-exact via the Node stdin driver (a real JS runtime check).
  3. Splice v78 into the live worker bytes (set_page_value, in memory);
     prove the spliced worker serves v78 byte-exact + markers via Node.
  4. PUT the free worker to naya-pricing-free-staging (KV binding), enable
     its workers.dev route, GET read-back (must equal PUT bytes), prove its
     static routes via Node, then verify live over HTTP (/, /free,
     /free/walk byte-match; /free/hub 302 to the Hub; /api/welcome/complete
     POST returns a reveal with pages).
  5. PUT the spliced pricing worker to naya-pricing-f4-staging (bindings:
     []), enable its workers.dev route, GET read-back (must equal PUT
     bytes), prove via Node, then curl the staged URL (browser UA — urllib's
     default UA 403s on workers.dev) and follow the free button's href.
  6. Best-effort: try to write the big files to disk at the end (the
     retrying writer); if the flake is still up, report the files as
     not-on-disk and note they are recoverable byte-exact from the staged
     workers' served bytes.
No PUT to any live worker anywhere in this script.
"""
import hashlib
import importlib.util
import json
import os
import random
import string
import subprocess
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))
from dynamic_credentials import add_surrogate_to_request

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bv = load("bv78", os.path.join(HERE, "build-v78.py"))
_bf = load("bfree", os.path.join(HERE, "build-free-staging-worker.py"))
_dn = load("dn", os.path.expanduser("~/workspace/ninaya/integration/deploy-ninaya.py"))
split_multipart, set_page_value = _dn.split_multipart, _dn.set_page_value

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
LIVE_WORKER = "naya-model-pricing"
STAGE_PRICING = "naya-pricing-f4-staging"
FREE_WORKER = "naya-pricing-free-staging"
FREE_HOST = f"https://{FREE_WORKER}.nayapower.workers.dev"
STAGE_HOST = f"https://{STAGE_PRICING}.nayapower.workers.dev"
BASE = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts"
V77 = os.path.expanduser("~/workspace/team-nitro/pricing/v77/pricing-v77.html")
V77_SHA = "b043167b2fa9a863a18216cdd2d282a20dcf5ff4159ac93e0da28ddea1635577"
FREE_URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

NODE_DRIVER = r"""
const fs = require('fs');
const crypto = require('crypto');
const src = fs.readFileSync(0, 'utf-8');
const body = src.replace(/export default(?![\s\S]*export default)/, 'module.exports =');
const module = { exports: {} };
new Function('module', 'exports', body)(module, module.exports);
const w = module.exports;
const url = process.argv[1];
const expectSha = process.argv[2];
const markers = JSON.parse(process.argv[3] || '[]');
const mustNot = JSON.parse(process.argv[4] || '[]');
(async () => {
  const r = await w.fetch(new Request(url));
  const t = await r.text();
  const sha = crypto.createHash('sha256').update(t).digest('hex');
  console.log('status', r.status, 'bytes', Buffer.byteLength(t, 'utf-8'), 'sha256', sha);
  console.log('SHA_MATCH:', expectSha === '__REDIRECT__' ? '(redirect — sha not compared)' : (sha === expectSha));
  let ok = expectSha === '__REDIRECT__' ? true : (sha === expectSha);
  for (const m of markers) { const f = t.includes(m); console.log('HAVE', JSON.stringify(m.slice(0, 60)), f); if (!f) ok = false; }
  for (const m of mustNot) { const f = t.includes(m); console.log('NOT', JSON.stringify(m), !f); if (f) ok = false; }
  if (r.status >= 300 && r.status < 400) console.log('LOCATION:', r.headers.get('location'));
  console.log('DRIVER:', ok ? 'PASS' : 'FAIL');
  if (!ok) process.exit(1);
})();
"""


def node_check(worker_src, url, expect_sha, markers=None, must_not=None):
    """Run the worker's real fetch handler in Node; worker source via stdin
    (no disk). expect_sha is the sha of the exact bytes the route must serve."""
    r = subprocess.run(
        ["node", "-e", NODE_DRIVER, url, expect_sha,
         json.dumps(markers or []), json.dumps(must_not or [])],
        input=worker_src, capture_output=True, text=True,
        timeout=180)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"node driver failed for {url}")


def node_redirect_check(worker_src, url, expect_location):
    """Driver variant: expect a redirect; checks status + Location only."""
    r = subprocess.run(
        ["node", "-e", NODE_DRIVER, url, "__REDIRECT__", "[]", "[]"],
        input=worker_src, capture_output=True, text=True,
        timeout=180)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"node redirect driver failed for {url}")
    assert f"LOCATION: {expect_location}" in r.stdout, \
        f"redirect Location mismatch for {url}"


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


def put_worker(name, worker_bytes, bindings):
    bnd = "----mt" + os.urandom(8).hex()
    meta = json.dumps({"main_module": "worker.js",
                       "compatibility_date": "2024-01-01",
                       "bindings": bindings})
    body = (
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
        f"Content-Type: application/json\r\n\r\n{meta}\r\n"
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"worker.js\"; "
        f"filename=\"worker.js\"\r\nContent-Type: application/javascript+module\r\n\r\n"
    ).encode() + worker_bytes + f"\r\n--{bnd}--\r\n".encode()
    status, resp = api("PUT", f"/{name}", body=body,
                       headers={"Content-Type": f"multipart/form-data; boundary={bnd}"})
    print(f"PUT {name}: {status} {resp[:200].decode('utf-8', 'replace')}")
    assert status in (200, 201), f"PUT {name} failed: {status}"
    status, resp = api("POST", f"/{name}/subdomain",
                       body=json.dumps({"enabled": True}).encode(),
                       headers={"Content-Type": "application/json"})
    print(f"subdomain {name}: {status} {resp[:160].decode('utf-8', 'replace')}")


def http_get(url):
    """GET with retries: urllib first (up to 3 tries — workers.dev sometimes
    drops a chunked transfer mid-body), then curl to stdout (no disk)."""
    last = None
    for _ in range(3):
        req = urllib.request.Request(url, headers=UA, method="GET")
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), e.read()
        except Exception as e:
            last = e
    # Fallback: curl with headers on stderr, body on stdout (no disk).
    r = subprocess.run(["curl", "-sS", "-A", UA["User-Agent"], "-D", "/dev/stderr",
                        url],
                       capture_output=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit(f"GET {url} failed (urllib: {last}; curl rc={r.returncode})")
    status = 200
    loc = None
    for line in r.stderr.decode("utf-8", "replace").splitlines():
        if line.startswith("HTTP/"):
            status = int(line.split()[1])
        if line.lower().startswith("location:"):
            loc = line.split(":", 1)[1].strip()
    return status, ({"Location": loc} if loc else {}), r.stdout


def http_post_json(url, obj):
    data = json.dumps(obj).encode()
    last = None
    for _ in range(3):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers={"Content-Type": "application/json", **UA})
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except Exception as e:
            last = e
    raise SystemExit(f"POST {url} failed after retries: {last}")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build_v78():
    src = open(V77, encoding="utf-8").read()
    assert sha(src.encode()) == V77_SHA, "v77 sha mismatch — STOP"
    page = src
    page = _bv.replace_once(page, _bv.CSS_ANCHOR, _bv.CSS_ANCHOR + _bv.CSS_ADD, "G1")
    page = _bv.replace_once(page, _bv.HTML_ANCHOR,
                            _bv.HTML_ADD + "      " + _bv.HTML_ANCHOR, "G2")
    page = _bv.replace_once(page, _bv.JS_ANCHOR, _bv.JS_ANCHOR + _bv.JS_ADD, "G3a")
    page = _bv.replace_once(page, _bv.FINALE_OLD, _bv.FINALE_NEW, "G3b")
    page = _bv.replace_once(page, _bv.CHOOSER_OLD, _bv.CHOOSER_NEW, "G3c")
    return page


def main():
    # 0. Build everything in memory.
    v78 = build_v78()
    v78_sha = sha(v78.encode())
    print(f"v78 built in memory: {len(v78.encode())} B sha256={v78_sha}")
    r = subprocess.run(["diff", V77, "/dev/stdin"], input=v78.encode(),
                       capture_output=True)
    diff_text = r.stdout.decode("utf-8")
    print(f"diff v77->v78: {len(diff_text.splitlines())} lines, "
          f"{len(diff_text.encode())} B")
    walk_free = _bf.build_walk_free()
    free_entry = _bf.build_free_entry()
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", STAGE_HOST + "/")
    free_worker = _bf.build_worker(walk_free, free_entry)
    print(f"free worker built in memory: {len(free_worker.encode())} B "
          f"sha256={sha(free_worker.encode())}")

    # 1. Live worker must still serve v77 byte-exact.
    status, raw = api("GET", f"/{LIVE_WORKER}")
    assert status == 200, f"GET live worker: {status}"
    _, worker_bytes, _ = split_multipart(raw)
    live_src = worker_bytes.decode("utf-8")
    print("live worker serves (expect v77):")
    node_check(live_src, "https://nayanet.app/pricing", V77_SHA,
               ["Plug in your AI", "The first thousand founders get half price",
                "trial-banner", '<span class="plan-free">Nine days free</span>'],
               ["freeEntry", "free-entry-btn", "FREE_ENTRY_URL"])

    # 2. Splice v78; prove the spliced worker serves v78 via Node.
    new_worker = set_page_value(live_src, v78)
    print(f"spliced worker: {len(new_worker)} B sha256={sha(new_worker.encode())}")
    # The driver parses the module (a syntax error fails the import) — it IS
    # the syntax check here (node --check needs a real file, which the flake
    # will not let us write; the staged read-back + served-bytes checks below
    # are the proof instead).
    print("spliced worker serves (expect v78):")
    node_check(new_worker, "https://nayanet.app/pricing", v78_sha,
               ['id="freeEntry"', FREE_URL, "Enter free", "Zero cost, zero risk",
                "Nine days free on every plan — nothing is charged for 9 days. Day 10, you&rsquo;re charged for the level you&rsquo;re on.",
                '<span class="plan-free">Nine days free</span>',
                "or continue with Naya Free",
                "The first thousand founders get half price",
                "Plug in your AI", "WANT THE FULL PICTURE",
                "If PayPal holds a payment",
                "nayanet.app/power-monthly", "nayanet.app/max-yearly",
                "openChooser"],
               ["bonus", "bottomStart", "blockchain", "Welcome in — you"])

    # 3. Stage the FREE worker first (the pricing button points at it).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    put_worker(FREE_WORKER, free_worker.encode(), kv)
    status, raw = api("GET", f"/{FREE_WORKER}")
    assert status == 200
    _, wb, _ = split_multipart(raw)
    assert wb == free_worker.encode(), "free read-back differs from PUT — STOP"
    print(f"free read-back sha256={sha(wb)} — MATCH")
    print("free worker serves /free (expect free-entry.html):")
    node_check(free_worker, FREE_HOST + "/free", sha(free_entry.encode()),
               ["Enter free &mdash; no payment, no card.", 'id="freeEye"',
                "WALKTHROUGH_URL = '/free/walk'"], [])
    print("free worker serves /free/walk (expect walk-free.html):")
    node_check(free_worker, FREE_HOST + "/free/walk", sha(walk_free.encode()),
               ["nayanet_free_entry", "data-door=\"Hub\"",
                "You&rsquo;re in on Naya Free"], [])
    print("free worker serves / (expect free-index.html):")
    node_check(free_worker, FREE_HOST + "/", sha(free_index.encode()),
               ["Enter free — the route, staged"], [])
    print("free worker /free/hub (expect 302 to the Hub):")
    node_redirect_check(free_worker, FREE_HOST + "/free/hub",
                        "https://nayanet.app/")

    # 4. Verify the staged free worker over real HTTP.
    for path, want in [("/", free_index), ("/free", free_entry),
                       ("/free/walk", walk_free)]:
        st, _, got = http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    st, hdrs, _ = http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ (the Hub) MATCH")
    alias = "f4test" + "".join(random.choices(string.ascii_lowercase, k=8))
    st, out = http_post_json(
        FREE_HOST + "/api/welcome/complete",
        {"alias": alias, "name": "F4 Test",
         "answers": {"about": "free-entry route test"}, "topics": ["test"],
         "pageNames": {"personal": {"title": "F4 Test"}}})
    assert st == 200, f"POST /api/welcome/complete: {st} {out[:200]}"
    rev = json.loads(out.decode())
    assert rev.get("pages", {}).get("personal") == "/" + alias
    assert rev["pages"]["dashboard"].startswith("https://nayanet.app/dashboard")
    print(f"POST /api/welcome/complete ({alias}): 200, reveal pages OK")
    st, _, out = http_get(FREE_HOST + f"/api/welcome/complete?alias={alias}")
    assert st == 200 and json.loads(out.decode())["alias"] == alias
    print("GET /api/welcome/complete: stored record reads back MATCH")
    st, hdrs, _ = http_get(FREE_HOST + "/" + alias)
    assert st in (301, 302) and hdrs.get("Location", "").startswith(
        "https://nayanet.app/personal?")
    print(f"GET /{alias}: 302 -> live personal page MATCH")

    # 5. Stage the pricing worker (v78), then verify over HTTP.
    put_worker(STAGE_PRICING, new_worker.encode(), [])
    status, raw = api("GET", f"/{STAGE_PRICING}")
    assert status == 200
    _, wb, _ = split_multipart(raw)
    assert wb.decode("utf-8") == new_worker, "pricing read-back differs — STOP"
    print(f"pricing read-back sha256={sha(wb)} — MATCH")
    print("read-back staging worker serves (expect v78):")
    node_check(new_worker, "https://nayanet.app/pricing", v78_sha,
               ['id="freeEntry"', FREE_URL], [])
    st, _, got = http_get(STAGE_HOST + "/")
    assert st == 200 and got.decode("utf-8") == v78, "staged URL bytes != v78 — STOP"
    print(f"GET {STAGE_HOST}/ : 200, {len(got)} B == v78 MATCH")
    st, _, free = http_get(FREE_URL)
    assert st == 200 and b"Enter free" in free and b"freeEye" in free
    print(f"GET {FREE_URL} (the free button's href): 200, {len(free)} B — the route answers")
    print("STAGED:")
    print(f"  pricing v78: {STAGE_HOST}/  sha256={v78_sha}")
    print(f"  free route:  {FREE_HOST}/free  worker sha256={sha(free_worker.encode())}")
    print(f"  test alias left in KV: complete_{alias}")

    # 6. Best-effort: try ONCE per file to write the big files to disk for
    # the checker (no 10-minute retry here — the builders' retrying writer
    # runs separately in the background; if the flake is still up, the files
    # are recoverable byte-exact from the staged workers' served bytes).
    print("attempting one-shot disk writes for the checker (best-effort)…")
    import shlex as _sh
    node_js = ("require('fs').writeFileSync(process.argv[1], "
               "require('fs').readFileSync(0));")

    def try_once(path, data):
        raw = data.encode("utf-8")
        for mode in ("node", "py"):
            try:
                if mode == "node":
                    r = subprocess.run(["node", "-e", node_js, path],
                                       input=raw, capture_output=True, timeout=60)
                    if r.returncode != 0:
                        continue
                else:
                    with open(path, "wb") as f:
                        f.write(raw)
                if os.path.getsize(path) == len(raw):
                    print(f"  on disk ({mode}): {path}")
                    return True
            except Exception as e:
                print(f"  {mode} failed for {os.path.basename(path)}: {e}")
        print(f"  NOT on disk (flake still up): {path}")
        return False

    for path, data in [
            (os.path.expanduser("~/workspace/team-nitro/pricing/v78/pricing-v78.html"), v78),
            (os.path.expanduser("~/workspace/team-nitro/pricing/v78/diff-v78.txt"), diff_text),
            (os.path.join(HERE, "walk-free.html"), walk_free),
            (os.path.join(HERE, "free-entry.html"), free_entry),
            (os.path.join(HERE, "free-index.html"), free_index),
            (os.path.join(HERE, "free-staging-worker.js"), free_worker)]:
        try_once(path, data)


if __name__ == "__main__":
    main()
