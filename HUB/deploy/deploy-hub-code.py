#!/usr/bin/env python3
"""Deploy Hub CODE — Balanced Machine step 4 (deploy split from sync).

Until now the only thing that ever deployed worker `hub` was the note
sync, and only when a new note landed — finished Hub fixes sat
invisible until a note happened to arrive. This wrapper deploys the
Hub's HTML on its own, whenever the code changes:

  1. CSS brace gate — the SAME check deploy.py runs (imported, not
     reimplemented; a red gate blocks the deploy).
  2. Rollback snapshot — the currently-live bytes are fetched and
     saved BEFORE anything is overwritten, and a rollback note
     (previous md5 + snapshot path + the exact restore command) is
     appended to HUB-ROLLBACK.md.
  3. Deploy — through deploy.py's own deploy() (Cloudflare PUT).
  4. Smoke check — the live URL must answer HTTP 200, contain the
     byte marker, and serve bytes whose md5 equals the deployed
     file's md5 (the worker serves the page verbatim). Any failure
     prints the rollback command in the output.

This wrapper NEVER edits the HTML file and never touches the feed
table. index-2.html has exactly one content writer (the note sync's
bake) and now two deploy triggers (bake, code) — both through the
same deploy.py gate.

Usage:
  deploy-hub-code.py --check   # dry-run: gate + md5 + live read only
  deploy-hub-code.py           # full deploy with snapshot + smoke
Options: --html PATH (default ~/workspace/user/files/index-2.html)
         --worker NAME (default hub)
         --url URL (default https://nayanet.live/)
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HTML = os.path.expanduser('~/workspace/user/files/index-2.html')
SNAPSHOT_DIR = os.path.join(HERE, 'hub-snapshots')
ROLLBACK_NOTE = os.path.join(HERE, 'HUB-ROLLBACK.md')
DEPLOY_STATE = os.path.join(HERE, '.hub-deploy-state.json')
MARKER = 'window.NayaFeedIntelligence'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/126.0 Safari/537.36'}


def load_deploy_module():
    spec = importlib.util.spec_from_file_location(
        'naya_deploy', os.path.join(HERE, 'deploy.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def fetch_live(url, retries=3):
    """GET the live page; returns (status, bytes). Read-only.

    Uses curl: this box's urllib reads of the Cloudflare edge drop
    mid-body (IncompleteRead) while curl --retry completes — observed
    repeatedly, including this wrapper's first dry-run."""
    import subprocess
    import tempfile
    last = None
    for _ in range(retries):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tmp = tf.name
            r = subprocess.run(
                ['curl', '-sS', '--retry', '4', '--retry-all-errors',
                 '-A', UA['User-Agent'], '-o', tmp, '-w', '%{http_code}',
                 url],
                capture_output=True, text=True, timeout=60)
            with open(tmp, 'rb') as f:
                body = f.read()
            os.unlink(tmp)
            status = int(r.stdout.strip()[-3:])
            if status == 200 and len(body) > 0:
                return status, body
            last = f'HTTP {status}, {len(body)} bytes'
        except Exception as e:
            last = e
    raise RuntimeError(f'live fetch failed after {retries} tries: {last}')


def smoke(url, expect_md5):
    status, body = fetch_live(url)
    ok_status = status == 200
    ok_marker = MARKER.encode() in body
    got_md5 = md5_bytes(body)
    ok_md5 = got_md5 == expect_md5
    return ok_status and ok_marker and ok_md5, {
        'status': status, 'marker': ok_marker,
        'live_md5': got_md5, 'md5_match': ok_md5}


def main():
    ap = argparse.ArgumentParser(description='Deploy Hub code, decoupled '
                                                 'from the note sync')
    ap.add_argument('--check', action='store_true',
                    help='dry-run: gate + hashes + live read; deploy nothing')
    ap.add_argument('--html', default=DEFAULT_HTML)
    ap.add_argument('--worker', default='hub')
    ap.add_argument('--url', default='https://nayanet.live/')
    args = ap.parse_args()

    deploy_mod = load_deploy_module()

    with open(args.html, 'rb') as f:
        html_bytes = f.read()
    html_text = html_bytes.decode('utf-8')
    file_md5 = md5_bytes(html_bytes)
    print(f"file: {args.html}")
    print(f"file md5: {file_md5} ({len(html_bytes)} bytes)")

    # Gate 1 — the deploy.py CSS brace check, imported verbatim.
    if not deploy_mod.css_brace_check(html_text, args.html):
        print('✗ BLOCKED by CSS brace gate — nothing deployed')
        return 1
    if MARKER not in html_text:
        print(f'✗ BLOCKED: byte marker {MARKER!r} absent from file')
        return 1

    # Read the live state (read-only in both modes).
    try:
        status, live_bytes = fetch_live(args.url)
        live_md5 = md5_bytes(live_bytes)
        print(f"live: {args.url} HTTP {status}, md5 {live_md5} "
              f"({len(live_bytes)} bytes)")
    except Exception as e:
        print(f'✗ cannot read live page: {e}')
        return 1

    if args.check:
        same = live_md5 == file_md5
        print(f"DRY-RUN: live {'==' if same else '!='} file — "
              f"a real run would {'skip nothing (bytes identical)' if same else 'deploy the file bytes'}"
              f", snapshotting the live bytes first for rollback.")
        print('DRY-RUN: nothing deployed, nothing written.')
        return 0

    # Step 2 — rollback snapshot of the bytes live RIGHT NOW.
    ts = datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y%m%dT%H%M%SZ')
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    snap_path = os.path.join(SNAPSHOT_DIR, f'live-before-{ts}.html')
    with open(snap_path, 'wb') as f:
        f.write(live_bytes)
    rollback_cmd = (f"python3 {os.path.join(HERE, 'deploy.py')} "
                    f"{snap_path} {args.worker}")
    with open(ROLLBACK_NOTE, 'a') as f:
        f.write(f"\n## {ts} — deploy of {args.html}\n"
                f"- previous live md5: {live_md5} ({len(live_bytes)} bytes)\n"
                f"- snapshot of previous live bytes: {snap_path}\n"
                f"- new file md5: {file_md5}\n"
                f"- rollback: `{rollback_cmd}`\n")
    print(f"rollback snapshot: {snap_path} (md5 {live_md5})")

    # Step 3 — deploy through deploy.py itself.
    url = deploy_mod.deploy(args.html, args.worker)
    if not url:
        print(f'✗ deploy failed — live bytes unchanged. '
              f'Rollback (if ever needed): {rollback_cmd}')
        return 1
    print(f"deployed: {url}")

    # Step 4 — smoke check on the natural address.
    ok, detail = smoke(args.url, file_md5)
    print(f"smoke: {detail}")
    if not ok:
        print(f'✗ SMOKE FAILED — roll back now with: {rollback_cmd}')
        return 1
    with open(DEPLOY_STATE, 'w') as f:
        json.dump({'md5': file_md5, 'url': args.url, 'worker': args.worker,
                   'at': datetime.datetime.now(
                       datetime.timezone.utc).isoformat(),
                   'rollback_snapshot': snap_path}, f, indent=2)
    print('✓ smoke passed — live serves exactly the deployed bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
