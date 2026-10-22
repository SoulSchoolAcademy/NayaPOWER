#!/usr/bin/env python3
"""Post-Merge Guardian — the house-fire loop for landings on main.

Law (Shawn, 2026-10-21 ~22:28Z — the HOUSE-FIRE LAW): if something gets
merged and it shouldn't have been, you don't note it and watch it — you
unmerge it and make it right, right away. Revert first, diagnose second,
fix forward third, automate the prevention fourth. The system runs fast
*because* the watch is continuous and the correction is immediate; the
slow lane is reserved for the few changes with major consequences
(Tier A in the Balanced Machine design, files/balanced-machine/).

What already watched merges before this tool (inventory, 2026-10-21):
  - the team-relay cron's merge-protocol watch — every 15 min it checks
    each merge for a cross-seat review + a ## SCORECARD naming the head.
    Protocol compliance only; it never checks the landing itself.
  - tools/verify_gitdata_merge_tree.py — pre-ref-move tree diff for
    git-data fallback merges only. Prevention for one merge route.
  - tools/auto_merge_self_heal.py — FULL-AUTO-MERGE-V1 clause H3's
    direct-revert hand: auto-merges only, only while the bad merge is
    still the tip, and it PATCHes main's ref directly. Nothing calls it.
  - the push workflows (kernel-tests.yml et al.) — they run the tip's
    own checks on every push; nothing diffs the failing set across a
    merge, checks blob faithfulness of endpoint merges, probes the live
    Hub surface after a Hub landing, prepares a revert, or keeps the
    post-merge defect log the balance gauge reads (DESIGN.ai.md §6:
    escape rate baseline "unmeasured" — this tool is the measure).

This guardian EXTENDS that watch; it replaces none of it. Per push to
main it verifies every landing (PR merge — merge-commit, squash, or
rebase series — and every direct-push range, the door included):

  (a) FAITHFULNESS — the merge commit is an ancestor of the tip, and
      every file the PR changed carries the identical blob at the PR
      head, at the merge commit, and at the tip (a tip difference is
      excused only when a later commit in merge..tip touched the path).
  (b) NO NEW RED — a check failing at the tip is charged to the push
      only when it was PRESENT at the parent commit and completed
      not-failing there (the L636 derivation: parent-vs-merge failing
      sets, per workflow). Inherited reds (failing on both sides) are
      recorded, never charged. A check ABSENT at the parent — no
      check-run at all — or still pending there derives UNKNOWN,
      never a charge: absence is not evidence the check was green.
      (Both historical mischarges — the b1e8d514 claim, voided by
      correction 6347895618, and the PR #2936 claim 6351319337,
      dispositioned MISCHARGE — came from treating absent as passing.)
      Every record carries the derivation itself — per-workflow
      before/after states plus both failing-set counts — so a charge
      is inspectable, never asserted.
  (c) SURFACE — for landings touching HUB/**, the live Hub answers
      200 with its feed present. (Liveness, not freshness: deploy
      freshness is the deploy lane's gauge metric, DESIGN.ai.md §6.)

On a VERIFIED escape the guardian acts in one motion: it prepares the
revert (branch + revert commit + a PR labeled GUARDIAN-REVERT whose
body is the detection evidence — the scorecard substitute the law
allows a safety action) and posts the alarm + evidence + revert link
to the live board. It NEVER merges the revert: merges stay protocol,
so the revert sits one different-seat scorecard from landing. A landing
that is itself a GUARDIAN-REVERT is verified but never revert-prepped
(no loop); if it escapes, the guardian alarms only.

Every landing — clean, escaped, or still pending — writes one JSONL
record to the guardian log (branch live/guardian-log, file
guardian-log.jsonl). The balance gauge counts escapes from this log.

Detection latency: faithfulness + surface verify inside the push
workflow run (~1-2 min after the push). The new-red verdict waits for
the tip's own checks to complete (poll, --wait-secs budget); if they
have not completed when the budget ends, the record is PENDING with
the outstanding check names — recorded, never silent, never charged.

Run by .github/workflows/post-merge-guardian.yml on every push to
main. May also be run by a lane against any before/after pair:

    python3 tools/post_merge_guardian.py --before <sha> --after <sha> \
        --repo-path ~/workspace/naya/repo-tests

Stdlib only. GitHub access via REST (token from GH_TOKEN/GITHUB_TOKEN).
Byte questions are answered by the local clone's git objects — never
by code search, never by a cached listing.
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

LAW_ID = "POST-MERGE-GUARDIAN-V1"
DEFAULT_REPO = "SoulSchoolAcademy/NayaPOWER"
DEFAULT_BOARD = 2793
LOG_BRANCH = "live/guardian-log"
LOG_PATH = "guardian-log.jsonl"
REVERT_LABEL = "GUARDIAN-REVERT"
SURFACE_URL = "https://nayanet.live/"
SURFACE_MARKER = "OFFICIAL_NOTES"
HUB_PREFIXES = ("HUB/",)
FAILING_CONCLUSIONS = {
    "failure", "timed_out", "cancelled", "action_required", "startup_failure",
}
ZERO_SHA = "0" * 40


class ApiError(Exception):
    def __init__(self, status, path, detail=""):
        super().__init__(f"GitHub API {status} on {path}: {detail[:300]}")
        self.status = status
        self.path = path


class GHClient:
    """Thin REST adapter. Tests substitute a fake with the same surface."""

    def __init__(self, repo=DEFAULT_REPO, token=None, api_base="https://api.github.com"):
        self.repo = repo
        self.token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
        self.api_base = api_base.rstrip("/")

    def request(self, method, path, body=None):
        url = path if path.startswith("http") else f"{self.api_base}/repos/{self.repo}{path}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace") if exc.fp else ""
            raise ApiError(exc.code, path, detail) from exc

    def get(self, path):
        return self.request("GET", path)

    def get_all(self, path, key):
        """Paginate a list endpoint (per_page=100) and concatenate `key`."""
        out, page = [], 1
        sep = "&" if "?" in path else "?"
        while True:
            chunk = self.get(f"{path}{sep}per_page=100&page={page}")
            items = chunk.get(key, []) if isinstance(chunk, dict) else chunk
            out.extend(items)
            if len(items) < 100:
                return out
            page += 1

    def post(self, path, body):
        return self.request("POST", path, body)

    def patch(self, path, body):
        return self.request("PATCH", path, body)


# ---------------------------------------------------------------- git seam

def _git(repo, *args, check=True):
    proc = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, timeout=300,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:400]}")
    return proc


def git_is_ancestor(repo, anc, desc):
    return _git(repo, "merge-base", "--is-ancestor", anc, desc, check=False).returncode == 0


def git_blob_at(repo, ref, path):
    """Blob SHA of `path` at `ref`, or None when the path is absent there."""
    proc = _git(repo, "rev-parse", "--verify", "-q", f"{ref}:{path}", check=False)
    return proc.stdout.strip() if proc.returncode == 0 else None


def git_parents(repo, sha):
    out = _git(repo, "show", "-s", "--format=%P", sha).stdout.strip()
    return out.split() if out else []


def git_subject(repo, sha):
    return _git(repo, "show", "-s", "--format=%s", sha).stdout.strip()


def git_commit_time(repo, sha):
    return _git(repo, "show", "-s", "--format=%cI", sha).stdout.strip()


def git_path_touched_between(repo, anc, desc, path):
    out = _git(repo, "log", "--format=%H", f"{anc}..{desc}", "--", path).stdout.strip()
    return bool(out)


def git_object_exists(repo, sha):
    return _git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0


# ------------------------------------------------------------- check runs

def check_sets(client, sha):
    """(failing, pending, completed) check-name sets at a SHA, latest per name."""
    runs = client.get_all(f"/commits/{sha}/check-runs", "check_runs")
    latest = {}
    for run in runs:
        name = run.get("name", "")
        key = (run.get("started_at") or "", run.get("id") or 0)
        if name not in latest or key > latest[name][0]:
            latest[name] = (key, run)
    failing, pending, completed = set(), set(), set()
    for name, (_, run) in latest.items():
        if run.get("status") != "completed":
            pending.add(name)
        else:
            completed.add(name)
            if run.get("conclusion") in FAILING_CONCLUSIONS:
                failing.add(name)
    return failing, pending, completed


# -------------------------------------------------------------- discovery

def discover_landings(client, repo_path, before, after):
    """Group a push's commits into landings: one per PR, one for the rest."""
    comparison = client.get(f"/compare/{before}...{after}")
    commits = comparison.get("commits", [])
    compare_files = {
        f["filename"] for f in comparison.get("files", []) if f.get("filename")
    }
    by_pr, direct = {}, []
    for commit in commits:
        sha = commit["sha"]
        pulls = []
        try:
            pulls = client.get(f"/commits/{sha}/pulls")
        except ApiError:
            pulls = []
        pr = next((p for p in pulls if p.get("merged_at") or p.get("state") == "closed"), None)
        if pr is None and pulls:
            pr = pulls[0]
        if pr is not None:
            by_pr.setdefault(pr["number"], {"pr": pr, "commits": []})["commits"].append(sha)
        else:
            direct.append(sha)

    landings = []
    for number, group in by_pr.items():
        pr = group["pr"]
        files = [
            {"path": f["filename"], "status": f.get("status", "")}
            for f in _pr_files(client, number)
            if f.get("filename")
        ]
        merge_sha = group["commits"][-1]
        landings.append({
            "kind": "PR_MERGE",
            "pr": number,
            "pr_url": pr.get("html_url", ""),
            "pr_title": pr.get("title", ""),
            "labels": [l.get("name", "") for l in pr.get("labels", [])],
            "head_branch": (pr.get("head") or {}).get("ref", ""),
            "head_sha": (pr.get("head") or {}).get("sha", ""),
            "merge_sha": merge_sha,
            "commits": group["commits"],
            "files": files,
            "subject": git_subject(repo_path, merge_sha) if git_object_exists(repo_path, merge_sha) else pr.get("title", ""),
        })
    if direct:
        landings.append({
            "kind": "DIRECT_PUSH",
            "pr": None,
            "pr_url": "",
            "pr_title": "",
            "labels": [],
            "head_branch": "",
            "head_sha": "",
            "merge_sha": direct[-1],
            "commits": direct,
            "files": [{"path": p, "status": ""} for p in sorted(compare_files)],
            "subject": git_subject(repo_path, direct[-1]) if git_object_exists(repo_path, direct[-1]) else "",
        })
    return landings


