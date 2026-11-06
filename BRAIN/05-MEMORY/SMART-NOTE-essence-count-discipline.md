# SN-2112 — The Discipline of the Count: Merges, Indexes, and the Moving Baseline

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-1).** Distilled from 8 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Verified without correction. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A generated index is a claim about the tree, and it drifts the moment the tree moves — so pins are read as intent, not accident (SN-038), and the count ledger travels with the change that moves the count: regenerate the index and deliberately bump the ledger in the same merge (SN-062, SN-078). Merge claims are audited against the reconciled base, and no reconciliation artifact means no reconciliation claim (SN-039, SN-040). Caveats carry expiry triggers (SN-041), replaced diagnoses are declared SUPERSEDED in public (SN-042), and expected values are recomputed at the merge tip — correct-at-base is not sufficient-at-tip (SN-0128).

## Essence

A generated index is a claim about the tree, and like every claim it drifts the moment the tree moves. The first law of the count: **regeneration encodes intent, not accident** — when a deliberate pin (an expected domain count) disagrees with both main and the branch tree, the disagreement is diagnosed against what was deliberately added and removed, never resolved by blindly regenerating to whatever the tree happens to hold (SN-038). Its operational twin: the count ledger is part of the change — any merge that adds files under a counted domain must regenerate the index AND deliberately bump the count ledger in the same motion, baked into merge checklists, because a green test suite beside a red index check on main itself is what happens when the ledger is treated as someone else's job (SN-062, SN-078).

Merges carry their own failure geometry. A merge decision is audited against the **reconciled base**, not just the source: a carry-forward can be faithful in almost every particular and still adopt, in one document, a framework the base never held — the audit reads the merge against what the base actually was (SN-039). No reconciliation artifact, no reconciliation claim: when a merge document asserts its base was "red-teamed and fully reconciled," the artifact of that reconciliation must exist and be checkable, or the claim does not ship (SN-040). Caveats inside merge documents decay: a condition written when the calculus was CANDIDATE keeps gating after the state changes, so every caveat must carry its expiry trigger — the event that retires it — or it becomes a stale gate nobody remembers imposing (SN-041). And when new evidence replaces a diagnosis, the old one is declared SUPERSEDED explicitly, on the board, with the evidence — a silently corrected premise leaves every other lane acting on the stale version (SN-042).

The baseline moves under repairs, too: a repair PR provably correct against its base can still be insufficient at the merge tip, because main advanced while it was being built — so the expected value is recomputed at the actual merge tip before merging a drift repair, and the residual delta gets a parked one-commit follow-up rather than a surprise red gate after landing (SN-0128). Correct-at-base ≠ sufficient-at-tip (SN-0128).

## What this settles

- A count pin is a deliberate claim; drift is diagnosed against intent (what was added/removed on purpose), never absorbed by blind regeneration (SN-038).
- Index regeneration + ledger bump travel with the change that moves the count — same merge, same checklist (SN-062, SN-078).
- Merge claims are audited against the reconciled base; reconciliation claims require reconciliation artifacts (SN-039, SN-040).
- Every caveat carries an expiry trigger or it is a defect in waiting (SN-041); every replaced diagnosis is declared SUPERSEDED in public, with evidence (SN-042).
- Expected values are recomputed at the merge tip, not the PR base, before a drift repair lands (SN-0128).

## Human

Keeping score sounds trivial until many people change the thing being counted at once. These rules keep the scoreboard honest: the expected numbers are deliberate, not accidental; whoever changes the count updates the scoreboard in the same move; claims about how a merge was checked need the paperwork to prove it; warnings carry their own expiry dates; and before any fix lands, you re-check the target as it stands *now*, not as it stood when you started.

## Child

Imagine the class keeps a chart of how many books are in the library. If someone adds a book, they update the chart the same day — that's part of adding a book. If a note on the chart says "careful, this shelf is wobbly," it also says when to take the note down. And if you count the books to check the chart, you count them today, not from last week's number.

