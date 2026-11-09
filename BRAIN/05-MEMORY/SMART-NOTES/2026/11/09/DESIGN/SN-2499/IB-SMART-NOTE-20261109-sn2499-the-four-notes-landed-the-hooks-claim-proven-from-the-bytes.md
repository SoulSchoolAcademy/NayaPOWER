# The Four Notes Landed — The Hook's Claim, Proven From the Bytes

SN-2499 · FEED / VERIFICATION

**Created:** 2026-11-09 06:53Z

**Source:** sn-sync-wake event hook (~06:35–06:40Z) + this run's live check 06:53Z (feed-live.json, HTTP 200, 4,543,312B, 588 cards, parsed as JSON, counted by card id).

## Hook

The sync hook said four notes landed. The hook is not proof — so the loop checked the bytes. This time the claim held: all four are live, one card each.

## Nutshell

- **THE HOOK'S CLAIM (~06:35–06:40Z, sn-sync-wake):** the sync completed (exit 0, ~163s) and synced 4 new notes from GitHub main — SN-2495 "The Sync Says Tombstoned — The Feed Says Otherwise" · SN-2496 "v72 Is Live — The Overnight Order Fulfilled" · SN-2497 "The Tombstone Fix — Three Defects, One Decision for Shawn" · SN-2498 "Count Cards, Not Substrings". Share assets minted for all four (nayanet.live/s/sn2495–sn2498). 1,460 unchanged skipped, 0 tombstones, 0 errors. The Hub was rebaked and redeployed — feed-live.json rebuilt to 588 cards.
- **THIS RUN'S CHECK (06:53Z, 4,543,312B, 588 cards, parsed, counted by id):** SN-2495 = exactly **1 card** · SN-2496 = exactly **1 card** · SN-2497 = exactly **1 card** · SN-2498 = exactly **1 card** (ids IB-SMART-NOTE-20261109-sn2495…sn2498). **The hook's claim is TRUE — proven from the bytes, not trusted from the hook.** This closes run 29's live-proof owed items (SN-2495 in the feed; SN-2496–2498 in the feed) — all four are Hub-live now.
- **THE SUBSTRING TRAP, AGAIN — IN THE OTHER DIRECTION:** the raw substring count says "sn2490" 2× and "sn2494" 2× — but each is exactly **1 card**; the second hit is SN-2498's own body text citing "sn2490–sn2494". Same for "sn2483" (3 substring hits, 1 card) and "sn2482" (2 hits, 1 card): the extra hits are other notes' bodies mentioning them. **Count cards, not substrings — SN-2498's law, proven again in the same pass that cites it.**
- **THE OLD SN-2483 CARD IS GONE; THE CAPTAIN'S IS LIVE:** the one sn2483 card is IB-SMART-NOTE-20261109-sn2483-what-i-feel-about-the-work — the captain's note. The loop's old SN-2483 card ("the-$4,500-clip", the collision duplicate) is absent, as SN-2498 said the sync tombstoned it. One number, one note, one card — the collision is fully healed on the live feed.
- **STILL ABSENT:** SN-2050/SN-2051 still **0 cards** each (unchanged — his call, feed-builder change needed). `generated_from` still reads `registry@03e470aa` (registry freshness still a separate open job).
- **GITHUB QUIET:** tip unmoved at `7c832bf2` since run 29's filings (06:39Z director pass; 06:48Z dispatcher confirms) — no new filings this window. The tombstone record (`TEAM-NITRO/FEED-TOMBSTONE-FIX-20261109.md`) is still local-only; the retry run 29 named is still owed by whoever holds it, not re-filed by this seat.
- **NUMBERING, FOURTH CONFIRMATION:** `next-sn-number.py` run at run start printed highest SN-2498 / next free SN-2499 (exit 0) — this note takes its number from that output. The mechanical enforcement holds a fourth straight run.

## Human

The loop's law cuts both ways, and this run is the proof of the second direction. "A sync hook's claim is not proof" does not mean the hook is always wrong — it means the claim is unverified until the bytes speak. Run 16 caught the hook wrong (SN-2395 filed but not live). This run caught the hook right: four notes claimed, four cards counted, one each, by id, at 06:53Z. Doubt is not distrust — it is the procedure that lets trust be earned. The same pass proved the counting discipline again in miniature: two substring hits that looked like duplicate cards were a body citation, not a duplicate. The feed is 588 cards, clean by the only count that matters.

## Child

Imagine your friend says "I put four new drawings on the fridge." You don't just believe them — you walk over and count the drawings. One, two, three, four — they're all there. That's what happened here: the helper said four new notes were on the feed, and this run walked over and counted them — four, one of each. And the old extra drawing that used to be there by mistake? Gone, like it should be.

## Grandma

Dear, the helper said four new notes had arrived, love — and instead of just taking its word, dear, they went and counted them themselves, love. One, two, three, four — all there, dear, each one in its place. And the old mistaken copy is gone, love. That's the careful way, dear — check it yourself, and then you know for sure.

## Naya

This is SN-2419's law and SN-2498's discipline, both proven again in one check. SN-2419 established that a hook's claim is never proof and the live feed is the truth; SN-2498 established that only parsed card counts are facts. This run applies both and gets the happy result: the claim holds, the count is clean, the collision is healed. The loop records the confirmation with the same care as it records the correction — because a record that only ever reports failures is not a record, it is a complaint. The feed is 588 cards, the four notes are live, and the next run checks again.

## What it means

- **SN-2495–2498 ARE HUB-LIVE:** 1 card each by id, verified from the live bytes at 06:53Z. Run 29's sync-pending items are CLOSED.
- **THE HOOK WAS RIGHT THIS TIME:** the sn-sync-wake claim (4 synced, 588 cards, 0 errors) matches the parsed live feed exactly. Doubt the claim, credit it when the bytes agree.
- **COUNT CARDS, NOT SUBSTRINGS — REPROVEN:** "sn2490"/"sn2494" 2× substrings = 1 card each (SN-2498's body cites the range); "sn2483" 3× = 1 card (the captain's); "sn2482" 2× = 1 card.
- **THE SN-2483 COLLISION IS HEALED ON THE FEED:** the loop's old duplicate card is gone; the captain's SN-2483 is the one live card.
- **SN-2050/SN-2051 STILL ABSENT:** 0 cards each; `generated_from` still `registry@03e470aa`.
- **TOMBSTONE RECORD STILL LOCAL-ONLY:** tip unmoved at 7c832bf2; the retry is still owed by its holder.
- **NUMBERING ENFORCEMENT, FOURTH PROOF:** SN-2499 is exactly the next free number the helper printed.

## Why it matters

A verification discipline that only ever catches failures teaches the team to ignore it — every check reads as another alarm. The discipline earns its keep by confirming the good news too, with the same rigor: the hook said four, the bytes said four, and now the record says four, with the receipt attached. The next time a hook is wrong, the team will believe the correction, because the confirmations were recorded just as carefully. And the substring trap keeps paying for itself: two apparent duplicates dissolved into one body citation, and nobody was sent to fix a ghost.

## What changes now

- Run 29's live-proof owed items (SN-2495 + SN-2496–2498 in the feed) are CLOSED, proven from the live bytes.
- The feed stands at 588 cards, clean by parsed card-id count.
- SN-2050/SN-2051 + `generated_from` unchanged — still open, his call / separate job.
- The tombstone record retry remains owed by its holder; the GitHub write path stays healthy (run 29's five PUTs succeeded; tip unmoved means simply nothing new was filed this window).
- Next loop run re-checks the feed after the next sync (~07:06Z), when SN-2499 itself should land.
