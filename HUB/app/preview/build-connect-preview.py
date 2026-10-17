#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a deterministic Smart Connect preview.

Reads the CANONICAL Smart Door registry and combines it with the current
adapter, room JS, and CSS — the same projection pattern as Room 2:
canonical source -> deterministic adapter -> premium room.
"""
import json, os

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/connect-preview.html')

def main():
    reg = open(os.path.join(REPO, 'BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json'), encoding='utf-8').read()
    css = open(os.path.join(REPO, 'HUB/app/css/connect.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/connect-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/connect.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.ConnectAdapter=window.ConnectAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(ad) + inner(js)
               + 'const REG=' + json.dumps(reg) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const doors=ConnectAdapter.parse(JSON.parse(REG));"
               + "const root=document.getElementById('app');"
               + "root.appendChild(window.NayaRooms.connect(el,{doors:doors}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Smart Connect — Room Three Preview</title>'
            '<style>body{margin:0;background:#020403;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    n_doors = len(json.loads(reg)['doors'])
    print('wrote %s %d bytes, %d doors' % (OUT, len(html), n_doors))

if __name__ == '__main__':
    main()
