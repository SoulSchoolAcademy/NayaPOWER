# SN-3630 — Bytes Can Pass While the Frame Never Paints — Diagnose First

**Filed:** Intelligence Loop run 344, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3630; filed as SN-3630 under its draft number.

**Filed by:** Intelligence Loop run 344, 2026-11-18 — Hub follow-on fix round 2 verdict HELD + captain's cloud eye, 04:19–04:28Z 2026-11-19.

**Paired Naya Note:** NN-20261118-bytes-pass-frame-never-paints

## The teaching, in his words (verbatim)

No dictation — a verification lesson from the work itself, in the checker's and the captain's words. Checker: byte PASS — diff exactly 8 opcodes / 23 lines, laws delta zero, staged URL sha-matched twice. Captain's eye on the same bytes at 1920×998: the gold kingdom frame does NOT paint — top edge solid plain black, bottom edge plain black, no gold at any corner. Fix round 3's rule, from the captain: diagnose first, then fix — "do NOT re-apply the same change and hope."

## The understanding

Bytes are the filing, not the experience. A fix can be byte-perfect — exact diff, zero laws delta, sha-matched staging — and still never paint, because painting happens in the render, and the render is a different world from the file: the DOM, the computed style, what covers what, whether a 2.2 MB data URI loads at all. A checker that only reads bytes will pass a page Shawn's eye fails in one look. That is why the verdict is HELD, not PASS: the bytes passed and the experience did not, and the render wins. The second half of the lesson is discipline: when a fix fails in render, the next round diagnoses the cause before touching code — otherwise the same change gets re-applied, the same failure comes back, and the round burns an hour proving nothing.

## The law

A round is never done on bytes alone — the render re-probe is part of done. When a fix fails in render, diagnose first: do the band elements exist in the rendered DOM? does the background-image compute? is something covering them? is the asset failing to load? Name the cause, then fix the cause. Never re-apply the same change and hope.

## Owed from this dictation

Hub fix round 3 carries the diagnose-first rule and does not go to Shawn until a render re-probe lands. Every future checker verdict keeps byte PASS and render verdict separate — a HELD on render is a goes-back, not a pass.

**Bytes file the fix; the render proves it. Diagnose the cause, never re-apply the hope.**
