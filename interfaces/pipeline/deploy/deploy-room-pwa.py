#!/usr/bin/env python3
"""Deploy Smart Spaces as a real PWA — the installable-app prototype.

Serves from the nayaroom-spaces worker:
  /rooms/spaces                -> the page (HTML, no-store)
  /rooms/spaces/manifest.json  -> PWA manifest
  /rooms/spaces/sw.js          -> service worker (offline shell)
  /rooms/spaces/icons/*.png    -> the crystal-N icon assets (naya-icon-192/512, apple-touch-icon)

Icons are embedded as base64 (same assets the Hub's PWA pass used).
Usage: python3 deploy-spaces-pwa.py <spaces.html> <worker_name>
"""

import base64
import json
import sys
import urllib.request
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
BASE = "https://api.cloudflare.com/client/v4"
HERE = sys.argv[3] if len(sys.argv) > 3 else "/home/hatch/workspace/factory-pipeline/pwa-assets/spaces"
ROOM = sys.argv[4] if len(sys.argv) > 4 else "/rooms/spaces"
ICONS = "/home/hatch/workspace/user/files/icons"

WORKER_TMPL = r"""
const ROOM = %s;
const PAGE = %s;
const MANIFEST = %s;
const SW = %s;
const ICONS = {
  "naya-icon-192.png": { type: "image/png", b64: %s },
  "naya-icon-512.png": { type: "image/png", b64: %s },
  "apple-touch-icon.png": { type: "image/png", b64: %s }
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
    if (p.endsWith("/manifest.json")) {
      return new Response(MANIFEST, { headers: {
        "content-type": "application/manifest+json;charset=utf-8",
        "cache-control": "no-cache" } });
    }
    if (p.endsWith("/sw.js")) {
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
    if (p === ROOM || p === ROOM + "/" || p === "/") {
      return new Response(PAGE, { headers: {
        "content-type": "text/html;charset=utf-8",
        "cache-control": "no-store, no-cache, must-revalidate" } });
    }
    return new Response("not found", { status: 404 });
  }
};
"""


def read_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def deploy(html_path, worker_name):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    with open(HERE + "/manifest.json", encoding="utf-8") as f:
        manifest = f.read()
    with open(HERE + "/sw.js", encoding="utf-8") as f:
        sw = f.read()

    worker_js = (WORKER_TMPL % (
        json.dumps(ROOM),
        json.dumps(html),
        json.dumps(manifest),
        json.dumps(sw),
        json.dumps(read_b64(ICONS + "/naya-icon-192.png")),
        json.dumps(read_b64(ICONS + "/naya-icon-512.png")),
        json.dumps(read_b64(ICONS + "/apple-touch-icon.png")),
    )).encode()

    print(f"worker size: {len(worker_js)} bytes")

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
            print(f"\u2713 Deployed: {url}")
            return url
        else:
            print(f"\u2717 Deploy failed: {result}")
            return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: deploy-room-pwa.py <page.html> <worker_name> [assets_dir] [room_path]")
        sys.exit(1)
    deploy(sys.argv[1], sys.argv[2])
