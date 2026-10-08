#!/usr/bin/env python3
"""Production Readiness Checklist — machine-executable readiness verdict for NayaPOWER.

Slice: readiness checklist (production readiness lane). NOT proof execution
(prod-proof-builder), NOT pipeline repair (Naya 4). This instrument MEASURES
and reports; it never deploys, never writes production state, never mutates
the repository.

Question answered: "Is the current main tip deployable, and is production healthy?"

Checks (each emits PASS / WARN / FAIL / UNKNOWN with evidence):
  C1 tip_currency        — origin/main re-resolved at execution; exact SHA recorded (SN-0493).
  C2 production_stamp    — the production branch holds a deploy-stamp commit for the tip.
  C3 workflow_health     — recent Governed Production Promotion runs: verdicts + failing step.
  C4 standing_policy     — STANDING-PRODUCTION-PROMOTION-V1.json is RATIFIED and well-formed.
  C5 dispatch_contract   — workflow_dispatch requires confirm=DEPLOY + exact 40-hex source_sha,
                           and the YAML contains fail-closed binding checks.
  C6 migration_hygiene   — migration filenames unique/ordered/conforming; every pending
                           ledger entry's file exists (read-only; no SQL parsing needed).
  C7 proof_workflows_exist— every workflow file referenced by the promotion workflow exists.
  C8 receipt_path        — the promotion workflow writes a durable promotion receipt artifact.

Exit codes: 0 = all PASS (WARN allowed), 1 = any FAIL, 2 = instrument error.

GitHub API access: uses GITHUB_TOKEN env when present (CI). Otherwise delegates to
the NAYA_GH_API helper script (default: ~/workspace/naya/bin/gh-api), which carries
the credential without exposing it. With neither, C2/C3 report UNKNOWN.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github/workflows/governed-supabase-production-deploy.yml"
POLICY_PATH = ROOT / ".naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json"
MIGRATIONS_DIR = ROOT / "supabase/migrations"
LEDGER_PATH = ROOT / "supabase/PRODUCTION-MIGRATION-LEDGER-V1.json"
WORKFLOWS_DIR = ROOT / ".github/workflows"

PROMOTION_WORKFLOW_FILE = "governed-supabase-production-deploy.yml"
# The promotion workflow fail-closes unless these CI workflows completed
# successfully for the exact head SHA (see its inline required-CI block).
REQUIRED_CI_WORKFLOWS = ("kernel-tests.yml", "collective-chain-readiness-gate.yml")
API_HOST = "https://api.github.com"
REPO = "SoulSchoolAcademy/NayaPOWER"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MIGRATION_NAME_RE = re.compile(r"^[0-9]{14}_[a-z0-9_]+\.sql$")
STAMP_MSG_RE = re.compile(r"deploy: stamp Naya runtime source ([0-9a-f]{40})")

SCHEMA = "NAYAPOWER_PRODUCTION_READINESS_CHECKLIST_V1"


# ---------------------------------------------------------------- utilities

def check_result(check_id: str, verdict: str, summary: str, evidence: dict | None = None) -> dict:
    assert verdict in ("PASS", "WARN", "FAIL", "UNKNOWN")
    return {"check": check_id, "verdict": verdict, "summary": summary,
            "evidence": evidence or {}}


def gh_get(path: str) -> dict | list | None:
    """Read-only GitHub API GET. Returns parsed JSON, or None when no credential path."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req = urllib.request.Request(API_HOST + path, method="GET")
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except (urllib.error.URLError, OSError, json.JSONDecodeError):
            return None
    helper = os.environ.get("NAYA_GH_API") or str(Path.home() / "workspace/naya/bin/gh-api")
    if Path(helper).is_file():
        try:
            out = subprocess.run([helper, "GET", path], capture_output=True,
                                 text=True, timeout=60)
            if out.returncode == 0 and out.stdout.strip():
                return json.loads(out.stdout)
        except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
            return None
    return None


def git(args: list[str]) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT)] + args, capture_output=True,
                             text=True, timeout=120)
        return out.stdout.strip() if out.returncode == 0 else None
    except (subprocess.SubprocessError, OSError):
        return None


# ---------------------------------------------------------------- checks

