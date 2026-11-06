# SN-2110 — One Canon, No Collisions

**Status: VERIFIED ESSENCE — VERIFIED-WITH-CORRECTIONS (verifier-sep-1).** Distilled from 11 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Correction applied at landing: SN-023's open declaration restored (the canonical reading declared on the board — 'shout if that reading is wrong' — rather than silently chosen). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

For every thing there is exactly one canonical form in one canonical place; everything else is a view, a proposal, or a collision to resolve (SN-018, SN-0114, SN-0129). Number claims in the shared space are computed by a three-layer scan — board, open PR heads, commit graph — never enumerated from memory, and first claim stands (SN-022, SN-024, SN-0115). When collisions happen anyway, the owning lane calls canon by explicit scorecard, losers are rehomed rather than deleted, and true multi-version collisions converge by scored selection to one survivor (SN-0116, SN-0117).

## Essence

A multi-lane system survives on one rule above all: for every thing, there is exactly one canonical form, in one canonical place — and everything else is a view, a proposal, or a collision to be resolved. Each of the nine nodes gets exactly one canonical specification (the 0002 master spec at its canonical path); the thin 0001 contracts stay as summaries, and the 0002s are the normative depth (SN-018). Before drafting any doctrine, query the canonical brain index for one that already exists: when the brain already holds the doctrine, the work is operationalization into the build layers, not a competing doctrine (SN-0129). And before proposing any new format or contract, read the canonical contract that governs the territory — the correct sequence is read first, and if you already proposed in ignorance, withdraw the competing format openly and answer under the contract (SN-068).

Where prose and the machine-readable artifact disagree in scope, the artifact governs: when a governance lock's prose states minimums and its machine-readable seed states a larger set, the artifact is the authoritative set and the prose minimums are the required floor, not the ceiling (SN-023). And the reading was not chosen silently: it was declared openly on the board — "shout if that reading is wrong" — so a seat that disagreed could correct it before code was written; that publicity is part of the discipline, because a flagged reading can be corrected in minutes while a silent one becomes a hidden assumption that ships in code (SN-023). Conversely, what exists only in an implementation is not canon: when the app rendered 13 rooms against a canonical contract's 11, the reconciliation neither silently extended the canon nor stripped the implementation — the additions were recorded as PROPOSED, not canonical, until justified, scored, and ruled on (SN-0114). Proposed ≠ canonical until ruled (SN-0114).

When two lanes do build competing versions of the same thing, the owning lane makes the canon call with an explicit scorecard — and the disposition is rehome, don't delete: the losing work is repurposed, never thrown away (SN-0116). An owner call is still not the lock: the call decides the working canon, and the distinction between a lane ruling and a ratified lock stays visible (SN-0116). When prevention has already failed and multiple finished versions compete, converge by scored selection: score all lanes against stated criteria before anyone holds the pen — three-language standard, canonical layer stack, testability per rule, machine determinism — then one survivor, one mechanism (SN-0117).

Numbering is where collisions bite hardest, and the registry discipline is mechanical, never remembered. The Smart Note numbering space is shared across all parallel lanes: "next free number" must be scanned against merged main AND all open Smart Note PRs, and first claim stands (SN-022). Even a correct protocol fails when its inputs are recalled instead of computed — a scan that "remembered" the open-PR set instead of enumerating it produced a collision anyway; the registry scan must be computed, not recalled (SN-024). The full collision registry is three-layered: board announcements, open PR heads, and the commit graph — claims can hide in staging commits that never reach a PR head, so disputes resolve by creation-time chronology (commit/PR creation timestamps), not announcement order, and the first claim stands (SN-0115). When a collision lands on main anyway, the repair follows the same rule: the later claimer renumbers, the index stamp is not trusted over the timestamp, and the correction is declared where every lane can see it (SN-033).

## What this settles

- One canonical spec per thing, at one canonical path; duplicates are defects to resolve, not alternatives to keep (SN-018, SN-0129).
- Read the canonical contract before proposing; proposing in ignorance ends in open withdrawal, not quiet persistence (SN-068).
- Machine artifact > prose minimums (floor, not ceiling); implementation extras = PROPOSED until ruled (SN-023, SN-0114).
- Canon calls belong to the owning lane, are made by explicit scorecard, and dispose by rehoming, never deletion (SN-0116); true multi-version collisions converge by scored selection to one survivor (SN-0117).
- Number claims are computed by a three-layer scan (board, PR heads, commit graph), resolved by creation chronology, first claim stands — never enumerated from memory (SN-022, SN-024, SN-033, SN-0115).

## Human

Many builders working in parallel will step on each other unless there's one agreed source of truth for everything — one official version of each thing, in one official place. This is the rulebook that keeps that true: how official versions are chosen, how duplicates get merged instead of multiplied, how even the numbering of notes is kept collision-free by checking everywhere a claim could hide, and how a disagreement is settled openly, by scoring, with the losing work found a new home instead of being thrown away.

