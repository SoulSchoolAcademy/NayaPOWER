#!/usr/bin/env python3
"""Build the DELEGATED-MERGE-AUTHORITY packet from real PR data (B-25).

L245: "Invalid merge authority -> revert, then re-invoke." The canonical
check (tools/protocol/checks/merge_authority.py) verifies a merge-to-main
packet, but nothing ever built that packet from real PR data — so the check
only ever fired when a human hand-fed it a hand-written record. This tool
closes that gap: it reads the live PR (head SHA, base, seat, reviews,
comments, check-runs) plus the venue thread, and emits the packet the check
verifies.

Fail-closed, always:
  - every packet field is derived from API data; a field that cannot be
    derived is left false/absent (the check then fails with its exact
    reason — absence fails closed, never defaults to permitted)
  - API failure / malformed data -> exit 2 "unable to verify" with plain
    words, never a traceback, never a guess

Exit codes:
  0 - packet assembled AND merge_authority PASS
  1 - packet assembled but authority FAIL (the check's exact reason printed)
  2 - unable to assemble (API down, malformed data) - fail closed

Provider seam: every GitHub read goes through GitHubClient. Tests inject
FakeGitHub with fixture payloads (zero network in tests). The real client
shells to `gh api` (GH_API_BIN env override exists for smoke tests).

Usage:
  python3 tools/assemble_merge_packet.py --pr 2510 [--repo OWNER/REPO]
      [--venue 2175] [--json] [--verify]

  --verify pipes the assembled packet into merge_authority.check and exits
  0/1/2 per the contract above. Without --verify the packet JSON is printed
  and the process exits 0 (assembly only).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_CHECKS_DIR = Path(__file__).resolve().parent / "protocol" / "checks"
sys.path.insert(0, str(_CHECKS_DIR.parent))  # `from checks import ...`
sys.path.insert(0, str(_CHECKS_DIR))          # `import merge_authority`
from checks import emit  # noqa: E402
import merge_authority  # noqa: E402

GH_API_BIN = os.environ.get("GH_API_BIN", "gh")
# Single source for the exercised-authority identity (B-25 fix #13):
# authority_audit.py imports this rather than defining its own.
DIRECTOR_LOGIN = "SoulSchoolAcademy"

# The check's canonical field name is legacy ("posted_to_1354" — the
# delegation's original venue). The team's coordination venue is #2175.
# The assembler checks the live venue and records WHICH venue in the
# evidence; the boolean keeps the check's canonical name.
DEFAULT_VENUE = 2175
LEGACY_VENUE = 1354  # the delegation's original venue, named in LAW-A03's
                     # ratified text

KERNEL_TESTS_WORKFLOW = Path(".github/workflows/kernel-tests.yml")


def _kernel_test_job_name(workflow_path: Path) -> str:
    """Resolve the kernel-test check-run name from the workflow file.

    GitHub names a check-run after the job's `name:` field, or the job id
    when no `name:` is set. Hardcoding "test" would silently break the
    moment someone adds a `name:` to kernel-tests.yml — the file is the
    source of truth for the name. Fail-closed: missing file, no jobs
    block, or an ambiguous multi-job file (no canonical `test` job id)
    raises instead of guessing.
    """
    try:
        text = workflow_path.read_text()
    except OSError as e:
        raise GitHubError(f"cannot read {workflow_path}: {e}")
    m = re.search(r"(?m)^jobs:\s*$", text)
    if not m:
        raise GitHubError(f"{workflow_path}: no jobs: block")
    job_ids: list[str] = []
    names: dict[str, str] = {}
    current: str | None = None
    for line in text[m.end():].splitlines():
        if re.match(r"^[A-Za-z]", line):
            break  # next top-level key: the jobs block is over
        jm = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if jm:
            current = jm.group(1)
            job_ids.append(current)
            continue
        if current:
            nm = re.match(r"^    name:\s*(.+?)\s*$", line)
            if nm:
                names[current] = nm.group(1).strip().strip("'\"")
    if not job_ids:
        raise GitHubError(f"{workflow_path}: no jobs found")
    if "test" in job_ids:
        job = "test"  # canonical kernel-test job id
    elif len(job_ids) == 1:
        job = job_ids[0]
    else:
        raise GitHubError(
            f"{workflow_path}: ambiguous kernel-test job {job_ids} — "
            "no canonical `test` job id")
    return names.get(job, job)


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    """Real provider: `gh api` against the repo."""

    def __init__(self, repo: str):
        self.repo = repo

    def _api(self, path: str, jq: str | None = None) -> object:
        cmd = [GH_API_BIN, "api", f"repos/{self.repo}/{path}"]
        if jq:
            cmd += ["--jq", jq]
        try:
            out = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60, check=False
            )
        except Exception as e:  # noqa: BLE001 - network/exec failure is fail-closed
            raise GitHubError(f"gh api failed for {path}: {e}")
        if out.returncode != 0:
            raise GitHubError(
                f"gh api {path} exited {out.returncode}: "
                f"{(out.stderr or out.stdout).strip()[:200]}"
            )
        text = out.stdout.strip()
        if jq:
            return text
        try:
            return json.loads(text)
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

    def get_pr(self, pr: int) -> dict:
        data = self._api(f"pulls/{pr}")
        if not isinstance(data, dict):
            raise GitHubError(f"pulls/{pr} did not return a PR object")
        return data

    def list_reviews(self, pr: int) -> list:
        return self._paged(f"pulls/{pr}/reviews")

    def list_pr_comments(self, pr: int) -> list:
        return self._paged(f"issues/{pr}/comments")

    def list_check_runs(self, head_sha: str) -> list:
        data = self._api(
            f"commits/{head_sha}/check-runs?per_page=100")
        if not isinstance(data, dict):
            raise GitHubError(f"check-runs for {head_sha} malformed")
        return data.get("check_runs", [])

    def list_venue_comments(self, venue: int) -> list:
        return self._paged(f"issues/{venue}/comments")


def _seat_from_branch(branch: str, author_login: str) -> str:
    """Seat = branch prefix before '/', else the author login.

    Convention: naya5/learn-..., naya2/b37-..., lane4/b60-..., brain-build/...

    TRUST BOUNDARY (round-3 G9): the branch prefix is a team convention, not
    an authenticated identity — anyone with push access could name a branch
    "naya5/x". This is accepted because the blast radius is bounded: the
    seat is used for evidence attribution and for the independent-validator
    comparison (validator must be a DIFFERENT seat's login naming the head
    SHA — spoofing the prefix cannot manufacture that). There is no
    login->seat roster in the repo; building one here would be a second
    identity mechanism. The evidence records seat_source so any consumer
    can see the attribution basis.
    """
    branch = (branch or "").strip()
    if "/" in branch:
        return branch.split("/", 1)[0]
    return (author_login or "").strip()


_SCORE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*10")
_VERDICT_RE = re.compile(r"verdict\s*:\s*(\d+(?:\.\d+)?)", re.IGNORECASE)
_FINAL_SCORE_RE = re.compile(
    r"final\s+score\s+(\d+(?:\.\d+)?)\s*/\s*10", re.IGNORECASE)


def _parse_scorecard(body: str, head_sha: str) -> dict | None:
    """A scorecard receipt names the exact head SHA. Return its parsed
    claims, or None if the body is not a head-pinned scorecard."""
    if head_sha not in body and head_sha[:8] not in body:
        return None
    lowered = body.lower()
    if "scorecard" not in lowered:
        return None
    score = None
    m = _FINAL_SCORE_RE.search(body) or _VERDICT_RE.search(body)
    if m:
        score = float(m.group(1))
    else:
        scores = [float(x) for x in _SCORE_RE.findall(body)]
        score = max(scores) if scores else None
    return {
        "score": score,
        "evidence_backed": "## evidence" in lowered,
        "value_calculus_run": ("value calculus" in lowered
                               or "value_calculus" in lowered),
        "report_planned": any(
            marker in lowered
            for marker in ("post-merge report", "report after", "sign-out",
                           "sign out")),
    }


def _latest_reviews_by_reviewer(reviews: list, head_sha: str) -> dict:
    """Latest review state per reviewer, but an APPROVAL only counts when it
    was given ON THE CURRENT HEAD (review commit_id == head_sha).

    A stale approval on an old head never validates the current head —
    otherwise a reviewer could approve v1 and the author could merge v2.
    """
    latest: dict = {}
    for r in reviews:
        user = (r.get("user") or {}).get("login", "")
        state = r.get("state", "")
        if not (user and state):
            continue
        if state == "APPROVED" and r.get("commit_id") != head_sha:
            # stale approval: recorded, never counted as validation
            latest[user] = "STALE_APPROVAL"
        else:
            latest[user] = state  # API returns chronological; last wins
    return latest


_PR_TAG_RE_CACHE: dict = {}
_SCORE_PATTERN_RE = re.compile(r"\d+(?:\.\d+)?\s*/\s*10")


def _pr_tag_re(pr_number: int) -> "re.Pattern":
    if pr_number not in _PR_TAG_RE_CACHE:
        _PR_TAG_RE_CACHE[pr_number] = re.compile(rf"#{pr_number}\b")
    return _PR_TAG_RE_CACHE[pr_number]


def _venue_posted(venue_comments: list, pr_number: int,
                  head_sha: str) -> tuple[bool, int | None, str]:
    """Intent + scorecard + validation posted on the venue.

    Strict derivation: a venue comment must name the PR (regex #N\\b — so
    #2510 never matches #25101), carry a score pattern (N.N/10 — the
    scorecard's verdict, not a bare "scorecard to follow" sign-in), AND
    name the head SHA (full or short). Returns (posted, comment_id, author).
    """
    tag = _pr_tag_re(pr_number)
    for c in venue_comments:
        body = c.get("body") or ""
        if not tag.search(body):
            continue
        if not _SCORE_PATTERN_RE.search(body):
            continue
        if head_sha not in body and head_sha[:8] not in body:
            continue
        return True, c.get("id"), ((c.get("user") or {}).get("login") or "")
    return False, None, ""


def _venue_posted_with_fallback(client, venue: int, pr_number: int,
                                head_sha: str) -> tuple[bool, int,
                                                       int | None, str]:
    """Check the live venue; fall back to the delegation's original venue.

    LAW-A03's ratified text names the original venue; the team moved
    coordination to #2175. A seat following the law's letter (posts on the
    original venue) must not be misread as missing authority — check the
    live venue first, then the legacy venue. Returns
    (posted, venue_used, comment_id, author).
    """
    comments = client.list_venue_comments(venue)
    posted, cid, author = _venue_posted(comments, pr_number, head_sha)
    if posted:
        return posted, venue, cid, author
    if venue != LEGACY_VENUE:
        comments = client.list_venue_comments(LEGACY_VENUE)
        posted, cid, author = _venue_posted(comments, pr_number, head_sha)
        if posted:
            return posted, LEGACY_VENUE, cid, author
    return False, venue, None, ""


def assemble(client: GitHubClient, pr_number: int,
             venue: int = DEFAULT_VENUE,
             repo_dir: Path | None = None,
             test_job: str | None = None) -> tuple[dict, dict]:
    """Returns (packet, evidence). Raises GitHubError on API failure.

    The kernel-test check-run name is resolved from the checkout's
    kernel-tests.yml (pass test_job explicitly to pin it, e.g. in tests).
    """
    pr = client.get_pr(pr_number)
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_sha = head.get("sha", "")
    head_ref = head.get("ref", "")
    base_ref = base.get("ref", "")
    author = (pr.get("user") or {}).get("login", "")
    if test_job is None:
        base_dir = repo_dir if repo_dir is not None else Path.cwd()
        test_job = _kernel_test_job_name(
            base_dir / ".github/workflows/kernel-tests.yml")

    if not head_sha:
        raise GitHubError(f"PR #{pr_number}: head SHA missing from API data")

    seat = _seat_from_branch(head_ref, author)

    # --- tests_green: latest check-runs on the exact head -----------------
    # Fail-closed on conclusions: anything that is not an explicit
    # success/skipped/neutral counts against green — cancelled, timed_out,
    # action_required, stale, and in-progress (conclusion null) are all
    # "not green". A gate that reads absence as green is fail-open.
    OK_CONCLUSIONS = {"success", "skipped", "neutral"}
    check_runs = client.list_check_runs(head_sha)
    latest: dict = {}
    for cr in check_runs:
        name = cr.get("name", "")
        # newest first is not guaranteed; keep the max completed_at
        prev = latest.get(name)
        stamp = cr.get("completed_at") or ""
        if prev is None or stamp >= (prev.get("completed_at") or ""):
            latest[name] = cr
    failures = [n for n, cr in latest.items()
                if cr.get("conclusion") not in OK_CONCLUSIONS]
    successes = [n for n, cr in latest.items()
                 if cr.get("conclusion") == "success"]
    # Resolved from kernel-tests.yml (G3) — never a hardcoded job name.
    test_ok = latest.get(test_job, {}).get("conclusion") == "success"
    tests_green = bool(test_ok and not failures)
    run_ids = sorted({str(cr.get("id"))
                      for cr in latest.values() if cr.get("id")})
    test_evidence = (
        f"CI check-runs on head {head_sha[:8]}: "
        f"{len(successes)} success / {len(failures)} failure "
        f"(run ids: {', '.join(run_ids[:8])})"
        if check_runs else ""
    )

    # --- self_scorecard: head-pinned ## SCORECARD on the PR ----------------
    comments = client.list_pr_comments(pr_number)
    best: dict | None = None
    scorecard_comment_id = None
    scorecard_comment_author = ""
    for c in comments:
        parsed = _parse_scorecard(c.get("body") or "", head_sha)
        if parsed and parsed["score"] is not None:
            if best is None or parsed["score"] > best["score"]:
                best = parsed
                scorecard_comment_id = c.get("id")
                scorecard_comment_author = (
                    (c.get("user") or {}).get("login") or "")
    self_scorecard = False
    if best is not None:
        self_scorecard = {
            "score": best["score"],
            "evidence_backed": best["evidence_backed"],
            "value_calculus_run": best["value_calculus_run"],
        }

    # --- independent_validator: approving review, different seat -----------
    # The approval must be ON THIS HEAD (commit_id == head_sha). A stale
    # approval on an old head never validates the current head — otherwise
    # a reviewer could approve v1 and the author could merge v2.
    reviews = client.list_reviews(pr_number)
    latest_reviews = _latest_reviews_by_reviewer(reviews, head_sha)
    approvers = [u for u, s in latest_reviews.items() if s == "APPROVED"]
    independent_validator = ""
    validator_commit_id = ""
    for approver in approvers:
        if merge_authority.seat_key(approver) != merge_authority.seat_key(seat):
            independent_validator = approver
            for r in reviews:
                if ((r.get("user") or {}).get("login") == approver
                        and r.get("state") == "APPROVED"
                        and r.get("commit_id") == head_sha):
                    validator_commit_id = head_sha
                    break
            break

    # --- posted_to_venue: intent + scorecard + validation on the venue -----
    # Live venue first, legacy venue as fallback (a seat following LAW-A03's
    # letter posts on the original venue; that must not read as missing).
    (posted, venue_used,
     venue_comment_id, venue_comment_author) = _venue_posted_with_fallback(
        client, venue, pr_number, head_sha)

    # --- team_objections: machine-countable = CHANGES_REQUESTED -----------
    team_objections = sum(
        1 for s in latest_reviews.values() if s == "CHANGES_REQUESTED")

    report_planned = bool(best and best["report_planned"])

    packet = {
        "target": base_ref,
        "branch": head_ref,
        "seat": seat,
        "tests_green": tests_green,
        "test_evidence": test_evidence,
        "self_scorecard": self_scorecard,
        "independent_validator": independent_validator,
        "posted_to_1354": posted,
        "team_objections": team_objections,
        "post_merge_report_planned": report_planned,
    }
    evidence = {
        "pr": pr_number,
        "head_sha": head_sha,
        "base_ref": base_ref,
        "author": author,
        "seat_source": ("branch prefix" if "/" in head_ref
                        else "author login"),
        "test_job": test_job,  # check-run name resolved from kernel-tests.yml
        "check_runs_seen": len(check_runs),
        "check_run_failures": failures,
        "scorecard_comment_id": scorecard_comment_id,
        "scorecard_comment_author": scorecard_comment_author,
        "approvers": approvers,
        "validator_commit_id": validator_commit_id,
        "stale_approvals_ignored": [u for u, s in latest_reviews.items()
                                    if s == "STALE_APPROVAL"],
        "venue": venue,
        "venue_matched": venue_used,  # which venue actually carried the post
        "venue_comment_id": venue_comment_id,
        "venue_comment_author": venue_comment_author,
        "changes_requested_by": [u for u, s in latest_reviews.items()
                                 if s == "CHANGES_REQUESTED"],
    }
    return packet, evidence


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the DELEGATED-MERGE-AUTHORITY packet from PR data")
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--repo", default=os.environ.get(
        "REPO", "SoulSchoolAcademy/NayaPOWER"))
    ap.add_argument("--venue", type=int, default=DEFAULT_VENUE)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="run the packet through merge_authority.check")
    args = ap.parse_args()

    client = GitHubClient(args.repo)
    try:
        packet, evidence = assemble(client, args.pr, args.venue)
    except GitHubError as e:
        # Fail closed with plain words: API failures never read as verdicts.
        msg = (f"unable to verify merge authority for PR #{args.pr}: {e} "
               f"(API unavailable or malformed data — fail closed)")
        if args.json:
            print(json.dumps({"ok": False, "error": msg}))
        else:
            print(msg)
        return 2

    if not args.verify:
        print(json.dumps({"packet": packet, "evidence": evidence}, indent=2))
        return 0

    verdict = merge_authority.check(packet)
    report = {
        "packet": packet,
        "evidence": evidence,
        "authority": verdict,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "PASS" if verdict.get("pass") else "FAIL"
        print(f"merge authority: {status} (PR #{args.pr}, "
              f"{packet['branch']} -> {packet['target']})")
        for reason in verdict.get("reasons", []):
            print(f"  - {reason}")
    return 0 if verdict.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
