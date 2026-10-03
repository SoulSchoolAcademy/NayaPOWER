#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Smart Spaces preview — the LIVING ROOM.

Bakes the shared CONTACTS/SPACES contract with clearly-labeled DEMO activity,
seeds the shared people spine, and pre-seeds one DEMO mail-to-space post so the
mail loop is demonstrable (DEMO-labeled, never presented as user content).
Inlines css + people-registry + adapter + room and renders into #app.
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

def ago(hours=0, minutes=0):
    return (datetime.now(timezone.utc) - timedelta(hours=hours, minutes=minutes)).isoformat()

SPACES = [
    {'id': 'team-naya', 'name': 'Team Naya', 'color': '#a855f7',
     'members': ['shawn', 'naya1', 'naya2', 'naya3', 'naya4'],
     'desc': 'The full build team \u2014 directors, lanes, and builders moving as one.',
     'activity': [
         {'ts': ago(minutes=12), 'author': 'Naya 2', 'text': 'Has anyone run the Room Two loader against all six daily reports yet?', 'demo': True},
         {'ts': ago(minutes=9), 'author': 'Naya 4', 'text': 'Just did \u2014 verified clean across all six.', 'demo': True},
         {'ts': ago(minutes=4), 'author': 'Shawn',  'text': 'Beautiful. Connect 9.5 is locked too \u2014 per-door color law.', 'demo': True},
         {'ts': ago(minutes=2), 'author': 'Naya 4', 'text': 'Living Intel v3 pushed \u2014 the heartbeat hit 10/10.', 'demo': True},
     ]},
    {'id': 'hub-builders', 'name': 'Hub Builders', 'color': '#22d3ee',
     'members': ['shawn', 'naya3', 'naya4'],
     'desc': 'Rooms, interfaces, and convergence \u2014 where the Hub gets built.',
     'activity': [
         {'ts': ago(minutes=18), 'author': 'Naya 3', 'text': 'Projection model signed off \u2014 are we good to converge the rooms?', 'demo': True},
         {'ts': ago(minutes=6), 'author': 'Naya 4', 'text': 'Ledger heartbeat dashboard shipped. We are good.', 'demo': True},
     ]},
    {'id': 'design-review', 'name': 'Design Review', 'color': '#ec4899',
     'members': ['shawn', 'naya3'],
     'desc': 'Taste, design law, and visual QA. Nothing ships ugly.',
     'activity': [
         {'ts': ago(minutes=25), 'author': 'Naya 3', 'text': 'Glass pass on the ledger panels \u2014 approved, but the borders need the full-perimeter treatment.', 'demo': True},
         {'ts': ago(minutes=11), 'author': 'Shawn',  'text': 'Agreed \u2014 jewels stay lit, full-perimeter color. Connect approved on that basis.', 'demo': True},
     ]},
]

# One DEMO mail-to-space post: shows the loop (a mail addressed to the space
# IS a post here). Demo-labeled in the room, never presented as user content.
MAIL_SEED = {
    'design-review': [
        {'ts': ago(2), 'author': 'Naya 2',
         'text': 'Mailed in from Smart Mail \u2014 same conversation, two views.', 'demo': True},
    ],
}

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/spaces.css'), encoding='utf-8').read()
    reg = open(os.path.join(REPO, 'HUB/app/js/people-registry.js'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/spaces-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/spaces.js'), encoding='utf-8').read()

    harness = (
        "function el(tag,cls,text){var e=document.createElement(tag);"
        "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
        "return e;}window.NayaRooms=window.NayaRooms||{};"
        "window.SpacesAdapter=window.SpacesAdapter||{};"
    )
    toast_js = (
        "function __spToast(m){"
        "var t=document.getElementById(\u0027sp-demo-toast\u0027);"
        "if(!t){t=document.createElement(\u0027div\u0027);t.id=\u0027sp-demo-toast\u0027;"
        "t.style.position=\u0027fixed\u0027;t.style.bottom=\u002728px\u0027;"
        "t.style.left=\u002750%\u0027;t.style.transform=\u0027translateX(-50%)\u0027;"
        "t.style.zIndex=\u002799\u0027;t.style.background=\u0027#17171c\u0027;"
        "t.style.color=\u0027#fff\u0027;t.style.border=\u00271px solid rgba(139,92,246,.6)\u0027;"
        "t.style.borderRadius=\u0027999px\u0027;t.style.padding=\u002712px 24px\u0027;"
        "t.style.font=\u0027700 13px system-ui\u0027;"
        "document.body.appendChild(t);}"
        "t.textContent=m;t.style.display=\u0027block\u0027;"
        "clearTimeout(t._h);"
        "t._h=setTimeout(function(){t.style.display=\u0027none\u0027;},2600);}"
    )
    harness = harness + toast_js

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    data = {'contacts': CONTACTS, 'spaces': SPACES}
    full_js = (harness + inner(reg) + inner(ad) + inner(js)
               + 'const PACKS=' + json.dumps(data, ensure_ascii=False) + ';'
               + 'const MAILSEED=' + json.dumps(MAIL_SEED, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "window.NayaPeople.ensureSeeded(PACKS.contacts);"
               + "try{localStorage.setItem('naya.smartspaces.posts',JSON.stringify(MAILSEED));}catch(e){}"
               + "const spaces=SpacesAdapter.parseSpaces(PACKS.spaces, PACKS.contacts);"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.smartSpaces(el,{spaces:spaces,contacts:PACKS.contacts,me:'naya4',initialSpaceId:'team-naya',"
               + "onCompose:(req)=>{__spToast('In the Hub this opens Smart Mail addressed to '+req.to);}}));"
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
