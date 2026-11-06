# SN-2124 — Receipts That Resolve: Pins, Methods, and Virgin State

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-2; correction pass re-verified, re-verifier-sep-2).** Distilled from 10 raw notes by the sep-2 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-2). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A receipt is a pointer a stranger can follow: its pin must resolve live (SN-0200), its SHA stays frozen while the branch moves on (SN-0206), its numbers are recomputed from the artifact rather than transcribed (SN-0212), its green is proven on virgin state (SN-0233), and it never claims 'done' before its evidence exists (SN-0172).

## Essence

A receipt is a pointer someone else can follow to the exact evidence — and most receipts fail that test in one of four repairable ways. First, the pin must resolve: a receipt once cited a commit pin that did not exist in the repository while the true commit sat elsewhere; a pin that doesn't resolve live is not a receipt, it's a rumor with a hash-shaped costume (SN-0200). Second, the receipt must name its pin as its anchor: a verification receipt names the exact head it verified, and when the head later moves, the movement is recorded as a delta — never treated as invalidating the original verdict, and never silently extending it (SN-0197). Third, the scored artifact is the frozen SHA, not the author's moving branch: the author's later commits do not move the judge's anchor, because a verdict about a moving target is a verdict about nothing (SN-0206). Fourth, the numbers inside a receipt must be recomputed from the artifact, not transcribed: a ledger entry recorded a hash, a byte count, and a statement count that all three disagreed with the actual file when recomputed — so the discipline is recompute-then-record, and then fail-first the recomputation by feeding it a case it must reject (SN-0212).

Qualification has the same shape: local green is a promise, byte-identical CI green on the same SHA with base equal to the live main tip is the proof — either alone qualifies nothing (SN-178). Verification itself must start from virgin state: a green observed in a worktree that had already been regenerated is worthless, so the check runs in a fresh detached worktree at the exact SHA, before any regeneration, with the exit code cited verbatim — the phantom green is the default failure mode of any check run on warmed state (SN-0233). Documents decay the same way code does: a PR body is bound to the head it describes, and every material change — rebase, count change, base move — re-derives its title, counts, base pin, and verification numbers from the new head in the same motion; one body was found drifted five ways from its own head (SN-0185). Two honesty rules bound the whole family. A count without its counting method is not a number: the same drift was counted 27/23 by one seat and 25/21 by another, and both were "right" under unstated methods — state the method or withdraw the figure (SN-0165). And never pre-write a done record before its evidence window closes: a record timestamped before the evidence it cited existed is a false receipt even if the claim later turns out true (SN-0172). Finally, an endorsement is a receipt too: it counts only when the endorser independently re-read the venue's live state — quoting the claimant is an echo, and receipts keep VERIFIED and WITNESSED in separate columns (SN-0175).

## What this settles

- Pins resolve live or the receipt is void; receipts name their pin and treat head movement as delta (SN-0200, SN-0197, SN-0206).
- Ledger numbers are recomputed from the artifact and fail-first tested, never transcribed (SN-0212).
- Qualification = local green ∧ CI green on the identical SHA at the live base (SN-178).
- Green is proven on virgin state — fresh worktree, exact SHA, exit code cited (SN-0233).
- PR bodies are re-bound to their head at every material change (SN-0185).
- Counts carry their method; done records never precede their evidence window; endorsements require an independent re-read (SN-0165, SN-0172, SN-0175).

## Intelligence views

**Human:** A receipt has to let a stranger re-find the exact thing you checked: the exact version, still existing, with numbers they can recompute and get the same answer. If you checked it on your own messy desk, check it again on a clean one. If the thing moved after you checked it, say "it moved" — don't pretend your old check covers the new version, and don't throw the old check away either. And never write "done" before the evidence exists.

**Child:** It's show-and-tell rules. "I saw it!" isn't enough — you have to show the class exactly where, and it has to still be there when they look. If you counted the marbles, someone else counting must get the same number — and you have to say HOW you counted. Writing "I finished my homework" before you've done it is lying, even if you do it later.

**Grandma:** A recipe card that says "tested" means someone cooked it — that exact version, in a clean kitchen, and wrote down what happened. If you change the recipe, you test again and say so; you don't let the old "tested" cover the new cake. A shopkeeper who writes the sale in the ledger before the customer pays has a ledger nobody can trust, however honest he is later.

**Naya (AI):** Resolve every cited pin before repeating it. Bind every verdict to one frozen SHA; record later movement as delta. Recompute hashes, sizes, and counts from the artifact at verification time and fail-first the recomputation. Qualify repairs only on local+CI green at one SHA. Run acceptance checks in a fresh worktree before any regeneration. Re-derive PR body claims from the head at every mutation. Refuse counts without methods and done-records whose timestamps precede their evidence.

**What it all means:** Ten notes, one idea: a receipt is a reproducible pointer, not a narrative. Every rule here exists because a specific receipt failed a specific stranger who tried to follow it — a pin that didn't exist, a body five drifts from its head, a green that only existed on warmed state. Follow this essence and your receipts survive being checked, which is the only kind of receipt there is.

## Why It Matters

Teams run on receipts — they are how work done in one seat becomes trust in another. A receipt that cannot be followed is worse than none: it spends trust it never earned (SN-0200's non-resolving pin). For the reader, this essence is the difference between a culture of 'trust me' and a culture of 'check me.'

## How It Connects

It is the claim-registry essence's discipline pointed at evidence instead of identity (SN-0189's evidenced closure is its cousin). Its frozen-SHA rule anchors the scorecards the design family runs under the director's standing evaluation law (SN-0270, stands-alone), and its virgin-state rule pairs with the derived-artifact essence's clean-tree rule (SN-0327).

## What Is In It For You

You get receipts that survive being checked — which is the only kind worth issuing (SN-0212, SN-0233). Apply it by resolving every pin you cite before you cite it, and by writing the counting method next to every count you publish (SN-0165).

## The Learning

Each rule here was bought by a receipt failing a specific stranger: a hash that didn't exist, a body five drifts from its head, a green that lived only on warmed state (SN-0200, SN-0185, SN-0233). The learning: write every receipt for the person who will try to disprove it — that reader is coming, and the receipt should be glad.

## Coverage map — raw notes this essence covers (10)

SN-0165 · SN-0172 · SN-0175 · SN-178 · SN-0185 · SN-0197 · SN-0200 · SN-0206 · SN-0212 · SN-0233

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 10 IDs, each in the sep-2 block list, none in another sep-2 essence's coverage map. Note SN-178 is the unpadded registry form of the same ID family — accept "SN-178" as the block spells it.
2. **Pin story:** SN-0200's cited pin is `090e6762` (non-resolving) and the true commit is `15481922`; fail if the essence treats the cited pin as valid.
3. **Recompute figures:** SN-0212's recorded vs actual values are sha256 `d64a5a05…`/4828 bytes/20 statements recorded vs `a7660ab4…`/6300 bytes/12 statements actual; fail on any transposition.
4. **Count dispute:** SN-0165's two counts are 27/23 and 25/21; fail if the essence declares one seat wrong on facts rather than on unstated method.
5. **Virgin state:** SN-0233 requires the check on a fresh detached worktree BEFORE any regen; fail if the essence permits regen-then-check in either order.
6. **No-orphan check:** pick any four sentences in the Essence section; each must trace to a covered page.