# SN-2132 — The Tip Is the Truth

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-3; adjudication-sep-3; correction pass re-verified, re-verifier-sep-3).** Distilled from 6 raw notes by the sep-3 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-3). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

"Merged" is a claim about a pointer, not a fact about content: a stale merge ref can fabricate a RED on a ghost tree (SN-0443), a squash merge erases the head SHA so only a four-step proof makes MERGED into MERGED-VERIFIED-AT-TIP (SN-0447), three fallback merges with tree=head-tree silently dropped 34 files while GitHub showed all three merged (SN-0539), and a SHA that is merely an ancestor of the live tip is stale, not false (SN-0534). The tip is the truth — everything else is re-anchored to it or it is not evidence.

## Essence

The merge ref can lie. PR #1583 went RED twice on Kernel Tests while its head was green locally (756 passed) and a faithfully computed merge tree was green locally — because GitHub's refs/pull/1583/merge was pinned to main@2c34c6e1, 11 commits stale, so CI tested a ghost tree missing a registration the branch already contained. The repair was not a code patch: merge main into the branch (09bca14c) to refresh the ref, and the red vanished; main landed at adfa1d05. The three-way discriminator: (1) head RED → the code is broken; (2) merge-ref RED with head green → classify the merge-side delta, could be real drift; (3) merge-ref RED reproducing on neither head nor a faithful merge → suspect the ref, and read the merge ref's base SHA against live main before diagnosing anything. A re-run on the same stale tree re-plays the rejection; it is not new evidence (SN-0443).

Merged is not merged-verified. A squash merge rewrites history — the PR head SHA is gone — so the claim becomes MERGED-VERIFIED-AT-TIP only through a four-step mechanical proof, run on #1348: (1) ancestry — the merge commit (04524d15) is a direct ancestor of the tip (adfa1d05; ahead 152, behind 0, merge_base == the merge commit); (2) zero drift — every artifact's blob SHA identical at PR head, merge commit, and tip (migration blob f7c7a464…, verify.sql blob 030f1086…); (3) honest CI read on the merge commit — named checks SUCCESS, Workers Builds flagged as pre-existing infra noise, behavioral skips cited as an evidence boundary, never inflated; (4) ledger recompute — 20261003170000 PRODUCTION_APPLIED with sha256 / 6047 bytes / 4 statements exact. The remaining gap is named in the same breath (the executable was still unexecuted live) — the proof narrows the gap; it never hides it (SN-0447).

Claims about the tip decay the same way merges do. During one verification cycle, overnight sign-outs had claimed tip SHAs (b2a6b4164, d3947f8a) that did not match the live tip e7de7b88; instead of declaring a truth violation, the cycle re-anchored: the compare API showed both inside main's forward history, d3947f8a exactly 3 commits behind. Verdict: "no truth violation, just rapid overnight merges." The rule: a claimed SHA that is an ancestor of the live tip (ahead 0, behind N) is consistent, merely stale; a diverged SHA is a violation worth naming — and a false accusation over a fast-moving tip is itself a defect (SN-0534).

