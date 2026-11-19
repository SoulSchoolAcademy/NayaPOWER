#!/usr/bin/env python3
"""FIX8 law check (2026-11-19): base-vs-new with check-design-laws.py's own
rules. Base blobs are the fix-7 filed blobs (welcome c66e2fa2 / identity
7920438e / walk 7b8fe1bf / unfold b2f04aaa), fetched via the git blob API
and checked IN MEMORY — no disk writes (EPERM flake live). The new unfold
+ new welcome come from their FILED fix-8 blobs (the local worker file
now holds the fix-8 worker, so the transform's base extraction no longer
applies — the filed blob is the truth). The new worker is rebuilt in
memory via build-fix8.py and its sha asserted. Also runs the checker CLI
on the new identity + walk + welcome files for the canonical counts.
Identity / walk are unchanged; checked anyway so the delta is proven,
not assumed. Usage: python3 law-fix8.py <worker_sha> <unfold_blob> <welcome_blob>
"""
import base64, hashlib, importlib.util, json, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
V23 = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114"
WELCOME_LOCAL = V23 + "/welcome-staged.html"
IDENT_LOCAL = V23 + "/identity-fixed.html"
WALK_LOCAL = V23 + "/walk-beginning-fixed.html"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"
WORK8 = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work"
BASES = {
    "welcome": "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f",
    "identity": "7920438ed488869f29d520fd8dcd590061cb6586",
    "walk": "7b8fe1bfbfe7d821c6e268890c682080421ff920",
    "unfold": "b2f04aaad4982bb35a29eb736c9178a444738b99",
}
UNFOLD_SHA = "0a68a2839ab2bebd570a7fee186074d77e3c22afc0e7c412d82508053c5f26dd"
WELCOME_SHA = "2062739ecb968b78cd823440bcfd4bbb8f7d0190d3bb2e5443ab3b35c0081955"
WORKER_SHA = sys.argv[1]
UNFOLD_BLOB = sys.argv[2]
WELCOME_BLOB = sys.argv[3]

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)
spec8 = importlib.util.spec_from_file_location("build_fix8", WORK8 + "/build-fix8.py")
bf = importlib.util.module_from_spec(spec8)
spec8.loader.exec_module(bf)


def gh_blob(sha):
    r = subprocess.run([sys.executable, GH, "GET",
                        "/repos/%s/git/blobs/%s" % (REPO, sha)],
                       capture_output=True, timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    payload = out.split("\n", 1)[1]
    d = json.loads(payload)
    raw = base64.b64decode("".join(d["content"].split()))
    print("blob %s: %d B sha %s" % (sha[:8], len(raw), hashlib.sha256(raw).hexdigest()[:12]), flush=True)
    return raw


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


def run(base_bytes, new_bytes, label):
    base = base_bytes.decode("utf-8", errors="replace")
    new = new_bytes.decode("utf-8", errors="replace")
    bf_, bw = check_text(base, label + "-base")
    nf, nw = check_text(new, label + "-new")
    bset, nset = norm(bf_), norm(nf)
    added = [x for x in nset if x not in bset]
    removed = [x for x in bset if x not in nset]
    print("%s: base %d FAIL / %d WARN -> new %d FAIL / %d WARN" % (label, len(bf_), len(bw), len(nf), len(nw)))
    print("%s: added: %s" % (label, added[:10]))
    print("%s: removed: %s" % (label, removed[:10]))
    assert not added, "%s has NEW law violations: %s" % (label, added[:5])
    return len(bf_), len(nf)


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


new_unfold = gh_blob(UNFOLD_BLOB)
assert hashlib.sha256(new_unfold).hexdigest() == UNFOLD_SHA, "unfold moved"
new_welcome = gh_blob(WELCOME_BLOB)
assert hashlib.sha256(new_welcome).hexdigest() == WELCOME_SHA, "welcome moved"
new_ident = read_bytes(IDENT_LOCAL)
new_walk = read_bytes(WALK_LOCAL)
worker = bf.run_builder8(new_welcome, WELCOME_SHA, bf.IDENT_SHA, UNFOLD_SHA, new_unfold)
print("worker rebuilt: %d B sha %s" % (len(worker), hashlib.sha256(worker).hexdigest()[:12]), flush=True)
assert hashlib.sha256(worker).hexdigest() == WORKER_SHA, "worker sha moved"
assert b"fpFrame8" in worker, "worker missing the FIX8 frame marker"
assert b"stay on the entrance" in worker, "worker missing the F6 marker"
run(gh_blob(BASES["welcome"]), new_welcome, "welcome")
run(gh_blob(BASES["identity"]), new_ident, "identity")
run(gh_blob(BASES["walk"]), new_walk, "walk")
run(gh_blob(BASES["unfold"]), new_unfold, "unfold")
for label, path in (("welcome", WELCOME_LOCAL), ("identity", IDENT_LOCAL), ("walk", WALK_LOCAL)):
    r = subprocess.run([sys.executable, CHECKER, path], capture_output=True, timeout=300)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    print("CLI %s: rc=%d %s" % (label, r.returncode, out.strip().splitlines()[-3:]))
print("LAW CHECK DONE: zero new violations")
