#!/usr/bin/env python3
"""Merge-readiness gate: no merge unless ALL required CI checks are green.

Constitution §14 (WHAT WE NEVER DO): "merge red CI".
Constitution §7 (LAW OF PROOF): the evidence must be strong enough for the claim.

This is the executable form of "no merge with red CI". It queries the
GitHub API for every check run on the PR's exact head SHA and FAILS unless
every required check has conclusion == 'success'.

Why this exists: PR #2200 was merged via the API while its consensus gate
was failing. Branch protection (when enabled) enforces this server-side,
but agents merging via API bypass it. This script is the client-side
enforcement — run it immediately before any merge, and abort on failure.

Reads from env:
  GH_TOKEN   - GitHub token
  REPO       - owner/repo (e.g. SoulSchoolAcademy/NayaPOWER)
  PR_NUMBER  - pull request number

Exit 0 = all required checks green on the exact head SHA.
Exit 1 = fail with a plain-words reason (names the failing check).
Stdlib only.
"""
import json
import os
import sys
import urllib.request

API = "https://api.github.com"

# Checks that must be green. These are the job/check names as they appear
# in the GitHub checks API. Keep in sync with .github/workflows/.
REQUIRED_CHECKS = [
    "test",                              # kernel-tests.yml: node + pytest + brain index
    "Team review + scorecard receipt",   # merge-consensus-gate.yml
]


def fail(msg):
    print(f"MERGE READINESS FAILED: {msg}")
    sys.exit(1)


def api_get(path, token):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-merge-readiness/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    token = os.environ.get("GH_TOKEN") or ""
    repo = os.environ.get("REPO") or ""
    pr_number = os.environ.get("PR_NUMBER") or ""
    if not (token and repo and pr_number):
        fail("missing GH_TOKEN/REPO/PR_NUMBER in environment.")

    pr = api_get(f"/repos/{repo}/pulls/{pr_number}", token)
    head_sha = pr["head"]["sha"]
    state = pr.get("state")
    merged = pr.get("merged", False)
    if state != "open" or merged:
        fail(f"PR #{pr_number} is not open (state={state}, merged={merged}).")

    # Get the combined status + check runs for the exact head SHA.
    combined = api_get(f"/repos/{repo}/commits/{head_sha}/status", token)
    check_runs_resp = api_get(
        f"/repos/{repo}/commits/{head_sha}/check-runs?per_page=100", token)

    # Index check runs by name (latest per name wins).
    latest = {}
    for cr in check_runs_resp.get("check_runs", []):
        name = cr.get("name", "")
        # Keep the most recently completed run per name.
        prev = latest.get(name)
        if prev is None or (cr.get("completed_at") or "") >= (prev.get("completed_at") or ""):
            latest[name] = cr

    missing = []
    failing = []
    for req_name in REQUIRED_CHECKS:
        run = latest.get(req_name)
        if run is None:
            missing.append(req_name)
            continue
        status = run.get("status")
        conclusion = run.get("conclusion")
        if status != "completed" or conclusion != "success":
            failing.append(f"{req_name} (status={status}, conclusion={conclusion})")

    if missing:
        fail(f"required checks have not run on head {head_sha[:10]}: "
             f"{', '.join(missing)}. Wait for CI, then re-check.")
    if failing:
        fail(f"required checks NOT GREEN on head {head_sha[:10]}: "
             f"{'; '.join(failing)}. Fix them before merging. "
             f"Merging red CI is a Constitution violation (§14).")

    print(f"MERGE READINESS PASSED: all {len(REQUIRED_CHECKS)} required checks "
          f"green on {head_sha[:10]}.")


if __name__ == "__main__":
    main()
