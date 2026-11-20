# SN-3961 — A Fix Proven at Rest Is Not Proven in Motion

**Filed:** Intelligence Loop run 386, 2026-11-19 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3961; drafted and filed in run 386.

**Filed by:** Intelligence Loop run 386, 2026-11-19 — Dashboard follow-up 14 checker PASS, ~00:01Z 2026-11-20 (17:01 MST 2026-11-19).

**Paired Naya Note:** NN-20261119-a-fix-proven-at-rest-is-not-proven-in-motion

## The teaching, in his words (in substance, as recorded)

Dashboard follow-up 14 passed its checker — both f13 fails cured on render: gear vs X is 10px clear at 1920 (was 26×22px overlap), clear at scroll 0/1200/2400, panel open + closed; the state-cell labels sit exactly aligned. But the checker carried two honest limits. The first: transient scroll pass-through — the gear overlaps the X at scroll offsets 20–80, because the gear is `position:absolute` and scrolls with the document while the X is sticky. At every measured stop the fix is clear; in motion between the stops it fails. It is pre-existing broken fixing, and the brief's measured positions are all clear — so the round passes — but a follow-on round is owed to cure the fixing itself. The second limit: no data-loaded render from the seat (41 Supabase requests, 2 responses) — the conversation line, first-paint numbers, world-board stats routing and the X-vs-WEEK pill are owed to the captain's eye on a data-loaded render.

## The understanding

A page at rest is not the page in use. Stops are where a checker measures; motion is where a citizen lives — every scroll passes through the offsets between the stops. A fix that holds at 0, 1200 and 2400 and breaks at 20–80 was never proven; it was sampled. The pass-through is the proof, not the stops. And a render with no data behind it proves the frame, not the page — the numbers the citizen reads are the page.

## The law

Measure the pass-through, not just the stops. A fix is proven only when it holds while the page moves — through every scroll offset, not only at the measured ones — and on a render with real data behind it. A PASS with a named in-motion failure carries its follow-on in the same pass; the follow-on is part of the verdict, not an afterthought.

## Owed from this dictation

The gear-fixing follow-on round (cure the fixing itself, not the measured positions); the captain's eye on a data-loaded render (conversation line, first-paint numbers 400/1,735/50, world-board stats routing, X-vs-WEEK pill). Both awaiting Shawn's word.

**At rest is a sample. In motion is the proof.**
