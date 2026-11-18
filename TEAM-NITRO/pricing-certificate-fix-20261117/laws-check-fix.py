#!/usr/bin/env python3
"""Design-laws machine check for the Pricing Certificate Fix, in memory.
Runs check-design-laws.py's EXACT regexes over the BASE bytes (the
certificate-current tip, reproduced in memory) and the NEW bytes (fetched
live from staging, sha-verified), then diffs the FAIL sets: zero NEW real
fails is the bar. A FAIL in both is inherited; a FAIL only in NEW is named
and judged in the maker report. Mirrors laws-check-new.py.
"""
import hashlib
import importlib.util
import os
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


laws = load("laws", "/home/hatch/workspace/team-nitro/check-design-laws.py")
bf = load("buildfix", os.path.join(FIXDIR, "build-fix.py"))
_cur = bf._cur
_sim = bf._sim

WANT = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"

walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
h = _cur.harvest_identity()
base = _cur.apply_certificate(entry_pf, h)
assert sha(base) == bf.BASE_ENTRY_SHA, "base tip NOT reproduced — STOP"
new_mem = bf.apply_fix(base, h)
assert sha(new_mem) == WANT, "re-derived new entry != staged — STOP"

st, _, got = _sim.http_get(
    "https://naya-pricing-free-staging.nayapower.workers.dev/free")
assert st == 200
new = got.decode("utf-8")
assert hashlib.sha256(new.encode()).hexdigest() == WANT, "staged /free moved"
assert new == new_mem, "live staged bytes != re-derived bytes — STOP"
print(f"base {len(base.encode())} B, new {len(new.encode())} B (sha MATCH)")


def run(text, label):
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in laws.GRAY_RES:
            if rx.search(line):
                fails.append(f'{label}:{i}: GRAY: {line.strip()[:120]}')
                break
    for m in laws.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            line_no = text[:m.start()].count('\n') + 1
            fails.append(f'{label}:{line_no}: SIZE below 17px: {m.group(0)}')
    for m in laws.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith('var('):
            continue
        val = val.split()[0].rstrip(';')
        if val in laws.FORBIDDEN_TEXT:
            line_no = text[:m.start()].count('\n') + 1
            fails.append(f'{label}:{line_no}: TEXT-COLOR forbidden: {m.group(0).strip()[:120]}')
        elif val not in laws.ALLOWED_TEXT and not val.startswith('#'):
            line_no = text[:m.start()].count('\n') + 1
            warns.append(f'{label}:{line_no}: TEXT-COLOR? check by eye: {m.group(0).strip()[:120]}')
    if ':hover' not in text:
        warns.append(f'{label}: NO-HOVER')
    return fails, warns


bfails, bwarns = run(base, "BASE")
nfails, nwarns = run(new, "NEW")
print(f"\nBASE: {len(bfails)} FAILs, {len(bwarns)} WARNs")
for f in bfails:
    print("  FAIL", f)
for w in bwarns:
    print("  WARN", w)
print(f"\nNEW: {len(nfails)} FAILs, {len(nwarns)} WARNs")
for f in nfails:
    print("  FAIL", f)
for w in nwarns:
    print("  WARN", w)


def key(f):
    return f.split(": ", 1)[1] if ": " in f else f


bkeys = {key(f) for f in bfails}
nkeys = {key(f) for f in nfails}
print("\nINHERITED (in both):", len(bkeys & nkeys))
print("NEW-ONLY FAILs:", len(nkeys - bkeys))
for f in sorted(nkeys - bkeys):
    print("  NEW-ONLY:", f)
print("FIXED (base-only):", len(bkeys - nkeys))
for f in sorted(bkeys - nkeys):
    print("  FIXED:", f)
print("\nNEW-ONLY WARNs:", len({key(w) for w in nwarns} - {key(w) for w in bwarns}))
for w in sorted({key(w) for w in nwarns} - {key(w) for w in bwarns}):
    print("  NEW-ONLY WARN:", w)
