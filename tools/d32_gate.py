"""D32 — Uncertainty-Discipline Document Gate.

Directive D32 (Shawn, 2026-10-10): separate observed, inferred, assumed,
unverified and disproven claims. No false precision. Every consequential
report carries "WHAT THIS DOES NOT CLAIM."

This module makes D32 mechanically enforceable on markdown documents.
It is a GATE, not a suggestion: it returns PASS/FAIL with specific
violations, and CI blocks PRs whose gate-controlled documents fail.

Three rules (all checked mechanically):
  R1 SOURCED-NUMBERS .... every quantitative claim (a number) must have a
     source reference (URL, #issue/PR number, commit SHA, or explicit
     citation) within 3 lines.
  R2 DOES-NOT-CLAIM ..... the document must contain a "WHAT THIS DOES NOT
     CLAIM" (or "DOES NOT CLAIM") section, case-insensitive.
  R3 EVIDENCED-CONFIDENCE  every confidence word (proven, verified,
     guaranteed, certain) must share its paragraph with an evidence
     reference (URL, #number, SHA, or markdown link). Bare confidence
     words are flagged.

Usage:
    python tools/d32_gate.py <file.md>        # CLI: prints JSON, exit 0 PASS / 1 FAIL
    from tools.d32_gate import check_document  # library: check_document(text) -> dict

The JSON verdict shape:
    {"verdict": "PASS"|"FAIL",
     "violations": [{"line": int, "rule": "R1"|"R2"|"R3", "text": str}, ...]}
"""

from __future__ import annotations

import json
import re
import sys

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Quantitative claim: a standalone number (integer or decimal), optionally
# followed by %, x, or a unit word. Dates, times, versions excluded below.
_NUMBER_RE = re.compile(r"(?<![\w#])\d[\d,]*(?:\.\d+)?%?(?![\w.])")

# Things that look like numbers but are NOT quantitative claims.
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")          # 2026-10-11
_TIME_RE = re.compile(r"\d{1,2}:\d{2}")              # 23:44
_VERSION_RE = re.compile(r"[vV]?\d+\.\d+(?:\.\d+)*")  # v1.2, 2.0.1
_HEX_LONG_RE = re.compile(r"\b[0-9a-f]{7,40}\b")      # SHAs (handled as sources)

# Source references: URL, #issue/PR, commit SHA, explicit citation.
_URL_RE = re.compile(r"https?://\S+")
_ISSUE_RE = re.compile(r"#\d{2,}")
_SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
_CITE_RE = re.compile(r"(?i)\bsource\s*[:：]")
_MD_LINK_RE = re.compile(r"\[[^\]]+\]\(\s*https?://")

# Confidence words that demand same-paragraph evidence.
_CONFIDENCE_WORDS = ("proven", "verified", "guaranteed", "certain")
_CONFIDENCE_RE = re.compile(
    r"\b(" + "|".join(_CONFIDENCE_WORDS) + r")\b", re.IGNORECASE
)

# The mandatory humility section.
_DOES_NOT_CLAIM_RE = re.compile(r"does\s+not\s+claim", re.IGNORECASE)

_SOURCE_WINDOW = 3  # lines before/after a number to look for a source


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _line_has_source(line: str) -> bool:
    """True if the line carries any recognized source reference."""
    return bool(
        _URL_RE.search(line)
        or _ISSUE_RE.search(line)
        or _SHA_RE.search(line)
        or _CITE_RE.search(line)
        or _MD_LINK_RE.search(line)
    )


def _strip_non_claims(line: str) -> str:
    """Remove dates, times, versions, SHAs so they are not read as claims."""
    line = _DATE_RE.sub(" ", line)
    line = _TIME_RE.sub(" ", line)
    line = _VERSION_RE.sub(" ", line)
    line = _HEX_LONG_RE.sub(" ", line)
    return line


def _paragraphs(lines: list[str]) -> list[tuple[int, int, str]]:
    """Split into paragraphs; return (start_line_1idx, end_line_1idx, text)."""
    paras: list[tuple[int, int, str]] = []
    start: int | None = None
    buf: list[str] = []
    for i, line in enumerate(lines, start=1):
        if line.strip():
            if start is None:
                start = i
            buf.append(line)
        else:
            if start is not None:
                paras.append((start, i - 1, "\n".join(buf)))
                start = None
                buf = []
    if start is not None:
        paras.append((start, len(lines), "\n".join(buf)))
    return paras


# ---------------------------------------------------------------------------
# Rule checks
# ---------------------------------------------------------------------------

def _check_r1_sourced_numbers(lines: list[str]) -> list[dict]:
    """R1: every quantitative claim needs a source within 3 lines."""
    violations: list[dict] = []
    # Precompute which lines have sources.
    sourced = [_line_has_source(ln) for ln in lines]
    for i, line in enumerate(lines):
        clean = _strip_non_claims(line)
        for m in _NUMBER_RE.finditer(clean):
            # Skip numbers that ARE issue references (#1234) — they are sources.
            before = clean[max(0, m.start() - 1):m.start()]
            if before.endswith("#"):
                continue
            lo = max(0, i - _SOURCE_WINDOW)
            hi = min(len(lines), i + _SOURCE_WINDOW + 1)
            if not any(sourced[lo:hi]):
                violations.append({
                    "line": i + 1,
                    "rule": "R1",
                    "text": f"unsourced quantitative claim '{m.group(0)}': {line.strip()[:100]}",
                })
                break  # one violation per line is enough
    return violations


def _check_r2_does_not_claim(text: str) -> list[dict]:
    """R2: document must contain a DOES NOT CLAIM section."""
    if _DOES_NOT_CLAIM_RE.search(text):
        return []
    return [{
        "line": 0,
        "rule": "R2",
        "text": "missing mandatory 'WHAT THIS DOES NOT CLAIM' section",
    }]


def _check_r3_evidenced_confidence(lines: list[str]) -> list[dict]:
    """R3: confidence words need an evidence reference in the same paragraph."""
    violations: list[dict] = []
    for start, end, para in _paragraphs(lines):
        if not _CONFIDENCE_RE.search(para):
            continue
        if _line_has_source(para):
            continue
        # Find the offending word and its line for a precise report.
        for lineno in range(start, end + 1):
            m = _CONFIDENCE_RE.search(lines[lineno - 1])
            if m and not _line_has_source(lines[lineno - 1]):
                violations.append({
                    "line": lineno,
                    "rule": "R3",
                    "text": f"unevidenced confidence word '{m.group(1)}': "
                            f"{lines[lineno - 1].strip()[:100]}",
                })
                break
    return violations


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_document(text: str) -> dict:
    """Check a markdown document against D32. Returns the verdict dict."""
    lines = text.splitlines()
    violations = (
        _check_r1_sourced_numbers(lines)
        + _check_r2_does_not_claim(text)
        + _check_r3_evidenced_confidence(lines)
    )
    # Deterministic order: by line, then rule.
    violations.sort(key=lambda v: (v["line"], v["rule"]))
    return {
        "verdict": "FAIL" if violations else "PASS",
        "violations": violations,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/d32_gate.py <file.md>", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        result = check_document(f.read())
    print(json.dumps(result, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
