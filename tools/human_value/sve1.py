#!/usr/bin/env python3
"""sve1.py — Instrument SVE-1 (Stated Value Events), mechanical extraction step.

Spec: hidden_files/areas/mu-value-instrument-1-20261012T2145.md §7 step 1.

This is the EXTRACTION capability only: it finds quote spans that COULD be
Shawn-attributed stated-value evidence and classifies them by the bytes, not
by the narrative. It does NOT adjudicate. MEASURED vs PROVISIONAL vs rejected
is a seat judgment made against the instrument's rules; this tool supplies
the candidate list + evidence pointers so that judgment is checkable.

Usage:
    python3 tools/human_value/sve1.py extract <logfile> [--format json|md]

Classification (mechanical, from the spec):
  verbatim   — a quoted span sits in the source bytes WITH an attribution
               clause on the same line (Shawn said / Shawn: "...").
  reported   — colon-attribution quoting him from seat recollection
               (the bytes are seat-authored; authorship=inferred).
               The tool cannot distinguish "original bytes" from "recalled"
               bytes, so ALL colon-attribution from seat-authored sources
               lands here. Naming it is the honesty.
  paraphrase — a seat-authored restatement about what he said, with NO quote
               marks in the bytes -> side ledger, NEVER counted as a unit.
  uncertain  — a quote span with no attribution clause at all.

Dedupe: sha256 of normalized span (curly quotes straightened, lowercased,
punctuation/whitespace collapsed). The same sentence across C1/C2/MEMORY.md
is 1 unit.

Exit codes: 0 = ran clean (even with 0 candidates — silence is NULL, not an
error); 1 = usage/file error.
"""

import hashlib
import json
import re
import sys
import unicodedata

# --- the mechanical part, verbatim from the spec §7 ---------------------------
ATTRIBUTION_VERBS = (
    "said|told|asked|directed|ordered|approved|gave|established|stated|"
    "pasted|affirmed|described|reported|called"
)
# colon-attribution:  Shawn: "...."
COLON_RE = re.compile(
    r'\bShawn\s*:\s*["\u201c]([^"\u201d]{8,400})["\u201d]'
)
# attribution clause in the same line: Shawn said ... / he said ...
CLAUSE_RE = re.compile(
    r'\b(?:Shawn|he)\s+(?:' + ATTRIBUTION_VERBS + r')\b', re.IGNORECASE
)
# quoted spans: straight or curly, 8..400 chars (bounded — no runaway greed)
SPAN_RE = re.compile(r'["\u201c]([^"\u201d]{8,400})["\u201d]')
# seat restatements with no quote marks: "he liked it" style signals
PARAPHRASE_HINTS = (
    "he liked", "he loved", "he approved", "he agreed", "he was happy",
    "he thought", "he feels", "he seemed", "he confirmed", "he ratified",
)


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFKC", text)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    t = re.sub(r"[^a-z0-9\s]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def content_hash(span: str) -> str:
    return hashlib.sha256(normalize(span).encode()).hexdigest()[:16]


def extract(path: str) -> dict:
    candidates = []
    side_ledger = []  # paraphrases: recorded, never counted
    seen = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            raw = line.rstrip("\n")

            # (a) colon-attribution spans
            for m in COLON_RE.finditer(raw):
                span = m.group(1).strip()
                h = content_hash(span)
                if h in seen:
                    continue
                seen.add(h)
                candidates.append({
                    "line": lineno,
                    "span": span,
                    "class": "reported",  # seat-authored source: authorship=inferred
                    "attribution": "colon",
                    "content_hash": h,
                })

            # (b) quote spans sharing a line with an attribution clause
            if CLAUSE_RE.search(raw):
                for m in SPAN_RE.finditer(raw):
                    span = m.group(1).strip()
                    if COLON_RE.search(raw):  # already captured above
                        continue
                    h = content_hash(span)
                    if h in seen:
                        continue
                    seen.add(h)
                    candidates.append({
                        "line": lineno,
                        "span": span,
                        "class": "verbatim",
                        "attribution": "clause",
                        "content_hash": h,
                    })
            else:
                # quote spans with no attribution: uncertain (never units)
                for m in SPAN_RE.finditer(raw):
                    span = m.group(1).strip()
                    if COLON_RE.search(raw):
                        continue
                    h = content_hash(span)
                    if h in seen:
                        continue
                    seen.add(h)
                    side_ledger.append({
                        "line": lineno,
                        "span": span[:120],
                        "class": "uncertain",
                        "attribution": "none",
                        "content_hash": h,
                    })

            # paraphrase hints without any quote marks -> side ledger only
            lowered = raw.lower()
            if ('"' not in raw and "\u201c" not in raw
                    and any(hint in lowered for hint in PARAPHRASE_HINTS)):
                side_ledger.append({
                    "line": lineno,
                    "span": raw.strip()[:120],
                    "class": "paraphrase",
                    "attribution": "none",
                    "content_hash": None,
                })

    return {
        "source": path,
        "candidates": candidates,      # shawn-attributed quote spans (units, pending adjudication)
        "side_ledger": side_ledger,    # paraphrase/uncertain: recorded, NEVER counted
        "counts": {
            "candidates": len(candidates),
            "side_ledger": len(side_ledger),
        },
    }


def main(argv):
    if len(argv) < 3 or argv[1] != "extract":
        print(__doc__, file=sys.stderr)
        return 1
    path = argv[2]
    fmt = "json"
    if "--format" in argv:
        fmt = argv[argv.index("--format") + 1]
    try:
        result = extract(path)
    except FileNotFoundError:
        print(f"sve1: no such file: {path}", file=sys.stderr)
        return 1
    if fmt == "md":
        print(f"# SVE-1 extraction — {result['source']}\n")
        print(f"Candidates: {result['counts']['candidates']} | "
              f"side ledger: {result['counts']['side_ledger']}\n")
        for c in result["candidates"]:
            print(f"- L{c['line']} [{c['class']}/{c['attribution']}] "
                  f"`{c['content_hash']}` — \"{c['span'][:140]}\"")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
