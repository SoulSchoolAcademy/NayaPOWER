#!/usr/bin/env python3
"""v5 Factory generator: WHOLE working pages + PI injection. Never extract, never rebuild.

THE FACTORY LAW (2026-11-03): The Factory holds whole working pages, not fragments.
Each template = the live page (nayanet.app/personal, /dashboard, /space) fetched fresh
+ the citizen's PI injected as window.PAGE_* globals. The page's own code reads these
and renders itself alive. When Shawn upgrades a page, every future citizen page gets
the upgrade automatically — because we use what we have, we don't copy it.

Usage: build-v5.py <alias> <name> <vision> <mission> <goal> <outdir>
   or: build-v5.py --selftest  (builds Shawn's pages to /tmp/naya-preview/)
"""
import re, sys, json, urllib.request, os

SOURCES = {
    'personal': 'https://nayanet.app/personal',
    'business': 'https://nayanet.app/dashboard',
    'space':    'https://nayanet.app/space',
}
# membership: no standalone page exists. It is a view inside space/personal.
# We do NOT invent one. When Shawn builds a real membership page, add it here.

_cache = {}
def fetch(url):
    if url not in _cache:
        req = urllib.request.Request(url, headers={'User-Agent': 'NayaFactory/5.0'})
        _cache[url] = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
    return _cache[url]

def build(page_type, pi):
    src = fetch(SOURCES[page_type])
    if '<script' not in src:
        raise RuntimeError(f"{page_type}: source has no scripts — not a working page")
    inject = ("<script>\n"
        "/* NIAS PI INJECTION — citizen identity. The page's own code reads these. */\n"
        f"window.PAGE_ALIAS={json.dumps(pi['alias'])};\n"
        f"window.PAGE_NAME={json.dumps(pi['name'])};\n"
        f"window.PAGE_VISION={json.dumps(pi['vision'])};\n"
        f"window.PAGE_MISSION={json.dumps(pi['mission'])};\n"
        f"window.PAGE_GOAL={json.dumps(pi['goal'])};\n"
        f"window.PAGE_TYPE={json.dumps(page_type)};\n"
        "</script>\n")
    out, n = re.subn(r'<head[^>]*>', lambda m: m.group(0) + '\n' + inject, src, count=1)
    assert n == 1, f"no <head> in {page_type}"
    assert out.count('<script') == src.count('<script') + 1, f"scripts damaged in {page_type}"
    assert '{{' not in out or out.count('{{') < 5, f"unfilled template vars in {page_type}"
    return out

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--selftest':
        pi = {'name': 'Shawn', 'alias': 'shawnlife',
              'vision': 'A world where every person has a home for their intelligence.',
              'mission': 'Give every citizen a page that works as hard as they do.',
              'goal': 'One million citizens, every one thriving.'}
        os.makedirs('/tmp/naya-preview', exist_ok=True)
        for t in SOURCES:
            out = build(t, pi)
            open(f'/tmp/naya-preview/v5-{t}.html', 'w').write(out)
            print(f"{t}: {len(out)} bytes, {out.count('<script')} scripts, ALIVE")
        return
    if len(sys.argv) != 8:
        print(__doc__); sys.exit(2)
    _, alias, name, vision, mission, goal, outdir = sys.argv
    pi = {'alias': alias, 'name': name, 'vision': vision, 'mission': mission, 'goal': goal}
    os.makedirs(outdir, exist_ok=True)
    for t in SOURCES:
        out = build(t, pi)
        p = os.path.join(outdir, f'{t}.html')
        open(p, 'w').write(out)
        print(f"WROTE {p} ({len(out)} bytes)")

if __name__ == '__main__':
    main()
