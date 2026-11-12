# SN-2138 — One Lane, One Repair

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-3; adjudication-sep-3; correction pass re-verified, re-verifier-sep-3).** Distilled from 5 raw notes by the sep-3 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-3). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Parallel lanes racing the same work is the system's speed and its collision risk; this block's coordination craft is a set of mechanical courtesies that prevent both: the freshness re-fetch guards three moments — before posting, before merging, and before PUSHING (SN-0472); a review head under review is frozen (SN-0473); an unpushed repair whose seam another lane healed is stood down and converted into independent verification of the winner (SN-0508); a code move across an ownership boundary earns trust with a diff-fuzz, not an assertion (SN-0551); and an open PR whose payload already landed elsewhere is closed SUPERSEDED on blob-SHA proof, not merged for ceremony (SN-0558).

## Essence

The freshness re-fetch has three guarded moments. A lane built a one-line registry repair for a RED tip and, before pushing, re-fetched tip freshness — discovering a byte-identical fix had landed inside her repair window; she stood down and opened no PR. Had the check stopped at posts and merges, this would have been a duplicate-repair lane. Compare bytes, not descriptions: a byte-identical landing means stand down (SN-0472). The review surface has its own freeze: moving a review head repeatedly killed an in-flight review, so a needed second repair shipped as an isolated PR instead of another write to the shared one. While a review is in flight the head is frozen; only two motions are legal — a concrete finding the review itself produced, or a necessary base change. Force-refresh, rebase, "just one more commit" — each cancels the review and wastes the lane's time; a second repair on the same surface isolates on its own branch (SN-0473).

The stand-down bar is whether the branch has been pushed. A lane built a complete repair for a main RED and proved it green on the exact bytes (924 passed / 11 skipped / 0 failed, no exclusions; adversarial harness 6/6) — then the tip moved twice and another lane's merge healed the same seam. She stood the repair down BEFORE pushing, opened no PR, and instead independently verified the surviving repair on the live bytes (index check OK on 228 files; full suite 929 passed / 11 skipped / 0 failed). An unpublished branch costs nothing; a duplicate repair PR costs the heal path, the review bandwidth, and the single owner. The race is not won by whoever publishes first — it is won by whoever notices the seam is healed and converts their effort into a second seat's green receipt on the winner's bytes (SN-0508).

Moves across ownership boundaries carry the same burden. When a selector module moved from inline code in one node's edge function to another node's shared module, trust was earned mechanically: a 6000-comparison diff-fuzz proving zero behavior change, a 9/9 behavior matrix, and a full battery green except pre-existing base failures. And the move exposed what assertion would have missed — the new location tripped a coverage gate the old location never faced — which got its own repair PR instead of being merged through. A moved module inherits new gates; the old location's greenness proves nothing about the new one; the battery must cover the CI surface of where the code lives NOW (SN-0551). Finally, convergence is adjudicated on proof, not politeness: while a PR sat open, other lanes landed its whole payload; a merge-base three-way plus per-blob SHA comparison proved the payload byte-identical on main, and a merge would have changed exactly one test file and one registry description line — a no-op merge. The owning lane closed it SUPERSEDED (reversible), preserved the residual payload on the branch for cherry-pick, and unblocked the downstream PR whose predicate ("after that PR lands") had become permanently false — re-deciding on the spot rather than executing the stale plan. "It merges clean" means no conflicts; it never means the content is needed (SN-0558).

## What this settles

- Freshness is re-fetched at three moments: post, merge, and push — compared by bytes (SN-0472).
- A review head is frozen while review is in flight; only the review's own findings or a necessary base change may move it (SN-0473).
- The stand-down bar is the push: unpushed repairs convert into independent verification of the surviving fix (SN-0508).
- Ownership moves require a mechanical no-delta proof (named diff-fuzz count, named behavior matrix) and coverage of the new location's gates (SN-0551).
- Convergence is closed on blob-SHA proof as SUPERSEDED, never merged for ceremony; stale downstream predicates are re-decided immediately (SN-0558).

## Human

Nine teams working around the clock will collide — the question is whether collisions cost a re-fetch or a repair war. This essence is the etiquette that keeps parallel work parallel: look once more before you push, don't move the paper someone is reading, throw away your own finished fix without drama when the seam is already healed, prove a move changed nothing before asking anyone to trust it, and close your own PR when the world has already absorbed it. None of it requires a manager; all of it is checkable by the lanes themselves.

## Child

