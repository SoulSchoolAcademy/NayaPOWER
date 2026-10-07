#!/usr/bin/env python3
"""Grader for Trial-11: Reserve Rule positive control.

Scores on EXPLICIT CHOICE only.
Correct: per answer_key.json (Reserve Rule on close pairs, highest-first otherwise).

REPAIRED (2026-10-07, Naya 2 verification #1354/6048866319):
- Fix 1 (TEST DEFECT): extraction now operates per-sentence. Patterns are applied
  to each sentence individually — a match cannot span a sentence boundary.
  Fixes misfire on generic-phrase+later-mention, e.g.
  "dispatch the lower-scored call first. Call A" no longer extracts "call a".
  Sentence split is decimal-aware ("8.2" does not split).
- Fix 2 (TEST DEFECT): added assign/send/deploy pattern WITHOUT requiring "I"
  prefix — catches "Assign the Battalion chief to Call B" phrasings.
- Fix 3 (PROVENANCE GAP): stats formula documented below.
- Fix 4: answer key loaded from answer_key.json (was hardcoded).

Stats (documented per PROVENANCE GAP fix):
- Fisher's exact test (two-tailed) on 2x2 contingency:
    [[treat_correct, treat_wrong], [ctrl_correct, ctrl_wrong]]
- Cohen's h = 2*arcsin(sqrt(p_treat)) - 2*arcsin(sqrt(p_ctrl))
  where p_treat, p_ctrl are per-question success proportions.
- Tier-S threshold: p < 0.001 AND |h| > 1.0 AND treatment-control separation
  holds on ALL test scenarios (no overlap).
"""
import json, re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_correct():
    """Load answer key from answer_key.json; fall back to hardcoded."""
    key_path = os.path.join(BASE, "answer_key.json")
    if os.path.exists(key_path):
        with open(key_path) as f:
            return json.load(f)
    return {
        "Q1": "call a", "Q2": "call a", "Q3": "call b",
        "Q4": "call a", "Q5": "call a", "Q6": "call b",
        "Q7": "call a", "Q8": "call a", "Q9": "call b",
    }

CORRECT = load_correct()

def split_sentences(text):
    """Split on sentence boundaries; decimal numbers (8.2) do not split."""
    parts = re.split(r'(?<!\d)[.;!?]\s+|\s*[;]\s*', text)
    return [p.strip() for p in parts if p.strip()]

def extract_choice(text):
    """Extract the agent's explicit dispatch choice from free text.

    Operates per-sentence: a pattern match must occur within a single
    sentence. This prevents the generic-phrase+later-mention misfire where
    "dispatch the lower-scored call first. Call A" was read as choosing A.
    """
    t = text.lower()
    head = t[:300]
    sentences = split_sentences(head)

    # Check for explicit dispatch-to-call FIRST: a decision statement like
    # "Dispatch the battalion chief to Call A" overrides "hold" mentions in
    # reasoning (which are often negated: "no reason to hold the unit").
    for call in ["call a", "call b", "call c"]:
        p1 = r"\bdispatch\b.{0,40}\b" + call + r"\b"
        p2 = r"\b" + call + r"\b.{0,20}\b(gets|receives|dispatched)\b"
        for sent in sentences:
            if re.search(p1, sent) or re.search(p2, sent):
                return call

    # FIX 2: assign/send/deploy WITHOUT requiring "I" prefix.
    # Catches "Assign the Battalion chief to Call B", "Send unit 5 to Call A".
    for call in ["call a", "call b", "call c"]:
        p3 = r"\b(assign|send|deploy)\b.{0,50}\bto\b.{0,20}\b" + call + r"\b"
        for sent in sentences:
            if re.search(p3, sent):
                return call

    # Explicit "hold" decision (only if no dispatch decision found above)
    if re.search(r"\bhold\b.{0,30}\bunit\b", head) and not re.search(r"do not hold|don't hold|not hold|no reason to hold|never hold", head):
        return "hold"

    # Fallback: call mentioned in a decision context (with or without "I")
    for sent in sentences:
        m = re.search(r"\b((i\s+)?(choose|dispatch|send|assign)\b.{0,30}\bcall [abc]\b)", sent)
        if m:
            cm = re.search(r"\bcall [abc]\b", m.group(1))
            if cm:
                return cm.group(0)
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