def _pr_files(client, number):
    out, page = [], 1
    while True:
        chunk = client.get(f"/pulls/{number}/files?per_page=100&page={page}")
        items = chunk if isinstance(chunk, list) else []
        out.extend(items)
        if len(items) < 100:
            return out
        page += 1


# ------------------------------------------------------------ verification

def verify_faithfulness(repo_path, landing, tip_sha, head_fetcher=None):
    """Returns a list of defect dicts (empty = faithful).

    A PR head that is not in the local object store (the squash-merge
    shape: the head commit is no ancestor of main) is fetched via
    head_fetcher first; if it still cannot be obtained, the landing is
    UNVERIFIABLE — never silently skipped, because a skipped blob check
    wearing an OK verdict is precisely the failure this tool exists
    to abolish."""
    defects = []
    merge_sha = landing["merge_sha"]
    if not git_object_exists(repo_path, merge_sha):
        return [{
            "class": "FAITHFULNESS_UNVERIFIABLE",
            "detail": f"merge commit {merge_sha} not present in the local clone",
        }]
    if not git_object_exists(repo_path, tip_sha):
        return [{
            "class": "FAITHFULNESS_UNVERIFIABLE",
            "detail": f"tip {tip_sha} not present in the local clone",
        }]
    if not git_is_ancestor(repo_path, merge_sha, tip_sha):
        defects.append({
            "class": "FAITHFULNESS_NOT_ANCESTOR",
            "detail": f"merge commit {merge_sha} is not an ancestor of tip {tip_sha} "
                      "(history moved without it — rewritten or orphaned landing)",
        })
        return defects  # blob comparison across rewritten history is meaningless
    head_sha = landing.get("head_sha") or ""
    if landing["kind"] != "PR_MERGE" or not head_sha:
        return defects  # direct pushes carry no head to be faithful to
    if not git_object_exists(repo_path, head_sha):
        if head_fetcher is not None:
            head_fetcher(landing.get("pr"), head_sha)
        if not git_object_exists(repo_path, head_sha):
            return defects + [{
                "class": "FAITHFULNESS_UNVERIFIABLE",
                "detail": f"PR head {head_sha} is not in the local clone and "
                          "could not be fetched — blob identity not checked",
            }]
    for f in landing["files"]:
        path, status = f["path"], f.get("status", "")
        b_head = git_blob_at(repo_path, head_sha, path)
        b_merge = git_blob_at(repo_path, merge_sha, path)
        b_tip = git_blob_at(repo_path, tip_sha, path)
        if status == "removed":
            if b_merge is not None or b_tip is not None:
                defects.append({
                    "class": "FAITHFULNESS_BLOB_DRIFT", "path": path,
                    "detail": "file the PR deleted is present at the merge commit or the tip (resurrected)",
                })
            continue
        if b_head != b_merge:
            defects.append({
                "class": "FAITHFULNESS_BLOB_DRIFT", "path": path,
                "detail": f"blob at PR head ({b_head}) != blob at merge commit ({b_merge}) — "
                          "what was reviewed is not what landed",
            })
            continue
        if b_tip != b_merge and not git_path_touched_between(repo_path, merge_sha, tip_sha, path):
            defects.append({
                "class": "FAITHFULNESS_BLOB_DRIFT", "path": path,
                "detail": f"blob at tip ({b_tip}) != blob at merge commit ({b_merge}) and no "
                          "later commit in merge..tip touched the path — the landing's bytes moved",
            })
    return defects


