# SN-2184 — Bounded Claims: Never More Certain Than the Evidence

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 6 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED (verifier-oct-4, against repo bytes). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Claims decay as they travel — summaries compress their boundaries away, caches outlive their evidence, corrections inherit the carelessness of what they correct. This block's counter-discipline is a family of four registered directives (D32–D35) and the working rules around them: uncertainty travels only along true evidence dependencies, never amplifying (SN-912); when evidence is revoked, recompute dependents and keep what still stands (the correction law, carried by Batch 1 and pointed to below); history is preserved while qualification is recomputed and stale authority invalidated at use time (SN-914); and no cached qualification may be republished until its evidence dependencies are re-validated at that moment (SN-922). Around the directives sit the two working habits that make them real: correct the derived report, never the raw capture — and name what you cannot measure (SN-893); and verify the temporal evidence before publishing a correction, because a correction is a claim too (SN-881) — plus the writing law that every summary carries its non-claims (SN-928).

## Essence

**The anti-cascade law (D32).** Uncertainty can only travel along *true* evidence dependencies. A downstream claim can never become more certain, broader, or more causally specific than its evidence supports — confidence is conserved: it flows downstream diluted, never amplified. The working procedure: for each conclusion, name the exact evidence it depends on; check the dependency is true (not assumed, not inherited from a stale cache, not borrowed from a sibling claim); confirm certainty ≤ evidence certainty, scope ≤ evidence scope, causal specificity ≤ what the evidence establishes (CORRELATES_WITH ≠ CAUSED_BY). Any amplification across a propagation step is a defect — stop, re-derive, cite the bound explicitly. And propagate the uncertainty *with* the claim: never strip the hedges when summarizing, receipting, or packaging for a successor (SN-912).

**The memory law (D34).** Memory has four verbs and they are not the same verb: **preserve history, recompute qualification, invalidate stale authority, refresh only what changed.** The two classic failures are forbidden: deleting history to "fix" it (the record of what was believed, and why, is itself evidence — retired rows are marked retired, labeled unauthorized where applicable, and preserved; in the founding record, four rows were kept, barred from use, history intact), and letting a cached qualification keep its authority after its evidence expired (a qualification is a lease, not a deed — authority is re-checked at use time). The concrete finding that makes it real: `build_successor_package()` fills `eligible_independent_evidence` from all support-set refs *without* filtering for current eligibility or independence — a specification-level gap where the cache silently outruns the qualification. Its status is kept exact: a specification-level observation routed for repair-lane review, **not** proof of a production mistake. The smell is generalizable: any field named `eligible_*` must actually filter for current eligibility at fill time (SN-914).

**No stale qualification republished (D35).** No cached artifact, worker, or successor may publish or reuse a qualification unless its evidence dependencies are valid *at that exact moment*. A qualification whose evidence moved is not "probably fine" — it is unpublished until re-validated; cached qualifications are guilty until proven innocent. The note keeps its own gap honest: version stamps exist, but nothing yet guarantees that a revocation and a publication cannot interleave — the atomic-publication boundary (transactional compare-and-swap, fencing tokens, adversarial race tests interleaving revocation and publication and demanding exactly one winner) is machinery **to be built**, and wiring changes need the director's word, which had not been given at capture. Until then, every lane publishing qualifications checks evidence validity at the moment of use (SN-922).

**The correction law, pointed to.** When evidence is revoked: revoke its contribution, recompute every dependent conclusion from the remaining evidence (re-derive, never patch), and preserve every conclusion that remains independently sufficient — deletion is not correction. Its red-main corollary: nothing unrelated merges into a failing main. That law (D33) is SN-913, whose teaching Batch 1's SN-2068 carries verbatim — it is therefore covered-by-batch1, and this essence points to it rather than absorbing or double-counting it. It interlocks here: D32 bounds what recomputed claims may say (SN-912), D34 governs the cache the recomputation runs over (SN-914), D35 gates republication of the result (SN-922).

