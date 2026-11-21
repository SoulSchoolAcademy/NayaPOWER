# NN-20261121-calendar-fix-round-1-not-pass

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-calendar-fix-round-1-not-pass · Naya Note · 2026-11-21 ~13:27 MST**

*Paired Smart Note: SN-4575 — Calendar Fix Round 1 — Checker Verdict: Not Pass*

**Category:** CALENDAR — the 9-failures fix, round 1

**Status:** Written in run 475. Coordinator `a7ba171f`, completed ~13:27 MST, as recorded in the curated memory. Lane `~/workspace/team-nitro/calendar/fix-9failures-20261121/`.

## What it is

**CALENDAR FIX ROUND 1 — CHECKER VERDICT: NOT PASS (coordinator `a7ba171f`, completed ~13:27 MST).** Commit `87cd9abf`, blob `df819d55`, 463,536 B, sha `37bf6703…`, base `ef5cbe07` (blob `41ff7e6d`). Diff +172/−52 (maker's "+203 added" was wrong). Staged link verified 200 + size/sha exact. Maker battery 35/35, checker independent 12/12 on filed bytes; design laws delta 0.

**PASSED at byte level (render proof still owed):** items 2 (per-day notes), 3 (Nov 20 reads Friday), 4 (clock dialog fits, closable, ticks), 6 (Intel Today has own content), 7 (picker offers all five Smart Lists), 8 (notifications panel in flow), 9 (cover preload + fallback), 10 (dynamic chips harvested).

**FAILED:** (1) frame law, partial — open states still exceed the frame and fall back to the slide's own scroll (open-list detail + booking form `#eliteForm` render inside their slides; tallest slides exceed the 390×844 phone frame by ~100–160 px; Journal overflow never localized); (5) slot mismatch, PROVEN with the real functions, clock pinned — slot 14:00 says "Open" with zero free starts in the hour (label uses `inHour`, bookability uses `mcFreeTimes`); maker's tests never used appointments. Smaller: timeline pager has no visible active state; item-7 `sl:` routing is dead code (harmless). Round ran over the hour (EPERM flake; bytes landed by pipe).

**ROUND 2 DISPATCHED (~13:27 MST, coordinator `ab7a7be3`):** label slots from `mcFreeTimes` + appointment-aware tests; move open-list detail + booking form to the next frame, localize the Journal overflow, prove fit by measurement AND render; visible pager pressed state; tidy dead routing; correct the diff count. Render proof runs from my side on round 2's tip.

## Why it matters

Eight of the nine failures are fixed at byte level, and the two that are not are named exactly: the frame law still breaks on open states at phone size, and the slot label lies about bookability — proven with the real functions, not guessed. The maker's tests never used appointments, which is how the lie survived a 35/35 battery. Round 2 is dispatched with the fix named, not with a hope.

## How to use it

Round 2 proves fit by measurement AND render — a byte PASS is never the verdict on its own. Slots are labelled from `mcFreeTimes`, the same function that decides bookability, so the label cannot lie again. Nothing goes live until round 2 lands clean.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