def verify_surface(landing, fetcher):
    """Live-surface liveness for Hub landings. Returns defect dict or None."""
    if not any(f["path"].startswith(HUB_PREFIXES) for f in landing["files"]):
        return None
    try:
        status, body = fetcher(SURFACE_URL)
    except Exception as exc:  # a fetch failure is evidence, not a crash
        return {"class": "SURFACE_DOWN", "detail": f"surface fetch failed: {exc}"}
    if status != 200:
        return {"class": "SURFACE_DOWN", "detail": f"GET {SURFACE_URL} -> {status}"}
    if SURFACE_MARKER not in body:
        return {"class": "SURFACE_DOWN",
                "detail": f"GET {SURFACE_URL} -> 200 but the feed marker {SURFACE_MARKER} is absent"}
    return None


def http_fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "post-merge-guardian"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""


def derive_red_verdicts(before_sets, failing_after):
    """The L636 derivation, per workflow failing after a push.

    before_sets is check_sets() at the parent commit: (failing,
    pending, completed). A charge requires proof the check was green
    before: only a workflow PRESENT at the parent and completed
    not-failing there can derive NEW_RED. Failing on both sides is
    INHERITED. Absent at the parent (no check-run at all) or still
    pending there, the before-state is unknowable: UNKNOWN — recorded
    on the run's report, never charged, never revert-prepped, never
    alarmed. Returns {name: {"before", "after", "verdict"}}.
    """
    failing_before, pending_before, completed_before = before_sets
    derivation = {}
    for name in sorted(failing_after):
        if name in failing_before:
            before_state, verdict = "failing", "INHERITED"
        elif name in pending_before:
            before_state, verdict = "pending", "UNKNOWN"
        elif name in completed_before:
            before_state, verdict = "passing", "NEW_RED"
        else:
            before_state, verdict = "absent", "UNKNOWN"
        derivation[name] = {
            "before": before_state, "after": "failing", "verdict": verdict,
        }
    return derivation