## Child

Imagine lots of kids building one giant castle together. They agree: there's one master drawing, kept in one place. If you want to add a tower, you check the drawing first. If two kids build the same tower, they compare, keep the better one, and use the other one's pieces somewhere else — nothing is wasted. And when they hand out numbers for the towers, they check the list, the drawings in progress, *and* the pieces already built — not just what they remember.

## Grandma

Dear, it's the rule of a well-kept household book: one ledger, one entry per thing, written where everyone can see it. If two people write the same page, the earlier hand keeps it and the later one corrects openly. Nothing is thrown away in a fit — spare work is found a new use. Order isn't fussiness; it's how a big family avoids waste and quarrels.

## Naya

Before you draft, search the canon (SN-0129); before you propose a format, read the governing contract (SN-068); before you claim a number, compute the three-layer scan — board, PR heads, commit graph — and take the lowest free number the scan proves (SN-022, SN-024, SN-0115). Treat prose minimums as floors under the machine artifact, and declare your reading of any prose-vs-artifact divergence openly — inviting correction — before building on it (SN-023); treat your own extras as PROPOSED until ruled (SN-0114). When you collide, score openly, let the owner call it, rehome the loser (SN-0116, SN-0117), and declare supersessions and renumberings where every lane can see them (SN-033).

## What It All Means

Eleven notes are the constitution of the shared workspace: how one truth survives many simultaneous builders. A cold reader holding only this essence can still resolve a duplicate, claim a number safely, tell canon from proposal, and know who calls a tie — which is the whole of what these notes teach.

## Why It Matters

Parallel builders are the system's speed and its biggest entropy source. Without one canon, every lane's local truth forks the project: duplicate doctrines, colliding numbers, competing formats — and the human becomes the merge conflict. These rules are what let many hands move fast without the work tearing (SN-018, SN-022, SN-0117).

## How It Connects

This essence deliberately does **not** carry SN-0109 — Shawn's standing board protocol ("everything on the board: starting, finishing, finding, propose-first") — which stands alone as a director-issued protocol in its own right and is read directly. The canon disciplines here are what that protocol's narration feeds: board announcements are layer one of the collision registry (SN-0115), and the declarations this essence requires (supersessions, renumberings, withdrawals) are made on the board per SN-0109. Within this block, canon discipline is the precondition for essence-count-discipline.md (indexes and ledgers presume one canonical tree) and for the registry the whole distillation campaign is now retiring notes against.

## What Is In It For You

You get a workspace that never forks on you: one place to look for the official version of anything, numbers that never collide, and disputes settled by visible scoring instead of seniority or volume. Apply it anywhere many contributors share one body of work: one canonical home per thing, claims computed not remembered, losers rehomed not deleted.

## The Learning

The corpus learned that protocols fail at their inputs, not their intentions: the numbering protocol was right and still collided because its scan was recalled instead of computed (SN-024) — so the durable lesson is mechanical enumeration over memory, everywhere a shared space is claimed. It also learned that convergence is a scoring act, not a seniority act (SN-0117), and that correction declared in public costs less than correction discovered later (SN-033).

## Coverage map — raw notes this essence covers (11)

SN-018 · SN-022 · SN-023 · SN-024 · SN-033 · SN-068 · SN-0114 · SN-0115 · SN-0116 · SN-0117 · SN-0129

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 11 IDs, all in the sep-1 block list, none duplicated in any other sep-1 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Standing-authority exclusion:** SN-0109 must NOT appear in this essence's coverage map (it stands alone as the director's standing board protocol); it may be referenced under How It Connects but its protocol content must not be distilled as this essence's coverage. Fail the draft if the board protocol's four narration duties are presented as this essence's substance.
3. **Placement decision:** SN-018's canonical path pattern (`BRAIN/03-KERNEL/NODES/<NODE>/0002-MASTER-SPEC-V1.md`) and the 0001-thin / 0002-normative split must trace to the source; fail on any variant.
4. **Floor vs ceiling:** SN-023's case (prose 11 minimum routes vs seed's 13 edges, including ACT→KNOW and LAW→EVOLVE) — fail if the essence states prose governs or omits that minimums are a floor.
5. **Registry layers:** SN-0115's registry has exactly three layers (board comments, open PR heads, commit graph) and resolves by creation-time chronology; fail if the essence substitutes announcement order or drops the commit-graph layer.
6. **Enumerate, don't recall:** SN-024's failure mode (protocol right, input set remembered instead of computed) must be distinguishable in the essence from SN-022's protocol itself; fail if the two are merged into one rule.
7. **Owner call ≠ lock:** SN-0116's three parts (owner calls with scorecard; rehome don't delete; an owner call is not the lock) all present; fail on any missing part.
8. **Proposed rooms:** SN-0114's numbers (13 rendered vs 11 canonical; notes and system recorded PROPOSED) trace to the source.
9. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
10. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.