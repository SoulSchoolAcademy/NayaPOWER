# Count Cards, Not Substrings

SN-2498 · FEED / VERIFICATION

**Created:** 2026-11-09 06:23Z

**Source:** 06:14Z feed verification (captain's own parsed card count) + this run's live check 06:23Z (feed-live.json, HTTP 200, 4,500,544B, 584 cards).

## Hook

"Too Many Buttons" appears 14 times in the feed — and zero cards carry that title. The substring count is noise; the card count is the fact.

## Nutshell

- **THE 06:14Z CHECK (parsed as JSON, counted CARDS, not substrings):** "Too Many Buttons" = **0 cards** (the stale duplicate is GONE) · SN-2474 = exactly 1 ("The Speed of Intelligence — The Cycle") · SN-2482 = exactly 1 ("The Seed and the Forest") · SN-2483 = exactly 1 ("What I Feel About the Work") · SN-2488 = exactly 1 ("The Learn-More Viewpoint") · SN-2489 = exactly 1 ("The $4,500 Clip Was Never a Defect"). **Lesson, in the captain's words: raw substring counts lie — the collision notes' BODIES mention "Too Many Buttons" (14 occurrences) while the card count is 0. Always count parsed cards.**
- **THE SYNC'S OWN COUNT DIDN'T ADD UP EITHER:** the 06:14Z sync synced 5 new notes — SN-2490 "His Verdict on the Day" · SN-2491 "The Magic of Life" · SN-2492 "Belief Before Proof" · SN-2493 "The v71 Full-Page Review" · SN-2494 "The Numbering Law, Mechanically Enforced" (share assets nayanet.live/s/sn2490–sn2494); feed 584 cards. The sync also tombstoned the loop's old SN-2483 card ("the-$4,500-clip") and noted SN-2482/SN-2474's old files as gone but left their cards as-is — the parsed card count shows no stale cards remain for either number, so nothing is left hanging.
- **THIS RUN'S CHECK (06:23Z, 4,500,544B, 584 cards):** SN-2490/2491/2492/2493/2494 each exactly **1 card** (ids IB-SMART-NOTE-20261109-sn2490…sn2494) · SN-2488/2489 each 1 · **SN-2495 still 0 cards — sync pending** (the 06:14Z sync carried 2490–2494 only; SN-2495 "The Sync Says Tombstoned" was filed by run 28 in the same batch but did not land — next sync carries it, re-check next run) · SN-2050/SN-2051 still **0 cards** each (unchanged — his call) · `generated_from` still `registry@03e470aa` (registry freshness still open).
- **NUMBERING, THIRD CONFIRMATION:** SN-2490 was exactly the next free number the helper printed — no collision this run; the mechanical enforcement is working (SN-2494's law, proven a third time).

## Human

Two kinds of counting live in this system, and only one of them is true. A substring count searches the whole file — every body, every cross-reference, every mention — and reports noise as if it were signal: "Too Many Buttons" 14 times, when no card carries the title. A card count parses the JSON, walks the cards, and counts the things citizens actually see: zero. The difference is the difference between reading the room and reading the echoes. The same discipline applies to the sync's own arithmetic — 5 new minus 1 tombstoned from 580 is 584, and the parsed count agrees — but the arithmetic is a cross-check, not the proof. The proof is the parsed cards, by id, at the moment you read them. SN-2495 is still waiting on its sync; that is not a defect, it is a clock — the next run checks again.

## Child

Imagine counting how many red cars are on the road — but you count every time someone SAYS "red car" on the radio, too. You'd get fourteen, but there are zero red cars on the road. The right way is to look at the road and count the cars you actually see. That's what they did: they looked at the feed itself and counted the cards — zero old cards, one of each new one. And one note hasn't arrived yet — it's still on its way, and they'll check again next time.

## Grandma

Dear, they learned to count properly, love — not by how many times the words appear, dear, but by how many cards are really there, love. The words "Too Many Buttons" show up fourteen times in the writing, dear, but there's not a single card with that name anymore — it's gone, love. One note is still on its way, dear — they'll look for it again next time. That's the careful way, love, and it's the only way to know for sure.

## Naya

This is SN-2495's discipline, proven a third time and now its own note. SN-2495 established "count card ids, check twice"; the 06:14Z check proved the substring trap in the other direction (14 mentions, 0 cards); this run's check confirms the clean state holds at 584 cards. The discipline now has three proofs: the two-check ghost (SN-2495), the substring trap (06:14Z), and the steady-state confirmation (this run). It belongs in the record as its own law because it is the kind of mistake that looks like diligence — counting more is not counting better. Counting the right thing once beats counting the wrong thing fourteen times.

## What it means

- **PARSE THE JSON, COUNT THE CARDS, BY ID:** substring counts include note bodies that mention each other. A card-id count is the only fact about what citizens see.
- **THE FEED IS CLEAN AT 584 CARDS:** SN-2490–2494 each 1 card; SN-2488/2489 each 1; SN-2474/2482/2483 each 1; "Too Many Buttons" 0 cards. The tombstone fix holds on the live bytes.
- **SN-2495 STILL PENDING SYNC:** 0 cards — the 06:14Z sync carried 2490–2494 only. Not a defect; re-check next run.
- **SN-2050/SN-2051 STILL ABSENT:** 0 cards each — unchanged, his call. `generated_from` still `registry@03e470aa`.
- **NUMBERING ENFORCEMENT, THIRD PROOF:** SN-2490 was exactly the next free number; no collision.

## Why it matters

Every verification this team does stands or falls on how it counts. A substring count that says "2×" when the truth is "1 card" sends a seat to fix a ghost that is already gone — wasted work, and worse, a false record. A card-id count that says "0" when the truth is "0" lets the team move on. The loop's job is the record, and the record is only as true as its counting. This note exists so the next verifier counts cards the first time, not after being fooled by substrings.

## What changes now

- The verification discipline is now a named law: parse the JSON, count cards by id, never substrings.
- SN-2495 sync pending — next loop run re-checks (same as SN-2489 was, now landed).
- SN-2050/SN-2051 + `generated_from` unchanged — still open, his call / separate job.
- The six pre-existing duplicate-title pairs (SN-2495's side observation) remain recorded for the feed seat.
