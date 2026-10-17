#!/usr/bin/env python3
"""Plain-words communication linter — Law 2.1 (Plain Meaning First).

Law: "LITERALLY WHAT I'M SAYING, then THE TECHNICAL."
REQUIRES: plain words first — what things DO and what they MEAN, not their
numbers. Every report explains: what happened, why it matters, what
capability changed, what remains, what the math concluded.
FORBIDS: PR numbers without purpose. Jargon without translation.
"I can't answer a question without being explained what you're even saying."

What this check does (the machinable core — blocklist + structure, not NLP):
  1. LEAD-WITH-MEANING: the document must open with plain meaning. Within
     the first 30 lines there must be a plain-words section marker —
     "what happened", "what changed", "summary", "tl;dr", "in plain words",
     or "the short version". Technical detail may follow; it must not lead.
  2. NO-BARE-PR-NUMBERS: a #NNNN reference on a line with fewer than 5
     alphabetic words is a PR number without purpose — it fails.
     ("Fixed the merge (#1709): base changes were dropped" passes;
     "#1709, #1701 merged" fails.)
  3. JARGON-WITHOUT-GLOSS: on first use, blocklisted jargon must be
     glossed within 2 lines — a parenthetical, "i.e.", "e.g.", an em dash,
     or the word "means". Blocklist: idempot*, orthogona*, instantiat*,
     hydrat*, dedup*, refspec, canonicaliz*, falsifi*.

What it does NOT check (honest limit): whether the plain words are true,
clear, or sufficient — that is taste and judgment (Law 2.2, the Delivery
Gate's usefulness test). This linter enforces the checkable surface:
meaning leads, numbers are explained, jargon is translated.

Usage:
    python3 check_plain_words.py --workdir <dir>

Exit code 0: all documents pass.
Exit code 1: one or more violations.
Exit code 2: usage error.

Stdlib only.
"""

import argparse
import os
import re
import sys

LEAD_MARKERS = (
    "what happened",
    "what changed",
    "summary",
    "tl;dr",
    "in plain words",
    "the short version",
)
LEAD_WINDOW_LINES = 30

PR_REF = re.compile(r"#\d{2,}")
WORD = re.compile(r"[A-Za-z]{2,}")

JARGON_STEMS = (
    "idempot",
    "orthogona",
    "instantiat",
    "hydrat",
    "dedup",
    "refspec",
    "canonicaliz",
    "falsifi",
)
GLOSS_CUES = ("(", "i.e.", "e.g.", "means", "--", "\u2014", ":", "in plain words")


def words_on(line):
    return WORD.findall(line)


def check_lead(lines, rel):
    window = "\n".join(lines[:LEAD_WINDOW_LINES]).lower()
    if not any(m in window for m in LEAD_MARKERS):
        return [f"{rel}:1: LEAD-WITH-MEANING — the document never says "
                f"plainly what happened. Put a plain-words summary "
                f"('what happened', 'what changed', 'summary') in the "
                f"first {LEAD_WINDOW_LINES} lines. LITERALLY WHAT YOU'RE "
                f"SAYING first, then the technical."]
    return []


def check_pr_refs(lines, rel):
    out = []
    for i, line in enumerate(lines, 1):
        if PR_REF.search(line) and len(words_on(line)) < 5:
            out.append(f"{rel}:{i}: BARE-PR-NUMBER — {line.strip()[:90]!r} is "
                       f"a PR/issue number without plain meaning. Say what "
                       f"it IS and why it matters, not just its number.")
    return out


def check_jargon(lines, rel):
    out = []
    seen = set()
    for i, line in enumerate(lines):
        low = line.lower()
        for stem in JARGON_STEMS:
            if stem in seen:
                continue
            m = re.search(r"\b\w*" + re.escape(stem) + r"\w*\b", low)
            if not m:
                continue
            seen.add(stem)
            term = m.group(0)
            context = "\n".join(lines[max(0, i - 2):i + 3]).lower()
            if not any(cue in context for cue in GLOSS_CUES):
                out.append(f"{rel}:{i + 1}: JARGON-WITHOUT-GLOSS — "
                           f"'{term}' is used with no plain-words "
                           f"translation nearby. Gloss it once "
                           f"(parenthetical, 'i.e.', 'means') so a human "
                           f"can answer without asking what you're saying.")
    return out


def check_file(path, rel):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    violations = []
    violations += check_lead(lines, rel)
    violations += check_pr_refs(lines, rel)
    violations += check_jargon(lines, rel)
    return violations


def main(argv):
    ap = argparse.ArgumentParser(description="Law 2.1 plain-words linter")
    ap.add_argument("--workdir", required=True, help="directory to scan")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.workdir):
        print(f"USAGE ERROR: not a directory: {args.workdir}")
        return 2

    violations, scanned = [], 0
    for root, _dirs, files in os.walk(args.workdir):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            scanned += 1
            path = os.path.join(root, name)
            rel = os.path.relpath(path, args.workdir)
            violations += check_file(path, rel)

    if violations:
        print("PLAIN-WORDS CHECK FAILED:")
        for v in violations:
            print(f"  {v}")
        print()
        print(f"{len(violations)} violation(s) in {scanned} file(s).")
        print("Law 2.1: plain meaning first. Talk about what things DO and")
        print("what they MEAN, not their numbers. Jargon without translation")
        print("and PR numbers without purpose never reach a human.")
        return 1

    print(f"PLAIN-WORDS CHECK PASSED — {scanned} document(s): meaning leads, "
          "numbers are explained, jargon is glossed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
