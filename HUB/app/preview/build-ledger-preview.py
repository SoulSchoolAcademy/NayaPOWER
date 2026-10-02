#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a deterministic Smart Ledger preview.

Reads receipt artifacts (decision + execution receipts) and combines them with
the current adapter, room JS, and CSS — the same projection pattern:
canonical source -> deterministic adapter -> premium room.
"""
import json, os, glob

REPO = os.path.expanduser('~/workspace/nayapower-room02')
RECEIPTS = os.path.expanduser('~/workspace/demo-staging/receipts')
OUT = os.path.expanduser('~/workspace/your_files/ledger-preview.html')

def main():
    objs = []
    for f in sorted(glob.glob(os.path.join(RECEIPTS, '*.json'))):
        try:
            objs.append(json.load(open(f, encoding='utf-8')))
        except Exception:
            pass
    css = open(os.path.join(REPO, 'HUB/app/css/ledger.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/ledger-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/ledger.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.LedgerAdapter=window.LedgerAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(ad) + inner(js)
               + 'const RAW=' + json.dumps(objs) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const entries=LedgerAdapter.parseMany(RAW);"
               + "const root=document.getElementById('app');"
               + "root.appendChild(window.NayaRooms.ledger(el,{entries:entries}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Smart Ledger — Room Four Preview</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes, %d receipts' % (OUT, len(html), len(objs)))

if __name__ == '__main__':
    main()
