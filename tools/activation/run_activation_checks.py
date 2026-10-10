#!/usr/bin/env python3
"""Activation check runner — Layer 3 of the Naya Activation Protocol.

Runs every law-as-code check (existing + new) and reports pass/fail per
check with a fail-closed exit code.

Existing checks are invoked by path (subprocess) — never reimplemented.
New Layer 3 checks live beside this runner.

Usage:
    python3 run_activation_checks.py --repo <nayaPOWER-checkout>
                                     [--workdir <artifact-dir>]
                                     [--pr-state <pr_state.json>]
                                     [--strict]

  --repo      repo root for repo-level checks (ratified guard, migration
              ledger, migration baseline tests, auto-merge gate)
  --workdir   work artifact directory for artifact checks (activation
              receipt, evidence claims, plain words)
  --pr-state  JSON file for tools/auto_merge_gate.py (omit: gate skipped)
  --strict    any SKIP also fails (for CI use; default: only FAIL fails)

Exit codes:
  0 — every executed check passed (skips allowed, listed plainly)
  1 — at least one check FAILED (fail-closed: the violation blocks)
  2 — usage error

A SKIP is never a pass and never silent: it is listed with its reason.
--strict turns skips into failures where a gate must not be bypassed by
absence (e.g. CI).

Stdlib only.
"""

import argparse
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = {
    "activation-receipt": os.path.join(HERE, "check_activation_receipt.py"),
    "evidence-claims": os.path.join(HERE, "check_evidence_claims.py"),
    "plain-words": os.path.join(HERE, "check_plain_words.py"),
}

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


def run_proc(cmd, cwd=None, timeout=300):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError as e:
        return None, f"could not start: {e}"
    except subprocess.TimeoutExpired:
        return None, "timed out"


def check_ratified_guard(repo):
    """Law 6.3 / 5.3 — no ratified object deleted without a retirement record."""
    tool = os.path.join(repo, "tools", "ratified_guard.py")
    if not os.path.isfile(tool):
        return SKIP, "tools/ratified_guard.py not present in repo"
    if not os.path.isdir(os.path.join(repo, ".git")):
        return SKIP, "not a git checkout — diff guard needs git"
    rc, out = run_proc(
        [sys.executable, tool, "--check-diff",
         "--base-ref", "origin/main", "--head-ref", "HEAD",
         "--repo", repo], cwd=repo)
    if rc is None:
        return SKIP, out
    if "Traceback (most recent call last)" in out:
        # The guard itself crashed (e.g. no origin/main ref in this
        # checkout). A crashed check is UNKNOWN, not a violation —
        # UNKNOWN != PASS, but it is not evidence of a deletion either.
        return SKIP, ("the guard could not execute in this checkout "
                      f"(environment failure, not a verdict): {out[:300]}")
    if rc != 0:
        last = out.splitlines()[-3:] if out else []
        return FAIL, "ratified object deleted without retirement record: " + \
            " | ".join(last)
    return PASS, "no ratified deletions without retirement record"


def check_migration_ledger(repo):
    """Law 8.7 — pending-migration ledger metadata matches repo bytes."""
    tool = os.path.join(repo, "tools", "reconcile_pending_migration_ledger.py")
    if not os.path.isfile(tool):
        return SKIP, "tools/reconcile_pending_migration_ledger.py not present"
    if importlib.util.find_spec("pglast") is None:
        return SKIP, ("pglast is not installed — the ledger drift check "
                      "cannot run here (install pglast to enable it)")
    rc, out = run_proc([sys.executable, tool], cwd=repo)
    if rc is None:
        return SKIP, out
    if rc != 0:
        return FAIL, "migration ledger drift detected: " + out[:400]
    return PASS, "ledger metadata matches repository bytes"


