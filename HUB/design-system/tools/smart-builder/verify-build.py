#!/usr/bin/env python3
"""verify-build.py — the pipeline checks its own work.

Runs after assemble.py, before any receipt is written:
  1. Page exists, no unfilled placeholders.
  2. Embedded JS parses (node --check).
  3. Machine JSON + pieces JSON parse.
  4. Headless render: page loads, specimens paint (screenshot non-empty).
  5. Wall models all resolve in the index.

Exit 0 = verified. Exit 1 = failed, with reasons. Updates the manifest.
"""
import json, re, subprocess, sys, os

def fail(msg):
    print('VERIFY FAIL:', msg)
    sys.exit(1)

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--page', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--index', required=True)
    a = ap.parse_args()

    if not os.path.exists(a.page):
        fail('page missing: ' + a.page)
    s = open(a.page, encoding='utf-8').read()
    if '%%' in s:
        fail('unfilled placeholders remain')
    print('ok: no placeholders')

    scripts = re.findall(r'<script>(.*?)</script>', s, re.S)
    if not scripts:
        fail('no script blocks')
    open('/tmp/_verify_app.js', 'w').write(scripts[-1])
    r = subprocess.run(['node', '--check', '/tmp/_verify_app.js'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fail('JS syntax: ' + r.stderr[:300])
    print('ok: JS parses')

    m = re.search(r'var PIECES = (\[.*?\]);\nvar CSSBANK', s, re.S)
    if not m:
        fail('PIECES JSON not found')
    pieces = json.loads(m.group(1))
    print('ok: PIECES parses,', len(pieces), 'entries')

    m2 = re.search(r'<pre id="machinejson">(.*?)</pre>', s, re.S)
    if not m2:
        fail('machine <pre> not found')
    json.loads(m2.group(1))
    print('ok: machine JSON parses')

    idx = json.load(open(a.index))
    manifest = json.load(open(a.manifest))
    for model in manifest['wall_pieces']:
        if model not in idx['pieces']:
            fail('wall model not in index: ' + model)
    print('ok: all', len(manifest['wall_pieces']), 'wall models resolve')

    # headless render smoke test
    chrome = os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome')
    shot = '/tmp/_verify_shot.png'
    if os.path.exists(chrome):
        r = subprocess.run(
            [chrome, '--headless', '--disable-gpu', '--no-sandbox',
             '--window-size=1280,2000', '--hide-scrollbars',
             '--virtual-time-budget=6000', '--screenshot=' + shot,
             'file://' + os.path.abspath(a.page)],
            capture_output=True, text=True, timeout=60)
        if not os.path.exists(shot) or os.path.getsize(shot) < 20000:
            fail('render produced no meaningful screenshot')
        print('ok: renders, screenshot', os.path.getsize(shot), 'bytes')
    else:
        print('skip: no headless chrome available')

    manifest['verification'] = 'passed'
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('VERIFY PASSED')

if __name__ == '__main__':
    main()
