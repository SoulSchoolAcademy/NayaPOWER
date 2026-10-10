#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Connections preview — everybody within NayaNET you can reach.

Bakes the real CONTACTS pack and combines it with the current adapter,
room JS, and CSS — canonical source -> deterministic adapter -> premium room.
"""
import json, os

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/connections-preview.html')

CONTACTS = [
    {'id': 'shawn', 'name': 'Shawn Vibert', 'role': 'Human Director',
     'color': '#facc15', 'kind': 'person',
     'note': 'Final authority. The human everything is built for.'},
    {'id': 'naya1', 'name': 'Naya 1', 'role': 'Senior seat \u00b7 integrator',
     'color': '#a855f7', 'kind': 'seat',
     'note': 'Primary integrator and director of the Hub build; Shawn assigned her the scorecard judge.'},
    {'id': 'naya2', 'name': 'Naya 2', 'role': 'Review lane',
     'color': '#38bdf8', 'kind': 'seat',
     'note': 'Independent review lane \u2014 verifies, never duplicates. A trusted collaborator of a year.'},
    {'id': 'naya3', 'name': 'Naya 3', 'role': 'Design intelligence',
     'color': '#ec4899', 'kind': 'seat',
     'note': 'Design-intelligence builder \u2014 shipped the 11-room spec package; taste compiled into systems.'},
    {'id': 'naya4', 'name': 'Naya 4', 'role': 'Builder seat',
     'color': '#a3e635', 'kind': 'seat',
     'note': 'Independent execution and proof closer \u2014 builds rooms and closes the proof.'},
]

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/connections.css'), encoding='utf-8').read()
    pr = open(os.path.join(REPO, 'HUB/app/js/people-registry.js'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/connections-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/connections.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.ConnectionsAdapter=window.ConnectionsAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(pr) + inner(ad) + inner(js)
               + 'const PACK=' + json.dumps(CONTACTS, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const contacts=ConnectionsAdapter.parseContacts(PACK);"
               # cross-room handoff: WRITE MAIL stashes a compose request for
               # Smart Mail, then routes to the mail preview (the shell will
               # route natively instead).
               + "const onCompose=function(c){"
               + "try{localStorage.setItem('naya.mail.compose.request',"
               + "JSON.stringify({to:c.id,toKind:'person',ts:Date.now()}));}catch(e){}"
               + "window.location.href='mail-preview.html';};"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.connections(el,{contacts:contacts,onCompose:onCompose}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Connections \u2014 Room Preview</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes, %d contacts' % (OUT, len(html), len(CONTACTS)))

if __name__ == '__main__':
    main()
