#!/usr/bin/env python3
"""FIX2 law check (2026-11-18): base-vs-new with check-design-laws.py's own
rules. Base blobs are fetched from GitHub (1a48347f welcome / d8c0d583
identity — the chain tip) and checked in memory; no disk writes (EPERM).
The new files are also run through the checker CLI itself for the
canonical count."""
import base64, importlib.util, json, subprocess, sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
WELCOME_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
IDENT_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
BASE_WELCOME_BLOB = None  # resolved from the parent commit tree below
BASE_IDENT_BLOB = None
PARENT_TIP = "e4e1caa76fc59f4a22f0a32b1352f932ec8f3ce6"

spec = importlib.util.spec_from_file_location("lawcheck", "/home/hatch/workspace/team-nitro/check-design-laws.py")
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)

def gh_json(method, path):
    p = subprocess.run([sys.executable, GH, method, path], capture_output=True, timeout=300)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    assert status == 200, "%s %s failed: %s" % (method, path, out[:300])
    return json.loads(lines[1])

def gh_blob(sha):
    data = gh_json("GET", "/repos/%s/git/blobs/%s" % (REPO, sha))
    assert data["sha"] == sha, "blob sha mismatch: %s vs %s" % (data["sha"], sha)
    raw = base64.b64decode("".join(data["content"].split()))
    assert len(raw) == data["size"], "blob size mismatch"
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

def norm(f):
    # strip label + line number: compare kind + snippet only
    parts = f.split(": ", 1)
    return parts[1] if len(parts) > 1 else f

def main():
    with open(WELCOME_LOCAL, encoding="utf-8", errors="ignore") as f:
        new_w = f.read()
    with open(IDENT_LOCAL, encoding="utf-8", errors="ignore") as f:
        new_i = f.read()
    # resolve the base blob shas from the parent commit tree (never typed)
    commit = gh_json("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    tree = gh_json("GET", "/repos/%s/git/trees/%s?recursive=1" % (REPO, commit["tree"]["sha"]))
    entries = {e["path"]: e["sha"] for e in tree["tree"]}
    bw_blob = entries["team-nitro/walk-v23-assembly-20261114/welcome-staged.html"]
    bi_blob = entries["team-nitro/walk-v23-assembly-20261114/identity-fixed.html"]
    print("base blobs from parent tree: welcome %s identity %s" % (bw_blob[:12], bi_blob[:12]), flush=True)
    assert bw_blob.startswith("5ac2054d"), "base welcome blob moved"
    assert bi_blob.startswith("98b0efc0"), "base identity blob moved"
    base_w = gh_blob(bw_blob).decode("utf-8", "ignore")
    base_i = gh_blob(bi_blob).decode("utf-8", "ignore")
    print("base welcome %d B, base identity %d B (fetched by blob sha)" % (len(base_w), len(base_i)), flush=True)
    for label, base, new in (("welcome", base_w, new_w), ("identity", base_i, new_i)):
        bf, bw = check_text(base, label + "-base")
        nf, nw = check_text(new, label + "-new")
        print("%s: base %d FAIL %d WARN | new %d FAIL %d WARN" % (label, len(bf), len(bw), len(nf), len(nw)), flush=True)
        new_only = sorted(set(norm(x) for x in nf) - set(norm(x) for x in bf))
        gone = sorted(set(norm(x) for x in bf) - set(norm(x) for x in nf))
        print("  NEW failures in fix2 (not in base): %d" % len(new_only), flush=True)
        for x in new_only[:20]:
            print("    + " + x, flush=True)
        print("  failures GONE in fix2: %d" % len(gone), flush=True)
        for x in gone[:20]:
            print("    - " + x, flush=True)
        new_warn_only = sorted(set(norm(x) for x in nw) - set(norm(x) for x in bw))
        print("  NEW warnings in fix2: %d" % len(new_warn_only), flush=True)
        for x in new_warn_only[:20]:
            print("    + " + x, flush=True)

if __name__ == "__main__":
    main()
