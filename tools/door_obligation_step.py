#!/usr/bin/env python3
"""The door-obligation step: close the leak the write path left open.

After a run files its BRAIN projection pages (and the byte-identical
read-backs pass), this step runs mechanically for exactly that run's ids:

  (a) check out the branch tip into a scratch worktree (never the stale
      local copy — the worktree is fetched fresh from origin first);
  (b) run tools/check_door_obligation.py CHECK, scoped to the run's ids;
  (c) run --fix --ids for any defects — the fixer generates the capture +
      registry entry FROM THE PUBLISHED PAGE, with honest backfill
      provenance, and REFUSES ids with no page on disk;
  (d) regenerate the brain index (the fixer does this with --with-regen);
  (e) file capture + registry + index in ONE commit via the GitHub git
      data API, with the head-guard (the branch head is re-read
      immediately before the ref update; on any move the step aborts and
      the caller re-runs it — nothing is filed over a moved head);
  (f) re-run CHECK, scoped to the run's ids, to exit 0 — and read every
      filed file back from the new head, byte-identical.

Nothing here is hand-written: no capture, no registry entry, no invented
field, id, or value. The only files that may change are the run's
captures, the registry, and the brain index — any other change stops
the step cold.

Usage (called by the run file scripts after the projection PUTs):
  python3 tools/door_obligation_step.py --ids SN-2692,SN-2693,... \
      [--branch main] [--repo /home/hatch/workspace/nayapower-repo] \
      [--worktree /path/to/an/existing/checkout] \
      [--date YYYY-MM-DD] [--message "..."] [--dry-run]

Exit codes: 0 = obligation met (or nothing to do); 1 = refused / stop
(fixer refusals, unexpected changes, CHECK still failing after the fix);
2 = machinery error (fail closed); 3 = branch head moved (re-run).
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://api.github.com"
OWNER_REPO = "SoulSchoolAcademy/NayaPOWER"
GH_DIRECT = "/home/hatch/workspace/team-nitro/gh-direct.py"
DEFAULT_REPO = "/home/hatch/workspace/nayapower-repo"

REGISTRY_REL = ".naya/memory/smart-notes/index.json"
INDEX_REL = "BRAIN/NAYAPOWER-BRAIN-INDEX.json"
REAL_TREE_JSON = "BRAIN/REAL-TREE.json"
REAL_TREE_MD = "BRAIN/REAL-TREE.md"
CAPTURE_DIR = ".naya/capture"


def _load_gh_direct(path: str):
    spec = importlib.util.spec_from_file_location("gh_direct", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class GitHub:
    """Minimal API client: token minted in memory, never the cache."""

    def __init__(self, gh_direct_path: str):
        self.token = _load_gh_direct(gh_direct_path).get_token()

    def call(self, method: str, path: str, body=None):
        req = urllib.request.Request(
            BASE + path,
            data=json.dumps(body).encode() if body is not None else None,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "muse-github-skill/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            try:
                return e.code, json.loads(raw)
            except json.JSONDecodeError:
                return e.code, {"raw": raw[:300]}


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=600)
    return r


def _tail(text, n=300):
    """Last n chars of git stderr — the real error lives at the end,
    after the progress lines, never at the head."""
    lines = [ln for ln in text.replace("\r", "\n").splitlines()
             if ln.strip() and "Updating files" not in ln]
    return "\n".join(lines[-3:])[-n:] if lines else text[-n:]


def _verify_tree_equivalence(gh, worktree: Path, tip: str):
    """Prove the worktree's CONTENT equals the branch tip's content,
    without fetching (used only when the fetch is EPERM-blocked).

    The guarantee the step needs is content, not a HEAD pointer: the
    fixer reads page bytes, registry bytes, captures, and the pages'
    git history — all of which live in the worktree already when the
    tip differs from the worktree HEAD only by files already on disk
    with identical bytes. Both trees are compared through the API
    alone (tip tree vs HEAD tree by sha — never by parsing local
    ls-tree output, whose quoting miscounted the diff as 3 paths
    when the true diff was 1 file), then every differing path is
    byte-compared against the blob the tip names. Returns
    (True, evidence) or (False, reason)."""
    status, commit = gh.call("GET", f"/repos/{OWNER_REPO}/git/commits/{tip}")
    if status != 200:
        return False, f"cannot read tip commit: {status}"
    tip_tree = commit["tree"]["sha"]
    r = run(["git", "-C", str(worktree), "rev-parse", "HEAD^{tree}"])
    if r.returncode != 0:
        return False, f"rev-parse HEAD tree failed: {_tail(r.stderr)}"
    head_tree = r.stdout.strip()
    if head_tree == tip_tree:
        return True, "trees identical"

    def _blob_map(tree_sha):
        status, listing = gh.call(
            "GET", f"/repos/{OWNER_REPO}/git/trees/{tree_sha}?recursive=1")
        if status != 200:
            return None, f"cannot list tree {tree_sha[:10]}: {status}"
        return ({t["path"]: t["sha"] for t in listing.get("tree", [])
                 if t["type"] == "blob"}, "")
    tip_files, err = _blob_map(tip_tree)
    if tip_files is None:
        return False, err
    head_files, err = _blob_map(head_tree)
    if head_files is None:
        return False, err
    diff_paths = sorted(set(tip_files) ^ set(head_files) |
                        {p for p in set(tip_files) & set(head_files)
                         if tip_files[p] != head_files[p]})
    if not diff_paths:
        return True, "trees identical"
    for path in diff_paths:
        if path in tip_files and path not in head_files:
            action = "added in tip"
        elif path not in tip_files and path in head_files:
            if (worktree / path).exists():
                return False, (f"tip deletes {path} but it still exists "
                               f"on disk")
            continue
        else:
            action = "modified in tip"
        disk = worktree / path
        if not disk.is_file():
            return False, f"tip {action}: {path} missing on disk"
        status, blob = gh.call(
            "GET", f"/repos/{OWNER_REPO}/git/blobs/{tip_files[path]}")
        if status != 200:
            return False, f"cannot read tip blob for {path}: {status}"
        if base64.b64decode(blob["content"]) != disk.read_bytes():
            return False, f"tip {action}: {path} differs on disk"
    return True, (f"content equals tip ({len(diff_paths)} differing "
                  f"path(s): {', '.join(diff_paths)} — all byte-identical "
                  f"on disk)")


def fail(msg, code=1):
    print(f"DOOR-STEP STOP: {msg}", flush=True)
    return code


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ids", required=True,
                    help="comma-separated SN ids, e.g. SN-2692,SN-2693")
    ap.add_argument("--branch", default="main",
                    help="branch to file the cure on (default: main)")
    ap.add_argument("--repo", default=DEFAULT_REPO,
                    help="local repo checkout to worktree from")
    ap.add_argument("--worktree", default=None,
                    help="reuse an existing checkout instead of a scratch "
                         "worktree: it is fetched, moved to the branch tip, "
                         "and verified clean before the fixer runs. Use when "
                         "the VM's EPERM flake refuses a full checkout; the "
                         "guarantee is the same (HEAD == tip, verified). "
                         "If the fetch itself is EPERM-blocked, the step "
                         "falls back to proving tree-equivalence with the "
                         "tip via the API (see _verify_tree_equivalence) "
                         "and runs on the worktree as-is.")
    ap.add_argument("--date", default=None,
                    help="backfill date stamp YYYY-MM-DD (default: today UTC)")
    ap.add_argument("--message", default=None,
                    help="commit message for the cure commit")
    ap.add_argument("--dry-run", action="store_true",
                    help="run through the on-disk CHECK, file nothing")
    ap.add_argument("--gh-direct", default=GH_DIRECT)
    args = ap.parse_args(argv)

    ids = [s.strip().upper() for s in args.ids.split(",") if s.strip()]
    if not ids:
        return fail("no ids given", 2)
    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ids_csv = ",".join(ids)
    branch = args.branch
    repo = Path(args.repo)
    if not (repo / ".git").exists() and not (repo / "tools").exists():
        return fail(f"{repo} does not look like the NayaPOWER checkout", 2)

    gh = GitHub(args.gh_direct)

    # ---- 1. resolve the branch tip (first-hand, from the API) ----
    status, ref = gh.call("GET", f"/repos/{OWNER_REPO}/git/refs/heads/{branch}")
    if status != 200:
        return fail(f"cannot resolve branch {branch}: {status} "
                     f"{str(ref)[:200]}", 2)
    tip = ref["object"]["sha"]
    print(f"branch {branch} tip: {tip}", flush=True)

    # ---- 2. worktree at the tip (never the stale local copy) ----
    import time as _time
    scratch_is_mine = args.worktree is None
    scratch = (Path(args.worktree) if args.worktree
               else Path(tempfile.mkdtemp(prefix="door-step-")))
    try:
        # Fetch the tip SHA itself: `git fetch origin <branch>` only fills
        # FETCH_HEAD and never creates origin/<branch>, so a worktree add
        # by branch name fails closed. The tip SHA is reachable from the
        # branch ref, so GitHub serves it by SHA.
        fetch_repo = str(scratch if args.worktree else repo)
        fetched = False
        last_err = ""
        for attempt in range(1, 4):
            r = run(["git", "-C", fetch_repo, "fetch", "origin", tip])
            if r.returncode == 0:
                fetched = True
                break
            last_err = _tail(r.stderr)
            print(f"fetch attempt {attempt}/3 failed: {last_err}",
                  flush=True)
            if attempt < 3:
                _time.sleep(10)
        equivalent = False
        equiv_note = ""
        if not fetched and args.worktree:
            # The fetch itself is EPERM-blocked (it writes loose objects).
            # Fall back to proving the worktree's content already equals
            # the tip — the guarantee the step needs is content, not a
            # HEAD pointer. If equivalence fails, this is a hard stop.
            print("fetch EPERM-blocked; proving tree-equivalence with "
                  "the tip via the API instead", flush=True)
            equivalent, equiv_note = _verify_tree_equivalence(
                gh, scratch, tip)
            if not equivalent:
                return fail(f"fetch failed and tree-equivalence failed: "
                            f"{last_err} / {equiv_note}", 2)
            print(f"tree-equivalence proven: {equiv_note}", flush=True)
        elif not fetched:
            return fail(f"fetch origin {tip} failed after 3 attempts: "
                        f"{last_err}", 2)
        if args.worktree:
            if equivalent:
                # Content already proven equal to the tip; the HEAD pointer
                # stays behind, and the record says so. Still verify the
                # tree is clean before the fixer runs.
                print(f"reused worktree {scratch} at "
                      f"{run(['git', '-C', str(scratch), 'rev-parse', 'HEAD']).stdout.strip()} "
                      f"(content == tip {tip[:10]}, HEAD not moved — "
                      f"equivalence proven above)", flush=True)
            else:
                # Reuse the existing checkout: move it to the tip (writes
                # only the diff) and verify it is clean before the fixer.
                # First, clear the checkout's own blocker: an untracked
                # file that the tip tracks ("would be overwritten by
                # checkout"). The step script itself is exactly such a
                # file — it lives on disk untracked at HEAD, tracked at
                # the tip. Remove it ONLY when its bytes are byte-
                # identical to the tip blob (hash-object vs ls-tree);
                # differing content stops the run instead of being
                # destroyed. (The running process already holds the
                # script in memory, so re-writing identical bytes is
                # safe.)
                r = run(["git", "-C", str(scratch), "ls-files", "--others",
                         "--exclude-standard"])
                for path in [ln.strip() for ln in r.stdout.splitlines()
                             if ln.strip()]:
                    ls = run(["git", "-C", str(scratch), "ls-tree", tip,
                              "--", path])
                    if ls.returncode != 0 or not ls.stdout.strip():
                        continue  # tip does not track it; checkout leaves it
                    tip_sha = ls.stdout.split()[2]
                    ho = run(["git", "-C", str(scratch), "hash-object",
                              path])
                    if ho.returncode == 0 and ho.stdout.strip() == tip_sha:
                        print(f"removing untracked {path} (byte-identical "
                              f"to tip)", flush=True)
                        (scratch / path).unlink()
                    else:
                        return fail(f"untracked {path} differs from the "
                                    f"tip version; move or remove it before "
                                    f"re-running", 1)
                # Tracked files with local modifications that the tip
                # would overwrite (the step script, re-filed since the
                # last run): restore from the TIP — not HEAD — but only
                # when byte-identical to the tip blob; differing content
                # stops the run instead of being destroyed. (Restoring
                # from the tip stages the file; the full checkout below
                # moves HEAD to the tip, after which the tree is clean.)
                r = run(["git", "-C", str(scratch), "status", "--porcelain"])
                for line in r.stdout.splitlines():
                    if not line.strip() or line.startswith("??"):
                        continue
                    path = line[3:].strip()
                    if "M" not in line[:2]:
                        continue
                    ls = run(["git", "-C", str(scratch), "ls-tree", tip,
                              "--", path])
                    if ls.returncode != 0 or not ls.stdout.strip():
                        continue
                    tip_sha = ls.stdout.split()[2]
                    ho = run(["git", "-C", str(scratch), "hash-object",
                              path])
                    if ho.returncode == 0 and ho.stdout.strip() == tip_sha:
                        print(f"restoring {path} from tip (byte-identical "
                              f"local modification)", flush=True)
                        run(["git", "-C", str(scratch), "checkout", tip,
                             "--", path])
                    else:
                        return fail(f"tracked {path} has local changes "
                                    f"differing from the tip; commit or "
                                    f"stash them before re-running", 1)
                moved = False
                last_err = ""
                for attempt in range(1, 4):
                    r = run(["git", "-C", str(scratch), "checkout",
                             "--detach", tip])
                    if r.returncode == 0:
                        moved = True
                        break
                    last_err = _tail(r.stderr)
                    print(f"checkout attempt {attempt}/3 failed: {last_err}",
                          flush=True)
                    if attempt < 3:
                        _time.sleep(10)
                if not moved:
                    return fail(f"checkout to tip failed after 3 attempts: "
                                f"{last_err}", 2)
                head = run(["git", "-C", str(scratch), "rev-parse", "HEAD"]
                           ).stdout.strip()
                if head != tip:
                    return fail(f"worktree HEAD {head} != branch tip {tip}",
                                2)
                print(f"reused worktree {scratch} at {head} (clean)",
                      flush=True)
            r = run(["git", "-C", str(scratch), "status", "--porcelain"])
            tracked_dirty = [ln for ln in r.stdout.splitlines()
                             if ln[:2].strip() and not ln.startswith("??")]
            if tracked_dirty:
                return fail(f"worktree has tracked changes before the fix: "
                            f"{tracked_dirty[:5]}", 1)
        else:
            # Fresh scratch worktree: the checkout writes ~8k files and the
            # VM's EPERM flake can refuse writes mid-checkout and clears on
            # its own — retry boundedly (never silently, never forever),
            # pruning between attempts.
            added = False
            last_err = ""
            for attempt in range(1, 4):
                r = run(["git", "-C", str(repo), "worktree", "add",
                         "--detach", str(scratch), tip])
                if r.returncode == 0:
                    added = True
                    break
                last_err = _tail(r.stderr)
                print(f"worktree add attempt {attempt}/3 failed: {last_err}",
                      flush=True)
                run(["git", "-C", str(repo), "worktree", "prune"])
                run(["rm", "-rf", str(scratch)])
                scratch.mkdir(parents=True, exist_ok=True)
                if attempt < 3:
                    _time.sleep(10)
            if not added:
                return fail(f"worktree add failed after 3 attempts: "
                            f"{last_err}", 2)
            head = run(["git", "-C", str(scratch), "rev-parse", "HEAD"]
                       ).stdout.strip()
            if head != tip:
                return fail(f"scratch HEAD {head} != branch tip {tip}", 2)
            print(f"scratch worktree {scratch} at {head}", flush=True)
        # NOTE: no second HEAD check here — each branch above already
        # verified its own guarantee (checkout mode: HEAD == tip;
        # equivalence mode: content == tip, HEAD deliberately unmoved).

        tool = str(scratch / "tools" / "check_door_obligation.py")

        # ---- 3. CHECK, scoped to the run's ids ----
        r = run([sys.executable, tool, "--root", str(scratch),
                 "--ids", ids_csv, "--json"])
        try:
            check_before = json.loads(r.stdout)
            defects_before = check_before.get("defects", [])
        except json.JSONDecodeError:
            return fail(f"CHECK output unparsable: {r.stdout[:300]}", 2)
        print(f"CHECK before: {len(defects_before)} defect(s) for the "
              f"{len(ids)} id(s)", flush=True)
        if not defects_before:
            print("DOOR-STEP: obligation already met for these ids; "
                  "nothing to file.", flush=True)
            return 0

        # ---- 4. FIX (generates from the published pages) + regen ----
        # The VM's EPERM flake can refuse the fixer's Python writes
        # mid-run (it dies on the first capture write, leaving a 0-byte
        # .tmp behind) and clears on its own — retry boundedly, on the
        # flake's own timescale. The fixer is idempotent: captures
        # already written are skipped, so a retry resumes where the last
        # attempt died. Stale .tmp files are removed before each attempt
        # (failed-write residue, never part of a filing). The failure's
        # own stderr tail is printed, so the cause is visible instead
        # of an empty "unparsable". Span: 10 attempts x 180 s (~30
        # min) — the flake's observed windows run 35-60 min, and a run
        # needs a clear window lasting the whole FIX (~30 s of writes);
        # 5 attempts over 5 min lost twice to the same window, so the
        # loop now outlasts the window instead of re-running the step.
        fix_out = None
        last_err = ""
        for attempt in range(1, 11):
            for tmp in (scratch / CAPTURE_DIR).glob("*.tmp"):
                try:
                    tmp.unlink()
                except OSError:
                    pass
            r = run([sys.executable, tool, "--root", str(scratch),
                     "--ids", ids_csv, "--fix", "--with-regen",
                     "--date", date, "--json"])
            try:
                # raw_decode: the fixer prints the JSON first, then the
                # regen's human-readable line ("regenerated index layer
                # ...") on the same stream — json.loads on the whole
                # stdout fails on that trailing line (run 5: 10/10
                # attempts "failed" on a FIX that had already completed).
                fix_out, _ = json.JSONDecoder().raw_decode(r.stdout)
                break
            except json.JSONDecodeError:
                last_err = _tail(r.stderr) or r.stdout[:300]
                print(f"FIX attempt {attempt}/10 failed: {last_err}",
                      flush=True)
                if attempt < 10:
                    _time.sleep(180)
        if fix_out is None:
            return fail(f"FIX failed after 10 attempts (EPERM flake did "
                        f"not clear in ~30 min): {last_err}", 2)
        refusals = fix_out.get("refusals", [])
        if refusals:
            return fail(f"fixer REFUSED {refusals} — no page on disk; "
                        f"owner: LAW lane (lifecycle tombstone decision)", 1)
        actions = fix_out.get("fix", {}).get("actions", [])
        print(f"FIX: {len(actions)} action(s); "
              f"registry_changed={fix_out.get('fix', {}).get('registry_changed')}",
              flush=True)

        # ---- 5. exactly the expected files changed — nothing else ----
        r = run(["git", "-C", str(scratch), "status", "--porcelain"])
        changed = {}
        for line in r.stdout.splitlines():
            if not line.strip():
                continue
            code = line[:2].strip()
            p = line[3:].strip()
            if "__pycache__" in p:
                continue  # interpreter bytecode, never a filing
            if p.endswith(".tmp"):
                continue  # failed-write residue, never part of a filing
            if code == "??" and not p.startswith(CAPTURE_DIR + "/"):
                # Pre-existing untracked file, not the fixer's doing
                # (in tree-equivalence mode the step script itself shows
                # here — it is tracked at the tip, untracked at HEAD).
                continue
            changed[p] = code
        new_captures = sorted(p for p, s in changed.items()
                              if p.startswith(CAPTURE_DIR + "/")
                              and s in ("??", "A"))
        # The regen writes three files, not one: the brain index plus
        # the real tree (json + md). The step's expected set missed
        # the real-tree pair (run 5 would have stopped here).
        expected = {REGISTRY_REL, INDEX_REL, REAL_TREE_JSON, REAL_TREE_MD}
        unexpected = sorted(p for p in changed
                            if p not in expected
                            and not p.startswith(CAPTURE_DIR + "/"))
        if unexpected:
            return fail(f"unexpected changes on disk: {unexpected}", 1)
        if len(new_captures) != len(ids):
            return fail(f"expected {len(ids)} new capture(s), found "
                        f"{len(new_captures)}: {new_captures}", 1)
        if set(changed) - set(new_captures) != expected:
            return fail(f"changed set is not exactly captures + registry + "
                        f"index + real tree: {sorted(changed)}", 1)
        print(f"on-disk change set: {len(new_captures)} capture(s) + "
              f"registry + brain index + real tree — nothing else",
              flush=True)

        # ---- 6. CHECK again, scoped to the ids — must exit 0 ----
        r = run([sys.executable, tool, "--root", str(scratch),
                 "--ids", ids_csv, "--json"])
        try:
            check_after = json.loads(r.stdout)
        except json.JSONDecodeError:
            return fail(f"CHECK-after output unparsable: {r.stdout[:300]}", 2)
        # Judge the RUN's ids, not the raw exit code: the door tool
        # reports TOMBSTONE_REQUIRED globally (every vanished id
        # anywhere, not just the run's), so its exit code stays 1
        # until the LAW lane records tombstones for the other ids —
        # out of this round's scope. Pass = no defect for the run's
        # ids and no tombstone naming a run id. (Run 5 proved the
        # cure: 0 defects for the 25, exit 1 on 40 tombstones
        # elsewhere — SN-2648, SN-2650, SN-2670..2683, SN-2717..2731,
        # SN-2733..2741 — exactly the post-cure vanish set.)
        run_tombstones = [t for t in check_after.get("tombstones", [])
                          if t.get("sn") in ids]
        global_tombstones = len(check_after.get("tombstones", []))
        if check_after.get("defects") or run_tombstones:
            return fail(f"CHECK after fix still failing: "
                        f"{str(check_after.get('defects'))[:400]} "
                        f"{str(run_tombstones)[:400]}", 1)
        print(f"CHECK after: 0 defect(s) for the run's ids "
              f"({global_tombstones} tombstone(s) elsewhere, LAW lane's "
              f"— not this run's)", flush=True)

        if args.dry_run:
            print("DOOR-STEP DRY RUN: filing skipped by request; the "
                  "on-disk change set above is what would be filed.",
                  flush=True)
            return 0

        # ---- 7. head-guard + file ONE commit via the git data API ----
        status, ref2 = gh.call(
            "GET", f"/repos/{OWNER_REPO}/git/refs/heads/{branch}")
        if status != 200 or ref2["object"]["sha"] != tip:
            return fail(f"branch head moved ({tip} -> "
                        f"{ref2.get('object', {}).get('sha')}); re-run", 3)
        status, commit = gh.call("GET", f"/repos/{OWNER_REPO}/git/commits/{tip}")
        if status != 200:
            return fail(f"cannot read tip commit: {status}", 2)
        base_tree = commit["tree"]["sha"]

        files = sorted(changed)
        blobs = {}
        for rel in files:
            raw = (scratch / rel).read_bytes()
            status, blob = gh.call(
                "POST", f"/repos/{OWNER_REPO}/git/blobs",
                {"content": base64.b64encode(raw).decode("ascii"),
                 "encoding": "base64"})
            if status != 201:
                return fail(f"blob create failed for {rel}: {status} "
                            f"{str(blob)[:200]}", 2)
            blobs[rel] = (blob["sha"], raw)
        status, tree = gh.call(
            "POST", f"/repos/{OWNER_REPO}/git/trees",
            {"base_tree": base_tree,
             "tree": [{"path": rel, "mode": "100644", "type": "blob",
                       "sha": blobs[rel][0]} for rel in files]})
        if status != 201:
            return fail(f"tree create failed: {status} {str(tree)[:200]}", 2)
        msg = args.message or (
            f"safety: cure vanish {ids[0]}..{ids[-1]} "
            f"(capture + registry backfill via door step)")
        status, new_commit = gh.call(
            "POST", f"/repos/{OWNER_REPO}/git/commits",
            {"message": msg, "tree": tree["sha"], "parents": [tip]})
        if status != 201:
            return fail(f"commit create failed: {status} "
                        f"{str(new_commit)[:200]}", 2)
        new_sha = new_commit["sha"]

        # re-read the head immediately before the ref update — abort on move
        status, ref3 = gh.call(
            "GET", f"/repos/{OWNER_REPO}/git/refs/heads/{branch}")
        if status != 200 or ref3["object"]["sha"] != tip:
            return fail(f"branch head moved before ref update "
                        f"({tip} -> {ref3.get('object', {}).get('sha')}); "
                        f"commit {new_sha} orphaned — re-run", 3)
        status, updated = gh.call(
            "PATCH", f"/repos/{OWNER_REPO}/git/refs/heads/{branch}",
            {"sha": new_sha})
        if status != 200 or updated.get("object", {}).get("sha") != new_sha:
            return fail(f"ref update failed: {status} "
                        f"{str(updated)[:200]}", 2)
        print(f"filed commit {new_sha} on {branch} "
              f"(parent {tip})", flush=True)

        # ---- 8. read every filed file back from the new head, byte-identical
        for rel in files:
            status, blob = gh.call(
                "GET", f"/repos/{OWNER_REPO}/git/blobs/{blobs[rel][0]}")
            if status != 200:
                return fail(f"read-back failed for {rel}: {status}", 2)
            if base64.b64decode(blob["content"]) != blobs[rel][1]:
                return fail(f"read-back MISMATCH for {rel}", 1)
        print(f"read-back: {len(files)} file(s) byte-identical on the new "
              f"head", flush=True)
        print(json.dumps({
            "branch": branch, "parent": tip, "commit": new_sha,
            "files": files, "defects_before": len(defects_before),
            "ids": ids}, indent=2), flush=True)
        return 0
    finally:
        if scratch_is_mine:
            run(["git", "-C", str(repo), "worktree", "remove", "--force",
                 str(scratch)])
            print(f"scratch worktree {scratch} removed", flush=True)
        else:
            print(f"reused worktree {scratch} left in place (not removed)",
                  flush=True)


if __name__ == "__main__":
    sys.exit(main())
