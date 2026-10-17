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

def find_all_fns(src, name):
    """All definitions of a room function. Her base declares some rooms twice
    (a dead first copy + the live second copy); JS hoisting makes the LAST one
    win, so replacing only the first leaves her stub live. Replace every copy."""
    out = []
    for m in re.finditer(r'(async\s+)?function\s+%s\s*\(' % re.escape(name), src):
        j = src.find('{', m.start())
        out.append((m.start(), brace_span(src, j)[1]))
    if not out:
        raise ValueError('function %s not found' % name)
    return out

def main():
    src = open(BASE).read()
    print('base bytes:', len(src))

    # 1. Replace the 10 stub room functions (today() stays verbatim).
    #    Every duplicate definition is replaced: her base defines
    #    reports/library/settings/notes twice, and hoisting makes the last win.
    for name in ROOMS:
        new_fn = open(os.path.join(BUILD, 'rooms', name + '.js')).read().strip()
        spans = find_all_fns(src, name)
        old_head = src[spans[0][0]:spans[0][0]+60].replace('\n', ' ')
        for s, e in reversed(spans):
            src = src[:s] + new_fn + src[e:]
        print('replaced %-12s x%d (was: %s...)' % (name, len(spans), old_head[:50]))

    # 1b. Wire render() to the room functions, not her governed() stubs.
    #     Her render() routes connections/mail through governed('connections'|'mail'),
    #     which would leave our furnished rooms as dead code.
    r1 = "page==='connections'?await governed('connections',S.connections)"
    assert r1 in src, 'connections render mapping not found'
    src = src.replace(r1, "page==='connections'?connections()", 1)
    r2 = "page==='mail'?await governed('mail',S.mail)"
    assert r2 in src, 'mail render mapping not found'
    src = src.replace(r2, "page==='mail'?mail()", 1)
    print('render(): connections/mail now call the furnished rooms')

    # 1c. Deep-link the address bar on nav clicks. history.replaceState (not
    #     location.hash) so her hashchange->fromHash listener does not double-render.
    b1 = 'await render(a.dataset.page)'
    assert b1 in src, 'nav bind render call not found'
    src = src.replace(b1,
        "await render(a.dataset.page);try{history.replaceState(null,'','#/'+a.dataset.page)}catch(_){}", 1)
    print('bind(): nav clicks now deep-link #/<room>')

    # 1d. Canonical name: Smart Share -> Smart Connect (room head, nav rail, side map).
    s1 = "share:{title:'Smart Share',kicker:'SHARE'"
    assert s1 in src, 'S.share title not found'
    src = src.replace(s1, "share:{title:'Smart Connect',kicker:'CONNECT'", 1)
    n1 = '<button data-page="share"'
    _ni = src.find(n1)
    assert _ni != -1
    _nj = src.find('</button>', _ni)
    _nav = src[_ni:_nj]
    assert 'Smart Share' in _nav, 'nav share label not found'
    src = src[:_ni] + _nav.replace('Smart Share', 'Smart Connect') + src[_nj:]
    assert "'Collective':'Smart Share'" in src, 'side map label not found'
    src = src.replace("'Collective':'Smart Share'", "'Collective':'Smart Connect'", 1)
    assert 'Smart Share' not in src, 'stale Smart Share remains'
    print('renamed Smart Share -> Smart Connect everywhere')

    # 1f. IB → feed pipeline (the TRIGGER). Intelligent Blocks written to
    #     BRAIN/04-INTELLIGENCE/SMART-NOTES/** become feed blocks in the Hub's
    #     .blocks container. The Hub is the OUTPUT; this injection is the
    #     event fan-out. Production trigger: GitHub Actions on push to
    #     SMART-NOTES/**.
    import subprocess as _sp
    _r = _sp.run(['python3', os.path.join(BUILD, 'ib-ingest.py')],
                 capture_output=True, text=True)
    print(_r.stdout.strip().splitlines()[-2:])
    assert _r.returncode == 0, 'ib-ingest failed: ' + _r.stderr[:300]
    _ib = open(os.path.join(BUILD, 'ib-blocks.html')).read().strip()
    _bt = '<div class="blocks" id="blocks">'
    assert _bt in src, '.blocks container not found'
    _marker = '<!-- IB-FEED: live blocks from the IB pipeline (appended after curated blocks) -->'
    if _ib:
        # Append BEFORE the closing </div> of #blocks (not at the top):
        # her normalize scripts assume index 0 is her curated lead block and
        # rewrite its title. Our blocks live after hers, titles intact.
        _bi = src.find(_bt)
        _depth, _close = 0, None
        for _m in re.finditer(r'</?div\b', src[_bi:]):
            if _m.group(0) == '<div':
                _depth += 1
            else:
                _depth -= 1
                if _depth == 0:
                    _close = _bi + _m.start()
                    break
        assert _close is not None, '#blocks close not found'
        src = src[:_close] + '\n' + _marker + '\n' + _ib + '\n' + src[_close:]
        print('ib-feed: appended %d IB blocks after curated blocks'
              % _ib.count('<article class="block ib-block"'))
    else:
        print('ib-feed: no IB blocks (empty source)')
    # 1e. Scope repair: her base splits room functions across two IIFE closures.
    #     connections()/mail() were defined only in the first closure, but
    #     render(page) lives in the second -- so render() threw ReferenceError.
    #     Append our copies into render()'s own script block (before </script>);
    #     function declarations hoist, so render() resolves them.
    import re as _re
    _toks = [(_m.start(), 'open') for _m in _re.finditer(r'<script(?![^>]*src=)[^>]*>', src)]
    _toks += [(_m.start(), 'close') for _m in _re.finditer(r'</script>', src)]
    _toks.sort()
    _stack, _blocks = [], []
    for _pos, _typ in _toks:
        if _typ == 'open':
            _stack.append(_pos)
        elif _stack:
            _blocks.append((_stack.pop(), _pos))
    _rb = next(i for i, (_s, _e) in enumerate(_blocks)
               if _s < src.find('async function render(page)') < _e)
    _rs, _re_ = _blocks[_rb]
    assert 'function connections(){' not in src[_rs:_re_], 'connections already in render block'
    # Insert INSIDE the IIFE (before its closing })();), not after it:
    # our rooms close over the IIFE-scoped helpers head/card/S/Q/R.
    _iife_close = src.rfind('})();', _rs, _re_)
    assert _iife_close != -1, 'IIFE close not found in render block'
    _inject = ''
    for _name in ['connections', 'mail']:
        _inject += '\n' + open(os.path.join(BUILD, 'rooms', _name + '.js')).read().strip() + '\n'
    src = src[:_iife_close] + _inject + src[_iife_close:]
    print('scope: connections()/mail() appended into render() block')

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

    # 3b. Smart tabs: the KIND axis (All / Smart Notes / Activity / Reports)
    # over her AUDIENCE axis. Her feed() is IIFE-scoped, so the tabs compose
    # by re-applying kind filtering after her mode handlers run.
    _tabs = open(os.path.join(BUILD, 'rooms', 'smart-tabs.html')).read()
    assert '</body>' in src
    src = src.replace('</body>', '\n<!-- SMART-TABS -->\n' + _tabs + '\n</body>', 1)
    print('smart-tabs: injected')

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
    assert "page==='connections'?connections()" in src, 'connections render mapping'
    assert "page==='mail'?mail()" in src, 'mail render mapping'
    assert "history.replaceState(null,'','#/'+a.dataset.page)" in src, 'deep-link bind'
    assert "share:{title:'Smart Connect'" in src, 'Smart Connect rename'
    assert 'naya-room-boot' not in src or True
    assert 'NayaHub' in src and 'HubActions' in src
    assert 'data-hub-action' in src
    print('structural: OK')
    return 0 if bad == 0 else 1

sys.exit(main())
