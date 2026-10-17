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

def parse_chrome_log(stderr):
    """Pure: extract (js_errors, network_urls) from chrome
    --enable-logging=stderr output.

    js_errors: CONSOLE lines reporting uncaught exceptions or failed
    resource loads (dbus/GPU noise never matches these patterns).
    network_urls: every URL the renderer actually requested, via
    NetworkDelegate::NotifyBeforeURLRequest.
    """
    js_errors, urls = [], []
    for line in stderr.splitlines():
        if ':CONSOLE' in line and ('Uncaught' in line
                                   or 'Failed to load resource' in line):
            js_errors.append(line.strip())
        m = re.search(r'NetworkDelegate::NotifyBeforeURLRequest:\s*(\S+)', line)
        if m:
            urls.append(m.group(1))
    return js_errors, urls

def url_fetch_failed(url, timeout=10):
    """True if an http(s) URL the page fetched cannot be fetched. Only
    http/https can fail over the network; file:/data:/blob: are local."""
    if not url.startswith(('http://', 'https://')):
        return False
    try:
        import urllib.request
        req = urllib.request.Request(url, method='HEAD',
                                     headers={'User-Agent': 'NayaPOWER-day-one/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return not (200 <= r.status < 400)
    except Exception:
        return True

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

def day_one_check(sb_dir, index_path, chrome):
    """Day-one acceptance: assemble the MINIMAL contract (no connections,
    no privacy, no optional features) and prove the page renders with
    ZERO JS errors and ZERO failed network fetches, and every chrome
    control has an accessible name. Returns a status dict; never raises.
    """
    tag = 'day-one'
    contract = os.path.join(sb_dir, 'contracts', 'minimal-day-one-v1.json')
    template = os.path.join(sb_dir, 'templates', 'page.html')
    page = '/tmp/_dayone_page.html'
    manifest = '/tmp/_dayone_manifest.json'
    shot = '/tmp/_dayone_shot.png'
    for f in (page, shot):
        if os.path.exists(f):
            os.remove(f)
    r = subprocess.run(
        [sys.executable, os.path.join(sb_dir, 'assemble.py'),
         '--contract', contract, '--index', index_path,
         '--template', template, '--out', page, '--manifest', manifest],
        capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not os.path.exists(page):
        return {'status': 'failed',
                'note': 'minimal contract refused to assemble: '
                        + (r.stdout + r.stderr)[:200]}
    s = open(page, encoding='utf-8').read()
    if '%%' in s:
        return {'status': 'failed', 'note': 'minimal page has unfilled placeholders'}
    r = subprocess.run(
        [chrome, '--headless', '--disable-gpu', '--no-sandbox',
         '--enable-logging=stderr', '--v=1',
         '--window-size=1280,2000', '--hide-scrollbars',
         '--virtual-time-budget=8000', '--screenshot=' + shot,
         'file://' + os.path.abspath(page)],
        capture_output=True, text=True, timeout=90)
    js_errors, net_urls = parse_chrome_log(r.stderr)
    if js_errors:
        return {'status': 'failed',
                'note': 'JS errors on minimal page: %s' % js_errors[0][:200]}
    failed = sorted({u for u in net_urls if url_fetch_failed(u)})
    if failed:
        return {'status': 'failed',
                'note': 'failed network fetches: %s' % failed[0][:200]}
    chrome_html = re.sub(r'<div class="spec-stage">.*?</div>\s*</div>', '', s, flags=re.S)
    bad_btns = [b for b in re.findall(r'<button([^>]*)>(.*?)</button>', chrome_html, re.S)
                if not (b[1].strip() or 'aria-label' in b[0])]
    if bad_btns:
        return {'status': 'failed',
                'note': '%d controls without accessible names' % len(bad_btns)}
    if not os.path.exists(shot) or os.path.getsize(shot) < 20000:
        return {'status': 'failed', 'note': 'minimal page did not paint'}
    return {'status': 'passed',
            'note': ('zero JS errors, zero failed fetches '
                     '(%d external request(s) all OK), controls named, painted %d bytes')
                    % (len([u for u in net_urls if u.startswith('http')]),
                       os.path.getsize(shot))}

def consent_honesty_check(page_html, manifest):
    """UI/receipt honesty (consent-line): the assembler must never emit copy
    or receipt fields saying 'connected' when the feature is merely ready.

    Naming convention the verifier asserts: every feature row carries
    data-feature + data-consent. data-consent="connected" requires the
    build receipt's consent entry for that feature to show at least one
    grant-active connected action; data-consent="ready" requires none.
    The receipt must also mirror the machine block's resolved connections
    (the audit trail). Returns (ok, note)."""
    receipt = manifest.get('receipt', {})
    consent = receipt.get('consent', {})
    rows = re.findall(r'data-feature="([^"]+)"[^>]*data-consent="([^"]+)"',
                      page_html)
    for fid, state in rows:
        entry = consent.get(fid, {})
        has_active = bool(entry.get('connected_active'))
        if state == 'connected' and not has_active:
            return (False, 'page claims CONNECTED for %s but the receipt shows '
                           'no active grant' % fid)
        if state == 'ready' and has_active:
            return (False, 'page labels %s READY but the receipt shows active '
                           'connected actions' % fid)
    m = re.search(r'<pre id="machinejson">(.*?)</pre>', page_html, re.S)
    if m:
        try:
            mach = json.loads(m.group(1))
        except Exception:
            return False, 'machine JSON in page does not parse'
        if mach.get('connections') != receipt.get('grants'):
            return (False, 'receipt grants do not mirror the machine block '
                           '(audit trail broken)')
    return True, '%d feature row(s) honest; receipt mirrors %d grant(s)' % (
        len(rows), len(receipt.get('grants', {})))

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--page', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--skip-day-one', action='store_true',
                    help='skip the day-one acceptance check (already run)')
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

    # day-one acceptance: the MINIMAL contract (no connections, no privacy,
    # no optional features) must render with zero JS errors, zero failed
    # network fetches, named controls. Part of structural PASS — a failed
    # day-one fails the verify; a skipped day-one (no chrome) is honest.
    day_one = {'status': 'skipped',
               'note': 'no headless chrome available — ' + chrome_source}
    if not a.skip_day_one and chrome:
        sb_dir = os.path.dirname(os.path.abspath(__file__))
        day_one = day_one_check(sb_dir, a.index, chrome)
        if day_one['status'] == 'failed':
            fail('day-one acceptance: ' + day_one['note'])
        print('ok: day-one working —', day_one['note'])
    elif not a.skip_day_one:
        print('day-one: SKIPPED —', day_one['note'])

    # consent-line honesty: never claim "connected" for a merely-ready
    # feature; the receipt must mirror the resolved grants. Part of
    # structural PASS.
    consent_ok, consent_note = consent_honesty_check(s, manifest)
    if not consent_ok:
        fail('consent honesty: ' + consent_note)
    print('ok: consent honesty —', consent_note)

    manifest['verification'] = {
        'structural': 'passed',
        'render': render_status,
        'render_note': render_note,
        'day_one': day_one,
        'consent_honesty': 'passed',
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('VERIFY structural PASSED; render:', render_status.upper(),
          '; day-one:', day_one['status'].upper(), '; consent: HONEST')

if __name__ == '__main__':
    main()
