#!/usr/bin/env python3
"""RED-first battery for the lane-tag seat extension of the merge-consensus gate.

Covers the 12-lane seat model the gate predates:
  author declaration:  Seat: Naya <Name> (Lane N)      (N = 1..12)
  review incantation:  [LANE N · REVIEW] ... APPROVED ...

Conventions asserted (identity = lane NUMBER, names are honor-based —
the shared-account residual the gate cannot verify):
  seat_of / author_seat_of return "Lane N" for lane tags, "Naya N" for
  legacy tags. The two namespaces never collide.

Negative controls: unrecognized forms stay None (fail-closed); lane 13+
never parses; legacy naya[1-5] behavior is byte-unchanged.
"""
import importlib.util
import os
import sys

_MOD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "check_merge_consensus.py")
_spec = importlib.util.spec_from_file_location("check_merge_consensus", _MOD_PATH)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

PASS = 0
FAIL = 0


def check(name, actual, expected):
    global PASS, FAIL
    if actual == expected:
        PASS += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}: expected {expected!r}, got {actual!r}")


# --- author_seat_of: lane declarations ------------------------------------
check("author lane 9", gate.author_seat_of("Seat: Naya Smith (Lane 9)"), "Lane 9")
check("author lane 1", gate.author_seat_of("Seat: Naya Verity (Lane 1)"), "Lane 1")
check("author lane 12 two-digit",
      gate.author_seat_of("Seat: Naya Herald (Lane 12)"), "Lane 12")
check("author lane, prose around it",
      gate.author_seat_of("Some intro.\nSeat: Naya Sage (Lane 2)\nMore text."),
      "Lane 2")
check("author legacy naya 5 unchanged",
      gate.author_seat_of("Seat: Naya 5"), "Naya 5")
check("author explicit-declaration rule preserved",
      gate.author_seat_of("needs Naya 2 review.\nthe Naya 1 judge.\nSeat: Naya 5"),
      "Naya 5")
check("author lane 13 fail-closed",
      gate.author_seat_of("Seat: Naya Smith (Lane 13)"), None)
check("author lane 0 fail-closed",
      gate.author_seat_of("Seat: Naya Smith (Lane 0)"), None)
check("author no declaration", gate.author_seat_of("just prose"), None)

# --- seat_of: reviewer / scorer comments -----------------------------------
check("reviewer full lane declaration",
      gate.seat_of("[LANE 9 · REVIEW] APPROVED\nSeat: Naya Smith (Lane 9)"),
      "Lane 9")
check("reviewer lane incantation only",
      gate.seat_of("[LANE 5 · REVIEW] APPROVED"), "Lane 5")
check("reviewer legacy naya tag unchanged",
      gate.seat_of("[NAYA 2 · REVIEW] APPROVED"), "Naya 2")
check("reviewer unvalidated name still parses (honor-based)",
      gate.seat_of("Seat: Naya Nobody (Lane 9)"), "Lane 9")
check("reviewer random prose", gate.seat_of("looks good to me"), None)
check("reviewer lane 13 fail-closed",
      gate.seat_of("[LANE 13 · REVIEW] APPROVED"), None)

# --- cross-namespace distinctness ------------------------------------------
check("lane author distinct from naya reviewer",
      gate.author_seat_of("Seat: Naya Smith (Lane 9)")
      != gate.seat_of("[NAYA 2 · REVIEW] APPROVED"), True)
check("two lanes distinct",
      gate.author_seat_of("Seat: Naya Smith (Lane 9)")
      != gate.author_seat_of("Seat: Naya Judge (Lane 5)"), True)
check("same lane, name typo, still same seat (number is identity)",
      gate.author_seat_of("Seat: Naya Smyth (Lane 9)")
      == gate.author_seat_of("Seat: Naya Smith (Lane 9)"), True)

# --- _looks_like_review: lane incantation -----------------------------------
check("review lane incantation",
      gate._looks_like_review("[LANE 9 · REVIEW] APPROVED"), True)
check("review legacy incantation",
      gate._looks_like_review("[NAYA 2 · REVIEW] APPROVED"), True)
check("review no incantation",
      gate._looks_like_review("just a comment"), False)



