# SN-4350 — Prove It on Screen Before You Deploy

**Category:** LAW — a source-verified build is not a screen-proven build; the deploy gate is the render; 2026-11-20 ~16:21 MST

*Paired Naya Note: NN-20261120-prove-it-on-screen-before-you-deploy — the verbatim record of the build completion.*

**Filed:** SN-4350 — Intelligence Loop run 433, 2026-11-20. The agreement fix build completion on call bd6bc254, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The fix build is complete and source-verified — corner crystal logo restored, beautiful red N centered, saying in white certificate writing, obsidian buttons with only a quiet shine, motion restored, legal bar in place. But the corner logo was NOT proven on screen: the builder's own captures never showed it, and the embedded bytes did not match the crystal source. So the deploy carries a gate: verify the corner logo resolves to the crystal artwork BEFORE deploying. If it doesn't, stop and report — do not deploy a broken logo.

## The Lesson

Source-verified is not screen-proven. The mechanism (asset override to the identical artworks already in assets/) checks out in the source, while the render is contested — the captures show no crystal logo in the top-left, and the embedded logo/ball data URIs are identical to each other, not to the crystal source. A build can be right in its files and wrong on the screen, and the only thing that catches the gap is looking at the screen before shipping. The gate is the discipline: the deploy coordinator verifies the logo resolves to the crystal artwork first, and a failed verification stops the deploy instead of shipping a page whose corner is wrong. This is the same law as his eye being the final gate — nothing reaches him, and nothing goes live, that has not been seen on a screen.

Environment note, builder-proven this run: the VM write filter currently refuses to write ANY image bytes or image base64 through shell/Node, so embedding the new artworks as fresh base64 was impossible and the override was the way through. Stale flat bytes remain in the file unused (~36KB); a future rebuild, when the filter clears, swaps the override for true embedded bytes.

## Why It Matters

Deploying a build whose logo is unproven ships the exact defect he has already corrected twice — the corner logo going away. A stopped deploy costs a round; a live page with the wrong logo costs his trust and another correction.

## How to Use It

Every deploy with a visual claim carries a render gate: the claimed artwork must be seen resolving on screen — fresh fetch, matching hash — before the deploy runs. If the render contradicts the source, the source loses and the deploy stops. Record the gate and its result in the deploy receipt, never as an assumption.

## Owed from This Dictation

- The agreement deploy (coordinator dispatched ~16:21 MST): verify the corner crystal logo resolves on live before deploying; solve the assets/ resolution; confirm / and /hub unchanged.
- His last screenshot (816a4f59…, 16:19 MST) shows the bar the way he wants it — all ten legal links visible above the fold on that staging walk.