def diff_reds(client, before, after, wait_secs=0, poll_secs=30, sleep=time.sleep, now=time.monotonic):
    """New-red attribution for a push. Polls until the after-set settles.

    Charges come from derive_red_verdicts (L636): set difference alone
    is NOT attribution — a name missing from the before-set may be an
    inherited red, a proven new red, or a check that never ran at the
    parent (UNKNOWN). The result carries the full derivation and both
    failing-set counts so the guardian's own output shows its work.
    """
    before_sets = check_sets(client, before)
    deadline = now() + wait_secs
    while True:
        failing_after, pending_after, _ = check_sets(client, after)
        if not pending_after or now() >= deadline:
            break
        sleep(poll_secs)
    derivation = derive_red_verdicts(before_sets, failing_after)
    return {
        "failing_before": sorted(before_sets[0]),
        "failing_after": sorted(failing_after),
        "failing_before_count": len(before_sets[0]),
        "failing_after_count": len(failing_after),
        "derivation": derivation,
        "new_reds": sorted(n for n, d in derivation.items()
                           if d["verdict"] == "NEW_RED"),
        "unknown_reds": sorted(n for n, d in derivation.items()
                               if d["verdict"] == "UNKNOWN"),
        "pending_after": sorted(pending_after),
    }


# ------------------------------------------------------------------- tier