## Grandma

Dear, it's good housekeeping for shared records. The ledger and the shelves must agree, and the person who changes the shelves updates the ledger. Claims about what was checked need the receipts. Old warnings get taken down when they're no longer true — announced, not just quietly removed. And you always count what's actually there now.

## Naya

Treat every pin as intent: diagnose drift by enumerating the deliberate deltas before touching the generator (SN-038). Ship index regen + count-ledger bump inside the same PR that moves a counted domain (SN-062, SN-078). Audit merges against the reconciled base (SN-039); refuse reconciliation claims without artifacts (SN-040); attach an expiry trigger to every caveat you write (SN-041); declare supersessions on the board with the evidence attached (SN-042). Before merging any drift repair, recompute the expected value at the live tip and park the residual as a named follow-up (SN-0128).

## What It All Means

Eight notes govern the unglamorous machinery that keeps a fast-moving shared tree countable: pins as intent, ledgers as part of the change, merges audited against their true bases, caveats with lifetimes, and tips re-measured at landing. A cold reader holding only this essence can still keep the count honest — which is all these notes exist to teach.

## Why It Matters

Counts are how the system knows its own size — and how a director knows whether "the corpus" is 1,100 notes or 100 essences. A drifted index doesn't just fail a check; it makes every downstream number a rumor, including the numbers the distillation campaign itself is retiring against (SN-038, SN-078). For the reader: any total you are quoted is worth exactly the discipline behind it, and this essence is that discipline.

## How It Connects

The count presumes the canon of essence-one-canon.md — an index of a forked tree counts nothing meaningful — and its supersession rule (SN-042) is the merge-scale form of the forgetting discipline in essence-continuity.md (SN-009). Its artifact rule (SN-040) is a scoped sibling of the evidence law in essence-evidence-law.md (SN-020): there, claims need evidence; here, merge-document status claims need reconciliation artifacts specifically. The stale-caveat decay it names (SN-041) is the defect that self-invalidating tests in essence-composition.md (SN-092) were later designed to defeat by construction.

## What Is In It For You

You can trust the totals. When this system tells you a count — files, notes, tests — the count was maintained as part of the work, audited against intent, and re-measured at the moment it mattered. Apply the same discipline to any shared inventory you keep: the ledger update is part of the change, warnings carry expiry dates, and "correct when I started" is never the same as "correct when it lands."

## The Learning

The corpus learned that bookkeeping is not overhead on the work — it is part of the work's definition of done (SN-062, SN-078), and that a correct repair aimed at a stale baseline is a future red gate scheduled in advance (SN-0128). Both lessons now run mechanically: merge checklists carry the ledger, and drift repairs recompute at the tip before landing.

## Coverage map — raw notes this essence covers (8)

SN-038 · SN-039 · SN-040 · SN-041 · SN-042 · SN-062 · SN-078 · SN-0128

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 8 IDs, all in the sep-1 block list, none duplicated elsewhere in this block's accounting.
2. **Intent case:** SN-038's pin case (deliberate pin 27 vs main 28 vs branch tree 36, resolved by enumerating deliberate additions/removals) — fail if the essence prescribes regenerating to match the tree without the intent audit.
3. **Same-motion rule:** SN-062 and SN-078 both require regen + ledger bump with the change; fail if the essence makes either optional or a follow-up task by default.
4. **Artifact rule:** SN-040's rule is about *status claims in merge documents* lacking artifacts; fail if the essence broadens it into a general "no claim without artifact" that duplicates the evidence-law essence's SN-020 rule without distinction.
5. **Expiry trigger:** SN-041 requires the caveat itself to carry the trigger; fail if the essence substitutes periodic review for the carried trigger.
6. **Tip recompute:** SN-0128's numbers (base-correct fix; tip moved; gate red by exactly the delta) — fail if the essence states correctness at base is sufficient, or omits the parked follow-up.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.