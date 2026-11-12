#!/usr/bin/env python3
"""Deploy — customized HTML → live Cloudflare worker URL.

Takes HTML file + worker name → deploys → returns live URL.
"""

import json
import sys
import urllib.request
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
BASE = "https://api.cloudflare.com/client/v4"

def css_brace_check(html_text, path):
    """Balance check every <style> block (braces + comments + strings).
    Shawn 2026-10-20 incident: ONE dropped '}' silently swallowed ~1,100
    lines of CSS (lens tabs, feed cards). CSS fails silently; this gate
    makes the failure loud BEFORE deploy. Returns True when balanced."""
    lines = html_text.split("\n")
    blocks = []
    start = None
    for i, ln in enumerate(lines, 1):
        if "<style" in ln and start is None:
            start = i
        if "</style>" in ln and start is not None:
            blocks.append((start, i))
            start = None
    for a, b in blocks:
        depth, in_comment = 0, False
        for ln in lines[a - 1:b]:
            j, cstr = 0, None
            while j < len(ln):
                if in_comment:
                    if ln[j:j + 2] == "*/":
                        in_comment = False
                        j += 2
                    else:
                        j += 1
                    continue
                if cstr is not None:
                    if ln[j] == "\\":
                        j += 2
                        continue
                    if ln[j] == cstr:
                        cstr = None
                    j += 1
                    continue
                if ln[j:j + 2] == "/*":
                    in_comment = True
                    j += 2
                    continue
                if ln[j] in ('"', "'"):
                    cstr = ln[j]
                    j += 1
                    continue
                if ln[j] == "{":
                    depth += 1
                elif ln[j] == "}":
                    depth -= 1
                    if depth < 0:
                        print(f"✗ CSS CHECK FAIL {path}: extra '}}' in style block lines {a}-{b}")
                        return False
                j += 1
        if depth != 0 or in_comment:
            print(f"✗ CSS CHECK FAIL {path}: style block lines {a}-{b} unbalanced (depth={depth}, comment_open={in_comment})")
            return False
    print(f"✓ CSS check: {len(blocks)} style blocks balanced")
    return True


PWA_ASSETS = "/home/hatch/workspace/factory-pipeline/pwa-assets"
ICON_DIR = "/home/hatch/workspace/user/files/icons"


def build_worker_js(html_bytes, html_text):
    """Build the worker source. When the page carries a manifest link,
    emit the PWA worker (page + /manifest.json + /sw.js + /icons/*).
    Otherwise the classic single-page worker."""
    if 'rel="manifest"' not in html_text:
        return ("const HTML = %s;\n"
                "export default { fetch() { return new Response(HTML, "
                "{headers: {'content-type': 'text/html;charset=utf-8', "
                "'cache-control': 'no-store, no-cache, must-revalidate'}}); } };\n"
                % json.dumps(html_text)).encode()

    if 'id="os-script"' in html_text:
        # One-system flagship body: serve the PAGE'S OWN manifest, built
        # from the page's own title — not the shared Hub manifest (S2 /
        # interrogation cure, 2026-10-22). The shell SW stays the shared
        # one: it precaches '/', '/manifest.json' and the icons generically.
        import html as _html_mod
        import re as _re
        _m = _re.search(r"<title>(.*?)</title>", html_text, _re.S)
        _title = _html_mod.unescape(_m.group(1)).strip() if _m else "NayaNET"
        _page_manifest = {
            "name": _title,
            "short_name": _title.split("—")[0].split("|")[0].strip()[:30] or "NayaNET",
            "description": "A living NayaNET smart app — wall, messages, invites, "
                           "reports and a live dashboard, in one page.",
            "start_url": ".",
            "scope": ".",
            "display": "standalone",
            "orientation": "portrait-primary",
            "background_color": "#000000",
            "theme_color": "#000000",
            "icons": [
                {"purpose": "any", "sizes": "192x192",
                 "src": "/icons/naya-icon-192.png", "type": "image/png"},
                {"purpose": "any", "sizes": "512x512",
                 "src": "/icons/naya-icon-512.png", "type": "image/png"},
                {"purpose": "maskable", "sizes": "512x512",
                 "src": "/icons/naya-icon-512.png", "type": "image/png"},
            ],
        }
        manifest = json.dumps(_page_manifest)
    else:
        with open(PWA_ASSETS + "/hub/manifest.json", encoding="utf-8") as f:
            manifest = f.read()
    with open(PWA_ASSETS + "/hub/sw.js", encoding="utf-8") as f:
        sw = f.read()
    import base64

    def b64(name):
        with open(ICON_DIR + "/" + name, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    tmpl = r"""
const PAGE = %s;
const MANIFEST = %s;
const SW = %s;
const ICONS = {
  "naya-icon-192.png": { type: "image/png", b64: %s },
  "naya-icon-512.png": { type: "image/png", b64: %s },
  "apple-touch-icon.png": { type: "image/png", b64: %s },
  "naya-guide.jpg": { type: "image/jpeg", b64: %s }
};
function b64ToBytes(s) {
  const bin = atob(s);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}
export default {
  fetch(req) {
    const url = new URL(req.url);
    const p = url.pathname;
    if (p === "/manifest.json" || p.endsWith("/manifest.json")) {
      return new Response(MANIFEST, { headers: {
        "content-type": "application/manifest+json;charset=utf-8",
        "cache-control": "no-cache" } });
    }
    if (p === "/sw.js" || p.endsWith("/sw.js")) {
      return new Response(SW, { headers: {
        "content-type": "application/javascript;charset=utf-8",
        "cache-control": "no-cache" } });
    }
    const iconMatch = p.match(/\/icons\/([A-Za-z0-9\-_.]+)$/);
    if (iconMatch && ICONS[iconMatch[1]]) {
      const ic = ICONS[iconMatch[1]];
      return new Response(b64ToBytes(ic.b64), { headers: {
        "content-type": ic.type,
        "cache-control": "public, max-age=86400" } });
    }
    return new Response(PAGE, { headers: {
      "content-type": "text/html;charset=utf-8",
      "cache-control": "no-store, no-cache, must-revalidate" } });
  }
};
"""
    return (tmpl % (json.dumps(html_text), json.dumps(manifest), json.dumps(sw),
                    json.dumps(b64("naya-icon-192.png")),
                    json.dumps(b64("naya-icon-512.png")),
                    json.dumps(b64("apple-touch-icon.png")),
                    json.dumps(b64("naya-guide.jpg")))).encode()


def deploy(html_path, worker_name):
    with open(html_path, 'rb') as f:
        html = f.read()

    if not css_brace_check(html.decode("utf-8"), html_path):
        print("✗ Deploy BLOCKED by CSS check")
        return None
    worker_js = build_worker_js(html, html.decode("utf-8"))
    
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
        f"{BASE}/accounts/{ACCT}/workers/scripts/{worker_name}",
        data=body, method="PUT"
    )
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        if result.get("success"):
            url = f"https://{worker_name}.nayapower.workers.dev/"
            print(f"✓ Deployed: {url}")
            return url
        else:
            print(f"✗ Deploy failed: {result}")
            return None

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: deploy.py <html_file> <worker_name>")
        sys.exit(1)
    deploy(sys.argv[1], sys.argv[2])
