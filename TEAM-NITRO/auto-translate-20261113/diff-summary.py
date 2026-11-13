#!/usr/bin/env python3
"""Summarize base-vs-built diff. Reads BUILT html from stdin.
Usage: build-third-surface.py ... 2>/dev/null | python3 diff-summary.py"""
import sys, difflib

BASE = '/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'

def main():
    new = sys.stdin.read().split('\n')
    base = open(BASE, encoding='utf-8').read().split('\n')
    print(f'base lines {len(base)} -> new lines {len(new)}')
    sm = difflib.SequenceMatcher(a=base, b=new, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            hunks.append((tag, i1, i2, j1, j2))
    print(f'changed hunks: {len(hunks)}')
    changed = sum((i2 - i1) + (j2 - j1) for _, i1, i2, j1, j2 in hunks)
    print(f'changed lines (base+new): {changed}')
    for tag, i1, i2, j1, j2 in hunks:
        if len(sys.argv) > 1 and sys.argv[1] == 'ranges':
            print(f'{tag} base[{i1+1}:{i2}] new[{j1+1}:{j2}]')
            continue
        first = ''
        if tag in ('replace', 'delete'):
            first = 'BASE: ' + base[i1][:110] if i1 < i2 else ''
        if tag in ('replace', 'insert'):
            first += (' | NEW: ' + new[j1][:110]) if j1 < j2 else ''
        print(f'{tag} base[{i1+1}:{i2}] new[{j1+1}:{j2}] {first}')

if __name__ == '__main__':
    main()
