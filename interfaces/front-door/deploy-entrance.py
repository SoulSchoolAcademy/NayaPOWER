#!/usr/bin/env python3
"""Deploy — Front Door entrance (welcome + identity) → `nayanet` worker.

Modeled on ~/workspace/factory-pipeline/deploy.py (same Cloudflare PUT
mechanics). Differences:
  - Serves TWO pages (welcome at /, identity at /identity.html) plus the
    webmanifest, both crystal icons, a real /sw.js, and a /hub redirect.
  - Also serves /enter — the NAYA GUEST GUARD v1 gate page: hub-bound
    links on OUTSIDE pages (other origins, which cannot read this
    origin's localStorage) point here; the gate checks this origin's
    stored Smart Identity and forwards members to nayanet.live and
    guests back to the welcome door (/).
  - Gates on deploy.py's css_brace_check for BOTH pages and `node --check`
    on every <script> block of both pages before building.
  - Injects the Supabase anon key into identity.html at build time: the
    JWT is extracted from a durable in-repo source (the factory flagship
    templates ship this same public client key; the browser snapshot
    manifest remains as a fallback), its payload is verified
    (role="anon", ref="dahisasgpfvziswqvmvm"), and the
    '__SB_ANON_KEY__' placeholder is replaced. The key value is NEVER
    printed or logged.
"""

import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
from deploy import css_brace_check  # noqa: E402 — same gate as the factory lane

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
BASE = "https://api.cloudflare.com/client/v4"
WORKER_NAME = "nayanet"

HERE = os.path.dirname(os.path.abspath(__file__))
WELCOME_PATH = os.path.join(HERE, "welcome.html")
IDENTITY_PATH = os.path.join(HERE, "identity.html")
MANIFEST_PATH = "/home/hatch/workspace/user/files/manifest-2.webmanifest"
ICON_192_PATH = "/home/hatch/workspace/user/media_library/image/2b/2b033fc494fcaf14c9a42cc4a700ab5233ed7612eaf9e06e8a754ca1347c5c96.png"
ICON_512_PATH = "/home/hatch/workspace/user/media_library/image/e6/e66b77e03c7995b254db34002ca138471c7c238932a847b9a167508b759401ac.png"
SNAPSHOT_MANIFEST = "/home/hatch/workspace/.hatch-browser/snapshots/browser-task:c22970e5-2e04-59ad-9cb4-b5c838d42c65/20261019T054640.955785596Z/manifest.json"
# Durable anon-key source: the factory flagship templates ship the public
# Supabase anon key in their own bytes (verified identical across all 12
# templates). Snapshots rot; the templates are the living source.
ANON_KEY_SOURCE = "/home/hatch/workspace/factory-pipeline/templates/personal.html"
SB_REF = "dahisasgpfvziswqvmvm"


