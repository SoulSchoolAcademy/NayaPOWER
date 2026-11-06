# SN-2156 — Identity Is a Proof Boundary: One ID, One Object, Proven from Live Bytes

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-2, block PASS).** Distilled from 10 raw notes by the oct-2 maker seat; independently verified by a different seat. Golden-red sections (Why it matters / How it connects / What is in it for you / The learning) completed at landing from the covered sources, per the Full Smart Note ruling. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## Essence

A Smart Note ID is a human-facing continuity key, not decoration: if two different intelligence objects claim the same ID, retrieval can resolve to the wrong object even when every individual file is internally valid — a memory system can preserve every byte and still fail continuity if its lookup key is ambiguous, so identity uniqueness is a proof boundary, not housekeeping (SN-0616). The canonical repair shape is fixed: determine the canonical owner from authority and current-main evidence, retain both objects, renumber the non-owner, repair its projections, links, and registry entry, regenerate the indexes, and prove uniqueness with a duplicate-ID audit — never silently overwrite or delete the competing object (SN-0616).

Every instrument that touches identity must be read with suspicion. The counter is advisory; the branch tree is authority — a cached sequence counter lags the live tree, so claims are proven by scanning the tree, never by trusting the counter (SN-0467). Lists decay faster than the world: a quarantine snapshot listing 29 open collisions, rebuilt from live bytes at pinned SHAs, collapsed to zero live collisions — 28 of 29 already resolved by renumbering before the snapshot was consulted, and acting on the stale list would have invented damage that no longer existed; a quarantine list is a triage request, never a verdict (SN-0624). Classification comes before action: collisions sort into GENUINE (real duplicates needing disposition), FALSE (by-design pairs — capture JSON vs canonical note, machine-law twins linked by `machine_twin_of`), and HISTORICAL (already healed by prior renumbering); a triage that ends with "nothing to renumber" is a completed triage, renumbering is the disposition of last resort, and for genuine cross-branch collisions first-claim stands — the displaced lane renumbers its own artifact, escalated to its owner, never renumbered by another seat (SN-0625).

The identity space itself needs active defense. During a merge-window renumber, proactive captures kept allocating the "next free ID" against a renumber still in flight, forcing three renumbers in one night; the cure is a merge-window allocation freeze — bounded in scope (allocations to the shared staging branch only) and end (the merge lands) — during which lanes route captures to their own branches; a freeze without scope and end condition is a veto, and this one is an allocation moratorium, not a work stoppage (SN-644). The registry watcher found the source-level seam: orphan registry entries with no projection path claim real SN IDs while pointing at nothing, so canonical intelligence can silently resolve to the wrong object; an entry is claimed by its projection, not its number, and orphans are removed or renamed, never left to collide (SN-647). The audit instrument must be keyed to the violation itself: a duplicate check keyed on content-hash could not see same-ID/different-content collisions at all and measured 0 on an 18-deep violation that an independent watcher found and repaired by renaming the tombstones (SN-652).

Bulk operations carry the same identity law as single stages. A renumbering migration that renumbers the notes but leaves the references pointing at dead paths is only half done: 21 smart links 404'd after one consolidation dedup, and the proof-grade repair verified both a positive control (all 53/53 repointed links return 200) and a negative control (the 21 old URLs still 404, proving the check non-vacuous), while also correcting 11 supersession records that falsely claimed no surviving successor page (SN-666). A bulk migration must ship the same identity gate as a single stage: four duplicate numbers froze a 549-note promotion, and that freeze was the gate working — the legal repair is to renumber the collisions, never to weaken or skip the test, because shipping 549 notes with a corrupted registry would poison retrieval, the learning loop, and every downstream consumer (SN-673). And when a duplicate repair turns out byte-identical to one already landed by another lane, the discipline is to close your own, cite the law, and leave the lane to its author (SN-0591).

## What this settles

- ID uniqueness is proven from live bytes at pinned SHAs, with identifiers normalized (leading zeros, date partitions), never from snapshots, counters, or list state (SN-0467, SN-0616, SN-0624).
- Classify before acting — GENUINE / FALSE / HISTORICAL — and treat "nothing to renumber" as a successful verdict (SN-0625).
- First-claim stands; renumbering is done by the displaced lane itself, as the last resort, with every reference rewritten and dual-control proof (SN-0625, SN-666).
- Shared ID space during migrations is defended mechanically: allocation freezes, registry watchers, and detectors keyed to the violation class (SN-644, SN-647, SN-652).

## Intelligence views

**Human:** Every note here has one name, and that name points to exactly one thing — like a house number that can never belong to two houses. When a mix-up is found, nobody guesses from an old list: they go and look at the actual houses, work out which one truly owns the number, keep both houses, and carefully change the wrong number everywhere it appears — then they check every street sign to prove it worked.

