#!/usr/bin/env python3
"""Re-anchor naya4/evolve-proposal-lifecycle-v1 onto the exact live tip.

Pattern (per AGENTS.md lessons):
- blobs via API, verify local git hash-object == remote blob sha
- tree = tip tree + branch files (base_tree=tip), mechanical no-drop verify
- commit parented exactly on the live tip, seat authorship (never a human's)
- re-verify tip unmoved at action time (SN-0493) before the ref PATCH
- PATCH uses plural /git/refs/heads/ with the slash URL-encoded; force=true
"""

import base64
import hashlib
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
BRANCH = "naya4/evolve-proposal-lifecycle-v1"
GH = str(Path.home() / "workspace/skills/github/bin/gh-api")
BUILD = Path(__file__).resolve().parent
TIP = "78661f59a2090dcb2854e3f59b83cf49955ed80c"
FILES = [
    BUILD / "tools/evolve_proposals.py",
    BUILD / "tests/test_evolve_proposals.py",
]
REPO_PATHS = ["tools/evolve_proposals.py", "tests/test_evolve_proposals.py"]

COMMIT_MESSAGE = """feat(evolve): ADOPT gate — adoption requires measured-improvement receipt

The proposal-lifecycle ledger let VERIFIED -> ADOPTED through with a
free-text reason; the contract invariant "never promote speculative
improvements as facts" was a label, not machinery. This commit makes it
machinery:

- transition --to ADOPTED now requires --receipt <path> (fail-closed, exit 2)
- receipt schema: proposal_id must match, verdict exactly "improved",
  non-empty measured deltas (metric/before/after/method), measured_at set
- receipt sha256 sealed into the ledger entry for audit
- --receipt on any other transition is refused (mistyped-target signal)

Tests: 26/26 hermetic (16 existing + 10 new ADOPT-gate tests), stdlib only.
Re-anchored on exact tip 78661f59: parent == tip, tree = tip + 2 files,
mechanical no-drop verification (tip blob count + 2, 0 dropped, 0 changed).

CANDIDATE — Scorecard Law merge protocol applies; merge is the authorized
merger's call. Supersedes f2708be3 (which carried a false human attribution
from a poisoned worktree identity config; that commit is now dangling).
"""


def api(method, path, body=None):
    cmd = [GH, method, f"/repos/{REPO}{path}"]
    if body is not None:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as fh:
            json.dump(body, fh)
            tmp = fh.name
        cmd.append("@" + tmp)
    else:
        tmp = None
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if tmp:
            Path(tmp).unlink(missing_ok=True)
    if out.returncode != 0:
        print(f"API FAILED: {method} {path}\n{out.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out.stdout)


def sh(cmd, **kw):
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)
    if out.returncode != 0:
        print(f"CMD FAILED: {cmd}\n{out.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return out.stdout.strip()


def main():
    # 1. Re-verify the tip is still the tip (SN-0493: decide -> re-anchor -> act).
    live = sh(
        ["git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD"]
    ).split()[0]
    assert live == TIP, f"tip moved during build: {live} != {TIP}"
    print(f"tip confirmed: {TIP}")

    # 2. Blobs for the two files; verify content-addressing locally.
    blobs = {}
    for local, repo_path in zip(FILES, REPO_PATHS):
        raw = local.read_bytes()
        local_sha = sh(["git", "hash-object", "-t", "blob", str(local)])
        b = api(
            "POST",
            "/git/blobs",
            {"content": base64.b64encode(raw).decode(), "encoding": "base64"},
        )
        assert b["sha"] == local_sha, (
            f"blob sha mismatch for {repo_path}: remote {b['sha']} != local {local_sha}"
        )
        blobs[repo_path] = b["sha"]
        print(f"blob ok: {repo_path} {b['sha'][:12]} ({len(raw)} bytes)")

    # 3. Tip tree sha.
    tip_commit = api("GET", f"/git/commits/{TIP}")
    tip_tree = tip_commit["tree"]["sha"]
    print(f"tip tree: {tip_tree[:12]}")

    # 4. New tree = tip tree + branch files.
    new_tree = api(
        "POST",
        "/git/trees",
        {
            "base_tree": tip_tree,
            "tree": [
                {"path": p, "mode": "100644", "type": "blob", "sha": s}
                for p, s in blobs.items()
            ],
        },
    )
    new_tree_sha = new_tree["sha"]
    print(f"new tree: {new_tree_sha[:12]}")

    # 5. Mechanical no-drop verification: recursive listings must differ by
    #    exactly the two added files — 0 dropped, 0 changed.
    def tree_map(sha):
        t = api("GET", f"/git/trees/{sha}?recursive=1")
        return {e["path"]: e["sha"] for e in t["tree"] if e["type"] == "blob"}

    tip_map = tree_map(tip_tree)
    new_map = tree_map(new_tree_sha)
    added = {p for p in new_map if p not in tip_map}
    dropped = {p for p in tip_map if p not in new_map}
    changed = {p for p in new_map if p in tip_map and new_map[p] != tip_map[p]}
    assert added == set(REPO_PATHS), f"added mismatch: {added}"
    assert not dropped, f"DROPPED FILES: {dropped}"
    assert not changed, f"CHANGED FILES: {changed}"
    for p in REPO_PATHS:
        assert new_map[p] == blobs[p], f"blob sha wrong in tree for {p}"
    print(
        f"tree verified: tip {len(tip_map)} blobs -> new {len(new_map)} blobs; "
        f"+{len(added)} added, 0 dropped, 0 changed"
    )

    # 6. Commit parented exactly on the tip, seat authorship (t0796: executing seat).
    commit = api(
        "POST",
        "/git/commits",
        {
            "message": COMMIT_MESSAGE,
            "tree": new_tree_sha,
            "parents": [TIP],
            "author": author(),
            "committer": author(),
        },
    )
    new_sha = commit["sha"]
    assert commit["parents"][0]["sha"] == TIP, "parent != tip"
    assert commit["author"]["name"] == author()["name"], "author identity wrong"
    print(f"commit: {new_sha[:12]} parent == tip, author == {author()['name']}")

    # 7. Re-verify tip unmoved at action time — a decision expires when it moves.
    live2 = sh(
        ["git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD"]
    ).split()[0]
    if live2 != TIP:
        print(
            f"ABORT: tip moved {TIP[:8]} -> {live2[:8]} before ref move; "
            f"commit {new_sha[:12]} created but ref NOT moved.",
            file=sys.stderr,
        )
        sys.exit(2)

    # 8. Move the branch ref (non-fast-forward: force=true; plural path,
    #    slash URL-encoded).
    ref = api(
        "PATCH",
        "/git/refs/heads/naya4%2Fevolve-proposal-lifecycle-v1",
        {"sha": new_sha, "force": True},
    )
    print(f"ref moved: {ref['ref']} -> {ref['object']['sha'][:12]}")
    print(f"NEW_HEAD={new_sha}")


if __name__ == "__main__":
    main()
