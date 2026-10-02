#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Smart Spaces preview.

Bakes the shared CONTACTS/SPACES contract with clearly-labeled DEMO activity,
then inlines css + adapter + room and renders into #app.
No canonical group store exists; seeded spaces/activity are DEMO, members real.
"""
import json, os
from datetime import datetime, timedelta, timezone

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/spaces-preview.html')

CONTACTS = [
    {'id': 'shawn', 'name': 'Shawn Vibert', 'role': 'Human Director', 'color': '#facc15'},
    {'id': 'naya1', 'name': 'Naya 1', 'role': 'Senior seat \u00b7 integrator', 'color': '#a855f7'},
    {'id': 'naya2', 'name': 'Naya 2', 'role': 'Review lane', 'color': '#38bdf8'},
    {'id': 'naya3', 'name': 'Naya 3', 'role': 'Design intelligence', 'color': '#ec4899'},
    {'id': 'naya4', 'name': 'Naya 4', 'role': 'Builder seat', 'color': '#a3e635'},
]

def ago(hours):
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

SPACES = [
    {'id': 'team-naya', 'name': 'Team Naya', 'color': '#a855f7',
     'members': ['shawn', 'naya1', 'naya2', 'naya3', 'naya4'],
     'desc': 'The full build team \u2014 directors, lanes, and builders moving as one.',
     'activity': [
         {'ts': ago(3),  'text': 'Naya 4 pushed Living Intel v3 \u2014 the heartbeat hit 10/10.', 'demo': True},
         {'ts': ago(9),  'text': 'Shawn rated Connect 9.5 and locked the per-door color law.', 'demo': True},
         {'ts': ago(30), 'text': 'Naya 2 verified the Room Two loader across all six daily reports.', 'demo': True},
     ]},
    {'id': 'hub-builders', 'name': 'Hub Builders', 'color': '#22d3ee',
     'members': ['shawn', 'naya3', 'naya4'],
     'desc': 'Rooms, interfaces, and convergence \u2014 where the Hub gets built.',
     'activity': [
         {'ts': ago(5),  'text': 'Naya 4 shipped the Smart Ledger heartbeat dashboard.', 'demo': True},
         {'ts': ago(26), 'text': 'Naya 3 signed off on the design-intelligence projection model.', 'demo': True},
     ]},
    {'id': 'design-review', 'name': 'Design Review', 'color': '#ec4899',
     'members': ['shawn', 'naya3'],
     'desc': 'Taste, design law, and visual QA. Nothing ships ugly.',
     'activity': [
         {'ts': ago(7),  'text': 'Shawn: jewels stay lit, full-perimeter color \u2014 Connect approved.', 'demo': True},
         {'ts': ago(20), 'text': 'Naya 3 filed the type floor: 16px body, 11px labels minimum.', 'demo': True},
         {'ts': ago(44), 'text': 'Glass pass approved for ledger panels.', 'demo': True},
     ]},
]

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/spaces.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/spaces-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/spaces.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.SpacesAdapter=window.SpacesAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    data = {'contacts': CONTACTS, 'spaces': SPACES}
    full_js = (harness + inner(ad) + inner(js)
               + 'const PACKS=' + json.dumps(data, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const spaces=SpacesAdapter.parseSpaces(PACKS.spaces, PACKS.contacts);"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.smartSpaces(el,{spaces:spaces}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Smart Spaces \u2014 Room Preview</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes | spaces %d contacts %d' % (
        OUT, len(html), len(SPACES), len(CONTACTS)))

if __name__ == '__main__':
    main()