def node_check_scripts(html_text, path):
    """Syntax-check every <script> block with node --check. Blocks without
    a src attribute only. Returns True when all blocks parse."""
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>",
                          html_text, re.DOTALL | re.IGNORECASE)
    checked = 0
    for i, block in enumerate(blocks):
        if not block.strip():
            continue
        with tempfile.NamedTemporaryFile(
                "w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(block)
            tmp = f.name
        try:
            r = subprocess.run(["node", "--check", tmp],
                               capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                print(f"✗ JS CHECK FAIL {path} script block {i}: "
                      f"{r.stderr.strip()[:400]}")
                return False
            checked += 1
        finally:
            os.unlink(tmp)
    print(f"✓ JS check: {checked} script blocks parse ({path})")
    return True


def extract_anon_key():
    """Find the Supabase anon JWT in a durable source, verify its payload
    claims (role=anon, ref=<project>) and return it. Primary source: the
    factory flagship template (ANON_KEY_SOURCE) — the public client key
    ships in the templates' own bytes. Fallback: the browser snapshot
    manifest, if it still exists. Never prints the key."""
    sources = [(ANON_KEY_SOURCE, "factory flagship template"),
               (SNAPSHOT_MANIFEST, "snapshot manifest")]
    for path, label in sources:
        if not os.path.exists(path):
            continue
        raw = open(path, "rb").read().decode("utf-8", "replace")
        candidates = re.findall(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+", raw)
        for tok in candidates:
            try:
                payload = tok.split(".")[1]
                payload += "=" * (-len(payload) % 4)
                claims = json.loads(base64.urlsafe_b64decode(payload))
            except Exception:
                continue
            if claims.get("role") == "anon" and claims.get("ref") == SB_REF:
                print(f"✓ Anon key extracted from {label} "
                      "(payload verified: role=anon, ref matches)")
                return tok
    print("✗ Anon key NOT found / claims mismatched in any source — aborting")
    return None


GATE_HTML = """\
<!doctype html>
<!-- NAYA GUEST GUARD v1 -->
<html lang="en" data-guard="NAYA GUEST GUARD v1">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>NayaNET — Checking your Smart Identity…</title>
<style>
  html,body{height:100%;margin:0;background:#010103;color:#fff;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    -webkit-font-smoothing:antialiased}
  body{display:flex;flex-direction:column;align-items:center;justify-content:center;
    gap:16px;text-align:center;padding:24px}
  .mark{font-size:44px;line-height:1;color:#c084fc;
    text-shadow:0 0 18px rgba(168,85,247,.85),0 0 46px rgba(168,85,247,.45)}
  p{margin:0;font-size:.95rem;font-weight:700;letter-spacing:.06em;color:#e2e8f0}
  a{color:#c084fc}
</style>
</head>
<body>
<div class="mark" aria-hidden="true">◆</div>
<p>One moment — checking your Smart Identity…</p>
<noscript><p>JavaScript is needed to check your Smart Identity.
Please <a href="/">go to the welcome page</a> to sign in.</p></noscript>
<script>
function __guardDecision() {
  try {
    var name = localStorage.getItem('nayanet_smart_name');
    var alias = localStorage.getItem('nayanet_smart_alias');
    return (name || alias) ? 'hub' : 'welcome';
  } catch (e) {
    return 'welcome';
  }
}
window.__guardDecision = __guardDecision;
function __guardTarget() {
  if (__guardDecision() !== 'hub') { return '/'; }
  var to = null;
  try { to = new URLSearchParams(location.search).get('to'); } catch (e) {}
  if (to && to.charAt(0) === '/' && to.charAt(1) !== '/') {
    return 'https://nayanet.live' + to;
  }
  return 'https://nayanet.live/';
}
location.replace(__guardTarget());
</script>
</body>
</html>
"""


SW_JS = """\
const CACHE = 'nayanet-entrance-v2';
const PRECACHE = ['/', '/identity.html', '/icon-192.png', '/icon-512.png'];
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(PRECACHE); })
      .then(function () { return self.skipWaiting(); })
  );
});
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        return k === CACHE ? null : caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});
self.addEventListener('fetch', function (e) {
  var url = new URL(e.request.url);
  var isDoc = e.request.mode === 'navigate' ||
    url.pathname === '/' || url.pathname.endsWith('.html');
  if (isDoc) {
    /* Network-first for documents. */
    e.respondWith(
      fetch(e.request).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        return res;
      }).catch(function () { return caches.match(e.request); })
    );
    return;
  }
  /* Cache-first for icons and everything else. */
  e.respondWith(
    caches.match(e.request).then(function (hit) {
      return hit || fetch(e.request).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        return res;
      });
    })
  );
});
"""


def build_worker_js(welcome_text, identity_text, manifest_text):
    def b64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    tmpl = r"""
const WELCOME = %s;
const IDENTITY = %s;
const GATE = %s;
const MANIFEST = %s;
const SW = %s;
const ICON_192 = %s;
const ICON_512 = %s;
function b64ToBytes(s) {
  const bin = atob(s);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}
const HTML_HEADERS = {
  "content-type": "text/html;charset=utf-8",
  "cache-control": "no-store, no-cache, must-revalidate"
};
export default {
  fetch(req) {
    const url = new URL(req.url);
    const p = url.pathname;
    if (p === "/hub" || p.startsWith("/hub/")) {
      return Response.redirect(
        "https://nayanet.live" + url.pathname + url.search, 302);
    }
    if (p === "/enter") {
      /* NAYA GUEST GUARD v1 — see GATE_HTML in deploy-entrance.py. */
      return new Response(GATE, { headers: HTML_HEADERS });
    }
    if (p === "/identity.html") {
      return new Response(IDENTITY, { headers: HTML_HEADERS });
    }
    if (p === "/manifest.webmanifest" || p === "/manifest.json") {
      return new Response(MANIFEST, { headers: {
        "content-type": "application/manifest+json;charset=utf-8",
        "cache-control": "no-cache" } });
    }
    if (p === "/icon-192.png") {
      return new Response(b64ToBytes(ICON_192), { headers: {
        "content-type": "image/png",
        "cache-control": "public, max-age=86400" } });
    }
    if (p === "/icon-512.png") {
      return new Response(b64ToBytes(ICON_512), { headers: {
        "content-type": "image/png",
        "cache-control": "public, max-age=86400" } });
    }
    if (p === "/sw.js") {
      return new Response(SW, { headers: {
        "content-type": "application/javascript;charset=utf-8",
        "cache-control": "no-cache" } });
    }
    return new Response(WELCOME, { headers: HTML_HEADERS });
  }
};
"""
    return (tmpl % (json.dumps(welcome_text), json.dumps(identity_text),
                    json.dumps(GATE_HTML),
                    json.dumps(manifest_text), json.dumps(SW_JS),
                    json.dumps(b64(ICON_192_PATH)),
                    json.dumps(b64(ICON_512_PATH)))).encode()


def deploy():
    with open(WELCOME_PATH, encoding="utf-8") as f:
        welcome = f.read()
    with open(IDENTITY_PATH, encoding="utf-8") as f:
        identity = f.read()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = f.read()

    # Gates first — block on any failure.
    if not css_brace_check(welcome, WELCOME_PATH):
        print("✗ Deploy BLOCKED by CSS check (welcome)")
        return None
    if not css_brace_check(identity, IDENTITY_PATH):
        print("✗ Deploy BLOCKED by CSS check (identity)")
        return None
    if not node_check_scripts(welcome, WELCOME_PATH):
        print("✗ Deploy BLOCKED by JS check (welcome)")
        return None
    if not node_check_scripts(identity, IDENTITY_PATH):
        print("✗ Deploy BLOCKED by JS check (identity)")
        return None

    # Inject the anon key (value never printed).
    if "__SB_ANON_KEY__" not in identity:
        print("✗ Deploy BLOCKED: '__SB_ANON_KEY__' placeholder missing in identity.html")
        return None
    anon_key = extract_anon_key()
    if not anon_key:
        return None
    identity = identity.replace("__SB_ANON_KEY__", anon_key)
    if "__SB_ANON_KEY__" in identity:
        print("✗ Deploy BLOCKED: placeholder still present after injection")
        return None
    print("✓ Anon key injected into identity page for this build")

    worker_js = build_worker_js(welcome, identity, manifest)

    metadata = json.dumps({
        "main_module": "worker.js",
        "compatibility_date": "2024-01-01"
    }).encode()

    boundary = "----nayaformdata7d3f9a1c"
    b = boundary.encode()
    body = (b"--" + b + b"\r\n"
            b'Content-Disposition: form-data; name="metadata"\r\n'
            b"Content-Type: application/json\r\n\r\n" + metadata + b"\r\n"
            b"--" + b + b"\r\n"
            b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n'
            b"Content-Type: application/javascript+module\r\n\r\n" + worker_js + b"\r\n"
            b"--" + b + b"--\r\n")

    req = urllib.request.Request(
        f"{BASE}/accounts/{ACCT}/workers/scripts/{WORKER_NAME}",
        data=body, method="PUT"
    )
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        if result.get("success"):
            url = f"https://{WORKER_NAME}.nayapower.workers.dev/"
            print(f"✓ Deployed: {url}")
            return url
        else:
            print(f"✗ Deploy failed: {result}")
            return None


if __name__ == '__main__':
    deploy()