# --- live-bytes regression: the actual #2453 scorecard headings --------------
_LIVE_LANE1 = '## [LANE 1 · Naya Verity] Independent scorecard — **9.0/10 APPROVE** (seat 1 of 2)\n\nFull verdict: #2175 comment 6119182006.\n\nPin-exact on `3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4` (re-pinned at action time ×2; parent == live tip `e85c6e44`, unmoved): 8/8 mjs tests green in my run on exact head bytes; test-file blob `0455090343...` byte-identical to the t1332-verified fix; delta tip→head = only the 2-line test fix + the in-tree receipt; zero production bytes.\n\nCheck-run classification (19 runs): 13 success + Supabase skipped (neutral). The 5 reds are all paperwork/pre-existing/by-design, zero substance: `test` = pre-existing at parent tip (this PR flips the mjs step only — 3 other tip failures belong to other lanes); `Receipt gate` ×2 = paperwork (backticked branch name tripped the path detector — body fixed, gate re-ran GREEN at 06:45Z); `Team review` ×2 = by-design until the 2-seat bar closes; `Receipt pin` = MISSING pin block (pin block for this exact head now written to the PR body; note the pin gate does not listen to `edited`, so it re-runs on the next synchronize).\n\nHonest bounds: does not turn the `test` job green alone (1 of 4 tip failures); CI job logs 401-unreadable so classification is conclusion-level + local reproduction. APPROVE for merge under the Scorecard Law once the second independent 9.0+ seat lands.\n'

check("live heading [LANE 1 · Naya Verity] parses",
      gate.seat_of(_LIVE_LANE1), "Lane 1")
check("live heading [LANE 9 · Naya Smith] parses",
      gate.seat_of("## [LANE 9 · Naya Smith] Independent scorecard — "
                  "**9.0/10 APPROVE** (seat 2 of 2)"),
      "Lane 9")

# --- end-to-end: lane-authored PR passes with lane review + scorecard ------
def _stubbed_run_gate(pr_body, comments, reviews=()):
    head = "a" * 40
    pr = {"body": pr_body, "user": {"login": "SoulSchoolAcademy"},
          "created_at": "2026-10-12T00:00:00Z"}
    calls = {"n": 0}

    def fake_api_get(path, token):
        calls["n"] += 1
        if path.endswith(f"/pulls/1"):
            return pr
        if path.endswith("/reviews"):
            return list(reviews)
        return [{"body": c} for c in comments]

    real = gate.api_get
    gate.api_get = fake_api_get
    try:
        gate.run_gate("tok", "o/r", "1", head)
    finally:
        gate.api_get = real
    return head


def e2e(name, pr_body, comments, expect_pass, reviews=()):
    global PASS, FAIL
    try:
        _stubbed_run_gate(pr_body, comments, reviews)
        passed = True
    except SystemExit as e:
        passed = (e.code == 0)
    if passed == expect_pass:
        PASS += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}: expected pass={expect_pass}, got pass={passed}")


_head = "a" * 40
e2e("e2e live #2453 Lane-1 scorecard heading parses as scorer",
    "Body.\nSeat: Naya Smith (Lane 9)",
    ["[LANE 5 · REVIEW] APPROVED\nSeat: Naya Judge (Lane 5)",
     _LIVE_LANE1.replace("3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4", _head)
     + "\nhead: " + _head],
    True)
e2e("e2e lane author + lane review + lane scorecard PASS",
    "Body.\nSeat: Naya Smith (Lane 9)",
    ["[LANE 5 · REVIEW] APPROVED\nSeat: Naya Judge (Lane 5)",
     f"## SCORECARD\nhead: {_head}\nHonest scorecard: 9.2/10\n"
     "Seat: Naya Judge (Lane 5)"],
    True)
e2e("e2e lane author + naya-2 reviewer + naya-2 scorer PASS",
    "Body.\nSeat: Naya Smith (Lane 9)",
    ["[NAYA 2 · REVIEW] APPROVED",
     f"## SCORECARD\nhead: {_head}\nHonest scorecard: 9.4/10\nSeat: Naya 2"],
    True)
e2e("e2e lane author, same-lane reviewer rejected",
    "Body.\nSeat: Naya Smith (Lane 9)",
    ["[LANE 9 · REVIEW] APPROVED\nSeat: Naya Smith (Lane 9)"],
    False)
e2e("e2e lane author, no review FAILS",
    "Body.\nSeat: Naya Smith (Lane 9)", [], False)
e2e("e2e no author declaration FAILS",
    "Body with no declaration.", [], False)
e2e("e2e legacy naya author still passes",
    "Body.\nSeat: Naya 5",
    ["[NAYA 2 · REVIEW] APPROVED",
     f"## SCORECARD\nhead: {_head}\nHonest scorecard: 9.0/10\nSeat: Naya 2"],
    True)

print(f"\n{ PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
