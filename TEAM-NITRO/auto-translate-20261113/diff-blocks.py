#!/usr/bin/env python3
"""Diff script blocks base-vs-built. Reads the BUILT html from stdin.
Usage: build-third-surface.py ... 2>/dev/null | python3 diff-blocks.py [n ...]"""
import sys, re, difflib

BASE = '/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
PAT = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>')

def main():
    new = sys.stdin.read()
    base = open(BASE, encoding='utf-8').read()
    b0, b1 = PAT.findall(base), PAT.findall(new)
    print('blocks base/new:', len(b0), len(b1))
    want = [int(x) for x in sys.argv[1:]] or [8, 9, 28, 29]
    for n in want:
        a, b = b0[n-1].split('\n'), b1[n-1].split('\n')
        print(f'===== block {n}: base lines {len(a)} -> new lines {len(b)} =====')
        for line in difflib.unified_diff(a, b, lineterm='', n=0):
            if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
                print(line[:300])

if __name__ == '__main__':
    main()