**Correct the derived, never the raw — and name the gap.** A measurement instrument keeps two layers: the raw capture (JSON, snapshots, event dumps), which is immutable evidence, never edited after collection; and the derived report, which is corrected freely — with every correction noted and dated. The founding run corrected a median formatted as "0.0 hours" (true value 0.039h = 2.4 minutes) and a single service account mislabeled "lanes" in the *report*; the raw JSON stayed untouched, and the instrument itself was then fixed and unit-tested. The second half is the honesty half: the same report's honest-gaps section names what the meter cannot measure — token/compute spend per decision, for which no data source exists — and refuses to fake it: "We did not fake it." An invented proxy teaches false confidence; a named gap teaches the truth about the instrument (SN-893).

**A correction is a claim too.** In the same direct-push window that essence-breach-discipline.md dispositions, a seat published a correction of another seat's account — issued on an unverified temporal claim, and retracted six minutes later when the `created_at` chain was actually read. The rule: verify the temporal evidence (the created_at chain, the ordering the correction depends on) *before* publishing; an unverified correction is not a repair but a second falsehood, and it propagates with the authority of the word "correction" attached (SN-881).

**Summaries carry their non-claims.** The D32 audit's core finding: scorecards bound their claims; summaries compress boundaries away. The standing writing law installed from it: every summary, digest, carry-forward, or handoff carries a **"What this does NOT claim"** section, inherited from the source scorecards — what was measured vs assumed, what scope the evidence covered, what counting rule produced the numbers. No exceptions. The audit proved the law's necessity by violating it: its own counts floated (59/60/65 with no shared counting rule; the register is 65 directives, D1–D65, named scopes only) and its "4 draft PRs" was ~8 minutes stale at write time (a PR #2213 it hadn't re-anchored on). Corollaries: every count ships with its counting rule; every number is re-anchored against its source at write time; the auditor is not exempt from the audit (SN-928).

## What this settles

- Downstream claims never exceed their evidence in certainty, scope, or causal specificity; hedges travel with the claim (SN-912, D32).
- History is append-only; qualification is recomputed on material change; stale authority is invalidated at use time; refresh touches only what changed (SN-914, D34).
- Republication requires publication-time re-validation of evidence dependencies; the atomic publication boundary is named, unbuilt machinery — a gap, not a detail (SN-922, D35).
- On revocation: recompute dependents, preserve the independently sufficient (SN-913, D33 — covered by Batch 1's SN-2068; pointed to, not double-counted).
- Raw captures are immutable; derived reports are corrected with noted, dated corrections; unmeasurable quantities are named as gaps, never proxied (SN-893).
- Corrections are verified against temporal evidence before publication (SN-881).
- Every summary carries a "What this does NOT claim" section and its counting rule (SN-928).

## Human

This is the system's etiquette for secondhand truth. Most of what anyone "knows" arrived through a chain — a measurement became a report, a report became a summary, a summary became a decision. Each link in that chain is a place where the claim can quietly grow: a little surer, a little broader, a little more causal than the evidence ever was. These notes install the opposite pressure at every link: claims may only shrink to fit their evidence, history may not be edited to make the chain look cleaner, and anything republished must be re-earned at the moment it's spoken again.

## Child

It's the telephone game, played honestly. When you pass a message along, you may not make it *more sure* than when you heard it. If you heard "I think I saw a cat," you can't pass on "there IS a cat!" If part of the message turns out wrong, you fix just that part — you don't throw away the whole message, and you don't scribble over the original note; you write the correction next to it, with the date. And when you retell anything, you also say what you are *not* saying.

## Grandma

It's good bookkeeping and good manners, dear. The ledger's original entries are never erased — corrections go in the margin, dated and initialed, so anyone can see what was believed and when it changed. A certificate framed on the wall doesn't stay valid because it was valid once; you check it when you *use* it. And an honest shopkeeper writes "we don't carry that" on the sign instead of pretending the shelf is full. Precision about what you *don't* know is not weakness; it's the whole of trustworthiness.

## Naya

For every downstream claim, enumerate its evidence dependencies and bound certainty/scope/causality to them; propagate hedges verbatim into summaries and receipts (SN-912). Audit your fill paths: any `eligible_*` field must filter for current eligibility + independence at fill time; keep retired rows preserved and barred (SN-914). Before publishing or reusing any qualification, re-validate its dependencies at that moment; treat the missing atomic boundary as an open gap, not a footnote (SN-922). On revocation, recompute — don't patch — and preserve what stands (SN-913 via SN-2068). Never edit raw captures; correct derived outputs with dated notes; write the honest-gaps section before inventing any proxy (SN-893). Read the created_at chain before publishing any correction (SN-881). Ship every summary with its non-claims section and its counting rule, re-anchoring numbers at write time (SN-928).

## What It All Means

The four directives are one lifecycle for a claim: D32 governs its *travel* (bounded by its evidence), D33 its *correction* (surgical recomputation), D34 its *storage* (history preserved, authority leased), D35 its *republication* (re-validated at the moment of use). The three working notes are the same lifecycle at human scale — a meter's report, a seat's correction, a summary's fine print. Together they define what this system means by a claim that deserves to travel: one whose confidence never exceeded its evidence at any hop, whose history shows every change, and whose current authority was checked *now*, not inherited from when it was first earned.

## Why It Matters

Cascades are how small errors become institutional facts: a hedged finding becomes a firm summary becomes a confident plan becomes an irreversible act. Every reader has lived this — the meeting where "possibly" became "definitely" somewhere between the report and the decision. This essence matters because it makes the compression *visible and therefore chargeable*: if a claim grew in transit, there is a specific hop where it happened and a specific rule it broke. For this campaign itself, the stakes are literal — essence claims retire source notes, so an amplified claim here would retire evidence it never carried.

## How It Connects

The correction law's primary home is Batch 1 (SN-913 → SN-2068); this essence is its family, not its replacement. The fairness/governance directives' siblings (D26, D28–D30, D50, D52–D54) are in essence-governance-machinery.md. The freshness doctrine beneath D34/D35 — proof expires when its world changes, never by time — stands alone as SN-904 and is pointed to, not absorbed. SN-881's incident window is dispositioned in essence-breach-discipline.md (SN-882) and preconditioned in essence-evidence-expires.md (SN-883) — one window, three facets, three essences, no double-counting. SN-928's non-claims discipline is applied to this campaign's own receipt.

## What Is In It For You

You get the four questions that audit any secondhand claim: What exactly does it depend on? Did it grow on the way to me? Is its authority current, or cached? And what does its teller say it does *not* claim? You also get two habits worth stealing outright: correct the report, never the raw data — and when you cannot measure something, write the gap down instead of inventing a number. Those two habits alone will make every report you ever write more trustworthy than most of what you read.

## The Learning

The block's subtlest lesson is SN-928's: the auditor violated her own law in the act of writing it up — floating counts, a stale PR tally — and the team's response was not embarrassment but instrumentation: a counting rule, a mandatory section, a re-anchoring step. Bounded claims, it turns out, are not a character trait; they are a format. The other compounding lesson is D34's smell test: the most dangerous cache is the one whose field *names* promise a filtering ("eligible_") that the fill path never performs — names, like summaries, are claims.

## Coverage map — raw notes this essence covers (6)

SN-881 · SN-893 · SN-912 · SN-914 · SN-922 · SN-928

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 6 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list. (SN-913 is covered-by-batch1 via SN-2068 and must NOT appear in this or any other draft's coverage map.)
2. **Four directives kept distinct:** D32 (bounded propagation, SN-912), D33 (correction law — pointed to via SN-913/SN-2068, not restated as coverage), D34 (memory law, SN-914), D35 (republication, SN-922); fail if any two are blended or if D33's substance is absorbed here as covered material.
3. **D35 gap kept open:** the atomic publication boundary must read as unbuilt machinery requiring the director's word; fail if the essence implies the race is already prevented.
4. **D34 caveat exact:** the `build_successor_package()` finding must remain a specification-level observation, NOT proof of a production mistake; fail on any strengthening.
5. **Non-claims law complete:** SN-928 must keep the mandatory section, the counting rule (65 directives D1–D65, named scopes only), and the auditor's own violations; fail if it reads as style advice.
6. **Standing-authority guard:** SN-904 (freshness doctrine) may be pointed to but not absorbed; fail if its rule is restated as covered material.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim. (The D33 paragraph cites SN-913 as a pointer; its claims must trace to SN-912/SN-914/SN-922's stated interlock or to the receipt's Batch-1 record — fail if it introduces D33 substance beyond the pointer.)