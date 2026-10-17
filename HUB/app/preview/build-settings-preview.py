#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Settings room preview.

No adapter: Settings is pure control surface. Inlines the room CSS + JS and
renders window.NayaRooms.settings into #app on DOMContentLoaded.
"""
import os

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/settings-preview.html')

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/settings.css'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/settings.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(js)
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.settings(el,{userName:'Shawn Vibert'}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Settings \u2014 Hub control surface</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes' % (OUT, len(html)))

if __name__ == '__main__':
    main()
