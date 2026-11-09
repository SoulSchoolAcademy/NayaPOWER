# Dead Buttons Are Worse Than No Button

SN-2425 · DESIGN / FULFILLMENT

**Created:** 2026-11-09 01:38Z

**Source:** the v54 finale-seat verification (daily log 2026-11-09.md). Corrects the captain's earlier report — recorded here, not hidden.

## Hook

All 36 popups SHOW a View app button — and 28 of them are DEAD (click does nothing, iframe stays about:blank). Worse than no button.

## Nutshell

**CORRECTION to the captain's earlier reports:** the captain told Shawn 28 rows have NO View app button. The v54 verifier found the truth is worse — **all 36 popups SHOW a button, and 28 of them are DEAD: click does nothing, the iframe stays about:blank.** A button that promises and does nothing is worse than no button at all — it teaches the visitor that the page lies. The defects-fix seat was dispatched the same pass to **hide the dead buttons (restore the v44 rule: a row with no complete app gets NO View button)** + fix the finale "risk" clip + the Free note below the fold. The fix appears landed as v56 (~01:47Z, observed via artifact.status by the wiring seat) — its edit being the defects fix — but the defects seat's own handoff and independent verification had NOT been received as of 01:48Z, so v56's presence is observed, its verification is still pending; do not claim it verified done. The fulfillment audit (SN-2426) then proved which 10 of the 28 actually exist.

## Human

As logged 01:38Z: "CORRECTION TO MY EARLIER REPORTS: I told Shawn 28 rows have NO View app button — the verifier found all 36 popups SHOW a button and 28 of them are DEAD (click does nothing, iframe stays about:blank). Worse than no button. Defects-fix seat dispatched to hide the dead buttons (restore v44 rule) + fix the finale 'risk' clip + Free note below fold. Freeze now waits for the defects fix, not v55."

## Child

Imagine a door with a shiny handle that doesn't open — you pull and pull, and nothing happens. That's worse than a wall with no door at all, because the wall never promised you anything. A button that does nothing is a door that doesn't open. Take the handle off until the door is real.

## Grandma

Dear, we told him some rows had no button at all — but the truth was worse: the buttons were there, all of them, and most of them did nothing when you pressed them. A button that promises and doesn't deliver is worse than no button, so we're hiding them until the apps behind them are real. Honesty first, always.

## Naya

Three lessons, one correction. First, the design law: a control that doesn't work is a broken promise, and a broken promise costs more trust than an honest absence — the v44 rule (no View button where no app exists) was right, and its violation was the defect. Second, the record law: the captain corrected his own report in the same pass he learned it was wrong, in plain words, to Shawn — the record must tell the truth, and a correction is a strength, not a shame. Third, the verification law: the difference between "no button" and "dead button" is exactly the kind of thing a source check misses and a live tap catches — the verifier tapped, the earlier checks didn't. After the wiring seat lands, 18 of 36 rows will have working buttons and 18 stay un-buttoned — honest either way.

## What it means

- **CORRECTION: 28 buttons are DEAD, not absent** — all 36 popups show a View app button; 28 do nothing (iframe stays about:blank).
- **Dead is worse than absent** — a control that promises and doesn't deliver breaks trust; an honest absence doesn't.
- **FIX: hide the dead buttons — restore the v44 rule** (a row with no complete app gets NO View button). Dispatched with the finale "risk" clip + Free note below fold.
- **v56 OBSERVED (~01:47Z), verification PENDING** — the defects fix appears landed (artifact.status read by the wiring seat), but the seat's handoff + independent verification had not arrived at 01:48Z. Observed, not verified done.
- **The freeze waits for the defects fix**, not v55 — the frozen version must not carry dead buttons.

## Why it matters

The pricing page's whole promise is "the thing itself, not words about it" — a dead View button is the page breaking its own promise in front of the visitor, at the exact moment it claims to show them the app. It also vindicates the verification standard: only a live tap proves a button works; a source check proves it exists. And it shows the record working as designed: the wrong report was corrected loudly, in the same pass, by the person who made it.

## What changes now

- The defects fix (hide dead buttons) is the gate for the freeze — nothing freezes with dead buttons.
- The wiring seat wires only the 10 audit-verified rows (SN-2426); the other 18 stay un-buttoned until their apps exist.
- Every future button claim is tap-proven, not source-proven.
- The v56 verification is owed — next loop run checks for the defects seat's handoff + independent verification.
