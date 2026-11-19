#!/usr/bin/env python3
"""FIX3 law check (2026-11-19): base-vs-new with check-design-laws.py's own
rules. Base blobs are the fix2 blobs (c8581fca welcome / 803e7ea8 identity),
checked in memory from the already-fetched local copies; no disk writes
(EPERM). Also runs the checker CLI on the new files for the canonical count.
"""
import hashlib, importlib.util, subprocess, sys

BASES = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/bases"
WELCOME_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
IDENT_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)

def check_text(text, label):
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in law.GRAY_RES:
            if rx.search(line):
                fails.append("%s:%d: GRAY: %s" % (label, i, line.strip()[:120]))
                break
    for m in law.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            fails.append("%s:%d: SIZE: %s" % (label, text[:m.start()].count("\n") + 1, m.group(0)))
    for m in law.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith("var("):
            continue
        val = val.split()[0].rstrip(";")
        if val in law.FORBIDDEN_TEXT:
            fails.append("%s:%d: TEXT-COLOR: %s" % (label, text[:m.start()].count("\n") + 1, m.group(0).strip()[:120]))
        elif val not in law.ALLOWED_TEXT and not val.startswith("#"):
            warns.append("%s:%d: TEXT-COLOR?: %s" % (label, text[:m.start()].count("\n") + 1, m.group(0).strip()[:120]))
    if ":hover" not in text:
        warns.append("%s: NO-HOVER" % label)
    return fails, warns

def norm(fails):
    return sorted(f.split(": ", 1)[1] if ": " in f else f for f in fails)

def run(path_base, path_new, label):
    base = open(path_base, encoding="utf-8", errors="replace").read()
    new = open(path_new, encoding="utf-8", errors="replace").read()
    bf, bw = check_text(base, label + "-base")
    nf, nw = check_text(new, label + "-new")
    bset, nset = norm(bf), norm(nf)
    added = [x for x in nset if x not in bset]
    removed = [x for x in bset if x not in nset]
    print("%s: base %d FAIL / %d WARN -> new %d FAIL / %d WARN" % (label, len(bf), len(bw), len(nf), len(nw)))
    print("%s: added: %s" % (label, added[:10]))
    print("%s: removed: %s" % (label, removed[:10]))
    assert not added, "%s has NEW law violations: %s" % (label, added[:5])
    return len(bf), len(nf)

run(BASES + "/welcome-staged.html", WELCOME_LOCAL, "welcome")
run(BASES + "/identity-fixed.html", IDENT_LOCAL, "identity")
# CLI canonical counts on the new files
for label, path in (("welcome", WELCOME_LOCAL), ("identity", IDENT_LOCAL)):
    r = subprocess.run([sys.executable, CHECKER, path], capture_output=True, timeout=300)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    print("CLI %s: rc=%d %s" % (label, r.returncode, out.strip().splitlines()[-3:]))
print("LAW CHECK DONE: zero new violations")
