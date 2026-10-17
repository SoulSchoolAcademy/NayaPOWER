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
import json, re, shutil, subprocess, sys, os

def fail(msg):
    print('VERIFY FAIL:', msg)
    sys.exit(1)

def find_chrome():
    """Locate a headless-chrome binary.

    Priority: CHROME env var override -> PATH binaries ->
    Playwright installs (any version, chrome or chrome-headless-shell) ->
    legacy pinned path. Returns (path or None, probed description).
    """
    probed = []

    def accept(p):
        if p:
            probed.append(p)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return p
        return None

    env = os.environ.get('CHROME')
    if env:
        found = accept(env)
        if found:
            return found, 'CHROME=' + env
        return None, 'CHROME=%s (missing/not executable)' % env
    for name in ('google-chrome', 'google-chrome-stable', 'chrome',
                 'chromium', 'chromium-browser'):
        found = accept(shutil.which(name))
        if found:
            return found, 'PATH:' + name
    import glob
    base = os.path.expanduser('~/.cache/ms-playwright')
    for pat in (os.path.join(base, 'chromium-*', 'chrome-linux*', 'chrome'),
                os.path.join(base, 'chromium_headless_shell-*',
                             'chrome-headless-shell-linux64',
                             'chrome-headless-shell')):
        for p in sorted(glob.glob(pat)):
            found = accept(p)
            if found:
                return found, 'playwright:' + p
    # legacy pinned path — last resort, kept so old receipts stay explainable
    found = accept(os.path.expanduser(
        '~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'))
    if found:
        return found, 'legacy-pinned'
    return None, 'probed: ' + ', '.join(probed) + ' — none executable'

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--page', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--require-render', action='store_true',
                    help='Fail acceptance if headless browser rendering is unavailable or fails')
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

    m = re.search(r'<pre id="machinejson">(.*?)</pre>', s, re.S)
    if not m:
        fail('machine <pre> not found')
    json.loads(m.group(1))
    print('ok: machine JSON parses')

    idx = json.load(open(a.index))
    manifest = json.load(open(a.manifest))
    wall_models = manifest.get('resolution', {}).get('wall_pieces',
                                                     manifest.get('wall_pieces', []))
    for model in wall_models:
        if model not in idx['pieces']:
            fail('wall model not in index: ' + model)
    print('ok: all', len(wall_models), 'wall models resolve')

    # bounded accessibility checks on page chrome (specimen contents are
    # library data, judged at the library level, not per page)
    if not re.search(r'<html[^>]*\slang=', s):
        fail('a11y: <html> missing lang')
    if 'name="viewport"' not in s:
        fail('a11y: viewport meta missing')
    chrome_html = re.sub(r'<div class="spec-stage">.*?</div>\s*</div>', '', s, flags=re.S)
    bad_btns = [b for b in re.findall(r'<button([^>]*)>(.*?)</button>', chrome_html, re.S)
                if not (b[1].strip() or 'aria-label' in b[0])]
    if bad_btns:
        fail('a11y: %d chrome buttons without accessible names' % len(bad_btns))
    print('ok: a11y chrome checks (lang, viewport, button names)')

    # headless render check — recorded separately, never silently passed.
    # Structural PASS does not imply visual PASS. Trial 1 acceptance
    # requires render == "passed".
    chrome, chrome_source = find_chrome()
    shot = '/tmp/_verify_shot.png'
    render_status, render_note = 'skipped', 'no headless chrome available — ' + chrome_source
    if chrome:
        if os.path.exists(shot):
            os.remove(shot)  # never judge a render on a stale screenshot
        r = subprocess.run(
            [chrome, '--headless', '--disable-gpu', '--no-sandbox',
             '--window-size=1280,2000',
             '--hide-scrollbars',
             '--virtual-time-budget=6000', '--screenshot=' + shot,
             'file://' + os.path.abspath(a.page)],
            capture_output=True, text=True, timeout=60)
        if not os.path.exists(shot) or os.path.getsize(shot) < 20000:
            render_status, render_note = (
                'failed', 'render produced no meaningful screenshot via ' + chrome_source)
        else:
            render_status = 'passed'
            render_note = 'screenshot %d bytes via %s' % (os.path.getsize(shot), chrome_source)
            print('ok: renders,', render_note)
    else:
        print('render: SKIPPED —', render_note)

    manifest['verification'] = {
        'structural': 'passed',
        'render': render_status,
        'render_note': render_note,
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('VERIFY structural PASSED; render:', render_status.upper())
    if a.require_render and render_status != 'passed':
        fail('release acceptance requires browser render PASS, got ' + render_status)

if __name__ == '__main__':
    main()
