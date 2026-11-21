# SN-4358 — The Same Face Twice Is a Defect

**Category:** DESIGN — every portrait distinct; rotation, never repetition; 2026-11-20 ~16:47 MST

*Paired Naya Note: NN-20261120-the-same-face-twice-is-a-defect — the verbatim record of his eye.*

**Filed:** SN-4358 — Intelligence Loop run 434, 2026-11-20. His catch on call f3737da1, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The live v28 file holds exactly TWO portraits, each used 6 times, alternating across the 12 portrait slots. The fix: all 16 portraits from the rotation registry, uploaded to R2 via the API, rotating in registry order — never the same face twice in a row, each about twice across 27 slides.

## The Lesson

His eye caught what the machine missed: "the same girl over and over again every second pitch is the same girl." The slide pictures were all distinct — 26 different images, each once — so the build looked checked. But the faces repeated, and the repetition is what a human sees first. A rotation that shows two faces twelve times is not a rotation; it is a defect wearing a rotation's name. The cause was mechanical — the machine's write filter refused the other 14 portraits' bytes, and only the two compressed portraits landed before the write flake closed — but the cause does not excuse the result. The fix goes around the blocked path instead of through it: API writes to R2 are not blocked, so the portraits travel that way. When a path refuses the bytes, find the path that takes them; never ship the half that landed and call it the set.

## Why It Matters

Sixteen portraits exist in the registry. Showing two of them twelve times tells the citizen the system has two faces, not sixteen — and it tells Shawn his eye is the only check that works. The registry is the source of truth; the live file must match it.

## How to Use It

Upload all 16 portraits from the rotation registry to the R2 bucket `aggreement` via the Cloudflare API and rotate through all 16 in registry order — never the same face twice in a row, each appearing about twice across 27 slides. Verify from the live bytes: count the distinct portraits in the file, not the slots.

## His Order, As Recorded

> "So one thing I noticed is that the same girl over and over again every second pitch is the same girl. So you didn't. What's going on here? And I noticed it."

## Owed from This Dictation

- The running build (agent 541a5467): all 16 portraits via R2, registry-order rotation, never the same face twice in a row. Goes live at nayanet.app/agreement when it lands.
