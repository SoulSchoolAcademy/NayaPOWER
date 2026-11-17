#!/usr/bin/env python3
"""In-memory design-law check (2026-11-17 bridge presentation round).

The EPERM flake blocks writing the built files to disk, so the checker
(check-design-laws.py, file-based) cannot run on them directly. This
driver reuses the checker's own compiled regexes/constants and runs the
IDENTICAL checks over the in-memory built text (build scripts run as
subprocesses, stdout captured through a pipe — no disk write anywhere).

Usage: python3 check-in-memory.py
Exit 0 = zero NEW fails on every touched file (base vs new sets equal).
Prints base/new FAIL+WARN counts per file and any new fail lines.
"""
import importlib.util, subprocess, sys

spec = importlib.util.spec_from_file_location(
    'lawcheck', '/home/hatch/workspace/team-nitro/check-design-laws.py')
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)

def check_text(name, text):
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in law.GRAY_RES:
            if rx.search(line):
                fails.append(f'{name}:{i}: GRAY: {line.strip()[:120]}')
                break
    for m in law.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            ln = text[:m.start()].count('\n') + 1
            fails.append(f'{name}:{ln}: SIZE: {m.group(0)}')
    for m in law.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith('var('):
            continue
        val = val.split()[0].rstrip(';')
        if val in law.FORBIDDEN_TEXT:
            ln = text[:m.start()].count('\n') + 1
            fails.append(f'{name}:{ln}: TEXT-COLOR: {m.group(0).strip()[:120]}')
        elif val not in law.ALLOWED_TEXT and not val.startswith('#'):
            ln = text[:m.start()].count('\n') + 1
            warns.append(f'{name}:{ln}: TEXT-COLOR?: {m.group(0).strip()[:120]}')
    if ':hover' not in text:
        warns.append(f'{name}: NO-HOVER')
    return fails, warns

FILES = [
    ('welcome', '/home/hatch/workspace/team-nitro/bridge-page-fix-20261117/welcome-bridge-fix.html',
     '/home/hatch/workspace/team-nitro/bridge-presentation-20261117/build-bridge-presentation.py'),
    ('walk', '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html',
     '/home/hatch/workspace/team-nitro/bridge-presentation-20261117/build-walk-presentation.py'),
    ('identity', '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html',
     '/home/hatch/workspace/team-nitro/bridge-presentation-20261117/build-identity-presentation.py'),
]

overall_new = 0
for name, base_path, build_script in FILES:
    base = open(base_path, encoding='utf-8', errors='ignore').read()
    r = subprocess.run([sys.executable, build_script], capture_output=True)
    assert r.returncode == 0, f'{name}: build failed: {r.stderr.decode()[-500:]}'
    new = r.stdout.decode('utf-8', errors='ignore')
    bf, bw = check_text(name + ' BASE', base)
    nf, nw = check_text(name + ' NEW', new)
    # compare fail BODIES (strip the name prefix) — a fail is NEW if its
    # body is not in the base set.
    def body(f):
        return f.split(': ', 1)[1] if ': ' in f else f
    base_bodies = {body(f) for f in bf}
    new_fails = [f for f in nf if body(f) not in base_bodies]
    print(f'{name}: BASE {len(bf)} FAIL + {len(bw)} WARN  |  NEW {len(nf)} FAIL + {len(nw)} WARN  |  NEW-FAILs: {len(new_fails)}')
    for f in new_fails[:10]:
        print(f'   NEW FAIL: {f}')
    overall_new += len(new_fails)

print(f'TOTAL NEW FAILs: {overall_new}')
sys.exit(1 if overall_new else 0)
