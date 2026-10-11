#!/usr/bin/env python3
"""UD-12 — THE PROVING MACHINERY MUST PROVE ITSELF.

A checker that has never been tested against known-bad input is decoration.
This harness registers every proving tool (scorecards, checkers, gates,
validators), runs each tool's adversarial suite — known-good inputs must
pass, known-bad inputs must fail, edge cases must not crash — and produces
a single proving-machinery health report.

Fail-closed contract:
  * Any tool without a passing adversarial suite is UNPROVEN.
  * A suite with no teeth (no must_fail cases, duplicate IDs, malformed
    cases) is REJECTED — a rigged suite cannot launder a broken tool.
  * `gate <tool>` exits 0 only if the latest report marks the tool PROVEN
    AND the tool file's hash still matches the proven bytes. Any drift,
    any missing report, any UNPROVEN verdict -> gate refuses (exit 1).
  * `run` exits 0 only if every registered tool is PROVEN.

Other gates call `proving_machinery.py gate <tool>` before letting that
tool's verdict authorize anything.

Stdlib only.

Usage:
  python3 proving_machinery.py run [--record-dir DIR]
  python3 proving_machinery.py report [--record-dir DIR]
  python3 proving_machinery.py gate <tool-name> [--record-dir DIR]
"""

import argparse
import datetime
import hashlib
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # so `import suites.xxx` works

DEFAULT_RECORD_DIR = os.path.expanduser(
    "~/workspace/goals/bring-naya-to-life/hidden_files/enforcement/"
    "tools/proving-machinery-records")

# ---------------------------------------------------------------------------
# Registry — every proving tool that wants its verdicts trusted.
# ---------------------------------------------------------------------------

TOOL_REGISTRY = [
    {
        "name": "scorecard",
        "description": "Artifact scorecard — fixed-rubric independent scoring.",
        "suite": "suites.scorecard_adversarial",
        "tool_paths": [
            "tools/scorecard.py",                 # repo-relative, if landed
            "~/workspace/tools/scorecard.py",     # workspace build location
        ],
    },
    {
        "name": "plain-words-check",
        "description": "SL-012 plain-words-first briefing checker.",
        "suite": "suites.plain_words_adversarial",
        "tool_paths": [
            "tools/plain_words_check.py",
            "~/workspace/goals/bring-naya-to-life/hidden_files/"
            "enforcement/tools/plain_words_check.py",
        ],
    },
]

REQUIRED_KINDS = ("must_pass", "must_fail", "must_not_crash")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_repo_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def resolve_tool(entry):
    """First candidate path that exists, or None (fail closed downstream)."""
    repo_root = find_repo_root(HERE)
    for cand in entry.get("tool_paths", []):
        if cand.startswith("~") or os.path.isabs(cand):
            p = os.path.expanduser(cand)
        elif repo_root:
            p = os.path.join(repo_root, cand)
        else:
            p = os.path.join(os.getcwd(), cand)
        if os.path.isfile(p):
            return p
    # explicit env override, e.g. PROVING_TOOL_SCORECARD=/path/to/scorecard.py
    env_key = "PROVING_TOOL_" + entry["name"].upper().replace("-", "_")
    p = os.environ.get(env_key, "")
    if p and os.path.isfile(p):
        return p
    return None


def load_suite(entry):
    ref = entry["suite"]
    if isinstance(ref, str):
        return importlib.import_module(ref)
    return ref  # already a module object (tests inject doubles)


# ---------------------------------------------------------------------------
# Suite integrity — a rigged suite cannot launder a broken tool.
# ---------------------------------------------------------------------------

