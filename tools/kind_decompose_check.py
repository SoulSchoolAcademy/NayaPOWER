"""
kind_decompose_check.py — the §7 guard (Naya Alpha, 2026-10-16; canon from the
w229/w268 disposition: a kind-blind LIKE turned 22 composite-packet rows into
"missing treatment rows").

CANON (§7, acceptance recipe): any row-count claim against an evidence table
MUST decompose by kind (jsonb_typeof of the evidence column) BEFORE any delta
is named. "Count the kinds before counting the rows."

This guard is write-time, fail-closed enforcement at the emission point: a
verification packet that names a row delta WITHOUT a kind decomposition is
REJECTED (exit 1). It does NOT verify the numbers against live Supabase — that
is the independent-verification rung (a different seat re-runs the standing
queries below). This guard enforces the SHAPE of an admissible claim; live
bytes enforce its TRUTH. Two rungs, never confused.

Failure it prevents: kind-blind delta claims (w229/w268 class).

STANDING QUERIES (the live pathway this guard's admissible packets must be
produced from — Supabase READ-ONLY, sb-api without --allow-write):
  1. SELECT column_name, data_type FROM information_schema.columns
     WHERE table_name='<table>' ORDER BY ordinal_position;
  2. SELECT jsonb_typeof(<evidence_col>) AS kind, count(*) AS n
     FROM <table> GROUP BY 1 ORDER BY 2 DESC;
"""

import re
import sys

# jsonb_typeof's full kind vocabulary (SQL NULL -> None -> "null" kind).
KINDS = {"object", "array", "string", "number", "boolean", "null"}

# A count/delta assertion: a number adjacent to row-delta language.
_DELTA_PAT = re.compile(
    r"(\d[\d,]*)\s+(missing|lost|added|new|remaining|present|found|dropped|duplicate)",
    re.IGNORECASE,
)
_TOTAL_PAT = re.compile(r"\btotal\D{0,20}(\d[\d,]*)", re.IGNORECASE)
_ROWS_PAT = re.compile(r"(\d[\d,]*)\s+rows?\b", re.IGNORECASE)

# A kind decomposition line: kind-name + its count, tight binding only.
# Matches: "object 1839", "object=1839", "object: 1839", "| object | 1839 |".
# Deliberately does NOT reach across intervening words ("object-kind arm rows"
# is handled by _KIND_FIRST_PAT; the (68 CONTROL) parenthetical stays out).
_KIND_PAT = re.compile(
    r"\b(object|array|string|number|boolean|null)\b\s*[:=|/]?\s*(\d[\d,]*)",
    re.IGNORECASE,
)
_KIND_FIRST_PAT = re.compile(
    r"(\d[\d,]*)\s+(object|array|string|number|boolean|null)\b",
    re.IGNORECASE,
)
# A block-scoped total: "total N" or "N rows = ..." (run-key-filtered subsets).
# _TOTAL_BEFORE_PAT takes precedence: "124 rows total:" means 124, not 102.
_TOTAL_BEFORE_PAT = re.compile(r"(\d[\d,]*)\s+(?:rows?\s+)?total\b", re.IGNORECASE)
_ROWS_EQ_PAT = re.compile(r"(\d[\d,]*)\s+rows?\s*=", re.IGNORECASE)


def _block_total(block):
    m = _TOTAL_BEFORE_PAT.search(block) or _TOTAL_PAT.search(block) or _ROWS_EQ_PAT.search(block)
    return _num(m.group(1)) if m else None

# Words that may sit next to numbers but are structural/delta language, never
# kind names. Keeps unknown-kind detection from flagging "124 rows" or the
# w268 parenthetical "(68 CONTROL + 34 TREATMENT)".
_STRUCTURAL = {
    "rows", "row", "total", "kind",
    "missing", "lost", "added", "new", "remaining", "present", "found",
    "dropped", "duplicate",
    "control", "treatment", "packets", "packet", "composite", "arm",
    "legacy", "sql",
}
# Articles/prepositions that sit before numbers in prose ("The 124 rows") —
# never kind names.
_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "with", "and", "or", "to", "for",
    "as", "is", "are", "was", "were", "be", "at", "by", "from", "no",
    "not", "this", "that", "these", "those", "it", "its",
}
_NAME_FIRST_CAND = re.compile(
    r"\b([a-zA-Z][a-zA-Z0-9_-]*)\b\s*[:=|/]?\s*\d[\d,]*", re.IGNORECASE)
