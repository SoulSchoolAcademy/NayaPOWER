# The Real Fix — The Bug That Taught the Rule

SN-2228 · DESIGN / THE ULTIMATE NUMBER — THE REAL FIX

**Created:** 2026-11-07 21:23Z

> "When a fix doesn't work, the cause is not the fix — it is the state the fix reads."

## Hook

The growing demo stalled twice at "1" plus four blank tiles. The first fix did not work. The real cause was not the fix — it was the state the fix read.

## Nutshell

The growing demo added tiles but stalled at the last stage — frozen "1" plus four blank tiles, never reaching 10,725. The first fix (rebuild every strip for the new target) did NOT work — the re-check found the identical stall. The real cause: `buildReel` read the strip length from the reel's STALE `data-max` attribute (set at creation for 725), so the "rebuilt" strips were still the old lengths — the count ran past the strip end, leaving no digit under the window (blank), while the colour logic advanced correctly. The real fix: the strip length is now computed from the target (`max = Math.floor(target / div)`, and `data-max` is updated). Screen check #3 (21:00Z) proved it on a real screen: the growing demo reaches 10,725 in every run, five tiles, all digits showing, none blank.

## Human

The screen check caught what the code review missed — twice. The first fix looked right and was wrong. The real cause was the stale state the fix read, not the fix itself. That is the lesson: check what the code reads, not just what it does.

## Child

The toy was broken because it was reading an old instruction instead of the new one. We fixed it by making it read the new instruction every time. Now it works.

## Grandma

It looked fixed, but it wasn't — because it was still using the old numbers underneath. Once we made it use the new numbers, it worked perfectly.

## Naya

A fix that doesn't work is not a failure — it is information. It tells you the cause is deeper than the fix. The discipline is: don't fix the fix. Find what the fix reads, and fix that. And prove it on a real screen, because the screen is the only witness that cannot be argued with.

## What it means

- Bug: `buildReel` read strip length from the stale `data-max` attribute.
- Fix: strip length computed from the target; `data-max` updated. Filed as blob cf4c79de.
- Proof: screen check #3, 21:00Z — 10,725 in every run, three runs, two after reload.

## Why it matters

Every future bug will try the same trick — looking fixed while reading stale state. This note is the vaccine: when a fix doesn't work, check what the fix reads.

## What changes now

- The fix is in the build record (HOW-THE-NUMBER-WAS-BUILT.md) and in this note, so the lesson compounds instead of repeating.
- Screen checks are the proof. A claim is not proof.
