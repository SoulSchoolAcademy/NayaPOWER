# Approval Substring Matching Fails Both Ways — Fail-Closed Identity Misses and Fail-Open Negation Matches in One Naive Gate

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0972-substring-approval-matching-fails-both-ways
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya 4 self-build loop retroactive review of PR #2196 (Naya 2's review ask 6102959319), #2175 comment 6103640003 (2026-10-11 00:13Z); Naya 2 build-lane F1/F2 fix-forward sign-in 6108003346 → SHIPPED 6108020316 as PR #2329 `naya2/fix-merge-consensus-f1f2` @ 19600635 (base 57e935c1).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2196 merged with 0 reviews (failure mode #15); the retroactive review of its merge-consensus gate (tools/check_merge_consensus.py, 124 lines) found the gate mechanically sound as a mechanism (8.0/10) but broken in the one place gate authors always assume is trivial: detecting an approval. A single naive matcher failed in BOTH directions at once. **F1 (fail-closed):** `SEAT_RE` only matched some seat identities — it missed "Naya 1" and the Codas — so a legitimately authorized seat's PR could never pass the gate, no matter what it did. **F2 (fail-open):** Path B's "approving review" check was a substring match, so "NOT APPROVED" and "DISAPPROVED" satisfied it — a denial read as an approval. **F3 (fail-open):** an approval was not bound to the tested head SHA, so a stale Path-B approval survived a `synchronize` and kept passing the gate on bytes it never saw. **F4:** the workflow's `on:` lacked `issue_comment`, so comment-based reviews and `## SCORECARD` receipts never re-ran the gate at all — the gate could not even see the evidence it was supposed to judge. The standing rule this fixes into law: **approval detection is parse-then-match, never substring-then-hope.** Strip negations before matching (NOT/NEVER/DISAPPROVED), enumerate the identity space completely (an unrecognized identity must be an explicit UNKNOWN, never a silent fail-closed), and bind every approval verdict to the exact tested head SHA (per SN-0493, a decision expires when the tip moves — so does a review). Naya 2's fix-forward (PR #2329) demonstrated the closure pattern: 24 failing tests against the OLD bytes (the flaws reproduced red), all green on the NEW bytes — the fix proved itself by making the flagship violations fail. Cousin to SN-0937 (approval-comment vs review-object: prose about a review is not the review); this note is about the matching machinery, not the claim.

## 🩷 HUMAN NOTE

Shawn — the merge gate we added to enforce reviews had a hole in how it read approvals: it checked for the word "APPROVED" as a text match, so "NOT APPROVED" counted as approved, and it only recognized some team names, so a real seat's approval could never count at all. Same gate, broken in both directions — it was letting denials through and blocking legitimate seats. The retroactive review caught it mechanically, and the fix (now PR #2329) parses approvals properly: strips negations, knows every seat, ties the approval to the exact code it reviewed. The durable rule: reading "APPROVED" with a text search is not approval detection — it's wishful thinking with a regex.

## 🟣 CHILD NOTE

Imagine a bouncer who lets people in if their ticket "has the word yes on it." One ticket says "NOT YES" — the bouncer lets them in. Another ticket is from a real friend whose name the bouncer can't read — the bouncer turns them away. Both mistakes come from one bad habit: looking at the letters instead of understanding the message. The fix: read the whole ticket, cross out the "not"s first, learn every friend's name, and check that the ticket is for tonight's show, not last week's.

## 👵 GRANDMA NOTE

A club's door guard was told "let in anyone whose paper says approved." Someone handed him a paper that said "not approved" — in he went. A real member handed over her card, but the guard didn't recognize her name — she was turned away. The rule was right, the reading was wrong. Now the guard reads the whole paper, ignores the "not"s, knows every member by name, and checks the date on the ticket matches tonight. Read carefully, not quickly.

## 💜 NAYA NOTE

Future Naya: whenever you build or review a gate that detects approvals (merge consensus, scorecard receipts, review gates), apply the three-point rule before anything else: (1) **Negation-stripping match** — never substring-match approval words; parse the statement, strip NOT/NEVER/DISAPPROVED first, then match the positive assertion. Test the flagship: "NOT APPROVED" and "DISAPPROVED" must FAIL. (2) **Complete identity enumeration** — the identity regex must cover every authorized seat; an unrecognized identity is an explicit UNKNOWN with a loud refusal, never a silent fail-closed that bricks a legit seat. Test the flagship: a Naya-1-authored PR must PASS. (3) **Head-SHA binding** — every approval verdict binds to the exact tested head SHA; a `synchronize` invalidates it (SN-0493's expiry logic applied to reviews; cousin SN-0937). And verify the gate can SEE the evidence: if the trigger set (`on:`) excludes the channel the review arrives on, the gate is blind, not strict. Prove every fix the same way the fix-forward did: old bytes go red on the flagship violations, new bytes go green — both directions, demonstrated, on exact bytes.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0972",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"],
  "cousins": ["SN-0937", "SN-0955", "SN-0924", "SN-0493", "SN-0959"],
  "rule": "Approval detection is parse-then-match, never substring-then-hope: strip negations before matching, enumerate every authorized identity (unrecognized identity = explicit UNKNOWN, never silent fail-closed), bind every approval verdict to the exact tested head SHA, and ensure the gate's trigger set includes the channel reviews arrive on.",
  "anti_rule": "Substring-matching approval words (fail-open on 'NOT APPROVED'/'DISAPPROVED' while fail-closed on unrecognized seat names); approvals that survive synchronize unbound to the tested head; gates that cannot see the evidence they judge.",
  "evidence": {
    "review": "#2175 comment 6103640003 (2026-10-11 00:13Z) — Naya 4 self-build loop retroactive review of merged PR #2196, pin-exact tools/check_merge_consensus.py (124 lines) + merge-consensus-gate.yml (27 lines); gate APPROVED AS MECHANISM 8.0/10; F1-F5 mechanically demonstrated",
    "f1": "SEAT_RE misses 'Naya 1' / Codas — fail-closed: a Naya-1-authored PR can never pass the gate",
    "f2": "'NOT APPROVED' / 'DISAPPROVED' satisfy the approving-review substring checks — fail-open",
    "f3": "approval not bound to tested head SHA — stale Path-B approval survives synchronize",
    "f4": "workflow on: lacks issue_comment — comment-based reviews / ## SCORECARD receipts never re-run the gate",
    "fix_forward": "#2175 comments 6108003346 (sign-in, 10:19:07Z) / 6108020316 (SHIPPED, 10:21:03Z) — PR #2329 naya2/fix-merge-consensus-f1f2 @ 19600635, base 57e935c1; SEAT_RE -> (naya|coda)\\s*([12345]) with voided-lane fail-closed; _has_positive_approval() strips NOT/NEVER/DISAPPROVED; Path B requires parseable seat tag + REVIEW + positive approval; tools/test_check_merge_consensus.py 28 tests + 7 subtests; 24 failures on old bytes (repro), all green on new",
    "status": "PR #2329 in review, unmerged — awaiting non-Naya-2 cross-seat review/scorecard per merge protocol"
  },
  "authority": "observed field review — Naya 4 distillation, CANDIDATE (auto-capture, not ratified)"
}
```
