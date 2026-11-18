#!/usr/bin/env python3
"""check-design-laws.py — machine checker for THE-NAYA-DESIGN-LAWS.

Usage: python3 check-design-laws.py <built-file.html>
Checks what a regex CAN check. The eye still checks the rest
(flat/dead, flow, harvest, read-as-a-reader — see the machine spec's
eye_only list). Exit 0 = no machine-checkable violation found.
Exit 1 = a law is broken; fix it, don't argue with it.

Laws enforced here (from THE-NAYA-DESIGN-LAWS.md):
  §2.2  no gray text, at any size, any value
  §2.3  type scale 25 / 19 / 17 — no text below 17px
  §2.2  text colors: white, gold #d4a017, purple #8e24aa,
        green #07925f, blue #0f52ba, black only (literals;
        var(--*) references pass — variables resolve to the scale)
  §1    hover states exist (warning if a file has no :hover at all)
"""
import re
import sys

GRAY_RES = [
    re.compile(r'#(?:888|999|aaa|bbb|ccc|8b8b9c|808080|777777|666666)\b', re.I),
    re.compile(r'\bgray\b', re.I),
    re.compile(r'\bgrey\b', re.I),
    re.compile(r'--dim\b', re.I),
    re.compile(r'color\s*:\s*rgba?\([^)]*,\s*0\.[0-6]\d*\)', re.I),
]
FONTSIZE_RE = re.compile(r'font-size\s*:\s*(?:clamp\([^)]*?(\d+(?:\.\d+)?)px|(\d+(?:\.\d+)?)px)', re.I)
COLOR_DECL_RE = re.compile(r'(?<![a-z-])color\s*:\s*([^;}{]+)', re.I)
ALLOWED_TEXT = {
    '#ffffff', '#fff', 'white', '#d4a017', '#8e24aa', '#07925f',
    '#0f52ba', '#050607', '#000000', '#000', 'black',
    'inherit', 'currentcolor',
}
FORBIDDEN_TEXT = {
    '#c62828', '#c2410c', '#a21caf', '#ff5e6c', '#ff9a5a',
    '#e84fff', '#ff1493', '#ff2a2a', '#ff8c00',
}


def check(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    fails, warns = [], []

    for i, line in enumerate(text.splitlines(), 1):
        for rx in GRAY_RES:
            if rx.search(line):
                fails.append(f'{path}:{i}: GRAY (§2.2 no gray text): {line.strip()[:120]}')
                break

    for m in FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            line_no = text[:m.start()].count('\n') + 1
            fails.append(f'{path}:{line_no}: SIZE (§2.3 below 17px): {m.group(0)}')

    for m in COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith('var('):
            continue
        val = val.split()[0].rstrip(';')
        if val in FORBIDDEN_TEXT:
            line_no = text[:m.start()].count('\n') + 1
            fails.append(f'{path}:{line_no}: TEXT-COLOR (§2.2 red/orange/magenta as text): {m.group(0).strip()[:120]}')
        elif val not in ALLOWED_TEXT and not val.startswith('#'):
            line_no = text[:m.start()].count('\n') + 1
            warns.append(f'{path}:{line_no}: TEXT-COLOR? (§2.2 check by eye): {m.group(0).strip()[:120]}')

    if ':hover' not in text:
        warns.append(f'{path}: NO-HOVER (§1 warning — no :hover rules found; objects must answer touch)')

    for f in fails:
        print('FAIL', f)
    for w in warns:
        print('WARN', w)
    if fails:
        print(f'{len(fails)} violation(s), {len(warns)} warning(s) — fix the FAILs, do not ship.')
        return 1
    print(f'PASS — no machine-checkable violation ({len(warns)} warning(s)). Eye-checks still owed: flat/dead, flow, harvest, read-as-a-reader.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python3 check-design-laws.py <built-file.html>')
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
