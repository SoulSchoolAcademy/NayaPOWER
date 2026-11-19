#!/usr/bin/env python3
"""FIX9 law check (2026-11-19): base-vs-new with check-design-laws.py's own
rules. Base blobs are the fix-8 filed blobs (welcome ca0a4093 / identity
7920438e / walk 7b8fe1bf / unfold de7970d2), fetched via the git blob API
and checked IN MEMORY — no disk writes (EPERM flake live). The new unfold
+ new welcome come from their FILED fix-9 blobs (the local worker file
holds the fix-9 worker after the build, so the transform's base
extraction no longer applies — the filed blob is the truth). The new
worker is rebuilt in memory via build-fix9.py and its sha asserted.
Also runs the checker CLI on the new identity + walk + welcome files
for the canonical counts. Identity / walk / welcome are unchanged;
checked anyway so the delta is proven, not assumed. Usage:
python3 law-fix9.py <worker_sha> <unfold_blob> <welcome_blob>
"""
import base64, hashlib, importlib.util, json, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
V23 = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114"
WELCOME_LOCAL = V23 + "/welcome-staged.html"
IDENT_LOCAL = V23 + "/identity-fixed.html"
WALK_LOCAL = V23 + "/walk-beginning-fixed.html"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"
WORK9 = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work"
BASES = {
    "welcome": "ca0a4093c95b3d567d31ba56b81252dd13dc12cc",
    "identity": "7920438ed488869f29d520fd8dcd590061cb6586",
    "walk": "7b8fe1bfbfe7d821c6e268890c682080421ff920",
    "unfold": "de7970d2c6cf577ca64b9404aff332031b953bfd",
}
UNFOLD_SHA = "ab8da1faf825d9d24e3f4991063e81c052738502063d9e89f4479730fa94348f"
WELCOME_SHA = "2062739ecb968b78cd823440bcfd4bbb8f7d0190d3bb2e5443ab3b35c0081955"
WORKER_SHA = sys.argv[1]
UNFOLD_BLOB = sys.argv[2]
WELCOME_BLOB = sys.argv[3]

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)
spec9 = importlib.util.spec_from_file_location("build_fix9", WORK9 + "/build-fix9.py")
bf = importlib.util.module_from_spec(spec9)
spec9.loader.exec_module(bf)


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
# The transform extracts its fix-8 base from the LOCAL worker file, so the
# fix-8 worker must be in place before the pipeline runs (the build/stage
# leave the fix-9 worker there). Restore it from its filed blob when
# needed — the filed blob is the truth, the local copy is the working copy.
WORKER8_SHA = "8dc01221e8c3e08266c4c70f3d584511009f8d106a589172a2b74a6602fbba70"
WORKER8_BLOB = "ea1b89c8d1fc82bc30dc4431b6dad2f252c54c02"
WORKER_LOCAL = V23 + "/walk-beginning-staging-worker.js"
WRITER9 = WORK9 + "/writer9.js"
if hashlib.sha256(read_bytes(WORKER_LOCAL)).hexdigest() != WORKER8_SHA:
    w8 = gh_blob(WORKER8_BLOB)
    assert hashlib.sha256(w8).hexdigest() == WORKER8_SHA, "fix-8 worker blob moved"
    r = subprocess.run(["node", WRITER9, WORKER_LOCAL, "40"],
                       input=w8, capture_output=True, timeout=300)
    assert r.returncode == 0, "fix-8 worker restore failed: %s" % r.stderr.decode("utf-8", "replace")[-400:]
    assert hashlib.sha256(read_bytes(WORKER_LOCAL)).hexdigest() == WORKER8_SHA, "fix-8 worker restore mismatch"
    print("local worker restored to fix-8 for the pipeline", flush=True)
worker = bf.run_builder9(new_welcome, WELCOME_SHA, bf.IDENT_SHA, UNFOLD_SHA, new_unfold)
print("worker rebuilt: %d B sha %s" % (len(worker), hashlib.sha256(worker).hexdigest()[:12]), flush=True)
assert hashlib.sha256(worker).hexdigest() == WORKER_SHA, "worker sha moved"
assert b"fpFrame9" in worker, "worker missing the FIX9 frame marker"
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