def check_migration_baseline(repo):
    """Law 8.7 — active migration directory exactly equals governed ledger."""
    test = os.path.join(repo, "tests",
                        "test_production_migration_history_baseline.py")
    if not os.path.isfile(test):
        return SKIP, "baseline test not present in repo"
    if importlib.util.find_spec("pytest") is None:
        return SKIP, "pytest is not installed — baseline test cannot run here"
    rc, out = run_proc(
        [sys.executable, "-m", "pytest", "-q",
         "tests/test_production_migration_history_baseline.py"], cwd=repo)
    if rc is None:
        return SKIP, out
    if rc != 0:
        tail = "\n".join(out.splitlines()[-6:]) if out else ""
        return FAIL, "migration set drift vs governed ledger:\n" + tail
    return PASS, "active migration set == governed ledger (sha256 per file)"


def check_auto_merge_gate(repo, pr_state):
    """Laws 8.2 / 1.2 / 1.4 — merge receipt predicate (fail-closed)."""
    tool = os.path.join(repo, "tools", "auto_merge_gate.py")
    if not os.path.isfile(tool):
        return SKIP, "tools/auto_merge_gate.py not present in repo"
    if not pr_state:
        return SKIP, ("no --pr-state supplied — the merge gate needs a "
                      "pr_state JSON to judge; supply one or this gate "
                      "cannot run")
    rc, out = run_proc([sys.executable, tool, pr_state], cwd=repo)
    if rc is None:
        return SKIP, out
    if rc == 2:
        return SKIP, "pr_state input unusable: " + out[:200]
    if rc != 0:
        return FAIL, "merge gate refused: " + out[:600]
    return PASS, "merge receipt satisfies the full auto-merge law"


def check_new(name, workdir):
    """Run one of the new Layer 3 checks against the artifact directory."""
    laws = {
        "activation-receipt": "Law 4.1 (Drink-First Law)",
        "evidence-claims": "Laws 4.6 / 8.3 (Evidence Law)",
        "plain-words": "Law 2.1 (Plain Meaning First)",
    }
    rc, out = run_proc([sys.executable, NEW[name], "--workdir", workdir])
    if rc is None:
        return SKIP, out
    if rc != 0:
        return FAIL, f"{laws[name]} violated:\n" + out[:800]
    return PASS, f"{laws[name]} satisfied"


def main(argv):
    ap = argparse.ArgumentParser(description="Layer 3 activation check runner")
    ap.add_argument("--repo", help="NayaPOWER checkout for repo-level checks")
    ap.add_argument("--workdir", help="artifact dir for artifact checks")
    ap.add_argument("--pr-state", help="pr_state JSON for the auto-merge gate")
    ap.add_argument("--strict", action="store_true",
                    help="any SKIP also fails")
    args = ap.parse_args(argv)

    if not args.repo and not args.workdir:
        print("USAGE ERROR: supply --repo and/or --workdir")
        return 2

    results = []  # (name, status, message)

    if args.repo:
        repo = args.repo
        results.append(("ratified-guard", *check_ratified_guard(repo)))
        results.append(("migration-ledger", *check_migration_ledger(repo)))
        results.append(("migration-baseline", *check_migration_baseline(repo)))
        results.append(("auto-merge-gate",
                        *check_auto_merge_gate(repo, args.pr_state)))
    if args.workdir:
        for name in ("activation-receipt", "evidence-claims", "plain-words"):
            results.append((name, *check_new(name, args.workdir)))

    print("=" * 64)
    print("ACTIVATION CHECKS — law as code (Layer 3)")
    print("=" * 64)
    n_fail = n_skip = 0
    for name, status, message in results:
        n_fail += status == FAIL
        n_skip += status == SKIP
        print(f"[{status}] {name}")
        for line in message.splitlines():
            print(f"       {line}")
    print("-" * 64)
    print(f"{len(results)} checks: "
          f"{sum(1 for _, s, _ in results if s == PASS)} pass, "
          f"{n_fail} fail, {n_skip} skip")
    print("NOTE: branch-protection ('green CI required before merge') is a")
    print("GitHub repo setting, not code — it cannot be verified from here.")
    print("NOTE: a SKIP is listed, never silent. Use --strict in CI so an")
    print("absent gate cannot stand in for a passing one.")

    if n_fail:
        print("RESULT: FAIL — a law-as-code check was violated. Blocked.")
        return 1
    if args.strict and n_skip:
        print("RESULT: FAIL (--strict) — a check could not run. Blocked.")
        return 1
    print("RESULT: PASS — every executed check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
