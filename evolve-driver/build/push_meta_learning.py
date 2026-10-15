#!/usr/bin/env python3
"""Create naya4/evolve-meta-learning-v1 on the exact live tip via the Git Data API.

Pattern (per AGENTS.md lessons):
- blobs via API, verify local git hash-object == remote blob sha
- tree = tip tree + 2 branch files (base_tree=tip), mechanical no-drop verify
- commit parented exactly on the live tip, seat authorship (never a human's)
- re-verify tip unmoved at action time (SN-0493) before the ref CREATE
- new branch -> POST /git/refs (create); raw slash tolerated on POST
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
BRANCH = "naya4/evolve-meta-learning-v1"
GH = str(Path.home() / "workspace/skills/github/bin/gh-api")
BUILD = Path(__file__).resolve().parent
TIP = "9931dc96cba6b6c9f26394c2e484e4da9abf6056"

FILES = [
    BUILD / "tools/evolve_meta_learning.py",
    BUILD / "tests/test_evolve_meta_learning.py",
]
REPO_PATHS = ["tools/evolve_meta_learning.py", "tests/test_evolve_meta_learning.py"]

COMMIT_MESSAGE = """feat(evolve): meta-learning health instrument v1 (CANDIDATE)

EVOLVE is defined as "the system getting better at getting better:
self-improvement discipline, meta-learning (optimizing how we learn), RSI
hygiene, compounding intelligence across generations" — but nothing measured
whether the LEARNING ITSELF is improving. Area scores were human guesses.
This closes that hole with machinery:

- tools/evolve_meta_learning.py: read-only scan of a learn-state root
  (ledger.json + optional receipts/). Computes ingestion velocity per day,
  status mix, integration coverage (landed vs. merely filed; DUPLICATE_OF
  excluded), integration-target counter, stale_unintegrated learning debt
  (INGESTED, zero integrations, older than --stale-days), calibration_churn
  (entries superseding earlier lessons — the meta-learning signal that
  matters most), receipt health (found/missing, check PASS/FAIL), and the
  authority-gate queue load. Stdlib only. Fail-closed exit 2 on bad input.
- The bundle deliberately carries NO score: a machine that scores its own
  learning is theater. Every bundle ships an explicit caveats block
  (filed != adopted; gate state != value).
- tests/test_evolve_meta_learning.py: 14/14 hermetic, CLI-level, tmp-fixture;
  asserts metric math, fail-closed paths, read-only scan, and the no-score
  honesty boundary.

Evidence:
- 14/14 hermetic tests green locally (repo never mutated).
- Real-data smoke test on the actual learn ledger (698 entries): scan ok,
  coverage 1.0 (every entry filed — caveat applies), status 85.5% INGESTED /
  13.2% FLAGGED_AUTHORITY / 1.15% RATIFIED, 18 calibration-churn entries,
  receipts 697 found / 1 missing / 1677 checks PASS / 0 FAIL.
- Mechanical no-drop verification: tree = tip tree + exactly the 2 new
  files; 0 dropped, 0 changed; remote blob SHAs == local git hash-object.

Status: CANDIDATE. Not merged, not deployed, not ratified. No governance
changes, no production touch, no credentials. Pure addition (2 files),
fully reversible.

Merge path: base wave heals -> tip green -> CI green -> merge under
Scorecard Law. I do not merge my own PRs without the protocol.
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
        print(f"CMD FAILED: {cmd}\n{out.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return out.stdout.strip()


def main():
    live = sh(["git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD"]).split()[0]
    assert live == TIP, f"tip moved during build: {live} != {TIP}"
    print(f"tip confirmed: {TIP}")

    blobs = {}
    for local, repo_path in zip(FILES, REPO_PATHS):
        raw = local.read_bytes()
        local_sha = sh(["git", "hash-object", "-t", "blob", str(local)])
        b = api("POST", "/git/blobs",
                {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        assert b["sha"] == local_sha, (
            f"blob sha mismatch for {repo_path}: remote {b['sha']} != local {local_sha}"
        )
        blobs[repo_path] = b["sha"]
        print(f"blob ok: {repo_path} {b['sha'][:12]} ({len(raw)} bytes)")

    tip_commit = api("GET", f"/git/commits/{TIP}")
    tip_tree = tip_commit["tree"]["sha"]
    print(f"tip tree: {tip_tree[:12]}")

    new_tree = api("POST", "/git/trees", {
        "base_tree": tip_tree,
        "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s}
                 for p, s in blobs.items()],
    })
    new_tree_sha = new_tree["sha"]
    print(f"new tree: {new_tree_sha[:12]}")

    def tree_map(sha):
        t = api("GET", f"/git/trees/{sha}?recursive=1")
        return {e["path"]: e["sha"] for e in t["tree"] if e["type"] == "blob"}

    tip_map = tree_map(tip_tree)
    new_map = tree_map(new_tree_sha)
    added = {p for p in new_map if p not in tip_map}
    dropped = {p for p in tip_map if p not in new_map}
    changed = {p for p in new_map if p in tip_map and new_map[p] != tip_map[p]}
    assert added == set(REPO_PATHS), f"added mismatch: {added}"
    assert not dropped, f"DROPPED FILES: {sorted(dropped)[:10]}"
    assert not changed, f"CHANGED FILES: {sorted(changed)[:10]}"
    for p in REPO_PATHS:
        assert new_map[p] == blobs[p], f"blob sha wrong in tree for {p}"
    print(f"tree verified: tip {len(tip_map)} blobs -> new {len(new_map)} blobs; "
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