def check_suite_integrity(suite):
    problems = []
    for attr in ("TOOL_NAME", "TOOL_PATH_CANDIDATES", "DECLARED_EXITS",
                 "CASES", "run_case"):
        if not hasattr(suite, attr):
            problems.append("suite missing attribute '%s'" % attr)
    if problems:
        return problems
    if not callable(suite.run_case):
        problems.append("suite.run_case is not callable")
    if not suite.TOOL_PATH_CANDIDATES:
        problems.append("suite declares no tool path candidates")
    if not suite.DECLARED_EXITS:
        problems.append("suite declares no exit codes")
    cases = suite.CASES or []
    if not cases:
        problems.append("suite has zero cases")
    ids = [c.get("id") for c in cases]
    if len(set(ids)) != len(ids):
        problems.append("suite has duplicate case IDs")
    for c in cases:
        if not isinstance(c, dict):
            problems.append("non-dict case entry")
            continue
        for field in ("id", "kind", "note"):
            if field not in c:
                problems.append("case %r missing field '%s'"
                                % (c.get("id"), field))
        if c.get("kind") not in REQUIRED_KINDS:
            problems.append("case %r has bad kind %r (need one of %s)"
                            % (c.get("id"), c.get("kind"),
                               "/".join(REQUIRED_KINDS)))
    kinds = {c.get("kind") for c in cases if isinstance(c, dict)}
    for k in REQUIRED_KINDS:
        if k not in kinds:
            problems.append("suite has no '%s' cases — no teeth" % k)
    return problems


# ---------------------------------------------------------------------------
# Case evaluation
# ---------------------------------------------------------------------------

def evaluate_case(case, result):
    """Does the tool's observed behavior match what the case demands?"""
    kind, verdict = case["kind"], result["verdict"]
    ok = ((kind == "must_pass" and verdict == "pass") or
          (kind == "must_fail" and verdict == "fail") or
          (kind == "must_not_crash" and verdict in ("pass", "fail")))
    if ok:
        for s in case.get("stdout_contains", []):
            if s not in result.get("stdout", ""):
                ok = False
        for s in case.get("stdout_not_contains", []):
            if s in result.get("stdout", ""):
                ok = False
    return ok


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------

def run_one(entry, record_dir):
    name = entry["name"]
    tool_path = resolve_tool(entry)
    if not tool_path:
        return {
            "name": name, "description": entry.get("description", ""),
            "tool_path": None, "tool_sha256": None,
            "tool_paths": entry.get("tool_paths", []),
            "suite_module": (entry["suite"] if isinstance(entry["suite"], str)
                             else "injected-test-double"),
            "verdict": "UNPROVEN",
            "reasons": ["tool not found at any candidate path: %s"
                        % entry.get("tool_paths")],
            "run_utc": utcnow(),
        }
    tool_sha = sha256_file(tool_path)
    suite = load_suite(entry)
    problems = check_suite_integrity(suite)
    base = {
        "name": name, "description": entry.get("description", ""),
        "tool_path": tool_path, "tool_sha256": tool_sha,
        "tool_paths": entry.get("tool_paths", []),
        "suite_module": (entry["suite"] if isinstance(entry["suite"], str)
                         else "injected-test-double"),
    }
    if problems:
        return dict(base, **{
            "verdict": "UNPROVEN",
            "reasons": ["suite rejected: " + p for p in problems],
            "run_utc": utcnow(),
        })
    case_results = []
    workdir = os.path.join(record_dir, "work", name)
    os.makedirs(workdir, exist_ok=True)
    for case in suite.CASES:
        try:
            result = suite.run_case(case, tool_path, workdir)
        except Exception as e:  # noqa: BLE001 — adapter blew up = crash
            result = {"verdict": "crash", "exit_code": None,
                      "stdout": "", "stderr": "",
                      "detail": "adapter exception: %r" % e}
        match = evaluate_case(case, result)
        case_results.append({
            "id": case["id"], "kind": case["kind"],
            "verdict": result.get("verdict"),
            "exit_code": result.get("exit_code"),
            "match": match,
            "detail": result.get("detail", "")[:300],
            "note": case.get("note", ""),
        })
    mismatches = [c["id"] for c in case_results if not c["match"]]
    total, passed = len(case_results), sum(1 for c in case_results if c["match"])
    verdict = "PROVEN" if not mismatches else "UNPROVEN"
    return dict(base, **{
        "suite_cases": total,
        "suite_kinds": {k: sum(1 for c in case_results if c["kind"] == k)
                        for k in REQUIRED_KINDS},
        "pass_rate": (passed / total) if total else 0.0,
        "case_results": case_results,
        "verdict": verdict,
        "reasons": (["mismatched cases: " + ", ".join(mismatches)]
                    if mismatches else []),
        "run_utc": utcnow(),
    })


