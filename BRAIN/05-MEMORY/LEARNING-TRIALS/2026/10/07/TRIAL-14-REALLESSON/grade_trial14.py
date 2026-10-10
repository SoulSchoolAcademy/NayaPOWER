#!/usr/bin/env python3
"""Grader for Trial-14: real lesson (state file ternary)."""
import json, re, sys

CORRECT = {
    "Q1": "UNSAFE",
    "Q2": "SAFE",
    "Q3": "SAFE",
    "Q4": "UNSAFE",
    "Q5": "SAFE",
    "Q6": "UNSAFE",
    "Q7": "SAFE",
    "Q8": "UNSAFE",
    "Q9": "SAFE",
}

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
    # Look for "UNSAFE" or "SAFE" in caps or as a clear verdict
    m = re.search(r"^\s*(unsafe|safe)\b", t, re.MULTILINE)
    if m:
        return m.group(1).upper()
    # Last resort: which word appears first in a verdict context
    ui = t.find("unsafe")
    si = t.find("safe")
    # "unsafe" contains "safe", so be careful
    # Find "safe" not part of "unsafe"
    safe_positions = [m.start() for m in re.finditer(r"(?<!un)safe\b", t)]
    unsafe_positions = [m.start() for m in re.finditer(r"\bunsafe\b", t)]
    if unsafe_positions and (not safe_positions or min(unsafe_positions) < min(safe_positions)):
        # Check it's a verdict, not just describing
        ctx = t[max(0,min(unsafe_positions)-50):min(unsafe_positions)+50]
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