def classify_tier(repo_path, title, paths):
    """Reuse the Balanced Machine step-1 classifier when it is on the tree
    (PR #2856's tools/pr_flow_tier.py); never a second classifier."""
    tools_dir = os.path.join(repo_path, "tools")
    if os.path.isfile(os.path.join(tools_dir, "pr_flow_tier.py")):
        try:
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            import pr_flow_tier  # type: ignore
            return pr_flow_tier.classify_tier(title, paths)
        except Exception:
            return None
    return None


# -------------------------------------------------------------------- act

def is_revert_landing(landing):
    """A guardian revert landing is verified but never revert-prepped."""
    if REVERT_LABEL in (landing.get("labels") or []):
        return True
    if (landing.get("head_branch") or "").startswith("guardian/revert-"):
        return True
    return REVERT_LABEL in (landing.get("subject") or "")


def evidence_markdown(record):
    """The detection evidence — the revert PR's scorecard substitute and
    the substance of the board alarm. One shape, both surfaces."""
    lines = [
        "## Post-Merge Guardian — verified escape",
        "",
        f"**Landing:** `{record['merge_sha']}`"
        + (f" — PR #{record['pr']} ({record['pr_url']})" if record.get("pr") else
           f" — direct push ({record.get('kind')})"),
        f"**Subject:** {record.get('subject', '')}",
        f"**Verdict:** {record['verdict']} · **detected:** {record['ts']} · "
        f"**detection latency:** {record.get('detection_latency_s')}s after the landing commit",
        "",
        "**Defects (each independently derived, none claimed):**",
    ]
    for d in record.get("defects", []):
        where = f" `{d['path']}`" if d.get("path") else ""
        lines.append(f"- `{d['class']}`{where} — {d['detail']}")
    checks = record.get("checks") or {}
    if checks:
        lines += [
            "",
            f"**Tip checks before:** {', '.join(checks.get('failing_before') or []) or 'none failing'}",
            f"**Tip checks after:** {', '.join(checks.get('failing_after') or []) or 'none failing'}",
            f"**New reds charged to this landing:** {', '.join(checks.get('new_reds') or []) or 'none'}",
            f"**Failing-set counts (parent → this push):** "
            f"{checks.get('failing_before_count', len(checks.get('failing_before') or []))} → "
            f"{checks.get('failing_after_count', len(checks.get('failing_after') or []))}",
        ]
        if checks.get("unknown_reds"):
            lines.append(
                f"**Reds NOT charged — before-state UNKNOWN (absent or pending "
                f"at the parent, L636):** {', '.join(checks['unknown_reds'])}")
    lines += [
        "",
        "Prepared under the **HOUSE-FIRE LAW** (Shawn, 2026-10-21): revert first, "
        "diagnose second, fix forward third. This detection evidence is the "
        "revert's scorecard substitute — a safety action carries its proof with "
        "it. The guardian never merges; this revert lands on one different-seat "
        "scorecard through the normal protocol.",
        "",
        f"`{LAW_ID}` · merge `{record['merge_sha']}` · tip at detection `{record.get('tip_sha', '')}`",
    ]
    return "\n".join(lines)


