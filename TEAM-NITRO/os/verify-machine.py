#!/usr/bin/env python3
"""verify-machine.py — Machine 3 of the Ultimate Operating System.

Takes a receipt (JSON) and checks it MECHANICALLY. Done is a fact the
machine checks, not a claim a seat makes. If any check fails, the item is
NOT VERIFIED — the board shows it in-motion with a "proof missing" marker,
never as done.

Receipt fields:
  file             — path to the delivered file (required)
  sha256           — the claimed sha256 of the file (required)
  bytes            — the claimed size in bytes (required)
  live_url         — (optional) a URL that must serve the same bytes
                     (proof-host URL with &cb=<blob>); fetched with a
                     browser User-Agent (Cloudflare 1010 lesson)
  verifier_report  — (optional) path to the verifier's written report
  items            — (optional) [{name, verdict}] — each item's verdict must
                     appear in the verifier's report as "PASS"

Usage:
  python3 verify-machine.py --receipt receipt.json
  python3 verify-machine.py --file <path> --sha256 <sha> --bytes <n>
      [--live-url <url>] [--verifier-report <path>] [--items <json>]

Exit codes: 0 = VERIFIED (every check passed).
            1 = NOT VERIFIED (failed checks listed).
            2 = the receipt cannot be read (the check itself is broken).
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_bytes(url, timeout=60):
    import http.client
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")})
    last_exc = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    return None, resp.status
                return resp.read(), resp.status
        except Exception as exc:
            # IncompleteRead and transient cuts are retryable; after 3
            # attempts the fetch is reported as failed (honest "couldn't
            # check", never a false "bytes differ").
            last_exc = exc
            time.sleep(5)
    raise last_exc


def verify(receipt):
    failures = []
    checks = []

    path = os.path.expanduser(receipt.get("file", ""))
    if not path or not os.path.isfile(path):
        failures.append("file missing on disk: %s" % path)
        return checks, failures
    checks.append("file exists: %s" % path)

    actual_sha = sha256_of(path)
    expected_sha = (receipt.get("sha256") or "").lower()
    if not expected_sha:
        failures.append("receipt names no sha256")
    elif actual_sha != expected_sha:
        failures.append("sha256 mismatch: file is %s, receipt claims %s"
                        % (actual_sha, expected_sha))
    else:
        checks.append("sha256 matches: %s" % actual_sha[:16])

    actual_bytes = os.path.getsize(path)
    expected_bytes = receipt.get("bytes")
    if expected_bytes is None:
        failures.append("receipt names no byte size")
    elif actual_bytes != expected_bytes:
        failures.append("size mismatch: file is %d bytes, receipt claims %d"
                        % (actual_bytes, expected_bytes))
    else:
        checks.append("size matches: %d bytes" % actual_bytes)

    live_url = receipt.get("live_url")
    if live_url:
        try:
            body, status = fetch_bytes(live_url)
        except Exception as exc:
            failures.append("live URL fetch failed: %s (%s)" % (live_url, exc))
            body = None
        if body is not None:
            live_sha = hashlib.sha256(body).hexdigest()
            if live_sha != actual_sha:
                failures.append("live URL serves different bytes: %s != file %s"
                                % (live_sha[:16], actual_sha[:16]))
            else:
                checks.append("live URL serves the same bytes (%d B, sha match)"
                              % len(body))

    report_path = receipt.get("verifier_report")
    items = receipt.get("items") or []
    if items and not report_path:
        failures.append("receipt names items but no verifier report")
    if report_path:
        if not os.path.isfile(os.path.expanduser(report_path)):
            failures.append("verifier report missing on disk: %s" % report_path)
        else:
            with open(os.path.expanduser(report_path), errors="replace") as f:
                report = f.read()
            for item in items:
                name = item.get("name", "")
                verdict = (item.get("verdict") or "").upper()
                if verdict != "PASS":
                    failures.append("item '%s' verdict is %s, not PASS"
                                    % (name, verdict))
                elif name and name not in report:
                    failures.append("item '%s' not found in verifier report"
                                    % name)
                else:
                    checks.append("item '%s' PASS in verifier report" % name)

    return checks, failures


def main():
    parser = argparse.ArgumentParser(description="Check a receipt mechanically.")
    parser.add_argument("--receipt", help="JSON receipt file")
    parser.add_argument("--file", help="Delivered file path")
    parser.add_argument("--sha256", help="Claimed sha256")
    parser.add_argument("--bytes", type=int, help="Claimed size in bytes")
    parser.add_argument("--live-url", help="URL that must serve the same bytes")
    parser.add_argument("--verifier-report", help="Verifier's written report")
    parser.add_argument("--items", help="JSON list [{name, verdict}]")
    args = parser.parse_args()

    if args.receipt:
        try:
            with open(args.receipt) as f:
                receipt = json.load(f)
        except (OSError, ValueError) as exc:
            print("VERIFY BROKEN: cannot read receipt: %s" % exc, file=sys.stderr)
            return 2
    else:
        receipt = {"file": args.file, "sha256": args.sha256, "bytes": args.bytes,
                   "live_url": args.live_url,
                   "verifier_report": args.verifier_report}
        if args.items:
            try:
                receipt["items"] = json.loads(args.items)
            except ValueError as exc:
                print("VERIFY BROKEN: bad --items JSON: %s" % exc, file=sys.stderr)
                return 2

    checks, failures = verify(receipt)
    for line in checks:
        print("  ok: %s" % line)
    if failures:
        print("NOT VERIFIED:")
        for line in failures:
            print("  - %s" % line)
        return 1
    print("VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
