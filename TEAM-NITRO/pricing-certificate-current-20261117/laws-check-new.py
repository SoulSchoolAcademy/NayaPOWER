#!/usr/bin/env python3
"""Design-laws machine check, in memory (the EPERM flake blocks file
writes, so the new bytes are checked as a fetched string, not a file).
Runs check-design-laws.py's EXACT regexes over the BASE bytes (read from
disk) and the NEW bytes (fetched live from staging, sha-verified), then
diffs the FAIL sets: zero NEW fails is the bar. A FAIL that appears in
both is inherited; a FAIL only in NEW is named and judged in the report.
"""
import hashlib
import importlib.util
import os
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

spec = importlib.util.spec_from_file_location(
    "laws", "/home/hatch/workspace/team-nitro/check-design-laws.py")
laws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(laws)

spec2 = importlib.util.spec_from_file_location(
    "btaken", "/home/hatch/workspace/team-nitro/pricing-taken-state-fix-20261117/build-taken-fix.py")
_bt = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(_bt)
_sim = _bt._sim

WANT = "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"
BASE_PATH = "/home/hatch/workspace/team-nitro/pricing-fix-20261117/fixed-entry.html"


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


base = open(BASE_PATH, encoding="utf-8", errors="ignore").read()
st, _, got = _sim.http_get(
    "https://naya-pricing-free-staging.nayapower.workers.dev/free")
assert st == 200
new = got.decode("utf-8")
assert hashlib.sha256(new.encode()).hexdigest() == WANT, "staged /free moved"
print(f"base {len(base.encode())} B, new {len(new.encode())} B (sha MATCH)")

bf, bw = run(base, "BASE")
nf, nw = run(new, "NEW")
print(f"\nBASE: {len(bf)} FAILs, {len(bw)} WARNs")
for f in bf:
    print("  FAIL", f)
for w in bw:
    print("  WARN", w)
print(f"\nNEW: {len(nf)} FAILs, {len(nw)} WARNs")
for f in nf:
    print("  FAIL", f)
for w in nw:
    print("  WARN", w)


def key(f):
    return f.split(": ", 1)[1] if ": " in f else f


bkeys = {key(f) for f in bf}
nkeys = {key(f) for f in nf}
print("\nINHERITED (in both):", len(bkeys & nkeys))
print("NEW-ONLY FAILs:", len(nkeys - bkeys))
for f in sorted(nkeys - bkeys):
    print("  NEW-ONLY:", f)
print("FIXED (base-only):", len(bkeys - nkeys))
for f in sorted(bkeys - nkeys):
    print("  FIXED:", f)
