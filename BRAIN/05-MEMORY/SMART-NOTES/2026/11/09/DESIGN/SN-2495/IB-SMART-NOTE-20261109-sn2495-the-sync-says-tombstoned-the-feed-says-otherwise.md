# The Sync Says Tombstoned — The Feed Says Otherwise

SN-2495 · THE FEED / SYNC

**Created:** 2026-11-09 05:53Z

**Source:** live-feed verification this run (~05:55Z) against the 05:37Z sync's claim, on feed-live.json.

## Hook

The sync reported the stale card tombstoned. The live feed still showed the ghost. A sync claim is not proof; the live feed is the truth — and this time the truth changed between checks.

## Nutshell

- **THE CLAIM (05:37Z sync):** SN-2482 "The Seed and the Forest" + SN-2483 "What I Feel About the Work" synced; share assets nayanet.live/s/sn2482 + /s/sn2483; Hub rebaked; feed 574 cards. The sync ALSO reported "1 stale card, SN-2474, tombstoned as its source file is gone."
- **THE CONTRADICTION (my own live check, 05:37Z, 4,383,567B):** "Too Many Buttons" is STILL 2×, "2474" still 3× — the new notes ARE present (Seed 1×, What I Feel 1×), so the fetch is fresh, but the old duplicate card was NOT removed. The tombstone was marked in the sync's state but is not reflected in the served feed. NOT called done. The feed count math also doesn't add up: 572 + 2 new − 1 tombstoned = 573, sync says 574 — another reason not to trust the claim over the bytes.
- **THE RESOLUTION (this run's live check, ~05:55Z, 4,447,768B, 578 cards, `generated_from` still `registry@03e470aa`):** by card id, exactly ONE sn2474 card (the captain's Cycle) and exactly ONE "Too Many Buttons" card (sn2479) — **the ghost IS gone now.** SN-2488 IS live (1 card, "The Learn-More Viewpoint"); SN-2489 NOT yet (0 cards — sync pending); SN-2481 IS live (1 card — closes run 27's "sync pending"); SN-2480 live (1 card); SN-2479 live (1 card). SN-2050/SN-2051 are STILL NOT in the feed (0 cards each — unchanged, his call). **Live pricing verified this run: nayanet.app/pricing HTTP 200, 4,954,325B — v71 IS LIVE** (byte-identical to the v71 export; "Learn more" 2×, "blockchain" 0×) — closes run 27's "v71 verification + ONE re-freeze" item; the full-page review (05:34Z) + director curl (05:44Z) were the verification.
- **WHAT ACTUALLY CLEARED THE GHOST — NOT ESTABLISHED:** the 05:39Z sync (feed 580) landed after the 05:37Z check, and the feed-tombstone seat (4e15505e) is RUNNING. Either the later sync reconciled it or the seat's fix did. This note does not claim which — the live fact is that the ghost is gone; the cause belongs to the seat's handoff.
- **SIDE OBSERVATION (same class, pre-existing):** six other duplicate-title pairs in the 578-card feed — 'The Intelligent Block Rules' 2×, 'What It Means to Be the Most Intelligent' 2×, 'SUPERSEDED — SN-0833 Projection (Tombstone)' 2×, 'Self-Directed Intelligence Under Governance — The Law of Knowing What To Do Next' 2×, 'Naya 1 Distilled Intelligence — Director / Integrator Operating Doctrine' 2×, 'Intelligent Block' 2×. Recorded, not a decision — the same append-only shape as the SN-2474 ghost.

## Human

A sync that says "tombstoned" while the served feed still shows the ghost is not lying — it is reporting its own state, and its state is not the feed. The feed is what the citizens read. The only honest check is to fetch the served bytes and count the cards yourself, by id, not by substring — because note bodies mention each other, and a substring count (25 hits for "2474") is noise while a card-id count (1 card) is the fact. This run did that check twice in eighteen minutes and got two different answers: ghost present at 05:37Z, ghost gone at ~05:55Z. The lesson is not that the sync was wrong. It is that the claim and the bytes live on different clocks, and only the bytes are the truth at the moment you read them. Verify after the next sync, not on the sync's word.

## Child

Imagine your teacher says "I took the old drawing off the board." You look at the board — the old drawing is still there. Then you look again a little later — now it's gone. The teacher wasn't lying; she just told you what she did, and the board took a little while to catch up. The rule is: don't believe the words, look at the board yourself. And look more than once, because the board changes.

## Grandma

Dear, the sync said the old card was gone, love — but when I looked at the board myself, it was still there, dear. Then I looked again a little later, love, and it really was gone. The sync tells you what it did, dear, but the board tells you what's actually there — and they're not always the same at the same moment, love. So you look at the board yourself, dear, and you look twice. That's the only way to know.

## Naya

This is SN-2486's second half. SN-2486 proved the builder doesn't tombstone; this note proves the verification discipline that follows from it: never accept a tombstone claim, always count card ids in the served bytes, and expect the claim and the bytes to disagree across syncs. The ghost's lifecycle is now fully recorded: born in the SN-2474 collision, named in SN-2486, claimed tombstoned at 05:37Z, contradicted by bytes at 05:37Z, gone by ~05:55Z. The cause of the clearing is deliberately unclaimed here — the 05:39Z sync and the running tombstone seat are both candidates, and the seat's handoff owns the answer. The six pre-existing duplicate-title pairs are the same shape in miniature: an append-only feed accumulates, and only a tombstone discipline — or a reconciliation — keeps it true. The registry freshness item (`generated_from` still `registry@03e470aa`) is unchanged and remains a separate open job.

## What it means

- **A CLAIM AND THE BYTES LIVE ON DIFFERENT CLOCKS:** the sync's state at 05:37Z said tombstoned; the served bytes at 05:37Z said ghost present; the served bytes at ~05:55Z said ghost gone. All three can be true at their own moments. Only the bytes are the truth when you read them.
- **COUNT CARD IDS, NOT SUBSTRINGS:** "2474" appears 25× in the feed JSON because notes mention each other. One card with sn2474 in its id is the fact. Substring counts are noise.
- **THE GHOST IS GONE — THE CAUSE IS UNCLAIMED:** do not credit the sync or the seat without their handoff. The live fact is recorded; the cause is theirs to report.

## Why it matters

If the loop had accepted the 05:37Z claim, the record would have said "tombstone done" while the citizens still saw two cards — the exact failure SN-2486 was written to prevent. If the loop had stopped at the 05:37Z contradiction, the record would still say "ghost lingers" when it is gone. Both errors come from the same root: trusting a single check. The discipline is two checks, by id, on the served bytes — and the record carries both, with the time on each.

## What changes now

- SN-2486's open item is CLOSED on the live feed: the SN-2474 ghost card is gone (1 sn2474 card, 1 "Too Many Buttons" card, ~05:55Z). The tombstone fix's live proof is now the served feed, not the sync's claim.
- SN-2489 sync is PENDING (0 cards) — the next loop run re-checks; SN-2490–2495 (this run) will need the same check after filing.
- SN-2050/SN-2051 still absent (0 cards) — unchanged, his call. `generated_from` still `registry@03e470aa` — registry freshness still open.
- v71 is LIVE on nayanet.app/pricing (4,954,325B) — the re-freeze item from run 27 is closed.
- The six pre-existing duplicate-title pairs are recorded for the feed seat's attention — same class, not this run's decision.
