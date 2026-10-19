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

def deploy(html_path, worker_name):
    with open(html_path, 'rb') as f:
        html = f.read()
    
    worker_js = ("const HTML = %s;\n"
                 "export default { fetch() { return new Response(HTML, "
                 "{headers: {'content-type': 'text/html;charset=utf-8', "
                 "'cache-control': 'no-store, no-cache, must-revalidate'}}); } };\n"
                 % json.dumps(html.decode("utf-8"))).encode()
    
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
