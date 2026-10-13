#!/usr/bin/env python3
"""Post-merge authority audit (L245, B-25).

"Invalid merge authority -> revert, then re-invoke." The pre-merge gate
(tools/assemble_merge_packet.py, wired into merge-consensus-gate.yml) is
advisory until branch protection requires it — so this audit is the teeth:
it re-checks recent main commits' authority packets and, on an invalid
merge, OPENS A REVERT PR (propose + report, never auto-merge) with a
tree-verified revert, then hands the re-invocation lane the gated PR
(the #2455 -> #2459 pattern, machine-executed).

Coverage: every first-parent commit in the window, not just multi-parent
merges — squash merges and direct pushes are the exact class L245 exists
for, and skipping them would be fail-open.

Per commit, the verdict is one of:
  PACKET_VALID        - the "Verify merge authority" check ran green on the
                        exact merged head (protocol-complete evidence)
  EXERCISED_AUTHORITY - the merge COMMIT's author identity is the
                        director's own (Shawn Vibert
                        <humanmaximuscodex@gmail.com>). Recorded, NOT
                        flagged. A director merge is exercised authority,
                        distinct from protocol-complete evidence.
                        REPAIR NOTE (2026-10-13, B-25 repair round, Naya 4
                        review 5500983723 on PR #2514): the discriminator
                        USED to be `merged_by == "SoulSchoolAcademy"`.
                        Live API evidence showed `merged_by` is the org
                        login on 5/5 sampled merges spanning both classes
                        (director clicks #2421/#2459 AND lane merges
                        #2511/#2503/#2506) — the old rule made EVERY PR
                        merge read as the director's own click, so the
                        INVALID branch was unreachable and the audit's
                        stated function ("this audit is the teeth") did not
                        hold. The discriminator is now the merge commit's
                        author name/email, as the merge-watch uses.
                        `merged_by` remains in receipts as informational
                        text only — it is NEVER consulted for the verdict.
                        ACCEPTED RESIDUAL: the missing-evidence case (a
                        director merge with no packet) is NOT flagged by
                        this tool — flagging director merges is B-24's
                        queued breach-post watchdog entry, which is not yet
                        built. Until it lands, such merges are recorded
                        here with evidence_complete=False and nothing
                        follows up.
  INVALID             - neither packet nor exercised authority: open the
                        revert PR, post the venue receipt.
  SKIP                - the tool's own revert PR (no ping-pong), or a commit
                        that already carries an open revert PR.

Fail-closed: API failure -> exit 2 "unable to verify" with plain words.
If the merge-consensus workflow no longer defines the authority job the
audit depends on, the audit refuses to run (exit 2) rather than reading
absence of signal as guilt.
--dry-run prints verdicts and the revert plan without opening anything.

Dedup: a commit that already carries an open revert PR is skipped, never
double-filed.

Usage:
  python3 tools/authority_audit.py [--window-hours 24] [--venue 2175]
      [--dry-run] [--json] [--repo OWNER/REPO]

Exit codes: 0 = audit complete (verdicts reported); 1 = at least one
INVALID commit found (revert PRs opened or planned); 2 = unable to audit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
# NOTE: authority_audit.py deliberately does NOT import DIRECTOR_LOGIN from
# assemble_merge_packet. That constant encodes the falsified premise
# (`merged_by == "SoulSchoolAcademy"` == the director's own click) — the
# B-25 repair round (2026-10-13, Naya 4 review 5500983723) voided it.

GH_API_BIN = os.environ.get("GH_API_BIN", "gh")
AUTHORITY_CHECK_NAME = "Verify merge authority"
AUTHORITY_JOB_FILE = ".github/workflows/merge-consensus-gate.yml"
REVERT_BRANCH_PREFIX = "revert/"
REVERT_MARKER = "L245-REVERT-FOR:"
VENUE_DEFAULT = 2175

# The director's merge identity — the EXERCISED_AUTHORITY discriminator.
# Live evidence (Naya 4 review 5500983723, PR #2514): the director's own
# merge click authors the merge commit as `Shawn Vibert
# <humanmaximuscodex@gmail.com>`; a lane merge authors e.g. `Naya 5
# <naya5@soulschool.academy>`. `merged_by` on the live API is the org login
# on merges of both classes, so it can never discriminate and is never
# consulted for the verdict.
DIRECTOR_AUTHOR_NAME = "Shawn Vibert"
DIRECTOR_AUTHOR_EMAIL = "humanmaximuscodex@gmail.com"


def _is_director_commit(author_name: str, author_email: str) -> bool:
    """True iff the commit's git author identity is the director's own.

    Name and email are casefolded and stripped: GitHub display names are
    not case-stable, and a "shawn vibert" merge must not fail closed
    against the director's own click.

    NAMED RESIDUAL (forgeability): git author identity is UNAUTHENTICATED —
    anyone with push access can set user.name/user.email to the director's
    pair, and this discriminator will then return True (EXERCISED_AUTHORITY,
    recorded-not-flagged, nothing follows up until B-24's watchdog lands).
    The repair trades the old vacuous signal (merged_by, wrong on 100% of
    live merges) for a forgeable one (git author, right on 6/6 live merges
    but spoofable by a malicious pusher). The audit cannot mint trust the
    platform didn't sign. Live-byte check 2026-10-13: the commits API
    returns NO `verification` payload on any sampled merge commit, so
    signature-gating is unavailable — requiring verified==True would
    INVALID the director's own clicks.
    NAMED RISK (false INVALID): a director merge authored from a device
    using a ...@users.noreply.github.com variant address fails closed to
    INVALID. Unobserved on live bytes (6/6 use the canonical address), so
    no invented variants list — the risk is named, not guessed.
    """
    return (author_name.strip().casefold()
            == DIRECTOR_AUTHOR_NAME.casefold()
            and (author_email or "").strip().casefold()
            == DIRECTOR_AUTHOR_EMAIL.casefold())


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, repo: str):
        self.repo = repo

    def _api(self, path: str, method: str = "GET",
             body: dict | None = None) -> object:
        cmd = [GH_API_BIN, "api", f"repos/{self.repo}/{path}"]
        if method != "GET":
            cmd += ["-X", method]
        if body is not None:
            cmd += ["--input", "-"]
        try:
            out = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60,
                input=json.dumps(body) if body is not None else None,
                check=False)
        except Exception as e:  # noqa: BLE001 - fail closed
            raise GitHubError(f"gh api failed for {path}: {e}")
        if out.returncode != 0:
            raise GitHubError(
                f"gh api {method} {path} exited {out.returncode}: "
                f"{(out.stderr or out.stdout).strip()[:200]}")
        try:
            return json.loads(out.stdout.strip() or "null")
        except json.JSONDecodeError as e:
            raise GitHubError(f"gh api {path} returned malformed JSON: {e}")

    def _paged(self, path: str) -> list:
        items: list = []
        page = 1
        while True:
            chunk = self._api(f"{path}?per_page=100&page={page}")
            if not isinstance(chunk, list) or not chunk:
                break
            items.extend(chunk)
            if len(chunk) < 100:
                break
            page += 1
        return items

    def list_main_commits(self, since: datetime) -> list:
        """Every first-parent commit to main since `since` (newest first).

        The first-parent chain is walked explicitly: the flat
        `commits?sha=main` listing is reverse-chronological, NOT
        first-parent, and would audit branch heads that were never
        first-parent tips. Multi-parent merges AND single-parent commits
        are both audited — squash merges and direct pushes get zero audit
        under a merges-only enumeration, and those are precisely the
        unauthorized-authority class.
        """
        try:
            tip = self._api("git/refs/heads/main")["object"]["sha"]
        except (GitHubError, KeyError, TypeError) as e:
            raise GitHubError(f"cannot resolve main tip: {e}")
        out = []
        sha = tip
        for _ in range(1000):  # safety bound; windows are hours, not years
            if not sha:
                break
            c = self._api(f"commits/{sha}")
            if not isinstance(c, dict):
                raise GitHubError(f"commits/{sha} did not return an object")
            parents = [p.get("sha", "") for p in c.get("parents", [])]
            date_s = (((c.get("commit") or {}).get("committer") or {})
                      .get("date", ""))
            try:
                committed = datetime.fromisoformat(
                    date_s.replace("Z", "+00:00"))
            except ValueError:
                break
            if committed < since:
                break
            author = c.get("author") or {}
            commit_author = (c.get("commit") or {}).get("author") or {}
            out.append({
                "sha": c.get("sha", ""),
                "message": (c.get("commit") or {}).get("message", ""),
                "parents": parents,
                "author_login": author.get("login") or "",
                # The exercised-authority discriminator keys on the git
                # author identity (name/email), never on `merged_by`
                # (B-25 repair round, 2026-10-13).
                "author_name": commit_author.get("name") or "",
                "author_email": commit_author.get("email") or "",
                "date": date_s,
            })
            sha = parents[0] if parents else ""
        return out

    def get_pr(self, pr: int) -> dict:
        data = self._api(f"pulls/{pr}")
        if not isinstance(data, dict):
            raise GitHubError(f"pulls/{pr} did not return a PR object")
        return data

    def authority_check_passed(self, head_sha: str) -> bool:
        data = self._api(
            f"commits/{head_sha}/check-runs?per_page=100")
        runs = data.get("check_runs", []) if isinstance(data, dict) else []
        for cr in runs:
            if cr.get("name") == AUTHORITY_CHECK_NAME:
                return cr.get("conclusion") == "success"
        return False

    def open_revert_pr(self, branch: str, title: str, body: str,
                       base: str = "main") -> dict:
        data = self._api("pulls", method="POST", body={
            "title": title, "head": branch, "base": base, "body": body,
            "draft": False,
        })
        if not isinstance(data, dict):
            raise GitHubError("pulls POST did not return a PR object")
        return data

    def find_open_revert_pr(self, sha: str) -> dict | None:
        """Dedup: exact head-ref match only. The 8-hex title disjunct was
        dropped — it could false-match an unrelated PR whose title happens
        to contain the same 8 hex chars. Revert PRs opened by this tool use
        the exact ref "revert/<short>"; manual revert PRs are not deduped
        here (harmless duplicate is better than a wrong one)."""
        prs = self._paged("pulls?state=open&per_page=100")
        want = f"{REVERT_BRANCH_PREFIX}{sha[:8]}"
        for p in prs:
            if (p.get("head") or {}).get("ref", "") == want:
                return p
        return None

    def post_venue_comment(self, venue: int, body: str) -> dict:
        data = self._api(f"issues/{venue}/comments", method="POST",
                         body={"body": body})
        if not isinstance(data, dict):
            raise GitHubError("venue comment POST failed")
        return data


_MERGE_PR_RE = re.compile(r"Merge pull request #(\d+)")
_AUTHORITY_JOB_RE = re.compile(
    r"(?m)^\s*name:\s*Verify merge authority\s*$")


def authority_job_present(repo_dir: Path) -> bool:
    """The audit's PACKET_VALID path depends on the workflow defining the
    authority job. If the job is gone (renamed/removed), absence of signal
    must NEVER read as guilt — the audit refuses to run instead."""
    try:
        text = (repo_dir / AUTHORITY_JOB_FILE).read_text()
    except OSError:
        return False
    return bool(_AUTHORITY_JOB_RE.search(text))


def _run_git(args: list[str], cwd: Path) -> str:
    out = subprocess.run(["git"] + args, capture_output=True, text=True,
                         cwd=str(cwd), timeout=120, check=False)
    if out.returncode != 0:
        raise GitHubError(
            f"git {' '.join(args)} failed: "
            f"{(out.stderr or out.stdout).strip()[:300]}")
    return out.stdout.strip()


def _push_branch(repo_dir: Path, branch: str) -> None:
    _run_git(["push", "origin", branch], repo_dir)


def build_revert(repo_dir: Path, sha: str, base_sha: str,
                 is_merge: bool) -> dict:
    """Create the revert commit. Returns branch + tree-verification.

    The revert is tree-verified: `git diff <base> <revert-head>` must be
    EMPTY for the revert to be byte-identical to the pre-commit tip, where
    base is the merge's first parent (multi-parent) or the commit's parent
    (single). A non-empty diff means later commits touched the same files —
    reported honestly, never claimed clean. A conflicting revert is aborted
    and reported as conflict=True; the repo is left with a clean tree on
    main — the tool never leaves a conflicted tree behind.
    """
    branch = f"{REVERT_BRANCH_PREFIX}{sha[:8]}"
    # Fresh base: the scheduled job's full clone is current, but a manual
    # run's origin/main may be stale — fetch first so the revert builds on
    # the true current tip rather than yesterday's.
    _run_git(["fetch", "origin", "main"], repo_dir)
    _run_git(["checkout", "-B", branch, "origin/main"], repo_dir)
    args = (["revert", "-m", "1", "--no-edit", sha] if is_merge
            else ["revert", "--no-edit", sha])
    try:
        _run_git(args, repo_dir)
    except GitHubError as revert_err:
        # Abort only if a revert actually started: a failed-to-start revert
        # (bad sha, shallow boundary, empty) has nothing to abort, and a
        # failing abort would mask the original error.
        try:
            _run_git(["revert", "--abort"], repo_dir)
            was_in_progress = True
        except GitHubError:
            was_in_progress = False
        _run_git(["checkout", "-q", "main"], repo_dir)
        if was_in_progress:
            return {"branch": branch, "revert_head": None,
                    "tree_verified": False, "diff_stat": "",
                    "conflict": True}
        raise GitHubError(
            f"revert of {sha[:8]} failed without starting: {revert_err}")
    revert_head = _run_git(["rev-parse", "HEAD"], repo_dir)
    diff_stat = _run_git(["diff", "--stat", base_sha, revert_head], repo_dir)
    return {
        "branch": branch,
        "revert_head": revert_head,
        "tree_verified": diff_stat == "",
        "diff_stat": diff_stat,
        "conflict": False,
    }


def _pr_number_of(message: str) -> int | None:
    """PR number from a merge/squash commit message.

    GitHub merge commits: "Merge pull request #N from ...".
    GitHub squash merges: "<PR title> (#N)" on the SUBJECT line, followed
    by the PR body. The squash pattern is matched against the subject line
    ONLY — anchoring at end-of-message misclassified every squash merge
    that carries a body (this team's pre-submit rule requires a body on
    every PR) as "names no PR", a spurious INVALID -> spurious revert PR.
    """
    m = _MERGE_PR_RE.search(message or "")
    if m:
        return int(m.group(1))
    subject = (message or "").split("\n", 1)[0]
    m = re.search(r"\(#(\d+)\)", subject)
    if m:
        return int(m.group(1))
    return None


def _open_invalid_revert(client: GitHubClient, sha: str, base_sha: str,
                         is_merge: bool, pr_number: int | None,
                         merged_by: str, head_sha: str, repo_dir: Path,
                         venue: int, dry_run: bool,
                         reason: str, actor_key: str = "merged_by") -> dict:
    """INVALID path: propose + report, never auto-merge.

    actor_key names the record field for who acted: "merged_by" on the PR
    path (the PR's merged_by value, informational only — never the
    discriminator), "actor" on the no-PR path (a direct push has no
    merged_by; mislabeling it would smuggle a PR field where none exists).
    """
    revert = build_revert(repo_dir, sha, base_sha, is_merge)
    pr_ref = f"PR #{pr_number}" if pr_number else "no PR"
    if revert["conflict"]:
        # No revert commit exists: the venue post IS the proposal record.
        # Never push an empty branch, never open an empty PR.
        if not dry_run:
            client.post_venue_comment(venue,
                f"**L245 authority audit:** {sha[:8]} ({pr_ref}) verdict "
                f"INVALID ({reason}) — the mechanical revert CONFLICTS with "
                f"later commits (no revert commit created). Manual revert "
                f"required; re-invocation lane owns the gated follow-up.")
        return {"verdict": "INVALID", "reason": reason,
                "authority_basis": "none", "evidence_complete": False,
                actor_key: merged_by, "conflict": True,
                "revert_pr": None, "dry_run": dry_run}

    title = (f"Revert \"{sha[:8]}\" (L245 authority audit)")
    body = (
        f"<!-- {REVERT_MARKER} {sha} -->\n"
        f"## Authority audit verdict: INVALID\n\n"
        f"Commit {sha} ({pr_ref}, by {merged_by}) — {reason}.\n\n"
        f"Per L245 (\"Invalid merge authority -> revert, then re-invoke\") "
        f"this revert is PROPOSED, never auto-merged.\n\n"
        f"### Tree verification\n\n"
        + ("`git diff <base> <revert-head>` is EMPTY — the revert restores "
           "the pre-commit tree byte-identically.\n"
           if revert["tree_verified"] else
           "WARNING: the revert diff vs the base is NOT empty "
           "(later commits touched the same files) — manual review required:\n"
           f"```\n{revert['diff_stat'][:2000]}\n```\n")
        + f"\n### Next\n\nThe re-invocation lane owns the gated follow-up "
          f"(the #2455 -> #2459 pattern): rebuild the change with a valid "
          f"authority packet, then merge under protocol.\n"
    )
    pr_number_out = None
    if not dry_run:
        _push_branch(repo_dir, revert["branch"])
        try:
            opened = client.open_revert_pr(revert["branch"], title, body)
        except GitHubError:
            # Never leave an orphan branch behind on PR-open failure.
            try:
                _run_git(["push", "origin", "--delete", revert["branch"]],
                         repo_dir)
            except GitHubError:
                pass
            raise
        pr_number_out = opened.get("number")
        client.post_venue_comment(venue,
            f"**L245 authority audit:** {sha[:8]} ({pr_ref}) verdict "
            f"INVALID ({reason}) — revert PR #{pr_number_out} opened "
            f"(propose + report, never auto-merge). "
            f"Tree-verified: {revert['tree_verified']}. "
            f"Re-invocation lane owns the gated follow-up.")
    return {"verdict": "INVALID", "reason": reason,
            "authority_basis": "none", "evidence_complete": False,
            actor_key: merged_by, "conflict": False,
            "tree_verified": revert["tree_verified"],
            "revert_branch": revert["branch"],
            "revert_pr": pr_number_out, "dry_run": dry_run}


def audit_commit(client: GitHubClient, commit: dict, repo_dir: Path,
                 venue: int, dry_run: bool) -> dict:
    sha = commit["sha"]
    parents = commit["parents"]
    is_merge = len(parents) >= 2
    base_sha = parents[0] if parents else ""
    pr_number = _pr_number_of(commit["message"])

    if pr_number is not None:
        pr = client.get_pr(pr_number)
        head_sha = ((pr.get("head") or {}).get("sha")) or ""
        head_ref = ((pr.get("head") or {}).get("ref")) or ""
        pr_body = pr.get("body") or ""
        merged_by = ((pr.get("merged_by") or {}).get("login")) or ""

        # No ping-pong: the tool's own revert PRs are never audited.
        if (head_ref.startswith(REVERT_BRANCH_PREFIX)
                and REVERT_MARKER in pr_body):
            return {"sha": sha, "pr": pr_number, "verdict": "SKIP",
                    "reason": "own L245 revert PR — not audited"}
    else:
        head_sha = ""
        merged_by = ""

    # Dedup, hoisted above the PR/no-PR fork: a commit that already carries
    # an open revert PR is skipped, never double-filed — the module's
    # documented guarantee. Previously this ran only on the PR branch, so a
    # direct-push INVALID opened a fresh revert PR on every audit run (and
    # build_revert's `checkout -B` resets the branch each time, so run N+1
    # opened PR #2, #3, ...).
    existing = client.find_open_revert_pr(sha)
    if existing:
        record = {"sha": sha, "verdict": "SKIP",
                  "reason": f"revert PR already open: "
                            f"#{existing.get('number')}"}
        if pr_number is not None:
            record["pr"] = pr_number
        return record

    if pr_number is not None:
        if head_sha and client.authority_check_passed(head_sha):
            return {"sha": sha, "pr": pr_number, "verdict": "PACKET_VALID",
                    "reason": f"'{AUTHORITY_CHECK_NAME}' green on head "
                              f"{head_sha[:8]}",
                    "authority_basis": "packet", "evidence_complete": True}

        # Exercised authority: the merge COMMIT's author identity is the
        # director's own. `merged_by` is NOT consulted — on the live API it
        # is the org login for merges of both classes (B-25 repair round,
        # 2026-10-13, Naya 4 review 5500983723).
        commit_author_name = commit.get("author_name") or ""
        commit_author_email = commit.get("author_email") or ""
        if _is_director_commit(commit_author_name, commit_author_email):
            return {"sha": sha, "pr": pr_number,
                    "verdict": "EXERCISED_AUTHORITY",
                    "reason": f"merge-commit author is the director "
                              f"({commit_author_name} <{commit_author_email}>) "
                              f"— exercised authority, recorded not flagged; "
                              f"missing-evidence case is an accepted "
                              f"residual pending B-24's watchdog (not yet "
                              f"built)",
                    "authority_basis": "exercised",
                    "evidence_complete": False, "merged_by": merged_by}

        return {"sha": sha, "pr": pr_number, **_open_invalid_revert(
            client, sha, base_sha, is_merge, pr_number,
            merged_by or "unknown", head_sha, repo_dir, venue, dry_run,
            reason="no authority packet, no exercised authority")}

    # No PR reference: authority unprovable. The commit's own author is the
    # exercised-authority fallback (a direct push by the director is his
    # click, not an invalid merge). Identity keys on the git author
    # name/email, never the linked login (B-25 repair round, 2026-10-13).
    author_name = commit.get("author_name") or ""
    author_email = commit.get("author_email") or ""
    author_login = commit.get("author_login") or ""
    if _is_director_commit(author_name, author_email):
        return {"sha": sha, "verdict": "EXERCISED_AUTHORITY",
                "reason": f"direct push by the director ({author_name} "
                          f"<{author_email}>) — exercised authority, "
                          f"recorded not flagged",
                "authority_basis": "exercised", "evidence_complete": False,
                "actor": author_login}

    return {"sha": sha, **_open_invalid_revert(
        client, sha, base_sha, is_merge, None,
        author_login or "unknown", "", repo_dir, venue, dry_run,
        reason="names no PR — authority unprovable", actor_key="actor")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Post-merge authority audit (L245)")
    ap.add_argument("--window-hours", type=float, default=24.0)
    ap.add_argument("--venue", type=int, default=VENUE_DEFAULT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--repo-dir", default=".",
                    help="local clone of the repo (for building reverts)")
    ap.add_argument("--repo", default=os.environ.get(
        "REPO", "SoulSchoolAcademy/NayaPOWER"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    repo_dir = Path(args.repo_dir)

    # The PACKET_VALID path depends on the workflow defining the authority
    # job. If the job is gone, absence of signal must never read as guilt.
    if not authority_job_present(repo_dir):
        msg = (f"authority audit blind: '{AUTHORITY_CHECK_NAME}' job not "
               f"found in {AUTHORITY_JOB_FILE} — refusing to audit "
               f"(fail closed)")
        if args.json:
            print(json.dumps({"ok": False, "error": msg}))
        else:
            print(msg)
        return 2

    client = GitHubClient(args.repo)
    since = datetime.now(timezone.utc) - timedelta(hours=args.window_hours)
    try:
        commits = client.list_main_commits(since)
    except GitHubError as e:
        msg = f"unable to audit merge authority: {e} (fail closed)"
        if args.json:
            print(json.dumps({"ok": False, "error": msg}))
        else:
            print(msg)
        return 2

    verdicts = []
    for commit in commits:
        try:
            verdicts.append(audit_commit(
                client, commit, repo_dir, args.venue, args.dry_run))
        except GitHubError as e:
            verdicts.append({"sha": commit["sha"], "verdict": "ERROR",
                             "reason": f"unable to verify: {e}"})

    invalid = sum(1 for v in verdicts if v["verdict"] == "INVALID")
    report = {"window_hours": args.window_hours,
              "commits_seen": len(commits), "invalid": invalid,
              "verdicts": verdicts, "dry_run": args.dry_run}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"authority audit: {len(commits)} commits in window, "
              f"{invalid} INVALID")
        for v in verdicts:
            print(f"  {v['sha'][:8]} {v['verdict']}: "
                  f"{v.get('reason', '')[:120]}")
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())