def check_tip_currency() -> dict:
    """C1 — re-resolve origin/main at execution; record exact SHA (SN-0493)."""
    git(["fetch", "origin", "main", "--quiet"])
    sha = git(["rev-parse", "origin/main"])
    if not sha or not SHA_RE.match(sha):
        return check_result("C1", "FAIL", "could not resolve origin/main to a 40-hex SHA",
                            {"resolved": sha})
    msg = git(["log", "-1", "--format=%s", sha]) or ""
    return check_result("C1", "PASS", f"tip resolved at execution: {sha[:12]}",
                        {"tip_sha": sha, "tip_subject": msg[:120]})


def check_production_stamp(tip_sha: str | None) -> dict:
    """C2 — production branch holds a deploy-stamp commit for the current tip."""
    if not tip_sha:
        return check_result("C2", "UNKNOWN", "no tip SHA to look for",
                            {"reason": "C1 did not produce a SHA"})
    data = gh_get(f"/repos/{REPO}/branches/production")
    if data is None:
        return check_result("C2", "UNKNOWN", "GitHub API unreachable (no credential path)",
                            {"reason": "no_api"})
    commit = (data.get("commit") or {})
    message = ((commit.get("commit") or {}).get("message") or "")
    m = STAMP_MSG_RE.search(message)
    stamped_sha = m.group(1) if m else None
    evidence = {"production_tip": commit.get("sha"),
                "stamp_message": message[:120],
                "stamped_source_sha": stamped_sha,
                "wanted_sha": tip_sha}
    if stamped_sha == tip_sha:
        return check_result("C2", "PASS",
                            f"production stamped for current tip {tip_sha[:12]}", evidence)
    if stamped_sha:
        return check_result("C2", "WARN",
                            f"production stamped for {stamped_sha[:12]}, not current tip {tip_sha[:12]}",
                            evidence)
    return check_result("C2", "WARN",
                        "production tip is not a deploy-stamp commit; cannot bind it to a main SHA",
                        evidence)


def check_workflow_health(recent: int = 12) -> dict:
    """C3 — recent Governed Production Promotion runs: verdicts + failing step."""
    data = gh_get(f"/repos/{REPO}/actions/workflows/{PROMOTION_WORKFLOW_FILE}/runs?per_page={recent}")
    if data is None:
        return check_result("C3", "UNKNOWN", "GitHub API unreachable (no credential path)",
                            {"reason": "no_api"})
    runs = data.get("workflow_runs", [])
    if not runs:
        return check_result("C3", "WARN", "no recent promotion workflow runs found", {})
    failures = []
    successes = 0
    failing_steps: dict[str, int] = {}
    latest_failed_sha: str | None = None
    for r in runs:
        rid, event = r.get("id"), r.get("event")
        head = (r.get("head_sha") or "")[:12]
        conclusion = r.get("conclusion")
        if conclusion == "success":
            successes += 1
            continue
        failures.append({"run_id": rid, "event": event, "head_sha": head,
                         "conclusion": conclusion, "created_at": r.get("created_at")})
        if latest_failed_sha is None and r.get("head_sha"):
            latest_failed_sha = r["head_sha"]
        jobs = gh_get(f"/repos/{REPO}/actions/runs/{rid}/jobs?per_page=30")
        steps = []
        if isinstance(jobs, dict):
            for j in jobs.get("jobs", []):
                for s in j.get("steps", []) or []:
                    if s.get("conclusion") not in ("success", "skipped", None):
                        steps.append(s.get("name"))
        for st in steps:
            failing_steps[st] = failing_steps.get(st, 0) + 1
        failures[-1]["failing_steps"] = steps
    evidence = {"runs_examined": len(runs), "successes": successes,
                "failures": failures, "failing_step_histogram": failing_steps,
                "required_ci_at_latest_tip": required_ci_status(latest_failed_sha)}
    failing_ci = [w for w, s in evidence["required_ci_at_latest_tip"].items()
                  if s.get("conclusion") not in ("success", None) or
                  (s.get("status") == "completed" and s.get("conclusion") != "success")]
    ci_note = ""
    if failing_ci:
        ci_note = (f"; required CI failing at latest tip {latest_failed_sha[:12] if latest_failed_sha else '?'}: "
                   f"{', '.join(failing_ci)}")
    if not failures:
        return check_result("C3", "PASS", f"last {len(runs)} promotion runs all succeeded", evidence)
    if successes == 0:
        return check_result("C3", "FAIL",
                            f"all {len(runs)} recent promotion runs failed; "
                            f"failing steps: {failing_steps or 'unknown'}{ci_note}", evidence)
    return check_result("C3", "WARN",
                        f"{len(failures)}/{len(runs)} recent promotion runs failed; "
                        f"failing steps: {failing_steps or 'unknown'}{ci_note}", evidence)


