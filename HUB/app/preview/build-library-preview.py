#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Intelligent Library preview.

Implements the DRAFT blueprint (room-library-BLUEPRINT-DRAFT.pdf) — NOT
locked. Inlines library.css + library-adapter.js + library.js and renders
window.NayaRooms.library into #app. Seeds: real canonical references
(SN-016/017/217, IB-006, DEC-6TO10) + DEMO-labeled illustrations.
"""
import os

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/library-preview.html')

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/library.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/library-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/library.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.LibraryAdapter=window.LibraryAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(ad) + inner(js)
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const objs=LibraryAdapter.parseMany(LibraryAdapter.REAL.concat(LibraryAdapter.DEMO,LibraryAdapter.QA_SEEDS));"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.library(el,{objects:objs,verified:true}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Intelligent Library \u2014 Shelved, not stored</title>'
            '<style>body{margin:0;background:#060608;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes' % (OUT, len(html)))

if __name__ == '__main__':
    main()
