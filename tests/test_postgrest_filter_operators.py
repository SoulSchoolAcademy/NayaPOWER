"""Every PostgREST predicate in an edge function must carry an explicit operator.

FAILURE-FIRST PROVENANCE
------------------------
This test fails against `origin/main` as of commit 987147821. The live proof run
36502360529 failed in `cold-successor` with `SUPABASE_READ_400`, and the only
novel query in that mode was:

    /rest/v1/nayanet_intelligent_blocks?intelligent_block_id=<id>&owner_id=<id>

No operator. Every other predicate in the same file spells `eq.` out. The
identical predicate three hundred lines earlier -- the one that runs in
`learning-influence` and succeeds -- is `intelligent_block_id=eq.` + `owner_id=eq.`.

`SUPABASE_READ_400` carried no path, no body and no predicate, so the failure was
indistinguishable from a dozen other possible causes. Two defects, one outage:

  1. the query omitted the operator;
  2. the error refused to say which query failed.

This test closes (1). `get()` reporting the path and the PostgREST body closes (2).

Nothing here is a security assertion and nothing is weakened: the operator is a
query-syntax obligation, not a boundary. Boundaries live in
`tests/test_naya_identity_owner_binding.py` and `tests/test_github_oidc_binding.py`.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = ROOT / "supabase" / "functions"

# Query parameters that are directives, not predicates.
NON_FILTER_PARAMS = {"select", "order", "limit", "offset", "on_conflict", "apikey", "or", "and"}

# PostgREST operators. A value must begin with one of these followed by a dot.
OPERATORS = {
    "eq", "neq", "gt", "gte", "lt", "lte", "like", "ilike", "match", "imatch",
    "in", "is", "isdistinct", "cs", "cd", "ov", "sl", "sr", "nxr", "nxl", "adj",
    "fts", "plfts", "phfts", "not", "all", "any",
}

PARAM = re.compile(r"[?&]([A-Za-z_][A-Za-z0-9_]*)=([^&]*)")


def _bare_predicates(source: str) -> list[str]:
    """Return `file:line: param=value` for every predicate missing an operator."""
    findings = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if "/rest/v1/" not in line:
            continue
        for match in PARAM.finditer(line):
            key, value = match.group(1), match.group(2)
            if key in NON_FILTER_PARAMS:
                continue
            head = value.split(".", 1)[0].lstrip('"')
            if head not in OPERATORS:
                snippet = line.strip()
                findings.append(f"line {lineno}: {key}={value[:60]!r} in {snippet[:160]}")
    return findings


def test_every_postgrest_predicate_declares_its_operator():
    offenders = []
    for path in sorted(FUNCTIONS.rglob("*.ts")):
        findings = _bare_predicates(path.read_text(encoding="utf-8"))
        offenders.extend(f"{path.relative_to(ROOT)} -> {f}" for f in findings)
    assert not offenders, (
        "PostgREST predicates must state their operator (eq., in., gt., ...). "
        "A bare `column=value` is not a readable intent, and when it is rejected "
        "the runtime cannot tell which predicate failed:\n  " + "\n  ".join(offenders)
    )


def test_a_failed_postgrest_read_names_the_query_and_the_body():
    source = (FUNCTIONS / "nayanet-cold-runtime-proof" / "index.ts").read_text(encoding="utf-8")
    assert "SUPABASE_READ_" in source
    # The error must carry the predicate it failed on and PostgREST's own reason.
    assert "await r.text()" in source, "a failed read must surface the response body"
    assert 'throw new Error("SUPABASE_READ_" + r.status + " " + path' in source, (
        "a failed read must name the query that failed, not only the status code"
    )
