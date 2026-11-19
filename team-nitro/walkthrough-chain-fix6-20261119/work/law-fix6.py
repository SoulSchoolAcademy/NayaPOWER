#!/usr/bin/env python3
"""FIX6 law check (2026-11-19): base-vs-new with check-design-laws.py's own
rules. Base blobs are the fix5 filed blobs (welcome c66e2fa2 / identity
9e0ed79d / walk ea0b7a92-embed 4b5f9264), fetched via the git blob API and
checked IN MEMORY — no disk writes (EPERM flake live). The walk base is
extracted from the fix5 worker blob (the walk source fetch 404s the same
way the fix5 checker hit it). Also runs the checker CLI on the new
identity + walk files for the canonical counts. Welcome is unchanged;
checked anyway so the delta is proven, not assumed.
"""
import base64, hashlib, importlib.util, json, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
V23 = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114"
WELCOME_LOCAL = V23 + "/welcome-staged.html"
IDENT_LOCAL = V23 + "/identity-fixed.html"
WALK_LOCAL = V23 + "/walk-beginning-fixed.html"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"
BASES = {
    "welcome": "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f",
    "identity": "9e0ed79da9057d878aed198bfa8e971b07e50e92",
    "worker": "ea0b7a92fa78dff3dbe53de0b41bb1d916562735",
}

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)


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


def run(base_bytes, path_new, label):
    base = base_bytes.decode("utf-8", errors="replace")
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


def extract_walk(worker_bytes):
    dec = json.JSONDecoder()
    w = worker_bytes.decode("utf-8")
    i = w.find("const WALK = ")
    assert i >= 0, "worker missing WALK"
    j = w.find('"', i)
    val, _ = dec.raw_decode(w[j:])
    return val.encode("utf-8")


worker5 = gh_blob(BASES["worker"])
walk5 = extract_walk(worker5)
print("fix5 walk embed: %d B sha %s" % (len(walk5), hashlib.sha256(walk5).hexdigest()[:12]), flush=True)
assert hashlib.sha256(walk5).hexdigest().startswith("4b5f9264"), "fix5 walk embed moved"
run(gh_blob(BASES["welcome"]), WELCOME_LOCAL, "welcome")
run(gh_blob(BASES["identity"]), IDENT_LOCAL, "identity")
run(walk5, WALK_LOCAL, "walk")
for label, path in (("welcome", WELCOME_LOCAL), ("identity", IDENT_LOCAL), ("walk", WALK_LOCAL)):
    r = subprocess.run([sys.executable, CHECKER, path], capture_output=True, timeout=300)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    print("CLI %s: rc=%d %s" % (label, r.returncode, out.strip().splitlines()[-3:]))
print("LAW CHECK DONE: zero new violations")