def run_registry(registry, record_dir):
    os.makedirs(record_dir, exist_ok=True)
    tools = [run_one(e, record_dir) for e in registry]
    report = {
        "generated_utc": utcnow(),
        "harness_sha256": sha256_file(os.path.abspath(__file__)),
        "registry": [e["name"] for e in registry],
        "tools": tools,
        "overall": ("PROVEN" if tools and
                    all(t["verdict"] == "PROVEN" for t in tools)
                    else "UNPROVEN"),
    }
    stamp = report["generated_utc"].replace(":", "").replace("-", "")
    with open(os.path.join(record_dir, "health-%s.json" % stamp), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(record_dir, "latest.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report


def print_human(report):
    print("== proving-machinery health  %s ==" % report["generated_utc"])
    for t in report["tools"]:
        kinds = t.get("suite_kinds", {})
        print("  [%s] %-18s sha256=%.12s cases=%s pass_rate=%.2f %s" % (
            t["verdict"], t["name"], t.get("tool_sha256") or "n/a",
            t.get("suite_cases", 0), t.get("pass_rate", 0.0),
            "kinds=%s" % kinds if kinds else ""))
        for r in t.get("reasons", []):
            print("       reason: %s" % r)
        for c in t.get("case_results", []):
            if not c["match"]:
                print("       MISMATCH %s (%s): tool said %s — %s" % (
                    c["id"], c["kind"], c["verdict"], c["note"]))
    print("  OVERALL: %s" % report["overall"])


# ---------------------------------------------------------------------------
# Fail-closed gate
# ---------------------------------------------------------------------------

def gate(tool_name, record_dir):
    latest = os.path.join(record_dir, "latest.json")
    if not os.path.isfile(latest):
        return 1, "no health report — run the harness first (fail closed)"
    with open(latest) as f:
        report = json.load(f)
    match = [t for t in report.get("tools", []) if t["name"] == tool_name]
    if not match:
        return 1, "tool '%s' not registered (fail closed)" % tool_name
    t = match[0]
    if t["verdict"] != "PROVEN":
        return 1, "tool '%s' is UNPROVEN: %s (fail closed)" % (
            tool_name, "; ".join(t.get("reasons", ["no reason recorded"])))
    # the proven bytes must be the current bytes — drift voids the proof.
    # Resolve from the REPORT's stored entry (the registry used at run time),
    # not the current global registry.
    pseudo_entry = {"name": tool_name,
                    "tool_paths": t.get("tool_paths", [])}
    current = resolve_tool(pseudo_entry)
    if not current or not os.path.isfile(current):
        return 1, "tool '%s' not found on disk now (fail closed)" % tool_name
    if sha256_file(current) != t.get("tool_sha256"):
        return 1, ("tool '%s' changed since it was proven "
                   "(fail closed — re-run the harness)" % tool_name)
    return 0, "tool '%s' PROVEN (sha256 %.12s, %s)" % (
        tool_name, t["tool_sha256"], t["run_utc"])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="UD-12 proving-machinery harness")
    ap.add_argument("--record-dir", default=DEFAULT_RECORD_DIR)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run", help="run every registered tool's adversarial suite")
    p_rep = sub.add_parser("report", help="print the latest health report")
    p_gate = sub.add_parser("gate", help="fail-closed gate for one tool")
    p_gate.add_argument("tool_name")
    for p in (p_run, p_rep, p_gate):
        p.add_argument("--record-dir", default=None)
    args = ap.parse_args(argv)
    record_dir = args.record_dir or DEFAULT_RECORD_DIR

    if args.cmd == "run":
        report = run_registry(TOOL_REGISTRY, record_dir)
        print_human(report)
        return 0 if report["overall"] == "PROVEN" else 1
    if args.cmd == "report":
        latest = os.path.join(record_dir, "latest.json")
        if not os.path.isfile(latest):
            print("no health report yet — run the harness first")
            return 1
        with open(latest) as f:
            print_human(json.load(f))
        return 0
    if args.cmd == "gate":
        code, msg = gate(args.tool_name, record_dir)
        print(msg)
        return code
    return 1


if __name__ == "__main__":
    sys.exit(main())
