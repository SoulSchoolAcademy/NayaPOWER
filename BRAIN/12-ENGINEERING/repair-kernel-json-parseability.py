"""Repair pass 1: make the two canonical kernel JSON artifacts parseable.

Both files on main contain a LITERAL backslash-n typed into the text instead of a real
newline, which makes them unparseable by any JSON reader. Because kernel/validator
code paths that read them were silently skipped or short-circuited, the repository
carried a green test suite over corrupt canonical artifacts.

This is a data repair only. It changes no semantics.
"""
import json
from pathlib import Path

TARGETS = [
    'BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json',
    'BRAIN/03-KERNEL/MANIFEST.json',
]

for rel in TARGETS:
    p = Path(rel)
    raw = p.read_text(encoding='utf-8')
    try:
        json.loads(raw)
        print(f'{rel}: already valid, untouched')
        continue
    except Exception as exc:
        print(f'{rel}: BEFORE invalid -> {exc}')
    fixed = raw.replace('\\n', '\n')
    doc = json.loads(fixed)
    p.write_text(fixed, encoding='utf-8')
    print(f'{rel}: AFTER valid, {len(fixed.splitlines())} lines, keys={list(doc.keys())[:5]}')

print()
bad = 0
for f in Path('BRAIN').rglob('*.json'):
    try:
        json.loads(f.read_text(encoding='utf-8'))
    except Exception as exc:
        bad += 1
        print(f'STILL INVALID: {f} -> {exc}')
print(f'BRAIN json files still invalid: {bad}')
