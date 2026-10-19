"""Tests for kind_decompose_check.py — the §7 guard.

Fail-fast style (matches tools/test_claim_check.py): under pytest a failure
raises at collection (honest red); under direct execution the traceback names
the failed case.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kind_decompose_check as kc


def t(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    assert cond, f"FAIL {name} — {detail}"


# --- vacuous: no quantitative claim, nothing to decompose ---
ok, d = kc.check_claim("verdict: reviewed the briefing; no counts asserted\nnext: sleep | owner: Naya Verity")
t("no-claim-vacuous-pass", ok, d)

# --- the w268-shaped packet: decomposition present, sums, no null-kind ---
w268 = """SELECT jsonb_typeof(evidence) AS kind, count(*) AS n FROM nayanet_execution_receipts GROUP BY 1
object 1839 / array 31 / total 1870. The 124 rows = 102 object-kind arm rows (68 CONTROL + 34 TREATMENT) + 22 array-kind composite packets. The '22 missing treatment rows' was a kind-blind misread."""
ok, d = kc.check_claim(w268)
t("w268-shape-decomposed-passes", ok, d)

# --- the w229 failure: kind-blind delta names a count, zero kinds ---
w229 = """verdict: 22 missing treatment rows observed
next: investigate | owner: Naya Verity"""
ok, d = kc.check_claim(w229)
t("kind-blind-delta-rejected", not ok and "§7 REJECT" in d, d)

# --- delta language with only a total, no kinds ---
ok, d = kc.check_claim("total 1870 rows; 22 missing rows found")
t("total-only-no-kinds-rejected", not ok and "NO kind decomposition" in d, d)

# --- decomposition that does not sum to the asserted total ---
ok, d = kc.check_claim("object 100 / array 20 / total 1870")
t("non-summing-decomposition-rejected", not ok and "but block total is" in d, d)

# --- unknown kind name ---
ok, d = kc.check_claim("object 100 / blob 20 / total 120")
t("unknown-kind-rejected", not ok and "unknown kind" in d.lower(), d)

# --- null-kind rows present, unexplained ---
ok, d = kc.check_claim("object 100 / array 20 / null 5 / total 125; 5 missing rows")
t("null-kind-unexplained-rejected", not ok and "null-kind" in d, d)

# --- null-kind rows present, explained ---
ok, d = kc.check_claim(
    "object 100 / array 20 / null 5 / total 125. null-kind rows explained: SQL NULL evidence on 5 legacy rows, expected."
)
t("null-kind-explained-passes", ok, d)

# --- quoted/fenced claims never bind the author ---
ok, d = kc.check_claim('> 22 missing rows\nverdict: reviewing a claim\nnext: n/a | owner: Naya Verity')
t("quoted-delta-does-not-bind", ok, d)

ok, d = kc.check_claim('```\n22 missing treatment rows\n```\nverdict: pasted log\nnext: n/a | owner: Naya Verity')
t("fenced-delta-does-not-bind", ok, d)

# --- table-rendering decomposition ---
ok, d = kc.check_claim("| object | 1839 |\n| array | 31 |\ntotal 1870. 0 missing rows.")
t("markdown-table-decomposition-passes", ok, d)

# --- kind-first rendering ---
ok, d = kc.check_claim("124 rows total: 102 object-kind arm rows + 22 array-kind composite packets")
t("kind-first-rendering-passes", ok, d)

print("ALL §7 GUARD TESTS GREEN")