def prepare_revert(repo_path, landing, tip_sha, pusher=None, pr_opener=None, pr_body=""):
    """Build the revert on a branch and open the GUARDIAN-REVERT PR.

    Effects are injectable (pusher, pr_opener) so tests exercise the real
    git machinery without network. Returns a cure dict; on a conflicting
    revert it returns {prepared: False, reason} — the alarm still fires.
    """
    merge_sha = landing["merge_sha"]
    branch = f"guardian/revert-{merge_sha[:10]}"
    scratch = f"{repo_path}-guardian-scratch"
    wt = os.path.join(scratch, f"revert-{merge_sha[:10]}")
    os.makedirs(scratch, exist_ok=True)
    try:
        _git(repo_path, "worktree", "add", "-b", branch, wt, tip_sha)
        commits = list(landing.get("commits") or [merge_sha])
        # Revert newest first; -m 1 for true merge commits (2+ parents).
        for sha in reversed(commits):
            args = ["revert", "--no-commit"]
            if len(git_parents(wt, sha)) >= 2:
                args += ["-m", "1"]
            args.append(sha)
            proc = _git(wt, *args, check=False)
            if proc.returncode != 0:
                _git(wt, "revert", "--abort", check=False)
                return {"prepared": False, "branch": branch,
                        "reason": f"git revert of {sha} conflicts: "
                                  f"{(proc.stderr or proc.stdout).strip()[:300]}"}
        if not _git(wt, "status", "--porcelain").stdout.strip():
            # The merge changed nothing relative to its first parent:
            # the defect is an omission (the reviewed change never
            # arrived), so there is no revert to make — the cure is to
            # apply the PR's own diff, which a seat prepares from the
            # evidence. Report it; never crash, never fake a revert.
            _git(wt, "revert", "--abort", check=False)
            return {"prepared": False, "branch": branch,
                    "reason": "reverting this merge is a no-op against its first "
                              "parent — the landing's defect is an omission (the "
                              "reviewed change never arrived); cure = apply the "
                              "PR's diff forward, prepared from the evidence above"}
        _git(wt, "commit", "-q", "-m",
             f"Revert {landing.get('subject', merge_sha)[:72]} [{REVERT_LABEL}]\n\n"
             f"Post-Merge Guardian ({LAW_ID}): verified escape on {merge_sha}. "
             "Revert first, diagnose second, fix forward third.")
        revert_sha = _git(wt, "rev-parse", "HEAD").stdout.strip()
        if pusher is not None:
            pusher(wt, branch)
        cure = {"prepared": True, "branch": branch, "revert_sha": revert_sha}
        if pr_opener is not None:
            cure.update(pr_opener(branch, landing, pr_body))
        return cure
    finally:
        _git(repo_path, "worktree", "remove", "--force", wt, check=False)
        _git(repo_path, "branch", "-D", branch, check=False)


def open_revert_pr(client):
    """Returns a pr_opener(branch, landing, body) bound to the real API."""
    def _open(branch, landing, body):
        pr = client.post("/pulls", {
            "title": f"[{REVERT_LABEL}] Revert: {landing.get('subject', '')[:80]}",
            "head": branch,
            "base": "main",
            "body": body,
        })
        try:
            client.post("/labels", {"name": REVERT_LABEL, "color": "b60205",
                                    "description": "Guardian-prepared revert of a verified bad landing"})
        except ApiError:
            pass  # label already exists
        try:
            client.post(f"/issues/{pr['number']}/labels", {"labels": [REVERT_LABEL]})
        except ApiError:
            pass
        return {"revert_pr": pr["number"], "revert_pr_url": pr.get("html_url", "")}
    return _open


def git_pusher(wt, branch):
    proc = _git(wt, "push", "origin", f"HEAD:refs/heads/{branch}", check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"push of {branch} failed: {proc.stderr.strip()[:300]}")


# -------------------------------------------------------------------- log

class ListSink:
    def __init__(self):
        self.records = []

    def append(self, records):
        self.records.extend(records)


class FileSink:
    def __init__(self, path):
        self.path = path

    def append(self, records):
        with open(self.path, "a", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, sort_keys=True) + "\n")