def required_ci_status(head_sha: str | None) -> dict:
    """Required-CI verdicts at the exact head SHA (mirrors the workflow's own gate).

    Returns {workflow_file: {status, conclusion, run_id}} for REQUIRED_CI_WORKFLOWS.
    This names WHICH fail-closed sub-gate trips when the promotion step fails.
    """
    if not head_sha:
        return {}
    out: dict[str, dict] = {}
    for wf in REQUIRED_CI_WORKFLOWS:
        data = gh_get(f"/repos/{REPO}/actions/workflows/{wf}/runs"
                      f"?head_sha={head_sha}&event=push&per_page=10")
        if not isinstance(data, dict):
            out[wf] = {"status": "unknown", "conclusion": None, "reason": "no_api"}
            continue
        matches = [r for r in data.get("workflow_runs", [])
                   if r.get("head_sha") == head_sha and r.get("head_branch") == "main"]
        if not matches:
            out[wf] = {"status": "missing", "conclusion": None}
            continue
        best = max(matches, key=lambda r: (int(r.get("id", 0)), int(r.get("run_attempt", 0))))
        out[wf] = {"status": best.get("status"), "conclusion": best.get("conclusion"),
                   "run_id": best.get("id")}
    return out


def _paged_open_prs(max_pages: int = 3) -> list | None:
    """Fetch open PRs oldest-first across bounded pages (API caps at 100/page)."""
    out: list = []
    for page in range(1, max_pages + 1):
        data = gh_get(f"/repos/{REPO}/pulls?state=open&per_page=100"
                      f"&sort=created&direction=asc&page={page}")
        if data is None:
            return None
        if not isinstance(data, list) or not data:
            break
        out.extend(data)
        if len(data) < 100:
            break
    return out


def check_branch_hygiene(dirty_scan_limit: int = 15) -> dict:
    """C9 — production branch state: merge-queue health and integration debt.

    Signal only (never FAIL by itself): measures the open-PR pile against merge
    velocity, ancient PRs, and conflicted (dirty) PRs among the oldest open
    ones — with bounded API cost. A healthy fast-moving repo can carry a large
    fresh pile; a stale or conflicted pile is integration debt.
    """
    data = _paged_open_prs()
    if data is None:
        return check_result("C9", "UNKNOWN", "GitHub API unreachable (no credential path)",
                            {"reason": "no_api"})
    prs = data if isinstance(data, list) else []
    now = datetime.now(timezone.utc)
    ancient = [p["number"] for p in prs
               if (now - datetime.fromisoformat(
                   p["created_at"].replace("Z", "+00:00"))).days > 14]
    # mergeable_state needs a per-PR fetch: scan only the oldest, bounded.
    dirty, blocked, scan_failures = [], [], 0
    for p in prs[:dirty_scan_limit]:
        detail = gh_get(f"/repos/{REPO}/pulls/{p['number']}")
        state = detail.get("mergeable_state") if isinstance(detail, dict) else None
        if state == "dirty":
            dirty.append(p["number"])
        elif state == "blocked":
            blocked.append(p["number"])
        elif state is None:
            scan_failures += 1
    merged_data = gh_get(f"/repos/{REPO}/pulls?state=closed&per_page=100")
    merged_24h = 0
    if isinstance(merged_data, list):
        merged_24h = sum(
            1 for p in merged_data if p.get("merged_at") and
            (now - datetime.fromisoformat(
                p["merged_at"].replace("Z", "+00:00"))).days < 1)
    evidence = {"open_prs": len(prs), "merged_last_24h": merged_24h,
                "ancient_prs_over_14d": ancient,
                "dirty_scanned": min(dirty_scan_limit, len(prs)),
                "dirty_scan_failures": scan_failures,
                "dirty_prs": dirty, "blocked_prs": blocked}
    problems = []
    if dirty:
        problems.append(f"{len(dirty)} conflicted PR(s): {dirty}")
    if ancient:
        problems.append(f"{len(ancient)} ancient PR(s) >14d: {ancient[:10]}")
    if merged_24h > 0 and len(prs) > 3 * merged_24h:
        problems.append(f"open pile {len(prs)} > 3x daily merge velocity {merged_24h}")
    if problems:
        return check_result("C9", "WARN", "branch hygiene: " + "; ".join(problems), evidence)
    return check_result("C9", "PASS",
                        f"branch hygiene clean: {len(prs)} open, {merged_24h} merged/24h, "
                        f"no conflicts in oldest {min(dirty_scan_limit, len(prs))}", evidence)


