# SN-4588 — SN-4467 Is Filed and Live — the Picture Test, Half-Proven

**Category:** SMART NOTES — SN-4467 filing done, picture test half-proven — 2026-11-21 ~14:02 MST

*Paired Naya Note: NN-20261121-sn4467-filed-live-on-feed — the verbatim record of the filing, the live feed, and the half-proven picture.*

**Filed:** SN-4588 — Intelligence Loop run 476, 2026-11-21. SN-4467 filing completed by agent `8d4b9efa` ~14:02 MST, as recorded in the curated memory. Closes SN-4573's owed SN-4467 filing.

## In a Nutshell

SN-4467 ("What Is a Wise Naya?", the first complete intelligent block) is finally filed and live on the Hub feed — filed + verified on GitHub main (blob `97b203e7`, commit `a0c4a885`, 6,161 B, sha-verified), live on the feed, current: 3,463 cards, 7 layers, Naya Note 2,881 chars (full deal). The picture test is half-proven: Naya's portrait renders IN the filed block (hosted beside the note, `naya-portrait.webp`, blob `f0301213`, 437,564 B) but NOT on the feed card yet — the feed builder sets no image field, the Hub renderer has no image slot. The baked Hub card is still stale (old title, 5 layers, Naya Note 214 chars): the deploy retry loop ran all 12 attempts (18:59–20:51Z) and every one died on the EPERM flake at local staging; no loop running now.

## The Lesson

**SN-4467 FILING — DONE, LOOP FINISHED (agent `8d4b9efa`, completed ~14:02 MST):** filed + verified on GitHub main (`BRAIN/05-MEMORY/SMART-NOTES/2026/11/21/LAW/SN-4467/IB-SMART-NOTE-20261121-sn4467-what-does-it-mean-to-be-a-wise-naya.md`, blob `97b203e7`, commit `a0c4a885`, 6,161 B, sha-verified); LIVE on the Hub feed, current — 3,463 cards, SN-4467 titled "What Is a Wise Naya?", 7 layers, Naya Note 2,881 chars (full deal).

**PICTURE TEST — HALF-PROVEN:** portrait renders IN the filed block (hosted beside the note, `naya-portrait.webp`, blob `f0301213`, 437,564 B) but NOT on the feed card yet — feed builder sets no image field, Hub renderer has no image slot.

**BAKED HUB CARD STILL STALE** (old title, 5 layers, Naya Note 214 chars): the deploy retry loop ran all 12 attempts (18:59–20:51Z) and every one died on the EPERM flake at local staging (`deploy_hub_assets.py:339`, `open(dest, "wb")`); Python-write window closed since 17:45Z (~3h); live Hub untouched by every failure; no loop running now.

**OWED:** retry the deploy when the write window opens (no loop running — captain's call on restarting one) · parser+bake go-ahead (means/how-to-apply/why-connects/machine extraction, WIIFY apostrophe fix, leading-image → card.image) · Hub coordinator's lane (image top-frame + missing-layer rendering) · share link `nayanet.live/s/sn4467` still 404s service-wide · filename slug still reads `what-does-it-mean-to-be-a-wise-naya` (rename or keep — his call).

## Why It Matters

SN-4467 is the first complete intelligent block — the anatomy thesis (SN-4466) made real — and it sat unfiled for hours while the loop kept poking for it. Filing it closes the oldest owed item from the morning call, and the feed proves it live and current. But the picture test is the honest half: the portrait is IN the block and NOT on the card, and the baked card the Hub actually serves is still the stale one — because the deploy loop died twelve times on the EPERM flake, not because anyone chose to leave it stale. Naming the stale card plainly is what keeps the "live" claim honest: the note is live in the feed table, the card the Hub bakes is not yet the new one.

## How to Use It

The deploy retry runs when the write window opens (captain's call on restarting the loop); the parser+bake go-ahead and the Hub coordinator's image lane close the card gap; the share link and the filename slug wait on his call. Until then: SN-4467 is filed, live in the feed, portrait in the block — and the baked card is stale, named, not hidden.

## Owed from This Dictation

- Deploy retry when the write window opens (captain's call on restarting the loop).
- Parser+bake go-ahead (means/how-to-apply/why-connects/machine extraction, WIIFY apostrophe fix, leading-image → card.image).
- Hub coordinator's lane (image top-frame + missing-layer rendering).
- Share link `nayanet.live/s/sn4467` 404s service-wide.
- Filename slug `what-does-it-mean-to-be-a-wise-naya` — rename or keep, his call.