class GitDataLogSink:
    """Appends records to guardian-log.jsonl on the live/guardian-log
    branch via the git-data API — the live/mission-state pattern. Pushes
    to that branch never trigger the guardian (it fires on main only)."""

    def __init__(self, client, branch=LOG_BRANCH, path=LOG_PATH):
        self.client = client
        self.branch = branch
        self.path = path

    def _ref_sha(self):
        try:
            return self.client.get(f"/git/refs/heads/{self.branch}")["object"]["sha"]
        except ApiError as exc:
            if exc.status != 404:
                raise
            main_sha = self.client.get("/git/refs/heads/main")["object"]["sha"]
            self.client.post("/git/refs", {"ref": f"refs/heads/{self.branch}", "sha": main_sha})
            return main_sha

    def append(self, records):
        tip = self._ref_sha()
        commit = self.client.get(f"/git/commits/{tip}")
        tree_sha = commit["tree"]["sha"]
        existing = ""
        try:
            content = self.client.get(f"/contents/{self.path}?ref={self.branch}")
            existing = base64.b64decode(content["content"]).decode("utf-8")
        except ApiError as exc:
            if exc.status != 404:
                raise
        new_text = existing + "".join(json.dumps(r, sort_keys=True) + "\n" for r in records)
        blob = self.client.post("/git/blobs", {
            "content": base64.b64encode(new_text.encode()).decode(), "encoding": "base64",
        })
        tree = self.client.post("/git/trees", {
            "base_tree": tree_sha,
            "tree": [{"path": self.path, "mode": "100644", "type": "blob", "sha": blob["sha"]}],
        })
        new_commit = self.client.post("/git/commits", {
            "message": f"guardian log: {len(records)} record(s) [{LAW_ID}]",
            "tree": tree["sha"],
            "parents": [tip],
        })
        self.client.patch(f"/git/refs/heads/{self.branch}",
                          {"sha": new_commit["sha"], "force": False})
        return new_commit["sha"]


# ------------------------------------------------------------- orchestrate