def check_standing_policy(policy_path: Path | None = None) -> dict:
    """C4 — standing promotion policy is RATIFIED and well-formed."""
    ppath = policy_path or POLICY_PATH
    if not ppath.is_file():
        return check_result("C4", "FAIL", "standing policy file missing",
                            {"path": str(ppath)})
    try:
        policy = json.loads(ppath.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return check_result("C4", "FAIL", f"standing policy unreadable: {e}", {})
    evidence = {"policy_id": policy.get("policy_id"), "status": policy.get("status"),
                "scope": policy.get("scope")}
    if policy.get("policy_id") != "STANDING-PRODUCTION-PROMOTION-V1":
        return check_result("C4", "FAIL", "policy_id mismatch", evidence)
    if policy.get("status") != "RATIFIED":
        return check_result("C4", "FAIL", f"policy status is {policy.get('status')}, not RATIFIED",
                            evidence)
    return check_result("C4", "PASS", "STANDING-PRODUCTION-PROMOTION-V1 is RATIFIED", evidence)


def check_dispatch_contract(text: str | None = None) -> dict:
    """C5 — workflow_dispatch requires confirm=DEPLOY + exact 40-hex source_sha, fail-closed."""
    try:
        content = text if text is not None else WORKFLOW_PATH.read_text(encoding="utf-8")
    except OSError as e:
        return check_result("C5", "FAIL", f"promotion workflow unreadable: {e}", {})
    required_fragments = {
        "dispatch inputs": "workflow_dispatch:",
        "confirm input": "confirm:",
        "source_sha input": "source_sha:",
        "DEPLOY literal": '"DEPLOY"',
        "40-hex length check": '${#authorized_sha}" -ne 40',
        "hex charset check": "[!0-9a-f]",
        "SHA binding": 'authorized_sha" != "$GITHUB_SHA"',
        "tip-movement guard": "main moved",
    }
    missing = [name for name, frag in required_fragments.items() if frag not in content]
    evidence = {"fragments_checked": len(required_fragments), "missing": missing}
    if missing:
        return check_result("C5", "FAIL",
                            f"dispatch contract missing: {', '.join(missing)}", evidence)
    return check_result("C5", "PASS",
                        "dispatch contract intact: DEPLOY + 40-hex SHA + fail-closed binding", evidence)


def check_migration_hygiene(migrations_dir: Path | None = None,
                             ledger_path: Path | None = None) -> dict:
    """C6 — migration filenames unique/ordered/conforming; ledger pending files exist."""
    mdir = migrations_dir or MIGRATIONS_DIR
    lpath = ledger_path or LEDGER_PATH
    problems: list[str] = []
    try:
        names = sorted(p.name for p in mdir.iterdir() if p.is_file())
    except OSError as e:
        return check_result("C6", "FAIL", f"migrations dir unreadable: {e}", {})
    seen: set[str] = set()
    for n in names:
        if not MIGRATION_NAME_RE.match(n):
            problems.append(f"non-conforming name: {n}")
        stamp = n.split("_")[0]
        if stamp in seen:
            problems.append(f"duplicate timestamp: {n}")
        seen.add(stamp)
    if names != sorted(names):
        problems.append("directory order is not lexicographic")
    ledger_pending = "n/a"
    if lpath.is_file():
        try:
            ledger = json.loads(lpath.read_text(encoding="utf-8"))
            pending = ledger.get("pending", [])
            ledger_pending = len(pending)
            for entry in pending:
                rel = entry.get("path", "")
                if rel and not (ROOT / rel).is_file():
                    problems.append(f"ledger pending file missing: {rel}")
        except (OSError, json.JSONDecodeError) as e:
            problems.append(f"ledger unreadable: {e}")
    else:
        problems.append("production migration ledger missing")
    evidence = {"migration_count": len(names), "ledger_pending": ledger_pending,
                "problems": problems}
    if problems:
        return check_result("C6", "FAIL", f"migration hygiene: {len(problems)} problem(s)", evidence)
    return check_result("C6", "PASS", f"migration hygiene clean: {len(names)} files, ledger ok",
                        evidence)


def check_proof_workflows_exist(text: str | None = None,
                                workflows_dir: Path | None = None) -> dict:
    """C7 — every workflow file referenced by the promotion workflow exists on disk."""
    wdir = workflows_dir or WORKFLOWS_DIR
    try:
        content = text if text is not None else WORKFLOW_PATH.read_text(encoding="utf-8")
    except OSError as e:
        return check_result("C7", "FAIL", f"promotion workflow unreadable: {e}", {})
    refs = sorted(set(re.findall(r"([a-z0-9][a-z0-9\-]*\.yml)", content)))
    missing = [r for r in refs if not (wdir / r).is_file()]
    evidence = {"referenced": refs, "missing": missing}
    if missing:
        return check_result("C7", "FAIL", f"referenced workflow(s) missing: {missing}", evidence)
    return check_result("C7", "PASS", f"all {len(refs)} referenced workflows exist", evidence)


def check_receipt_path(text: str | None = None) -> dict:
    """C8 — the promotion workflow writes a durable promotion receipt artifact."""
    try:
        content = text if text is not None else WORKFLOW_PATH.read_text(encoding="utf-8")
    except OSError as e:
        return check_result("C8", "FAIL", f"promotion workflow unreadable: {e}", {})
    has_receipt = "production-promotion-receipt" in content
    has_schema = "NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1" in content
    evidence = {"receipt_artifact": has_receipt, "receipt_schema": has_schema}
    if has_receipt and has_schema:
        return check_result("C8", "PASS", "durable promotion receipt path present", evidence)
    return check_result("C8", "WARN", "promotion receipt path incomplete", evidence)


# ---------------------------------------------------------------- report

def score(checks: list[dict]) -> tuple[str, int]:
    verdicts = [c["verdict"] for c in checks]
    if any(v == "FAIL" for v in verdicts):
        return "NOT_READY", 1
    if any(v == "UNKNOWN" for v in verdicts):
        return "READY_WITH_UNKNOWN", 0
    if any(v == "WARN" for v in verdicts):
        return "READY_WITH_WARNINGS", 0
    return "READY", 0


def run() -> tuple[dict, int]:
    tip = check_tip_currency()
    tip_sha = tip["evidence"].get("tip_sha")
    checks = [
        tip,
        check_production_stamp(tip_sha),
        check_workflow_health(),
        check_standing_policy(),
        check_dispatch_contract(),
        check_migration_hygiene(),
        check_proof_workflows_exist(),
        check_receipt_path(),
        check_branch_hygiene(),
    ]
    verdict, exit_code = score(checks)
    report = {"schema": SCHEMA, "verdict": verdict,
              "checks": checks,
              "summary": {v: sum(1 for c in checks if c["verdict"] == v)
                          for v in ("PASS", "WARN", "FAIL", "UNKNOWN")}}
    return report, exit_code


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    try:
        report, exit_code = run()
    except Exception as e:  # instrument must fail loudly, never silently
        print(json.dumps({"schema": SCHEMA, "verdict": "INSTRUMENT_ERROR",
                          "error": f"{type(e).__name__}: {e}"}, indent=2))
        return 2
    if "--json" in args:
        # machine consumers: pure JSON on stdout, nothing else.
        print(json.dumps(report))
        return exit_code
    print(json.dumps(report, indent=2))
    print()
    for c in report["checks"]:
        print(f"[{c['verdict']:7}] {c['check']}: {c['summary']}")
    print(f"\nverdict: {report['verdict']} "
          f"(PASS {report['summary']['PASS']}, WARN {report['summary']['WARN']}, "
          f"FAIL {report['summary']['FAIL']}, UNKNOWN {report['summary']['UNKNOWN']})")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
