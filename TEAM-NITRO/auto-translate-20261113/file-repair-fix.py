#!/usr/bin/env python3
"""File the Auto-Translate Repair Fix branch as ONE commit via gh-direct.py.

One API write at a time: a blob per file, then one tree, one commit, one
ref-create (POST — the branch is new; PATCH force if it already exists).
The new commit's parent is the third-surface tip
a87575bbc13588fa7d9eb1c72591451920b6dff2, so the branch ends with exactly
one commit on top of the round. Base tree is fetched LIVE from that
commit (never hardcoded).

The built page never touches disk: the build runs twice — once up front
(to verify the bytes and the expected blob sha) and once inside the blob
step (stdout piped straight into the base64 encoder via process
substitution). The build reads its base from the literal TIP (the tip
blob fetched from GitHub in memory, sha asserted before any edit) —
the local worktree file is 0 bytes (EPERM flake damage) and is NOT
used as the base. Small JSON bodies (tree/commit/ref) pass as raw argv
strings to gh-direct.py (it takes a raw body arg); only the page blob
uses a shell with @<(...). No /tmp files anywhere (EPERM flake).

Usage: file-repair-fix.py
Prints the new commit sha. Verifies the ref afterwards."""
import hashlib, json, re, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
WORK = "/home/hatch/workspace/team-nitro/auto-translate-20261113"
PARENT = "a87575bbc13588fa7d9eb1c72591451920b6dff2"
BRANCH = "personal/auto-translate-repair-fix-20261113"
EXPECTED_PAGE_BLOB = "20afd32c41fb2975adb23888f65bffa54e1d7bd1"
EXPECTED_PAGE_SHA256 = "b98d2f5c9545c14735f450cbeecbd0ebf4670ca7b1ee12e2b488587f1715f51a"

MESSAGE = ("Auto-translate repair fix: the ten English fixed labels the "
           "checker caught (F1-F10) closed — Dashboard heading, Tacho "
           "captions, Links empty state, week-bars notes, funnel, old "
           "+ menu, avatar button, Video/Voice note bake, wall title, "
           "breakdown toggle. Dictionary 791 -> 807 keys/language; "
           "631 mwTr guard sites; 36/36 script blocks parse. Staged only.")

DISK_FILES = [
    ("TEAM-NITRO/auto-translate-20261113/RECORD-AUTO-TRANSLATE-REPAIR-FIX-20261113.md",
     WORK + "/RECORD-AUTO-TRANSLATE-REPAIR-FIX-20261113.md"),
    ("TEAM-NITRO/auto-translate-20261113/SCORECARD-AUTO-TRANSLATE-REPAIR-FIX-20261113.md",
     WORK + "/SCORECARD-AUTO-TRANSLATE-REPAIR-FIX-20261113.md"),
    ("TEAM-NITRO/auto-translate-20261113/apply-repair-dict.py",
     WORK + "/apply-repair-dict.py"),
    ("TEAM-NITRO/auto-translate-20261113/build-repair.py",
     WORK + "/build-repair.py"),
    ("TEAM-NITRO/auto-translate-20261113/locate-repair-sites.py",
     WORK + "/locate-repair-sites.py"),
    ("TEAM-NITRO/auto-translate-20261113/check-repair-keys.py",
     WORK + "/check-repair-keys.py"),
    ("TEAM-NITRO/auto-translate-20261113/diff-repair.py",
     WORK + "/diff-repair.py"),
    ("TEAM-NITRO/auto-translate-20261113/file-repair-fix.py",
     WORK + "/file-repair-fix.py"),
]
PAGE_REPO = "TEAM-NITRO/personal-page-complete-20261113/personal-complete.html"


