#!/usr/bin/env python3
"""Evidence-claim validator — Laws 4.6 (Evidence Law) and 8.3 (Proof Must Not
Exceed Evidence).

Law 4.6: "Never fabricate. Verify, don't trust." REQUIRES: cite exact bytes
and refs. FORBIDS: claiming verification without evidence.
"A 'done' report is not evidence."
Law 8.3: claims cite their exact evidence and stay inside it. UNKNOWN /
BLOCKED / IMPLEMENTED masquerading as VERIFIED is forbidden.

What this check does (the machinable core):
  Scans report/receipt markdown for factual-claim patterns — quantified
  assertions (percentages, scores, counts) and state claims (VERIFIED, SHIPPED,
  MERGED, PASSING...) — and requires each claim's paragraph to carry at
  least one citation marker: a PR/issue ref (#1234), a URL, a commit SHA, a
  file path, an explicit label (evidence:/source:/ref:/proof:), or a footnote.
  A claim without a citation fails.

What it does NOT check (honest limit): it enforces that a claim CARRIES a
citation, not that the citation is real or supports the claim. A fake
citation passes this check. Citation truth is Law 5.5 (Honesty Covenant) —
judgment-only. This check kills the far more common failure: the bare,
sourceless assertion.

Usage:
    python3 check_evidence_claims.py --workdir <dir> [--exclude PAT ...]

Scans *.md recursively under <dir>, skipping fenced code blocks and
blockquote lines (quoted words are attributed speech, not claims).

Exit code 0: every factual claim carries a citation.
Exit code 1: one or more uncited claims.
Exit code 2: usage error.

Stdlib only.
"""

import argparse
import fnmatch
import os
import re
import sys

# --- claim signals: patterns that make a factual assertion ---
CLAIM_PATTERNS = [
    re.compile(r"\d+\s*%"),                                            # 90%, 100%
    re.compile(r"\d+(?:\.\d+)?\s*/\s*(?:10|100)\b"),                    # 9.0/10 scores
    re.compile(r"(?<!\blayer )\b\d+\s+(?:tests?|files?|PRs?|issues?|commits?|agents?|"
               r"seats?|checks?|laws?|blocks?|migrations?|defects?|failures?)\b",
               re.IGNORECASE),                                          # 14 tests, 3 PRs
                                                                       # ("layer 3" is a name, not a count)
    re.compile(r"\b(?:VERIFIED|PROVEN|CONFIRMED|SHIPPED|MERGED|DEPLOYED|"
               r"PASSING|GUARANTEED|PRODUCTION-PROVEN)\b"),            # state claims
    re.compile(r"\b(?:no|zero)\s+(?:failures?|errors?|defects?)\b",
               re.IGNORECASE),                                        # no failures
    re.compile(r"\ball\s+(?:tests?|checks?)\s+pass(?:ed|ing)?\b",
               re.IGNORECASE),                                        # all tests pass
]

# --- citation signals: markers that a claim points at evidence ---
CITATION_PATTERNS = [
    re.compile(r"#\d{2,}"),                                           # PR/issue ref
    re.compile(r"https?://"),                                         # URL
    re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b"),              # commit SHA
    re.compile(r"[\w\-./]+\.(?:py|md|json|ya?ml|sql|mjs|ts|html|css|sh)\b"),
    re.compile(r"\b(?:evidence|source|ref|receipt|sha256|proof|commit|branch)\s*:",
               re.IGNORECASE),                                        # explicit labels
    re.compile(r"\[\^[^\]]+\]"),                                      # footnote ref
]

FENCE = re.compile(r"^\s*```")


def paragraphs_of(path):
    """Yield (lineno, text) paragraphs; skip fenced code; merge headings
    into the paragraph that follows them."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    blocks, cur, start = [], [], None
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith(">"):
            continue  # quoted speech is attributed, not a claim
        if not stripped:
            if cur:
                blocks.append((start, "\n".join(cur)))
                cur, start = [], None
            continue
        if start is None:
            start = i
        cur.append(line)
    if cur:
        blocks.append((start, "\n".join(cur)))
    # Merge a heading-only block into the block that follows it.
    merged = []
    pending = None
    for start, text in blocks:
        if re.match(r"^\s*#{1,6}\s", text.splitlines()[0]) and len(text.splitlines()) == 1:
            pending = (start, text)
            continue
        if pending is not None:
            merged.append((pending[0], pending[1] + "\n" + text))
            pending = None
        else:
            merged.append((start, text))
    if pending is not None:
        merged.append(pending)
    return merged


def uncited_claims(path):
    out = []
    for lineno, para in paragraphs_of(path):
        if any(p.search(para) for p in CLAIM_PATTERNS):
            if not any(p.search(para) for p in CITATION_PATTERNS):
                # Report the first line that actually carries a claim signal,
                # not just the paragraph's first line (may be a merged heading).
                shown = para.splitlines()[0].strip()
                for line in para.splitlines():
                    if any(p.search(line) for p in CLAIM_PATTERNS):
                        shown = line.strip()
                        break
                out.append((lineno, shown[:100]))
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="Laws 4.6/8.3 evidence-claim check")
    ap.add_argument("--workdir", required=True, help="directory to scan")
    ap.add_argument("--exclude", action="append", default=[],
                    help="fnmatch pattern to exclude (repeatable)")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.workdir):
        print(f"USAGE ERROR: not a directory: {args.workdir}")
        return 2

    violations = []
    scanned = 0
    for root, _dirs, files in os.walk(args.workdir):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, name), args.workdir)
            if any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(name, pat)
                   for pat in args.exclude):
                continue
            scanned += 1
            for lineno, claim in uncited_claims(os.path.join(root, name)):
                violations.append(f"{rel}:{lineno}: {claim}")

    if violations:
        print("EVIDENCE-CLAIM CHECK FAILED — factual claims without citations:")
        for v in violations:
            print(f"  {v}")
        print()
        print(f"{len(violations)} uncited claim(s) in {scanned} file(s).")
        print("Law 4.6: never fabricate, verify don't trust — every factual")
        print("claim must cite its evidence: a PR/issue ref (#1234), a URL, a")
        print("commit SHA, a file path, or an evidence:/source:/proof: label.")
        print("A 'done' report is not evidence.")
        return 1

    print(f"EVIDENCE-CLAIM CHECK PASSED — {scanned} markdown file(s) scanned, "
          "every factual claim carries a citation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
