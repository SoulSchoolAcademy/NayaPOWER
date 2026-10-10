#!/usr/bin/env python3
"""Grader for Trial-12: Compositional reasoning.

Scores on EXPLICIT CHOICE only.
Correct: per answer_key.json (Reserve Rule on close pairs, highest-first otherwise).
"""
import json, re, sys

BASE = "/home/hatch/workspace/goals/learning-10-10/hidden_files/trial-12-compositional"

# Correct choice per question (from answer_key.json - Reserve Rule trial)
CORRECT = {
    "Q1": "call a",
    "Q2": "call a",
    "Q3": "call a",
    "Q4": "call b",
    "Q5": "call a",
    "Q6": "call b",
    "Q7": "call a",
    "Q8": "call a",
    "Q9": "call a",
}

def extract_choice(text):
    """Extract the agent's explicit dispatch choice from free text."""
    t = text.lower()
    # Look for "dispatch call X" or "call X" near the start (the decision statement)
    # Check first 300 chars for the choice
    head = t[:300]
    # Check for explicit dispatch-to-call FIRST: a decision statement like
    # "Dispatch the battalion chief to Call A" overrides "hold" mentions in
    # reasoning (which are often negated: "no reason to hold the unit").
    for call in ["call a", "call b", "call c"]:
        # Must appear as a dispatch decision, not just a mention
        p1 = "\\bdispatch\\b.{0,40}\\b" + call + "\\b"
        p2 = "\\b" + call + "\\b.{0,20}\\b(gets|receives|dispatched)\\b"
        if re.search(p1, head) or re.search(p2, head):
            return call
    # Explicit "hold" decision (only if no dispatch decision found above)
    if re.search(r"\bhold\b.{0,30}\bunit\b", head) and not re.search(r"do not hold|don't hold|not hold|no reason to hold|never hold", head):
        # But check if they say "do not hold" (which means dispatch)
        return "hold"
    # Fallback: first call mentioned in a decision context
    m = re.search(r"\b(i (choose|dispatch|send|assign)\b.{0,30}\bcall [abc]\b)", head)
    if m:
        cm = re.search(r"\bcall [abc]\b", m.group(1))
        if cm: return cm.group(0)
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
        print("usage: grade_trial09.py <answers_json>")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        answers = json.load(f)
    # Handle dict format: values should be plain strings per the standardized schema
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
