#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Smart List preview.

Bakes the 24 canonical smart-note files as raw {path, content} and runs them
through the real ListAdapter.parseNotes in-page — the same projection pattern:
canonical source -> deterministic adapter -> premium room.
"""
import json, os, glob

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/list-preview.html')

def main():
    files = []
    for f in sorted(glob.glob(os.path.join(REPO,
            'BRAIN/05-MEMORY/SMART-NOTES/2026/*/*/*/*/*/*/IB-SMART-NOTE*.md'))):
        try:
            files.append({
                'path': os.path.relpath(f, REPO),
                'content': open(f, encoding='utf-8').read(),
            })
        except Exception:
            pass

    css = open(os.path.join(REPO, 'HUB/app/css/list.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/list-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/list.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.ListAdapter=window.ListAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(ad) + inner(js)
               + 'const RAW=' + json.dumps(files, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const notes=ListAdapter.parseNotes(RAW);"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.smartList(el,{notes:notes}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Smart List \u2014 Room Preview</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes, %d note files' % (OUT, len(html), len(files)))

if __name__ == '__main__':
    main()
