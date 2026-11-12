# SN-2117 — The Handoff Is a Claim: Delivery, Coverage, and Duplicates Between Lanes

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-1).** Distilled from 8 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Verified without correction. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Work handed between lanes crosses three gaps — delivery, coverage, duplication — and each has a named discipline: a lost announcement is not lost work (repair the channel, repost the verified receipt, never rerun) (SN-045); verification coverage is pinned to a commit, so every head move opens a gap that must be named with its head (SN-046); duplicate repairs are caught by diffing the diffs (SN-052) and duplicate artifacts are owned openly and consolidated in public (SN-054). Authority shapes handoffs too: you supersede by comment on artifacts you don't own — the opener owns the close (SN-060). Verifiers publish their own numbers and make deltas interpretable with parent comparisons (SN-089); intake verification does not protect consumption-time state (SN-0112); and a push receipt proves nothing about contents — verify the tree (SN-0125).

## Essence

Work handed between lanes crosses three gaps — delivery, coverage, and duplication — and each gap has a named discipline. **Delivery:** when a worker's delivery channel swallows completed work, the work is not lost — only its announcement is. Twice in one night a verify worker finished its full verification and its board comment died in an approval queue at execution timeout; the recovery law is: repair the delivery mechanism, then **repost the verified receipt — never rerun the work**. The receipt is the work product; the channel is replaceable (SN-045). **Coverage:** verification is pinned to a commit, not a branch, so every head move opens a coverage gap — and the gap must be named out loud, with the uncovered head identified, and the baton passed explicitly; a small benign commit is exactly when gaps go silent, because nothing broke to announce them (SN-046). **Duplication:** parallel lanes repairing the same backlog will sometimes build the same repair twice — so diff the diffs before the merge list carries two of the same repair: two PRs proved byte-identical modulo index lines (the same single-field ledger change, the same migration path, the same entry) and were caught by direct comparison, not by either lane's self-report (SN-052). When two seats race the same trigger and both post artifacts — two Decision Scorecards 44 seconds apart on the same dispatch — the repair is public and mechanical: own the duplicate artifact openly in a consolidation comment, keep the better artifact canonical, and patch the trigger so the race cannot recur quietly (SN-054).

Authority shapes handoffs too. The opener owns the close: a lane that re-exactified a stale PR and opened a clean successor deliberately left the original PR **open**, because it had been opened under the director's account — supersession is recorded as a comment pointing at the successor, completing the record without touching an artifact that isn't yours; tidiness is never a reason to close something you don't own (SN-060).

Two receipt disciplines close the set. An independent verifier is a second measurer, not an auditor of the builder's report: when the builder reported 1127/0 and her own clean checkout returned 31/1091/3/5, she **published her own number** — never reconciled, averaged, or adopted — and then made the unfamiliar failing number interpretable by running the parent commit under identical conditions (parent failed 33, child 31: the change fixed two, added 21 passes, introduced zero new failures). "Zero new failures" is the strongest sentence a verifier can write, and it requires both measurements; the irreproducible builder number stayed on the record as an unresolved open item, disclosed rather than smoothed (SN-089). And intake is not consumption: a second independent execution held a trust seam's intake boundary under 48 systematic attacks, and sharpened what the boundary does *not* cover — the store is aliased by design, so a same-process mutation of the producer's store *after* intake propagates into the consumer's extraction (the learned lesson became attacker text). Pin what you consume, not just what you verify: intake verification does not protect consumption-time state (SN-0112). The general form of the same law closes the loop on delivery itself: a push receipt is not proof of contents — a reported commit SHA's tree simply did not contain the announced files, because a push-map extension had silently not applied; verify file-by-file through the tree at the resulting commit before claiming anything exists anywhere (SN-0125).

## What this settles

- Lost announcement ≠ lost work: repair the channel, repost the verified receipt, never rerun (SN-045).
- Coverage is per-commit; every head move's gap is named with its head, and the baton is passed explicitly (SN-046).
- Duplicate repairs are caught by diffing the diffs, not by trusting lane reports (SN-052); duplicate artifacts are owned openly, consolidated publicly, and the trigger patched (SN-054).
- You supersede your own artifacts; artifacts opened under another's authority get a pointing comment, not your close (SN-060).
- Verifiers publish their own numbers; parent comparisons make deltas interpretable; irreproducible claims stay open, disclosed (SN-089).
- Verification at intake does not cover consumption-time aliasing — pin what you consume (SN-0112); push receipts prove nothing about trees — verify the tree (SN-0125).

## Human

Passing work between people is where things quietly go wrong: a finished report never arrives, the thing that was checked is no longer the thing that exists, two people unknowingly do the same job, or a delivery note claims files that never landed. These rules make every handoff checkable: repost receipts instead of redoing work, name exactly which version your check covers, compare duplicate work directly, never close someone else's ticket for tidiness, publish your own measurements rather than trusting the other person's, and verify what's actually in the delivered package.

