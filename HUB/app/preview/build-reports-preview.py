#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ~/workspace/your_files/reports-preview.html from the current HUB room
sources plus the canonical daily reports on this branch's main.

Usage: python3 HUB/app/preview/build-reports-preview.py [--main]
  --main  read reports from origin/main instead of the working tree
"""
import json, subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # HUB/app
REPO = os.path.dirname(os.path.dirname(os.path.dirname(ROOT)))  # repo root... (HUB/app -> repo)
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAYS = ['09/27', '09/28', '09/29', '09/30', '10/01', '10/02']

def report_md(day, use_main):
    base = 'BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/' + day
    if use_main:
        names = subprocess.run(
            ['git', '-C', REPO, 'ls-tree', '--name-only', 'origin/main', base],
            capture_output=True, text=True).stdout.split()
        if not names:
            raise SystemExit('no report on origin/main for ' + day)
        name = sorted(n for n in names if n.endswith('.md'))[0]
        out = subprocess.run(
            ['git', '-C', REPO, 'show', 'origin/main:%s/%s' % (base, name)],
            capture_output=True, text=True)
        return out.stdout
    entries = sorted(f for f in os.listdir(os.path.join(REPO, base)) if f.endswith('.md'))
    with open(os.path.join(REPO, base, entries[0]), encoding='utf-8') as f:
        return f.read()

def main():
    use_main = '--main' in sys.argv
    mds = [report_md(d, use_main) for d in DAYS]
    css = open(os.path.join(REPO, 'HUB/app/css/reports.css'), encoding='utf-8').read()
    ad = open(os.path.join(REPO, 'HUB/app/js/rooms/reports-adapter.js'), encoding='utf-8').read()
    js = open(os.path.join(REPO, 'HUB/app/js/rooms/reports.js'), encoding='utf-8').read()
    harness = ("function el(tag,cls,text){const e=document.createElement(tag);"
               "if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;"
               "return e;}window.NayaRooms=window.NayaRooms||{};"
               "window.ReportsAdapter=window.ReportsAdapter||{};")

    def inner(s):
        a = s.find('(function(){')
        b = s.rfind('})();')
        assert a != -1 and b != -1, 'IIFE wrapper missing'
        return s[a + len('(function(){'):b]

    full_js = (harness + inner(ad) + inner(js)
               + 'const RAW_MD=' + json.dumps(mds) + ';'
               + "document.addEventListener('DOMContentLoaded',()=>{"
               + "const reps=RAW_MD.map(md=>ReportsAdapter.parse(md));"
               + "const root=document.getElementById('app');"
               + "root.appendChild(window.NayaRooms.reports(el,{reports:reps}));"
               + "});")
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Reports — Room Two Preview</title>'
            '<style>body{margin:0;background:#020204;}' + css + '</style></head>'
            '<body><div id="app"></div><script>' + full_js + '</script></body></html>')
    out = os.path.expanduser('~/workspace/your_files/reports-preview.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', out, len(html), 'bytes,', len(mds), 'reports')

if __name__ == '__main__':
    main()
