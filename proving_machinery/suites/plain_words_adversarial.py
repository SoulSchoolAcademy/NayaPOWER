"""Adversarial suite for the SL-012 plain-words-first checker.

The checker's job: every identifier in a briefing must arrive with plain
words touching it. A bare number is never the message. These cases pin the
behaviors the checker was built and fixed against — including the
false-negative the author caught during construction ("and #2062" must fail).

Verdict mapping (adapter): exit 0 -> pass (all glossed), exit 1 -> fail
(bare identifiers found), anything else incl. timeout/exception -> crash.
"""

import subprocess
import sys

TOOL_NAME = "plain-words-check"
TOOL_PATH_CANDIDATES = [
    "tools/plain_words_check.py",
    "~/workspace/goals/bring-naya-to-life/hidden_files/"
    "enforcement/tools/plain_words_check.py",
]
DECLARED_EXITS = {0, 1}
TIMEOUT_S = 30


def run_case(case, tool_path, workdir):
    text = case.get("text", "")
    stdin_b = text.encode("utf-8", errors="replace")
    try:
        r = subprocess.run([sys.executable, tool_path],
                           input=stdin_b, capture_output=True,
                           timeout=TIMEOUT_S, cwd=workdir)
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
            "detail": (out.strip().splitlines() or [""])[0][:200]}


CASES = [
    # ---------------- must_pass: identifiers arrive WITH plain words ----------------
    {"id": "PP1", "kind": "must_pass",
     "note": "label touching the number passes",
     "text": "The trial runs after two code changes merge: the nine-node "
             "wiring (#2062) and the learning-yield scorer (#2104)."},
    {"id": "PP2", "kind": "must_pass",
     "note": "parenthetical label passes",
     "text": "Posted to the coordination board (#2175)."},
    {"id": "PP3", "kind": "must_pass",
     "note": "bare comment ID inside a labeled parenthetical passes",
     "text": "See the freeze notice (comment 6103944483)."},
    {"id": "PP4", "kind": "must_pass",
     "note": "no identifiers at all passes",
     "text": "The harness ran clean and every tool is proven."},
    {"id": "PP5", "kind": "must_pass",
     "note": "dash gloss after the number passes",
     "text": "The draft smart-notes carrier (#1825 — never merge it) holds the notes."},
    {"id": "PP6", "kind": "must_pass",
     "note": "weak-but-present label ('See #2175') passes — the checker is lenient here by design",
     "text": "See #2175."},
    # ---------------- must_fail: bare numbers must be caught ----------------
    {"id": "PF1", "kind": "must_fail",
     "note": "the original violation: numbers as the message",
     "text": "Blocked on #2062 merge + #2104 merge."},
    {"id": "PF2", "kind": "must_fail",
     "note": "the author's own bad sentence from the SL-012 incident",
     "text": "The trial itself runs after the freeze lifts and #2062/#2104 merge."},
    {"id": "PF3", "kind": "must_fail",
     "note": "bare comment ID with only a type-word before it",
     "text": "See comment 6103944483 for the freeze notice."},
    {"id": "PF4", "kind": "must_fail",
     "note": "bare SHA with only a preposition before it",
     "text": "Deployed as f2c614a53."},
    {"id": "PF5", "kind": "must_fail",
     "note": "bare branch name after a preposition",
     "text": "Pushed to naya4/ud-12-proving-machinery."},
    {"id": "PF6", "kind": "must_fail",
     "note": "identifier leading the sentence",
     "text": "#2062 merged."},
    # ---------------- must_not_crash: hostile input, clean exit ----------------
    {"id": "PE1", "kind": "must_not_crash",
     "note": "empty input exits 0",
     "text": ""},
    {"id": "PE2", "kind": "must_not_crash",
     "note": "1MB of plain text does not crash",
     "text": "a" * 1_000_000},
    {"id": "PE3", "kind": "must_not_crash",
     "note": "emoji soup around an identifier does not crash",
     "text": "\U0001F600\U0001F680 #12345 \u2603" * 1000},
    {"id": "PE4", "kind": "must_not_crash",
     "note": "lone parenthesis does not crash",
     "text": "((("},
    {"id": "PE5", "kind": "must_not_crash",
     "note": "identifier-like noise at boundaries does not crash",
     "text": "# f2c614a53# #99999999999999999999 naya4/"},
]