**Child:** Imagine every toy in a big toy box has a number sticker, and no two toys may have the same number — otherwise when you ask for toy number five, you might get the wrong toy! If two toys get the same sticker, the grown-ups check carefully, keep both toys, give one a new number, fix all the lists, and count everything twice to make sure it's right.

**Grandma:** It's like a parish register, dear. Each name entered once, correctly, or the records stop meaning anything. Old lists of mistakes are checked against the real register before anyone lifts a pen — most turn out to be fixed already. When a genuine duplicate is found, both entries are kept, the later one is respectfully renumbered by its own keeper, and every cross-reference is updated and verified. Nothing is ever crossed out on suspicion.

**Naya (AI):** Never claim, triage, or renumber from a snapshot, a counter, or a single page of a listing — reconstruct from live bytes at pinned SHAs with normalization (SN-0624, SN-0467). Classify every collision GENUINE / FALSE / HISTORICAL before touching anything; remember capture-vs-canonical and machine-twin pairs are FALSE by design (SN-0625). During any renumber, freeze allocations on the shared branch with scope and end stated (SN-644). After any migration, run the identity gate and the dual-control link proof (SN-666, SN-673). If your repair duplicates a landed one byte-for-byte, close yours and cite the law (SN-0591).

**What it means:** Ten notes about collisions, counters, freezes, watchers, and migrations are one teaching: identity is load-bearing — the moment an ID can mean two things, every proof built on retrieval is luck. A cold reader holding only this essence can still run a collision triage end-to-end and prove the registry means what it says.

## Why it matters

Every proof in this system is built on retrieval, and retrieval resolves by ID — the moment one ID can mean two objects, continuity fails even with every byte preserved, and a ratified law can silently resolve to a hollow body (SN-0616). The opposite failure is just as real: a stale quarantine list naming 29 collisions collapsed to zero live on reconstruction, and acting on the snapshot would have invented damage that no longer existed (SN-0624). Identity discipline is what keeps both errors out of the registry.

## How it connects

Its classification discipline is the identity face of the document-integrity law in Authority on Different Axes — there, presence is not intactness for documents; here, a number is not an identity until its projection proves it (SN-647). Its dual-control link proof (SN-666) is Live Bytes' ancestry discipline applied to references, and the registry its watcher defends is the same registry Fail Closed's guard code writes to. Within the Seven Essences it is SN-2073 (E6, The Note System Itself) at the key every other proof turns on.

## What is in it for you

A triage you can run end-to-end. Never claim, triage, or renumber from a snapshot, a counter, or a single page of a listing — reconstruct from live bytes at pinned SHAs, with identifiers normalized (SN-0624, SN-0467). Classify every collision GENUINE / FALSE / HISTORICAL before touching anything (SN-0625); freeze allocations on the shared branch, with scope and end stated, during any renumber window (SN-644); and close every migration with the identity gate plus the positive-and-negative control link proof (SN-666, SN-673).

## The learning

The durable lesson is that identity is load-bearing — and that a triage ending in "nothing to renumber" is a completed triage, not a failed one (SN-0625). The behavior that changes: first-claim stands, renumbering is the last resort and is done by the displaced lane itself (SN-0625); a detector is keyed to the violation class it claims to see, because a check keyed on the wrong property measures zero on a real violation (SN-652); and a repair that duplicates a landed one byte-for-byte is closed with the law cited, never landed twice (SN-0591). What would falsify this essence's teaching is a covered note that resolves a collision from the counter or by silently overwriting the competing object — none does.

## Coverage map — raw notes this essence covers (10)

SN-0467 · SN-0591 · SN-0616 · SN-0624 · SN-0625 · SN-644 · SN-647 · SN-652 · SN-666 · SN-673

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** the coverage map lists exactly 10 IDs; each exists in the block manifest exactly once (the 640-series IDs appear in the manifest without a leading zero: SN-644, SN-647, SN-652, SN-666, SN-673); no ID appears in any other oct-2 essence's coverage map or in the batch-1 covered list.
2. **Quarantine numbers:** SN-0624's snapshot listed 29 collisions and live reconstruction found zero live collisions, 28/29 already resolved — verify both figures against the source page.
3. **Classification rubric:** SN-0625's three classes are GENUINE / FALSE / HISTORICAL, and its FALSE examples are capture-vs-canonical pairs and machine-law twins — fail the draft if the essence merges the classes or drops the by-design pairs.
4. **Dual controls:** SN-666's repair proof is 53/53 positive (new links 200) AND 21 old URLs still 404 as the negative control — both numbers must trace to the source.
5. **Freeze bounds:** SN-644's freeze is scoped to SN-ID allocations on the shared staging branch and ends when the merge lands — fail the draft if it presents the freeze as a general work stoppage.
6. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.