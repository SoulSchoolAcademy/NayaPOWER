# SN-2181 — One Canon: Collisions, Convergence, and Stale Asks

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 8 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED (verifier-oct-4, against repo bytes). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A shared system constantly manufactures duplicates — of IDs, of files, of documents, of work — and this block records the discipline of keeping exactly one canon without destroying history. Duplicate Smart Note IDs are repaired by renumbering the registry, never by deleting history, and a *skipped* repair is itself a recorded decision (SN-834). Two documents each claiming to be "the single canonical" one is a duplicate mechanism, caught by re-reading the sources before authoring a convergence (SN-898) — and semantic convergence never licenses calling two artifacts "the same" without a byte or provenance check (SN-930). Work that collides mid-flight is finished and transferred, never restarted or duplicated (SN-933); work already done is delta-checked, never re-executed (SN-941); and "canonical" itself is a reconciliation result — main's ledger was wrong about its own decision log until an orphan branch's verified record was cherry-picked forward (SN-864).

## Essence

**Dedup repairs the registry, never history.** When duplicate IDs surface, the repair is renumber-only: delete nothing. The canonical note keeps its ID under the first-claim rule; new numbers must clear three layers before use (main + all open PRs); the sequence counter advances honestly (next_sequence 783→821). The discipline includes its own refusal: the SN-346 R1 tombstone was *not* renumbered (immutable-R1 doctrine; 8 published notes) — a skipped repair recorded as a decision, with its doctrine and its override path, not an oversight. Vanity IDs get the same treatment as collisions: SN-NET-POWER-MAGIC-001 became SN-0820, directory renamed, references updated — and the IB identity, the thing that actually names the artifact, was left untouched (SN-834). The counting side of the same hygiene: an index citation is not doctrine integration. A C5.1 count that treated REAL-TREE.json citations as integration was excluded on audit; the honest rate stood at 59/629 (9.4%), FAIL against a 0.60 bar — and a zero-with-explanation beats an inflated positive every time. Duplicate IDs found during counting (19, e.g. SN-018 ×2) and a vanity ID were flagged, never silently normalized (SN-830).

