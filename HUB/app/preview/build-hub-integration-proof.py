#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Hub integration proof page.

Assembles the REAL Hub shell from branch naya/hub-complete-app-v1
(framework: runtime, router, views, shell CSS) with Naya 4's rich rooms
mounted through HUB/app/js/rooms/shell-adapter.js — instead of the shell's
own placeholder room files.

This is a PROOF, not a production change: it verifies that
  1. the sidebar rail navigates between rooms (hash routing), and
  2. the rich rooms render full-bleed and beautiful inside the shell.
The two PROOF-ONLY CSS overrides are a proposal for the chassis lane
(Naya 2, PR #1340) to accept, modify, or reject — not a unilateral change.
"""
import json, os, subprocess, sys

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/hub-integration-proof.html')
GH = os.path.expanduser('~/workspace/skills/github/bin/gh-api')
BRANCH = 'naya/hub-complete-app-v1'

SHELL_CSS = ['tokens', 'base', 'shell', 'components', 'states', 'views', 'rooms']
SHELL_JS = ['runtime', 'runtime-live', 'components', 'router',
            'views/welcome', 'views/identity', 'views/hub']
MY_CSS = ['spaces', 'mail', 'connections', 'list', 'ledger', 'connect',
          'reports', 'settings']
MY_JS = ['people-registry.js',
         'rooms/spaces-adapter.js', 'rooms/spaces.js',
         'rooms/mail-adapter.js', 'rooms/mail.js',
         'rooms/connections-adapter.js', 'rooms/connections.js',
         'rooms/list-adapter.js', 'rooms/list.js',
         'rooms/ledger-adapter.js', 'rooms/ledger.js',
         'rooms/connect-adapter.js', 'rooms/connect.js',
         'rooms/reports-adapter.js', 'rooms/reports-loader.js', 'rooms/reports.js',
         'rooms/settings.js',
         'rooms/shell-adapter.js']


def gh_file(path):
    r = subprocess.run([GH, 'GET',
                        f'/repos/SoulSchoolAcademy/NayaPOWER/contents/{path}?ref={BRANCH}'],
                       capture_output=True, text=True)
    d = json.loads(r.stdout)
    import base64
    return base64.b64decode(d['content']).decode('utf-8')


def local(path):
    with open(os.path.join(REPO, path), encoding='utf-8') as f:
        return f.read()


def mod(path):
    """Import a preview builder module by file path (hyphenated filename)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'mod_' + os.path.basename(path).replace('-', '_').replace('.py', ''), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    css_parts = []
    for name in SHELL_CSS:
        css_parts.append(f"/* shell:{name} */\n" + gh_file(f'HUB/app/css/{name}.css'))
    for name in MY_CSS:
        css_parts.append(f"/* naya4:{name} */\n" + local(f'HUB/app/css/{name}.css'))
    # PROOF-ONLY overrides: full-bleed room outlet, no duplicate room head.
    # Proposed to the chassis lane (Naya 2 / PR #1340) — accept/modify/reject.
    css_parts.append("""/* PROOF-ONLY (proposal, not a shell change):
   The rich rooms were composed for the full viewport, like their previews.
   The shell's 1460px centered column + duplicated room head squeeze them. */
.shell .main{ max-width:none; padding:0 0 80px; }
.shell .room-head{ display:none; }""")

    # Seeds: one source of truth — the preview builders' module constants.
    sp = mod(os.path.join(REPO, 'HUB/app/preview/build-spaces-preview.py'))
    mp = mod(os.path.join(REPO, 'HUB/app/preview/build-mail-preview.py'))
    seed_json = json.dumps({
        'contacts': sp.CONTACTS,
        'spaces': sp.SPACES,
        'threads': mp.THREADS,
        'notes': [], 'entries': [], 'doors': [], 'reports': [],
        'me': 'shawn', 'userName': 'Shawn Vibert',
    }, ensure_ascii=False)

    js_parts = []
    for name in MY_JS:
        js_parts.append(f"/* naya4:{name} */\n" + local(f'HUB/app/js/{name}'))
    js_parts.append("/* proof seeds */\nwindow.__NayaShellSeeds = " + seed_json + ";")
    # shell-adapter must run AFTER seeds are set (it is last in MY_JS, so re-emit order matters).
    # MY_JS already ends with shell-adapter.js; seeds were appended after it — wrong order.
    # Fix: rebuild with seeds before the adapter.
    js_parts = []
    for name in MY_JS[:-1]:
        js_parts.append(f"/* naya4:{name} */\n" + local(f'HUB/app/js/{name}'))
    js_parts.append("/* proof seeds */\nwindow.__NayaShellSeeds = " + seed_json + ";")
    js_parts.append("/* naya4:rooms/shell-adapter.js */\n" + local('HUB/app/js/rooms/shell-adapter.js'))
    for name in SHELL_JS:
        js_parts.append(f"/* shell:{name} */\n" + gh_file(f'HUB/app/js/{name}.js'))
    js_parts.append("/* proof boot */\nif(!location.hash){location.hash='#/hub/spaces';}")
    js_parts.append("/* shell:app */\n" + gh_file('HUB/app/js/app.js'))

    html = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>Hub Integration Proof — Naya 4 rooms in the real shell</title>'
            '<style>' + '\n'.join(css_parts) + '</style></head>'
            '<body><div id="app"></div><noscript><p>Needs JavaScript</p></noscript>'
            '<script>' + '\n'.join(js_parts) + '</script></body></html>')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', OUT, len(html), 'bytes')


if __name__ == '__main__':
    main()
