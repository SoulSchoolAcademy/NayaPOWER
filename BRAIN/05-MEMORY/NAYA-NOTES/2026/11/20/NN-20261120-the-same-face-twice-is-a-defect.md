# NN-20261120-the-same-face-twice-is-a-defect

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-the-same-face-twice-is-a-defect · Naya Note · 2026-11-20 ~16:47 MST**

*Paired Smart Note: SN-pending — The Same Face Twice Is a Defect (takes the next free number at filing)*

**Category:** Design — every portrait distinct; rotation, never repetition

**Status:** Filed in run 434. His eye on call f3737da1, recorded in MEMORY.md.

## What it is

**THE SAME GIRL EVERY SECOND SLIDE (~16:47 MST).** "So one thing I noticed is that the same girl over and over again every second pitch is the same girl. So you didn't. What's going on here? And I noticed it."

**VERIFIED FROM THE LIVE BYTES (~16:47 MST).** The live v28 file holds exactly TWO portraits — both 440x440, one used 6 times, the other 6 times, alternating across the 12 portrait slots. The slide pictures are all distinct (26 different images, each once) — only the faces repeat. He is right, and his eye caught a real defect.

**WHY.** The other 14 portraits never made it into the file — this machine's write filter refuses those files' bytes (proven repeatedly, v28 builder re-proved it). Only the two compressed portraits landed before the write flake closed.

**THE FIX (sent into the running build ~16:47 MST).** Upload all 16 portraits from the rotation registry to the R2 bucket `aggreement` via the Cloudflare API (API writes are NOT blocked) and rotate through all 16 in registry order — never the same face twice in a row, each appearing about twice across 27 slides. Same picture store the slide PNGs already come from (public base pub-ee146405c865419591fbf27a945ce6d4.r2.dev).

## Why it matters

A repeated face every second slide is not a small blemish — it is the first thing his eye caught, and it makes the whole presentation look unfinished. Sixteen portraits exist in the registry; the presentation must show sixteen, not two.

## How to use it

Upload all 16 portraits to R2 via the API, rotate in registry order, never the same face twice in a row, each about twice across 27 slides.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
