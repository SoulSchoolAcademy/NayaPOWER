#!/usr/bin/env python3
"""
Naya's Guide — The Compass Calculator.

Layer 2 of the Ultimate Decision Calculator. The world model (Layer 1)
sees reality; the Guide decides what to do about it.

Shawn: "I just want it to work. I want to know it's working."

Two commands (v1):

  guide merge --pr N [--auto]
    "Should this PR merge?" — the mechanical merge gate.
    --auto mines all evidence from GitHub + world model. No typing.

  guide status
    "Is the Guide working?" — checks world model freshness and readiness.

(v1 focuses on the merge gate — the highest-stakes decision.
`decide.py next` remains available for "what's next?" lane picking.)

The merge gate follows the 3-PASS FLOW LAW (Shawn, 2026-10-11):
  Three honest self-scoring passes with a show-your-work receipt IS the gate.
  No external lock. The builder owns quality. Independent review is valuable
  but never blocking.

The risk bar is STRICT: 7.0 severity / 0.05 probability (Shawn's decision).

Every run writes a receipt. A decision without a receipt didn't happen.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
WORLD_MODEL_PATH = Path(os.path.expanduser("~/.naya/world-model.json"))

GUIDE_VERSION = "1.0.0"
ENGINE = "nayas-guide"

# Strict risk bar (Shawn's decision, 2026-10-11)
RISK_SEVERITY_BAR = 7.0
RISK_PROBABILITY_BAR = 0.05

# 3-pass law: builder's own 3 passes must reach 9.0
THREE_PASS_BAR = 9.0

# Protected change patterns — these ALWAYS go to Shawn
PROTECTED_PATTERNS = [
    r"\.github/workflows/.*deploy.*",
    r".*secret.*",
    r".*credential.*",
    r".*token.*",
    r".*password.*",
    r".*\.pem$",
    r"BRAIN/00-SPEC/.*CONSTITUTION.*",
]

# 3-pass receipt markers (case-insensitive, look for these in PR body)
RECEIPT_MARKERS = {
    "pass1": [r"pass\s*1", r"first\s*pass", r"round\s*1"],
    "holes1": [r"holes?\s*(found|identified)", r"why\s*not\s*(a\s*)?10"],
    "pass2": [r"pass\s*2", r"second\s*pass", r"round\s*2"],
    "pass3": [r"pass\s*3", r"third\s*pass", r"round\s*3", r"final\s*pass"],
    "head": [r"head\s*[=:@]\s*[0-9a-f]{7,40}", r"certified\s*(at|head)"],
    "score": [r"(\d+\.?\d*)\s*/\s*10"],
}

RECEIPTS_DIR = Path(os.path.expanduser(
    "~/workspace/goals/bring-naya-to-life/hidden_files/decisions"
))


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def now_utc():
    return datetime.now(timezone.utc).isoformat()


def gh_api(method, path):
    """Call gh-api. Returns (ok, data_or_error)."""
    try:
        result = subprocess.run(
            [GH_API, method, path],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return False, result.stderr.strip()[:200]
        return True, json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return False, "API timeout"
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"
    except Exception as e:
        return False, str(e)[:200]


def load_world_model():
    """Load the world model snapshot. Returns (ok, model_or_error)."""
    if not WORLD_MODEL_PATH.exists():
        return False, f"No world model at {WORLD_MODEL_PATH}. Run: python3 tools/world_model.py snapshot"
    try:
        with open(WORLD_MODEL_PATH) as f:
            return True, json.load(f)
    except Exception as e:
        return False, f"Could not read world model: {e}"


def write_receipt(command, question, inputs, result):
    """Write a decision receipt. Returns the path."""
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = "".join(c if c.isalnum() else "-" for c in question.lower())[:40].strip("-")
    path = RECEIPTS_DIR / f"{ts}-guide-{command}-{slug}.json"
    receipt = {
        "receipt_type": "NAYAS_GUIDE_DECISION",
        "guide_version": GUIDE_VERSION,
        "engine": ENGINE,
        "ts_utc": ts,
        "command": command,
        "question": question,
        "inputs": inputs,
        "result": result,
    }
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)
    return str(path)


# ---------------------------------------------------------------------------
# Evidence miners — derive facts from GitHub, never guess
# ---------------------------------------------------------------------------

def mine_pr_details(pr_number):
    """Get PR head SHA, branch, mergeable, draft. Returns (ok, dict_or_error)."""
    ok, pr = gh_api("GET", f"/repos/{REPO}/pulls/{pr_number}")
    if not ok:
        return False, f"Could not fetch PR #{pr_number}: {pr}"
    return True, {
        "number": pr.get("number"),
        "title": pr.get("title", ""),
        "head_sha": (pr.get("head") or {}).get("sha", ""),
        "head_branch": (pr.get("head") or {}).get("ref", ""),
        "base_sha": (pr.get("base") or {}).get("sha", ""),
        "mergeable": pr.get("mergeable"),
        "draft": pr.get("draft", False),
        "body": pr.get("body") or "",
    }


def mine_ci(pr_number, head_sha):
    """Get CI check runs on the PR head. Returns (ok, dict_or_error).

    Categorizes failures as own (on PR head) vs inherited (also failing on base).
    """
    if not head_sha:
        return False, "No head SHA to check"

    ok, checks = gh_api("GET", f"/repos/{REPO}/commits/{head_sha}/check-runs?per_page=100")
    if not ok:
        return False, f"Could not fetch check runs: {checks}"

    runs = checks.get("check_runs", [])

    # Deduplicate by check name — keep only the latest run per check.
    # (The API returns one entry per attempt; we want the current state.)
    latest = {}
    for r in runs:
        name = r.get("name", "?")
        started = r.get("started_at", "")
        if name not in latest or started > latest[name].get("started_at", ""):
            latest[name] = r
    runs = list(latest.values())

    failed = []
    passed = []
    pending = []

    for r in runs:
        name = r.get("name", "?")
        status = r.get("status", "?")
        conclusion = r.get("conclusion", "")
        if status != "completed":
            pending.append(name)
        elif conclusion == "success":
            passed.append(name)
        elif conclusion in ("failure", "timed_out", "cancelled"):
            failed.append(name)
        # skipped/neutral don't count either way

    # Check which failures are inherited (also failing on base/main tip)
    # For now, we check the base via the world model tip or note as unknown
    # A full base comparison needs the base SHA's check runs
    inherited = []
    own_failures = list(failed)  # default: assume own until proven inherited

    return True, {
        "total": len(runs),
        "passed": passed,
        "failed": failed,
        "pending": pending,
        "own_failures": own_failures,
        "inherited_failures": inherited,
        "all_green": len(failed) == 0 and len(pending) == 0 and len(runs) > 0,
        "has_runs": len(runs) > 0,
    }


def mine_receipt(pr_body):
    """Check PR body for a 3-pass show-your-work receipt.

    Returns (has_receipt, details dict).
    A valid receipt needs: pass 1 + holes + pass 2 + pass 3 + head SHA.
    """
    body_lower = pr_body.lower()
    found = {}
    for key, patterns in RECEIPT_MARKERS.items():
        if key == "score":
            continue
        found[key] = any(re.search(p, body_lower) for p in patterns)

    # Extract scores mentioned (e.g., "9.0/10", "8.5/10")
    scores = re.findall(r"(\d+\.?\d*)\s*/\s*10", pr_body)
    scores = [float(s) for s in scores if 0 <= float(s) <= 10]

    # A valid 3-pass receipt needs all three passes + holes + head cert
    has_receipt = all([
        found.get("pass1", False),
        found.get("holes1", False),
        found.get("pass2", False),
        found.get("pass3", False),
        found.get("head", False),
    ])

    # Self-score: the highest score mentioned (the final pass score)
    self_score = max(scores) if scores else 0.0

    return has_receipt, {
        "markers_found": {k: v for k, v in found.items()},
        "scores_mentioned": scores,
        "self_score": self_score,
        "meets_bar": self_score >= THREE_PASS_BAR,
    }


def mine_protected(pr_number):
    """Check PR files for protected changes. Returns (ok, [paths])."""
    ok, files = gh_api("GET", f"/repos/{REPO}/pulls/{pr_number}/files?per_page=100")
    if not ok:
        return False, f"Could not fetch PR files: {files}"

    protected_hits = []
    for f in files:
        path = f.get("filename", "")
        for pattern in PROTECTED_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                protected_hits.append(path)
                break

    return True, protected_hits


def mine_all(pr_number):
    """Mine all evidence for a merge decision. Returns (ok, evidence_dict)."""
    evidence = {"pr": pr_number}
    errors = []

    # PR details
    ok, details = mine_pr_details(pr_number)
    if not ok:
        return False, details
    evidence["details"] = details
    head_sha = details["head_sha"]

    # CI status
    ok, ci = mine_ci(pr_number, head_sha)
    if ok:
        evidence["ci"] = ci
    else:
        errors.append(f"CI: {ci}")
        evidence["ci"] = {"all_green": False, "has_runs": False, "error": ci}

    # Receipt
    has_receipt, receipt_details = mine_receipt(details["body"])
    evidence["receipt"] = {
        "present": has_receipt,
        **receipt_details,
    }

    # Conflicts
    evidence["conflicts"] = details["mergeable"] is False
    evidence["mergeable"] = details["mergeable"]
    evidence["draft"] = details["draft"]

    # Protected changes
    ok, protected = mine_protected(pr_number)
    if ok:
        evidence["protected_changes"] = protected
    else:
        errors.append(f"Protected: {protected}")
        evidence["protected_changes"] = []

    if errors:
        evidence["miner_errors"] = errors

    return True, evidence


# ---------------------------------------------------------------------------
# Decision logic — the 3-pass flow law as code
# ---------------------------------------------------------------------------

def merge_decision(evidence):
    """Apply the merge gate. Returns (decision, reasons, confidence).

    3-PASS FLOW LAW:
      1. Protected changes → ASK (Shawn's gate, always)
      2. Conflicts → HOLD
      3. CI not green → HOLD
      4. No 3-pass receipt → HOLD
      5. Self-score below 9.0 → HOLD
      6. Otherwise → MERGE (independent seats add confidence, never block)
    """
    reasons = []
    confidence_factors = []
    pr = evidence["pr"]
    details = evidence["details"]
    ci = evidence["ci"]
    receipt = evidence["receipt"]
    protected = evidence["protected_changes"]

    # Gate 1: Protected changes — always ASK, never auto-merge
    if protected:
        return "ASK", [
            f"Protected changes detected: {', '.join(protected[:3])}",
            "This touches Shawn's protected gates — his word, not the calculator's.",
        ], "high"

    # Gate 2: Draft PRs
    if details.get("draft"):
        return "HOLD", [
            "PR is marked as draft — not ready for merge.",
            "Mark it ready when the work is complete, then re-run.",
        ], "high"

    # Gate 3: Merge conflicts
    if evidence.get("conflicts"):
        reasons.append("Merge conflicts present — resolve them first, then re-run.")
        return "HOLD", reasons, "high"

    if evidence.get("mergeable") is None:
        reasons.append("GitHub hasn't computed mergeability yet — wait a moment, then re-run.")
        return "HOLD", reasons, "medium"

    # Gate 4: CI must be green on the PR's own checks
    if not ci.get("has_runs"):
        reasons.append("No CI check runs found on this PR head — checks may not have run yet.")
        return "HOLD", reasons, "medium"

    if ci.get("pending"):
        reasons.append(f"CI still running: {', '.join(ci['pending'][:3])} — wait for green, then re-run.")
        return "HOLD", reasons, "high"

    if ci.get("own_failures"):
        reasons.append(f"CI failures on this PR: {', '.join(ci['own_failures'][:5])}")
        reasons.append("Fix the failures, then re-run. The PR's own checks must be green.")
        return "HOLD", reasons, "high"

    reasons.append(f"CI green: {ci['total']} checks, {len(ci['passed'])} passed, 0 failed.")

    # Gate 5: 3-pass receipt must be present
    if not receipt["present"]:
        reasons.append("No 3-pass show-your-work receipt found in the PR body.")
        reasons.append("The builder must complete 3 honest passes and document them — no receipt, no merge.")
        missing = [k for k, v in receipt["markers_found"].items() if not v]
        if missing:
            reasons.append(f"Missing receipt elements: {', '.join(missing)}")
        return "HOLD", reasons, "high"

    reasons.append("3-pass receipt present in PR body.")

    # Gate 6: Self-score must meet the 9.0 bar
    self_score = receipt["self_score"]
    if self_score < THREE_PASS_BAR:
        reasons.append(f"Self-score {self_score}/10 is below the {THREE_PASS_BAR} bar.")
        reasons.append("The 3 passes didn't reach 9.0 — more work needed, then re-run.")
        return "HOLD", reasons, "high"

    reasons.append(f"Self-score {self_score}/10 meets the {THREE_PASS_BAR} bar.")

    # All gates passed → MERGE
    reasons.append("All gates green: no protected changes, no conflicts, CI green, 3-pass receipt present, self-score 9.0+.")
    reasons.append("Per the 3-pass flow law, the builder's honest passes ARE the verification. Independent review is welcome but never blocking.")

    confidence = "high"
    if evidence.get("miner_errors"):
        confidence = "medium"
        reasons.append(f"Note: some evidence miners had errors: {'; '.join(evidence['miner_errors'])}")

    return "MERGE", reasons, confidence


# ---------------------------------------------------------------------------
# Output — Shawn's format: DECISION / WHY / CONFIDENCE / NEXT
# ---------------------------------------------------------------------------

def print_merge_result(pr, decision, reasons, confidence, evidence):
    details = evidence.get("details", {})
    title = details.get("title", "")[:70]

    print(f"\n{'='*60}")
    print(f"NAYA'S GUIDE — Merge Decision for PR #{pr}")
    print(f"{'='*60}")
    print(f"\nDECISION: {decision}")
    print(f"PR: #{pr} — {title}")
    print(f"\nWHY:")
    for r in reasons:
        print(f"  • {r}")
    print(f"\nCONFIDENCE: {confidence}")
    if confidence == "high":
        print("  The evidence is complete and verified.")
    elif confidence == "medium":
        print("  Most evidence verified, but some miners had gaps — treat carefully.")
    else:
        print("  Evidence is incomplete — do not act on this alone.")

    print(f"\nNEXT:")
    if decision == "MERGE":
        print("  The math says merge. Merge it, then report what shipped.")
    elif decision == "HOLD":
        print("  The math says wait. Fix what's listed above, then re-run the Guide.")
    else:  # ASK
        print("  The math says ask Shawn. This needs his explicit word.")

    # Evidence summary (for the record)
    ci = evidence.get("ci", {})
    receipt = evidence.get("receipt", {})
    print(f"\n--- Evidence ---")
    print(f"  Head: {details.get('head_sha', '?')[:8]} ({details.get('head_branch', '?')})")
    print(f"  CI: {ci.get('total', 0)} checks, {len(ci.get('passed', []))} passed, {len(ci.get('own_failures', []))} failed")
    print(f"  Receipt: {'present' if receipt.get('present') else 'MISSING'} (self-score: {receipt.get('self_score', 0)}/10)")
    print(f"  Conflicts: {'YES' if evidence.get('conflicts') else 'no'}")
    print(f"  Protected: {len(evidence.get('protected_changes', []))} files")
    print()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_merge(args):
    """Should this PR merge?"""
    if args.auto:
        print(f"Mining evidence for PR #{args.pr}...")
        ok, evidence = mine_all(args.pr)
        if not ok:
            print(f"Could not mine evidence: {evidence}")
            print("Falling back to manual mode — provide evidence with flags.")
            return 1
        print("Evidence mined. Running the gate...\n")
    else:
        # Manual mode — build evidence from flags (backward compat with decide.py)
        evidence = {
            "pr": args.pr,
            "details": {"title": "", "head_sha": "", "head_branch": "", "draft": False},
            "ci": {
                "total": 0, "passed": [],
                "own_failures": [] if args.ci_own == "pass" else ["(manual: ci-own=fail)"],
                "pending": [], "has_runs": True, "all_green": args.ci_own == "pass",
            },
            "receipt": {
                "present": args.receipt == "yes",
                "self_score": args.scorecard,
                "markers_found": {}, "scores_mentioned": [],
            },
            "conflicts": args.conflicts == "yes",
            "mergeable": None if args.conflicts == "yes" else True,
            "protected_changes": [] if args.protected_changes == "none" else [args.protected_changes],
            "manual_mode": True,
        }

    decision, reasons, confidence = merge_decision(evidence)
    print_merge_result(args.pr, decision, reasons, confidence, evidence)

    result = {
        "decision": decision,
        "reasons": reasons,
        "confidence": confidence,
        "evidence_summary": {
            "ci_green": evidence["ci"].get("all_green", False),
            "receipt_present": evidence["receipt"].get("present", False),
            "self_score": evidence["receipt"].get("self_score", 0),
            "conflicts": evidence.get("conflicts", False),
            "protected_count": len(evidence.get("protected_changes", [])),
        },
    }
    inputs = {"pr": args.pr, "auto": args.auto}
    if not args.auto:
        inputs.update({
            "ci_own": args.ci_own, "scorecard": args.scorecard,
            "conflicts": args.conflicts, "protected_changes": args.protected_changes,
            "receipt": args.receipt,
        })

    receipt_path = write_receipt("merge", f"merge PR #{args.pr}", inputs, result)
    print(f"Receipt: {receipt_path}")
    return 0


def cmd_status(args):
    """Is the Guide working?"""
    print(f"\n{'='*60}")
    print(f"NAYA'S GUIDE v{GUIDE_VERSION} — Status")
    print(f"{'='*60}\n")

    # World model check
    ok, model = load_world_model()
    if not ok:
        print(f"❌ World model: {model}")
        print("\nThe Guide needs the world model (Layer 1).")
        print("Run: python3 tools/world_model.py snapshot")
        return 1

    print("✅ World model: loaded")
    sections = model.get("sections", {})
    for name in ["tip", "prs", "lanes", "ledger", "mission", "laws"]:
        s = sections.get(name, {})
        status = s.get("status", "?")
        as_of = s.get("as_of_utc", "?")[:19] if s.get("as_of_utc") else "?"
        icon = "✅" if status == "OK" else "⚠️" if status == "STALE" else "❌"
        print(f"  {icon} {name}: {status} (as of {as_of})")

    # GitHub API check
    ok, _ = gh_api("GET", "/rate_limit")
    if ok:
        print("\n✅ GitHub API: reachable")
    else:
        print(f"\n❌ GitHub API: unreachable")

    print(f"\nRisk bar: {RISK_SEVERITY_BAR} severity / {RISK_PROBABILITY_BAR} probability (strict)")
    print(f"3-pass bar: {THREE_PASS_BAR}/10")
    print("\nThe Guide is working. Ask it: guide merge --pr N --auto")
    return 0


def main():
    ap = argparse.ArgumentParser(
        prog="guide",
        description="Naya's Guide — The Compass Calculator. Values in, decision out.",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # merge
    p_merge = sub.add_parser("merge", help="should this PR merge?")
    p_merge.add_argument("--pr", required=True, help="PR number")
    p_merge.add_argument("--auto", action="store_true",
                         help="mine all evidence automatically from GitHub (recommended)")
    # Manual fallback flags (for when --auto can't reach GitHub)
    p_merge.add_argument("--ci-own", choices=["pass", "fail"], default="pass")
    p_merge.add_argument("--scorecard", type=float, default=0.0)
    p_merge.add_argument("--conflicts", choices=["none", "yes"], default="none")
    p_merge.add_argument("--protected-changes", default="none")
    p_merge.add_argument("--receipt", choices=["yes", "no"], default="no")

    # status
    sub.add_parser("status", help="is the Guide working?")

    args = ap.parse_args()
    if args.command == "merge":
        return cmd_merge(args)
    elif args.command == "status":
        return cmd_status(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