_NUM_FIRST_CAND = re.compile(
    r"\d[\d,]*\s+([a-zA-Z][a-zA-Z0-9_-]*)\b", re.IGNORECASE)


def candidate_kind_words(block):
    """Words shaped like kind names in this block ('blob 20', '20 blob-kind'),
    minus known kinds and structural words. Only called on blocks that already
    parsed a KNOWN kind — so SQL text and prose never false-positive."""
    cands = set()
    for m in _NAME_FIRST_CAND.finditer(block):
        cands.add(m.group(1).lower().removesuffix("-kind"))
    for m in _NUM_FIRST_CAND.finditer(block):
        cands.add(m.group(1).lower().removesuffix("-kind"))
    return cands - KINDS - _STRUCTURAL - _STOPWORDS


def _strip_quoted(text):
    """Quoted/fenced text is someone else's words — never binds the author."""
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.lstrip().startswith(">"):
            continue
        lines.append(line)
    return "\n".join(lines)


def _num(s):
    return int(s.replace(",", ""))


def parse_decomposition(text):
    """Extract {kind: count} from the author's own (unquoted) text."""
    kinds = {}
    for m in _KIND_PAT.finditer(text):
        kinds[m.group(1).lower()] = _num(m.group(2))
    for m in _KIND_FIRST_PAT.finditer(text):
        kinds[m.group(2).lower()] = _num(m.group(1))
    return kinds


def _asserts_count(text):
    """True when the packet names a row-count delta in the author's own words."""
    return bool(
        _DELTA_PAT.search(text)
        or _TOTAL_PAT.search(text)
        or _ROWS_PAT.search(text)
    )


def check_claim(packet):
    """
    Returns (ok, detail). Fail-closed: a kind-blind delta is rejected.
    A packet with no quantitative claim passes vacuously (nothing to decompose).
    """
    text = _strip_quoted(packet)
    if not _asserts_count(text):
        return True, "vacuous-pass: no row-count claim"

    kinds = parse_decomposition(text)
    if not kinds:
        return False, (
            "§7 REJECT: packet names a row-count delta with NO kind decomposition. "
            "Decompose by jsonb_typeof(evidence) kind BEFORE naming any delta "
            "(canon: w229/w268 — kind-blind LIKE turned 22 composite-packet "
            "rows into 'missing treatment rows')."
        )

    # (unknown-kind detection runs block-local below, where candidate words
    # can be seen in context; the packet-global parse only holds KNOWN kinds)

    # Block-local sum check: a packet may carry decompositions at several
    # scopes (whole table + a run-key-filtered subset, the w268 shape). Each
    # block that asserts its own total must sum within that block. A global
    # sum check would falsely reject multi-scope packets, so it is not done.
    # Unknown-kind detection also runs block-local, only on blocks that
    # already parsed a KNOWN kind — so SQL text and prose never false-positive.
    for block in re.split(r"\n+|(?<=[.!?])\s+", text):
        bkinds = parse_decomposition(block)
        if bkinds:
            unknown = candidate_kind_words(block)
            if unknown:
                return False, (
                    f"§7 REJECT: unknown kind name(s) {sorted(unknown)} — "
                    f"not jsonb_typeof vocabulary"
                )
        tm = _block_total(block)
        if tm is not None:
            if bkinds and sum(bkinds.values()) != tm:
                return False, (
                    f"§7 REJECT: block kind counts sum to "
                    f"{sum(bkinds.values())} but block total is {tm}: "
                    f"{block.strip()[:80]}"
                )

    if kinds.get("null", 0) > 0:
        # Null-kind rows (evidence SQL NULL) are the silent kind: the number
        # alone is not a decomposition — state what they ARE before any delta.
        expl = re.search(r"null[- ]kind[^.\n]{0,80}(explain|expect|composite|packet|sql null)",
                         text, re.IGNORECASE)
        if not expl:
            return False, (
                "§7 REJECT: null-kind rows present with no explanation. "
                "State what the null-kind rows ARE before any delta."
            )

    return True, f"§7 PASS: kind-decomposed ({', '.join(f'{k}={v}' for k, v in sorted(kinds.items()))})"


def main(argv):
    if len(argv) != 2:
        print("usage: kind_decompose_check.py <packet-file>", file=sys.stderr)
        return 2
    with open(argv[1]) as f:
        packet = f.read()
    ok, detail = check_claim(packet)
    print(("PASS " if ok else "FAIL ") + detail)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