**Names collide in more places than registries.** Filenames that differ only by case — `ACTIVATION-CHECKLIST.json` vs `activation-checklist.json` — are *the same file* on macOS and Windows filesystems, a collision invisible on the Linux box that authored it. The check is a lowercase-folded `git ls-tree` proven duplicate-free including the base; the flag goes to the owner lane (you don't fix across the boundary uninvited); and the gate belongs in CI, because the authoring environment cannot see its own defect (SN-831).

**Canonical is a reconciliation result, not a branch name.** Main's ledger said DEC-006 / 46 events. The verified record — DEC-007 / 57 events, proven by cold recompute — lived only on a never-PR'd orphan branch. The sweep's rule: cherry-pick the verified commits forward (5766dda22, 84fe6e17); never redo the work, because redoing loses the provenance that made the record worth trusting. The branch a thing lives on confers nothing; verification confers everything (SN-864).

**Before authoring a convergence, check whether the sources already converged.** A seat was asked to open a PR carrying a "single canonical" WORKER-STANDARD.md converging two in-flight documents (#2145, #2149), closing both in its favor once green. Six minutes later a relay flagged the collision: the distilled doctrine already lived on #2145 — the director's 14-question audit verdict (6100080418) had reviewed it at `43595a40`, parented on the live tip, and passed it with the other seat's voice and best lines intact. Two documents each claiming single-canonical status is a duplicate mechanism, and the two would have raced to merge. The relay adjudicated nothing and routed the decision to its owner: fold any real delta into the living document, or close the convergence in #2145's favor. Rule: re-read sources on *current bytes* before drafting — documents move while you draft; if a source already converged in flight, your job is a delta-fold, never a competing canon (SN-898).

**Convergence is not identity.** When a second NayaNET analysis arrived, a seat replied instantly that it was "the same document," "same text" as the Mirror PDF. It wasn't. The two converge substantially — and the second carries distinct contributions the collapse would have destroyed: a Continuous Intelligence Loop framing inside SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE, ten reusable capabilities, and a ranked action list with independent runtime proof of learning as its top action (all candidate recommendations, no implementation evidenced — kept CANDIDATE here). The standing check order runs *before* any sameness claim: (1) byte-identity, (2) provenance, (3) structural comparison — what does each claim that the other doesn't? Only (1) licenses the words "the same." The asymmetry is the reason: falsely claiming difference costs one more comparison; falsely claiming sameness costs the distinct artifact (SN-930).

**When prevention fails, finish and transfer.** A directive routing (65 directives to lane owners) landed while another seat's Wave-2 builders were already in flight on D34/D36 — a dispatch-without-re-observing miss, owned openly by the dispatching seat. The resolution (6103331706): the in-flight builds **finish**; their PRs **transfer** to the assigned owner to verify and own (doer ≠ verifier survives the handoff; the builder claims no ownership credit for a directive it no longer owns); the displaced seat does **not** start a parallel build; and the resolution is posted on the board, not in a side channel, so a cold successor can reconstruct the ownership chain. Prevention (scan the board before executing) is a different note's law; this is the resolution when prevention has already failed — and it explicitly does not apply to work violating a standing law, which is reverted, not finished (SN-933).

**A stale ask gets a delta check, not a second execution.** A cross-seat review ask arrived for PRs #2224/#2225 — already complete: independent reviews had been posted at 19:21 PDT (7.34/10 VERIFY WITH HOLES; 8.00/10 VERIFY), recorded in the durable memory log, acknowledged by three ticks. The ask came from a queue note written at 19:38, before the completion landed in the shared record. The loop's no-duplicates guard fired: no second review. Instead — spot-verify the heads, reproduce the earlier holes, post *supplement* comments with delta findings only (which surfaced two genuinely new findings: #2225's CI red-by-construction index drift, #2224's false "ENFORCED" claim on a workflow that only runs its own tests). Every incoming ask is a *claim that work is pending*; the completion check runs in order — durable memory log → board record → pin-exact bytes — and only a failed check licenses execution. Re-doing delivered work is doubly expensive: it spends the budget and corrupts the evidence record with duplicate receipts (SN-941).

## What this settles

- Dedup = renumber the registry, delete nothing; canonical keeps its ID by first-claim; new numbers clear main + all open PRs; a skipped repair is a recorded decision with doctrine (SN-834).
- Citations are not integration; honest zeros beat inflated positives; duplicate and vanity IDs are flagged, never normalized (SN-830).
- Case-only filename differences are collisions on case-insensitive filesystems; check is lowercase-folded `ls-tree` incl. base; gate belongs in CI (SN-831).
- Canonical = verified reconciliation, wherever it lives; cherry-pick verified commits forward, never redo (SN-864).
- Re-read sources on current bytes before authoring any convergence; a converged source gets a delta-fold, not a competitor (SN-898).
- Sameness requires byte-identity (or a verified provenance chain); convergence licenses "converges with" + a list of distinct contributions (SN-930).
- Mid-flight collisions resolve finish → transfer → no parallel build → board-posted resolution; the dispatcher owns the miss (SN-933).
- Incoming asks are claims of pending work; verify (memory → board → bytes) and post deltas only when complete (SN-941).

## Human

A busy team is a machine for making two of everything: two notes with one number, two documents both calling themselves *the* standard, two people fixing the same thing, two requests for work already done. Keeping one canon isn't tidiness — it's what makes the record readable by the next person. These notes share a temperament: slow down at the moment of duplication, check what's actually true (bytes, provenance, the board), and resolve the collision in the open — renumbering instead of deleting, folding instead of competing, transferring instead of restarting, and answering a stale request with what changed instead of doing the work twice.

## Child

Imagine the class makes two birthday posters for the same party, and both say "THE poster." You don't throw one away or hang both and confuse everyone. You check: are they really the same poster? (Hold them side by side.) If a friend already finished the poster, you don't make a third — you look at theirs and add only what's missing. And if two toys have the same name tag, you change one tag — you never throw a toy away just to fix the tags.

## Grandma

It's the family Bible problem, dear: three copies, two with the same pages numbered differently, one with grandmother's notes in the margins. You don't burn any of them. You check which is the true record — sometimes it's the copy in the attic, not the one on the shelf — you renumber carefully, you write down what you did and why, and you never, ever pretend two different books are the same book just because their covers match.

## Naya

On any duplicate ID: renumber, never delete; clear new numbers across main + open PRs; record skipped repairs as decisions (SN-834). Count integration from substance, not citations; flag duplicates instead of normalizing them (SN-830). Fold filenames to lowercase in the tree check, base included (SN-831). Treat "canonical" as a verdict to earn by recompute; cherry-pick verified orphan work forward (SN-864). Before drafting any convergence, re-read the sources at their current tips; delta-fold or stand down (SN-898). Before any sameness claim, run byte-identity → provenance → structural comparison, in that order (SN-930). On a mid-flight collision: finish, transfer to the assigned owner for verification, forbid parallel builds, post the resolution on the board (SN-933). On any incoming ask: run the completion check before executing; deliver deltas, not duplicates (SN-941).

## What It All Means

The eight notes are one conservation law: **the system's memory must contain each thing once, under one name, with its history intact.** Every mechanism here protects a different face of that law — registry (SN-834), counting (SN-830), filenames (SN-831), truth-location (SN-864), documents (SN-898, SN-930), in-flight work (SN-933), and the work queue itself (SN-941). The failures they prevent are also one failure: a second copy quietly becoming a second truth, after which no one can say which record the next decision should trust.

## Why It Matters

Duplicates don't merely waste storage; they fork reality. Two canonical documents produce two compliant-but-different behaviors; a redone record loses the provenance that made it evidence; a duplicated review doubles receipts and muddies every later scorecard; a normalized-away duplicate ID hides the collision that the next numbering decision needed to know about. For the reader: this is the discipline that keeps a growing shared memory *singular* — the precondition for every other essence in this campaign being findable, citable, and true.

## How It Connects

The no-duplicate-mechanisms law these notes apply is standing doctrine for the whole build (see AGENTS.md conventions); the numbering census discipline has its own custom skill in the maker's wider system. SN-864's provenance-preservation is the branch form of essence-bounded-claims.md's memory law (SN-914: preserve history, recompute qualification). SN-930 pairs with the freshness family (essence-evidence-expires.md): temporal identity there, categorical identity here. The No-Ego Merge — the director's doctrine for resolving duplicate *work products* by cross-scoring — stands alone as SN-920; SN-933 is its collision-time protocol companion, and the doctrine itself is pointed to, not absorbed.

## What Is In It For You

You get collision reflexes that save real money in any shared workspace: check before you converge, compare before you call things the same, transfer before you restart, and verify before you redo. Each reflex replaces an expensive default (a competing document, a lost contribution, a doubled work order) with a cheap question asked at the right moment. And when you must repair a duplicate, you get the ethical shape of the repair: change the label, keep the history, write down the decision.

## The Learning

The block's collisions taught that duplication is rarely carelessness — it's *asynchrony*: documents converge while you draft, completions land while the ask is in flight, routings arrive while builders are mid-build. The learning that compounded is therefore temporal, not moral: re-observe at the moment of action (the board, the bytes, the queue), because the collision you prevent is the one that formed in the last six minutes. The second learning is asymmetry-awareness: several rules here exist because one direction of error is cheap and the other destroys something irreplaceable.

## Coverage map — raw notes this essence covers (8)

SN-830 · SN-831 · SN-834 · SN-864 · SN-898 · SN-930 · SN-933 · SN-941

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 8 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **History preserved:** SN-834 must keep renumber-only + delete-nothing + the SN-346 skipped-repair-as-decision; fail if the essence presents the tombstone as an oversight or recommends deletion anywhere.
3. **Check order exact:** SN-930's order (byte-identity → provenance → structural comparison) must appear in sequence, with the false-sameness asymmetry; fail if reordered or if "converges substantially" is treated as sameness anywhere.
4. **Finish-and-transfer limits:** SN-933 must keep all five protocol parts *and* its non-claim (work violating standing law is reverted, not finished); fail if either is dropped.
5. **Candidate status kept:** the second analysis's contributions (SN-930) must remain candidate recommendations with no implementation claimed; fail on any inflation.
6. **Standing-authority guard:** SN-920 (No-Ego Merge) may be pointed to but not absorbed; fail if its cross-scoring doctrine is restated as covered material.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.