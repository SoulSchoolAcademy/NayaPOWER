#!/usr/bin/env python3
"""Push naya4/evolve-meta-trend-v1: tools/evolve_meta_trend.py + tests.

Pattern (per AGENTS.md lessons):
- verify live tip == TIP before anything
- blobs via API, verify local git hash-object == remote blob sha
- tree = tip tree + 2 new files (base_tree=tip), mechanical no-drop verify
- commit parented exactly on the live tip, seat authorship
- re-verify tip unmoved at action time (SN-0493) before the ref create
- open PR under the Scorecard Law; NEVER merge
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
BRANCH = "naya4/evolve-meta-trend-v1"
GH = str(Path.home() / "workspace/skills/github/bin/gh-api")
WORK = Path("/tmp/evolve-trend-work")
TIP = "094634be45b2fb82baac281c95db17e86ee07cc9"

FILES = [
    (WORK / "tools/evolve_meta_trend.py", "tools/evolve_meta_trend.py"),
    (WORK / "tests/test_evolve_meta_trend.py", "tests/test_evolve_meta_trend.py"),
]

COMMIT_MESSAGE = """feat(evolve): meta-learning trend comparator v1

The meta-learning instrument (PR #1931) produced its first live bundle this
morning (739 entries) — but a single snapshot is a baseline, not a running
loop. EVOLVE is \"the system getting better at getting better\": without
deltas across runs, the area cannot tell whether the learning system is
improving at all.

This commit adds the smallest effective machinery for that:

- tools/evolve_meta_trend.py: compares baseline -> current bundles and emits
  the DELTA — entries, per-day ingestion velocity, status-mix counts+fractions,
  integration-coverage fraction, stale learning debt (newly-stale vs resolved
  ids), calibration churn NEW self-corrections since baseline (the
  meta-learning signal that matters most), authority-gate load, receipt health
  (newly-missing vs recovered). Read-only on both inputs; stdlib only.
- Deliberately carries NO score — a machine scoring its own learning
  trajectory is theater (test-asserted, with an explicit caveats block).
- Fail-closed exit 2: missing/unreadable/malformed bundles, missing metric
  blocks, envelope-version mismatch (stale threshold_days mismatch warns,
  not fails).
- tests/test_evolve_meta_trend.py: 5/5 hermetic (delta math, id-set deltas,
  threshold-mismatch warning, all fail-closed paths, no-score boundary +
  input read-only assertion).

First real trend run (morning bundle 1445Z vs 2045Z): 739 -> 775 entries
(+36, all INGESTED/filed, +0 RATIFIED); stale debt 0 -> 0; NEW
self-corrections 0; gate 95 flagged unchanged; receipts unchanged. Throughput
happened; the meta-learning signal did not move. The machine reports; the
human scores.

Stacks cleanly with #1931 (no code dependency — reads bundle JSON only).
CANDIDATE — Scorecard Law merge protocol applies; I do not merge my own PRs.
"""


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
        print(f"API FAILED: {method} {path}\n{out.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out.stdout)


def sh(cmd, **kw):
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)
    if out.returncode != 0:
        print(f"CMD FAILED: {' '.join(cmd)}\n{out.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return out.stdout.strip()


def main():
    live = sh(["git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD"]).split()[0]
    if live != TIP:
        print(f"ABORT: tip moved {TIP[:8]} -> {live[:8]} before push", file=sys.stderr)
        sys.exit(2)
    print(f"tip verified: {live[:12]}")

    # existing branch? must not exist (404 = absent, anything else fatal)
    cmd = [GH, "GET", f"/repos/{REPO}/git/ref/heads/{BRANCH.replace('/', '%2F')}"]
    chk = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    existing = chk.returncode == 0
    if chk.returncode != 0 and "404" not in chk.stderr[:500]:
        print(f"API FAILED: branch existence check\n{chk.stderr[:2000]}",
              file=sys.stderr)
        sys.exit(1)
    if existing:
        print(f"ABORT: branch {BRANCH} already exists", file=sys.stderr)
        sys.exit(2)

    tip_tree = api("GET", f"/git/trees/{TIP}?recursive=1")
    tip_blobs = {t["path"]: t["sha"] for t in tip_tree["tree"] if t["type"] == "blob"}
    print(f"tip tree: {len(tip_blobs)} blobs")

    for local, repo_path in FILES:
        if repo_path in tip_blobs:
            print(f"ABORT: {repo_path} already exists on tip", file=sys.stderr)
            sys.exit(2)

    blobs = {}
    for local, repo_path in FILES:
        content = local.read_bytes()
        # compute via git hash-object on the file
        out = subprocess.run(
            ["git", "hash-object", str(local)], capture_output=True, text=True
        )
        if out.returncode != 0:
            print(f"hash-object failed for {local}", file=sys.stderr)
            sys.exit(1)
        local_sha = out.stdout.strip()
        blob = api("POST", "/git/blobs", {
            "content": base64.b64encode(content).decode(),
            "encoding": "base64",
        })
        if blob["sha"] != local_sha:
            print(f"ABORT: blob sha mismatch for {repo_path}: "
                  f"remote {blob['sha'][:12]} != local {local_sha[:12]}",
                  file=sys.stderr)
            sys.exit(2)
        blobs[repo_path] = blob["sha"]
        print(f"blob ok: {repo_path} {blob['sha'][:12]}")

    tree_entries = [{"path": p, "mode": "100644", "type": "blob", "sha": s}
                    for p, s in blobs.items()]
    new_tree = api("POST", "/git/trees", {
        "base_tree": tip_tree["sha"],
        "tree": tree_entries,
    })
    new_tree_sha = new_tree["sha"]

    # mechanical no-drop verification
    new_full = api("GET", f"/git/trees/{new_tree_sha}?recursive=1")
    new_map = {t["path"]: t["sha"] for t in new_full["tree"] if t["type"] == "blob"}
    dropped = set(tip_blobs) - set(new_map)
    changed = {p for p in tip_blobs if p in new_map and tip_blobs[p] != new_map[p]}
    added = set(new_map) - set(tip_blobs)
    assert not dropped, f"dropped files: {sorted(dropped)}"
    assert not changed, f"changed files: {sorted(changed)}"
    assert added == set(blobs), f"added mismatch: {sorted(added)}"
    for p in added:
        assert new_map[p] == blobs[p], f"blob sha wrong in tree for {p}"
    print(f"tree verified: tip {len(tip_blobs)} blobs -> new {len(new_map)} blobs; "
          f"+{len(added)} added, 0 dropped, 0 changed")

    commit = api("POST", "/git/commits", {
        "message": COMMIT_MESSAGE,
        "tree": new_tree_sha,
        "parents": [TIP],
        "author": author(),
        "committer": author(),
    })
    new_sha = commit["sha"]
    assert commit["parents"][0]["sha"] == TIP, "parent != tip"
    assert commit["author"]["name"] == author()["name"], "author identity wrong"
    print(f"commit: {new_sha[:12]} parent == tip, author == {author()['name']}")

    live2 = sh(["git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD"]).split()[0]
    if live2 != TIP:
        print(f"ABORT: tip moved {TIP[:8]} -> {live2[:8]} before ref create; "
              f"commit {new_sha[:12]} created but ref NOT created.", file=sys.stderr)
        sys.exit(2)

    ref = api("POST", "/git/refs",
              {"ref": f"refs/heads/{BRANCH}", "sha": new_sha})
    print(f"ref created: {ref['ref']} -> {ref['object']['sha'][:12]}")
    print(f"NEW_HEAD={new_sha}")


if __name__ == "__main__":
    main()
