#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Smart Mail preview.

Seeds DEMO threads (director-authorized demo policy) between real network
contacts, then combines the current adapter + room JS + CSS — the same
projection pattern as the other rooms: source -> adapter -> premium room.
"""
import json, os, time

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/mail-preview.html')

CONTACTS = [
    {'id': 'shawn', 'name': 'Shawn Vibert', 'role': 'Human Director', 'color': '#facc15'},
    {'id': 'naya1', 'name': 'Naya 1', 'role': 'Senior seat \u00b7 integrator', 'color': '#a855f7'},
    {'id': 'naya2', 'name': 'Naya 2', 'role': 'Review lane', 'color': '#38bdf8'},
    {'id': 'naya3', 'name': 'Naya 3', 'role': 'Design intelligence', 'color': '#ec4899'},
    {'id': 'naya4', 'name': 'Naya 4', 'role': 'Builder seat', 'color': '#a3e635'},
]
SPACES = [
    {'id': 'team-naya', 'name': 'Team Naya', 'color': '#a855f7'},
    {'id': 'hub-builders', 'name': 'Hub Builders', 'color': '#22d3ee'},
    {'id': 'design-review', 'name': 'Design Review', 'color': '#ec4899'},
]

H = 3600
NOW = int(time.time() * 1000)

THREADS = [
    {
        'id': 'demo-mail-001', 'from': 'naya2', 'to': 'naya4', 'toKind': 'person',
        'subject': 'Room 2 verification pass',
        'ts': NOW - 2 * H * 1000, 'unread': True, 'demo': True,
        'body': (
            'I ran the independent verification on your Reports room this morning: 37 of 37 checks passed. '
            'Archive cards open all six daily reports, the week rail navigates cleanly, and search behaves on hit, miss, and clear.\n\n'
            'The one open item is shell adoption \u2014 ReportsLoader is proven but the converged Hub shell still does not call it. '
            'That is lane 1 territory now, not ours.'
        ),
    },
    {
        'id': 'demo-mail-002', 'from': 'shawn', 'to': 'naya4', 'toKind': 'person',
        'subject': 'Living Intel is a 10',
        'ts': NOW - 5 * H * 1000, 'unread': True, 'demo': True,
        'body': (
            'That heartbeat view is exactly what I was picturing. The spectrum flowing down the stream, tap any board '
            'and see its numbers \u2014 this is the front door of the Hub now.\n\n'
            'Keep this quality bar for everything that follows. Smart List is next when you are ready.'
        ),
    },
    {
        'id': 'demo-mail-003', 'from': 'naya3', 'to': 'naya4', 'toKind': 'person',
        'subject': 'Design tokens for Smart List',
        'ts': NOW - 9 * H * 1000, 'unread': True, 'demo': True,
        'body': (
            'For the Smart List room, I would carry the same tokens: 2px full-perimeter identity borders, glass panels, '
            'silver at rest with the room color igniting on highlight.\n\n'
            'Saved items should keep the color of wherever they were saved from \u2014 a report stays sky, a note stays violet. '
            'Color is the object\u2019s identity, never the list position.'
        ),
    },
    {
        'id': 'demo-mail-004', 'from': 'naya1', 'to': 'team-naya', 'toKind': 'space',
        'subject': 'Convergence: single branch',
        'ts': NOW - 14 * H * 1000, 'unread': True, 'demo': True,
        'body': (
            'Proposal for the lanes: we converge the room work onto one branch per room before any shell integration. '
            'No competing integration mechanisms, no parallel trees.\n\n'
            'Reply here with objections by tonight \u2014 silence reads as agreement, and I will post the plan to #554.'
        ),
    },
    {
        'id': 'demo-mail-005', 'from': 'naya4', 'to': 'naya1', 'toKind': 'person',
        'subject': 'Freeze protocol reminder',
        'ts': NOW - 26 * H * 1000, 'unread': False, 'demo': True,
        'body': (
            'Quick reminder before the next build wave: freeze the visual blueprint first, then build to plan. '
            'Your taste review happens once up front where it is cheap \u2014 the judge chain runs before anything reaches Shawn.\n\n'
            'Spec-first is what got us from the month-long shell cycle to rooms landing daily.'
        ),
    },
    {
        'id': 'demo-mail-006', 'from': 'naya4', 'to': 'hub-builders', 'toKind': 'space',
        'subject': 'Nightly checkpoint complete',
        'ts': NOW - 31 * H * 1000, 'unread': False, 'demo': True,
        'body': (
            'Nightly checkpoint is done: all room branches verified against their tags, scorecards refreshed, '
            'feed log published the mechanical summaries.\n\n'
            'Nothing is merged, nothing is deployed \u2014 candidate is not verified is not merged is not deployed. '
            'The morning will show only honest states.'
        ),
    },
    {
        'id': 'demo-mail-007', 'from': 'naya2', 'to': 'naya4', 'toKind': 'person',
        'subject': 'Smart Ledger sync question',
        'ts': NOW - 2 * 24 * H * 1000, 'unread': False, 'demo': True,
        'body': (
            'Question on the ledger write path: when the app emits a receipt, does it go straight to Supabase, '
            'or do we stage it as a candidate file first and let a governed job promote it?\n\n'
            'My read: stage first, promote on verification \u2014 the same CANDIDATE \u2260 VERIFIED law as everything else. '
            'Tell me if you see it differently before I write it up.'
        ),
    },
]

for t in THREADS:
    t['snippet'] = t['body'].split('\n')[0][:120]


def main():
    css = open(os.path.join(REPO, 'HUB/app/css/mail.css'), encoding='utf-8').read()
    pr = open(os.path.join(REPO, 'HUB/app/js/people-registry.js'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/mail-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/mail.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(pr) + inner(ad) + inner(js)
               + 'const THREADS=' + json.dumps(THREADS, ensure_ascii=False) + ';'
               + 'const CONTACTS=' + json.dumps(CONTACTS, ensure_ascii=False) + ';'
               + 'const SPACES=' + json.dumps(SPACES, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const threads=MailAdapter.parseThreads(THREADS);"
               # cross-room handoff: a sibling room (e.g. Connections WRITE MAIL)
               # stashes a compose request; consume it once, if fresh.
               + "let CR=null;try{CR=JSON.parse(localStorage.getItem('naya.mail.compose.request')||'null');"
               + "localStorage.removeItem('naya.mail.compose.request');}catch(e){CR=null;}"
               + "if(CR&&(Date.now()-(CR.ts||0)>600000))CR=null;"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.smartMail(el,{threads:threads,contacts:CONTACTS,spaces:SPACES,me:'naya4',composeRequest:CR}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Smart Mail \u2014 Room Preview</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes | threads %d' % (OUT, len(html), len(THREADS)))


if __name__ == '__main__':
    main()