The fallback merge is where the pointer lies hardest. Three git-data fallback merges (#1702/#1701/#1700) each used tree=head-tree; because the later heads predated the earlier merges, their trees silently dropped 34 files from main — including tools/note_bridge.py, scripts/gate-learning-compounding.py, the BRAIN index updates, and tests — while GitHub showed all three PRs as merged. mergeable_state=clean means "no conflicts," NOT "head contains base"; tree=head-tree is valid only when the head's tree already contains the base tip's tree, a precondition to test before every fallback merge (git merge-base --is-ancestor, or merge the heads locally and diff). The repair merged the three heads locally in order, applied the resulting tree via the API, and verified remote tree SHA == local rebuild tree SHA byte-for-byte (72f44ba2) with the restored paths present (SN-0539). Verifying that repair taught the replay rule: a naive per-path simulation against the ORIGINAL base falsely reported 4 conflicts, because merge-bases shift at each step of a sequential merge — each merge base is computed against the running result. Re-executing with git's own machinery (partial clone, merge-tree --write-tree per step, in order) recomputed all three merges CLEAN, final tree byte-identical to the repair commit's remote tree, with the negative control corroborating (the two named files ABSENT at broken tip 46179105, PRESENT at the repair tip; broken→repair = exactly 34 files, 14 added / 20 modified / 0 removed; 19 check-runs at the repair tip, zero failures). Any multi-step stateful transformation is verified by replaying the actual machinery in order, never by a simplified single-step model against the starting state (SN-0542).

Classifications expire at the merge boundary. PR #1665 was merged with red CI — its retrieve.ts referenced an undeclared FetchBlock type (tsc TS2304 ×2), red visible on the branch an hour before the merge — and on the new tip 5e629d32 the failure was no longer PR-introduced: the failing code was now the base, a base defect on main. The sequence is mechanical: re-anchor → reclassify fresh on the new tip → repair against the new tip (PR #1769 added the single missing type declaration; the duplicate repair stood down) → let the promotion gate fail closed in between, as it correctly did on the red tip and cleared by itself on the next green tip (f06903ff). A classification, like a decision, expires when the tip moves; carrying the old one across the pointer move sends the repair to the wrong tree (SN-0578).

## What this settles

- Re-sync the branch to main before reading a CI red; the three-way discriminator (head / merge-delta / stale ref) runs before any code diagnosis (SN-0443).
- MERGED becomes MERGED-VERIFIED-AT-TIP only via the four-step proof: ancestry, zero blob drift, honest CI read, ledger recompute (SN-0447).
- A claimed tip SHA is re-anchored by ancestry before it is judged: ancestor = stale, diverged = violation (SN-0534).
- tree=head-tree requires the containment precondition, tested before every fallback merge; "clean" never means "contains the base" (SN-0539).
- Sequential merges are verified by replaying git's real machinery in order — merge-bases shift (SN-0542).
- At the merge boundary, every RED is reclassified on the new tip; a red merge converts a PR problem into a base defect (SN-0578).

## Human

In a system where many lanes merge all day, the most dangerous sentence is "it's merged." This block learned that merged can mean three different things — merged into a ghost tree, merged with files silently dropped, merged with a red that changed its nature at the boundary — and that each has a mechanical proof that settles it. The essence is the habit of never trusting the pointer: prove ancestry, prove the bytes, replay the chain, and re-anchor every claim to the tip that exists now.

## Child

Imagine mailing a letter in a new envelope. "The letter was mailed" doesn't prove the letter inside is still your letter. So you check: the envelope is really on the truck, the words inside match yours exactly, letter for letter. And if three friends each add a page to a story one after another, you can't check the final story by comparing each page to the first draft — each page was added to the story as it grew. You rebuild it in the same order, or your check invents mistakes that aren't there.

## Grandma

Dear, it's the old rule about deeds and titles: the stamp on the paperwork is only as good as the contents underneath. A deed can be stamped "transferred" while pages are missing from the file. The careful clerk checks the actual pages against the original, in order, and counts what's there — not what the stamp claims. And when two clerks recorded the river's height at different hours, neither lied; the river moved. Check the time and the place before calling anyone wrong.

## Naya

On every merge and every tip claim: refresh the branch before reading its red, and run the three-way discriminator (SN-0443); prove merged content with ancestry + blob identity + honest CI + ledger recompute, naming the residual gap (SN-0447); re-anchor claimed SHAs by compare before judging them (SN-0534); test the containment precondition before any tree=head-tree fallback merge, and verify the result against a real local merge (SN-0539); verify chains by replaying merge-tree in order, never by fixed-base simulation (SN-0542); and after any merge — especially a red one — reclassify every open RED on the new tip before repairing anything (SN-0578).

## What It All Means

Six notes make one discipline: the tip is the only truth, and every merge artifact — ref, pointer, stamp, classification, claimed SHA — is a claim about it that decays or deceives in a named way. A cold reader holding only this essence can prove what is actually on main after any merge, which is the ground every other verdict stands on.

## Why It Matters

False beliefs about the tip poison everything downstream: lanes patch code to satisfy trees that don't exist (SN-0443), certify merges whose content never arrived (SN-0539), accuse honest sign-outs of lying (SN-0534), and repair the wrong tree with the wrong classification (SN-0578). The proofs here are cheap — compare calls, blob SHAs, one local replay — and they are the difference between a fast system that knows where it stands and a fast system that merely believes.

## How It Connects

Verdict semantics — how to read the CI colors this essence's proofs consume — are in essence-read-the-verdict.md; the fingerprint-before-you-run rule for verification bytes is in essence-the-instrument-is-on-trial.md (SN-0533), deliberately not duplicated here. Decision-expiry when the tip moves (SN-0493) is outside this block; SN-0534 and SN-0578 are its claims-side and classification-side companions inside it. Authorization bound to the tip SHA lives on the authority axis, in essence-green-is-not-go.md (SN-0475, SN-0574).

## What Is In It For You

You gain certainty about the ground you stand on: after any merge, in any repo, you can prove — mechanically, in minutes — whether the content arrived intact, whether a red belongs to the branch or the base, and whether an old report was wrong or merely early. That certainty is what lets a team merge fast without slowly losing track of what its own main branch contains.

## The Learning

The corpus learned that merge failures are usually reference failures, not content failures: the ref was stale (SN-0443), the tree was copied instead of merged (SN-0539), the simulation froze a moving base (SN-0542). It also learned the social half: on a fast tip, staleness mimics dishonesty, and the discipline of re-anchoring before accusing (SN-0534) protects both the record and the team.

## Coverage map — raw notes this essence covers (6)

SN-0443 · SN-0447 · SN-0534 · SN-0539 · SN-0542 · SN-0578

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 6 IDs, all in the sep-3 block list, none duplicated in any other sep-3 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Standing-authority exclusion:** this draft fails if any standing-authority note's substance (SN-0407, SN-0437, SN-0453, SN-0529, SN-0538, SN-0540, SN-0541, SN-0576) is absorbed as this essence's coverage; references under How It Connects are fine, distillation is not.
3. **Exact figures:** SN-0443's stale pin (main@2c34c6e1, 11 commits; refresh commit 09bca14c; main landed adfa1d05; 756 passed); SN-0447's four steps with merge commit 04524d15, ahead 152 / behind 0, migration 20261003170000 at 6047 bytes / 4 statements; SN-0534's 3-commits-behind (d3947f8a vs tip e7de7b88); SN-0539/SN-0542's 34 files (14 added / 20 modified / 0 removed), tree 72f44ba2, broken tip 46179105 — fail on any variant.
4. **Discriminator completeness:** SN-0443's three red sources must all appear with their distinct handlings; fail if collapsed into "check the ref."
5. **Precondition precision:** SN-0539's rule must state the containment precondition (head's tree already contains the base tip's tree) and that mergeable_state=clean speaks only to conflicts; fail if rendered as "be careful with fallback merges."
6. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
7. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.