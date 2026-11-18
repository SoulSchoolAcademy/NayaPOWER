# Find the Cause First, Then Retry

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-find-the-cause-first-then-retry-vm-browsers.md · Naya Note · 2026-11-18 03:16–03:17Z**

**Category:** Operations — diagnosis before retry

## What it is

Shawn, 2026-11-18 03:16Z, tapped "Find the cause first, then retry" on the Dashboard card. The diagnosis seat (625d38db) found the cause, COMPLETE 03:17:59Z — confirmed, NOT new: the cell's filter on writable file-backed shared memory mappings, the same 2026-11-11 cause, its scope now widened (at 02:32Z only memfd MAP_SHARED failed; from ~03:07Z all three file-backed paths fail). Resources ruled out.

- **THE TIMELINE:** dead 23:32Z Nov 17 → alive 00:02Z, 00:46Z, ~02:17Z → dead ~02:27Z → alive 03:02:05Z (all 8 mappings OK, Firefox PNG 5,763 B) → alive ~03:03Z → dead ~03:04Z (alive window lasted ~2 min) → dead through 03:17:27Z, re-confirmed DEAD 03:22Z.
- **THE RETRY CONDITION (green = ALL):** (a) mmapprobe all 8 mappings OK; (b) a real browser launch — Firefox or Chromium headless on about:blank, exit 0, real PNG >0 bytes; (c) the SAME result on a SECOND probe at least 5 minutes after the first — a single alive probe is NOT green; (d) the eye re-tests immediately before walking and stops if it traps. No VM eye dispatch on a single alive probe; no retries into a dead browser. Cloud eyes continue unaffected.

## Why it matters

He said it twice in one night — first on the deploy, then on the Dashboard card — and both times the discipline is the same: do not drive into the broken road again, find out why it is broken first. The timeline is the proof that a single green probe means nothing — alive at 03:02Z, dead again by 03:04Z, a two-minute window that would have swallowed any eye dispatched on it. Cause-first is not slowness; it is the thing that stops seven identical failures from becoming eight.

## How to use it

No VM eye dispatch until the four-part retry condition holds in full. Every browser-probe result is judged against the timeline, not alone — one alive probe is never green. Cloud eyes carry all walks until the VM condition holds. The state file is updated on every flip, so the tripwire's next dead→alive detection is correct.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3309 — Find the Cause First, Then Retry*
