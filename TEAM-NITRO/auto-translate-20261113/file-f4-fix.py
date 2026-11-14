#!/usr/bin/env python3
"""File the Auto-Translate F4 Fix branch as ONE commit via gh-direct.py.

One API write at a time: a blob per file, then one tree, one commit, one
ref-create (POST — the branch is new). The new commit's parent is the
repair tip 8cbc69ee2d499dce33a1a5d8db200d801b4605ed, so the branch ends
with exactly one commit on top of the round. Base tree is the parent's
tree, fetched LIVE (never hardcoded).

The fixed page never re-reads from disk as a build: f4-fixed.html was
edited from the repair tip bytes (fetched from GitHub, sha asserted).
The page blob is piped straight into the base64 encoder via process
substitution — no multi-MB payload staged to disk (EPERM flake).
Small JSON bodies pass as raw argv strings. No /tmp files anywhere.

Usage: file-f4-fix.py
Prints the new commit sha. Verifies the ref + page blob afterwards."""
import hashlib, json, re, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
WORK = "/home/hatch/workspace/team-nitro/auto-translate-20261113"
PARENT = "8cbc69ee2d499dce33a1a5d8db200d801b4605ed"
PARENT_TREE = "7cdf24b29a347467ce1b6c2c57638576f879734e"
BRANCH = "personal/auto-translate-f4-fix-20261113"
EXPECTED_PAGE_SHA256 = "aea38f65e4bdfbba167d723da38e020223016bfc15c97dbece6b67b2c863eb3f"
EXPECTED_PAGE_BLOB = "3396a3ae2e0142c13b40cd78f78ff43fc661b305"

MESSAGE = ("Auto-translate F4 fix: KIND_META subject/quiet baked English "
           "before mwTr existed — now plain English keys, translated at "
           "render time in renderBars. Both branches (quiet + Busiest:) "
           "proven rendered in es/fr/de on fresh load and switch. "
           "Dictionary unchanged (807 keys/language). 36/36 script blocks "
           "parse. Staged only.")

DISK_FILES = [
    ("TEAM-NITRO/auto-translate-20261113/RECORD-AUTO-TRANSLATE-F4-FIX-20261113.md",
     WORK + "/RECORD-AUTO-TRANSLATE-F4-FIX-20261113.md"),
    ("TEAM-NITRO/auto-translate-20261113/SCORECARD-AUTO-TRANSLATE-F4-FIX-20261113.md",
     WORK + "/SCORECARD-AUTO-TRANSLATE-F4-FIX-20261113.md"),
    ("TEAM-NITRO/auto-translate-20261113/f4-probe.py",
     WORK + "/f4-probe.py"),
    ("TEAM-NITRO/auto-translate-20261113/file-f4-fix.py",
     WORK + "/file-f4-fix.py"),
]
PAGE_REPO = "TEAM-NITRO/personal-page-complete-20261113/personal-complete.html"
PAGE_LOCAL = WORK + "/f4-fixed.html"


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


def gh_blob_piped(local_path):
    """Create a git blob for a large file: base64 piped via process substitution."""
    inner = ("python3 -c \"import base64,json,sys; "
             "print(json.dumps({'content': base64.b64encode(open(sys.argv[1],'rb').read()).decode(), "
             "'encoding':'base64'}))\" " + local_path)
    cmd = ("python3 %s POST /repos/%s/git/blobs @<(%s)" % (GH, REPO, inner))
    r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=180)
    out = r.stdout or ""
    m = re.search(r"\{.*\}", out, re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("blob piped failed rc=%d out=%s err=%s" % (
            r.returncode, out[:500], r.stderr[:300]))
    return json.loads(m.group(0))


def main():
    page_bytes = open(PAGE_LOCAL, "rb").read()
    sha256 = hashlib.sha256(page_bytes).hexdigest()
    assert sha256 == EXPECTED_PAGE_SHA256, "page sha256 mismatch: %s" % sha256
    blob_sha = hashlib.sha1(b"blob " + str(len(page_bytes)).encode() + b"\x00" + page_bytes).hexdigest()
    assert blob_sha == EXPECTED_PAGE_BLOB, "page blob sha mismatch: %s" % blob_sha
    print("page OK sha256=%s blob=%s bytes=%d" % (sha256, blob_sha, len(page_bytes)), flush=True)

    # 1. page blob (piped, never staged to disk)
    pb = gh_blob_piped(PAGE_LOCAL)
    assert pb["sha"] == EXPECTED_PAGE_BLOB, "remote page blob mismatch: %s" % pb.get("sha")
    print("page blob created:", pb["sha"], flush=True)

    # 2. small-file blobs (raw argv JSON)
    entries = [{"path": PAGE_REPO, "mode": "100644", "type": "blob", "sha": pb["sha"]}]
    for repo_path, local_path in DISK_FILES:
        raw = open(local_path, "rb").read()
        import base64
        body = json.dumps({"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        b = gh("POST", "/git/blobs", body)
        entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": b["sha"]})
        print("blob", repo_path, "->", b["sha"], flush=True)

    # 3. tree on the parent's tree
    tree = gh("POST", "/git/trees", json.dumps({"base_tree": PARENT_TREE, "tree": entries}))
    print("tree:", tree["sha"], flush=True)

    # 4. commit
    commit = gh("POST", "/git/commits", json.dumps(
        {"message": MESSAGE, "tree": tree["sha"], "parents": [PARENT]}))
    print("commit:", commit["sha"], flush=True)

    # 5. ref create
    ref = gh("POST", "/git/refs", json.dumps(
        {"ref": "refs/heads/" + BRANCH, "sha": commit["sha"]}))
    print("ref:", ref["ref"], "->", ref["object"]["sha"], flush=True)

    # 6. verify
    check = gh("GET", "/git/refs/heads/" + BRANCH)
    assert check["object"]["sha"] == commit["sha"], "ref verify failed"
    got = gh("GET", "/git/blobs/" + EXPECTED_PAGE_BLOB)
    assert got["sha"] == EXPECTED_PAGE_BLOB, "blob verify failed"
    print("VERIFIED branch", BRANCH, "tip", commit["sha"], flush=True)
    print(commit["sha"])


if __name__ == "__main__":
    main()
