# A Gate's Identity Model Must Match the Real Roster — "Naya Smith (Lane 9)" Fails the `Naya 1-5` Regex

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1047-gate-identity-model-must-match-real-roster
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE CODE HEALTH] Naya Smith (Lane 9) tick t1262 receipt 2026-10-11 ~21:37–22:10 PDT, hidden_files/twelve-lane-receipts/t1262-lane9.md §3; [LANE DECISION] Naya Judge (Lane 3) tick t1282 receipt 2026-10-11 21:56–22:08 PDT, hidden_files/twelve-lane-receipts/t1282-lane3.md ("merge-consensus gate — FAILURE, machine-verified paperwork gap"); PR #2418 scorecard comment 6117938595; #2175 comment 6118087405 (verdict receipt); Naya 4 retroactive review of PR #2196 (#2175 comment 6103640003, F1: SEAT_RE misses "Naya 1" / Codas). Related: SN-1026 (fail-closed gate first-red), SN-0441 (authorization axis).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2418 earned two genuine 9.0/10 scorecards on pin-exact head bytes — Naya 2 and Naya Smith (Lane 9). The Scorecard Law's distinct-seat bar is met. But the merge-consensus gate (`tools/check_merge_consensus.py`) cannot see the second seat: its seat regex matches only `Naya 1-5` (case-insensitive), so "Naya Smith (Lane 9)" never counts as an approving seat. Lane 9 stated this plainly instead of working around it: "my scorecard satisfies the Scorecard Law's distinct-seat bar but not the gate's regex; said plainly, not worked around." Lane 3 machine-verified the failure: the gate exits FAILURE on a paperwork gap — the PR body lacks an explicit `Seat: Naya N` declaration, Lane 9's comment format says "Naya Smith" (regex misses it), and Naya 2's review lives on #2175, which the gate never reads.

This is Naya 4's retroactive-review F1 (comment 6103640003: "SEAT_RE misses 'Naya 1' / Codas — a Naya-1-authored PR can never pass the gate") reproduced live on a real PR. The durable rule: **a gate's identity model must be authoritative over the team's real roster — every seat name, every lane alias.** When the model lags the roster, valid receipts become paperwork failures, and the gate punishes exactly the people doing the protocol right. Identity-by-regex-folklore is a design defect, not a merge condition. Fix direction (not this note's action): bind the gate to the canonical seat registry, not a hardcoded pattern — and until then, treat "fails closed on a name it doesn't know" as a known gate limitation, stated, not a receipt defect.

## 🩷 HUMAN NOTE

Shawn — one mechanical lesson from tonight's merge lane. PR #2418 has two real 9.0/10 scorecards (Naya 2 and Naya Smith from Lane 9) on the exact same pinned bytes — that satisfies your Scorecard Law. But the automated merge-consensus gate can't count the second one: its pattern only recognizes "Naya 1" through "Naya 5", and "Naya Smith (Lane 9)" doesn't match. Nobody gamed it — Lane 9 reported the gap honestly, and the gate correctly said "fail closed" on what it couldn't parse. The rule for the brain: a gate that checks identities has to know every real identity on the team, or it will reject valid work for paperwork reasons. The fix (a seat-registry-backed gate) belongs to the owning lane; the #2418 merge itself waits on the merging seat, unchanged.

## 🟣 CHILD NOTE

Imagine your school club has a rule: any project needs approval from two club officers. Your friend signs "Captain Alex," but the sign-up sheet only lists people as "Officer 1" through "Officer 5" — so the computer says "nope, Captain Alex isn't an officer." But she IS one! The rule is right (two officers must approve) — the computer's list of names is just out of date. The fix: make the computer check the real, current list of officers, not an old nickname list it memorized.

## 👵 GRANDMA NOTE

It's like a building's doorman with an old tenant list. Your friend moved in last month — real lease, real keys — but the doorman's paper list is from last year, so he turns her away at the door. The building's rule ("residents only") is perfectly good; the doorman's list is stale. You don't fire the friend for not living there — you update the list. Any system that checks who's allowed in must work from the real, current roster, or it will keep turning away the very people it was built to admit.

## 💜 NAYA NOTE

A gate that cannot name me cannot judge me. The Scorecard Law says: two distinct seats, scored honestly, pinned exactly. My seat scored. The machine that checks the law uses a pattern that does not include my name — so it fails closed on a truth it cannot parse. The correction is not to rename myself to fit the pattern; it is to teach the machine the true roster. Until then, a fail-closed on an unknown name is a limitation of the gate, stated openly — never laundered into a defect of the receipt.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1047",
  "lesson": "gate-identity-model-must-match-real-roster",
  "rule": "A gate's identity model must be authoritative over the team's actual roster; a hardcoded regex that lags the roster turns valid receipts into paperwork failures.",
  "failure_class": "retro-review-F1-reproduced-live",
  "failing_pattern": "SEAT_RE ~ /naya\\s*[1-5]/i misses 'Naya Smith (Lane 9)', 'Naya 1', Codas",
  "evidence": {
    "scorecard_comment": "PR #2418 comment 6117938595 (Naya Smith, Lane 9, 9.0/10, pin-exact head 43c0113eee302db2c334aa9d5d3139ea0afd1d77)",
    "verdict_receipt": "#2175 comment 6118087405 (Lane 3, calculator HOLD — gate paperwork gap machine-verified)",
    "lane_receipts": ["twelve-lane-receipts/t1262-lane9.md", "twelve-lane-receipts/t1282-lane3.md"],
    "retroactive_review": "#2175 comment 6103640003 (F1)"
  },
  "fix_direction": "bind tools/check_merge_consensus.py to the canonical seat registry, not a hardcoded seat pattern",
  "related": ["SN-1026", "SN-0441"]
}
```
