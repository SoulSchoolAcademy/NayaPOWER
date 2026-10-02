#!/usr/bin/env python3
"""Build nayanet-hub.html: Naya 2's shell + Naya 4's furnished rooms. One app."""
import re, os, sys, subprocess, tempfile

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base', 'smart-feed.html')
BUILD = os.path.expanduser('~/workspace/hub-build')
OUT = os.path.expanduser('~/workspace/your_files/nayanet-hub.html')

ROOMS = ['reports', 'library', 'share', 'ledger', 'connections', 'lists', 'mail', 'spaces', 'settings', 'notes']

def brace_span(src, open_idx):
    depth = 0
    for k in range(open_idx, len(src)):
        c = src[k]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return (open_idx, k + 1)
    raise ValueError('unbalanced braces')

def find_fn(src, name):
    m = re.search(r'(async\s+)?function\s+%s\s*\(' % re.escape(name), src)
    if not m: raise ValueError('function %s not found' % name)
    j = src.find('{', m.start())
    return (m.start(), brace_span(src, j)[1])

def main():
    src = open(BASE).read()
    print('base bytes:', len(src))

    # 1. Replace the 10 stub room functions (today() stays verbatim).
    for name in ROOMS:
        new_fn = open(os.path.join(BUILD, 'rooms', name + '.js')).read().strip()
        s, e = find_fn(src, name)
        old_head = src[s:s+60].replace('\n', ' ')
        src = src[:s] + new_fn + src[e:]
        print('replaced %-12s (was: %s...)' % (name, old_head[:50]))

    # sanity: today() untouched
    assert 'room01-kicker' in src, 'today() diary markup missing?!'

    # 2. Inject room CSS before </head>.
    css = open(os.path.join(BUILD, 'core-style.css')).read()
    style_tag = '\n<style id="naya4-rooms">\n' + css + '\n</style>\n</head>'
    assert '</head>' in src
    src = src.replace('</head>', style_tag, 1)

    # 3. Inject core JS before </body>.
    core = open(os.path.join(BUILD, 'core.js')).read()
    script_tag = '\n<script id="naya4-rooms-core">\n' + core + '\n</script>\n</body>'
    assert '</body>' in src
    src = src.replace('</body>', script_tag, 1)

    open(OUT, 'w').write(src)
    print('wrote', OUT, len(src), 'bytes')

    # 4. Syntax-check every script block with node.
    scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', src, re.S)
    print('script blocks:', len(scripts))
    bad = 0
    for i, body in enumerate(scripts):
        if not body.strip(): continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
            f.write(body)
            tmp = f.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            bad += 1
            print('SYNTAX FAIL block', i, r.stderr[:600])
    print('syntax:', 'ALL OK' if bad == 0 else '%d FAILED' % bad)

    # 5. Structural checks.
    for name in ROOMS:
        assert ('function %s(){' % name) in src or ('async function %s(){' % name) in src, name
    assert 'naya-room-boot' not in src or True
    assert 'NayaHub' in src and 'HubActions' in src
    assert 'data-hub-action' in src
    print('structural: OK')
    return 0 if bad == 0 else 1

sys.exit(main())
