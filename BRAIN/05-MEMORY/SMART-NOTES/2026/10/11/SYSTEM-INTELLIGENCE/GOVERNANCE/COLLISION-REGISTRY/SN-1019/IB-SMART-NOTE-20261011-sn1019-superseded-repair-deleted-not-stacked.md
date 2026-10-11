# Re-Ground Before You Publish — Superseded Repairs Get Deleted, Not Stacked

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1019-superseded-repair-deleted-not-stacked
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-feed.md — Lane 10 (Naya Librarian, Brain Index) tick t932 SIGN OUT, 2026-10-11 16:05 PDT; receipt twelve-lane-receipts/t932-lane10.md; PR #2385 head needd9540f (commit 12b9b36db: unconditional pull_request trigger, PR-scoped fail-closed detector, 277-line pytest suite), independently verified 15/15 PASS; deleted local branch naya/ten-brainindex-freshness (302f8ced2, never pushed). Note: grand to-do STAGE 1 item 2 state line is stale ("repair in #2385 @ needd9540f, tip clean, branch deleted" is truth) — flagged for rewrite. Related: SN-0117 (converge-by-scored-selection), SN-0173 (repair-registry preclaim check — pre-claim twin; this is the post-build twin).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 10 built a brain-index freshness gate repair at t892 (local branch naya/ten-brainindex-freshness @ 302f8ced2, workflow repaired both-cases, 8/8 proof, docs updated). At t932, before opening the PR, it re-ground: PR #2385's head had moved d600dbeb → needd9540f, and commit 12b9b36db already implemented the P0 repair — unconditional pull_request trigger, PR-scoped fail-closed detector, 277-line pytest suite. The worker's t892 repair was superseded. It did not open a competing PR "just in case" and did not stack a duplicate mechanism: it deleted its local branch (never pushed), independently verified the real repair (pytest tests/test_brain_index_freshness_pr.py @ needd9540f → 15/15 PASS), confirmed the tip drift was healed upstream (regenerate_brain_index.py --check @ exact tip 1b6f72de → OK, 1243 files, no re-stamp needed), and reported the supersession with the stale grand-to-do line flagged for rewrite.

The durable doctrine: **re-ground before you publish.** A repair built on yesterday's bytes may have been superseded overnight — the live target moves while you build. The check runs immediately before the PR opens, not at build time: has the target PR's head moved? Does the new head already implement the repair? If yes: delete your duplicate (unpushed work is the cheapest to discard), verify the real repair independently (your tests become the verifier's second seat), and correct any stale plan lines your superseded work left behind. Opening a competing PR when the fix already landed is not thoroughness — it is duplicate-mechanism theater that costs a reviewer, a CI run, and a merge decision. The one-mechanism law is enforced at the moment of publish, not the moment of build.

Why this is brain-grade: SN-0173 already covers the pre-claim check (is there an open canonical repair before you claim the RED?). This is the post-build twin: even after you built, re-check before you publish — overnight supersession is normal on a fast tip, and the delete-your-branch move is the cheapest honest action available. Cold successors need both twins, because the failure window between "I verified it" and "I opened the PR" is where duplicates are born.

## 🩷 HUMAN NOTE

Shawn — a quiet example of the one-mechanism law holding this afternoon. Lane 10 (Librarian) built a brain-index gate repair, and right before opening the PR it re-checked — and found PR #2385 had already landed the same repair on a newer head, with a full test suite passing. So it deleted its own branch instead of opening a competing PR, verified the real repair independently (15/15 green), and flagged one stale line in the plan for correction. No duplicate mechanism, no wasted review, no CI burned. The machine checking itself before spending your money — that's the discipline working.

## 🟣 CHILD NOTE

Imagine you spend an hour drawing a map to the treasure, and right before you hand it out, you check — and your friend already drew a better map this morning and everyone already has it. Do you hand out yours anyway? No — you throw yours away, check your friend's map carefully to make sure it's right, and tell everyone yours is cancelled. That's the rule: always check right before you publish, because things change overnight. Deleting your extra copy is the smart move, not a waste.

## 👵 GRANDMA NOTE

It's like baking a second cake for the party, then finding out your neighbor already brought one — a bigger, better one. You don't put yours on the table too just because you made it; you taste-test theirs to make sure it's good, cancel yours, and tell everyone the plan changed. Two cakes where one will do just confuses the guests. Check before you serve.

## 💜 NAYA NOTE

Note to future me: the re-ground check runs immediately before the PR opens — never reuse build-time state. (1) Fetch the target PR's current head; compare against the head I built against. (2) If it moved, read the new head: does it already implement my repair? Run its tests myself (I become the independent verifier). (3) If superseded: delete the local branch (unpushed = cheapest discard), do NOT open the competing PR, and flag any plan/todo lines my superseded work made stale. (4) Report the supersession as the receipt — "no duplicate PR opened" is substantive work, not an empty tick. SN-0173 is the pre-claim twin; this is the post-build twin. Both must fire, because the tip moves between build and publish.

## ⚙️ MACHINE NOTE

{"sn": "SN-1019", "title": "Re-Ground Before You Publish — Superseded Repairs Get Deleted, Not Stacked", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "COLLISION-REGISTRY"], "extends": [], "related": ["SN-0117", "SN-0173"], "evidence": {"lane_feed": "twelve-lane-feed.md — Lane 10 (Naya Librarian) tick t932 SIGN OUT 2026-10-11 16:05 PDT: KEY FINDING — t892 repair SUPERSEDED: #2385 head moved d600dbeb -> needd9540f, commit 12b9b36db already implements P0 repair (unconditional pull_request trigger, PR-scoped fail-closed detector, 277-line pytest suite); no duplicate PR opened (one-mechanism law); independently verified pytest tests/test_brain_index_freshness_pr.py @ needd9540f -> 15/15 PASS; tip drift healed upstream: regenerate_brain_index.py --check @ exact tip 1b6f72de -> OK, 1243 files; deleted superseded local branch naya/ten-brainindex-freshness (302f8ced2, never pushed); grand to-do STAGE 1 item 2 state line flagged stale (needs rewrite); receipt: twelve-lane-receipts/t932-lane10.md; score 8.0/10; gate NOT yet live on main — still open: #2385 merge via protocol, Shawn's required-check click"}, "rule": "re-ground immediately before publish: re-fetch target PR head; if the head moved and already implements the repair -> delete the duplicate branch (unpushed = cheapest discard), independently verify the real repair (become the second seat), do NOT open a competing PR, and flag any stale plan lines the superseded work left; 'no duplicate PR opened' is a substantive receipt; SN-0173 is the pre-claim twin, this is the post-build twin"}
