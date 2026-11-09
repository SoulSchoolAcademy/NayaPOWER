# The $4,500 Clipped Defect Was a False Positive

SN-2437 · CORRECTION / RECORD

**Created:** 2026-11-09 02:23Z

**Source:** Flush correction 02:13Z, from the mobile-first audit 02:12Z (daily log 2026-11-09.md). A defect cleared from the open lists — do not re-file it.

## Hook

The "$4,500 clipped" defect was never a defect. The visible bandline reads whole.

## Nutshell

The 02:13Z flush correction **CLEARS the "$4,500 clipped" pricing defect as a false positive.** The clipped text the open lists carried is a hidden animation/duplicate node inside the gauge — not visible text. The visible bandline reads whole: "$4 500 of $10 000 — Advancing at $6 000". The evidence is the 02:12Z mobile-first audit, which read the page as a phone user and found the bandline complete. **Do not re-file it as an open defect on that evidence.** The correction matters because a false defect is not harmless: it sends fix seats after a ghost, and it keeps a clean page looking broken in the open lists. The record now says plainly: looked, measured, whole — cleared.

## Human

What the audit found, 02:12Z, and the correction recorded 02:13Z: the "$4,500" that looked clipped is a hidden copy inside the gauge — an animation node the eye never sees. The line a person actually reads says "$4 500 of $10 000 — Advancing at $6 000", whole and unclipped. So the defect is cleared. It was never broken; the list was wrong. Don't file it again.

## Child

Imagine someone says "look, this word is broken!" — but the broken word is on a piece of paper hidden behind the picture, where nobody can see it. The word on the front of the picture is whole and perfect. So there is nothing to fix. We cross it off the list and don't write it down again.

## Grandma

Dear, someone wrote down that the money number was cut off — but it wasn't, love. The cut-off one is a hidden copy tucked away inside the machine, where no eye ever goes. The one you actually see reads beautifully, whole and clear: four thousand five hundred of ten thousand, advancing at six thousand. So we cross it off, and we don't worry about it again.

## Naya

A false positive is a lie the record tells about the page, and the record's law is that it must tell the truth — so the correction is as important as any fix. The audit earned the clearance the right way: it looked at the rendered page as a user, at phone width, and read the actual visible line. The hidden node is a real thing in the code, but a hidden node is not a visible defect, and the open list is a list of visible defects. Naming the clearance in a note is what stops the next seat from "discovering" the same ghost and filing it again.

## What it means

- **The "$4,500 clipped" defect is CLEARED — false positive.** Do not re-file it.
- **The evidence:** a hidden animation/duplicate node inside the gauge; the visible bandline reads whole ("$4 500 of $10 000 — Advancing at $6 000").
- **The method:** the 02:12Z mobile-first audit read the rendered page as a phone user — visible text, not code inspection.

## Why it matters

Open lists are the team's memory of what is broken. A ghost on the list costs real work — a fix seat, a verification, a re-freeze — chasing something no user will ever see, and it makes a clean page look broken to anyone reading the list, including Shawn. Clearing it loudly is what keeps the list honest, and an honest list is what lets the team spend its effort on the real defects (the true-360 overflow, the tap targets, the first screen).

## What changes now

- The "$4,500 clipped" item comes off every open-defect list it still sits on; if it reappears, it needs new visible evidence, not the old report.
- The hidden animation node stays as it is — it is not a defect, and removing it is not a fix.
- The mobile-first audit's other findings stand as real defects (true-360 overflow, first-screen, tap targets) — the clearance touches only this one item.
