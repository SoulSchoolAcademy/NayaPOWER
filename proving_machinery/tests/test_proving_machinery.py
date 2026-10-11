#!/usr/bin/env python3
"""Adversarial test for the proving-machinery harness itself (UD-12).

The harness must catch:
  1. A RIGGED TOOL — an adapter that always says "pass" (a checker that
     can't catch bugs). Its must_fail cases must mismatch -> UNPROVEN.
  2. A RIGGED SUITE — a suite with no must_fail cases (no teeth).
     Suite integrity must reject it -> UNPROVEN.
  3. A CRASHING tool -> UNPROVEN.
  4. STALE PROOF — gate() must refuse when the tool file changed since
     the proven run, when there is no report, or when the tool is UNPROVEN.

An honest tool with an honest suite must come out PROVEN — the harness
must not reject everything.

Run: python3 tests/test_proving_machinery.py
Exit 0 = harness catches everything it must. Exit 1 = harness is broken.
Stdlib only.
"""

import json
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, PKG)

import proving_machinery as pm  # noqa: E402


def make_suite(cases, name="fake-tool"):
    mod = types.ModuleType("fake_suite_" + name)
    mod.TOOL_NAME = name
    mod.TOOL_PATH_CANDIDATES = ["fake/path.py"]  # entry.tool_paths is authoritative
    mod.DECLARED_EXITS = {0, 1}
    mod.CASES = cases
    return mod


HONEST_CASES = [
    {"id": "T1", "kind": "must_pass", "note": "good input passes"},
    {"id": "T2", "kind": "must_pass", "note": "good input passes"},
    {"id": "T3", "kind": "must_fail", "note": "bad input fails"},
    {"id": "T4", "kind": "must_fail", "note": "bad input fails"},
    {"id": "T5", "kind": "must_not_crash", "note": "edge does not crash"},
]


def honest_run_case(case, tool_path, workdir):
    # a truthful tool: passes good input, fails bad input
    verdict = {"must_pass": "pass", "must_fail": "fail",
               "must_not_crash": "pass"}[case["kind"]]
    return {"verdict": verdict, "exit_code": 0 if verdict == "pass" else 1,
            "stdout": "", "stderr": "", "detail": ""}


def rigged_run_case(case, tool_path, workdir):
    # a DECORATION tool: everything passes, catches nothing
    return {"verdict": "pass", "exit_code": 0, "stdout": "",
            "stderr": "", "detail": "always pass"}


def crashing_run_case(case, tool_path, workdir):
    return {"verdict": "crash", "exit_code": 137, "stdout": "",
            "stderr": "traceback...", "detail": "segfault"}


def make_entry(name, suite_mod, run_case, tool_file=None):
    suite_mod.run_case = run_case
    return {"name": name, "description": "test double",
            "suite": suite_mod,
            "tool_paths": [tool_file] if tool_file else []}


RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name +
          (" — " + detail if detail and not cond else ""))


def main():
    tmp = tempfile.mkdtemp(prefix="pm-test-")
    record_dir = os.path.join(tmp, "records")

    # 1. honest tool + honest suite -> PROVEN
    tool_file = os.path.join(tmp, "honest_tool.py")
    with open(tool_file, "w") as f:
        f.write("# honest tool v1\n")
    e1 = make_entry("honest", make_suite(HONEST_CASES), honest_run_case, tool_file)
    r1 = pm.run_one(e1, record_dir)
    check("honest tool is PROVEN", r1["verdict"] == "PROVEN", str(r1.get("reasons")))

    # 2. RIGGED TOOL (always passes) + honest suite -> UNPROVEN (must catch)
    e2 = make_entry("rigged-tool", make_suite(HONEST_CASES), rigged_run_case, tool_file)
    r2 = pm.run_one(e2, record_dir)
    caught = (r2["verdict"] == "UNPROVEN" and
              any("T3" in r for r in r2.get("reasons", [])))
    check("rigged tool is caught (UNPROVEN, must_fail mismatches)",
          caught, str(r2.get("reasons")))

    # 3. RIGGED SUITE (no must_fail cases) -> rejected, UNPROVEN (must catch)
    toothless = [c for c in HONEST_CASES if c["kind"] != "must_fail"]
    e3 = make_entry("rigged-suite", make_suite(toothless), honest_run_case, tool_file)
    r3 = pm.run_one(e3, record_dir)
    rejected = (r3["verdict"] == "UNPROVEN" and
                any("no 'must_fail'" in r for r in r3.get("reasons", [])))
    check("rigged suite is rejected (no teeth -> UNPROVEN)",
          rejected, str(r3.get("reasons")))

    # 4. crashing tool -> UNPROVEN
    e4 = make_entry("crasher", make_suite(HONEST_CASES), crashing_run_case, tool_file)
    r4 = pm.run_one(e4, record_dir)
    check("crashing tool is UNPROVEN", r4["verdict"] == "UNPROVEN",
          str(r4.get("reasons")))

    # 5. gate() behavior — write a report first via run_registry
    report = pm.run_registry([e1, e2], record_dir)
    code, msg = pm.gate("honest", record_dir)
    check("gate allows PROVEN tool", code == 0, msg)
    code, msg = pm.gate("rigged-tool", record_dir)
    check("gate refuses UNPROVEN tool", code == 1, msg)
    code, msg = pm.gate("no-such-tool", record_dir)
    check("gate refuses unregistered tool", code == 1, msg)

    # 6. STALE PROOF — tool file changes after the proven run -> gate refuses
    with open(tool_file, "a") as f:
        f.write("# changed after proof\n")
    code, msg = pm.gate("honest", record_dir)
    check("gate refuses after tool bytes changed", code == 1, msg)

    # 7. no report at all -> gate refuses (fail closed)
    code, msg = pm.gate("honest", os.path.join(tmp, "empty-records"))
    check("gate refuses with no health report", code == 1, msg)

    # 8. full run exit contract: registry with an UNPROVEN tool -> overall UNPROVEN
    check("overall is UNPROVEN when any tool is", report["overall"] == "UNPROVEN",
          report["overall"])

    failed = [n for n, ok, _ in RESULTS if not ok]
    print("\n%d/%d harness self-tests passed" %
          (len(RESULTS) - len(failed), len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
