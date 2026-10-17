#!/usr/bin/env python3
"""Exact-tip organism health receipt -- CODA 3, Naya 2 master directive 2026-10-05.

Takes a main SHA and produces ONE machine-readable health card (JSON) at a
canonical path, plus a human-readable one-page summary (same data, warm tone).

The receipt is a DERIVED VIEW, not a maintained document: every field is
measured from live sources at the pinned SHA. Re-running on any SHA
reproduces that SHA's receipt. If the underlying data changes, the receipt
changes -- that is the whole point.

Usage:
    python tools/organism_health_receipt.py --sha <main-sha>
        [--repo PATH] [--out PATH] [--human-out PATH] [--timeout SEC]

Defaults:
    --repo       the git repository containing this script
    --out        evidence/organism-health/ORGANISM-HEALTH-RECEIPT.json
    --human-out  evidence/organism-health/ORGANISM-HEALTH-RECEIPT.md
Outputs are written relative to --repo (the branch checkout), never into
the measured tree when a temp worktree is used.

Measurement rule: if --repo's HEAD is not --sha, a temporary detached
worktree at --sha is created, measured, and removed. The receipt records
whether HEAD matched. Read-only: the tool never touches the production
branch, the production database, credentials, workflows, or any remote.

Law above all laws here: a receipt that says HEALTHY when something is red
is worse than no receipt. Bias toward flagging. Statuses are PASS / FLAG /
UNKNOWN. Overall is HEALTHY only if EVERY area is PASS. UNKNOWN is not
healthy. False alarms get tuned; missed reds erode trust.

Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

TOOL_VERSION = "1.1.0"
SCHEMA = "naya.organism.health.receipt/v1"

# First non-PASS in this order becomes top_problem. Rationale: build
# integrity, then safety, then deploy truth, then data parity, then memory
# integrity, then chain completeness, then retrieval, then learning and
# drill freshness. Documented so the ranking itself is inspectable.
PRIORITY_RANK = [
    "kernel_suite",
    "poison_battery",
    "production_parity",
    "migration_parity",
    "smart_note_index",
    "chain_readiness",
    "know_retrieval",
    "learning_proof",
    "cold_successor_drill",
]

FRESH_DAYS = 7  # canary / experiment / drill freshness threshold


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def parse_ts(value: str) -> datetime.datetime | None:
    try:
        t = value.strip()
        if t.endswith("Z"):
            t = t[:-1] + "+00:00"
        dt = datetime.datetime.fromisoformat(t)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    except (ValueError, TypeError, AttributeError):
        return None


def run(cmd: list[str], cwd: Path, timeout: int, tail: int = 12) -> dict:
    """Run a command, never raise. Returns exit/stdout-tail/stderr-tail."""
    try:
        p = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True,
            timeout=timeout, errors="replace",
        )
        out = (p.stdout or "").splitlines()
        err = (p.stderr or "").splitlines()
        return {
            "command": " ".join(cmd),
            "exit": p.returncode,
            "stdout_tail": out[-tail:],
            "stderr_tail": err[-8:],
            "timed_out": False,
        }
    except FileNotFoundError as e:
        return {"command": " ".join(cmd), "exit": None, "stdout_tail": [],
                "stderr_tail": [f"NOT_FOUND: {e}"], "timed_out": False}
    except subprocess.TimeoutExpired:
        return {"command": " ".join(cmd), "exit": None, "stdout_tail": [],
                "stderr_tail": [f"TIMEOUT after {timeout}s"], "timed_out": True}


def git(repo: Path, *args: str, timeout: int = 120) -> dict:
    return run(["git", *args], cwd=repo, timeout=timeout)


def area(status: str, summary: str, evidence: dict, details: dict | None = None) -> dict:
    assert status in ("PASS", "FLAG", "UNKNOWN")
    return {"status": status, "summary": summary, "evidence": evidence,
            "details": details or {}}


# ---------------------------------------------------------------- instruments

def measure_kernel(tree: Path, timeout: int) -> dict:
    node = shutil.which("node")
    if not node:
        return area("UNKNOWN", "node not found; kernel JS tests unmeasurable here.",
                    {"command": "node --version", "exit": None})
    test_files = sorted(glob.glob(str(tree / "tests" / "*.test.mjs")))
    if not test_files:
        return area("UNKNOWN", "no tests/*.test.mjs at this SHA.",
                    {"files_glob": "tests/*.test.mjs"})
    node_res = run([node, "--test", *test_files], cwd=tree, timeout=timeout)
    node_pass = node_fail = node_total = None
    # re-scan output tail for the summary counters
    full = node_res["stdout_tail"]
    for line in full:
        mp = re.search(r"pass\s+(\d+)", line)
        mf = re.search(r"fail\s+(\d+)", line)
        mt = re.search(r"tests\s+(\d+)", line)
        if "pass" in line and mp:
            node_pass = int(mp.group(1))
        if "fail" in line and mf:
            node_fail = int(mf.group(1))
        if "tests" in line and mt and node_total is None:
            node_total = int(mt.group(1))
    py_res = run([sys.executable, "-m", "pytest", "-q"], cwd=tree, timeout=timeout)
    py_pass = py_fail = py_skip = None
    for line in py_res["stdout_tail"]:
        mp = re.search(r"(\d+)\s+passed", line)
        mf = re.search(r"(\d+)\s+failed", line)
        ms = re.search(r"(\d+)\s+skipped", line)
        if mp:
            py_pass = int(mp.group(1))
        if mf:
            py_fail = int(mf.group(1))
        if ms:
            py_skip = int(ms.group(1))
    ev = {"node": node_res, "pytest": py_res,
          "node_files": len(test_files),
          "node_counts": {"total": node_total, "pass": node_pass, "fail": node_fail},
          "pytest_counts": {"pass": py_pass, "fail": py_fail, "skip": py_skip}}
    if node_res["timed_out"] or py_res["timed_out"] or node_res["exit"] is None:
        return area("UNKNOWN", "kernel instrument timed out or missing; not measured.",
                    ev)
    blob = "\n".join(py_res["stdout_tail"] + py_res["stderr_tail"])
    if py_res["exit"] != 0 and "No module named 'fcntl'" in blob and (node_fail or 0) == 0:
        # POSIX-only repo tooling (smart_note_v2 imports fcntl): collection
        # fails on win32 before a single test runs. This is a measurement
        # platform limit, NOT a red on the bytes. Defer to Linux CI.
        return area("UNKNOWN",
                    f"pytest UNMEASURABLE on this runner (win32 lacks fcntl; 3 files fail "
                    f"collection before running). Node suite green ({node_total}/{node_total}). "
                    f"Kernel verdict deferred to Linux CI.",
                    ev)
    fails = (node_fail or 0) + (py_fail or 0)
    if node_res["exit"] == 0 and py_res["exit"] == 0 and fails == 0:
        return area("PASS",
                    f"node {node_total}/{node_total} + pytest {py_pass} passed, 0 failed on exact bytes.",
                    ev)
    return area("FLAG",
                f"kernel RED on exact bytes: node fail={node_fail}, pytest fail={py_fail} "
                f"(node exit {node_res['exit']}, pytest exit {py_res['exit']}).",
                ev)


def measure_chain(tree: Path, timeout: int) -> dict:
    script = tree / "BRAIN" / "12-ENGINEERING" / "verify-collective-chain-readiness.py"
    baseline_f = tree / "BRAIN" / "12-ENGINEERING" / "CHAIN-READINESS-BASELINE.json"
    if not script.exists():
        return area("UNKNOWN", "chain readiness script absent at this SHA.", {})
    res = run([sys.executable, str(script)], cwd=tree, timeout=timeout, tail=40)
    satisfied = None
    for line in res["stdout_tail"]:
        m = re.search(r"(\d+)/11 links SATISFIED", line)
        if m:
            satisfied = int(m.group(1))
    try:
        floor = json.loads(baseline_f.read_text(encoding="utf-8"))["satisfied_links_floor"]
    except (OSError, KeyError, ValueError):
        floor = None
    ev = {"run": res, "satisfied": satisfied, "floor": floor,
          "baseline_ref": "BRAIN/12-ENGINEERING/CHAIN-READINESS-BASELINE.json"}
    if res["timed_out"] or satisfied is None or floor is None:
        return area("UNKNOWN", "chain readiness unmeasurable (instrument error or no verdict line).", ev)
    if satisfied >= floor:
        return area("PASS",
                    f"{satisfied}/11 links SATISFIED, at/above floor {floor}: no regression. "
                    f"{11 - satisfied} links open (incompleteness, not rot).",
                    ev, {"open_links": 11 - satisfied})
    return area("FLAG",
                f"chain REGRESSION: {satisfied}/11 below floor {floor}.",
                ev)


def measure_index(tree: Path, timeout: int) -> dict:
    res = run([sys.executable, "tools/regenerate_brain_index.py", "--check"],
              cwd=tree, timeout=timeout)
    files = None
    for line in res["stdout_tail"]:
        m = re.search(r"\((\d+) files\)", line)
        if m:
            files = int(m.group(1))
    ev = {"run": res, "indexed_files": files}
    if res["timed_out"]:
        return area("UNKNOWN", "brain index --check timed out; not measured.", ev)
    if res["exit"] == 0:
        return area("PASS", f"brain index matches git tree ({files} files), no drift.", ev)
    return area("FLAG", f"brain index DRIFT on exact bytes (exit {res['exit']}).", ev)


def measure_know(tree: Path, timeout: int) -> dict:
    spec_f = tree / "tools" / "know_measure" / "query_spec_v1.json"
    harness = tree / "tools" / "know_measure" / "harness.py"
    scorer = tree / "tools" / "know_measure" / "scorer.py"
    if not (spec_f.exists() and harness.exists() and scorer.exists()):
        return area("UNKNOWN", "KNOW harness files absent at this SHA.", {})
    try:
        spec = json.loads(spec_f.read_text(encoding="utf-8"))
        pin = spec.get("corpus_pin", {}).get("git_sha")
    except (OSError, ValueError):
        return area("UNKNOWN", "KNOW spec unreadable.", {})
    head = git(tree, "rev-parse", "HEAD")["stdout_tail"]
    head_sha = head[-1].strip() if head else ""
    pin_match = (pin == head_sha)
    outdir = Path(tempfile.mkdtemp(prefix="know-run-"))
    h_res = run([sys.executable, str(harness), "--repo", str(tree),
                 "--spec", str(spec_f), "--out", str(outdir)],
                cwd=tree, timeout=timeout)
    log = outdir / "retrieval_log.jsonl"
    log_ok = log.exists()
    summary = {}
    if log_ok:
        try:
            summ_f = outdir / "summary.json"
            if summ_f.exists():
                summary = json.loads(summ_f.read_text(encoding="utf-8"))
        except ValueError:
            pass
        s_res = run([sys.executable, str(scorer), "--spec", str(spec_f),
                     "--log", str(log)], cwd=tree, timeout=timeout)
    else:
        s_res = {"command": "scorer (skipped: no retrieval log)",
                 "exit": None, "stdout_tail": [], "stderr_tail": h_res["stderr_tail"][-4:],
                 "timed_out": False}
    shutil.rmtree(outdir, ignore_errors=True)
    ev = {"harness": h_res, "scorer": s_res, "summary": summary,
          "spec_corpus_pin": pin, "measured_sha": head_sha, "pin_match": pin_match,
          "spec_ref": "tools/know_measure/query_spec_v1.json"}
    if "No module named 'fcntl'" in "\n".join(h_res["stderr_tail"]):
        # POSIX-only system under test (smart_note_v2 imports fcntl): the
        # harness cannot run on win32 at all. Platform limit, not a red.
        # Separately, the spec pin does not match the measured SHA.
        return area("UNKNOWN",
                    "KNOW UNMEASURABLE on this runner (win32 lacks fcntl; harness imports "
                    "smart_note_v2 which requires it). Rerun on Linux. Note: spec corpus pin "
                    f"{(pin or '?')[:8]} != measured {head_sha[:8]} -- expectations are "
                    "corpus-bound and need re-verification at this SHA regardless.",
                    ev)
    if h_res["timed_out"] or (not log_ok and h_res["exit"] != 0):
        return area("UNKNOWN", "KNOW harness failed to produce a log; retrieval unmeasured.", ev)
    if s_res["exit"] is None:
        return area("UNKNOWN", "KNOW scorer never ran (no retrieval log); retrieval unmeasured.", ev)
    if s_res["exit"] == 0 and pin_match:
        return area("PASS",
                    f"KNOW scorer ALL criteria pass at measured SHA (hits={summary.get('hits')}, "
                    f"misses={summary.get('misses')}); spec pin matches.",
                    ev)
    if s_res["exit"] == 0 and not pin_match:
        return area("FLAG",
                    f"KNOW scorer passes BUT spec corpus pin { (pin or '?')[:8] } != measured "
                    f"{head_sha[:8]}: expectations are corpus-bound, re-verification required.",
                    ev)
    return area("FLAG",
                f"KNOW scorer FAILS at measured SHA (exit {s_res['exit']}); retrieval needs work.",
                ev)


def measure_poison(tree: Path, timeout: int) -> dict:
    node = shutil.which("node")
    battery = tree / "tests" / "know-negative-battery.test.mjs"
    adv_script = tree / "tools" / "test_brain_index_adversarial.sh"
    adv_ev = tree / "tools" / "brain-index-adversarial-evidence-2026-09-30.md"
    if not node or not battery.exists():
        return area("UNKNOWN", "poison battery test absent or node missing.", {})
    res = run([node, "--test", str(battery)], cwd=tree, timeout=timeout)
    bpass = bfail = None
    for line in res["stdout_tail"]:
        mp = re.search(r"pass\s+(\d+)", line)
        mf = re.search(r"fail\s+(\d+)", line)
        if "pass" in line and mp:
            bpass = int(mp.group(1))
        if "fail" in line and mf:
            bfail = int(mf.group(1))
    ev = {"battery_run": res, "battery_pass": bpass, "battery_fail": bfail,
          "adversarial_script_present": adv_script.exists(),
          "adversarial_evidence_present": adv_ev.exists()}
    if res["timed_out"] or res["exit"] is None:
        return area("UNKNOWN", "poison battery run timed out; not measured.", ev)
    if res["exit"] == 0 and (bfail or 0) == 0 and (bpass or 0) > 0:
        return area("PASS", f"poison battery {bpass}/{bpass} adversarial cases rejected.", ev)
    return area("FLAG", f"poison battery RED: fail={bfail} (exit {res['exit']}).", ev)


def measure_migrations(tree: Path) -> dict:
    ledger_f = tree / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
    mig_dir = tree / "supabase" / "migrations"
    try:
        ledger = json.loads(ledger_f.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return area("UNKNOWN", f"migration ledger unreadable: {e}.", {})
    ledger_vers = {e["version"] for e in ledger.get("production_applied", [])}
    recorded_pending = {e["version"] for e in ledger.get("pending", [])}
    accounted = ledger_vers | recorded_pending
    repo_files = sorted(glob.glob(str(mig_dir / "*.sql")))
    repo_vers = {os.path.basename(f)[:14] for f in repo_files}
    orphans = sorted(ledger_vers - repo_vers)
    unaccounted = sorted(repo_vers - accounted)
    pending_review = sorted(repo_vers & recorded_pending)
    stale_pending = sorted(recorded_pending - repo_vers)
    ev = {"repo_files": len(repo_files), "ledger_versions": len(ledger_vers),
          "ledger_claimed_applied": ledger.get("production_applied_count"),
          "ledger_recorded_pending": len(recorded_pending),
          "ledger_authority_note": ledger.get("authority_note"),
          "in_ledger_applied_not_repo": orphans,
          "in_repo_not_in_ledger_at_all": unaccounted,
          "recorded_pending_not_production_applied": pending_review,
          "recorded_pending_missing_from_repo": stale_pending,
          "production_db": "NEVER CONTACTED -- lane rule forbids touching production DB/credentials; "
                           "DB side is UNKNOWN by construction."}
    if (orphans or unaccounted or stale_pending
            or len(ledger_vers) != ledger.get("production_applied_count")):
        return area("FLAG",
                    f"migration parity BROKEN: {len(unaccounted)} repo files absent from ledger, "
                    f"{len(orphans)} applied ledger versions missing from repo, {len(stale_pending)} "
                    f"recorded-pending versions missing from repo, claimed-applied count mismatch "
                    f"({ledger.get('production_applied_count')} vs {len(ledger_vers)}); "
                    f"production DB unverified.",
                    ev)
    if pending_review:
        return area("FLAG",
                    f"repo<->ledger accounting EXACT ({len(repo_files)} = {len(ledger_vers)} applied "
                    f"+ {len(pending_review)} recorded pending), but {len(pending_review)} migration(s) "
                    f"are PENDING_REVIEW_NOT_PRODUCTION_APPLIED; production DB side UNVERIFIED "
                    f"(never touched).",
                    ev)
    return area("FLAG",
                f"repo<->ledger parity EXACT ({len(repo_files)}/{len(repo_files)}), ledger claims "
                f"reconciled {ledger.get('captured_date')}; production DB side UNVERIFIED (never touched).",
                ev)


def measure_production(repo: Path, sha: str) -> dict:
    ref = git(repo, "rev-parse", "origin/production")
    if not ref["stdout_tail"]:
        return area("UNKNOWN", "origin/production ref absent locally; parity unmeasurable offline.", {})
    prod_sha = ref["stdout_tail"][-1].strip()
    subj = git(repo, "log", "-1", "--format=%s", prod_sha)
    subject = subj["stdout_tail"][-1].strip() if subj["stdout_tail"] else ""
    stamp_date = git(repo, "log", "-1", "--format=%cI", prod_sha)
    stamp_at = stamp_date["stdout_tail"][-1].strip() if stamp_date["stdout_tail"] else "?"
    m = re.search(r"([0-9a-f]{40})", subject)
    stamp_src = m.group(1) if m else None
    ev = {"production_ref": prod_sha, "stamp_subject": subject,
          "stamp_committed_at": stamp_at, "stamp_source": stamp_src, "main_sha": sha,
          "ref_note": "origin/production as fetched locally; re-fetch before acting."}
    if not stamp_src:
        return area("UNKNOWN", "production stamp subject carries no source SHA; cannot compare.", ev)
    if stamp_src == sha:
        return area("PASS", f"production stamps exact main {sha[:8]}: CURRENT.", ev)
    cnt = git(repo, "rev-list", "--count", f"{stamp_src}..{sha}")
    dist = cnt["stdout_tail"][-1].strip() if cnt["stdout_tail"] else "?"
    anc = git(repo, "merge-base", "--is-ancestor", stamp_src, sha)
    if anc["exit"] == 0:
        return area("FLAG",
                    f"production BEHIND: stamps {stamp_src[:8]}, main is {sha[:8]} "
                    f"({dist} main-commits ahead of the stamped source).",
                    ev, {"commits_behind": dist})
    return area("FLAG",
                f"production DIVERGED: stamped source {stamp_src[:8]} is not an ancestor of {sha[:8]}.",
                ev)


def file_age_days(tree: Path, rel: str, now: datetime.datetime) -> tuple | None:
    r = git(tree, "log", "-1", "--format=%cI", "--", rel)
    if not r["stdout_tail"]:
        return None
    dt = parse_ts(r["stdout_tail"][-1].strip())
    if not dt:
        return None
    return (now - dt).total_seconds() / 86400.0, dt.isoformat()


def measure_learning(tree: Path, now: datetime.datetime) -> dict:
    canaries = sorted(glob.glob(str(tree / ".naya" / "capture" / "*canary*.json")))
    cans = [os.path.relpath(c, str(tree)).replace(os.sep, "/") for c in canaries]
    can_ages = [(c, file_age_days(tree, c, now)) for c in cans]
    receipt_f = tree / "causal-learning-experiment-receipt.json"
    causal_at = causal_age = None
    if receipt_f.exists():
        try:
            rec = json.loads(receipt_f.read_text(encoding="utf-8"))
            causal_at = rec.get("causal_verification", {}).get("verified_at")
            dt = parse_ts(causal_at or "")
            if dt:
                causal_age = (now - dt).total_seconds() / 86400.0
        except ValueError:
            pass
    fresh_c = [c for c, a in can_ages if a and a[0] <= FRESH_DAYS]
    ev = {"canaries": cans, "canary_ages_days": {c: (round(a[0], 2) if a else None) for c, a in can_ages},
          "causal_verified_at": causal_at,
          "causal_age_days": round(causal_age, 2) if causal_age is not None else None,
          "fresh_threshold_days": FRESH_DAYS}
    problems = []
    if not cans:
        problems.append("no canary file committed")
    elif not fresh_c:
        oldest = min((a[0] for _, a in can_ages if a), default=None)
        problems.append(f"canary stale (newest age {oldest:.1f}d > {FRESH_DAYS}d)")
    if causal_age is None:
        problems.append("causal experiment receipt missing/unparseable")
    elif causal_age > FRESH_DAYS:
        problems.append(f"latest causal experiment {causal_age:.1f}d old (> {FRESH_DAYS}d)")
    if problems:
        return area("FLAG", "learning proof STALE: " + "; ".join(problems) + ".", ev)
    return area("PASS",
                f"learning proof FRESH: canary {len(fresh_c)}/{len(cans)} fresh, "
                f"causal experiment {causal_age:.1f}d old.", ev)


def measure_drill(tree: Path, now: datetime.datetime) -> dict:
    bank_f = tree / "tools" / "cold_retrieve_drill" / "drill_bank.json"
    try:
        bank = json.loads(bank_f.read_text(encoding="utf-8"))
        items = [i for i in bank.get("items", []) if not i.get("retired")]
    except (OSError, ValueError):
        return area("UNKNOWN", "drill bank unreadable.", {})
    tracked = git(tree, "ls-files")
    logs = [l for l in tracked["stdout_tail"]
            if re.search(r"drill[_-]?log|DRILL-RECEIPT|drill[_-]?receipt", l, re.I)]
    log_age = None
    if logs:
        ages = [file_age_days(tree, l.strip(), now) for l in logs]
        ages = [a for a in ages if a]
        if ages:
            log_age = min(a[0] for a in ages)
    ev = {"bank_items": len(items),
          "bank_ids": [i.get("id") for i in items],
          "drill_logs_tracked": logs,
          "newest_log_age_days": round(log_age, 2) if log_age is not None else None,
          "fresh_threshold_days": FRESH_DAYS}
    if log_age is not None and log_age <= FRESH_DAYS:
        return area("PASS", f"cold drill PROVEN {log_age:.1f}d ago ({len(items)} items in bank).", ev)
    if logs:
        return area("FLAG", f"cold drill STALE: newest log {log_age:.1f}d old.", ev)
    return area("FLAG",
                f"cold drill NEVER PROVEN: bank holds {len(items)} items, zero drill logs tracked.", ev)


# ---------------------------------------------------------------- rendering

def render_human(r: dict) -> str:
    L = []
    L.append(f"# Organism health -- {r['sha_measured'][:8]}")
    L.append("")
    L.append(f"Shawn -- one card, whole organism, measured {r['measured_at'][:10]} from the exact bytes "
             f"of `{r['sha_measured'][:8]}`. Nothing here is hand-written; the command at the bottom "
             f"reproduces it.")
    L.append("")
    L.append(f"## Verdict: {'HEALTHY' if r['overall'] == 'HEALTHY' else 'NOT HEALTHY'}")
    L.append("")
    tp = r.get("top_problem")
    if tp:
        L.append(f"**The top problem is {tp['area']}: {tp['headline']}**")
    else:
        L.append("Every signal is green. The organism is healthy at this tip.")
    L.append("")
    L.append("## The nine signals")
    L.append("")
    names = {"kernel_suite": "Kernel suite", "chain_readiness": "Chain readiness",
             "smart_note_index": "Smart Note index", "know_retrieval": "KNOW retrieval",
             "poison_battery": "Poison battery", "migration_parity": "Migration parity",
             "production_parity": "Production parity", "learning_proof": "Learning proof",
             "cold_successor_drill": "Cold-successor drill"}
    for key in ["kernel_suite", "chain_readiness", "smart_note_index", "know_retrieval",
                "poison_battery", "migration_parity", "production_parity",
                "learning_proof", "cold_successor_drill"]:
        a = r["areas"][key]
        dot = {"PASS": "green", "FLAG": "red", "UNKNOWN": "unknown"}[a["status"]]
        L.append(f"- **{names[key]}** ({dot}): {a['summary']}")
    if r.get("caveats"):
        L.append("")
        L.append("## Caveats -- what this card could NOT measure")
        L.append("")
        plat = r["measurement_env"].get("platform", "?")
        L.append(f"(Runner is {plat}; POSIX-only instruments defer to Linux CI.)")
        for c in r["caveats"]:
            L.append(f"- {names.get(c['area'], c['area'])}: {c['headline']}")
    L.append("")
    L.append("## What would turn this green")
    L.append("")
    for key in r["priority_rank"]:
        a = r["areas"][key]
        if a["status"] == "FLAG":
            L.append(f"- {names.get(key, key)} (red): resolve the red line above, re-run the tool, watch this go green.")
        elif a["status"] == "UNKNOWN":
            L.append(f"- {names.get(key, key)} (unmeasured): measure it per the caveat above (usually: re-run on Linux), then re-run the tool.")
    L.append("")
    L.append("## Reproduce this card")
    L.append("")
    L.append(f"`{r['how_to_regenerate']}`")
    L.append("")
    L.append(f"Measured {r['measured_at']} * tool v{r['tool_version']} * schema {r['schema']}. "
             f"False alarms get tuned; missed reds erode trust -- this card flags first.")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Exact-tip organism health receipt.")
    ap.add_argument("--sha", required=True, help="main SHA to measure")
    ap.add_argument("--repo", default=None, help="repo checkout (default: script's repo)")
    ap.add_argument("--out", default="evidence/organism-health/ORGANISM-HEALTH-RECEIPT.json")
    ap.add_argument("--human-out", default="evidence/organism-health/ORGANISM-HEALTH-RECEIPT.md")
    ap.add_argument("--timeout", type=int, default=900, help="per-instrument timeout seconds")
    args = ap.parse_args()

    script_repo = Path(__file__).resolve().parents[1]
    repo = Path(args.repo).resolve() if args.repo else script_repo
    sha = args.sha.strip()

    exists = git(repo, "cat-file", "-t", sha)
    if not (exists["stdout_tail"] and exists["stdout_tail"][-1].strip() == "commit"):
        print(f"FAIL: {sha} is not a commit in {repo}", file=sys.stderr)
        return 2

    head = git(repo, "rev-parse", "HEAD")
    head_sha = head["stdout_tail"][-1].strip() if head["stdout_tail"] else ""
    tmp_wt = None
    try:
        if head_sha == sha:
            tree = repo
            head_matched = True
        else:
            # Short base path: this repo's tree contains ~240-char paths that
            # exceed win32 MAX_PATH under deep temp dirs. core.longpaths
            # covers git; the short base covers everything else.
            wt_base = repo.parent
            tmp_wt = Path(tempfile.mkdtemp(prefix="om-", dir=str(wt_base)))
            shutil.rmtree(tmp_wt)
            c = git(repo, "-c", "core.longpaths=true", "worktree", "add",
                    "--detach", str(tmp_wt), sha, timeout=300)
            if c["exit"] != 0:
                print(f"FAIL: could not materialize worktree at {sha}", file=sys.stderr)
                for line in (c["stderr_tail"] or [])[-4:]:
                    print(f"git: {line}", file=sys.stderr)
                return 2
            tree = tmp_wt
            head_matched = False

        now = utcnow()
        py_v = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        node_v = run(["node", "--version"], cwd=tree, timeout=60)["stdout_tail"]
        areas = {
            "kernel_suite": measure_kernel(tree, args.timeout),
            "chain_readiness": measure_chain(tree, args.timeout),
            "smart_note_index": measure_index(tree, args.timeout),
            "know_retrieval": measure_know(tree, min(args.timeout, 600)),
            "poison_battery": measure_poison(tree, args.timeout),
            "migration_parity": measure_migrations(tree),
            "production_parity": measure_production(repo, sha),
            "learning_proof": measure_learning(tree, now),
            "cold_successor_drill": measure_drill(tree, now),
        }
        overall = "HEALTHY" if all(a["status"] == "PASS" for a in areas.values()) else "NOT_HEALTHY"
        # Proven reds lead: top_problem is the first FLAG in priority order.
        # UNKNOWNs are measurement caveats, listed separately -- an unmeasured
        # area must never masquerade as the diagnosed problem while a proven
        # red exists. If nothing is red but something is unmeasured, the
        # first UNKNOWN becomes top_problem (cannot claim healthy).
        top = None
        for key in PRIORITY_RANK:
            if areas[key]["status"] == "FLAG":
                top = {"area": key, "headline": areas[key]["summary"],
                       "evidence": areas[key]["evidence"]}
                break
        if top is None:
            for key in PRIORITY_RANK:
                if areas[key]["status"] == "UNKNOWN":
                    top = {"area": key, "headline": areas[key]["summary"],
                           "evidence": areas[key]["evidence"]}
                    break
        caveats = [{"area": k, "headline": areas[k]["summary"]}
                   for k in PRIORITY_RANK if areas[k]["status"] == "UNKNOWN"]
        receipt = {
            "schema": SCHEMA,
            "sha_measured": sha,
            "measured_at": now.isoformat(),
            "measured_by": "tools/organism_health_receipt.py (CODA 3)",
            "tool_version": TOOL_VERSION,
            "measurement_env": {
                "python": py_v,
                "node": (node_v[-1].strip() if node_v else "?"),
                "platform": sys.platform,
                "head_matched_sha": head_matched,
            },
            "overall": overall,
            "top_problem": top,
            "caveats": caveats,
            "priority_rank": PRIORITY_RANK,
            "areas": areas,
            "how_to_regenerate": f"python tools/organism_health_receipt.py --sha {sha}",
        }
        out_p = (repo / args.out) if not os.path.isabs(args.out) else Path(args.out)
        hum_p = (repo / args.human_out) if not os.path.isabs(args.human_out) else Path(args.human_out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        hum_p.write_text(render_human(receipt), encoding="utf-8")
        print(f"overall={overall} sha={sha[:8]}")
        if top:
            print(f"top_problem={top['area']}: {top['headline']}")
        else:
            print("top_problem=none: all signals green")
        print(f"json={out_p}")
        print(f"human={hum_p}")
        return 0
    finally:
        if tmp_wt is not None:
            git(repo, "worktree", "remove", "--force", str(tmp_wt), timeout=300)


if __name__ == "__main__":
    raise SystemExit(main())
