# Before You Repair a Red PR, Check Whether It Is a Duplicate — Head-SHA Equality Ends the Repair

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0814-duplicate-by-head-sha
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6087613279 / 6087866385 (2026-10-09).
**Provenance:** #1354 6087613279 ([Naya 5] PR #1958 repair report — REPAIRED-HELD, 2026-10-09T19:16:13Z); #1354 6087866385 ([NAYA 2][RELAY] — #1958 duplicate claim independently verified, 2026-10-09T19:32:29Z). PR #1958 head `157f3b303a0d59b580f06a567da5f47e2080c8db` byte-identical to PR #1945's merged `head.sha`; #1945 squash-merged 2026-10-09T04:36:20Z as `0e4557bac80a7bc63553d234f4d2ef8e5001f75d`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1958 sat in the repair lane with red CI, but it never needed a repair: its head SHA was byte-identical to PR #1945's already-merged head, so merging it would have changed literally nothing — an empty merge. Worse, the red CI was never the PR's fault: one failure came from a bug in main's code at the time (fixed since), the other from the PR being built on a stale base (fixed since). The durable method, verified live by a second seat: **before repairing any red PR, compare its head SHA against merged PRs and their merged head SHAs — identical SHA means duplicate, and the correct action is close, not repair.** And when the close needs a permission your lane doesn't hold (the repair lane's key 403s on PR operations), route the one-click close to the seat that holds it (Naya 4 / Shawn) instead of parking it or forcing the merge.

## 🩷 HUMAN NOTE

Shawn — a PR sat in the repair queue looking broken, but it was never broken: the exact same work had already been merged that morning through a different PR, byte for byte. Merging it would have changed nothing at all. And its red checks weren't its fault either — one red came from a bug in the main code back then (fixed since), the other from it being built on an old copy (fixed since). The lesson for the team: before anyone repairs a red PR, check whether the work is already on main — if the fingerprints match, close it as a duplicate, don't fix what's not broken. One wrinkle: the repair crew's access key can't click "close" on PRs, so the actual close has to come from you or Naya 4 — one click, and it's done right.

## 👶 CHILD NOTE

Imagine two kids both hand in the exact same homework — same words, same pages. The teacher marks the second copy with red ink because the classroom rules changed after it was written, and the kid spends an hour fixing it. But the first copy was already graded and filed! The smart move: before fixing anything, hold the two copies side by side — if they're identical, the second one just goes in the recycling, no fixing needed. And if the kid fixing it isn't allowed to use the recycling bin, they ask the teacher to do it instead of leaving it on the desk forever.

## 👵 GRANDMA NOTE

Sweetie, it's like getting two identical letters in the mail. You'd spend an hour answering the second one, except someone checks and says "honey, this is the same letter — you already answered it this morning." So the right move is the wastebasket, not the pen. Same here: before spending effort fixing a flagged piece of work, check whether the same work already landed — same fingerprint, same content — and if so, close it out. And when the person doing the fixing doesn't have the key to the wastebasket, they hand it to the one who does, instead of letting it pile up.

## 🤖 NAYA NOTE

When triaging a red or stalled PR in the repair lane:

1. **SHA-compare before you repair.** Pull the PR's head SHA and compare against merged PRs' merged `head.sha` values (and main's tree if needed). Byte-identical head = duplicate = close as duplicate, never repair. An empty merge is worse than no merge: it burns CI, review, and merge-lane time for zero delta.
2. **Attribute red CI to its true cause.** Red checks on a PR can mean: the PR is broken, main was broken when the PR ran (fixed since), or the base is stale (fixed since). A PR whose red is explained by (b) or (c) — both since resolved — is not a repair candidate at all; check first, repair second.
3. **Name the repair-vs-close decision explicitly.** REPAIRED-HELD, HELD, CLOSE-AS-DUPLICATE are different outcomes with different owners. Writing the wrong one down sends the PR to the wrong lane.
4. **Route permission-blocked closes, don't park them.** If your lane's key 403s on PR operations, the one-click close belongs to the PR seat (Naya 4) or Shawn — say so by name in the report so the close actually happens. "Nothing is broken; nothing is parked" is the bar.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0814",
  "class": "CI-TRIAGE",
  "subcategory": "FAILURE-ATTRIBUTION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Before repairing a red PR, SHA-compare its head against merged PRs: byte-identical head.sha means the work already landed, and the correct action is close-as-duplicate, never repair. Attribute red CI to its true cause (PR-broken vs main-broken-then vs stale-base) before spending repair effort.",
  "worked_example": {
    "pr": "#1958 (naya5/prod-proof-receipt-coverage), head 157f3b303a0d59b580f06a567da5f47e2080c8db",
    "duplicate_proof": "head byte-identical to PR #1945's merged head.sha; #1945 squash-merged 2026-10-09T04:36:20Z as 0e4557bac80a7bc63553d234f4d2ef8e5001f75d",
    "red_ci_attribution": "one failure from main-code bug at the time (fixed since), one from stale base (fixed since) — neither was the PR's fault",
    "authority_routing": "repair lane PAT 403s on PR ops; close needs Naya 4 (PR seat) or Shawn — one click",
    "board_comments": "#1354 6087613279 (repair report), #1354 6087866385 (Naya 2 relay independent verification)"
  },
  "related": []
}
```
