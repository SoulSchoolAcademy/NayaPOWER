# SN-2179 — The Tip Moves: Evidence Expires

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 9 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED-WITH-CORRECTIONS — the SN-883 timeline sentence was corrected (the pushes at 09:59:33–34Z precede the scorecard; the ~15 seconds is scorecard→PUT); re-verification then required the same restatement in the Nutshell and The Learning, which a second correction pass executed and a different seat CONFIRMED against the page (re-verifier-oct-4, second-pass confirmation) — the SN-883 retirement hold is lifted. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

On a fast main, every observation is perishable. A headline announcing "Now on main (RUNG 1)" described a kit that lived only on a branch (SN-819); an hourly "nothing is broken" post was falsified four minutes later by a red tip (SN-823); regen evidence gathered inside a PR expired at the moment of merge, twice (SN-821); a merge executed on a PR record's stale base while two unreviewed pushes, landed before the scorecard was even written, had already falsified its base (SN-883). The family's law: **verify at the action instant, against the live ref, and carry nothing forward** — status claims are tip-anchored and timestamped or they are hope (SN-823), read and mutation must be adjacent (SN-883), and re-anchoring belongs at verify-time, not burned in advance against a tip that will move again (SN-889).

## Essence

**Claims about the present expire with the present.** A headline is a claim about the world, and a false headline is worse than a missing one: the "Now on main (RUNG 1)" announcement pointed at bytes that were branch-only, catchable by a 404-check of the live path. Tools make claims too — the freshness checker printed a false pin==tip equality in its own success message. The correction discipline is annotation, not erasure: mark the false claim (newest-dated section wins), keep the history verbatim (SN-819). Reports inherit the rule in its strictest form: every status claim is anchored — "green at `<sha>` as of `<time>`" — and an unanchored status claim is hope wearing a timestamp's clothes. The hourly "nothing is broken" post (6089194089) was falsified four minutes later by RED tip `185c8beb`; the report wasn't careless, it was *unanchored* (SN-823). Diagnostic documents split into two layers under the same law: their architecture survives, their status claims expire at write time. Findings get marked CONFIRMED / FIXED / STALE / UNKNOWN with source + SHA, canonical assembly authority outranks diagnostic documents, and a module's presence never proves its runtime binding (SN-835).

**Regen evidence dies at the merge.** In-PR regen evidence — the index regenerated, `--check` green inside the PR — expires at merge, because the merge lands on a tip the PR never saw. PR #2023 (tick 146) and #2056 (tick 151, tip `185c8beb`) both proved it, and the CI drift tripwire caught both. The law: regen + `--check` on a clean worktree at the *exact merge tip*, after the merge, not inside the PR before it (SN-821). The diff-side sibling: a two-dot `git diff base head` is a false-alarm machine on a moved main — it renders main's newer work as the branch's deletions (#2053: 2,172 phantom deletions). The honest instrument is a rehearsed merge: merge in a scratch worktree at the exact live tip and read the true delta (1 added + 2 modified, 23 passed). Merge evidence = rehearsed merge (SN-856).

**The actor's own precondition is the sharpest case.** A scorecard anchored "base == live tip" on the PR record — derived state from an earlier read — while the live tip had moved: the scorecard named parents `fe25661c+84c9f4fe`; the merge's real parents were `21d17e8e+84c9f4fe`, because two unreviewed direct pushes had landed at 09:59:33–34Z — before the scorecard (10:01:41Z), after the earlier read its anchor derived from. The seat *had* re-anchored at decision time; the window that remained was the ~15 seconds between scorecard and PUT (10:01:56Z), and the discipline that gap was missing is adjacency: **the read and the mutation must be adjacent**, with nothing unverified between them, and the parents named from a `GET refs/heads/main` performed immediately before the mutating call. The PR record's base is a claim about the past; only a ref read at the action instant is the present (SN-883). The observer's mirror image: a failure anchored on a superseded tip (`c41ad1a4`) during a merge burst is a race artifact, not a red. Re-verify the FINAL tip (`fd7f13ec`) three ways, carry nothing forward from the dead tip's run — observations expire exactly like decisions (SN-879).

**Completeness is a claim too, and watermarks lie.** A polling loop advanced a high-water mark over a window it never verified: the count-fetch vs page-fetch pagination shift skipped 25 comments (6091237689–6092215142) — including a DIRECTOR TEACHING (6091689263) — and the watermark held only 1,174 of 2,234 IDs while claiming the range. The prescription: fetch the last page *and* the one before it, reconcile every ID in the window, and advance the mark only over the reconciled set. Absence in an unreconciled window proves nothing (SN-853).

**Don't burn freshness in advance.** On a main moving at ~13 merges per 6 hours, staged PRs re-dirty faster than verification reaches them. One LEARN-DRIVER run re-anchored four staged trial-evidence PRs onto tip `801e3922` — the second re-anchor that day, each one real work (rebase, byte-verify evidence, re-run CI, re-notify the verifier) — and collected zero verifications; everything expired again with the next merges. The structural fix: re-anchor **at verify-time**, making "pull the current tip" step one of the verifier's recipe, or hold a merge-queue slot — and post the stale state openly instead of pre-freshening it. Two re-anchors and zero verifications means the process is doing the wrong work, not too little work (SN-889).

## What this settles

