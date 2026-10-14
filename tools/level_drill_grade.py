#!/usr/bin/env python3
"""External grader for the key-split level drill (Lane 9, t0730).

Scoring seat only. Takes a subject's blind answers and the SEALED key file,
emits PASS/FAIL. The subject's eyes never touch the key path.

Usage:
    python3 tools/level_drill_grade.py --answers answers.json --key tools/level_drill_key.py

answers.json: {"S1": 2, "S2": 4, ...} (id -> rung, rungs in -9..+9).

Scoring (identical to the t0720 instrument's math): exact rung = 1.0,
off by one = 0.5, anything else = 0.0. PASS iff mean score >= 0.8 AND the
worst miss is at most one rung.

Fail closed, always: a missing/unreadable key refuses to score (exit 1),
never guesses. Incomplete answers, unknown ids, or out-of-range rungs are
also refusals, not silent zeros — a verdict must be earned, not defaulted.

Exit 0 = scored, verdict printed as JSON. Exit 1 = refused, reason printed.
Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import sys


def fail(msg):
    print(f"DRILL GRADER REFUSED: {msg}", file=sys.stderr)
    sys.exit(1)


def load_key(path):
    if not os.path.isfile(path):
        fail(f"key file not found: {path} — refusing to score without the sealed key.")
    spec = importlib.util.spec_from_file_location("level_drill_key", path)
    if spec is None or spec.loader is None:
        fail(f"cannot load key module: {path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        fail(f"key module failed to import ({e}) — refusing.")
    key = getattr(mod, "KEY", None)
    if not isinstance(key, dict) or not key:
        fail("key file has no usable KEY dict — refusing.")
    return key


def grade(answer, truth):
    if answer == truth:
        return 1.0
    if abs(answer - truth) == 1:
        return 0.5
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--key", required=True)
    args = ap.parse_args()

    key = load_key(args.key)
    try:
        with open(args.answers) as f:
            answers = json.load(f)
    except Exception as e:
        fail(f"answers file unreadable ({e})")

    if not isinstance(answers, dict):
        fail("answers must be a JSON object of id -> rung")
    ids = set(key)
    if set(answers) != ids:
        missing = sorted(ids - set(answers))
        extra = sorted(set(answers) - ids)
        detail = []
        if missing:
            detail.append(f"missing: {missing}")
        if extra:
            detail.append(f"unknown ids: {extra}")
        fail("incomplete drill — " + "; ".join(detail))
    for sid, rung in answers.items():
        if not isinstance(rung, int) or not (-9 <= rung <= 9):
            fail(f"{sid}: {rung!r} is not a ladder rung (-9..+9)")

    per, detail = {}, {}
    for sid, (truth, label) in key.items():
        s = grade(answers[sid], truth)
        per[sid] = s
        detail[sid] = {"answer": answers[sid], "truth": truth,
                       "label": label, "score": s}
    score = round(sum(per.values()) / len(per), 3)
    worst = max(abs(answers[sid] - key[sid][0]) for sid in ids)
    verdict = "PASS" if score >= 0.8 and worst <= 1 else "FAIL"
    print(json.dumps({"verdict": verdict, "score": score,
                      "worst_miss": worst, "per": detail}, indent=2))


if __name__ == "__main__":
    main()