def run_guardian(client, repo_path, before, after, *,
                 fetcher=http_fetch, wait_secs=0, poll_secs=30,
                 sleep=time.sleep, act=True, sinks=(), board=DEFAULT_BOARD,
                 pusher=None, pr_opener=None, now_iso=None):
    """Verify every landing in before..after; act on verified escapes.

    Returns (records, exit_code). exit_code is 1 iff any landing escaped.
    """
    now_iso = now_iso or (lambda: datetime.now(timezone.utc).isoformat())
    landings = discover_landings(client, repo_path, before, after)
    # Anchor on the live ref, never on the push payload: if main moved
    # again after this push (or was rewritten), the guardian judges the
    # landing against the tip as it stands now.
    try:
        tip_sha = client.get("/git/refs/heads/main")["object"]["sha"]
    except ApiError:
        tip_sha = after
    if not git_object_exists(repo_path, tip_sha):
        _git(repo_path, "fetch", "origin", "main", check=False)
    reds = diff_reds(client, before, after, wait_secs=wait_secs,
                     poll_secs=poll_secs, sleep=sleep)
    records, exit_code = [], 0
    # New reds belong to the push; charge them to its head-most landing.
    head_most = landings[-1] if landings else None
    def _fetch_head(pr_number, _head_sha):
        if pr_number:
            _git(repo_path, "fetch", "origin", f"pull/{pr_number}/head",
                 check=False)

    for landing in landings:
        defects = verify_faithfulness(repo_path, landing, tip_sha,
                                      head_fetcher=_fetch_head)
        surface_defect = verify_surface(landing, fetcher)
        if surface_defect:
            defects.append(surface_defect)
        landing_checks = None
        if landing is head_most:
            landing_checks = reds
            for name in reds["new_reds"]:
                defects.append({
                    "class": "NEW_RED", "path": name,
                    "detail": f"check '{name}' was present and passing at "
                              f"{before[:10]} and fails at {after[:10]} — "
                              "proven new red (L636 derivation in checks.derivation); "
                              "this push turned it red",
                })
        revert = is_revert_landing(landing)
        hard_defects = [d for d in defects
                        if d["class"] != "FAITHFULNESS_UNVERIFIABLE"]
        if hard_defects and revert:
            verdict = "ESCAPE_ON_REVERT"
        elif hard_defects:
            verdict = "ESCAPE"
        elif defects or (landing is head_most and
                         (reds["pending_after"] or reds["unknown_reds"])):
            # Unverifiable bytes, unsettled checks, or reds whose
            # before-state derived UNKNOWN (absent/pending at the
            # parent): recorded in the log with the reason and the
            # derivation — pending proof, never a silent pass and
            # never an escape charged on evidence we do not have.
            verdict = "PENDING"
        else:
            verdict = "OK"
        merged_at = git_commit_time(repo_path, landing["merge_sha"]) \
            if git_object_exists(repo_path, landing["merge_sha"]) else ""
        detected = now_iso()
        latency = None
        if merged_at:
            try:
                m = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
                d = datetime.fromisoformat(detected.replace("Z", "+00:00"))
                latency = max(0, int((d - m).total_seconds()))
            except ValueError:
                latency = None
        record = {
            "v": 1, "law": LAW_ID, "ts": detected,
            "push": {"before": before, "after": after},
            "kind": landing["kind"], "pr": landing.get("pr"),
            "pr_url": landing.get("pr_url", ""),
            "subject": landing.get("subject", ""),
            "merge_sha": landing["merge_sha"], "head_sha": landing.get("head_sha", ""),
            "tip_sha": tip_sha,
            "tier": classify_tier(repo_path, landing.get("pr_title", ""),
                                  [f["path"] for f in landing["files"]]),
            "files": [f["path"] for f in landing["files"]],
            "verdict": verdict, "defects": defects,
            "defect_classes": sorted({d["class"] for d in defects}),
            "checks": landing_checks, "detection_latency_s": latency,
            "cure": None,
        }
        if verdict in ("ESCAPE", "ESCAPE_ON_REVERT"):
            exit_code = 1
            body = evidence_markdown(record)
            if verdict == "ESCAPE" and act:
                cure = prepare_revert(
                    repo_path, landing, tip_sha,
                    pusher=pusher, pr_body=body,
                    pr_opener=pr_opener or open_revert_pr(client))
                record["cure"] = cure
                if cure.get("prepared") and cure.get("revert_pr_url"):
                    body += (f"\n\n**Revert prepared:** {cure['revert_pr_url']} "
                             f"(branch `{cure['branch']}`) — one different-seat "
                             "scorecard lands it.")
                elif not cure.get("prepared"):
                    body += (f"\n\n**Revert preparation failed:** {cure.get('reason', '')}\n"
                             "The escape stands verified; the revert must be prepared "
                             "by hand — now, not watched.")
            alarm = body if verdict == "ESCAPE" else (
                body + f"\n\n**This escape is ON a [{REVERT_LABEL}] landing.** No "
                       "revert-of-a-revert was prepared (loop guard); a seat takes "
                       "the fix forward from here.")
            if act:
                client.post(f"/issues/{board}/comments", {"body": alarm})
                record["alarm_posted"] = True
        records.append(record)
    for sink in sinks:
        sink.append(records)
    return records, exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(description="Post-Merge Guardian (HOUSE-FIRE LAW)")
    parser.add_argument("--before", required=True, help="push before SHA (tip prior to the push)")
    parser.add_argument("--after", required=True, help="push after SHA (new tip)")
    parser.add_argument("--repo-path", default=".", help="local clone containing the objects")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--board", type=int, default=DEFAULT_BOARD)
    parser.add_argument("--wait-secs", type=int, default=1500,
                        help="budget for the tip's checks to settle before PENDING")
    parser.add_argument("--poll-secs", type=int, default=30)
    parser.add_argument("--no-act", action="store_true",
                        help="detect + log only: no revert PR, no board alarm")
    parser.add_argument("--log-file", default="",
                        help="also append records to this local JSONL file")
    args = parser.parse_args(argv)

    if args.before == ZERO_SHA:
        print(json.dumps({"law": LAW_ID, "verdict": "SKIP",
                          "reason": "branch creation push — no prior tip to diff against"}))
        return 0
    client = GHClient(repo=args.repo)
    sinks = [GitDataLogSink(client)]
    if args.log_file:
        sinks.append(FileSink(args.log_file))
    records, exit_code = run_guardian(
        client, args.repo_path, args.before, args.after,
        wait_secs=args.wait_secs, poll_secs=args.poll_secs,
        act=not args.no_act, sinks=sinks, board=args.board,
        pusher=git_pusher,
    )
    print(json.dumps({"law": LAW_ID, "records": records}, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