## Child

Imagine passing a note in class. If the note gets lost, you don't redo your whole homework — you just send the note again. If your friend adds a page to the project after you checked it, you say "I checked it before the new page" out loud. If you and a classmate accidentally do the same worksheet, you compare them side by side and keep one. And you never throw away someone else's paper just to tidy up — that's theirs.

## Grandma

Dear, it's the etiquette of reliable messengers. A lost letter doesn't mean the news never happened — write the letter again, don't redo the event. Say exactly which version of things your word covers. When two people send the same message, acknowledge it openly and keep one. Never dispose of another person's papers for neatness. And check the parcel's contents yourself rather than trusting the delivery slip.

## Naya

On any delivery failure, separate the work from its announcement: repair the channel, repost the receipt (SN-045). Pin every verification claim to its commit and announce head moves as coverage gaps (SN-046). Diff competing repairs byte-wise before merge listing (SN-052); consolidate race duplicates in public and patch the trigger (SN-054). Record supersession by comment on artifacts you don't own (SN-060). Measure independently and publish your own counts, with a parent comparison when they differ (SN-089). Audit consumption-time state, not just intake (SN-0112), and verify pushed contents at the tree, file by file (SN-0125).

## What It All Means

Eight notes govern the space between lanes — where work is most often lost, doubled, or overclaimed without anyone lying. A cold reader holding only this essence can still hand work over, receive it, and audit the seam, which is exactly what these notes were written to make reliable.

## Why It Matters

Handoffs are where a multi-lane system's truth quietly leaks: the work exists but nobody knows, the check was real but covers a version that no longer exists, the delivery slip lies by omission (SN-045, SN-046, SN-0125). For the reader, this essence is the guarantee that what crosses between lanes in this system arrives checkable — receipt reposted, coverage pinned, contents verified at the tree — so "done and handed over" means the same thing to the sender and the receiver.

## How It Connects

The handoff disciplines run on the narration protocol of SN-0109 — the director's standing board protocol, which stands alone and is not distilled in this block: reposts, coverage-gap announcements, and consolidation comments are all board acts under it. Within the block, SN-089's own-number rule is the lane-scale form of essence-evidence-law.md's independence law (SN-028), SN-0112's aliasing warning bounds the intake proofs of essence-composition.md (SN-085, SN-088), and SN-0125's tree verification is the delivery form of that essence's pushed-bytes rule (SN-050). Duplicate consolidation (SN-054) is the receipt-side twin of essence-one-canon.md's convergence protocol (SN-0117).

## What Is In It For You

Work you hand off — or receive — stops evaporating: finished work is announced recoverably, checks state exactly what they cover, duplicates are caught by comparison instead of by embarrassment, and your own artifacts are never tidied away by someone else's lane. Apply it in any team: separate the work from its announcement, pin claims to versions, diff duplicates directly, and verify the delivered contents, not the delivery slip.

## The Learning

The corpus learned that the channel is not the work (SN-045), that coverage silently expires with every head move unless someone names it (SN-046), and that a receipt — of a push, of an intake, of a builder's count — is a claim about a different act than the one it is usually cited for (SN-0125, SN-0112, SN-089). The behavior change: handoffs in this system now ship with their own verification step, because the seam, not the sender, turned out to be where truth was lost.

## Coverage map — raw notes this essence covers (8)

SN-045 · SN-046 · SN-052 · SN-054 · SN-060 · SN-089 · SN-0112 · SN-0125

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 8 IDs, all in the sep-1 block list, none duplicated elsewhere in this block's accounting.
2. **Recovery rule:** SN-045's recovery is repost-the-receipt after repairing the channel; fail if the essence permits rerunning the verification as the default recovery.
3. **Coverage pinning:** SN-046's gap case (verify at `cf62b761`, head moved to `bd8fda27`) — fail if the essence states coverage follows the branch.
4. **Duplicate detection:** SN-052's pair (#1238 vs #1209) was byte-identical modulo index lines, caught by diffing the diffs; fail if the essence relies on lane self-reports as the detection mechanism.
5. **Race timing:** SN-054's two scorecards landed 44 seconds apart and were consolidated by a public comment that owned the duplication; fail on altered timing or a quiet-stand resolution.
6. **Ownership close:** SN-060's original PR (#1139, opened under the director's account) was left open with a supersession comment; fail if the essence allows closing another's artifact for tidiness.
7. **Verifier numbers:** SN-089's figures (builder 1127/0; verifier 31/1091/3/5; parent 33 failures; child fixed two, added 21 passes, zero new failures) must match the source; fail on any altered number.
8. **Aliasing mechanism:** SN-0112's residual risk is post-intake mutation through the aliased store, demonstrated under 48 attacks at intake; fail if the essence claims the intake proof covers consumption.
9. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
10. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.