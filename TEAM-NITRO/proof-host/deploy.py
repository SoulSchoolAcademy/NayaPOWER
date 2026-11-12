#!/usr/bin/env python3
"""Deploy naya-proof-host to Cloudflare via multipart PUT.
Reuses the registered custom.cloudflare credential mechanism (dynamic_credentials),
exactly like cf-api.py — the token never appears in code, args, env, or logs.
Multipart shape (proven 2026-11-06): metadata part first (application/json),
then the script part with Content-Type application/javascript+module.
Plain application/javascript on the script part 400s with error 10021.
Usage: python3 deploy.py [put|subdomain|status]
"""
import json
import sys
import urllib.request
import uuid

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ACCOUNT_ID = "b5e2a51b3e883f7722287c5f51b1196b"
WORKER_NAME = "naya-proof-host"
BASE = "https://api.cloudflare.com/client/v4"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def _open(req):
    add_surrogate_to_request(req, "custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
        return read_json_response(resp)


def put_worker():
    with open("worker.js", "rb") as f:
        script = f.read()
    boundary = "----naya-proof-host-" + uuid.uuid4().hex
    bnd = boundary.encode()
    metadata = json.dumps({"main_module": "worker.js"}).encode()
    parts = []
    parts.append(b"--" + bnd)
    parts.append(b'Content-Disposition: form-data; name="metadata"')
    parts.append(b"Content-Type: application/json")
    parts.append(b"")
    parts.append(metadata)
    parts.append(b"--" + bnd)
    parts.append(b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"')
    parts.append(b"Content-Type: application/javascript+module")
    parts.append(b"")
    parts.append(script)
    parts.append(b"--" + bnd + b"--")
    parts.append(b"")
    body = b"\r\n".join(parts)
    req = urllib.request.Request(
        f"{BASE}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="PUT")
    result = _open(req)
    print(json.dumps(result, indent=2))
    return result.get("success")


def enable_subdomain():
    req = urllib.request.Request(
        f"{BASE}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}/subdomain",
        data=json.dumps({"enabled": True}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST")
    result = _open(req)
    print(json.dumps(result, indent=2))
    return result.get("success")


def status():
    req = urllib.request.Request(
        f"{BASE}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}",
        method="GET")
    result = _open(req)
    print(json.dumps(result, indent=2))
    return result.get("success")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "put"
    if action == "put":
        ok = put_worker()
    elif action == "subdomain":
        ok = enable_subdomain()
    elif action == "status":
        ok = status()
    else:
        print(f"unknown action: {action}")
        sys.exit(2)
    sys.exit(0 if ok else 1)
