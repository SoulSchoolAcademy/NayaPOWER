# SN-4575 — Calendar Fix Round 1 — Checker Verdict: Not Pass

**Category:** CALENDAR — the 9-failures fix, round 1 — 2026-11-21 ~13:27 MST

*Paired Naya Note: NN-20261121-calendar-fix-round-1-not-pass — the verbatim record of the verdict.*

**Filed:** SN-4575 — Intelligence Loop run 475, 2026-11-21. Coordinator `a7ba171f`, completed ~13:27 MST, as recorded in the curated memory. Commit `87cd9abf`, blob `df819d55`, 463,536 B, sha `37bf6703…`. Lane: `~/workspace/team-nitro/calendar/fix-9failures-20261121/`.

## In a Nutshell

Eight of the nine calendar failures are fixed at byte level; the checker verdict is still NOT PASS. The two that failed: (1) the frame law, partial — open states still exceed the 390×844 phone frame by ~100–160 px and fall back to the slide's own scroll; (5) the slot mismatch, proven with the real functions — slot 14:00 says "Open" with zero free starts in the hour, because the label uses `inHour` while bookability uses `mcFreeTimes`, and the maker's tests never used appointments. Round 2 is dispatched (coordinator `ab7a7be3`): label slots from `mcFreeTimes`, move open states to the next frame, prove fit by measurement AND render.

## The Lesson

**CALENDAR FIX ROUND 1 — CHECKER VERDICT: NOT PASS (coordinator `a7ba171f`, completed ~13:27 MST).** Commit `87cd9abf`, blob `df819d55`, 463,536 B, sha `37bf6703…`, base `ef5cbe07` (blob `41ff7e6d`). Diff +172/−52 (maker's "+203 added" was wrong). Staged link verified 200 + size/sha exact. Maker battery 35/35, checker independent 12/12 on filed bytes; design laws delta 0.

**PASSED AT BYTE LEVEL (render proof still owed):** items 2 (per-day notes), 3 (Nov 20 reads Friday), 4 (clock dialog fits, closable, ticks), 6 (Intel Today has own content), 7 (picker offers all five Smart Lists), 8 (notifications panel in flow), 9 (cover preload + fallback), 10 (dynamic chips harvested).

**FAILED — (1) FRAME LAW, PARTIAL.** Open states still exceed the frame and fall back to the slide's own scroll (open-list detail + booking form `#eliteForm` render inside their slides; tallest slides exceed the 390×844 phone frame by ~100–160 px; Journal overflow never localized).

**FAILED — (5) SLOT MISMATCH, PROVEN WITH THE REAL FUNCTIONS, CLOCK PINNED.** Slot 14:00 says "Open" with zero free starts in the hour (label uses `inHour`, bookability uses `mcFreeTimes`); maker's tests never used appointments. Smaller: timeline pager has no visible active state; item-7 `sl:` routing is dead code (harmless). Round ran over the hour (EPERM flake; bytes landed by pipe).

**ROUND 2 DISPATCHED (~13:27 MST, coordinator `ab7a7be3`):** label slots from `mcFreeTimes` + appointment-aware tests; move open-list detail + booking form to the next frame, localize the Journal overflow, prove fit by measurement AND render; visible pager pressed state; tidy dead routing; correct the diff count. Render proof runs from my side on round 2's tip.

## Why It Matters

Eight of nine fixed is not done — the verdict is NOT PASS because the two that failed are the ones a citizen feels first: a frame that scrolls inside itself at phone size, and a slot that says "Open" when nothing is free. The maker's 35/35 battery passed because its tests never used appointments; the checker proved the lie with the real functions. That is the lesson: a test battery that never exercises the function it claims to prove is not a battery. Round 2 is dispatched with the fix named — label from the same function that decides bookability, so the label cannot lie again — and with fit proven by measurement AND render, never by bytes alone.

## How to Use It

Slots are labelled from `mcFreeTimes`, the same function that decides bookability. Open states move to the next frame; nothing scrolls inside itself. Fit is proven by measurement AND render. Nothing goes live until round 2 lands clean.

## Owed from This Dictation

- Round 2 (coordinator `ab7a7be3`): label slots from `mcFreeTimes` + appointment-aware tests; open states to the next frame; Journal overflow localized; fit proven by measurement AND render; pager pressed state; dead routing tidied; diff count corrected.
- Render proof on round 2's tip.
