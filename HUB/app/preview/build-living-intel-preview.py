#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Living Intel preview — the heartbeat of it all.

Bakes real canonical data (intelligence reports, smart notes, door registry)
and combines it with the ledger demo stream (labeled DEMO) through
LivingIntelAdapter into one living stream.
"""
import json, os, re, glob

REPO = os.path.expanduser('~/workspace/nayapower-room02')
OUT = os.path.expanduser('~/workspace/your_files/living-intel-preview.html')

DOOR_STYLE = {  # stable identity color + jewel per door (director palette)
    'GitHub Connect':          ('#a371f7', '\u25c6'),
    'MCP Connect':             ('#6366f1', '\u25c8'),
    'AI Connect':              ('#2f7bff', '\u25c9'),
    'Supabase / Data Connect': ('#22d3ee', '\u25cf'),
    'Email Connect':           ('#a3e635', '\u25b2'),
    'Calendar Connect':        ('#facc15', '\u25a0'),
    'Voice Connect':           ('#d4a017', '\u2b1f'),
    'Web Connect':             ('#fb923c', '\u2736'),
    'Naya-to-Naya Connect':    ('#ef4444', '\u2726'),
}

def reports():
    out = []
    for f in sorted(glob.glob(os.path.join(REPO,
            'BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/*/*/IB-DIR-*.md'))):
        s = open(f, encoding='utf-8').read()
        m = re.search(r'ONE THING TO REMEMBER\s*\n+(.+?)(?=\n#{1,3}\s|\Z)', s, re.S)
        d = re.search(r'(2026-\d{2}-\d{2})', f.replace(os.sep, '-'))
        nutshell = ''
        if m:
            nutshell = re.sub(r'\s+', ' ',
                re.sub(r'[*_`>#\U0001f9e0\U0001f4e1\U0001f441\ufe0f]', '', m.group(1)).strip())[:240]
        sections = len(re.findall(r'^#{1,3}\s+', s, re.M))
        words = len(re.findall(r'\S+', s))
        out.append({'date': d.group(1) if d else '', 'nutshell': nutshell,
                    'sections': sections, 'words': words})
    return out

def notes():
    out = []
    for f in sorted(glob.glob(os.path.join(REPO,
            'BRAIN/05-MEMORY/SMART-NOTES/2026/*/*/*/*/*/*/IB-SMART-NOTE*.md')))[-8:]:
        s = open(f, encoding='utf-8').read()
        m = re.search(r'IN A NUTSHELL\s*\n+(.+?)(?=\n#|\n\*\*[A-Z ]+\*\*\s*\n)', s, re.S)
        t = re.search(r'^#\s+(.+)$', s, re.M)
        d = re.search(r'(2026)/(\d{2})/(\d{2})', f)
        tr = re.search(r'\*\*Truth state:\*\*\s*([^\n]+)', s)
        title = t.group(1).strip()[:70] if t else os.path.basename(f)[:50]
        title = re.sub(r'^[#\s\W]+', '', title)
        out.append({
            'date': '%s-%s-%s' % d.groups() if d else '',
            'title': title,
            'nutshell': re.sub(r'\s+', ' ', m.group(1).strip())[:220] if m else '',
            'truth': tr.group(1).strip()[:20] if tr else 'CANDIDATE',
            'words': len(re.findall(r'\S+', s)),
        })
    return out

def doors():
    r = json.load(open(os.path.join(REPO,
        'BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json'), encoding='utf-8'))
    ds = r['doors'] if isinstance(r, dict) and 'doors' in r else r
    out = []
    for d in ds:
        name = d.get('name') or d.get('display_name') or d.get('id')
        color, jewel = DOOR_STYLE.get(name, ('#6366f1', '\u25c9'))
        out.append({'name': name, 'status': d.get('status', ''),
                    'color': color, 'jewel': jewel,
                    'capabilities': d.get('capabilities', []) or []})
    return out

def real_receipts():
    out = []
    for f in sorted(glob.glob(os.path.join(
            os.path.expanduser('~/workspace/demo-staging/receipts'), '*.json'))):
        try:
            out.append(json.load(open(f, encoding='utf-8')))
        except Exception:
            pass
    return out

def main():
    css = open(os.path.join(REPO, 'HUB/app/css/living-intel.css'), encoding='utf-8').read()
    la = open(os.path.join(REPO, 'HUB/app/js/rooms/ledger-adapter.js'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/living-intel-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/living-intel.js'), encoding='utf-8').read()

    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    data = {'reports': reports(), 'notes': notes(), 'doors': doors(),
            'realReceipts': real_receipts()}
    full_js = (harness + inner(la) + inner(ad) + inner(js)
               + 'const PACKS=' + json.dumps(data, ensure_ascii=False) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const items=LivingIntelAdapter.build({reports:PACKS.reports,notes:PACKS.notes,"
               + "doors:PACKS.doors,ledger:LedgerAdapter.demoStream(),"
               + "ledgerReal:LedgerAdapter.parseMany(PACKS.realReceipts)});"
               + "document.getElementById('app').appendChild("
               + "window.NayaRooms.livingIntel(el,{items:items,simLive:true}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Living Intel \u2014 the heartbeat of it all</title>'
            '<style>body{margin:0;background:#020202;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote %s %d bytes | reports %d notes %d doors %d' % (
        OUT, len(html), len(data['reports']), len(data['notes']), len(data['doors'])))

if __name__ == '__main__':
    main()
