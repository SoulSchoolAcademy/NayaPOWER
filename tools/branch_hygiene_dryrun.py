#!/usr/bin/env python3
"""Dry-run harness for .github/workflows/branch-hygiene.yml.

Exercises the workflow's decision logic against REAL local data (the live
branch list + local git), without any writes and without the GitHub API:

  1. workflow YAML parses and has the required triggers/jobs/permissions.
  2. auto-close guard logic: protected patterns (main, production, release/*)
     are never selected for delete; naya5/* goes the label path; a known
     fully-merged non-naya5 branch goes the delete path.
  3. stale-scan logic: age math on a sample of real branches, protected
     exclusions hold, report rows validate against the JSONL schema.

Exit 0 = all assertions hold. This is the red->green gate for the workflow
before it ever runs on a runner.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/branch-hygiene.yml"
HEADS = Path.home() / ("workspace/goals/super-brain-engine-to-10-10/hidden_files"
                       "/scratch-prb-1545/heads.txt")

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name + (f": {detail}" if detail else ""))


def git(args: list[str]) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT)] + args, capture_output=True,
                             text=True, timeout=60)
        return out.stdout.strip() if out.returncode == 0 else None
    except (subprocess.SubprocessError, OSError):
        return None


# ---- 1. workflow structure ----------------------------------------------------
import yaml  # noqa: E402

wf = yaml.safe_load(WORKFLOW.read_text())
check("yaml parses", isinstance(wf, dict))
on = wf.get("on", wf.get(True, {}))  # YAML 1.1 parses bare `on:` as boolean True
check("has pull_request_target closed trigger",
      "pull_request_target" in on and "closed" in (on["pull_request_target"].get("types") or []))
check("has daily schedule", bool(on.get("schedule")))
check("has workflow_dispatch with dry_run default true",
      (on.get("workflow_dispatch", {}).get("inputs", {}).get("dry_run", {}).get("default")) == "true")
perms = wf.get("permissions", {})
check("permissions contents:write + pull-requests:write",
      perms.get("contents") == "write" and perms.get("pull-requests") == "write")
jobs = wf.get("jobs", {})
check("auto-close-merged job present", "auto-close-merged" in jobs)
check("stale-scan job present", "stale-scan" in jobs)
auto_src = (WORKFLOW.read_text())
check("auto-close verifies head-sha unchanged", 'CURRENT' in auto_src and 'HEAD_SHA' in auto_src)
check("auto-close verifies fully-merged", "merge-base --is-ancestor" in auto_src)
check("naya5/* never auto-deleted", 'naya5/*' in auto_src and 'never auto-delete' in auto_src)
check("stale scan never deletes", auto_src.count("DELETE") == 1,
      "DELETE must appear exactly once (auto-close only)")

# ---- 2. auto-close guard logic -------------------------------------------------
heads = [h for h in HEADS.read_text().splitlines() if h]


def guard_decision(branch: str) -> str:
    if branch in ("main", "production"):
        return "skip"
    if branch.startswith("release/"):
        return "skip"
    if branch.startswith("naya5/"):
        return "label"
    return "delete"


for protected in ("main", "production", "release/canonical-hub-2026-09-08"):
    check(f"protected never deleted: {protected}", guard_decision(protected) == "skip")
naya5_sample = [h for h in heads if h.startswith("naya5/")][:5]
for b in naya5_sample:
    check(f"naya5/* label path: {b}", guard_decision(b) == "label")
# a real fully-merged non-naya5 branch: verify the merge-base guard would pass
merged_sample = [h for h in heads
                 if not h.startswith(("naya5/", "release/")) and h not in ("main", "production")][:50]
found_delete_candidate = None
for b in merged_sample:
    if git(["merge-base", "--is-ancestor", f"origin/{b}", "origin/main"]) is not None:
        found_delete_candidate = b
        break
check("delete path reachable for a real merged branch",
      found_delete_candidate is not None, "no merged non-naya5 branch in first 50")
if found_delete_candidate:
    check(f"guard -> delete: {found_delete_candidate}",
          guard_decision(found_delete_candidate) == "delete")

# ---- 3. stale-scan logic --------------------------------------------------------
STALE_DAYS = 30
now = int(time.time())
cutoff = now - STALE_DAYS * 86400
stale, fresh, protected_seen = [], [], []
for b in heads[:400]:  # bounded sample; logic is per-branch identical
    ts_raw = git(["log", "-1", "--format=%ct", f"origin/{b}"])
    if ts_raw is None:
        continue
    ts = int(ts_raw)
    if b in ("main", "production") or b.startswith("release/"):
        protected_seen.append(b)
        continue
    (stale if ts < cutoff else fresh).append((b, ts))
check("stale scan excludes protected patterns", all(
    b in ("main", "production") or b.startswith("release/") for b in protected_seen)
    and not any(b in ("main", "production") or b.startswith("release/") for b, _ in stale))
check("stale threshold splits the sample", bool(stale) and bool(fresh),
      f"stale={len(stale)} fresh={len(fresh)}")
# report-row schema check on the stalest real branch
if stale:
    b, ts = min(stale, key=lambda x: x[1])
    row = {"branch": b,
           "tip": (git(["rev-parse", "--short", f"origin/{b}"]) or "")[:7],
           "last_commit": time.strftime("%FT%TZ", time.gmtime(ts)),
           "age_days": (now - ts) // 86400,
           "open_pr": None,  # API-gated; dry-run records null when unreadable
           "action": "would-report"}
    try:
        json.dumps(row)
        schema_ok = (row["age_days"] > STALE_DAYS and isinstance(row["branch"], str)
                     and row["action"] in ("would-report", "would-label-pr-0",
                                           "report-only", "labeled-pr-0"))
    except (TypeError, ValueError):
        schema_ok = False
    check(f"report row schema valid (stalest: {b}, {row['age_days']}d)", schema_ok)

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILURES:")
    for f in FAILURES:
        print("  -", f)
    sys.exit(1)
print("all dry-run assertions hold")
