#!/usr/bin/env python3
"""Adversarial tests for the UD-19 overlap arbiter.

Run: python3 tools/test_overlap_arbiter.py
Exit 0 = all green. Any failure prints the case and exits 1.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from overlap_arbiter import (Claim, cross_score, find_overlaps, arbitrate,
                             OverlapError)


def mkclaim(who, aid, key="doc-checker"):
    return Claim(claimant=who, artifact_id=aid, work_key=key,
                 artifact_hash="sha:" + aid, location=f"branch/{who}/{aid}")


def expect(code, fn, label):
    try:
        fn()
    except OverlapError as e:
        assert e.code == code, f"{label}: want {code}, got {e.code}"
        print(f"  ok  {label} -> refused {code}")
        return
    raise AssertionError(f"{label}: expected refusal {code}, but it passed")


passed = []


def case(name):
    print(f"case: {name}")
    passed.append(name)


# --- positive: clear winner decided by the numbers -----------------------
case("clear winner by cross-scores")
a = mkclaim("naya2", "checker-A")
b = mkclaim("naya5", "checker-B")
sa = cross_score(a, "naya4", {"usefulness": 9, "logic": 8},
                 ["PR #2224 files: tools/d32_gate.py", "12/12 tests green"])
sb = cross_score(b, "naya4", {"usefulness": 6, "logic": 6},
                 ["PR #2225 files: register.json", "10/10 tests green"])
r = arbitrate([a, b], [sa, sb], verifier="naya1",
              resolution="ADVANCE_WINNER",
              reasoning="Checker A scores higher on usefulness with cited "
                        "test evidence; B is sound but narrower in scope.")
assert r["winner"] == "checker-A", r["winner"]
assert r["margin"] > 0.5
assert len(r["preserved_losers"]) == 1
assert r["preserved_losers"][0]["artifact_id"] == "checker-B"
assert r["evidence_refs"], "receipt must cite evidence"
print("  ok  winner=checker-A, loser preserved")

# --- positive: tie broken by evidence quality ------------------------------
case("tie broken by evidence quality")
a = mkclaim("naya2", "gate-X")
b = mkclaim("naya5", "gate-Y")
sa = cross_score(a, "naya4", {"usefulness": 8, "logic": 8},
                 ["tests/test_x.py 14/14 green",
                  "sabotage run caught by 9 tests",
                  "review 5481596914 with evidence"])
sb = cross_score(b, "naya4", {"usefulness": 8, "logic": 8},
                 ["tests/test_y.py 10/10 green"])
r = arbitrate([a, b], [sa, sb], verifier="naya1",
              resolution="ADVANCE_WINNER",
              reasoning="Scores tied at 8.0; X wins on evidence depth: three "
                        "independent evidence refs including an adversarial "
                        "sabotage run, versus one.")
assert r["winner"] == "gate-X", r["winner"]
assert r["tiebreak"] and "evidence" in r["tiebreak"]
print("  ok  tie -> evidence quality decides")

# --- positive: full tie needs Intelligence-Question answer -----------------
case("full tie requires recorded IQ answer")
a = mkclaim("naya2", "m-1")
b = mkclaim("naya5", "m-2")
sa = cross_score(a, "naya4", {"usefulness": 8}, ["tests/a.py 5/5 green"])
sb = cross_score(b, "naya4", {"usefulness": 8}, ["tests/b.py 5/5 green"])
expect("TIEBREAK_MISSING",
       lambda: arbitrate([a, b], [sa, sb], verifier="naya1",
                         resolution="MERGE_BOTH",
                         reasoning="Both merge-worthy; combined they cover "
                                   "more ground than either alone."),
       "tie without IQ answer")
r = arbitrate([a, b], [sa, sb], verifier="naya1",
              resolution="MERGE_BOTH",
              reasoning="Both merge-worthy; combined they cover more ground "
                        "than either alone.",
              iq_answer="Merging serves the user best: A handles documents, "
                        "B handles code, and the combined gate covers both "
                        "with no extra cost.")
assert r["resolution"] == "MERGE_BOTH" and r["tiebreak"]
print("  ok  recorded IQ answer breaks the tie")

# --- positive: overlap detection trigger -----------------------------------
case("find_overlaps groups genuine overlaps only")
claims = [mkclaim("naya2", "a1", "k1"), mkclaim("naya5", "a2", "k1"),
          mkclaim("naya2", "a3", "k2")]
groups = find_overlaps(claims)
assert set(groups) == {"k1"}, groups
print("  ok  only multi-claimant groups trigger")

# --- negative: self-judging refused ----------------------------------------
case("claimant may not score their own artifact")
a = mkclaim("naya2", "checker-A")
expect("SELF_JUDGE",
       lambda: cross_score(a, "naya2", {"usefulness": 10},
                           ["my own tests all pass"]),
       "self score")
expect("SELF_VERIFY",
       lambda: arbitrate(
           [a, mkclaim("naya5", "checker-B")],
           [cross_score(a, "naya4", {"usefulness": 9}, ["tests 12/12 green"]),
            cross_score(mkclaim("naya5", "checker-B"), "naya4",
                        {"usefulness": 6}, ["tests 10/10 green"])],
           verifier="naya2", resolution="ADVANCE_WINNER",
           reasoning="A is better evidenced across the cited test runs."),
       "claimant as verifier")

# --- negative: scoreless inflation rejected ---------------------------------
case("score without evidence is inflation")
a = mkclaim("naya2", "checker-A")
expect("SCORE_WITHOUT_EVIDENCE",
       lambda: cross_score(a, "naya4", {"usefulness": 10}, []),
       "no evidence")
expect("SCORE_WITHOUT_EVIDENCE",
       lambda: cross_score(a, "naya4", {"usefulness": 10}, ["ok"]),
       "thin evidence")
expect("SCORE_WITHOUT_EVIDENCE",
       lambda: cross_score(a, "naya4", {}, ["tests 12/12 green"]),
       "empty scorecard")

# --- negative: rank-based reasoning refused ---------------------------------
case("receipt may cite evidence, never rank")
a, b = mkclaim("naya2", "r-1"), mkclaim("naya5", "r-2")
sa = cross_score(a, "naya4", {"usefulness": 9}, ["tests/r1.py 8/8 green"])
sb = cross_score(b, "naya4", {"usefulness": 6}, ["tests/r2.py 8/8 green"])
expect("RANK_NOT_EVIDENCE",
       lambda: arbitrate([a, b], [sa, sb], verifier="naya1",
                         resolution="ADVANCE_WINNER",
                         reasoning="naya2 is senior so A wins"),
       "rank reasoning")
expect("RANK_NOT_EVIDENCE",
       lambda: arbitrate([a, b], [sa, sb], verifier="naya1",
                         resolution="ADVANCE_WINNER", reasoning="A wins"),
       "thin reasoning")

# --- negative: duplicate evidence flagged ------------------------------------
case("same evidence for both artifacts is flagged")
a, b = mkclaim("naya2", "d-1"), mkclaim("naya5", "d-2")
sa = cross_score(a, "naya4", {"usefulness": 9}, ["tests/shared.py 8/8 green"])
sb = cross_score(b, "naya4", {"usefulness": 5}, ["tests/shared.py 8/8 green"])
r = arbitrate([a, b], [sa, sb], verifier="naya1",
              resolution="ADVANCE_WINNER",
              reasoning="A's evidence is specific to its claims while B leans "
                        "on the same shared run; A wins on the numbers.")
assert any(f["code"] == "DUPLICATE_EVIDENCE" for f in r["evidence_flags"]), \
    r["evidence_flags"]
print("  ok  duplicated evidence flagged in receipt")

# --- negative: artifact with no cross-score refused --------------------------
case("no verdict without independent scoring")
a, b = mkclaim("naya2", "u-1"), mkclaim("naya5", "u-2")
sa = cross_score(a, "naya4", {"usefulness": 9}, ["tests/u1.py 8/8 green"])
expect("SCORE_WITHOUT_EVIDENCE",
       lambda: arbitrate([a, b], [sa], verifier="naya1",
                         resolution="ADVANCE_WINNER",
                         reasoning="A is scored and evidenced; B has no "
                                   "independent score so no decision can land."),
       "unscored artifact")

print(f"\nALL {len(passed)} CASES GREEN")