def gh(method, path, body=None):
    cmd = ["python3", GH, method, "/repos/%s%s" % (REPO, path)]
    if body is not None:
        cmd.append(body)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    out = r.stdout or ""
    m = re.search(r"\{.*\}", out, re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("gh %s %s failed rc=%d out=%s err=%s" % (
            method, path, r.returncode, out[:500], r.stderr[:300]))
    return json.loads(m.group(0))


def run_build():
    """Run the build once, return (built_bytes, stderr). Abort unless OK."""
    r = subprocess.run(
        ["python3", WORK + "/build-repair.py", "TIP"],
        capture_output=True, timeout=180)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0 or "OK sha256=" not in err:
        raise RuntimeError("build failed rc=%d err=%s" % (r.returncode, err[:800]))
    return r.stdout, err


def blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def blob_for_page():
    """Blob the built page: build stdout piped to the base64 encoder."""
    gen = ("python3 %s/build-repair.py TIP 2>/dev/null | python3 -c "
           "\"import sys,base64,json; print(json.dumps({'content': "
           "base64.b64encode(sys.stdin.buffer.read()).decode(), "
           "'encoding': 'base64'}))\"" % WORK)
    cmd = "python3 %s POST /repos/%s/git/blobs @<( %s )" % (GH, REPO, gen)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       executable="/bin/bash", timeout=180)
    m = re.search(r"\{.*\}", r.stdout or "", re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("page blob failed rc=%d out=%s err=%s" % (
            r.returncode, (r.stdout or "")[:400], (r.stderr or "")[:300]))
    sha = json.loads(m.group(0))["sha"]
    if sha != EXPECTED_PAGE_BLOB:
        raise RuntimeError("page blob sha mismatch: got %s expected %s" % (
            sha, EXPECTED_PAGE_BLOB))
    return sha


def blob_for(local):
    gen = ("python3 -c \"import base64,json; d=open(%r,'rb').read(); "
           "print(json.dumps({'content':base64.b64encode(d).decode(),'encoding':'base64'}))\"" % local)
    cmd = "python3 %s POST /repos/%s/git/blobs @<( %s )" % (GH, REPO, gen)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       executable="/bin/bash", timeout=180)
    m = re.search(r"\{.*\}", r.stdout or "", re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("blob %s failed rc=%d out=%s err=%s" % (
            local, r.returncode, (r.stdout or "")[:400], (r.stderr or "")[:300]))
    return json.loads(m.group(0))["sha"]


def main():
    built, err = run_build()
    sha256 = hashlib.sha256(built).hexdigest()
    if sha256 != EXPECTED_PAGE_SHA256:
        raise RuntimeError("built sha256 mismatch: got %s expected %s" % (
            sha256, EXPECTED_PAGE_SHA256))
    if blob_sha(built) != EXPECTED_PAGE_BLOB:
        raise RuntimeError("built blob sha mismatch")
    print("build verified: sha256=%s bytes=%d" % (sha256, len(built)), flush=True)
    print(err.strip().split("\n")[0], flush=True)

    parent = gh("GET", "/git/commits/" + PARENT)
    base_tree = parent["tree"]["sha"]
    print("parent tree", base_tree, flush=True)

    entries = []
    page_sha = blob_for_page()
    print("blob %-70s %s" % (PAGE_REPO, page_sha), flush=True)
    entries.append({"path": PAGE_REPO, "mode": "100644",
                    "type": "blob", "sha": page_sha})
    for repo_path, local in DISK_FILES:
        sha = blob_for(local)
        print("blob %-70s %s" % (repo_path, sha), flush=True)
        entries.append({"path": repo_path, "mode": "100644",
                        "type": "blob", "sha": sha})

    tree = gh("POST", "/git/trees",
              json.dumps({"base_tree": base_tree, "tree": entries}))
    print("tree", tree["sha"], flush=True)
    commit = gh("POST", "/git/commits", json.dumps({
        "message": MESSAGE, "tree": tree["sha"], "parents": [PARENT]}))
    print("commit", commit["sha"], flush=True)
    try:
        ref = gh("POST", "/git/refs", json.dumps({
            "ref": "refs/heads/" + BRANCH, "sha": commit["sha"]}))
    except RuntimeError:
        ref = gh("PATCH", "/git/refs/heads/" + BRANCH, json.dumps({
            "sha": commit["sha"], "force": True}))
    print("ref", json.dumps(ref.get("object", ref))[:300], flush=True)
    check = gh("GET", "/git/refs/heads/" + BRANCH)
    assert check["object"]["sha"] == commit["sha"], "ref verify failed"
    print("ref verified at", commit["sha"], flush=True)
    print("NEW_COMMIT", commit["sha"])


if __name__ == "__main__":
    main()