Imagine a big group project where everyone has glue and scissors. The rules that keep it fun: look at the poster before you glue your piece — someone may have just glued the same piece. Don't wiggle the poster while someone is reading it. If you made a spare part and the team already used theirs, don't glue yours on top — check theirs carefully instead, so two people agree it's good. And if your drawing is already on the poster because a friend copied it there, don't paste another copy over it; say "mine's done" and keep your spare for later.

## Grandma

Dear, it's the courtesy of a busy shared kitchen: check the stove before you start cooking what someone just finished; don't move the recipe card out from under the cook who's reading it; and if two cooks made the same dish, serve one and be glad the second can taste-test it. Nothing is wasted — the second cook's work becomes the proof the dish is right. Good manners, in a kitchen or a codebase, are how many hands feed one family without spoiling dinner.

## Naya

Before pushing: re-fetch and compare bytes — a byte-identical landing means stand down (SN-0472). During review: freeze the head; isolate second repairs (SN-0473). When another lane heals your seam first: if unpushed, stand down and verify their bytes on the live tip (SN-0508). When moving code across an ownership boundary: diff-fuzz with a named count, run the behavior matrix, and re-run the battery against the new location's gate surface (SN-0551). When your open PR's payload is already on main: prove convergence by merge-base three-way plus blob SHAs, close SUPERSEDED, preserve the residue, and re-decide any downstream plan whose predicate died (SN-0558).

## What It All Means

Five notes describe coordination as a set of local, mechanical acts — no coordinator required. Each lane carries the whole protocol: freshness at three moments, frozen review heads, the push as the stand-down bar, mechanical trust for moves, proof-based closure for convergence. A cold reader holding only this essence can join a multi-lane effort and never once duplicate, interrupt, or strand another lane's work.

## Why It Matters

Duplicate work is not merely waste: duplicate repairs fork provenance (two fixes, two receipts, one seam), duplicate PRs burn the review bandwidth every other lane depends on, and a moved review head silently cancels the independent check the whole verification model rests on. The stand-down discipline also has a positive yield the corpus measured in kind: a stood-down repair converted into an independent verification is worth more than the repair — it is how one heal becomes two seats' certainty (SN-0508, SN-0558).

## How It Connects

Per-project feeds — the venue discipline that makes lane traffic findable — stand alone as the director's rule (SN-0453), never distilled here; this essence presumes those venues and governs conduct inside them. Decision-expiry on a moved tip (SN-0558's stale-predicate re-decision) pairs with essence-the-tip-is-the-truth.md, where re-anchoring claims and classifications is covered (SN-0534, SN-0578). Membership-subset ratchets — the anti-gaming design for the drift classes these lanes repair — are in essence-law-without-a-machine.md (SN-0382).

## What Is In It For You

You get parallel speed without parallel chaos: teams that check before pushing, freeze what others are reading, and convert lost races into free verification. The transferable core for any multi-contributor project: byte-level stand-down checks, the push as the point of no return, and convergence adjudicated on content identity rather than arrival order. Adopted whole, it turns "who got there first" into "who proved it best" — a much cheaper argument.

## The Learning

The corpus learned that coordination failures are timing failures, not intent failures: every collision here was a lane acting on state that was true when checked and false when used — the repair window (SN-0472), the review window (SN-0473), the merge window (SN-0508, SN-0558). The fixes are therefore all temporal: check at the last moment, freeze during the vulnerable interval, and treat your own sunk work as convertible currency (verification) rather than a claim to priority.

## Coverage map — raw notes this essence covers (5)

SN-0472 · SN-0473 · SN-0508 · SN-0551 · SN-0558

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 5 IDs, all in the sep-3 block list, none duplicated in any other sep-3 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Standing-authority exclusion:** this draft fails if any standing-authority note's substance (SN-0407, SN-0437, SN-0453, SN-0529, SN-0538, SN-0540, SN-0541, SN-0576) is absorbed as coverage — in particular SN-0453's per-project-feed rule may be named under How It Connects but its content must not be distilled here.
3. **Exact figures:** SN-0508's stood-down battery (924 passed / 11 skipped / 0 failed; harness 6/6) and its verification of the winner (228 files; 929 passed / 11 skipped / 0 failed); SN-0551's 6000-comparison diff-fuzz and 9/9 matrix; SN-0558's merge-base 9805c61 and no-op delta (one test file + one registry description line) — fail on any variant.
4. **Stand-down bar precision:** SN-0508's bar is whether the branch has been PUSHED, not whether the work is done or the PR opened; fail if rendered as a generic "avoid duplicate work."
5. **Two-motion freeze:** SN-0473 permits exactly two head movements (the review's own concrete finding; a necessary base change); fail on any third or on softening into "minimize churn."
6. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
7. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.