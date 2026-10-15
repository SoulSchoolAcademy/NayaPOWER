#!/usr/bin/env python3
"""Push EVOLVE branch syncs via the GitHub git-data API (git push has no credential helper here).

For each EVOLVE branch whose CI `test` check is red on a stale base:
  blobs (already remote for unchanged files; uploaded for the fixed test) ->
  tree (base_tree = exact main tip merged locally; verify tree SHA == local merge tree SHA) ->
  commit (parents = [remote branch head, main tip]; re-verify tip unmoved at action time) ->
  PATCH git ref. NEVER touches main. Fail closed on any mismatch.
"""
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# t0796 (lane 1, Verity) identity repair: seat-parameterized authorship,
# fail-closed when NAYA_SEAT_NAME/NAYA_SEAT_EMAIL are unset.
sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
from seat_identity import seat_identity

_AUTHOR = None


def author():
    """The executing seat's {"name","email"}, resolved once (t0796)."""
    global _AUTHOR
    if _AUTHOR is None:
        _AUTHOR = seat_identity()
    return _AUTHOR

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = str(Path.home() / "workspace/skills/github/bin/gh-api")
WORK1931 = Path.home() / "workspace/goals/bring-naya-to-life/hidden_files/evolve-driver/work/np1931"

MERGE_MSG = "chore(evolve): sync branch with main to pick up fixed CI test baseline"
FIX_MSG = """fix(evolve): unpin stale-boundary test fixture from fixed calendar date

test_stale_boundary_is_strictly_greater pinned its fixture clock to
2026-10-09T02:45Z. Once real time moved past 2026-10-10, the exact-7-day
SN-EDGE fixture aged to 8 days and the boundary assertion broke — a
calendar time bomb, not a behavior change. NOW is the actual current
UTC time; iso() truncates to the second, so the strictly-greater
boundary stays deterministic on any run date."""

# Per-branch plan. Blob SHAs verified == local `git hash-object` of the exact content merged.
BRANCHES = [
    {
        "ref": "naya4/evolve-receipt-v1",
        "remote_head": "4a0ba75b141dd6b35b9ba4bdec08aa8c4ef246d9",
        "main_tip": "b83f6ded22c5e48018be8e798c4166520a4992cc",
        "main_tree": "31f37fe0c2426de520a348abc8aed279844fa976",
        "commits": [
            {
                "message": MERGE_MSG,
                "parents": ["BRANCH_HEAD", "MAIN_TIP"],
                "files": {
                    "tests/test_evolve_receipt.py": "6008ae1230424d661f0d4dbfe0c937fc97b12f21",
                    "tools/evolve_receipt.py": "742842640da9d184f58d67cf215b4083db62813d",
                },
                "expect_tree": "72f85da3f96c1f1ac0f514898890a5f040bf1b86",
            },
        ],
    },
    {
        "ref": "naya4/evolve-meta-learning-v1",
        "remote_head": "7db909a21887d52748a8d80b753011f6f97e5157",
        "main_tip": "2aa08049892f2479ce5d4297bdc72f14a68da3ec",
        "main_tree": "3beee67a117d591cd011e9661971293ea0dc46ce",
        "commits": [
            {
                "message": MERGE_MSG,
                "parents": ["BRANCH_HEAD", "MAIN_TIP"],
                "files": {
                    "tests/test_evolve_meta_learning.py": "0da82cacb796f6ba1d6f929f74d849bda9556cd3",
                    "tools/evolve_meta_learning.py": "d1fa6a628cc33c378dc8437b8d1bf89d1f1ce908",
                },
                "expect_tree": "b46064af2f23f340ff4d38b8f9e7ab6126ea187b",
            },
            {
                "message": FIX_MSG,
                "parents": ["PREV"],
                "files": {
                    # fixed test content uploaded below; placeholder filled at runtime
                    "tests/test_evolve_meta_learning.py": "UPLOAD",
                },
                "expect_tree": "db3782b5c2949a9390b618e739e5e5aac4be51b6",
                "upload": str(WORK1931 / "tests/test_evolve_meta_learning.py"),
            },
        ],
    },
]


def api(method, path, body=None):
    cmd = [GH, method, f"/repos/{REPO}{path}"]
    tmp = None
    if body is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(body, fh)
            tmp = fh.name
        cmd.append("@" + tmp)
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if tmp:
            Path(tmp).unlink(missing_ok=True)
    if out.returncode != 0:
        raise RuntimeError(f"API {method} {path} failed: {out.stderr[:500]} {out.stdout[:500]}")
    return json.loads(out.stdout)


def ref_sha(branch_ref):
    enc = branch_ref.replace("/", "%2F")
    return api("GET", f"/git/ref/heads/{enc}")["object"]["sha"]


def main():
    for b in BRANCHES:
        print(f"=== {b['ref']} ===", flush=True)
        live = ref_sha(b["ref"])
        if live != b["remote_head"]:
            raise RuntimeError(f"tip moved: {live} != {b['remote_head']} — refusing (SN-0493)")
        print(f"tip verified unmoved: {live[:8]}", flush=True)

        parent = b["remote_head"]
        base_tree = b["main_tree"]
        for i, c in enumerate(b["commits"]):
            tree_entries = []
            for path, sha in c["files"].items():
                if sha == "UPLOAD":
                    raw = Path(c["upload"]).read_bytes()
                    blob = api("POST", "/git/blobs", {
                        "content": base64.b64encode(raw).decode(),
                        "encoding": "base64",
                    })
                    sha = blob["sha"]
                    expect = "e0657182b470239ec93a13e55a08a11af4827dd8"
                    if sha != expect:
                        raise RuntimeError(
                            f"BLOB MISMATCH: remote {sha} != local hash-object {expect}")
                    print(f"uploaded blob {path} -> {sha[:8]} (== local hash-object)", flush=True)
                tree_entries.append({
                    "path": path, "mode": "100644", "type": "blob", "sha": sha,
                })
            if any(p == "PREV" for p in c["parents"]):
                parents = [parent]
            else:
                parents = [
                    parent if p == "BRANCH_HEAD" else b["main_tip"]
                    for p in c["parents"]
                ]
            tree = api("POST", "/git/trees", {"base_tree": base_tree, "tree": tree_entries})
            if tree["sha"] != c["expect_tree"]:
                raise RuntimeError(
                    f"TREE MISMATCH: api {tree['sha']} != local {c['expect_tree']} — refusing ref move")
            print(f"tree verified == local tree: {tree['sha'][:8]}", flush=True)
            commit = api("POST", "/git/commits", {
                "message": c["message"],
                "tree": tree["sha"],
                "parents": parents,
                "author": author(),       # t0796: executing seat, not a hardcode
                "committer": author(),
            })
            parent = commit["sha"]
            base_tree = tree["sha"]
            print(f"commit {i+1} created: {parent[:8]}", flush=True)

        # Re-verify tip unmoved at action time, then move the ref.
        live = ref_sha(b["ref"])
        if live != b["remote_head"]:
            raise RuntimeError(f"tip moved before PATCH: {live} — refusing")
        enc = b["ref"].replace("/", "%2F")
        api("PATCH", f"/git/refs/heads/{enc}", {"sha": parent})
        final = ref_sha(b["ref"])
        if final != parent:
            raise RuntimeError(f"ref PATCH failed: {final} != {parent}")
        print(f"OK: {b['ref']} -> {parent[:8]}", flush=True)


if __name__ == "__main__":
    main()
