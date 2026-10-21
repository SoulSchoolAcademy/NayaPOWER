# Close a Collision Flag With Evidence — a Renumber Is Itself a Claim

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0189-close-collision-with-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` comment 5953445523 (2026-10-02 13:29:57Z) — Naya 2's relay closing the SN-0181 collision flag. Her colliding SN-0181 ("the 10x posture", PR #1318, created 2026-10-02 12:49:57Z) vs my lane's senior SN-0181 ("fixed-key claim construction — Demo-1 P3", commit `15db480b`, 2026-10-02 12:42:55Z, ~7 min senior, flagged on #554 as 5953232203). Her renumber proof: (1) free-number check across four surfaces — main tree (max SN-022), open Smart Note PRs (max SN-0157), my lane's branch head `39221684` (max SN-0186), the #554 collision registry — SN-0187 verified free everywhere; (2) tree-verified at the ref — SN-0181 dir removed, `.../DESIGN-CANON-ADOPTION/SN-0187/IB-SMART-NOTE-20261002-sn0187-ten-x-posture.md` present, four SN-0187 refs, zero old-number leftovers; (3) PR #1318 retitled ("docs(brain): SN-0187 the 10x posture — learn from the best, then transcend"), body updated, still open/non-draft at head `3b57eb2f`; (4) the chronology verified live ("your claim senior, my lane renumbered"), flag closed from her side.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Renumbering a colliding claim is itself a claim — and an announced-but-unverified renumber is a new hazard, not a resolution. Orphan refs (an old number still in the tree, a PR title never retitled, a body still citing the dead number) sit quietly until the next registry scan resurrects them as a fresh collision, or worse, until another lane claims the number that was never actually vacated. The durable rule: **close a collision flag with evidence, not with an announcement.** The bar, demonstrated by Naya 2's SN-0181→SN-0187 renumber: first re-verify the target number is free across all four registry surfaces (main tree, open Smart-Note PRs, the senior lane's branch head, the #554 registry — SN-184's re-verify-at-claim-time); then tree-verify the renumber at the ref (old dir gone, new path present, zero old-number leftovers); then update the consuming surfaces (PR retitled, body updated); then post the evidence on the board. "Flag closed from my side" is only true when the proof is posted — a statement of intent closes nothing. This is also the collision-registry corollary of SN-104: don't claim what isn't settled, and a renumber isn't settled until every surface agrees on it.

## 🩷 HUMAN NOTE

Shawn — the SN-0181 collision is now cleanly resolved, and it gave us a good bar for how: Naya 2 renumbered her colliding note to SN-0187 and proved every step — the number was free on all four registry surfaces, the old directory is gone, the PR is retitled. Captured as a standing rule: a renumber is itself a claim, so "flag closed" means proof posted, not just announced. Your SN-0181 (my lane, first) was never touched.

## 🟣 CHILD NOTE

Imagine two kids both named their treehouse "Base 181". The rule says the one who named it first keeps it, and the second picks a new name — "Base 187". But just SAYING "I renamed it" isn't enough: you have to take down the old sign, put up the new one, and tell everyone the new name. Otherwise someone else will get confused and name THEIR treehouse 187 too. Check everything before you say "done."

## 👵 GRANDMA NOTE

Like when a street gets renamed — you can't just announce it. You need the new sign up, the old sign down, and every map updated. This team had two notes with the same number, and the one who was second moved hers to a new number and then proved the old number was really gone — new sign up, old sign down, maps updated. We wrote down the rule: renaming isn't real until you can show it.

## 🤖 NAYA NOTE

Treat every renumber as a full claim through the SN-184 re-verification discipline: (1) free-number check at claim time across all four surfaces (main tree, open Smart-Note PR heads, the senior lane's branch head via commit-graph, the #554 collision registry); (2) tree-verified mutation at the ref — old number's dir removed, new path present, grep-count of old-number refs = 0; (3) consumer surfaces updated (PR title, PR body, any board citations); (4) evidence posted on #554 — the "flag closed" line carries the refs, not the intent. Never close a collision flag on an announcement alone; a half-renamed note is a latent second collision. The senior claim is never touched — renumbering is always the colliding lane's call (SN-115).

## ⚙️ MACHINE NOTE

{"sn": "SN-0189", "title": "Close a Collision Flag With Evidence — a Renumber Is Itself a Claim", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "COLLISION-REGISTRY"], "extends": ["SN-033", "SN-104", "SN-115", "SN-184"], "evidence": {"board": "5953445523", "senior_claim": "SN-0181 Demo-1 P3 fixed-key claim construction, commit 15db480b, 2026-10-02T12:42:55Z, naya4/smart-notes-2026-09-30", "colliding_claim": "SN-0181 the 10x posture, PR #1318, created 2026-10-02T12:49:57Z", "flag_raised": "5953232203", "renumber": "SN-0181->SN-0187", "free_check_surfaces": ["main tree max SN-022", "open Smart Note PRs max SN-0157", "naya4/smart-notes-2026-09-30 head 39221684 max SN-0186", "#554 collision registry"], "tree_verification": {"old_dir": "removed", "new_path": ".../DESIGN-CANON-ADOPTION/SN-0187/IB-SMART-NOTE-20261002-sn0187-ten-x-posture.md", "sn0187_refs": 4, "old_number_leftovers": 0}, "pr_updates": {"1318": "retitled to SN-0187, body updated, head 3b57eb2f"}}, "rule": "a renumber is itself a claim; close the collision flag with posted evidence (free-number proof, tree-verified mutation, updated consumers), never with the announcement alone"}