- Headlines and tool success messages are claims about the world; verify against the live path, annotate false claims, never erase them (SN-819).
- Status claims are tip-anchored + timestamped or they are hope (SN-823); diagnostic status expires at write time while architecture survives, findings marked CONFIRMED/FIXED/STALE/UNKNOWN (SN-835).
- Regen evidence gathered in-PR expires at merge; regen + `--check` run on a clean worktree at the exact merge tip (SN-821).
- Two-dot diffs on a moved main manufacture phantom deletions; merge evidence is a rehearsed merge at the live tip (SN-856).
- Base preconditions are re-read from the live ref immediately before the mutating call, parents named from that read — read and mutation adjacent (SN-883).
- A failure anchored on a superseded tip is a race artifact; re-verify the final tip three ways, carry nothing forward (SN-879).
- A watermark advances only over a reconciled ID set; unreconciled absence proves nothing (SN-853).
- At high tip velocity, re-anchor at verify-time or take a merge-queue slot — never as repeated pre-verification work (SN-889).

## Human

Everything in this system moves — the code, the board, the record — and it moves fast. These notes are about what that does to truth: a fact about the system is only true *at a moment, at a version*. Saying "it's green" without saying *which* version and *when* is like saying "the shop is open" without a day or an hour. The discipline here is simply always naming the moment your fact belongs to — and re-checking at the moment you act, because the fifteen seconds between checking and acting is exactly where trouble rides in.

## Child

Imagine a river. You take a picture of it and say "the river looks like this!" But the river keeps flowing — your picture is already old. Smart people write on the picture: "this is how it looked at 3 o'clock." And if they're about to jump in, they look at the river again *right before jumping*, not at the old picture.

## Grandma

It's the milk rule, dear: check the date, and check it when you're about to pour, not when you bought it. These engineers learned that "it was fine a minute ago" is not a safety standard when a minute is all it takes for two strangers' changes to land inside your work. And they learned to write the date on everything — a claim without its date is just a rumor with confidence.

## Naya

Anchor every status claim: "green at `<sha>` as of `<time>`," or don't make it (SN-823). 404-check live paths behind headlines — including your own tools' success output (SN-819). Split diagnostics into architecture (durable) and status (expires at write time), marking findings CONFIRMED/FIXED/STALE/UNKNOWN with source + SHA (SN-835). Run regen + `--check` post-merge at the exact merge tip (SN-821); replace two-dot diffs with rehearsed merges (SN-856). Immediately before any mutating call, `GET refs/heads/main` and name preconditions from that read; keep read and mutation adjacent (SN-883). On a superseded tip's failure, re-verify the final tip three ways and carry nothing forward (SN-879). Advance watermarks only over reconciled ID sets — fetch last page and last page − 1 (SN-853). Stage verification so re-anchoring happens at verify-time; post stale states openly (SN-889).

## What It All Means

Nine notes refine one ancestor law (SN-0493: a decision expires when the tip moves) into its working forms — for headlines, reports, diagnostics, regens, diffs, merge preconditions, failure observations, watermarks, and verification staging. The refinement that matters most is SN-883's: the expiry window is not the decision, it's the *gap between the last read and the mutation*, and on a busy main that gap is measured in seconds. Freshness is not a property a claim has; it's a property of the distance between the claim and the act.

## Why It Matters

Every other discipline in this campaign spends this one's currency. A classification (essence-classify-the-red.md) anchored on a superseded tip classifies a ghost; a scorecard whose base moved is a verdict on a world that no longer exists; a watermark that skips a director teaching loses instruction silently. For the reader: whenever anyone — person or system — tells you the state of a moving thing, the only questions that matter are "as of when?" and "checked again at the moment of action?" This essence is why those questions are reflex here.

## How It Connects

This is SN-0493's family album; the ancestor itself lives outside the block and is refined, not replaced, by these notes. The expiry logic applies to reviews in essence-merge-discipline.md (a stale-head approval does not bind the merged head, SN-937's cousin SN-883 axis) and to qualifications in essence-bounded-claims.md (SN-922: re-validate at publication moment — the same adjacency law for claims). The freshness of *proof* as doctrine — proof expires when its world changes, never by time — stands alone as SN-904 and is pointed to, not absorbed.

## What Is In It For You

You get the habit that prevents the most embarrassing class of error in any fast-moving work: acting on a true fact that stopped being true. Date your claims. Re-check at the moment of action, not the moment of decision. Treat any undated status — a dashboard, a summary, a colleague's "it's done" — as a picture of a river. The cost is one extra read; the payoff is never building on a world that has already moved.

## The Learning

The block's hardest freshness lesson was that the seat did almost everything right and still got caught: scorecard written, base read at decision time — but the environment had already moved before the scorecard was written; the ~15 seconds that remained was the gap between scorecard and PUT, and nothing landed inside it. The learning that compounded is that freshness is engineered, not intended: adjacency of read and mutation, verify-time re-anchoring, reconciled watermarks, and rehearsed merges are mechanisms, each built because a careful person was beaten by a gap they couldn't see.

## Coverage map — raw notes this essence covers (9)

SN-819 · SN-821 · SN-823 · SN-835 · SN-853 · SN-856 · SN-879 · SN-883 · SN-889

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 9 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Adjacency, not decision-time:** SN-883 must read as re-anchor at *action* time (fresh ref read immediately before the PUT, parents named from it, ~15s window, named vs actual parents both present); fail if softened to "re-check before merging."
3. **Verify-time rule:** SN-889 must keep "two re-anchors + zero verifications = the wrong work" and the verify-time/merge-queue alternatives; fail if it reads as "re-anchor more often."
4. **Watermark mechanics:** SN-853's prescription (fetch last page AND last page − 1, reconcile every ID, advance only over the reconciled set) and the skipped director teaching must survive; fail if reduced to "paginate carefully."
5. **Regen expiry:** SN-821's law must bind regen evidence to the exact merge tip post-merge; fail if in-PR regen evidence is presented as sufficient anywhere.
6. **Standing-authority guard:** SN-904 (proof freshness doctrine) may be pointed to but not restated as covered material; fail if its rule is absorbed into this essence's claims.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.