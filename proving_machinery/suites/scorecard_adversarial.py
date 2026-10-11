"""Adversarial suite for the artifact scorecard (tools/scorecard.py).

The scorecard's job: refuse self-certification, demand cited evidence per
dimension, never grant readiness above the evidence. Every case below pins
one of those behaviors. If the scorecard ever stops refusing, stops demanding
evidence, or inflates readiness, this suite catches it.

Verdict mapping (adapter): exit 0 -> pass (emitted), exit 2/3 -> fail
(refused/unreadable), anything else incl. timeout/exception -> crash.
"""

import os
import subprocess
import sys

TOOL_NAME = "scorecard"
TOOL_PATH_CANDIDATES = [
    "tools/scorecard.py",
    "~/workspace/tools/scorecard.py",
]
DECLARED_EXITS = {0, 2, 3}
TIMEOUT_S = 45

DIMS = ["usefulness", "helpfulness", "logic", "intelligence",
        "ux", "speed", "efficiency", "effectiveness"]


def _scores(all_score, evidence="cited: independent test run 2026-10-10"):
    return {d: {"score": all_score, "evidence": evidence} for d in DIMS}


def run_case(case, tool_path, workdir):
    """Run the scorecard CLI on the case. Never raises for tool behavior."""
    case_dir = os.path.join(workdir, "cases", case["id"])
    os.makedirs(case_dir, exist_ok=True)
    files = dict(case.get("files", {}))
    argv = [sys.executable, tool_path, "--no-record"]
    for a in case.get("argv", []):
        argv.append(a.replace("{CASEDIR}", case_dir))
    for rel, content in files.items():
        p = os.path.join(case_dir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        mode = "wb" if isinstance(content, bytes) else "w"
        with open(p, mode) as f:
            f.write(content)
    stdin = case.get("stdin")
    stdin_b = stdin.encode("utf-8", errors="replace") if isinstance(stdin, str) else stdin
    try:
        r = subprocess.run(argv, input=stdin_b, capture_output=True,
                           timeout=TIMEOUT_S, cwd=case_dir)
    except subprocess.TimeoutExpired:
        return {"verdict": "crash", "exit_code": None, "stdout": "",
                "stderr": "", "detail": "timeout after %ss" % TIMEOUT_S}
    except Exception as e:  # noqa: BLE001
        return {"verdict": "crash", "exit_code": None, "stdout": "",
                "stderr": "", "detail": "adapter exception: %r" % e}
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    if r.returncode == 0:
        verdict = "pass"
    elif r.returncode in DECLARED_EXITS:
        verdict = "fail"
    else:
        verdict = "crash"
    return {"verdict": verdict, "exit_code": r.returncode,
            "stdout": out, "stderr": err,
            "detail": (err.strip().splitlines() or [""])[0][:200]}


def _json_file(scores):
    import json
    return json.dumps(scores)


_GOOD_TEXT = (
    "The proving-machinery harness registers every proving tool, runs each "
    "tool's adversarial suite, and produces a single health report. "
    "Known-good inputs must pass, known-bad inputs must fail, edge cases "
    "must not crash. Any tool without a passing suite is UNPROVEN and "
    "blocked from gating anything."
)

CASES = [
    # ---------------- must_pass: valid invocations must emit ----------------
    {"id": "SP1", "kind": "must_pass", "note": "heuristic triage emits, labeled TRIAGE-",
     "argv": ["--area", "document", "--auto", "--input-file", "{CASEDIR}/artifact.txt"],
     "files": {"artifact.txt": _GOOD_TEXT * 20},
     "stdout_contains": ["TRIAGE-"]},
    {"id": "SP2", "kind": "must_pass", "note": "complete explicit scorecard emits",
     "argv": ["--area", "code", "--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json", "--json"],
     "files": {"scores.json": _json_file(_scores(7))},
     "stdout_contains": ['"readiness": "VERIFIED"']},
    {"id": "SP3", "kind": "must_pass",
     "note": "independent verification evidence gates PROVEN",
     "argv": ["--area", "code", "--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json",
              "--verification-evidence", "independent test run 23/23 green",
              "--json"],
     "files": {"scores.json": _json_file(_scores(9))},
     "stdout_contains": ['"readiness": "PROVEN"']},
    {"id": "SP4", "kind": "must_pass", "note": "--rubric prints and exits 0",
     "argv": ["--rubric"],
     "stdout_contains": ["USEFULNESS"]},
    {"id": "SP5", "kind": "must_pass",
     "note": "self-score WITH logged override is allowed (reason goes to the record)",
     "argv": ["--area", "document", "--scorer", "Naya 4", "--doer", "Naya 4",
              "--self-score-override", "single-seat night shift, logged",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file(_scores(6))}},
    # ---------------- must_fail: the tool must refuse ----------------
    {"id": "SF1", "kind": "must_fail",
     "note": "scorer == doer without override is refused (no self-certification)",
     "argv": ["--scorer", "Naya 4", "--doer", "naya 4",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file(_scores(8))}},
    {"id": "SF2", "kind": "must_fail", "note": "score file missing a dimension is refused",
     "argv": ["--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file({d: {"score": 7, "evidence": "x"}
                                          for d in DIMS if d != "logic"})}},
    {"id": "SF3", "kind": "must_fail", "note": "out-of-range score (11) is refused",
     "argv": ["--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file(
         {d: {"score": (11 if d == "logic" else 7), "evidence": "cited"} for d in DIMS})}},
    {"id": "SF4", "kind": "must_fail", "note": "score without cited evidence is refused",
     "argv": ["--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file(
         {d: {"score": 7, "evidence": ("" if d == "ux" else "cited")} for d in DIMS})}},
    {"id": "SF5", "kind": "must_fail", "note": "malformed score JSON is refused",
     "argv": ["--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": "{not json at all"}},
    {"id": "SF6", "kind": "must_fail",
     "note": "real scorecard without a named scorer is refused",
     "argv": ["--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json"],
     "files": {"scores.json": _json_file(_scores(7))}},
    {"id": "SF7", "kind": "must_fail",
     "note": "neither --score nor --auto is refused",
     "argv": ["--scorer", "Naya 2", "--text", _GOOD_TEXT]},
    {"id": "SF8", "kind": "must_fail", "note": "empty artifact text is refused",
     "argv": ["--scorer", "Naya 2", "--auto", "--text", "   "]},
    {"id": "SF9", "kind": "must_pass",
     "note": "high scores WITHOUT verification evidence cap at VERIFIED, never PROVEN",
     "argv": ["--area", "code", "--scorer", "Naya 2", "--doer", "Coda 1",
              "--text", _GOOD_TEXT, "--score", "{CASEDIR}/scores.json", "--json"],
     "files": {"scores.json": _json_file(_scores(9))},
     "stdout_contains": ['"readiness": "VERIFIED"'],
     "stdout_not_contains": ['"readiness": "PROVEN"']},
    # ---------------- must_not_crash: hostile input, clean exit ----------------
    {"id": "SE1", "kind": "must_not_crash", "note": "missing input file exits 3, no traceback",
     "argv": ["--scorer", "Naya 2", "--auto", "--input-file", "{CASEDIR}/nope.txt"]},
    {"id": "SE2", "kind": "must_not_crash", "note": "missing score file exits 2, no traceback",
     "argv": ["--scorer", "Naya 2", "--text", _GOOD_TEXT,
              "--score", "{CASEDIR}/nope.json"]},
    {"id": "SE3", "kind": "must_not_crash", "note": "1MB unicode artifact does not crash",
     "argv": ["--scorer", "Naya 2", "--auto", "--input-file", "{CASEDIR}/big.txt"],
     "files": {"big.txt": ("héllo wörld \U0001F600 " * 40000)}},
    {"id": "SE4", "kind": "must_not_crash", "note": "unreachable URL exits 3, no hang, no traceback",
     "argv": ["--scorer", "Naya 2", "--auto", "--url", "http://127.0.0.1:1/"]},
    {"id": "SE5", "kind": "must_not_crash", "note": "binary-ish bytes in artifact do not crash",
     "argv": ["--scorer", "Naya 2", "--auto", "--input-file", "{CASEDIR}/bin.dat"],
     "files": {"bin.dat": bytes(range(256)) * 100}},
]
