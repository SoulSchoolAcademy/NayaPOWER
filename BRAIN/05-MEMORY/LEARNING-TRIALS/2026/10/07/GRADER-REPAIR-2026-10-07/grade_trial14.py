#!/usr/bin/env python3
"""Grader for Trial-14: real lesson (state file ternary).

REPAIRED (2026-10-07, Naya 2 verification #1354/6048866319):
- No extraction defects found in t14 ("no grader diffs" per verification).
- Fix (minor): added main() for standalone re-run.
- Fix (PROVENANCE GAP): stats formula documented below.

Stats (documented per PROVENANCE GAP fix):
- Fisher's exact test (two-tailed) on 2x2 contingency.
- Cohen's h = 2*arcsin(sqrt(p_treat)) - 2*arcsin(sqrt(p_ctrl))
- Tier-S threshold: p < 0.001 AND |h| > 1.0.
"""
import json, re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_correct():
    key_path = os.path.join(BASE, "answer_key.json")
    if os.path.exists(key_path):
        with open(key_path) as f:
            return json.load(f)
    return {
        "Q1": "UNSAFE", "Q2": "SAFE", "Q3": "SAFE",
        "Q4": "UNSAFE", "Q5": "SAFE", "Q6": "UNSAFE",
        "Q7": "SAFE", "Q8": "UNSAFE", "Q9": "SAFE",
    }

CORRECT = load_correct()

def extract_choice(text):
    t = text.lower()
    head = t[:400]
    # Look for explicit SAFE or UNSAFE verdict
    # Must be a verdict, not just a mention
    unsafe_patterns = [
        r"\bverdict\s*:\s*unsafe\b",
        r"\bthis\s+is\s+unsafe\b",
        r"\bunsafe\b.{0,30}\b(state file|inline conditional|ternary)\b",
        r"\bflag\w*\s+as\s+unsafe\b",
    ]
    safe_patterns = [
        r"\bverdict\s*:\s*safe\b",
        r"\bthis\s+is\s+safe\b",
        r"\bsafe\b.{0,30}\b(no ternary|not a state|display|config)\b",
    ]
    # Check UNSAFE first (more specific)
    for pat in unsafe_patterns:
        if re.search(pat, head):
            return "UNSAFE"
    for pat in safe_patterns:
        if re.search(pat, head):
            return "SAFE"
    # Fallback: first occurrence of SAFE/UNSAFE as a standalone verdict word
    m = re.search(r"^\s*(unsafe|safe)\b", t, re.MULTILINE)
    if m:
        return m.group(1).upper()
    # Last resort: which word appears first in a verdict context
    ui = t.find("unsafe")
    si = t.find("safe")
    # "unsafe" contains "safe", so be careful
    safe_positions = [m.start() for m in re.finditer(r"(?<!un)safe\b", t)]
    unsafe_positions = [m.start() for m in re.finditer(r"\bunsafe\b", t)]
    if unsafe_positions and (not safe_positions or min(unsafe_positions) < min(safe_positions)):
        ctx = t[max(0, min(unsafe_positions)-50):min(unsafe_positions)+50]
        if "verdict" in ctx or "is unsafe" in ctx or "flag" in ctx:
            return "UNSAFE"
    if safe_positions and (not unsafe_positions or min(safe_positions) < min(unsafe_positions)):
        return "SAFE"
    return "unclear"

def grade_answer(qid, text):
    choice = extract_choice(text)
    correct = CORRECT[qid]
    if choice == correct:
        return True, f"choice:{choice}"
    elif choice == "unclear":
        return False, "unclear-choice"
    else:
        return False, f"choice:{choice}"

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <answers_json>")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        answers = json.load(f)
    results = {}
    for qid in [f"Q{i}" for i in range(1, 10)]:
        text = answers.get(qid, "")
        if isinstance(text, dict):
            text = " ".join(str(v) for v in text.values() if isinstance(v, str))
        ok, why = grade_answer(qid, str(text))
        results[qid] = {"pass": ok, "why": why}
    passed = sum(1 for r in results.values() if r["pass"])
    print(json.dumps({"passed": passed, "total": 9, "results": results}, indent=2))

if __name__ == "__main__":
    main()
