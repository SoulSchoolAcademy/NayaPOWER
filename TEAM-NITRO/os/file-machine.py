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

Usage:
  python3 file-machine.py --file <local path> --dest <github path>
      --message <commit message> [--receipt <out.json>] [--wait <seconds>]

Exit codes: 0 = filed AND read-back verified (receipt written).
            1 = PUT failed, or read-back did not match (receipt still
                written when possible, with verified=false).
            2 = the local file cannot be read (the filing itself is broken).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

GH_DIRECT = os.path.expanduser("~/workspace/team-nitro/gh-direct.py")
RAW_BASE = "https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/"


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
    args = parser.parse_args()

    local = os.path.expanduser(args.file)
    if not os.path.isfile(local):
        print("FILING BROKEN: local file missing: %s" % local, file=sys.stderr)
        return 2
    size = os.path.getsize(local)
    sha = sha256_of(local)
    receipt = {"dest": args.dest, "bytes": size, "sha256": sha,
               "verified": False, "blob_sha": None}

    put = subprocess.run(
        [sys.executable, GH_DIRECT, "PUT",
         "/repos/SoulSchoolAcademy/NayaPOWER/contents/" + args.dest,
         "--file", local, "--message", args.message],
        capture_output=True, text=True, timeout=120)
    out = (put.stdout or "") + (put.stderr or "")
    blob = None
    for token in out.split('"sha":"'):
        if len(token) >= 40:
            blob = token[:40]
            break
    receipt["blob_sha"] = blob
    if put.returncode != 0 or not blob:
        print("PUT FAILED (exit %d): %s" % (put.returncode, out[:300]))
        write_receipt(args.receipt, receipt)
        return 1

    time.sleep(args.wait)
    url = RAW_BASE + args.dest
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            status = resp.status
    except Exception as exc:
        print("READ-BACK FAILED: %s (%s)" % (url, exc))
        write_receipt(args.receipt, receipt)
        return 1
    if status != 200:
        print("READ-BACK FAILED: HTTP %d for %s" % (status, url))
        write_receipt(args.receipt, receipt)
        return 1
    live_sha = hashlib.sha256(body).hexdigest()
    if live_sha != sha or len(body) != size:
        print("READ-BACK MISMATCH: live %d B sha %s != local %d B sha %s"
              % (len(body), live_sha[:16], size, sha[:16]))
        write_receipt(args.receipt, receipt)
        return 1
    receipt["verified"] = True
    receipt["url"] = url
    print("FILED + VERIFIED: %s (%d B, sha %s, blob %s)"
          % (args.dest, size, sha[:16], blob))
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
