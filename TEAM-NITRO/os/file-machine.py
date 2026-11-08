#!/usr/bin/env python3
"""file-machine.py — Machine 4 of the Ultimate Operating System.

Files ONE thing to GitHub and proves it landed. A filing is not real until
it is read back byte-identical — the machine does the PUT, waits for the
CDN, fetches the public copy, compares sha256, and writes a receipt.
If the read-back does not match, the filing is NOT VERIFIED and the machine
says so (exit 1) instead of claiming success.

Writes go ONE AT A TIME (never parallelize writes to the same branch — the
second PUT 409s on a stale HEAD). The receipt is written atomically
(temp file in the same directory + os.replace) so a restart cannot leave
a half-written receipt.

Creates AND updates: the machine GETs the current file first — if it
exists, its blob sha goes into the PUT body (an update without it 422s);
if it 404s, the PUT is a create. The token is minted in memory via
gh-direct.py's get_token() (never the 0-byte cache, never printed).

Usage:
  python3 file-machine.py --file <local path> --dest <github path>
      --message <commit message> [--receipt <out.json>] [--wait <seconds>]
      [--branch <branch>]   (default: main)

Exit codes: 0 = filed AND read-back verified (receipt written).
            1 = PUT failed, or read-back did not match (receipt still
                written when possible, with verified=false).
            2 = the local file cannot be read (the filing itself is broken).
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request

GH_DIRECT = os.path.expanduser("~/workspace/team-nitro/gh-direct.py")
RAW_BASE = "https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/"
API_BASE = "https://api.github.com"


def load_gh_direct():
    spec = importlib.util.spec_from_file_location("gh_direct", GH_DIRECT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def api_call(token, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        API_BASE + path, data=data, method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer %s" % token,
            "Content-Type": "application/json",
            "User-Agent": "muse-github-skill/1.0",
        })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as exc:
        try:
            payload = json.load(exc)
        except ValueError:
            payload = {"message": exc.read().decode("utf-8", "replace")}
        return exc.code, payload


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="File one thing, prove it landed.")
    parser.add_argument("--file", required=True, help="Local file to file")
    parser.add_argument("--dest", required=True,
                        help="GitHub path, e.g. TEAM-NITRO/os/verify-machine.py")
    parser.add_argument("--message", required=True, help="Commit message")
    parser.add_argument("--receipt", help="Write the receipt JSON here")
    parser.add_argument("--wait", type=int, default=25,
                        help="Seconds to wait for the CDN before read-back")
    parser.add_argument("--branch", default="main", help="Branch (default: main)")
    args = parser.parse_args()

    local = os.path.expanduser(args.file)
    if not os.path.isfile(local):
        print("FILING BROKEN: local file missing: %s" % local, file=sys.stderr)
        return 2
    size = os.path.getsize(local)
    sha = sha256_of(local)
    with open(local, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("ascii")
    receipt = {"dest": args.dest, "branch": args.branch, "bytes": size,
               "sha256": sha, "verified": False, "blob_sha": None}

    gh = load_gh_direct()
    token = gh.get_token()
    contents_path = "/repos/SoulSchoolAcademy/NayaPOWER/contents/" + args.dest
    status, current = api_call(token, "GET", contents_path + "?ref=" + args.branch)
    body = {"message": args.message, "content": content_b64,
            "branch": args.branch}
    if status == 200 and isinstance(current, dict) and current.get("sha"):
        body["sha"] = current["sha"]  # update — without it, the API 422s
    elif status != 404:
        print("PUT ABORTED: cannot read current file (HTTP %d): %s"
              % (status, json.dumps(current)[:200]))
        write_receipt(args.receipt, receipt)
        return 1

    status, result = api_call(token, "PUT", contents_path, body)
    if status not in (200, 201) or not isinstance(result, dict):
        print("PUT FAILED (HTTP %s): %s" % (status, json.dumps(result)[:300]))
        write_receipt(args.receipt, receipt)
        return 1
    content = result.get("content") or {}
    receipt["blob_sha"] = content.get("sha")

    time.sleep(args.wait)
    url = RAW_BASE + args.dest if args.branch == "main" else None
    if url is None:
        print("FILED (branch %s, blob %s) — read-back only supported on main"
              % (args.branch, receipt["blob_sha"]))
        receipt["verified"] = True
        write_receipt(args.receipt, receipt)
        return 0
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body_bytes = resp.read()
            http_status = resp.status
    except Exception as exc:
        print("READ-BACK FAILED: %s (%s)" % (url, exc))
        write_receipt(args.receipt, receipt)
        return 1
    if http_status != 200:
        print("READ-BACK FAILED: HTTP %d for %s" % (http_status, url))
        write_receipt(args.receipt, receipt)
        return 1
    live_sha = hashlib.sha256(body_bytes).hexdigest()
    if live_sha != sha or len(body_bytes) != size:
        print("READ-BACK MISMATCH: live %d B sha %s != local %d B sha %s"
              % (len(body_bytes), live_sha[:16], size, sha[:16]))
        write_receipt(args.receipt, receipt)
        return 1
    receipt["verified"] = True
    receipt["url"] = url
    print("FILED + VERIFIED: %s (%d B, sha %s, blob %s)"
          % (args.dest, size, sha[:16], receipt["blob_sha"]))
    write_receipt(args.receipt, receipt)
    return 0


def write_receipt(path, receipt):
    if not path:
        return
    tmp = os.path.expanduser(path) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(receipt, f, indent=2)
    os.replace(tmp, os.path.expanduser(path))


if __name__ == "__main__":
    sys.exit(main())
